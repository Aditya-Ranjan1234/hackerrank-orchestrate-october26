import sys,json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.steps.ir import Step
from agent.steps.serializer import to_steps_json
def test_valid():
    assert json.loads(to_steps_json([Step(1,'VERIFICATION','s','r','VERIFY_RECORD_ABSENT','ABSENT','e')]))[0]['step_no']==1
def test_compact():
    assert ' ' not in to_steps_json([Step(1,'VERIFICATION','s','r','VERIFY_RECORD_ABSENT','ABSENT','e')])
def test_empty():
    assert to_steps_json([])=='[]'
