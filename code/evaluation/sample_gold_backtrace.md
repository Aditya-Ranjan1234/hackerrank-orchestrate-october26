# Sample gold backtrace

Evaluation only: the production agent never imports this module or reads sample answers. A cited source can provide wider context; the counts below test full resource IDs and exact user IDs, current/historical emails or email hashes within the same JSON record, SQL row, PDF table row or log line.

## Summary

Status: 32/32; exact parsed step arrays: 12/32; missing semantic steps: 26; extra semantic steps: 0; shared-step citation differences: 0.

## All cases

| Case | Gold status | Agent status | Gold steps | Agent steps | Missing | Extra | Citation differences |
|---|---|---|---:|---:|---:|---:|---:|
| case_01 | COMPLETE | COMPLETE | 1 | 0 | 1 | 0 | 0 |
| case_02 | COMPLETE | COMPLETE | 1 | 0 | 1 | 0 | 0 |
| case_03 | COMPLETE | COMPLETE | 3 | 2 | 1 | 0 | 0 |
| case_04 | COMPLETE | COMPLETE | 2 | 0 | 2 | 0 | 0 |
| case_05 | INCOMPLETE | INCOMPLETE | 3 | 3 | 0 | 0 | 0 |
| case_06 | INCOMPLETE | INCOMPLETE | 4 | 4 | 0 | 0 | 0 |
| case_07 | INCOMPLETE | INCOMPLETE | 4 | 3 | 1 | 0 | 0 |
| case_08 | INCOMPLETE | INCOMPLETE | 4 | 3 | 1 | 0 | 0 |
| case_09 | INCOMPLETE | INCOMPLETE | 5 | 5 | 0 | 0 | 0 |
| case_10 | INCOMPLETE | INCOMPLETE | 4 | 3 | 1 | 0 | 0 |
| case_11 | INCOMPLETE | INCOMPLETE | 14 | 14 | 0 | 0 | 0 |
| case_12 | INCOMPLETE | INCOMPLETE | 5 | 5 | 0 | 0 | 0 |
| case_13 | INCOMPLETE | INCOMPLETE | 8 | 8 | 0 | 0 | 0 |
| case_14 | INCOMPLETE | INCOMPLETE | 5 | 5 | 0 | 0 | 0 |
| case_15 | INCOMPLETE | INCOMPLETE | 5 | 5 | 0 | 0 | 0 |
| case_16 | INCOMPLETE | INCOMPLETE | 7 | 7 | 0 | 0 | 0 |
| case_17 | INCOMPLETE | INCOMPLETE | 5 | 5 | 0 | 0 | 0 |
| case_18 | INCOMPLETE | INCOMPLETE | 14 | 12 | 2 | 0 | 0 |
| case_19 | INCOMPLETE | INCOMPLETE | 8 | 8 | 0 | 0 | 0 |
| case_20 | INCOMPLETE | INCOMPLETE | 8 | 6 | 2 | 0 | 0 |
| case_21 | COMPLETE | COMPLETE | 3 | 1 | 2 | 0 | 0 |
| case_22 | INCOMPLETE | INCOMPLETE | 8 | 7 | 1 | 0 | 0 |
| case_23 | INCOMPLETE | INCOMPLETE | 8 | 7 | 1 | 0 | 0 |
| case_24 | INCOMPLETE | INCOMPLETE | 7 | 7 | 0 | 0 | 0 |
| case_25 | COMPLETE | COMPLETE | 3 | 1 | 2 | 0 | 0 |
| case_26 | COMPLETE | COMPLETE | 6 | 5 | 1 | 0 | 0 |
| case_27 | COMPLETE | COMPLETE | 6 | 5 | 1 | 0 | 0 |
| case_28 | COMPLETE | COMPLETE | 6 | 4 | 2 | 0 | 0 |
| case_29 | INCOMPLETE | INCOMPLETE | 14 | 13 | 1 | 0 | 0 |
| case_30 | INCOMPLETE | INCOMPLETE | 14 | 13 | 1 | 0 | 0 |
| case_31 | COMPLETE | COMPLETE | 3 | 2 | 1 | 0 | 0 |
| case_32 | INCOMPLETE | INCOMPLETE | 5 | 4 | 1 | 0 | 0 |

## Missing semantic steps and their source links

