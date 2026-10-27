"""SQL flag and legal-hold decisions grounded in the supplied schema/rules."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.evidence.handlers.sql_handler import extract
from agent.evidence.ir import ExtractedEvidence
from agent.policy.engine import PolicyEngine
from agent.state.reconstructor import reconstruct


ROOT = Path(__file__).resolve().parents[2]
IDENTITY = SimpleNamespace(primary_user_id="user_1", all_user_ids={"user_1"},
                           all_emails={"a@example.test"})
AUDIT = "2026-06-01T00:00:00Z"


def decide(tmp_path, sql):
    source = tmp_path / "fixture.sql"
    source.write_text(sql, encoding="utf-8")
    records = extract(source, "evidence_synthetic", IDENTITY)
    ev = ExtractedEvidence("evidence_synthetic", str(source), "hash", records,
                           "sqlite", datetime.now(timezone.utc))
    facts = reconstruct(IDENTITY, [ev], [], AUDIT)
    verdicts = PolicyEngine.from_csv(ROOT / "dataset/deletion_rules.csv").apply(
        facts, requested_at="2026-05-01T00:00:00Z", audit_at=AUDIT)
    return records, facts, verdicts


def test_sqlite_zero_connector_is_disabled_flow_not_record_to_delete(tmp_path):
    sql = """CREATE TABLE connector_subscriptions (
      resource_id TEXT, customer_reference TEXT, enabled INTEGER, updated_at TEXT);
      INSERT INTO connector_subscriptions VALUES
      ('data_flow_1','user_1',0,'2026-05-20T00:00:00Z');"""
    records, facts, verdicts = decide(tmp_path, sql)
    assert records[0].raw_row["enabled"] is False
    assert "connector_disabled_by_evidence" in facts[0].notes
    assert verdicts[0].required_action == "DISABLE_DATA_FLOW"
    assert verdicts[0].is_in_compliance


def test_sqlite_one_connector_is_active_flow(tmp_path):
    sql = """CREATE TABLE connector_subscriptions (
      resource_id TEXT, customer_reference TEXT, enabled INTEGER, updated_at TEXT);
      INSERT INTO connector_subscriptions VALUES
      ('data_flow_1','user_1',1,'2026-05-20T00:00:00Z');"""
    records, facts, verdicts = decide(tmp_path, sql)
    assert records[0].raw_row["enabled"] is True
    assert "connector_enabled_by_evidence" in facts[0].notes
    assert verdicts[0].required_action == "DISABLE_DATA_FLOW"
    assert not verdicts[0].is_in_compliance


def test_sqlite_zero_restore_flag_is_blocked_risk(tmp_path):
    sql = """CREATE TABLE backup_restore_entries (
      resource_id TEXT, customer_reference TEXT, restore_allowed INTEGER, updated_at TEXT);
      INSERT INTO backup_restore_entries VALUES
      ('backup_1','user_1',0,'2026-05-20T00:00:00Z');"""
    records, facts, verdicts = decide(tmp_path, sql)
    assert records[0].raw_row["restore_allowed"] is False
    assert "restore_access_blocked_by_evidence" in facts[0].notes
    assert verdicts[0].required_action == "BLOCK_RESTORE"
    assert verdicts[0].is_in_compliance


def test_nested_sql_json_state_flag_survives_extraction(tmp_path):
    body = json.dumps({"resource_id": "backup_1", "subject_reference": "user_1",
                       "restore_allowed": False})
    sql = ("CREATE TABLE customer_data_primary (resource_id TEXT, origin_system TEXT, "
           "record_json TEXT, as_of TEXT); "
           "INSERT INTO customer_data_primary VALUES "
           f"('backup_1','backup_service','{body}','2026-05-20T00:00:00Z');")
    records, facts, verdicts = decide(tmp_path, sql)
    assert records[0].raw_row["restore_allowed"] is False
    assert "restore_access_blocked_by_evidence" in facts[0].notes
    assert verdicts[0].required_action == "BLOCK_RESTORE"


def test_active_legal_hold_is_retained(tmp_path):
    body = json.dumps({"resource_id": "legal_hold_1", "subject_reference": "user_1",
                       "retention_reason": "payment_dispute_and_tax_record",
                       "retained_until": "2033-12-31T23:59:59Z"})
    sql = ("CREATE TABLE customer_data_primary (resource_id TEXT, origin_system TEXT, "
           "record_json TEXT, as_of TEXT); "
           "INSERT INTO customer_data_primary VALUES "
           f"('legal_hold_1','legal_service','{body}','2026-05-20T00:00:00Z');")
    records, _, verdicts = decide(tmp_path, sql)
    assert records[0].raw_row["retained_until"] == "2033-12-31T23:59:59Z"
    assert verdicts[0].required_action == "RETAIN"
    assert verdicts[0].winning_rule_id == "rule_13"
    assert verdicts[0].is_in_compliance


def test_expired_legal_hold_does_not_activate_retention_rule(tmp_path):
    body = json.dumps({"resource_id": "legal_hold_1", "subject_reference": "user_1",
                       "retained_until": "2026-05-30T00:00:00Z"})
    sql = ("CREATE TABLE customer_data_primary (resource_id TEXT, origin_system TEXT, "
           "record_json TEXT, as_of TEXT); "
           "INSERT INTO customer_data_primary VALUES "
           f"('legal_hold_1','legal_service','{body}','2026-05-20T00:00:00Z');")
    _, _, verdicts = decide(tmp_path, sql)
    assert verdicts[0].required_action == "DELETE_RECORD"
    assert "rule_13" not in verdicts[0].applicable_rule_ids


def test_sql_support_contacts_explicitly_null_are_redacted(tmp_path):
    sql = """CREATE TABLE support_records (resource_id TEXT, customer_reference TEXT,
      requester_email TEXT, requester_name TEXT, requester_phone TEXT, updated_at TEXT);
      INSERT INTO support_records VALUES
      ('support_1','user_1',NULL,NULL,NULL,'2026-05-20T00:00:00Z');"""
    records, _, verdicts = decide(tmp_path, sql)
    assert records[0].state_at_evidence == "REDACTED"
    assert verdicts[0].required_action == "REDACT_RECORD"
    assert verdicts[0].is_in_compliance


def test_sql_support_partial_redaction_still_exposes_pii(tmp_path):
    sql = """CREATE TABLE support_records (resource_id TEXT, customer_reference TEXT,
      requester_email TEXT, requester_name TEXT, requester_phone TEXT, updated_at TEXT);
      INSERT INTO support_records VALUES
      ('support_1','user_1','a@example.test',NULL,NULL,'2026-05-20T00:00:00Z');"""
    records, _, verdicts = decide(tmp_path, sql)
    assert records[0].state_at_evidence == "PRESENT"
    assert not verdicts[0].is_in_compliance
