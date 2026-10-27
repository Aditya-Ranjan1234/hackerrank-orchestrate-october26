"""Source-only audit of log trace ownership joins; never reads sample answers."""

import csv
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


TRACE = re.compile(r'(?:\btrace_id=|"trace_id"\s*:\s*")([\w-]+)')
STAMP = re.compile(r"20\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z")
IDENTIFIER = re.compile(r"(?<![\w-])user_\d+(?![\w-])|[\w.+-]+@[\w.-]+\.[a-z]{2,}", re.I)
FIELD = re.compile(r'(?<!\w)"?([a-zA-Z_][\w-]*)"?\s*[:=]\s*"?([^"\s,}]+)')
OWNER_FIELDS = {
    "user_id", "user_uuid", "customer_reference", "subject_reference", "subject_ref",
    "customer_email", "owner_email", "requester_email", "email", "lookup_key",
    "match_key", "subject_key", "matched_value", "correlation_key", "owner_key",
}


def owner_index(root):
    """Map current and historical exact identifiers to a stable source user ID."""
    root = Path(root)
    index = {}
    with (root / "dataset/user_identities.csv").open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            index[row["user_id"].casefold()] = row["user_id"]
            index[row["email"].casefold()] = row["user_id"]
    with (root / "dataset/user_audit_log.csv").open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["field_name"].casefold() != "email":
                continue
            for field in ("old_value", "new_value"):
                value = row[field].strip().casefold()
                if value:
                    index[value] = row["user_id"]
    return index


def scan_text(text, index, file_name="synthetic.log"):
    """Check one file; unrelated lines cannot establish trace ownership."""
    groups = defaultdict(list)
    for number, original in enumerate(text.splitlines(), 1):
        match = TRACE.search(original)
        if not match:
            continue
        line = original.replace('\\"', '"')
        literal = {index[value.group(0).casefold()] for value in IDENTIFIER.finditer(line)
                   if value.group(0).casefold() in index}
        structured = {index[value.casefold()] for key, value in FIELD.findall(line)
                      if key.casefold() in OWNER_FIELDS and value.casefold() in index}
        stamp_match = STAMP.search(line)
        stamp = datetime.fromisoformat(stamp_match.group(0).replace("Z", "+00:00")) if stamp_match else None
        groups[match.group(1)].append((number, stamp, literal, structured, "resource_id" in line))

    counts = Counter()
    issues = []
    counts["trace_groups"] = len(groups)
    for trace_id, events in groups.items():
        literal = set().union(*(event[2] for event in events))
        owners = set().union(*(event[3] for event in events))
        if literal:
            counts["traces_with_known_identity"] += 1
        if literal and not owners:
            counts["identity_only_in_unstructured_text"] += 1
            issues.append(f"{file_name}:{trace_id}:identity_without_structured_field")
        if len(owners) > 1:
            counts["conflicting_trace_owners"] += 1
            issues.append(f"{file_name}:{trace_id}:multiple_canonical_owners")
        for line_number, stamp, _, direct, has_resource in events:
            if not has_resource:
                continue
            counts["resource_lines"] += 1
            if not owners:
                counts["resource_lines_without_owner_signal"] += 1
            if stamp and owners and not direct and not any(
                other_stamp is not None and other_stamp <= stamp and other_owners
                for _, other_stamp, _, other_owners, _ in events
            ):
                counts["resource_lines_with_only_later_owner_signal"] += 1
                issues.append(f"{file_name}:{line_number}:owner_signal_only_after_resource")
    return counts, issues


def scan_logs(root):
    root = Path(root)
    index = owner_index(root)
    counts = Counter()
    issues = []
    with (root / "dataset/evidence_files.csv").open(encoding="utf-8-sig", newline="") as stream:
        paths = [root / "dataset" / row["file_path"] for row in csv.DictReader(stream)
                 if Path(row["file_path"]).suffix.casefold() == ".log"]
    counts["log_files"] = len(paths)
    for path in paths:
        if not path.is_file():
            issues.append(f"{path.name}:missing_file")
            continue
        found, problems = scan_text(path.read_text(encoding="utf-8", errors="replace"), index, path.name)
        counts.update(found)
        issues.extend(problems)
    for key in ("conflicting_trace_owners", "identity_only_in_unstructured_text",
                "resource_lines_with_only_later_owner_signal"):
        counts.setdefault(key, 0)
    return counts, issues


def write_report(root):
    root = Path(root)
    counts, issues = scan_logs(root)
    target = root / "code/evaluation/log_trace_integrity.md"
    lines = ["# Structured log trace integrity", "",
             "Source-only check of all manifest-listed `.log` files against current and historical exact identifiers. It does not read `sample_output.csv` or a prior agent output. A trace with multiple canonical people, an owner signal only after a resource line, or an identifier seen only in unstructured text is flagged. Ownerless resource lines are held apart; a trace ID alone is not an owner.",
             "", "| Measure | Count |", "|---|---:|",
             *[f"| {key} | {value} |" for key, value in sorted(counts.items())],
             "", f"Integrity issues: {len(issues)}.",
             *[f"- {issue}" for issue in issues[:30]], "",
             "This is a source-integrity screen. It does not prove that every structured query refers to a stored record; the evidence handler and state reconstruction apply their own event and time rules.", ""]
    target.write_text("\n".join(lines), encoding="utf-8")
    return target, counts, issues


if __name__ == "__main__":
    report, totals, problems = write_report(Path(__file__).resolve().parents[2])
    print(f"{totals['log_files']} logs; {totals['trace_groups']} traces; {len(problems)} issues; report={report}")
    raise SystemExit(bool(problems))
