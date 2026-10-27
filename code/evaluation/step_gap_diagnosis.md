# Sample step gap diagnosis

**Evaluation only.** Public sample answers are read only to identify missing steps. Production imports and predictions are unchanged.

Statuses: 32/32. Exact ordered arrays: 13/32. Gold steps: 193; agent steps: 168; missing semantic steps: 25.

15 target IDs have no occurrence in the 94 evidence files, across 13 sample cases. If direct owner-bearing evidence were the only permitted affiliation path, the conditional ceiling would be 19/32 exact arrays even if every other case were repaired. The calibrated activity route is a separate indirect path and has already recovered one absent-from-evidence target; this ceiling is not a claim about every possible safe inference.

## First failed link for each missing step

| Failure class | Steps | Pipeline consequence |
|---|---:|---|
| Resource ID absent from all participant inputs | 3 | No possible source-to-case link |
| Ownerless activity only, no evidence ID | 12 | Activity expander cannot assign user |
| Raw evidence has ID but per-user extraction omits it | 7 | No owned record enters state reconstruction |
| Anonymous record extracted, not affiliated | 3 | Reconstructor drops it before verdict |
| Later pipeline failure | 0 | Inspect fact, policy or step builder |

## Per-step trace

Counts are raw evidence occurrences / other participant CSV occurrences / original activity rows / case-extracted records / derived activities / ResourceFacts / policy verdicts.

| Case | Missing resource / operation | Gold cite | Counts | First failed link |
|---|---|---|---|---|
| case_01 | `account_001` `VERIFY_RECORD_ABSENT` | `evidence_54` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |
| case_02 | `account_002` `VERIFY_RECORD_ABSENT` | `evidence_54` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |
| case_03 | `analytics_9406` `VERIFY_RECORD_ANONYMIZED` | `evidence_94` | 2 / 1 / 1 / 0 / 0 / 0 / 0 | raw_evidence_not_extracted_for_user |
| case_04 | `account_004` `VERIFY_RECORD_ABSENT` | `evidence_54` | 0 / 0 / 0 / 0 / 0 / 0 / 0 | no_participant_input_names_resource |
| case_04 | `analytics_901` `VERIFY_RECORD_ANONYMIZED` | `evidence_56` | 1 / 1 / 1 / 0 / 0 / 0 / 0 | raw_evidence_not_extracted_for_user |
| case_07 | `account_007` `VERIFY_RECORD_ABSENT` | `` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |
| case_08 | `account_008` `VERIFY_RECORD_ABSENT` | `` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |
| case_10 | `account_010` `VERIFY_RECORD_ABSENT` | `` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |
| case_18 | `account_5521` `VERIFY_RECORD_ABSENT` | `` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |
| case_18 | `audit_record_6645` `VERIFY_RECORD_PRESENT` | `` | 0 / 0 / 0 / 0 / 0 / 0 / 0 | no_participant_input_names_resource |
| case_20 | `account_5037` `VERIFY_RECORD_ABSENT` | `` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |
| case_20 | `audit_record_5569` `VERIFY_RECORD_PRESENT` | `` | 0 / 0 / 0 / 0 / 0 / 0 / 0 | no_participant_input_names_resource |
| case_21 | `account_6440` `VERIFY_RECORD_ABSENT` | `evidence_92` | 1 / 1 / 1 / 1 / 0 / 0 / 0 | anonymous_extraction_not_affiliated |
| case_21 | `analytics_5335` `VERIFY_RECORD_ANONYMIZED` | `evidence_92` | 2 / 1 / 1 / 0 / 0 / 0 / 0 | raw_evidence_not_extracted_for_user |
| case_22 | `account_4990` `VERIFY_RECORD_ABSENT` | `` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |
| case_23 | `account_410` `VERIFY_RECORD_ABSENT` | `` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |
| case_25 | `account_3136` `VERIFY_RECORD_ABSENT` | `evidence_92` | 1 / 1 / 1 / 1 / 0 / 0 / 0 | anonymous_extraction_not_affiliated |
| case_25 | `analytics_1895` `VERIFY_RECORD_ANONYMIZED` | `evidence_92` | 2 / 1 / 1 / 0 / 0 / 0 / 0 | raw_evidence_not_extracted_for_user |
| case_26 | `analytics_4566` `VERIFY_RECORD_ANONYMIZED` | `evidence_92` | 2 / 1 / 1 / 0 / 0 / 0 / 0 | raw_evidence_not_extracted_for_user |
| case_27 | `analytics_4574` `VERIFY_RECORD_ANONYMIZED` | `evidence_92` | 2 / 1 / 1 / 0 / 0 / 0 / 0 | raw_evidence_not_extracted_for_user |
| case_28 | `account_5482` `VERIFY_RECORD_ABSENT` | `evidence_92` | 1 / 1 / 1 / 1 / 0 / 0 / 0 | anonymous_extraction_not_affiliated |
| case_28 | `analytics_6077` `VERIFY_RECORD_ANONYMIZED` | `evidence_92` | 2 / 1 / 1 / 0 / 0 / 0 / 0 | raw_evidence_not_extracted_for_user |
| case_29 | `account_7012` `VERIFY_RECORD_ABSENT` | `` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |
| case_31 | `account_4857` `VERIFY_RECORD_ABSENT` | `evidence_51` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |
| case_32 | `account_8858` `VERIFY_RECORD_ABSENT` | `` | 0 / 1 / 1 / 0 / 0 / 0 / 0 | ownerless_activity_only |

