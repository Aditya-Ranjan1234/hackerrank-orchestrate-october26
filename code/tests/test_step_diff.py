import json
from types import SimpleNamespace as Row
import pytest
from orchestrator.step_diff import classify_mismatch, diff_case

def row(status,steps,case_id="case_x"):
    return Row(case_id=case_id,deletion_status=status,steps_json=json.dumps(steps))
def step(**kwargs):
    value=dict(step_no=1,phase="VERIFICATION",system_id="account_service",resource_id="account_1",operation="VERIFY_RECORD_ABSENT",state="ABSENT",evidence_id="e1")
    value.update(kwargs);return value

def test_same_status_different_steps():
    diff=diff_case(row("COMPLETE",[step()]),row("COMPLETE",[step(resource_id="account_2")]))
    assert diff.status_match and not diff.step_array_match and diff.mismatches
def test_not_applicable_empty_matches():
    diff=diff_case(row("NOT_APPLICABLE",[]),row("NOT_APPLICABLE",[]))
    assert diff.step_array_match and diff.mismatches==[]
def test_not_applicable_missing_step():
    diff=diff_case(row("NOT_APPLICABLE",[]),row("COMPLETE",[step()]))
    assert diff.mismatches[0]["mismatch_type"]=="COUNT_MISMATCH" and diff.mismatches[0]["gold_value"]
def test_extra_step_count():
    diff=diff_case(row("COMPLETE",[step(),step(step_no=2)]),row("COMPLETE",[step()]))
    assert diff.our_step_count==2 and diff.gold_step_count==1
@pytest.mark.parametrize("field,expected",[
    ("phase","PHASE_ORDER_MISMATCH"),("operation","OPERATION_MISMATCH"),
    ("state","STATE_MISMATCH"),("system_id","SYSTEM_ID_MISMATCH"),
    ("resource_id","RESOURCE_ID_MISMATCH"),("step_no","STEP_NO_MISMATCH")])
def test_field_classification(field,expected):
    assert classify_mismatch(field,"ours","gold")==expected
@pytest.mark.parametrize("ours,gold,expected",[("","e1","EVIDENCE_ID_MISMATCH_SHOULD_CITE"),("e1","","EVIDENCE_ID_MISMATCH_SHOULD_BE_EMPTY"),("e1","e2","EVIDENCE_ID_MISMATCH_WRONG_CITATION")])
def test_evidence_classification(ours,gold,expected):
    assert classify_mismatch("evidence_id",ours,gold)==expected
