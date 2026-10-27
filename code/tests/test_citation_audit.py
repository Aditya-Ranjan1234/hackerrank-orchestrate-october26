import csv
import json

from orchestrator.citation_audit import _capture_after_audit, _verified_log_line_handle, audit_citations


def _csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_exact_source_citation_is_accepted_without_gold_file(tmp_path):
    evidence = tmp_path / "dataset/evidence/records/a.json"
    evidence.parent.mkdir(parents=True)
    evidence.write_text('{"resource_id":"account_1","user_id":"U1"}', encoding="utf-8")
    _csv(tmp_path / "dataset/evidence_files.csv", ["file_id", "file_path"],
         [{"file_id": "e1", "file_path": "evidence/records/a.json"}])
    _csv(tmp_path / "dataset/system_activity.csv", ["activity_id", "resource_id"], [])
    _csv(tmp_path / "dataset/user_audit_log.csv", ["audit_id"], [])
    _csv(tmp_path / "output.csv", ["case_id", "steps_json"],
         [{"case_id": "synthetic", "steps_json": json.dumps([{"evidence_id": "e1", "resource_id": "account_1"}])}])
    counts, problems = audit_citations(tmp_path)
    assert counts["cited_steps"] == 1
    assert problems == []


def test_unseen_resource_or_unknown_citation_is_reported(tmp_path):
    evidence = tmp_path / "dataset/evidence/records/a.json"
    evidence.parent.mkdir(parents=True)
    evidence.write_text('{"resource_id":"account_1"}', encoding="utf-8")
    _csv(tmp_path / "dataset/evidence_files.csv", ["file_id", "file_path"],
         [{"file_id": "e1", "file_path": "evidence/records/a.json"}])
    _csv(tmp_path / "dataset/system_activity.csv", ["activity_id", "resource_id"], [])
    _csv(tmp_path / "dataset/user_audit_log.csv", ["audit_id"], [])
    _csv(tmp_path / "output.csv", ["case_id", "steps_json"],
         [{"case_id": "synthetic", "steps_json": json.dumps([
             {"evidence_id": "e1", "resource_id": "account_2"},
             {"evidence_id": "invented", "resource_id": "account_1"},
         ])}])
    _, problems = audit_citations(tmp_path)
    assert {problem[3] for problem in problems} == {
        "resource_id_not_visible_in_cited_file", "unknown_citation_id"
    }


def test_generated_log_line_handle_requires_exact_subject_on_cited_line(tmp_path):
    from types import SimpleNamespace

    path = tmp_path / "events.log"
    path.write_text("2026-01-01 service=account_service user_id=U10\n"
                    "2026-01-02 service=account_service user_id=U1\n", encoding="utf-8")
    identity = SimpleNamespace(all_user_ids={"U1"}, all_emails=set())
    assert _verified_log_line_handle(path, "evidence_8", "evidence_8_line_2", identity)
    assert not _verified_log_line_handle(path, "evidence_8", "evidence_8_line_1", identity)
    assert not _verified_log_line_handle(path, "evidence_8", "evidence_8_line_3", identity)


def test_capture_cutoff_is_distinct_from_row_time():
    assert _capture_after_audit("2026-09-18T11:55:24Z", "2026-09-16T09:00:00Z")
    assert not _capture_after_audit("2026-09-15T11:44:55Z", "2026-09-15T12:00:00Z")
