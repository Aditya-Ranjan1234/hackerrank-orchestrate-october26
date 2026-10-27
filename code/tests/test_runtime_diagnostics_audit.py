import csv
import json

from orchestrator.runtime_diagnostics_audit import summarize


def test_run_summary_counts_manifest_and_tool_inspections(tmp_path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    with (dataset / "deletion_requests.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["case_id"])
        writer.writeheader()
        writer.writerow({"case_id": "case_1"})
    with (dataset / "evidence_files.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["file_id"])
        writer.writeheader()
        writer.writerows([{"file_id": "e1"}, {"file_id": "e2"}])
    path = tmp_path / "code/.cache/diagnostics/case_1.jsonl"
    path.parent.mkdir(parents=True)
    events = [
        {"phase": "evidence", "event": "start", "inputs": {"manifest_count": 2}},
        {"phase": "evidence", "event": "extract_evidence", "outputs": {"stale_negative_lookups_excluded": 1, "post_audit_exact_owner_joins": 2}},
        {"phase": "evidence_review", "event": "tool_loop", "outputs": {"tool_results": [{}, {}]}},
        {"phase": "steps", "event": "generate", "outputs": {"errors": []}},
    ]
    path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
    with (tmp_path / "output.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["case_id", "deletion_status", "steps_json"])
        writer.writeheader()
        writer.writerow({"case_id": "case_1", "deletion_status": "COMPLETE", "steps_json": "[]"})
    totals, issues = summarize(tmp_path)
    assert issues == []
    assert totals["manifest_dispatches_expected"] == 2
    assert totals["cases_with_agent_tool_inspection"] == 1
    assert totals["tool_inspections"] == 2
    assert totals["stale_negative_lookups_excluded"] == 1
    assert totals["post_audit_exact_owner_joins"] == 2
    assert totals["complete_without_verification"] == 1
