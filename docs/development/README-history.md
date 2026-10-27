# Historical README before repository organization

These are historical development notes. For the current project overview and reported contest results, see [README](../../README.md). Relative links below reflect the original repository-root location.

# Northstar Shop Deletion Audit Agent

**Current revision — assistant review of the scored output:** all 518 row plans were reviewed; 115 rows changed, including 34 status decisions. The root CSV has 518 rows and passes 19,440 structural checks. See [changed rows](code/evaluation/changed_rows.md), [all-row review](artifacts/csv/all_518_row_review.csv), and [validation and limits](code/evaluation/score_iteration_validation.md). Tests: 502 pass, one existing exact-step gate fails; public sample: 32/32 statuses, 12/32 exact arrays. The revised hidden score is unmeasured. This section supersedes historical current-run metrics below.

This project audits whether customer data was actually deleted across primary records, replicas, logs, exports, flows, and backups. It produces ordered JSON step plans and validates the final CSV.

## Architecture

```text
1 identity → 2 evidence/state → 3 flows/restore → 4 policy → 5 status → 6 steps → 7 orchestration
```

The rule-based phases are tested independently. The orchestrator uses bounded
`gpt-4o-mini` calls for ambiguous semantic labels, citations, full-image
Vision, and a two-round read-only tool-planning loop when evidence conflicts.
Vision uses strict JSON Schema, retries malformed output, and checks exact IDs
against OCR (or a second Vision reading when OCR is empty). The model suggests;
identifiers, row ownership, policy and state transitions remain evidence-bound.
Per-case errors are isolated and traced.

Each run walks all 94 manifest entries **for each case**. These are local
point-in-time files, not live connections to Northstar systems. File bytes are
read to identify changed content; non-image extraction is cached on disk under
`code/.cache/evidence/` by file bytes, identity, audit time and extractor
fingerprint. Image OCR and model responses have separate content/prompt-aware
caches. A cache hit skips recomputation/API use, but changing source bytes or
the relevant extractor invalidates it. The cache is excluded from submission.
The [dataset catalog](code/evaluation/dataset_catalog.md),
[image text audit](code/evaluation/image_text_inventory.md), and
[SQL schema audit](code/evaluation/schema_mapping_audit.md) enumerate coverage.
The independent SQL pass checks 186 direct owner-column rows and 530 nested
JSON payload rows across 127 tables, including historical email aliases,
with zero extraction omissions.

## Setup and run

```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
$env:PYTHONPATH='code'
.\.venv\Scripts\python.exe -m orchestrator.run dataset/deletion_requests.csv output.csv
```

Use `ORCHESTRATOR_SKIP_EVIDENCE=1` only for a fast structural diagnostic run;
the CLI marks such a run fatal so it cannot be mistaken for a submission audit.

## Validate and compare

```powershell
$env:PYTHONPATH='code'
.\.venv\Scripts\python.exe -c "from orchestrator.validator import validate_output; print(validate_output('output.csv','dataset/deletion_requests.csv').errors)"
.\.venv\Scripts\python.exe -m orchestrator.step_diff
.\.venv\Scripts\python.exe -m orchestrator.schema_mapping_audit
.\.venv\Scripts\python.exe -m orchestrator.json_owner_coverage
.\.venv\Scripts\python.exe -m orchestrator.log_schema_coverage
.\.venv\Scripts\python.exe -m orchestrator.csv_schema_audit
.\.venv\Scripts\python.exe -m orchestrator.leakage_audit
.\.venv\Scripts\python.exe -m orchestrator.log_trace_integrity
.\.venv\Scripts\python.exe -m orchestrator.citation_audit
.\.venv\Scripts\python.exe -m orchestrator.runtime_diagnostics_audit
.\.venv\Scripts\python.exe -m orchestrator.workflow_output_audit
.\.venv\Scripts\python.exe -m orchestrator.sample_gold_backtrace artifacts/csv/phase17_final_sample.csv
.\.venv\Scripts\python.exe -m orchestrator.step_gap_diagnosis
.\.venv\Scripts\python.exe -m orchestrator.temporal_owner_probe
.\.venv\Scripts\pytest.exe code/tests -q
.\.venv\Scripts\python.exe -m orchestrator.repackage
```

## File structure

`code/agent/` contains phases 1–6; `code/orchestrator/` contains phase 7;
`code/evaluation/` contains reports; `dataset/` contains inputs; `output.csv`
is the final output; `tradeoff.md` records design reasoning.

## Design decisions

See [tradeoff.md](tradeoff.md) for deterministic decisions, cutoff-aware
evidence, strict ordering, fail-closed policies, and per-case isolation.

## Known limitations

Historical Phase 8 and Phase 16 results are superseded by the current run. The latest
authenticated sample matches **32/32 statuses but only 13/32 exact step
arrays**; rerun the comparator after source or prompt changes. The 85% dual
release gate is therefore **NOT MET**. Several gold
steps require an identity-to-resource link not present in the supplied files;
the agent does not infer such ownership from case-number suffixes or page/file
co-mentions. A unique account deletion in a source-calibrated report-time
window can supply a bounded workflow affiliation, with known-owner and
ambiguity vetoes. An activity-only SUCCESS cannot prove a COMPLETE account
verification: the completion-proof gate instead requests a future check with
an empty citation until a source readback corroborates absence. See
`code/evaluation/workflow_affiliation_validation.md`, `code/evaluation/step_diff_report.md`,
and `code/evaluation/step_gap_diagnosis.md`. The last report pinpoints the
first failed pipeline link for all 25 remaining missing steps. Three COMPLETE sample
cases have zero policy verdicts, so status agreement alone is not proof of
resource coverage. `code/evaluation/case01_process_trace.md` examines the
17-second deletion activity and later SQL snapshot for case 01, including
the missing negative-snapshot citation path.
A fast no-evidence diagnostic mode exists for structural validation only.

