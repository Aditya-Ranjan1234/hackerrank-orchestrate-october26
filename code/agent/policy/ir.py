from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class PolicyRule:
    rule_id: str; category: str; system_id: str|None; required_treatment: str
    retainable_fields: frozenset[str]=frozenset(); retention_period_days: int|None=None
    direct_identifiers: frozenset[str]=frozenset({"email","name","phone","email_hash"})
    priority: int=0; notes: str=""

@dataclass
class PolicyVerdict:
    target_kind: str; system_id: str; resource_id: str; user_id: str; required_action: str
    retainable_fields: frozenset[str]; retention_expires_at: datetime|None; current_state: str
    is_in_compliance: bool; pii_fields_to_redact: frozenset[str]
    applicable_rule_ids: list[str]; winning_rule_id: str; conflict_notes: list[str]=field(default_factory=list)

@dataclass
class SystemCategory:
    system_id: str; category: str

@dataclass
class CategoryMap:
    entries: dict[tuple[str,str],str]
    @classmethod
    def fallback_for_unknown(cls, system_id):
        return {"account_service":"account","account_service_tombstone":"account_tombstone","order_service":"orders","support_service":"support_tickets","search_service":"search_index","analytics_service":"analytics_export","analytics_platform":"analytics_export","log_service":"logs","logs":"logs","backup_service":"backup_snapshot"}.get(system_id,"unknown")
