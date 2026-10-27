# Dataset CSV schema audit

Read-only checks of all nine supplied CSV files: exact column order, row shape, unique primary keys where applicable, ISO timestamps, and manifest paths. This report records no request or answer values.

| CSV | rows | columns | malformed rows | duplicate keys | invalid times | result |
|---|---:|---|---:|---:|---:|---|
| `deletion_requests.csv` | 518 | case_id, email, requested_at, reported_status, reported_at, audit_at, request_text | 0 | 0 | 0 | PASS |
| `sample_deletion_requests.csv` | 32 | case_id, email, requested_at, reported_status, reported_at, audit_at, request_text | 0 | 0 | 0 | PASS |
| `sample_output.csv` | 32 | case_id, deletion_status, steps_json | 0 | 0 | 0 | PASS |
| `output.csv` | 0 | case_id, deletion_status, steps_json | 0 | 0 | 0 | PASS |
| `user_identities.csv` | 850 | user_id, name, email, phone, email_hash, updated_at | 0 | 0 | 0 | PASS |
| `user_audit_log.csv` | 306 | audit_id, user_id, event_time, field_name, old_value, new_value | 0 | 0 | 0 | PASS |
| `system_activity.csv` | 4011 | activity_id, event_time, event_type, source_system, target_system, resource_id, reported_result, details | 0 | 0 | 0 | PASS |
| `deletion_rules.csv` | 15 | rule_id, data_category, condition, required_action | 0 | 0 | 0 | PASS |
| `evidence_files.csv` | 94 | file_id, file_path, origin, captured_at | 0 | 0 | 0 | PASS |

Manifest/path and schema errors: 0.

The production loader reads `deletion_requests.csv`, `user_identities.csv`, `user_audit_log.csv`, `system_activity.csv`, `deletion_rules.csv`, and `evidence_files.csv`. `sample_output.csv` and the blank `output.csv` are outside the production input set. The former is used only by evaluation commands; the latter is the submission destination/template.
