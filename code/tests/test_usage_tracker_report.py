from agent.llm.usage_tracker import UsageTracker


def test_full_run_usage_report_has_provider_model_and_per_request_average(tmp_path):
    tracker=UsageTracker()
    tracker.record("image_pii","gpt-4o-mini",100,20,"case_1")
    tracker.request_count=2
    path=tmp_path/"usage_report.md"
    tracker.write_report(path)
    report=path.read_text(encoding="utf-8")
    assert "Provider: OpenAI" in report
    assert "gpt-4o-mini" in report
    assert "Requests in run: 2" in report
    assert "Average input tokens/request: 50.00" in report
    assert "average output tokens/request: 10.00" in report


def test_sample_run_cannot_overwrite_submission_usage_report():
    from pathlib import Path
    from orchestrator.run import _usage_path,_validation_path
    root=Path(__file__).resolve().parents[2]
    assert _usage_path(root,root/'dataset/deletion_requests.csv',root/'output.csv')==root/'code/evaluation/usage_report.md'
    assert _usage_path(root,root/'dataset/sample_deletion_requests.csv',root/'artifacts/csv/sample.csv')!=root/'code/evaluation/usage_report.md'
    assert _validation_path(root,root/'dataset/sample_deletion_requests.csv',root/'artifacts/csv/sample.csv')!=root/'code/evaluation/phase7_orchestrator_validation.md'
