import sys
from pathlib import Path
from types import SimpleNamespace as N
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.steps.generator import StepGenerator
from agent.steps.serializer import to_steps_json
def verdict(action='DELETE_RECORD',ok=False,r='r',e='e'):
    return N(system_id='s',resource_id=r,required_action=action,is_in_compliance=ok,evidence_id=e,winning_rule_id='v',current_state='PRESENT')
def trigger(kind,action='DELETE_RECORD',r='r'):
    return N(trigger_kind=kind,system_id='s',resource_id=r,required_action=action,current_state='PRESENT',verdict_id='v')
def decision(status,triggers=None): return N(deletion_status=status,incomplete_triggers=triggers or [])
def test_na(): assert to_steps_json(StepGenerator.generate(None,decision('NOT_APPLICABLE'),[]))=='[]'
def test_empty_complete(): assert StepGenerator.generate(None,decision('COMPLETE'),[])==[]
def test_retention(): assert StepGenerator.generate(None,decision('INCOMPLETE',[trigger('RETENTION_VIOLATED','RETAIN')]),[verdict('RETAIN')])[0].operation=='VERIFY_RECORD_PRESENT'
def test_mix(): assert len(StepGenerator.generate(None,decision('INCOMPLETE',[trigger('REMAINING_RECORD'),trigger('ACTIVE_DATA_FLOW','DISABLE_DATA_FLOW','r2')]),[verdict(),verdict('DISABLE_DATA_FLOW',False,'r2')]))==6
def test_numbers(): assert [x.step_no for x in StepGenerator.generate(None,decision('INCOMPLETE',[trigger('REMAINING_RECORD')]),[verdict()])]==[1,2,3]
def test_deterministic():
    a=to_steps_json(StepGenerator.generate(None,decision('INCOMPLETE',[trigger('REMAINING_RECORD')]),[verdict()])); b=to_steps_json(StepGenerator.generate(None,decision('INCOMPLETE',[trigger('REMAINING_RECORD')]),[verdict()])); assert a==b
def test_evidence_rules():
    x=StepGenerator.generate(None,decision('INCOMPLETE',[trigger('REMAINING_RECORD')]),[verdict()]); assert x[0].evidence_id=='e' and all(y.evidence_id=='' for y in x[1:])
def test_pairing():
    x=StepGenerator.generate(None,decision('INCOMPLETE',[trigger('REMAINING_RECORD')]),[verdict()]); assert x[1].operation=='DELETE_RECORD' and x[2].operation=='VERIFY_RECORD_ABSENT'
def test_none_skipped(): assert StepGenerator.generate(None,decision('COMPLETE'),[verdict('NONE',True)])==[]
def test_large():
    ts=[trigger('REMAINING_RECORD',r=str(i)) for i in range(20)]; vs=[verdict(r=str(i)) for i in range(20)]; assert len(StepGenerator.generate(None,decision('INCOMPLETE',ts),vs))==60
