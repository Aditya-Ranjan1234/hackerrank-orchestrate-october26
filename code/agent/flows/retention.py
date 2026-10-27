from datetime import datetime, timedelta
import re

DEFAULT_RETENTION = {"daily_backup": timedelta(days=30), "weekly_backup": timedelta(days=90), "monthly_backup": timedelta(days=365), "annual_backup": timedelta(days=365 * 7), "snapshot": None}

def dt(value):
    if not value: return None
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))

def parse_retention(value):
    if not value: return None
    text = str(value).strip().casefold()
    if text in {"permanent", "none", "never"}: return None
    match = re.fullmatch(r"(\d+)\s*(d|day|days|w|week|weeks|m|month|months|y|year|years)", text)
    if not match: return None
    n, unit = int(match.group(1)), match.group(2)
    return timedelta(days=n * (7 if unit.startswith("w") else 30 if unit.startswith("m") else 365 if unit.startswith("y") else 1))

def get_retention_expires(backup_activity, policy=DEFAULT_RETENTION):
    start = dt(backup_activity.get("event_time") or backup_activity.get("backup_time"))
    raw = backup_activity.get("retention")
    if not raw:
        found = re.search(r"retention\s*[:=]\s*([\w -]+)", backup_activity.get("details", ""), re.I)
        raw = found.group(1).strip() if found else None
    delta = parse_retention(raw)
    if delta is None: delta = policy.get(str(backup_activity.get("backup_type", "snapshot")).casefold(), policy.get("snapshot"))
    return None if start is None or delta is None else start + delta

def is_backup_within_retention(backup_activity, audit_at, retention_policy=DEFAULT_RETENTION):
    expiry = get_retention_expires(backup_activity, retention_policy)
    cutoff = dt(audit_at) if isinstance(audit_at, str) else audit_at
    return expiry is None or expiry > cutoff
