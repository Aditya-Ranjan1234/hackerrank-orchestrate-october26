"""Query events are not stored records, and stale misses are not audit proof."""

from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from agent.evidence.handlers.log_handler import extract
from agent.evidence.ir import ExtractedEvidence, RecordState
from orchestrator.evidence_admission import (
    affiliate_absent_readbacks_from_later_owner,
    exclude_stale_negative_lookups,
)


IDENTITY = SimpleNamespace(primary_user_id="U1", all_user_ids={"U1"}, all_emails={"a@example.com"})


def _item(method="regex-log"):
    return ExtractedEvidence("ev", "evidence/logs/query.log", "hash", [], method, datetime.now(timezone.utc))


def _record(time, state="ABSENT", event="profile_lookup_completed", rows="0"):
    return RecordState(
        "account_service", "account_1", "a@example.com", state,
        evidence_timestamp=datetime.fromisoformat(time.replace("Z", "+00:00")),
        raw_row={"event": event, "rows": rows, "http_status": "404" if rows == "0" else "200"},
    )


def test_key_value_lookup_started_with_resource_id_is_not_present_record(tmp_path):
    path = tmp_path / "query.log"
    path.write_text(
        "2026-09-01T10:00:00Z service=account_service trace_id=t1 event=profile_lookup_started resource_id=account_1 lookup_key=a@example.com\n"
        "2026-09-01T10:00:01Z service=account_service trace_id=t1 event=profile_lookup_completed resource_id=account_1 rows=0 http_status=404\n",
        encoding="utf-8",
    )
    records, _ = extract(path, "ev", IDENTITY, "2026-09-02T00:00:00Z")
    assert [(record.resource_id, record.state_at_evidence) for record in records] == [("account_1", "ABSENT")]


def test_json_line_lookup_started_with_resource_id_is_not_present_record(tmp_path):
    path = tmp_path / "query.log"
    path.write_text(
        '{"timestamp":"2026-09-01T10:00:00Z","service":"account_service","trace_id":"t1","event":"profile_lookup_started","resource_id":"account_1","email":"a@example.com"}\n'
        '{"timestamp":"2026-09-01T10:00:01Z","service":"account_service","trace_id":"t1","event":"profile_lookup_completed","resource_id":"account_1","rows":0,"http_status":404}\n',
        encoding="utf-8",
    )
    records, _ = extract(path, "ev", IDENTITY, "2026-09-02T00:00:00Z")
    assert len(records) == 1 and records[0].state_at_evidence == "ABSENT"


def test_pre_request_negative_log_lookup_is_excluded_with_a_note():
    item = _item()
    item.records = [_record("2026-03-01T00:00:00Z")]
    assert exclude_stale_negative_lookups([item], "2026-09-01T00:00:00Z") == 1
    assert item.records == []
    assert "stale_negative_lookup_before_request:1" in item.notes


def test_current_negative_lookup_is_retained():
    item = _item()
    record = _record("2026-09-01T00:00:01Z")
    item.records = [record]
    assert exclude_stale_negative_lookups([item], "2026-09-01T00:00:00Z") == 0
    assert item.records == [record]


def test_positive_rows_and_non_log_snapshots_are_not_removed():
    item = _item()
    snapshot = _item("json")
    item.records = [_record("2026-03-01T00:00:00Z", state="PRESENT", rows="1")]
    snapshot.records = [_record("2026-03-01T00:00:00Z")]
    assert exclude_stale_negative_lookups([item, snapshot], "2026-09-01T00:00:00Z") == 0
    assert len(item.records) == len(snapshot.records) == 1


