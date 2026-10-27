from datetime import datetime,timezone
from agent.evidence.ir import ExtractedEvidence,RecordState
from orchestrator.evidence_time import apply_manifest_capture


def _evidence(timestamp=None):
    at=datetime(2026,9,1,tzinfo=timezone.utc)
    return ExtractedEvidence("ev","file.png","hash",[
        RecordState("account_service","account_1","user_1","PRESENT",[],timestamp,{})
    ],"ocr",at)


def test_post_audit_manifest_capture_is_flow_only_not_resource_state():
    evidence=_evidence()
    apply_manifest_capture(evidence,{"captured_at":"2026-09-02T00:00:00Z"},"2026-09-01T00:00:00Z")
    assert evidence.records==[]
    assert len(evidence.records_post_audit)==1


def test_pre_audit_capture_sets_missing_timestamp():
    evidence=_evidence()
    apply_manifest_capture(evidence,{"captured_at":"2026-08-31T00:00:00Z"},"2026-09-01T00:00:00Z")
    assert evidence.records[0].evidence_timestamp.isoformat()=="2026-08-31T00:00:00+00:00"


def test_intrinsic_record_time_is_not_replaced_by_later_file_capture():
    at=datetime(2026,8,30,tzinfo=timezone.utc)
    evidence=_evidence(at)
    apply_manifest_capture(evidence,{"captured_at":"2026-09-02T00:00:00Z"},"2026-09-01T00:00:00Z")
    assert evidence.records[0].evidence_timestamp==at
