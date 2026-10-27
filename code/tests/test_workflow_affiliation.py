from copy import deepcopy
from datetime import datetime, timezone
from types import SimpleNamespace

from agent.evidence.ir import ExtractedEvidence, RecordState
from orchestrator.workflow_affiliation import affiliate_unique_account_delete
from orchestrator.workflow_affiliation_probe import measure_window


IDENTITY = SimpleNamespace(primary_user_id="user_a", all_user_ids={"user_a"},
                           all_emails={"a@example.test"})
REQUESTED = "2026-08-20T09:00:00Z"
REPORTED = "2026-08-20T12:00:00Z"
AUDIT = "2026-08-21T12:00:00Z"


def action(resource="account_a", when="2026-08-20T11:00:00Z",
           result="SUCCESS", **extra):
    return {"activity_id": "activity_a", "event_time": when,
            "event_type": "DELETE_RECORD", "source_system": "deletion_worker",
            "target_system": "account_service", "resource_id": resource,
            "reported_result": result, "details": "Primary profile submitted.", **extra}


def run(rows, reported=REPORTED, requested=REQUESTED, audit=AUDIT):
    return affiliate_unique_account_delete(rows, IDENTITY, reported, requested, audit)


def test_unique_successful_account_delete_derives_without_mutating_original():
    original = action()
    saved = deepcopy(original)
    result = run([original])
    assert len(result) == 2
    assert original == saved == result[0]
    assert result[1]["target_user_id"] == "user_a"
    assert result[1]["inference_method"] == "unique_calibrated_report_window"
    assert result[1]["original_activity_id"] == original["activity_id"]


def test_competing_account_deletes_cause_abstention():
    first = action()
    second = action(resource="account_b", when="2026-08-20T10:50:00Z",
                    activity_id="activity_b")
    assert len(run([first, second])) == 2


def test_failed_account_delete_still_competes_with_a_successful_one():
    successful = action()
    failed = action(resource="account_b", activity_id="activity_b", result="FAILED")
    trace = []
    result = affiliate_unique_account_delete([successful, failed], IDENTITY,
                                              REPORTED, REQUESTED, AUDIT,
                                              trace=trace)
    assert len(result) == 2
    assert trace[0]["reason"] == "competing_account_actions"


def test_five_minute_nearest_event_is_not_affiliated():
    assert len(run([action(when="2026-08-20T11:59:43Z")])) == 1


def test_failed_result_cannot_be_used_as_successful_delete():
    assert len(run([action(result="FAILED")])) == 1


def test_out_of_request_or_audit_window_is_rejected():
    assert len(run([action()], requested="2026-08-20T11:30:00Z")) == 1
    assert len(run([action()], audit="2026-08-20T10:30:00Z")) == 1


def test_existing_exact_affiliation_is_not_duplicated():
    original = action()
    exact = action(activity_id="activity_a::derived_0001_for_user_a",
                   derived=True, original_activity_id="activity_a",
                   target_user_id="user_a")
    assert len(run([original, exact])) == 2


def test_no_reported_time_causes_abstention():
    assert len(run([action()], reported=None)) == 1


def test_existing_owned_account_prevents_a_second_primary_assignment():
    observed = RecordState("account_service", "account_existing", "user_a", "PRESENT")
    evidence = ExtractedEvidence("file", "file.json", "hash", [observed], "json",
                                 datetime(2026, 8, 20, tzinfo=timezone.utc))
    assert len(affiliate_unique_account_delete([action()], IDENTITY, REPORTED,
                                               REQUESTED, AUDIT, [evidence])) == 1


def test_exact_owner_of_another_person_vetoes_time_inference():
    assert len(affiliate_unique_account_delete([action()], IDENTITY, REPORTED,
                                               REQUESTED, AUDIT, (),
                                               {"account_a": "user_other"})) == 1


def test_ambiguous_requesters_with_same_report_time_cause_abstention():
    assert len(affiliate_unique_account_delete([action()], IDENTITY, REPORTED,
                                               REQUESTED, AUDIT, (), {}, 2)) == 1


def test_known_other_owner_is_removed_before_uniqueness_check():
    first = action()
    other = action(resource="account_202", activity_id="activity_b")
    trace = []
    result = affiliate_unique_account_delete([first, other], IDENTITY, REPORTED,
                                              REQUESTED, AUDIT, (),
                                              {"account_202": "user_other"}, 1, trace)
    assert len(result) == 3
    assert result[-1]["resource_id"] == "account_a"
    assert trace == [{"reason": "derived_unique_calibrated_report_window",
                      "candidate_activity_ids": ["activity_a"]}]


def test_ambiguous_actions_are_logged_without_derivation():
    trace = []
    first = action()
    second = action(resource="account_b", activity_id="activity_b")
    result = affiliate_unique_account_delete([first, second], IDENTITY, REPORTED,
                                              REQUESTED, AUDIT, trace=trace)
    assert len(result) == 2
    assert trace[0]["reason"] == "competing_account_actions"
    assert trace[0]["candidate_activity_ids"] == ["activity_a", "activity_b"]


def test_source_only_probe_distinguishes_calibrated_from_nearest_band():
    request = {"email": "a@example.test", "requested_at": REQUESTED,
               "reported_at": REPORTED, "audit_at": AUDIT}
    resolver = SimpleNamespace(resolve=lambda *_: IDENTITY)
    owners = {"account_a": "user_a"}
    calibrated = measure_window([request], [action()], resolver, owners, 30, 90,
                                winner_success_only=True)
    nearest = measure_window([request], [action()], resolver, owners, 0, 5,
                             winner_success_only=True)
    assert calibrated["unique"] == calibrated["known"] == calibrated["correct"] == 1
    assert nearest["unique"] == 0


def test_source_only_probe_abstains_when_two_events_compete():
    request = {"email": "a@example.test", "requested_at": REQUESTED,
               "reported_at": REPORTED, "audit_at": AUDIT}
    resolver = SimpleNamespace(resolve=lambda *_: IDENTITY)
    rows = [action(), action(resource="account_b", activity_id="activity_b")]
    assert measure_window([request], rows, resolver, {}, 30, 90)["unique"] == 0


def test_source_only_probe_exposes_false_owner_from_success_prefilter():
    request = {"email": "a@example.test", "requested_at": REQUESTED,
               "reported_at": REPORTED, "audit_at": AUDIT}
    resolver = SimpleNamespace(resolve=lambda *_: IDENTITY)
    rows = [action(result="FAILED"),
            action(resource="account_b", activity_id="activity_b", result="SUCCESS")]
    owners = {"account_a": "user_a", "account_b": "user_b"}
    unsafe = measure_window([request], rows, resolver, owners, 30, 90,
                            successful_only=True)
    admitted = measure_window([request], rows, resolver, owners, 30, 90,
                              winner_success_only=True)
    assert unsafe["other_person"] == 1
    assert admitted["unique"] == 0
