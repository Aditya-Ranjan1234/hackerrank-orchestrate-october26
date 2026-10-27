import csv
from types import SimpleNamespace
from orchestrator.gold_validation import validate_against_gold

def setup(tmp_path):
    d=tmp_path/'dataset';d.mkdir()
    for name,rows in [('sample_output.csv',[{'case_id':'case_1','deletion_status':'COMPLETE','steps_json':'[]'},{'case_id':'case_2','deletion_status':'INCOMPLETE','steps_json':'[]'}]),('sample_deletion_requests.csv',[{'case_id':'case_1'},{'case_id':'case_2'}])]:
        with (d/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def test_status_accuracy(tmp_path):
    setup(tmp_path);r=validate_against_gold(tmp_path,run=lambda c,d:SimpleNamespace(deletion_status='COMPLETE',steps_json='[]',errors=[]),write=False)
    assert r.status_correct==1 and r.total==2
def test_pipeline_crash_isolated(tmp_path):
    setup(tmp_path)
    def run(c,d):
        if c.case_id=='case_1': raise RuntimeError('boom')
        return SimpleNamespace(deletion_status='INCOMPLETE',steps_json='[]',errors=[])
    r=validate_against_gold(tmp_path,run=run,write=False)
    assert r.status_correct==1 and r.divergences[0]['type']=='PIPELINE_CRASH'
def test_steps_exact(tmp_path):
    setup(tmp_path);r=validate_against_gold(tmp_path,run=lambda c,d:SimpleNamespace(deletion_status='INCOMPLETE',steps_json='[]',errors=[]),write=False)
    assert r.steps_correct==2
