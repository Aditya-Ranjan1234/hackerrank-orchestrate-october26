"""The evaluation probe must distinguish missing facts from step mapping errors."""

from orchestrator.step_gap_diagnosis import classify_gap, missing_steps, reported_time_control


def step(resource, evidence=""):
    return {"phase": "VERIFICATION", "system_id": "account_service",
            "resource_id": resource, "operation": "VERIFY_RECORD_ABSENT",
            "state": "ABSENT", "evidence_id": evidence}


def test_semantic_alignment_ignores_position_shift_and_citation():
    expected = [step("account_a", "evidence_a"), step("account_b", "evidence_b")]
    actual = [step("account_b", "evidence_other")]
    assert missing_steps(actual, expected) == [expected[0]]


def test_semantic_alignment_respects_duplicate_step_counts():
    item = step("account_a")
    assert missing_steps([item], [item, item]) == [item]


def test_no_participant_reference_is_distinct_from_ownerless_activity():
    assert classify_gap(0, 0, 0, 0, 0, 0, 0) == "no_participant_input_names_resource"
    assert classify_gap(0, 1, 1, 0, 0, 0, 0) == "ownerless_activity_only"


def test_anonymous_readback_is_not_a_resource_fact():
    assert classify_gap(1, 0, 1, 1, 0, 0, 0) == "anonymous_extraction_not_affiliated"


def test_a_real_verdict_gap_is_attributed_downstream():
    assert classify_gap(1, 0, 1, 1, 1, 1, 1) == "verdict_exists_step_missing"


def test_reported_time_control_detects_wrong_person_with_unique_candidate():
    request = {"email": "requester@example.org", "reported_at": "2026-01-02T12:00:00Z"}
    activity = {"source_system": "deletion_worker", "target_system": "account_service",
                "event_type": "DELETE_RECORD", "event_time": "2026-01-02T11:59:30Z",
                "resource_id": "account_other"}
    result = reported_time_control([request], [activity],
                                   {"account_other": "user_other"},
                                   {"requester@example.org": "user_requester"})
    assert result["unique_candidate"] == 1
    assert result["independently_owned"] == 1
    assert result["correct_owner"] == 0
