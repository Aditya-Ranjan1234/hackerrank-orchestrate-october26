"""Explicit structured-log booleans must reach state and policy as booleans."""

from datetime import datetime, timezone
from types import SimpleNamespace

from agent.evidence.handlers.log_handler import _fields, extract
from agent.evidence.ir import ExtractedEvidence
from agent.policy.engine import PolicyEngine
from agent.state.reconstructor import reconstruct


IDENTITY = SimpleNamespace(primary_user_id="user_1", all_user_ids={"user_1"},
                           all_emails=set(), all_email_hashes=set())
AUDIT = datetime(2026, 1, 2, tzinfo=timezone.utc)


def _verdict(tmp_path, system, resource, attribute):
    source = tmp_path / "readback.log"
    source.write_text(
        f"2026-01-01T12:00:00Z level=INFO service={system} "
        f"event=read_completed resource_id={resource} "
        f"customer_reference=user_1 {attribute}\n", encoding="utf-8")
    records, post = extract(source, "evidence_readback", IDENTITY, AUDIT)
    assert not post and len(records) == 1
    evidence = ExtractedEvidence("evidence_readback", str(source), "hash",
                                 records, "regex-log", AUDIT)
    facts = reconstruct(IDENTITY, [evidence], [], AUDIT)

    class ForbiddenModel:
        def classify_flow_vs_record(self, *_args, **_kwargs):
            raise AssertionError("explicit source flag must bypass model classification")

    verdicts = PolicyEngine([], ForbiddenModel()).apply(facts, [], [], AUDIT, AUDIT)
    return records[0], facts[0], verdicts[0]


def test_log_boolean_parser_preserves_true_false_and_unknown():
    assert _fields('enabled=false restore_allowed="true"')["enabled"] is False
    assert _fields('enabled=false restore_allowed="true"')["restore_allowed"] is True
    assert _fields(r'enabled=\"false\"')["enabled"] is False
    assert _fields("enabled=maybe")["enabled"] == "maybe"


def test_disabled_log_connector_is_compliant_flow_without_model(tmp_path):
    record, fact, verdict = _verdict(tmp_path, "integration_service",
                                     "data_flow_42", "enabled=false")
    assert record.raw_row["enabled"] is False
    assert "connector_disabled_by_evidence" in fact.notes
    assert (verdict.target_kind, verdict.current_state,
            verdict.is_in_compliance) == ("flow", "INACTIVE", True)


def test_enabled_log_connector_is_active_flow_without_model(tmp_path):
    record, fact, verdict = _verdict(tmp_path, "integration_service",
                                     "data_flow_43", 'enabled="true"')
    assert record.raw_row["enabled"] is True
    assert "connector_enabled_by_evidence" in fact.notes
    assert (verdict.target_kind, verdict.current_state,
            verdict.is_in_compliance) == ("flow", "ACTIVE", False)


def test_blocked_log_restore_is_compliant_without_model(tmp_path):
    record, fact, verdict = _verdict(tmp_path, "backup_service",
                                     "backup_42", "restore_allowed=false")
    assert record.raw_row["restore_allowed"] is False
    assert "restore_access_blocked_by_evidence" in fact.notes
    assert (verdict.target_kind, verdict.current_state,
            verdict.is_in_compliance) == ("restore_risk", "BLOCKED", True)


def test_allowed_log_restore_is_risky_without_model(tmp_path):
    record, fact, verdict = _verdict(tmp_path, "backup_service",
                                     "backup_43", 'restore_allowed="true"')
    assert record.raw_row["restore_allowed"] is True
    assert "restore_access_allowed_by_evidence" in fact.notes
    assert (verdict.target_kind, verdict.current_state,
            verdict.is_in_compliance) == ("restore_risk", "RISKY", False)
