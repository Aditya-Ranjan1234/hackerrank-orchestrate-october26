# Residual missing-step source audit

Diagnostic only: gold is used to choose what to inspect, never by the production agent. Exact full-resource occurrences are counted in all 94 evidence files, including OCR and PDF tables. A same-line owner is a candidate join, not automatically sufficient proof; an owner elsewhere in the same file is not a join.

| Case | Missing resource / operation | Source occurrences | Same-line subject hits | Source locations |
|---|---|---:|---:|---|
| case_01 | `account_service/account_001` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_02 | `account_service/account_002` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_03 | `analytics_platform/analytics_9406` `VERIFY_RECORD_ANONYMIZED` | 2 | 0 | `dataset/evidence/logs/resource_lookup_trace_20260926_103856.log:42`, `dataset/evidence/logs/resource_lookup_trace_20260926_103856.log:43` |
| case_04 | `account_service/account_004` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_04 | `analytics_platform/analytics_901` `VERIFY_RECORD_ANONYMIZED` | 1 | 0 | `dataset/evidence/records/customer_analytics_report_20260907.json:7` |
| case_07 | `account_service/account_007` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_08 | `account_service/account_008` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_10 | `account_service/account_010` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_18 | `account_service/account_5521` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_18 | `security_service/audit_record_6645` `VERIFY_RECORD_PRESENT` | 0 | 0 | — |
| case_20 | `account_service/account_5037` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_20 | `security_service/audit_record_5569` `VERIFY_RECORD_PRESENT` | 0 | 0 | — |
| case_21 | `account_service/account_6440` `VERIFY_RECORD_ABSENT` | 1 | 0 | `dataset/evidence/records/service_resource_export_20260915_114455.json:46` |
| case_21 | `analytics_platform/analytics_5335` `VERIFY_RECORD_ANONYMIZED` | 2 | 0 | `dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:59`, `dataset/evidence/records/service_resource_export_20260915_114455.json:105` |
| case_22 | `account_service/account_4990` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_23 | `account_service/account_410` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_25 | `account_service/account_3136` `VERIFY_RECORD_ABSENT` | 1 | 0 | `dataset/evidence/records/service_resource_export_20260915_114455.json:10` |
| case_25 | `analytics_platform/analytics_1895` `VERIFY_RECORD_ANONYMIZED` | 2 | 0 | `dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:83`, `dataset/evidence/records/service_resource_export_20260915_114455.json:60` |
| case_26 | `analytics_platform/analytics_4566` `VERIFY_RECORD_ANONYMIZED` | 2 | 0 | `dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:107`, `dataset/evidence/records/service_resource_export_20260915_114455.json:78` |
| case_27 | `analytics_platform/analytics_4574` `VERIFY_RECORD_ANONYMIZED` | 2 | 0 | `dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:132`, `dataset/evidence/records/service_resource_export_20260915_114455.json:87` |
| case_28 | `account_service/account_5482` `VERIFY_RECORD_ABSENT` | 1 | 0 | `dataset/evidence/records/service_resource_export_20260915_114455.json:34` |
| case_28 | `analytics_platform/analytics_6077` `VERIFY_RECORD_ANONYMIZED` | 2 | 0 | `dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:161`, `dataset/evidence/records/service_resource_export_20260915_114455.json:114` |
| case_29 | `account_service/account_7012` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_30 | `account_service/account_4163` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_31 | `account_service/account_4857` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |
| case_32 | `account_service/account_8858` `VERIFY_RECORD_ABSENT` | 0 | 0 | — |

## Classification totals

- no_occurrence: 16
- ownerless_occurrence: 10
- Distinct cases with a gold target absent from every evidence file: 14.
- Those no-occurrence targets with a direct subject identifier in their activity details: 0.

A zero occurrence means the supplied evidence files contain no literal full resource ID. It does not prove the resource never existed. Activity logs are a separate, often ownerless source and cannot by themselves establish which requester owned a target.

Under the agent's strict evidence-to-owner rule, these 14 distinct no-occurrence cases cannot have exact gold step arrays without additional direct ownership evidence. Even if every other case matched, that rule implies a conditional ceiling of 18/32 exact arrays; this is a provenance constraint, not a proof that the gold answers are false.

## Why activity time alone cannot supply ownership

For each missing full ID, this diagnostic counts requests whose `requested_at` to `reported_at` window overlaps an activity for that ID. `reported_at` is a claim and this calculation is not used by the agent. Even one temporal candidate would not be a direct ownership field.

| Case | Resource ID | Pre-audit activity rows | Minimum overlapping requests per activity |
|---|---|---:|---:|
| case_01 | `account_001` | 1 | 8 |
| case_02 | `account_002` | 1 | 6 |
| case_04 | `account_004` | 0 | n/a |
| case_07 | `account_007` | 1 | 10 |
| case_08 | `account_008` | 1 | 12 |
| case_10 | `account_010` | 1 | 9 |
| case_18 | `account_5521` | 1 | 8 |
| case_18 | `audit_record_6645` | 0 | n/a |
| case_20 | `account_5037` | 1 | 8 |
| case_20 | `audit_record_5569` | 0 | n/a |
| case_22 | `account_4990` | 1 | 11 |
| case_23 | `account_410` | 1 | 12 |
| case_29 | `account_7012` | 1 | 11 |
| case_30 | `account_4163` | 1 | 5 |
| case_31 | `account_4857` | 1 | 8 |
| case_32 | `account_8858` | 1 | 9 |
