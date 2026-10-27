# SQL schema and owner-mapping audit

Opened 24 SQL files, 127 table instances; extracted 716 exact-identity-linked rows. Unknown-system extracted rows: 0.

Independent exact-column cross-check: 186 direct-owner rows, 0 missing from the production extractor.

Independent nested-JSON cross-check: 530 exact-owner payload rows, 0 missing from the production extractor.

The inventory identity set includes current and historical emails and email hashes, and is used only to audit parser coverage; production filters per request and audit cutoff. Generic `customer_data_*` tables use explicit `origin_system` from the matched row and owner fields inside `record_json`. `snapshot_scope` has no direct owner; it is not a per-user resource.

| File | Table | Total rows | Owner columns | Identity-linked rows | Result systems |
|---|---|---:|---|---:|---|
| `customer_accounts_failover_replica_20260902.sql` | `customer_profiles_failover_replica` | 4 | user_id, email | 1 | account_service |
| `customer_accounts_failover_replica_20260902.sql` | `customer_profiles_primary` | 3 | user_id, email | 0 | no identity-linked row |
| `customer_data_failover_replica_20260920.sql` | `customer_data_failover_replica` | 16 | nested `record_json` / none | 16 | identity_service, security_service |
| `customer_data_failover_replica_20260920.sql` | `customer_data_primary` | 16 | nested `record_json` / none | 16 | identity_service, security_service |
| `customer_data_inventory_20260213.sql` | `backup_restore_entries` | 1 | customer_reference, customer_email | 1 | backup_service |
| `customer_data_inventory_20260213.sql` | `connector_subscriptions` | 1 | customer_reference, customer_email | 1 | integration_service |
| `customer_data_inventory_20260213.sql` | `customer_analytics_profiles` | 3 | customer_reference, email, email_hash | 0 | no identity-linked row |
| `customer_data_inventory_20260213.sql` | `customer_exports` | 0 | customer_reference, owner_email | 0 | no identity-linked row |
| `customer_data_inventory_20260213.sql` | `customer_profiles` | 2 | customer_reference, email, email_hash | 2 | account_service |
| `customer_data_inventory_20260213.sql` | `customer_search_documents` | 4 | customer_reference, email, email_hash | 4 | search_service |
| `customer_data_inventory_20260213.sql` | `security_audit_records` | 4 | subject_reference | 4 | security_service |
| `customer_data_inventory_20260213.sql` | `snapshot_scope` | 7 | nested `record_json` / none | 0 | no identity-linked row |
| `customer_data_inventory_20260213.sql` | `support_records` | 2 | customer_reference, requester_email | 2 | support_platform |
| `customer_data_inventory_20260310.sql` | `backup_restore_entries` | 1 | customer_reference, customer_email | 1 | backup_service |
| `customer_data_inventory_20260310.sql` | `connector_subscriptions` | 4 | customer_reference, customer_email | 4 | integration_service |
| `customer_data_inventory_20260310.sql` | `customer_analytics_profiles` | 5 | customer_reference, email, email_hash | 3 | analytics_platform |
| `customer_data_inventory_20260310.sql` | `customer_exports` | 1 | customer_reference, owner_email | 1 | export_service |
| `customer_data_inventory_20260310.sql` | `customer_profiles` | 0 | customer_reference, email, email_hash | 0 | no identity-linked row |
| `customer_data_inventory_20260310.sql` | `customer_search_documents` | 7 | customer_reference, email, email_hash | 7 | search_service |
| `customer_data_inventory_20260310.sql` | `security_audit_records` | 2 | subject_reference | 2 | security_service |
| `customer_data_inventory_20260310.sql` | `snapshot_scope` | 8 | nested `record_json` / none | 0 | no identity-linked row |
| `customer_data_inventory_20260310.sql` | `support_records` | 3 | customer_reference, requester_email | 3 | support_platform |
| `customer_data_inventory_20260404.sql` | `backup_restore_entries` | 1 | customer_reference, customer_email | 1 | backup_service |
| `customer_data_inventory_20260404.sql` | `connector_subscriptions` | 2 | customer_reference, customer_email | 2 | integration_service |
| `customer_data_inventory_20260404.sql` | `customer_analytics_profiles` | 4 | customer_reference, email, email_hash | 2 | analytics_platform |
| `customer_data_inventory_20260404.sql` | `customer_exports` | 1 | customer_reference, owner_email | 1 | export_service |
| `customer_data_inventory_20260404.sql` | `customer_profiles` | 0 | customer_reference, email, email_hash | 0 | no identity-linked row |
| `customer_data_inventory_20260404.sql` | `customer_search_documents` | 5 | customer_reference, email, email_hash | 5 | search_service |
| `customer_data_inventory_20260404.sql` | `security_audit_records` | 3 | subject_reference | 3 | security_service |
| `customer_data_inventory_20260404.sql` | `snapshot_scope` | 8 | nested `record_json` / none | 0 | no identity-linked row |
| `customer_data_inventory_20260404.sql` | `support_records` | 2 | customer_reference, requester_email | 2 | support_platform |
| `customer_data_inventory_20260504.sql` | `backup_restore_entries` | 1 | customer_reference, customer_email | 1 | backup_service |
| `customer_data_inventory_20260504.sql` | `connector_subscriptions` | 4 | customer_reference, customer_email | 4 | integration_service |
| `customer_data_inventory_20260504.sql` | `customer_analytics_profiles` | 3 | customer_reference, email, email_hash | 1 | analytics_platform |
| `customer_data_inventory_20260504.sql` | `customer_exports` | 0 | customer_reference, owner_email | 0 | no identity-linked row |
| `customer_data_inventory_20260504.sql` | `customer_profiles` | 1 | customer_reference, email, email_hash | 1 | account_service |
| `customer_data_inventory_20260504.sql` | `customer_search_documents` | 6 | customer_reference, email, email_hash | 6 | search_service |
| `customer_data_inventory_20260504.sql` | `security_audit_records` | 3 | subject_reference | 3 | security_service |
| `customer_data_inventory_20260504.sql` | `snapshot_scope` | 7 | nested `record_json` / none | 0 | no identity-linked row |
| `customer_data_inventory_20260504.sql` | `support_records` | 3 | customer_reference, requester_email | 3 | support_platform |
| `customer_data_inventory_20260524.sql` | `backup_restore_entries` | 1 | customer_reference, customer_email | 1 | backup_service |
| `customer_data_inventory_20260524.sql` | `connector_subscriptions` | 4 | customer_reference, customer_email | 4 | integration_service |
| `customer_data_inventory_20260524.sql` | `customer_analytics_profiles` | 6 | customer_reference, email, email_hash | 2 | analytics_platform |
| `customer_data_inventory_20260524.sql` | `customer_exports` | 1 | customer_reference, owner_email | 1 | export_service |
| `customer_data_inventory_20260524.sql` | `customer_profiles` | 0 | customer_reference, email, email_hash | 0 | no identity-linked row |
| `customer_data_inventory_20260524.sql` | `customer_search_documents` | 5 | customer_reference, email, email_hash | 5 | search_service |
| `customer_data_inventory_20260524.sql` | `security_audit_records` | 4 | subject_reference | 4 | security_service |
| `customer_data_inventory_20260524.sql` | `snapshot_scope` | 8 | nested `record_json` / none | 0 | no identity-linked row |
| `customer_data_inventory_20260524.sql` | `support_records` | 3 | customer_reference, requester_email | 3 | support_platform |
| `customer_data_inventory_20260618.sql` | `backup_restore_entries` | 0 | customer_reference, customer_email | 0 | no identity-linked row |
| `customer_data_inventory_20260618.sql` | `connector_subscriptions` | 1 | customer_reference, customer_email | 1 | integration_service |
| `customer_data_inventory_20260618.sql` | `customer_analytics_profiles` | 4 | customer_reference, email, email_hash | 2 | analytics_platform |
| `customer_data_inventory_20260618.sql` | `customer_exports` | 1 | customer_reference, owner_email | 1 | export_service |
| `customer_data_inventory_20260618.sql` | `customer_profiles` | 2 | customer_reference, email, email_hash | 2 | account_service |
| `customer_data_inventory_20260618.sql` | `customer_search_documents` | 6 | customer_reference, email, email_hash | 6 | search_service |
| `customer_data_inventory_20260618.sql` | `security_audit_records` | 2 | subject_reference | 2 | security_service |
| `customer_data_inventory_20260618.sql` | `snapshot_scope` | 7 | nested `record_json` / none | 0 | no identity-linked row |
| `customer_data_inventory_20260618.sql` | `support_records` | 3 | customer_reference, requester_email | 3 | support_platform |
| `customer_data_inventory_20260703.sql` | `backup_restore_entries` | 1 | customer_reference, customer_email | 1 | backup_service |
| `customer_data_inventory_20260703.sql` | `connector_subscriptions` | 2 | customer_reference, customer_email | 2 | integration_service |
| `customer_data_inventory_20260703.sql` | `customer_analytics_profiles` | 5 | customer_reference, email, email_hash | 1 | analytics_platform |
| `customer_data_inventory_20260703.sql` | `customer_exports` | 1 | customer_reference, owner_email | 1 | export_service |
| `customer_data_inventory_20260703.sql` | `customer_profiles` | 0 | customer_reference, email, email_hash | 0 | no identity-linked row |
| `customer_data_inventory_20260703.sql` | `customer_search_documents` | 5 | customer_reference, email, email_hash | 5 | search_service |
| `customer_data_inventory_20260703.sql` | `security_audit_records` | 5 | subject_reference | 5 | security_service |
| `customer_data_inventory_20260703.sql` | `snapshot_scope` | 8 | nested `record_json` / none | 0 | no identity-linked row |
| `customer_data_inventory_20260703.sql` | `support_records` | 5 | customer_reference, requester_email | 5 | support_platform |
| `customer_data_inventory_20260723.sql` | `backup_restore_entries` | 1 | customer_reference, customer_email | 1 | backup_service |
| `customer_data_inventory_20260723.sql` | `connector_subscriptions` | 4 | customer_reference, customer_email | 4 | integration_service |
| `customer_data_inventory_20260723.sql` | `customer_analytics_profiles` | 5 | customer_reference, email, email_hash | 3 | analytics_platform |
| `customer_data_inventory_20260723.sql` | `customer_exports` | 1 | customer_reference, owner_email | 1 | export_service |
| `customer_data_inventory_20260723.sql` | `customer_profiles` | 1 | customer_reference, email, email_hash | 1 | account_service |
| `customer_data_inventory_20260723.sql` | `customer_search_documents` | 7 | customer_reference, email, email_hash | 7 | search_service |
| `customer_data_inventory_20260723.sql` | `security_audit_records` | 2 | subject_reference | 2 | security_service |
| `customer_data_inventory_20260723.sql` | `snapshot_scope` | 8 | nested `record_json` / none | 0 | no identity-linked row |
| `customer_data_inventory_20260723.sql` | `support_records` | 5 | customer_reference, requester_email | 5 | support_platform |
| `customer_data_inventory_20260817.sql` | `backup_restore_entries` | 1 | customer_reference, customer_email | 1 | backup_service |
| `customer_data_inventory_20260817.sql` | `connector_subscriptions` | 1 | customer_reference, customer_email | 1 | integration_service |
| `customer_data_inventory_20260817.sql` | `customer_analytics_profiles` | 4 | customer_reference, email, email_hash | 2 | analytics_platform |
| `customer_data_inventory_20260817.sql` | `customer_exports` | 1 | customer_reference, owner_email | 1 | export_service |
| `customer_data_inventory_20260817.sql` | `customer_profiles` | 1 | customer_reference, email, email_hash | 1 | account_service |
| `customer_data_inventory_20260817.sql` | `customer_search_documents` | 5 | customer_reference, email, email_hash | 5 | search_service |
| `customer_data_inventory_20260817.sql` | `security_audit_records` | 2 | subject_reference | 2 | security_service |
| `customer_data_inventory_20260817.sql` | `snapshot_scope` | 8 | nested `record_json` / none | 0 | no identity-linked row |
| `customer_data_inventory_20260817.sql` | `support_records` | 4 | customer_reference, requester_email | 4 | support_platform |
| `customer_data_inventory_20260905.sql` | `backup_restore_entries` | 0 | customer_reference, customer_email | 0 | no identity-linked row |
| `customer_data_inventory_20260905.sql` | `connector_subscriptions` | 0 | customer_reference, customer_email | 0 | no identity-linked row |
| `customer_data_inventory_20260905.sql` | `customer_analytics_profiles` | 0 | customer_reference, email, email_hash | 0 | no identity-linked row |
| `customer_data_inventory_20260905.sql` | `customer_exports` | 0 | customer_reference, owner_email | 0 | no identity-linked row |
| `customer_data_inventory_20260905.sql` | `customer_profiles` | 0 | customer_reference, email, email_hash | 0 | no identity-linked row |
| `customer_data_inventory_20260905.sql` | `customer_search_documents` | 0 | customer_reference, email, email_hash | 0 | no identity-linked row |
| `customer_data_inventory_20260905.sql` | `security_audit_records` | 0 | subject_reference | 0 | no identity-linked row |
| `customer_data_inventory_20260905.sql` | `snapshot_scope` | 1 | nested `record_json` / none | 0 | no identity-linked row |
| `customer_data_inventory_20260905.sql` | `support_records` | 0 | customer_reference, requester_email | 0 | no identity-linked row |
| `customer_data_inventory_20260916.sql` | `backup_restore_entries` | 2 | customer_reference, customer_email | 2 | backup_service |
| `customer_data_inventory_20260916.sql` | `connector_subscriptions` | 2 | customer_reference, customer_email | 2 | integration_service |
| `customer_data_inventory_20260916.sql` | `customer_analytics_profiles` | 2 | customer_reference, email, email_hash | 1 | analytics_platform |
| `customer_data_inventory_20260916.sql` | `customer_exports` | 1 | customer_reference, owner_email | 1 | export_service |
| `customer_data_inventory_20260916.sql` | `customer_profiles` | 1 | customer_reference, email, email_hash | 1 | account_service |
| `customer_data_inventory_20260916.sql` | `customer_search_documents` | 3 | customer_reference, email, email_hash | 3 | search_service |
| `customer_data_inventory_20260916.sql` | `security_audit_records` | 3 | subject_reference | 3 | security_service |
| `customer_data_inventory_20260916.sql` | `snapshot_scope` | 8 | nested `record_json` / none | 0 | no identity-linked row |
| `customer_data_inventory_20260916.sql` | `support_records` | 3 | customer_reference, requester_email | 3 | support_platform |
| `customer_data_read_replica_20260613.sql` | `customer_data_primary` | 24 | nested `record_json` / none | 20 | backup_service, legal_service, search_service, security_service, support_platform |
| `customer_data_read_replica_20260613.sql` | `customer_data_read_replica` | 26 | nested `record_json` / none | 22 | account_service, backup_service, legal_service, search_service, security_service, support_platform |
| `customer_data_read_replica_20260708.sql` | `customer_data_primary` | 31 | nested `record_json` / none | 24 | analytics_platform, backup_service, search_service, security_service, support_platform |
| `customer_data_read_replica_20260708.sql` | `customer_data_read_replica` | 32 | nested `record_json` / none | 25 | account_service, analytics_platform, backup_service, search_service, security_service, support_platform |
| `customer_data_read_replica_20260802.sql` | `customer_data_primary` | 24 | nested `record_json` / none | 20 | analytics_platform, backup_service, export_service, search_service, security_service, support_platform |
| `customer_data_read_replica_20260802.sql` | `customer_data_read_replica` | 25 | nested `record_json` / none | 21 | account_service, analytics_platform, backup_service, export_service, search_service, security_service, support_platform |
| `customer_data_read_replica_20260827.sql` | `customer_data_primary` | 29 | nested `record_json` / none | 19 | analytics_platform, backup_service, search_service, security_service, support_platform |
| `customer_data_read_replica_20260827.sql` | `customer_data_read_replica` | 30 | nested `record_json` / none | 20 | account_service, analytics_platform, backup_service, search_service, security_service, support_platform |
| `customer_data_read_replica_20260921.sql` | `customer_data_primary` | 30 | nested `record_json` / none | 22 | analytics_platform, backup_service, search_service, security_service, support_platform |
| `customer_data_read_replica_20260921.sql` | `customer_data_read_replica` | 31 | nested `record_json` / none | 23 | account_service, analytics_platform, backup_service, search_service, security_service, support_platform |
| `customer_data_regional_replicas_20260330.sql` | `customer_data_primary` | 28 | nested `record_json` / none | 20 | analytics_platform, search_service, security_service, support_platform |
| `customer_data_regional_replicas_20260330.sql` | `customer_data_replica_ap_south` | 29 | nested `record_json` / none | 21 | account_service, analytics_platform, search_service, security_service, support_platform |
| `customer_data_regional_replicas_20260330.sql` | `customer_data_replica_eu_west` | 28 | nested `record_json` / none | 20 | analytics_platform, search_service, security_service, support_platform |
| `customer_data_regional_replicas_20260424.sql` | `customer_data_primary` | 29 | nested `record_json` / none | 23 | analytics_platform, export_service, search_service, security_service, support_platform |
| `customer_data_regional_replicas_20260424.sql` | `customer_data_replica_ap_south` | 29 | nested `record_json` / none | 23 | analytics_platform, export_service, search_service, security_service, support_platform |
| `customer_data_regional_replicas_20260424.sql` | `customer_data_replica_eu_west` | 31 | nested `record_json` / none | 25 | account_service, analytics_platform, export_service, search_service, security_service, support_platform |
| `customer_data_regional_replicas_20260519.sql` | `customer_data_primary` | 28 | nested `record_json` / none | 23 | analytics_platform, backup_service, export_service, search_service, security_service, support_platform |
| `customer_data_regional_replicas_20260519.sql` | `customer_data_replica_ap_south` | 29 | nested `record_json` / none | 24 | account_service, analytics_platform, backup_service, export_service, search_service, security_service, support_platform |
| `customer_data_regional_replicas_20260519.sql` | `customer_data_replica_eu_west` | 28 | nested `record_json` / none | 23 | analytics_platform, backup_service, export_service, search_service, security_service, support_platform |
| `customer_data_reporting_replica_20260208.sql` | `customer_data_primary` | 24 | nested `record_json` / none | 20 | analytics_platform, backup_service, export_service, legal_service, search_service, security_service, support_platform |
| `customer_data_reporting_replica_20260208.sql` | `customer_data_reporting_replica` | 25 | nested `record_json` / none | 21 | account_service, analytics_platform, backup_service, export_service, legal_service, search_service, security_service, support_platform |
| `customer_data_reporting_replica_20260305.sql` | `customer_data_primary` | 25 | nested `record_json` / none | 19 | analytics_platform, backup_service, legal_service, search_service, security_service, support_platform |
| `customer_data_reporting_replica_20260305.sql` | `customer_data_reporting_replica` | 26 | nested `record_json` / none | 20 | account_service, analytics_platform, backup_service, legal_service, search_service, security_service, support_platform |
| `customer_search_primary_20260910.sql` | `search_documents_primary` | 3 | email | 1 | search_service |
