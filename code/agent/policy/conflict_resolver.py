from .ir import PolicyRule
ORDER={"DELETE":4,"ANONYMIZE":3,"REDACT":2,"RETAIN":1}
def resolve(rules,category):
    if not rules:return None,["no_matching_rule_fail_closed_to_delete"]
    notes=[f"single_applicable_rule={rules[0].rule_id}"] if len(rules)==1 else []
    def key(r): return (1 if category=="account_tombstone" and r.category=="account_tombstone" else 0,1 if r.system_id else 0,ORDER.get(r.required_treatment,0),r.priority,-(r.retention_period_days if r.retention_period_days is not None else 10**9),-ord(r.rule_id[0]) if r.rule_id else 0)
    winner=sorted(rules,key=lambda r:(key(r),r.rule_id),reverse=True)[0]
    if len(rules)>1:notes.append("conflict_resolved_by_precedence="+winner.rule_id)
    return winner,notes
