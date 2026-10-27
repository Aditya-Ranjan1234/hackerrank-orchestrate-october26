from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from types import SimpleNamespace as N
from orchestrator.pipeline import run_case
def test_pipeline_case_isolated():
 d=N(resolver=N(resolve=lambda e,a:N(primary_user_id=None,all_user_ids=set(),all_emails=set())),manifest=[],activities=[],rules=[],root=Path('.'));r=run_case(N(case_id='x',email='x',audit_at='2026-01-01T00:00:00Z',requested_at='2026-01-01T00:00:00Z',request_text='export',reported_status='COMPLETE'),d);assert r.deletion_status in {'NOT_APPLICABLE','INCOMPLETE'}
def test_result_has_json():
 d=N(resolver=N(resolve=lambda e,a:N(primary_user_id=None,all_user_ids=set(),all_emails=set())),manifest=[],activities=[],rules=[],root=Path('.'));r=run_case(N(case_id='x',email='x',audit_at='2026-01-01T00:00:00Z',requested_at='2026-01-01T00:00:00Z',request_text='delete',reported_status='COMPLETE'),d);assert r.steps_json=='[]'
def test_errors_list():
 d=N(resolver=N(resolve=lambda e,a:(_ for _ in ()).throw(Exception('x'))),manifest=[],activities=[],rules=[],root=Path('.'));r=run_case(N(case_id='x',email='x',audit_at='2026-01-01T00:00:00Z',requested_at='2026-01-01T00:00:00Z',request_text='delete',reported_status='COMPLETE'),d);assert r.errors
def test_self_cases():
 from orchestrator.self_cases import self_cases
 assert len(self_cases())>=3


def test_one_bad_evidence_file_does_not_erase_other_extractions(tmp_path,monkeypatch):
 import json
 from datetime import datetime,timezone
 from agent.evidence.ir import ExtractedEvidence,RecordState
 from orchestrator import pipeline
 good=ExtractedEvidence('good','evidence/good.json','hash',
     [RecordState('account_service','account_1','U1','PRESENT')],
     'json',datetime.now(timezone.utc))
 def fake_extract(root,file_id,*args,**kwargs):
  if file_id=='bad':raise ValueError('broken SQL')
  return good
 monkeypatch.setattr(pipeline,'extract_file',fake_extract)
 datasets=N(root=tmp_path,resolver=N(resolve=lambda *_:N(primary_user_id='U1',all_user_ids={'U1'},all_emails={'a@example.com'})),
            activities=[],rules=[],manifest=[{'file_id':'bad','file_path':'evidence/bad.sql','captured_at':'2026-01-01T00:00:00Z'},
                                           {'file_id':'good','file_path':'evidence/good.json','captured_at':'2026-01-01T00:00:00Z'}],
            _llm_client=N(enabled=False))
 case=N(case_id='case_test',email='a@example.com',audit_at='2026-01-02T00:00:00Z',
        requested_at='2026-01-01T00:00:00Z',request_text='delete')
 result=run_case(case,datasets)
 assert any('evidence_extraction_failed:bad:ValueError' in message for message in result.errors)
 lines=(tmp_path/'code/.cache/diagnostics/case_test.jsonl').read_text(encoding='utf-8').splitlines()
 extracted=next(json.loads(line) for line in lines if json.loads(line)['event']=='extract_evidence')
 assert any(row['file_id']=='good' for row in extracted['outputs']['files'])


def test_skip_evidence_mode_is_marked_fatal_for_submission(tmp_path,monkeypatch):
 monkeypatch.setenv('ORCHESTRATOR_SKIP_EVIDENCE','1')
 d=N(resolver=N(resolve=lambda *_:N(primary_user_id='U1',all_user_ids={'U1'},all_emails={'a@example.com'})),
     manifest=[],activities=[],rules=[],root=tmp_path,_llm_client=N(enabled=False))
 result=run_case(N(case_id='synthetic_skip',email='a@example.com',audit_at='2026-01-02T00:00:00Z',
                   requested_at='2026-01-01T00:00:00Z',request_text='delete'),d)
 assert 'evidence_skipped_diagnostic_mode' in result.errors


def test_derived_activity_citation_resolves_to_original_source_row():
 from orchestrator.pipeline import _canonical_citation
 assert _canonical_citation('activity_5::derived_0001_for_U1',{'activity_5'})=='activity_5'
 assert _canonical_citation('activity_5::derived_0001_for_U1',set())==''
 assert _canonical_citation('evidence_3',{'activity_5'})=='evidence_3'
