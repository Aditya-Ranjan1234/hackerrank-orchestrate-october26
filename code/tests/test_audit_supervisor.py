import json
from types import SimpleNamespace as N

from orchestrator.audit_supervisor import PLAN_SCHEMA, review_candidates, supervise_evidence


class Planner:
    enabled = True
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []
    def call(self, prompt, purpose, **kwargs):
        self.calls.append((prompt, purpose, kwargs))
        return self.replies.pop(0)


def evidence(file_id, notes=(), records=()):
    return N(file_id=file_id, notes=list(notes), records=list(records))


def subject():
    return N(all_user_ids={"user_13"}, all_emails={"a@example.com"}, all_email_hashes=set())


def source(tmp_path, file_id, relative, text):
    path=tmp_path/"dataset"/relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return {"file_id": file_id, "file_path": relative}


def test_conflict_triggers_exact_json_inspection_and_strict_plan(tmp_path):
    left=source(tmp_path,"e1","evidence/json/a.json",'{"records":[{"resource_id":"search_7","user_id":"user_13","note":"other@example.com"}]}')
    right=source(tmp_path,"e2","evidence/json/b.json",'{"records":[{"resource_id":"search_7","user_id":"user_13","state":"ABSENT"}]}')
    records=[evidence("e1",records=[N(system_id="search_service",resource_id="search_7",user_ref="user_13",state_at_evidence="PRESENT")]),
             evidence("e2",records=[N(system_id="search_service",resource_id="search_7",user_ref="user_13",state_at_evidence="ABSENT")])]
    planner=Planner([json.dumps({"tool":"inspect_json","file_id":"e1","reason":"conflict"}),json.dumps({"tool":"stop","file_id":"","reason":"done"})])
    history=supervise_evidence("case_x",records,[left,right],subject(),tmp_path,planner)
    assert history[0]["result"]["exact_identifier_fields"]==[{"field_path":"$.records[0].user_id","field_name":"user_id","value":"user_13"}]
    assert planner.calls[0][2]["response_schema"]==PLAN_SCHEMA
    assert len(history)==1 and len(planner.calls)==2


def test_invalid_model_plan_falls_back_to_real_read_only_tool(tmp_path):
    entry=source(tmp_path,"e1","evidence/logs/a.log","2026-01-01 [account_service] user_id=user_13 resource_id=account_7\n")
    planner=Planner([json.dumps({"tool":"inspect_sql","file_id":"invented","reason":"guess"})])
    history=supervise_evidence("case_x",[evidence("e1",notes=["unsupported_extension"])],[entry],subject(),tmp_path,planner)
    assert history[0]["error"]=="rejected_unlisted_or_wrong_tool"
    assert history[1]["tool"]=="inspect_log"
    assert history[1]["result"]["identifier_line_count"]==1


def test_malformed_model_plan_uses_real_inspection_not_placeholder(tmp_path):
    entry=source(tmp_path,"e1","evidence/json/a.json",'{"user_id":"user_13"}')
    history=supervise_evidence("case_x",[evidence("e1",notes=["vision_schema_failed_after_retry"])],[entry],subject(),tmp_path,Planner(["broken"]))
    assert history[-1]["result"]["exact_identifier_count"]==1


def test_sql_inspection_maps_multiple_tables_without_guessing(tmp_path):
    entry=source(tmp_path,"db","evidence/databases/a.sql",'CREATE TABLE accounts(resource_id TEXT,user_id TEXT); INSERT INTO accounts VALUES("account_1","user_13"); CREATE TABLE search_index(resource_id TEXT,email TEXT); INSERT INTO search_index VALUES("search_2","a@example.com");')
    history=supervise_evidence("case_x",[evidence("db",notes=["missing_file"])],[entry],subject(),tmp_path,None)
    result=history[0]["result"]
    assert {row["name"] for row in result["tables"]}=={"accounts","search_index"}
    assert {row["resource_id"] for row in result["exact_owner_rows"]}=={"account_1","search_2"}


def test_missing_and_outside_path_fail_closed(tmp_path):
    entry={"file_id":"missing","file_path":"evidence/json/absent.json"}
    history=supervise_evidence("case_x",[evidence("missing",notes=["missing_file"])],[entry],subject(),tmp_path,None)
    assert history[0]["error"]=="missing_or_outside_evidence_root"
    outside={"file_id":"outside","file_path":"../outside.json"}
    history=supervise_evidence("case_x",[evidence("outside",notes=["missing_file"])],[outside],subject(),tmp_path,None)
    assert history[0]["error"]=="missing_or_outside_evidence_root"


def test_no_anomaly_no_extra_calls_and_no_fact_mutation(tmp_path):
    record=N(system_id="account_service",resource_id="account_1",user_ref="user_13",state_at_evidence="PRESENT")
    items=[evidence("e1",records=[record])]
    planner=Planner([])
    assert review_candidates(items)==[]
    assert supervise_evidence("case_x",items,[],subject(),tmp_path,planner)==[]
    assert record.state_at_evidence=="PRESENT" and planner.calls==[]
