from .builder import StepBuilder
from .ordering import sort_steps
class StepGenerator:
 @staticmethod
 def generate(case_row,decision,verdicts):
  if decision.deletion_status=="NOT_APPLICABLE": raw=StepBuilder.build_not_applicable()
  elif decision.deletion_status=="COMPLETE":raw=StepBuilder.build_complete(decision,verdicts)
  elif decision.deletion_status=="INCOMPLETE":raw=StepBuilder.build_incomplete(decision,verdicts)
  else:raise ValueError(f"unknown deletion_status: {decision.deletion_status}")
  return sort_steps(raw)
