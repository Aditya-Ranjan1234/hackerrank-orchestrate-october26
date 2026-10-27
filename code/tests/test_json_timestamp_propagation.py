import json
import os
from datetime import datetime, timezone
from types import SimpleNamespace
from agent.evidence.handlers.json_handler import extract
from agent.evidence.ir import ExtractedEvidence
from orchestrator.activity_expander import expand_activities_for_user,lookup_activity_time_for_resource

I=SimpleNamespace(primary_user_id="U005",all_user_ids={"U005"},all_emails={"u005@example.com"})
AUDIT="2024-09-20T00:00:00Z"
def write(tmp_path, data, name="snapshot.json"):
    path=tmp_path/name; path.write_text(json.dumps(data),encoding="utf-8"); return path
def row(): return {"resource_id":"account_005","user_id":"U005","email":"u005@example.com"}

def test_json_handler_extracts_snapshot_at_field(tmp_path):
    rec=extract(write(tmp_path,{"snapshot_at":"2024-09-15T10:00:00Z","records":[row()]}),"e",I,AUDIT)[0]
    assert rec.evidence_timestamp==datetime(2024,9,15,10,tzinfo=timezone.utc)

def test_json_handler_falls_back_to_mtime_when_pre_audit(tmp_path):
    path=write(tmp_path,{"records":[row()]}); stamp=datetime(2024,9,18,tzinfo=timezone.utc).timestamp(); os.utime(path,(stamp,stamp))
    assert extract(path,"e",I,AUDIT)[0].evidence_timestamp==datetime(2024,9,18,tzinfo=timezone.utc)

def test_json_handler_rejects_post_audit_mtime(tmp_path):
    path=write(tmp_path,{"records":[row()]}); stamp=datetime(2024,9,25,tzinfo=timezone.utc).timestamp(); os.utime(path,(stamp,stamp))
    assert extract(path,"e",I,AUDIT)[0].evidence_timestamp is None

def test_json_handler_propagates_system_id_from_filename(tmp_path):
    path=write(tmp_path,{"records":[row()]},"evidence_account_service_001.json")
    rec=extract(path,"evidence_account_service_001",I,AUDIT)[0]
    assert (rec.system_id,rec.system_id_source)==("account_service","filename")

def test_json_handler_uses_activity_time_when_missing(tmp_path):
    path=write(tmp_path,{"records":[row()]}); rec=extract(path,"e",I,AUDIT)[0]
    ev=ExtractedEvidence("e",str(path),"h",[rec],"json",datetime(2026,1,1,tzinfo=timezone.utc))
    activity={"activity_id":"a1","event_time":"2024-09-15T10:00:00Z","event_type":"SYNC_RECORD","source_system":"account_service","target_system":"search_service","resource_id":"account_005","details":""}
    expand_activities_for_user([activity],[ev],I,AUDIT)
    assert rec.evidence_timestamp==datetime(2024,9,15,10,tzinfo=timezone.utc)
    assert lookup_activity_time_for_resource("account_005",[activity],AUDIT)==rec.evidence_timestamp

def test_nested_capture_time_overrides_file_export(tmp_path):
    data={"exported_at":"2024-09-25T00:00:00Z","snapshots":[{"captured_at":"2024-09-15T00:00:00Z","data_store":"account_service","records":[row()]}]}
    rec=extract(write(tmp_path,data),"e",I,AUDIT)[0]
    assert rec.evidence_timestamp==datetime(2024,9,15,tzinfo=timezone.utc) and rec.system_id=="account_service"

def test_handler_activity_time_callback(tmp_path):
    path=write(tmp_path,{"records":[row()]})
    rec=extract(path,"e",I,AUDIT,activity_time_lookup=lambda rid: "2024-09-15T10:00:00Z" if rid=="account_005" else None)[0]
    assert rec.evidence_timestamp==datetime(2024,9,15,10,tzinfo=timezone.utc)
