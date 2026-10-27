from datetime import datetime
from .ir import PolicyVerdict, PolicyRule
from .category_map import category_for, RECORD_TYPE_TO_CATEGORY
from .conflict_resolver import resolve
from .retention_evaluator import has_retention_expired

class PolicyEngine:
    def __init__(self,rules,llm_resolver=None,case_id=None):
        self.rules=list(rules); self.llm_resolver=llm_resolver; self.case_id=case_id
    @classmethod
    def from_csv(cls,path):
        from .rules_loader import load_rules
        return cls(load_rules(path))
    def _record(self,f,requested_at,audit_at):
        cat=category_for(f.system_id,f.resource_id)
        raw=getattr(f,"raw_record",None) or {}
        explicit=str(raw.get("data_category") or raw.get("category") or raw.get("record_type") or "").upper()
        cat=RECORD_TYPE_TO_CATEGORY.get(explicit,cat)
        if (explicit=="SUPPORT_ATTACHMENT" or raw.get("document_kind")=="support_attachment"
                or (raw.get("collection_name") or raw.get("collection"))=="ticket_attachments"
                or raw.get("storage_class")=="ticket_attachment"):
            cat="support_attachment"
        elif explicit=="SUPPORT_MESSAGE":
            cat="support_tickets"
        elif raw.get("trace_source")=="legacy_contact_index" or "event=contact_lookup_completed" in str(raw.get("line","")):
            # An indexed contact lookup is a secondary identifier, not an
            # analytics profile or a retained support conversation.
            cat="account"
        applicable=[r for r in self.rules if r.category==cat and (r.system_id is None or r.system_id==f.system_id)]
        if cat=="legal_hold":
            # Rule 13 applies only while a supplied hold is active. A row whose
            # explicit retention date has passed must not be kept forever.
            until=raw.get("retained_until")
            if until:
                try: expired=datetime.fromisoformat(str(until).replace("Z","+00:00"))<=audit_at
                except (ValueError,TypeError): expired=False
                if expired: applicable=[r for r in applicable if r.rule_id!="rule_13"]
            if raw.get("hold_active") is False:
                applicable=[r for r in applicable if r.rule_id!="rule_13"]
        if f.system_id=="security_service" and f.resource_id.startswith("audit_record_"):
            applicable=[r for r in applicable if r.rule_id=="rule_12"]
        winner,notes=resolve(applicable,cat); ids=[r.rule_id for r in applicable]; user=f.user_id; state=f.state_at_audit; pii=set(f.direct_pii_present)
        if winner is None:return PolicyVerdict("record",f.system_id,f.resource_id,user,"DELETE_RECORD",frozenset(),None,state,state=="ABSENT",frozenset(),ids,"",notes)
        expiry=None; action=winner.required_treatment; retain=winner.retainable_fields; red=frozenset(pii & set(winner.direct_identifiers))
        if cat=="account_tombstone": action="REDACT"; retain=frozenset(set(retain)|{"user_id"}); compliant=not red and state in {"REDACTED","TOMBSTONE"}
        elif action=="DELETE": compliant=state=="ABSENT"
        elif action=="REDACT": compliant=not red and state=="REDACTED"
        elif action=="ANONYMIZE": compliant=state=="ANONYMIZED"
        else:
            expiry=requested_at + __import__("datetime").timedelta(days=winner.retention_period_days) if winner.retention_period_days is not None else None
            if has_retention_expired(winner,requested_at,audit_at): action="DELETE"; compliant=state=="ABSENT"; notes.append("retention_expired_upgraded_to_delete")
            else: compliant=state=="PRESENT"
        mapping={"DELETE":"DELETE_RECORD","REDACT":"REDACT_RECORD","ANONYMIZE":"ANONYMIZE_RECORD","RETAIN":"RETAIN"}
        return PolicyVerdict("record",f.system_id,f.resource_id,user,mapping[action],frozenset(retain),expiry,state,compliant,red,ids,winner.rule_id,notes)
    def apply(self,records=(),flows=(),restore_risks=(),requested_at=None,audit_at=None):
        requested_at=requested_at if isinstance(requested_at,datetime) else datetime.fromisoformat(str(requested_at).replace("Z","+00:00"))
        audit_at=audit_at if isinstance(audit_at,datetime) else datetime.fromisoformat(str(audit_at).replace("Z","+00:00"))
        out=[]
        selected_risks={}
        for risk in restore_risks:
            key=(risk.system_id,risk.resource_id)
            previous=selected_risks.get(key)
            if previous is None or (risk.evidence_timestamp or risk.backup_time) > (previous.evidence_timestamp or previous.backup_time):
                selected_risks[key]=risk
        risk_keys=set(selected_risks)
        for f in records:
            if (f.system_id,f.resource_id) in risk_keys and f.system_id=="backup_service":
                # One backup has one restore obligation, even when both a
                # snapshot row and an access-check activity describe it.
                continue
            restore_signal=next((n for n in f.notes if n in {"restore_access_allowed_by_evidence","restore_access_blocked_by_evidence"}),None)
            connector_signal=next((n for n in f.notes if n in {"connector_enabled_by_evidence","connector_disabled_by_evidence"}),None)
            inferred_flow=False
            if (self.llm_resolver is not None and f.system_id=="integration_service"
                    and f.resource_id.startswith("data_flow_") and connector_signal is None
                    and f.state_at_audit=="PRESENT" and getattr(f,"raw_record",None)):
                inferred_flow=self.llm_resolver.classify_flow_vs_record(
                    f.raw_record,f.resource_id,case_id=self.case_id)=="flow"
            if f.system_id=="integration_service" and f.resource_id.startswith("data_flow_") and (connector_signal or inferred_flow):
                disabled=connector_signal=="connector_disabled_by_evidence"
                out.append(PolicyVerdict("flow",f.system_id,f.resource_id,f.user_id,"DISABLE_DATA_FLOW",frozenset(),None,"INACTIVE" if disabled else "ACTIVE",disabled,frozenset(),["flow_default"],"flow_default",[connector_signal or "llm_flow_classification"]))
            elif f.system_id=="backup_service" and restore_signal:
                blocked=restore_signal=="restore_access_blocked_by_evidence"
                out.append(PolicyVerdict("restore_risk",f.system_id,f.resource_id,f.user_id,"BLOCK_RESTORE",frozenset(),None,"BLOCKED" if blocked else "RISKY",blocked,frozenset(),["rule_14"],"rule_14",[restore_signal]))
            else: out.append(self._record(f,requested_at,audit_at))
        for f in flows:
            active=f.is_active_at_audit and f.can_recreate_at_audit; out.append(PolicyVerdict("flow",f.system_id,f.resource_id,f.user_ref,"DISABLE_DATA_FLOW" if active else "NONE",frozenset(),None,"ACTIVE" if f.is_active_at_audit else "INACTIVE",not active,frozenset(),["flow_default"],"flow_default",[]))
        for key in sorted(selected_risks):
            r=selected_risks[key]
            out.append(PolicyVerdict("restore_risk",r.system_id,r.resource_id,"","BLOCK_RESTORE" if r.is_risk_at_audit else "NONE",frozenset(),None,"RISKY" if r.is_risk_at_audit else "BLOCKED",(not r.is_risk_at_audit) or r.is_blocked,frozenset(),["restore_risk_default"],"restore_risk_default",[]))
        return out
