"""Document provenance and explicit restore-access semantics."""
from pathlib import Path
from types import SimpleNamespace
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.evidence.handlers.pdf_handler import extract as extract_pdf
from agent.evidence.handlers.log_handler import extract as extract_log
from agent.evidence.handlers.common import email_hashes
import hashlib
from agent.flows.restore_risk import RestoreRiskAnalyzer


class Identity:
    primary_user_id = "user_1"
    all_user_ids = {"user_1"}
    all_emails = {"a@example.com"}
    all_email_hashes = set()


def test_retention_register_is_context_not_live_resource(tmp_path):
    from reportlab.pdfgen import canvas
    path = tmp_path / "register.pdf"
    pdf = canvas.Canvas(str(path))
    pdf.drawString(20, 800, "DISPUTED ORDERS AND TAX RECORDS REGISTER")
    pdf.drawString(20, 780, "ORD-123 | user_1 | Retain until 2033")
    pdf.save()
    records, notes = extract_pdf(path, "evidence_x", Identity())
    assert records == []
    assert "retention_register_context_only" in notes


def test_pdf_selected_record_uses_visible_resource_not_page_placeholder(tmp_path):
    from reportlab.pdfgen import canvas
    path=tmp_path/"selected.pdf"
    pdf=canvas.Canvas(str(path))
    pdf.drawString(20,800,"COMPLIANCE JOURNAL - SIGNED RECORD EXTRACT")
    pdf.drawString(20,780,"Record Event reference audit_record_1")
    pdf.drawString(20,760,"Detail subject reference user_1")
    pdf.save()
    records,_=extract_pdf(path,"ev",Identity())
    assert [(r.system_id,r.resource_id,r.user_ref) for r in records]==[("security_service","audit_record_1","user_1")]


def test_pdf_multiple_resources_without_row_join_does_not_cross_product(tmp_path):
    from reportlab.pdfgen import canvas
    path=tmp_path/"ambiguous.pdf"
    pdf=canvas.Canvas(str(path))
    pdf.drawString(20,800,"Resource list")
    pdf.drawString(20,780,"account_1 account_2")
    pdf.drawString(20,760,"user_1")
    pdf.save()
    assert extract_pdf(path,"ev",Identity())[0]==[]


def _check(details="Restore-access check confirmed that archive can still be restored.", **kwargs):
    row = {"activity_id": "check", "event_time": "2026-02-10T00:00:00Z",
           "event_type": "CHECK_RESTORE_ACCESS", "source_system": "deletion_worker",
           "target_system": "backup_service", "resource_id": "backup_1",
           "target_user_id": "user_1", "details": details}
    row.update(kwargs)
    return row


def _evidence(user="user_1"):
    return [SimpleNamespace(file_id="ev_1", records=[SimpleNamespace(resource_id="backup_1", user_ref=user)])]


def test_affirmative_restore_check_with_exact_owner_is_risk():
    risks = RestoreRiskAnalyzer.build_risks(Identity(), _evidence(), [], [_check()], "2026-02-11T00:00:00Z")
    assert len(risks) == 1 and risks[0].is_risk_at_audit
    assert risks[0].evidence_id == "ev_1"


def test_restore_check_without_owner_does_not_cross_users():
    assert not RestoreRiskAnalyzer.build_risks(Identity(), _evidence("user_2"), [], [_check()], "2026-02-11T00:00:00Z")


def test_restore_check_without_affirmative_result_is_not_risk():
    assert not RestoreRiskAnalyzer.build_risks(Identity(), _evidence(), [], [_check("Restore access unknown")], "2026-02-11T00:00:00Z")


def test_later_restore_block_overrides_affirmative_check():
    block = {"event_time": "2026-02-10T12:00:00Z", "event_type": "BLOCK_RESTORE", "resource_id": "backup_1"}
    risks = RestoreRiskAnalyzer.build_risks(Identity(), _evidence(), [], [_check(), block], "2026-02-11T00:00:00Z")
    assert len(risks) == 1 and risks[0].is_blocked and not risks[0].is_risk_at_audit


def test_trace_lookup_is_context_only_but_completed_resource_is_owned(tmp_path):
    path=tmp_path/"events.log"
    path.write_text("2026-02-01T00:00:00Z service=account_service trace_id=tr-1 event=profile_lookup_started lookup_key=a@example.com\n"
                    "2026-02-01T00:00:01Z service=account_service trace_id=tr-1 resource_id=account_1 event=profile_lookup_completed rows=0 http_status=404\n")
    records, post=extract_log(path,"evidence_x",Identity(),"2026-02-02T00:00:00Z")
    assert post==[]
    assert [(r.resource_id,r.state_at_evidence) for r in records]==[("account_1","ABSENT")]


