from datetime import datetime, timezone, timedelta
from types import SimpleNamespace as N
from agent.evidence.ir import ExtractedEvidence, RecordState
from orchestrator.activity_expander import expand_activities_for_user

I=N(all_user_ids={"U1","U2"},all_emails={"u1@example.com","u2@example.com"},primary_user_id="U1")
def ev(resource="r1", system="account_service", user="U1", ts="2026-01-01T12:00:00+00:00"):
    t=datetime.fromisoformat(ts); rec=RecordState(system,resource,user,"PRESENT",[],t,{})
    return ExtractedEvidence("e1","x","h",[rec],"json",t)
def act(op="SYNC", resource="r0", system="account_service", t="2026-01-01T12:00:00+00:00", target=None):
    return {"activity_id":"a1","event_time":t,"event_type":op,"source_system":system,"target_system":"search_index","resource_id":resource,"target_user_id":target,"details":""}
def go(rows, evidence, **kw): return expand_activities_for_user(rows,evidence,I,datetime(2026,1,2,tzinfo=timezone.utc),**kw)
def derived(xs): return [x for x in xs if x.get("derived")]
def test_i1_sync_proximity(): assert not derived(go([act()], [ev()]))
def test_i2_backup_proximity(): assert not derived(go([act("BACKUP")], [ev()]))
def test_i3_resource_match(): assert derived(go([act("BACKUP","r1")], [ev("r1")]))[0]["inference_method"]=="resource_id_match"
def test_i4_delete_proximity(): assert not derived(go([act("DELETE")], [ev()]))
def test_i5_known_target_passthrough(): assert not derived(go([act(target="U1")], [ev()]))
def test_i6_no_evidence(): assert not derived(go([act()], []))
def test_i7_multiple_users(): assert len(derived(go([act(resource="r1")], [ev(user="U1"),ev("r1",user="U2")])))==2
def test_i8_window(): assert not derived(go([act()], [ev(ts="2026-01-04T12:00:00+00:00")], time_window=timedelta(hours=1)))
def test_i9_precedence(): assert [x["inference_method"] for x in derived(go([act("BACKUP","r1")],[ev("r1")]))]==["resource_id_match"]
def test_i10_deterministic(): assert go([act()], [ev()])==go([act()], [ev()])
def test_i11_original_preserved():
    rows=[act(resource="r1")]; out=go(rows,[ev()]); assert out[0]==rows[0] and len(out)==2
def test_i12_audit_cutoff(): assert not derived(expand_activities_for_user([act()], [ev(ts="2026-01-03T00:00:00+00:00")], I, datetime(2026,1,2,tzinfo=timezone.utc)))

def test_p14_e1_no_unowned_same_system(): assert not derived(go([act(resource="other")],[ev(resource="r1")]))
def test_p14_e2_exact_resource(): assert derived(go([act(resource="r1")],[ev(resource="r1")]))[0]["inference_method"]=="resource_id_match"
def test_p14_e3_wrong_user_no_derivation(): assert not derived(go([act(resource="r1")],[ev(resource="r1",user="someone_else")]))
def test_p14_e4_explicit_file_id_match():
    evidence=ev(resource="record_inside_file"); evidence.file_id="evidence_r1"
    assert len(derived(go([act(resource="r1")],[evidence])))==1
def test_p14_e5_duplicate_evidence_dedup(): assert len(derived(go([act(resource="r1")],[ev(resource="r1"),ev(resource="r1")])))==1
def test_p14_e6_deterministic(): assert go([act(resource="r1")],[ev(resource="r1")])==go([act(resource="r1")],[ev(resource="r1")])
def test_p14_e7_no_method2_even_zero_window(): assert not derived(go([act(resource="r0")],[ev(resource="r1")],time_window=timedelta(0)))
def test_p14_e8_other_target_not_derived(): assert not derived(go([act(resource="r1",target="other")],[ev(resource="r1")]))
def test_p14_e9_pre_audit_exact_match(): assert len(derived(go([act(resource="r1")],[ev(resource="r1")])))==1
def test_p14_e10_post_audit_evidence_excluded(): assert not derived(go([act(resource="r1")],[ev(resource="r1",ts="2026-01-03T00:00:00+00:00")]))

