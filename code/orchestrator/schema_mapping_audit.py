"""Inventory every SQL export, its tables and exact-owner extraction coverage."""

import csv
import hashlib
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace

from agent.evidence.handlers.sql_handler import extract
from .database_inspector import inspect_database, ownership_rows


NESTED_OWNER_FIELDS = {
    "user_id", "user_uuid", "userid", "customer_id", "account_id",
    "customer_reference", "subject_reference", "email", "customer_email",
    "requester_email", "owner_email", "contact_email", "billing_email",
    "shipping_email", "email_hash", "email_sha256", "hashed_email",
}


def nested_ownership_rows(path, identifiers):
    """Independently inspect JSON payload columns for exact subject fields."""
    wanted = {str(value).casefold() for value in identifiers if value}

    def owns(value):
        if isinstance(value, dict):
            if any(key.casefold() in NESTED_OWNER_FIELDS and isinstance(child, str)
                   and child.casefold() in wanted for key, child in value.items()):
                return True
            return any(owns(child) for child in value.values())
        return isinstance(value, list) and any(owns(child) for child in value)

    db = sqlite3.connect(":memory:")
    try:
        db.executescript(Path(path).read_text(encoding="utf-8", errors="replace"))
        found = []
        for (table,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
            quoted = '"' + table.replace('"', '""') + '"'
            columns = [row[1] for row in db.execute(f"PRAGMA table_info({quoted})")]
            payloads = [column for column in columns if column.casefold().endswith("_json")]
            for values in db.execute(f"SELECT * FROM {quoted}"):
                row = dict(zip(columns, values))
                for column in payloads:
                    try:
                        payload = json.loads(row[column]) if isinstance(row[column], str) else None
                    except json.JSONDecodeError:
                        continue
                    if owns(payload):
                        found.append({"table": table,
                                      "resource_id": str(row.get("resource_id") or row.get("id") or ""),
                                      "payload_column": column})
                        break
        return found
    finally:
        db.close()


def inspect_all_sql(root):
    root = Path(root)
    with (root / "dataset/user_identities.csv").open(encoding="utf-8-sig", newline="") as handle:
        identities = list(csv.DictReader(handle))
    emails = {row["email"].strip().casefold() for row in identities if row.get("email")}
    hashes = {row["email_hash"].strip().casefold() for row in identities if row.get("email_hash")}
    with (root / "dataset/user_audit_log.csv").open(encoding="utf-8-sig", newline="") as handle:
        for event in csv.DictReader(handle):
            values = (event.get("old_value", ""), event.get("new_value", ""))
            if event.get("field_name", "").casefold() == "email":
                emails.update(value.strip().casefold() for value in values if value.strip())
            elif event.get("field_name", "").casefold() == "email_hash":
                hashes.update(value.strip().casefold() for value in values if value.strip())
    hashes.update(hashlib.sha256(email.encode("utf-8")).hexdigest() for email in emails)
    bundle = SimpleNamespace(
        all_user_ids={row["user_id"] for row in identities if row.get("user_id")},
        all_emails=emails,
        all_email_hashes=hashes,
        primary_user_id=None,
    )
    rows = []
    direct_owner_rows = 0
    direct_owner_missing = []
    nested_owner_rows = 0
    nested_owner_missing = []
    files = sorted((root / "dataset/evidence/databases").glob("*.sql"))
    for path in files:
        inspection = inspect_database(path)
        extracted = extract(path, path.name, bundle)
        direct = ownership_rows(path, bundle.all_user_ids | bundle.all_emails | bundle.all_email_hashes)
        nested = nested_ownership_rows(path, bundle.all_user_ids | bundle.all_emails | bundle.all_email_hashes)
        direct_owner_rows += len(direct)
        nested_owner_rows += len(nested)
        present = Counter((record.raw_row.get("_source_table"), record.resource_id) for record in extracted)
        for source_row in direct:
            key = (source_row["table"], source_row["resource_id"])
            if present[key] == 0:
                direct_owner_missing.append((path.name, *key))
        for source_row in nested:
            key = (source_row["table"], source_row["resource_id"])
            if present[key] == 0:
                nested_owner_missing.append((path.name, *key))
        by_table = defaultdict(list)
        for record in extracted:
            by_table[str(record.raw_row.get("_source_table", ""))].append(record)
        for table in inspection["tables"]:
            matching = by_table[table["name"]]
            rows.append({"file": path.name, "table": table["name"], "rows": table["row_count"],
                         "columns": table["columns"], "owner_columns": table["ownership_columns"],
                         "matched": len(matching), "systems": sorted({record.system_id for record in matching})})
    return {"file_count": len(files), "table_count": len(rows),
            "matched_count": sum(item["matched"] for item in rows),
            "unknown_count": sum(item["matched"] for item in rows if "sql" in item["systems"]),
            "direct_owner_rows": direct_owner_rows,
            "direct_owner_missing": direct_owner_missing,
            "nested_owner_rows": nested_owner_rows,
            "nested_owner_missing": nested_owner_missing,
            "rows": rows}


def write_report(root, target=None):
    root = Path(root)
    result = inspect_all_sql(root)
    target = Path(target) if target else root / "code/evaluation/schema_mapping_audit.md"
    lines = ["# SQL schema and owner-mapping audit", "",
             f"Opened {result['file_count']} SQL files, {result['table_count']} table instances; "
             f"extracted {result['matched_count']} exact-identity-linked rows. "
             f"Unknown-system extracted rows: {result['unknown_count']}.", "",
             f"Independent exact-column cross-check: {result['direct_owner_rows']} direct-owner rows, "
             f"{len(result['direct_owner_missing'])} missing from the production extractor.", "",
             f"Independent nested-JSON cross-check: {result['nested_owner_rows']} exact-owner payload rows, "
             f"{len(result['nested_owner_missing'])} missing from the production extractor.", "",
             "The inventory identity set includes current and historical emails and email hashes, and is used only to audit parser coverage; production filters per request and audit cutoff. "
             "Generic `customer_data_*` tables use explicit `origin_system` from the matched row and owner fields inside `record_json`. "
             "`snapshot_scope` has no direct owner; it is not a per-user resource.", "",
             "| File | Table | Total rows | Owner columns | Identity-linked rows | Result systems |",
             "|---|---|---:|---|---:|---|"]
    for row in result["rows"]:
        lines.append(f"| `{row['file']}` | `{row['table']}` | {row['rows']} | "
                     f"{', '.join(row['owner_columns']) or 'nested `record_json` / none'} | "
                     f"{row['matched']} | {', '.join(row['systems']) or 'no identity-linked row'} |")
    if result["nested_owner_missing"]:
        lines += ["", "## Missed nested owner rows", ""]
        lines.extend(f"- {file_name} / {table} / {resource}"
                     for file_name, table, resource in result["nested_owner_missing"][:30])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    result = write_report(root)
    print(f"SQL files={result['file_count']} tables={result['table_count']} exact rows={result['matched_count']} unknown={result['unknown_count']}")
