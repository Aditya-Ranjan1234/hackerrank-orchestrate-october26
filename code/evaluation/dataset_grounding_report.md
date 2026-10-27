# Dataset grounding report

dataset_root: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset

### deletion_requests.csv
columns: ['case_id', 'email', 'requested_at', 'reported_status', 'reported_at', 'audit_at', 'request_text']
row_count: 518
first_5_rows:
- line 2: {'case_id': 'case_33', 'email': 'ingrid.dahl@outlook.com', 'requested_at': '2026-07-16T08:00:00Z', 'reported_status': 'COMPLETE', 'reported_at': '2026-07-18T02:00:00Z', 'audit_at': '2026-07-19T13:00:00Z', 'request_text': 'Please close my account and process the associated personal-data deletion. Please handle any copies that fall within the scope of the deletion request. Please confirm when the re…
- line 3: {'case_id': 'case_34', 'email': 'haruka.s1838@zoho.com', 'requested_at': '2026-09-24T08:00:00Z', 'reported_status': 'COMPLETE', 'reported_at': '2026-09-26T02:00:00Z', 'audit_at': '2026-09-27T13:00:00Z', 'request_text': 'I would like the account associated with this address to be erased. Please handle any copies that fall within the scope of the deletion request. Please contact me if you need infor…
- line 4: {'case_id': 'case_35', 'email': 'g.silva76@gmail.com', 'requested_at': '2026-08-30T03:00:00Z', 'reported_status': 'NOT_STARTED', 'reported_at': '2026-08-31T21:00:00Z', 'audit_at': '2026-09-02T08:00:00Z', 'request_text': 'Please close my account and process the associated personal-data deletion. Please check the records connected to the account before confirming completion. Please contact me if you…
- line 5: {'case_id': 'case_36', 'email': 'aadebayo3975@fastmail.com', 'requested_at': '2026-09-07T12:00:00Z', 'reported_status': 'COMPLETE', 'reported_at': '2026-09-09T12:00:00Z', 'audit_at': '2026-10-01T12:00:00Z', 'request_text': 'Please close my account and process the associated personal-data deletion. Please review the account data that is eligible for deletion or de-identification. Please send a conf…
- line 6: {'case_id': 'case_37', 'email': 'abena.o189491@zoho.com', 'requested_at': '2026-09-06T12:00:00Z', 'reported_status': 'COMPLETE', 'reported_at': '2026-09-09T12:00:00Z', 'audit_at': '2026-10-01T12:00:00Z', 'request_text': 'I want to close this account and have its associated personal data deleted. Please apply the request across the systems covered by your deletion policy. Please let me know once th…
distinct_values_per_column:
- case_id: distinct=518 first_10_sorted=['case_100', 'case_101', 'case_102', 'case_103', 'case_104', 'case_105', 'case_106', 'case_107', 'case_108', 'case_109'] top_10_by_frequency=[('case_33', 1), ('case_34', 1), ('case_35', 1), ('case_36', 1), ('case_37', 1), ('case_38', 1), ('case_39', 1), ('case_40', 1), ('case_41', 1), ('case_42', 1)]
- email: distinct=517 first_10_sorted=['ABENA.A30485@OUTLOOK.COM', 'BCARVALHO6517@GMAIL.COM', 'CARTER.AMELIA92@GMAIL.COM', 'CHOI.JIHOON94@GMAIL.COM', 'H.LIM96@GMAIL.COM', 'HLEFEVRE4815@FASTMAIL.COM', 'HYUNWOO.KANG94@GMAIL.COM', 'INES.ROUSSEAU@OUTLOOK.COM', 'JULES-LAURENT@PROTON.ME', 'K.KOWALSKI36@GMAIL.COM'] top_10_by_frequency=[('ingrid.dahl@outlook.com', 2), ('haruka.s1838@zoho.com', 1), ('g.silva76@gmail.com', 1), ('aadebayo3975@fastmail.com', 1), ('abena.o189491@zoho.com', 1), ('SIPHO.MOKOENA@GMAIL.COM', 1), ('jain.aditi@gmail.com', 1), ('CHOI.JIHOON94@GMAIL.COM', 1), ('lucas-souza95@gmail.com', 1), ('asingh1489@gmail.com', 1)]
- requested_at: distinct=508 first_10_sorted=['2026-01-05T06:00:00Z', '2026-01-06T06:00:00Z', '2026-01-07T06:00:00Z', '2026-01-08T06:00:00Z', '2026-01-09T06:00:00Z', '2026-01-09T12:00:00Z', '2026-01-10T06:00:00Z', '2026-01-10T12:00:00Z', '2026-01-11T06:00:00Z', '2026-01-11T12:00:00Z'] top_10_by_frequency=[('2026-09-06T12:00:00Z', 3), ('2026-09-02T12:00:00Z', 3), ('2026-09-07T12:00:00Z', 2), ('2026-09-05T12:00:00Z', 2), ('2026-09-03T12:00:00Z', 2), ('2026-07-11T07:00:00Z', 2), ('2026-09-04T12:00:00Z', 2), ('2026-08-31T12:00:00Z', 2), ('2026-07-16T08:00:00Z', 1), ('2026-09-24T08:00:00Z', 1)]
- reported_status: distinct=3 first_10_sorted=['COMPLETE', 'NOT_STARTED', 'PARTIALLY_COMPLETE'] top_10_by_frequency=[('COMPLETE', 254), ('PARTIALLY_COMPLETE', 152), ('NOT_STARTED', 112)]
- reported_at: distinct=238 first_10_sorted=['2026-01-06T06:00:00Z', '2026-01-09T06:00:00Z', '2026-01-12T06:00:00Z', '2026-01-12T12:00:00Z', '2026-01-15T06:00:00Z', '2026-01-15T12:00:00Z', '2026-01-17T08:00:00Z', '2026-01-18T12:00:00Z', '2026-01-20T07:00:00Z', '2026-01-20T08:00:00Z'] top_10_by_frequency=[('2026-09-05T12:00:00Z', 4), ('2026-09-09T12:00:00Z', 3), ('2026-09-12T11:00:00Z', 3), ('2026-08-29T10:00:00Z', 3), ('2026-09-04T09:00:00Z', 3), ('2026-09-01T09:00:00Z', 3), ('2026-08-21T08:00:00Z', 3), ('2026-08-18T08:00:00Z', 3), ('2026-08-27T07:00:00Z', 3), ('2026-08-24T07:00:00Z', 3)]
- audit_at: distinct=72 first_10_sorted=['2026-01-29T12:00:00Z', '2026-02-03T06:00:00Z', '2026-02-08T07:00:00Z', '2026-02-13T08:00:00Z', '2026-02-14T10:00:00Z', '2026-02-18T09:00:00Z', '2026-02-23T10:00:00Z', '2026-02-28T11:00:00Z', '2026-03-05T12:00:00Z', '2026-03-10T06:00:00Z'] top_10_by_frequency=[('2026-09-11T08:00:00Z', 10), ('2026-09-06T07:00:00Z', 10), ('2026-09-01T06:00:00Z', 10), ('2026-08-27T12:00:00Z', 10), ('2026-08-22T11:00:00Z', 10), ('2026-08-17T10:00:00Z', 10), ('2026-08-12T09:00:00Z', 10), ('2026-08-07T08:00:00Z', 10), ('2026-08-02T07:00:00Z', 10), ('2026-07-28T06:00:00Z', 10)]
- request_text: distinct=375 first_10_sorted=['Can you tell me what personal information you hold about me? This is an information request, not a request to erase it.', "Could you send me a copy of the information held on my account? I still use it, so please don't delete or change anything.", 'I am asking you to remove my account and the personal information linked to it. Please apply the correct treatment to records covered by the request. A short confirmation when the process is complete is sufficient.', 'I am asking you to remove my account and the personal information linked to it. Please apply the correct treatment to records covered by the request. I would appreciate confirmation of the final outcome.', 'I am asking you to remove my account and the personal information linked to it. Please apply the correct treatment to records covered by the request. Please contact me if you need information to verify the request.', 'I am asking you to remove my account and the personal information linked to it. Please apply the request across the systems covered by your deletion policy. A short confirmation when the process is complete is sufficient.', 'I am asking you to remove my account and the personal information linked to it. Please apply the request across the systems covered by your deletion policy. Please confirm the result after completing the required checks.', 'I am asking you to remove my account and the personal information linked to it. Please apply the request across the systems covered by your deletion policy. Please contact me if you need information to verify the request.', 'I am asking you to remove my account and the personal information linked to it. Please apply the request across the systems covered by your deletion policy. Please let me know once the request has been reviewed.', 'I am asking you to remove my account and the personal information linked to it. Please check the records connected to the account before confirming completion. Please confirm when the review is complete.'] top_10_by_frequency=[('Solicito a exclusão permanente da conta associada a este e-mail. Verifiquem os identificadores atuais e anteriores conforme o processo de privacidade. Por favor, confirmem o resultado quando a análise terminar.', 14), ('이 이메일 주소에 연결된 계정의 영구 삭제를 요청합니다. 개인정보 처리 절차에 따라 현재 및 이전 식별자를 검토해 주세요. 검토가 완료되면 결과를 확인해 주세요.', 12), ('Solicito la eliminación permanente de la cuenta asociada a este correo. Revisen los identificadores actuales y anteriores según su política de privacidad. Por favor, confirmen el resultado cuando termine la revisión.', 12), ('このメールアドレスに関連するアカウントの完全な削除を依頼します。 プライバシー手続きに従い、現在および過去の識別情報を確認してください。 確認が完了したら結果をお知らせください。', 12), ('Je demande la suppression définitive du compte associé à cette adresse e-mail. Veuillez examiner les identifiants actuels et antérieurs conformément à votre procédure de confidentialité. Merci de confirmer le résultat une fois la vérification terminée.', 12), ('Please erase the account linked to this email address. Please handle any copies that fall within the scope of the deletion request. Let me know when the request has been completed.', 3), ('Please treat this message as a request for permanent account deletion. Please review any identifiers connected to this account as part of the request. Please confirm when the review is complete.', 3), ('Please permanently delete the account associated with this email address. Please apply the correct treatment to records covered by the request. Please confirm when the review is complete.', 3), ('Please treat this message as a request for permanent account deletion. Please apply the request across the systems covered by your deletion policy. Please send a confirmation after the process finishes.', 3), ('I would like to submit a request to delete this account and its personal data. Please process this under the standard personal-data deletion procedure. Please contact me if you need information to verify the request.', 3)]
null_counts:
- case_id: 0
- email: 0
- requested_at: 0
- reported_status: 0
- reported_at: 0
- audit_at: 0
- request_text: 0
malformed_rows: 0

### deletion_rules.csv
columns: ['rule_id', 'data_category', 'condition', 'required_action']
row_count: 15
first_5_rows:
- line 2: {'rule_id': 'rule_01', 'data_category': 'USER_PROFILE', 'condition': 'Always', 'required_action': 'DELETE'}
- line 3: {'rule_id': 'rule_02', 'data_category': 'SECONDARY_IDENTIFIER', 'condition': 'Always', 'required_action': 'DELETE'}
- line 4: {'rule_id': 'rule_03', 'data_category': 'SEARCH_INDEX_ENTRY', 'condition': 'Always', 'required_action': 'DELETE'}
- line 5: {'rule_id': 'rule_04', 'data_category': 'CACHE_ENTRY', 'condition': 'Always', 'required_action': 'DELETE'}
- line 6: {'rule_id': 'rule_05', 'data_category': 'SUPPORT_MESSAGE', 'condition': 'Conversation contains shared customer, agent, or order context that must be retained', 'required_action': 'REDACT'}
distinct_values_per_column:
- rule_id: distinct=15 first_10_sorted=['rule_01', 'rule_02', 'rule_03', 'rule_04', 'rule_05', 'rule_06', 'rule_07', 'rule_08', 'rule_09', 'rule_10'] top_10_by_frequency=[('rule_01', 1), ('rule_02', 1), ('rule_03', 1), ('rule_04', 1), ('rule_05', 1), ('rule_06', 1), ('rule_07', 1), ('rule_08', 1), ('rule_09', 1), ('rule_10', 1)]
- data_category: distinct=15 first_10_sorted=['ACCOUNT_TOMBSTONE', 'ANALYTICS_PROFILE', 'BACKUP_ARCHIVE', 'CACHE_ENTRY', 'EMAIL_DELIVERY_LOG', 'LEGAL_HOLD_RECORD', 'MARKETING_PROFILE', 'PRODUCT_TELEMETRY', 'SEARCH_INDEX_ENTRY', 'SECONDARY_IDENTIFIER'] top_10_by_frequency=[('USER_PROFILE', 1), ('SECONDARY_IDENTIFIER', 1), ('SEARCH_INDEX_ENTRY', 1), ('CACHE_ENTRY', 1), ('SUPPORT_MESSAGE', 1), ('SUPPORT_ATTACHMENT', 1), ('ANALYTICS_PROFILE', 1), ('PRODUCT_TELEMETRY', 1), ('USER_EXPORT', 1), ('MARKETING_PROFILE', 1)]
- condition: distinct=9 first_10_sorted=['A supplied legal hold is active', 'Account is deleted and only a stable internal user_id is needed to preserve references to retained records', 'Always', 'Attachment belongs only to the deletion subject', 'Conversation contains shared customer, agent, or order context that must be retained', 'Log contains a user email address', 'Record is still attributable to a user', 'Record is within the supplied retention period', 'Restore access can be blocked'] top_10_by_frequency=[('Always', 6), ('Record is still attributable to a user', 2), ('Conversation contains shared customer, agent, or order context that must be retained', 1), ('Attachment belongs only to the deletion subject', 1), ('Log contains a user email address', 1), ('Record is within the supplied retention period', 1), ('A supplied legal hold is active', 1), ('Restore access can be blocked', 1), ('Account is deleted and only a stable internal user_id is needed to preserve references to retained records', 1)]
- required_action: distinct=4 first_10_sorted=['ANONYMIZE', 'DELETE', 'REDACT', 'RETAIN'] top_10_by_frequency=[('DELETE', 7), ('REDACT', 3), ('RETAIN', 3), ('ANONYMIZE', 2)]
null_counts:
- rule_id: 0
- data_category: 0
- condition: 0
- required_action: 0
malformed_rows: 0

#### Full rows: deletion_rules.csv
- line 2: {'rule_id': 'rule_01', 'data_category': 'USER_PROFILE', 'condition': 'Always', 'required_action': 'DELETE'}
- line 3: {'rule_id': 'rule_02', 'data_category': 'SECONDARY_IDENTIFIER', 'condition': 'Always', 'required_action': 'DELETE'}
- line 4: {'rule_id': 'rule_03', 'data_category': 'SEARCH_INDEX_ENTRY', 'condition': 'Always', 'required_action': 'DELETE'}
- line 5: {'rule_id': 'rule_04', 'data_category': 'CACHE_ENTRY', 'condition': 'Always', 'required_action': 'DELETE'}
- line 6: {'rule_id': 'rule_05', 'data_category': 'SUPPORT_MESSAGE', 'condition': 'Conversation contains shared customer, agent, or order context that must be retained', 'required_action': 'REDACT'}
- line 7: {'rule_id': 'rule_06', 'data_category': 'SUPPORT_ATTACHMENT', 'condition': 'Attachment belongs only to the deletion subject', 'required_action': 'DELETE'}
- line 8: {'rule_id': 'rule_07', 'data_category': 'ANALYTICS_PROFILE', 'condition': 'Record is still attributable to a user', 'required_action': 'ANONYMIZE'}
- line 9: {'rule_id': 'rule_08', 'data_category': 'PRODUCT_TELEMETRY', 'condition': 'Record is still attributable to a user', 'required_action': 'ANONYMIZE'}
- line 10: {'rule_id': 'rule_09', 'data_category': 'USER_EXPORT', 'condition': 'Always', 'required_action': 'DELETE'}
- line 11: {'rule_id': 'rule_10', 'data_category': 'MARKETING_PROFILE', 'condition': 'Always', 'required_action': 'DELETE'}
- line 12: {'rule_id': 'rule_11', 'data_category': 'EMAIL_DELIVERY_LOG', 'condition': 'Log contains a user email address', 'required_action': 'REDACT'}
- line 13: {'rule_id': 'rule_12', 'data_category': 'SECURITY_AUDIT_LOG', 'condition': 'Record is within the supplied retention period', 'required_action': 'RETAIN'}
- line 14: {'rule_id': 'rule_13', 'data_category': 'LEGAL_HOLD_RECORD', 'condition': 'A supplied legal hold is active', 'required_action': 'RETAIN'}
- line 15: {'rule_id': 'rule_14', 'data_category': 'BACKUP_ARCHIVE', 'condition': 'Restore access can be blocked', 'required_action': 'RETAIN'}
- line 16: {'rule_id': 'rule_15', 'data_category': 'ACCOUNT_TOMBSTONE', 'condition': 'Account is deleted and only a stable internal user_id is needed to preserve references to retained records', 'required_action': 'REDACT'}

### evidence_files.csv
columns: ['file_id', 'file_path', 'origin', 'captured_at']
row_count: 94
first_5_rows:
- line 2: {'file_id': 'evidence_01', 'file_path': 'evidence/logs/service_events_ap_south_20260915.log', 'origin': 'central_observability_export', 'captured_at': '2026-09-15T11:59:39Z'}
- line 3: {'file_id': 'evidence_02', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260917.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-09-17T12:00:00Z'}
- line 4: {'file_id': 'evidence_03', 'file_path': 'evidence/records/customer_account_handover_20261001.txt', 'origin': 'customer_account_service', 'captured_at': '2026-10-01T12:00:00Z'}
- line 5: {'file_id': 'evidence_04', 'file_path': 'evidence/images/account_admin_console_20260926.png', 'origin': 'account_admin_portal', 'captured_at': '2026-09-26T11:00:00Z'}
- line 6: {'file_id': 'evidence_05', 'file_path': 'evidence/databases/customer_data_read_replica_20260921.sql', 'origin': 'customer_data_read_replica_capture', 'captured_at': '2026-09-21T10:00:00Z'}
distinct_values_per_column:
- file_id: distinct=94 first_10_sorted=['evidence_01', 'evidence_02', 'evidence_03', 'evidence_04', 'evidence_05', 'evidence_06', 'evidence_07', 'evidence_08', 'evidence_09', 'evidence_10'] top_10_by_frequency=[('evidence_01', 1), ('evidence_02', 1), ('evidence_03', 1), ('evidence_04', 1), ('evidence_05', 1), ('evidence_06', 1), ('evidence_07', 1), ('evidence_08', 1), ('evidence_09', 1), ('evidence_10', 1)]
- file_path: distinct=94 first_10_sorted=['evidence/databases/customer_accounts_failover_replica_20260902.sql', 'evidence/databases/customer_data_failover_replica_20260920.sql', 'evidence/databases/customer_data_inventory_20260213.sql', 'evidence/databases/customer_data_inventory_20260310.sql', 'evidence/databases/customer_data_inventory_20260404.sql', 'evidence/databases/customer_data_inventory_20260504.sql', 'evidence/databases/customer_data_inventory_20260524.sql', 'evidence/databases/customer_data_inventory_20260618.sql', 'evidence/databases/customer_data_inventory_20260703.sql', 'evidence/databases/customer_data_inventory_20260723.sql'] top_10_by_frequency=[('evidence/logs/service_events_ap_south_20260915.log', 1), ('evidence/records/customer_data_snapshot_bundle_20260917.json', 1), ('evidence/records/customer_account_handover_20261001.txt', 1), ('evidence/images/account_admin_console_20260926.png', 1), ('evidence/databases/customer_data_read_replica_20260921.sql', 1), ('evidence/logs/structured_service_events_eu_west_20260918.log', 1), ('evidence/records/customer_data_snapshot_bundle_20260913.json', 1), ('evidence/logs/search_index_diagnostic_20260906.log', 1), ('evidence/images/search_index_inspector_20260901.png', 1), ('evidence/databases/customer_data_read_replica_20260827.sql', 1)]
- origin: distinct=30 first_10_sorted=['account_admin_portal', 'account_history_service', 'analytics_platform', 'backup_service', 'central_observability_export', 'customer_account_failover_replica_capture', 'customer_account_service', 'customer_data_failover_replica_capture', 'customer_data_inventory_capture', 'customer_data_read_replica_capture'] top_10_by_frequency=[('central_observability_export', 12), ('records_assurance_snapshot_bundle', 12), ('service_resource_export', 11), ('customer_data_inventory_capture', 11), ('service_readback_logs', 11), ('customer_data_read_replica_capture', 5), ('support_platform', 3), ('customer_data_regional_replicas_capture', 3), ('analytics_platform', 2), ('export_service', 2)]
- captured_at: distinct=93 first_10_sorted=['2026-01-29T11:44:59Z', '2026-01-31T15:00:00Z', '2026-02-03T05:59:42Z', '2026-02-08T07:00:00Z', '2026-02-13T07:43:27Z', '2026-02-13T08:00:00Z', '2026-02-18T08:39:11Z', '2026-02-23T10:00:00Z', '2026-02-28T10:36:37Z', '2026-03-02T10:59:23Z'] top_10_by_frequency=[('2026-10-01T12:00:00Z', 2), ('2026-09-15T11:59:39Z', 1), ('2026-09-17T12:00:00Z', 1), ('2026-09-26T11:00:00Z', 1), ('2026-09-21T10:00:00Z', 1), ('2026-09-18T11:55:24Z', 1), ('2026-09-13T08:00:00Z', 1), ('2026-09-06T07:00:00Z', 1), ('2026-09-01T06:00:00Z', 1), ('2026-08-27T12:00:00Z', 1)]
null_counts:
- file_id: 0
- file_path: 0
- origin: 0
- captured_at: 0
malformed_rows: 0

#### Full rows: evidence_files.csv
- line 2: {'file_id': 'evidence_01', 'file_path': 'evidence/logs/service_events_ap_south_20260915.log', 'origin': 'central_observability_export', 'captured_at': '2026-09-15T11:59:39Z'}
- line 3: {'file_id': 'evidence_02', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260917.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-09-17T12:00:00Z'}
- line 4: {'file_id': 'evidence_03', 'file_path': 'evidence/records/customer_account_handover_20261001.txt', 'origin': 'customer_account_service', 'captured_at': '2026-10-01T12:00:00Z'}
- line 5: {'file_id': 'evidence_04', 'file_path': 'evidence/images/account_admin_console_20260926.png', 'origin': 'account_admin_portal', 'captured_at': '2026-09-26T11:00:00Z'}
- line 6: {'file_id': 'evidence_05', 'file_path': 'evidence/databases/customer_data_read_replica_20260921.sql', 'origin': 'customer_data_read_replica_capture', 'captured_at': '2026-09-21T10:00:00Z'}
- line 7: {'file_id': 'evidence_06', 'file_path': 'evidence/logs/structured_service_events_eu_west_20260918.log', 'origin': 'central_observability_export', 'captured_at': '2026-09-18T11:55:24Z'}
- line 8: {'file_id': 'evidence_07', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260913.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-09-13T08:00:00Z'}
- line 9: {'file_id': 'evidence_08', 'file_path': 'evidence/logs/search_index_diagnostic_20260906.log', 'origin': 'search_index_service', 'captured_at': '2026-09-06T07:00:00Z'}
- line 10: {'file_id': 'evidence_09', 'file_path': 'evidence/images/search_index_inspector_20260901.png', 'origin': 'search_index_admin', 'captured_at': '2026-09-01T06:00:00Z'}
- line 11: {'file_id': 'evidence_10', 'file_path': 'evidence/databases/customer_data_read_replica_20260827.sql', 'origin': 'customer_data_read_replica_capture', 'captured_at': '2026-08-27T12:00:00Z'}
- line 12: {'file_id': 'evidence_11', 'file_path': 'evidence/logs/syslog_archive_us_east_20260824.log', 'origin': 'central_observability_export', 'captured_at': '2026-08-24T13:56:43Z'}
- line 13: {'file_id': 'evidence_12', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260819.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-08-19T10:00:00Z'}
- line 14: {'file_id': 'evidence_13', 'file_path': 'evidence/records/connector_configurations_20260812.json', 'origin': 'integration_management_service', 'captured_at': '2026-08-12T09:00:00Z'}
- line 15: {'file_id': 'evidence_14', 'file_path': 'evidence/images/connector_management_console_20260807.png', 'origin': 'integration_admin', 'captured_at': '2026-08-07T08:00:00Z'}
- line 16: {'file_id': 'evidence_15', 'file_path': 'evidence/databases/customer_data_read_replica_20260802.sql', 'origin': 'customer_data_read_replica_capture', 'captured_at': '2026-08-02T07:00:00Z'}
- line 17: {'file_id': 'evidence_16', 'file_path': 'evidence/logs/application_trace_ap_northeast_20260730.log', 'origin': 'central_observability_export', 'captured_at': '2026-07-30T08:53:12Z'}
- line 18: {'file_id': 'evidence_17', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260725.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-07-25T15:00:00Z'}
- line 19: {'file_id': 'evidence_18', 'file_path': 'evidence/documents/account_history_report_20260718.pdf', 'origin': 'account_history_service', 'captured_at': '2026-07-18T11:00:00Z'}
- line 20: {'file_id': 'evidence_19', 'file_path': 'evidence/images/analytics_profile_view_20260713.png', 'origin': 'analytics_platform', 'captured_at': '2026-07-13T10:00:00Z'}
- line 21: {'file_id': 'evidence_20', 'file_path': 'evidence/databases/customer_data_read_replica_20260708.sql', 'origin': 'customer_data_read_replica_capture', 'captured_at': '2026-07-08T09:00:00Z'}
- line 22: {'file_id': 'evidence_21', 'file_path': 'evidence/logs/operations_stream_eu_central_20260705.log', 'origin': 'central_observability_export', 'captured_at': '2026-07-05T07:54:27Z'}
- line 23: {'file_id': 'evidence_22', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260630.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-06-30T07:00:00Z'}
- line 24: {'file_id': 'evidence_23', 'file_path': 'evidence/images/customer_export_console_20260618.png', 'origin': 'export_service', 'captured_at': '2026-06-18T12:00:00Z'}
- line 25: {'file_id': 'evidence_24', 'file_path': 'evidence/databases/customer_data_read_replica_20260613.sql', 'origin': 'customer_data_read_replica_capture', 'captured_at': '2026-06-13T11:00:00Z'}
- line 26: {'file_id': 'evidence_25', 'file_path': 'evidence/logs/cloud_runtime_export_us_west_20260608.log', 'origin': 'central_observability_export', 'captured_at': '2026-06-08T09:58:28Z'}
- line 27: {'file_id': 'evidence_26', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260605.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-06-05T12:00:00Z'}
- line 28: {'file_id': 'evidence_27', 'file_path': 'evidence/documents/legal_retention_register_20260529.pdf', 'origin': 'legal_retention_service', 'captured_at': '2026-05-29T08:00:00Z'}
- line 29: {'file_id': 'evidence_28', 'file_path': 'evidence/images/support_ticket_console_20260524.png', 'origin': 'support_platform', 'captured_at': '2026-05-24T07:00:00Z'}
- line 30: {'file_id': 'evidence_29', 'file_path': 'evidence/databases/customer_data_regional_replicas_20260519.sql', 'origin': 'customer_data_regional_replicas_capture', 'captured_at': '2026-05-19T06:00:00Z'}
- line 31: {'file_id': 'evidence_30', 'file_path': 'evidence/logs/service_events_sa_east_20260516.log', 'origin': 'central_observability_export', 'captured_at': '2026-05-16T11:58:25Z'}
- line 32: {'file_id': 'evidence_31', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260511.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-05-11T11:00:00Z'}
- line 33: {'file_id': 'evidence_32', 'file_path': 'evidence/images/backup_restore_console_20260429.png', 'origin': 'backup_service', 'captured_at': '2026-04-29T09:00:00Z'}
- line 34: {'file_id': 'evidence_33', 'file_path': 'evidence/databases/customer_data_regional_replicas_20260424.sql', 'origin': 'customer_data_regional_replicas_capture', 'captured_at': '2026-04-24T08:00:00Z'}
- line 35: {'file_id': 'evidence_34', 'file_path': 'evidence/logs/structured_service_events_ca_central_20260419.log', 'origin': 'central_observability_export', 'captured_at': '2026-04-19T06:59:43Z'}
- line 36: {'file_id': 'evidence_35', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260416.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-04-16T06:00:00Z'}
- line 37: {'file_id': 'evidence_36', 'file_path': 'evidence/records/customer_export_manifest_20260409.json', 'origin': 'customer_export_service', 'captured_at': '2026-04-09T12:00:00Z'}
- line 38: {'file_id': 'evidence_37', 'file_path': 'evidence/images/security_audit_explorer_20260905.png', 'origin': 'security_service', 'captured_at': '2026-09-05T07:00:00Z'}
- line 39: {'file_id': 'evidence_38', 'file_path': 'evidence/databases/customer_data_regional_replicas_20260330.sql', 'origin': 'customer_data_regional_replicas_capture', 'captured_at': '2026-03-30T10:00:00Z'}
- line 40: {'file_id': 'evidence_39', 'file_path': 'evidence/logs/syslog_archive_ap_southeast_20260325.log', 'origin': 'central_observability_export', 'captured_at': '2026-03-25T08:59:44Z'}
- line 41: {'file_id': 'evidence_40', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260322.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-03-22T08:00:00Z'}
- line 42: {'file_id': 'evidence_41', 'file_path': 'evidence/logs/notification_delivery_20260315.log', 'origin': 'downstream_delivery_service', 'captured_at': '2026-03-15T07:00:00Z'}
- line 43: {'file_id': 'evidence_42', 'file_path': 'evidence/images/deleted_account_reference_20260310.png', 'origin': 'identity_service', 'captured_at': '2026-03-10T06:00:00Z'}
- line 44: {'file_id': 'evidence_43', 'file_path': 'evidence/databases/customer_data_reporting_replica_20260305.sql', 'origin': 'customer_data_reporting_replica_capture', 'captured_at': '2026-03-05T12:00:00Z'}
- line 45: {'file_id': 'evidence_44', 'file_path': 'evidence/logs/application_trace_eu_north_20260302.log', 'origin': 'central_observability_export', 'captured_at': '2026-03-02T10:59:23Z'}
- line 46: {'file_id': 'evidence_45', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260223.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-02-23T10:00:00Z'}
- line 47: {'file_id': 'evidence_46', 'file_path': 'evidence/images/object_storage_browser_20260213.png', 'origin': 'object_storage', 'captured_at': '2026-02-13T08:00:00Z'}
- line 48: {'file_id': 'evidence_47', 'file_path': 'evidence/databases/customer_data_reporting_replica_20260208.sql', 'origin': 'customer_data_reporting_replica_capture', 'captured_at': '2026-02-08T07:00:00Z'}
- line 49: {'file_id': 'evidence_48', 'file_path': 'evidence/logs/operations_stream_me_central_20260203.log', 'origin': 'central_observability_export', 'captured_at': '2026-02-03T05:59:42Z'}
- line 50: {'file_id': 'evidence_49', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260131.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-01-31T15:00:00Z'}
- line 51: {'file_id': 'evidence_50', 'file_path': 'evidence/records/security_audit_ledger_20261001.json', 'origin': 'security_audit_service', 'captured_at': '2026-10-01T12:00:00Z'}
- line 52: {'file_id': 'evidence_51', 'file_path': 'evidence/records/customer_data_snapshot_bundle_20260915.json', 'origin': 'records_assurance_snapshot_bundle', 'captured_at': '2026-09-15T12:00:00Z'}
- line 53: {'file_id': 'evidence_52', 'file_path': 'evidence/databases/customer_data_failover_replica_20260920.sql', 'origin': 'customer_data_failover_replica_capture', 'captured_at': '2026-09-20T12:00:00Z'}
- line 54: {'file_id': 'evidence_53', 'file_path': 'evidence/logs/cloud_runtime_export_af_south_20260930.log', 'origin': 'central_observability_export', 'captured_at': '2026-09-30T11:59:44Z'}
- line 55: {'file_id': 'evidence_54', 'file_path': 'evidence/databases/customer_accounts_failover_replica_20260902.sql', 'origin': 'customer_account_failover_replica_capture', 'captured_at': '2026-09-02T23:00:00Z'}
- line 56: {'file_id': 'evidence_55', 'file_path': 'evidence/documents/security_retention_extract.pdf', 'origin': 'security_service', 'captured_at': '2026-09-05T06:30:00Z'}
- line 57: {'file_id': 'evidence_56', 'file_path': 'evidence/records/customer_analytics_report_20260907.json', 'origin': 'analytics_platform', 'captured_at': '2026-09-07T09:45:00Z'}
- line 58: {'file_id': 'evidence_57', 'file_path': 'evidence/databases/customer_search_primary_20260910.sql', 'origin': 'customer_search_primary_capture', 'captured_at': '2026-09-10T08:45:00Z'}
- line 59: {'file_id': 'evidence_58', 'file_path': 'evidence/documents/delivery_correction_attachment.pdf', 'origin': 'support_platform', 'captured_at': '2026-09-12T07:30:00Z'}
- line 60: {'file_id': 'evidence_59', 'file_path': 'evidence/records/customer_export_jobs_20260914.json', 'origin': 'export_service', 'captured_at': '2026-09-14T15:40:00Z'}
- line 61: {'file_id': 'evidence_60', 'file_path': 'evidence/images/marketing_profile_console.png', 'origin': 'marketing_platform', 'captured_at': '2026-09-16T07:20:00Z'}
- line 62: {'file_id': 'evidence_61', 'file_path': 'evidence/logs/support_replica.log', 'origin': 'support_platform', 'captured_at': '2026-09-17T22:00:19Z'}
- line 63: {'file_id': 'evidence_62', 'file_path': 'evidence/records/service_resource_export_20260129_114459.json', 'origin': 'service_resource_export', 'captured_at': '2026-01-29T11:44:59Z'}
- line 64: {'file_id': 'evidence_63', 'file_path': 'evidence/databases/customer_data_inventory_20260213.sql', 'origin': 'customer_data_inventory_capture', 'captured_at': '2026-02-13T07:43:27Z'}
- line 65: {'file_id': 'evidence_64', 'file_path': 'evidence/logs/resource_lookup_trace_20260218_083911.log', 'origin': 'service_readback_logs', 'captured_at': '2026-02-18T08:39:11Z'}
- line 66: {'file_id': 'evidence_65', 'file_path': 'evidence/records/service_resource_export_20260228_103637.json', 'origin': 'service_resource_export', 'captured_at': '2026-02-28T10:36:37Z'}
- line 67: {'file_id': 'evidence_66', 'file_path': 'evidence/databases/customer_data_inventory_20260310.sql', 'origin': 'customer_data_inventory_capture', 'captured_at': '2026-03-10T05:38:48Z'}
- line 68: {'file_id': 'evidence_67', 'file_path': 'evidence/logs/resource_lookup_trace_20260310_061801.log', 'origin': 'service_readback_logs', 'captured_at': '2026-03-10T06:18:01Z'}
- line 69: {'file_id': 'evidence_68', 'file_path': 'evidence/records/service_resource_export_20260320_072349.json', 'origin': 'service_resource_export', 'captured_at': '2026-03-20T07:23:49Z'}
- line 70: {'file_id': 'evidence_69', 'file_path': 'evidence/databases/customer_data_inventory_20260404.sql', 'origin': 'customer_data_inventory_capture', 'captured_at': '2026-04-04T10:04:19Z'}
- line 71: {'file_id': 'evidence_70', 'file_path': 'evidence/logs/resource_lookup_trace_20260414_054007.log', 'origin': 'service_readback_logs', 'captured_at': '2026-04-14T05:40:07Z'}
- line 72: {'file_id': 'evidence_71', 'file_path': 'evidence/records/service_resource_export_20260429_083222.json', 'origin': 'service_resource_export', 'captured_at': '2026-04-29T08:32:22Z'}
- line 73: {'file_id': 'evidence_72', 'file_path': 'evidence/databases/customer_data_inventory_20260504.sql', 'origin': 'customer_data_inventory_capture', 'captured_at': '2026-05-04T09:41:47Z'}
- line 74: {'file_id': 'evidence_73', 'file_path': 'evidence/logs/resource_lookup_trace_20260509_104353.log', 'origin': 'service_readback_logs', 'captured_at': '2026-05-09T10:43:53Z'}
- line 75: {'file_id': 'evidence_74', 'file_path': 'evidence/records/service_resource_export_20260514_114454.json', 'origin': 'service_resource_export', 'captured_at': '2026-05-14T11:44:54Z'}
- line 76: {'file_id': 'evidence_75', 'file_path': 'evidence/databases/customer_data_inventory_20260524.sql', 'origin': 'customer_data_inventory_capture', 'captured_at': '2026-05-24T06:39:55Z'}
- line 77: {'file_id': 'evidence_76', 'file_path': 'evidence/logs/resource_lookup_trace_20260529_074313.log', 'origin': 'service_readback_logs', 'captured_at': '2026-05-29T07:43:13Z'}
- line 78: {'file_id': 'evidence_77', 'file_path': 'evidence/records/service_resource_export_20260603_083457.json', 'origin': 'service_resource_export', 'captured_at': '2026-06-03T08:34:57Z'}
- line 79: {'file_id': 'evidence_78', 'file_path': 'evidence/databases/customer_data_inventory_20260618.sql', 'origin': 'customer_data_inventory_capture', 'captured_at': '2026-06-18T11:44:03Z'}
- line 80: {'file_id': 'evidence_79', 'file_path': 'evidence/logs/resource_lookup_trace_20260623_053726.log', 'origin': 'service_readback_logs', 'captured_at': '2026-06-23T05:37:26Z'}
- line 81: {'file_id': 'evidence_80', 'file_path': 'evidence/records/service_resource_export_20260628_062556.json', 'origin': 'service_resource_export', 'captured_at': '2026-06-28T06:25:56Z'}
- line 82: {'file_id': 'evidence_81', 'file_path': 'evidence/databases/customer_data_inventory_20260703.sql', 'origin': 'customer_data_inventory_capture', 'captured_at': '2026-07-03T07:43:56Z'}
- line 83: {'file_id': 'evidence_82', 'file_path': 'evidence/logs/resource_lookup_trace_20260713_093359.log', 'origin': 'service_readback_logs', 'captured_at': '2026-07-13T09:33:59Z'}
- line 84: {'file_id': 'evidence_83', 'file_path': 'evidence/records/service_resource_export_20260718_104335.json', 'origin': 'service_resource_export', 'captured_at': '2026-07-18T10:43:35Z'}
- line 85: {'file_id': 'evidence_84', 'file_path': 'evidence/databases/customer_data_inventory_20260723.sql', 'origin': 'customer_data_inventory_capture', 'captured_at': '2026-07-23T11:43:30Z'}
- line 86: {'file_id': 'evidence_85', 'file_path': 'evidence/logs/resource_lookup_trace_20260728_054417.log', 'origin': 'service_readback_logs', 'captured_at': '2026-07-28T05:44:17Z'}
- line 87: {'file_id': 'evidence_86', 'file_path': 'evidence/records/service_resource_export_20260807_074104.json', 'origin': 'service_resource_export', 'captured_at': '2026-08-07T07:41:04Z'}
- line 88: {'file_id': 'evidence_87', 'file_path': 'evidence/databases/customer_data_inventory_20260817.sql', 'origin': 'customer_data_inventory_capture', 'captured_at': '2026-08-17T09:42:50Z'}
- line 89: {'file_id': 'evidence_88', 'file_path': 'evidence/logs/resource_lookup_trace_20260822_103910.log', 'origin': 'service_readback_logs', 'captured_at': '2026-08-22T10:39:10Z'}
- line 90: {'file_id': 'evidence_89', 'file_path': 'evidence/records/service_resource_export_20260901_053316.json', 'origin': 'service_resource_export', 'captured_at': '2026-09-01T05:33:16Z'}
- line 91: {'file_id': 'evidence_90', 'file_path': 'evidence/databases/customer_data_inventory_20260905.sql', 'origin': 'customer_data_inventory_capture', 'captured_at': '2026-09-05T07:18:01Z'}
- line 92: {'file_id': 'evidence_91', 'file_path': 'evidence/logs/resource_lookup_trace_20260911_074253.log', 'origin': 'service_readback_logs', 'captured_at': '2026-09-11T07:42:53Z'}
- line 93: {'file_id': 'evidence_92', 'file_path': 'evidence/records/service_resource_export_20260915_114455.json', 'origin': 'service_resource_export', 'captured_at': '2026-09-15T11:44:55Z'}
- line 94: {'file_id': 'evidence_93', 'file_path': 'evidence/databases/customer_data_inventory_20260916.sql', 'origin': 'customer_data_inventory_capture', 'captured_at': '2026-09-16T08:37:39Z'}
- line 95: {'file_id': 'evidence_94', 'file_path': 'evidence/logs/resource_lookup_trace_20260926_103856.log', 'origin': 'service_readback_logs', 'captured_at': '2026-09-26T10:38:56Z'}

### output.csv
columns: ['case_id', 'deletion_status', 'steps_json']
row_count: 0
first_5_rows:
distinct_values_per_column:
- case_id: distinct=0 first_10_sorted=[] top_10_by_frequency=[]
- deletion_status: distinct=0 first_10_sorted=[] top_10_by_frequency=[]
- steps_json: distinct=0 first_10_sorted=[] top_10_by_frequency=[]
null_counts:
- case_id: 0
- deletion_status: 0
- steps_json: 0
malformed_rows: 0

### sample_deletion_requests.csv
columns: ['case_id', 'email', 'requested_at', 'reported_status', 'reported_at', 'audit_at', 'request_text']
row_count: 32
first_5_rows:
- line 2: {'case_id': 'case_01', 'email': 'amina.elmasri@gmail.com', 'requested_at': '2026-08-18T09:14:00Z', 'reported_status': 'COMPLETE', 'reported_at': '2026-08-20T16:42:00Z', 'audit_at': '2026-09-03T11:30:00Z', 'request_text': 'Hi, I haven’t used this account in years and would like it closed. Please remove the profile and the personal details attached to it.'}
- line 3: {'case_id': 'case_02', 'email': 'mateo.rios@outlook.com', 'requested_at': '2026-08-21T18:06:00Z', 'reported_status': 'PARTIALLY_COMPLETE', 'reported_at': '2026-08-22T07:25:00Z', 'audit_at': '2026-09-04T15:00:00Z', 'request_text': 'Intenté eliminar mi cuenta ayer, pero la página terminó mostrando un error. ¿Pueden comprobar si todavía queda algún dato y completar la eliminación si hace falta?'}
- line 4: {'case_id': 'case_03', 'email': 'l.fontaine46@yahoo.com', 'requested_at': '2026-09-13T11:00:00Z', 'reported_status': 'COMPLETE', 'reported_at': '2026-09-15T11:00:00Z', 'audit_at': '2026-09-26T11:00:00Z', 'request_text': 'Je demande la suppression définitive du compte associé à cette adresse e-mail. Veuillez examiner les identifiants actuels et antérieurs conformément à votre procédure de confident…
- line 5: {'case_id': 'case_04', 'email': 'thandiwe.n@gmail.com', 'requested_at': '2026-08-25T12:32:00Z', 'reported_status': 'COMPLETE', 'reported_at': '2026-08-27T08:54:00Z', 'audit_at': '2026-09-07T10:20:00Z', 'request_text': 'I’m deleting my account. You can keep anonymous statistics, but nothing in analytics should still point back to me.'}
- line 6: {'case_id': 'case_05', 'email': 'leila.haddad@yahoo.com', 'requested_at': '2026-08-27T14:17:00Z', 'reported_status': 'COMPLETE', 'reported_at': '2026-08-28T09:03:00Z', 'audit_at': '2026-09-08T13:40:00Z', 'request_text': 'I deleted this account and received a confirmation, but the same email address is still recognized. Please remove any remaining copy of my profile.'}
distinct_values_per_column:
- case_id: distinct=32 first_10_sorted=['case_01', 'case_02', 'case_03', 'case_04', 'case_05', 'case_06', 'case_07', 'case_08', 'case_09', 'case_10'] top_10_by_frequency=[('case_01', 1), ('case_02', 1), ('case_03', 1), ('case_04', 1), ('case_05', 1), ('case_06', 1), ('case_07', 1), ('case_08', 1), ('case_09', 1), ('case_10', 1)]
- email: distinct=32 first_10_sorted=['a.eze08@gmail.com', 'addo.kofi@gmail.com', 'akosua.gyasi@gmail.com', 'almeida.mariana@gmail.com', 'amara-okeke@proton.me', 'amina.elmasri@gmail.com', 'ananya-nair@gmail.com', 'camille.bernard86@outlook.com', 'diya.k4436@outlook.com', 'e.varga90@yahoo.com'] top_10_by_frequency=[('amina.elmasri@gmail.com', 1), ('mateo.rios@outlook.com', 1), ('l.fontaine46@yahoo.com', 1), ('thandiwe.n@gmail.com', 1), ('leila.haddad@yahoo.com', 1), ('jonas.berg@outlook.com', 1), ('priya.raman@gmail.com', 1), ('gabriel.costa@proton.me', 1), ('k.appiah88@gmail.com', 1), ('nadia.ionescu@yahoo.com', 1)]
- requested_at: distinct=30 first_10_sorted=['2026-08-17T12:00:00Z', '2026-08-18T09:14:00Z', '2026-08-19T12:00:00Z', '2026-08-21T12:00:00Z', '2026-08-21T18:06:00Z', '2026-08-24T12:00:00Z', '2026-08-25T12:32:00Z', '2026-08-26T12:00:00Z', '2026-08-27T12:00:00Z', '2026-08-27T14:17:00Z'] top_10_by_frequency=[('2026-09-04T12:00:00Z', 3), ('2026-08-18T09:14:00Z', 1), ('2026-08-21T18:06:00Z', 1), ('2026-09-13T11:00:00Z', 1), ('2026-08-25T12:32:00Z', 1), ('2026-08-27T14:17:00Z', 1), ('2026-08-29T06:51:00Z', 1), ('2026-08-31T11:26:00Z', 1), ('2026-08-29T20:03:00Z', 1), ('2026-09-05T09:00:00Z', 1)]
- reported_status: distinct=3 first_10_sorted=['COMPLETE', 'NOT_STARTED', 'PARTIALLY_COMPLETE'] top_10_by_frequency=[('COMPLETE', 17), ('NOT_STARTED', 10), ('PARTIALLY_COMPLETE', 5)]
- reported_at: distinct=22 first_10_sorted=['2026-08-19T12:00:00Z', '2026-08-20T16:42:00Z', '2026-08-22T07:25:00Z', '2026-08-22T12:00:00Z', '2026-08-25T12:00:00Z', '2026-08-27T08:54:00Z', '2026-08-27T12:00:00Z', '2026-08-28T09:03:00Z', '2026-08-30T12:00:00Z', '2026-08-30T17:12:00Z'] top_10_by_frequency=[('2026-09-06T12:00:00Z', 3), ('2026-09-02T12:00:00Z', 3), ('2026-08-30T12:00:00Z', 3), ('2026-08-22T12:00:00Z', 2), ('2026-09-01T10:00:00Z', 2), ('2026-09-09T11:00:00Z', 2), ('2026-09-05T12:00:00Z', 2), ('2026-08-20T16:42:00Z', 1), ('2026-08-22T07:25:00Z', 1), ('2026-09-15T11:00:00Z', 1)]
- audit_at: distinct=13 first_10_sorted=['2026-09-03T11:30:00Z', '2026-09-04T15:00:00Z', '2026-09-07T10:20:00Z', '2026-09-08T13:40:00Z', '2026-09-10T09:15:00Z', '2026-09-12T08:00:00Z', '2026-09-14T16:10:00Z', '2026-09-15T12:00:00Z', '2026-09-16T09:00:00Z', '2026-09-18T12:25:00Z'] top_10_by_frequency=[('2026-09-15T12:00:00Z', 15), ('2026-09-26T11:00:00Z', 3), ('2026-10-01T12:00:00Z', 3), ('2026-09-21T10:00:00Z', 2), ('2026-09-03T11:30:00Z', 1), ('2026-09-04T15:00:00Z', 1), ('2026-09-07T10:20:00Z', 1), ('2026-09-08T13:40:00Z', 1), ('2026-09-10T09:15:00Z', 1), ('2026-09-12T08:00:00Z', 1)]
- request_text: distinct=32 first_10_sorted=['Can you verify that my account was deleted? A search result with a similar email belongs to someone else, so please do not treat that record as mine.', 'Hi, I haven’t used this account in years and would like it closed. Please remove the profile and the personal details attached to it.', 'I am asking you to remove my account and the personal information linked to it. Please review any identifiers connected to this account as part of the request. Please let me know once the request has been reviewed.', 'I changed the email on this account before deleting it. Please check that nothing tied to the old address was left behind, even in systems that do not display the email.', 'I closed my account, but an old “download your data” link still works. Please delete that export file as well.', 'I deleted my account and received the confirmation email. Could you verify that the profile is gone and that anything retained for security is limited to what is required?', 'I deleted this account and received a confirmation, but the same email address is still recognized. Please remove any remaining copy of my profile.', 'I disconnected my account last week, but one of the integrations still seems active. Close the account completely and make sure it can no longer send my data to other systems.', 'I found an old report saying my account still existed. Please check the latest state and confirm that the profile is gone and that remaining records cannot identify me.', 'I no longer need this account. Please remove my name and contact details, but keeping an internal deleted-account reference is fine if other required records still depend on it.'] top_10_by_frequency=[('Hi, I haven’t used this account in years and would like it closed. Please remove the profile and the personal details attached to it.', 1), ('Intenté eliminar mi cuenta ayer, pero la página terminó mostrando un error. ¿Pueden comprobar si todavía queda algún dato y completar la eliminación si hace falta?', 1), ('Je demande la suppression définitive du compte associé à cette adresse e-mail. Veuillez examiner les identifiants actuels et antérieurs conformément à votre procédure de confidentialité. Merci de confirmer le résultat une fois la vérification terminée.', 1), ('I’m deleting my account. You can keep anonymous statistics, but nothing in analytics should still point back to me.', 1), ('I deleted this account and received a confirmation, but the same email address is still recognized. Please remove any remaining copy of my profile.', 1), ('My account page is gone, but my old profile still appears when I search for it. Can you remove that search result too?', 1), ('Please delete my account and the identity document I sent to support while resolving a delivery issue.', 1), ('I closed my account, but an old “download your data” link still works. Please delete that export file as well.', 1), ('Please permanently delete the account associated with this email address. Please apply the correct treatment to records covered by the request. Please confirm when the review is complete.', 1), ('I used this Yahoo address before changing the email on my account. Please remove records linked to both the old and current addresses.', 1)]
null_counts:
- case_id: 0
- email: 0
- requested_at: 0
- reported_status: 0
- reported_at: 0
- audit_at: 0
- request_text: 0
malformed_rows: 0

### sample_output.csv
columns: ['case_id', 'deletion_status', 'steps_json']
row_count: 32
first_5_rows:
- line 2: {'case_id': 'case_01', 'deletion_status': 'COMPLETE', 'steps_json': '[{"evidence_id":"evidence_54","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_001","state":"ABSENT","step_no":1,"system_id":"account_service"}]'}
- line 3: {'case_id': 'case_02', 'deletion_status': 'COMPLETE', 'steps_json': '[{"evidence_id":"evidence_54","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_002","state":"ABSENT","step_no":1,"system_id":"account_service"}]'}
- line 4: {'case_id': 'case_03', 'deletion_status': 'COMPLETE', 'steps_json': '[{"step_no":1,"phase":"VERIFICATION","system_id":"account_service","resource_id":"account_7566","operation":"VERIFY_RECORD_ABSENT","state":"ABSENT","evidence_id":"evidence_94"},{"step_no":2,"phase":"VERIFICATION","system_id":"security_service","resource_id":"audit_record_2016","operation":"VERIFY_RECORD_PRESENT","state":"PRESENT"…
- line 5: {'case_id': 'case_04', 'deletion_status': 'COMPLETE', 'steps_json': '[{"evidence_id":"evidence_54","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_004","state":"ABSENT","step_no":1,"system_id":"account_service"},{"evidence_id":"evidence_56","operation":"VERIFY_RECORD_ANONYMIZED","phase":"VERIFICATION","resource_id":"analytics_901","state":"ANONYMIZED","step_no":2,"…
- line 6: {'case_id': 'case_05', 'deletion_status': 'INCOMPLETE', 'steps_json': '[{"evidence_id":"evidence_54","operation":"REPORT_REMAINING_RECORD","phase":"FINDING","resource_id":"account_005","state":"PRESENT","step_no":1,"system_id":"account_service"},{"evidence_id":"","operation":"DELETE_RECORD","phase":"REMEDIATION","resource_id":"account_005","state":"ABSENT","step_no":2,"system_id":"account_service"…
distinct_values_per_column:
- case_id: distinct=32 first_10_sorted=['case_01', 'case_02', 'case_03', 'case_04', 'case_05', 'case_06', 'case_07', 'case_08', 'case_09', 'case_10'] top_10_by_frequency=[('case_01', 1), ('case_02', 1), ('case_03', 1), ('case_04', 1), ('case_05', 1), ('case_06', 1), ('case_07', 1), ('case_08', 1), ('case_09', 1), ('case_10', 1)]
- deletion_status: distinct=2 first_10_sorted=['COMPLETE', 'INCOMPLETE'] top_10_by_frequency=[('INCOMPLETE', 22), ('COMPLETE', 10)]
- steps_json: distinct=32 first_10_sorted=['[{"evidence_id":"evidence_54","operation":"REPORT_REMAINING_RECORD","phase":"FINDING","resource_id":"account_005","state":"PRESENT","step_no":1,"system_id":"account_service"},{"evidence_id":"","operation":"DELETE_RECORD","phase":"REMEDIATION","resource_id":"account_005","state":"ABSENT","step_no":2,"system_id":"account_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_005","state":"ABSENT","step_no":3,"system_id":"account_service"}]', '[{"evidence_id":"evidence_54","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_001","state":"ABSENT","step_no":1,"system_id":"account_service"}]', '[{"evidence_id":"evidence_54","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_002","state":"ABSENT","step_no":1,"system_id":"account_service"}]', '[{"evidence_id":"evidence_54","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_004","state":"ABSENT","step_no":1,"system_id":"account_service"},{"evidence_id":"evidence_56","operation":"VERIFY_RECORD_ANONYMIZED","phase":"VERIFICATION","resource_id":"analytics_901","state":"ANONYMIZED","step_no":2,"system_id":"analytics_platform"}]', '[{"evidence_id":"evidence_57","operation":"REPORT_REMAINING_RECORD","phase":"FINDING","resource_id":"search_001","state":"PRESENT","step_no":1,"system_id":"search_service"},{"evidence_id":"","operation":"DELETE_RECORD","phase":"REMEDIATION","resource_id":"search_001","state":"ABSENT","step_no":2,"system_id":"search_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_006","state":"ABSENT","step_no":3,"system_id":"account_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"search_001","state":"ABSENT","step_no":4,"system_id":"search_service"}]', '[{"evidence_id":"evidence_58","operation":"REPORT_REMAINING_RECORD","phase":"FINDING","resource_id":"support_001","state":"PRESENT","step_no":1,"system_id":"support_platform"},{"evidence_id":"","operation":"DELETE_RECORD","phase":"REMEDIATION","resource_id":"support_001","state":"ABSENT","step_no":2,"system_id":"support_platform"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_007","state":"ABSENT","step_no":3,"system_id":"account_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"support_001","state":"ABSENT","step_no":4,"system_id":"support_platform"}]', '[{"evidence_id":"evidence_59","operation":"REPORT_REMAINING_RECORD","phase":"FINDING","resource_id":"export_001","state":"PRESENT","step_no":1,"system_id":"export_service"},{"evidence_id":"","operation":"DELETE_RECORD","phase":"REMEDIATION","resource_id":"export_001","state":"ABSENT","step_no":2,"system_id":"export_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_008","state":"ABSENT","step_no":3,"system_id":"account_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"export_001","state":"ABSENT","step_no":4,"system_id":"export_service"}]', '[{"evidence_id":"evidence_61","operation":"REPORT_REMAINING_RECORD","phase":"FINDING","resource_id":"support_002","state":"PRESENT","step_no":1,"system_id":"support_platform"},{"evidence_id":"","operation":"DELETE_RECORD","phase":"REMEDIATION","resource_id":"support_002","state":"ABSENT","step_no":2,"system_id":"support_platform"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_010","state":"ABSENT","step_no":3,"system_id":"account_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"support_002","state":"ABSENT","step_no":4,"system_id":"support_platform"}]', '[{"step_no":1,"phase":"FINDING","system_id":"account_service","resource_id":"account_5334","operation":"REPORT_REMAINING_RECORD","state":"PRESENT","evidence_id":"evidence_92"},{"step_no":2,"phase":"FINDING","system_id":"search_service","resource_id":"search_5577","operation":"REPORT_REMAINING_RECORD","state":"PRESENT","evidence_id":"evidence_92"},{"step_no":3,"phase":"REMEDIATION","system_id":"account_service","resource_id":"account_5334","operation":"DELETE_RECORD","state":"ABSENT","evidence_id":""},{"step_no":4,"phase":"REMEDIATION","system_id":"search_service","resource_id":"search_5577","operation":"DELETE_RECORD","state":"ABSENT","evidence_id":""},{"step_no":5,"phase":"VERIFICATION","system_id":"account_service","resource_id":"account_5334","operation":"VERIFY_RECORD_ABSENT","state":"ABSENT","evidence_id":""},{"step_no":6,"phase":"VERIFICATION","system_id":"search_service","resource_id":"search_5577","operation":"VERIFY_RECORD_ABSENT","state":"ABSENT","evidence_id":""},{"step_no":7,"phase":"VERIFICATION","system_id":"security_service","resource_id":"audit_record_7095","operation":"VERIFY_RECORD_PRESENT","state":"PRESENT","evidence_id":""}]', '[{"step_no":1,"phase":"FINDING","system_id":"account_service","resource_id":"account_994","operation":"REPORT_REMAINING_RECORD","state":"PRESENT","evidence_id":"evidence_05"},{"step_no":2,"phase":"FINDING","system_id":"search_service","resource_id":"search_1007","operation":"REPORT_REMAINING_RECORD","state":"PRESENT","evidence_id":"evidence_05"},{"step_no":3,"phase":"REMEDIATION","system_id":"account_service","resource_id":"account_994","operation":"DELETE_RECORD","state":"ABSENT","evidence_id":""},{"step_no":4,"phase":"REMEDIATION","system_id":"search_service","resource_id":"search_1007","operation":"DELETE_RECORD","state":"ABSENT","evidence_id":""},{"step_no":5,"phase":"VERIFICATION","system_id":"account_service","resource_id":"account_994","operation":"VERIFY_RECORD_ABSENT","state":"ABSENT","evidence_id":""},{"step_no":6,"phase":"VERIFICATION","system_id":"search_service","resource_id":"search_1007","operation":"VERIFY_RECORD_ABSENT","state":"ABSENT","evidence_id":""},{"step_no":7,"phase":"VERIFICATION","system_id":"security_service","resource_id":"audit_record_9528","operation":"VERIFY_RECORD_PRESENT","state":"PRESENT","evidence_id":""}]'] top_10_by_frequency=[('[{"evidence_id":"evidence_54","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_001","state":"ABSENT","step_no":1,"system_id":"account_service"}]', 1), ('[{"evidence_id":"evidence_54","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_002","state":"ABSENT","step_no":1,"system_id":"account_service"}]', 1), ('[{"step_no":1,"phase":"VERIFICATION","system_id":"account_service","resource_id":"account_7566","operation":"VERIFY_RECORD_ABSENT","state":"ABSENT","evidence_id":"evidence_94"},{"step_no":2,"phase":"VERIFICATION","system_id":"security_service","resource_id":"audit_record_2016","operation":"VERIFY_RECORD_PRESENT","state":"PRESENT","evidence_id":"evidence_94"},{"step_no":3,"phase":"VERIFICATION","system_id":"analytics_platform","resource_id":"analytics_9406","operation":"VERIFY_RECORD_ANONYMIZED","state":"ANONYMIZED","evidence_id":"evidence_94"}]', 1), ('[{"evidence_id":"evidence_54","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_004","state":"ABSENT","step_no":1,"system_id":"account_service"},{"evidence_id":"evidence_56","operation":"VERIFY_RECORD_ANONYMIZED","phase":"VERIFICATION","resource_id":"analytics_901","state":"ANONYMIZED","step_no":2,"system_id":"analytics_platform"}]', 1), ('[{"evidence_id":"evidence_54","operation":"REPORT_REMAINING_RECORD","phase":"FINDING","resource_id":"account_005","state":"PRESENT","step_no":1,"system_id":"account_service"},{"evidence_id":"","operation":"DELETE_RECORD","phase":"REMEDIATION","resource_id":"account_005","state":"ABSENT","step_no":2,"system_id":"account_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_005","state":"ABSENT","step_no":3,"system_id":"account_service"}]', 1), ('[{"evidence_id":"evidence_57","operation":"REPORT_REMAINING_RECORD","phase":"FINDING","resource_id":"search_001","state":"PRESENT","step_no":1,"system_id":"search_service"},{"evidence_id":"","operation":"DELETE_RECORD","phase":"REMEDIATION","resource_id":"search_001","state":"ABSENT","step_no":2,"system_id":"search_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_006","state":"ABSENT","step_no":3,"system_id":"account_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"search_001","state":"ABSENT","step_no":4,"system_id":"search_service"}]', 1), ('[{"evidence_id":"evidence_58","operation":"REPORT_REMAINING_RECORD","phase":"FINDING","resource_id":"support_001","state":"PRESENT","step_no":1,"system_id":"support_platform"},{"evidence_id":"","operation":"DELETE_RECORD","phase":"REMEDIATION","resource_id":"support_001","state":"ABSENT","step_no":2,"system_id":"support_platform"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_007","state":"ABSENT","step_no":3,"system_id":"account_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"support_001","state":"ABSENT","step_no":4,"system_id":"support_platform"}]', 1), ('[{"evidence_id":"evidence_59","operation":"REPORT_REMAINING_RECORD","phase":"FINDING","resource_id":"export_001","state":"PRESENT","step_no":1,"system_id":"export_service"},{"evidence_id":"","operation":"DELETE_RECORD","phase":"REMEDIATION","resource_id":"export_001","state":"ABSENT","step_no":2,"system_id":"export_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_008","state":"ABSENT","step_no":3,"system_id":"account_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"export_001","state":"ABSENT","step_no":4,"system_id":"export_service"}]', 1), ('[{"step_no":1,"phase":"FINDING","system_id":"backup_service","resource_id":"backup_4978","operation":"REPORT_RESTORE_RISK","state":"ACTIVE","evidence_id":"evidence_93"},{"step_no":2,"phase":"REMEDIATION","system_id":"backup_service","resource_id":"backup_4978","operation":"BLOCK_RESTORE","state":"BLOCKED","evidence_id":""},{"step_no":3,"phase":"VERIFICATION","system_id":"account_service","resource_id":"account_3960","operation":"VERIFY_RECORD_ABSENT","state":"ABSENT","evidence_id":""},{"step_no":4,"phase":"VERIFICATION","system_id":"security_service","resource_id":"audit_record_4902","operation":"VERIFY_RECORD_PRESENT","state":"PRESENT","evidence_id":""},{"step_no":5,"phase":"VERIFICATION","system_id":"backup_service","resource_id":"backup_4978","operation":"VERIFY_RESTORE_BLOCKED","state":"BLOCKED","evidence_id":""}]', 1), ('[{"evidence_id":"evidence_61","operation":"REPORT_REMAINING_RECORD","phase":"FINDING","resource_id":"support_002","state":"PRESENT","step_no":1,"system_id":"support_platform"},{"evidence_id":"","operation":"DELETE_RECORD","phase":"REMEDIATION","resource_id":"support_002","state":"ABSENT","step_no":2,"system_id":"support_platform"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"account_010","state":"ABSENT","step_no":3,"system_id":"account_service"},{"evidence_id":"","operation":"VERIFY_RECORD_ABSENT","phase":"VERIFICATION","resource_id":"support_002","state":"ABSENT","step_no":4,"system_id":"support_platform"}]', 1)]
null_counts:
- case_id: 0
- deletion_status: 0
- steps_json: 0
malformed_rows: 0

#### Gold statuses
- case_01: COMPLETE
- case_02: COMPLETE
- case_03: COMPLETE
- case_04: COMPLETE
- case_05: INCOMPLETE
- case_06: INCOMPLETE
- case_07: INCOMPLETE
- case_08: INCOMPLETE
- case_09: INCOMPLETE
- case_10: INCOMPLETE
- case_11: INCOMPLETE
- case_12: INCOMPLETE
- case_13: INCOMPLETE
- case_14: INCOMPLETE
- case_15: INCOMPLETE
- case_16: INCOMPLETE
- case_17: INCOMPLETE
- case_18: INCOMPLETE
- case_19: INCOMPLETE
- case_20: INCOMPLETE
- case_21: COMPLETE
- case_22: INCOMPLETE
- case_23: INCOMPLETE
- case_24: INCOMPLETE
- case_25: COMPLETE
- case_26: COMPLETE
- case_27: COMPLETE
- case_28: COMPLETE
- case_29: INCOMPLETE
- case_30: INCOMPLETE
- case_31: COMPLETE
- case_32: INCOMPLETE

### system_activity.csv
columns: ['activity_id', 'event_time', 'event_type', 'source_system', 'target_system', 'resource_id', 'reported_result', 'details']
row_count: 4011
first_5_rows:
- line 2: {'activity_id': 'activity_01', 'event_time': '2026-01-04T14:56:29Z', 'event_type': 'INDEX_RECORD', 'source_system': 'account_service', 'target_system': 'search_service', 'resource_id': 'search_9729', 'reported_result': 'SUCCESS', 'details': 'Customer search-index refresh processed search_9729.'}
- line 3: {'activity_id': 'activity_02', 'event_time': '2026-01-04T16:08:26Z', 'event_type': 'INDEX_RECORD', 'source_system': 'account_service', 'target_system': 'search_service', 'resource_id': 'search_6919', 'reported_result': 'SUCCESS', 'details': 'Customer search-index refresh processed search_6919.'}
- line 4: {'activity_id': 'activity_03', 'event_time': '2026-01-04T17:14:03Z', 'event_type': 'INDEX_RECORD', 'source_system': 'account_service', 'target_system': 'search_service', 'resource_id': 'search_4613', 'reported_result': 'SUCCESS', 'details': 'Customer search-index refresh processed search_4613.'}
- line 5: {'activity_id': 'activity_04', 'event_time': '2026-01-04T18:36:21Z', 'event_type': 'UPDATE_RECORD', 'source_system': 'support_platform', 'target_system': 'search_service', 'resource_id': 'support_4185', 'reported_result': 'SUCCESS', 'details': 'Support-case index update processed support_4185.'}
- line 6: {'activity_id': 'activity_05', 'event_time': '2026-01-04T18:36:36Z', 'event_type': 'UPDATE_RECORD', 'source_system': 'profile_service', 'target_system': 'account_service', 'resource_id': 'account_2689', 'reported_result': 'FAILED', 'details': 'Profile preference update processed account_2689.'}
distinct_values_per_column:
- activity_id: distinct=4011 first_10_sorted=['activity_01', 'activity_02', 'activity_03', 'activity_04', 'activity_05', 'activity_06', 'activity_07', 'activity_08', 'activity_09', 'activity_10'] top_10_by_frequency=[('activity_01', 1), ('activity_02', 1), ('activity_03', 1), ('activity_04', 1), ('activity_05', 1), ('activity_06', 1), ('activity_07', 1), ('activity_08', 1), ('activity_09', 1), ('activity_10', 1)]
- event_time: distinct=4011 first_10_sorted=['2026-01-04T14:56:29Z', '2026-01-04T16:08:26Z', '2026-01-04T17:14:03Z', '2026-01-04T18:36:21Z', '2026-01-04T18:36:36Z', '2026-01-04T19:32:42Z', '2026-01-04T23:30:59Z', '2026-01-05T02:52:52Z', '2026-01-05T04:54:03Z', '2026-01-05T08:44:32Z'] top_10_by_frequency=[('2026-01-04T14:56:29Z', 1), ('2026-01-04T16:08:26Z', 1), ('2026-01-04T17:14:03Z', 1), ('2026-01-04T18:36:21Z', 1), ('2026-01-04T18:36:36Z', 1), ('2026-01-04T19:32:42Z', 1), ('2026-01-04T23:30:59Z', 1), ('2026-01-05T02:52:52Z', 1), ('2026-01-05T04:54:03Z', 1), ('2026-01-05T08:44:32Z', 1)]
- event_type: distinct=17 first_10_sorted=['ANONYMIZE_RECORD', 'BLOCK_RESTORE', 'CHECK_DATA_FLOW', 'CHECK_RESTORE_ACCESS', 'CLASSIFY_REQUEST', 'CREATE_EXPORT', 'DELETE_RECORD', 'DISABLE_DATA_FLOW', 'INDEX_RECORD', 'LINK_RESOURCE_IDENTITY'] top_10_by_frequency=[('DELETE_RECORD', 890), ('UPDATE_RECORD', 672), ('SYNC_RECORD', 447), ('INDEX_RECORD', 400), ('SEND_EMAIL', 368), ('REFRESH_CACHE', 284), ('RETAIN_RECORD', 206), ('ANONYMIZE_RECORD', 204), ('REDACT_RECORD', 173), ('CREATE_EXPORT', 155)]
- source_system: distinct=11 first_10_sorted=['account_service', 'backup_service', 'data_catalog', 'deletion_worker', 'export_service', 'integration_service', 'notification_service', 'privacy_intake', 'profile_service', 'security_service'] top_10_by_frequency=[('deletion_worker', 1466), ('account_service', 1100), ('profile_service', 440), ('notification_service', 368), ('support_platform', 232), ('security_service', 196), ('export_service', 155), ('integration_service', 31), ('data_catalog', 12), ('privacy_intake', 10)]
- target_system: distinct=19 first_10_sorted=['account_failover_replica', 'account_replication_cluster', 'account_service', 'analytics_platform', 'archive_service', 'backup_service', 'cache_service', 'email_delivery_service', 'export_service', 'identity_service'] top_10_by_frequency=[('account_service', 980), ('search_service', 954), ('analytics_platform', 566), ('email_delivery_service', 368), ('cache_service', 284), ('archive_service', 196), ('support_platform', 193), ('object_store', 155), ('integration_service', 126), ('backup_service', 65)]
- resource_id: distinct=3948 first_10_sorted=['account_001', 'account_002', 'account_005', 'account_006', 'account_007', 'account_008', 'account_010', 'account_018', 'account_022', 'account_034'] top_10_by_frequency=[('account_1334', 2), ('account_634', 2), ('account_4974', 2), ('account_3626', 2), ('account_2424', 2), ('account_1035', 2), ('account_3119', 2), ('account_6654', 2), ('account_3205', 2), ('account_5293', 2)]
- reported_result: distinct=3 first_10_sorted=['FAILED', 'PARTIAL', 'SUCCESS'] top_10_by_frequency=[('SUCCESS', 2914), ('FAILED', 721), ('PARTIAL', 376)]
- details: distinct=4011 first_10_sorted=['Active connector repopulated downstream resource search_1474.', 'Active connector repopulated downstream resource search_1725.', 'Active connector repopulated downstream resource search_1934.', 'Active connector repopulated downstream resource search_2016.', 'Active connector repopulated downstream resource search_2126.', 'Active connector repopulated downstream resource search_2591.', 'Active connector repopulated downstream resource search_2818.', 'Active connector repopulated downstream resource search_2886.', 'Active connector repopulated downstream resource search_3120.', 'Active connector repopulated downstream resource search_3232.'] top_10_by_frequency=[('Customer search-index refresh processed search_9729.', 1), ('Customer search-index refresh processed search_6919.', 1), ('Customer search-index refresh processed search_4613.', 1), ('Support-case index update processed support_4185.', 1), ('Profile preference update processed account_2689.', 1), ('Security-event archival processed audit_record_7206.', 1), ('Support-case index update processed support_1854.', 1), ('Transactional email delivery processed email_delivery_354.', 1), ('Transactional email delivery processed email_delivery_9741.', 1), ('Profile preference update processed account_1910.', 1)]
null_counts:
- activity_id: 0
- event_time: 0
- event_type: 0
- source_system: 0
- target_system: 0
- resource_id: 0
- reported_result: 0
- details: 0
malformed_rows: 0

### user_audit_log.csv
columns: ['audit_id', 'user_id', 'event_time', 'field_name', 'old_value', 'new_value']
row_count: 306
first_5_rows:
- line 2: {'audit_id': 'audit_01', 'user_id': 'user_485', 'event_time': '2024-12-14T16:31:44Z', 'field_name': 'phone', 'old_value': '+33 6 24 34 80 16', 'new_value': '+33 6 63 29 68 28'}
- line 3: {'audit_id': 'audit_02', 'user_id': 'user_505', 'event_time': '2024-12-25T00:51:04Z', 'field_name': 'phone', 'old_value': '+81 90 6278 6936', 'new_value': '+81 90 7870 0272'}
- line 4: {'audit_id': 'audit_03', 'user_id': 'user_525', 'event_time': '2025-01-04T00:11:24Z', 'field_name': 'phone', 'old_value': '+46 70 144 08 06', 'new_value': '+46 70 808 74 05'}
- line 5: {'audit_id': 'audit_04', 'user_id': 'user_380', 'event_time': '2025-01-28T13:16:29Z', 'field_name': 'phone', 'old_value': '+44 7700 900880', 'new_value': '+44 7700 900380'}
- line 6: {'audit_id': 'audit_05', 'user_id': 'user_400', 'event_time': '2025-02-08T04:36:49Z', 'field_name': 'phone', 'old_value': '+27 72 156 3064', 'new_value': '+27 72 384 3167'}
distinct_values_per_column:
- audit_id: distinct=306 first_10_sorted=['audit_01', 'audit_02', 'audit_03', 'audit_04', 'audit_05', 'audit_06', 'audit_07', 'audit_08', 'audit_09', 'audit_10'] top_10_by_frequency=[('audit_01', 1), ('audit_02', 1), ('audit_03', 1), ('audit_04', 1), ('audit_05', 1), ('audit_06', 1), ('audit_07', 1), ('audit_08', 1), ('audit_09', 1), ('audit_10', 1)]
- user_id: distinct=196 first_10_sorted=['user_10', 'user_100', 'user_105', 'user_108', 'user_11', 'user_110', 'user_115', 'user_116', 'user_12', 'user_120'] top_10_by_frequency=[('user_10', 4), ('user_35', 4), ('user_11', 3), ('user_523', 2), ('user_528', 2), ('user_530', 2), ('user_518', 2), ('user_509', 2), ('user_497', 2), ('user_496', 2)]
- event_time: distinct=198 first_10_sorted=['2024-12-14T16:31:44Z', '2024-12-25T00:51:04Z', '2025-01-04T00:11:24Z', '2025-01-28T13:16:29Z', '2025-02-08T04:36:49Z', '2025-02-17T16:01:14Z', '2025-02-27T14:16:29Z', '2025-02-28T00:21:34Z', '2025-03-10T00:41:54Z', '2025-03-10T05:36:49Z'] top_10_by_frequency=[('2026-05-17T20:18:43Z', 3), ('2025-09-30T21:50:27Z', 2), ('2025-10-01T07:25:02Z', 2), ('2025-10-01T08:27:16Z', 2), ('2025-10-05T20:15:52Z', 2), ('2025-10-11T00:36:49Z', 2), ('2025-10-15T19:24:25Z', 2), ('2025-10-16T02:53:18Z', 2), ('2025-10-20T21:41:54Z', 2), ('2025-10-21T03:08:33Z', 2)]
- field_name: distinct=3 first_10_sorted=['email', 'email_hash', 'phone'] top_10_by_frequency=[('email', 107), ('email_hash', 107), ('phone', 92)]
- old_value: distinct=306 first_10_sorted=['+1 (312) 555-0165', '+1 (415) 555-0105', '+1 (718) 555-0135', '+233 24 034 4993', '+233 24 052 8925', '+233 24 539 2068', '+233 24 863 3363', '+233 24 879 6395', '+233 24 983 7846', '+234 803 450 9724'] top_10_by_frequency=[('+33 6 24 34 80 16', 1), ('+81 90 6278 6936', 1), ('+46 70 144 08 06', 1), ('+44 7700 900880', 1), ('+27 72 156 3064', 1), ('+34 659 253 340', 1), ('+81 90 3704 0751', 1), ('+233 24 863 3363', 1), ('+1 (312) 555-0165', 1), ('+46 70 833 29 03', 1)]
- new_value: distinct=306 first_10_sorted=['+1 (202) 555-0185', '+1 (415) 555-0115', '+1 (617) 555-0155', '+233 24 262 4576', '+233 24 352 7302', '+233 24 643 0035', '+233 24 660 3074', '+233 24 713 5812', '+233 24 955 4457', '+234 803 064 1391'] top_10_by_frequency=[('+33 6 63 29 68 28', 1), ('+81 90 7870 0272', 1), ('+46 70 808 74 05', 1), ('+44 7700 900380', 1), ('+27 72 384 3167', 1), ('+34 628 427 174', 1), ('+81 90 2123 2514', 1), ('+233 24 352 7302', 1), ('+1 (415) 555-0115', 1), ('+46 70 124 53 62', 1)]
null_counts:
- audit_id: 0
- user_id: 0
- event_time: 0
- field_name: 0
- old_value: 0
- new_value: 0
malformed_rows: 0

### user_identities.csv
columns: ['user_id', 'name', 'email', 'phone', 'email_hash', 'updated_at']
row_count: 850
first_5_rows:
- line 2: {'user_id': 'user_01', 'name': 'Amina El-Masri', 'email': 'amina.elmasri@gmail.com', 'phone': '+971 50 482 7316', 'email_hash': 'd4e1f59abcf9a1e0cfdc7c27ad6c07ed4ff88b326a16ed5eed5ec6bc31618c93', 'updated_at': '2026-05-28T04:03:00Z'}
- line 3: {'user_id': 'user_02', 'name': 'Mateo Ríos', 'email': 'mateo.rios@outlook.com', 'phone': '+34 612 847 593', 'email_hash': 'fad1c282b6b8ff346ee92e617331f69c2b6bb345af954eeb44581c57529eab9d', 'updated_at': '2026-04-24T07:44:00Z'}
- line 4: {'user_id': 'user_03', 'name': 'Oliver Bennett', 'email': 'oliver-bennett@gmail.com', 'phone': '+1 (202) 555-0103', 'email_hash': '1fa7764c96e40e8570cbb7569f707f6d84c593cecbe5c1ed2b0a07a624dba039', 'updated_at': '2026-03-14T14:21:00Z'}
- line 5: {'user_id': 'user_04', 'name': 'Thandiwe Ndlovu', 'email': 'thandiwe.n@gmail.com', 'phone': '+27 71 684 5928', 'email_hash': 'f730ef60615bde7a8f5ee21138637b4e9d4094855fbb02da6afcdba9c076281f', 'updated_at': '2026-03-21T20:59:00Z'}
- line 6: {'user_id': 'user_05', 'name': 'Leila Haddad', 'email': 'leila.haddad@yahoo.com', 'phone': '+212 6 48 27 15 93', 'email_hash': '62667ed065b846a842474f916da51b658edb0f9754ab2da6bf38e68779ff0d08', 'updated_at': '2026-02-14T17:33:00Z'}
distinct_values_per_column:
- user_id: distinct=850 first_10_sorted=['user_01', 'user_02', 'user_03', 'user_04', 'user_05', 'user_06', 'user_07', 'user_08', 'user_09', 'user_10'] top_10_by_frequency=[('user_01', 1), ('user_02', 1), ('user_03', 1), ('user_04', 1), ('user_05', 1), ('user_06', 1), ('user_07', 1), ('user_08', 1), ('user_09', 1), ('user_10', 1)]
- name: distinct=847 first_10_sorted=['Aarav Basu', 'Aarav Mehta', 'Aarav Menon', 'Aarav Nair', 'Aarav Rao', 'Aarav Singh', 'Abena Agyeman', 'Abena Appiah', 'Abena Boateng', 'Abena Frimpong'] top_10_by_frequency=[('Mateo Ríos', 2), ('Thandiwe Ndlovu', 2), ('Gabriel Costa', 2), ('Amina El-Masri', 1), ('Oliver Bennett', 1), ('Leila Haddad', 1), ('Jonas Berg', 1), ('Priya Raman', 1), ('Kwame Mensah', 1), ('Nadia Petrescu', 1)]
- email: distinct=850 first_10_sorted=['a.adeyemi98@yahoo.com', 'a.appiah44@gmail.com', 'a.basu12@gmail.com', 'a.basu68@gmail.com', 'a.eze08@gmail.com', 'a.horvat28@gmail.com', 'a.ionescu18@yahoo.com', 'a.lefevre74@yahoo.com', 'a.martinez76@gmail.com', 'a.menon58@yahoo.com'] top_10_by_frequency=[('amina.elmasri@gmail.com', 1), ('mateo.rios@outlook.com', 1), ('oliver-bennett@gmail.com', 1), ('thandiwe.n@gmail.com', 1), ('leila.haddad@yahoo.com', 1), ('jonas.berg@outlook.com', 1), ('priya.raman@gmail.com', 1), ('gabriel.costa@proton.me', 1), ('kwame-mensah@proton.me', 1), ('n.petrescu@yahoo.com', 1)]
- phone: distinct=850 first_10_sorted=['+1 (202) 555-0103', '+1 (202) 555-0131', '+1 (202) 555-0149', '+1 (202) 555-0167', '+1 (202) 555-0185', '+1 (212) 555-0107', '+1 (212) 555-0135', '+1 (212) 555-0153', '+1 (212) 555-0171', '+1 (212) 555-0189'] top_10_by_frequency=[('+971 50 482 7316', 1), ('+34 612 847 593', 1), ('+1 (202) 555-0103', 1), ('+27 71 684 5928', 1), ('+212 6 48 27 15 93', 1), ('+46 70 482 91 37', 1), ('+91 98765 73142', 1), ('+55 11 97284-3165', 1), ('+233 24 456 1267', 1), ('+40 723 481 638', 1)]
- email_hash: distinct=850 first_10_sorted=['000b4a359e7bfb9632035fec16d9bfeba9aadfa547f183f8835bcd9ce953df63', '001d533c599d187966e3c7c7ec9b1efef67e69e18cf8e6a59163af61dd518d30', '007c8b80fd3dd19c63c4e155412922dfb98f111706f9139552c56bbe5396cfe2', '01335ce89c55c8bd901adc58a4b91311e7fa8495221db7f7de5ea92945c0fbe0', '01405f4109740d9989e557d89561807bd3ed72d2325aee5e0c43ed1e57b0dbd6', '0155a5ec12b8d7a94b96df59e7aa6168711f046e69ca6b007208714acebd5620', '0157f987b0fb5373a6b73db252169d109ab242f289c875be2509112ad1694927', '01b863e977b0d79ede109d37c3fcc8ca565640aeb7ef39be3821b1cbeee2dcab', '025085603b82c32e7febf86ae064516d8af0f2c9bf1df1200bd611bec5843c98', '025caf8ef287b0a337ef75f57daa9a12946b46ac8646f0c46802599c3aef0e23'] top_10_by_frequency=[('d4e1f59abcf9a1e0cfdc7c27ad6c07ed4ff88b326a16ed5eed5ec6bc31618c93', 1), ('fad1c282b6b8ff346ee92e617331f69c2b6bb345af954eeb44581c57529eab9d', 1), ('1fa7764c96e40e8570cbb7569f707f6d84c593cecbe5c1ed2b0a07a624dba039', 1), ('f730ef60615bde7a8f5ee21138637b4e9d4094855fbb02da6afcdba9c076281f', 1), ('62667ed065b846a842474f916da51b658edb0f9754ab2da6bf38e68779ff0d08', 1), ('4cd3f3cfee997d1ba25313c60209776e30d4038199421b7382ac737d86002666', 1), ('284c7b87b8237e241293c9e81c8f0bef10c4dc1dffefb382c45107ea40c39668', 1), ('1301193d061e1845f5b6a27dbe60e896845339b5315c3a61b57d7e7636f78617', 1), ('e7ce7f1fd5cd4e5873576243ee7a0ca8599c51d0e9f2197f6184efc514e5bd2a', 1), ('6385b5b5e70720c197abedd379f714bb84330a9c7bc86bbb4bfbc4405bdba326', 1)]
- updated_at: distinct=850 first_10_sorted=['2023-06-22T10:59:00Z', '2023-08-09T17:12:00Z', '2023-08-13T23:26:00Z', '2023-08-15T14:33:00Z', '2023-09-03T12:47:00Z', '2023-09-06T03:54:00Z', '2023-10-01T06:39:00Z', '2023-10-02T21:46:00Z', '2023-10-05T05:53:00Z', '2023-10-23T10:07:00Z'] top_10_by_frequency=[('2026-05-28T04:03:00Z', 1), ('2026-04-24T07:44:00Z', 1), ('2026-03-14T14:21:00Z', 1), ('2026-03-21T20:59:00Z', 1), ('2026-02-14T17:33:00Z', 1), ('2026-01-11T04:56:00Z', 1), ('2025-12-07T05:20:00Z', 1), ('2025-10-29T08:46:00Z', 1), ('2025-05-30T20:03:00Z', 1), ('2026-04-12T14:38:26Z', 1)]
null_counts:
- user_id: 0
- name: 0
- email: 0
- phone: 0
- email_hash: 0
- updated_at: 0
malformed_rows: 0

## Evidence file inventory

#### evidence_01
### service_events_ap_south_20260915.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\service_events_ap_south_20260915.log
bytes: 22237
line_count: 104
first_20_lines:
- 2026-09-15T08:51:43Z level=DEBUG service=log_router instance=collector-3 event=export_started sources=platform_services expected_source_events=98
- 2026-09-15T08:51:45Z level=DEBUG service=search_service instance=search-2 pod=search-12cc region=ap-south-1 trace_id=tr-5887496 event=index_query_started match_key="g.silva76.jr@gmail.com" attempt=1
- 2026-09-15T08:51:53Z level=DEBUG service=search_service instance=search-2 pod=search-12cc region=ap-south-1 trace_id=tr-5887496 event=connection_acquired pool=search_service_replica wait_ms=56
- 2026-09-15T08:51:55Z level=WARN service=search_service instance=search-2 pod=search-12cc region=ap-south-1 trace_id=tr-5887496 event=dependency_retry dependency=search_service_store attempt=1 retry_in_ms=474 reason=read_timeout
- 2026-09-15T08:51:56Z level=INFO service=search_service instance=search-2 pod=search-12cc region=ap-south-1 trace_id=tr-5887496 event=dependency_recovered attempt=2 route=primary
- 2026-09-15T08:51:57Z level=INFO service=search_service instance=search-2 pod=search-12cc region=ap-south-1 trace_id=tr-5887496 resource_id=search_1874 event=index_query_completed index=customer_directory_v3 result=hit shard=2 took_ms=17
- 2026-09-15T09:29:19Z level=WARN service=queue_consumer instance=worker-3 event=consumer_lag topic=notification_events partition=2 lag=33
- 2026-09-15T10:06:53Z level=DEBUG service=dns_cache instance=resolver-3 event=cache_refresh entries=85
- 2026-09-15T10:44:28Z level=INFO service=secret_agent instance=vault-3 event=lease_extended ttl_seconds=1202
- 2026-09-15T11:22:02Z level=ERROR service=webhook_delivery instance=notify-3 event=delivery_abandoned destination=status_page attempts=4 http_status=503
- 2026-09-15T11:50:57Z level=DEBUG service=support_platform instance=support-2 pod=support-70f0 region=ap-south-1 trace_id=tr-8896806 event=message_scan_started subject_key="e.varga90@yahoo.com" attempt=1
- 2026-09-15T11:51:04Z level=DEBUG service=support_platform instance=support-2 pod=support-70f0 region=ap-south-1 trace_id=tr-8896806 event=connection_acquired pool=support_platform_replica wait_ms=49
- 2026-09-15T11:51:06Z level=WARN service=support_platform instance=support-2 pod=support-70f0 region=ap-south-1 trace_id=tr-8896806 event=dependency_retry dependency=support_platform_store attempt=1 retry_in_ms=173 reason=read_timeout
- 2026-09-15T11:51:07Z level=INFO service=support_platform instance=support-2 pod=support-70f0 region=ap-south-1 trace_id=tr-8896806 event=dependency_recovered attempt=2 route=primary
- 2026-09-15T11:51:08Z level=WARN service=support_platform instance=support-2 pod=support-70f0 region=ap-south-1 trace_id=tr-8896806 resource_id=support_9553 event=message_pii_scan matched_value="e.varga90@yahoo.com" detector=direct_identifier
- 2026-09-15T11:51:09Z level=DEBUG service=account_service instance=account-6 pod=account-581a region=us-east-2 trace_id=tr-4708586 event=profile_lookup_started lookup_key="leonie.g9352@outlook.com" attempt=1
- 2026-09-15T11:51:15Z level=DEBUG service=account_service instance=account-6 pod=account-581a region=us-east-2 trace_id=tr-4708586 event=connection_acquired pool=account_service_replica wait_ms=17
- 2026-09-15T11:51:16Z level=INFO service=search_service instance=search-7 pod=search-acaf region=eu-central-1 trace_id=tr-0506485 resource_id=search_4639 event=index_query_completed index=customer_directory_v3 result=hit shard=7 took_ms=23 correlation_key="darwish.omar@icloud.com"
- 2026-09-15T11:51:17Z level=WARN service=account_service instance=account-6 pod=account-581a region=us-east-2 trace_id=tr-4708586 event=dependency_retry dependency=account_service_store attempt=1 retry_in_ms=412 reason=read_timeout
- 2026-09-15T11:51:18Z level=INFO service=account_service instance=account-6 pod=account-581a region=us-east-2 trace_id=tr-4708586 event=dependency_recovered attempt=2 route=primary
last_20_lines:
- 2026-09-15T11:58:08Z level=DEBUG service=integration_service instance=integration-1 pod=integration-95c3 region=eu-central-1 trace_id=tr-9750867 event=connector_config_read_started subject_key="lucia-torres@gmail.com" attempt=1
- 2026-09-15T11:58:08Z level=DEBUG service=security_service instance=security-2 pod=security-0d19 region=eu-west-1 trace_id=tr-1514907 event=audit_record_query_started subject_ref="user_13" attempt=1
- 2026-09-15T11:58:09Z level=DEBUG service=integration_service instance=integration-1 pod=integration-95c3 region=eu-central-1 trace_id=tr-9750867 event=connection_acquired pool=integration_service_primary wait_ms=19
- 2026-09-15T11:58:11Z level=WARN service=integration_service instance=integration-1 pod=integration-95c3 region=eu-central-1 trace_id=tr-9750867 resource_id=data_flow_9846 event=connector_heartbeat enabled=true scheduler_registered=true last_run=success
- 2026-09-15T11:58:15Z level=DEBUG service=security_service instance=security-2 pod=security-0d19 region=eu-west-1 trace_id=tr-1514907 event=connection_acquired pool=security_service_primary wait_ms=22
- 2026-09-15T11:58:17Z level=DEBUG service=security_service instance=security-2 pod=security-0d19 region=eu-west-1 trace_id=tr-1514907 resource_id=audit_record_8925 event=audit_record_read_completed integrity_check=passed rows=1
- 2026-09-15T11:58:20Z level=DEBUG service=backup_service instance=backup-5 pod=backup-4627 region=eu-central-1 trace_id=tr-5638333 event=restore_policy_check_started subject_key="areed1433@gmail.com" attempt=1
- 2026-09-15T11:58:26Z level=DEBUG service=analytics_platform instance=analytics-2 pod=analytics-9b40 region=ap-south-1 trace_id=tr-9137340 resource_id=analytics_9914 event=contact_lookup_completed rows=1 email_opt_in=true correlation_key="44a65154bfd8e408852578fbd76813d094d1944f255ac1769ee81ba90492f10e"
- 2026-09-15T11:58:30Z level=DEBUG service=backup_service instance=backup-5 pod=backup-4627 region=eu-central-1 trace_id=tr-5638333 event=cache_lookup result=miss cache=backup_service_lookup_v2
- 2026-09-15T11:58:31Z level=ERROR service=backup_service instance=backup-5 pod=backup-4627 region=eu-central-1 trace_id=tr-5638333 resource_id=backup_9287 event=restore_candidate_evaluated eligible=true deletion_block=false
- 2026-09-15T11:58:49Z level=DEBUG service=account_service instance=account-1 pod=account-cdfa region=us-east-2 trace_id=tr-7973332 event=profile_lookup_started lookup_key="g.silva76@gmail.com" attempt=1
- 2026-09-15T11:58:54Z level=DEBUG service=account_service instance=account-1 pod=account-cdfa region=us-east-2 trace_id=tr-7973332 event=connection_acquired pool=account_service_primary wait_ms=8
- 2026-09-15T11:58:56Z level=INFO service=account_service instance=account-1 pod=account-cdfa region=us-east-2 trace_id=tr-7973332 resource_id=account_8491 event=profile_lookup_completed rows=0 http_status=404 duration_ms=33
- 2026-09-15T11:59:12Z level=DEBUG service=search_service instance=search-4 pod=search-4169 region=eu-west-1 trace_id=tr-4331893 event=index_query_started match_key="g.silva76@gmail.com" attempt=1
- 2026-09-15T11:59:19Z level=DEBUG service=search_service instance=search-4 pod=search-4169 region=eu-west-1 trace_id=tr-4331893 event=cache_lookup result=miss cache=search_service_lookup_v2
- 2026-09-15T11:59:20Z level=INFO service=search_service instance=search-4 pod=search-4169 region=eu-west-1 trace_id=tr-4331893 resource_id=search_428 event=index_query_completed index=customer_directory_v3 result=hit shard=8 took_ms=28
- 2026-09-15T11:59:31Z level=DEBUG service=security_service instance=security-3 pod=security-ecfc region=ap-south-1 trace_id=tr-4314388 event=audit_record_query_started subject_ref="user_15" attempt=1
- 2026-09-15T11:59:36Z level=DEBUG service=security_service instance=security-3 pod=security-ecfc region=ap-south-1 trace_id=tr-4314388 event=cache_lookup result=miss cache=security_service_lookup_v2
- 2026-09-15T11:59:37Z level=DEBUG service=security_service instance=security-3 pod=security-ecfc region=ap-south-1 trace_id=tr-4314388 resource_id=audit_record_1596 event=audit_record_read_completed integrity_check=passed rows=1
- 2026-09-15T11:59:39Z level=INFO service=log_router instance=collector-3 event=export_completed source_events=98 auxiliary_events=4 dropped_auxiliary=2

#### evidence_02
### customer_data_snapshot_bundle_20260917.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260917.json
bytes: 17941
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-09-17T12:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-09-09T12:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_5684', 'customer_reference': 'user_26', 'full_name': 'Mariana Almeida', 'email': 'almeida.mariana@gmail.com', 'phone': '+55 21 90180-9087', 'account_status': 'ACTIVE', 'signup_channel': 'organic_search'}]}, {'captured_at': '2026-09-15T09:00:00Z', 'data_store': 'search_service', 'collection': 'customer_search_documents', 'records': [{'resource_id': 'search_8168…

#### evidence_03
### customer_account_handover_20261001.txt
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_account_handover_20261001.txt
bytes: 4534
line_count: 46
first_20_lines:
- CUSTOMER PLATFORM - SHIFT HANDOVER
- Snapshot: 2026-10-01T12:00:00Z
- 
- Account and downstream checks completed during the shift:
- 
- - 2026-10-01T12:00:00Z | account_service | account_146 | USER_PROFILE | NOT_FOUND | e.lindberg18@yahoo.com
- - 2026-10-01T12:00:00Z | account_service | account_1810 | USER_PROFILE | NOT_FOUND | CHOI.JIHOON94@GMAIL.COM
- - 2026-10-01T12:00:00Z | account_service | account_2381 | USER_PROFILE | NOT_FOUND | SIPHO.MOKOENA@GMAIL.COM
- - 2026-10-01T12:00:00Z | account_service | account_3677 | USER_PROFILE | NOT_FOUND | y.tanaka32@gmail.com
- - 2026-10-01T12:00:00Z | account_service | account_4051 | USER_PROFILE | NOT_FOUND | lucas-souza95@gmail.com
- - 2026-10-01T12:00:00Z | account_service | account_4248 | USER_PROFILE | NOT_FOUND | novak.tomasz@icloud.com
- - 2026-10-01T12:00:00Z | account_service | account_4337 | USER_PROFILE | NOT_FOUND | asingh1489@gmail.com
- - 2026-10-01T12:00:00Z | account_service | account_5193 | USER_PROFILE | NOT_FOUND | abena.o189491@zoho.com
- - 2026-10-01T12:00:00Z | account_service | account_5823 | USER_PROFILE | NOT_FOUND | aadebayo3975@fastmail.com
- - 2026-10-01T12:00:00Z | account_service | account_9335 | USER_PROFILE | NOT_FOUND | noor-khalil@proton.me
- - 2026-10-01T12:00:00Z | analytics_platform | analytics_2034 | ANALYTICS_PROFILE | IDENTIFIABLE | novak.tomasz@icloud.com
- - 2026-10-01T12:00:00Z | analytics_platform | analytics_6830 | ANALYTICS_PROFILE | ANONYMIZED | no direct identifier
- - 2026-10-01T12:00:00Z | analytics_platform | analytics_9447 | ANALYTICS_PROFILE | ANONYMIZED | no direct identifier
- - 2026-10-01T12:00:00Z | backup_service | backup_3870 | BACKUP_ARCHIVE | ACTIVE | y.tanaka32@gmail.com
- - 2026-10-01T12:00:00Z | backup_service | backup_706 | BACKUP_ARCHIVE | BLOCKED | user_39
last_20_lines:
- - 2026-10-01T12:00:00Z | search_service | search_1308 | SEARCH_INDEX_ENTRY | FOUND | noor-khalil@proton.me
- - 2026-10-01T12:00:00Z | search_service | search_1934 | SEARCH_INDEX_ENTRY | FOUND | abena.o189491@zoho.com
- - 2026-10-01T12:00:00Z | search_service | search_3200 | SEARCH_INDEX_ENTRY | FOUND | CHOI.JIHOON94@GMAIL.COM
- - 2026-10-01T12:00:00Z | search_service | search_5575 | SEARCH_INDEX_ENTRY | FOUND | aadebayo3975@fastmail.com
- - 2026-10-01T12:00:00Z | search_service | search_7078 | SEARCH_INDEX_ENTRY | FOUND | asingh1489@gmail.com
- - 2026-10-01T12:00:00Z | security_service | audit_record_2019 | SECURITY_AUDIT_LOG | FOUND | user_35
- - 2026-10-01T12:00:00Z | security_service | audit_record_2966 | SECURITY_AUDIT_LOG | FOUND | user_34
- - 2026-10-01T12:00:00Z | security_service | audit_record_4816 | SECURITY_AUDIT_LOG | FOUND | user_33
- - 2026-10-01T12:00:00Z | security_service | audit_record_5307 | SECURITY_AUDIT_LOG | FOUND | user_31
- - 2026-10-01T12:00:00Z | security_service | audit_record_633 | SECURITY_AUDIT_LOG | FOUND | user_36
- - 2026-10-01T12:00:00Z | security_service | audit_record_6760 | SECURITY_AUDIT_LOG | FOUND | user_40
- - 2026-10-01T12:00:00Z | security_service | audit_record_7814 | SECURITY_AUDIT_LOG | FOUND | user_39
- - 2026-10-01T12:00:00Z | security_service | audit_record_8349 | SECURITY_AUDIT_LOG | FOUND | user_38
- - 2026-10-01T12:00:00Z | security_service | audit_record_9394 | SECURITY_AUDIT_LOG | FOUND | user_32
- - 2026-10-01T12:00:00Z | security_service | audit_record_987 | SECURITY_AUDIT_LOG | FOUND | user_37
- - 2026-10-01T12:00:00Z | support_platform | support_2667 | SUPPORT_MESSAGE | REDACTED | user_39
- - 2026-10-01T12:00:00Z | support_platform | support_4218 | SUPPORT_ATTACHMENT | FOUND | noor-khalil@proton.me
- - 2026-10-01T12:00:00Z | support_platform | support_4887 | SUPPORT_MESSAGE | IDENTIFIABLE | CHOI.JIHOON94@GMAIL.COM
- - 2026-10-01T12:00:00Z | support_platform | support_7769 | SUPPORT_MESSAGE | IDENTIFIABLE | asingh1489@gmail.com
- - 2026-10-01T12:00:00Z | support_platform | support_864 | SUPPORT_MESSAGE | IDENTIFIABLE | novak.tomasz@icloud.com

#### evidence_04
### account_admin_console_20260926.png
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\images\account_admin_console_20260926.png
bytes: 124989
IMAGE_INSPECTION_ERROR: No module named 'PIL'

#### evidence_05
### customer_data_read_replica_20260921.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_read_replica_20260921.sql
bytes: 24740
CREATE_TABLE: ['CREATE TABLE customer_data_primary', 'CREATE TABLE customer_data_read_replica']
sample_INSERT: ['INSERT INTO "customer_data_primary" VALUES(\'analytics_1738\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_1738","user_id":"user_52","email":"bcarvalho6517@gmail.com","phone":"+55 41 90257-9346","email_hash":"da5e264130a…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_2572\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_2572","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_4440\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_4440","user_id":"user_51","email":"seoyeon-han@gmail.com","phone":"+82 10 8943 9310","email_hash":"bbd5522cc42afd…']

#### evidence_06
### structured_service_events_eu_west_20260918.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\structured_service_events_eu_west_20260918.log
bytes: 31311
line_count: 112
first_20_lines:
- 2026-09-10T08:56:15Z {"severity":"DEBUG","logger":"log_router","service":"log_router","instance":"collector-8","event":"export_started","sources":"platform_services","expected_source_events":"106"}
- 2026-09-10T08:56:17Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-6","pod":"account-ca1e","region":"us-east-2","trace_id":"tr-5563868","event":"profile_lookup_started","lookup_key":"collins.grace@icloud.com","attempt":"1"}
- 2026-09-10T08:56:19Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-6","pod":"account-ca1e","region":"us-east-2","trace_id":"tr-5563868","event":"cache_lookup","result":"miss","cache":"account_service_lookup_v2"}
- 2026-09-10T08:56:20Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-6","pod":"account-ca1e","region":"us-east-2","trace_id":"tr-5563868","resource_id":"account_6633","event":"profile_lookup_completed","rows":"1","http_status":"200","duration_ms":"84"}
- 2026-09-11T23:56:06Z {"severity":"DEBUG","logger":"feature_flags","service":"feature_flags","instance":"flags-3","event":"flag_snapshot_loaded","revision":"428"}
- 2026-09-13T14:55:55Z {"severity":"WARN","logger":"circuit_breaker","service":"circuit_breaker","instance":"breaker-2","event":"slow_call_rate","window":"37s","rate_pct":"15"}
- 2026-09-15T05:55:44Z {"severity":"DEBUG","logger":"dns_cache","service":"dns_cache","instance":"resolver-3","event":"cache_refresh","entries":"90"}
- 2026-09-16T05:57:57Z {"severity":"DEBUG","logger":"search_service","service":"search_service","instance":"search-2","pod":"search-f972","region":"us-east-2","trace_id":"tr-2218962","event":"index_query_started","match_key":"zulu.lindiwe.jr@gmail.com","attempt":"1"}
- 2026-09-16T05:58:03Z {"severity":"DEBUG","logger":"search_service","service":"search_service","instance":"search-2","pod":"search-f972","region":"us-east-2","trace_id":"tr-2218962","event":"connection_acquired","pool":"search_service_primary","wait_ms":"17"}
- 2026-09-16T05:58:05Z {"severity":"INFO","logger":"search_service","service":"search_service","instance":"search-2","pod":"search-f972","region":"us-east-2","trace_id":"tr-2218962","resource_id":"search_5252","event":"index_query_completed","index":"customer_directory_v3","result":"hit","shard":"8","took_ms":"16"}
- 2026-09-16T08:51:22Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-5","pod":"account-1d87","region":"eu-central-1","trace_id":"tr-4611491","event":"profile_lookup_started","lookup_key":"aoi-yamamoto@gmail.com","attempt":"1"}
- 2026-09-16T08:51:26Z {"severity":"DEBUG","logger":"support_platform","service":"support_platform","instance":"support-4","pod":"support-6cd2","region":"us-east-2","trace_id":"tr-5428224","event":"message_scan_started","subject_key":"hcho154598@gmail.com","attempt":"1"}
- 2026-09-16T08:51:29Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-5","pod":"account-1d87","region":"eu-central-1","trace_id":"tr-4611491","event":"connection_acquired","pool":"account_service_replica","wait_ms":"71"}
- 2026-09-16T08:51:30Z {"severity":"WARN","logger":"support_platform","service":"support_platform","instance":"support-4","pod":"support-6cd2","region":"us-east-2","trace_id":"tr-5428224","resource_id":"support_4249","event":"message_pii_scan","matched_value":"hcho154598@gmail.com","detector":"direct_identifier"}
- 2026-09-16T08:51:31Z {"severity":"WARN","logger":"account_service","service":"account_service","instance":"account-5","pod":"account-1d87","region":"eu-central-1","trace_id":"tr-4611491","event":"dependency_retry","dependency":"account_service_store","attempt":"1","retry_in_ms":"288","reason":"read_timeout"}
- 2026-09-16T08:51:32Z {"severity":"INFO","logger":"account_service","service":"account_service","instance":"account-5","pod":"account-1d87","region":"eu-central-1","trace_id":"tr-4611491","event":"dependency_recovered","attempt":"2","route":"primary"}
- 2026-09-16T08:51:33Z {"severity":"INFO","logger":"account_service","service":"account_service","instance":"account-5","pod":"account-1d87","region":"eu-central-1","trace_id":"tr-4611491","resource_id":"account_5488","event":"profile_lookup_completed","rows":"0","http_status":"404","duration_ms":"18"}
- 2026-09-16T08:52:07Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-3","pod":"security-063e","region":"us-east-2","trace_id":"tr-6695634","event":"audit_record_query_started","subject_ref":"user_68","attempt":"1"}
- 2026-09-16T08:52:09Z {"severity":"INFO","logger":"integration_service","service":"integration_service","instance":"integration-3","pod":"integration-e103","region":"eu-central-1","trace_id":"tr-5156035","resource_id":"data_flow_6846","event":"connector_config_loaded","enabled":"false","scheduler_registered":"false","correlation_key":"user_62"}
- 2026-09-16T08:52:11Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-3","pod":"security-063e","region":"us-east-2","trace_id":"tr-6695634","resource_id":"audit_record_1738","event":"audit_record_read_completed","integrity_check":"passed","rows":"1"}
last_20_lines:
- 2026-09-16T08:58:05Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-1","pod":"account-ed75","region":"eu-west-1","trace_id":"tr-4257173","event":"cache_lookup","result":"miss","cache":"account_service_lookup_v2"}
- 2026-09-16T08:58:06Z {"severity":"INFO","logger":"account_service","service":"account_service","instance":"account-1","pod":"account-ed75","region":"eu-west-1","trace_id":"tr-4257173","resource_id":"account_1602","event":"profile_lookup_completed","rows":"0","http_status":"404","duration_ms":"33"}
- 2026-09-16T08:58:06Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-3","pod":"security-cb8a","region":"us-east-2","trace_id":"tr-4144134","event":"audit_record_query_started","subject_ref":"user_70","attempt":"1"}
- 2026-09-16T08:58:14Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-3","pod":"security-cb8a","region":"us-east-2","trace_id":"tr-4144134","resource_id":"audit_record_1310","event":"audit_record_read_completed","integrity_check":"passed","rows":"1"}
- 2026-09-16T08:58:22Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-1","pod":"security-aaa3","region":"eu-central-1","trace_id":"tr-1925823","event":"audit_record_query_started","subject_ref":"user_69","attempt":"1"}
- 2026-09-16T08:58:31Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-1","pod":"security-aaa3","region":"eu-central-1","trace_id":"tr-1925823","event":"cache_lookup","result":"miss","cache":"security_service_lookup_v2"}
- 2026-09-16T08:58:32Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-1","pod":"security-aaa3","region":"eu-central-1","trace_id":"tr-1925823","resource_id":"audit_record_1096","event":"audit_record_read_completed","integrity_check":"passed","rows":"1"}
- 2026-09-16T08:58:57Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-6","pod":"security-0fd4","region":"ap-south-1","trace_id":"tr-5891060","resource_id":"audit_record_1848","event":"audit_record_read_completed","integrity_check":"passed","rows":"1","correlation_key":"user_63"}
- 2026-09-16T08:59:23Z {"severity":"DEBUG","logger":"support_platform","service":"support_platform","instance":"support-3","pod":"support-d2a2","region":"us-east-2","trace_id":"tr-4200358","event":"attachment_scan_started","scan_key":"JULES-LAURENT@PROTON.ME","attempt":"1"}
- 2026-09-16T08:59:27Z {"severity":"DEBUG","logger":"support_platform","service":"support_platform","instance":"support-3","pod":"support-d2a2","region":"us-east-2","trace_id":"tr-4200358","event":"cache_lookup","result":"miss","cache":"support_platform_lookup_v2"}
- 2026-09-16T08:59:28Z {"severity":"WARN","logger":"support_platform","service":"support_platform","instance":"support-3","pod":"support-d2a2","region":"us-east-2","trace_id":"tr-4200358","resource_id":"support_1370","event":"attachment_pii_scan","matched_value":"JULES-LAURENT@PROTON.ME","file":"delivery_confirmation_12.pdf","detector":"direct_identifier"}
- 2026-09-16T20:55:33Z {"severity":"INFO","logger":"secret_agent","service":"secret_agent","instance":"vault-4","event":"lease_extended","ttl_seconds":"1207"}
- 2026-09-18T11:51:34Z {"severity":"DEBUG","logger":"search_service","service":"search_service","instance":"search-1","pod":"search-9540","region":"ap-south-1","trace_id":"tr-9889054","event":"index_query_started","match_key":"rafael.r9464@outlook.com","attempt":"1"}
- 2026-09-18T11:51:37Z {"severity":"INFO","logger":"search_service","service":"search_service","instance":"search-1","pod":"search-9540","region":"ap-south-1","trace_id":"tr-9889054","resource_id":"search_9837","event":"index_query_completed","index":"customer_directory_v3","result":"hit","shard":"9","took_ms":"13"}
- 2026-09-18T11:55:10Z {"severity":"DEBUG","logger":"search_service","service":"search_service","instance":"search-7","pod":"search-2c04","region":"ap-south-1","trace_id":"tr-5320586","event":"index_query_started","match_key":"ajohansson9059@fastmail.com","attempt":"1"}
- 2026-09-18T11:55:18Z {"severity":"DEBUG","logger":"search_service","service":"search_service","instance":"search-7","pod":"search-2c04","region":"ap-south-1","trace_id":"tr-5320586","event":"connection_acquired","pool":"search_service_replica","wait_ms":"38"}
- 2026-09-18T11:55:20Z {"severity":"WARN","logger":"search_service","service":"search_service","instance":"search-7","pod":"search-2c04","region":"ap-south-1","trace_id":"tr-5320586","event":"dependency_retry","dependency":"search_service_store","attempt":"1","retry_in_ms":"329","reason":"read_timeout"}
- 2026-09-18T11:55:21Z {"severity":"INFO","logger":"search_service","service":"search_service","instance":"search-7","pod":"search-2c04","region":"ap-south-1","trace_id":"tr-5320586","event":"dependency_recovered","attempt":"2","route":"primary"}
- 2026-09-18T11:55:22Z {"severity":"INFO","logger":"search_service","service":"search_service","instance":"search-7","pod":"search-2c04","region":"ap-south-1","trace_id":"tr-5320586","resource_id":"search_209","event":"index_query_completed","index":"customer_directory_v3","result":"hit","shard":"5","took_ms":"26"}
- 2026-09-18T11:55:24Z {"severity":"INFO","logger":"log_router","service":"log_router","instance":"collector-8","event":"export_completed","source_events":"106","auxiliary_events":"4"}

#### evidence_07
### customer_data_snapshot_bundle_20260913.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260913.json
bytes: 12514
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-09-13T08:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-09-11T05:00:00Z', 'data_store': 'search_service', 'collection': 'customer_search_documents', 'records': [{'resource_id': 'search_5349', 'index_name': 'customer_directory_v3', 'document': {'display_name': None, 'email': 'isabela.oliveira.jr@outlook.com', 'customer_reference': None}}]}, {'captured_at': '2026-09-11T08:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': []}, {'captured_at': '2026-09-11T08:00:00Z', 'data_store': 'analytics_platform',…

#### evidence_08
### search_index_diagnostic_20260906.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\search_index_diagnostic_20260906.log
bytes: 8049
line_count: 36
first_20_lines:
- 2026-08-31T07:00:00Z INFO service=search_index_service event=record_lookup seq=1 system="account_service" resource_id="account_8473" record_type="USER_PROFILE" result="FOUND" subject_reference="marek.zielinski@gmail.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=2 system="account_service" resource_id="account_2387" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="cchevalier408794@fastmail.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=3 system="account_service" resource_id="account_2449" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="liam-walker@proton.me"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=4 system="account_service" resource_id="account_3609" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="doyun.lim@outlook.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=5 system="account_service" resource_id="account_4911" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="NILS.L200695@ZOHO.COM"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=6 system="account_service" resource_id="account_6075" record_type="USER_PROFILE" result="FOUND" subject_reference="mei.k952079@outlook.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=7 system="account_service" resource_id="account_8166" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="z.saleh44@gmail.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=8 system="account_service" resource_id="account_8473" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="marek.zielinski@gmail.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=9 system="account_service" resource_id="account_868" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="oladipo.ikenna98@gmail.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=10 system="account_service" resource_id="account_8764" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="yaw-amponsah@gmail.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=11 system="account_service" resource_id="account_9673" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="zmahlangu160178@gmail.com"
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=12 system="analytics_platform" resource_id="analytics_3181" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="zmahlangu160178@gmail.com"
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=13 system="analytics_platform" resource_id="analytics_6499" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="yaw-amponsah@gmail.com"
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=14 system="analytics_platform" resource_id="analytics_8539" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="mei.k952079@outlook.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=15 system="analytics_platform" resource_id="analytics_9500" record_type="ANALYTICS_PROFILE" result="ANONYMIZED" subject_reference=""
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=16 system="backup_service" resource_id="backup_4689" record_type="BACKUP_ARCHIVE" result="ACTIVE" subject_reference="z.saleh44@gmail.com"
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=17 system="integration_service" resource_id="data_flow_2085" record_type="DATA_FLOW" result="ACTIVE" subject_reference="zmahlangu160178@gmail.com"
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=18 system="integration_service" resource_id="data_flow_7535" record_type="DATA_FLOW" result="ACTIVE" subject_reference="doyun.lim@outlook.com"
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=19 system="integration_service" resource_id="data_flow_9927" record_type="DATA_FLOW" result="ACTIVE" subject_reference="NILS.L200695@ZOHO.COM"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=20 system="search_service" resource_id="search_1839" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="yaw-amponsah@gmail.com"
last_20_lines:
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=17 system="integration_service" resource_id="data_flow_2085" record_type="DATA_FLOW" result="ACTIVE" subject_reference="zmahlangu160178@gmail.com"
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=18 system="integration_service" resource_id="data_flow_7535" record_type="DATA_FLOW" result="ACTIVE" subject_reference="doyun.lim@outlook.com"
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=19 system="integration_service" resource_id="data_flow_9927" record_type="DATA_FLOW" result="ACTIVE" subject_reference="NILS.L200695@ZOHO.COM"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=20 system="search_service" resource_id="search_1839" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="yaw-amponsah@gmail.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=21 system="search_service" resource_id="search_5561" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="zmahlangu160178@gmail.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=22 system="search_service" resource_id="search_6302" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="NILS.L200695@ZOHO.COM"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=23 system="search_service" resource_id="search_9156" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="mei.k952079@outlook.com"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=24 system="security_service" resource_id="audit_record_2539" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_87"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=25 system="security_service" resource_id="audit_record_2636" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_81"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=26 system="security_service" resource_id="audit_record_3787" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_82"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=27 system="security_service" resource_id="audit_record_3825" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_86"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=28 system="security_service" resource_id="audit_record_4474" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_85"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=29 system="security_service" resource_id="audit_record_5580" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_84"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=30 system="security_service" resource_id="audit_record_5625" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_90"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=31 system="security_service" resource_id="audit_record_8094" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_83"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=32 system="security_service" resource_id="audit_record_8304" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_89"
- 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=33 system="security_service" resource_id="audit_record_9355" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_88"
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=34 system="support_platform" resource_id="support_266" record_type="SUPPORT_MESSAGE" result="IDENTIFIABLE" subject_reference="mei.k952079@outlook.com"
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=35 system="support_platform" resource_id="support_2967" record_type="SUPPORT_MESSAGE" result="IDENTIFIABLE" subject_reference="oladipo.ikenna98@gmail.com"
- 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=36 system="support_platform" resource_id="support_7460" record_type="SUPPORT_MESSAGE" result="IDENTIFIABLE" subject_reference="zmahlangu160178@gmail.com"

#### evidence_09
### search_index_inspector_20260901.png
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\images\search_index_inspector_20260901.png
bytes: 121101
IMAGE_INSPECTION_ERROR: No module named 'PIL'

#### evidence_10
### customer_data_read_replica_20260827.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_read_replica_20260827.sql
bytes: 23657
CREATE_TABLE: ['CREATE TABLE customer_data_primary', 'CREATE TABLE customer_data_read_replica']
sample_INSERT: ['INSERT INTO "customer_data_primary" VALUES(\'analytics_2777\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_2777","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_3264\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_3264","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_4882\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_4882","user_id":"user_102","email":"kenta.ito@outlook.com","phone":"+81 90 8325 7910","email_hash":"7fe61754d6c2d…']

#### evidence_11
### syslog_archive_us_east_20260824.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\syslog_archive_us_east_20260824.log
bytes: 26532
line_count: 118
first_20_lines:
- 2026-08-22T10:51:11Z <15>1 node-1 account_service tr-4973247 - - level=DEBUG instance="account-2" pod="account-0525" region="eu-west-1" event="profile_lookup_started" lookup_key="nana.b9576@outlook.com" attempt="1"
- 2026-08-22T10:51:15Z <15>1 node-1 account_service tr-4973247 - - level=DEBUG instance="account-2" pod="account-0525" region="eu-west-1" event="connection_acquired" pool="account_service_primary" wait_ms="22"
- 2026-08-22T10:51:17Z <15>1 node-1 account_service tr-4973247 - - level=DEBUG instance="account-2" pod="account-0525" region="eu-west-1" resource_id="account_1785" event="profile_lookup_completed" rows="1" http_status="200" duration_ms="50"
- 2026-08-22T10:51:27Z <15>1 node-3 support_platform tr-6231467 - - level=DEBUG instance="support-3" pod="support-4ae9" region="eu-west-1" event="attachment_scan_started" scan_key="joao-santos@proton.me" attempt="1"
- 2026-08-22T10:51:31Z <15>1 node-3 support_platform tr-6231467 - - level=DEBUG instance="support-3" pod="support-4ae9" region="eu-west-1" event="connection_acquired" pool="support_platform_primary" wait_ms="14"
- 2026-08-22T10:51:33Z <12>1 node-3 support_platform tr-6231467 - - level=WARN instance="support-3" pod="support-4ae9" region="eu-west-1" resource_id="support_9309" event="attachment_pii_scan" matched_value="joao-santos@proton.me" file="delivery_confirmation_94.pdf" detector="direct_identifier"
- 2026-08-22T10:51:45Z <15>1 node-2 account_service tr-9320077 - - level=DEBUG instance="account-3" pod="account-75a1" region="eu-west-1" event="profile_lookup_started" lookup_key="hannah.sullivan@gmail.com" attempt="1"
- 2026-08-22T10:51:50Z <15>1 node-2 account_service tr-9320077 - - level=DEBUG instance="account-3" pod="account-75a1" region="eu-west-1" event="connection_acquired" pool="account_service_primary" wait_ms="5"
- 2026-08-22T10:51:52Z <14>1 node-2 account_service tr-9320077 - - level=INFO instance="account-3" pod="account-75a1" region="eu-west-1" resource_id="account_9580" event="profile_lookup_completed" rows="0" http_status="404" duration_ms="43"
- 2026-08-22T10:51:53Z <15>1 node-6 security_service tr-6248291 - - level=DEBUG instance="security-1" pod="security-6463" region="eu-central-1" event="audit_record_query_started" subject_ref="user_113" attempt="1"
- 2026-08-22T10:51:57Z <15>1 node-6 security_service tr-6248291 - - level=DEBUG instance="security-1" pod="security-6463" region="eu-central-1" event="connection_acquired" pool="security_service_replica" wait_ms="72"
- 2026-08-22T10:51:59Z <12>1 node-6 security_service tr-6248291 - - level=WARN instance="security-1" pod="security-6463" region="eu-central-1" event="dependency_retry" dependency="security_service_store" attempt="1" retry_in_ms="410" reason="read_timeout"
- 2026-08-22T10:52:00Z <14>1 node-6 security_service tr-6248291 - - level=INFO instance="security-1" pod="security-6463" region="eu-central-1" event="dependency_recovered" attempt="2" route="primary"
- 2026-08-22T10:52:01Z <15>1 node-9 account_service tr-3138272 - - level=DEBUG instance="account-7" pod="account-c852" region="us-east-2" event="profile_lookup_started" lookup_key="sami-elsayed@gmail.com" attempt="1"
- 2026-08-22T10:52:01Z <15>1 node-6 security_service tr-6248291 - - level=DEBUG instance="security-1" pod="security-6463" region="eu-central-1" resource_id="audit_record_670" event="audit_record_read_completed" integrity_check="passed" rows="1"
- 2026-08-22T10:52:03Z <15>1 node-9 account_service tr-3138272 - - level=DEBUG instance="account-7" pod="account-c852" region="us-east-2" event="connection_acquired" pool="account_service_primary" wait_ms="6"
- 2026-08-22T10:52:05Z <14>1 node-9 account_service tr-3138272 - - level=INFO instance="account-7" pod="account-c852" region="us-east-2" resource_id="account_6697" event="profile_lookup_completed" rows="0" http_status="404" duration_ms="65"
- 2026-08-22T10:52:08Z <15>1 node-6 search_service tr-7768544 - - level=DEBUG instance="search-1" pod="search-6d08" region="ap-south-1" event="index_query_started" match_key="lee.junseo84@icloud.com" attempt="1"
- 2026-08-22T10:52:17Z <15>1 node-9 account_service tr-1269818 - - level=DEBUG instance="account-3" pod="account-ed52" region="us-east-2" event="profile_lookup_started" lookup_key="rbasu9171@fastmail.com" attempt="1"
- 2026-08-22T10:52:18Z <14>1 node-6 search_service tr-7768544 - - level=INFO instance="search-1" pod="search-6d08" region="ap-south-1" resource_id="search_9556" event="index_query_completed" index="customer_directory_v3" result="hit" shard="4" took_ms="11"
last_20_lines:
- 2026-08-22T10:58:29Z <15>1 node-3 search_service tr-0504758 - - level=DEBUG instance="search-7" pod="search-93bc" region="ap-south-1" event="cache_lookup" result="miss" cache="search_service_lookup_v2"
- 2026-08-22T10:58:30Z <14>1 node-3 search_service tr-0504758 - - level=INFO instance="search-7" pod="search-93bc" region="ap-south-1" resource_id="search_943" event="index_query_completed" index="customer_directory_v3" result="hit" shard="7" took_ms="16"
- 2026-08-22T10:58:37Z <15>1 node-5 security_service tr-1428313 - - level=DEBUG instance="security-5" pod="security-9a97" region="eu-central-1" event="audit_record_query_started" subject_ref="user_120" attempt="1"
- 2026-08-22T10:58:44Z <15>1 node-5 security_service tr-1428313 - - level=DEBUG instance="security-5" pod="security-9a97" region="eu-central-1" event="cache_lookup" result="miss" cache="security_service_lookup_v2"
- 2026-08-22T10:58:45Z <15>1 node-5 security_service tr-1428313 - - level=DEBUG instance="security-5" pod="security-9a97" region="eu-central-1" resource_id="audit_record_9833" event="audit_record_read_completed" integrity_check="passed" rows="1"
- 2026-08-22T10:58:52Z <15>1 node-3 security_service tr-4330226 - - level=DEBUG instance="security-5" pod="security-ed46" region="us-east-2" event="audit_record_query_started" subject_ref="user_115" attempt="1"
- 2026-08-22T10:58:59Z <15>1 node-3 security_service tr-4330226 - - level=DEBUG instance="security-5" pod="security-ed46" region="us-east-2" event="connection_acquired" pool="security_service_replica" wait_ms="24"
- 2026-08-22T10:59:01Z <12>1 node-3 security_service tr-4330226 - - level=WARN instance="security-5" pod="security-ed46" region="us-east-2" event="dependency_retry" dependency="security_service_store" attempt="1" retry_in_ms="198" reason="read_timeout"
- 2026-08-22T10:59:02Z <14>1 node-3 security_service tr-4330226 - - level=INFO instance="security-5" pod="security-ed46" region="us-east-2" event="dependency_recovered" attempt="2" route="primary"
- 2026-08-22T10:59:03Z <15>1 node-3 security_service tr-4330226 - - level=DEBUG instance="security-5" pod="security-ed46" region="us-east-2" resource_id="audit_record_1598" event="audit_record_read_completed" integrity_check="passed" rows="1"
- 2026-08-22T10:59:42Z <14>1 node-3 analytics_platform tr-0659855 - - level=INFO instance="analytics-1" pod="analytics-efd7" region="eu-central-1" resource_id="analytics_8698" event="analytics_profile_read" direct_identifiers="0" email="null" phone="null"
- 2026-08-22T21:04:17Z <15>1 node-5 systemd node-4 - - level=DEBUG instance="node-4" event="timer_tick" unit="logrotate.timer"
- 2026-08-23T07:17:23Z <14>1 node-5 cert_agent node-4 - - level=INFO instance="node-4" event="certificate_checked" expires_in_days="41"
- 2026-08-23T17:30:30Z <12>1 node-5 kernel_monitor node-4 - - level=WARN instance="node-4" event="disk_latency" device="nvme0n1" p95_ms="30"
- 2026-08-24T03:43:36Z <15>1 node-4 dns_cache resolver-3 - - level=DEBUG instance="resolver-3" event="cache_refresh" entries="95"
- 2026-08-24T13:56:32Z <15>1 node-9 search_service tr-1541186 - - level=DEBUG instance="search-7" pod="search-10a4" region="ap-south-1" event="index_query_started" match_key="nicolas.n7090@zoho.com" attempt="1"
- 2026-08-24T13:56:39Z <15>1 node-9 search_service tr-1541186 - - level=DEBUG instance="search-7" pod="search-10a4" region="ap-south-1" event="connection_acquired" pool="search_service_replica" wait_ms="47"
- 2026-08-24T13:56:41Z <12>1 node-9 search_service tr-1541186 - - level=WARN instance="search-7" pod="search-10a4" region="ap-south-1" event="dependency_retry" dependency="search_service_store" attempt="1" retry_in_ms="273" reason="read_timeout"
- 2026-08-24T13:56:42Z <14>1 node-9 search_service tr-1541186 - - level=INFO instance="search-7" pod="search-10a4" region="ap-south-1" event="dependency_recovered" attempt="2" route="primary"
- 2026-08-24T13:56:43Z <14>1 node-9 search_service tr-1541186 - - level=INFO instance="search-7" pod="search-10a4" region="ap-south-1" resource_id="search_3573" event="index_query_completed" index="customer_directory_v3" result="hit" shard="9" took_ms="11"

#### evidence_12
### customer_data_snapshot_bundle_20260819.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260819.json
bytes: 13456
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-08-19T10:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-08-11T10:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_8819', 'customer_reference': 'user_124', 'full_name': 'Yasmine Farouk', 'email': 'yfarouk6685@gmail.com', 'phone': '+971 56 375 0216', 'account_status': 'ACTIVE', 'signup_channel': 'paid_social'}]}, {'captured_at': '2026-08-17T10:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_6673', 'customer_r…

#### evidence_13
### connector_configurations_20260812.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\connector_configurations_20260812.json
bytes: 10107
top_level_type: dict
top_level_keys: ['exported_at', 'origin', 'record_count', 'records']
sample: {'exported_at': '2026-08-12T09:00:00Z', 'origin': 'integration_management_service', 'record_count': 39, 'records': [{'recorded_at': '2026-08-12T09:00:00Z', 'system': 'account_service', 'resource_id': 'account_1084', 'record_type': 'USER_PROFILE', 'result': 'NOT_FOUND', 'subject_reference': 'mateo.alvarez@gmail.com'}, {'recorded_at': '2026-08-12T09:00:00Z', 'system': 'account_service', 'resource_id': 'account_1417', 'record_type': 'USER_PROFILE', 'result': 'NOT_FOUND', 'subject_reference': 'o.morgan56@gmail.com'}, {'recorded_at': '2026-08-12T09:00:00Z', 'system': 'account_service', 'resource_id…

#### evidence_14
### connector_management_console_20260807.png
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\images\connector_management_console_20260807.png
bytes: 130271
IMAGE_INSPECTION_ERROR: No module named 'PIL'

#### evidence_15
### customer_data_read_replica_20260802.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_read_replica_20260802.sql
bytes: 19383
CREATE_TABLE: ['CREATE TABLE customer_data_primary', 'CREATE TABLE customer_data_read_replica']
sample_INSERT: ['INSERT INTO "customer_data_primary" VALUES(\'analytics_2008\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_2008","user_id":"user_159","email":"noah-sullivan@gmail.com","phone":"+1 (646) 555-0159","email_hash":"9f380df558…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_7372\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_7372","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_8425\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_8425","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…']

#### evidence_16
### application_trace_ap_northeast_20260730.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\application_trace_ap_northeast_20260730.log
bytes: 18932
line_count: 93
first_20_lines:
- 2026-07-28T05:51:16Z [DEBUG] [log_router] [collector-9] export_started: instance="collector-9" sources="platform_services" expected_source_events="87"
- 2026-07-28T05:51:18Z [DEBUG] [account_service] [tr-6074163] profile_lookup_started: instance="account-5" pod="account-886d" region="eu-west-1" lookup_key="l.nascimento40@gmail.com" attempt="1"
- 2026-07-28T05:51:20Z [DEBUG] [account_service] [tr-6074163] cache_lookup: instance="account-5" pod="account-886d" region="eu-west-1" result="miss" cache="account_service_lookup_v2"
- 2026-07-28T05:51:21Z [INFO] [account_service] [tr-6074163] profile_lookup_completed: instance="account-5" pod="account-886d" region="eu-west-1" resource_id="account_7947" rows="0" http_status="404" duration_ms="70"
- 2026-07-28T05:51:38Z [DEBUG] [support_platform] [tr-2053433] message_scan_started: instance="support-6" pod="support-5d69" region="eu-west-1" subject_key="menon.arjun@gmail.com" attempt="1"
- 2026-07-28T05:51:40Z [DEBUG] [support_platform] [tr-2053433] cache_lookup: instance="support-6" pod="support-5d69" region="eu-west-1" result="miss" cache="support_platform_lookup_v2"
- 2026-07-28T05:51:41Z [DEBUG] [security_service] [tr-0147748] audit_record_query_started: instance="security-3" pod="security-d09c" region="ap-south-1" subject_ref="user_163" attempt="1"
- 2026-07-28T05:51:41Z [WARN] [support_platform] [tr-2053433] message_pii_scan: instance="support-6" pod="support-5d69" region="eu-west-1" resource_id="support_2322" matched_value="menon.arjun@gmail.com" detector="direct_identifier"
- 2026-07-28T05:51:48Z [DEBUG] [security_service] [tr-0147748] cache_lookup: instance="security-3" pod="security-d09c" region="ap-south-1" result="miss" cache="security_service_lookup_v2"
- 2026-07-28T05:51:49Z [DEBUG] [security_service] [tr-0147748] audit_record_read_completed: instance="security-3" pod="security-d09c" region="ap-south-1" resource_id="audit_record_4964" integrity_check="passed" rows="1"
- 2026-07-28T05:51:51Z [DEBUG] [account_service] [tr-4069320] profile_lookup_completed: instance="account-7" pod="account-6c4a" region="us-east-2" resource_id="account_4289" rows="1" http_status="200" duration_ms="64" correlation_key="erik.h9688@outlook.com"
- 2026-07-28T05:52:42Z [INFO] [account_service] [tr-9859330] profile_lookup_completed: instance="account-4" pod="account-2322" region="us-east-2" resource_id="account_7268" rows="0" http_status="404" duration_ms="55" correlation_key="yuki.k7202@zoho.com"
- 2026-07-28T05:53:09Z [DEBUG] [account_service] [tr-5803951] profile_lookup_started: instance="account-2" pod="account-0e3d" region="eu-west-1" lookup_key="OBI.ADAEZE@ICLOUD.COM" attempt="1"
- 2026-07-28T05:53:15Z [DEBUG] [account_service] [tr-5803951] connection_acquired: instance="account-2" pod="account-0e3d" region="eu-west-1" pool="account_service_replica" wait_ms="19"
- 2026-07-28T05:53:17Z [WARN] [account_service] [tr-5803951] dependency_retry: instance="account-2" pod="account-0e3d" region="eu-west-1" dependency="account_service_store" attempt="1" retry_in_ms="437" reason="read_timeout"
- 2026-07-28T05:53:18Z [INFO] [account_service] [tr-5803951] dependency_recovered: instance="account-2" pod="account-0e3d" region="eu-west-1" attempt="2" route="primary"
- 2026-07-28T05:53:19Z [INFO] [account_service] [tr-5803951] profile_lookup_completed: instance="account-2" pod="account-0e3d" region="eu-west-1" resource_id="account_1837" rows="0" http_status="404" duration_ms="19"
- 2026-07-28T05:53:21Z [DEBUG] [search_service] [tr-0010982] index_query_started: instance="search-6" pod="search-10aa" region="us-east-2" match_key="menon.arjun@gmail.com" attempt="1"
- 2026-07-28T05:53:23Z [DEBUG] [search_service] [tr-0010982] connection_acquired: instance="search-6" pod="search-10aa" region="us-east-2" pool="search_service_primary" wait_ms="19"
- 2026-07-28T05:53:25Z [INFO] [search_service] [tr-0010982] index_query_completed: instance="search-6" pod="search-10aa" region="us-east-2" resource_id="search_7102" index="customer_directory_v3" result="hit" shard="10" took_ms="6"
last_20_lines:
- 2026-07-28T05:58:52Z [DEBUG] [analytics_platform] [tr-2636266] analytics_profile_scan_started: instance="analytics-2" pod="analytics-8c74" region="ap-south-1" lookup_key="n.farouk26@yahoo.com" attempt="1"
- 2026-07-28T05:58:53Z [DEBUG] [account_service] [tr-7989089] profile_lookup_started: instance="account-6" pod="account-6a5f" region="eu-central-1" lookup_key="jihoon.jang@gmail.com" attempt="1"
- 2026-07-28T05:58:59Z [DEBUG] [analytics_platform] [tr-2636266] connection_acquired: instance="analytics-2" pod="analytics-8c74" region="ap-south-1" pool="analytics_platform_replica" wait_ms="41"
- 2026-07-28T05:59:01Z [WARN] [analytics_platform] [tr-2636266] dependency_retry: instance="analytics-2" pod="analytics-8c74" region="ap-south-1" dependency="analytics_platform_store" attempt="1" retry_in_ms="173" reason="read_timeout"
- 2026-07-28T05:59:02Z [INFO] [analytics_platform] [tr-2636266] dependency_recovered: instance="analytics-2" pod="analytics-8c74" region="ap-south-1" attempt="2" route="primary"
- 2026-07-28T05:59:03Z [WARN] [analytics_platform] [tr-2636266] analytics_identity_scan: instance="analytics-2" pod="analytics-8c74" region="ap-south-1" resource_id="analytics_2713" matched_value="n.farouk26@yahoo.com" direct_identifiers="1" detector="direct_identifier"
- 2026-07-28T05:59:04Z [INFO] [account_service] [tr-7989089] profile_lookup_completed: instance="account-6" pod="account-6a5f" region="eu-central-1" resource_id="account_665" rows="0" http_status="404" duration_ms="9"
- 2026-07-28T05:59:06Z [DEBUG] [search_service] [tr-6020958] index_query_started: instance="search-5" pod="search-8ce0" region="ap-south-1" match_key="erik.h9688@outlook.com" attempt="1"
- 2026-07-28T05:59:08Z [DEBUG] [search_service] [tr-6020958] cache_lookup: instance="search-5" pod="search-8ce0" region="ap-south-1" result="miss" cache="search_service_lookup_v2"
- 2026-07-28T05:59:09Z [INFO] [search_service] [tr-6020958] index_query_completed: instance="search-5" pod="search-8ce0" region="ap-south-1" resource_id="search_4509" index="customer_directory_v3" result="hit" shard="9" took_ms="17"
- 2026-07-28T16:03:40Z [ERROR] [webhook_delivery] [notify-2] delivery_abandoned: instance="notify-2" destination="status_page" attempts="3" http_status="503"
- 2026-07-29T02:16:02Z [DEBUG] [thread_pool] [app-2] pool_sample: instance="app-2" active="24" queued="8"
- 2026-07-29T12:28:25Z [INFO] [runtime_config] [app-2] properties_reloaded: instance="app-2" changed="2"
- 2026-07-29T22:40:47Z [WARN] [http_client] [app-2] connection_pool_pressure: instance="app-2" leased="48" max="50"
- 2026-07-30T05:55:30Z [DEBUG] [account_service] [tr-3729118] profile_lookup_started: instance="account-4" pod="account-02ce" region="us-east-2" lookup_key="abena-frimpong@proton.me" attempt="1"
- 2026-07-30T05:55:33Z [DEBUG] [account_service] [tr-3729118] cache_lookup: instance="account-4" pod="account-02ce" region="us-east-2" result="miss" cache="account_service_lookup_v2"
- 2026-07-30T05:55:34Z [DEBUG] [account_service] [tr-3729118] profile_lookup_completed: instance="account-4" pod="account-02ce" region="us-east-2" resource_id="account_5284" rows="1" http_status="200" duration_ms="63"
- 2026-07-30T08:53:06Z [DEBUG] [search_service] [tr-1486544] index_query_started: instance="search-7" pod="search-15b6" region="us-east-2" match_key="jihoon.jang@gmail.com" attempt="1"
- 2026-07-30T08:53:10Z [INFO] [search_service] [tr-1486544] index_query_completed: instance="search-7" pod="search-15b6" region="us-east-2" resource_id="search_3619" index="customer_directory_v3" result="hit" shard="7" took_ms="26"
- 2026-07-30T08:53:12Z [INFO] [log_router] [collector-9] export_completed: instance="collector-9" source_events="87" auxiliary_events="4"

#### evidence_17
### customer_data_snapshot_bundle_20260725.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260725.json
bytes: 15789
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-07-25T15:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-07-23T12:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_8423', 'customer_reference': 'user_175', 'full_name': 'Zofia Popescu', 'email': 'z.popescu54@yahoo.com', 'phone': '+48 618 418 387', 'account_status': 'ACTIVE', 'signup_channel': 'paid_social'}]}, {'captured_at': '2026-07-23T12:00:00Z', 'data_store': 'analytics_platform', 'collection': 'customer_analytics_reports', 'records': [{'resource_id': 'analytics_6000',…

#### evidence_18
### account_history_report_20260718.pdf
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\documents\account_history_report_20260718.pdf
bytes: 65704
PDF_INSPECTION_ERROR: No module named 'pdfplumber'

#### evidence_19
### analytics_profile_view_20260713.png
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\images\analytics_profile_view_20260713.png
bytes: 129362
IMAGE_INSPECTION_ERROR: No module named 'PIL'

#### evidence_20
### customer_data_read_replica_20260708.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_read_replica_20260708.sql
bytes: 23632
CREATE_TABLE: ['CREATE TABLE customer_data_primary', 'CREATE TABLE customer_data_read_replica']
sample_INSERT: ['INSERT INTO "customer_data_primary" VALUES(\'analytics_2463\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_2463","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_3156\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_3156","user_id":"user_207","email":"jieun-yoon@gmail.com","phone":"+82 10 0843 4211","email_hash":"e24e535d67319e…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_9580\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_9580","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…']

#### evidence_21
### operations_stream_eu_central_20260705.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\operations_stream_eu_central_20260705.log
bytes: 26326
line_count: 128
first_20_lines:
- 2026-07-03T07:51:30Z | DEBUG | log_router | collector-5 | export_started | instance="collector-5" sources="platform_services" expected_source_events="122"
- 2026-07-03T07:51:32Z | DEBUG | security_service | tr-5156005 | audit_record_read_completed | instance="security-6" pod="security-7e9b" region="eu-central-1" resource_id="audit_record_4413" integrity_check="passed" rows="1" correlation_key="user_211"
- 2026-07-03T07:51:49Z | DEBUG | analytics_platform | tr-4862866 | analytics_profile_scan_started | instance="analytics-5" pod="analytics-2fcc" region="ap-south-1" lookup_key="analytics_257" attempt="1"
- 2026-07-03T07:51:55Z | DEBUG | analytics_platform | tr-4862866 | connection_acquired | instance="analytics-5" pod="analytics-2fcc" region="ap-south-1" pool="analytics_platform_replica" wait_ms="25"
- 2026-07-03T07:51:57Z | WARN | analytics_platform | tr-4862866 | dependency_retry | instance="analytics-5" pod="analytics-2fcc" region="ap-south-1" dependency="analytics_platform_store" attempt="1" retry_in_ms="377" reason="read_timeout"
- 2026-07-03T07:51:58Z | INFO | analytics_platform | tr-4862866 | dependency_recovered | instance="analytics-5" pod="analytics-2fcc" region="ap-south-1" attempt="2" route="primary"
- 2026-07-03T07:51:59Z | INFO | analytics_platform | tr-4862866 | analytics_profile_read | instance="analytics-5" pod="analytics-2fcc" region="ap-south-1" resource_id="analytics_257" direct_identifiers="0" email="null" phone="null"
- 2026-07-03T07:52:02Z | DEBUG | security_service | tr-4861590 | audit_record_read_completed | instance="security-2" pod="security-fd0a" region="us-east-2" resource_id="audit_record_1718" integrity_check="passed" rows="1" correlation_key="user_213"
- 2026-07-03T07:52:09Z | DEBUG | account_service | tr-9500772 | profile_lookup_started | instance="account-6" pod="account-9a54" region="ap-south-1" lookup_key="mei-tanaka@gmail.com" attempt="1"
- 2026-07-03T07:52:13Z | DEBUG | account_service | tr-9500772 | connection_acquired | instance="account-6" pod="account-9a54" region="ap-south-1" pool="account_service_primary" wait_ms="5"
- 2026-07-03T07:52:15Z | INFO | account_service | tr-9500772 | profile_lookup_completed | instance="account-6" pod="account-9a54" region="ap-south-1" resource_id="account_4512" rows="0" http_status="404" duration_ms="38"
- 2026-07-03T07:52:21Z | DEBUG | account_service | tr-8242693 | profile_lookup_started | instance="account-3" pod="account-7d45" region="eu-west-1" lookup_key="mnovak939594@fastmail.com" attempt="1"
- 2026-07-03T07:52:30Z | DEBUG | account_service | tr-8242693 | cache_lookup | instance="account-3" pod="account-7d45" region="eu-west-1" result="miss" cache="account_service_lookup_v2"
- 2026-07-03T07:52:31Z | INFO | account_service | tr-8242693 | profile_lookup_completed | instance="account-3" pod="account-7d45" region="eu-west-1" resource_id="account_9682" rows="0" http_status="404" duration_ms="62"
- 2026-07-03T07:54:08Z | DEBUG | export_service | tr-4154962 | export_download_check_started | instance="export-7" pod="export-0c18" region="ap-south-1" owner_key="mnovak939594@fastmail.com" attempt="1"
- 2026-07-03T07:54:14Z | DEBUG | export_service | tr-4154962 | connection_acquired | instance="export-7" pod="export-0c18" region="ap-south-1" pool="export_service_primary" wait_ms="4"
- 2026-07-03T07:54:16Z | INFO | export_service | tr-4154962 | export_download_check_completed | instance="export-7" pod="export-0c18" region="ap-south-1" resource_id="export_5351" file="customer_export_5351.zip" available="true"
- 2026-07-03T07:54:41Z | DEBUG | account_service | tr-6641583 | profile_lookup_started | instance="account-1" pod="account-1f0b" region="eu-central-1" lookup_key="nils-lindberg@proton.me" attempt="1"
- 2026-07-03T07:54:46Z | DEBUG | account_service | tr-6641583 | cache_lookup | instance="account-1" pod="account-1f0b" region="eu-central-1" result="miss" cache="account_service_lookup_v2"
- 2026-07-03T07:54:47Z | INFO | account_service | tr-6641583 | profile_lookup_completed | instance="account-1" pod="account-1f0b" region="eu-central-1" resource_id="account_1956" rows="0" http_status="404" duration_ms="55"
last_20_lines:
- 2026-07-03T07:59:21Z | INFO | integration_service | tr-2328046 | dependency_recovered | instance="integration-7" pod="integration-fcf4" region="ap-south-1" attempt="2" route="primary"
- 2026-07-03T07:59:22Z | INFO | integration_service | tr-2328046 | connector_config_loaded | instance="integration-7" pod="integration-fcf4" region="ap-south-1" resource_id="data_flow_5279" enabled="false" scheduler_registered="false"
- 2026-07-03T07:59:24Z | DEBUG | account_service | tr-8364191 | profile_lookup_started | instance="account-7" pod="account-b193" region="eu-central-1" lookup_key="bernard.chloe@icloud.com" attempt="1"
- 2026-07-03T07:59:30Z | DEBUG | account_service | tr-8364191 | connection_acquired | instance="account-7" pod="account-b193" region="eu-central-1" pool="account_service_replica" wait_ms="67"
- 2026-07-03T07:59:32Z | WARN | account_service | tr-8364191 | dependency_retry | instance="account-7" pod="account-b193" region="eu-central-1" dependency="account_service_store" attempt="1" retry_in_ms="312" reason="read_timeout"
- 2026-07-03T07:59:33Z | INFO | account_service | tr-8364191 | dependency_recovered | instance="account-7" pod="account-b193" region="eu-central-1" attempt="2" route="primary"
- 2026-07-03T07:59:34Z | INFO | account_service | tr-8364191 | profile_lookup_completed | instance="account-7" pod="account-b193" region="eu-central-1" resource_id="account_4752" rows="0" http_status="404" duration_ms="29"
- 2026-07-03T07:59:38Z | DEBUG | analytics_platform | tr-7943893 | analytics_profile_scan_started | instance="analytics-5" pod="analytics-962f" region="eu-central-1" lookup_key="mnovak939594@fastmail.com" attempt="1"
- 2026-07-03T07:59:40Z | DEBUG | analytics_platform | tr-7943893 | cache_lookup | instance="analytics-5" pod="analytics-962f" region="eu-central-1" result="miss" cache="analytics_platform_lookup_v2"
- 2026-07-03T07:59:41Z | WARN | analytics_platform | tr-7943893 | analytics_identity_scan | instance="analytics-5" pod="analytics-962f" region="eu-central-1" resource_id="analytics_4527" matched_value="mnovak939594@fastmail.com" direct_identifiers="1" detector="direct_identifier"
- 2026-07-03T17:28:06Z | INFO | secret_agent | vault-3 | lease_extended | instance="vault-3" ttl_seconds="1222"
- 2026-07-04T03:04:41Z | ERROR | webhook_delivery | notify-7 | delivery_abandoned | instance="notify-7" destination="status_page" attempts="4" http_status="503"
- 2026-07-04T12:41:15Z | INFO | scheduler | sched-3 | lease_renewed | instance="sched-3" lease="maintenance-1"
- 2026-07-04T22:17:50Z | DEBUG | checkpoint_writer | worker-1 | checkpoint_saved | instance="worker-1" offset="84014"
- 2026-07-05T07:54:16Z | DEBUG | account_service | tr-6851041 | profile_lookup_started | instance="account-3" pod="account-1fd5" region="eu-west-1" lookup_key="nils-lindberg@proton.me" attempt="1"
- 2026-07-05T07:54:21Z | DEBUG | account_service | tr-6851041 | connection_acquired | instance="account-3" pod="account-1fd5" region="eu-west-1" pool="account_service_replica" wait_ms="16"
- 2026-07-05T07:54:23Z | WARN | account_service | tr-6851041 | dependency_retry | instance="account-3" pod="account-1fd5" region="eu-west-1" dependency="account_service_store" attempt="1" retry_in_ms="176" reason="read_timeout"
- 2026-07-05T07:54:24Z | INFO | account_service | tr-6851041 | dependency_recovered | instance="account-3" pod="account-1fd5" region="eu-west-1" attempt="2" route="primary"
- 2026-07-05T07:54:25Z | DEBUG | account_service | tr-6851041 | profile_lookup_completed | instance="account-3" pod="account-1fd5" region="eu-west-1" resource_id="account_1956" rows="1" http_status="200" duration_ms="55"
- 2026-07-05T07:54:27Z | INFO | log_router | collector-5 | export_completed | instance="collector-5" source_events="122" auxiliary_events="4" dropped_auxiliary="1"

#### evidence_22
### customer_data_snapshot_bundle_20260630.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260630.json
bytes: 24337
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-06-30T07:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-06-28T07:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_5479', 'customer_reference': 'user_221', 'full_name': 'Thiago Souza', 'email': 'thiago.s4828@outlook.com', 'phone': '+55 51 92710-4321', 'account_status': 'ACTIVE', 'signup_channel': 'paid_social'}]}, {'captured_at': '2026-06-28T07:00:00Z', 'data_store': 'analytics_platform', 'collection': 'customer_analytics_reports', 'records': [{'resource_id': 'analytics_81…

#### evidence_23
### customer_export_console_20260618.png
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\images\customer_export_console_20260618.png
bytes: 134597
IMAGE_INSPECTION_ERROR: No module named 'PIL'

#### evidence_24
### customer_data_read_replica_20260613.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_read_replica_20260613.sql
bytes: 19683
CREATE_TABLE: ['CREATE TABLE customer_data_primary', 'CREATE TABLE customer_data_read_replica']
sample_INSERT: ['INSERT INTO "customer_data_primary" VALUES(\'analytics_2977\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_2977","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_5053\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_5053","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_6136\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_6136","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…']

#### evidence_25
### cloud_runtime_export_us_west_20260608.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\cloud_runtime_export_us_west_20260608.log
bytes: 32394
line_count: 128
first_20_lines:
- 2026-06-08T06:52:07Z requestId=collector-1 level=DEBUG function=log_router message="instance=\"collector-1\" event=\"export_started\" sources=\"platform_services\" expected_source_events=\"123\""
- 2026-06-08T06:52:09Z requestId=tr-1108860 level=INFO function=search_service message="instance=\"search-3\" pod=\"search-0696\" region=\"us-east-2\" resource_id=\"search_021\" event=\"index_query_completed\" index=\"customer_directory_v3\" result=\"hit\" shard=\"9\" took_ms=\"24\" correlation_key=\"mrios9507.jr@fastmail.com\""
- 2026-06-08T07:29:24Z requestId=resolver-3 level=DEBUG function=dns_cache message="instance=\"resolver-3\" event=\"cache_refresh\" entries=\"110\""
- 2026-06-08T08:06:40Z requestId=vault-4 level=INFO function=secret_agent message="instance=\"vault-4\" event=\"lease_extended\" ttl_seconds=\"1227\""
- 2026-06-08T08:43:56Z requestId=notify-4 level=ERROR function=webhook_delivery message="instance=\"notify-4\" event=\"delivery_abandoned\" destination=\"status_page\" attempts=\"5\" http_status=\"503\""
- 2026-06-08T09:21:12Z requestId=ext-3 level=DEBUG function=lambda_extension message="instance=\"ext-3\" event=\"telemetry_flushed\" records=\"91\""
- 2026-06-08T09:50:56Z requestId=tr-0305307 level=DEBUG function=support_platform message="instance=\"support-5\" pod=\"support-6b03\" region=\"eu-central-1\" event=\"message_scan_started\" subject_key=\"aarav-singh@proton.me\" attempt=\"1\""
- 2026-06-08T09:51:02Z requestId=tr-0305307 level=DEBUG function=support_platform message="instance=\"support-5\" pod=\"support-6b03\" region=\"eu-central-1\" event=\"connection_acquired\" pool=\"support_platform_primary\" wait_ms=\"7\""
- 2026-06-08T09:51:04Z requestId=tr-0305307 level=WARN function=support_platform message="instance=\"support-5\" pod=\"support-6b03\" region=\"eu-central-1\" resource_id=\"support_2498\" event=\"message_pii_scan\" matched_value=\"aarav-singh@proton.me\" detector=\"direct_identifier\""
- 2026-06-08T09:51:12Z requestId=tr-0315808 level=DEBUG function=integration_service message="instance=\"integration-2\" pod=\"integration-3314\" region=\"ap-south-1\" event=\"connector_config_read_started\" subject_key=\"thabo.masuku@outlook.com\" attempt=\"1\""
- 2026-06-08T09:51:17Z requestId=tr-0315808 level=DEBUG function=integration_service message="instance=\"integration-2\" pod=\"integration-3314\" region=\"ap-south-1\" event=\"cache_lookup\" result=\"miss\" cache=\"integration_service_lookup_v2\""
- 2026-06-08T09:51:18Z requestId=tr-0315808 level=WARN function=integration_service message="instance=\"integration-2\" pod=\"integration-3314\" region=\"ap-south-1\" resource_id=\"data_flow_2010\" event=\"connector_heartbeat\" enabled=\"true\" scheduler_registered=\"true\" last_run=\"success\""
- 2026-06-08T09:51:26Z requestId=tr-7753246 level=DEBUG function=account_service message="instance=\"account-4\" pod=\"account-7efc\" region=\"ap-south-1\" event=\"profile_lookup_started\" lookup_key=\"cchukwu7021@gmail.com\" attempt=\"1\""
- 2026-06-08T09:51:31Z requestId=tr-7753246 level=DEBUG function=account_service message="instance=\"account-4\" pod=\"account-7efc\" region=\"ap-south-1\" event=\"connection_acquired\" pool=\"account_service_replica\" wait_ms=\"12\""
- 2026-06-08T09:51:33Z requestId=tr-7753246 level=WARN function=account_service message="instance=\"account-4\" pod=\"account-7efc\" region=\"ap-south-1\" event=\"dependency_retry\" dependency=\"account_service_store\" attempt=\"1\" retry_in_ms=\"271\" reason=\"read_timeout\""
- 2026-06-08T09:51:34Z requestId=tr-7753246 level=INFO function=account_service message="instance=\"account-4\" pod=\"account-7efc\" region=\"ap-south-1\" event=\"dependency_recovered\" attempt=\"2\" route=\"primary\""
- 2026-06-08T09:51:35Z requestId=tr-7753246 level=INFO function=account_service message="instance=\"account-4\" pod=\"account-7efc\" region=\"ap-south-1\" resource_id=\"account_4331\" event=\"profile_lookup_completed\" rows=\"0\" http_status=\"404\" duration_ms=\"23\""
- 2026-06-08T09:51:38Z requestId=tr-0310343 level=DEBUG function=support_platform message="instance=\"support-5\" pod=\"support-a913\" region=\"eu-central-1\" event=\"message_scan_started\" subject_key=\"user_262\" attempt=\"1\""
- 2026-06-08T09:51:39Z requestId=tr-0155306 level=DEBUG function=account_service message="instance=\"account-5\" pod=\"account-11c8\" region=\"ap-south-1\" event=\"profile_lookup_started\" lookup_key=\"kwame.g4940@outlook.com\" attempt=\"1\""
- 2026-06-08T09:51:40Z requestId=tr-8487476 level=DEBUG function=account_service message="instance=\"account-5\" pod=\"account-c3a4\" region=\"ap-south-1\" event=\"profile_lookup_started\" lookup_key=\"j.nystrom64@gmail.com\" attempt=\"1\""
last_20_lines:
- 2026-06-08T09:56:18Z requestId=tr-7430685 level=WARN function=integration_service message="instance=\"integration-1\" pod=\"integration-b363\" region=\"eu-central-1\" resource_id=\"data_flow_8277\" event=\"connector_heartbeat\" enabled=\"true\" scheduler_registered=\"true\" last_run=\"success\" correlation_key=\"hugo.fontaine@gmail.com\""
- 2026-06-08T09:56:19Z requestId=tr-5189472 level=DEBUG function=search_service message="instance=\"search-6\" pod=\"search-4106\" region=\"us-east-2\" event=\"index_query_started\" match_key=\"thabo.masuku@outlook.com\" attempt=\"1\""
- 2026-06-08T09:56:25Z requestId=tr-5189472 level=DEBUG function=search_service message="instance=\"search-6\" pod=\"search-4106\" region=\"us-east-2\" event=\"connection_acquired\" pool=\"search_service_primary\" wait_ms=\"12\""
- 2026-06-08T09:56:27Z requestId=tr-5189472 level=INFO function=search_service message="instance=\"search-6\" pod=\"search-4106\" region=\"us-east-2\" resource_id=\"search_3875\" event=\"index_query_completed\" index=\"customer_directory_v3\" result=\"hit\" shard=\"11\" took_ms=\"3\""
- 2026-06-08T09:57:02Z requestId=tr-1085563 level=DEBUG function=security_service message="instance=\"security-5\" pod=\"security-afab\" region=\"eu-central-1\" event=\"audit_record_query_started\" subject_ref=\"user_270\" attempt=\"1\""
- 2026-06-08T09:57:05Z requestId=tr-4697248 level=DEBUG function=support_platform message="instance=\"support-1\" pod=\"support-67b6\" region=\"us-east-2\" event=\"message_scan_started\" subject_key=\"cchukwu7021@gmail.com\" attempt=\"1\""
- 2026-06-08T09:57:06Z requestId=tr-1085563 level=DEBUG function=security_service message="instance=\"security-5\" pod=\"security-afab\" region=\"eu-central-1\" event=\"cache_lookup\" result=\"miss\" cache=\"security_service_lookup_v2\""
- 2026-06-08T09:57:07Z requestId=tr-1085563 level=DEBUG function=security_service message="instance=\"security-5\" pod=\"security-afab\" region=\"eu-central-1\" resource_id=\"audit_record_4646\" event=\"audit_record_read_completed\" integrity_check=\"passed\" rows=\"1\""
- 2026-06-08T09:57:10Z requestId=tr-4697248 level=DEBUG function=support_platform message="instance=\"support-1\" pod=\"support-67b6\" region=\"us-east-2\" event=\"cache_lookup\" result=\"miss\" cache=\"support_platform_lookup_v2\""
- 2026-06-08T09:57:11Z requestId=tr-4697248 level=WARN function=support_platform message="instance=\"support-1\" pod=\"support-67b6\" region=\"us-east-2\" resource_id=\"support_7707\" event=\"message_pii_scan\" matched_value=\"cchukwu7021@gmail.com\" detector=\"direct_identifier\""
- 2026-06-08T09:57:14Z requestId=tr-4787100 level=DEBUG function=security_service message="instance=\"security-5\" pod=\"security-fdd8\" region=\"ap-south-1\" resource_id=\"audit_record_5206\" event=\"audit_record_read_completed\" integrity_check=\"passed\" rows=\"1\" correlation_key=\"user_268\""
- 2026-06-08T09:57:17Z requestId=tr-2340805 level=INFO function=analytics_platform message="instance=\"analytics-1\" pod=\"analytics-2ce3\" region=\"eu-central-1\" resource_id=\"analytics_3793\" event=\"analytics_profile_read\" direct_identifiers=\"0\" email=\"null\" phone=\"null\""
- 2026-06-08T09:57:22Z requestId=tr-4557555 level=DEBUG function=security_service message="instance=\"security-6\" pod=\"security-e0b5\" region=\"eu-west-1\" resource_id=\"audit_record_6863\" event=\"audit_record_read_completed\" integrity_check=\"passed\" rows=\"1\" correlation_key=\"user_261\""
- 2026-06-08T09:57:31Z requestId=tr-4141476 level=DEBUG function=security_service message="instance=\"security-2\" pod=\"security-7ef8\" region=\"ap-south-1\" event=\"audit_record_query_started\" subject_ref=\"user_269\" attempt=\"1\""
- 2026-06-08T09:57:36Z requestId=tr-4141476 level=DEBUG function=security_service message="instance=\"security-2\" pod=\"security-7ef8\" region=\"ap-south-1\" event=\"connection_acquired\" pool=\"security_service_replica\" wait_ms=\"57\""
- 2026-06-08T09:57:38Z requestId=tr-4141476 level=WARN function=security_service message="instance=\"security-2\" pod=\"security-7ef8\" region=\"ap-south-1\" event=\"dependency_retry\" dependency=\"security_service_store\" attempt=\"1\" retry_in_ms=\"386\" reason=\"read_timeout\""
- 2026-06-08T09:57:39Z requestId=tr-4141476 level=INFO function=security_service message="instance=\"security-2\" pod=\"security-7ef8\" region=\"ap-south-1\" event=\"dependency_recovered\" attempt=\"2\" route=\"primary\""
- 2026-06-08T09:57:40Z requestId=tr-4141476 level=DEBUG function=security_service message="instance=\"security-2\" pod=\"security-7ef8\" region=\"ap-south-1\" resource_id=\"audit_record_2546\" event=\"audit_record_read_completed\" integrity_check=\"passed\" rows=\"1\""
- 2026-06-08T09:58:19Z requestId=tr-5705359 level=DEBUG function=analytics_platform message="instance=\"analytics-7\" pod=\"analytics-0f79\" region=\"eu-west-1\" event=\"analytics_profile_scan_started\" lookup_key=\"analytics_1851\" attempt=\"1\""
- 2026-06-08T09:58:28Z requestId=tr-5705359 level=INFO function=analytics_platform message="instance=\"analytics-7\" pod=\"analytics-0f79\" region=\"eu-west-1\" resource_id=\"analytics_1851\" event=\"analytics_profile_read\" direct_identifiers=\"0\" email=\"null\" phone=\"null\""

#### evidence_26
### customer_data_snapshot_bundle_20260605.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260605.json
bytes: 14243
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-06-05T12:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-06-03T09:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_8689', 'customer_reference': 'user_271', 'full_name': 'Haruka Mori', 'email': 'h.mori78@yahoo.com', 'phone': '+81 90 9155 7228', 'account_status': 'ACTIVE', 'signup_channel': 'mobile_app'}]}, {'captured_at': '2026-06-03T09:00:00Z', 'data_store': 'analytics_platform', 'collection': 'customer_analytics_reports', 'records': [{'resource_id': 'analytics_4051', 'use…

#### evidence_27
### legal_retention_register_20260529.pdf
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\documents\legal_retention_register_20260529.pdf
bytes: 65857
PDF_INSPECTION_ERROR: No module named 'pdfplumber'

#### evidence_28
### support_ticket_console_20260524.png
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\images\support_ticket_console_20260524.png
bytes: 135008
IMAGE_INSPECTION_ERROR: No module named 'PIL'

#### evidence_29
### customer_data_regional_replicas_20260519.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_regional_replicas_20260519.sql
bytes: 32282
CREATE_TABLE: ['CREATE TABLE customer_data_primary', 'CREATE TABLE customer_data_replica_ap_south', 'CREATE TABLE customer_data_replica_eu_west']
sample_INSERT: ['INSERT INTO "customer_data_primary" VALUES(\'analytics_096\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_096","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"sess…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_3678\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_3678","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_9285\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_9285","user_id":"user_303","email":"louis-chevalier@gmail.com","phone":"+33 6 63 02 04 88","email_hash":"1c9fc93d…']

#### evidence_30
### service_events_sa_east_20260516.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\service_events_sa_east_20260516.log
bytes: 23591
line_count: 110
first_20_lines:
- 2026-05-14T11:51:20Z level=INFO service=account_service instance=account-4 pod=account-e506 region=us-east-2 trace_id=tr-4210650 resource_id=account_1530 event=profile_lookup_completed rows=0 http_status=404 duration_ms=44 correlation_key="mrousseau7133@gmail.com"
- 2026-05-14T11:51:23Z level=DEBUG service=search_service instance=search-3 pod=search-eb12 region=us-east-2 trace_id=tr-0398528 event=index_query_started match_key="ethan-morgan@gmail.com" attempt=1
- 2026-05-14T11:51:32Z level=DEBUG service=search_service instance=search-3 pod=search-eb12 region=us-east-2 trace_id=tr-0398528 event=cache_lookup result=miss cache=search_service_lookup_v2
- 2026-05-14T11:51:33Z level=INFO service=search_service instance=search-3 pod=search-eb12 region=us-east-2 trace_id=tr-0398528 resource_id=search_8665 event=index_query_completed index=customer_directory_v3 result=hit shard=1 took_ms=19
- 2026-05-14T11:52:29Z level=DEBUG service=account_service instance=account-2 pod=account-0a19 region=eu-west-1 trace_id=tr-1265803 event=profile_lookup_started lookup_key="k.nasser9089@yahoo.com" attempt=1
- 2026-05-14T11:52:37Z level=DEBUG service=account_service instance=account-2 pod=account-0a19 region=eu-west-1 trace_id=tr-1265803 event=cache_lookup result=miss cache=account_service_lookup_v2
- 2026-05-14T11:52:38Z level=INFO service=account_service instance=account-2 pod=account-0a19 region=eu-west-1 trace_id=tr-1265803 resource_id=account_3525 event=profile_lookup_completed rows=0 http_status=404 duration_ms=47
- 2026-05-14T11:52:46Z level=DEBUG service=account_service instance=account-2 pod=account-398e region=us-east-2 trace_id=tr-5612994 event=profile_lookup_started lookup_key="andrei.horvat@outlook.com" attempt=1
- 2026-05-14T11:52:48Z level=DEBUG service=analytics_platform instance=analytics-4 pod=analytics-8294 region=ap-south-1 trace_id=tr-3425002 event=analytics_profile_scan_started lookup_key="analytics_2601" attempt=1
- 2026-05-14T11:52:49Z level=DEBUG service=analytics_platform instance=analytics-4 pod=analytics-8294 region=ap-south-1 trace_id=tr-3425002 event=connection_acquired pool=analytics_platform_primary wait_ms=26
- 2026-05-14T11:52:51Z level=INFO service=analytics_platform instance=analytics-4 pod=analytics-8294 region=ap-south-1 trace_id=tr-3425002 resource_id=analytics_2601 event=analytics_profile_read direct_identifiers=0 email=null phone=null
- 2026-05-14T11:52:56Z level=INFO service=account_service instance=account-2 pod=account-398e region=us-east-2 trace_id=tr-5612994 resource_id=account_9178 event=profile_lookup_completed rows=0 http_status=404 duration_ms=56
- 2026-05-14T11:53:08Z level=DEBUG service=analytics_platform instance=analytics-5 pod=analytics-7237 region=eu-central-1 trace_id=tr-7469153 event=analytics_profile_scan_started lookup_key="analytics_4229" attempt=1
- 2026-05-14T11:53:18Z level=DEBUG service=analytics_platform instance=analytics-5 pod=analytics-7237 region=eu-central-1 trace_id=tr-7469153 event=cache_lookup result=miss cache=analytics_platform_lookup_v2
- 2026-05-14T11:53:19Z level=INFO service=analytics_platform instance=analytics-5 pod=analytics-7237 region=eu-central-1 trace_id=tr-7469153 resource_id=analytics_4229 event=analytics_profile_read direct_identifiers=0 email=null phone=null
- 2026-05-14T11:53:28Z level=DEBUG service=search_service instance=search-6 pod=search-524b region=eu-central-1 trace_id=tr-1111863 event=index_query_started match_key="andrei.horvat@outlook.com" attempt=1
- 2026-05-14T11:53:36Z level=DEBUG service=search_service instance=search-6 pod=search-524b region=eu-central-1 trace_id=tr-1111863 event=cache_lookup result=miss cache=search_service_lookup_v2
- 2026-05-14T11:53:37Z level=INFO service=search_service instance=search-6 pod=search-524b region=eu-central-1 trace_id=tr-1111863 resource_id=search_2256 event=index_query_completed index=customer_directory_v3 result=hit shard=0 took_ms=27
- 2026-05-14T11:53:41Z level=DEBUG service=security_service instance=security-3 pod=security-76c2 region=us-east-2 trace_id=tr-3028312 event=audit_record_query_started subject_ref="user_312" attempt=1
- 2026-05-14T11:53:42Z level=DEBUG service=security_service instance=security-3 pod=security-76c2 region=us-east-2 trace_id=tr-3028312 event=connection_acquired pool=security_service_primary wait_ms=26
last_20_lines:
- 2026-05-14T11:58:44Z level=WARN service=support_platform instance=support-6 pod=support-88ad region=eu-west-1 trace_id=tr-7037563 resource_id=support_4439 event=message_pii_scan matched_value="ethan-morgan@gmail.com" detector=direct_identifier
- 2026-05-14T11:58:45Z level=INFO service=account_service instance=account-6 pod=account-3740 region=ap-south-1 trace_id=tr-9048368 resource_id=account_2088 event=profile_lookup_completed rows=0 http_status=404 duration_ms=21
- 2026-05-14T11:58:46Z level=DEBUG service=security_service instance=security-6 pod=security-2e4a region=us-east-2 trace_id=tr-0719928 event=audit_record_query_started subject_ref="user_317" attempt=1
- 2026-05-14T11:58:48Z level=DEBUG service=security_service instance=security-1 pod=security-5f0b region=eu-central-1 trace_id=tr-9898865 resource_id=audit_record_2407 event=audit_record_read_completed integrity_check=passed rows=1 correlation_key="user_313"
- 2026-05-14T11:58:50Z level=DEBUG service=security_service instance=security-5 pod=security-81ad region=eu-west-1 trace_id=tr-0431165 resource_id=audit_record_6170 event=audit_record_read_completed integrity_check=passed rows=1 correlation_key="user_315"
- 2026-05-14T11:58:50Z level=DEBUG service=security_service instance=security-6 pod=security-2e4a region=us-east-2 trace_id=tr-0719928 event=cache_lookup result=miss cache=security_service_lookup_v2
- 2026-05-14T11:58:51Z level=DEBUG service=security_service instance=security-6 pod=security-2e4a region=us-east-2 trace_id=tr-0719928 resource_id=audit_record_7337 event=audit_record_read_completed integrity_check=passed rows=1
- 2026-05-14T11:59:32Z level=DEBUG service=security_service instance=security-7 pod=security-6fcd region=eu-west-1 trace_id=tr-5092853 event=audit_record_query_started subject_ref="user_314" attempt=1
- 2026-05-14T11:59:36Z level=DEBUG service=security_service instance=security-7 pod=security-6fcd region=eu-west-1 trace_id=tr-5092853 event=cache_lookup result=miss cache=security_service_lookup_v2
- 2026-05-14T11:59:37Z level=DEBUG service=security_service instance=security-7 pod=security-6fcd region=eu-west-1 trace_id=tr-5092853 resource_id=audit_record_4286 event=audit_record_read_completed integrity_check=passed rows=1
- 2026-05-14T21:28:44Z level=WARN service=queue_consumer instance=worker-9 event=consumer_lag topic=notification_events partition=0 lag=63
- 2026-05-15T07:06:09Z level=DEBUG service=dns_cache instance=resolver-3 event=cache_refresh entries=115
- 2026-05-15T16:43:33Z level=INFO service=secret_agent instance=vault-1 event=lease_extended ttl_seconds=1232
- 2026-05-16T02:20:58Z level=ERROR service=webhook_delivery instance=notify-1 event=delivery_abandoned destination=status_page attempts=2 http_status=503
- 2026-05-16T11:58:12Z level=DEBUG service=account_service instance=account-1 pod=account-380a region=us-east-2 trace_id=tr-9257826 event=profile_lookup_started lookup_key="lars.e5052@outlook.com" attempt=1
- 2026-05-16T11:58:19Z level=DEBUG service=account_service instance=account-1 pod=account-380a region=us-east-2 trace_id=tr-9257826 event=connection_acquired pool=account_service_replica wait_ms=26
- 2026-05-16T11:58:21Z level=WARN service=account_service instance=account-1 pod=account-380a region=us-east-2 trace_id=tr-9257826 event=dependency_retry dependency=account_service_store attempt=1 retry_in_ms=308 reason=read_timeout
- 2026-05-16T11:58:22Z level=INFO service=account_service instance=account-1 pod=account-380a region=us-east-2 trace_id=tr-9257826 event=dependency_recovered attempt=2 route=primary
- 2026-05-16T11:58:23Z level=DEBUG service=account_service instance=account-1 pod=account-380a region=us-east-2 trace_id=tr-9257826 resource_id=account_2088 event=profile_lookup_completed rows=1 http_status=200 duration_ms=21
- 2026-05-16T11:58:25Z level=INFO service=log_router instance=collector-6 event=export_completed source_events=105 auxiliary_events=4 dropped_auxiliary=2

#### evidence_31
### customer_data_snapshot_bundle_20260511.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260511.json
bytes: 25927
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-05-11T11:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-05-03T11:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_3785', 'customer_reference': 'user_324', 'full_name': 'Hyun-woo Kang', 'email': 'HYUNWOO.KANG94@GMAIL.COM', 'phone': '+82 10 2411 4559', 'account_status': 'ACTIVE', 'signup_channel': 'mobile_app'}]}, {'captured_at': '2026-05-09T11:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': []}, {'captured_at': '2026-05-09T11:00:00Z'…

#### evidence_32
### backup_restore_console_20260429.png
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\images\backup_restore_console_20260429.png
bytes: 155587
IMAGE_INSPECTION_ERROR: No module named 'PIL'

#### evidence_33
### customer_data_regional_replicas_20260424.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_regional_replicas_20260424.sql
bytes: 36128
CREATE_TABLE: ['CREATE TABLE customer_data_primary', 'CREATE TABLE customer_data_replica_ap_south', 'CREATE TABLE customer_data_replica_eu_west']
sample_INSERT: ['INSERT INTO "customer_data_primary" VALUES(\'analytics_4273\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_4273","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_439\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_439","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"sess…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_5413\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_5413","user_id":"user_354","email":"sophie.hughes@outlook.com","phone":"+44 7700 900354","email_hash":"d429ccf2b3…']

#### evidence_34
### structured_service_events_ca_central_20260419.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\structured_service_events_ca_central_20260419.log
bytes: 38796
line_count: 136
first_20_lines:
- 2026-04-19T06:51:11Z {"severity":"DEBUG","logger":"log_router","service":"log_router","instance":"collector-2","event":"export_started","sources":"platform_services","expected_source_events":"130"}
- 2026-04-19T06:51:13Z {"severity":"DEBUG","logger":"search_service","service":"search_service","instance":"search-6","pod":"search-56f3","region":"eu-central-1","trace_id":"tr-7722221","event":"index_query_started","match_key":"dubois.ines94@icloud.com","attempt":"1"}
- 2026-04-19T06:51:17Z {"severity":"DEBUG","logger":"search_service","service":"search_service","instance":"search-6","pod":"search-56f3","region":"eu-central-1","trace_id":"tr-7722221","event":"connection_acquired","pool":"search_service_replica","wait_ms":"44"}
- 2026-04-19T06:51:19Z {"severity":"WARN","logger":"search_service","service":"search_service","instance":"search-6","pod":"search-56f3","region":"eu-central-1","trace_id":"tr-7722221","event":"dependency_retry","dependency":"search_service_store","attempt":"1","retry_in_ms":"365","reason":"read_timeout"}
- 2026-04-19T06:51:20Z {"severity":"INFO","logger":"search_service","service":"search_service","instance":"search-6","pod":"search-56f3","region":"eu-central-1","trace_id":"tr-7722221","event":"dependency_recovered","attempt":"2","route":"primary"}
- 2026-04-19T06:51:21Z {"severity":"INFO","logger":"search_service","service":"search_service","instance":"search-6","pod":"search-56f3","region":"eu-central-1","trace_id":"tr-7722221","resource_id":"search_9365","event":"index_query_completed","index":"customer_directory_v3","result":"hit","shard":"5","took_ms":"6"}
- 2026-04-19T06:51:21Z {"severity":"WARN","logger":"support_platform","service":"support_platform","instance":"support-5","pod":"support-30fd","region":"eu-west-1","trace_id":"tr-6093335","resource_id":"support_5609","event":"message_pii_scan","matched_value":"lpereira7245@gmail.com","detector":"direct_identifier"}
- 2026-04-19T06:51:30Z {"severity":"DEBUG","logger":"backup_service","service":"backup_service","instance":"backup-5","pod":"backup-1978","region":"ap-south-1","trace_id":"tr-7750694","event":"restore_policy_check_started","subject_key":"m.khumalo88@gmail.com","attempt":"1"}
- 2026-04-19T06:51:30Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-5","pod":"security-498b","region":"eu-central-1","trace_id":"tr-6856923","event":"audit_record_query_started","subject_ref":"user_363","attempt":"1"}
- 2026-04-19T06:51:31Z {"severity":"DEBUG","logger":"analytics_platform","service":"analytics_platform","instance":"analytics-5","pod":"analytics-5301","region":"eu-west-1","trace_id":"tr-5378983","event":"analytics_profile_scan_started","lookup_key":"haeun-jung@gmail.com","attempt":"1"}
- 2026-04-19T06:51:34Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-5","pod":"security-498b","region":"eu-central-1","trace_id":"tr-6856923","event":"cache_lookup","result":"miss","cache":"security_service_lookup_v2"}
- 2026-04-19T06:51:35Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-5","pod":"security-498b","region":"eu-central-1","trace_id":"tr-6856923","resource_id":"audit_record_5798","event":"audit_record_read_completed","integrity_check":"passed","rows":"1"}
- 2026-04-19T06:51:40Z {"severity":"DEBUG","logger":"analytics_platform","service":"analytics_platform","instance":"analytics-5","pod":"analytics-5301","region":"eu-west-1","trace_id":"tr-5378983","event":"cache_lookup","result":"miss","cache":"analytics_platform_lookup_v2"}
- 2026-04-19T06:51:41Z {"severity":"WARN","logger":"analytics_platform","service":"analytics_platform","instance":"analytics-5","pod":"analytics-5301","region":"eu-west-1","trace_id":"tr-5378983","resource_id":"analytics_547","event":"analytics_identity_scan","matched_value":"haeun-jung@gmail.com","direct_identifiers":"1","detector":"direct_identifier"}
- 2026-04-19T06:51:41Z {"severity":"ERROR","logger":"backup_service","service":"backup_service","instance":"backup-5","pod":"backup-1978","region":"ap-south-1","trace_id":"tr-7750694","resource_id":"backup_7253","event":"restore_candidate_evaluated","eligible":"true","deletion_block":"false"}
- 2026-04-19T06:51:42Z {"severity":"DEBUG","logger":"support_platform","service":"support_platform","instance":"support-3","pod":"support-e0d2","region":"us-east-2","trace_id":"tr-7341934","event":"message_scan_started","subject_key":"haeun-jung@gmail.com","attempt":"1"}
- 2026-04-19T06:51:45Z {"severity":"WARN","logger":"support_platform","service":"support_platform","instance":"support-3","pod":"support-e0d2","region":"us-east-2","trace_id":"tr-7341934","resource_id":"support_3294","event":"message_pii_scan","matched_value":"haeun-jung@gmail.com","detector":"direct_identifier"}
- 2026-04-19T06:51:49Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-7","pod":"account-53ad","region":"eu-west-1","trace_id":"tr-1023023","event":"profile_lookup_started","lookup_key":"watanabe.kenta@gmail.com","attempt":"1"}
- 2026-04-19T06:51:54Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-7","pod":"account-53ad","region":"eu-west-1","trace_id":"tr-1023023","event":"cache_lookup","result":"miss","cache":"account_service_lookup_v2"}
- 2026-04-19T06:51:55Z {"severity":"INFO","logger":"account_service","service":"account_service","instance":"account-7","pod":"account-53ad","region":"eu-west-1","trace_id":"tr-1023023","resource_id":"account_7653","event":"profile_lookup_completed","rows":"0","http_status":"404","duration_ms":"25"}
last_20_lines:
- 2026-04-19T06:58:02Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-2","pod":"security-0959","region":"eu-west-1","trace_id":"tr-7033629","event":"audit_record_query_started","subject_ref":"user_362","attempt":"1"}
- 2026-04-19T06:58:05Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-5","pod":"account-d6f8","region":"ap-south-1","trace_id":"tr-7467056","event":"profile_lookup_started","lookup_key":"priya.s5164@outlook.com","attempt":"1"}
- 2026-04-19T06:58:06Z {"severity":"WARN","logger":"support_platform","service":"support_platform","instance":"support-4","pod":"support-7c2d","region":"eu-west-1","trace_id":"tr-7434755","resource_id":"support_9699","event":"message_pii_scan","matched_value":"watanabe.kenta@gmail.com","detector":"direct_identifier"}
- 2026-04-19T06:58:13Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-5","pod":"account-d6f8","region":"ap-south-1","trace_id":"tr-7467056","event":"connection_acquired","pool":"account_service_replica","wait_ms":"44"}
- 2026-04-19T06:58:13Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-2","pod":"security-0959","region":"eu-west-1","trace_id":"tr-7033629","resource_id":"audit_record_7136","event":"audit_record_read_completed","integrity_check":"passed","rows":"1"}
- 2026-04-19T06:58:15Z {"severity":"WARN","logger":"account_service","service":"account_service","instance":"account-5","pod":"account-d6f8","region":"ap-south-1","trace_id":"tr-7467056","event":"dependency_retry","dependency":"account_service_store","attempt":"1","retry_in_ms":"284","reason":"read_timeout"}
- 2026-04-19T06:58:16Z {"severity":"INFO","logger":"account_service","service":"account_service","instance":"account-5","pod":"account-d6f8","region":"ap-south-1","trace_id":"tr-7467056","event":"dependency_recovered","attempt":"2","route":"primary"}
- 2026-04-19T06:58:17Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-5","pod":"account-d6f8","region":"ap-south-1","trace_id":"tr-7467056","resource_id":"account_3204","event":"profile_lookup_completed","rows":"1","http_status":"200","duration_ms":"58"}
- 2026-04-19T06:58:30Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-1","pod":"security-72f8","region":"ap-south-1","trace_id":"tr-9540622","event":"audit_record_query_started","subject_ref":"user_369","attempt":"1"}
- 2026-04-19T06:58:34Z {"severity":"WARN","logger":"analytics_platform","service":"analytics_platform","instance":"analytics-5","pod":"analytics-9232","region":"us-east-2","trace_id":"tr-0004870","resource_id":"analytics_946","event":"analytics_identity_scan","matched_value":"priya.s5164@outlook.com","direct_identifiers":"1","detector":"direct_identifier"}
- 2026-04-19T06:58:36Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-1","pod":"security-72f8","region":"ap-south-1","trace_id":"tr-9540622","event":"connection_acquired","pool":"security_service_primary","wait_ms":"18"}
- 2026-04-19T06:58:38Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-1","pod":"security-72f8","region":"ap-south-1","trace_id":"tr-9540622","resource_id":"audit_record_689","event":"audit_record_read_completed","integrity_check":"passed","rows":"1"}
- 2026-04-19T06:58:49Z {"severity":"DEBUG","logger":"account_service","service":"account_service","instance":"account-2","pod":"account-32ce","region":"us-east-2","trace_id":"tr-2999124","event":"profile_lookup_started","lookup_key":"m.khumalo88@gmail.com","attempt":"1"}
- 2026-04-19T06:58:52Z {"severity":"WARN","logger":"integration_service","service":"integration_service","instance":"integration-5","pod":"integration-b940","region":"ap-south-1","trace_id":"tr-8499950","resource_id":"data_flow_8293","event":"connector_heartbeat","enabled":"true","scheduler_registered":"true","last_run":"success","correlation_key":"valeria.garcia92@outlook.com"}
- 2026-04-19T06:58:59Z {"severity":"INFO","logger":"account_service","service":"account_service","instance":"account-2","pod":"account-32ce","region":"us-east-2","trace_id":"tr-2999124","resource_id":"account_9205","event":"profile_lookup_completed","rows":"0","http_status":"404","duration_ms":"83"}
- 2026-04-19T06:59:20Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-2","pod":"security-a6b6","region":"us-east-2","trace_id":"tr-8433880","resource_id":"audit_record_4655","event":"audit_record_read_completed","integrity_check":"passed","rows":"1","correlation_key":"user_364"}
- 2026-04-19T06:59:38Z {"severity":"DEBUG","logger":"search_service","service":"search_service","instance":"search-6","pod":"search-04de","region":"us-east-2","trace_id":"tr-3759012","event":"index_query_started","match_key":"lpereira7245@gmail.com","attempt":"1"}
- 2026-04-19T06:59:39Z {"severity":"DEBUG","logger":"search_service","service":"search_service","instance":"search-6","pod":"search-04de","region":"us-east-2","trace_id":"tr-3759012","event":"connection_acquired","pool":"search_service_primary","wait_ms":"10"}
- 2026-04-19T06:59:41Z {"severity":"INFO","logger":"search_service","service":"search_service","instance":"search-6","pod":"search-04de","region":"us-east-2","trace_id":"tr-3759012","resource_id":"search_5301","event":"index_query_completed","index":"customer_directory_v3","result":"hit","shard":"9","took_ms":"3"}
- 2026-04-19T06:59:43Z {"severity":"INFO","logger":"log_router","service":"log_router","instance":"collector-2","event":"export_completed","source_events":"130","auxiliary_events":"4"}

#### evidence_35
### customer_data_snapshot_bundle_20260416.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260416.json
bytes: 13423
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-04-16T06:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-04-08T06:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_8598', 'customer_reference': 'user_372', 'full_name': 'Obinna Okafor', 'email': 'obinna.okafor@gmail.com', 'phone': '+234 803 888 8709', 'account_status': 'ACTIVE', 'signup_channel': 'referral'}]}, {'captured_at': '2026-04-14T06:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_6246', 'customer_re…

#### evidence_36
### customer_export_manifest_20260409.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_export_manifest_20260409.json
bytes: 11837
top_level_type: dict
top_level_keys: ['exported_at', 'origin', 'record_count', 'records']
sample: {'exported_at': '2026-04-09T12:00:00Z', 'origin': 'customer_export_service', 'record_count': 46, 'records': [{'recorded_at': '2026-04-03T12:00:00Z', 'system': 'account_service', 'resource_id': 'account_7618', 'record_type': 'USER_PROFILE', 'result': 'FOUND', 'subject_reference': 'dnakamura7301@gmail.com'}, {'recorded_at': '2026-04-09T09:00:00Z', 'system': 'search_service', 'resource_id': 'search_9606', 'record_type': 'SEARCH_INDEX_ENTRY', 'result': 'FOUND', 'subject_reference': 'camila.almeida.jr@outlook.com'}, {'recorded_at': '2026-04-09T12:00:00Z', 'system': 'account_service', 'resource_id':…

#### evidence_37
### security_audit_explorer_20260905.png
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\images\security_audit_explorer_20260905.png
bytes: 147699
IMAGE_INSPECTION_ERROR: No module named 'PIL'

#### evidence_38
### customer_data_regional_replicas_20260330.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_regional_replicas_20260330.sql
bytes: 35620
CREATE_TABLE: ['CREATE TABLE customer_data_primary', 'CREATE TABLE customer_data_replica_ap_south', 'CREATE TABLE customer_data_replica_eu_west']
sample_INSERT: ['INSERT INTO "customer_data_primary" VALUES(\'analytics_1792\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_1792","user_id":"user_402","email":"minjun.jung@outlook.com","phone":"+82 10 8655 5230","email_hash":"2971cbd0a4a…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_1922\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_1922","user_id":"user_405","email":"lucia-garcia@proton.me","phone":"+34 775 705 836","email_hash":"4c877035304d8…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_298\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_298","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"sess…']

#### evidence_39
### syslog_archive_ap_southeast_20260325.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\syslog_archive_ap_southeast_20260325.log
bytes: 26082
line_count: 114
first_20_lines:
- 2026-03-25T08:51:13Z <15>1 node-8 log_router collector-7 - - level=DEBUG instance="collector-7" event="export_started" sources="platform_services" expected_source_events="109"
- 2026-03-25T08:51:15Z <15>1 node-1 support_platform tr-7458912 - - level=DEBUG instance="support-4" pod="support-6150" region="ap-south-1" event="message_scan_started" subject_key="silva.mariana@icloud.com" attempt="1"
- 2026-03-25T08:51:21Z <15>1 node-1 support_platform tr-7458912 - - level=DEBUG instance="support-4" pod="support-6150" region="ap-south-1" event="connection_acquired" pool="support_platform_primary" wait_ms="1"
- 2026-03-25T08:51:23Z <12>1 node-1 support_platform tr-7458912 - - level=WARN instance="support-4" pod="support-6150" region="ap-south-1" resource_id="support_9464" event="message_pii_scan" matched_value="silva.mariana@icloud.com" detector="direct_identifier"
- 2026-03-25T08:51:51Z <15>1 node-7 support_platform tr-6141219 - - level=DEBUG instance="support-4" pod="support-b427" region="eu-central-1" event="attachment_scan_started" scan_key="ananya-jain@proton.me" attempt="1"
- 2026-03-25T08:51:54Z <14>1 node-4 account_service tr-3269055 - - level=INFO instance="account-6" pod="account-56bf" region="eu-central-1" resource_id="account_7606" event="profile_lookup_completed" rows="0" http_status="404" duration_ms="61" correlation_key="storres487178@fastmail.com"
- 2026-03-25T08:51:55Z <12>1 node-7 support_platform tr-6141219 - - level=WARN instance="support-4" pod="support-b427" region="eu-central-1" resource_id="support_2944" event="attachment_pii_scan" matched_value="ananya-jain@proton.me" file="delivery_confirmation_34.pdf" detector="direct_identifier"
- 2026-03-25T08:52:03Z <15>1 node-9 account_service tr-5817131 - - level=DEBUG instance="account-3" pod="account-c1f5" region="eu-west-1" event="profile_lookup_started" lookup_key="KEIKO.SATO@OUTLOOK.COM" attempt="1"
- 2026-03-25T08:52:07Z <15>1 node-9 account_service tr-5817131 - - level=DEBUG instance="account-3" pod="account-c1f5" region="eu-west-1" event="connection_acquired" pool="account_service_replica" wait_ms="37"
- 2026-03-25T08:52:09Z <12>1 node-9 account_service tr-5817131 - - level=WARN instance="account-3" pod="account-c1f5" region="eu-west-1" event="dependency_retry" dependency="account_service_store" attempt="1" retry_in_ms="155" reason="read_timeout"
- 2026-03-25T08:52:10Z <14>1 node-9 account_service tr-5817131 - - level=INFO instance="account-3" pod="account-c1f5" region="eu-west-1" event="dependency_recovered" attempt="2" route="primary"
- 2026-03-25T08:52:11Z <14>1 node-9 account_service tr-5817131 - - level=INFO instance="account-3" pod="account-c1f5" region="eu-west-1" resource_id="account_3075" event="profile_lookup_completed" rows="0" http_status="404" duration_ms="12"
- 2026-03-25T08:52:15Z <15>1 node-9 search_service tr-5482781 - - level=DEBUG instance="search-5" pod="search-1fc7" region="eu-central-1" event="index_query_started" match_key="s.kim14@yahoo.com" attempt="1"
- 2026-03-25T08:52:23Z <15>1 node-9 search_service tr-5482781 - - level=DEBUG instance="search-5" pod="search-1fc7" region="eu-central-1" event="connection_acquired" pool="search_service_replica" wait_ms="62"
- 2026-03-25T08:52:25Z <12>1 node-9 search_service tr-5482781 - - level=WARN instance="search-5" pod="search-1fc7" region="eu-central-1" event="dependency_retry" dependency="search_service_store" attempt="1" retry_in_ms="279" reason="read_timeout"
- 2026-03-25T08:52:26Z <14>1 node-9 search_service tr-5482781 - - level=INFO instance="search-5" pod="search-1fc7" region="eu-central-1" event="dependency_recovered" attempt="2" route="primary"
- 2026-03-25T08:52:27Z <14>1 node-9 search_service tr-5482781 - - level=INFO instance="search-5" pod="search-1fc7" region="eu-central-1" resource_id="search_5479" event="index_query_completed" index="customer_directory_v3" result="hit" shard="7" took_ms="26"
- 2026-03-25T08:52:52Z <12>1 node-2 support_platform tr-7039315 - - level=WARN instance="support-4" pod="support-24c9" region="eu-west-1" resource_id="support_1993" event="message_pii_scan" matched_value="thandiwe.n5276@outlook.com" detector="direct_identifier"
- 2026-03-25T08:52:56Z <15>1 node-8 systemd node-7 - - level=DEBUG instance="node-7" event="timer_tick" unit="logrotate.timer"
- 2026-03-25T08:53:03Z <15>1 node-6 account_service tr-4420589 - - level=DEBUG instance="account-7" pod="account-2e69" region="eu-west-1" event="profile_lookup_started" lookup_key="silva.mariana@icloud.com" attempt="1"
last_20_lines:
- 2026-03-25T08:58:41Z <15>1 node-6 security_service tr-5017172 - - level=DEBUG instance="security-6" pod="security-85d2" region="us-east-2" event="connection_acquired" pool="security_service_primary" wait_ms="8"
- 2026-03-25T08:58:42Z <12>1 node-2 account_service tr-6239926 - - level=WARN instance="account-2" pod="account-5d4c" region="ap-south-1" event="dependency_retry" dependency="account_service_store" attempt="1" retry_in_ms="407" reason="read_timeout"
- 2026-03-25T08:58:43Z <14>1 node-2 account_service tr-6239926 - - level=INFO instance="account-2" pod="account-5d4c" region="ap-south-1" event="dependency_recovered" attempt="2" route="primary"
- 2026-03-25T08:58:43Z <15>1 node-6 security_service tr-5017172 - - level=DEBUG instance="security-6" pod="security-85d2" region="us-east-2" resource_id="audit_record_7959" event="audit_record_read_completed" integrity_check="passed" rows="1"
- 2026-03-25T08:58:44Z <14>1 node-2 account_service tr-6239926 - - level=INFO instance="account-2" pod="account-5d4c" region="ap-south-1" resource_id="account_4087" event="profile_lookup_completed" rows="0" http_status="404" duration_ms="28"
- 2026-03-25T08:59:02Z <15>1 node-6 search_service tr-4045793 - - level=DEBUG instance="search-3" pod="search-c09d" region="eu-west-1" event="index_query_started" match_key="KEIKO.SATO@OUTLOOK.COM" attempt="1"
- 2026-03-25T08:59:04Z <15>1 node-9 integration_service tr-2857292 - - level=DEBUG instance="integration-1" pod="integration-d264" region="ap-south-1" event="connector_config_read_started" subject_key="KEIKO.SATO@OUTLOOK.COM" attempt="1"
- 2026-03-25T08:59:07Z <15>1 node-6 search_service tr-4045793 - - level=DEBUG instance="search-3" pod="search-c09d" region="eu-west-1" event="cache_lookup" result="miss" cache="search_service_lookup_v2"
- 2026-03-25T08:59:08Z <14>1 node-6 search_service tr-4045793 - - level=INFO instance="search-3" pod="search-c09d" region="eu-west-1" resource_id="search_6600" event="index_query_completed" index="customer_directory_v3" result="hit" shard="0" took_ms="31"
- 2026-03-25T08:59:09Z <12>1 node-3 integration_service tr-4333880 - - level=WARN instance="integration-7" pod="integration-1186" region="us-east-2" resource_id="data_flow_8871" event="connector_heartbeat" enabled="true" scheduler_registered="true" last_run="success" correlation_key="camille.girard80@gmail.com"
- 2026-03-25T08:59:13Z <15>1 node-9 integration_service tr-2857292 - - level=DEBUG instance="integration-1" pod="integration-d264" region="ap-south-1" event="connection_acquired" pool="integration_service_primary" wait_ms="13"
- 2026-03-25T08:59:15Z <12>1 node-9 integration_service tr-2857292 - - level=WARN instance="integration-1" pod="integration-d264" region="ap-south-1" resource_id="data_flow_1412" event="connector_heartbeat" enabled="true" scheduler_registered="true" last_run="success"
- 2026-03-25T08:59:27Z <15>1 node-6 search_service tr-9514913 - - level=DEBUG instance="search-5" pod="search-e413" region="eu-central-1" event="index_query_started" match_key="noah.r2790@zoho.com" attempt="1"
- 2026-03-25T08:59:31Z <15>1 node-6 search_service tr-9514913 - - level=DEBUG instance="search-5" pod="search-e413" region="eu-central-1" event="cache_lookup" result="miss" cache="search_service_lookup_v2"
- 2026-03-25T08:59:32Z <14>1 node-6 search_service tr-9514913 - - level=INFO instance="search-5" pod="search-e413" region="eu-central-1" resource_id="search_3251" event="index_query_completed" index="customer_directory_v3" result="hit" shard="11" took_ms="30"
- 2026-03-25T08:59:34Z <15>1 node-7 search_service tr-0441096 - - level=DEBUG instance="search-7" pod="search-d518" region="ap-south-1" event="index_query_started" match_key="storres487178@fastmail.com" attempt="1"
- 2026-03-25T08:59:40Z <15>1 node-7 search_service tr-0441096 - - level=DEBUG instance="search-7" pod="search-d518" region="ap-south-1" event="connection_acquired" pool="search_service_replica" wait_ms="66"
- 2026-03-25T08:59:42Z <12>1 node-7 search_service tr-0441096 - - level=WARN instance="search-7" pod="search-d518" region="ap-south-1" event="dependency_retry" dependency="search_service_store" attempt="1" retry_in_ms="232" reason="read_timeout"
- 2026-03-25T08:59:43Z <14>1 node-7 search_service tr-0441096 - - level=INFO instance="search-7" pod="search-d518" region="ap-south-1" event="dependency_recovered" attempt="2" route="primary"
- 2026-03-25T08:59:44Z <14>1 node-7 search_service tr-0441096 - - level=INFO instance="search-7" pod="search-d518" region="ap-south-1" resource_id="search_8472" event="index_query_completed" index="customer_directory_v3" result="hit" shard="0" took_ms="12"

#### evidence_40
### customer_data_snapshot_bundle_20260322.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260322.json
bytes: 13647
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-03-22T08:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-03-14T08:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_6006', 'customer_reference': 'user_428', 'full_name': 'Ji-hoon Yoon', 'email': 'yoon.jihoon@icloud.com', 'phone': '+82 10 2686 9320', 'account_status': 'ACTIVE', 'signup_channel': 'referral'}]}, {'captured_at': '2026-03-20T05:00:00Z', 'data_store': 'search_service', 'collection': 'customer_search_documents', 'records': [{'resource_id': 'search_9094', 'index_na…

#### evidence_41
### notification_delivery_20260315.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\notification_delivery_20260315.log
bytes: 9011
line_count: 39
first_20_lines:
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=1 system="account_service" resource_id="account_022" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="zofia-novak@gmail.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=2 system="account_service" resource_id="account_1538" record_type="USER_PROFILE" result="FOUND" subject_reference="n.mokoena70@yahoo.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=3 system="account_service" resource_id="account_1680" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="lkhalil7413@gmail.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=4 system="account_service" resource_id="account_1897" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="tanaka.ren@icloud.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=5 system="account_service" resource_id="account_3002" record_type="USER_PROFILE" result="FOUND" subject_reference="tunde.a533297@outlook.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=6 system="account_service" resource_id="account_3078" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="lindberg.freja@gmail.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=7 system="account_service" resource_id="account_4813" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="charlotte.foster@gmail.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=8 system="account_service" resource_id="account_5817" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="javier.m7818@zoho.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=9 system="account_service" resource_id="account_790" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="akosua.owusu@outlook.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=10 system="account_service" resource_id="account_9194" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="l.bernard56@gmail.com"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=11 system="analytics_platform" resource_id="analytics_2354" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="charlotte.foster@gmail.com"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=12 system="analytics_platform" resource_id="analytics_6172" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="zofia-novak@gmail.com"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=13 system="analytics_platform" resource_id="analytics_6528" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="lkhalil7413@gmail.com"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=14 system="backup_service" resource_id="backup_5237" record_type="BACKUP_ARCHIVE" result="ACTIVE" subject_reference="l.bernard56@gmail.com"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=15 system="integration_service" resource_id="data_flow_1283" record_type="DATA_FLOW" result="ACTIVE" subject_reference="javier.m7818@zoho.com"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=16 system="integration_service" resource_id="data_flow_3226" record_type="DATA_FLOW" result="ACTIVE" subject_reference="lkhalil7413@gmail.com"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=17 system="integration_service" resource_id="data_flow_5967" record_type="DATA_FLOW" result="ACTIVE" subject_reference="akosua.owusu@outlook.com"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=18 system="integration_service" resource_id="data_flow_9854" record_type="DATA_FLOW" result="ACTIVE" subject_reference="charlotte.foster@gmail.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=19 system="search_service" resource_id="search_1194" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="tanaka.ren@icloud.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=20 system="search_service" resource_id="search_2052" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="lkhalil7413@gmail.com"
last_20_lines:
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=20 system="search_service" resource_id="search_2052" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="lkhalil7413@gmail.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=21 system="search_service" resource_id="search_2922" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="akosua.owusu@outlook.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=22 system="search_service" resource_id="search_3058" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="n.mokoena70@yahoo.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=23 system="search_service" resource_id="search_5626" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="charlotte.foster@gmail.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=24 system="search_service" resource_id="search_6599" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="lindberg.freja@gmail.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=25 system="search_service" resource_id="search_9100" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="javier.m7818@zoho.com"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=26 system="security_service" resource_id="audit_record_1149" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_437"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=27 system="security_service" resource_id="audit_record_1366" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_436"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=28 system="security_service" resource_id="audit_record_2748" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_434"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=29 system="security_service" resource_id="audit_record_4043" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_432"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=30 system="security_service" resource_id="audit_record_4839" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_440"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=31 system="security_service" resource_id="audit_record_5488" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_438"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=32 system="security_service" resource_id="audit_record_6665" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_431"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=33 system="security_service" resource_id="audit_record_6846" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_435"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=34 system="security_service" resource_id="audit_record_7313" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_439"
- 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=35 system="security_service" resource_id="audit_record_9695" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_433"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=36 system="support_platform" resource_id="support_165" record_type="SUPPORT_MESSAGE" result="IDENTIFIABLE" subject_reference="lindberg.freja@gmail.com"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=37 system="support_platform" resource_id="support_3364" record_type="SUPPORT_MESSAGE" result="IDENTIFIABLE" subject_reference="charlotte.foster@gmail.com"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=38 system="support_platform" resource_id="support_4123" record_type="SUPPORT_MESSAGE" result="IDENTIFIABLE" subject_reference="tanaka.ren@icloud.com"
- 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=39 system="support_platform" resource_id="support_6688" record_type="SUPPORT_MESSAGE" result="IDENTIFIABLE" subject_reference="lkhalil7413@gmail.com"

#### evidence_42
### deleted_account_reference_20260310.png
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\images\deleted_account_reference_20260310.png
bytes: 136696
IMAGE_INSPECTION_ERROR: No module named 'PIL'

#### evidence_43
### customer_data_reporting_replica_20260305.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_reporting_replica_20260305.sql
bytes: 20348
CREATE_TABLE: ['CREATE TABLE customer_data_primary', 'CREATE TABLE customer_data_reporting_replica']
sample_INSERT: ['INSERT INTO "customer_data_primary" VALUES(\'analytics_1126\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_1126","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_5221\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_5221","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_6750\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_6750","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…']

#### evidence_44
### application_trace_eu_north_20260302.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\application_trace_eu_north_20260302.log
bytes: 25010
line_count: 125
first_20_lines:
- 2026-02-22T10:58:43Z [DEBUG] [log_router] [collector-3] export_started: instance="collector-3" sources="platform_services" expected_source_events="119"
- 2026-02-22T10:58:45Z [DEBUG] [account_service] [tr-9071194] profile_lookup_started: instance="account-1" pod="account-0410" region="ap-south-1" lookup_key="isabela.rodrigues@gmail.com" attempt="1"
- 2026-02-22T10:58:51Z [DEBUG] [account_service] [tr-9071194] profile_lookup_completed: instance="account-1" pod="account-0410" region="ap-south-1" resource_id="account_7023" rows="1" http_status="200" duration_ms="59"
- 2026-02-24T01:22:52Z [ERROR] [webhook_delivery] [notify-8] delivery_abandoned: instance="notify-8" destination="status_page" attempts="5" http_status="503"
- 2026-02-25T15:46:59Z [DEBUG] [thread_pool] [app-8] pool_sample: instance="app-8" active="30" queued="2"
- 2026-02-27T06:11:06Z [INFO] [runtime_config] [app-8] properties_reloaded: instance="app-8" changed="2"
- 2026-02-28T07:57:13Z [DEBUG] [search_service] [tr-3561007] index_query_started: instance="search-5" pod="search-9ed9" region="eu-west-1" match_key="salma.hamdan.jr@outlook.com" attempt="1"
- 2026-02-28T07:57:22Z [DEBUG] [search_service] [tr-3561007] connection_acquired: instance="search-5" pod="search-9ed9" region="eu-west-1" pool="search_service_primary" wait_ms="16"
- 2026-02-28T07:57:24Z [INFO] [search_service] [tr-3561007] index_query_completed: instance="search-5" pod="search-9ed9" region="eu-west-1" resource_id="search_2843" index="customer_directory_v3" result="hit" shard="11" took_ms="25"
- 2026-02-28T10:51:11Z [DEBUG] [search_service] [tr-8748803] index_query_started: instance="search-3" pod="search-c869" region="eu-west-1" match_key="appiah.ama80@icloud.com" attempt="1"
- 2026-02-28T10:51:15Z [DEBUG] [search_service] [tr-8748803] cache_lookup: instance="search-3" pod="search-c869" region="eu-west-1" result="miss" cache="search_service_lookup_v2"
- 2026-02-28T10:51:16Z [INFO] [search_service] [tr-8748803] index_query_completed: instance="search-3" pod="search-c869" region="eu-west-1" resource_id="search_8417" index="customer_directory_v3" result="hit" shard="5" took_ms="19"
- 2026-02-28T10:51:26Z [INFO] [integration_service] [tr-4170430] connector_config_loaded: instance="integration-2" pod="integration-8a16" region="us-east-2" resource_id="data_flow_8024" enabled="false" scheduler_registered="false" correlation_key="user_461"
- 2026-02-28T10:51:37Z [INFO] [search_service] [tr-7545425] index_query_completed: instance="search-4" pod="search-6fed" region="eu-west-1" resource_id="search_728" index="customer_directory_v3" result="hit" shard="8" took_ms="18" correlation_key="n.ogunleye2679@yahoo.com"
- 2026-02-28T10:51:38Z [DEBUG] [backup_service] [tr-0066806] restore_policy_check_started: instance="backup-2" pod="backup-330e" region="us-east-2" subject_key="user_462" attempt="1"
- 2026-02-28T10:51:42Z [DEBUG] [backup_service] [tr-0066806] connection_acquired: instance="backup-2" pod="backup-330e" region="us-east-2" pool="backup_service_replica" wait_ms="31"
- 2026-02-28T10:51:44Z [WARN] [backup_service] [tr-0066806] dependency_retry: instance="backup-2" pod="backup-330e" region="us-east-2" dependency="backup_service_store" attempt="1" retry_in_ms="300" reason="read_timeout"
- 2026-02-28T10:51:45Z [INFO] [backup_service] [tr-0066806] dependency_recovered: instance="backup-2" pod="backup-330e" region="us-east-2" attempt="2" route="primary"
- 2026-02-28T10:51:45Z [DEBUG] [security_service] [tr-5327714] audit_record_query_started: instance="security-1" pod="security-2614" region="ap-south-1" subject_ref="user_470" attempt="1"
- 2026-02-28T10:51:46Z [INFO] [backup_service] [tr-0066806] restore_authorization_completed: instance="backup-2" pod="backup-330e" region="us-east-2" resource_id="backup_7400" decision="deny" policy="privacy_deletion"
last_20_lines:
- 2026-02-28T10:59:02Z [DEBUG] [account_service] [tr-8861736] profile_lookup_started: instance="account-6" pod="account-0346" region="us-east-2" lookup_key="isabela.rodrigues@gmail.com" attempt="1"
- 2026-02-28T10:59:07Z [DEBUG] [backup_service] [tr-6610698] cache_lookup: instance="backup-4" pod="backup-248c" region="ap-south-1" result="miss" cache="backup_service_lookup_v2"
- 2026-02-28T10:59:08Z [INFO] [backup_service] [tr-6610698] restore_authorization_completed: instance="backup-4" pod="backup-248c" region="ap-south-1" resource_id="backup_2005" decision="deny" policy="privacy_deletion"
- 2026-02-28T10:59:09Z [DEBUG] [account_service] [tr-8861736] connection_acquired: instance="account-6" pod="account-0346" region="us-east-2" pool="account_service_replica" wait_ms="20"
- 2026-02-28T10:59:11Z [WARN] [account_service] [tr-8861736] dependency_retry: instance="account-6" pod="account-0346" region="us-east-2" dependency="account_service_store" attempt="1" retry_in_ms="303" reason="read_timeout"
- 2026-02-28T10:59:12Z [INFO] [account_service] [tr-8861736] dependency_recovered: instance="account-6" pod="account-0346" region="us-east-2" attempt="2" route="primary"
- 2026-02-28T10:59:13Z [INFO] [account_service] [tr-8861736] profile_lookup_completed: instance="account-6" pod="account-0346" region="us-east-2" resource_id="account_7023" rows="0" http_status="404" duration_ms="59"
- 2026-02-28T10:59:24Z [DEBUG] [security_service] [tr-1986738] audit_record_query_started: instance="security-6" pod="security-f0a8" region="ap-south-1" subject_ref="user_462" attempt="1"
- 2026-02-28T10:59:32Z [DEBUG] [account_service] [tr-3551191] profile_lookup_started: instance="account-6" pod="account-f5cf" region="eu-central-1" lookup_key="ana.n5388@outlook.com" attempt="1"
- 2026-02-28T10:59:32Z [ERROR] [backup_service] [tr-3607990] restore_candidate_evaluated: instance="backup-7" pod="backup-50cc" region="ap-south-1" resource_id="backup_7543" eligible="true" deletion_block="false" correlation_key="k.iyer40@gmail.com"
- 2026-02-28T10:59:34Z [DEBUG] [security_service] [tr-1986738] cache_lookup: instance="security-6" pod="security-f0a8" region="ap-south-1" result="miss" cache="security_service_lookup_v2"
- 2026-02-28T10:59:35Z [DEBUG] [security_service] [tr-1986738] audit_record_read_completed: instance="security-6" pod="security-f0a8" region="ap-south-1" resource_id="audit_record_5183" integrity_check="passed" rows="1"
- 2026-02-28T10:59:39Z [DEBUG] [account_service] [tr-3551191] connection_acquired: instance="account-6" pod="account-f5cf" region="eu-central-1" pool="account_service_replica" wait_ms="63"
- 2026-02-28T10:59:41Z [WARN] [account_service] [tr-3551191] dependency_retry: instance="account-6" pod="account-f5cf" region="eu-central-1" dependency="account_service_store" attempt="1" retry_in_ms="298" reason="read_timeout"
- 2026-02-28T10:59:42Z [INFO] [account_service] [tr-3551191] dependency_recovered: instance="account-6" pod="account-f5cf" region="eu-central-1" attempt="2" route="primary"
- 2026-02-28T10:59:43Z [INFO] [account_service] [tr-3551191] profile_lookup_completed: instance="account-6" pod="account-f5cf" region="eu-central-1" resource_id="account_1698" rows="0" http_status="404" duration_ms="46"
- 2026-02-28T20:35:13Z [WARN] [http_client] [app-8] connection_pool_pressure: instance="app-8" leased="42" max="50"
- 2026-03-02T10:59:12Z [DEBUG] [account_service] [tr-3760649] profile_lookup_started: instance="account-1" pod="account-f699" region="eu-west-1" lookup_key="ana.n5388@outlook.com" attempt="1"
- 2026-03-02T10:59:21Z [DEBUG] [account_service] [tr-3760649] profile_lookup_completed: instance="account-1" pod="account-f699" region="eu-west-1" resource_id="account_1698" rows="1" http_status="200" duration_ms="46"
- 2026-03-02T10:59:23Z [INFO] [log_router] [collector-3] export_completed: instance="collector-3" source_events="119" auxiliary_events="4"

#### evidence_45
### customer_data_snapshot_bundle_20260223.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260223.json
bytes: 24885
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-02-23T10:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-02-23T07:00:00Z', 'data_store': 'search_service', 'collection': 'customer_search_documents', 'records': [{'resource_id': 'search_5192', 'index_name': 'customer_directory_v3', 'document': {'display_name': None, 'email': 'znkosi0011.jr@fastmail.com', 'customer_reference': None}}]}, {'captured_at': '2026-02-23T10:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_3205', 'customer_reference': 'user_473', 'full_name': 'Nils…

#### evidence_46
### object_storage_browser_20260213.png
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\images\object_storage_browser_20260213.png
bytes: 154193
IMAGE_INSPECTION_ERROR: No module named 'PIL'

#### evidence_47
### customer_data_reporting_replica_20260208.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_reporting_replica_20260208.sql
bytes: 19302
CREATE_TABLE: ['CREATE TABLE customer_data_primary', 'CREATE TABLE customer_data_reporting_replica']
sample_INSERT: ['INSERT INTO "customer_data_primary" VALUES(\'analytics_1558\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_1558","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window":"last_90_days","metrics":{"se…', 'INSERT INTO "customer_data_primary" VALUES(\'analytics_784\',\'analytics_platform\',\'customer_analytics_reports\',\'{"resource_id":"analytics_784","user_id":"user_507","email":"joao-costa@gmail.com","phone":"+55 31 94739-9361","email_hash":"c83e1f4e40e9d75…', 'INSERT INTO "customer_data_primary" VALUES(\'audit_record_1361\',\'security_service\',\'security_audit_events\',\'{"resource_id":"audit_record_1361","subject_reference":"user_504","event_name":"account_deletion_reviewed","actor_type":"automated_privacy_work…']

#### evidence_48
### operations_stream_me_central_20260203.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\operations_stream_me_central_20260203.log
bytes: 21302
line_count: 103
first_20_lines:
- 2026-02-03T05:51:23Z | DEBUG | security_service | tr-4612767 | audit_record_query_started | instance="security-1" pod="security-5049" region="eu-west-1" subject_ref="user_517" attempt="1"
- 2026-02-03T05:51:28Z | DEBUG | security_service | tr-4612767 | connection_acquired | instance="security-1" pod="security-5049" region="eu-west-1" pool="security_service_primary" wait_ms="24"
- 2026-02-03T05:51:30Z | DEBUG | security_service | tr-4612767 | audit_record_read_completed | instance="security-1" pod="security-5049" region="eu-west-1" resource_id="audit_record_4027" integrity_check="passed" rows="1"
- 2026-02-03T05:51:41Z | DEBUG | security_service | tr-7075997 | audit_record_query_started | instance="security-4" pod="security-0105" region="eu-west-1" subject_ref="user_513" attempt="1"
- 2026-02-03T05:51:48Z | DEBUG | security_service | tr-7075997 | connection_acquired | instance="security-4" pod="security-0105" region="eu-west-1" pool="security_service_primary" wait_ms="7"
- 2026-02-03T05:51:49Z | DEBUG | security_service | tr-6428706 | audit_record_query_started | instance="security-2" pod="security-2e02" region="us-east-2" subject_ref="user_516" attempt="1"
- 2026-02-03T05:51:50Z | DEBUG | security_service | tr-7075997 | audit_record_read_completed | instance="security-4" pod="security-0105" region="eu-west-1" resource_id="audit_record_7062" integrity_check="passed" rows="1"
- 2026-02-03T05:51:55Z | DEBUG | security_service | tr-6428706 | connection_acquired | instance="security-2" pod="security-2e02" region="us-east-2" pool="security_service_replica" wait_ms="33"
- 2026-02-03T05:51:56Z | INFO | analytics_platform | tr-9718540 | analytics_profile_read | instance="analytics-5" pod="analytics-bca4" region="ap-south-1" resource_id="analytics_4804" direct_identifiers="0" email="null" phone="null"
- 2026-02-03T05:51:57Z | WARN | security_service | tr-6428706 | dependency_retry | instance="security-2" pod="security-2e02" region="us-east-2" dependency="security_service_store" attempt="1" retry_in_ms="372" reason="read_timeout"
- 2026-02-03T05:51:58Z | INFO | security_service | tr-6428706 | dependency_recovered | instance="security-2" pod="security-2e02" region="us-east-2" attempt="2" route="primary"
- 2026-02-03T05:51:59Z | DEBUG | security_service | tr-6428706 | audit_record_read_completed | instance="security-2" pod="security-2e02" region="us-east-2" resource_id="audit_record_5572" integrity_check="passed" rows="1"
- 2026-02-03T05:52:14Z | INFO | account_service | tr-2582785 | profile_lookup_completed | instance="account-2" pod="account-19e7" region="eu-central-1" resource_id="account_141" rows="0" http_status="404" duration_ms="66" correlation_key="yelsayed5095@fastmail.com"
- 2026-02-03T05:52:34Z | DEBUG | account_service | tr-2361113 | profile_lookup_started | instance="account-3" pod="account-daab" region="eu-central-1" lookup_key="suzuki.daichi90@gmail.com" attempt="1"
- 2026-02-03T05:52:38Z | DEBUG | account_service | tr-2361113 | cache_lookup | instance="account-3" pod="account-daab" region="eu-central-1" result="miss" cache="account_service_lookup_v2"
- 2026-02-03T05:52:38Z | DEBUG | security_service | tr-6100318 | audit_record_query_started | instance="security-6" pod="security-1e44" region="ap-south-1" subject_ref="user_512" attempt="1"
- 2026-02-03T05:52:39Z | INFO | account_service | tr-2361113 | profile_lookup_completed | instance="account-3" pod="account-daab" region="eu-central-1" resource_id="account_4979" rows="0" http_status="404" duration_ms="90"
- 2026-02-03T05:52:43Z | DEBUG | integration_service | tr-6648486 | connector_config_read_started | instance="integration-2" pod="integration-a398" region="ap-south-1" subject_key="yetunde.a3014@zoho.com" attempt="1"
- 2026-02-03T05:52:45Z | DEBUG | security_service | tr-6100318 | cache_lookup | instance="security-6" pod="security-1e44" region="ap-south-1" result="miss" cache="security_service_lookup_v2"
- 2026-02-03T05:52:46Z | DEBUG | security_service | tr-6100318 | audit_record_read_completed | instance="security-6" pod="security-1e44" region="ap-south-1" resource_id="audit_record_1967" integrity_check="passed" rows="1"
last_20_lines:
- 2026-02-03T05:58:10Z | DEBUG | security_service | tr-1598401 | connection_acquired | instance="security-2" pod="security-102b" region="eu-central-1" pool="security_service_replica" wait_ms="41"
- 2026-02-03T05:58:12Z | WARN | security_service | tr-1598401 | dependency_retry | instance="security-2" pod="security-102b" region="eu-central-1" dependency="security_service_store" attempt="1" retry_in_ms="267" reason="read_timeout"
- 2026-02-03T05:58:13Z | INFO | security_service | tr-1598401 | dependency_recovered | instance="security-2" pod="security-102b" region="eu-central-1" attempt="2" route="primary"
- 2026-02-03T05:58:14Z | DEBUG | security_service | tr-1598401 | audit_record_read_completed | instance="security-2" pod="security-102b" region="eu-central-1" resource_id="audit_record_3567" integrity_check="passed" rows="1"
- 2026-02-03T05:58:15Z | DEBUG | backup_service | tr-8270299 | restore_policy_check_started | instance="backup-4" pod="backup-b50f" region="eu-central-1" subject_key="s.dlamini52@gmail.com" attempt="1"
- 2026-02-03T05:58:20Z | ERROR | backup_service | tr-8270299 | restore_candidate_evaluated | instance="backup-4" pod="backup-b50f" region="eu-central-1" resource_id="backup_8264" eligible="true" deletion_block="false"
- 2026-02-03T05:58:49Z | DEBUG | support_platform | tr-2266561 | message_scan_started | instance="support-7" pod="support-4249" region="eu-west-1" subject_key="andersson.linnea@icloud.com" attempt="1"
- 2026-02-03T05:58:55Z | DEBUG | support_platform | tr-2266561 | connection_acquired | instance="support-7" pod="support-4249" region="eu-west-1" pool="support_platform_replica" wait_ms="29"
- 2026-02-03T05:58:57Z | WARN | support_platform | tr-2266561 | dependency_retry | instance="support-7" pod="support-4249" region="eu-west-1" dependency="support_platform_store" attempt="1" retry_in_ms="302" reason="read_timeout"
- 2026-02-03T05:58:58Z | INFO | support_platform | tr-2266561 | dependency_recovered | instance="support-7" pod="support-4249" region="eu-west-1" attempt="2" route="primary"
- 2026-02-03T05:58:59Z | WARN | support_platform | tr-2266561 | message_pii_scan | instance="support-7" pod="support-4249" region="eu-west-1" resource_id="support_3982" matched_value="andersson.linnea@icloud.com" detector="direct_identifier"
- 2026-02-03T05:59:15Z | DEBUG | search_service | tr-2128459 | index_query_started | instance="search-6" pod="search-8ac5" region="eu-west-1" match_key="andersson.linnea@icloud.com" attempt="1"
- 2026-02-03T05:59:24Z | INFO | search_service | tr-2128459 | index_query_completed | instance="search-6" pod="search-8ac5" region="eu-west-1" resource_id="search_2715" index="customer_directory_v3" result="hit" shard="3" took_ms="21"
- 2026-02-03T05:59:27Z | WARN | support_platform | tr-7153575 | attachment_pii_scan | instance="support-3" pod="support-93e5" region="eu-west-1" resource_id="support_4533" matched_value="katarina-ionescu@proton.me" file="delivery_confirmation_71.pdf" detector="direct_identifier"
- 2026-02-03T05:59:31Z | DEBUG | security_service | tr-9376496 | audit_record_query_started | instance="security-6" pod="security-8fd4" region="ap-south-1" subject_ref="user_515" attempt="1"
- 2026-02-03T05:59:36Z | DEBUG | security_service | tr-9376496 | connection_acquired | instance="security-6" pod="security-8fd4" region="ap-south-1" pool="security_service_replica" wait_ms="43"
- 2026-02-03T05:59:38Z | WARN | security_service | tr-9376496 | dependency_retry | instance="security-6" pod="security-8fd4" region="ap-south-1" dependency="security_service_store" attempt="1" retry_in_ms="306" reason="read_timeout"
- 2026-02-03T05:59:39Z | INFO | security_service | tr-9376496 | dependency_recovered | instance="security-6" pod="security-8fd4" region="ap-south-1" attempt="2" route="primary"
- 2026-02-03T05:59:40Z | DEBUG | security_service | tr-9376496 | audit_record_read_completed | instance="security-6" pod="security-8fd4" region="ap-south-1" resource_id="audit_record_946" integrity_check="passed" rows="1"
- 2026-02-03T05:59:42Z | INFO | log_router | collector-8 | export_completed | instance="collector-8" source_events="98" auxiliary_events="4" dropped_auxiliary="1"

#### evidence_49
### customer_data_snapshot_bundle_20260131.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260131.json
bytes: 15256
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-01-31T15:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-01-29T12:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': [{'resource_id': 'account_2424', 'customer_reference': 'user_521', 'full_name': 'Aarav Rao', 'email': 'aarav.r528@outlook.com', 'phone': '+91 91726 13808', 'account_status': 'ACTIVE', 'signup_channel': 'organic_search'}, {'resource_id': 'account_4974', 'customer_reference': 'user_523', 'full_name': 'Oliver Walker', 'email': 'o.walker6695@yahoo.com', 'phone': '+1 (646) 555-0123', 'accou…

#### evidence_50
### security_audit_ledger_20261001.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\security_audit_ledger_20261001.json
bytes: 5152
top_level_type: dict
top_level_keys: ['exported_at', 'origin', 'record_count', 'records']
sample: {'exported_at': '2026-10-01T12:00:00Z', 'origin': 'security_audit_service', 'record_count': 20, 'records': [{'recorded_at': '2026-10-01T12:00:00Z', 'system': 'account_service', 'resource_id': 'account_1733', 'record_type': 'USER_PROFILE', 'result': 'FOUND', 'subject_reference': 'haruka-kato@gmail.com'}, {'recorded_at': '2026-10-01T12:00:00Z', 'system': 'account_service', 'resource_id': 'account_2176', 'record_type': 'USER_PROFILE', 'result': 'FOUND', 'subject_reference': 'ieriksen5151@fastmail.com'}, {'recorded_at': '2026-10-01T12:00:00Z', 'system': 'account_service', 'resource_id': 'account_2…

#### evidence_51
### customer_data_snapshot_bundle_20260915.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_data_snapshot_bundle_20260915.json
bytes: 1901
top_level_type: dict
top_level_keys: ['exported_at', 'source', 'snapshots']
sample: {'exported_at': '2026-09-15T12:00:00Z', 'source': 'records_assurance_service', 'snapshots': [{'captured_at': '2026-09-15T12:00:00Z', 'data_store': 'account_service', 'collection': 'customer_profiles', 'records': []}, {'captured_at': '2026-09-15T12:00:00Z', 'data_store': 'identity_service', 'collection': 'deleted_customer_references', 'records': [{'resource_id': 'tombstone_440', 'subject_reference': 'user_541', 'name': None, 'email': None, 'phone': None, 'email_hash': None, 'account_status': 'DELETED'}, {'resource_id': 'tombstone_9178', 'subject_reference': 'user_542', 'name': 'Kofi Addo', 'ema…

#### evidence_52
### customer_data_failover_replica_20260920.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_failover_replica_20260920.sql
bytes: 12304
CREATE_TABLE: ['CREATE TABLE customer_data_failover_replica', 'CREATE TABLE customer_data_primary']
sample_INSERT: ['INSERT INTO "customer_data_failover_replica" VALUES(\'audit_record_1037\',\'security_service\',\'security_audit_events\',\'{"resource_id":"audit_record_1037","subject_reference":"user_544","event_name":"account_deletion_reviewed","actor_type":"automated_pri…', 'INSERT INTO "customer_data_failover_replica" VALUES(\'audit_record_1491\',\'security_service\',\'security_audit_events\',\'{"resource_id":"audit_record_1491","subject_reference":"user_549","event_name":"account_deletion_reviewed","actor_type":"automated_pri…', 'INSERT INTO "customer_data_failover_replica" VALUES(\'audit_record_3831\',\'security_service\',\'security_audit_events\',\'{"resource_id":"audit_record_3831","subject_reference":"user_550","event_name":"account_deletion_reviewed","actor_type":"automated_pri…']

#### evidence_53
### cloud_runtime_export_af_south_20260930.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\cloud_runtime_export_af_south_20260930.log
bytes: 94823
line_count: 305
first_20_lines:
- 2026-09-30T11:51:01Z requestId=collector-4 level=DEBUG function=log_router message="instance=\"collector-4\" event=\"export_started\" sources=\"platform_services\" expected_source_events=\"300\""
- 2026-09-30T11:51:03Z requestId=tr-2263120 level=DEBUG function=profile_service message="instance=\"profile-3\" pod=\"profile-c062\" region=\"us-east-2\" resource_id=\"account_66777\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"53\" correlation_key=\"a.watanabe06@yahoo.com\""
- 2026-09-30T11:51:06Z requestId=tr-4101190 level=DEBUG function=profile_service message="instance=\"profile-4\" pod=\"profile-36f2\" region=\"us-east-2\" resource_id=\"account_75954\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"17\" correlation_key=\"jjung0683@fastmail.com\""
- 2026-09-30T11:51:06Z requestId=tr-4429940 level=DEBUG function=profile_service message="instance=\"profile-6\" pod=\"profile-27c2\" region=\"us-east-2\" resource_id=\"account_46079\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"22\" correlation_key=\"mathis.f808@outlook.com\""
- 2026-09-30T11:51:09Z requestId=tr-6596760 level=DEBUG function=profile_service message="instance=\"profile-2\" pod=\"profile-8f22\" region=\"us-east-2\" resource_id=\"account_25381\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"74\" correlation_key=\"naledi-nkosi@gmail.com\""
- 2026-09-30T11:51:09Z requestId=tr-6268010 level=DEBUG function=profile_service message="instance=\"profile-7\" pod=\"profile-9e52\" region=\"us-east-2\" resource_id=\"account_55256\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"69\" correlation_key=\"dahl.freja@icloud.com\""
- 2026-09-30T11:51:13Z requestId=tr-6896020 level=DEBUG function=profile_service message="instance=\"profile-1\" pod=\"profile-4f42\" region=\"us-east-2\" resource_id=\"account_65967\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"73\" correlation_key=\"nneka.o696@outlook.com\""
- 2026-09-30T11:51:16Z requestId=tr-8734090 level=DEBUG function=profile_service message="instance=\"profile-2\" pod=\"profile-c5d2\" region=\"us-east-2\" resource_id=\"account_75144\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"37\" correlation_key=\"mensah.adwoa@icloud.com\""
- 2026-09-30T11:51:16Z requestId=tr-9062840 level=DEBUG function=profile_service message="instance=\"profile-4\" pod=\"profile-b6a2\" region=\"us-east-2\" resource_id=\"account_45269\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"42\" correlation_key=\"aarav-nair@gmail.com\""
- 2026-09-30T11:51:19Z requestId=tr-0900910 level=DEBUG function=profile_service message="instance=\"profile-5\" pod=\"profile-2d32\" region=\"us-east-2\" resource_id=\"account_54446\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"89\" correlation_key=\"elena.martinez@outlook.com\""
- 2026-09-30T11:51:19Z requestId=tr-1229660 level=DEBUG function=profile_service message="instance=\"profile-7\" pod=\"profile-1e02\" region=\"us-east-2\" resource_id=\"account_24571\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"11\" correlation_key=\"k.saleh00@gmail.com\""
- 2026-09-30T11:51:23Z requestId=tr-1528920 level=DEBUG function=profile_service message="instance=\"profile-6\" pod=\"profile-de22\" region=\"us-east-2\" resource_id=\"account_65157\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"10\" correlation_key=\"nils-dahl@gmail.com\""
- 2026-09-30T11:51:26Z requestId=tr-3695740 level=DEBUG function=profile_service message="instance=\"profile-2\" pod=\"profile-4582\" region=\"us-east-2\" resource_id=\"account_44459\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"62\" correlation_key=\"h.tanaka88@gmail.com\""
- 2026-09-30T11:51:26Z requestId=tr-3366990 level=DEBUG function=profile_service message="instance=\"profile-7\" pod=\"profile-54b2\" region=\"us-east-2\" resource_id=\"account_74334\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"57\" correlation_key=\"nadia.stojanovic@outlook.com\""
- 2026-09-30T11:51:29Z requestId=tr-5533810 level=DEBUG function=profile_service message="instance=\"profile-3\" pod=\"profile-bc12\" region=\"us-east-2\" resource_id=\"account_53636\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"26\" correlation_key=\"hchoi8365@gmail.com\""
- 2026-09-30T11:51:29Z requestId=tr-5862560 level=DEBUG function=profile_service message="instance=\"profile-5\" pod=\"profile-ace2\" region=\"us-east-2\" resource_id=\"account_23761\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"31\" correlation_key=\"jules.r8490@zoho.com\""
- 2026-09-30T11:51:30Z requestId=tr-3995000 level=DEBUG function=profile_service message="instance=\"profile-1\" pod=\"profile-05a2\" region=\"us-east-2\" resource_id=\"account_85045\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"61\" correlation_key=\"abena-boateng@gmail.com\""
- 2026-09-30T11:51:33Z requestId=tr-6161820 level=DEBUG function=profile_service message="instance=\"profile-4\" pod=\"profile-6d02\" region=\"us-east-2\" resource_id=\"account_64347\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"30\" correlation_key=\"a.martinez76@gmail.com\""
- 2026-09-30T11:51:36Z requestId=tr-7999890 level=DEBUG function=profile_service message="instance=\"profile-5\" pod=\"profile-e392\" region=\"us-east-2\" resource_id=\"account_73524\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"77\" correlation_key=\"ahughes8253@gmail.com\""
- 2026-09-30T11:51:36Z requestId=tr-8328640 level=DEBUG function=profile_service message="instance=\"profile-7\" pod=\"profile-d462\" region=\"us-east-2\" resource_id=\"account_43649\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"82\" correlation_key=\"amara.c8378@zoho.com\""
last_20_lines:
- 2026-09-30T11:59:11Z requestId=tr-5569590 level=DEBUG function=profile_service message="instance=\"profile-5\" pod=\"profile-fb72\" region=\"us-east-2\" resource_id=\"account_79194\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"20\" correlation_key=\"sota.ito@outlook.com\""
- 2026-09-30T11:59:11Z requestId=tr-5898340 level=DEBUG function=profile_service message="instance=\"profile-7\" pod=\"profile-ec42\" region=\"us-east-2\" resource_id=\"account_49319\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"25\" correlation_key=\"l.reed48@gmail.com\""
- 2026-09-30T11:59:14Z requestId=tr-7736410 level=DEBUG function=profile_service message="instance=\"profile-1\" pod=\"profile-62d2\" region=\"us-east-2\" resource_id=\"account_58496\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"72\" correlation_key=\"hmercier3225@gmail.com\""
- 2026-09-30T11:59:14Z requestId=tr-8065160 level=DEBUG function=profile_service message="instance=\"profile-3\" pod=\"profile-53a2\" region=\"us-east-2\" resource_id=\"account_28621\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"77\" correlation_key=\"kwame.o3350@zoho.com\""
- 2026-09-30T11:59:17Z requestId=tr-9903230 level=DEBUG function=profile_service message="instance=\"profile-4\" pod=\"profile-ca32\" region=\"us-east-2\" resource_id=\"account_37798\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"41\" correlation_key=\"mokoena.lindiwe@gmail.com\""
- 2026-09-30T11:59:18Z requestId=tr-8364420 level=DEBUG function=profile_service message="instance=\"profile-2\" pod=\"profile-13c2\" region=\"us-east-2\" resource_id=\"account_69207\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"76\" correlation_key=\"n.elsayed36@gmail.com\""
- 2026-09-30T11:59:21Z requestId=tr-0202490 level=DEBUG function=profile_service message="instance=\"profile-3\" pod=\"profile-8a52\" region=\"us-east-2\" resource_id=\"account_78384\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"40\" correlation_key=\"iadeyemi3113@gmail.com\""
- 2026-09-30T11:59:21Z requestId=tr-0531240 level=DEBUG function=profile_service message="instance=\"profile-5\" pod=\"profile-7b22\" region=\"us-east-2\" resource_id=\"account_48509\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"45\" correlation_key=\"thiago.a3238@zoho.com\""
- 2026-09-30T11:59:24Z requestId=tr-2698060 level=DEBUG function=profile_service message="instance=\"profile-1\" pod=\"profile-e282\" region=\"us-east-2\" resource_id=\"account_27811\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"14\" correlation_key=\"elena-dvorak@proton.me\""
- 2026-09-30T11:59:24Z requestId=tr-2369310 level=DEBUG function=profile_service message="instance=\"profile-6\" pod=\"profile-f1b2\" region=\"us-east-2\" resource_id=\"account_57686\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"9\" correlation_key=\"menon.aditi@gmail.com\""
- 2026-09-30T11:59:28Z requestId=tr-2997320 level=DEBUG function=profile_service message="instance=\"profile-7\" pod=\"profile-a2a2\" region=\"us-east-2\" resource_id=\"account_68397\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"13\" correlation_key=\"louis.m3126@zoho.com\""
- 2026-09-30T11:59:31Z requestId=tr-4835390 level=DEBUG function=profile_service message="instance=\"profile-1\" pod=\"profile-1932\" region=\"us-east-2\" resource_id=\"account_77574\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"60\" correlation_key=\"holm.maja@gmail.com\""
- 2026-09-30T11:59:31Z requestId=tr-5164140 level=DEBUG function=profile_service message="instance=\"profile-3\" pod=\"profile-0a02\" region=\"us-east-2\" resource_id=\"account_47699\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"65\" correlation_key=\"mandla-mokoena@proton.me\""
- 2026-09-30T11:59:34Z requestId=tr-7002210 level=DEBUG function=profile_service message="instance=\"profile-4\" pod=\"profile-8092\" region=\"us-east-2\" resource_id=\"account_56876\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"29\" correlation_key=\"keiko.watanabe@gmail.com\""
- 2026-09-30T11:59:34Z requestId=tr-7330960 level=DEBUG function=profile_service message="instance=\"profile-6\" pod=\"profile-7162\" region=\"us-east-2\" resource_id=\"account_27001\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"34\" correlation_key=\"n.parker30@yahoo.com\""
- 2026-09-30T11:59:38Z requestId=tr-7630220 level=DEBUG function=profile_service message="instance=\"profile-5\" pod=\"profile-3182\" region=\"us-east-2\" resource_id=\"account_67587\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"33\" correlation_key=\"diya-menon@proton.me\""
- 2026-09-30T11:59:41Z requestId=tr-9797040 level=DEBUG function=profile_service message="instance=\"profile-1\" pod=\"profile-98e2\" region=\"us-east-2\" resource_id=\"account_46889\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"85\" correlation_key=\"s.najjar18@yahoo.com\""
- 2026-09-30T11:59:41Z requestId=tr-9468290 level=DEBUG function=profile_service message="instance=\"profile-6\" pod=\"profile-a812\" region=\"us-east-2\" resource_id=\"account_76764\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"80\" correlation_key=\"valeria.rodriguez@gmail.com\""
- 2026-09-30T11:59:44Z requestId=tr-1635110 level=DEBUG function=profile_service message="instance=\"profile-2\" pod=\"profile-0f72\" region=\"us-east-2\" resource_id=\"account_56066\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"49\" correlation_key=\"aokafor0795@fastmail.com\""
- 2026-09-30T11:59:44Z requestId=tr-1963860 level=DEBUG function=profile_service message="instance=\"profile-4\" pod=\"profile-0042\" region=\"us-east-2\" resource_id=\"account_26191\" event=\"profile_lookup_completed\" rows=\"1\" http_status=\"200\" duration_ms=\"54\" correlation_key=\"lucas.r920@outlook.com\""

#### evidence_54
### customer_accounts_failover_replica_20260902.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_accounts_failover_replica_20260902.sql
bytes: 2077
CREATE_TABLE: ['CREATE TABLE customer_profiles_failover_replica', 'CREATE TABLE customer_profiles_primary']
sample_INSERT: ['INSERT INTO "customer_profiles_failover_replica" VALUES(\'account_005\',\'user_05\',\'Leila Haddad\',\'leila.haddad@yahoo.com\',\'+212 6 48 27 15 93\',\'ACTIVE\',\'2026-09-02T22:45:00Z\');', 'INSERT INTO "customer_profiles_failover_replica" VALUES(\'account_8741\',\'user_8741\',\'Karim El-Masri\',\'karim.elmasri@gmail.com\',\'+971 50 731 6284\',\'ACTIVE\',\'2026-09-02T22:45:00Z\');', 'INSERT INTO "customer_profiles_failover_replica" VALUES(\'account_9116\',\'user_9116\',\'Mateo Rios Gil\',\'m.rios.gil@outlook.com\',\'+34 628 491 736\',\'ACTIVE\',\'2026-09-02T22:45:00Z\');']

#### evidence_55
### security_retention_extract.pdf
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\documents\security_retention_extract.pdf
bytes: 64847
PDF_INSPECTION_ERROR: No module named 'pdfplumber'

#### evidence_56
### customer_analytics_report_20260907.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_analytics_report_20260907.json
bytes: 1404
top_level_type: dict
top_level_keys: ['captured_at', 'source', 'collection', 'records']
sample: {'captured_at': '2026-09-07T09:45:00Z', 'source': 'analytics_identity_store', 'collection': 'customer_analytics_reports', 'records': [{'resource_id': 'analytics_901', 'user_id': None, 'email': None, 'phone': None, 'email_hash': None, 'reporting_window': 'last_90_days', 'metrics': {'sessions_30d': 11, 'products_viewed_30d': 24, 'orders_completed_90d': 2, 'revenue_90d_usd': 146.8}, 'recent_activity': [{'event': 'product_viewed', 'product': 'Travel backpack'}, {'event': 'purchase_completed', 'product': 'Travel backpack', 'quantity': 1}]}, {'resource_id': 'analytics_824', 'user_id': 'user_824', 'e…

#### evidence_57
### customer_search_primary_20260910.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_search_primary_20260910.sql
bytes: 838
CREATE_TABLE: ['CREATE TABLE search_documents_primary']
sample_INSERT: ['INSERT INTO "search_documents_primary" VALUES(\'search_001\',\'Jonas Berg\',\'jonas.berg@outlook.com\',\'account_006\',\'2026-09-09T22:12:00Z\');', 'INSERT INTO "search_documents_primary" VALUES(\'search_8814\',\'Jonas Berglund\',\'jonas.berglund@outlook.com\',\'account_8814\',\'2026-09-09T22:13:00Z\');', 'INSERT INTO "search_documents_primary" VALUES(\'search_4203\',\'Joana Berg\',\'joana.berg@outlook.com\',\'account_4203\',\'2026-09-09T22:13:00Z\');']

#### evidence_58
### delivery_correction_attachment.pdf
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\documents\delivery_correction_attachment.pdf
bytes: 66039
PDF_INSPECTION_ERROR: No module named 'pdfplumber'

#### evidence_59
### customer_export_jobs_20260914.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\customer_export_jobs_20260914.json
bytes: 848
top_level_type: dict
top_level_keys: ['captured_at', 'source', 'collection', 'records']
sample: {'captured_at': '2026-09-14T15:40:00Z', 'source': 'user_export_store', 'collection': 'customer_export_jobs', 'records': [{'resource_id': 'export_001', 'owner_email': 'gabriel.costa@proton.me', 'file_name': 'customer_export_001.zip', 'created_at': '2026-08-04T16:11:00Z', 'expires_at': '2026-10-04T16:11:00Z', 'download_available': True, 'included_sections': ['profile', 'orders', 'saved_addresses']}, {'resource_id': 'export_843', 'owner_email': 'aoi-tanaka@gmail.com', 'file_name': 'customer_export_843.zip', 'created_at': '2026-05-10T09:02:00Z', 'expires_at': '2026-06-10T09:02:00Z', 'download_avai…

#### evidence_60
### marketing_profile_console.png
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\images\marketing_profile_console.png
bytes: 129711
IMAGE_INSPECTION_ERROR: No module named 'PIL'

#### evidence_61
### support_replica.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\support_replica.log
bytes: 1873
line_count: 10
first_20_lines:
- 2026-09-17T22:00:00Z level=DEBUG service=support_replica instance=support-eu-03 pod=replica-7c9f event=batch_started batch=rp-7718 source=legacy_contact_index cursor=884019
- 2026-09-17T22:00:02Z level=DEBUG service=support_replica instance=support-eu-03 pod=replica-7c9f trace_id=tr-rp-4104 event=contact_query_started lookup_key=customer4104@yahoo.com
- 2026-09-17T22:00:03Z level=INFO service=support_replica instance=support-eu-03 pod=replica-7c9f trace_id=tr-rp-4104 event=contact_query_completed resource_id=support_4104 rows=1 latency_ms=18
- 2026-09-17T22:00:04Z level=DEBUG service=support_replica instance=support-eu-03 pod=replica-7c9f trace_id=tr-rp-002 event=contact_query_started lookup_key=nadia.ionescu@yahoo.com source=legacy_contact_index
- 2026-09-17T22:00:05Z level=INFO service=support_replica instance=support-eu-03 pod=replica-7c9f trace_id=tr-rp-002 event=contact_query_completed resource_id=support_002 rows=1 latency_ms=23
- 2026-09-17T22:00:06Z level=WARN service=support_replica instance=support-eu-03 pod=replica-7c9f trace_id=tr-rp-002 event=deletion_marker_check resource_id=support_002 marker_found=false last_write=2026-09-07T10:01:00Z
- 2026-09-17T22:00:08Z level=ERROR service=attachment_preview instance=preview-eu-02 pod=preview-14ad event=thumbnail_failed resource_id=support_7731 reason=unsupported_media retry=false
- 2026-09-17T22:00:11Z level=INFO service=support_replica instance=support-eu-03 pod=replica-7c9f event=contact_query_completed resource_id=support_5914 lookup_key=nadia.popescu@yahoo.com rows=1 source=case_archive latency_ms=31
- 2026-09-17T22:00:15Z level=WARN service=queue_consumer instance=replica-eu-03 pod=replica-7c9f event=consumer_lag partition=2 lag=63
- 2026-09-17T22:00:19Z level=INFO service=support_replica instance=support-eu-03 pod=replica-7c9f event=checkpoint_saved batch=rp-7718 cursor=884022 rows_read=3
last_20_lines:
- 2026-09-17T22:00:00Z level=DEBUG service=support_replica instance=support-eu-03 pod=replica-7c9f event=batch_started batch=rp-7718 source=legacy_contact_index cursor=884019
- 2026-09-17T22:00:02Z level=DEBUG service=support_replica instance=support-eu-03 pod=replica-7c9f trace_id=tr-rp-4104 event=contact_query_started lookup_key=customer4104@yahoo.com
- 2026-09-17T22:00:03Z level=INFO service=support_replica instance=support-eu-03 pod=replica-7c9f trace_id=tr-rp-4104 event=contact_query_completed resource_id=support_4104 rows=1 latency_ms=18
- 2026-09-17T22:00:04Z level=DEBUG service=support_replica instance=support-eu-03 pod=replica-7c9f trace_id=tr-rp-002 event=contact_query_started lookup_key=nadia.ionescu@yahoo.com source=legacy_contact_index
- 2026-09-17T22:00:05Z level=INFO service=support_replica instance=support-eu-03 pod=replica-7c9f trace_id=tr-rp-002 event=contact_query_completed resource_id=support_002 rows=1 latency_ms=23
- 2026-09-17T22:00:06Z level=WARN service=support_replica instance=support-eu-03 pod=replica-7c9f trace_id=tr-rp-002 event=deletion_marker_check resource_id=support_002 marker_found=false last_write=2026-09-07T10:01:00Z
- 2026-09-17T22:00:08Z level=ERROR service=attachment_preview instance=preview-eu-02 pod=preview-14ad event=thumbnail_failed resource_id=support_7731 reason=unsupported_media retry=false
- 2026-09-17T22:00:11Z level=INFO service=support_replica instance=support-eu-03 pod=replica-7c9f event=contact_query_completed resource_id=support_5914 lookup_key=nadia.popescu@yahoo.com rows=1 source=case_archive latency_ms=31
- 2026-09-17T22:00:15Z level=WARN service=queue_consumer instance=replica-eu-03 pod=replica-7c9f event=consumer_lag partition=2 lag=63
- 2026-09-17T22:00:19Z level=INFO service=support_replica instance=support-eu-03 pod=replica-7c9f event=checkpoint_saved batch=rp-7718 cursor=884022 rows_read=3

#### evidence_62
### service_resource_export_20260129_114459.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\service_resource_export_20260129_114459.json
bytes: 10720
top_level_type: dict
top_level_keys: ['exported_at', 'region', 'service_exports', 'source']
sample: {'exported_at': '2026-01-29T11:44:59Z', 'region': 'global', 'service_exports': {'account_service': {'profile_lookups': [{'observed_at': '2026-01-29T09:08:49Z', 'profile': {'customer_reference': None, 'email': 'aarav.r528@outlook.com', 'email_hash': None, 'full_name': None, 'phone': None}, 'resource_id': 'account_2424', 'status_code': 200}, {'observed_at': '2026-01-29T11:44:14Z', 'profile': None, 'resource_id': 'account_470', 'status_code': 404}, {'observed_at': '2026-01-29T09:56:58Z', 'profile': {'customer_reference': None, 'email': 'o.walker6695@yahoo.com', 'email_hash': None, 'full_name': No…

#### evidence_63
### customer_data_inventory_20260213.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_inventory_20260213.sql
bytes: 5478
CREATE_TABLE: ['CREATE TABLE snapshot_scope', 'CREATE TABLE customer_profiles', 'CREATE TABLE customer_search_documents', 'CREATE TABLE customer_analytics_profiles', 'CREATE TABLE support_records', 'CREATE TABLE customer_exports', 'CREATE TABLE connector_subscriptions', 'CREATE TABLE backup_restore_entries', 'CREATE TABLE security_audit_records']
sample_INSERT: ["INSERT INTO snapshot_scope VALUES ('account_service', '2026-02-13T07:43:27Z');", "INSERT INTO snapshot_scope VALUES ('analytics_platform', '2026-02-13T07:43:27Z');", "INSERT INTO snapshot_scope VALUES ('backup_service', '2026-02-13T07:43:27Z');"]

#### evidence_64
### resource_lookup_trace_20260218_083911.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\resource_lookup_trace_20260218_083911.log
bytes: 11049
line_count: 54
first_20_lines:
- 2026-02-18T05:47:12Z level=INFO service=readback_collector event=export_started target_count=26 mode=point_in_time
- 2026-02-18T05:47:12Z level=DEBUG service=integration_service trace_id=rb-054712-001 event=connector_config_read_started resource_id=data_flow_3669 lookup_key=t.oliveira6897@gmail.com
- 2026-02-18T05:47:12Z level=INFO service=integration_service trace_id=rb-054712-001 event=connector_config_read_completed resource_id=data_flow_3669 enabled=true last_delivery_status=delivered connector_name=analytics_identity_bridge customer_email=t.oliveira6897@gmail.com customer_reference=null
- 2026-02-18T05:47:23Z level=DEBUG service=analytics_platform trace_id=rb-054723-002 event=analytics_profile_read_started resource_id=analytics_1575 lookup_key=eamponsah5039@fastmail.com
- 2026-02-18T05:47:23Z level=INFO service=analytics_platform trace_id=rb-054723-002 event=analytics_profile_read_completed resource_id=analytics_1575 customer_reference=null email=eamponsah5039@fastmail.com phone=null email_hash=null audience_cohort=returning_customer
- 2026-02-18T06:02:13Z level=DEBUG service=export_service trace_id=rb-060213-003 event=export_metadata_read_started resource_id=export_6406 lookup_key=eamponsah5039@fastmail.com
- 2026-02-18T06:02:13Z level=INFO service=export_service trace_id=rb-060213-003 event=export_metadata_read_completed resource_id=export_6406 available=true owner_email=eamponsah5039@fastmail.com object_key=exports/export_6406/customer_data.zip
- 2026-02-18T06:22:53Z level=DEBUG service=search_service trace_id=rb-062253-004 event=index_query_started resource_id=search_901 lookup_key=arthur.c5444@outlook.com
- 2026-02-18T06:22:53Z level=INFO service=search_service trace_id=rb-062253-004 event=index_query_completed resource_id=search_901 result=hit total_hits=1 index=customer_directory_v3 email=arthur.c5444@outlook.com customer_reference=null
- 2026-02-18T06:26:43Z level=DEBUG service=account_service trace_id=rb-062643-005 event=profile_lookup_started resource_id=account_5293 lookup_key=arthur.c5444@outlook.com
- 2026-02-18T06:26:43Z level=INFO service=account_service trace_id=rb-062643-005 event=profile_lookup_completed resource_id=account_5293 rows=1 http_status=200 customer_reference=null email=arthur.c5444@outlook.com phone=null
- 2026-02-18T06:44:21Z level=DEBUG service=support_platform trace_id=rb-064421-006 event=support_ticket_read_started resource_id=support_7973 lookup_key=rao.neel@gmail.com
- 2026-02-18T06:44:21Z level=INFO service=support_platform trace_id=rb-064421-006 event=support_ticket_read_completed resource_id=support_7973 customer_reference=null requester_name=null requester_email=rao.neel@gmail.com requester_phone=null
- 2026-02-18T06:45:22Z level=DEBUG service=analytics_platform trace_id=rb-064522-007 event=analytics_profile_read_started resource_id=analytics_7818 lookup_key=arthur.c5444@outlook.com
- 2026-02-18T06:45:22Z level=INFO service=analytics_platform trace_id=rb-064522-007 event=analytics_profile_read_completed resource_id=analytics_7818 customer_reference=null email=arthur.c5444@outlook.com phone=null email_hash=null audience_cohort=home_lifestyle
- 2026-02-18T06:47:34Z level=DEBUG service=support_platform trace_id=rb-064734-008 event=support_ticket_read_started resource_id=support_4364 lookup_key=t.oliveira6897@gmail.com
- 2026-02-18T06:47:34Z level=INFO service=support_platform trace_id=rb-064734-008 event=support_ticket_read_completed resource_id=support_4364 customer_reference=null requester_name=null requester_email=t.oliveira6897@gmail.com requester_phone=null
- 2026-02-18T06:54:06Z level=DEBUG service=search_service trace_id=rb-065406-009 event=index_query_started resource_id=search_9733 lookup_key=eamponsah5039@fastmail.com
- 2026-02-18T06:54:06Z level=INFO service=search_service trace_id=rb-065406-009 event=index_query_completed resource_id=search_9733 result=hit total_hits=1 index=customer_directory_v3 email=eamponsah5039@fastmail.com customer_reference=null
- 2026-02-18T06:55:54Z level=DEBUG service=security_service trace_id=rb-065554-010 event=audit_record_read_started resource_id=audit_record_5451 lookup_key=user_484
last_20_lines:
- 2026-02-18T07:48:34Z level=INFO service=search_service trace_id=rb-074834-017 event=index_query_completed resource_id=search_9931 result=hit total_hits=1 index=customer_directory_v3 email=saleh.mariam@icloud.com customer_reference=null
- 2026-02-18T07:57:06Z level=DEBUG service=account_service trace_id=rb-075706-018 event=profile_lookup_started resource_id=account_6654 lookup_key=i.zielinski8281@yahoo.com
- 2026-02-18T07:57:06Z level=INFO service=account_service trace_id=rb-075706-018 event=profile_lookup_completed resource_id=account_6654 rows=1 http_status=200 customer_reference=null email=i.zielinski8281@yahoo.com phone=null
- 2026-02-18T07:57:31Z level=DEBUG service=security_service trace_id=rb-075731-019 event=audit_record_read_started resource_id=audit_record_7073 lookup_key=user_489
- 2026-02-18T07:57:31Z level=INFO service=security_service trace_id=rb-075731-019 event=audit_record_read_completed resource_id=audit_record_7073 rows=1 subject_reference=user_489 event_code=SUBJECT_REQUEST_AUDITED retention_until=2033-12-31T23:59:59Z
- 2026-02-18T08:15:47Z level=DEBUG service=backup_service trace_id=rb-081547-020 event=restore_policy_read_started resource_id=backup_4600 lookup_key=t.oliveira6897@gmail.com
- 2026-02-18T08:15:47Z level=INFO service=backup_service trace_id=rb-081547-020 event=restore_policy_read_completed resource_id=backup_4600 archive_present=true restore_allowed=true archive_key=archive/customer-data/backup_4600.tar.zst customer_email=t.oliveira6897@gmail.com customer_reference=null
- 2026-02-18T08:26:31Z level=DEBUG service=support_platform trace_id=rb-082631-021 event=support_ticket_read_started resource_id=support_5361 lookup_key=arthur.c5444@outlook.com
- 2026-02-18T08:26:31Z level=INFO service=support_platform trace_id=rb-082631-021 event=support_ticket_read_completed resource_id=support_5361 customer_reference=null requester_name=null requester_email=arthur.c5444@outlook.com requester_phone=null
- 2026-02-18T08:27:20Z level=DEBUG service=support_platform trace_id=rb-082720-022 event=support_ticket_read_started resource_id=support_4247 lookup_key=saleh.mariam@icloud.com
- 2026-02-18T08:27:20Z level=INFO service=support_platform trace_id=rb-082720-022 event=support_ticket_read_completed resource_id=support_4247 customer_reference=null requester_name=null requester_email=saleh.mariam@icloud.com requester_phone=null
- 2026-02-18T08:36:10Z level=DEBUG service=search_service trace_id=rb-083610-023 event=index_query_started resource_id=search_4216 lookup_key=maja.lund@outlook.com
- 2026-02-18T08:36:10Z level=INFO service=search_service trace_id=rb-083610-023 event=index_query_completed resource_id=search_4216 result=hit total_hits=1 index=customer_directory_v3 email=maja.lund@outlook.com customer_reference=null
- 2026-02-18T08:36:51Z level=DEBUG service=search_service trace_id=rb-083651-024 event=index_query_started resource_id=search_3582 lookup_key=andres-castillo@gmail.com
- 2026-02-18T08:36:51Z level=INFO service=search_service trace_id=rb-083651-024 event=index_query_completed resource_id=search_3582 result=hit total_hits=1 index=customer_directory_v3 email=andres-castillo@gmail.com customer_reference=null
- 2026-02-18T08:39:05Z level=DEBUG service=analytics_platform trace_id=rb-083905-025 event=analytics_profile_read_started resource_id=analytics_1981 lookup_key=andres-castillo@gmail.com
- 2026-02-18T08:39:05Z level=INFO service=analytics_platform trace_id=rb-083905-025 event=analytics_profile_read_completed resource_id=analytics_1981 customer_reference=null email=andres-castillo@gmail.com phone=null email_hash=null audience_cohort=mobile_browser
- 2026-02-18T08:39:11Z level=DEBUG service=search_service trace_id=rb-083911-026 event=index_query_started resource_id=search_3426 lookup_key=i.zielinski8281@yahoo.com
- 2026-02-18T08:39:11Z level=INFO service=search_service trace_id=rb-083911-026 event=index_query_completed resource_id=search_3426 result=hit total_hits=1 index=customer_directory_v3 email=i.zielinski8281@yahoo.com customer_reference=null
- 2026-02-18T08:39:11Z level=INFO service=readback_collector event=export_completed queries=26 dropped=0

#### evidence_65
### service_resource_export_20260228_103637.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\service_resource_export_20260228_103637.json
bytes: 9689
top_level_type: dict
top_level_keys: ['exported_at', 'region', 'service_exports', 'source']
sample: {'exported_at': '2026-02-28T10:36:37Z', 'region': 'global', 'service_exports': {'account_service': {'profile_lookups': [{'observed_at': '2026-02-28T10:08:20Z', 'profile': None, 'resource_id': 'account_1698', 'status_code': 404}, {'observed_at': '2026-02-28T08:44:48Z', 'profile': None, 'resource_id': 'account_2437', 'status_code': 404}, {'observed_at': '2026-02-28T09:37:43Z', 'profile': None, 'resource_id': 'account_2480', 'status_code': 404}, {'observed_at': '2026-02-28T08:01:15Z', 'profile': {'customer_reference': None, 'email': 'n.ogunleye2679@yahoo.com', 'email_hash': None, 'full_name': Non…

#### evidence_66
### customer_data_inventory_20260310.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_inventory_20260310.sql
bytes: 6594
CREATE_TABLE: ['CREATE TABLE snapshot_scope', 'CREATE TABLE customer_profiles', 'CREATE TABLE customer_search_documents', 'CREATE TABLE customer_analytics_profiles', 'CREATE TABLE support_records', 'CREATE TABLE customer_exports', 'CREATE TABLE connector_subscriptions', 'CREATE TABLE backup_restore_entries', 'CREATE TABLE security_audit_records']
sample_INSERT: ["INSERT INTO snapshot_scope VALUES ('account_service', '2026-03-10T05:38:48Z');", "INSERT INTO snapshot_scope VALUES ('analytics_platform', '2026-03-10T05:38:48Z');", "INSERT INTO snapshot_scope VALUES ('backup_service', '2026-03-10T05:38:48Z');"]

#### evidence_67
### resource_lookup_trace_20260310_061801.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\resource_lookup_trace_20260310_061801.log
bytes: 548
line_count: 4
first_20_lines:
- 2026-03-10T06:18:01Z level=INFO service=readback_collector event=export_started target_count=1 mode=point_in_time
- 2026-03-10T06:18:01Z level=DEBUG service=account_service trace_id=rb-061801-001 event=profile_lookup_started resource_id=account_6523 lookup_key=leonie.g9352@outlook.com
- 2026-03-10T06:18:01Z level=INFO service=account_service trace_id=rb-061801-001 event=profile_lookup_completed resource_id=account_6523 rows=0 http_status=404
- 2026-03-10T06:18:01Z level=INFO service=readback_collector event=export_completed queries=1 dropped=0
last_20_lines:
- 2026-03-10T06:18:01Z level=INFO service=readback_collector event=export_started target_count=1 mode=point_in_time
- 2026-03-10T06:18:01Z level=DEBUG service=account_service trace_id=rb-061801-001 event=profile_lookup_started resource_id=account_6523 lookup_key=leonie.g9352@outlook.com
- 2026-03-10T06:18:01Z level=INFO service=account_service trace_id=rb-061801-001 event=profile_lookup_completed resource_id=account_6523 rows=0 http_status=404
- 2026-03-10T06:18:01Z level=INFO service=readback_collector event=export_completed queries=1 dropped=0

#### evidence_68
### service_resource_export_20260320_072349.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\service_resource_export_20260320_072349.json
bytes: 9296
top_level_type: dict
top_level_keys: ['exported_at', 'region', 'service_exports', 'source']
sample: {'exported_at': '2026-03-20T07:23:49Z', 'region': 'global', 'service_exports': {'account_service': {'profile_lookups': [{'observed_at': '2026-03-20T06:07:21Z', 'profile': None, 'resource_id': 'account_2420', 'status_code': 404}, {'observed_at': '2026-03-20T06:29:58Z', 'profile': None, 'resource_id': 'account_2696', 'status_code': 404}, {'observed_at': '2026-03-20T07:23:49Z', 'profile': {'customer_reference': None, 'email': 'y.nakamura42@yahoo.com', 'email_hash': None, 'full_name': None, 'phone': None}, 'resource_id': 'account_4204', 'status_code': 200}, {'observed_at': '2026-03-20T05:29:33Z', …

#### evidence_69
### customer_data_inventory_20260404.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_inventory_20260404.sql
bytes: 5765
CREATE_TABLE: ['CREATE TABLE snapshot_scope', 'CREATE TABLE customer_profiles', 'CREATE TABLE customer_search_documents', 'CREATE TABLE customer_analytics_profiles', 'CREATE TABLE support_records', 'CREATE TABLE customer_exports', 'CREATE TABLE connector_subscriptions', 'CREATE TABLE backup_restore_entries', 'CREATE TABLE security_audit_records']
sample_INSERT: ["INSERT INTO snapshot_scope VALUES ('account_service', '2026-04-04T10:04:19Z');", "INSERT INTO snapshot_scope VALUES ('analytics_platform', '2026-04-04T10:04:19Z');", "INSERT INTO snapshot_scope VALUES ('backup_service', '2026-04-04T10:04:19Z');"]

#### evidence_70
### resource_lookup_trace_20260414_054007.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\resource_lookup_trace_20260414_054007.log
bytes: 9886
line_count: 50
first_20_lines:
- 2026-04-14T02:50:49Z level=INFO service=readback_collector event=export_started target_count=24 mode=point_in_time
- 2026-04-14T02:50:49Z level=DEBUG service=analytics_platform trace_id=rb-025049-001 event=analytics_profile_read_started resource_id=analytics_3234 lookup_key=null
- 2026-04-14T02:50:49Z level=INFO service=analytics_platform trace_id=rb-025049-001 event=analytics_profile_read_completed resource_id=analytics_3234 customer_reference=null email=null phone=null email_hash=null audience_cohort=returning_customer
- 2026-04-14T03:19:12Z level=DEBUG service=analytics_platform trace_id=rb-031912-002 event=analytics_profile_read_started resource_id=analytics_9918 lookup_key=reed.hannah@icloud.com
- 2026-04-14T03:19:12Z level=INFO service=analytics_platform trace_id=rb-031912-002 event=analytics_profile_read_completed resource_id=analytics_9918 customer_reference=null email=reed.hannah@icloud.com phone=null email_hash=null audience_cohort=returning_customer
- 2026-04-14T03:26:36Z level=DEBUG service=account_service trace_id=rb-032636-003 event=profile_lookup_started resource_id=account_2854 lookup_key=n.mensah16@gmail.com
- 2026-04-14T03:26:36Z level=INFO service=account_service trace_id=rb-032636-003 event=profile_lookup_completed resource_id=account_2854 rows=0 http_status=404
- 2026-04-14T03:27:15Z level=DEBUG service=integration_service trace_id=rb-032715-004 event=connector_config_read_started resource_id=data_flow_2984 lookup_key=sami.h267897@zoho.com
- 2026-04-14T03:27:15Z level=INFO service=integration_service trace_id=rb-032715-004 event=connector_config_read_completed resource_id=data_flow_2984 enabled=true last_delivery_status=delivered connector_name=customer_events_connector customer_email=sami.h267897@zoho.com customer_reference=null
- 2026-04-14T03:29:14Z level=DEBUG service=integration_service trace_id=rb-032914-005 event=connector_config_read_started resource_id=data_flow_6090 lookup_key=reed.hannah@icloud.com
- 2026-04-14T03:29:14Z level=INFO service=integration_service trace_id=rb-032914-005 event=connector_config_read_completed resource_id=data_flow_6090 enabled=true last_delivery_status=delivered connector_name=support_profile_sync customer_email=reed.hannah@icloud.com customer_reference=null
- 2026-04-14T03:37:08Z level=DEBUG service=account_service trace_id=rb-033708-006 event=profile_lookup_started resource_id=account_8598 lookup_key=obinna.okafor@gmail.com
- 2026-04-14T03:37:08Z level=INFO service=account_service trace_id=rb-033708-006 event=profile_lookup_completed resource_id=account_8598 rows=0 http_status=404
- 2026-04-14T03:47:02Z level=DEBUG service=analytics_platform trace_id=rb-034702-007 event=analytics_profile_read_started resource_id=analytics_3651 lookup_key=rina-sato@gmail.com
- 2026-04-14T03:47:02Z level=INFO service=analytics_platform trace_id=rb-034702-007 event=analytics_profile_read_completed resource_id=analytics_3651 customer_reference=null email=rina-sato@gmail.com phone=null email_hash=null audience_cohort=returning_customer
- 2026-04-14T03:48:14Z level=DEBUG service=account_service trace_id=rb-034814-008 event=profile_lookup_started resource_id=account_6784 lookup_key=n.torres30@yahoo.com
- 2026-04-14T03:48:14Z level=INFO service=account_service trace_id=rb-034814-008 event=profile_lookup_completed resource_id=account_6784 rows=1 http_status=200 customer_reference=null email=n.torres30@yahoo.com phone=null
- 2026-04-14T03:48:23Z level=DEBUG service=account_service trace_id=rb-034823-009 event=profile_lookup_started resource_id=account_6246 lookup_key=joao.s192@outlook.com
- 2026-04-14T03:48:23Z level=INFO service=account_service trace_id=rb-034823-009 event=profile_lookup_completed resource_id=account_6246 rows=1 http_status=200 customer_reference=null email=joao.s192@outlook.com phone=null
- 2026-04-14T03:55:48Z level=DEBUG service=account_service trace_id=rb-035548-010 event=profile_lookup_started resource_id=account_976 lookup_key=jkim227380@gmail.com
last_20_lines:
- 2026-04-14T04:45:32Z level=INFO service=account_service trace_id=rb-044532-015 event=profile_lookup_completed resource_id=account_4001 rows=0 http_status=404
- 2026-04-14T04:54:02Z level=DEBUG service=analytics_platform trace_id=rb-045402-016 event=analytics_profile_read_started resource_id=analytics_9326 lookup_key=null
- 2026-04-14T04:54:02Z level=INFO service=analytics_platform trace_id=rb-045402-016 event=analytics_profile_read_completed resource_id=analytics_9326 customer_reference=null email=null phone=null email_hash=null audience_cohort=mobile_browser
- 2026-04-14T04:54:43Z level=DEBUG service=analytics_platform trace_id=rb-045443-017 event=analytics_profile_read_started resource_id=analytics_5779 lookup_key=null
- 2026-04-14T04:54:43Z level=INFO service=analytics_platform trace_id=rb-045443-017 event=analytics_profile_read_completed resource_id=analytics_5779 customer_reference=null email=null phone=null email_hash=null audience_cohort=returning_customer
- 2026-04-14T05:02:54Z level=DEBUG service=security_service trace_id=rb-050254-018 event=audit_record_read_started resource_id=audit_record_4489 lookup_key=user_378
- 2026-04-14T05:02:54Z level=INFO service=security_service trace_id=rb-050254-018 event=audit_record_read_completed resource_id=audit_record_4489 rows=1 subject_reference=user_378 event_code=SUBJECT_REQUEST_AUDITED retention_until=2033-12-31T23:59:59Z
- 2026-04-14T05:13:55Z level=DEBUG service=security_service trace_id=rb-051355-019 event=audit_record_read_started resource_id=audit_record_6359 lookup_key=user_373
- 2026-04-14T05:13:55Z level=INFO service=security_service trace_id=rb-051355-019 event=audit_record_read_completed resource_id=audit_record_6359 rows=1 subject_reference=user_373 event_code=IDENTITY_CHANGE_RECORDED retention_until=2034-09-30T23:59:59Z
- 2026-04-14T05:19:59Z level=DEBUG service=security_service trace_id=rb-051959-020 event=audit_record_read_started resource_id=audit_record_5137 lookup_key=user_372
- 2026-04-14T05:19:59Z level=INFO service=security_service trace_id=rb-051959-020 event=audit_record_read_completed resource_id=audit_record_5137 rows=1 subject_reference=user_372 event_code=PRIVACY_REQUEST_ACCEPTED retention_until=2032-06-30T23:59:59Z
- 2026-04-14T05:31:08Z level=DEBUG service=support_platform trace_id=rb-053108-021 event=support_ticket_read_started resource_id=support_475 lookup_key=ndlovu.ayanda78@gmail.com
- 2026-04-14T05:31:08Z level=INFO service=support_platform trace_id=rb-053108-021 event=support_ticket_read_completed resource_id=support_475 customer_reference=null requester_name=null requester_email=ndlovu.ayanda78@gmail.com requester_phone=null
- 2026-04-14T05:36:48Z level=DEBUG service=security_service trace_id=rb-053648-022 event=audit_record_read_started resource_id=audit_record_7312 lookup_key=user_376
- 2026-04-14T05:36:48Z level=INFO service=security_service trace_id=rb-053648-022 event=audit_record_read_completed resource_id=audit_record_7312 rows=1 subject_reference=user_376 event_code=SUBJECT_REQUEST_AUDITED retention_until=2033-12-31T23:59:59Z
- 2026-04-14T05:38:04Z level=DEBUG service=search_service trace_id=rb-053804-023 event=index_query_started resource_id=search_9124 lookup_key=joao.s192@outlook.com
- 2026-04-14T05:38:04Z level=INFO service=search_service trace_id=rb-053804-023 event=index_query_completed resource_id=search_9124 result=hit total_hits=1 index=customer_directory_v3 email=joao.s192@outlook.com customer_reference=null
- 2026-04-14T05:40:07Z level=DEBUG service=search_service trace_id=rb-054007-024 event=index_query_started resource_id=search_8171 lookup_key=reed.hannah@icloud.com
- 2026-04-14T05:40:07Z level=INFO service=search_service trace_id=rb-054007-024 event=index_query_completed resource_id=search_8171 result=hit total_hits=1 index=customer_directory_v3 email=reed.hannah@icloud.com customer_reference=null
- 2026-04-14T05:40:07Z level=INFO service=readback_collector event=export_completed queries=24 dropped=0

#### evidence_71
### service_resource_export_20260429_083222.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\service_resource_export_20260429_083222.json
bytes: 10005
top_level_type: dict
top_level_keys: ['exported_at', 'region', 'service_exports', 'source']
sample: {'exported_at': '2026-04-29T08:32:22Z', 'region': 'global', 'service_exports': {'account_service': {'profile_lookups': [{'observed_at': '2026-04-29T07:42:28Z', 'profile': None, 'resource_id': 'account_1949', 'status_code': 404}, {'observed_at': '2026-04-29T06:48:58Z', 'profile': None, 'resource_id': 'account_5059', 'status_code': 404}, {'observed_at': '2026-04-29T05:53:44Z', 'profile': None, 'resource_id': 'account_5214', 'status_code': 404}, {'observed_at': '2026-04-29T05:56:53Z', 'profile': None, 'resource_id': 'account_8834', 'status_code': 404}]}, 'analytics_platform': {'profiles': [{'audi…

#### evidence_72
### customer_data_inventory_20260504.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_inventory_20260504.sql
bytes: 6130
CREATE_TABLE: ['CREATE TABLE snapshot_scope', 'CREATE TABLE customer_profiles', 'CREATE TABLE customer_search_documents', 'CREATE TABLE customer_analytics_profiles', 'CREATE TABLE support_records', 'CREATE TABLE customer_exports', 'CREATE TABLE connector_subscriptions', 'CREATE TABLE backup_restore_entries', 'CREATE TABLE security_audit_records']
sample_INSERT: ["INSERT INTO snapshot_scope VALUES ('account_service', '2026-05-04T09:41:47Z');", "INSERT INTO snapshot_scope VALUES ('analytics_platform', '2026-05-04T09:41:47Z');", "INSERT INTO snapshot_scope VALUES ('backup_service', '2026-05-04T09:41:47Z');"]

#### evidence_73
### resource_lookup_trace_20260509_104353.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\resource_lookup_trace_20260509_104353.log
bytes: 13670
line_count: 68
first_20_lines:
- 2026-05-09T07:46:43Z level=INFO service=readback_collector event=export_started target_count=33 mode=point_in_time
- 2026-05-09T07:46:43Z level=DEBUG service=security_service trace_id=rb-074643-001 event=audit_record_read_started resource_id=audit_record_4466 lookup_key=user_322
- 2026-05-09T07:46:43Z level=INFO service=security_service trace_id=rb-074643-001 event=audit_record_read_completed resource_id=audit_record_4466 rows=1 subject_reference=user_322 event_code=IDENTITY_CHANGE_RECORDED retention_until=2034-09-30T23:59:59Z
- 2026-05-09T07:47:14Z level=DEBUG service=integration_service trace_id=rb-074714-002 event=connector_config_read_started resource_id=data_flow_2468 lookup_key=user_324
- 2026-05-09T07:47:14Z level=INFO service=integration_service trace_id=rb-074714-002 event=connector_config_read_completed resource_id=data_flow_2468 enabled=false last_delivery_status=stopped connector_name=search_profile_indexer customer_email=null customer_reference=user_324
- 2026-05-09T07:49:25Z level=DEBUG service=support_platform trace_id=rb-074925-003 event=support_ticket_read_started resource_id=support_1403 lookup_key=user_329
- 2026-05-09T07:49:25Z level=INFO service=support_platform trace_id=rb-074925-003 event=support_ticket_read_completed resource_id=support_1403 customer_reference=user_329 requester_name=null requester_email=null requester_phone=null
- 2026-05-09T07:55:18Z level=DEBUG service=account_service trace_id=rb-075518-004 event=profile_lookup_started resource_id=account_2917 lookup_key=kojo-addo@proton.me
- 2026-05-09T07:55:18Z level=INFO service=account_service trace_id=rb-075518-004 event=profile_lookup_completed resource_id=account_2917 rows=0 http_status=404
- 2026-05-09T08:13:45Z level=DEBUG service=integration_service trace_id=rb-081345-005 event=connector_config_read_started resource_id=data_flow_4769 lookup_key=user_322
- 2026-05-09T08:13:45Z level=INFO service=integration_service trace_id=rb-081345-005 event=connector_config_read_completed resource_id=data_flow_4769 enabled=false last_delivery_status=stopped connector_name=search_profile_indexer customer_email=null customer_reference=user_322
- 2026-05-09T08:14:05Z level=DEBUG service=security_service trace_id=rb-081405-006 event=audit_record_read_started resource_id=audit_record_461 lookup_key=user_325
- 2026-05-09T08:14:05Z level=INFO service=security_service trace_id=rb-081405-006 event=audit_record_read_completed resource_id=audit_record_461 rows=1 subject_reference=user_325 event_code=IDENTITY_CHANGE_RECORDED retention_until=2034-09-30T23:59:59Z
- 2026-05-09T08:15:29Z level=DEBUG service=account_service trace_id=rb-081529-007 event=profile_lookup_started resource_id=account_6814 lookup_key=jules.m080@outlook.com
- 2026-05-09T08:15:29Z level=INFO service=account_service trace_id=rb-081529-007 event=profile_lookup_completed resource_id=account_6814 rows=0 http_status=404
- 2026-05-09T08:22:47Z level=DEBUG service=analytics_platform trace_id=rb-082247-008 event=analytics_profile_read_started resource_id=analytics_671 lookup_key=diego-fernandez@gmail.com
- 2026-05-09T08:22:47Z level=INFO service=analytics_platform trace_id=rb-082247-008 event=analytics_profile_read_completed resource_id=analytics_671 customer_reference=null email=diego-fernandez@gmail.com phone=null email_hash=null audience_cohort=general_shopper
- 2026-05-09T08:27:31Z level=DEBUG service=security_service trace_id=rb-082731-009 event=audit_record_read_started resource_id=audit_record_6731 lookup_key=user_329
- 2026-05-09T08:27:31Z level=INFO service=security_service trace_id=rb-082731-009 event=audit_record_read_completed resource_id=audit_record_6731 rows=1 subject_reference=user_329 event_code=IDENTITY_CHANGE_RECORDED retention_until=2034-09-30T23:59:59Z
- 2026-05-09T08:30:55Z level=DEBUG service=search_service trace_id=rb-083055-010 event=index_query_started resource_id=search_049 lookup_key=astrid.andersson@outlook.com
last_20_lines:
- 2026-05-09T10:05:21Z level=INFO service=support_platform trace_id=rb-100521-024 event=support_ticket_read_completed resource_id=support_4851 customer_reference=null requester_name=null requester_email=gcarter216198@gmail.com requester_phone=null
- 2026-05-09T10:08:40Z level=DEBUG service=integration_service trace_id=rb-100840-025 event=connector_config_read_started resource_id=data_flow_4392 lookup_key=astrid.andersson@outlook.com
- 2026-05-09T10:08:40Z level=INFO service=integration_service trace_id=rb-100840-025 event=connector_config_read_completed resource_id=data_flow_4392 enabled=true last_delivery_status=delivered connector_name=analytics_identity_bridge customer_email=astrid.andersson@outlook.com customer_reference=null
- 2026-05-09T10:09:26Z level=DEBUG service=support_platform trace_id=rb-100926-026 event=support_ticket_read_started resource_id=support_305 lookup_key=user_324
- 2026-05-09T10:09:26Z level=INFO service=support_platform trace_id=rb-100926-026 event=support_ticket_read_completed resource_id=support_305 customer_reference=user_324 requester_name=null requester_email=null requester_phone=null
- 2026-05-09T10:16:21Z level=DEBUG service=search_service trace_id=rb-101621-027 event=index_query_started resource_id=search_4560 lookup_key=gcarter216198@gmail.com
- 2026-05-09T10:16:21Z level=INFO service=search_service trace_id=rb-101621-027 event=index_query_completed resource_id=search_4560 result=hit total_hits=1 index=customer_directory_v3 email=gcarter216198@gmail.com customer_reference=null
- 2026-05-09T10:23:23Z level=DEBUG service=analytics_platform trace_id=rb-102323-028 event=analytics_profile_read_started resource_id=analytics_9681 lookup_key=null
- 2026-05-09T10:23:23Z level=INFO service=analytics_platform trace_id=rb-102323-028 event=analytics_profile_read_completed resource_id=analytics_9681 customer_reference=null email=null phone=null email_hash=null audience_cohort=mobile_browser
- 2026-05-09T10:28:19Z level=DEBUG service=support_platform trace_id=rb-102819-029 event=support_ticket_read_started resource_id=support_7249 lookup_key=user_322
- 2026-05-09T10:28:19Z level=INFO service=support_platform trace_id=rb-102819-029 event=support_ticket_read_completed resource_id=support_7249 customer_reference=user_322 requester_name=null requester_email=null requester_phone=null
- 2026-05-09T10:29:49Z level=DEBUG service=account_service trace_id=rb-102949-030 event=profile_lookup_started resource_id=account_4606 lookup_key=R.COSTA04@GMAIL.COM
- 2026-05-09T10:29:49Z level=INFO service=account_service trace_id=rb-102949-030 event=profile_lookup_completed resource_id=account_4606 rows=0 http_status=404
- 2026-05-09T10:32:52Z level=DEBUG service=search_service trace_id=rb-103252-031 event=index_query_started resource_id=search_4054 lookup_key=aoi.i256693@zoho.com
- 2026-05-09T10:32:52Z level=INFO service=search_service trace_id=rb-103252-031 event=index_query_completed resource_id=search_4054 result=hit total_hits=1 index=customer_directory_v3 email=aoi.i256693@zoho.com customer_reference=null
- 2026-05-09T10:33:02Z level=DEBUG service=analytics_platform trace_id=rb-103302-032 event=analytics_profile_read_started resource_id=analytics_2072 lookup_key=null
- 2026-05-09T10:33:02Z level=INFO service=analytics_platform trace_id=rb-103302-032 event=analytics_profile_read_completed resource_id=analytics_2072 customer_reference=null email=null phone=null email_hash=null audience_cohort=mobile_browser
- 2026-05-09T10:43:53Z level=DEBUG service=search_service trace_id=rb-104353-033 event=index_query_started resource_id=search_5226 lookup_key=diego-fernandez@gmail.com
- 2026-05-09T10:43:53Z level=INFO service=search_service trace_id=rb-104353-033 event=index_query_completed resource_id=search_5226 result=hit total_hits=1 index=customer_directory_v3 email=diego-fernandez@gmail.com customer_reference=null
- 2026-05-09T10:43:53Z level=INFO service=readback_collector event=export_completed queries=33 dropped=0

#### evidence_74
### service_resource_export_20260514_114454.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\service_resource_export_20260514_114454.json
bytes: 9017
top_level_type: dict
top_level_keys: ['exported_at', 'region', 'service_exports', 'source']
sample: {'exported_at': '2026-05-14T11:44:54Z', 'region': 'global', 'service_exports': {'account_service': {'profile_lookups': [{'observed_at': '2026-05-14T10:01:23Z', 'profile': None, 'resource_id': 'account_2088', 'status_code': 404}, {'observed_at': '2026-05-14T09:36:10Z', 'profile': None, 'resource_id': 'account_591', 'status_code': 404}, {'observed_at': '2026-05-14T10:31:23Z', 'profile': None, 'resource_id': 'account_8264', 'status_code': 404}, {'observed_at': '2026-05-14T10:29:05Z', 'profile': None, 'resource_id': 'account_9354', 'status_code': 404}]}, 'analytics_platform': {'profiles': [{'audie…

#### evidence_75
### customer_data_inventory_20260524.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_inventory_20260524.sql
bytes: 6651
CREATE_TABLE: ['CREATE TABLE snapshot_scope', 'CREATE TABLE customer_profiles', 'CREATE TABLE customer_search_documents', 'CREATE TABLE customer_analytics_profiles', 'CREATE TABLE support_records', 'CREATE TABLE customer_exports', 'CREATE TABLE connector_subscriptions', 'CREATE TABLE backup_restore_entries', 'CREATE TABLE security_audit_records']
sample_INSERT: ["INSERT INTO snapshot_scope VALUES ('account_service', '2026-05-24T06:39:55Z');", "INSERT INTO snapshot_scope VALUES ('analytics_platform', '2026-05-24T06:39:55Z');", "INSERT INTO snapshot_scope VALUES ('backup_service', '2026-05-24T06:39:55Z');"]

#### evidence_76
### resource_lookup_trace_20260529_074313.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\resource_lookup_trace_20260529_074313.log
bytes: 9674
line_count: 48
first_20_lines:
- 2026-05-29T04:54:21Z level=INFO service=readback_collector event=export_started target_count=23 mode=point_in_time
- 2026-05-29T04:54:21Z level=DEBUG service=account_service trace_id=rb-045421-001 event=profile_lookup_started resource_id=account_285 lookup_key=t.zulu0697@yahoo.com
- 2026-05-29T04:54:21Z level=INFO service=account_service trace_id=rb-045421-001 event=profile_lookup_completed resource_id=account_285 rows=1 http_status=200 customer_reference=null email=t.zulu0697@yahoo.com phone=null
- 2026-05-29T05:22:37Z level=DEBUG service=support_platform trace_id=rb-052237-002 event=support_ticket_read_started resource_id=support_7432 lookup_key=soojin-cho@proton.me
- 2026-05-29T05:22:37Z level=INFO service=support_platform trace_id=rb-052237-002 event=support_ticket_read_completed resource_id=support_7432 customer_reference=null requester_name=null requester_email=soojin-cho@proton.me requester_phone=null
- 2026-05-29T05:26:36Z level=DEBUG service=search_service trace_id=rb-052636-003 event=index_query_started resource_id=search_3144 lookup_key=sofia.lopez@gmail.com
- 2026-05-29T05:26:36Z level=INFO service=search_service trace_id=rb-052636-003 event=index_query_completed resource_id=search_3144 result=hit total_hits=1 index=customer_directory_v3 email=sofia.lopez@gmail.com customer_reference=null
- 2026-05-29T05:36:24Z level=DEBUG service=backup_service trace_id=rb-053624-004 event=restore_policy_read_started resource_id=backup_1825 lookup_key=user_290
- 2026-05-29T05:36:24Z level=INFO service=backup_service trace_id=rb-053624-004 event=restore_policy_read_completed resource_id=backup_1825 archive_present=true restore_allowed=false archive_key=archive/customer-data/backup_1825.tar.zst customer_email=null customer_reference=user_290
- 2026-05-29T05:42:55Z level=DEBUG service=integration_service trace_id=rb-054255-005 event=connector_config_read_started resource_id=data_flow_179 lookup_key=sofia.lopez@gmail.com
- 2026-05-29T05:42:55Z level=INFO service=integration_service trace_id=rb-054255-005 event=connector_config_read_completed resource_id=data_flow_179 enabled=true last_delivery_status=delivered connector_name=search_profile_indexer customer_email=sofia.lopez@gmail.com customer_reference=null
- 2026-05-29T05:46:12Z level=DEBUG service=security_service trace_id=rb-054612-006 event=audit_record_read_started resource_id=audit_record_1714 lookup_key=user_284
- 2026-05-29T05:46:12Z level=INFO service=security_service trace_id=rb-054612-006 event=audit_record_read_completed resource_id=audit_record_1714 rows=1 subject_reference=user_284 event_code=ACCOUNT_DELETION_RECORDED retention_until=2031-12-31T23:59:59Z
- 2026-05-29T05:49:15Z level=DEBUG service=export_service trace_id=rb-054915-007 event=export_metadata_read_started resource_id=export_7906 lookup_key=mrodrigues956378@fastmail.com
- 2026-05-29T05:49:15Z level=INFO service=export_service trace_id=rb-054915-007 event=export_metadata_read_completed resource_id=export_7906 available=true owner_email=mrodrigues956378@fastmail.com object_key=exports/export_7906/customer_data.zip
- 2026-05-29T05:54:49Z level=DEBUG service=integration_service trace_id=rb-055449-008 event=connector_config_read_started resource_id=data_flow_5598 lookup_key=user_290
- 2026-05-29T05:54:49Z level=INFO service=integration_service trace_id=rb-055449-008 event=connector_config_read_completed resource_id=data_flow_5598 enabled=false last_delivery_status=stopped connector_name=search_profile_indexer customer_email=null customer_reference=user_290
- 2026-05-29T06:00:28Z level=DEBUG service=analytics_platform trace_id=rb-060028-009 event=analytics_profile_read_started resource_id=analytics_7283 lookup_key=null
- 2026-05-29T06:00:28Z level=INFO service=analytics_platform trace_id=rb-060028-009 event=analytics_profile_read_completed resource_id=analytics_7283 customer_reference=null email=null phone=null email_hash=null audience_cohort=general_shopper
- 2026-05-29T06:03:36Z level=DEBUG service=analytics_platform trace_id=rb-060336-010 event=analytics_profile_read_started resource_id=analytics_2322 lookup_key=null
last_20_lines:
- 2026-05-29T06:39:38Z level=INFO service=search_service trace_id=rb-063938-014 event=index_query_completed resource_id=search_036 result=hit total_hits=1 index=customer_directory_v3 email=t.zulu0697@yahoo.com customer_reference=null
- 2026-05-29T06:46:09Z level=DEBUG service=integration_service trace_id=rb-064609-015 event=connector_config_read_started resource_id=data_flow_6953 lookup_key=kofi.appiah96@outlook.com
- 2026-05-29T06:46:09Z level=INFO service=integration_service trace_id=rb-064609-015 event=connector_config_read_completed resource_id=data_flow_6953 enabled=true last_delivery_status=delivered connector_name=analytics_identity_bridge customer_email=kofi.appiah96@outlook.com customer_reference=null
- 2026-05-29T06:48:53Z level=DEBUG service=security_service trace_id=rb-064853-016 event=audit_record_read_started resource_id=audit_record_3432 lookup_key=user_290
- 2026-05-29T06:48:53Z level=INFO service=security_service trace_id=rb-064853-016 event=audit_record_read_completed resource_id=audit_record_3432 rows=1 subject_reference=user_290 event_code=PRIVACY_REQUEST_ACCEPTED retention_until=2032-06-30T23:59:59Z
- 2026-05-29T06:50:34Z level=DEBUG service=search_service trace_id=rb-065034-017 event=index_query_started resource_id=search_5705 lookup_key=soojin-cho@proton.me
- 2026-05-29T06:50:34Z level=INFO service=search_service trace_id=rb-065034-017 event=index_query_completed resource_id=search_5705 result=hit total_hits=1 index=customer_directory_v3 email=soojin-cho@proton.me customer_reference=null
- 2026-05-29T07:10:16Z level=DEBUG service=account_service trace_id=rb-071016-018 event=profile_lookup_started resource_id=account_1125 lookup_key=laurent.camille@gmail.com
- 2026-05-29T07:10:16Z level=INFO service=account_service trace_id=rb-071016-018 event=profile_lookup_completed resource_id=account_1125 rows=0 http_status=404
- 2026-05-29T07:26:53Z level=DEBUG service=integration_service trace_id=rb-072653-019 event=connector_config_read_started resource_id=data_flow_743 lookup_key=ananya.i7482@zoho.com
- 2026-05-29T07:26:53Z level=INFO service=integration_service trace_id=rb-072653-019 event=connector_config_read_completed resource_id=data_flow_743 enabled=true last_delivery_status=delivered connector_name=search_profile_indexer customer_email=ananya.i7482@zoho.com customer_reference=null
- 2026-05-29T07:28:05Z level=DEBUG service=security_service trace_id=rb-072805-020 event=audit_record_read_started resource_id=audit_record_5680 lookup_key=user_281
- 2026-05-29T07:28:05Z level=INFO service=security_service trace_id=rb-072805-020 event=audit_record_read_completed resource_id=audit_record_5680 rows=1 subject_reference=user_281 event_code=PRIVACY_REQUEST_ACCEPTED retention_until=2032-06-30T23:59:59Z
- 2026-05-29T07:37:13Z level=DEBUG service=support_platform trace_id=rb-073713-021 event=support_ticket_read_started resource_id=support_1526 lookup_key=user_290
- 2026-05-29T07:37:13Z level=INFO service=support_platform trace_id=rb-073713-021 event=support_ticket_read_completed resource_id=support_1526 customer_reference=user_290 requester_name=null requester_email=null requester_phone=null
- 2026-05-29T07:38:43Z level=DEBUG service=account_service trace_id=rb-073843-022 event=profile_lookup_started resource_id=account_947 lookup_key=amara.o9968@outlook.com
- 2026-05-29T07:38:43Z level=INFO service=account_service trace_id=rb-073843-022 event=profile_lookup_completed resource_id=account_947 rows=0 http_status=404
- 2026-05-29T07:43:13Z level=DEBUG service=account_service trace_id=rb-074313-023 event=profile_lookup_started resource_id=account_2016 lookup_key=yamamoto.keiko@icloud.com
- 2026-05-29T07:43:13Z level=INFO service=account_service trace_id=rb-074313-023 event=profile_lookup_completed resource_id=account_2016 rows=0 http_status=404
- 2026-05-29T07:43:13Z level=INFO service=readback_collector event=export_completed queries=23 dropped=0

#### evidence_77
### service_resource_export_20260603_083457.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\service_resource_export_20260603_083457.json
bytes: 9775
top_level_type: dict
top_level_keys: ['exported_at', 'region', 'service_exports', 'source']
sample: {'exported_at': '2026-06-03T08:34:57Z', 'region': 'global', 'service_exports': {'account_service': {'profile_lookups': [{'observed_at': '2026-06-03T08:02:40Z', 'profile': None, 'resource_id': 'account_4853', 'status_code': 404}, {'observed_at': '2026-06-03T08:09:19Z', 'profile': None, 'resource_id': 'account_6575', 'status_code': 404}, {'observed_at': '2026-06-03T06:44:31Z', 'profile': None, 'resource_id': 'account_731', 'status_code': 404}, {'observed_at': '2026-06-03T07:22:52Z', 'profile': {'customer_reference': None, 'email': 'h.mori78@yahoo.com', 'email_hash': None, 'full_name': None, 'pho…

#### evidence_78
### customer_data_inventory_20260618.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_inventory_20260618.sql
bytes: 5831
CREATE_TABLE: ['CREATE TABLE snapshot_scope', 'CREATE TABLE customer_profiles', 'CREATE TABLE customer_search_documents', 'CREATE TABLE customer_analytics_profiles', 'CREATE TABLE support_records', 'CREATE TABLE customer_exports', 'CREATE TABLE connector_subscriptions', 'CREATE TABLE backup_restore_entries', 'CREATE TABLE security_audit_records']
sample_INSERT: ["INSERT INTO snapshot_scope VALUES ('account_service', '2026-06-18T11:44:03Z');", "INSERT INTO snapshot_scope VALUES ('analytics_platform', '2026-06-18T11:44:03Z');", "INSERT INTO snapshot_scope VALUES ('export_service', '2026-06-18T11:44:03Z');"]

#### evidence_79
### resource_lookup_trace_20260623_053726.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\resource_lookup_trace_20260623_053726.log
bytes: 12074
line_count: 60
first_20_lines:
- 2026-06-23T02:45:15Z level=INFO service=readback_collector event=export_started target_count=29 mode=point_in_time
- 2026-06-23T02:45:15Z level=DEBUG service=analytics_platform trace_id=rb-024515-001 event=analytics_profile_read_started resource_id=analytics_1964 lookup_key=null
- 2026-06-23T02:45:15Z level=INFO service=analytics_platform trace_id=rb-024515-001 event=analytics_profile_read_completed resource_id=analytics_1964 customer_reference=null email=null phone=null email_hash=null audience_cohort=mobile_browser
- 2026-06-23T02:47:51Z level=DEBUG service=account_service trace_id=rb-024751-002 event=profile_lookup_started resource_id=account_2838 lookup_key=daniel-parker@proton.me
- 2026-06-23T02:47:51Z level=INFO service=account_service trace_id=rb-024751-002 event=profile_lookup_completed resource_id=account_2838 rows=0 http_status=404
- 2026-06-23T02:48:26Z level=DEBUG service=security_service trace_id=rb-024826-003 event=audit_record_read_started resource_id=audit_record_8350 lookup_key=user_231
- 2026-06-23T02:48:26Z level=INFO service=security_service trace_id=rb-024826-003 event=audit_record_read_completed resource_id=audit_record_8350 rows=1 subject_reference=user_231 event_code=SUBJECT_REQUEST_AUDITED retention_until=2033-12-31T23:59:59Z
- 2026-06-23T02:59:55Z level=DEBUG service=search_service trace_id=rb-025955-004 event=index_query_started resource_id=search_5659 lookup_key=oskar.n737097@zoho.com
- 2026-06-23T02:59:55Z level=INFO service=search_service trace_id=rb-025955-004 event=index_query_completed resource_id=search_5659 result=hit total_hits=1 index=customer_directory_v3 email=oskar.n737097@zoho.com customer_reference=null
- 2026-06-23T03:00:12Z level=DEBUG service=backup_service trace_id=rb-030012-005 event=restore_policy_read_started resource_id=backup_2775 lookup_key=user_233
- 2026-06-23T03:00:12Z level=INFO service=backup_service trace_id=rb-030012-005 event=restore_policy_read_completed resource_id=backup_2775 archive_present=true restore_allowed=false archive_key=archive/customer-data/backup_2775.tar.zst customer_email=null customer_reference=user_233
- 2026-06-23T03:00:52Z level=DEBUG service=integration_service trace_id=rb-030052-006 event=connector_config_read_started resource_id=data_flow_4475 lookup_key=pavel.nowak98@gmail.com
- 2026-06-23T03:00:52Z level=INFO service=integration_service trace_id=rb-030052-006 event=connector_config_read_completed resource_id=data_flow_4475 enabled=true last_delivery_status=delivered connector_name=analytics_identity_bridge customer_email=pavel.nowak98@gmail.com customer_reference=null
- 2026-06-23T03:12:04Z level=DEBUG service=support_platform trace_id=rb-031204-007 event=support_ticket_read_started resource_id=support_9670 lookup_key=user_231
- 2026-06-23T03:12:04Z level=INFO service=support_platform trace_id=rb-031204-007 event=support_ticket_read_completed resource_id=support_9670 customer_reference=user_231 requester_name=null requester_email=null requester_phone=null
- 2026-06-23T03:15:07Z level=DEBUG service=search_service trace_id=rb-031507-008 event=index_query_started resource_id=search_2433 lookup_key=p.kapoor94@yahoo.com
- 2026-06-23T03:15:07Z level=INFO service=search_service trace_id=rb-031507-008 event=index_query_completed resource_id=search_2433 result=hit total_hits=1 index=customer_directory_v3 email=p.kapoor94@yahoo.com customer_reference=null
- 2026-06-23T03:28:05Z level=DEBUG service=account_service trace_id=rb-032805-009 event=profile_lookup_started resource_id=account_886 lookup_key=haeun.h9856@outlook.com
- 2026-06-23T03:28:05Z level=INFO service=account_service trace_id=rb-032805-009 event=profile_lookup_completed resource_id=account_886 rows=0 http_status=404
- 2026-06-23T03:30:57Z level=DEBUG service=analytics_platform trace_id=rb-033057-010 event=analytics_profile_read_started resource_id=analytics_6723 lookup_key=null
last_20_lines:
- 2026-06-23T04:42:25Z level=INFO service=search_service trace_id=rb-044225-020 event=index_query_completed resource_id=search_2615 result=hit total_hits=1 index=customer_directory_v3 email=kmori1937@gmail.com customer_reference=null
- 2026-06-23T05:06:03Z level=DEBUG service=support_platform trace_id=rb-050603-021 event=support_ticket_read_started resource_id=support_9391 lookup_key=user_233
- 2026-06-23T05:06:03Z level=INFO service=support_platform trace_id=rb-050603-021 event=support_ticket_read_completed resource_id=support_9391 customer_reference=user_233 requester_name=null requester_email=null requester_phone=null
- 2026-06-23T05:10:14Z level=DEBUG service=search_service trace_id=rb-051014-022 event=index_query_started resource_id=search_2904 lookup_key=pavel.nowak98@gmail.com
- 2026-06-23T05:10:14Z level=INFO service=search_service trace_id=rb-051014-022 event=index_query_completed resource_id=search_2904 result=hit total_hits=1 index=customer_directory_v3 email=pavel.nowak98@gmail.com customer_reference=null
- 2026-06-23T05:12:38Z level=DEBUG service=support_platform trace_id=rb-051238-023 event=support_ticket_read_started resource_id=support_1254 lookup_key=kmori1937@gmail.com
- 2026-06-23T05:12:38Z level=INFO service=support_platform trace_id=rb-051238-023 event=support_ticket_read_completed resource_id=support_1254 customer_reference=null requester_name=null requester_email=kmori1937@gmail.com requester_phone=null
- 2026-06-23T05:15:38Z level=DEBUG service=integration_service trace_id=rb-051538-024 event=connector_config_read_started resource_id=data_flow_4568 lookup_key=oskar.n737097@zoho.com
- 2026-06-23T05:15:38Z level=INFO service=integration_service trace_id=rb-051538-024 event=connector_config_read_completed resource_id=data_flow_4568 enabled=true last_delivery_status=delivered connector_name=customer_events_connector customer_email=oskar.n737097@zoho.com customer_reference=null
- 2026-06-23T05:15:55Z level=DEBUG service=integration_service trace_id=rb-051555-025 event=connector_config_read_started resource_id=data_flow_6754 lookup_key=user_231
- 2026-06-23T05:15:55Z level=INFO service=integration_service trace_id=rb-051555-025 event=connector_config_read_completed resource_id=data_flow_6754 enabled=false last_delivery_status=stopped connector_name=support_profile_sync customer_email=null customer_reference=user_231
- 2026-06-23T05:19:09Z level=DEBUG service=security_service trace_id=rb-051909-026 event=audit_record_read_started resource_id=audit_record_7103 lookup_key=user_233
- 2026-06-23T05:19:09Z level=INFO service=security_service trace_id=rb-051909-026 event=audit_record_read_completed resource_id=audit_record_7103 rows=1 subject_reference=user_233 event_code=PRIVACY_REQUEST_ACCEPTED retention_until=2032-06-30T23:59:59Z
- 2026-06-23T05:28:47Z level=DEBUG service=account_service trace_id=rb-052847-027 event=profile_lookup_started resource_id=account_945 lookup_key=romero.valeria94@icloud.com
- 2026-06-23T05:28:47Z level=INFO service=account_service trace_id=rb-052847-027 event=profile_lookup_completed resource_id=account_945 rows=0 http_status=404
- 2026-06-23T05:35:07Z level=DEBUG service=backup_service trace_id=rb-053507-028 event=restore_policy_read_started resource_id=backup_8162 lookup_key=user_231
- 2026-06-23T05:35:07Z level=INFO service=backup_service trace_id=rb-053507-028 event=restore_policy_read_completed resource_id=backup_8162 archive_present=true restore_allowed=false archive_key=archive/customer-data/backup_8162.tar.zst customer_email=null customer_reference=user_231
- 2026-06-23T05:37:26Z level=DEBUG service=integration_service trace_id=rb-053726-029 event=connector_config_read_started resource_id=data_flow_593 lookup_key=user_233
- 2026-06-23T05:37:26Z level=INFO service=integration_service trace_id=rb-053726-029 event=connector_config_read_completed resource_id=data_flow_593 enabled=false last_delivery_status=stopped connector_name=customer_events_connector customer_email=null customer_reference=user_233
- 2026-06-23T05:37:26Z level=INFO service=readback_collector event=export_completed queries=29 dropped=0

#### evidence_80
### service_resource_export_20260628_062556.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\service_resource_export_20260628_062556.json
bytes: 9028
top_level_type: dict
top_level_keys: ['exported_at', 'region', 'service_exports', 'source']
sample: {'exported_at': '2026-06-28T06:25:56Z', 'region': 'global', 'service_exports': {'account_service': {'profile_lookups': [{'observed_at': '2026-06-28T05:40:45Z', 'profile': None, 'resource_id': 'account_392', 'status_code': 404}, {'observed_at': '2026-06-28T04:18:09Z', 'profile': {'customer_reference': None, 'email': 'thiago.s4828@outlook.com', 'email_hash': None, 'full_name': None, 'phone': None}, 'resource_id': 'account_5479', 'status_code': 200}, {'observed_at': '2026-06-28T05:35:02Z', 'profile': None, 'resource_id': 'account_669', 'status_code': 404}, {'observed_at': '2026-06-28T06:25:56Z', …

#### evidence_81
### customer_data_inventory_20260703.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_inventory_20260703.sql
bytes: 6676
CREATE_TABLE: ['CREATE TABLE snapshot_scope', 'CREATE TABLE customer_profiles', 'CREATE TABLE customer_search_documents', 'CREATE TABLE customer_analytics_profiles', 'CREATE TABLE support_records', 'CREATE TABLE customer_exports', 'CREATE TABLE connector_subscriptions', 'CREATE TABLE backup_restore_entries', 'CREATE TABLE security_audit_records']
sample_INSERT: ["INSERT INTO snapshot_scope VALUES ('account_service', '2026-07-03T07:43:56Z');", "INSERT INTO snapshot_scope VALUES ('analytics_platform', '2026-07-03T07:43:56Z');", "INSERT INTO snapshot_scope VALUES ('backup_service', '2026-07-03T07:43:56Z');"]

#### evidence_82
### resource_lookup_trace_20260713_093359.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\resource_lookup_trace_20260713_093359.log
bytes: 10716
line_count: 54
first_20_lines:
- 2026-07-13T06:48:43Z level=INFO service=readback_collector event=export_started target_count=26 mode=point_in_time
- 2026-07-13T06:48:43Z level=DEBUG service=account_service trace_id=rb-064843-001 event=profile_lookup_started resource_id=account_2933 lookup_key=j.girard1079@yahoo.com
- 2026-07-13T06:48:43Z level=INFO service=account_service trace_id=rb-064843-001 event=profile_lookup_completed resource_id=account_2933 rows=1 http_status=200 customer_reference=null email=j.girard1079@yahoo.com phone=null
- 2026-07-13T06:53:09Z level=DEBUG service=account_service trace_id=rb-065309-002 event=profile_lookup_started resource_id=account_4320 lookup_key=a.sato96@gmail.com
- 2026-07-13T06:53:09Z level=INFO service=account_service trace_id=rb-065309-002 event=profile_lookup_completed resource_id=account_4320 rows=0 http_status=404
- 2026-07-13T07:05:05Z level=DEBUG service=security_service trace_id=rb-070505-003 event=audit_record_read_started resource_id=audit_record_1524 lookup_key=user_193
- 2026-07-13T07:05:05Z level=INFO service=security_service trace_id=rb-070505-003 event=audit_record_read_completed resource_id=audit_record_1524 rows=1 subject_reference=user_193 event_code=SUBJECT_REQUEST_AUDITED retention_until=2033-12-31T23:59:59Z
- 2026-07-13T07:13:44Z level=DEBUG service=integration_service trace_id=rb-071344-004 event=connector_config_read_started resource_id=data_flow_2310 lookup_key=grace.reed@outlook.com
- 2026-07-13T07:13:44Z level=INFO service=integration_service trace_id=rb-071344-004 event=connector_config_read_completed resource_id=data_flow_2310 enabled=true last_delivery_status=delivered connector_name=support_profile_sync customer_email=grace.reed@outlook.com customer_reference=null
- 2026-07-13T07:14:06Z level=DEBUG service=analytics_platform trace_id=rb-071406-005 event=analytics_profile_read_started resource_id=analytics_5166 lookup_key=null
- 2026-07-13T07:14:06Z level=INFO service=analytics_platform trace_id=rb-071406-005 event=analytics_profile_read_completed resource_id=analytics_5166 customer_reference=null email=null phone=null email_hash=null audience_cohort=mobile_browser
- 2026-07-13T07:20:27Z level=DEBUG service=account_service trace_id=rb-072027-006 event=profile_lookup_started resource_id=account_5599 lookup_key=kim.hyunwoo@gmail.com
- 2026-07-13T07:20:27Z level=INFO service=account_service trace_id=rb-072027-006 event=profile_lookup_completed resource_id=account_5599 rows=0 http_status=404
- 2026-07-13T07:24:22Z level=DEBUG service=search_service trace_id=rb-072422-007 event=index_query_started resource_id=search_7472 lookup_key=grace.reed@outlook.com
- 2026-07-13T07:24:22Z level=INFO service=search_service trace_id=rb-072422-007 event=index_query_completed resource_id=search_7472 result=hit total_hits=1 index=customer_directory_v3 email=grace.reed@outlook.com customer_reference=null
- 2026-07-13T07:25:54Z level=DEBUG service=integration_service trace_id=rb-072554-008 event=connector_config_read_started resource_id=data_flow_3195 lookup_key=lindiwe.ndlovu94@gmail.com
- 2026-07-13T07:25:54Z level=INFO service=integration_service trace_id=rb-072554-008 event=connector_config_read_completed resource_id=data_flow_3195 enabled=true last_delivery_status=delivered connector_name=search_profile_indexer customer_email=lindiwe.ndlovu94@gmail.com customer_reference=null
- 2026-07-13T07:39:16Z level=DEBUG service=search_service trace_id=rb-073916-009 event=index_query_started resource_id=search_9161 lookup_key=diego.t477299@outlook.com
- 2026-07-13T07:39:16Z level=INFO service=search_service trace_id=rb-073916-009 event=index_query_completed resource_id=search_9161 result=hit total_hits=1 index=customer_directory_v3 email=diego.t477299@outlook.com customer_reference=null
- 2026-07-13T07:43:22Z level=DEBUG service=account_service trace_id=rb-074322-010 event=profile_lookup_started resource_id=account_5547 lookup_key=dahl.astrid@icloud.com
last_20_lines:
- 2026-07-13T08:27:15Z level=INFO service=analytics_platform trace_id=rb-082715-017 event=analytics_profile_read_completed resource_id=analytics_3454 customer_reference=null email=null phone=null email_hash=null audience_cohort=home_lifestyle
- 2026-07-13T08:28:57Z level=DEBUG service=security_service trace_id=rb-082857-018 event=audit_record_read_started resource_id=audit_record_6389 lookup_key=user_194
- 2026-07-13T08:28:57Z level=INFO service=security_service trace_id=rb-082857-018 event=audit_record_read_completed resource_id=audit_record_6389 rows=1 subject_reference=user_194 event_code=IDENTITY_CHANGE_RECORDED retention_until=2034-09-30T23:59:59Z
- 2026-07-13T08:41:11Z level=DEBUG service=security_service trace_id=rb-084111-019 event=audit_record_read_started resource_id=audit_record_1839 lookup_key=user_191
- 2026-07-13T08:41:11Z level=INFO service=security_service trace_id=rb-084111-019 event=audit_record_read_completed resource_id=audit_record_1839 rows=1 subject_reference=user_191 event_code=ACCOUNT_DELETION_RECORDED retention_until=2031-12-31T23:59:59Z
- 2026-07-13T08:58:47Z level=DEBUG service=analytics_platform trace_id=rb-085847-020 event=analytics_profile_read_started resource_id=analytics_8037 lookup_key=null
- 2026-07-13T08:58:47Z level=INFO service=analytics_platform trace_id=rb-085847-020 event=analytics_profile_read_completed resource_id=analytics_8037 customer_reference=null email=null phone=null email_hash=null audience_cohort=mobile_browser
- 2026-07-13T09:08:17Z level=DEBUG service=analytics_platform trace_id=rb-090817-021 event=analytics_profile_read_started resource_id=analytics_349 lookup_key=null
- 2026-07-13T09:08:17Z level=INFO service=analytics_platform trace_id=rb-090817-021 event=analytics_profile_read_completed resource_id=analytics_349 customer_reference=null email=null phone=null email_hash=null audience_cohort=home_lifestyle
- 2026-07-13T09:09:52Z level=DEBUG service=support_platform trace_id=rb-090952-022 event=support_ticket_read_started resource_id=support_2863 lookup_key=j.girard1079@yahoo.com
- 2026-07-13T09:09:52Z level=INFO service=support_platform trace_id=rb-090952-022 event=support_ticket_read_completed resource_id=support_2863 customer_reference=null requester_name=null requester_email=j.girard1079@yahoo.com requester_phone=null
- 2026-07-13T09:10:03Z level=DEBUG service=search_service trace_id=rb-091003-023 event=index_query_started resource_id=search_1414 lookup_key=ijain6853@gmail.com
- 2026-07-13T09:10:03Z level=INFO service=search_service trace_id=rb-091003-023 event=index_query_completed resource_id=search_1414 result=hit total_hits=1 index=customer_directory_v3 email=ijain6853@gmail.com customer_reference=null
- 2026-07-13T09:13:20Z level=DEBUG service=support_platform trace_id=rb-091320-024 event=support_ticket_read_started resource_id=support_6131 lookup_key=ijain6853@gmail.com
- 2026-07-13T09:13:20Z level=INFO service=support_platform trace_id=rb-091320-024 event=support_ticket_read_completed resource_id=support_6131 customer_reference=null requester_name=null requester_email=ijain6853@gmail.com requester_phone=null
- 2026-07-13T09:20:12Z level=DEBUG service=account_service trace_id=rb-092012-025 event=profile_lookup_started resource_id=account_9917 lookup_key=diego.t477299@outlook.com
- 2026-07-13T09:20:12Z level=INFO service=account_service trace_id=rb-092012-025 event=profile_lookup_completed resource_id=account_9917 rows=1 http_status=200 customer_reference=null email=diego.t477299@outlook.com phone=null
- 2026-07-13T09:33:59Z level=DEBUG service=integration_service trace_id=rb-093359-026 event=connector_config_read_started resource_id=data_flow_5688 lookup_key=j.girard1079@yahoo.com
- 2026-07-13T09:33:59Z level=INFO service=integration_service trace_id=rb-093359-026 event=connector_config_read_completed resource_id=data_flow_5688 enabled=true last_delivery_status=delivered connector_name=support_profile_sync customer_email=j.girard1079@yahoo.com customer_reference=null
- 2026-07-13T09:33:59Z level=INFO service=readback_collector event=export_completed queries=26 dropped=0

#### evidence_83
### service_resource_export_20260718_104335.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\service_resource_export_20260718_104335.json
bytes: 11127
top_level_type: dict
top_level_keys: ['exported_at', 'region', 'service_exports', 'source']
sample: {'exported_at': '2026-07-18T10:43:35Z', 'region': 'global', 'service_exports': {'account_service': {'profile_lookups': [{'observed_at': '2026-07-18T09:33:26Z', 'profile': None, 'resource_id': 'account_4854', 'status_code': 404}, {'observed_at': '2026-07-18T10:24:53Z', 'profile': {'customer_reference': None, 'email': 'ethan.b9744@outlook.com', 'email_hash': None, 'full_name': None, 'phone': None}, 'resource_id': 'account_5375', 'status_code': 200}, {'observed_at': '2026-07-18T08:26:21Z', 'profile': {'customer_reference': None, 'email': 'l.berg82@yahoo.com', 'email_hash': None, 'full_name': None…

#### evidence_84
### customer_data_inventory_20260723.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_inventory_20260723.sql
bytes: 7046
CREATE_TABLE: ['CREATE TABLE snapshot_scope', 'CREATE TABLE customer_profiles', 'CREATE TABLE customer_search_documents', 'CREATE TABLE customer_analytics_profiles', 'CREATE TABLE support_records', 'CREATE TABLE customer_exports', 'CREATE TABLE connector_subscriptions', 'CREATE TABLE backup_restore_entries', 'CREATE TABLE security_audit_records']
sample_INSERT: ["INSERT INTO snapshot_scope VALUES ('account_service', '2026-07-23T11:43:30Z');", "INSERT INTO snapshot_scope VALUES ('analytics_platform', '2026-07-23T11:43:30Z');", "INSERT INTO snapshot_scope VALUES ('backup_service', '2026-07-23T11:43:30Z');"]

#### evidence_85
### resource_lookup_trace_20260728_054417.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\resource_lookup_trace_20260728_054417.log
bytes: 9098
line_count: 46
first_20_lines:
- 2026-07-28T02:49:32Z level=INFO service=readback_collector event=export_started target_count=22 mode=point_in_time
- 2026-07-28T02:49:32Z level=DEBUG service=search_service trace_id=rb-024932-001 event=index_query_started resource_id=search_5261 lookup_key=OBI.ADAEZE@ICLOUD.COM
- 2026-07-28T02:49:32Z level=INFO service=search_service trace_id=rb-024932-001 event=index_query_completed resource_id=search_5261 result=hit total_hits=1 index=customer_directory_v3 email=OBI.ADAEZE@ICLOUD.COM customer_reference=null
- 2026-07-28T02:51:36Z level=DEBUG service=support_platform trace_id=rb-025136-002 event=support_ticket_read_started resource_id=support_2322 lookup_key=menon.arjun@gmail.com
- 2026-07-28T02:51:36Z level=INFO service=support_platform trace_id=rb-025136-002 event=support_ticket_read_completed resource_id=support_2322 customer_reference=null requester_name=null requester_email=menon.arjun@gmail.com requester_phone=null
- 2026-07-28T02:52:12Z level=DEBUG service=account_service trace_id=rb-025212-003 event=profile_lookup_started resource_id=account_3064 lookup_key=n.farouk26@yahoo.com
- 2026-07-28T02:52:12Z level=INFO service=account_service trace_id=rb-025212-003 event=profile_lookup_completed resource_id=account_3064 rows=1 http_status=200 customer_reference=null email=n.farouk26@yahoo.com phone=null
- 2026-07-28T02:53:27Z level=DEBUG service=account_service trace_id=rb-025327-004 event=profile_lookup_started resource_id=account_5284 lookup_key=abena-frimpong@proton.me
- 2026-07-28T02:53:27Z level=INFO service=account_service trace_id=rb-025327-004 event=profile_lookup_completed resource_id=account_5284 rows=0 http_status=404
- 2026-07-28T02:57:10Z level=DEBUG service=analytics_platform trace_id=rb-025710-005 event=analytics_profile_read_started resource_id=analytics_6980 lookup_key=null
- 2026-07-28T02:57:10Z level=INFO service=analytics_platform trace_id=rb-025710-005 event=analytics_profile_read_completed resource_id=analytics_6980 customer_reference=null email=null phone=null email_hash=null audience_cohort=home_lifestyle
- 2026-07-28T03:36:54Z level=DEBUG service=analytics_platform trace_id=rb-033654-006 event=analytics_profile_read_started resource_id=analytics_6402 lookup_key=null
- 2026-07-28T03:36:54Z level=INFO service=analytics_platform trace_id=rb-033654-006 event=analytics_profile_read_completed resource_id=analytics_6402 customer_reference=null email=null phone=null email_hash=null audience_cohort=home_lifestyle
- 2026-07-28T03:38:41Z level=DEBUG service=export_service trace_id=rb-033841-007 event=export_metadata_read_started resource_id=export_4102 lookup_key=stshabalala9283@fastmail.com
- 2026-07-28T03:38:41Z level=INFO service=export_service trace_id=rb-033841-007 event=export_metadata_read_completed resource_id=export_4102 available=true owner_email=stshabalala9283@fastmail.com object_key=exports/export_4102/customer_data.zip
- 2026-07-28T03:41:20Z level=DEBUG service=search_service trace_id=rb-034120-008 event=index_query_started resource_id=search_2126 lookup_key=yuki.k7202@zoho.com
- 2026-07-28T03:41:20Z level=INFO service=search_service trace_id=rb-034120-008 event=index_query_completed resource_id=search_2126 result=hit total_hits=1 index=customer_directory_v3 email=yuki.k7202@zoho.com customer_reference=null
- 2026-07-28T03:44:08Z level=DEBUG service=security_service trace_id=rb-034408-009 event=audit_record_read_started resource_id=audit_record_3088 lookup_key=user_165
- 2026-07-28T03:44:08Z level=INFO service=security_service trace_id=rb-034408-009 event=audit_record_read_completed resource_id=audit_record_3088 rows=1 subject_reference=user_165 event_code=IDENTITY_CHANGE_RECORDED retention_until=2034-09-30T23:59:59Z
- 2026-07-28T03:52:52Z level=DEBUG service=analytics_platform trace_id=rb-035252-010 event=analytics_profile_read_started resource_id=analytics_2713 lookup_key=n.farouk26@yahoo.com
last_20_lines:
- 2026-07-28T04:24:19Z level=INFO service=integration_service trace_id=rb-042419-013 event=connector_config_read_completed resource_id=data_flow_7004 enabled=true last_delivery_status=delivered connector_name=analytics_identity_bridge customer_email=yuki.k7202@zoho.com customer_reference=null
- 2026-07-28T04:44:49Z level=DEBUG service=account_service trace_id=rb-044449-014 event=profile_lookup_started resource_id=account_9549 lookup_key=tomasz.stojanovic@outlook.com
- 2026-07-28T04:44:49Z level=INFO service=account_service trace_id=rb-044449-014 event=profile_lookup_completed resource_id=account_9549 rows=0 http_status=404
- 2026-07-28T04:56:58Z level=DEBUG service=account_service trace_id=rb-045658-015 event=profile_lookup_started resource_id=account_665 lookup_key=jihoon.jang@gmail.com
- 2026-07-28T04:56:58Z level=INFO service=account_service trace_id=rb-045658-015 event=profile_lookup_completed resource_id=account_665 rows=0 http_status=404
- 2026-07-28T05:02:50Z level=DEBUG service=search_service trace_id=rb-050250-016 event=index_query_started resource_id=search_8678 lookup_key=n.farouk26@yahoo.com
- 2026-07-28T05:02:50Z level=INFO service=search_service trace_id=rb-050250-016 event=index_query_completed resource_id=search_8678 result=hit total_hits=1 index=customer_directory_v3 email=n.farouk26@yahoo.com customer_reference=null
- 2026-07-28T05:03:37Z level=DEBUG service=support_platform trace_id=rb-050337-017 event=support_ticket_read_started resource_id=support_3155 lookup_key=OBI.ADAEZE@ICLOUD.COM
- 2026-07-28T05:03:37Z level=INFO service=support_platform trace_id=rb-050337-017 event=support_ticket_read_completed resource_id=support_3155 customer_reference=null requester_name=null requester_email=OBI.ADAEZE@ICLOUD.COM requester_phone=null
- 2026-07-28T05:03:55Z level=DEBUG service=support_platform trace_id=rb-050355-018 event=support_ticket_read_started resource_id=support_3586 lookup_key=n.farouk26@yahoo.com
- 2026-07-28T05:03:55Z level=INFO service=support_platform trace_id=rb-050355-018 event=support_ticket_read_completed resource_id=support_3586 customer_reference=null requester_name=null requester_email=n.farouk26@yahoo.com requester_phone=null
- 2026-07-28T05:04:52Z level=DEBUG service=backup_service trace_id=rb-050452-019 event=restore_policy_read_started resource_id=backup_5520 lookup_key=l.nascimento40@gmail.com
- 2026-07-28T05:04:52Z level=INFO service=backup_service trace_id=rb-050452-019 event=restore_policy_read_completed resource_id=backup_5520 archive_present=true restore_allowed=true archive_key=archive/customer-data/backup_5520.tar.zst customer_email=l.nascimento40@gmail.com customer_reference=null
- 2026-07-28T05:05:14Z level=DEBUG service=security_service trace_id=rb-050514-020 event=audit_record_read_started resource_id=audit_record_6780 lookup_key=user_162
- 2026-07-28T05:05:14Z level=INFO service=security_service trace_id=rb-050514-020 event=audit_record_read_completed resource_id=audit_record_6780 rows=1 subject_reference=user_162 event_code=SUBJECT_REQUEST_AUDITED retention_until=2033-12-31T23:59:59Z
- 2026-07-28T05:36:40Z level=DEBUG service=search_service trace_id=rb-053640-021 event=index_query_started resource_id=search_7102 lookup_key=menon.arjun@gmail.com
- 2026-07-28T05:36:40Z level=INFO service=search_service trace_id=rb-053640-021 event=index_query_completed resource_id=search_7102 result=hit total_hits=1 index=customer_directory_v3 email=menon.arjun@gmail.com customer_reference=null
- 2026-07-28T05:44:17Z level=DEBUG service=search_service trace_id=rb-054417-022 event=index_query_started resource_id=search_4509 lookup_key=erik.h9688@outlook.com
- 2026-07-28T05:44:17Z level=INFO service=search_service trace_id=rb-054417-022 event=index_query_completed resource_id=search_4509 result=hit total_hits=1 index=customer_directory_v3 email=erik.h9688@outlook.com customer_reference=null
- 2026-07-28T05:44:17Z level=INFO service=readback_collector event=export_completed queries=22 dropped=0

#### evidence_86
### service_resource_export_20260807_074104.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\service_resource_export_20260807_074104.json
bytes: 8619
top_level_type: dict
top_level_keys: ['exported_at', 'region', 'service_exports', 'source']
sample: {'exported_at': '2026-08-07T07:41:04Z', 'region': 'global', 'service_exports': {'account_service': {'profile_lookups': [{'observed_at': '2026-08-07T05:55:37Z', 'profile': None, 'resource_id': 'account_3897', 'status_code': 404}, {'observed_at': '2026-08-07T05:59:32Z', 'profile': None, 'resource_id': 'account_874', 'status_code': 404}, {'observed_at': '2026-08-07T07:39:36Z', 'profile': None, 'resource_id': 'account_8854', 'status_code': 404}]}, 'analytics_platform': {'profiles': [{'audience_cohort': 'mobile_browser', 'customer_reference': None, 'email': None, 'email_hash': None, 'observed_at': …

#### evidence_87
### customer_data_inventory_20260817.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_inventory_20260817.sql
bytes: 5967
CREATE_TABLE: ['CREATE TABLE snapshot_scope', 'CREATE TABLE customer_profiles', 'CREATE TABLE customer_search_documents', 'CREATE TABLE customer_analytics_profiles', 'CREATE TABLE support_records', 'CREATE TABLE customer_exports', 'CREATE TABLE connector_subscriptions', 'CREATE TABLE backup_restore_entries', 'CREATE TABLE security_audit_records']
sample_INSERT: ["INSERT INTO snapshot_scope VALUES ('account_service', '2026-08-17T09:42:50Z');", "INSERT INTO snapshot_scope VALUES ('analytics_platform', '2026-08-17T09:42:50Z');", "INSERT INTO snapshot_scope VALUES ('backup_service', '2026-08-17T09:42:50Z');"]

#### evidence_88
### resource_lookup_trace_20260822_103910.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\resource_lookup_trace_20260822_103910.log
bytes: 9105
line_count: 46
first_20_lines:
- 2026-08-22T07:45:59Z level=INFO service=readback_collector event=export_started target_count=22 mode=point_in_time
- 2026-08-22T07:45:59Z level=DEBUG service=integration_service trace_id=rb-074559-001 event=connector_config_read_started resource_id=data_flow_3199 lookup_key=hannah.sullivan@gmail.com
- 2026-08-22T07:45:59Z level=INFO service=integration_service trace_id=rb-074559-001 event=connector_config_read_completed resource_id=data_flow_3199 enabled=true last_delivery_status=delivered connector_name=search_profile_indexer customer_email=hannah.sullivan@gmail.com customer_reference=null
- 2026-08-22T07:46:55Z level=DEBUG service=search_service trace_id=rb-074655-002 event=index_query_started resource_id=search_1752 lookup_key=hannah.sullivan@gmail.com
- 2026-08-22T07:46:55Z level=INFO service=search_service trace_id=rb-074655-002 event=index_query_completed resource_id=search_1752 result=hit total_hits=1 index=customer_directory_v3 email=hannah.sullivan@gmail.com customer_reference=null
- 2026-08-22T08:03:57Z level=DEBUG service=search_service trace_id=rb-080357-003 event=index_query_started resource_id=search_5696 lookup_key=oadeyemi1657@gmail.com
- 2026-08-22T08:03:57Z level=INFO service=search_service trace_id=rb-080357-003 event=index_query_completed resource_id=search_5696 result=hit total_hits=1 index=customer_directory_v3 email=oadeyemi1657@gmail.com customer_reference=null
- 2026-08-22T08:13:32Z level=DEBUG service=support_platform trace_id=rb-081332-004 event=support_ticket_read_started resource_id=support_3786 lookup_key=oadeyemi1657@gmail.com
- 2026-08-22T08:13:32Z level=INFO service=support_platform trace_id=rb-081332-004 event=support_ticket_read_completed resource_id=support_3786 customer_reference=null requester_name=null requester_email=oadeyemi1657@gmail.com requester_phone=null
- 2026-08-22T08:15:24Z level=DEBUG service=account_service trace_id=rb-081524-005 event=profile_lookup_started resource_id=account_1785 lookup_key=nana.b9576@outlook.com
- 2026-08-22T08:15:24Z level=INFO service=account_service trace_id=rb-081524-005 event=profile_lookup_completed resource_id=account_1785 rows=1 http_status=200 customer_reference=null email=nana.b9576@outlook.com phone=null
- 2026-08-22T08:29:55Z level=DEBUG service=security_service trace_id=rb-082955-006 event=audit_record_read_started resource_id=audit_record_1598 lookup_key=user_115
- 2026-08-22T08:29:55Z level=INFO service=security_service trace_id=rb-082955-006 event=audit_record_read_completed resource_id=audit_record_1598 rows=1 subject_reference=user_115 event_code=SUBJECT_REQUEST_AUDITED retention_until=2033-12-31T23:59:59Z
- 2026-08-22T08:39:55Z level=DEBUG service=security_service trace_id=rb-083955-007 event=audit_record_read_started resource_id=audit_record_1127 lookup_key=user_111
- 2026-08-22T08:39:55Z level=INFO service=security_service trace_id=rb-083955-007 event=audit_record_read_completed resource_id=audit_record_1127 rows=1 subject_reference=user_111 event_code=PRIVACY_REQUEST_ACCEPTED retention_until=2032-06-30T23:59:59Z
- 2026-08-22T08:41:31Z level=DEBUG service=account_service trace_id=rb-084131-008 event=profile_lookup_started resource_id=account_6697 lookup_key=sami-elsayed@gmail.com
- 2026-08-22T08:41:31Z level=INFO service=account_service trace_id=rb-084131-008 event=profile_lookup_completed resource_id=account_6697 rows=0 http_status=404
- 2026-08-22T09:04:17Z level=DEBUG service=search_service trace_id=rb-090417-009 event=index_query_started resource_id=search_696 lookup_key=ayanda.dlamini@outlook.com
- 2026-08-22T09:04:17Z level=INFO service=search_service trace_id=rb-090417-009 event=index_query_completed resource_id=search_696 result=hit total_hits=1 index=customer_directory_v3 email=ayanda.dlamini@outlook.com customer_reference=null
- 2026-08-22T09:09:12Z level=DEBUG service=integration_service trace_id=rb-090912-010 event=connector_config_read_started resource_id=data_flow_6699 lookup_key=ayanda.dlamini@outlook.com
last_20_lines:
- 2026-08-22T09:34:12Z level=INFO service=support_platform trace_id=rb-093412-013 event=support_ticket_read_completed resource_id=support_036 customer_reference=null requester_name=null requester_email=lee.junseo84@icloud.com requester_phone=null
- 2026-08-22T09:34:43Z level=DEBUG service=search_service trace_id=rb-093443-014 event=index_query_started resource_id=search_9556 lookup_key=lee.junseo84@icloud.com
- 2026-08-22T09:34:43Z level=INFO service=search_service trace_id=rb-093443-014 event=index_query_completed resource_id=search_9556 result=hit total_hits=1 index=customer_directory_v3 email=lee.junseo84@icloud.com customer_reference=null
- 2026-08-22T09:43:58Z level=DEBUG service=security_service trace_id=rb-094358-015 event=audit_record_read_started resource_id=audit_record_2103 lookup_key=user_119
- 2026-08-22T09:43:58Z level=INFO service=security_service trace_id=rb-094358-015 event=audit_record_read_completed resource_id=audit_record_2103 rows=1 subject_reference=user_119 event_code=IDENTITY_CHANGE_RECORDED retention_until=2034-09-30T23:59:59Z
- 2026-08-22T09:48:25Z level=DEBUG service=analytics_platform trace_id=rb-094825-016 event=analytics_profile_read_started resource_id=analytics_8698 lookup_key=null
- 2026-08-22T09:48:25Z level=INFO service=analytics_platform trace_id=rb-094825-016 event=analytics_profile_read_completed resource_id=analytics_8698 customer_reference=null email=null phone=null email_hash=null audience_cohort=mobile_browser
- 2026-08-22T10:06:29Z level=DEBUG service=analytics_platform trace_id=rb-100629-017 event=analytics_profile_read_started resource_id=analytics_4800 lookup_key=null
- 2026-08-22T10:06:29Z level=INFO service=analytics_platform trace_id=rb-100629-017 event=analytics_profile_read_completed resource_id=analytics_4800 customer_reference=null email=null phone=null email_hash=null audience_cohort=returning_customer
- 2026-08-22T10:14:38Z level=DEBUG service=search_service trace_id=rb-101438-018 event=index_query_started resource_id=search_943 lookup_key=rbasu9171@fastmail.com
- 2026-08-22T10:14:38Z level=INFO service=search_service trace_id=rb-101438-018 event=index_query_completed resource_id=search_943 result=hit total_hits=1 index=customer_directory_v3 email=rbasu9171@fastmail.com customer_reference=null
- 2026-08-22T10:21:13Z level=DEBUG service=account_service trace_id=rb-102113-019 event=profile_lookup_started resource_id=account_081 lookup_key=nicolas.n7090@zoho.com
- 2026-08-22T10:21:13Z level=INFO service=account_service trace_id=rb-102113-019 event=profile_lookup_completed resource_id=account_081 rows=0 http_status=404
- 2026-08-22T10:35:13Z level=DEBUG service=search_service trace_id=rb-103513-020 event=index_query_started resource_id=search_4417 lookup_key=nana.b9576@outlook.com
- 2026-08-22T10:35:13Z level=INFO service=search_service trace_id=rb-103513-020 event=index_query_completed resource_id=search_4417 result=hit total_hits=1 index=customer_directory_v3 email=nana.b9576@outlook.com customer_reference=null
- 2026-08-22T10:39:09Z level=DEBUG service=search_service trace_id=rb-103909-021 event=index_query_started resource_id=search_5259 lookup_key=joao-santos@proton.me
- 2026-08-22T10:39:09Z level=INFO service=search_service trace_id=rb-103909-021 event=index_query_completed resource_id=search_5259 result=hit total_hits=1 index=customer_directory_v3 email=joao-santos@proton.me customer_reference=null
- 2026-08-22T10:39:10Z level=DEBUG service=support_platform trace_id=rb-103910-022 event=support_ticket_read_started resource_id=support_9309 lookup_key=joao-santos@proton.me
- 2026-08-22T10:39:10Z level=INFO service=support_platform trace_id=rb-103910-022 event=support_ticket_read_completed resource_id=support_9309 customer_reference=null requester_name=null requester_email=joao-santos@proton.me requester_phone=null
- 2026-08-22T10:39:10Z level=INFO service=readback_collector event=export_completed queries=22 dropped=0

#### evidence_89
### service_resource_export_20260901_053316.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\service_resource_export_20260901_053316.json
bytes: 9695
top_level_type: dict
top_level_keys: ['exported_at', 'region', 'service_exports', 'source']
sample: {'exported_at': '2026-09-01T05:33:16Z', 'region': 'global', 'service_exports': {'account_service': {'profile_lookups': [{'observed_at': '2026-09-01T05:06:02Z', 'profile': {'customer_reference': None, 'email': 't.lima5881@yahoo.com', 'email_hash': None, 'full_name': None, 'phone': None}, 'resource_id': 'account_4421', 'status_code': 200}, {'observed_at': '2026-09-01T04:31:43Z', 'profile': None, 'resource_id': 'account_6813', 'status_code': 404}]}, 'analytics_platform': {'profiles': [{'audience_cohort': 'returning_customer', 'customer_reference': None, 'email': 'andres-alvarez@proton.me', 'email…

#### evidence_90
### customer_data_inventory_20260905.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_inventory_20260905.sql
bytes: 2333
CREATE_TABLE: ['CREATE TABLE snapshot_scope', 'CREATE TABLE customer_profiles', 'CREATE TABLE customer_search_documents', 'CREATE TABLE customer_analytics_profiles', 'CREATE TABLE support_records', 'CREATE TABLE customer_exports', 'CREATE TABLE connector_subscriptions', 'CREATE TABLE backup_restore_entries', 'CREATE TABLE security_audit_records']
sample_INSERT: ["INSERT INTO snapshot_scope VALUES ('account_service', '2026-09-05T07:18:01Z');"]

#### evidence_91
### resource_lookup_trace_20260911_074253.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\resource_lookup_trace_20260911_074253.log
bytes: 12310
line_count: 62
first_20_lines:
- 2026-09-11T04:47:51Z level=INFO service=readback_collector event=export_started target_count=30 mode=point_in_time
- 2026-09-11T04:47:51Z level=DEBUG service=security_service trace_id=rb-044751-001 event=audit_record_read_started resource_id=audit_record_9645 lookup_key=user_79
- 2026-09-11T04:47:51Z level=INFO service=security_service trace_id=rb-044751-001 event=audit_record_read_completed resource_id=audit_record_9645 rows=1 subject_reference=user_79 event_code=SUBJECT_REQUEST_AUDITED retention_until=2033-12-31T23:59:59Z
- 2026-09-11T04:50:55Z level=DEBUG service=analytics_platform trace_id=rb-045055-002 event=analytics_profile_read_started resource_id=analytics_5059 lookup_key=null
- 2026-09-11T04:50:55Z level=INFO service=analytics_platform trace_id=rb-045055-002 event=analytics_profile_read_completed resource_id=analytics_5059 customer_reference=null email=null phone=null email_hash=null audience_cohort=home_lifestyle
- 2026-09-11T05:04:31Z level=DEBUG service=analytics_platform trace_id=rb-050431-003 event=analytics_profile_read_started resource_id=analytics_2176 lookup_key=null
- 2026-09-11T05:04:31Z level=INFO service=analytics_platform trace_id=rb-050431-003 event=analytics_profile_read_completed resource_id=analytics_2176 customer_reference=null email=null phone=null email_hash=null audience_cohort=mobile_browser
- 2026-09-11T05:08:27Z level=DEBUG service=integration_service trace_id=rb-050827-004 event=connector_config_read_started resource_id=data_flow_7773 lookup_key=user_75
- 2026-09-11T05:08:27Z level=INFO service=integration_service trace_id=rb-050827-004 event=connector_config_read_completed resource_id=data_flow_7773 enabled=false last_delivery_status=stopped connector_name=customer_events_connector customer_email=null customer_reference=user_75
- 2026-09-11T05:10:36Z level=DEBUG service=support_platform trace_id=rb-051036-005 event=support_ticket_read_started resource_id=support_9746 lookup_key=osei.ama@gmail.com
- 2026-09-11T05:10:36Z level=INFO service=support_platform trace_id=rb-051036-005 event=support_ticket_read_completed resource_id=support_9746 customer_reference=null requester_name=null requester_email=osei.ama@gmail.com requester_phone=null
- 2026-09-11T05:15:16Z level=DEBUG service=security_service trace_id=rb-051516-006 event=audit_record_read_started resource_id=audit_record_1734 lookup_key=user_77
- 2026-09-11T05:15:16Z level=INFO service=security_service trace_id=rb-051516-006 event=audit_record_read_completed resource_id=audit_record_1734 rows=1 subject_reference=user_77 event_code=ACCOUNT_DELETION_RECORDED retention_until=2031-12-31T23:59:59Z
- 2026-09-11T05:22:44Z level=DEBUG service=backup_service trace_id=rb-052244-007 event=restore_policy_read_started resource_id=backup_8673 lookup_key=n.nwosu16@gmail.com
- 2026-09-11T05:22:44Z level=INFO service=backup_service trace_id=rb-052244-007 event=restore_policy_read_completed resource_id=backup_8673 archive_present=true restore_allowed=true archive_key=archive/customer-data/backup_8673.tar.zst customer_email=n.nwosu16@gmail.com customer_reference=null
- 2026-09-11T05:29:07Z level=DEBUG service=support_platform trace_id=rb-052907-008 event=support_ticket_read_started resource_id=support_008 lookup_key=user_75
- 2026-09-11T05:29:07Z level=INFO service=support_platform trace_id=rb-052907-008 event=support_ticket_read_completed resource_id=support_008 customer_reference=user_75 requester_name=null requester_email=null requester_phone=null
- 2026-09-11T05:39:16Z level=DEBUG service=account_service trace_id=rb-053916-009 event=profile_lookup_started resource_id=account_4006 lookup_key=isabela.oliveira90@outlook.com
- 2026-09-11T05:39:16Z level=INFO service=account_service trace_id=rb-053916-009 event=profile_lookup_completed resource_id=account_4006 rows=0 http_status=404
- 2026-09-11T05:44:07Z level=DEBUG service=integration_service trace_id=rb-054407-010 event=connector_config_read_started resource_id=data_flow_4595 lookup_key=salma.mansour@gmail.com
last_20_lines:
- 2026-09-11T06:58:48Z level=INFO service=search_service trace_id=rb-065848-021 event=index_query_completed resource_id=search_8295 result=hit total_hits=1 index=customer_directory_v3 email=stakahashi6573@gmail.com customer_reference=null
- 2026-09-11T07:14:42Z level=DEBUG service=security_service trace_id=rb-071442-022 event=audit_record_read_started resource_id=audit_record_3747 lookup_key=user_80
- 2026-09-11T07:14:42Z level=INFO service=security_service trace_id=rb-071442-022 event=audit_record_read_completed resource_id=audit_record_3747 rows=1 subject_reference=user_80 event_code=IDENTITY_CHANGE_RECORDED retention_until=2034-09-30T23:59:59Z
- 2026-09-11T07:18:47Z level=DEBUG service=backup_service trace_id=rb-071847-023 event=restore_policy_read_started resource_id=backup_3332 lookup_key=user_79
- 2026-09-11T07:18:47Z level=INFO service=backup_service trace_id=rb-071847-023 event=restore_policy_read_completed resource_id=backup_3332 archive_present=true restore_allowed=false archive_key=archive/customer-data/backup_3332.tar.zst customer_email=null customer_reference=user_79
- 2026-09-11T07:25:41Z level=DEBUG service=analytics_platform trace_id=rb-072541-024 event=analytics_profile_read_started resource_id=analytics_5859 lookup_key=null
- 2026-09-11T07:25:41Z level=INFO service=analytics_platform trace_id=rb-072541-024 event=analytics_profile_read_completed resource_id=analytics_5859 customer_reference=null email=null phone=null email_hash=null audience_cohort=home_lifestyle
- 2026-09-11T07:28:48Z level=DEBUG service=security_service trace_id=rb-072848-025 event=audit_record_read_started resource_id=audit_record_5710 lookup_key=user_71
- 2026-09-11T07:28:48Z level=INFO service=security_service trace_id=rb-072848-025 event=audit_record_read_completed resource_id=audit_record_5710 rows=1 subject_reference=user_71 event_code=ACCOUNT_DELETION_RECORDED retention_until=2031-12-31T23:59:59Z
- 2026-09-11T07:30:33Z level=DEBUG service=integration_service trace_id=rb-073033-026 event=connector_config_read_started resource_id=data_flow_9666 lookup_key=user_80
- 2026-09-11T07:30:33Z level=INFO service=integration_service trace_id=rb-073033-026 event=connector_config_read_completed resource_id=data_flow_9666 enabled=false last_delivery_status=stopped connector_name=analytics_identity_bridge customer_email=null customer_reference=user_80
- 2026-09-11T07:34:48Z level=DEBUG service=support_platform trace_id=rb-073448-027 event=support_ticket_read_started resource_id=support_5953 lookup_key=user_79
- 2026-09-11T07:34:48Z level=INFO service=support_platform trace_id=rb-073448-027 event=support_ticket_read_completed resource_id=support_5953 customer_reference=user_79 requester_name=null requester_email=null requester_phone=null
- 2026-09-11T07:40:09Z level=DEBUG service=integration_service trace_id=rb-074009-028 event=connector_config_read_started resource_id=data_flow_3255 lookup_key=user_79
- 2026-09-11T07:40:09Z level=INFO service=integration_service trace_id=rb-074009-028 event=connector_config_read_completed resource_id=data_flow_3255 enabled=false last_delivery_status=stopped connector_name=search_profile_indexer customer_email=null customer_reference=user_79
- 2026-09-11T07:40:35Z level=DEBUG service=security_service trace_id=rb-074035-029 event=audit_record_read_started resource_id=audit_record_5425 lookup_key=user_75
- 2026-09-11T07:40:35Z level=INFO service=security_service trace_id=rb-074035-029 event=audit_record_read_completed resource_id=audit_record_5425 rows=1 subject_reference=user_75 event_code=ACCOUNT_DELETION_RECORDED retention_until=2031-12-31T23:59:59Z
- 2026-09-11T07:42:53Z level=DEBUG service=support_platform trace_id=rb-074253-030 event=support_ticket_read_started resource_id=support_9652 lookup_key=stakahashi6573@gmail.com
- 2026-09-11T07:42:53Z level=INFO service=support_platform trace_id=rb-074253-030 event=support_ticket_read_completed resource_id=support_9652 customer_reference=null requester_name=null requester_email=stakahashi6573@gmail.com requester_phone=null
- 2026-09-11T07:42:53Z level=INFO service=readback_collector event=export_completed queries=30 dropped=0

#### evidence_92
### service_resource_export_20260915_114455.json
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\records\service_resource_export_20260915_114455.json
bytes: 12177
top_level_type: dict
top_level_keys: ['exported_at', 'region', 'service_exports', 'source']
sample: {'exported_at': '2026-09-15T11:44:55Z', 'region': 'global', 'service_exports': {'account_service': {'profile_lookups': [{'observed_at': '2026-09-15T09:31:40Z', 'profile': None, 'resource_id': 'account_3136', 'status_code': 404}, {'observed_at': '2026-09-15T09:59:48Z', 'profile': None, 'resource_id': 'account_3866', 'status_code': 404}, {'observed_at': '2026-09-15T09:41:33Z', 'profile': {'customer_reference': None, 'email': 'keiko.nakamura@gmail.com', 'email_hash': None, 'full_name': None, 'phone': None}, 'resource_id': 'account_5334', 'status_code': 200}, {'observed_at': '2026-09-15T11:07:16Z'…

#### evidence_93
### customer_data_inventory_20260916.sql
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\databases\customer_data_inventory_20260916.sql
bytes: 5593
CREATE_TABLE: ['CREATE TABLE snapshot_scope', 'CREATE TABLE customer_profiles', 'CREATE TABLE customer_search_documents', 'CREATE TABLE customer_analytics_profiles', 'CREATE TABLE support_records', 'CREATE TABLE customer_exports', 'CREATE TABLE connector_subscriptions', 'CREATE TABLE backup_restore_entries', 'CREATE TABLE security_audit_records']
sample_INSERT: ["INSERT INTO snapshot_scope VALUES ('account_service', '2026-09-16T08:37:39Z');", "INSERT INTO snapshot_scope VALUES ('analytics_platform', '2026-09-16T08:37:39Z');", "INSERT INTO snapshot_scope VALUES ('backup_service', '2026-09-16T08:37:39Z');"]

#### evidence_94
### resource_lookup_trace_20260926_103856.log
path: D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\evidence\logs\resource_lookup_trace_20260926_103856.log
bytes: 11801
line_count: 58
first_20_lines:
- 2026-09-26T07:49:50Z level=INFO service=readback_collector event=export_started target_count=28 mode=point_in_time
- 2026-09-26T07:49:50Z level=DEBUG service=account_service trace_id=rb-074950-001 event=profile_lookup_started resource_id=account_2064 lookup_key=charlotte.wright@outlook.com
- 2026-09-26T07:49:50Z level=INFO service=account_service trace_id=rb-074950-001 event=profile_lookup_completed resource_id=account_2064 rows=0 http_status=404
- 2026-09-26T07:51:26Z level=DEBUG service=integration_service trace_id=rb-075126-002 event=connector_config_read_started resource_id=data_flow_4713 lookup_key=user_49
- 2026-09-26T07:51:26Z level=INFO service=integration_service trace_id=rb-075126-002 event=connector_config_read_completed resource_id=data_flow_4713 enabled=false last_delivery_status=stopped connector_name=support_profile_sync customer_email=null customer_reference=user_49
- 2026-09-26T07:54:41Z level=DEBUG service=backup_service trace_id=rb-075441-003 event=restore_policy_read_started resource_id=backup_7809 lookup_key=user_49
- 2026-09-26T07:54:41Z level=INFO service=backup_service trace_id=rb-075441-003 event=restore_policy_read_completed resource_id=backup_7809 archive_present=true restore_allowed=false archive_key=archive/customer-data/backup_7809.tar.zst customer_email=null customer_reference=user_49
- 2026-09-26T07:57:13Z level=DEBUG service=search_service trace_id=rb-075713-004 event=index_query_started resource_id=search_4262 lookup_key=akosua.gyasi@gmail.com
- 2026-09-26T07:57:13Z level=INFO service=search_service trace_id=rb-075713-004 event=index_query_completed resource_id=search_4262 result=hit total_hits=1 index=customer_directory_v3 email=akosua.gyasi@gmail.com customer_reference=null
- 2026-09-26T07:59:44Z level=DEBUG service=support_platform trace_id=rb-075944-005 event=support_ticket_read_started resource_id=support_5569 lookup_key=mori.ren@gmail.com
- 2026-09-26T07:59:44Z level=INFO service=support_platform trace_id=rb-075944-005 event=support_ticket_read_completed resource_id=support_5569 customer_reference=null requester_name=null requester_email=mori.ren@gmail.com requester_phone=null
- 2026-09-26T08:10:20Z level=DEBUG service=security_service trace_id=rb-081020-006 event=audit_record_read_started resource_id=audit_record_1105 lookup_key=user_42
- 2026-09-26T08:10:20Z level=INFO service=security_service trace_id=rb-081020-006 event=audit_record_read_completed resource_id=audit_record_1105 rows=1 subject_reference=user_42 event_code=IDENTITY_CHANGE_RECORDED retention_until=2034-09-30T23:59:59Z
- 2026-09-26T08:37:56Z level=DEBUG service=account_service trace_id=rb-083756-007 event=profile_lookup_started resource_id=account_3610 lookup_key=n.masuku60@gmail.com
- 2026-09-26T08:37:56Z level=INFO service=account_service trace_id=rb-083756-007 event=profile_lookup_completed resource_id=account_3610 rows=0 http_status=404
- 2026-09-26T08:49:37Z level=DEBUG service=support_platform trace_id=rb-084937-008 event=support_ticket_read_started resource_id=support_5742 lookup_key=zofia-dvorak79@proton.me
- 2026-09-26T08:49:37Z level=INFO service=support_platform trace_id=rb-084937-008 event=support_ticket_read_completed resource_id=support_5742 customer_reference=null requester_name=null requester_email=zofia-dvorak79@proton.me requester_phone=null
- 2026-09-26T08:57:37Z level=DEBUG service=account_service trace_id=rb-085737-009 event=profile_lookup_started resource_id=account_7566 lookup_key=l.fontaine46@yahoo.com
- 2026-09-26T08:57:37Z level=INFO service=account_service trace_id=rb-085737-009 event=profile_lookup_completed resource_id=account_7566 rows=0 http_status=404
- 2026-09-26T08:57:38Z level=DEBUG service=analytics_platform trace_id=rb-085738-010 event=analytics_profile_read_started resource_id=analytics_5589 lookup_key=null
last_20_lines:
- 2026-09-26T09:46:41Z level=INFO service=integration_service trace_id=rb-094641-019 event=connector_config_read_completed resource_id=data_flow_1043 enabled=true last_delivery_status=delivered connector_name=analytics_identity_bridge customer_email=tunde.c692281@zoho.com customer_reference=null
- 2026-09-26T09:52:54Z level=DEBUG service=integration_service trace_id=rb-095254-020 event=connector_config_read_started resource_id=data_flow_1770 lookup_key=akosua.gyasi@gmail.com
- 2026-09-26T09:52:54Z level=INFO service=integration_service trace_id=rb-095254-020 event=connector_config_read_completed resource_id=data_flow_1770 enabled=true last_delivery_status=delivered connector_name=customer_events_connector customer_email=akosua.gyasi@gmail.com customer_reference=null
- 2026-09-26T09:54:09Z level=DEBUG service=analytics_platform trace_id=rb-095409-021 event=analytics_profile_read_started resource_id=analytics_9406 lookup_key=null
- 2026-09-26T09:54:09Z level=INFO service=analytics_platform trace_id=rb-095409-021 event=analytics_profile_read_completed resource_id=analytics_9406 customer_reference=null email=null phone=null email_hash=null audience_cohort=general_shopper
- 2026-09-26T09:58:35Z level=DEBUG service=search_service trace_id=rb-095835-022 event=index_query_started resource_id=search_2127 lookup_key=lnajjar900380@fastmail.com
- 2026-09-26T09:58:35Z level=INFO service=search_service trace_id=rb-095835-022 event=index_query_completed resource_id=search_2127 result=hit total_hits=1 index=customer_directory_v3 email=lnajjar900380@fastmail.com customer_reference=null
- 2026-09-26T09:58:42Z level=DEBUG service=analytics_platform trace_id=rb-095842-023 event=analytics_profile_read_started resource_id=analytics_2265 lookup_key=null
- 2026-09-26T09:58:42Z level=INFO service=analytics_platform trace_id=rb-095842-023 event=analytics_profile_read_completed resource_id=analytics_2265 customer_reference=null email=null phone=null email_hash=null audience_cohort=home_lifestyle
- 2026-09-26T10:00:17Z level=DEBUG service=support_platform trace_id=rb-100017-024 event=support_ticket_read_started resource_id=support_1097 lookup_key=user_49
- 2026-09-26T10:00:17Z level=INFO service=support_platform trace_id=rb-100017-024 event=support_ticket_read_completed resource_id=support_1097 customer_reference=user_49 requester_name=null requester_email=null requester_phone=null
- 2026-09-26T10:21:52Z level=DEBUG service=backup_service trace_id=rb-102152-025 event=restore_policy_read_started resource_id=backup_6266 lookup_key=user_42
- 2026-09-26T10:21:52Z level=INFO service=backup_service trace_id=rb-102152-025 event=restore_policy_read_completed resource_id=backup_6266 archive_present=true restore_allowed=false archive_key=archive/customer-data/backup_6266.tar.zst customer_email=null customer_reference=user_42
- 2026-09-26T10:23:12Z level=DEBUG service=search_service trace_id=rb-102312-026 event=index_query_started resource_id=search_4013 lookup_key=mori.ren@gmail.com
- 2026-09-26T10:23:12Z level=INFO service=search_service trace_id=rb-102312-026 event=index_query_completed resource_id=search_4013 result=hit total_hits=1 index=customer_directory_v3 email=mori.ren@gmail.com customer_reference=null
- 2026-09-26T10:37:23Z level=DEBUG service=security_service trace_id=rb-103723-027 event=audit_record_read_started resource_id=audit_record_3308 lookup_key=user_49
- 2026-09-26T10:37:23Z level=INFO service=security_service trace_id=rb-103723-027 event=audit_record_read_completed resource_id=audit_record_3308 rows=1 subject_reference=user_49 event_code=ACCOUNT_DELETION_RECORDED retention_until=2031-12-31T23:59:59Z
- 2026-09-26T10:38:56Z level=DEBUG service=search_service trace_id=rb-103856-028 event=index_query_started resource_id=search_459 lookup_key=tunde.c692281@zoho.com
- 2026-09-26T10:38:56Z level=INFO service=search_service trace_id=rb-103856-028 event=index_query_completed resource_id=search_459 result=hit total_hits=1 index=customer_directory_v3 email=tunde.c692281@zoho.com customer_reference=null
- 2026-09-26T10:38:56Z level=INFO service=readback_collector event=export_completed queries=28 dropped=0

## Cross-file join analysis
Observed JSON scalar fields only; non-JSON evidence is separately inventoried above.

- activity.resource_id vs JSON resource_id: intersection=551, left=3948, right=755, Jaccard=0.132707; examples=['account_1015', 'account_1084', 'account_1340', 'account_1417', 'account_1433', 'account_1698', 'account_1718', 'account_1733', 'account_1789', 'account_1949', 'account_2088', 'account_2176', 'account_2255', 'account_228', 'account_2282', 'account_2420', 'account_2424', 'account_2434', 'account_2437', 'account_246']

- activity target/source system vs JSON system_id/data_store: intersection=10, left=24, right=13, Jaccard=0.37037; examples=['account_service', 'analytics_platform', 'backup_service', 'export_service', 'identity_service', 'integration_service', 'legal_service', 'search_service', 'security_service', 'support_platform']

- activity.target_user_id vs identities.user_id: intersection=0, left=0, right=850, Jaccard=0.0; examples=[]

- activity.target_user_id vs JSON user refs: intersection=0, left=0, right=80, Jaccard=0.0; examples=[]

## Actual activity columns and distincts

- event_type: distinct=17, first_20=['ANONYMIZE_RECORD', 'BLOCK_RESTORE', 'CHECK_DATA_FLOW', 'CHECK_RESTORE_ACCESS', 'CLASSIFY_REQUEST', 'CREATE_EXPORT', 'DELETE_RECORD', 'DISABLE_DATA_FLOW', 'INDEX_RECORD', 'LINK_RESOURCE_IDENTITY', 'REDACT_RECORD', 'REFRESH_CACHE', 'RESTORE_BACKUP', 'RETAIN_RECORD', 'SEND_EMAIL', 'SYNC_RECORD', 'UPDATE_RECORD']

- source_system: distinct=11, first_20=['account_service', 'backup_service', 'data_catalog', 'deletion_worker', 'export_service', 'integration_service', 'notification_service', 'privacy_intake', 'profile_service', 'security_service', 'support_platform']

- target_system: distinct=19, first_20=['account_failover_replica', 'account_replication_cluster', 'account_service', 'analytics_platform', 'archive_service', 'backup_service', 'cache_service', 'email_delivery_service', 'export_service', 'identity_service', 'integration_service', 'legal_service', 'marketing_platform', 'object_storage', 'object_store', 'privacy_case_management', 'search_service', 'security_service', 'support_platform']

- resource_id: distinct=3948, first_20=['account_001', 'account_002', 'account_005', 'account_006', 'account_007', 'account_008', 'account_010', 'account_018', 'account_022', 'account_034', 'account_035', 'account_050', 'account_058', 'account_060', 'account_063', 'account_077', 'account_081', 'account_1004', 'account_1005', 'account_1007']

- target_user_id: distinct=1, first_20=['']

- target_user_id null_count=4011
