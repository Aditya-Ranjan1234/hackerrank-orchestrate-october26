"""Gold-free calibration of account workflow report-time joins.

This diagnostic reads participant request inputs, identities, activities and
manifest evidence. It never imports or opens sample answers or prior output.
"""

import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

from agent.status.request_classifier import is_deletion_request
from .pipeline import load_datasets
from .source_owner_index import known_account_owners
from .workflow_affiliation import _dt


def _rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def _account_actions(activities):
    return [row for row in activities
            if row.get("event_type") == "DELETE_RECORD"
            and row.get("source_system") == "deletion_worker"
            and row.get("target_system") == "account_service"
            and str(row.get("resource_id", "")).startswith("account_")]


def measure_window(requests, activities, resolver, owners, lower_minutes, upper_minutes,
                   successful_only=False, winner_success_only=False):
    """Score unique candidate ownership against independent source owners."""
    if successful_only and winner_success_only:
        raise ValueError("Choose either prefilter or winner-outcome check")
    counts = Counter()
    actions = _account_actions(activities)
    for case in requests:
        identity = resolver.resolve(case["email"], case["audit_at"])
        if not identity.primary_user_id:
            continue
        reported = _dt(case.get("reported_at"))
        requested = _dt(case.get("requested_at"))
        audit = _dt(case.get("audit_at"))
        if not reported or not requested or not audit:
            continue
        matches = [row for row in actions
                   if (not successful_only or row.get("reported_result") == "SUCCESS")
                   and requested <= _dt(row["event_time"]) <= audit
                   and lower_minutes <= (reported - _dt(row["event_time"])).total_seconds() / 60
                   <= upper_minutes]
        if len(matches) != 1:
            continue
        if winner_success_only and matches[0].get("reported_result") != "SUCCESS":
            continue
        counts["unique"] += 1
        owner = owners.get(matches[0]["resource_id"])
        if owner:
            counts["known"] += 1
            counts["correct" if owner in identity.all_user_ids else "other_person"] += 1
        else:
            counts["unresolved"] += 1
    return counts


def masked_owner_folds(requests, activities, resolver, owners, fold_count=5):
    """Hide each fold of direct owners, then check derived IDs against it.

    This simulates a sparse evidence index. Truly ownerless resources remain
    unresolved; they are never scored as correct or wrong by this diagnostic.
    """
    actions = [(row, _dt(row["event_time"])) for row in _account_actions(activities)]
    resolved = []
    for case in requests:
        if not is_deletion_request(case.get("request_text")):
            continue
        identity = resolver.resolve(case["email"], case["audit_at"])
        report, request, audit = (_dt(case.get(field)) for field in
                                  ("reported_at", "requested_at", "audit_at"))
        if identity.primary_user_id and report and request and audit:
            resolved.append((identity, report, request, audit))
    results = []
    for fold in range(fold_count):
        visible = {resource: user for resource, user in owners.items()
                   if hashlib.sha256(resource.encode("utf-8")).digest()[0] % fold_count != fold}
        visible_users = set(visible.values())
        eligible = defaultdict(set)
        for identity, report, _, _ in resolved:
            if not set(identity.all_user_ids) & visible_users:
                eligible[report].add(identity.primary_user_id)
        counts = Counter()
        for identity, report, request, audit in resolved:
            if set(identity.all_user_ids) & visible_users or len(eligible[report]) != 1:
                continue
            matches = [row for row, event in actions
                       if request <= event <= audit
                       and 30 * 60 <= (report - event).total_seconds() <= 90 * 60
                       and (row["resource_id"] not in visible
                            or visible[row["resource_id"]] in identity.all_user_ids)]
            if len(matches) != 1 or matches[0].get("reported_result") != "SUCCESS":
                continue
            counts["derived"] += 1
            real_owner = owners.get(matches[0]["resource_id"])
            if real_owner:
                counts["known_correct" if real_owner in identity.all_user_ids
                       else "known_wrong"] += 1
            else:
                counts["unresolved"] += 1
        results.append(counts)
    return results


