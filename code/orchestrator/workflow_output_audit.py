"""Inspect full-run workflow derivations without consulting public answers."""

import csv
import json
from collections import Counter
from pathlib import Path


def _rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def audit(root=None):
    root = Path(root or Path(__file__).resolve().parents[2])
    outputs = {row["case_id"]: row for row in _rows(root / "output.csv")}
    requests = _rows(root / "dataset/deletion_requests.csv")
    counts = Counter()
    cases = []
    for request in requests:
        case_id = request["case_id"]
        path = root / "code/.cache/diagnostics" / f"{case_id}.jsonl"
        if not path.is_file():
            counts["missing_diagnostics"] += 1
            continue
        entries = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        expansion = next((entry["outputs"] for entry in entries
                          if entry["phase"] == "expander"
                          and entry["event"] == "expand_activities"), {})
        for reason in expansion.get("workflow_affiliation", []):
            counts[f"decision_{reason['reason']}"] += 1
        result = outputs.get(case_id)
        if result is None:
            counts["missing_output_rows"] += 1
            continue
        steps = json.loads(result["steps_json"])
        for derived in expansion.get("derived", []):
            if derived.get("method") != "unique_calibrated_report_window":
                continue
            resource = derived["resource_id"]
            original = derived["original_activity_id"]
            matching = [step for step in steps if step.get("resource_id") == resource]
            citations = [step.get("evidence_id", "") for step in matching]
            counts["derived_account_actions"] += 1
            counts[f"derived_case_status_{result['deletion_status']}"] += 1
            if matching:
                counts["derived_actions_with_steps"] += 1
            if result["deletion_status"] == "COMPLETE" and original in citations:
                counts["complete_cites_activity_claim"] += 1
            cases.append((case_id, resource, original, result["deletion_status"],
                          ", ".join(step["operation"] for step in matching),
                          ", ".join(citations)))
    lines = ["# Full-run workflow derivation audit", "",
             "This source-only audit reads `output.csv` and the same run's diagnostic traces; "
             "it does not read `sample_output.csv`. A workflow result is a claim, so "
             "COMPLETE verifications that cite only an activity require scrutiny.", "",
             "| Measure | Count |", "|---|---:|"]
    lines += [f"| {key} | {value} |" for key, value in sorted(counts.items())]
    lines += ["", "## Derived account actions", "",
              "| Case | Account | Original activity | Status | Step operations | Citations |",
              "|---|---|---|---|---|---|"]
    lines += ["| " + " | ".join(values) + " |" for values in cases]
    lines.append("")
    target = root / "code/evaluation/workflow_output_audit.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    return target, counts, cases


if __name__ == "__main__":
    path, counts, _ = audit()
    print(f"{counts['derived_account_actions']} account derivations; "
          f"{counts['complete_cites_activity_claim']} COMPLETE activity-only citations; "
          f"report={path}")
