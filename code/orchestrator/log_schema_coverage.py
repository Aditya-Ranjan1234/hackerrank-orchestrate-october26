"""Independent, source-only coverage audit for structured log owner/resource rows.

The expected owner/resource pairs come from a separate field parser, not from
the production extractor or sample answers. Trace-only joins are reported
separately because the independent source check uses direct same-line owners.
"""

import csv
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace

from .log_trace_integrity import owner_index
from agent.evidence.handlers.log_handler import extract


ATTRIBUTE = re.compile(r'(?<!\w)"?([A-Za-z_][\w-]*)"?\s*[:=]\s*"?([^"\s,}|]+)')
RESOURCE = re.compile(r'(?<!\w)resource_id\s*[:=]\s*"?([\w-]+)', re.I)
OWNER_KEYS = {
    "user_id", "user_uuid", "customer_reference", "subject_reference",
    "subject_ref", "customer_email", "owner_email", "requester_email",
    "email", "user_email", "email_hash", "email_sha256", "hashed_email",
    "matched_value", "correlation_key",
}
EVENT = re.compile(r'(?<!\w)event\s*[:=]\s*"?([\w-]+)', re.I)


def direct_source_pairs(text, identities):
    pairs = set()
    for line in text.splitlines():
        # Shift handover plain text has a fixed six-field pipe row rather
        # than key/value attributes. Parse it independently of the handler.
        cells = [cell.strip() for cell in line.removeprefix("- ").split("|")]
        if line.startswith("- ") and len(cells) == 6 and re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", cells[0]
        ):
            resource, owner = cells[2], cells[5].casefold()
            if resource and owner in identities:
                pairs.add((resource, identities[owner]))
            continue
        normalized = line.replace('\\"', '"')
        event = EVENT.search(normalized)
        if event and event.group(1).casefold().endswith("_started"):
            continue
        resource = RESOURCE.search(normalized)
        if not resource:
            continue
        owners = {identities[value.casefold()]
                  for key, value in ATTRIBUTE.findall(normalized)
                  if key.casefold() in OWNER_KEYS and value.casefold() in identities}
        for owner in owners:
            pairs.add((resource.group(1), owner))
    return pairs


def audit(root):
    root = Path(root)
    index = owner_index(root)
    with (root / "dataset/user_identities.csv").open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("email_hash"):
                index[row["email_hash"].casefold()] = row["user_id"]
    with (root / "dataset/user_audit_log.csv").open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("field_name", "").casefold() == "email_hash":
                for column in ("old_value", "new_value"):
                    if row.get(column):
                        index[row[column].casefold()] = row["user_id"]
    for identifier, user in list(index.items()):
        if "@" in identifier:
            index[hashlib.sha256(identifier.encode("utf-8")).hexdigest()] = user
    by_user = defaultdict(set)
    for identifier, user in index.items():
        by_user[user].add(identifier)
    files = []
    with (root / "dataset/evidence_files.csv").open(encoding="utf-8-sig", newline="") as handle:
        files = [(row["file_id"], root / "dataset" / row["file_path"])
                 for row in csv.DictReader(handle)
                 if Path(row["file_path"]).suffix.casefold() in {".log", ".txt"}]
    totals = Counter()
    details = []
    for file_id, path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        source = direct_source_pairs(text, index)
        # One extraction per source, with all known identifiers. This catches
        # coverage gaps without hundreds of repeated case-specific passes.
        bundle = SimpleNamespace(all_user_ids=set(by_user),
                                 all_emails={value for value in index if "@" in value},
                                 all_email_hashes={value for value in index if re.fullmatch(r"[0-9a-f]{64}", value)},
                                 primary_user_id=None)
        rows, post = extract(path, file_id, bundle)
        extracted = {(row.resource_id, index[row.user_ref.casefold()])
                     for row in rows + post if row.user_ref.casefold() in index}
        missing = source - extracted
        totals.update(files=1, source_direct_pairs=len(source),
                      extracted_pairs=len(extracted),
                      missing_direct_pairs=len(missing))
        details.append((file_id, path.name, len(source), len(extracted), missing))
    return totals, details


def write_report(root):
    root = Path(root)
    totals, details = audit(root)
    lines = ["# Structured log and handover owner/resource coverage", "",
             "Source-only comparison across every manifest-listed log and the plain-text shift handover. The independent field parser finds exact same-line structured owner/resource pairs; production extraction is checked against those pairs. This audit never reads sample answers.", "",
             "| File ID | Source | Direct source pairs | Extracted pairs | Missing direct pairs |",
             "|---|---|---:|---:|---:|"]
    for file_id, name, source, extracted, missing in details:
        lines.append(f"| {file_id} | {name} | {source} | {extracted} | {len(missing)} |")
    lines += ["", f"Total: {totals['source_direct_pairs']} direct source pairs; "
              f"{totals['extracted_pairs']} extracted pairs; "
              f"{totals['missing_direct_pairs']} missing direct pairs.", "",
              "Extra extracted pairs can be legitimate exact-trace joins from a prior structured query. The separate trace-integrity audit checks for conflicting trace owners and later-only owner signals.", ""]
    for file_id, name, _, _, missing in details:
        if missing:
            lines.append(f"- {file_id}: {', '.join(f'{resource}/{owner}' for resource, owner in sorted(missing)[:12])}")
    target = root / "code/evaluation/log_schema_coverage.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    return target, totals, details


if __name__ == "__main__":
    report, totals, _ = write_report(Path(__file__).resolve().parents[2])
    print(f"{totals['source_direct_pairs']} direct source pairs; "
          f"{totals['missing_direct_pairs']} missing; report={report}")
    raise SystemExit(bool(totals["missing_direct_pairs"]))
