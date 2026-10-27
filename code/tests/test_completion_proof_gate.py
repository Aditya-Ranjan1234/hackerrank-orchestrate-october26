"""A SUCCESS activity can suggest a future check, never prove completion."""

from datetime import datetime, timezone
from types import SimpleNamespace

from agent.evidence.ir import ResourceFact
from agent.status.ir import StatusDecision
from agent.steps.generator import StepGenerator
from orchestrator.completion_proof_gate import guard_unverified_completion


NOW = datetime(2026, 9, 1, tzinfo=timezone.utc)
DERIVED = "activity_101::derived_report_window_for_user_a"
ACTIVITY = {"activity_id": DERIVED,
            "inference_method": "unique_calibrated_report_window"}


def _decision(status):
    return StatusDecision("synthetic", status, None, [], ["initial decision"], NOW)


def _fact(citation):
    return ResourceFact("account_service", "account_101", "user_a", "ABSENT",
                        set(), citation, NOW,
                        ["timeline-only: no matching evidence record"])


def _verdict(citation):
    return SimpleNamespace(target_kind="record", system_id="account_service",
                           resource_id="account_101", required_action="DELETE_RECORD",
                           is_in_compliance=True, evidence_id=citation)


def test_activity_only_complete_becomes_incomplete_future_verification():
    verdict = _verdict("activity_101")
    decision, gaps = guard_unverified_completion(
        _decision("COMPLETE"), [_fact(DERIVED)], [verdict], [ACTIVITY])
    steps = StepGenerator.generate(SimpleNamespace(case_id="synthetic"),
                                   decision, [verdict])
    assert decision.deletion_status == "INCOMPLETE"
    assert gaps == [("account_service", "account_101", DERIVED)]
    assert len(steps) == 1
    assert steps[0].operation == "VERIFY_RECORD_ABSENT"
    assert steps[0].evidence_id == ""


def test_direct_absence_readback_keeps_complete_citation():
    verdict = _verdict("evidence_101")
    decision, gaps = guard_unverified_completion(
        _decision("COMPLETE"), [_fact("evidence_101")], [verdict], [ACTIVITY])
    steps = StepGenerator.generate(SimpleNamespace(case_id="synthetic"),
                                   decision, [verdict])
    assert decision.deletion_status == "COMPLETE"
    assert gaps == []
    assert steps[0].evidence_id == "evidence_101"


def test_existing_incomplete_case_retains_its_follow_up_check():
    verdict = _verdict("activity_101")
    decision, gaps = guard_unverified_completion(
        _decision("INCOMPLETE"), [_fact(DERIVED)], [verdict], [ACTIVITY])
    steps = StepGenerator.generate(SimpleNamespace(case_id="synthetic"),
                                   decision, [verdict])
    assert decision.deletion_status == "INCOMPLETE"
    assert gaps == []
    assert steps[0].evidence_id == ""
