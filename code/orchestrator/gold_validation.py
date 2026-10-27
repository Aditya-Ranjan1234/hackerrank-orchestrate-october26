"""Run and compare the supplied sample; gold contains only status and steps."""
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

from .pipeline import load_datasets, run_case


@dataclass
class GoldValidationReport:
    total: int
    status_correct: int
    steps_correct: int
    divergences: list[dict]
    regressions: list[str]


def _rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_against_gold(root=None, run=run_case, baseline=None, write=True):
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    gold = {r["case_id"]: r for r in _rows(root / "dataset/sample_output.csv")}
    sample = _rows(root / "dataset/sample_deletion_requests.csv")
    prior = {r["case_id"]: r for r in _rows(baseline)} if baseline else {}
    datasets = None if run is not run_case else load_datasets(root)
    if datasets is not None:
        datasets.active_case_rows = sample
    status_correct = steps_correct = 0
    divergences = []; regressions = []
    for row in sample:
        cid = row["case_id"]
        try:
            result = run(SimpleNamespace(**row), datasets)
            status, steps = result.deletion_status, json.loads(result.steps_json)
            errors = list(result.errors)
        except Exception as exc:
            status, steps, errors = "PIPELINE_CRASH", [], [f"{type(exc).__name__}: {exc}"]
        expected = gold[cid]
        want_steps = json.loads(expected["steps_json"])
        status_ok = status == expected["deletion_status"]
        steps_ok = steps == want_steps
        status_correct += status_ok; steps_correct += steps_ok
        if not status_ok or not steps_ok or errors:
            divergences.append({"case_id": cid, "actual": status,
                "gold": expected["deletion_status"], "type": "PIPELINE_CRASH" if status == "PIPELINE_CRASH" else ("STATUS" if not status_ok else "STEPS"),
                "errors": errors, "trace": f"code/.cache/diagnostics/{cid}.jsonl"})
        if cid in prior and prior[cid]["deletion_status"] == expected["deletion_status"] and not status_ok:
            regressions.append(cid)
    report = GoldValidationReport(len(sample), status_correct, steps_correct, divergences, regressions)
    if write:
        out = root / "code/evaluation/gold_validation_report.md"
        lines = ["# Gold validation", "", f"## 1. Case-level status accuracy\n{status_correct}/{len(sample)} ({100*status_correct/len(sample):.2f}%).", "",
            "## 2. Per-phase accuracy", "Gold provides no intermediate identity/evidence/state/policy labels; Phases 1–4 are not directly measurable. Phase 5 status: " + f"{status_correct}/{len(sample)}. Phase 6 exact steps: {steps_correct}/{len(sample)}.", "",
            "## 3. Per-case divergences", "| case | actual | gold | type | diagnostic trace |", "|---|---|---|---|---|"]
        lines += [f"| {d['case_id']} | {d['actual']} | {d['gold']} | {d['type']} | {d['trace']} |" for d in divergences]
        lines += ["", "## 4. Worst phase", "Not identifiable from gold alone; inspect cited traces for upstream attribution.", "", "## 5. Worst case", (f"{divergences[0]['case_id']} ({divergences[0]['type']}); see trace." if divergences else "None."), "", "## 6. Regression detection", ", ".join(regressions) or "None.", "", "## 7. Recommendations"]
        guidance={
            "case_03":"Ground security audit retention mapping in deletion_rules.csv and suppress unrelated same-system activity inference (evidence_94).",
            "case_21":"Join null-field readback to previously owned full resource ID; compare evidence_02 and evidence_92 timestamps.",
            "case_25":"Join null-field readback to previously owned full resource ID; compare evidence_02 and evidence_92 timestamps.",
            "case_26":"Override older present snapshots with later 404 account readback on exact account_5684 (evidence_92).",
            "case_27":"Reconcile later backup/flow readback against older evidence_02 states using exact resource IDs.",
            "case_28":"Reconcile later backup/flow readback against older evidence_02 states using exact resource IDs.",
            "case_31":"Check evidence_51 tombstone state against explicit retention rule and audit time.",
        }
        lines += [f"- {d['case_id']}: {guidance.get(d['case_id'], 'Inspect cited diagnostic trace and source evidence before a targeted fix.')}" for d in divergences if d['type']=="STATUS"]
        lines += ["", "Intermediate Phase 1–4 correctness cannot be inferred from status alone.", ""]
        out.write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    report = validate_against_gold(baseline=Path(__file__).resolve().parents[2] / "artifacts/csv/sample_output_phase11.csv")
    print(f"{report.status_correct}/{report.total} status, {report.steps_correct}/{report.total} exact steps")
