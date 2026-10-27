# Phase 11 evidence-backed fixes validation

## 1. Fix A: unsupported suffix inference

The only suffix ownership call site found was `code/agent/state/reconstructor.py:18-19` before change; the [audit](phase11_suffix_inference_audit.md) records the search. It is removed. The expander's `_norm` already used exact identifiers and was retained. Four new strict-ownership tests pass. Of the seven expected phantom-record cases, **case_02, case_03, and case_04** flipped from INCOMPLETE to the correct COMPLETE status. Cases 21, 25, 28, and 31 still have other facts/derived activities.

## 2. Fix B: JSON timestamp and system provenance

The timestamp priority is `snapshot_at`, `snapshot_time`, `as_of`, `as_of_date`, `exported_at`, `created_at`, `timestamp`, `generated_at`, then the observed `captured_at`. A nested snapshot timestamp overrides the file default. A pre-audit mtime fallback is available when `audit_at` is passed to the JSON handler. System provenance prefers explicit record/enclosing snapshot fields, then a system-bearing file ID, then a system-bearing path. `RecordState.system_id_source` records the choice. Seven new tests cover these behaviors and exact-resource activity time fallback. **No sample status mismatch recovered** from Fix B. The kickoff called cases 26 and 27 UNDER_DELETED, but the actual Phase 10 [trace](mismatch_triage_report.md#grounded-root-cause-review) shows both were already INCOMPLETE against COMPLETE gold; the expected direction was incorrect.

The frozen [registry call](../agent/evidence/registry.py) at line 15 invokes the JSON handler with only `all_user_ids`, omitting `all_emails` and `audit_at`. Case_08's request email is `gabriel.costa@proton.me` ([sample input line 9](../../dataset/sample_deletion_requests.csv)); `evidence_59` holds `export_001` with that exact `owner_email` ([JSON lines 7–8](../../dataset/evidence/records/customer_export_jobs_20260914.json)), yet its diagnostic trace reports zero extracted records. A read-only probe confirmed `extract(..., identity.all_user_ids)` returns zero rows while `extract(..., identity)` returns `export_001`. That row is still labelled `system_id=json` because the file ID/path contain no system name; the manifest origin is `export_service`. Phase 12 needs both the complete identity bundle and manifest system provenance. Activity-time fallback also cannot prove that a later snapshot existed at the earlier activity timestamp.

## 3. Fix C: deletion-intent stems

The classifier now uses **17 deletion** and **17 non-deletion** compiled word-boundary patterns. Six new tests cover `deleting`, `deleted`, `deletion`, `anonymise`, export-only intent, and a deletion/export tie. Case_12 correctly changed from NOT_APPLICABLE to applicable, but became COMPLETE while the gold is INCOMPLETE because no user evidence facts were extracted. It is not yet a recovered status mismatch.

## 4. Sample accuracy and per-case impact

| Stage | Status matches |
|---|---:|
| Phase 7 | 24/32 (75%) |
| Phase 8 failed tightening | 16/32 (50%) |
| Phase 8 recovery / Phase 9 / Phase 10 | 22/32 (68.75%) |
| Phase 11 | **13/32 (40.625%)** |

Three of the original ten mismatches recovered: cases 02, 03, 04. Twelve previously correct INCOMPLETE cases (08, 09, 10, 11, 13, 14, 15, 16, 18, 19, 20, 22) became incorrect COMPLETE because removing suffix affiliation exposed missing evidence extraction. Case_12 changed to COMPLETE but remains wrong; cases 21, 25, 26, 27, 28, and 31 remain wrong. The [Phase 11 sample triage](phase11_changes.md) and case JSONL traces under `code/.cache/diagnostics/` show this dependency.

## 5. Determinism and structural validation

Two full evidence-enabled 518-case runs produced byte-identical `output.csv` files (SHA-256 `852C71DEC021D8CCE23878C3292C7D1915A3586EA81CD19570D679B8C689CCDB`). Independent CSV inspection confirmed **518 rows, 518 unique IDs, and exact case-ID coverage** against `dataset/deletion_requests.csv`. The sample output contains 32 data rows. The baseline structural validator reports `0/0` checks, so its check counter is not treated as validation evidence. Final full-suite regression: **162 passed**.

## 6. Token usage

Phase 11 used **0 LLM/VLM calls, 0 input tokens, 0 output tokens, and no API key**.

## 7. Open questions and submission decision

**NOT READY.** The 85% threshold was missed. Phase 12 should first repair evidence ingestion at the registry boundary: pass the full `IdentityBundle` and `audit_at` to handlers, extract email-only rows, preserve `captured_at` and system IDs, and verify SQL/log/PDF identity joins against gold resource IDs. Then rerun the sample with strict ownership. Separately, constrain system-time proximity so it cannot claim arbitrary resource ownership. Do not restore numeric-suffix matching merely to recover status scores; the Phase 10 audit showed it creates phantom facts.
