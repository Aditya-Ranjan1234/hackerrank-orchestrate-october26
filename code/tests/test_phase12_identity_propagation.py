from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
import pytest
from agent.evidence.handlers import json_handler, sql_handler, log_handler, pdf_handler
from agent.evidence.registry import extract_file

FIXTURE=Path(__file__).parent/'fixtures/phase12/identity.json'
AUDIT=datetime(2026,9,16,tzinfo=timezone.utc)
def ident(ids=(),emails=(),hashes=()):
    return SimpleNamespace(all_user_ids=set(ids),all_emails=set(emails),all_email_hashes=set(hashes),primary_user_id=next(iter(ids),None))

def test_json_email_only():
    assert len(json_handler.extract(FIXTURE,'sample',ident(emails={'person@example.com'}),AUDIT))==1
def test_json_hash_only():
    assert len(json_handler.extract(FIXTURE,'sample',ident(ids={'user_1'},hashes={'abc123'}),AUDIT))==1
def test_json_no_match():
    assert json_handler.extract(FIXTURE,'sample',ident(emails={'nobody@example.com'}),AUDIT)==[]
def test_json_id_and_email_one_record():
    assert len(json_handler.extract(FIXTURE,'sample',ident(ids={'user_1'},emails={'person@example.com'}),AUDIT))==1
def test_json_no_audit_cutoff():
    assert len(json_handler.extract(FIXTURE,'sample',ident(emails={'person@example.com'}),None))==1
def test_json_post_audit_rejected():
    assert json_handler.extract(FIXTURE,'sample',ident(emails={'person@example.com'}),datetime(2026,9,14,tzinfo=timezone.utc))==[]
def test_sql_email_and_hash(tmp_path):
    p=tmp_path/'a.sql';p.write_text("CREATE TABLE accounts(id TEXT,email_hash TEXT,contact_email TEXT); INSERT INTO accounts VALUES ('account_1','abc123','person@example.com');")
    assert len(sql_handler.extract(p,'a',ident(emails={'person@example.com'})))==1
    assert len(sql_handler.extract(p,'a',ident(hashes={'abc123'})))==1
def test_log_service_trace(tmp_path):
    p=tmp_path/'a.log';p.write_text('2026-09-15T00:00:00Z service=support_platform trace_id=t1 event=lookup_started lookup_key=person@example.com\n2026-09-15T00:00:01Z service=support_platform trace_id=t1 event=lookup_completed resource_id=support_1 rows=1')
    records,_=log_handler.extract(p,'a',ident(emails={'person@example.com'}),AUDIT)
    assert any(r.resource_id=='support_1' for r in records)
def test_log_pipe_row(tmp_path):
    p=tmp_path/'a.txt';p.write_text('- 2026-09-15T00:00:00Z | account_service | account_1 | USER_PROFILE | FOUND | person@example.com')
    records,_=log_handler.extract(p,'a',ident(emails={'person@example.com'}),AUDIT)
    assert records[0].system_id=='account_service'
def test_registry_passes_email(tmp_path):
    p=tmp_path/'dataset';p.mkdir();(p/'a.json').write_bytes(FIXTURE.read_bytes())
    e=extract_file(tmp_path,'sample','a.json',ident(emails={'person@example.com'}),AUDIT)
    assert len(e.records)==1
