from orchestrator.log_trace_integrity import scan_text


def test_trace_owner_disagreement_is_flagged():
    source = ("2026-01-01T01:00:00Z trace_id=t1 subject_ref=user_1\n"
              "2026-01-01T01:00:01Z trace_id=t1 resource_id=account_42 email=a@b.test\n")
    counts, problems = scan_text(source, {"user_1": "user_1", "a@b.test": "user_2"})
    assert counts["conflicting_trace_owners"] == 1
    assert any("multiple_canonical_owners" in problem for problem in problems)


def test_future_only_owner_signal_is_flagged():
    source = ("2026-01-01T01:00:00Z trace_id=t1 resource_id=account_42 rows=0\n"
              "2026-01-01T01:00:02Z trace_id=t1 lookup_key=a@b.test\n")
    counts, problems = scan_text(source, {"a@b.test": "user_1"})
    assert counts["resource_lines_with_only_later_owner_signal"] == 1
    assert any("owner_signal_only_after_resource" in problem for problem in problems)


def test_same_time_query_owner_is_not_a_future_join():
    source = ("2026-01-01T01:00:00Z trace_id=t1 lookup_key=a@b.test\n"
              "2026-01-01T01:00:00Z trace_id=t1 resource_id=account_42 rows=0\n")
    counts, problems = scan_text(source, {"a@b.test": "user_1"})
    assert counts["resource_lines"] == 1
    assert counts["resource_lines_with_only_later_owner_signal"] == 0
    assert problems == []
