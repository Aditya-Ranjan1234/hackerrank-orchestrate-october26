"""Evaluation-only diagnosis of sample step gaps, phase by phase.

Gold answers select cases for inspection here. Nothing in the production
pipeline imports this module, and no gold association is written to runtime
state or caches.
"""

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from .residual_provenance import inventory_sources, source_hits
from .sample_gold_backtrace import exact
from .log_trace_integrity import owner_index
from .temporal_owner_probe import direct_account_owners


SEMANTIC_FIELDS = ("phase", "system_id", "resource_id", "operation", "state")


def _rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return {row["case_id"]: row for row in csv.DictReader(stream)}


def missing_steps(actual_steps, gold_steps):
    """Return missing steps by semantics, without positional cascade errors."""
    remaining = Counter(tuple(step.get(k) for k in SEMANTIC_FIELDS) for step in actual_steps)
    missing = []
    for step in gold_steps:
        key = tuple(step.get(k) for k in SEMANTIC_FIELDS)
        if remaining[key]:
            remaining[key] -= 1
        else:
            missing.append(step)
    return missing


def classify_gap(raw_evidence_count, participant_csv_count, activity_count,
                 extracted_count, derived_count, fact_count, verdict_count):
    """Locate the earliest absent link; never infer a person from a resource alone."""
    if verdict_count:
        return "verdict_exists_step_missing"
    if fact_count:
        return "fact_exists_verdict_missing"
    if derived_count:
        return "derived_activity_not_reconstructed"
    if extracted_count:
        return "anonymous_extraction_not_affiliated"
    if raw_evidence_count:
        return "raw_evidence_not_extracted_for_user"
    if activity_count:
        return "ownerless_activity_only"
    if participant_csv_count:
        return "participant_csv_reference_only"
    return "no_participant_input_names_resource"


def _phase_outputs(trace_path):
    rows = [json.loads(line) for line in Path(trace_path).read_text(encoding="utf-8").splitlines()]
    return {(row["phase"], row["event"]): row.get("outputs", {}) for row in rows}


def reported_time_control(requests, activities, direct_owners, identity_index,
                          window_seconds=300):
    """Measure a proposed time join on exact-owner controls, without gold."""
    def stamp(value):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    account_deletes = [(row, stamp(row["event_time"])) for row in activities
                       if row.get("source_system") == "deletion_worker"
                       and row.get("target_system") == "account_service"
                       and row.get("event_type") == "DELETE_RECORD"]
    counts = Counter()
    for request in requests:
        owner = identity_index.get(request["email"].strip().casefold())
        if not owner:
            continue
        reported = stamp(request["reported_at"])
        candidates = [row for row, event_time in account_deletes
                      if 0 <= (reported - event_time).total_seconds() <= window_seconds]
        if len(candidates) != 1:
            continue
        counts["unique_candidate"] += 1
        known_owner = direct_owners.get(candidates[0]["resource_id"])
        if known_owner:
            counts["independently_owned"] += 1
            counts["correct_owner"] += known_owner == owner
    return counts


