from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json, sqlite3
from agent.evidence.handlers.json_handler import extract as jextract
from agent.evidence.handlers.sql_handler import extract as sextract
from agent.evidence.handlers.log_handler import extract as lextract
from agent.evidence.handlers.pdf_handler import extract as pextract
from agent.evidence.handlers.image_handler import vlm_extract

class I:
    all_user_ids={"user_1"}; all_emails={"a@example.com"}

def test_json_handler(tmp_path):
    p=tmp_path/"x.json"; p.write_text(json.dumps({"id":"account_1","user_id":"user_1","email":"a@example.com"}))
    assert jextract(p,"e",I())

def test_json_selector_and_lookup_are_not_record_ownership(tmp_path):
    p=tmp_path/"x.json"
    p.write_text(json.dumps({"resource_id":"account_3","subject_selector":"user_1",
                             "lookup_value":"user_1","notes":"user_1"}),encoding="utf-8")
    assert jextract(p,"e",I())==[]
    p.write_text(json.dumps({"resource_id":"account_3","subject_reference":"user_1",
                             "lookup_value":"user_1"}),encoding="utf-8")
    assert [(r.resource_id,r.user_ref) for r in jextract(p,"e",I())]==[("account_3","user_1")]
def test_sql_handler(tmp_path):
    p=tmp_path/"x.sql"; p.write_text("create table accounts (id text,user_id text,email text); insert into accounts values ('account_1','user_1','a@example.com');")
    assert sextract(p,"e",I())[0].resource_id=="account_1"
def test_log_handler_cutoff(tmp_path):
    p=tmp_path/"x.log"; p.write_text("2026-01-01T00:00:00Z [account_service] user_id=user_1 email=a@example.com\n2027-01-01T00:00:00Z [account_service] user_id=user_1 email=a@example.com")
    out,post=lextract(p,"e",I(),"2026-06-01T00:00:00Z"); assert len(out)==1 and len(post)==1
def test_pdf_no_identifiers(tmp_path):
    try:
        import reportlab.pdfgen.canvas as c
    except ImportError: return
    p=tmp_path/"x.pdf"; q=c.Canvas(str(p)); q.drawString(10,10,"nothing relevant"); q.save(); assert pextract(p,"e",I())[0]==[]
def test_image_malformed_vlm():
    def bad(*a,**k): return "not json"
    out,c,*rest=vlm_extract(Path("x.png"),I(),bad); assert out==[] and c==2
def test_cache_round_trip(tmp_path):
    from agent.evidence.cache import save,load,file_hash
    from agent.evidence.ir import ExtractedEvidence
    from datetime import datetime,timezone
    e=ExtractedEvidence("e","x","a",[],"json",datetime.now(timezone.utc)); save(tmp_path,e); assert load(tmp_path,"a").file_id=="e"
