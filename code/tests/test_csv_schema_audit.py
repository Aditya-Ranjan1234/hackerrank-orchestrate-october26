from pathlib import Path

from orchestrator.csv_schema_audit import SPECS, audit_dataset, check_csv


ROOT = Path(__file__).resolve().parents[2]


def test_all_supplied_csv_schemas_and_manifest_paths_parse_cleanly():
    checks, errors = audit_dataset(ROOT)
    assert len(checks) == 9
    assert errors == []
    assert sum(check.rows for check in checks if check.name == "deletion_requests.csv") == 518
    assert next(check.rows for check in checks if check.name == "evidence_files.csv") == 94


def test_duplicate_headers_and_ragged_rows_are_reported(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("case_id,case_id\none,two,extra\n", encoding="utf-8")
    result = check_csv(path, ("case_id", "steps_json"), "case_id")
    assert "schema_mismatch" in result.errors
    assert "duplicate_header" in result.errors
    assert result.malformed_rows == 1


def test_invalid_timestamps_are_reported(tmp_path):
    path = tmp_path / "requests.csv"
    path.write_text("case_id,requested_at\none,not-a-date\n", encoding="utf-8")
    result = check_csv(path, ("case_id", "requested_at"), "case_id")
    assert result.invalid_timestamps == 1
