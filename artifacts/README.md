# Evaluation and submission artifacts

- `csv/`: historical sample runs, scored input copies, diffs and final row-review ledgers.
- `submissions/`: historical code package snapshots, retained for comparison.
- Current prediction and submission snapshots remain at repository root: `output.csv`, `code.zip`. The redacted public trace is `submissions/agent-trace-public.zip`; the original root trace remains local.

Historical predictions are evaluation artifacts, not agent inputs or ground truth. Local `interview_prep/` inspection copies belong to a separate four-file analysis and are excluded from this original project's Git history.
