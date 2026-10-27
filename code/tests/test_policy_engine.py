from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.policy.engine import PolicyEngine
from agent.policy.ir import PolicyRule
from agent.evidence.ir import ResourceFact
from agent.flows.ir import FlowFact,FlowSchedule,RestoreRiskFact
def rec(system='account_service',state='PRESENT',pii=frozenset()): return ResourceFact(system,'r','u',state,set(pii),'e',None,[])
def eng(cat,act,days=None): return PolicyEngine([PolicyRule('x',cat,None,act,retention_period_days=days)])
def test_p1_retention_expiry():
 v=eng('account','RETAIN',0).apply([rec(state='PRESENT')],requested_at='2026-01-01T00:00:00Z',audit_at='2026-01-02T00:00:00Z')[0]; assert v.required_action=='DELETE_RECORD' and not v.is_in_compliance
def test_p4_tombstone_hash():
 v=eng('account_tombstone','REDACT').apply([rec('account_service_tombstone','REDACTED',{'email_hash'})],requested_at='2026-01-01T00:00:00Z',audit_at='2026-01-02T00:00:00Z')[0]; assert v.pii_fields_to_redact=={'email_hash'} and not v.is_in_compliance
def test_p5_redacted_tombstone():
 v=eng('account_tombstone','REDACT').apply([rec('account_service_tombstone','REDACTED')],requested_at='2026-01-01T00:00:00Z',audit_at='2026-01-02T00:00:00Z')[0]; assert v.is_in_compliance and v.required_action=='REDACT_RECORD'
def test_p6_fail_closed():
 v=eng('unmapped','RETAIN').apply([rec('unmapped','PRESENT')],requested_at='2026-01-01T00:00:00Z',audit_at='2026-01-02T00:00:00Z')[0]; assert v.required_action=='DELETE_RECORD' and 'no_matching_rule' in v.conflict_notes[0]
def test_p7_retain_absent():
 v=eng('account','RETAIN').apply([rec(state='ABSENT')],requested_at='2026-01-01T00:00:00Z',audit_at='2026-01-02T00:00:00Z')[0]; assert not v.is_in_compliance and v.required_action=='RETAIN'
def test_p8_flow_no_source():
 f=FlowFact('f','account_service','search','r','u',FlowSchedule(),True,'e',None,False,False); v=eng('account','DELETE').apply(flows=[f],requested_at='2026-01-01T00:00:00Z',audit_at='2026-01-02T00:00:00Z')[0]; assert v.required_action=='NONE'
def test_p9_zero_retention_boundary():
 v=eng('account','RETAIN',0).apply([rec(state='ABSENT')],requested_at='2026-01-01T00:00:00Z',audit_at='2026-01-01T00:00:00Z')[0]; assert v.required_action=='DELETE_RECORD'
def test_restore_blocked_compliance():
 r=RestoreRiskFact('b','backup_service','b',__import__('datetime').datetime.fromisoformat('2026-01-01T00:00:00+00:00'),None,None,True,False,'e',None,[]); v=eng('backup_snapshot','RETAIN').apply(restore_risks=[r],requested_at='2026-01-01T00:00:00Z',audit_at='2026-01-02T00:00:00Z')[0]; assert v.required_action=='NONE' and v.is_in_compliance
def test_deterministic():
 args=dict(records=[rec(state='ABSENT')],requested_at='2026-01-01T00:00:00Z',audit_at='2026-01-02T00:00:00Z'); assert eng('account','DELETE').apply(**args)==eng('account','DELETE').apply(**args)

def test_support_attachment_uses_delete_rule_not_message_redaction():
 f=rec('support_platform'); f.raw_record={'data_category':'SUPPORT_ATTACHMENT'}
 rules=[PolicyRule('message','support_tickets',None,'REDACT'),PolicyRule('attachment','support_attachment',None,'DELETE')]
 verdict=PolicyEngine(rules).apply([f],requested_at='2026-01-01T00:00:00Z',audit_at='2026-01-02T00:00:00Z')[0]
 assert verdict.required_action=='DELETE_RECORD' and verdict.winning_rule_id=='attachment'

def test_hashed_contact_lookup_is_secondary_identifier_not_analytics_profile():
 f=rec('analytics_platform'); f.raw_record={'line':'event=contact_lookup_completed correlation_key=abc'}
 rules=[PolicyRule('profile','analytics_export',None,'ANONYMIZE'),PolicyRule('identifier','account',None,'DELETE')]
 verdict=PolicyEngine(rules).apply([f],requested_at='2026-01-01T00:00:00Z',audit_at='2026-01-02T00:00:00Z')[0]
 assert verdict.required_action=='DELETE_RECORD' and verdict.winning_rule_id=='identifier'

def test_backup_snapshot_and_restore_risk_emit_one_obligation():
 from datetime import datetime,timezone
 at=datetime(2026,1,1,tzinfo=timezone.utc)
 record=ResourceFact('backup_service','backup_1','u','PRESENT',set(),'ev',at,[])
 risk=RestoreRiskFact('backup_1','backup_service','backup_1',at,None,None,False,True,'ev',at,[])
 verdicts=eng('backup_snapshot','RETAIN').apply([record],restore_risks=[risk],requested_at=at,audit_at=at)
 assert len(verdicts)==1 and verdicts[0].required_action=='BLOCK_RESTORE'
