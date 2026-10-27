# Phase 14 validation — grounded recovery, unresolved exact steps

## 1. Fix A: remove Method 2

`activity_expander.py` now derives only from a full resource-ID match or an explicit `evidence_<resource_id>` file ID when that same evidence contains an identity-matched record. Same-system ±24h proximity is gone. The sample's generated step count fell from 885 (Phase 13) to 312 after this change; count mismatches fell from 716 to 155. Existing originals are retained, derived IDs deterministic, and post-audit evidence excluded. The deprecated `time_window` parameter remains callable but has no effect.

## 2. Fix B: verify evidence actually belongs to the user

Every candidate evidence row passes `_normalize_user_ref` before entering the exact-resource index. A resource match with a different subject produces no derived activity. Ten new expander cases test identity, exactness, explicit file ID, deduplication, cutoff, and determinism. Blank-owner 404 readbacks are likewise joined only to a previously identity-proven full `(system_id, resource_id)` pair; two additional tests guard against cross-user assignment.

## 3. Case 03 recovery

Status recovered from INCOMPLETE to gold COMPLETE after the unsupported cache affiliation disappeared and `security_service/audit_record_2016` received the supplied security-audit RETAIN rule. Case 14's active backup remains INCOMPLETE because literal restore-access evidence is separately evaluated. Case 03's exact steps still **do not** match gold: ours verifies `account_7566` and `audit_record_2016`, while gold additionally verifies anonymous `analytics_9406` from `evidence_94`. That log row has `customer_reference=null`, `email=null`, `phone=null`, and `email_hash=null`; the separate `ANONYMIZE_RECORD` activity does not identify a user. No source-grounded user link has been found.

## 4. Per-iteration results

| Iteration | Status match | Exact step arrays | Generated steps | Tests |
|---|---:|---:|---:|---|
| Phase 13 baseline | 25/32 (78.125%) | 0/32 | 885 | 197 pass |
| 14a exact-resource inference | 25/32 | 0/32 | 312 | 206 pass, 1 frozen obsolete test fails |
| 14b isolated audit-rule trial (reverted) | 25/32 | 0/32 | — | 206 pass, 1 fail |
| 14c explicit 404 and backup treatment | 28/32 (87.5%) | 0/32 | — | 208 pass, 1 fail |
| 14c redaction/connector/tombstone state | 29/32 (90.625%) | 0/32 | — | 208 pass, 1 fail |
| 14c support category alias | **32/32 (100%)** | **0/32 (0%)** | **191** | 213 pass, 2 fail (including hard gate) |
| 14d residual audit | 32/32 | 0/32 | 191 | same |

The step diff now counts 70 positional COUNT_MISMATCH records and 116 SYSTEM_ID_MISMATCH fields (the largest field class). Only one of 32 cases has equal step count; total generated steps 191 versus gold 193. This is not evidence that a Phase 6 count filter would be sound: positional mismatches include distinct missing and extra resources.

## 5. Per-case gold comparison

| Case | Status | Exact steps | Case | Status | Exact steps |
|---|---|---|---|---|---|
| 01 | match | no | 17 | match | no |
| 02 | match | no | 18 | match | no |
| 03 | match | no | 19 | match | no |
| 04 | match | no | 20 | match | no |
| 05 | match | no | 21 | match | no |
| 06 | match | no | 22 | match | no |
| 07 | match | no | 23 | match | no |
| 08 | match | no | 24 | match | no |
| 09 | match | no | 25 | match | no |
| 10 | match | no | 26 | match | no |
| 11 | match | no | 27 | match | no |
| 12 | match | no | 28 | match | no |
| 13 | match | no | 29 | match | no |
| 14 | match | no | 30 | match | no |
| 15 | match | no | 31 | match | no |
| 16 | match | no | 32 | match | no |

## 6. Regression check

Cases 02, 03, and 04 all match gold **status**, but none matches its full step array. All 13 documented Phase 12 recovered statuses (08–16, 18–20, 22; the kickoff calls them 12) remain correct. The executable full-sample regression test confirms this. The Phase 13 frozen test `test_same_system_proximity_is_not_exact_resource_ownership` still asserts the very Method 2 behavior Phase 14 explicitly removed. It is the one legacy test failure; editing that frozen file or restoring Method 2 would violate this phase's instructions.

## 7. Token usage

Phase 14 made **zero LLM/VLM calls and used zero model input/output tokens**. All inference and tests are local Python.

## 8. Ship readiness

**NOT_READY.** Status exceeds the 85% gate (32/32); exact step arrays fail it (0/32). The deliberate `test_p14_hard_gate_full_sample_pipeline` fails with `NOT_READY: exact steps 0/32`, and the incompatible frozen legacy test also fails. Do not present the package as a passing release or silently waive these checks. The generated `output.csv` and `code.zip` are diagnostic/submission artifacts with this limitation disclosed.

Full `output.csv` validation: 518 rows, 518 unique case IDs, exact input ID coverage, natural order, every `steps_json` parseable as an array, zero validator errors and zero warnings. SHA-256 on both full runs: `c7dc8b76fe328c8127d482397543a444d0784da47a72bd67b6c35d8dbf9147a9`; byte-identical determinism **verified**. The second run disabled diagnostic logging only (decision pipeline unchanged) to avoid rewriting the first run's per-case traces. Its temporary CSV was removed after hash comparison.

`code.zip` was rebuilt with 164 source/documentation files. Archive inspection found zero `.venv`, `.cache`, `__pycache__`, `.git`, `.pytest_cache`, or `.env` entries. It includes this validation report and the canonical root worklog. This is an artifact integrity check, not a release-gate pass.

Independent `gold_validation.py` rerun confirmed 32/32 statuses and 0/32 exact step arrays. Its report is `code/evaluation/gold_validation_report.md`; this is a failed step gate, not a green gold validation.

## 9. Residual gaps and root-cause audit

At least five gold step requirements have no directly identity-owned source record under the Phase 14 exact-ownership rule:

- **Cases 01, 02, 04:** gold cites `evidence_54` for absent `account_001`, `account_002`, `account_004`. `dataset/evidence/databases/customer_accounts_failover_replica_20260902.sql` lists only account_005, account_8741, account_9116, and account_7204; it never contains those three resource IDs. Their `system_activity.csv` DELETE rows have no user ID. A numeric case/resource suffix is not ownership evidence.
- **Case 03:** `dataset/evidence/logs/resource_lookup_trace_20260926_103856.log:42-43` reports `analytics_9406` with all identity fields null. `dataset/system_activity.csv:3853` records an anonymization operation for that resource without a user ID. It cannot be attributed to case 03 by the permitted exact resource-and-subject join.
- **Case 31:** `dataset/evidence/records/customer_data_snapshot_bundle_20260915.json:1-10` has an empty account collection, not an `account_4857` row. `dataset/system_activity.csv:3683` claims a DELETE for `account_4857` without a user ID. Gold's absent verification cites `evidence_51`, which has no account_4857 row.

Those five cases alone would cap exact-array accuracy at 27/32 (84.375%) **if** direct identity evidence were the only permitted affiliation route; the actual current result is lower because other cases also have missing anonymous analytics/flow facts, different evidence citations, and extra resource facts. Gold's case 26 expects all six verifications cited to `evidence_92`, while ours cites `evidence_02` for four and omits the anonymous analytics row. Addressing this responsibly needs a documented cross-system subject/resource link or a change in audit-evidence semantics, not resurrection of time proximity or a Phase 6 count filter. The explicitly frozen files and no-speculative-ownership rule prevent a justified ≥85% exact-step repair in this iteration.
