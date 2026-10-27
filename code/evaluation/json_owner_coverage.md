# JSON subject-to-resource coverage

Independent read of manifest-listed JSON source objects with a literal `resource_id` or `id` and an exact current/historical owner or readback-subject field. A `subject_reference` in a readback links the result to the queried person; it is not counted as PII retained in a NOT_FOUND or REDACTED resource. `query`, `lookup_value`, `subject_selector`, and `uploaded_by` are excluded because they can name a requester or actor without establishing record ownership. Source pairs are compared to the production JSON extractor without an audit cutoff. Nested inherited IDs are additional handler behavior outside this direct-row check.

Files: 28; direct owner/resource pairs: 544; parser records: 648; missing direct pairs: 0; conflicting direct owners: 0.

| File ID | Source file | Direct pairs | Extracted records | Missing direct pairs |
|---|---|---:|---:|---:|
| `evidence_02` | `customer_data_snapshot_bundle_20260917.json` | 25 | 30 | 0 |
| `evidence_07` | `customer_data_snapshot_bundle_20260913.json` | 20 | 21 | 0 |
| `evidence_12` | `customer_data_snapshot_bundle_20260819.json` | 20 | 25 | 0 |
| `evidence_13` | `connector_configurations_20260812.json` | 39 | 39 | 0 |
| `evidence_17` | `customer_data_snapshot_bundle_20260725.json` | 21 | 29 | 0 |
| `evidence_22` | `customer_data_snapshot_bundle_20260630.json` | 16 | 21 | 0 |
| `evidence_26` | `customer_data_snapshot_bundle_20260605.json` | 20 | 25 | 0 |
| `evidence_31` | `customer_data_snapshot_bundle_20260511.json` | 21 | 26 | 0 |
| `evidence_35` | `customer_data_snapshot_bundle_20260416.json` | 18 | 22 | 0 |
| `evidence_36` | `customer_export_manifest_20260409.json` | 42 | 42 | 0 |
| `evidence_40` | `customer_data_snapshot_bundle_20260322.json` | 18 | 24 | 0 |
| `evidence_45` | `customer_data_snapshot_bundle_20260223.json` | 18 | 25 | 0 |
| `evidence_49` | `customer_data_snapshot_bundle_20260131.json` | 22 | 28 | 0 |
| `evidence_50` | `security_audit_ledger_20261001.json` | 20 | 20 | 0 |
| `evidence_51` | `customer_data_snapshot_bundle_20260915.json` | 4 | 4 | 0 |
| `evidence_56` | `customer_analytics_report_20260907.json` | 1 | 1 | 0 |
| `evidence_59` | `customer_export_jobs_20260914.json` | 2 | 2 | 0 |
| `evidence_62` | `service_resource_export_20260129_114459.json` | 22 | 27 | 0 |
| `evidence_65` | `service_resource_export_20260228_103637.json` | 19 | 24 | 0 |
| `evidence_68` | `service_resource_export_20260320_072349.json` | 17 | 22 | 0 |
| `evidence_71` | `service_resource_export_20260429_083222.json` | 20 | 24 | 0 |
| `evidence_74` | `service_resource_export_20260514_114454.json` | 17 | 21 | 0 |
| `evidence_77` | `service_resource_export_20260603_083457.json` | 20 | 24 | 0 |
| `evidence_80` | `service_resource_export_20260628_062556.json` | 17 | 21 | 0 |
| `evidence_83` | `service_resource_export_20260718_104335.json` | 22 | 27 | 0 |
| `evidence_86` | `service_resource_export_20260807_074104.json` | 18 | 21 | 0 |
| `evidence_89` | `service_resource_export_20260901_053316.json` | 20 | 22 | 0 |
| `evidence_92` | `service_resource_export_20260915_114455.json` | 25 | 31 | 0 |

## Exceptions

No direct pair omissions.
