# Case 03 Phase 12 regression audit

## Identity and source evidence

`case_03` requests deletion for `l.fontaine46@yahoo.com` / `user_43`, audit 2026-09-26 11:00 UTC. The Phase 12 log handler sees `dataset/evidence/logs/resource_lookup_trace_20260926_103856.log:18-19`: an account lookup for `account_7566` and a 404 readback. It also sees `:34-35`, a retained security audit record for `user_43`. These are genuine source lines; the email matcher itself is not an over-broad substring match, and the cache key is identity/cutoff-specific.

## First incorrect decision

`code/orchestrator/activity_expander.py:34-63` adds the account readback to `by_system['account_service']` and then derives unrelated same-system activities for this user within 24 hours. For example, `dataset/system_activity.csv:3963` is a cache refresh for `cache_5233` with no user identifier or full-resource match to the account readback. The debug trace shows it became `activity_3962::derived_0008_for_user_43` via `system_time_proximity`, then a timeline-only PRESENT `ResourceFact`, then a `REPORT_REMAINING_RECORD` finding. Similar unsupported derivations affect search and analytics resources. This is the primary cause of the COMPLETE → INCOMPLETE regression.

The security audit row `audit_record_2016` is also treated as a fail-closed DELETE because `security_service` is absent from `code/agent/policy/category_map.py`, despite `dataset/deletion_rules.csv:13` requiring retention for security audit logs. However, mapping it alone would not remove the unrelated cache/search/analytics findings.

## Conclusion and constrained fix

The first wrong decision is in the frozen orchestrator activity expander, not Phase 5 status or Phase 6 step mapping. A correct repair would require a source-grounded rule that prevents a single account readback from affiliating unrelated same-system activities by time alone, while retaining exact-resource matches and legitimate flow signals. The Phase 13 scope explicitly freezes `orchestrator/activity_expander.py`, so no compensating Phase 5/6 exception was made. Case 03 remains a known regression and the release gate fails.
