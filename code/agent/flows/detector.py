from .ir import FlowFact, FlowSchedule
from .retention import dt

OPS = {"SYNC_RECORD", "CREATE_EXPORT", "INDEX_RECORD", "IMPORT_RECORD", "SYNC", "EXPORT", "INDEX", "IMPORT"}

class FlowDetector:
    @staticmethod
    def build_flows(identity, evidence, facts, activity_rows, audit_at):
        cutoff = dt(audit_at) if isinstance(audit_at, str) else audit_at
        ids = set(identity.all_user_ids) | set(identity.all_emails)
        result = []
        for row in activity_rows:
            op = str(row.get("event_type", row.get("op_type", ""))).upper()
            timestamp = dt(row.get("event_time") or row.get("activity_time"))
            if op not in OPS or not timestamp or timestamp > cutoff: continue
            text = " ".join(str(row.get(k, "")) for k in ("details", "schedule", "event_type")).casefold()
            user_ref = next((x for x in ids if x and x.casefold() in text), None)
            if not user_ref and not any(f.user_id == identity.primary_user_id and f.resource_id == row.get("resource_id") for f in facts): continue
            kind = "cron" if "cron" in text else "fixed_rate" if "fixed_rate" in text or "interval" in text else "one_time"
            last = dt(row.get("last_run_at")) or timestamp
            next_run = dt(row.get("next_run_at"))
            disabled = False
            for other in activity_rows:
                ot = dt(other.get("event_time") or other.get("activity_time"))
                same = other.get("resource_id") == row.get("resource_id")
                if same and ot and ot <= cutoff and str(other.get("event_type", other.get("op_type", ""))).upper() in {"DISABLE_DATA_FLOW", "DISABLE", "DISABLE_FLOW"}: disabled = True
                if same and ot and ot <= cutoff and ot > timestamp and str(other.get("event_type", other.get("op_type", ""))).upper() in {"ENABLE_DATA_FLOW", "ENABLE", "ENABLE_FLOW"}: disabled = False
            recurring = kind in {"cron", "fixed_rate"} or "recurr" in text
            # A completed or unscheduled one-off transfer is not an active
            # mechanism capable of recreating data at the audit time. Activity
            # logs often omit last_run_at for their single completed event.
            active = not disabled and (recurring or (next_run is not None and next_run > cutoff))
            source = any(f.user_id == identity.primary_user_id and f.system_id == row.get("source_system") and f.state_at_audit != "ABSENT" for f in facts)
            flow_id = row.get("activity_id") or f"flow_{row.get('source_system', 'unknown')}_{row.get('target_system', 'unknown')}_{row['resource_id']}"
            result.append(FlowFact(flow_id, row.get("source_system", ""), row.get("target_system", ""), row.get("resource_id") or flow_id, user_ref or identity.primary_user_id or "", FlowSchedule(kind, last, next_run, None, disabled), active, row.get("activity_id", ""), timestamp, source, active and source, ["disabled_at_audit"] if disabled else []))
        return sorted(result, key=lambda x: (x.system_id, x.target_system_id, x.resource_id, x.flow_id))
