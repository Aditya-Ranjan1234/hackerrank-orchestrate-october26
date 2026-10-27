"""The sample answer may be read by evaluators, never by the production agent."""

import ast
import builtins
import csv
from pathlib import Path
from types import SimpleNamespace

from orchestrator.leakage_audit import (
    EVALUATION_MODULES,
    _local_imports,
    audit_production,
    inspect_tree,
    module_files,
)


ROOT = Path(__file__).resolve().parents[2]


def test_production_import_closure_excludes_sample_answer_tools_and_literals():
    modules, findings = audit_production(ROOT / "code")
    assert "orchestrator.pipeline" in modules
    assert "agent.steps.generator" in modules
    assert not EVALUATION_MODULES.intersection(modules)
    assert findings == []


def test_static_audit_follows_relative_imports_in_packages(tmp_path):
    package = tmp_path / "orchestrator"
    package.mkdir()
    (package / "__init__.py").write_text("from .answer_reader import read_answer\n", encoding="utf-8")
    (package / "run.py").write_text("from . import answer_reader\n", encoding="utf-8")
    (package / "answer_reader.py").write_text(
        "def read_answer():\n    return 'dataset/sample_output.csv'\n", encoding="utf-8"
    )
    modules, findings = audit_production(tmp_path)
    assert "orchestrator.answer_reader" in modules
    assert any(item.kind == "gold_file_literal" for item in findings)


def test_static_audit_flags_case_specific_output_knowledge():
    tree = ast.parse("RESOURCE_OVERRIDE = {'case_03': 'analytics_9406'}")
    findings = inspect_tree("orchestrator.pipeline", tree)
    assert any(item.kind == "case_specific_literal" for item in findings)


def test_production_run_never_reads_gold_or_earlier_output(monkeypatch):
    from orchestrator.pipeline import load_datasets, run_case

    forbidden_attempts = []
    original_path_open = Path.open
    original_builtin_open = builtins.open

    def check(path, mode):
        name = Path(path).name.casefold() if isinstance(path, (str, bytes, Path)) else ""
        if ("r" in mode or "+" in mode) and (name.startswith("sample_output") or name == "output.csv"):
            forbidden_attempts.append(str(path))
            raise AssertionError("production attempted to read an answer file")

    def guarded_path_open(path, mode="r", *args, **kwargs):
        check(path, mode)
        return original_path_open(path, mode, *args, **kwargs)

    def guarded_builtin_open(path, mode="r", *args, **kwargs):
        check(path, mode)
        return original_builtin_open(path, mode, *args, **kwargs)

    monkeypatch.setenv("OPENAI_LLM_DISABLED", "1")
    monkeypatch.setattr(Path, "open", guarded_path_open)
    monkeypatch.setattr(builtins, "open", guarded_builtin_open)
    datasets = load_datasets(ROOT)
    with (ROOT / "dataset/deletion_requests.csv").open(encoding="utf-8-sig", newline="") as stream:
        case = SimpleNamespace(**next(csv.DictReader(stream)))
    result = run_case(case, datasets)
    assert result.case_id == case.case_id
    assert forbidden_attempts == []


def test_reported_status_is_unread_and_report_time_stays_out_of_decision(tmp_path, monkeypatch):
    from orchestrator.pipeline import run_case
    from agent.status.determinator import StatusDeterminator

    original_decide = StatusDeterminator.decide

    def guarded_decide(self, case, identity, verdicts):
        # The timestamp can correlate an ownerless workflow event, but neither
        # claim may become a status input or a case-specific answer shortcut.
        assert not hasattr(case, "reported_status")
        assert not hasattr(case, "reported_at")
        return original_decide(self, case, identity, verdicts)

    monkeypatch.setattr(StatusDeterminator, "decide", guarded_decide)

    class Request:
        case_id = "synthetic_request"
        email = "a@example.com"
        requested_at = "2026-09-01T00:00:00Z"
        audit_at = "2026-09-02T00:00:00Z"
        request_text = "Delete my account"

        @property
        def reported_status(self):
            raise AssertionError("reported status was read")

        reported_at = "2026-09-01T12:00:00Z"

    identity = SimpleNamespace(primary_user_id="U1", all_user_ids={"U1"}, all_emails={"a@example.com"})
    datasets = SimpleNamespace(
        root=tmp_path,
        resolver=SimpleNamespace(resolve=lambda *_: identity),
        manifest=[], activities=[], rules=[],
        _llm_client=SimpleNamespace(enabled=False),
    )
    result = run_case(Request(), datasets)
    assert result.case_id == "synthetic_request"
