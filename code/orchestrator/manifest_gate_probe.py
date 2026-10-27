"""Evaluation-only probe: exclude entire evidence files captured after audit."""

import csv
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from .csv_writer import write_output
from .evidence_time import apply_manifest_capture, _parse
from .pipeline import load_datasets, run_case
from .step_diff import build_report, _read


def gate_file_at_capture(evidence, manifest_row, audit_at):
    captured = _parse(manifest_row.get("captured_at"))
    cutoff = _parse(audit_at)
    if captured and cutoff and captured > cutoff:
        evidence.records_post_audit.extend(evidence.records)
        evidence.records = []
        evidence.notes.append("probe_file_captured_after_audit")
        return evidence
    return apply_manifest_capture(evidence, manifest_row, audit_at)


def run_probe(root):
    root = Path(root)
    with (root / "dataset/sample_deletion_requests.csv").open(encoding="utf-8-sig", newline="") as stream:
        requests = list(csv.DictReader(stream))
    data = load_datasets(root)
    with patch("orchestrator.pipeline.apply_manifest_capture", gate_file_at_capture):
        results = [run_case(SimpleNamespace(**row), data) for row in requests]
    output = root / "artifacts/csv/phase17_manifest_gate_probe.csv"
    write_output([(row.case_id, row.deletion_status, row.steps_json) for row in results], output)
    gold = root / "dataset/sample_output.csv"
    diffs, _ = build_report(output, gold)
    statuses = sum(diff.status_match for diff in diffs)
    exact = sum(diff.step_array_match for diff in diffs)
    return output, statuses, exact, results


if __name__ == "__main__":
    output, statuses, exact, results = run_probe(Path(__file__).resolve().parents[2])
    print(f"strict-file-capture probe: {statuses}/32 statuses, {exact}/32 exact arrays; "
          f"errors={sum(bool(result.errors) for result in results)}; {output}")
