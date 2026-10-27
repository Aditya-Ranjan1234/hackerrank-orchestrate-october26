# Final-run diagnostic coverage

Aggregated from the 518 full-request diagnostics and generated output, not from sample answers. The production loop enumerates every manifest entry per case; the diagnostic start event records its expected count. Cached sources are still rehashed locally. A COMPLETE row with no verification is counted separately as an evidence-quality risk even if the CSV shape passes. These counts describe this local evidence snapshot, not a live Northstar system query.

| Measure | Count |
|---|---:|
| cases_expected | 518 |
| cases_with_agent_tool_inspection | 11 |
| cases_with_complete_trace | 518 |
| complete_without_verification | 1 |
| derived_activities | 1084 |
| evidence_files_per_case | 94 |
| manifest_dispatches_expected | 48692 |
| post_audit_exact_owner_joins | 2 |
| stale_negative_lookups_excluded | 1 |
| tool_inspections | 17 |

Diagnostic issues: 0.
