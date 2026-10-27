import json
from orchestrator.triage_mismatches import triage_one, classify_divergence
from orchestrator.repackage import repackage
import zipfile

def test_missing_log():
    x=triage_one('case_x',{'deletion_status':'INCOMPLETE'},{'deletion_status':'COMPLETE'},'/nonexistent')
    assert x['failing_phase']=='NO_LOG'

def test_crash_phase_reported(tmp_path):
    log=tmp_path/'case_x.jsonl'
    log.write_text(json.dumps({'phase':'state','event':'reconstruct','grounded_in':'activity.csv:id=a1','decision':'crashed','outputs':{'errors':['state_reconstruction_failed: boom']}})+'\n',encoding='utf-8')
    x=triage_one('case_x',{'deletion_status':'INCOMPLETE'},{'deletion_status':'COMPLETE'},tmp_path)
    assert x['failing_phase']=='state' and 'PIPELINE_CRASH' in x['failing_decision']

def test_divergence_types():
    assert classify_divergence('COMPLETE','INCOMPLETE')=='UNDER_DELETED'
    assert classify_divergence('NOT_APPLICABLE','COMPLETE')=='WRONG_NA'

def test_archive_excludes_environment(tmp_path):
    (tmp_path/'code').mkdir(); (tmp_path/'code'/'main.py').write_text('x=1',encoding='utf-8')
    (tmp_path/'code'/'.venv').mkdir(); (tmp_path/'code'/'.venv'/'secret.py').write_text('bad',encoding='utf-8')
    archive,count,_=repackage(tmp_path)
    with zipfile.ZipFile(archive) as z: assert z.namelist()==['code/main.py']

def test_archive_exposes_required_evaluation_path(tmp_path):
    report=tmp_path/'code/evaluation/usage_report.md'
    report.parent.mkdir(parents=True)
    report.write_text('calls: 0',encoding='utf-8')
    archive,_,_=repackage(tmp_path)
    with zipfile.ZipFile(archive) as z:
        assert 'evaluation/usage_report.md' in z.namelist()
        assert 'code/evaluation/usage_report.md' in z.namelist()


def test_archive_includes_install_manifest_but_not_credentials(tmp_path):
    (tmp_path/'code').mkdir()
    (tmp_path/'code'/'agent.py').write_text('pass',encoding='utf-8')
    (tmp_path/'requirements.txt').write_text('openai>=1.0.0\n',encoding='utf-8')
    (tmp_path/'.env').write_text('DO_NOT_PACKAGE=1\n',encoding='utf-8')
    archive,_,_=repackage(tmp_path)
    with zipfile.ZipFile(archive) as z:
        assert 'requirements.txt' in z.namelist()
        assert '.env' not in z.namelist()
