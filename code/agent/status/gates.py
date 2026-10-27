from datetime import datetime
from .ir import NotApplicableReason,IncompleteTrigger
from .request_classifier import matched_keywords
def _dt(x): return x if isinstance(x,datetime) else datetime.fromisoformat(str(x).replace('Z','+00:00'))
def not_applicable_gate(case_row,identity,request_kind_is_deletion):
 if not getattr(identity,'primary_user_id',None): return True,NotApplicableReason('NO_USER_ID',f'email={case_row.email} not found in user_identities or user_audit_log',{'email':case_row.email})
 if not request_kind_is_deletion:return True,NotApplicableReason('NOT_A_DELETION_REQUEST',f'request_text indicates non-deletion intent; keywords matched: {matched_keywords(case_row.request_text)}',{'request_text':case_row.request_text,'keywords_matched':matched_keywords(case_row.request_text)})
 if _dt(case_row.audit_at)<_dt(case_row.requested_at):return True,NotApplicableReason('AUDIT_BEFORE_REQUEST',f'audit_at={case_row.audit_at} precedes requested_at={case_row.requested_at}',{'audit_at':case_row.audit_at,'requested_at':case_row.requested_at})
 return False,None
def incomplete_triggers(verdicts):
 out=[]
 for v in verdicts:
  if v.is_in_compliance or v.required_action=='NONE':continue
  kind=None
  if v.target_kind=='record':
   if v.required_action=='DELETE_RECORD':kind='REMAINING_RECORD'
   elif v.required_action=='REDACT_RECORD':kind='EXPOSED_PII' if v.pii_fields_to_redact or v.current_state!='ABSENT' else 'RETENTION_VIOLATED'
   elif v.required_action=='ANONYMIZE_RECORD':kind='ANONYMIZATION_INCOMPLETE'
   elif v.required_action=='RETAIN':kind='RETENTION_VIOLATED'
  elif v.target_kind=='flow' and v.required_action=='DISABLE_DATA_FLOW':kind='ACTIVE_DATA_FLOW'
  elif v.target_kind=='restore_risk' and v.required_action=='BLOCK_RESTORE':kind='RESTORE_RISK'
  if kind:out.append(IncompleteTrigger(v.target_kind,v.system_id,v.resource_id,v.required_action,v.current_state,kind,getattr(v,'winning_rule_id','')))
 return sorted(out,key=lambda x:(x.target_kind,x.system_id,x.resource_id))
def complete_gate(case_row,identity,request_kind_is_deletion,triggers):
 na, _ = not_applicable_gate(case_row, identity, request_kind_is_deletion)
 return (not na and bool(getattr(identity,'primary_user_id',None)) and
         _dt(case_row.audit_at) >= _dt(case_row.requested_at) and
         not triggers and request_kind_is_deletion)