def test_explicit_source_resource_id_joins_parent_activity():
    child=ev(resource="search_1",system="search_service")
    child.records[0].raw_row={"source_resource_id":"account_1"}
    out=derived(go([act("DELETE_RECORD",resource="account_1")],[child]))
    assert len(out)==1 and out[0]["inference_method"]=="explicit_reference_match"

def test_explicit_source_reference_requires_full_id_and_owner():
    child=ev(resource="search_1",system="search_service")
    child.records[0].raw_row={"source_resource_id":"account_10"}
    assert not derived(go([act("DELETE_RECORD",resource="account_1")],[child]))
    child.records[0].user_ref="someone_else"
    assert not derived(go([act("DELETE_RECORD",resource="account_10")],[child]))

def test_p15_nested_document_inherits_visible_parent_resource_id(tmp_path):
    from agent.evidence.handlers.json_handler import extract
    p=tmp_path/"nested.json"
    p.write_text('{"snapshots":[{"data_store":"search_service","captured_at":"2026-01-01T12:00:00Z","records":[{"resource_id":"search_1993","document":{"email":"u1@example.com","customer_reference":"U1"}}]}]}')
    records=extract(p,"e_nested",I,datetime(2026,1,2,tzinfo=timezone.utc))
    assert [(r.system_id,r.resource_id) for r in records]==[("search_service","search_1993")]

def test_p15_nested_explicit_id_overrides_parent_resource_id(tmp_path):
    from agent.evidence.handlers.json_handler import extract
    p=tmp_path/"nested.json"
    p.write_text('{"resource_id":"parent_1","child":{"resource_id":"child_2","email":"u1@example.com","user_id":"U1"}}')
    records=extract(p,"e_nested",I,datetime(2026,1,2,tzinfo=timezone.utc))
    assert [r.resource_id for r in records]==["child_2"]

def test_p15_incomplete_case_also_verifies_compliant_resources():
    from agent.steps.builder import StepBuilder
    failed=N(system_id="search_service",resource_id="search_1",winning_rule_id="r1",required_action="DELETE_RECORD",is_in_compliance=False,evidence_id="e1")
    compliant=N(system_id="account_service",resource_id="account_2",winning_rule_id="r2",required_action="DELETE_RECORD",is_in_compliance=True,evidence_id="e2")
    trigger=N(system_id="search_service",resource_id="search_1",verdict_id="r1",trigger_kind="REMAINING_RECORD")
    steps=StepBuilder.build_incomplete(N(incomplete_triggers=[trigger]),[failed,compliant])
    assert [(s.phase,s.resource_id,s.operation,s.evidence_id) for s in steps if s.phase=="VERIFICATION"]==[("VERIFICATION","search_1","VERIFY_RECORD_ABSENT",""),("VERIFICATION","account_2","VERIFY_RECORD_ABSENT","")]

def test_p15_incomplete_compliant_verification_is_deduplicated():
    from agent.steps.builder import StepBuilder
    compliant=N(system_id="account_service",resource_id="account_2",winning_rule_id="r2",required_action="DELETE_RECORD",is_in_compliance=True,evidence_id="e2")
    steps=StepBuilder.build_incomplete(N(incomplete_triggers=[]),[compliant,compliant])
    assert len(steps)==1 and steps[0].operation=="VERIFY_RECORD_ABSENT"

def test_p15_semantic_diff_ignores_step_order():
    from orchestrator.step_diff import semantic_counts
    a={"phase":"VERIFICATION","system_id":"a","resource_id":"r1","operation":"VERIFY_RECORD_ABSENT","state":"ABSENT","evidence_id":"e1"}
    b={"phase":"VERIFICATION","system_id":"b","resource_id":"r2","operation":"VERIFY_RECORD_PRESENT","state":"PRESENT","evidence_id":"e2"}
    counts=semantic_counts([a,b],[b,a])
    assert all(value==0 for value in counts.values())

