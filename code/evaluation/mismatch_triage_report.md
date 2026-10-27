# Mismatch triage report
Compared: sample_output_phase10.csv vs dataset\sample_output.csv
Status mismatches: 10 / 32
Step differences including status matches: 32
## Summary table
| case_id | yours | gold | divergence | candidate phase |
|---|---|---|---|---|
| case_02 | INCOMPLETE | COMPLETE | OVER_DELETED | state |
| case_03 | INCOMPLETE | COMPLETE | OVER_DELETED | state |
| case_04 | INCOMPLETE | COMPLETE | OVER_DELETED | state |
| case_12 | NOT_APPLICABLE | INCOMPLETE | WRONG_NA | status |
| case_21 | INCOMPLETE | COMPLETE | OVER_DELETED | state |
| case_25 | INCOMPLETE | COMPLETE | OVER_DELETED | state |
| case_26 | INCOMPLETE | COMPLETE | OVER_DELETED | state |
| case_27 | INCOMPLETE | COMPLETE | OVER_DELETED | state |
| case_28 | INCOMPLETE | COMPLETE | OVER_DELETED | state |
| case_31 | INCOMPLETE | COMPLETE | OVER_DELETED | state |
## Per-case details
### case_02
- Your status: INCOMPLETE; gold: COMPLETE; divergence: OVER_DELETED
- Candidate phase: state
- Decision: extra step REPORT_REMAINING_RECORD for account_3002; fact={'evidence_id': 'activity_638', 'notes': ['timeline-only: no matching evidence record'], 'resource_id': 'account_3002', 'state': 'PRESENT', 'system_id': 'account_replication_cluster'}
- Grounded in: dataset/system_activity.csv:L639 (activity_id=activity_638)
- Audit: HALLUCINATION_SUSPECTED: source row exists but user affiliation is inferred
- Proposed fix: Review the extra resource's activity/evidence join and policy category; compare cited source ID to gold steps.
### case_03
- Your status: INCOMPLETE; gold: COMPLETE; divergence: OVER_DELETED
- Candidate phase: state
- Decision: extra step REPORT_REMAINING_RECORD for account_6043; fact={'evidence_id': 'activity_457', 'notes': ['timeline-only: no matching evidence record'], 'resource_id': 'account_6043', 'state': 'PRESENT', 'system_id': 'account_service'}
- Grounded in: dataset/system_activity.csv:L458 (activity_id=activity_457)
- Audit: HALLUCINATION_SUSPECTED: source row exists but user affiliation is inferred
- Proposed fix: Review the extra resource's activity/evidence join and policy category; compare cited source ID to gold steps.
### case_04
- Your status: INCOMPLETE; gold: COMPLETE; divergence: OVER_DELETED
- Candidate phase: state
- Decision: extra step REPORT_REMAINING_RECORD for account_1004; fact={'evidence_id': 'activity_821', 'notes': ['timeline-only: no matching evidence record'], 'resource_id': 'account_1004', 'state': 'PRESENT', 'system_id': 'account_service'}
- Grounded in: dataset/system_activity.csv:L822 (activity_id=activity_821)
- Audit: HALLUCINATION_SUSPECTED: source row exists but user affiliation is inferred
- Proposed fix: Review the extra resource's activity/evidence join and policy category; compare cited source ID to gold steps.
### case_12
- Your status: NOT_APPLICABLE; gold: INCOMPLETE; divergence: WRONG_NA
- Candidate phase: status
- Decision: NOT_APPLICABLE; request_text=I changed the email on this account before deleting it. Please check that nothing tied to the old address was left behind, even in systems that do not display the email.
- Grounded in: dataset/sample_deletion_requests.csv:L13
- Audit: GROUNDED_CITATION_PRESENT
- Proposed fix: Check request intent and identity history against cited case/identity rows.
### case_21
- Your status: INCOMPLETE; gold: COMPLETE; divergence: OVER_DELETED
- Candidate phase: state
- Decision: extra step REPORT_REMAINING_RECORD for account_7021; fact={'evidence_id': 'activity_253', 'notes': ['timeline-only: no matching evidence record'], 'resource_id': 'account_7021', 'state': 'PRESENT', 'system_id': 'account_service'}
- Grounded in: dataset/system_activity.csv:L254 (activity_id=activity_253)
- Audit: HALLUCINATION_SUSPECTED: source row exists but user affiliation is inferred
- Proposed fix: Review the extra resource's activity/evidence join and policy category; compare cited source ID to gold steps.
### case_25
- Your status: INCOMPLETE; gold: COMPLETE; divergence: OVER_DELETED
- Candidate phase: state
- Decision: extra step REPORT_REMAINING_RECORD for audit_record_2025; fact={'evidence_id': 'activity_124', 'notes': ['timeline-only: no matching evidence record'], 'resource_id': 'audit_record_2025', 'state': 'PRESENT', 'system_id': 'archive_service'}
- Grounded in: dataset/system_activity.csv:L125 (activity_id=activity_124)
- Audit: HALLUCINATION_SUSPECTED: source row exists but user affiliation is inferred
- Proposed fix: Review the extra resource's activity/evidence join and policy category; compare cited source ID to gold steps.
### case_26
- Your status: INCOMPLETE; gold: COMPLETE; divergence: OVER_DELETED
- Candidate phase: state
- Decision: extra step REPORT_REMAINING_RECORD for account_5684; fact={'evidence_id': 'evidence_02', 'notes': [], 'resource_id': 'account_5684', 'state': 'PRESENT', 'system_id': 'json'}
- Grounded in: dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:L11 (manifest evidence_files.csv:L3)
- Audit: HALLUCINATION_SUSPECTED: source row exists but audit-time timestamp and system are lost
- Proposed fix: Review the extra resource's activity/evidence join and policy category; compare cited source ID to gold steps.
### case_27
- Your status: INCOMPLETE; gold: COMPLETE; divergence: OVER_DELETED
- Candidate phase: state
- Decision: extra step REPORT_REMAINING_RECORD for account_3866; fact={'evidence_id': 'evidence_02', 'notes': [], 'resource_id': 'account_3866', 'state': 'PRESENT', 'system_id': 'json'}
- Grounded in: dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:L524 (manifest evidence_files.csv:L3)
- Audit: HALLUCINATION_SUSPECTED: source row exists but audit-time timestamp and system are lost
- Proposed fix: Review the extra resource's activity/evidence join and policy category; compare cited source ID to gold steps.
### case_28
- Your status: INCOMPLETE; gold: COMPLETE; divergence: OVER_DELETED
- Candidate phase: state
- Decision: extra step REPORT_REMAINING_RECORD for account_1028; fact={'evidence_id': 'activity_2556', 'notes': ['timeline-only: no matching evidence record'], 'resource_id': 'account_1028', 'state': 'PRESENT', 'system_id': 'account_service'}
- Grounded in: dataset/system_activity.csv:L2557 (activity_id=activity_2556)
- Audit: HALLUCINATION_SUSPECTED: source row exists but user affiliation is inferred
- Proposed fix: Review the extra resource's activity/evidence join and policy category; compare cited source ID to gold steps.
### case_31
- Your status: INCOMPLETE; gold: COMPLETE; divergence: OVER_DELETED
- Candidate phase: state
- Decision: extra step REPORT_REMAINING_RECORD for account_541; fact={'evidence_id': 'activity_303', 'notes': ['timeline-only: no matching evidence record'], 'resource_id': 'account_541', 'state': 'PRESENT', 'system_id': 'account_service'}
- Grounded in: dataset/system_activity.csv:L304 (activity_id=activity_303)
- Audit: HALLUCINATION_SUSPECTED: source row exists but user affiliation is inferred
- Proposed fix: Review the extra resource's activity/evidence join and policy category; compare cited source ID to gold steps.
## Aggregate
- By divergence: {'OVER_DELETED': 9, 'WRONG_NA': 1}
- By candidate phase: {'state': 9, 'status': 1}
## Phase 11 decision
These phase labels are candidates from the trace, not proof of root cause. Inspect source rows behind each extra or missing resource before changing frozen modules.

