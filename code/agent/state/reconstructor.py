from collections import defaultdict
from datetime import datetime
import re
from ..evidence.ir import ResourceFact

def _dt(value):
    if isinstance(value, datetime): return value
    try: return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError): return None

def _mentions(row, ids):
    explicit = row.get("target_user_id") or row.get("user_id") or row.get("user_ref")
    text = " ".join(str(row.get(k, "")) for k in ("details", "message", "payload"))
    if explicit: return explicit in ids
    return any(x and re.search(rf"(?<![\w@.-]){re.escape(x)}(?![\w@.-])", text, re.I) for x in ids)

def _logical_system(system, resource_id):
    """Map a physical replica timeline to its logical resource system.

    The physical topology remains in the activity/evidence audit trail; it
    must not create a second verdict for the same logical record.
    """
    if not system or not resource_id:
        return system
    for suffix in ("_failover_replica", "_replication_cluster", "_read_replica", "_replica"):
        if system.endswith(suffix):
            base=system[:-len(suffix)]
            if resource_id.startswith(base+"_"):
                if base.endswith(("_service","_platform")):
                    return base
                return {"support":"support_platform", "analytics":"analytics_platform"}.get(base,base+"_service")
    return system

def _state_for_timeline(rows):
    state = "PRESENT"
    for row in sorted(rows, key=lambda r: _dt(r.get("event_time", r.get("activity_time"))) or datetime.min):
        op = str(row.get("event_type", row.get("op_type", ""))).upper()
        if op in {"DELETE", "DELETE_RECORD", "TOMBSTONE"}: state = "ABSENT"
        elif op in {"RESTORE", "RESTORE_BACKUP", "SYNC", "SYNC_RECORD", "CREATE", "CREATE_RECORD", "INDEX_RECORD", "CREATE_EXPORT"}: state = "PRESENT"
        elif op in {"REDACT", "REDACT_RECORD"}: state = "REDACTED"
        elif op in {"ANONYMIZE", "ANONYMIZE_RECORD"}: state = "ANONYMIZED"
    return state

STATE_OPS={"DELETE","DELETE_RECORD","TOMBSTONE","RESTORE","RESTORE_BACKUP",
           "SYNC","SYNC_RECORD","CREATE","CREATE_RECORD","INDEX_RECORD",
           "CREATE_EXPORT","UPDATE_RECORD","BACKUP","BACKUP_RECORD","CREATE_BACKUP",
           "REDACT","REDACT_RECORD","ANONYMIZE","ANONYMIZE_RECORD"}

