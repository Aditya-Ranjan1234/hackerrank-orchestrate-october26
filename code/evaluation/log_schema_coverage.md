# Structured log and handover owner/resource coverage

Source-only comparison across every manifest-listed log and the plain-text shift handover. The independent field parser finds exact same-line structured owner/resource pairs; production extraction is checked against those pairs. This audit never reads sample answers.

| File ID | Source | Direct source pairs | Extracted pairs | Missing direct pairs |
|---|---|---:|---:|---:|
| evidence_01 | service_events_ap_south_20260915.log | 11 | 34 | 0 |
| evidence_03 | customer_account_handover_20261001.txt | 39 | 39 | 0 |
| evidence_06 | structured_service_events_eu_west_20260918.log | 0 | 34 | 0 |
| evidence_08 | search_index_diagnostic_20260906.log | 34 | 34 | 0 |
| evidence_11 | syslog_archive_us_east_20260824.log | 7 | 34 | 0 |
| evidence_16 | application_trace_ap_northeast_20260730.log | 13 | 33 | 0 |
| evidence_21 | operations_stream_eu_central_20260705.log | 13 | 36 | 0 |
| evidence_25 | cloud_runtime_export_us_west_20260608.log | 14 | 40 | 0 |
| evidence_30 | service_events_sa_east_20260516.log | 12 | 33 | 0 |
| evidence_34 | structured_service_events_ca_central_20260419.log | 0 | 43 | 0 |
| evidence_39 | syslog_archive_ap_southeast_20260325.log | 16 | 40 | 0 |
| evidence_41 | notification_delivery_20260315.log | 39 | 39 | 0 |
| evidence_44 | application_trace_eu_north_20260302.log | 9 | 35 | 0 |
| evidence_48 | operations_stream_me_central_20260203.log | 10 | 34 | 0 |
| evidence_53 | cloud_runtime_export_af_south_20260930.log | 300 | 300 | 0 |
| evidence_61 | support_replica.log | 0 | 1 | 0 |
| evidence_64 | resource_lookup_trace_20260218_083911.log | 23 | 25 | 0 |
| evidence_67 | resource_lookup_trace_20260310_061801.log | 0 | 1 | 0 |
| evidence_70 | resource_lookup_trace_20260414_054007.log | 16 | 20 | 0 |
| evidence_73 | resource_lookup_trace_20260509_104353.log | 24 | 29 | 0 |
| evidence_76 | resource_lookup_trace_20260529_074313.log | 17 | 20 | 0 |
| evidence_79 | resource_lookup_trace_20260623_053726.log | 22 | 26 | 0 |
| evidence_82 | resource_lookup_trace_20260713_093359.log | 18 | 22 | 0 |
| evidence_85 | resource_lookup_trace_20260728_054417.log | 17 | 20 | 0 |
| evidence_88 | resource_lookup_trace_20260822_103910.log | 17 | 20 | 0 |
| evidence_91 | resource_lookup_trace_20260911_074253.log | 20 | 26 | 0 |
| evidence_94 | resource_lookup_trace_20260926_103856.log | 22 | 25 | 0 |

Total: 713 direct source pairs; 1043 extracted pairs; 0 missing direct pairs.

Extra extracted pairs can be legitimate exact-trace joins from a prior structured query. The separate trace-integrity audit checks for conflicting trace owners and later-only owner signals.
