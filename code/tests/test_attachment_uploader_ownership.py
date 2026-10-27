"""Persisted ticket attachment uploaders and their deletion rule."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.evidence.handlers.json_handler import extract as json_extract
from agent.evidence.handlers.sql_handler import extract as sql_extract
from agent.evidence.ir import ExtractedEvidence
from agent.state.reconstructor import reconstruct
from agent.policy.engine import PolicyEngine


ROOT = Path(__file__).resolve().parents[2]
IDENTITY = SimpleNamespace(primary_user_id="user_1", all_user_ids={"user_1"},
                           all_emails={"one@example.test"})


def attachment(collection="ticket_attachments", storage="ticket_attachment"):
    return {"snapshots": [{"captured_at": "2026-05-20T00:00:00Z",
                           "data_store": "support_platform", "collection": collection,
                           "records": [{"resource_id": "support_1", "uploaded_by": "one@example.test",
                                        "file_name": "receipt.pdf", "storage_class": storage}]}]}


def test_json_ticket_attachment_has_uploader_owner_and_delete_rule(tmp_path):
    path = tmp_path / "snapshot.json"
    path.write_text(json.dumps(attachment()), encoding="utf-8")
    records = json_extract(path, "evidence_fixture", IDENTITY)
    assert [(r.resource_id, r.user_ref) for r in records] == [("support_1", "one@example.test")]
    ev = ExtractedEvidence("evidence_fixture", str(path), "hash", records,
                           "json", datetime.now(timezone.utc))
    facts = reconstruct(IDENTITY, [ev], [], "2026-06-01T00:00:00Z")
    verdict = PolicyEngine.from_csv(ROOT / "dataset/deletion_rules.csv").apply(
        facts, requested_at="2026-05-01T00:00:00Z", audit_at="2026-06-01T00:00:00Z")[0]
    assert verdict.required_action == "DELETE_RECORD"
    assert verdict.winning_rule_id == "rule_06"


def test_json_unrelated_uploaded_by_field_does_not_establish_owner(tmp_path):
    path = tmp_path / "snapshot.json"
    path.write_text(json.dumps(attachment(collection="ticket_messages")), encoding="utf-8")
    assert json_extract(path, "evidence_fixture", IDENTITY) == []
    path.write_text(json.dumps(attachment(storage="internal_document")), encoding="utf-8")
    assert json_extract(path, "evidence_fixture", IDENTITY) == []


def sql_fixture(collection="ticket_attachments", storage="ticket_attachment"):
    row = json.dumps({"resource_id": "support_1", "uploaded_by": "one@example.test",
                      "file_name": "receipt.pdf", "storage_class": storage})
    return ("CREATE TABLE customer_data_primary (resource_id TEXT, origin_system TEXT, "
            "collection_name TEXT, record_json TEXT, updated_at TEXT); "
            "INSERT INTO customer_data_primary VALUES "
            f"('support_1','support_platform','{collection}','{row}',"
            "'2026-05-20T00:00:00Z');")


def test_sql_ticket_attachment_has_uploader_owner(tmp_path):
    path = tmp_path / "snapshot.sql"
    path.write_text(sql_fixture(), encoding="utf-8")
    records = sql_extract(path, "evidence_fixture", IDENTITY)
    assert [(r.system_id, r.resource_id, r.user_ref) for r in records] == [
        ("support_platform", "support_1", "user_1")]


def test_sql_unrelated_uploaded_by_is_not_owner(tmp_path):
    path = tmp_path / "snapshot.sql"
    path.write_text(sql_fixture(collection="ticket_messages"), encoding="utf-8")
    assert sql_extract(path, "evidence_fixture", IDENTITY) == []
