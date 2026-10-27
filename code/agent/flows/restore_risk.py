from .ir import RestoreRiskFact
from .retention import dt, get_retention_expires

class RestoreRiskAnalyzer:
    @staticmethod
    def build_risks(identity, evidence, facts, activity_rows, audit_at):
        cutoff = dt(audit_at) if isinstance(audit_at, str) else audit_at
        ids = set(identity.all_user_ids) | set(identity.all_emails)
        deletes = []
        for row in activity_rows:
            time = dt(row.get("event_time") or row.get("activity_time"))
            op = str(row.get("event_type", row.get("op_type", ""))).upper()
            if time and time <= cutoff and op == "DELETE_RECORD" and (row.get("target_system") == "account_service" or "account" in str(row.get("details", "")).casefold()) and any(x and x.casefold() in str(row.get("details", "")).casefold() for x in ids): deletes.append(time)
        deletion_time = max(deletes) if deletes else None
        result = []
        for row in activity_rows:
            op = str(row.get("event_type", row.get("op_type", ""))).upper(); backup_time = dt(row.get("event_time") or row.get("backup_time"))
            if op not in {"BACKUP", "BACKUP_RECORD", "CREATE_BACKUP"} or not backup_time or backup_time > cutoff or deletion_time is None: continue
            expiry = get_retention_expires(row); blocked = False; notes = []
            for other in activity_rows:
                ot = dt(other.get("event_time") or other.get("activity_time")); oo = str(other.get("event_type", other.get("op_type", ""))).upper()
                if other.get("resource_id") == row.get("resource_id") and ot and ot <= cutoff and oo in {"BLOCK_RESTORE", "DESTROY_KEY", "DESTROY_BACKUP"}: blocked = True
            text = str(row.get("details", "")).casefold()
            if "key_destroyed" in text or "key destroyed" in text or "key_rotated" in text: blocked = True; notes.append("key_destroyed")
            if backup_time >= deletion_time: notes.append("post_deletion_backup")
            if expiry is not None and expiry <= cutoff: notes.append("retention_expired")
            if any(str(x.get("resource_id")) == str(row.get("resource_id")) and str(x.get("event_type", x.get("op_type", ""))).upper() == "RESTORE_BACKUP" and dt(x.get("event_time") or x.get("activity_time")) and dt(x.get("event_time") or x.get("activity_time")) > cutoff for x in activity_rows): notes.append("post_audit_restore")
            result.append(RestoreRiskFact(row.get("activity_id") or f"backup_{backup_time.isoformat()}", row.get("source_system", ""), row.get("resource_id", ""), backup_time, deletion_time, expiry, blocked, backup_time < deletion_time and (expiry is None or expiry > cutoff) and not blocked, row.get("activity_id", ""), backup_time, notes))
        # A successful access check is direct evidence that a particular backup
        # remains restorable, even when the system-level log omits the older
        # BACKUP/DELETE events. Require both exact resource ownership and an
        # affirmative result; the check alone is not proof of access.
        existing={risk.resource_id for risk in result}
        for row in activity_rows:
            op=str(row.get("event_type",row.get("op_type",""))).upper()
            check_time=dt(row.get("event_time") or row.get("activity_time"))
            rid=row.get("resource_id")
            if op!="CHECK_RESTORE_ACCESS" or not rid or not check_time or check_time>cutoff or rid in existing:
                continue
            if row.get("target_user_id") not in identity.all_user_ids:
                continue
            details=str(row.get("details","")).casefold()
            affirmative=("can still be restored" in details or "restore access confirmed" in details
                         or "restore_allowed=true" in details)
            if not affirmative or any(word in details for word in ("cannot be restored","restore blocked","restore denied")):
                continue
            matching=[ev.file_id for ev in evidence for rec in ev.records
                      if rec.resource_id==rid and (rec.user_ref in ids)]
            if not matching:
                continue
            later_block=any(other.get("resource_id")==rid
                            and str(other.get("event_type",other.get("op_type",""))).upper() in {"BLOCK_RESTORE","DESTROY_KEY","DESTROY_BACKUP"}
                            and (t:=dt(other.get("event_time") or other.get("activity_time")))
                            and check_time<=t<=cutoff for other in activity_rows)
            evidence_id=sorted(matching)[-1]
            result.append(RestoreRiskFact(row.get("activity_id") or rid,
                row.get("target_system") or row.get("source_system") or "backup_service",
                rid,check_time,deletion_time,None,later_block,not later_block,
                evidence_id,check_time,["affirmative_restore_access_check"]))
            existing.add(rid)
        return sorted(result, key=lambda x: (x.system_id, x.resource_id, x.backup_time))
