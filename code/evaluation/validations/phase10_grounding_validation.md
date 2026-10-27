# Phase 10 grounding validation

## 1. Dataset grounding summary

The [dataset grounding report](dataset_grounding_report.md) inventories all CSVs and each of the 94 manifest evidence files. Observed CSV structure:

| File | Columns | Rows |
|---|---|---:|
| deletion_requests.csv | case_id, email, requested_at, reported_status, reported_at, audit_at, request_text | 518 |
| sample_deletion_requests.csv | same request columns | 32 |
| sample_output.csv | case_id, deletion_status, steps_json | 32 |
| user_identities.csv | user_id, name, email, phone, email_hash, updated_at | 850 |
| user_audit_log.csv | audit_id, user_id, event_time, field_name, old_value, new_value | 306 |
| system_activity.csv | activity_id, event_time, event_type, source_system, target_system, resource_id, reported_result, details | 4011 |
| deletion_rules.csv | rule_id, data_category, condition, required_action | 15 |
| evidence_files.csv | file_id, file_path, origin, captured_at | 94 |
| output.csv | case_id, deletion_status, steps_json | 0 (blank template) |

Measured joins from [Cross-file join analysis](dataset_grounding_report.md#cross-file-join-analysis): activity resource IDs vs JSON resource IDs have **551 shared values** (Jaccard 0.132707); activity source/target systems vs JSON `system_id`/`data_store` have **10 shared values** (Jaccard 0.37037). The activity CSV has **no `target_user_id` column**, so both joins based on that supposed field have zero left-side values. JSON-only extraction is the stated scope of these join figures; other evidence types are inventoried separately.

## 2. Hallucination audit

The broad-matching diagnosis was partially grounded: older reports show extra facts, and the exact-value tests constrain one source, but it did not explain all cases. The missing explicit user join is grounded by the actual [activity columns](dataset_grounding_report.md#system_activitycsv). The Phase 9 **“no overlap” diagnosis was false**: 551 resource IDs overlap. Phase 9 produced no derivations because [json_handler.py](../agent/evidence/handlers/json_handler.py) sets every JSON record's `evidence_timestamp=None`, while [activity_expander.py](../orchestrator/activity_expander.py) falls back to current extraction time and rejects it when later than `audit_at`. This is a code-path conclusion supported by the measured joins and the zero-derived diagnostic logs.

In the ten mismatch traces, seven activity-suffix affiliations and two untimestamped JSON interpretations are `HALLUCINATION_SUSPECTED`: the source records exist, but they do not support the inferred user or audit-time state. Case_12 is a grounded text classification error. See the [per-case review](mismatch_triage_report.md#grounded-root-cause-review).

## 3. LLM usage audit

The [usage audit](llm_usage_audit.md) found one optional injected VLM callback in `image_handler.py` and test-only pattern hits. The production path passes no callback; the 550 case logs (32 sample + 518 full) recorded **0 VLM calls**. Production code reads only `ORCHESTRATOR_SKIP_EVIDENCE`, not an API key variable. **No LLM/VLM API calls and no API keys are required** for output generation.

## 4. Mismatch triage summary

Sample status accuracy remains **22/32 (68.75%)**. Nine mismatches are `OVER_DELETED` (extra findings); one is `WRONG_NA` (case_12). Candidate phases: state 9, status 1. Seven state errors trace to resource suffix affiliation; two trace to JSON snapshot timestamp/system loss. Phase 11 can address these with a proven join, timestamp propagation, and request-intent morphology. The current evidence schema lacks an explicit activity user key, so ownership of activity-only resources needs a documented join rule.

## 5. Repackage status

`repackage.py` produced `code.zip` at the repository root: **100 files, 139,490 bytes** on the first packaging pass. The archive excludes `.venv`, `.cache`, `__pycache__`, `.env`, `.git`, compiled Python, and test caches; archive inspection found no excluded paths. No tar fallback was needed. The report is repackaged once more after this final documentation edit.

## 6. Token usage

Phase 10 performed no LLM/VLM calls: **0 input tokens and 0 output tokens**.

Two full 518-case runs produced the same `output.csv` SHA-256 (`FA1DD5525E5451A6953DA8168272E7388916818C55AFF62C2DB9E319E29D9B64`). Case_33's JSONL decision trace also matched byte-for-byte after removing only `timestamp` and `elapsed_ms` (`4ea5cdc310f70e5b66327ad0c5b1633a4d2d46d95b2379c32ec596a20164f7d4`). All **145 tests passed**. The validator reports zero errors, though its `0/0 checks` counter is itself not useful; independent CSV inspection confirmed 518 data rows plus header.

## 7. Open questions for Phase 11

- Which evidence field establishes the owner of an activity resource without relying on matching numeric suffixes?
- Should JSON snapshot `captured_at` or manifest `captured_at` be authoritative for each record?
- How should later ABSENT evidence supersede an older PRESENT snapshot when the same resource appears in different files?
- The ±24-hour proximity window should be reconsidered only after timestamps are propagated; tuning it now cannot fix the zero-derivation path.