## Causal trace

`pipeline.py` extracts the 94 manifest sources, expands activities, reconstructs ResourceFacts, applies policy and builds steps. `activity_expander.py` joins activities only to a record with a known owner and the same full resource ID or an explicit source reference. `reconstructor.py` discards ownerless records unless an already-owned copy of the same full resource exists. `steps/builder.py` emits a verification only for a policy verdict.

The positional `SYSTEM_ID_MISMATCH` and `RESOURCE_ID_MISMATCH` counts in `step_diff_report.md` are array-shift artifacts. The semantic comparison has no extra steps and no shared-step citation differences. The missing ResourceFacts are upstream of the step mapper and ordering code.

## Concrete examples

- `case_01/account_001`: `activity_3342` claims deletion 17 seconds before the request's reported time. This is a strong candidate correlation, but the activity has no user or case key. The later SQL snapshot `evidence_54` contains no `account_001` in either account table. The agent has no owner-affiliated fact and no closed-world negative-snapshot record, so it emits no verification. See `case01_process_trace.md` for the two separate gaps and timing controls.
- `case_03/analytics_9406`: the log's lookup key and all direct subject fields are null. A nearby `user_43` event has another trace ID. Its raw log observation does not establish ownership.
- `case_21/account_6440`: `evidence_92` has a 404 readback with `user_ref=''`. The record is extracted, then ignored because no independently owned copy of `account_6440` exists.
- `case_04/account_004`, `case_18/audit_record_6645` and `case_20/audit_record_5569` occur nowhere in participant inputs. Their exact IDs are visible only in the public sample answers.

## Status agreement does not prove resource coverage

COMPLETE with zero policy verdicts: case_01, case_02, case_04. The status gate returns COMPLETE when it sees no incomplete verdicts, so an undiscovered resource can leave the status unchanged while its required verification step is absent. This is a confidence limitation in the current three-status interface.

## Safe next action

Do not copy sample resource IDs into runtime logic or assign an anonymous row by file co-occurrence, numeric suffix or nearest time. The source-only temporal control in `temporal_owner_probe.md` found the nearest account action belonged to the requester for only 71/212 directly evaluable full requests. A stricter control using a unique account deletion in the five minutes before the reported time found 0/25 correct subjects among independently owned records (60 requests had a unique candidate; 0 owner conflicts). The production workflow affiliator now uses `reported_at` only as a bounded correlation hint when a 30–90-minute window contains one account deletion across ALL outcome classes. It checks the winner's SUCCESS claim afterward, vetoes known other owners and ambiguous requesters, and keeps the timestamp out of status determination. `workflow_affiliation_probe.md` reports the gold-free controls and the rejected SUCCESS-prefilter variant. For the remaining anonymous or absent IDs, a trustworthy subject-to-resource ledger, trace/correlation ID or prior owned snapshot would allow an exact affiliation join. Preserve the failing step gate until that link is available or the contract explicitly changes.
