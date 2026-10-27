from datetime import datetime,timezone
from .ir import StatusDecision
from .request_classifier import is_deletion_request
from .gates import not_applicable_gate,incomplete_triggers,complete_gate
class StatusDeterminator:
 def __init__(self,clock=None): self.clock=clock or (lambda:datetime.now(timezone.utc))
 def decide(self,case_row,identity,verdicts):
  trail=[]; deletion=is_deletion_request(case_row.request_text); trail.append(f'request_classifier: deletion_intent={deletion}')
  na,reason=not_applicable_gate(case_row,identity,deletion)
  if na: trail.append(f'not_applicable_gate: TRIGGERED reason={reason.reason_code}'); return StatusDecision(case_row.case_id,'NOT_APPLICABLE',reason,[],trail,self.clock())
  trail.append('not_applicable_gate: PASSED'); triggers=incomplete_triggers(verdicts); trail.append(f'incomplete_triggers: count={len(triggers)}')
  if triggers: trail.append('decision: INCOMPLETE'); return StatusDecision(case_row.case_id,'INCOMPLETE',None,triggers,trail,self.clock())
  if complete_gate(case_row,identity,deletion,triggers): trail.append('decision: COMPLETE'); return StatusDecision(case_row.case_id,'COMPLETE',None,[],trail,self.clock())
  trail.append('decision: FALLBACK_INCOMPLETE (unreachable branch hit)'); return StatusDecision(case_row.case_id,'INCOMPLETE',None,[],trail,self.clock())
