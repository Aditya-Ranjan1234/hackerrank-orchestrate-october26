from dataclasses import dataclass
@dataclass
class Step:
 step_no:int; phase:str; system_id:str; resource_id:str; operation:str; state:str; evidence_id:str
@dataclass(frozen=True, order=True)
class StepSortKey:
 phase_order:int; operation_order:int; system_id:str; resource_id:str
