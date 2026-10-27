"""Gold-free replay checks for the 518-row plan audit."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from orchestrator.plan_execution_audit import audit_case, resource_role_conflict


def step(phase, operation, evidence_id="", resource_id="account_9", system_id="account_service"):
    return dict(phase=phase, operation=operation, evidence_id=evidence_id,
                resource_id=resource_id, system_id=system_id, step_no=0,
                state="ABSENT")


def verdict(action="DELETE_RECORD", compliant=False, state="PRESENT",
            evidence_id="evidence_9", resource_id="account_9", system_id="account_service"):
    return dict(system_id=system_id, resource_id=resource_id,
                evidence_id=evidence_id,
                value=f"PolicyVerdict(target_kind='record', required_action='{action}', "
                      f"current_state='{state}', is_in_compliance={compliant})")


def trace(steps, verdicts, records=()):
    return [
        dict(phase="identity", event="resolve_identity",
             outputs=dict(all_user_ids=["user_9"], all_emails=["nine@example.test"])),
        dict(phase="evidence", event="extract_evidence",
             outputs=dict(files=[dict(file_id="evidence_9", records=list(records))])),
        dict(phase="policy", event="apply", outputs=dict(verdicts=verdicts)),
        dict(phase="steps", event="generate", outputs=dict(steps_json=json.dumps(steps))),
    ]


def run(status, steps, verdicts, records=()):
    row = dict(case_id="case_synthetic", deletion_status=status,
               steps_json=json.dumps(steps))
    return audit_case(row, trace(steps, verdicts, records),
                      frozenset({"evidence_9"}), frozenset())


OWNED = dict(system_id="account_service", resource_id="account_9",
             user_ref="user_9", state="PRESENT")


def test_complete_verification_is_source_backed():
    result = run("COMPLETE", [step("VERIFICATION", "VERIFY_RECORD_ABSENT", "evidence_9")],
                 [verdict(compliant=True, state="ABSENT")], [OWNED])
    assert not result.errors and not result.warnings


def test_incomplete_delete_plan_can_reach_absent_state():
    steps = [step("FINDING", "REPORT_REMAINING_RECORD", "evidence_9"),
             step("REMEDIATION", "DELETE_RECORD"),
             step("VERIFICATION", "VERIFY_RECORD_ABSENT")]
    result = run("INCOMPLETE", steps, [verdict()], [OWNED])
    assert not result.errors and not result.warnings


def test_missing_remediation_is_a_plan_error():
    steps = [step("FINDING", "REPORT_REMAINING_RECORD", "evidence_9"),
             step("VERIFICATION", "VERIFY_RECORD_ABSENT")]
    result = run("INCOMPLETE", steps, [verdict()], [OWNED])
    assert any("missing_plan_step" in issue and "DELETE_RECORD" in issue
               for issue in result.errors)


def test_absent_required_retained_record_has_no_permitted_repair():
    steps = [step("VERIFICATION", "VERIFY_RECORD_PRESENT")]
    result = run("INCOMPLETE", steps,
                 [verdict(action="RETAIN", compliant=False, state="ABSENT")])
    assert any("verification_cannot_pass_after_plan" in error
               for error in result.errors)
    assert any("retention_violation_has_no_repair" in warning
               for warning in result.warnings)


def test_empty_complete_plan_is_not_treated_as_proof():
    result = run("COMPLETE", [], [])
    assert not result.errors
    assert "complete_without_evidence_backed_verification" in result.warnings


def test_other_person_citation_is_flagged_as_ghost_data():
    other = dict(OWNED, user_ref="user_10")
    result = run("COMPLETE", [step("VERIFICATION", "VERIFY_RECORD_ABSENT", "evidence_9")],
                 [verdict(compliant=True, state="ABSENT")], [other])
    assert any("citation_lacks_directly_owned_extracted_record" in warning
               for warning in result.warnings)


def test_data_flow_must_be_disabled_before_record_mutation():
    steps = [step("FINDING", "REPORT_REMAINING_RECORD", "evidence_9"),
             step("FINDING", "REPORT_ACTIVE_DATA_FLOW", "evidence_9",
                  "data_flow_9", "integration_service"),
             step("REMEDIATION", "DELETE_RECORD"),
             step("REMEDIATION", "DISABLE_DATA_FLOW", "", "data_flow_9", "integration_service"),
             step("VERIFICATION", "VERIFY_RECORD_ABSENT"),
             step("VERIFICATION", "VERIFY_DATA_FLOW_DISABLED", "", "data_flow_9", "integration_service")]
    flow = dict(system_id="integration_service", resource_id="data_flow_9",
                evidence_id="evidence_9",
                value="PolicyVerdict(target_kind='flow', required_action='DISABLE_DATA_FLOW', "
                      "current_state='ACTIVE', is_in_compliance=False)")
    result = run("INCOMPLETE", steps, [verdict(), flow], [OWNED])
    assert "flow_or_restore_block_after_record_mutation" in result.errors


def test_flow_control_id_must_not_be_used_as_search_record_id():
    assert resource_role_conflict("search_service", "data_flow_4227")
    assert not resource_role_conflict("integration_service", "data_flow_4227")
    assert not resource_role_conflict("search_service", "search_1474")
