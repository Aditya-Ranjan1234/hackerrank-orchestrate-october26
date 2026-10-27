# Submission candidate manifest — reviewed revision

The assistant reviewed all 518 original output plans and the 115 changed final rows. The corrected root output has **518 rows, 2,894 steps; 134 COMPLETE, 374 INCOMPLETE, 10 NOT_APPLICABLE**. Compared with the preserved 21.6/30 output, 115 rows and 34 statuses changed. The new hidden score is **unmeasured**; >28/30 is not established.

| Artifact | Repository path | Current state |
|---|---|---|
| Prediction CSV | `output.csv` | 518 unique naturally sorted rows; 19,440/19,440 structural checks; no errors or warnings |
| Exact changed-row ledger | `artifacts/csv/changed_rows.csv` | 115 rows; row numbers, reasons, complete before/after arrays and added/removed steps |
| All-row review | `artifacts/csv/all_518_row_review.csv` | Every one of 518 cases; visible plan result, final states and evidence limits |
| Readable correction report | `code/evaluation/changed_rows.md` | Changed rows and all flagged limits |
| Runnable solution and evaluation reports | `code.zip` | Rebuilt; 405 ZIP entries; integrity verified and configured credential absent |
| Development work record | `log.txt` | Append-only Codex entries; include with the required chat transcript |
| Codex trace snapshot | `agent-trace.zip` | Earlier snapshot, **not refreshed for this review**; refresh before a final trace submission |

The hidden evaluation has no public labels. Local checks find zero contradictions against the 1,588 recorded policy obligations, zero invalid references among 1,010 cited steps, complete diagnostics for all 518 cases and no answer-leak dependencies among 70 production modules. **502 tests pass and one existing exact-array gate fails.** The public sample has 32/32 matching statuses and 12/32 exact arrays. The older 85% dual gate remains **NOT_READY**.

Thirty-two full rows carry explicit evidence-limit notes. One COMPLETE row remains without verification; 23 citations are later-captured observations; six cases have workflow-only absence claims. Other noted limits include a screenshot/catalog owner conflict, backup access proof and a separate owner join. See `code/evaluation/score_iteration_validation.md`. This is the requested source-reviewed revision, not a claim that every hidden row is correct.

For submission, use the revised `output.csv` and rebuilt `code.zip`, plus the contest's requested chat transcript/trace and AI interview. The change ledgers are review artifacts, not extra prediction rows. `code.zip` excludes dataset/, .env, .venv/, .cache/, .git/, __pycache__/ and .pyc. It contains the required root `evaluation/evaluation_report.md` and `evaluation/usage_report.md`. The prior scored CSVs and prior source archive are preserved under `artifacts/csv/` and `artifacts/submissions/`.

SHA-256 output.csv: `ed5af1b6733958a82d12b2d5ff0390ce39132a9ced0b062b870e3de0dbc3f20b`.

SHA-256 code.zip: `c86547b0d3bba3807b90acd09d3a1f20548c2b7e333ba3db6b45591d286bdb8a`.

The existing earlier trace ZIP has SHA-256 `65378F0890E5B07C9DB325541486F3AF5571BB0D70ADA182CA6DC790CA45666A`; it does not contain this review's final turns. No external submission was made during this task.