| Case | Resource / operation | Gold citation | ID in cited source | Owner in cited record | ID elsewhere | Pre-audit activity | Activity direct owner | Nearest activity to reported time |
|---|---|---|---:|---:|---:|---:|---:|---:|
| case_01 | account_service/account_001 VERIFY_RECORD_ABSENT | evidence_54 | 0 | 0 | 0 | 1 | 0 | 17s |
| case_02 | account_service/account_002 VERIFY_RECORD_ABSENT | evidence_54 | 0 | 0 | 0 | 1 | 0 | 303s |
| case_03 | analytics_platform/analytics_9406 VERIFY_RECORD_ANONYMIZED | evidence_94 | 2 | 0 | 2 | 1 | 0 | 1724s |
| case_04 | account_service/account_004 VERIFY_RECORD_ABSENT | evidence_54 | 0 | 0 | 0 | 0 | 0 | n/a |
| case_04 | analytics_platform/analytics_901 VERIFY_RECORD_ANONYMIZED | evidence_56 | 1 | 0 | 1 | 1 | 0 | 379s |
| case_07 | account_service/account_007 VERIFY_RECORD_ABSENT | empty | 0 | 0 | 0 | 1 | 0 | 81s |
| case_08 | account_service/account_008 VERIFY_RECORD_ABSENT | empty | 0 | 0 | 0 | 1 | 0 | 298s |
| case_10 | account_service/account_010 VERIFY_RECORD_ABSENT | empty | 0 | 0 | 0 | 1 | 0 | 37s |
| case_18 | account_service/account_5521 VERIFY_RECORD_ABSENT | empty | 0 | 0 | 0 | 1 | 0 | 4054s |
| case_18 | security_service/audit_record_6645 VERIFY_RECORD_PRESENT | empty | 0 | 0 | 0 | 0 | 0 | n/a |
| case_20 | account_service/account_5037 VERIFY_RECORD_ABSENT | empty | 0 | 0 | 0 | 1 | 0 | 2705s |
| case_20 | security_service/audit_record_5569 VERIFY_RECORD_PRESENT | empty | 0 | 0 | 0 | 0 | 0 | n/a |
| case_21 | account_service/account_6440 VERIFY_RECORD_ABSENT | evidence_92 | 1 | 0 | 1 | 1 | 0 | 3487s |
| case_21 | analytics_platform/analytics_5335 VERIFY_RECORD_ANONYMIZED | evidence_92 | 1 | 0 | 2 | 1 | 0 | 1706s |
| case_22 | account_service/account_4990 VERIFY_RECORD_ABSENT | empty | 0 | 0 | 0 | 1 | 0 | 2869s |
| case_23 | account_service/account_410 VERIFY_RECORD_ABSENT | empty | 0 | 0 | 0 | 1 | 0 | 2945s |
| case_25 | account_service/account_3136 VERIFY_RECORD_ABSENT | evidence_92 | 1 | 0 | 1 | 1 | 0 | 4293s |
| case_25 | analytics_platform/analytics_1895 VERIFY_RECORD_ANONYMIZED | evidence_92 | 1 | 0 | 2 | 1 | 0 | 1732s |
| case_26 | analytics_platform/analytics_4566 VERIFY_RECORD_ANONYMIZED | evidence_92 | 1 | 0 | 2 | 1 | 0 | 1716s |
| case_27 | analytics_platform/analytics_4574 VERIFY_RECORD_ANONYMIZED | evidence_92 | 1 | 0 | 2 | 1 | 0 | 1731s |
| case_28 | account_service/account_5482 VERIFY_RECORD_ABSENT | evidence_92 | 1 | 0 | 1 | 1 | 0 | 4427s |
| case_28 | analytics_platform/analytics_6077 VERIFY_RECORD_ANONYMIZED | evidence_92 | 1 | 0 | 2 | 1 | 0 | 1687s |
| case_29 | account_service/account_7012 VERIFY_RECORD_ABSENT | empty | 0 | 0 | 0 | 1 | 0 | 3183s |
| case_30 | account_service/account_4163 VERIFY_RECORD_ABSENT | empty | 0 | 0 | 0 | 1 | 0 | 3858s |
| case_31 | account_service/account_4857 VERIFY_RECORD_ABSENT | evidence_51 | 0 | 0 | 0 | 1 | 0 | 4442s |
| case_32 | account_service/account_8858 VERIFY_RECORD_ABSENT | empty | 0 | 0 | 0 | 1 | 0 | 3285s |