def test_later_direct_owner_can_affiliate_exact_earlier_404_without_using_future_state():
    before = _item("json")
    before.records = [RecordState("account_service", "account_1", "", "ABSENT",
                                  evidence_timestamp=datetime(2026, 9, 15, 9, tzinfo=timezone.utc),
                                  raw_row={"resource_id": "account_1", "profile": None, "status_code": 404})]
    later = _item("json")
    later.file_id = "later"
    later.records_post_audit = [RecordState("account_service", "account_1", "U1", "PRESENT",
                                            evidence_timestamp=datetime(2026, 9, 17, 9, tzinfo=timezone.utc),
                                            raw_row={"resource_id": "account_1", "customer_reference": "U1", "email": "a@example.com"})]
    assert affiliate_absent_readbacks_from_later_owner([before, later], IDENTITY, "2026-09-15T12:00:00Z") == 1
    assert len(before.records) == 2
    assert before.records[1].user_ref == "U1"
    assert before.records[1].state_at_evidence == "ABSENT"
    assert before.records[1].evidence_timestamp == before.records[0].evidence_timestamp
    assert before.records[1].raw_row["affiliation_source"] == ["later"]
    assert later.records == []


def test_later_query_selector_is_not_direct_owner():
    before = _item("json")
    before.records = [RecordState("account_service", "account_1", "", "ABSENT",
                                  evidence_timestamp=datetime(2026, 9, 15, 9, tzinfo=timezone.utc))]
    later = _item("json")
    later.records_post_audit = [RecordState("account_service", "account_1", "U1", "PRESENT",
                                            evidence_timestamp=datetime(2026, 9, 17, 9, tzinfo=timezone.utc),
                                            raw_row={"resource_id": "account_1", "subject_selector": "U1"})]
    assert affiliate_absent_readbacks_from_later_owner([before, later], IDENTITY, "2026-09-15T12:00:00Z") == 0
    assert len(before.records) == 1


def test_later_owner_requires_same_complete_resource_and_system():
    before = _item("json")
    before.records = [RecordState("account_service", "account_1", "", "ABSENT",
                                  evidence_timestamp=datetime(2026, 9, 15, 9, tzinfo=timezone.utc))]
    later = _item("json")
    later.records_post_audit = [RecordState("account_service", "account_10", "U1", "PRESENT",
                                            evidence_timestamp=datetime(2026, 9, 17, 9, tzinfo=timezone.utc),
                                            raw_row={"resource_id": "account_10", "user_id": "U1"}),
                                RecordState("search_service", "account_1", "U1", "PRESENT",
                                            evidence_timestamp=datetime(2026, 9, 17, 9, tzinfo=timezone.utc),
                                            raw_row={"resource_id": "account_1", "user_id": "U1"})]
    assert affiliate_absent_readbacks_from_later_owner([before, later], IDENTITY, "2026-09-15T12:00:00Z") == 0


def test_later_model_only_record_cannot_affiliate_anonymous_readback():
    before = _item("json")
    before.records = [RecordState("account_service", "account_1", "", "ABSENT",
                                  evidence_timestamp=datetime(2026, 9, 15, 9, tzinfo=timezone.utc))]
    later = _item("vlm")
    later.records_post_audit = [RecordState("account_service", "account_1", "U1", "PRESENT",
                                            evidence_timestamp=datetime(2026, 9, 17, 9, tzinfo=timezone.utc),
                                            raw_row={"resource_id": "account_1", "user_id": "U1"})]
    assert affiliate_absent_readbacks_from_later_owner([before, later], IDENTITY, "2026-09-15T12:00:00Z") == 0


def test_registry_preserves_later_json_row_separately_from_audit_state(tmp_path):
    import json
    from agent.evidence.registry import extract_file

    source = tmp_path / "dataset/evidence/records/later.json"
    source.parent.mkdir(parents=True)
    source.write_text(json.dumps({
        "captured_at": "2026-09-17T09:00:00Z",
        "data_store": "account_service",
        "records": [{"resource_id": "account_1", "customer_reference": "U1", "email": "a@example.com"}],
    }), encoding="utf-8")
    extracted = extract_file(tmp_path, "later", "evidence/records/later.json", IDENTITY, "2026-09-15T12:00:00Z")
    assert extracted.records == []
    assert [(row.resource_id, row.user_ref) for row in extracted.records_post_audit] == [("account_1", "U1")]