def write_report(root=None):
    root = Path(root or Path(__file__).resolve().parents[2])
    data = load_datasets(root)
    owners = known_account_owners(str(root))
    full = _rows(root / "dataset/deletion_requests.csv")
    sample = _rows(root / "dataset/sample_deletion_requests.csv")
    bands = ((0, 5), (20, 100), (30, 90), (40, 80), (45, 75))
    lines = ["# Source-only workflow affiliation calibration", "",
             "This probe does not read `sample_output.csv`, `output.csv`, or a cached answer. "
             "Ownership labels come from exact current/historical identifiers in the supplied evidence. "
             "A unique timestamp candidate is a correlation, not proof of deletion state.", "",
             f"Directly owned account IDs across all manifest formats: {len(owners)}.", "",
             "| Delay before report | Candidate/outcome rule | Unique request windows | Independently owned | Correct owner | Other owner | Unresolved |",
             "|---|---|---:|---:|---:|---:|---:|"]
    for lower, upper in bands:
        rules = ((False, False, "all actions"),
                 (False, True, "all actions; winner SUCCESS"))
        if (lower, upper) in {(0, 5), (30, 90)}:
            rules += ((True, False, "SUCCESS prefilter (rejected)"),)
        for successful_only, winner_success_only, label in rules:
            counts = measure_window(full, data.activities, data.resolver, owners,
                                    lower, upper, successful_only, winner_success_only)
            lines.append(f"| {lower}–{upper} min | {label} | "
                         f"{counts['unique']} | {counts['known']} | {counts['correct']} | "
                         f"{counts['other_person']} | {counts['unresolved']} |")
    folds = masked_owner_folds(full, data.activities, data.resolver, owners)
    lines += ["", "## Masked-owner control", "",
              "A stable five-fold hash split hides one fifth of exact account-owner links at a time. "
              "The production eligibility and ambiguity gates are replayed against the reduced index. "
              "Known held-out links are then checked against their original source owners; "
              "truly ownerless candidates remain unscored.", "",
              "| Fold | Derived | Known correct | Known wrong | Unresolved |",
              "|---:|---:|---:|---:|---:|"]
    for number, counts in enumerate(folds):
        lines.append(f"| {number} | {counts['derived']} | {counts['known_correct']} | "
                     f"{counts['known_wrong']} | {counts['unresolved']} |")
    summed = sum((counts for counts in folds), Counter())
    lines.append(f"| **Total** | **{summed['derived']}** | **{summed['known_correct']}** | "
                 f"**{summed['known_wrong']}** | **{summed['unresolved']}** |")
    lines += ["", "## Public sample request inputs: unresolved unique candidates", "",
              "The public sample *requests* are used only to count source-side candidates. "
              "This is not a score against answers.", "",
              "| Case | Activity | Account | Delay before report |",
              "|---|---|---|---:|"]
    for case in sample:
        identity = data.resolver.resolve(case["email"], case["audit_at"])
        reported = _dt(case.get("reported_at"))
        requested = _dt(case.get("requested_at"))
        audit = _dt(case.get("audit_at"))
        if not identity.primary_user_id or not reported or not requested or not audit:
            continue
        matches = [row for row in _account_actions(data.activities)
                   if requested <= _dt(row["event_time"]) <= audit
                   and 30 <= (reported - _dt(row["event_time"])).total_seconds() / 60 <= 90
                   and (row["resource_id"] not in owners
                        or owners[row["resource_id"]] in identity.all_user_ids)]
        if len(matches) == 1 and matches[0].get("reported_result") == "SUCCESS" \
                and matches[0]["resource_id"] not in owners:
            row = matches[0]
            delay = (reported - _dt(row["event_time"])).total_seconds() / 60
            lines.append(f"| {case['case_id']} | {row['activity_id']} | {row['resource_id']} | {delay:.1f} min |")
    lines += ["", "The production affiliator also vetoes directly owned accounts, "
              "competing eligible requesters and any account whose exact owner is another person. "
              "The source-only table therefore measures the timing signal before those extra gates.", ""]
    target = root / "code/evaluation/workflow_affiliation_probe.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    return target


if __name__ == "__main__":
    print(write_report())