def reconstruct(identity, evidence, activities, audit_at, llm_resolver=None, case_id=None):
    cutoff = _dt(audit_at); ids = set(identity.all_user_ids) | set(identity.all_emails); timelines = defaultdict(list)
    for row in activities:
        ts = _dt(row.get("event_time", row.get("activity_time"))); rid = row.get("resource_id")
        op=str(row.get("event_type",row.get("op_type",""))).upper()
        # On connector SYNC rows the resource_id names the data-flow control,
        # while target_system names the destination of the copy.  The copied
        # record has its own full ID in evidence or the activity details.  A
        # data_flow_* ID is never itself a search record to be deleted.
        if (op in {"SYNC", "SYNC_RECORD", "INDEX_RECORD", "IMPORT_RECORD"}
                and str(rid or "").startswith("data_flow_")
                and row.get("source_system") == "integration_service"):
            continue
        if op in STATE_OPS and ts and cutoff and ts <= cutoff and rid and _mentions(row, ids):
            system = row.get("target_system") or row.get("source_system") or row.get("system_id") or "unknown"
            system = _logical_system(system, str(rid))
            timelines[(system, str(rid))].append(row)
    facts = {}
    for key, rows in timelines.items():
        last = sorted(rows, key=lambda r: _dt(r.get("event_time", r.get("activity_time"))) or datetime.min)[-1]
        facts[key] = ResourceFact(key[0], key[1], identity.primary_user_id or "", _state_for_timeline(rows), set(), last.get("activity_id", "activity"), _dt(last.get("event_time", last.get("activity_time"))), ["timeline-only: no matching evidence record"])
    candidates = defaultdict(list); unowned_absences=[]; anonymous=[]
    for ev in evidence:
        for rec in ev.records:
            if rec.evidence_timestamp and cutoff and rec.evidence_timestamp > cutoff: continue
            if not rec.user_ref:
                anonymous.append((ev,rec))
                if rec.state_at_evidence=="ABSENT" and rec.resource_id:
                    unowned_absences.append((ev,rec))
                continue
            if rec.user_ref and not any(x and x.casefold() == rec.user_ref.casefold() for x in ids): continue
            candidates[(_logical_system(rec.system_id,rec.resource_id), rec.resource_id)].append((ev, rec))
    if llm_resolver is not None:
        for ev, rec in anonymous:
            key=(_logical_system(rec.system_id,rec.resource_id),rec.resource_id)
            # No model-only identity joins: an owner of the same full resource
            # must already be visible in directly attributed evidence.
            if key not in candidates: continue
            context=[{"resource_id": owned.resource_id,"user_ref":owned.user_ref}
                     for _,owned in candidates[key] if owned.user_ref in identity.all_user_ids]
            if not context: continue
            row={**(rec.raw_row or {}),"resource_id":rec.resource_id}
            owner=llm_resolver.affiliate_anonymous_record(row,identity,context,case_id=case_id)
            if owner in identity.all_user_ids:
                rec.user_ref=owner
                candidates[key].append((ev,rec))
    for ev, rec in unowned_absences:
        key=(_logical_system(rec.system_id,rec.resource_id),rec.resource_id)
        if key in candidates: candidates[key].append((ev,rec))
    for key, items in candidates.items():
        # Preserve the published latest-time/file-ID precedence. Within the
        # same SQL file and timestamp, prefer the copy retaining more direct
        # PII: a clean primary row must not hide a ghost in a replica table.
        def copy_risk(item):
            rec=item[1]
            table=str((rec.raw_row or {}).get("_source_table",""))
            if not table:
                # For log events sharing a second, preserve source-line order:
                # a completed 404 readback must override its started request.
                return (0,0,False,"")
            direct={hit.value_kind for hit in rec.pii_hits if hit.value_kind in {"email","name","phone","email_hash"}}
            return (len(direct),len(rec.pii_hits),rec.state_at_evidence=="PRESENT",
                    table)
        items.sort(key=lambda item: (item[1].evidence_timestamp or datetime.min, item[0].file_id, copy_risk(item))); ev, rec = items[-1]
        old = facts.get(key); notes = list(old.notes) if old else []
        if old and old.state_at_audit != rec.state_at_evidence:
            notes = [f"activity_log_said_{old.state_at_audit}, evidence_{rec.state_at_evidence}_says_{rec.state_at_evidence}", "evidence_wins_over_timeline"] + notes
        if len(items) > 1 and items[-2][1].evidence_timestamp == rec.evidence_timestamp: notes.append("same_timestamp_conflict_resolved_by_file_id")
        tables={str((candidate.raw_row or {}).get("_source_table","")) for _,candidate in items}
        if len(tables-{''})>1: notes.append("multiple_sql_copies_checked_for_replica_ghost")
        if not rec.user_ref: notes.append("unowned_absence_joined_by_exact_resource_id")
        if rec.system_id=="backup_service":
            raw=rec.raw_row or {}
            if raw.get("restore_allowed") is True: notes.append("restore_access_allowed_by_evidence")
            elif raw.get("restore_allowed") is False: notes.append("restore_access_blocked_by_evidence")
            elif str(raw.get("result") or "").upper()=="BLOCKED": notes.append("restore_access_blocked_by_evidence")
            elif str(raw.get("result") or "").upper()=="ACTIVE": notes.append("restore_access_allowed_by_evidence")
            else:
                line=str(raw.get("line", ""))
                if "| BACKUP_ARCHIVE | ACTIVE |" in line: notes.append("restore_access_allowed_by_evidence")
                elif "| BACKUP_ARCHIVE | BLOCKED |" in line: notes.append("restore_access_blocked_by_evidence")
        if rec.system_id=="integration_service" and rec.resource_id.startswith("data_flow_"):
            if rec.raw_row.get("enabled") is False: notes.append("connector_disabled_by_evidence")
            elif rec.raw_row.get("enabled") is True: notes.append("connector_enabled_by_evidence")
            elif str(rec.raw_row.get("result") or "").upper()=="DISABLED": notes.append("connector_disabled_by_evidence")
            elif str(rec.raw_row.get("result") or "").upper()=="ACTIVE": notes.append("connector_enabled_by_evidence")
        fact = ResourceFact(key[0], rec.resource_id, identity.primary_user_id or rec.user_ref, rec.state_at_evidence, {h.value_kind for h in rec.pii_hits if h.value_kind in {"email","name","phone","email_hash"}}, ev.file_id, rec.evidence_timestamp, notes)
        fact.raw_record=rec.raw_row
        facts[key]=fact
    return sorted(facts.values(), key=lambda x: (x.system_id, x.resource_id))