def diagnose(root, candidate_path, report_path=None):
    root = Path(root)
    gold = _rows(root / "dataset/sample_output.csv")
    actual = _rows(candidate_path)
    sources = inventory_sources(root)
    participant_csv = {
        path.name: path.read_text(encoding="utf-8-sig", errors="replace")
        for path in (root / "dataset").glob("*.csv")
        if path.name not in {"sample_output.csv", "output.csv"}
    }
    with (root / "dataset/system_activity.csv").open(encoding="utf-8-sig", newline="") as stream:
        activities = list(csv.DictReader(stream))
    with (root / "dataset/deletion_requests.csv").open(encoding="utf-8-sig", newline="") as stream:
        full_requests = list(csv.DictReader(stream))
    control_owners, control_conflicts = direct_account_owners(root)
    time_control = reported_time_control(full_requests, activities, control_owners,
                                         owner_index(root))
    gaps = []
    complete_without_verdict = []
    status_match = exact_match = 0
    for case_id, expected_row in sorted(gold.items()):
        observed_row = actual.get(case_id)
        if observed_row is None:
            raise ValueError(f"Candidate is missing {case_id}")
        expected = json.loads(expected_row["steps_json"] or "[]")
        observed = json.loads(observed_row["steps_json"] or "[]")
        status_match += observed_row["deletion_status"] == expected_row["deletion_status"]
        exact_match += observed == expected
        outputs = _phase_outputs(root / "code/.cache/diagnostics" / f"{case_id}.jsonl")
        evidence = [record for item in outputs.get(("evidence", "extract_evidence"), {}).get("files", [])
                    for record in item.get("records", [])]
        derived = outputs.get(("expander", "expand_activities"), {}).get("derived", [])
        facts = outputs.get(("state", "reconstruct"), {}).get("facts", [])
        verdicts = outputs.get(("policy", "apply"), {}).get("verdicts", [])
        if observed_row["deletion_status"] == "COMPLETE" and not verdicts:
            complete_without_verdict.append(case_id)
        for step in missing_steps(observed, expected):
            resource = step["resource_id"]
            raw_hits = source_hits(resource, (), sources)
            csv_hits = [name for name, body in participant_csv.items() if exact(resource, body)]
            activity_hits = [row for row in activities if row.get("resource_id") == resource]
            extracted_hits = [row for row in evidence if row.get("resource_id") == resource]
            derived_hits = [row for row in derived if row.get("resource_id") == resource]
            fact_hits = [row for row in facts if row.get("resource_id") == resource]
            verdict_hits = [row for row in verdicts if row.get("resource_id") == resource]
            counts = (len(raw_hits), len(csv_hits), len(activity_hits),
                      len(extracted_hits), len(derived_hits), len(fact_hits), len(verdict_hits))
            gaps.append({"case_id": case_id, "resource_id": resource,
                         "operation": step["operation"], "gold_citation": step.get("evidence_id", ""),
                         "counts": counts, "class": classify_gap(*counts),
                         "extracted_user_refs": sorted({str(row.get("user_ref") or "")
                                                        for row in extracted_hits}),
                         "raw_locations": [f"{name}:{location}" for name, location, _ in raw_hits[:3]],
                         "activity_ids": [row["activity_id"] for row in activity_hits[:3]]})
    groups = Counter(gap["class"] for gap in gaps)
    cases_without_evidence_id = {gap["case_id"] for gap in gaps if gap["counts"][0] == 0}
    all_gold_steps = sum(len(json.loads(row["steps_json"] or "[]")) for row in gold.values())
    all_agent_steps = sum(len(json.loads(actual[case_id]["steps_json"] or "[]")) for case_id in gold)
    lines = ["# Sample step gap diagnosis", "",
             "**Evaluation only.** Public sample answers are read only to identify missing steps. "
             "Production imports and predictions are unchanged.", "",
             f"Statuses: {status_match}/{len(gold)}. Exact ordered arrays: {exact_match}/{len(gold)}. "
             f"Gold steps: {all_gold_steps}; agent steps: {all_agent_steps}; missing semantic steps: {len(gaps)}.", "",
             f"{sum(gap['counts'][0] == 0 for gap in gaps)} target IDs have no occurrence "
             f"in the {len(sources)} evidence files, across "
             f"{len(cases_without_evidence_id)} sample cases. If direct owner-bearing "
             f"evidence were the only permitted affiliation path, the conditional ceiling "
             f"would be "
             f"{len(gold) - len(cases_without_evidence_id)}/{len(gold)} exact arrays even "
             "if every other case were repaired. The calibrated activity route is a "
             "separate indirect path and has already recovered one absent-from-evidence "
             "target; this ceiling is not a claim about every possible safe inference.", "",
             "## First failed link for each missing step", "",
             "| Failure class | Steps | Pipeline consequence |", "|---|---:|---|",
             f"| Resource ID absent from all participant inputs | {groups['no_participant_input_names_resource']} | No possible source-to-case link |",
             f"| Ownerless activity only, no evidence ID | {groups['ownerless_activity_only']} | Activity expander cannot assign user |",
             f"| Raw evidence has ID but per-user extraction omits it | {groups['raw_evidence_not_extracted_for_user']} | No owned record enters state reconstruction |",
             f"| Anonymous record extracted, not affiliated | {groups['anonymous_extraction_not_affiliated']} | Reconstructor drops it before verdict |",
             f"| Later pipeline failure | {sum(count for name, count in groups.items() if name not in {'no_participant_input_names_resource','ownerless_activity_only','raw_evidence_not_extracted_for_user','anonymous_extraction_not_affiliated'})} | Inspect fact, policy or step builder |",
             "", "## Per-step trace", "",
             "Counts are raw evidence occurrences / other participant CSV occurrences / original activity rows / "
             "case-extracted records / derived activities / ResourceFacts / policy verdicts.", "",
             "| Case | Missing resource / operation | Gold cite | Counts | First failed link |",
             "|---|---|---|---|---|"]
    for gap in gaps:
        lines.append(f"| {gap['case_id']} | `{gap['resource_id']}` `{gap['operation']}` | "
                     f"`{gap['gold_citation']}` | {' / '.join(map(str, gap['counts']))} | "
                     f"{gap['class']} |")
    lines += ["", "## Causal trace", "",
              "`pipeline.py` extracts the 94 manifest sources, expands activities, reconstructs ResourceFacts, "
              "applies policy and builds steps. `activity_expander.py` joins activities only to a record "
              "with a known owner and the same full resource ID or an explicit source reference. "
              "`reconstructor.py` discards ownerless records unless an already-owned copy of the "
              "same full resource exists. `steps/builder.py` emits a verification only for a policy verdict.", "",
              "The positional `SYSTEM_ID_MISMATCH` and `RESOURCE_ID_MISMATCH` counts in "
              "`step_diff_report.md` are array-shift artifacts. The semantic comparison has no extra "
              "steps and no shared-step citation differences. The missing ResourceFacts are upstream "
              "of the step mapper and ordering code.", "",
              "## Concrete examples", "",
              "- `case_01/account_001`: `activity_3342` claims deletion 17 seconds "
              "before the request's reported time. This is a strong candidate "
              "correlation, but the activity has no user or case key. The later "
              "SQL snapshot `evidence_54` contains no `account_001` in either account "
              "table. The agent has no owner-affiliated fact and no closed-world "
              "negative-snapshot record, so it emits no verification. See "
              "`case01_process_trace.md` for the two separate gaps and timing controls.",
              "- `case_03/analytics_9406`: the log's lookup key and all direct subject fields "
              "are null. A nearby `user_43` event has another trace ID. Its raw log observation "
              "does not establish ownership.",
              "- `case_21/account_6440`: `evidence_92` has a 404 readback with "
              "`user_ref=''`. The record is extracted, then ignored because no independently "
              "owned copy of `account_6440` exists.",
              "- `case_04/account_004`, `case_18/audit_record_6645` and "
              "`case_20/audit_record_5569` occur nowhere in participant inputs. "
              "Their exact IDs are visible only in the public sample answers.", "",
              "## Status agreement does not prove resource coverage", "",
              f"COMPLETE with zero policy verdicts: {', '.join(complete_without_verdict) or 'none'}. "
              "The status gate returns COMPLETE when it sees no incomplete verdicts, so an "
              "undiscovered resource can leave the status unchanged while its required verification "
              "step is absent. This is a confidence limitation in the current three-status interface.", "",
              "## Safe next action", "",
              "Do not copy sample resource IDs into runtime logic or assign an anonymous row by file "
              "co-occurrence, numeric suffix or nearest time. The source-only temporal control "
              "in `temporal_owner_probe.md` found the nearest account action belonged to the "
              "requester for only 71/212 directly evaluable full requests. A stricter control "
              "using a unique account deletion in the five minutes before the reported time "
              f"found {time_control['correct_owner']}/{time_control['independently_owned']} "
              "correct subjects among independently owned records "
              f"({time_control['unique_candidate']} requests had a unique candidate; "
              f"{len(control_conflicts)} owner conflicts). The production workflow affiliator "
              "now uses `reported_at` only as a bounded correlation hint when a 30–90-minute "
              "window contains one account deletion across ALL outcome classes. It checks the "
              "winner's SUCCESS claim afterward, vetoes known other owners and ambiguous "
              "requesters, and keeps the timestamp out of status determination. "
              "`workflow_affiliation_probe.md` reports the gold-free controls and the rejected "
              "SUCCESS-prefilter variant. For the remaining anonymous or absent IDs, a trustworthy "
              "subject-to-resource ledger, trace/correlation ID or prior owned snapshot would "
              "allow an exact affiliation join. Preserve the failing step gate until that link "
              "is available or the contract explicitly changes.", ""]
    target = Path(report_path) if report_path else root / "code/evaluation/step_gap_diagnosis.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")
    return {"target": target, "status_match": status_match, "array_match": exact_match,
            "cases": len(gold), "gaps": gaps, "groups": groups,
            "complete_without_verdict": complete_without_verdict,
            "reported_time_control": time_control,
            "cases_without_evidence_id": cases_without_evidence_id}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    candidate = args.candidate or args.root / "artifacts/csv/phase17_final_sample.csv"
    result = diagnose(args.root, candidate, args.report)
    print(f"{result['status_match']}/{result['cases']} statuses; "
          f"{result['array_match']}/{result['cases']} exact arrays; "
          f"{len(result['gaps'])} missing steps; classes={dict(result['groups'])}; "
          f"report={result['target']}")


if __name__ == "__main__":
    main()
