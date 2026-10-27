from pathlib import Path
from orchestrator.document_audit import write_report


def test_document_report_preserves_page_text_and_table_cells(tmp_path):
    from reportlab.pdfgen import canvas
    evidence=tmp_path/"dataset/evidence"
    evidence.mkdir(parents=True)
    pdf=evidence/"sample.pdf"
    draw=canvas.Canvas(str(pdf))
    draw.drawString(20,800,"Owner a@example.com resource account_1")
    draw.save()
    (evidence/"handover.txt").write_text("user_1 | account_1 | FOUND\n",encoding="utf-8")
    (tmp_path/"code/evaluation").mkdir(parents=True)
    report=write_report(tmp_path).read_text(encoding="utf-8")
    assert "Owner a@example.com resource account_1" in report
    assert "user_1 | account_1 | FOUND" in report