def test_p15_semantic_diff_isolates_citation_difference():
    from orchestrator.step_diff import semantic_counts
    a={"phase":"FINDING","system_id":"search_service","resource_id":"search_1","operation":"REPORT_REMAINING_RECORD","state":"PRESENT","evidence_id":"e_old"}
    counts=semantic_counts([a],[{**a,"evidence_id":"e_live"}])
    assert counts["EVIDENCE_CITATION_DIFFERENCE"]==1
    assert counts["MISSING_SEMANTIC_STEP"]==counts["EXTRA_SEMANTIC_STEP"]==0

def test_p15_json_path_fallback_without_visible_ancestor_id(tmp_path):
    from agent.evidence.handlers.json_handler import extract
    p=tmp_path/"nested.json"
    p.write_text('{"records":[{"email":"u1@example.com"}]}')
    records=extract(p,"e_nested",I,datetime(2026,1,2,tzinfo=timezone.utc))
    assert [r.resource_id for r in records]==["$.records[0]"]

def test_p15_no_proximity_even_when_timestamps_are_identical():
    assert not derived(go([act(resource="different",t="2026-01-01T12:00:00+00:00")],[ev(resource="r1",ts="2026-01-01T12:00:00+00:00")]))

def test_p14_unowned_404_requires_prior_exact_identity_evidence(tmp_path):
    from agent.evidence.handlers.json_handler import extract
    from agent.state.reconstructor import reconstruct
    p=tmp_path/"readback.json"
    p.write_text('{"service_exports":{"account_service":{"profile_lookups":[{"resource_id":"r1","profile":null,"status_code":404,"observed_at":"2026-01-01T13:00:00Z"}]}}}')
    readback=ExtractedEvidence("e2",str(p),"h2",extract(p,"e2",I,datetime(2026,1,2,tzinfo=timezone.utc)),"json",datetime(2026,1,1,tzinfo=timezone.utc))
    assert len(readback.records)==1 and readback.records[0].user_ref==""
    assert reconstruct(I,[readback],[],datetime(2026,1,2,tzinfo=timezone.utc))==[]
    facts=reconstruct(I,[ev(resource="r1"),readback],[],datetime(2026,1,2,tzinfo=timezone.utc))
    assert len(facts)==1 and facts[0].state_at_audit=="ABSENT" and facts[0].evidence_id=="e2"

def test_p14_unowned_404_does_not_join_different_resource(tmp_path):
    from agent.evidence.handlers.json_handler import extract
    from agent.state.reconstructor import reconstruct
    p=tmp_path/"readback.json"
    p.write_text('{"service_exports":{"account_service":{"profile_lookups":[{"resource_id":"other","profile":null,"status_code":404,"observed_at":"2026-01-01T13:00:00Z"}]}}}')
    readback=ExtractedEvidence("e2",str(p),"h2",extract(p,"e2",I,datetime(2026,1,2,tzinfo=timezone.utc)),"json",datetime(2026,1,1,tzinfo=timezone.utc))
    facts=reconstruct(I,[ev(resource="r1"),readback],[],datetime(2026,1,2,tzinfo=timezone.utc))
    assert len(facts)==1 and facts[0].resource_id=="r1" and facts[0].state_at_audit=="PRESENT"

def test_p14_explicit_support_contact_clearance_is_redacted(tmp_path):
    from agent.evidence.handlers.json_handler import extract
    p=tmp_path/"support.json"
    p.write_text('{"service_exports":{"support_platform":{"tickets":[{"resource_id":"support_1","customer_reference":"U1","requester_email":null,"requester_name":null,"requester_phone":null,"observed_at":"2026-01-01T12:00:00Z"}]}}}')
    records=extract(p,"e_support",I,datetime(2026,1,2,tzinfo=timezone.utc))
    assert [(r.system_id,r.resource_id,r.state_at_evidence) for r in records]==[("support_platform","support_1","REDACTED")]

