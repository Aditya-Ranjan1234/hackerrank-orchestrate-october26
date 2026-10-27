import sys
from pathlib import Path
from types import SimpleNamespace as N
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.steps.builder import StepBuilder
def verdict(action='DELETE_RECORD',ok=False,r='r',e='e'):
    return N(system_id='s',resource_id=r,required_action=action,is_in_compliance=ok,evidence_id=e,winning_rule_id='v',current_state='PRESENT')
def trigger(kind,action='DELETE_RECORD'):
    return N(trigger_kind=kind,system_id='s',resource_id='r',required_action=action,current_state='PRESENT',verdict_id='v')
def test_complete_delete(): assert StepBuilder.build_complete(N(),[verdict(ok=True)])[0].operation=='VERIFY_RECORD_ABSENT'
def test_complete_none(): assert StepBuilder.build_complete(N(),[verdict('NONE',True)])==[]
def test_remaining(): assert StepBuilder.build_incomplete(N(incomplete_triggers=[trigger('REMAINING_RECORD')]),[verdict()])[0].operation=='REPORT_REMAINING_RECORD'
def test_redact(): assert any(x.operation=='REDACT_RECORD' for x in StepBuilder.build_incomplete(N(incomplete_triggers=[trigger('EXPOSED_PII','REDACT_RECORD')]),[verdict('REDACT_RECORD')]))
def test_anonymize(): assert any(x.operation=='ANONYMIZE_RECORD' for x in StepBuilder.build_incomplete(N(incomplete_triggers=[trigger('ANONYMIZATION_INCOMPLETE','ANONYMIZE_RECORD')]),[verdict('ANONYMIZE_RECORD')]))
def test_retention(): assert [x.operation for x in StepBuilder.build_incomplete(N(incomplete_triggers=[trigger('RETENTION_VIOLATED','RETAIN')]),[verdict('RETAIN')])]==['VERIFY_RECORD_PRESENT']
def test_na(): assert StepBuilder.build_not_applicable()==[]
def test_evidence_required():
    try: StepBuilder.build_complete(N(),[verdict(ok=True,e='')]); assert False
    except ValueError: assert True
