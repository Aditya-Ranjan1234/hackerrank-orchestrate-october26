from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from agent.evidence.cache import cache_key, load, save, file_hash
from agent.evidence.ir import ExtractedEvidence, RecordState
from agent.evidence.registry import extract_file

def i(email): return SimpleNamespace(primary_user_id=None,all_user_ids=set(),all_emails={email},all_email_hashes=set())
def source(tmp_path):
    folder=tmp_path/'dataset';folder.mkdir()
    (folder/'a.json').write_text('{"id":"account_1","email":"one@example.com"}')
    return 'a.json'
def test_different_identity_keys(): assert cache_key(b'a',i('one@example.com'))!=cache_key(b'a',i('two@example.com'))
def test_same_identity_key(): assert cache_key(b'a',i('one@example.com'))==cache_key(b'a',i('one@example.com'))
def test_different_cutoff_keys(): assert cache_key(b'a',i('one@example.com'),'2026-01-01')!=cache_key(b'a',i('one@example.com'),'2026-02-01')
def test_different_file_keys(): assert cache_key(b'a',i('one@example.com'))!=cache_key(b'b',i('one@example.com'))
def test_registry_isolates_identities(tmp_path):
    path=source(tmp_path)
    one=extract_file(tmp_path,'x',path,i('one@example.com'))
    two=extract_file(tmp_path,'x',path,i('two@example.com'))
    assert len(one.records)==1 and two.records==[]
def test_cache_hit_same_identity(tmp_path):
    path=source(tmp_path)
    first=extract_file(tmp_path,'x',path,i('one@example.com'))
    second=extract_file(tmp_path,'x',path,i('one@example.com'))
    assert first.extracted_at==second.extracted_at
