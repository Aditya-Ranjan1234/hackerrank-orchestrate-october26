"""Readback result and category values must survive extraction into policy."""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from agent.evidence.handlers.json_handler import extract
from agent.evidence.ir import ExtractedEvidence
from agent.policy.category_map import RECORD_TYPE_TO_CATEGORY
from agent.policy.engine import PolicyEngine
from agent.policy.rules_loader import load_rules
from agent.state.reconstructor import reconstruct


ROOT = Path(__file__).resolve().parents[2]
IDENTITY = SimpleNamespace(primary_user_id="user_1", all_user_ids={"user_1"},
                           all_emails={"person@example.com"}, all_email_hashes=set())
AUDIT = datetime(2026, 9, 2, tzinfo=timezone.utc)


def _facts_and_verdicts(tmp_path, rows):
    path = tmp_path / "source.json"
    path.write_text(json.dumps({"exported_at": "2026-09-03T00:00:00Z", "records": rows}),
                    encoding="utf-8")
    records = extract(path, "evidence_source", IDENTITY, AUDIT)
    item = ExtractedEvidence("evidence_source", str(path), "hash", records, "json", AUDIT)
    facts = reconstruct(IDENTITY, [item], [], AUDIT)
    verdicts = PolicyEngine(load_rules(ROOT / "dataset/deletion_rules.csv")).apply(
        facts, [], [], AUDIT, AUDIT)
    return facts, verdicts


def test_explicit_disabled_and_blocked_readbacks_are_compliant(tmp_path):
    rows = [
        {"recorded_at": "2026-09-01T00:00:00Z", "system": "integration_service",
         "resource_id": "data_flow_42", "record_type": "DATA_FLOW",
         "subject_reference": "person@example.com", "result": "DISABLED"},
        {"recorded_at": "2026-09-01T00:00:00Z", "system": "backup_service",
         "resource_id": "backup_42", "record_type": "BACKUP_ARCHIVE",
         "subject_reference": "person@example.com", "result": "BLOCKED"},
    ]
    facts, verdicts = _facts_and_verdicts(tmp_path, rows)
    by_resource = {fact.resource_id: fact for fact in facts}
    assert "connector_disabled_by_evidence" in by_resource["data_flow_42"].notes
    assert "restore_access_blocked_by_evidence" in by_resource["backup_42"].notes
    assert {(v.resource_id, v.target_kind, v.is_in_compliance) for v in verdicts} == {
        ("data_flow_42", "flow", True), ("backup_42", "restore_risk", True)}


def test_explicit_active_readbacks_create_flow_and_restore_obligations(tmp_path):
    rows = [
        {"recorded_at": "2026-09-01T00:00:00Z", "system": "integration_service",
         "resource_id": "data_flow_42", "record_type": "DATA_FLOW",
         "subject_reference": "person@example.com", "result": "ACTIVE"},
        {"recorded_at": "2026-09-01T00:00:00Z", "system": "backup_service",
         "resource_id": "backup_42", "record_type": "BACKUP_ARCHIVE",
         "subject_reference": "person@example.com", "result": "ACTIVE"},
    ]
    _, verdicts = _facts_and_verdicts(tmp_path, rows)
    assert {(v.resource_id, v.target_kind, v.is_in_compliance) for v in verdicts} == {
        ("data_flow_42", "flow", False), ("backup_42", "restore_risk", False)}


def test_explicit_legal_hold_category_overrides_unknown_system_default(tmp_path):
    _, verdicts = _facts_and_verdicts(tmp_path, [
        {"recorded_at": "2026-09-01T00:00:00Z", "system": "legal_service",
         "resource_id": "hold_42", "record_type": "LEGAL_HOLD_RECORD",
         "subject_reference": "person@example.com", "result": "FOUND"}])
    assert len(verdicts) == 1
    assert verdicts[0].required_action == "RETAIN"
    assert verdicts[0].is_in_compliance is True


def test_readback_category_map_covers_every_supplied_rule():
    with (ROOT / "dataset/deletion_rules.csv").open(encoding="utf-8-sig", newline="") as stream:
        categories = {row["data_category"] for row in csv.DictReader(stream)}
    assert categories == RECORD_TYPE_TO_CATEGORY.keys()
