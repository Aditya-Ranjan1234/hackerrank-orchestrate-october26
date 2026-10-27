"""Nested SQL snapshots must expose PII and replica drift, not collapse it away."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime, timezone
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.evidence.handlers.sql_handler import extract
from agent.evidence.ir import ExtractedEvidence
from agent.state.reconstructor import reconstruct

IDENTITY=SimpleNamespace(all_user_ids={"user_1"},all_emails={"a@example.com"},primary_user_id="user_1")
STAMP="2026-09-20T12:00:00Z"
SCHEMA="(resource_id TEXT, origin_system TEXT, record_json TEXT, updated_at TEXT)"


def test_sql_nested_tombstone_carries_sibling_pii_and_state(tmp_path):
    path=tmp_path/"copy.sql"
    path.write_text("CREATE TABLE customer_data_primary "+SCHEMA+";"
                    "INSERT INTO customer_data_primary VALUES ('tombstone_1','identity_service',"
                    "'{\"subject_reference\":\"user_1\",\"account_status\":\"DELETED\",\"email_hash\":\"retained_hash\",\"name\":\"Alice\"}',"
                    "'"+STAMP+"');")
    record=extract(path,"ev",IDENTITY)[0]
    assert record.system_id=="identity_service" and record.state_at_evidence=="TOMBSTONE"
    assert {h.value_kind for h in record.pii_hits}>={"name","email_hash"}
    assert record.raw_row["_source_table"]=="customer_data_primary"


def test_clean_tombstone_is_redacted_not_present(tmp_path):
    path=tmp_path/"copy.sql"
    path.write_text("CREATE TABLE customer_data_primary "+SCHEMA+";"
                    "INSERT INTO customer_data_primary VALUES ('tombstone_1','identity_service',"
                    "'{\"subject_reference\":\"user_1\",\"account_status\":\"DELETED\",\"email\":null,\"phone\":null,\"name\":null,\"email_hash\":null}',"
                    "'"+STAMP+"');")
    record=extract(path,"ev",IDENTITY)[0]
    assert record.state_at_evidence=="REDACTED"
    assert {h.value_kind for h in record.pii_hits}=={"user_id"}


def test_replica_ghost_wins_same_file_same_time(tmp_path):
    path=tmp_path/"copy.sql"
    path.write_text("CREATE TABLE customer_data_failover_replica "+SCHEMA+";"
                    "CREATE TABLE customer_data_primary "+SCHEMA+";"
                    "INSERT INTO customer_data_failover_replica VALUES ('tombstone_1','identity_service',"
                    "'{\"subject_reference\":\"user_1\",\"account_status\":\"DELETED\",\"email\":\"a@example.com\"}',"
                    "'"+STAMP+"');"
                    "INSERT INTO customer_data_primary VALUES ('tombstone_1','identity_service',"
                    "'{\"subject_reference\":\"user_1\",\"account_status\":\"DELETED\",\"email\":null}',"
                    "'"+STAMP+"');")
    records=extract(path,"ev",IDENTITY)
    evidence=[ExtractedEvidence("ev",str(path),"digest",records,"sqlite",datetime.now(timezone.utc))]
    facts=reconstruct(IDENTITY,evidence,[],"2026-09-21T00:00:00Z")
    assert len(facts)==1 and facts[0].state_at_audit=="TOMBSTONE"
    assert facts[0].direct_pii_present=={"email"}
    assert "multiple_sql_copies_checked_for_replica_ghost" in facts[0].notes
