# Phase 14 grounded change ledger

## Change 1: Remove system-time ownership inference
- **Iteration / Fix ID / File:** 14a / A+B / `code/orchestrator/activity_expander.py:1-79`
- **Grounded in:** `step_diff_report.md` Phase 13 baseline (716 COUNT_MISMATCH), `phase13_case03_regression_audit.md` (unrelated `cache_5233`), and `dataset_grounding_report.md` (exact resource joins).
- **Problem:** A same-system event within ±24 hours did not prove a subject owned that event. The expander derived unrelated cache/search/analytics activities.
- **Change:** Derive only when an identity-matched evidence record has the exact activity resource ID, or an explicit `evidence_<resource_id>` file ID. Deduplicate per user. Keep `time_window` as a deprecated no-op argument for API compatibility; never use it to infer.
- **Before:** `by_system` lookup and `abs((ts-at).total_seconds()) <= time_window.total_seconds()`.
- **After:** `by_resource.get(rid, [])`, exact file-ID convention, and a per-user `seen` set.
- **Tests added:** pending Phase 14 test extension; earlier proximity tests must be rewritten because they assert the removed behavior.
- **Expected impact:** Remove phantom derived activities, recover case 03 and reduce extra steps.
- **Verification:** Initial sample status stays 25/32; exact arrays stay 0/32; generated steps fall 885 → 312 and count mismatches 716 → 155. Case 03 remains wrong, requiring further grounded triage.

## Change 2: Replace obsolete proximity tests with exact-resource invariants
- **Iteration / Fix ID / File:** 14a / B / `code/tests/test_activity_expander.py:14-39`
- **Grounded in:** Change 1 and `phase13_case03_regression_audit.md`, which proved the old proximity assertions were asserting the bug.
- **Problem:** Five allowed legacy tests required Method 2 to create ownership from shared system/time.
- **Change:** Rewrite those assertions and add ten synthetic tests for exact resource, wrong user, explicit file ID, deduplication, cutoff, deterministic output, and original preservation.
- **Before:** `assert derived(go([act()], [ev()]))` expected same-system inference.
- **After:** `assert not derived(go([act()], [ev()]))` and exact-resource positive cases.
- **Tests added:** `test_p14_e1` through `test_p14_e10`.
- **Expected impact / verification:** 206 pass; one frozen `test_case03_regression.py` test fails because it still asserts Method 2. That file is explicitly outside Phase 14's allowed test edits.

## Change 3: Security audit retention mapping — tested and reverted
- **Iteration / Fix ID / File:** 14b / targeted-case_03 / `code/agent/policy/category_map.py:2`, `code/agent/policy/engine.py:14-19` (reverted; final files unchanged).
- **Grounded in:** `phase13_case03_regression_audit.md`, `dataset/deletion_rules.csv:13`, and `code/.cache/diagnostics/case_03.jsonl` after 14a.
- **Problem:** `security_service/audit_record_2016` was fail-closed to DELETE despite the SECURITY_AUDIT_LOG retention rule.
- **Change:** Temporarily mapped security service to logs and selected `rule_12` for audit records; then reverted after the sample showed a regression.
- **Before:** `security_service` unmapped; `audit_record_2016` required DELETE.
- **Trial:** `security_service -> logs`; filter applicable rules to `rule_12` for audit records.
- **After:** exact original mapping and engine restored, because trial caused case 14 to become wrong.
- **Tests added:** none; evaluated on full 32-case sample.
- **Expected impact / verification:** case 03 recovered to COMPLETE, but case 14 flipped INCOMPLETE → COMPLETE (gold INCOMPLETE); net remained 25/32 and exact steps 0/32. Case 14 has no restore-risk fact despite a backup record; policy-only fix is insufficient. Reverted per no-regression rule.

## Change 4: Emit unowned explicit 404 JSON readbacks
- **Iteration / Fix ID / File:** 14c / targeted-case_26 / `code/agent/evidence/handlers/json_handler.py:7,51-88`
- **Grounded in:** `dataset/evidence/records/service_resource_export_20260915_114455.json`, `account_5684` readback with `profile: null`, `status_code: 404`, `observed_at`, and `phase13_validation.md` case 26 (old PRESENT won).
- **Problem:** A later, explicit ABSENT readback had no user identifier and was omitted by identity-filtered JSON extraction. The handler also ignored the per-row `observed_at` and `service_exports` enclosing system.
- **Change:** Emit only explicit 404/null-profile records with blank `user_ref`, preserve `observed_at`, and propagate a visible service-export system key. Blank-ref records are not assigned to a user in the handler.
- **Before:** unmatched dicts were dropped; timestamp priority lacked `observed_at`.
- **After:** `RecordState(system,resource_id,"","ABSENT",[],ts,...)` for 404 readbacks; `observed_at` first in timestamp priority.
- **Tests added:** pending targeted identity-join tests in the permitted expander test file.
- **Expected impact / verification:** enables a later exact-resource ownership join; alone it must not assert ownership. Measured effect awaits the reconstructor join.

