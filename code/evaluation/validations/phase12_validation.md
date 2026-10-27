# Phase 12 validation and iteration trace

## 1. Fix A — registry handoff
The real registry API is `extract_file(root,file_id,file_path,identities,audit_at)`. The pipeline already supplied the full bundle and audit time; `registry.py` discarded the bundle only for JSON. Dispatch now preserves it. `test_registry_passes_email` proves email-only JSON retrieval.

## 2. Fix B — handler coverage
JSON matches exact IDs, normalized emails, optional hashes, and filters timestamped post-audit rows. SQL matches scalar and parsed JSON-payload IDs/emails/hashes with exact equality. Logs support `service=`, trace-ID resource joins, pipe-delimited readbacks, and hash/email matches. PDF limits matches to scoped IDs/emails/hashes; it does not invent a PDF timestamp. Image VLM remains stubbed and untouched, so scanned images are not covered. Synthetic tests cover these paths.

## 3. Fix C — cache isolation
Key = SHA-256 of file-byte hash, normalized identity sets, primary user ID, and audit cutoff. The first extraction for a key is a miss; the second is a hit (same `extracted_at`); different identities and audit cutoffs have different keys. The orchestrator no longer clears cache per case. Development cache was cleared after handler edits, so stale entries were not used for the final sample. Legacy `load/save` signatures still work.

## 4. Fix D — gold validation
`gold_validation.py` reports status, exact step arrays, per-case divergences, crashes, and regressions. Supplied gold has no intermediate identity/evidence/state/policy labels, so Phase 1–4 accuracy cannot honestly be quantified. [Gold report](gold_validation_report.md) gives the measurable metrics: 25/32 status and 0/32 exact steps.

## 5. Iteration 12a
Full-bundle JSON dispatch and identity-aware cache raised status accuracy from 13/32 (40.625%) to 15/32 (46.875%). Cases 08 and 09 recovered. Early JSON cutoff pruned nested historical snapshots; the test caught this and filtering was moved to each emitted record.

## 6. Iteration 12b
Grounded `service=`/`trace_id` log parsing and pipe-row parsing in `support_replica.log`, `service_events_ap_south_20260915.log`, and `customer_account_handover_20261001.txt`. A local `PIIHit` import shadowed the module-level name and caused per-case evidence extraction to abort; removed it. Corrected rerun reached 23/32 (71.875%). A zero-hour proximity sensitivity run also scored 23/32; this did not justify changing the frozen expander.

## 7. Iteration 12c
Case 16 trace showed identities inside JSON strings in `customer_data_read_replica_20260921.sql:37,52,75`. Recursive exact matching in parsed SQL payloads reached 25/32 (78.125%). Remaining seven cases are not resolved by identifier propagation alone. In case 03, a retained security audit readback is classified fail-closed DELETE and same-system activity inference creates unrelated resource facts. Cases 21, 25, 26, 27, 28, and 31 need later readbacks to override older snapshots, including absent records whose identifying fields are null. These require cross-file ownership/state joins and policy category grounding; no case-ID or numeric-suffix shortcut was added.

## 8. Accuracy progression
| Stage | Status correct |
|---|---:|
| Phase 7 | 24/32 (75%) |
| Phase 8 failed fix | 16/32 (50%) |
| Phase 8 recovery / Phase 9 | 22/32 (68.75%) |
| Phase 11 | 13/32 (40.625%) |
| Phase 12a | 15/32 (46.875%) |
| Phase 12b | 23/32 (71.875%) |
| Phase 12c | 25/32 (78.125%) |

## 9. Regression check
All 13 Phase 11 false-COMPLETE sample cases (08–16, 18–20, 22) now have gold-correct INCOMPLETE status; the kickoff counted 12, but comparison of the stored Phase 11 sample to gold yields 13. Cases 02 and 04 remain correct. Case 03 regressed from COMPLETE to INCOMPLETE after the log expansion. Thus the no-regression gate fails. Residual mismatches: 03, 21, 25, 26, 27, 28, 31. The requested ≥85% hard-gate test cannot be asserted as passing and is not falsely marked green.

## 10. Token usage
Phase 12 made zero LLM/VLM calls and used zero model input/output tokens in the application pipeline. The image VLM was not invoked.

## 11. Ship readiness
**NOT_READY.** 25/32 (78.125%) is below 28/32 (85%), case 03 regressed, and exact step match is 0/32. The 518-case `output.csv` was regenerated: 518 unique IDs, exact input ID coverage, natural-sort order, parseable step arrays, and zero validator errors/warnings. `code.zip` was rebuilt with 114 files and excludes environment/cache/temp directories. These artifacts are diagnostic, not a submission-quality release. Next work needs a source-grounded null-field readback join and a policy mapping for security audit logs, with regression tests before rerun.
