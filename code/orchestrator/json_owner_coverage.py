"""Cross-check explicit JSON subject/resource rows against the extractor.

This independent source inventory never consults sample answers or output CSVs.
Only a literal owner or readback-subject field in the same JSON object as a
full resource ID is a coverage candidate. A readback subject can link a query
result to a person, but does not prove that the result stored that identifier.
Query selectors and upload actors are excluded.
"""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

from agent.evidence.handlers.json_handler import extract
from .log_trace_integrity import owner_index


DIRECT_OWNER_FIELDS = frozenset({
    "user_id", "user_uuid", "customer_id", "customer_reference", "subject_reference",
    "owner_user_id", "subject_user_id", "target_user_id", "user_ref", "account_owner_id",
    "email", "user_email", "customer_email", "owner_email", "requester_email",
    "contact_email", "billing_email", "shipping_email", "email_hash", "email_sha256",
    "hashed_email",
})


def _source_rows(node, index):
    """Find explicit object-level subject/resource pairs, independent of handler traversal."""
    if isinstance(node, dict):
        rid = node.get("resource_id") or node.get("id")
        owners = {index[value.strip().casefold().strip("<>")] for key, value in node.items()
                  if key.casefold() in DIRECT_OWNER_FIELDS and isinstance(value, str)
                  and value.strip().casefold().strip("<>") in index}
        if rid is not None and owners:
            yield str(rid), owners
        for value in node.values():
            yield from _source_rows(value, index)
    elif isinstance(node, list):
        for value in node:
            yield from _source_rows(value, index)


def inspect_json(root):
    root = Path(root)
    index = owner_index(root)
    with (root / "dataset/user_identities.csv").open(encoding="utf-8-sig", newline="") as stream:
        identities = list(csv.DictReader(stream))
    emails = {ref for ref in index if "@" in ref}
    hashes = {row["email_hash"].casefold() for row in identities if row["email_hash"]}
    for email in emails:
        hashes.add(hashlib.sha256(email.encode("utf-8")).hexdigest())
    # A recorded email hash is associated with the row's exact user; computed
    # hashes use the historical/current email owner index.
    for row in identities:
        if row["email_hash"]:
            index[row["email_hash"].casefold()] = row["user_id"]
    for email in emails:
        index[hashlib.sha256(email.encode("utf-8")).hexdigest()] = index[email]
    bundle = SimpleNamespace(all_user_ids={row["user_id"] for row in identities},
                             all_emails=emails, all_email_hashes=hashes,
                             primary_user_id=None)
    with (root / "dataset/evidence_files.csv").open(encoding="utf-8-sig", newline="") as stream:
        files = [(row["file_id"], root / "dataset" / row["file_path"])
                 for row in csv.DictReader(stream)
                 if Path(row["file_path"]).suffix.casefold() == ".json"]
    result = []
    missing = []
    conflicting = []
    for file_id, path in files:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        candidates = list(_source_rows(data, index))
        parsed = extract(path, file_id, bundle)
        extracted = Counter((record.resource_id, index.get(record.user_ref.strip().casefold(), ""))
                            for record in parsed)
        for rid, owners in candidates:
            if len(owners) > 1:
                conflicting.append((file_id, rid))
            for owner in owners:
                if extracted[(rid, owner)] == 0:
                    missing.append((file_id, rid, owner))
        result.append({"file_id": file_id, "file": path.name,
                       "direct_owner_rows": sum(len(owners) for _, owners in candidates),
                       "extracted_records": len(parsed),
                       "missing": sum(file_id == item[0] for item in missing)})
    return {"file_count": len(files), "direct_owner_rows": sum(row["direct_owner_rows"] for row in result),
            "extracted_records": sum(row["extracted_records"] for row in result),
            "missing": missing, "conflicting": conflicting, "files": result}


def write_report(root):
    root = Path(root)
    result = inspect_json(root)
    target = root / "code/evaluation/json_owner_coverage.md"
    lines = ["# JSON subject-to-resource coverage", "",
             "Independent read of manifest-listed JSON source objects with a literal `resource_id` or `id` and an exact current/historical owner or readback-subject field. A `subject_reference` in a readback links the result to the queried person; it is not counted as PII retained in a NOT_FOUND or REDACTED resource. `query`, `lookup_value`, `subject_selector`, and `uploaded_by` are excluded because they can name a requester or actor without establishing record ownership. Source pairs are compared to the production JSON extractor without an audit cutoff. Nested inherited IDs are additional handler behavior outside this direct-row check.",
             "", f"Files: {result['file_count']}; direct owner/resource pairs: {result['direct_owner_rows']}; parser records: {result['extracted_records']}; missing direct pairs: {len(result['missing'])}; conflicting direct owners: {len(result['conflicting'])}.",
             "", "| File ID | Source file | Direct pairs | Extracted records | Missing direct pairs |",
             "|---|---|---:|---:|---:|",
             *[f"| `{row['file_id']}` | `{row['file']}` | {row['direct_owner_rows']} | {row['extracted_records']} | {row['missing']} |" for row in result["files"]],
             "", "## Exceptions", "",
             *([f"- Missing: `{file_id}/{rid}/{owner}`" for file_id, rid, owner in result["missing"]] or ["No direct pair omissions."]),
             *[f"- Conflicting owners: `{file_id}/{rid}`" for file_id, rid in result["conflicting"]],
             ""]
    target.write_text("\n".join(lines), encoding="utf-8")
    return target, result


if __name__ == "__main__":
    report, result = write_report(Path(__file__).resolve().parents[2])
    print(f"{result['file_count']} JSON files; {result['direct_owner_rows']} direct pairs; "
          f"{len(result['missing'])} missing; {len(result['conflicting'])} conflicting; report={report}")
    raise SystemExit(bool(result["missing"] or result["conflicting"]))
