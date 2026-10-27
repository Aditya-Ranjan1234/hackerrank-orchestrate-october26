# Case 01 process and negative-snapshot trace

This is an evaluation-only investigation of the user's timestamp observation. The production agent does not read the public sample answer or this report.

## Exact source sequence

| Source | Time (UTC) | Observation |
|---|---|---|
| `dataset/sample_deletion_requests.csv`, `case_01` | 2026-08-20 16:42:00 | Workflow-reported time |
| `dataset/system_activity.csv`, `activity_3342` (row 3343) | 2026-08-20 16:41:43 | `DELETE_RECORD` for `account_001`; result `SUCCESS`; details say the deletion worker reported the requested operation as completed |
| `dataset/evidence_files.csv`, `evidence_54` | 2026-09-02 23:00:00 | Captured SQL account failover snapshot |
| `dataset/sample_deletion_requests.csv`, `case_01` | 2026-09-03 11:30:00 | Audit cutoff |

The operation is **17 seconds before** `reported_at`, not 19. It is in `system_activity.csv`, not inside `evidence_54`. The SQL file was captured 13 days, 6 hours, 18 minutes and 17 seconds *after* the operation and 12 hours 30 minutes before the audit cutoff. It contains four failover account rows and three primary account rows; `SELECT COUNT(*) ... WHERE resource_id='account_001'` returns **0 in both tables**. Conditional on those table captures being complete, this is a meaningful negative observation after the deletion claim.

Across both `sample_deletion_requests.csv` and `deletion_requests.csv`, the `case_01` reported time is the nearest reported time to this activity (17 seconds); the next nearest is 51,497 seconds away. This is a strong **candidate correlation** that the earlier source-only classification did not make clear. It is not an explicit subject/case key: neither `activity_3342` nor `evidence_54` names `user_01`, the case email or a request correlation ID.

## Two distinct missing pipeline capabilities

1. **Affiliation.** `pipeline.run_case` projects `reported_at` out before extraction and activity expansion. `activity_expander` requires an exact owned resource or explicit source reference, so `activity_3342` remains ownerless. Case 01 has zero derived activities and zero ResourceFacts.
2. **Negative snapshot citation.** The SQL handler emits rows that match an identity; it does not emit a fact for an *absent* target row. Extracting `evidence_54` for `user_01` returns zero records. In an offline counterfactual where `activity_3342` is explicitly given `target_user_id=user_01`, reconstruction creates `account_001/ABSENT`, policy marks it compliant and step generation emits `VERIFY_RECORD_ABSENT`—but cites **`activity_3342`**, not the gold's **`evidence_54`**. A closed-world table anti-join and source ranking would still be needed for that citation.

Thus, simply feeding the activity to Phase 3 would raise the case's step count from zero to one but would **not** make the array exact. The earlier explanation focused on affiliation and understated this separate negative-evidence gap.

## Why the timestamp cannot be promoted to a general ownership rule yet

The source-only control in `step_gap_diagnosis.py` matches a request to a *unique* account-deletion event before its reported time, then checks directly known account owners without consulting sample answers. Among the 518 full requests, a 20-second window yields 3 unique candidates, 1 independently owned and **0 correct**; a five-minute window yields 60 unique candidates, 25 independently owned and **0 correct**. The wording “reported the requested operation as completed” occurs in only eight activity rows and has no full-request reported time within ten minutes, so its precision cannot be calibrated on the full-input controls. A rule tailored to that wording would act almost exclusively on public sample cases.

Use `reported_at` and the operation wording to **retrieve and inspect** candidate activity, not as deletion proof or an automatic owner assignment. The later SQL snapshot can support absence only after the target ID is reliably linked to the requester and the snapshot's table coverage is established. A prior owner-bearing record or explicit workflow request/correlation ID would complete the link without guessing.

## Follow-up after calibrated account affiliation

The later implementation captures `reported_at` solely for a narrow workflow
affiliation rule; the older statement that the pipeline never reads it describes
the code at the time of this original trace. The rule requires one account
deletion across all reported outcomes 30–90 minutes before the report, then a
SUCCESS result and independent ownership/ambiguity guards. Source-owned
controls are 26/26 correct for the unique all-outcome band and 14/14 for a
successful winner. The 17-second `activity_3342` correlation does not satisfy
that calibrated band. The distinctive completion wording has no comparable
owned controls in the full request set; promoting it would fit public sample
cases without an independent precision estimate. `evidence_54` remains a
selective 7-row export with no declared complete account scope, so its lack of
`account_001` cannot be treated as a universal negative row.
