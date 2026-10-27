# Phase 12 grounded change ledger

Each entry cites the supplied dataset or an earlier grounded diagnosis. The registry API remained backward compatible; the prompt's hypothetical `extract_evidence` and `relevant_files` APIs do not exist in this checkout, so inventing them would have broken callers.

## Change 1: Full identity propagation
- **Iteration / Fix ID / File:** 12a / A / `code/agent/evidence/registry.py:8-19`, `code/orchestrator/pipeline.py:46-48`
- **Grounded in:** `phase11_changes.md`, case 08, and `dataset/evidence/records/customer_export_*.json` owner-email rows.
- **Problem / change:** JSON received only `all_user_ids`; pass the whole bundle and audit time. Pipeline already passed these to the registry, so only registry dispatch changed.
- **Before:** `json_handler.extract(path,file_id,identities.all_user_ids)`
- **After:** `json_handler.extract(path,file_id,identities,audit_at)`
- **Tests / impact / verification:** `test_registry_passes_email`; cases 08 and 09 recovered in 12a; sample comparison.

## Change 2: JSON email/hash and timestamp matching
- **Iteration / Fix ID / File:** 12a / B.1 / `code/agent/evidence/handlers/json_handler.py:38-83`
- **Grounded in:** `phase11_changes.md` changes 2–3; `dataset_grounding_report.md` evidence inventory.
- **Problem / change:** Hash-only records were ignored and post-audit records could be emitted; exact email/hash matching and per-record cutoff were added. A nested pre-audit snapshot overrides a later export timestamp.
- **Before:** `emails=set(identities.all_emails)`; no hash matching.
- **After:** normalized emails and optional hashes; `if user and (not cutoff or not ts or ts<=cutoff)`.
- **Tests / impact / verification:** `test_json_email_only`, `test_json_hash_only`, `test_json_post_audit_rejected`, `test_json_id_and_email_one_record`; 181-test suite.

## Change 3: SQL scalar identity columns
- **Iteration / Fix ID / File:** 12a / B.2 / `code/agent/evidence/handlers/sql_handler.py:6-35`
- **Grounded in:** `dataset_grounding_report.md` SQL inventory and `dataset/evidence/databases/customer_data_read_replica_20260921.sql:37,52,75`.
- **Problem / change:** Only a narrow scalar-column set was inspected. Contact/billing/shipping email and optional hash are now accepted by exact value, and row system/timestamp fields are preserved.
- **Before:** candidate set limited to `email,user_id,user_uuid,account_id` and a few unrelated PII columns.
- **After:** expanded identity-column set, exact matching against IDs/emails/hashes.
- **Tests / impact / verification:** `test_sql_email_and_hash`; case 16 recovery after 12b.

## Change 4: Structured logs and trace joins
- **Iteration / Fix ID / File:** 12b / B.3 / `code/agent/evidence/handlers/log_handler.py:8-54`
- **Grounded in:** `dataset/evidence/logs/support_replica.log:4-6` and `dataset/evidence/logs/service_events_ap_south_20260915.log:11,15,36`.
- **Problem / change:** Logs use `service=` and trace IDs rather than only bracket tags; the handler now joins same-trace resource lines to a subject identifier and recognizes exact hash/email values.
- **Before:** `if not tag: continue`; generic file-line resource IDs.
- **After:** `service=` or bracket tag; `trace_id` correlation; visible `resource_id`.
- **Tests / impact / verification:** `test_log_service_trace`; sample improved from 15/32 to 23/32 after fixing a local-import error.

## Change 5: Plain-text handover rows
- **Iteration / Fix ID / File:** 12b / targeted-case_11 / `code/agent/evidence/handlers/log_handler.py:11-34`
- **Grounded in:** `dataset/evidence/records/customer_account_handover_20261001.txt:11,16,25,26,46`.
- **Problem / change:** Pipe-delimited readbacks were ignored. Parse visible timestamp, system, resource, state, and email without inference from numeric suffixes.
- **Before:** untagged `.txt` lines skipped.
- **After:** `PIPE` rows produce timestamped `RecordState` objects.
- **Tests / impact / verification:** `test_log_pipe_row`; cases 11, 13, 14 recovered.

## Change 6: PDF scoped identity matching
- **Iteration / Fix ID / File:** 12a / B.4 / `code/agent/evidence/handlers/pdf_handler.py:4-22`
- **Grounded in:** `dataset_grounding_report.md` PDF inventory.
- **Problem / change:** The generic `hits` helper returned unrelated emails and only ID-scoped matching was useful; filter to bundle IDs/emails/hashes. Audit time is accepted by the handler API, but no page timestamp is inferred.
- **Before:** `hs=hits(text,...,identities.all_user_ids)` including all detected emails.
- **After:** exact scoped ID/email/hash hits.
- **Tests / impact / verification:** import and regression suite. Scanned PDF/VLM remains deferred.

## Change 7: Identity-aware cache key
- **Iteration / Fix ID / File:** 12a / C / `code/agent/evidence/cache.py:8-36`, `code/agent/evidence/registry.py:10-22`, `code/orchestrator/pipeline.py:46-48`
- **Grounded in:** `phase11_changes.md` case 08 and `dataset_grounding_report.md` 94-file shared manifest.
- **Problem / change:** File-byte-only keys could return another user's filtered records. Key now hashes file bytes, normalized bundle, and audit time; existing `load/save` API still works. Per-case cache clearing removed.
- **Before:** `load(root,file_hash(data))`; clear cache every case.
- **After:** `load(root,cache_key(data,identity,audit_at))`; no per-case clear.
- **Tests / impact / verification:** six `test_cache_key_fix.py` tests; second identical extraction has equal `extracted_at`; distinct bundles isolate records. Identity-agnostic extraction is a future simplification.

## Change 8: Gold validation harness
- **Iteration / Fix ID / File:** 12a / D / `code/orchestrator/gold_validation.py:1-70`
- **Grounded in:** `mismatch_triage_report.md` and `phase11_changes.md` score regression.
- **Problem / change:** No automated gold rerun with crash isolation. Harness runs 32 cases, compares status/exact steps, writes divergences and regression list.
- **Before:** manual `sample_compare.py` had aggregate metrics only.
- **After:** `validate_against_gold()` returns report and writes `gold_validation_report.md`.
- **Tests / impact / verification:** three `test_gold_validation.py` tests; generated report. Intermediate Phase 1–4 accuracy is explicitly unmeasurable from supplied gold.

## Change 9: Serialized SQL payload matching
- **Iteration / Fix ID / File:** 12c / targeted-case_16 / `code/agent/evidence/handlers/sql_handler.py:13-38`
- **Grounded in:** `dataset/evidence/databases/customer_data_read_replica_20260921.sql:37,52,75` (identity values inside JSON strings).
- **Problem / change:** Scalar-column matching missed exact IDs/emails in serialized payloads. Recursively inspect parsed JSON fields for exact identity values, preserving the row's full resource ID and system ID.
- **Before:** `if not candidates: continue` excluded payload-only tables.
- **After:** `scan(json.loads(value),col)` for JSON payload cells; no numeric-suffix match.
- **Tests / impact / verification:** full sample rerun raised 23/32 to 25/32; 181 tests pass.

## Deferred B.5: Image VLM
`image_handler.py` was not modified because the live VLM is absent and the user forbade invoking an LLM. Image-only cases remain a known extraction limitation.
