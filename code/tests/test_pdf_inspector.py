from pathlib import Path
from orchestrator.pdf_inspector import inspect_pdf

DOCS = Path(__file__).resolve().parents[2] / "dataset/evidence/documents"


def test_pdf_page_count():
    assert inspect_pdf(DOCS / "account_history_report_20260718.pdf")["page_count"] == 2


def test_pdf_text_and_tables():
    pages = inspect_pdf(DOCS / "security_retention_extract.pdf")["pages"]
    assert pages[0]["text_length"] > 50 and pages[0]["table_count"] >= 1


def test_pdf_scanned_flag_requires_low_text(monkeypatch):
    import sys
    from types import SimpleNamespace
    class FakePDF:
        pages = [SimpleNamespace(extract_text=lambda: "", extract_tables=lambda: [])]
        def __enter__(self): return self
        def __exit__(self, *args): return False
    monkeypatch.setitem(sys.modules, "pdfplumber", SimpleNamespace(open=lambda _: FakePDF()))
    info = inspect_pdf("fake.pdf")
    assert info["pages"][0]["scanned"] and "scanned, needs Vision" in info["notes"]


def test_scanned_pdf_page_is_rendered_and_sent_to_real_image_route(monkeypatch):
    from datetime import datetime,timezone
    from types import SimpleNamespace as N
    from agent.evidence.handlers import pdf_handler,image_handler
    from agent.evidence.ir import ExtractedEvidence,PIIHit,RecordState
    from orchestrator import pdf_inspector
    document=DOCS/"security_retention_extract.pdf"
    monkeypatch.setattr(pdf_inspector,"inspect_pdf",lambda _: {"pages":[{"page":1,"scanned":True,"text":"","tables":[]}],"notes":["scanned, needs Vision"]})
    seen=[]
    def fake_image_extract(path,file_id,identities,audit_at,llm_client,case_id):
        assert path.is_file() and path.suffix==".png" and path.stat().st_size>100
        seen.append(path)
        row=RecordState("security_service","audit_record_7","user_1","PRESENT",
                        [PIIHit("owner","user_id","user_1",source_page=1)])
        return ExtractedEvidence(file_id,str(path),"hash",[row],"ocr_plus_vision",datetime.now(timezone.utc))
    monkeypatch.setattr(image_handler,"extract",fake_image_extract)
    identity=N(all_user_ids={"user_1"},all_emails=set())
    rows,notes=pdf_handler.extract(document,"ev",identity,llm_client=N(enabled=True),case_id="case_x")
    assert len(seen)==1 and len(rows)==1 and rows[0].raw_row["pdf_page"]==1
    assert "scanned_page_1_routed_to_ocr_vision" in notes and "scanned, needs Vision" not in notes
