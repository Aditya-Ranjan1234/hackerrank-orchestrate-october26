from pathlib import Path
from types import SimpleNamespace
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.evidence.ir import RecordState
from agent.llm.semantic_resolver import SemanticResolver
from orchestrator.pipeline import _contemporaneous_file, _evidence_confirms_verdict


AUDIT = "2026-09-15T12:00:00Z"


def candidate(file_id, captured, observed):
    return {"file_id": file_id, "captured_at": captured,
            "timestamp": observed, "state": "PRESENT",
            "resource_id": "account_88"}


class FakeModel:
    def __init__(self, preferred):
        self.preferred = preferred

    def call(self, prompt, purpose, case_id=None):
        return '{"primary_file_id":"' + self.preferred + '","confidence":1}'


def test_contemporaneous_source_outweighs_retrospective_snapshot():
    sources = [
        candidate("old_capture", "2026-09-15T11:45:00Z", "2026-09-15T11:30:00Z"),
        candidate("later_bundle", "2026-09-17T12:00:00Z", AUDIT),
    ]
    assert _contemporaneous_file(sources, AUDIT) == "old_capture"
    resolver = SemanticResolver(FakeModel("later_bundle"))
    chosen = resolver.select_primary_evidence_file(
        sources, SimpleNamespace(case_id="synthetic", audit_at=AUDIT),
        SimpleNamespace(primary_user_id="user_alpha"))
    assert chosen == "old_capture"


def test_retrospective_only_source_remains_available():
    sources = [candidate("later_bundle", "2026-09-17T12:00:00Z",
                         "2026-09-15T11:00:00Z")]
    assert _contemporaneous_file(sources, AUDIT) is None
    resolver = SemanticResolver(FakeModel("later_bundle"))
    chosen = resolver.select_primary_evidence_file(
        sources, SimpleNamespace(case_id="synthetic", audit_at=AUDIT),
        SimpleNamespace(primary_user_id="user_alpha"))
    assert chosen == "later_bundle"


def test_backup_blocked_is_supported_by_explicit_restore_access():
    record = RecordState("backup_service", "backup_88", "user_alpha",
                         "PRESENT", [], raw_row={"restore_allowed": False})
    verdict = SimpleNamespace(target_kind="restore_risk", current_state="BLOCKED")
    assert _evidence_confirms_verdict(record, verdict)
    record.raw_row = {"restore_allowed": True}
    assert not _evidence_confirms_verdict(record, verdict)


def test_connector_disabled_is_supported_by_explicit_enabled_flag():
    record = RecordState("integration_service", "data_flow_88", "user_alpha",
                         "PRESENT", [], raw_row={"enabled": False})
    verdict = SimpleNamespace(target_kind="flow", current_state="INACTIVE")
    assert _evidence_confirms_verdict(record, verdict)
    record.raw_row = {"enabled": True}
    assert not _evidence_confirms_verdict(record, verdict)
