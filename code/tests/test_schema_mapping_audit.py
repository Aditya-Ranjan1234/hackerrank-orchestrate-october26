from pathlib import Path

from orchestrator.schema_mapping_audit import inspect_all_sql, nested_ownership_rows


def test_every_sql_file_and_extracted_row_has_a_system():
    root=Path(__file__).resolve().parents[2]
    report=inspect_all_sql(root)
    assert report["file_count"]==len(list((root/"dataset/evidence/databases").glob("*.sql")))
    assert report["table_count"]>report["file_count"]
    assert report["matched_count"]>0
    assert report["unknown_count"]==0
    assert report["direct_owner_rows"]>0
    assert report["direct_owner_missing"]==[]
    assert report["nested_owner_rows"]>0
    assert report["nested_owner_missing"]==[]


def test_generic_replica_tables_resolve_by_origin_not_table_name():
    root=Path(__file__).resolve().parents[2]
    report=inspect_all_sql(root)
    replica=[row for row in report["rows"] if row["table"].startswith("customer_data_")]
    assert replica and all("sql" not in row["systems"] for row in replica)
    assert any("analytics_platform" in row["systems"] for row in replica)


def test_nested_owner_scan_ignores_free_text_email(tmp_path):
    source = tmp_path / "nested.sql"
    source.write_text(
        "CREATE TABLE replica (resource_id TEXT, record_json TEXT);"
        "INSERT INTO replica VALUES ('account_1', '{\"profile\":{\"customer_reference\":\"user_a\"}}');"
        "INSERT INTO replica VALUES ('account_2', '{\"note\":\"user_a\"}');",
        encoding="utf-8",
    )
    assert nested_ownership_rows(source, {"user_a"}) == [
        {"table": "replica", "resource_id": "account_1", "payload_column": "record_json"}
    ]
