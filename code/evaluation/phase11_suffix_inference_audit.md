# Phase 11 suffix inference audit

Grounding: [Phase 10 mismatch triage](mismatch_triage_report.md#grounded-root-cause-review) identifies seven false resource affiliations. The raw [system activity schema](dataset_grounding_report.md#system_activitycsv) has no `target_user_id` column.

Search: `rg -n 'endswith|rsplit|suffix|normalize_user_ref|infer_user_from_resource' code/agent code/orchestrator` plus direct inspection of the reconstructor and expander.

| Call site before change | Behavior | Assessment |
|---|---|---|
| `code/agent/state/reconstructor.py:18-19` | `user_25` became suffix `025`; any resource ending with that suffix was affiliated with that user. | Unsupported; remove. |
| `code/orchestrator/activity_expander.py:10-16` | `_norm` accepts only exact user ID, email, or known email hash. | No suffix inference; retain. |

No other suffix-based user ownership call site was found. `resource_id` remains an exact-match join key between records and activities; matching the complete identifier is distinct from matching only its numeric suffix.
