"""Only a persisted connector selector can establish flow affiliation."""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.evidence.handlers.json_handler import extract as json_extract
from agent.evidence.handlers.sql_handler import extract as sql_extract


IDENTITY = SimpleNamespace(primary_user_id="user_1", all_user_ids={"user_1"},
                           all_emails={"one@example.test"})


def snapshot(collection):
    return {"snapshots": [{"captured_at": "2026-05-20T00:00:00Z",
                           "data_store": "integration_service", "collection": collection,
                           "records": [
                               {"resource_id": "data_flow_1", "subject_selector": "user_1",
                                "enabled": True, "mode": "continuous_sync"},
                               {"resource_id": "data_flow_10", "subject_selector": "user_10",
                                "enabled": True, "mode": "continuous_sync"},
                           ]}]}


def test_json_persisted_connector_selector_has_exact_owner(tmp_path):
    path = tmp_path / "snapshot.json"
    path.write_text(json.dumps(snapshot("connector_configurations")), encoding="utf-8")
    records = json_extract(path, "evidence_fixture", IDENTITY)
    assert [(r.system_id, r.resource_id, r.user_ref) for r in records] == [
        ("integration_service", "data_flow_1", "user_1")]


def test_json_lookup_selector_is_not_owned_record(tmp_path):
    path = tmp_path / "snapshot.json"
    path.write_text(json.dumps(snapshot("record_lookups")), encoding="utf-8")
    assert json_extract(path, "evidence_fixture", IDENTITY) == []


def sql_fixture(collection):
    record = json.dumps({"resource_id": "data_flow_1", "subject_selector": "one@example.test",
                         "enabled": False, "mode": "continuous_sync"})
    return ("CREATE TABLE customer_data_primary (resource_id TEXT, origin_system TEXT, "
            "collection_name TEXT, record_json TEXT, updated_at TEXT); "
            "INSERT INTO customer_data_primary VALUES "
            f"('data_flow_1','integration_service','{collection}','{record}',"
            "'2026-05-20T00:00:00Z');")


def test_sql_nested_connector_selector_has_exact_owner(tmp_path):
    path = tmp_path / "snapshot.sql"
    path.write_text(sql_fixture("connector_configurations"), encoding="utf-8")
    records = sql_extract(path, "evidence_fixture", IDENTITY)
    assert [(r.system_id, r.resource_id, r.user_ref) for r in records] == [
        ("integration_service", "data_flow_1", "user_1")]
    assert records[0].raw_row["enabled"] is False


def test_sql_transient_selector_is_not_owned_record(tmp_path):
    path = tmp_path / "snapshot.sql"
    path.write_text(sql_fixture("record_lookups"), encoding="utf-8")
    assert sql_extract(path, "evidence_fixture", IDENTITY) == []