### Full ID occurrences for missing steps

- case_01 account_001; cited evidence/databases/customer_accounts_failover_replica_20260902.sql; no literal occurrence in 94 evidence files
- case_02 account_002; cited evidence/databases/customer_accounts_failover_replica_20260902.sql; no literal occurrence in 94 evidence files
- case_03 analytics_9406; cited evidence/logs/resource_lookup_trace_20260926_103856.log; dataset/evidence/logs/resource_lookup_trace_20260926_103856.log:42, dataset/evidence/logs/resource_lookup_trace_20260926_103856.log:43
- case_04 account_004; cited evidence/databases/customer_accounts_failover_replica_20260902.sql; no literal occurrence in 94 evidence files
- case_04 analytics_901; cited evidence/records/customer_analytics_report_20260907.json; dataset/evidence/records/customer_analytics_report_20260907.json:7
- case_07 account_007; cited empty; no literal occurrence in 94 evidence files
- case_08 account_008; cited empty; no literal occurrence in 94 evidence files
- case_10 account_010; cited empty; no literal occurrence in 94 evidence files
- case_18 account_5521; cited empty; no literal occurrence in 94 evidence files
- case_18 audit_record_6645; cited empty; no literal occurrence in 94 evidence files
- case_20 account_5037; cited empty; no literal occurrence in 94 evidence files
- case_20 audit_record_5569; cited empty; no literal occurrence in 94 evidence files
- case_21 account_6440; cited evidence/records/service_resource_export_20260915_114455.json; dataset/evidence/records/service_resource_export_20260915_114455.json:46
- case_21 analytics_5335; cited evidence/records/service_resource_export_20260915_114455.json; dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:59, dataset/evidence/records/service_resource_export_20260915_114455.json:105
- case_22 account_4990; cited empty; no literal occurrence in 94 evidence files
- case_23 account_410; cited empty; no literal occurrence in 94 evidence files
- case_25 account_3136; cited evidence/records/service_resource_export_20260915_114455.json; dataset/evidence/records/service_resource_export_20260915_114455.json:10
- case_25 analytics_1895; cited evidence/records/service_resource_export_20260915_114455.json; dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:83, dataset/evidence/records/service_resource_export_20260915_114455.json:60
- case_26 analytics_4566; cited evidence/records/service_resource_export_20260915_114455.json; dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:107, dataset/evidence/records/service_resource_export_20260915_114455.json:78
- case_27 analytics_4574; cited evidence/records/service_resource_export_20260915_114455.json; dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:132, dataset/evidence/records/service_resource_export_20260915_114455.json:87
- case_28 account_5482; cited evidence/records/service_resource_export_20260915_114455.json; dataset/evidence/records/service_resource_export_20260915_114455.json:34
- case_28 analytics_6077; cited evidence/records/service_resource_export_20260915_114455.json; dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:161, dataset/evidence/records/service_resource_export_20260915_114455.json:114
- case_29 account_7012; cited empty; no literal occurrence in 94 evidence files
- case_30 account_4163; cited empty; no literal occurrence in 94 evidence files
- case_31 account_4857; cited evidence/records/customer_data_snapshot_bundle_20260915.json; no literal occurrence in 94 evidence files
- case_32 account_8858; cited empty; no literal occurrence in 94 evidence files

## Shared steps with different citations

| Case | Resource / operation | Gold citation | Gold ID/owner hits | Agent citation | Agent ID/owner hits |
|---|---|---|---:|---|---:|

## Citation interpretation

- Gold file citations lacking the literal resource ID: 4.
- Gold file citations naming the ID without an owner in the same structured record: 16.
- Empty citation on an INCOMPLETE follow-up step is expected output syntax.
- Reported time and nearby ownerless activity are contextual only; the production agent excludes reported time and reported status.
- This report does not reveal the gold generator's internal reasoning. It records visible support and gaps.


### Gold file citations without a literal target in that file

| Case | Resource ID | Cited file ID | Source |
|---|---|---|---|
| case_01 | account_001 | evidence_54 | evidence/databases/customer_accounts_failover_replica_20260902.sql |
| case_02 | account_002 | evidence_54 | evidence/databases/customer_accounts_failover_replica_20260902.sql |
| case_04 | account_004 | evidence_54 | evidence/databases/customer_accounts_failover_replica_20260902.sql |
| case_31 | account_4857 | evidence_51 | evidence/records/customer_data_snapshot_bundle_20260915.json |