## Grounded root-cause review

| Case | Source and observed value | Cause candidate | Phase 11 scope |
|---|---|---|---|
| case_02 | `system_activity.csv:L639`, `account_3002` | Resource suffix `002` was treated as `user_02` despite no user key; a replication checkpoint became a user fact. | Replace suffix affiliation with an evidence-backed join. |
| case_03 | `system_activity.csv:L458`, `account_6043` | Suffix `043` was treated as `user_43`; this profile update does not prove ownership. | Same join fix. |
| case_04 | `system_activity.csv:L822`, `account_1004` | Suffix `004` was treated as `user_04`; unrelated profile update became PRESENT. | Same join fix. |
| case_12 | `sample_deletion_requests.csv:L13`, “before deleting it” | The classifier checks `delete` but misses inflections such as `deleting`; `changed` triggers the non-deletion path. | Extend deletion intent morphology in `request_classifier.py`. |
| case_21 | `system_activity.csv:L254`, `account_7021` | Suffix `021` was treated as `user_21`; update has no explicit ownership key. | Evidence-backed join. |
| case_25 | `system_activity.csv:L125`, `audit_record_2025` | Numeric suffix `025` was treated as `user_25`, including an unrelated retained security record. | Restrict resource ownership inference. |
| case_26 | `customer_data_snapshot_bundle_20260917.json:L6-L19`, captured September 9 | The older PRESENT snapshot is emitted with `system_id=json` and no timestamp, so it is not reconciled with later account state. | Parse snapshot `data_store` and `captured_at`, then apply audit-time precedence. |
| case_27 | `customer_data_snapshot_bundle_20260917.json:L519-L532`, captured September 17 | A post-audit PRESENT snapshot was accepted for the September 15 audit because its record timestamp is `None`. | Exclude post-audit snapshots after timestamp parsing. |
| case_28 | `system_activity.csv:L2557`, `account_1028` | Suffix `028` was treated as `user_28`; the request explicitly warns about a similar person. | Evidence-backed ownership join. |
| case_31 | `system_activity.csv:L304`, `account_541` | Suffix `541` was treated as `user_541`; profile update does not establish audit-time PII state. | Evidence-backed join. |

The cited source rows are real; the **user affiliation or audit-time interpretation** is the ungrounded step in nine state cases. This is why the report marks them `HALLUCINATION_SUSPECTED` despite a nonempty `grounded_in` path. The case_12 status error is grounded in real request text but misclassified by a narrow keyword check.
