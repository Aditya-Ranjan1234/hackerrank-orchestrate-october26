# Phase 2 — Evidence Ingestion and State Reconstruction

## Handler coverage matrix

| Handler | Fixture | Records | LLM calls | Tokens | Result |
|---|---|---:|---:|---:|---|
| JSON | synthetic JSON | 1 | 0 | 0 | PASS |
| SQLite SQL | synthetic SQL | 1 | 0 | 0 | PASS |
| Log | synthetic pre/post-cutoff log | 1 + 1 post-audit | 0 | 0 | PASS |
| PDF | synthetic text PDF | 0 relevant | 0 | 0 | PASS |
| Image | malformed fake VLM | 0 | 2 retries | 0 | PASS |
| Cache | synthetic ExtractedEvidence | round-trip | 0 | 0 | PASS |

## Cache behavior

The cache is keyed by SHA-256 of file bytes and stores JSON under
`code/.cache/evidence/`. The round-trip test confirms a second load returns the
cached extraction. Identical fixture hit rate: 100% after the first run.

## Conflict-resolution cases tested

- Simple delete: `DELETE_RECORD` produces `ABSENT`.
- Sync recreation: a later `SYNC_RECORD` produces `PRESENT`.
- Restore override: a later `RESTORE_BACKUP` produces `PRESENT`.
- Evidence/activity conflict: evidence state `PRESENT` overrides activity `ABSENT` and records a note.
- Log post-audit event: retained in `records_post_audit`, excluded from normal records.

## Failures found and fixes

- Fixed Phase 2 test import to avoid requiring a non-existent IR symbol.
- Fixed package imports by adding the agent package boundary and test path setup.
- Fixed JSON identity-object handling and converted regex hit dictionaries into typed `PIIHit` values for log records.
- Kept image/VLM handling offline-safe with a two-attempt strict JSON stub.
- Missing files return a non-throwing empty extraction with `missing_file`.

## Token usage so far

No real LLM or VLM calls were made. Phase 2 token usage is 0 input tokens and
0 output tokens.

## Open questions for Phase 3

- Active-flow and restore-risk inference needs to use the actual activity/evidence vocabulary.
- Scanned-PDF VLM routing is deferred when optional rendering dependencies are absent.
- Resource category mapping will be finalized by the Phase 4 policy layer.

## Final regression result

```text
14 passed in 0.09s
```
