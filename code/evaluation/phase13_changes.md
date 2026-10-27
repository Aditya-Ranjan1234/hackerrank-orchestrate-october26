# Phase 13 change ledger

The mandatory diff ran before any frozen-code edit. It showed an upstream fact/verdict count problem, not evidence for a Phase 6 code defect. No Phase 1–12 production module was changed. The entries below are diagnostic code and tests; they are not represented as a successful production fix.

## Change 1: Field-by-field step diff
- **Iteration / Fix ID / File:** 13a / step-diff / `code/orchestrator/step_diff.py:1-54`
- **Grounded in:** [step diff](step_diff_report.md#1-aggregate-mismatch-counts), 0/32 exact arrays at Phase 12.
- **Problem / change:** Existing sample comparison reported only aggregate metrics; add `StepDiff`, field classifications, and count accounting.
- **Before:** no `diff_case` or field-level classification.
- **After:** `diff_case` emits one typed mismatch per differing field or extra/missing step.
- **Tests / impact / verification:** 13 parameterized tests in `test_step_diff.py`; step diff report generated.

## Change 2: Aggregate and five-case report
- **Iteration / Fix ID / File:** 13a / step-diff / `code/orchestrator/step_diff.py:55-96`
- **Grounded in:** [step diff](step_diff_report.md#2-dominant-mismatch-type), COUNT_MISMATCH 716/1542.
- **Problem / change:** No report located the dominant divergence or displayed gold side by side. Add aggregate table and five largest full per-case dumps.
- **Before:** no per-case step report.
- **After:** deterministic Markdown report with count, percentages, and full JSON arrays for five cases.
- **Tests / impact / verification:** run `python -m orchestrator.step_diff`; report has 32 cases.

## Change 3: Position-independent alignment diagnostic
- **Iteration / Fix ID / File:** 13a / step-diff / `code/orchestrator/step_diff.py:75-107`
- **Grounded in:** [step diff](step_diff_report.md#4-hypothesis), shifted positions can inflate per-field counts.
- **Problem / change:** Positional mismatches alone cannot distinguish misordering from extra resources. Count exact step identities independent of `step_no` and position.
- **Before:** only index-by-index mismatches.
- **After:** exact overlap 32 of 789 generated step identities versus 193 gold identities.
- **Tests / impact / verification:** deterministic report rerun; confirms missing/extra step identities, not a pure ordering error.

## Change 4: Synthetic diff edge-case tests
- **Iteration / Fix ID / File:** 13a / step-diff / `code/tests/test_step_diff.py:1-38`
- **Grounded in:** [step diff](step_diff_report.md#1-aggregate-mismatch-counts) and kickoff E1–E3.
- **Problem / change:** Status equality could hide step differences; empty arrays and citation mismatches needed explicit coverage.
- **Before:** no step-diff tests.
- **After:** matching/not-applicable, count, field, and three citation-direction tests.
- **Tests / impact / verification:** full suite 197 passing.

## Change 5: Case 03 provenance regression tests
- **Iteration / Fix ID / File:** 13a / case03-regression / `code/tests/test_case03_regression.py:1-27`
- **Grounded in:** [case 03 audit](phase13_case03_regression_audit.md#first-incorrect-decision), `evidence_94` and `activity_3962` source lines.
- **Problem / change:** The old gold status test did not expose the actual first wrong inference. Add readback and proximity provenance tests.
- **Before:** case 03 only visible as an aggregate wrong status.
- **After:** tests prove 404 account readback, retained audit row, and unrelated search activity affiliation by time proximity.
- **Tests / impact / verification:** 3 new tests pass; case 03 remains wrong, so no release claim.

## Frozen-module decision

The report's dominant count mismatch and seven state-phase triage results do **not** justify unfreezing Phase 6 mapper/builder/ordering. Case 03's first wrong decision is in `code/orchestrator/activity_expander.py:57-63`, explicitly frozen by this phase's scope. The six other wrong statuses show the same inferred-affiliation/stale-readback family. A category-map change alone cannot remove the extra resource facts, and a status/step special case would hide them. No such code change was made.
