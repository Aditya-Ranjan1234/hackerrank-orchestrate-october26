import json
from types import SimpleNamespace as N

from agent.llm.semantic_resolver import SemanticResolver


class FakeLLM:
    def __init__(self,result):self.result=result;self.calls=[]
    def call(self,prompt,purpose,case_id=None):
        self.calls.append(purpose);return self.result
    def call_vision(self,prompt,path,purpose,case_id=None):
        self.calls.append(purpose);return self.result


IDENTITY=N(all_user_ids={"U1"},all_emails={"a@example.com"},primary_user_id="U1")


def test_system_id_accepts_allowlisted_high_confidence():
    resolver=SemanticResolver(FakeLLM('{"system_id":"export_service","confidence":0.9}'))
    assert resolver.infer_system_id({"id":"export_1"},"f1","a.json","json")=="export_service"


def test_system_id_rejects_unknown_or_low_confidence():
    for response in ('{"system_id":"invented","confidence":1}', '{"system_id":"export_service","confidence":0.1}'):
        assert SemanticResolver(FakeLLM(response)).infer_system_id({},"f","x","json")=="json"


def test_flow_class_schema_failure_falls_back_to_record():
    assert SemanticResolver(FakeLLM('{"other":"flow"}')).classify_flow_vs_record({},"data_flow_1")=="record"


def test_flow_class_accepts_confident_flow():
    assert SemanticResolver(FakeLLM('{"classification":"flow","confidence":0.91}')).classify_flow_vs_record({},"data_flow_1")=="flow"


def test_affiliation_requires_direct_exact_resource_join():
    resolver=SemanticResolver(FakeLLM('{"user_id":"U1","supporting_resource_id":"account_1","confidence":0.95}'))
    row={"resource_id":"account_1"}
    assert resolver.affiliate_anonymous_record(row,IDENTITY,[]) is None
    assert resolver.affiliate_anonymous_record(row,IDENTITY,[{"resource_id":"account_10","user_ref":"U1"}]) is None
    assert resolver.affiliate_anonymous_record(row,IDENTITY,[{"resource_id":"account_1","user_ref":"U1"}])=="U1"


def test_primary_file_rejects_unlisted_id_and_post_audit(tmp_path):
    case=N(case_id="c",audit_at="2026-01-02T00:00:00+00:00")
    files=[{"file_id":"early","timestamp":"2026-01-01T00:00:00+00:00"},{"file_id":"late","timestamp":"2026-01-03T00:00:00+00:00"}]
    resolver=SemanticResolver(FakeLLM('{"primary_file_id":"late","confidence":0.99}'))
    assert resolver.select_primary_evidence_file(files,case,IDENTITY)=="early"


def test_primary_file_accepts_eligible_model_choice():
    case=N(case_id="c",audit_at="2026-01-03T00:00:00+00:00")
    files=[{"file_id":"early","timestamp":"2026-01-01T00:00:00+00:00"},{"file_id":"late","timestamp":"2026-01-02T00:00:00+00:00"}]
    resolver=SemanticResolver(FakeLLM('{"primary_file_id":"early","confidence":0.95}'))
    assert resolver.select_primary_evidence_file(files,case,IDENTITY)=="early"


def test_pipeline_without_key_preserves_sample_statuses(monkeypatch):
    import csv
    from pathlib import Path
    from orchestrator.pipeline import load_datasets,run_case
    monkeypatch.setenv("OPENAI_LLM_DISABLED","1")
    root=Path(__file__).resolve().parents[2]
    datasets=load_datasets(root)
    with (root/"dataset/sample_deletion_requests.csv").open(encoding="utf-8-sig",newline="") as stream:
        cases=list(csv.DictReader(stream))
    datasets.active_case_rows=cases
    with (root/"dataset/sample_output.csv").open(encoding="utf-8-sig",newline="") as stream:
        gold={r["case_id"]:r for r in csv.DictReader(stream)}
    actual={r["case_id"]:run_case(N(**r),datasets) for r in cases}
    assert len(actual)==32
    assert all(actual[c].deletion_status==gold[c]["deletion_status"] for c in gold)
    assert all(not result.errors for result in actual.values())


def test_flow_classification_uses_visible_raw_row_only():
    from datetime import datetime, timezone
    from agent.evidence.ir import ResourceFact
    from agent.policy.engine import PolicyEngine
    class Resolver:
        def __init__(self):self.seen=[]
        def classify_flow_vs_record(self,row,rid,case_id=None):
            self.seen.append(row);return "flow"
    resolver=Resolver(); now=datetime(2026,1,1,tzinfo=timezone.utc)
    fact=ResourceFact("integration_service","data_flow_1","U1","PRESENT",set(),"e",now,[])
    fact.raw_record={"connector":"live sync","resource_id":"data_flow_1"}
    verdict=PolicyEngine([],resolver,"c").apply([fact],[],[],now,now)[0]
    assert verdict.target_kind=="flow" and resolver.seen==[fact.raw_record]
    fact.state_at_audit="ABSENT"
    PolicyEngine([],resolver,"c").apply([fact],[],[],now,now)
    assert len(resolver.seen)==1


def test_reconstructor_exposes_winning_raw_evidence_to_policy():
    from datetime import datetime,timezone
    from agent.evidence.ir import ExtractedEvidence,RecordState
    from agent.state.reconstructor import reconstruct
    now=datetime(2026,1,1,tzinfo=timezone.utc)
    row={"resource_id":"data_flow_1","connector":"live sync"}
    evidence=ExtractedEvidence("e","x","h",[RecordState("integration_service","data_flow_1","U1","PRESENT",evidence_timestamp=now,raw_row=row)],"json",now)
    assert reconstruct(IDENTITY,[evidence],[],now)[0].raw_record==row


def test_focused_vision_fallback_uses_strict_schema_and_exact_owner():
    class Vision:
        enabled=True
        def __init__(self):self.calls=[]
        def call_vision(self,prompt,path,purpose,**kwargs):
            self.calls.append((prompt,purpose,kwargs))
            return '{"records":[{"resource_id":"search_428","user_ref":"U1","state_at_evidence":"PRESENT","pii_hits":[],"visible_text":"search_428 U1"},{"resource_id":"search_429","user_ref":"U2","state_at_evidence":"PRESENT","pii_hits":[],"visible_text":"search_429 U2"}]}'
    model=Vision()
    rows=SemanticResolver(model).extract_pii_from_image("fake.png",IDENTITY,"case_x")
    assert [row["resource_id"] for row in rows]==["search_428"]
    assert model.calls[0][2]["model"]=="gpt-4o-mini"
    assert model.calls[0][2]["response_schema"]["strict"] is True


def test_focused_vision_fallback_retries_then_fails_closed():
    class BrokenVision:
        enabled=True
        def __init__(self):self.calls=0
        def call_vision(self,*args,**kwargs):self.calls+=1;return "not json"
    model=BrokenVision()
    assert SemanticResolver(model).extract_pii_from_image("fake.png",IDENTITY)==[]
    assert model.calls==2