The full 518-row candidate passes 18,864/18,864 structural checks and citation-ID checks, but nine
COMPLETE rows have no resource verification and 29 citations use files captured
after the audit cutoff even though their observed rows predate it. These are
tracked as evidence-quality risks in the validation report.

The production import graph and a runtime read guard exclude `sample_output.csv`
and previous `output.csv` from agent input. The 32 sample answers have been
used repeatedly in development, so this score measures development fit rather
than unbiased hidden-case performance. The other 486 cases have no answer labels.

## Submission checklist

The contest requests `code.zip`, root `output.csv`, a `chat_transcript`, and an
AI interview. Submit root `log.txt` as the append-only development transcript
specified by `AGENTS.md`; `worklog.md` is supporting documentation.
`agent_trace_instructions.md` also requests `agent-trace.zip` containing the
relevant Codex session files after the session closes; review it for credentials
and unrelated sessions before sharing. The candidate currently fails
the exact-step release gate; do not present structural validation as approval
to submit it. Prepare the AI interview using `tradeoff.md` and the phase reports.

## Optional OpenAI semantic and Vision extraction

Install dependencies into the repository-local virtual environment using
`python -m pip install -r requirements.txt`. Put `OPENAI_API_KEY` in the
repository-local `.env` file to enable the five bounded decisions: unresolved system labels,
flow-vs-record classification, corroborated anonymous affiliation, citation
selection, and image extraction. `OPENAI_MODEL` defaults to `gpt-4o-mini`;
`OPENAI_TIMEOUT` defaults to 30 seconds and `OPENAI_MAX_RETRIES` to 3.
Image extraction uses local RapidOCR to read exact visible rows, plus a cached
high-detail `gpt-4o-mini` transcript of each screenshot. Model rows are
accepted only after schema and visible-identifier checks; OCR/model
disagreements are listed in `code/evaluation/image_text_inventory.md`.
RapidOCR is installed from `requirements.txt`; no external Tesseract
executable is required. Never commit or package
`.env`; this repository-local file is the sole API-key source.

Without a key in that `.env`, the pipeline retains its rule-only path. A
process-level `OPENAI_API_KEY` is deliberately ignored. With the local key, API calls
are cached and traced under `code/.cache/` (excluded from `code.zip`) and
actual response token counts are appended to `code/evaluation/usage_report.md`.
For offline tests only, `OPENAI_LLM_DISABLED=1` disables live calls without
removing or changing `.env`.
The model is not permitted to infer user ownership merely from nearby rows or
numeric suffixes. The bounded account workflow rule is calibrated on independently
owned full-input accounts; a five-minute nearest-time rule failed its controls.
These constraints can limit exact match against
sample output when the supplied evidence lacks an identity-to-resource link.
The independent source checks now recover 544/544 direct JSON owner/resource
pairs and 713/713 direct structured text pairs (674 log and 39 handover rows,
including historical hashes). All 20 shared-step sample citation differences
were resolved by preferring contemporaneously captured
evidence when the same state is supported; 25 semantic steps remain missing.
The case-level evidence backtrace is in
`code/evaluation/sample_gold_backtrace.md`. A gold-free timing probe found
that the account activity nearest reported time belonged to the directly
known requester in only 71/212 evaluable full requests. The 30–90-minute
unique-action rule had 26/26 correct owners among independently attributed
controls (14/14 when the unique winner was successful). A SUCCESS-only
prefilter falsely matched another owner in 48/90 known controls and is rejected.
The corrected rule is the only time-based affiliation
currently admitted, and the diagnostic trace records every abstention.
The submission archive also contains `code/requirements.txt` for installation
after unpacking `code.zip`. Authentication failures are traced and trigger the
rule-only fallback. The earlier uncached full candidate recorded 266 successful
`gpt-4o-mini` responses; the final 518-row regeneration made 10 fresh responses
and reused the model cache for earlier decisions. `usage_report.md` separates
current API usage from historical charges.

The sample cases are separate from the 518 full-run case IDs. A structurally
valid full `output.csv` does not establish gold accuracy. The current
`output.csv` is a candidate while the 85% exact-step gate is unmet; check
`code/evaluation/workflow_affiliation_validation.md` before submitting it.

Phase 17 opened all 94 evidence files and backtraced the original 26 missing sample
semantic steps. See `code/evaluation/dataset_catalog.md`,
`code/evaluation/document_text_inventory.md`,
`code/evaluation/image_text_inventory.md`,
`code/evaluation/cases_01_02_03_04_31_audit.md`, and
`code/evaluation/phase17_validation.md` for the preceding baseline and
`code/evaluation/workflow_affiliation_validation.md` for current readiness. Historical
sample CSV runs are grouped in `artifacts/csv/`; the required root `output.csv`
and `dataset/*.csv` retain their original paths. A compatibility collection of
phase validation reports is under `code/evaluation/validations/`.

The current source-owner veto scans all manifest formats, including historical
emails in the text handover, PDFs and local image OCR. It does not read sample
answers. `reported_at` is used only by the bounded activity affiliator; the
projected case sent to status determination and model tools excludes it and
`reported_status`. The full 518-case output and actual model usage are in
`code/evaluation/workflow_affiliation_validation.md` and `code/evaluation/usage_report.md`.
Structured log `enabled` and `restore_allowed` flags now retain Boolean types,
so an explicit disabled connector bypasses model type guessing; this source
repair changed six full-input cases from INCOMPLETE to COMPLETE without altering
the public sample. The source-only rejection controls for anonymous analytics
joins and the full-run parser trace are in `code/evaluation/anonymous_affiliation_controls.md`
and `code/evaluation/log_boolean_regression.md`.

