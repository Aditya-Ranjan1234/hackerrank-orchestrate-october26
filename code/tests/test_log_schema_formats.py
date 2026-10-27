"""Source-format regression tests independent of sample case labels."""

from pathlib import Path
from types import SimpleNamespace
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.evidence.handlers.log_handler import extract


@pytest.fixture
def identity():
    return SimpleNamespace(all_user_ids={"user_alpha"},
                           all_emails={"alpha@example.com"},
                           primary_user_id="user_alpha")


def parse(tmp_path, identity, content, audit_at="2026-09-01T00:00:00Z"):
    path = tmp_path / "fixture.log"
    path.write_text(content, encoding="utf-8")
    return extract(path, "synthetic", identity, audit_at)


def test_quoted_lookup_result_has_full_resource_and_negative_state(tmp_path, identity):
    rows, post = parse(
        tmp_path, identity,
        '2026-08-01T00:00:00Z INFO service=reader event=record_lookup '
        'system="account_service" resource_id="account_414" '
        'result="NOT_FOUND" subject_reference="alpha@example.com"\n',
    )
    assert post == []
    assert [(r.system_id, r.resource_id, r.state_at_evidence) for r in rows] == [
        ("account_service", "account_414", "ABSENT")
    ]
    assert rows[0].pii_hits == []  # The query subject is not stored PII.


def test_pipe_trace_joins_earlier_exact_owner(tmp_path, identity):
    rows, _ = parse(
        tmp_path, identity,
        '2026-08-01T00:00:00Z | DEBUG | security_service | tr-a | audit_record_query_started | subject_ref="user_alpha"\n'
        '2026-08-01T00:00:01Z | INFO | security_service | tr-a | audit_record_read_completed | resource_id="audit_record_814" rows="1"\n',
    )
    assert [(r.system_id, r.resource_id, r.user_ref) for r in rows] == [
        ("security_service", "audit_record_814", "user_alpha")
    ]


def test_cloud_runtime_nested_escaped_message(tmp_path, identity):
    rows, _ = parse(
        tmp_path, identity,
        r'2026-08-01T00:00:00Z requestId=tr-b level=INFO function=search_service message="resource_id=\"search_916\" event=\"index_query_completed\" result=\"hit\" correlation_key=\"alpha@example.com\""' "\n",
    )
    assert [(r.resource_id, r.system_id) for r in rows] == [
        ("search_916", "search_service")
    ]


def test_syslog_trace_does_not_join_other_trace(tmp_path, identity):
    rows, _ = parse(
        tmp_path, identity,
        '2026-08-01T00:00:00Z <15>1 node-1 account_service tr-c - - event="profile_lookup_started" lookup_key="alpha@example.com"\n'
        '2026-08-01T00:00:01Z <15>1 node-1 account_service tr-other - - event="profile_lookup_completed" resource_id="account_12" rows="1"\n'
        '2026-08-01T00:00:02Z <15>1 node-1 account_service tr-c - - event="profile_lookup_completed" resource_id="account_11" rows="0" http_status="404"\n',
    )
    assert [(r.resource_id, r.state_at_evidence) for r in rows] == [
        ("account_11", "ABSENT")
    ]


def test_bracket_trace_resource_and_component(tmp_path, identity):
    rows, _ = parse(
        tmp_path, identity,
        '2026-08-01T00:00:00Z [DEBUG] [support_platform] [tr-d] message_scan_started: subject_key="alpha@example.com"\n'
        '2026-08-01T00:00:01Z [WARN] [support_platform] [tr-d] attachment_pii_scan: resource_id="support_123" matched_value="alpha@example.com"\n',
    )
    assert [(r.system_id, r.resource_id, r.state_at_evidence) for r in rows] == [
        ("support_platform", "support_123", "PRESENT")
    ]
    assert {hit.value_kind for hit in rows[0].pii_hits} == {"email"}


def test_post_audit_structured_result_is_separated(tmp_path, identity):
    rows, post = parse(
        tmp_path, identity,
        '2026-09-02T00:00:00Z INFO service=reader event=record_lookup '
        'system="analytics_platform" resource_id="analytics_5" '
        'result="ANONYMIZED" subject_reference="alpha@example.com"\n',
    )
    assert rows == []
    assert [(r.resource_id, r.state_at_evidence) for r in post] == [
        ("analytics_5", "ANONYMIZED")
    ]


def test_query_start_and_unstructured_mentions_do_not_create_ghost(tmp_path, identity):
    rows, _ = parse(
        tmp_path, identity,
        '2026-08-01T00:00:00Z service=account_service event=profile_lookup_started resource_id=account_8 lookup_key=alpha@example.com\n'
        '2026-08-01T00:00:01Z service=account_service event=error message="alpha@example.com" resource_id=account_9\n',
    )
    assert rows == []


def test_trace_join_rejects_later_only_owner(tmp_path, identity):
    rows, _ = parse(
        tmp_path, identity,
        '2026-08-01T00:00:00Z trace_id=tr-e service=account_service event=profile_lookup_completed resource_id=account_10 rows=0\n'
        '2026-08-01T00:00:01Z trace_id=tr-e service=account_service event=profile_lookup_started lookup_key=alpha@example.com\n',
    )
    assert rows == []


def test_direct_identifier_in_completed_event_is_not_substring_matched(tmp_path, identity):
    rows, _ = parse(
        tmp_path, identity,
        '2026-08-01T00:00:00Z service=account_service event=profile_lookup_completed '
        'resource_id=account_1 rows=1 customer_reference=user_alpha2\n',
    )
    assert rows == []


def test_compact_readback_accepts_security_resource_and_owner(tmp_path, identity):
    rows, _ = parse(
        tmp_path, identity,
        '- 2026-08-01T00:00:00Z | security_service | audit_record_149 | '
        'SECURITY_AUDIT_LOG | FOUND | user_alpha\n',
    )
    assert [(row.system_id, row.resource_id) for row in rows] == [
        ("security_service", "audit_record_149")
    ]


def test_trace_source_follows_exact_trace_into_result(tmp_path, identity):
    rows, _ = parse(
        tmp_path, identity,
        '2026-08-01T00:00:00Z service=support_replica trace_id=tr-x '
        'event=contact_query_started lookup_key=alpha@example.com source=legacy_contact_index\n'
        '2026-08-01T00:00:01Z service=support_replica trace_id=tr-x '
        'event=contact_query_completed resource_id=support_300 rows=1\n',
    )
    assert len(rows) == 1
    assert rows[0].raw_row["trace_source"] == "legacy_contact_index"
