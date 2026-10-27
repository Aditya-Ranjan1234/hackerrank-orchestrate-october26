"""Explicit readback schemas use the subject reference and row's own result/time."""

import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from agent.evidence.handlers.json_handler import extract
from orchestrator.json_owner_coverage import inspect_json


IDENTITY = SimpleNamespace(primary_user_id="user_1", all_user_ids={"user_1"},
                           all_emails={"person@example.com"}, all_email_hashes={"hash_1"})


def _parse(tmp_path, records):
    path = tmp_path / "readback.json"
    path.write_text(json.dumps({"exported_at": "2026-10-01T00:00:00Z", "records": records}),
                    encoding="utf-8")
    return extract(path, "evidence_readback", IDENTITY)


def test_email_subject_reference_identifies_404_without_claiming_stored_pii(tmp_path):
    records = _parse(tmp_path, [{"recorded_at": "2026-09-01T00:00:00Z",
                                 "system": "account_service", "resource_id": "account_42",
                                 "subject_reference": "PERSON@EXAMPLE.COM", "result": "NOT_FOUND"}])
    assert len(records) == 1
    assert (records[0].system_id, records[0].resource_id, records[0].user_ref,
            records[0].state_at_evidence) == (
                "account_service", "account_42", "person@example.com", "ABSENT")
    assert records[0].evidence_timestamp.isoformat() == "2026-09-01T00:00:00+00:00"
    assert records[0].pii_hits == []


def test_readback_result_and_row_timestamp_override_export_metadata(tmp_path):
    records = _parse(tmp_path, [
        {"recorded_at": "2026-08-01T00:00:00Z", "system": "account_service",
         "resource_id": "account_42", "subject_reference": "person@example.com", "result": "FOUND"},
        {"recorded_at": "2026-08-02T00:00:00Z", "system": "analytics_platform",
         "resource_id": "analytics_42", "subject_reference": "person@example.com",
         "result": "ANONYMIZED"},
        {"recorded_at": "2026-08-03T00:00:00Z", "system": "support_platform",
         "resource_id": "support_42", "subject_reference": "person@example.com",
         "result": "REDACTED"},
    ])
    assert [(row.state_at_evidence, row.evidence_timestamp.day) for row in records] == [
        ("PRESENT", 1), ("ANONYMIZED", 2), ("REDACTED", 3)]
    assert all(row.pii_hits == [] for row in records)


def test_hash_in_owner_reference_resolves_exactly(tmp_path):
    records = _parse(tmp_path, [{"recorded_at": "2026-08-01T00:00:00Z",
                                 "system": "search_service", "resource_id": "search_42",
                                 "subject_reference": "hash_1", "result": "FOUND"}])
    assert len(records) == 1
    assert records[0].user_ref == "user_1"
    assert records[0].pii_hits == []


def test_later_recorded_row_stays_post_audit_despite_older_export_time(tmp_path):
    path = tmp_path / "readback.json"
    path.write_text(json.dumps({"exported_at": "2026-08-12T09:00:00Z", "records": [
        {"recorded_at": "2026-08-14T09:00:00Z", "system": "account_service",
         "resource_id": "account_42", "subject_reference": "person@example.com",
         "result": "FOUND"}]}), encoding="utf-8")
    before, after = extract(path, "evidence_readback", IDENTITY,
                            datetime(2026, 8, 13, tzinfo=timezone.utc), include_post_audit=True)
    assert before == []
    assert [(row.resource_id, row.state_at_evidence) for row in after] == [
        ("account_42", "PRESENT")]


def test_all_direct_owner_json_rows_are_extracted():
    root = Path(__file__).resolve().parents[2]
    coverage = inspect_json(root)
    assert coverage["file_count"] == 28
    assert coverage["direct_owner_rows"] > 0
    assert coverage["missing"] == []
    assert coverage["conflicting"] == []
