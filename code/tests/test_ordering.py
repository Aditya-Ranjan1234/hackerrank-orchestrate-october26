import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.steps.ir import Step
from agent.steps.ordering import sort_steps
STATES={'REPORT_REMAINING_RECORD':'PRESENT','DELETE_RECORD':'ABSENT','VERIFY_RECORD_ABSENT':'ABSENT'}
def step(phase,op,r='r'):
    return Step(0,phase,'s',r,op,STATES[op],'e')
def test_phase_order():
    assert [x.phase for x in sort_steps([step('VERIFICATION','VERIFY_RECORD_ABSENT'),step('FINDING','REPORT_REMAINING_RECORD')])] == ['FINDING','VERIFICATION']
def test_numbers():
    assert [x.step_no for x in sort_steps([step('FINDING','REPORT_REMAINING_RECORD'),step('REMEDIATION','DELETE_RECORD')])] == [1,2]
def test_stable_collision():
    x=sort_steps([step('FINDING','REPORT_REMAINING_RECORD','a'),step('FINDING','REPORT_REMAINING_RECORD','a')]); assert x[0].step_no==1
def test_invalid_state():
    try: sort_steps([Step(0,'FINDING','s','r','REPORT_REMAINING_RECORD','ABSENT','e')]); assert False
    except ValueError: assert True
