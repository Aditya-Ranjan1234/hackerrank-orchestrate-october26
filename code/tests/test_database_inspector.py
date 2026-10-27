from orchestrator.database_inspector import inspect_database, ownership_rows


def test_schema_and_owner_columns(tmp_path):
    path = tmp_path / "a.sql"
    path.write_text("CREATE TABLE orders (resource_id TEXT, user_id TEXT); INSERT INTO orders VALUES ('order_1','U1');", encoding="utf-8")
    table = inspect_database(path)["tables"][0]
    assert table["row_count"] == 1 and table["ownership_columns"] == ["user_id"]


def test_data_only_sql_notes_no_schema(tmp_path):
    path = tmp_path / "a.sql"
    path.write_text("INSERT INTO orders VALUES ('order_1','U1');", encoding="utf-8")
    assert inspect_database(path)["notes"] == ["no schema"]


def test_no_owner_column_does_not_infer(tmp_path):
    path = tmp_path / "a.sql"
    path.write_text("CREATE TABLE orders (resource_id TEXT, note TEXT); INSERT INTO orders VALUES ('order_1','U1');", encoding="utf-8")
    assert inspect_database(path)["tables"][0]["ownership_columns"] == []
    assert ownership_rows(path, {"U1"}) == []


def test_owner_equality_not_substring(tmp_path):
    path = tmp_path / "a.sql"
    path.write_text("CREATE TABLE orders (resource_id TEXT, user_id TEXT); INSERT INTO orders VALUES ('order_10','U10');", encoding="utf-8")
    assert ownership_rows(path, {"U1"}) == []


def test_sql_schema_family_maps_to_service_without_case_lookup():
    from agent.evidence.handlers.sql_handler import infer_system
    assert infer_system("customer_profiles_failover_replica", {"resource_id": "account_9"}) == "account_service"
    assert infer_system("customer_search_documents", {"resource_id": "search_9"}) == "search_service"
    assert infer_system("customer_data_read_replica", {"origin_system": "backup_service"}) == "backup_service"


def test_unknown_sql_table_does_not_invent_system():
    from agent.evidence.handlers.sql_handler import infer_system
    assert infer_system("arbitrary_snapshot", {"resource_id": "x"}) == "sql"
