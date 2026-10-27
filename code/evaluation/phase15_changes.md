# Phase 15 grounded change ledger

## Change 1: Keep nested JSON document under its visible resource ID
- **Iteration:** 15a
- **Fix ID:** step-diff-RESOURCE_ID_MISMATCH
- **File:** `code/agent/evidence/handlers/json_handler.py` (`visit` resource-ID propagation)
- **Grounded in:** post-Phase-14 `step_diff_report.md` §3, case_29; `dataset/evidence/records/customer_data_snapshot_bundle_20260917.json` search_1993 document.
- **Problem:** The nested document has the user's email and ID but no own resource ID. The extractor emitted `$.snapshots[7].records[3].document` as a second resource, adding three steps. Positional shifting then inflated the nominal `SYSTEM_ID_MISMATCH` count (116/539), so changing system IDs based on that aggregate would be unsound.
- **Before:** `rid=str(node.get("id",node.get("resource_id",node.get("account_id",prefix))))`; descendants received no resource context.
- **After:** A descendant lacking an ID inherits the nearest ancestor's explicit `id`, `resource_id`, or `account_id`; its own ID takes precedence. The JSON path remains the fallback when no visible ID exists anywhere in the branch.
- **Tests added:** `test_p15_nested_document_inherits_visible_parent_resource_id`, `test_p15_nested_explicit_id_overrides_parent_resource_id`.
- **Expected impact:** Remove the phantom JSON-path resource and its three steps in case_29 and similarly shaped cases without guessing ownership.
- **Verification:** Fresh-cache Phase 15a sample preserved 32/32 statuses and 0/32 exact arrays; positional system-ID mismatches fell 116 → 97. Both new nested-ID tests pass.

## Scope conflict: stale proximity test
The stale assertion is in `code/tests/test_case03_regression.py:17-23`, not `test_activity_expander.py`. Phase 15 explicitly freezes that file. The permitted test file already asserts the opposite invariant in `test_i1_sync_proximity`, `test_p14_e1_no_unowned_same_system`, and `test_p14_e7_no_method2_even_zero_window`. The stale test is retained and reported failing rather than silently edited or counteracted with unsafe Method 2.

## Change 2: Verify compliant resources in an incomplete case
- **Iteration:** 15b
- **Fix ID:** step-diff-COUNT_MISMATCH
- **File:** `code/agent/steps/builder.py` (`build_incomplete`)
- **Grounded in:** post-15a case_29 comparison in `step_diff_report.md` §3: gold includes `account_7012` and `audit_record_3954` verification steps alongside findings/remediations; ours emits no compliant verifications.
- **Problem:** The builder only walked `incomplete_triggers`, so a case with any failed resource omitted all verification steps for its compliant resources. This is distinct from the positional system-ID count.
- **Before:** `for t in decision.incomplete_triggers: ... out.append(_step("VERIFICATION",v,vop,vs,"")); return out`.
- **After:** After failed-trigger steps, append one empty-citation verification for each compliant verdict with a required action, deduplicated by system/resource/operation. No finding or remediation is added for a compliant verdict.
- **Tests added:** `test_p15_incomplete_case_also_verifies_compliant_resources`, `test_p15_incomplete_compliant_verification_is_deduplicated`.
- **Expected impact:** Recover gold verification steps for already-compliant resources in mixed-status cases, without altering status or resource ownership.
- **Verification:** Phase 15b preserved 32/32 statuses, raised exact arrays 0 → 1/32 (case_14), and matching step counts 1 → 7/32. The full test suite after eight additions has 221 pass and the same two known failures.

## Change 3: Distinguish positional shifts from semantic step errors
- **Iteration:** 15c
- **Fix ID:** step-diff-SYSTEM_ID_MISMATCH-diagnostic
- **File:** `code/orchestrator/step_diff.py` (`semantic_counts`, report, CLI default)
- **Grounded in:** post-15b `step_diff_report.md` §1–3: positional SYSTEM_ID_MISMATCH still dominates at 108, yet case_29 shares 13 of 14 semantic step identities and is missing one account verification. Other fields differ mainly from index shifts.
- **Problem:** The diagnostic report's index-by-index counts make a missing or inserted step look like many system/resource/operation defects. Its no-argument CLI also silently read the stale Phase 12 sample.
- **Before:** positional field counts only; `ours = root/"sample_output_phase12.csv"` when no path supplied.
- **After:** Keep existing positional counts, add position-independent missing/extra/citation counts by `(phase,system_id,resource_id,operation,state)`, and regenerate the current 32-case sample when called without arguments. No production decision code is changed.
- **Tests added:** `test_p15_semantic_diff_ignores_step_order`, `test_p15_semantic_diff_isolates_citation_difference`, plus JSON-path fallback and exact-timestamp no-proximity regressions.
- **Expected impact:** Reveal actual residual categories and prevent a stale report from driving further changes.
- **Verification:** No-argument CLI generated the current 32-case sample and report. Semantic counts: 76 missing, 87 extra, 23 citation differences; 1/32 exact arrays. All four associated tests pass; full suite 221 pass, 2 known fail.
