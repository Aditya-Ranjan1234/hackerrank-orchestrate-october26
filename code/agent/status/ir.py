from dataclasses import dataclass
from datetime import datetime
@dataclass
class NotApplicableReason: reason_code:str; detail:str; evidence:dict
@dataclass
class IncompleteTrigger:
    target_kind:str; system_id:str; resource_id:str; required_action:str; current_state:str; trigger_kind:str; verdict_id:str
@dataclass
class StatusDecision:
    case_id:str; deletion_status:str; not_applicable_reason:NotApplicableReason|None; incomplete_triggers:list[IncompleteTrigger]; audit_trail:list[str]; decision_timestamp:datetime
