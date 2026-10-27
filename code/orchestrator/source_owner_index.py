"""Build a source-only veto index for exact account-resource ownership.

Only a direct current/historical identifier in a parsed resource record can
establish an owner. The index never consults sample answers or predictions.
"""

import csv
import hashlib
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace

from agent.evidence.handlers import image_handler, json_handler, log_handler, pdf_handler, sql_handler


def _rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


@lru_cache(maxsize=4)
def known_account_owners(root):
    """Return full account ID -> unique visible owner; omit conflicting aliases.

    This is a veto for weak workflow affiliation, not a source of new facts.
    All manifest formats are inspected, using local OCR for images and no model.
    """
    root = Path(root).resolve()
    dataset = root / "dataset"
    if not (dataset / "evidence_files.csv").exists():
        return {}
    identities = _rows(dataset / "user_identities.csv")
    alias_users = defaultdict(set)
    for row in identities:
        user = row.get("user_id", "")
        for value in (user, row.get("email", ""), row.get("email_hash", "")):
            if value and user:
                alias_users[value.strip().casefold()].add(user)
    for row in _rows(dataset / "user_audit_log.csv"):
        if row.get("field_name", "").casefold() not in {"email", "email_hash"}:
            continue
        for field in ("old_value", "new_value"):
            value = row.get(field, "").strip().casefold()
            if value:
                alias_users[value].add(row["user_id"])
    for alias, users in list(alias_users.items()):
        if "@" in alias:
            alias_users[hashlib.sha256(alias.encode("utf-8")).hexdigest()].update(users)
    aliases = {alias: next(iter(users)) for alias, users in alias_users.items()
               if len(users) == 1}
    bundle = SimpleNamespace(
        all_user_ids={row["user_id"] for row in identities if row.get("user_id")},
        all_emails={alias for alias in alias_users if "@" in alias},
        all_email_hashes={alias for alias in alias_users if len(alias) == 64
                          and all(char in "0123456789abcdef" for char in alias)},
        primary_user_id=None,
    )
    owners = defaultdict(set)
    for source in _rows(dataset / "evidence_files.csv"):
        path = dataset / source["file_path"]
        if not path.is_file():
            continue
        if path.suffix.lower() == ".json":
            records = json_handler.extract(path, source["file_id"], bundle)
        elif path.suffix.lower() == ".sql":
            records = sql_handler.extract(path, source["file_id"], bundle)
        elif path.suffix.lower() in {".log", ".txt"}:
            records = log_handler.extract(path, source["file_id"], bundle)[0]
        elif path.suffix.lower() == ".pdf":
            records = pdf_handler.extract(path, source["file_id"], bundle)[0]
        elif path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            records = image_handler.extract(path, source["file_id"], bundle).records
        else:
            continue
        for record in records:
            if record.system_id != "account_service" or not record.resource_id.startswith("account_"):
                continue
            owner = aliases.get(str(record.user_ref).strip().casefold())
            if owner:
                owners[record.resource_id].add(owner)
    return {resource: next(iter(users)) for resource, users in owners.items() if len(users) == 1}
