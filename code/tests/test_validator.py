import csv
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from orchestrator.csv_writer import write_output
from orchestrator.validator import validate_output
def req(p):p.write_text('case_id,email,requested_at,reported_status,reported_at,audit_at,request_text\ncase_1,a@x,2026-01-01T00:00:00Z,COMPLETE,,2026-01-02T00:00:00Z,delete\n')
def test_valid(tmp_path):
 q=tmp_path/'r.csv';o=tmp_path/'o.csv';req(q);write_output([('case_1','NOT_APPLICABLE','[]')],o);assert not validate_output(o,q).errors
def test_count(tmp_path):
 q=tmp_path/'r.csv';o=tmp_path/'o.csv';req(q);write_output([],o);assert validate_output(o,q).errors
def test_bad_status(tmp_path):
 q=tmp_path/'r.csv';o=tmp_path/'o.csv';req(q);o.write_text('case_id,deletion_status,steps_json\ncase_1,BAD,[]\n');assert validate_output(o,q).errors
def test_bad_json(tmp_path):
 q=tmp_path/'r.csv';o=tmp_path/'o.csv';req(q);o.write_text('case_id,deletion_status,steps_json\ncase_1,COMPLETE,x\n');assert validate_output(o,q).errors
def test_bad_state(tmp_path):
 q=tmp_path/'r.csv';o=tmp_path/'o.csv';req(q);o.write_text('case_id,deletion_status,steps_json\ncase_1,COMPLETE,"[{""step_no"":1,""phase"":""VERIFICATION"",""system_id"":""s"",""resource_id"":""r"",""operation"":""VERIFY_RECORD_ABSENT"",""state"":""PRESENT"",""evidence_id"":""e""}]"\n');assert validate_output(o,q).errors
def test_na_nonempty(tmp_path):
 q=tmp_path/'r.csv';o=tmp_path/'o.csv';req(q);o.write_text('case_id,deletion_status,steps_json\ncase_1,NOT_APPLICABLE,"[{""x"":1}]"\n');assert validate_output(o,q).errors
