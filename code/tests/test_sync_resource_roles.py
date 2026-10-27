"""A connector ID is not the downstream record named in a sync event."""

import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.evidence.ir import ExtractedEvidence, RecordState
from agent.state.reconstructor import reconstruct


IDENTITY = SimpleNamespace(primary_user_id="user_1", all_user_ids={"user_1"},
                           all_emails={"one@example.test"})
AT = datetime(2026, 6, 1, tzinfo=timezone.utc)


def sync(resource_id, details):
    return dict(activity_id="activity_synthetic", event_time="2026-05-20T00:00:00Z",
                event_type="SYNC_RECORD", source_system="integration_service",
                target_system="search_service", resource_id=resource_id,
                details=details + " user_1", reported_result="SUCCESS")


def evidence():
    records = [
        RecordState("integration_service", "data_flow_1", "user_1", "PRESENT", [], AT,
                    {"enabled": True}),
        RecordState("search_service", "search_2", "user_1", "PRESENT", [], AT, {}),
    ]
    return ExtractedEvidence("evidence_synthetic", "source.json", "hash", records,
                             "json", AT)


def test_connector_sync_does_not_create_search_record_with_flow_id():
    facts = reconstruct(IDENTITY, [evidence()],
                        [sync("data_flow_1", "Active connector repopulated downstream resource search_2.")],
                        "2026-06-02T00:00:00Z")
    assert {(fact.system_id, fact.resource_id) for fact in facts} == {
        ("integration_service", "data_flow_1"), ("search_service", "search_2")}


def test_connector_sync_without_snapshot_is_flow_signal_not_record_proof():
    facts = reconstruct(IDENTITY, [],
                        [sync("data_flow_1", "Active connector repopulated downstream resource search_2.")],
                        "2026-06-02T00:00:00Z")
    assert facts == []


def test_regular_search_sync_still_reconstructs_search_record():
    row = sync("search_2", "Customer profile synchronization processed search_2.")
    row["source_system"] = "account_service"
    facts = reconstruct(IDENTITY, [], [row], "2026-06-02T00:00:00Z")
    assert [(fact.system_id, fact.resource_id, fact.state_at_audit) for fact in facts] == [
        ("search_service", "search_2", "PRESENT")]