### Gold file citations with a target but no owner on its literal line/row

For PDFs this scan does not resolve a multi-line page layout; the original page and surrounding table must be reviewed before declaring an ownership gap.

| Case | Resource ID | Cited file ID | Source |
|---|---|---|---|
| case_03 | analytics_9406 | evidence_94 | evidence/logs/resource_lookup_trace_20260926_103856.log |
| case_04 | analytics_901 | evidence_56 | evidence/records/customer_analytics_report_20260907.json |
| case_07 | support_001 | evidence_58 | evidence/documents/delivery_correction_attachment.pdf |
| case_10 | support_002 | evidence_61 | evidence/logs/support_replica.log |
| case_15 | data_flow_9846 | evidence_01 | evidence/logs/service_events_ap_south_20260915.log |
| case_17 | backup_3245 | evidence_01 | evidence/logs/service_events_ap_south_20260915.log |
| case_21 | account_6440 | evidence_92 | evidence/records/service_resource_export_20260915_114455.json |
| case_21 | analytics_5335 | evidence_92 | evidence/records/service_resource_export_20260915_114455.json |
| case_25 | account_3136 | evidence_92 | evidence/records/service_resource_export_20260915_114455.json |
| case_25 | analytics_1895 | evidence_92 | evidence/records/service_resource_export_20260915_114455.json |
| case_26 | account_5684 | evidence_92 | evidence/records/service_resource_export_20260915_114455.json |
| case_26 | analytics_4566 | evidence_92 | evidence/records/service_resource_export_20260915_114455.json |
| case_27 | account_3866 | evidence_92 | evidence/records/service_resource_export_20260915_114455.json |
| case_27 | analytics_4574 | evidence_92 | evidence/records/service_resource_export_20260915_114455.json |
| case_28 | account_5482 | evidence_92 | evidence/records/service_resource_export_20260915_114455.json |
| case_28 | analytics_6077 | evidence_92 | evidence/records/service_resource_export_20260915_114455.json |
## What the individual files establish

- case_01: the gold verification cites evidence_54, a failover-replica SQL file. Its four resource rows include account_005 and three unrelated accounts; account_001 does not occur. The account_001 deletion activity (activity_3342) has no subject identifier. Its time is 17 seconds before the request's reported time, which is a claim rather than an owner field.
- case_03: evidence_94 lines 42-43 and activity_3852 name analytics_9406. The lookup key, customer reference, email, phone and email hash are all null. The source establishes an anonymous profile observation, but not a link to the requester.
- case_04: evidence_56 contains analytics_901 with null user ID, email, phone and email hash. The gold account_004 ID appears neither in evidence nor in a pre-audit activity row. A direct subject-to-resource path is unavailable.
- case_21: evidence_92 includes account_6440 as a 404 readback and analytics_5335 as a profile with null identifiers. Activities name both IDs, but their details provide no user identifier. The sample assigns both to case_21; the visible sources do not identify that owner.
- case_24: evidence_92 was captured before the September 15 noon cutoff and directly names the account/search resources with the requester email. Evidence_02 repeats them in a bundle captured September 17. The agent now prefers the contemporaneous citation while retaining the later bundle's historical rows for state reconstruction.
- Across all missing steps, 16 full IDs have no occurrence in the 94 evidence files; 10 appear without a same-line/row owner. Every original PNG was also visually reviewed; none displays a missing full ID overlooked by OCR. Four PDF files were scanned through text and table extraction.
- Of the 16 IDs missing from evidence, 3 also have no full-ID occurrence in any other participant input CSV (excluding sample_output.csv and blank output.csv): case_04/account_004, case_18/audit_record_6645, case_20/audit_record_5569. The other 13 appear in system_activity.csv but have no direct user field. This is a literal-source inventory, not a claim that the gold answers are false.
- The gold-free temporal probe found that the nearest account action to reported time belonged to the direct owner in only 71 of 212 evaluable full-dataset requests. Numeric account/user suffixes agreed in only 1 of 240 directly owned account resources. The agent therefore uses neither timing nor numeric suffixes to fill these gaps.
