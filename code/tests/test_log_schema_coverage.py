from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from orchestrator.log_schema_coverage import direct_source_pairs


def test_source_pair_requires_structured_owner_value():
    index = {"alpha@example.com": "user_a"}
    text = (
        '2026-01-01T00:00:00Z resource_id="account_1" note="alpha@example.com"\n'
        '2026-01-01T00:00:01Z resource_id="account_2" subject_reference="alpha@example.com"\n'
    )
    assert direct_source_pairs(text, index) == {("account_2", "user_a")}


def test_source_query_start_is_not_presence():
    index = {"user_a": "user_a"}
    text = (
        '2026-01-01T00:00:00Z resource_id="account_1" event="lookup_started" subject_reference="user_a"\n'
        '2026-01-01T00:00:01Z resource_id="account_1" event="lookup_completed" subject_reference="user_a"\n'
    )
    assert direct_source_pairs(text, index) == {("account_1", "user_a")}


def test_plain_text_handover_owner_and_resource_are_same_row():
    index = {"alpha@example.com": "user_a"}
    text = (
        "- 2026-10-01T12:00:00Z | account_service | account_1 | USER_PROFILE | NOT_FOUND | ALPHA@EXAMPLE.COM\n"
        "- 2026-10-01T12:00:00Z | account_service | account_2 | USER_PROFILE | NOT_FOUND | no direct identifier\n"
        "- background | account_service | account_3 | USER_PROFILE | NOT_FOUND | ALPHA@EXAMPLE.COM\n"
    )
    assert direct_source_pairs(text, index) == {("account_1", "user_a")}


def test_source_pair_accepts_exact_historical_email_hash():
    digest = "a" * 64
    index = {digest: "user_a"}
    text = f'2026-01-01T00:00:00Z resource_id="analytics_1" email_hash="{digest}"\n'
    assert direct_source_pairs(text, index) == {("analytics_1", "user_a")}