## Change 5: Join unowned 404 only to a proven full resource ID
- **Iteration / Fix ID / File:** 14c / targeted-case_26 / `code/agent/state/reconstructor.py:33-55`
- **Grounded in:** `evidence_02` has user_26's `account_5684`; `evidence_92` has a later 404 for the same full ID. See `code/.cache/diagnostics/case_26.jsonl` after 14c.
- **Problem:** A blank-user 404 cannot be assigned by itself, while dropping it leaves an older PRESENT snapshot as winner.
- **Change:** Hold blank-user ABSENT records separately, then admit one only if `(system_id, resource_id)` already has direct identity-linked evidence. Do not infer from suffix or same-system proximity.
- **Before:** all `rec.user_ref==""` records entered candidates without proof.
- **After:** `if key in candidates: candidates[key].append((ev,rec))` and an audit note.
- **Tests added:** pending exact-resource join tests in the allowed expander test file.
- **Expected impact / verification:** case 26 `account_5684` now correctly becomes ABSENT with `evidence_92`. Whole-case status remains 25/32 and exact steps 0/32 because other categories/states are still wrong; no status regression observed.

## Change 6: Guard the 404 join with synthetic tests
- **Iteration / Fix ID / File:** 14c / targeted-case_26 / `code/tests/test_activity_expander.py:42-63`
- **Grounded in:** Changes 4–5 and `evidence_92`'s null-profile account readback.
- **Problem:** A blank-owner 404 must not become a fact for every identity or join a different full resource ID.
- **Change:** Added two tests using a synthetic service export: no prior ownership yields zero facts; exact prior ownership yields ABSENT; another resource ID remains unaffected.
- **Before:** no cross-file unowned readback test.
- **After:** `test_p14_unowned_404_requires_prior_exact_identity_evidence` and `test_p14_unowned_404_does_not_join_different_resource`.
- **Verification:** 208 passing, one frozen obsolete proximity test failing; Phase 14c sample 25/32 statuses, 0/32 exact steps, step overlap improved from 32 to 45 and count mismatches from 716 to 89.

## Change 7: Preserve explicit restore-access evidence in state notes
- **Iteration / Fix ID / File:** 14c / targeted-case_14 / `code/agent/state/reconstructor.py:55-66`
- **Grounded in:** `dataset/evidence/records/customer_account_handover_20261001.txt:19` (`BACKUP_ARCHIVE | ACTIVE`) and `evidence_92` backup readback (`restore_allowed: false`).
- **Problem:** Phase 4 sees only `ResourceFact`, losing the evidence's explicit restore-access signal; case 14 had no restore-risk fact.
- **Change:** Carry an audit note `restore_access_allowed_by_evidence` or `restore_access_blocked_by_evidence` for backup facts with those literal source fields.
- **Before:** backup `ResourceFact.notes` lacked restore-access state.
- **After:** notes quote the state kind while `state_at_audit` remains one of the five IR states.
- **Tests added:** pending backup-state test in the permitted test file.
- **Expected impact / verification:** enables a policy treatment without inventing a risk from mere backup presence; measured impact awaits paired policy change.

## Change 8: Distinguish retained security audits and explicit backup restore state
- **Iteration / Fix ID / File:** 14c / targeted-case_03, targeted-case_14 / `code/agent/policy/category_map.py:2`, `code/agent/policy/engine.py:13-45`
- **Grounded in:** `dataset/deletion_rules.csv:13,15` (`SECURITY_AUDIT_LOG` RETAIN and `BACKUP_ARCHIVE` restore-access condition); `customer_account_handover_20261001.txt:19` ACTIVE backup; `evidence_92` `restore_allowed:false`.
- **Problem:** Security audits were fail-closed DELETE, while restorable backups were treated as compliant RETAIN. The earlier isolated audit mapping regressed case 14 because it did not also handle its visible backup state.
- **Change:** Map `security_service` to logs and select only `rule_12` for `audit_record_*`; for backup facts with explicit allowed/blocked notes, emit a restore-risk verdict instead of a generic retained record verdict.
- **Before:** unknown security category; all backup PRESENT facts compliant RETAIN.
- **After:** audit record RETAIN; ACTIVE backup `BLOCK_RESTORE` noncompliant; blocked backup `BLOCK_RESTORE` compliant.
- **Tests added:** pending policy-context tests in the permitted test file.
- **Expected impact / verification:** cases 03, 21, 25 recovered; case 14 stayed correctly INCOMPLETE. Sample status 25/32 → 28/32, exact arrays 0/32. Four remaining status errors: 26, 27, 28, 31. Full suite 208 pass, one frozen Phase 13 test still requires removed Method 2.

