import json
import pytest
from orchestrator.diagnostic_logger import DiagnosticLogger

def test_rejects_ungrounded_entry(tmp_path):
    with DiagnosticLogger('c1',tmp_path) as log:
        with pytest.raises(ValueError): log.log('state','reconstruct','','PRESENT',{}, {})

def test_jsonl_schema_and_citation(tmp_path):
    with DiagnosticLogger('c1',tmp_path) as log:
        log.log('identity','resolve','identities.csv:line=2','U1',{'email':'a@b.co'},{'user_id':'U1'})
        path=log.path
    entry=json.loads(path.read_text(encoding='utf-8'))
    assert entry['grounded_in']=='identities.csv:line=2' and entry['case_id']=='c1' and entry['elapsed_ms']>=0

def test_decisions_deterministic_modulo_clock(tmp_path):
    bodies=[]
    for _ in range(2):
        with DiagnosticLogger('c1',tmp_path) as log:
            log.log('state','reconstruct','activity.csv:id=a1','ABSENT',{}, {'facts':[]})
            bodies.append(json.loads(log.path.read_text(encoding='utf-8')))
    for body in bodies: body.pop('timestamp'); body.pop('elapsed_ms')
    assert bodies[0]==bodies[1]
