# Phase 13 validation

## 1. Dominant step difference

`COUNT_MISMATCH` is 716/1542 positional mismatches (46.43%). The five largest cases include case 26: 159 generated steps versus 6 gold steps. Position-independent exact overlap is only 32 step identities out of 789 generated and 193 gold. Thus 0/32 exact arrays is **not proof of a systematic Phase 6 mapper defect**; the primary error is extra/missing upstream resource facts and verdicts. [Full diff](step_diff_report.md).

## 2. Phase 6 fix decision

No Phase 6 production edit was made. The grounded diff recommends repairing upstream fact ownership and audit-time state before altering step generation. Step-array match remains 0/32 (0%), below the 85% gate. Applying a builder count filter to conceal false facts would produce a misleading audit.

## 3. Case 03 regression

`evidence_94` confirms `account_7566` absent, but `activity_expander.py` uses a same-system ±24h match to derive unrelated cache/search/analytics activity for `user_43`. The trace's first extra finding is `cache_5233` from `activity_3962`; its activity row contains no user identifier or exact `account_7566` match. A security audit record is also miscategorized, but correcting it alone would not remove the unrelated facts. The first wrong decision is in an explicitly frozen orchestrator module, so no status/step patch was applied. Case 03 remains INCOMPLETE versus gold COMPLETE, with nonmatching steps. [Audit](phase13_case03_regression_audit.md).

## 4. Iteration results

| Iteration | Status accuracy | Exact step arrays | Tests | Finding |
|---|---:|---:|---:|---|
| Phase 12 baseline | 25/32 (78.125%) | 0/32 (0%) | 181 | Seven status errors |
| 13a | 25/32 (78.125%) | 0/32 (0%) | 197 | Diff proved count/ownership mismatch; no justified Phase 6 edit |
| 13b | 25/32 (78.125%) | 0/32 (0%) | 197 | Seven cases triaged; all first candidate phase = state |
| 13c | 25/32 (78.125%) | 0/32 (0%) | 197 | Corrective expander is frozen; no case-ID shortcut or unauthorized edit |

## 5. Per-case gold comparison

| Case | Ours | Gold | Status match | Step match |
|---|---|---|---|---|
| 01 | COMPLETE | COMPLETE | yes | no |
| 02 | COMPLETE | COMPLETE | yes | no |
| 03 | INCOMPLETE | COMPLETE | no | no |
| 04 | COMPLETE | COMPLETE | yes | no |
| 05 | INCOMPLETE | INCOMPLETE | yes | no |
| 06 | INCOMPLETE | INCOMPLETE | yes | no |
| 07 | INCOMPLETE | INCOMPLETE | yes | no |
| 08 | INCOMPLETE | INCOMPLETE | yes | no |
| 09 | INCOMPLETE | INCOMPLETE | yes | no |
| 10 | INCOMPLETE | INCOMPLETE | yes | no |
| 11 | INCOMPLETE | INCOMPLETE | yes | no |
| 12 | INCOMPLETE | INCOMPLETE | yes | no |
| 13 | INCOMPLETE | INCOMPLETE | yes | no |
| 14 | INCOMPLETE | INCOMPLETE | yes | no |
| 15 | INCOMPLETE | INCOMPLETE | yes | no |
| 16 | INCOMPLETE | INCOMPLETE | yes | no |
| 17 | INCOMPLETE | INCOMPLETE | yes | no |
| 18 | INCOMPLETE | INCOMPLETE | yes | no |
| 19 | INCOMPLETE | INCOMPLETE | yes | no |
| 20 | INCOMPLETE | INCOMPLETE | yes | no |
| 21 | INCOMPLETE | COMPLETE | no | no |
| 22 | INCOMPLETE | INCOMPLETE | yes | no |
| 23 | INCOMPLETE | INCOMPLETE | yes | no |
| 24 | INCOMPLETE | INCOMPLETE | yes | no |
| 25 | INCOMPLETE | COMPLETE | no | no |
| 26 | INCOMPLETE | COMPLETE | no | no |
| 27 | INCOMPLETE | COMPLETE | no | no |
| 28 | INCOMPLETE | COMPLETE | no | no |
| 29 | INCOMPLETE | INCOMPLETE | yes | no |
| 30 | INCOMPLETE | INCOMPLETE | yes | no |
| 31 | INCOMPLETE | COMPLETE | no | no |
| 32 | INCOMPLETE | INCOMPLETE | yes | no |

## 6. Regression and seven-case triage

Cases 02 and 04 retain correct statuses; case 03 fails both gates. All 13 Phase 12 recovered false-COMPLETE cases retain gold-correct INCOMPLETE status (the kickoff says 12, but stored Phase 11 versus gold yields 13); none have an exact gold step array. Read-only `triage_mismatches.py` classified cases 03, 21, 25, 26, 27, 28, and 31 as extra-resource/state mismatches. `debug_case.py` runs for all seven showed derived-activity counts of 14, 2, 2, 41, 13, 13, and 3 respectively. The recurring `audit_record_7348` attribution is a system-time proximity inference without direct user evidence; cases 26–28 also need later null-field readbacks to override older snapshots on full resource ID. A zero-hour proximity sweep in Phase 12 did not change status accuracy; broad window tuning alone is insufficient.

## 7. Token usage

Zero application LLM/VLM calls; zero input/output tokens. No image model was invoked.

## 8. Ship readiness

**NOT_READY:** status 25/32 < 28/32, exact steps 0/32 < 28/32, case 03 regressed. The ≥85% hard-gate test cannot honestly pass; it is therefore not marked green. The Phase 12 518-row output remains the latest production result because Phase 13 made no production decision change. A safe next phase must explicitly authorize a source-grounded activity-expander affiliation fix and a cross-file exact-resource readback join, followed by step-level revalidation. No numerical-suffix ownership or case-ID exception should be introduced.

Final deterministic rerun: the 518-row `output.csv` SHA-256 remained `361D15D619ECF9BE957D2AB20BE92DB221A48E3F3008745AA6B9492AB34C1BC1` before and after Phase 13's full regeneration. It has 518 unique IDs, exact request-ID coverage, natural-sort order, and parseable step arrays. Two `step_diff_report.md` runs were also byte-identical (SHA-256 `ABC208F67B6C69336B18E5ABD82A6615C05F59EEC899B03E62BAA4F240F903B7`). Final suite: 197/197 passing.
