from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from orchestrator.sample_gold_backtrace import (
    exact, json_record_ownership, other_input_occurrences,
)


def test_exact_identifier_does_not_match_longer_user_or_resource():
    assert exact("account_1", "resource_id=account_1")
    assert not exact("account_1", "resource_id=account_10")
    assert not exact("user_1", "subject=user_10")


def test_json_owner_can_be_nested_in_same_record(tmp_path):
    source = tmp_path / "records.json"
    source.write_text('{"records":[{"resource_id":"account_8",'
                      '"profile":{"email":"a@example.com"}},'
                      '{"resource_id":"account_9",'
                      '"profile":{"email":"b@example.com"}}]}',
                      encoding="utf-8")
    assert json_record_ownership(source, "account_8", {"a@example.com"}) == (1, 1)
    assert json_record_ownership(source, "account_9", {"a@example.com"}) == (1, 0)


def test_unrelated_json_sibling_does_not_supply_owner(tmp_path):
    source = tmp_path / "records.json"
    source.write_text('{"records":[{"resource_id":"account_8",'
                      '"profile":null},{"resource_id":"account_9",'
                      '"profile":{"email":"a@example.com"}}]}',
                      encoding="utf-8")
    assert json_record_ownership(source, "account_8", {"a@example.com"}) == (1, 0)


def test_other_input_scan_uses_exact_full_id_and_no_answer_file():
    inputs = {
        "system_activity.csv": "resource_id=account_0010",
        "deletion_requests.csv": "request for account_001",
    }
    assert other_input_occurrences("account_001", inputs) == ["deletion_requests.csv"]
    assert other_input_occurrences("audit_record_6645", inputs) == []


def test_json_owner_accepts_exact_hash_in_same_record_only(tmp_path):
    source = tmp_path / "records.json"
    digest = "a" * 64
    source.write_text(
        '{"records":[{"resource_id":"analytics_8","email_hash":"' + digest + '"},'
        '{"resource_id":"analytics_9","email_hash":null}]}',
        encoding="utf-8",
    )
    assert json_record_ownership(source, "analytics_8", {digest}) == (1, 1)
    assert json_record_ownership(source, "analytics_9", {digest}) == (1, 0)