def test_unresolved_trace_request_does_not_create_resource(tmp_path):
    path=tmp_path/"events.log"
    path.write_text("2026-02-01T00:00:00Z service=account_service trace_id=tr-1 event=profile_lookup_started lookup_key=a@example.com\n")
    records,_=extract_log(path,"evidence_x",Identity(),"2026-02-02T00:00:00Z")
    assert records==[]


def test_historical_email_hash_exactly_owns_structured_log_resource(tmp_path):
    identity=Identity()
    identity.all_emails={"a@example.com","old@example.com"}
    digest=hashlib.sha256(b"old@example.com").hexdigest()
    path=tmp_path/"events.log"
    path.write_text(f"2026-02-01T00:00:00Z service=analytics_platform trace_id=tr-1 resource_id=analytics_1 event=contact_lookup_completed rows=1 correlation_key=\"{digest}\"\n")
    records,_=extract_log(path,"evidence_x",identity,"2026-02-02T00:00:00Z")
    assert len(records)==1 and records[0].resource_id=="analytics_1"
    assert any(hit.value_kind=="email_hash" and hit.value==digest for hit in records[0].pii_hits)
    assert digest in email_hashes(identity)


def test_same_second_completed_404_overrides_started_lookup(tmp_path):
    from agent.evidence.ir import ExtractedEvidence
    from agent.state.reconstructor import reconstruct
    from datetime import datetime,timezone
    path=tmp_path/"readback.log"
    path.write_text("2026-02-01T00:00:00Z service=account_service trace_id=tr-1 event=profile_lookup_started resource_id=account_1 lookup_key=a@example.com\n"
                    "2026-02-01T00:00:00Z service=account_service trace_id=tr-1 event=profile_lookup_completed resource_id=account_1 rows=0 http_status=404\n")
    records,_=extract_log(path,"ev",Identity(),"2026-02-02T00:00:00Z")
    evidence=[ExtractedEvidence("ev",str(path),"hash",records,"regex-log",datetime.now(timezone.utc))]
    facts=reconstruct(Identity(),evidence,[],"2026-02-02T00:00:00Z")
    assert len(facts)==1 and facts[0].state_at_audit=="ABSENT"


def test_missing_deletion_marker_means_replica_row_survives(tmp_path):
    path=tmp_path/"replica.log"
    path.write_text("2026-02-01T00:00:00Z service=support_replica trace_id=tr-1 "
                    "event=contact_query_started lookup_key=a@example.com source=legacy_contact_index\n"
                    "2026-02-01T00:00:01Z service=support_replica trace_id=tr-1 "
                    "event=contact_query_completed resource_id=support_1 rows=1\n"
                    "2026-02-01T00:00:02Z service=support_replica trace_id=tr-1 "
                    "event=deletion_marker_check resource_id=support_1 marker_found=false\n")
    records,_=extract_log(path,"ev",Identity(),"2026-02-02T00:00:00Z")
    assert len(records)==2
    assert all(r.state_at_evidence=="PRESENT" for r in records)
    assert all(r.raw_row["trace_source"]=="legacy_contact_index" for r in records)


def test_attachment_document_kind_is_not_support_message(tmp_path):
    from reportlab.pdfgen import canvas
    path=tmp_path/"customer_attachment.pdf"
    pdf=canvas.Canvas(str(path))
    pdf.drawString(20,800,"Support reference support_1")
    pdf.drawString(20,780,"Customer a@example.com")
    pdf.save()
    records,_=extract_pdf(path,"ev",Identity())
    assert len(records)==1 and records[0].raw_row["document_kind"]=="support_attachment"


def test_jsonl_trace_joins_exact_completed_resource_but_not_started_event(tmp_path):
    path=tmp_path/"structured.log"
    path.write_text('2026-02-01T00:00:00Z {"service":"account_service","trace_id":"tr-1",'
                    '"event":"profile_lookup_started","lookup_key":"a@example.com"}\n'
                    '2026-02-01T00:00:01Z {"service":"account_service","trace_id":"tr-1",'
                    '"resource_id":"account_1","event":"profile_lookup_completed",'
                    '"rows":"0","http_status":"404"}\n'
                    '2026-02-01T00:00:02Z {"service":"account_service","trace_id":"tr-2",'
                    '"resource_id":"account_2","rows":"1"}\n')
    records,_=extract_log(path,"ev",Identity(),"2026-02-02T00:00:00Z")
    assert [(r.resource_id,r.state_at_evidence,r.user_ref) for r in records]==[
        ("account_1","ABSENT","a@example.com")]
