import sys
from pathlib import Path
from types import SimpleNamespace as N
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.status.determinator import StatusDeterminator
def case(text='delete',requested='2026-01-01T00:00:00Z',audit='2026-02-01T00:00:00Z',status='COMPLETE'): return N(case_id='c',request_text=text,requested_at=requested,audit_at=audit,reported_status=status,email='a@x')
class I: primary_user_id='u'
def v(kind='record',action='DELETE_RECORD',state='PRESENT',ok=False,sys='account_service',rid='r',pii=set()): return N(target_kind=kind,required_action=action,current_state=state,is_in_compliance=ok,system_id=sys,resource_id=rid,pii_fields_to_redact=pii,winning_rule_id='v')
def decide(c=None,i=None,vs=None):
 return StatusDeterminator(lambda:datetime(2026,1,1,tzinfo=timezone.utc)).decide(c or case(),i or I(),vs or [])
def test_s1_flow():
 x=decide(vs=[v('flow','DISABLE_DATA_FLOW','ACTIVE',False)]); assert x.deletion_status=='INCOMPLETE' and x.incomplete_triggers[0].trigger_kind=='ACTIVE_DATA_FLOW'
def test_s2_restore(): assert decide(vs=[v('restore_risk','BLOCK_RESTORE','RISKY',False)]).incomplete_triggers[0].trigger_kind=='RESTORE_RISK'
def test_s3_hash(): assert decide(vs=[v('record','REDACT_RECORD','REDACTED',False,pii={'email_hash'})]).incomplete_triggers[0].trigger_kind=='EXPOSED_PII'
def test_s4_no_user():
 x=decide(case(),N(primary_user_id=None),[]); assert x.deletion_status=='NOT_APPLICABLE' and x.not_applicable_reason.reason_code=='NO_USER_ID'
def test_s5_reported_status_ignored(): assert decide(case(status='PARTIALLY_COMPLETE'),vs=[v(state='ABSENT',ok=True)]).deletion_status=='COMPLETE'
def test_s6_non_deletion(): assert decide(case('export my data')).not_applicable_reason.reason_code=='NOT_A_DELETION_REQUEST'
def test_s7_delete_with_retention_language(): assert decide(case('close my account but retain order history'),vs=[v(state='ABSENT',ok=True)]).deletion_status=='COMPLETE'
def test_s8_audit_before_request(): assert decide(case(requested='2026-02-01T00:00:00Z',audit='2026-01-01T00:00:00Z')).not_applicable_reason.reason_code=='AUDIT_BEFORE_REQUEST'
def test_s9_equal_boundary(): assert decide(case(audit='2026-01-01T00:00:00Z'),vs=[v(state='PRESENT',ok=False)]).deletion_status=='INCOMPLETE'
def test_s10_offending_user(): assert decide(vs=[v(state='ABSENT',ok=True),v(rid='bad')]).deletion_status=='INCOMPLETE'
def test_s11_empty(): assert decide(case(''),vs=[v(state='ABSENT',ok=True)]).deletion_status=='COMPLETE'
def test_s12_none_flow_not_trigger(): assert decide(vs=[v('flow','NONE','ACTIVE',False)]).deletion_status=='COMPLETE'
def test_s13_retain_missing(): assert decide(vs=[v('record','RETAIN','ABSENT',False)]).incomplete_triggers[0].trigger_kind=='RETENTION_VIOLATED'
def test_s14_redact_absent(): assert decide(vs=[v('record','REDACT_RECORD','ABSENT',False)]).incomplete_triggers[0].trigger_kind=='RETENTION_VIOLATED'
def test_s15_complete(): assert decide(vs=[v(state='ABSENT',ok=True)]).deletion_status=='COMPLETE'
def test_s16_deterministic():
 a=decide(vs=[v(state='ABSENT',ok=True)]); b=decide(vs=[v(state='ABSENT',ok=True)]); a.decision_timestamp=b.decision_timestamp; assert a==b
def test_s17_reported_complete_does_not_hide_failure(): assert decide(case(status='COMPLETE'),vs=[v()]).deletion_status=='INCOMPLETE'
def test_s18_delete_export_tie(): assert decide(case('delete and export'),vs=[v(state='ABSENT',ok=True)]).deletion_status=='COMPLETE'
