"""Summarize the unlabeled 518-case run without opening sample answers."""

import csv
import json
from collections import Counter
from pathlib import Path


def summarize(root):
    root = Path(root)
    with (root / "dataset/deletion_requests.csv").open(encoding="utf-8-sig", newline="") as stream:
        case_ids = [row["case_id"] for row in csv.DictReader(stream)]
    with (root / "dataset/evidence_files.csv").open(encoding="utf-8-sig", newline="") as stream:
        manifest_count = sum(1 for _ in csv.DictReader(stream))
    totals = Counter()
    issues = []
    for case_id in case_ids:
        path = root / "code/.cache/diagnostics" / f"{case_id}.jsonl"
        if not path.is_file():
            issues.append(f"{case_id}:missing_diagnostic")
            continue
        events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        starts = [event for event in events if event.get("phase") == "evidence" and event.get("event") == "start"]
        extractions = [event for event in events if event.get("phase") == "evidence" and event.get("event") == "extract_evidence"]
        completions = [event for event in events if event.get("phase") == "steps" and event.get("event") == "generate"]
        if not starts or starts[-1].get("inputs", {}).get("manifest_count") != manifest_count:
            issues.append(f"{case_id}:manifest_count_mismatch")
        if not extractions or not completions:
            issues.append(f"{case_id}:incomplete_diagnostic")
            continue
        totals["cases_with_complete_trace"] += 1
        extracted = extractions[-1].get("outputs", {})
        totals["stale_negative_lookups_excluded"] += extracted.get("stale_negative_lookups_excluded", 0)
        totals["post_audit_exact_owner_joins"] += extracted.get("post_audit_exact_owner_joins", 0)
        totals["manifest_dispatches_expected"] += manifest_count
        errors = completions[-1].get("outputs", {}).get("errors", [])
        if errors:
            totals["cases_with_pipeline_errors"] += 1
            issues.append(f"{case_id}:pipeline_errors:{len(errors)}")
        for event in events:
            if event.get("phase") == "evidence_review" and event.get("event") == "tool_loop":
                totals["cases_with_agent_tool_inspection"] += 1
                totals["tool_inspections"] += len(event.get("outputs", {}).get("tool_results", []))
            if event.get("phase") == "expander" and event.get("event") == "expand_activities":
                totals["derived_activities"] += event.get("outputs", {}).get("derived_count", 0)
    totals["cases_expected"] = len(case_ids)
    totals["evidence_files_per_case"] = manifest_count
    output_path = root / "output.csv"
    if output_path.is_file():
        with output_path.open(encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                if row.get("deletion_status") == "COMPLETE" and row.get("steps_json", "").strip() == "[]":
                    totals["complete_without_verification"] += 1
    return totals, issues


def write_report(root):
    totals, issues = summarize(root)
    target = Path(root) / "code/evaluation/runtime_diagnostics_summary.md"
    lines = [
        "# Final-run diagnostic coverage", "",
        "Aggregated from the 518 full-request diagnostics and generated output, not from sample answers. The production loop enumerates every manifest entry per case; the diagnostic start event records its expected count. Cached sources are still rehashed locally. A COMPLETE row with no verification is counted separately as an evidence-quality risk even if the CSV shape passes. These counts describe this local evidence snapshot, not a live Northstar system query.",
        "", "| Measure | Count |", "|---|---:|",
        *[f"| {key} | {value} |" for key, value in sorted(totals.items())],
        "", f"Diagnostic issues: {len(issues)}.",
        *[f"- {issue}" for issue in issues[:30]], "",
    ]
    target.write_text("\n".join(lines), encoding="utf-8")
    return target, totals, issues


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    target, totals, issues = write_report(root)
    print(f"{totals['cases_with_complete_trace']}/{totals['cases_expected']} traces; {len(issues)} issues; report={target}")
    raise SystemExit(bool(issues))
