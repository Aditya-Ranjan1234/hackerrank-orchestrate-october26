from orchestrator.log_inspector import inspect_log


def test_log_format_classification(tmp_path):
    path = tmp_path / "a.log"
    path.write_text('{"system_id":"account_service","user_id":"U1"}\n2026-01-01 service=account_service user_id=U1\nplain text', encoding="utf-8")
    result = inspect_log(path)
    assert result["line_count"] == 3
    assert result["formats"] == {"jsonl": 1, "key_value": 1, "pipe": 0, "free_text": 1}


def test_log_pipe_and_samples(tmp_path):
    path = tmp_path / "b.log"
    path.write_text("a|b|c|d|e|f", encoding="utf-8")
    result = inspect_log(path)
    assert result["formats"]["pipe"] == 1 and result["first_lines"] == result["last_lines"]


def test_jsonl_handler_exact_subject_and_audit_cutoff(tmp_path):
    from types import SimpleNamespace
    from agent.evidence.handlers.log_handler import extract
    path = tmp_path / "c.log"
    path.write_text('{"timestamp":"2026-09-01T00:00:00Z","system_id":"account_service","resource_id":"account_1","user_id":"U1","state":"ABSENT"}\n'
                    '{"timestamp":"2026-09-03T00:00:00Z","system_id":"account_service","resource_id":"account_1","user_id":"U1","state":"PRESENT"}', encoding="utf-8")
    identity = SimpleNamespace(all_user_ids={"U1"}, all_emails=set())
    before, after = extract(path, "ev", identity, "2026-09-02T00:00:00Z")
    assert len(before) == len(after) == 1 and before[0].state_at_evidence == "ABSENT"
