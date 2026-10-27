"""Gold-free probe of whether reported time can safely identify ownerless actions."""

import csv
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

from agent.evidence.handlers import json_handler, log_handler, sql_handler
from .log_trace_integrity import owner_index


def rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def stamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def direct_account_owners(root):
    root = Path(root)
    index = owner_index(root)
    bundle = SimpleNamespace(all_user_ids=set(index.values()),
                             all_emails={ref for ref in index if "@" in ref},
                             primary_user_id=None)
    owners = defaultdict(set)
    for source in rows(root / "dataset/evidence_files.csv"):
        path = root / "dataset" / source["file_path"]
        suffix = path.suffix.casefold()
        if suffix == ".json":
            extracted = json_handler.extract(path, source["file_id"], bundle)
        elif suffix == ".sql":
            extracted = sql_handler.extract(path, source["file_id"], bundle)
        elif suffix == ".log":
            extracted = log_handler.extract(path, source["file_id"], bundle)[0]
        else:
            continue
        for record in extracted:
            if record.system_id != "account_service" or not record.resource_id.startswith("account_"):
                continue
            owner = index.get(record.user_ref.casefold())
            if owner:
                owners[record.resource_id].add(owner)
    return {resource: next(iter(users)) for resource, users in owners.items()
            if len(users) == 1}, {resource: users for resource, users in owners.items()
                                  if len(users) > 1}


def measure(requests, activities, known_owners, identities):
    totals = Counter()
    examples = []
    account_actions = [row for row in activities if row["target_system"] == "account_service"
                       and row["event_type"] in {"DELETE_RECORD", "CREATE_RECORD", "REDACT_RECORD"}
                       and row["resource_id"].startswith("account_")]
    for request in requests:
        user = identities.get(request["email"].strip().casefold())
        if not user:
            continue
        start = stamp(request["requested_at"])
        finish = stamp(request["reported_at"])
        nearby = [row for row in account_actions if start <= stamp(row["event_time"]) <= finish]
        if not nearby:
            continue
        totals["requests_with_any_account_action"] += 1
        nearest = min(nearby, key=lambda row: (abs((finish - stamp(row["event_time"])).total_seconds()),
                                               row["activity_id"]))
        known_candidates = [row for row in nearby if row["resource_id"] in known_owners]
        if known_candidates:
            totals["requests_with_labeled_candidates"] += 1
            truth = {row["resource_id"] for row in known_candidates
                     if known_owners[row["resource_id"]] == user}
            if truth:
                totals["requests_with_owned_action"] += 1
                totals["nearest_owned_action"] += int(nearest["resource_id"] in truth)
                if nearest["resource_id"] not in truth:
                    examples.append((request["case_id"], user, len(nearby),
                                     nearest["resource_id"], sorted(truth)[:3]))
            elif nearest["resource_id"] in known_owners:
                totals["nearest_known_other_owner_no_owned_action"] += 1
        totals[f"candidate_count_{min(len(nearby),10)}"] += 1
    return totals, examples


def write_report(root):
    root = Path(root)
    known, conflicts = direct_account_owners(root)
    suffix_agreements = sum(resource.rsplit("_", 1)[-1].isdigit()
                            and user.rsplit("_", 1)[-1].isdigit()
                            and int(resource.rsplit("_", 1)[-1]) == int(user.rsplit("_", 1)[-1])
                            for resource, user in known.items())
    identity = owner_index(root)
    activities = rows(root / "dataset/system_activity.csv")
    full, full_examples = measure(rows(root / "dataset/deletion_requests.csv"),
                                  activities, known, identity)
    sample, sample_examples = measure(rows(root / "dataset/sample_deletion_requests.csv"),
                                      activities, known, identity)
    lines = ["# Temporal affiliation probe", "",
             "This is a gold-free diagnostic. It reads request input times, manifest evidence, identities and activity rows; it never reads sample_output.csv or prior output.csv. A temporal match is only a candidate owner link.", "",
             f"Directly owned account resources discovered: {len(known)}; conflicting owners: {len(conflicts)}. Numeric account/user suffix agreement: {suffix_agreements}/{len(known)}.", "",
             "| Measure | Full 518-case input | 32-case sample input |",
             "|---|---:|---:|"]
    for key in sorted(set(full) | set(sample)):
        lines.append(f"| {key} | {full[key]} | {sample[key]} |")
    lines += ["", "## Known-owner counterexamples", "",
              "Each row is a request with at least one directly owned account activity in its request-to-reported window, but the nearest action belongs to a different or unowned resource.",
              "| Case | Canonical user | Window account actions | Nearest resource | Directly owned resource(s) |",
              "|---|---|---:|---|---|"]
    for cid, user, count, nearest, truth in (full_examples + sample_examples)[:30]:
        lines.append(f"| {cid} | {user} | {count} | {nearest} | {', '.join(truth)} |")
    lines += ["", "A high hit rate here would still not turn reported_at into a direct ownership field. The requested-to-reported interval is a claim-supplied time window, and ambiguous windows must remain unresolved.", ""]
    target = root / "code/evaluation/temporal_owner_probe.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    return target, full, sample, conflicts


if __name__ == "__main__":
    report, full, sample, conflicts = write_report(Path(__file__).resolve().parents[2])
    print(f"owned resources={full['requests_with_owned_action']} full requests with owned account actions; "
          f"nearest correct={full['nearest_owned_action']}; "
          f"sample={sample['nearest_owned_action']}/{sample['requests_with_owned_action']}; "
          f"conflicts={len(conflicts)}; report={report}")