## Change 9: Interpret explicit redaction and disabled-connector fields
- **Iteration / Fix ID / File:** 14c / targeted-case_26, targeted-case_31 / `code/agent/evidence/handlers/json_handler.py`, `code/agent/state/reconstructor.py`, `code/agent/policy/category_map.py`, `code/agent/policy/engine.py`.
- **Grounded in:** `dataset/evidence/records/service_resource_export_20260915_114455.json` rows `support_4715`, `data_flow_6244` and analogues for users 27–28; `dataset/evidence/records/customer_data_snapshot_bundle_20260915.json:17-23` tombstone_440; `dataset/deletion_rules.csv:6,16`; latest `sample_output_phase14d.csv` and diagnostic traces for cases 26–28 and 31.
- **Problem:** Explicit null contact fields, `[REDACTED]` message text, a `DELETED` tombstone with all contact fields null, and `enabled:false` connectors were all flattened into generic PRESENT record verdicts.
- **Change:** Classify only those narrowly visible JSON shapes as REDACTED; carry literal connector enabled/disabled state to policy notes, then emit flow verdicts for `integration_service/data_flow_*`; map `identity_service/tombstone_*` to the tombstone rule.
- **Before:** JSON `RecordState(..., 'PRESENT', ...)` for these rows; integration facts fell through to unknown-category DELETE.
- **After:** JSON records carry REDACTED where contact fields are explicitly cleared; a literal `enabled` boolean becomes a `DISABLE_DATA_FLOW` compliance verdict; tombstones receive `account_tombstone` treatment.
- **Tests added:** targeted synthetic tests pending in the permitted `test_activity_expander.py`.
- **Expected impact:** Recover four residual status mismatches without using proximity or suffix affiliation. Gold step-array match may remain low because missing identity-proof for other rows is a separate issue.
- **Verification:** fresh-cache sample reached 29/32 status, 0/32 exact arrays; case 31 recovered. The cases 26–28 were still blocked solely by the support category alias, addressed by Change 10.

Measured after clearing only the development evidence cache: case 31 recovered, status 29/32; exact arrays 0/32. Cases 26–28 now have REDACTED support facts and compliant disabled-flow verdicts, but `support_platform` remains unmapped, so the policy still requires DELETE. This grounds Change 10.

## Change 10: Map support-platform tickets to the support-message redaction rule
- **Iteration / Fix ID / File:** 14c / targeted-case_26, targeted-case_27, targeted-case_28 / `code/agent/policy/category_map.py`.
- **Grounded in:** `code/.cache/diagnostics/case_26.jsonl` after Change 9 (support_4715 REDACTED but `applicable_rule_ids=[]`); analogous case 27/28 traces; `dataset/deletion_rules.csv:6` (`SUPPORT_MESSAGE` REDACT); `code/agent/policy/rules_loader.py` support-message alias.
- **Problem:** `support_platform` was absent from the system-to-category map, although `support_service` already mapped to `support_tickets`.
- **Change:** Add the direct `support_platform -> support_tickets` alias.
- **Before:** `support_service: support_tickets` only; platform facts fell back to unknown DELETE.
- **After:** Both `support_service` and `support_platform` map to `support_tickets` and the supplied redaction rule.
- **Tests added:** pending permitted-file policy test.
- **Expected impact:** Recover cases 26–28; verify no previously correct status regresses.
- **Verification:** sample reached 32/32 status, 0/32 exact arrays. Full suite after Changes 11–12: 213 passing, 2 failing (hard step gate and the frozen obsolete proximity assertion).

Measured sample after Change 10: all 32 statuses correct, exact step arrays 0/32. The remaining mismatch is upstream missing/incorrectly cited ResourceFacts, not status policy. No previously correct status regressed.

## Change 11: Guard explicit-state interpretations with synthetic tests
- **Iteration / Fix ID / File:** 14c / targeted-case_26, targeted-case_31 / `code/tests/test_activity_expander.py`.
- **Grounded in:** Changes 9–10; diagnostic traces for cases 26–28 show the policy now accepts cleared support contacts and disabled connectors; case 31 tombstone is REDACTED.
- **Problem:** The new shape-specific interpretations were validated only on sample data and could regress silently.
- **Change:** Added four offline synthetic tests for null support contacts, deleted tombstone, disabled connector policy verdict, and support-platform category alias.
- **Before:** Only exact-resource and unowned-404 synthetic guards existed.
- **After:** The permitted Phase 14 test file covers the four newly introduced state/policy paths.
- **Expected impact:** Protect status recoveries without modifying frozen test modules.
- **Verification:** the four new synthetic tests pass; full suite 213 pass, 2 fail for the separately documented gate and frozen conflict.

## Change 12: Encode the sample release gates as an executable test
- **Iteration / Fix ID / File:** 14d / gate / `code/tests/test_activity_expander.py`.
- **Grounded in:** `code/evaluation/step_diff_report.md` after 14c (0/32 exact arrays) and the Phase 14 explicit dual ≥85% gate.
- **Problem:** Status reached 32/32 while exact steps remained 0/32; a status-only test could falsely suggest submission readiness.
- **Change:** Added cached full sample pipeline checks for the Phase 12 status recoveries and an explicit status-plus-exact-step hard gate. The latter is expected to fail until the step evidence gap is solved.
- **Before:** No Phase 14 executable dual-gate assertion.
- **After:** `test_p14_hard_gate_full_sample_pipeline` asserts both metrics; failure says NOT_READY with exact count.
- **Expected impact:** Prevent claiming READY or shipping a zero-step-match artifact.
- **Verification:** `test_p14_hard_gate_full_sample_pipeline` fails explicitly with `NOT_READY: exact steps 0/32`; status regression test passes. This is the required release-blocking signal.