def test_p14_deleted_tombstone_with_no_contacts_is_redacted(tmp_path):
    from agent.evidence.handlers.json_handler import extract
    p=tmp_path/"tombstone.json"
    p.write_text('{"snapshots":[{"data_store":"identity_service","captured_at":"2026-01-01T12:00:00Z","records":[{"resource_id":"tombstone_1","subject_reference":"U1","account_status":"DELETED","name":null,"email":null,"phone":null,"email_hash":null}]}]}')
    records=extract(p,"e_tombstone",I,datetime(2026,1,2,tzinfo=timezone.utc))
    assert [(r.system_id,r.resource_id,r.state_at_evidence) for r in records]==[("identity_service","tombstone_1","REDACTED")]

def test_p14_disabled_connector_yields_compliant_flow_verdict(tmp_path):
    from agent.evidence.handlers.json_handler import extract
    from agent.state.reconstructor import reconstruct
    from agent.policy.engine import PolicyEngine
    from agent.policy.rules_loader import load_rules
    from pathlib import Path
    p=tmp_path/"flow.json"
    p.write_text('{"service_exports":{"integration_service":{"connectors":[{"resource_id":"data_flow_1","customer_reference":"U1","enabled":false,"observed_at":"2026-01-01T12:00:00Z"}]}}}')
    at=datetime(2026,1,2,tzinfo=timezone.utc)
    records=extract(p,"e_flow",I,at)
    evidence=ExtractedEvidence("e_flow",str(p),"h",records,"json",at)
    facts=reconstruct(I,[evidence],[],at)
    rules=load_rules(Path(__file__).resolve().parents[2]/"dataset/deletion_rules.csv")
    verdicts=PolicyEngine(rules).apply(facts,[],[],at,at)
    assert len(verdicts)==1
    assert (verdicts[0].target_kind,verdicts[0].required_action,verdicts[0].is_in_compliance)==("flow","DISABLE_DATA_FLOW",True)

def test_p14_support_platform_uses_support_message_redaction_rule():
    from agent.policy.category_map import category_for
    from agent.policy.engine import PolicyEngine
    from agent.policy.rules_loader import load_rules
    from agent.evidence.ir import ResourceFact
    from pathlib import Path
    at=datetime(2026,1,2,tzinfo=timezone.utc)
    assert category_for("support_platform","support_1")=="support_tickets"
    fact=ResourceFact("support_platform","support_1","U1","REDACTED",set(),"e_support",at,[])
    rules=load_rules(Path(__file__).resolve().parents[2]/"dataset/deletion_rules.csv")
    verdict=PolicyEngine(rules).apply([fact],[],[],at,at)[0]
    assert verdict.required_action=="REDACT_RECORD" and verdict.is_in_compliance

from functools import lru_cache

@lru_cache(maxsize=1)
def _phase14_sample_result():
    import csv
    import json
    from pathlib import Path
    from orchestrator.pipeline import load_datasets,run_case
    root=Path(__file__).resolve().parents[2]
    data=load_datasets(root)
    with (root/"dataset/sample_deletion_requests.csv").open(encoding="utf-8-sig",newline="") as f:
        cases=list(csv.DictReader(f))
    data.active_case_rows=cases
    with (root/"dataset/sample_output.csv").open(encoding="utf-8-sig",newline="") as f:
        gold={r["case_id"]:r for r in csv.DictReader(f)}
    actual={r["case_id"]:run_case(N(**r),data) for r in cases}
    status_matches={c for c,r in actual.items() if r.deletion_status==gold[c]["deletion_status"]}
    step_matches={c for c,r in actual.items() if json.loads(r.steps_json)==json.loads(gold[c]["steps_json"])}
    return status_matches,step_matches,len(gold)

def test_p14_sample_regression_statuses():
    # Phase 12 documented these 13 recovered statuses; preserve them and cases 02-04.
    statuses,_,_= _phase14_sample_result()
    recovered={*(f"case_{n:02d}" for n in range(8,17)),"case_18","case_19","case_20","case_22"}
    assert recovered <= statuses
    assert {"case_02","case_03","case_04"} <= statuses

def test_p14_hard_gate_full_sample_pipeline():
    statuses,steps,total=_phase14_sample_result()
    assert len(statuses)/total >= 0.85
    assert len(steps)/total >= 0.85, f"NOT_READY: exact steps {len(steps)}/{total}"
