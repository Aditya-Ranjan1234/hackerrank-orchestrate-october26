"""Infer per-user activity rows from exact evidence/resource ownership only."""
from datetime import datetime, timedelta
from copy import deepcopy
import re

def _dt(v):
    if isinstance(v, datetime): return v
    try: return datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except (TypeError, ValueError): return None

def _norm(ref, identity):
    if not ref: return None
    if ref in identity.all_user_ids: return ref
    if ref in identity.all_emails: return identity.primary_user_id
    if ref in getattr(identity, "all_email_hashes", set()): return identity.primary_user_id
    return None

def lookup_activity_time_for_resource(resource_id, activity_rows, audit_at=None):
    """Latest pre-audit activity for an exact resource ID; no numeric suffix join."""
    cutoff=_dt(audit_at)
    times=[_dt(row.get("event_time",row.get("activity_time"))) for row in activity_rows if resource_id and row.get("resource_id")==resource_id]
    return max((ts for ts in times if ts and (not cutoff or ts<=cutoff)),default=None)

def _fields(row, activity):
    return {
        "activity_id": row.get("activity_id", row.get("activity_id", "")),
        "event_time": row.get("event_time", row.get("activity_time", "")),
        "event_type": row.get("event_type", row.get("op_type", "")),
        "source_system": row.get("source_system", row.get("system_id", "")),
        "target_system": row.get("target_system", row.get("target_system_id", "")),
        "resource_id": row.get("resource_id", ""),
        "details": row.get("details", ""),
    }

def _resource_id_matches_file_id(resource_id, file_id):
    """Only the explicit evidence_<resource_id> convention is admissible."""
    if not resource_id or not file_id: return False
    normalized=lambda value: re.sub(r"[^a-z0-9]", "", str(value).casefold())
    return normalized(file_id)=="evidence"+normalized(resource_id)

def expand_activities_for_user(activity_rows, evidence, identity, audit_at, time_window=timedelta(hours=24)):
    # time_window is retained only for callers of the former API; no proximity inference.
    cutoff = _dt(audit_at); by_resource = {}; by_file = {}; by_explicit_reference = {}
    for ev in evidence:
        for rec in getattr(ev, "records", []):
            user = _norm(rec.user_ref, identity)
            if not user: continue
            ts = rec.evidence_timestamp
            if ts is None:
                ts = lookup_activity_time_for_resource(rec.resource_id,activity_rows,cutoff)
                if ts: rec.evidence_timestamp=ts
            if not ts or (cutoff and ts > cutoff): continue
            item = (ev.file_id, ts, user)
            by_resource.setdefault(rec.resource_id, []).append(item)
            by_file.setdefault(ev.file_id, []).append(item)
            # A child row with a proven owner can identify its source record
            # through an explicit full resource ID (e.g. search index -> account).
            # Never join by a numeric suffix or co-occurrence in a file.
            source_id=(rec.raw_row or {}).get("source_resource_id")
            if isinstance(source_id,str) and source_id:
                by_explicit_reference.setdefault(source_id,[]).append(item)
    expanded = [deepcopy(row) for row in activity_rows]; counter = 0
    originals = sorted(activity_rows, key=lambda r: (_dt(r.get("event_time", r.get("activity_time"))) or datetime.min, r.get("activity_id", "")))
    for row in originals:
        target = row.get("target_user_id") or row.get("user_id")
        if target: continue
        rid = row.get("resource_id", "")
        resource = list(by_resource.get(rid, [])) if rid else []
        if rid: resource.extend(by_explicit_reference.get(rid,[]))
        for file_id, items in by_file.items():
            if _resource_id_matches_file_id(rid,file_id): resource.extend(items)
        seen=set()
        matches=[]
        for _, _, user in sorted(resource):
            if user not in seen:
                seen.add(user); matches.append((user,"explicit_reference_match" if rid in by_explicit_reference and not by_resource.get(rid) else "resource_id_match"))
        for user, method in matches:
            counter += 1; d = deepcopy(row)
            d["activity_id"] = f"{row.get('activity_id','activity')}::derived_{counter:04d}_for_{user}"
            d["target_user_id"] = user; d["derived"] = True; d["original_activity_id"] = row.get("activity_id", "")
            d["inference_method"] = method
            d["details"] = f"{d.get('details','')} derived_for={user}"
            expanded.append(d)
    return expanded
