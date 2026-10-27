from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace
from agent.evidence.ir import ExtractedEvidence, RecordState
from orchestrator.activity_expander import expand_activities_for_user
from agent.evidence.handlers.log_handler import extract

def ident(): return SimpleNamespace(primary_user_id="user_43",all_user_ids={"user_43"},all_emails={"l.fontaine46@yahoo.com"})
def test_case03_log_has_absent_account_readback():
    root=Path(__file__).resolve().parents[2]
    records,_=extract(root/'dataset/evidence/logs/resource_lookup_trace_20260926_103856.log','evidence_94',ident(),'2026-09-26T11:00:00Z')
    assert any(r.resource_id=='account_7566' and r.state_at_evidence=='ABSENT' for r in records)
def test_case03_log_has_retained_security_audit_record():
    root=Path(__file__).resolve().parents[2]
    records,_=extract(root/'dataset/evidence/logs/resource_lookup_trace_20260926_103856.log','evidence_94',ident(),'2026-09-26T11:00:00Z')
    assert any(r.resource_id=='audit_record_2016' and r.system_id=='security_service' for r in records)
def test_same_system_proximity_is_not_exact_resource_ownership():
    from datetime import datetime,timezone
    at=datetime(2026,9,26,10,tzinfo=timezone.utc)
    ev=ExtractedEvidence('e','x','h',[RecordState('account_service','account_7566','user_43','ABSENT',evidence_timestamp=at)],'regex-log',at)
    activity={'activity_id':'a','event_time':'2026-09-26T10:00:01Z','event_type':'INDEX_RECORD','source_system':'account_service','target_system':'search_service','resource_id':'search_926'}
    expanded=expand_activities_for_user([activity],[ev],ident(),'2026-09-26T11:00:00Z')
    assert expanded==[activity]
    assert not any(r.get('derived') for r in expanded)
