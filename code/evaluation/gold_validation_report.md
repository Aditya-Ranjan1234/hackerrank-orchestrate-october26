# Gold validation

## 1. Case-level status accuracy
32/32 (100.00%).

## 2. Per-phase accuracy
Gold provides no intermediate identity/evidence/state/policy labels; Phases 1–4 are not directly measurable. Phase 5 status: 32/32. Phase 6 exact steps: 12/32.

## 3. Per-case divergences
| case | actual | gold | type | diagnostic trace |
|---|---|---|---|---|
| case_01 | COMPLETE | COMPLETE | STEPS | code/.cache/diagnostics/case_01.jsonl |
| case_02 | COMPLETE | COMPLETE | STEPS | code/.cache/diagnostics/case_02.jsonl |
| case_03 | COMPLETE | COMPLETE | STEPS | code/.cache/diagnostics/case_03.jsonl |
| case_04 | COMPLETE | COMPLETE | STEPS | code/.cache/diagnostics/case_04.jsonl |
| case_07 | INCOMPLETE | INCOMPLETE | STEPS | code/.cache/diagnostics/case_07.jsonl |
| case_08 | INCOMPLETE | INCOMPLETE | STEPS | code/.cache/diagnostics/case_08.jsonl |
| case_10 | INCOMPLETE | INCOMPLETE | STEPS | code/.cache/diagnostics/case_10.jsonl |
| case_18 | INCOMPLETE | INCOMPLETE | STEPS | code/.cache/diagnostics/case_18.jsonl |
| case_20 | INCOMPLETE | INCOMPLETE | STEPS | code/.cache/diagnostics/case_20.jsonl |
| case_21 | COMPLETE | COMPLETE | STEPS | code/.cache/diagnostics/case_21.jsonl |
| case_22 | INCOMPLETE | INCOMPLETE | STEPS | code/.cache/diagnostics/case_22.jsonl |
| case_23 | INCOMPLETE | INCOMPLETE | STEPS | code/.cache/diagnostics/case_23.jsonl |
| case_25 | COMPLETE | COMPLETE | STEPS | code/.cache/diagnostics/case_25.jsonl |
| case_26 | COMPLETE | COMPLETE | STEPS | code/.cache/diagnostics/case_26.jsonl |
| case_27 | COMPLETE | COMPLETE | STEPS | code/.cache/diagnostics/case_27.jsonl |
| case_28 | COMPLETE | COMPLETE | STEPS | code/.cache/diagnostics/case_28.jsonl |
| case_29 | INCOMPLETE | INCOMPLETE | STEPS | code/.cache/diagnostics/case_29.jsonl |
| case_30 | INCOMPLETE | INCOMPLETE | STEPS | code/.cache/diagnostics/case_30.jsonl |
| case_31 | COMPLETE | COMPLETE | STEPS | code/.cache/diagnostics/case_31.jsonl |
| case_32 | INCOMPLETE | INCOMPLETE | STEPS | code/.cache/diagnostics/case_32.jsonl |

## 4. Worst phase
Not identifiable from gold alone; inspect cited traces for upstream attribution.

## 5. Worst case
case_01 (STEPS); see trace.

## 6. Regression detection
None.

## 7. Recommendations

Intermediate Phase 1–4 correctness cannot be inferred from status alone.
