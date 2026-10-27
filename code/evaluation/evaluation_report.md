# Final Evaluation Report

## Case-level status accuracy

The latest authenticated 32-row sample matches **32/32 deletion
statuses (100%)**: 22 INCOMPLETE and 10 COMPLETE. Earlier Phase 8 numbers below
are preserved as iteration history, not current performance. Sample IDs are
separate from the 518 full-dataset case IDs.

## Step-level, field-level, and sequence accuracy

The current `step_diff_report.md` compares the final candidate sample run to
gold: **13/32 exact ordered step arrays (40.625%)**. There are 193 gold steps,
168 generated steps, and 168 position-independent shared semantic steps
(87.05% recall, 100% precision). All 168 shared steps also have the correct
evidence citation. Of 1,176 index-aligned fields across 168 paired steps,
1,058 match (89.97%). Thirteen cases have matching step counts; phase ordering
has zero mismatches. These partial
metrics do not override the exact-array release gate.

## Additional evaluation cases

`code/orchestrator/self_cases.py` defines five self-case targets covering
tombstone hash exposure, sync recreation, backup restore risk, unknown identity,
and over-deletion.

## Failures found and improvements

- Added per-file error isolation; a corrupt evidence source no longer erases the other 93 extractions. Any case error makes the CLI exit nonzero rather than treating a fallback row as submission-ready.
- Added natural case-ID sorting, CSV escaping, and self-validation.
- Evidence cache keys include source bytes, identity, audit cutoff and parser fingerprint; image OCR and model prompts have separate caches. No case-boundary cache clear is needed.
- Removed JSON query-selector/lookup matches as a source of ghost ownership, and added strict full-image Vision plus independent OCR/second-read corroboration.
- A pre-request 404 lookup had seeded a ghost account. Query-start events no longer create PRESENT records, and old negative lookups are excluded from request-time reconstruction. This recovered one exact sample array without changing its status.
- Production import and runtime-read audits found no sample-answer access. All nine CSV schemas and 94 manifest paths passed structural checks. The 32 sample answers were repeatedly used during development, so their score is not an unbiased hidden-case estimate.
- A later direct-owner JSON row can now affiliate an earlier ownerless 404 with the same full resource ID while leaving the earlier timestamp/state authoritative. This filled one more missing semantic step without changing sample status or exact-array count.
- The remaining exact-step gap is source attribution, not Phase 6 ordering: 25 missing semantic steps, zero extra, and zero shared-step citation differences in the latest measured sample. Thirteen cases have at least one gold target absent as a literal full ID from all 94 evidence files; the agent does not manufacture an owner from a case suffix or an uncalibrated timestamp.
- A source-only account-owner veto now covers all 94 evidence formats and 250 direct account IDs. Across full-input requests, the accepted 30–90-minute unique all-outcome account band matched 26/26 independently owned candidates (14/14 for a successful winner). Filtering by SUCCESS before testing uniqueness matched only 42/90, so that unsafe implementation was removed. The corrected bounded affiliation recovered one exact sample array while keeping every previously exact array.
- A completion-proof gate prevents an inferred SUCCESS activity from being cited as proof of an absent account in a COMPLETE case. Without an independent readback, the case becomes INCOMPLETE with an uncited future verification check. Two full-input pilots confirmed the transition, with no change to the 32-case sample score.
- Structured log `enabled` and `restore_allowed` flags are parsed as Booleans when their values are explicitly `true` or `false`. This carries the source's connector/restore state into policy instead of letting a model type label imply an active flow. Six unlabeled full-input cases changed from INCOMPLETE to COMPLETE after explicit disabled-connector readbacks; the public sample rows were unchanged. The source and regression tests are documented in `log_boolean_regression.md`.
- The final full CSV contains 518 naturally sorted rows and passes 18,864/18,864 structural checks; 518/518 diagnostics and 952 citations pass their audits, with zero production import paths to public answers. The retained exact-array gate fails at 13/32, so this remains a candidate rather than a claim of 85% dual accuracy. See `workflow_affiliation_validation.md` for final metrics, source-only calibration, usage, and unresolved provenance limits.

## Phase traceability

See the phase validation reports in `code/evaluation/validations/` and the
Phase 17 source inventories for integration details.
## Phase 8 recovery update

The controlled recovery iteration addressed the 75% → 50% regression by restoring exact-value support for dataset-specific JSON fields and by reconstructing activity-only resources. The recovery sample reached 22/32 statuses (68.75%); 518-row output generation completed and the full regression suite remained green at 121 tests. Residual mismatches are documented in `phase8_recovery_validation.md` and are attributable to missing explicit activity-to-user joins in the supplied operational export.
## Phase 9 activity inference

Added an orchestrator-level activity expander with resource-ID and system-time inference, preserving the frozen Phase 3 modules. The full suite increased to 133 passing tests. In this dataset the expander produced no full-run derivations because the evidence/activity system and resource keys do not overlap, so sample accuracy remained 68.75%; this is recorded as an unresolved schema-join issue.
## Phase 10 grounding and audit

The raw dataset inventory disproved Phase 9's no-overlap explanation: 551 activity and JSON resource IDs overlap, but the activity export has no `target_user_id` column. The real zero-derivation path is missing JSON record timestamps plus an extraction-time fallback after each audit cutoff. Per-case diagnostic logs classified ten status mismatches: seven unsupported resource-suffix affiliations, two untimestamped JSON snapshot states, and one deletion-intent parsing error. Status accuracy remains 22/32 (68.75%). The full output contains 518 rows; 145 tests pass; the LLM/VLM audit recorded zero production calls and no required API key. See `dataset_grounding_report.md`, `mismatch_triage_report.md`, `llm_usage_audit.md`, and `phase10_grounding_validation.md` for citations and follow-up scope.
## Phase 11 surgical fixes

Removed resource-suffix ownership, propagated JSON snapshot timestamps/system IDs, added exact-resource activity-time fallback, and recognized inflected deletion intent. All 162 tests pass, but sample status accuracy fell from 22/32 to 13/32. Three of ten earlier mismatches recovered (02–04); twelve previously correct cases lost facts because the frozen evidence registry passes user IDs but not emails or audit cutoff to JSON extraction. This is a verified integration gap, not a reason to restore unsupported suffix matching. Phase 11 is **not submission-ready**; see `phase11_evidence_backed_fixes_validation.md` and `phase11_changes.md`.

## Phase 12 identity propagation and gold harness

The registry now passes the full bundle and audit cutoff to JSON; the cache key includes identity and audit time. Grounded structured-log, text readback, and serialized-SQL payload extraction recovered all 13 Phase 11 false-COMPLETE sample cases. The suite has 181 passing tests. Status accuracy is 25/32 (78.125%), below the 85% gate; case 03 regressed and six older-snapshot/readback cases remain false-INCOMPLETE. Exact step arrays match 0/32. The deliverables are diagnostic and **not submission-ready**. See `phase12_changes.md`, `phase12_validation.md`, and `gold_validation_report.md`.

## Phase 13 diff-driven diagnosis

The new field-level gold diff found 716/1542 positional mismatches to be extra/missing steps. Case 26 has 159 generated versus 6 gold steps, and only 32 step identities match independent of position across the entire sample (789 generated, 193 gold). All seven residual status mismatches first trace to extra state facts, not a verified Phase 6 mapping defect. Case 03's first wrong decision is the frozen activity expander assigning unrelated same-system activities to the user by time proximity. Phase 6 and status code were not changed to conceal these facts. The sample remains 25/32 statuses and 0/32 exact steps; 197 tests pass. **Not submission-ready.** See `step_diff_report.md`, `phase13_case03_regression_audit.md`, and `phase13_validation.md`.

## Phase 14a exact-resource expander change

Removed same-system time-proximity activity ownership, retaining exact resource matches against evidence belonging to the resolved identity. Generated sample steps dropped from 885 to 312; count mismatches dropped from 716 to 155. Status stayed 25/32 and exact arrays 0/32, so this is a substantial false-fact reduction but not a completed recovery. Further state/policy triage is required before submission.

The allowed expander tests now check the new invariant (206 pass). One frozen Phase 13 diagnostic test still asserts proximity and fails. Case 03's remaining finding is `security_service/audit_record_2016`, which the current policy maps to fail-closed DELETE despite `dataset/deletion_rules.csv` retaining security audit logs.

The conditional security-audit mapping was tested and reverted: it fixed case 03's status but regressed case 14, whose backup restore risk is not being detected. No case-specific policy exception was kept; sample remains 25/32 statuses and 0/32 exact steps.

Phase 14c began a narrower 404 readback repair: the JSON handler now records explicit absent/null-profile service-export rows with no assumed user ownership and their visible `observed_at` timestamp. Downstream use is conditional on a previously proven exact resource ID.

The paired reconstructor join now picks later `evidence_92` ABSENT for case 26's `account_5684`, with an explicit provenance note. Whole-case status and exact step score remain 25/32 and 0/32 because support, security, integration, and backup states/operations still diverge from the gold.

Phase 14c synthetic tests confirmed that 404 rows require a previously proven exact full resource ID. The step diff now has 89 count mismatches (down from 716 before the expander fix) and 45 position-independent exact overlaps (up from 32); the dominant residual is system ID mismatch. The frozen Phase 13 proximity-assertion test remains the sole suite failure.

The reconstructor now preserves explicit backup restore-access state as provenance notes; a policy verdict change is being tested to resolve case 14's missing risk without assuming every backup is restorable.

The paired Phase 14c policy change recovered cases 03, 21, and 25 and preserved case 14's INCOMPLETE status, raising sample status accuracy from 25/32 to 28/32 (87.5%). Exact step arrays remain 0/32; the dominant residual mismatch is system ID. Four status cases (26, 27, 28, 31) remain wrong. The frozen Phase 13 proximity assertion remains one failing test; 208 tests pass.

Phase 14c targeted the last four false-INCOMPLETE cases using literal cleared support contacts, tombstone contact fields, and disabled connector flags from their cited source JSON. The extractor, state notes, and policy interpretation were changed in the conditionally authorized modules; measured validation follows.

After clearing the local extraction cache, case 31 recovered and sample status reached 29/32; exact steps stayed 0/32. The remaining three wrong statuses all had REDACTED support facts but a missing `support_platform` category alias. Added that alias to the supplied SUPPORT_MESSAGE rule; verification follows.

The final Phase 14c category alias recovered cases 26–28: sample statuses now match 32/32. Exact step arrays remain 0/32. Four offline tests were added for the grounded redaction, tombstone, connector, and category interpretations. Readiness remains blocked by step-array mismatch.

Added an executable full-sample dual-gate assertion and a status-regression check. The exact-step gate is expected to fail until the missing ownership and citation evidence is resolved; this failure is not waived.

Phase 14d residual audit: at least five gold-required resource verifications (cases 01, 02, 03, 04, 31) lack a direct identity-owned evidence row under the exact-ownership rule. Even if all other arrays were repaired, these five alone limit exact-array matching to 27/32 without additional affiliation semantics. The current exact result is 0/32. No Phase 6 filter, proximity restoration, or gold-case lookup was added. See `phase14_validation.md` §9 for source-level citations; readiness remains NOT_READY.

The regenerated full `output.csv` contains 518 unique, naturally sorted case IDs covering the full input; all step arrays parse, and the structural validator reports zero errors and warnings. This confirms CSV shape only, not gold step correctness.

## Phase 15a failure and improvement
The post-Phase-14 step diff reports 116/539 positional system-ID mismatches, but case_29 shows a more concrete upstream defect: an ID-less nested search document became a phantom JSON-path resource and three extra steps. The extractor now inherits the parent `search_1993` ID. The frozen Phase 13 proximity test remains a documented constraint conflict; it is not repaired by restoring an unsound ownership heuristic. Validation results follow.

## Phase 15b failure and improvement
After the JSON correction, sample statuses remained 32/32 and exact arrays 0/32, while positional system-ID mismatches fell to 97. Case_29's gold array also verifies already-compliant account and security resources in an otherwise INCOMPLETE case. The step builder previously omitted every compliant verdict in that path; it now appends deduplicated empty-citation verifications. Whole-sample validation follows.

## Phase 15c diagnostic refinement
The mixed-case verification fix preserved 32/32 statuses and raised exact arrays to 1/32; matching step counts rose to 7/32. Positional system-ID mismatches rose to 108 as new, correctly placed verifications shifted comparisons. The diff tool now separates semantic missing/extra steps from citation differences, and its default run regenerates current sample output. We did not promote an older service readback over a later snapshot merely to imitate gold's evidence IDs, nor infer ownerless accounts from case numbers.

## Phase 16a OpenAI integration — in progress
The previous deterministic audit left format classification, flow semantics, and citation choices unresolved. An optional OpenAI adapter now validates bounded JSON responses, caches and traces calls, and records actual usage; its semantic resolver refuses to assign anonymous records without an independent exact-resource ownership join. No improvement or nonzero token count is claimed before end-to-end validation.

The five call sites are wired, with mocked retry/cache/schema/Vision tests and a full rule-only status regression. A live smoke request returned `AuthenticationError`; therefore no actual LLM response tokens have been observed and the hybrid step gate has not been validated. The key must be repaired externally; we retain the deterministic fallback and do not relax the evidence-ownership invariant to chase gold arrays.

Phase 16b added a credential-failure circuit breaker after observing the same `AuthenticationError` in a bounded sample attempt. The sample retained 32/32 statuses and 1/32 exact arrays with zero successful API responses. This is an operational failure, not evidence that LLM semantic decisions are ineffective; it prevents a truthful hybrid accuracy claim. The per-case residual sources remain in `phase15_validation.md` §9.

### Phase 17 — typed inventory, source-grounded audit and cost control
Opened all 94 evidence files through SQL/PDF/image/log/JSON inspectors; repaired a local missing `pdfplumber` dependency. Exact-row audits of cases 01/02/03/04/31 and visual review of 11 PNGs found no new direct subject-to-target-resource link; case 03's file-level co-mention is not ownership. Added structured table/log parsing and OCR-first cached `gpt-4o-mini` Vision fallback. The rule-only sample remains 32/32 statuses, 1/32 exact arrays. The external Tesseract executable is absent, so its observed OCR hit rate is zero; live mini-Vision cost and sample comparison are recorded in `phase17_validation.md` after measurement. Historical CSVs and validation reports were grouped in-repository without changing required submission paths.

Phase 16c source review found that the first flow-classification call lacked the underlying row and could have mistaken a suggestive resource name for a live connector. It now receives the winning raw evidence and is limited to PRESENT evidence-backed integration records. Mocked tests cover both accepted and rejected shapes. This guard does not change the rule-only sample output.

The valid-PNG mocked transport test initially failed because the local virtualenv lacked Pillow, though the package manifest listed it. Installing Pillow 12.3.0 in `.venv` cleared that environment-only failure. The final offline suite has 244 passing tests and the same two known failures; no model response tokens were reported.

Final Phase 16 measurement: rule-only full output has 518 unique rows and zero structural errors/warnings; independent sample scoring remains 32/32 status and 1/32 exact arrays. A repeated sample run was byte-identical. The configured API credential was rejected, so the hybrid path cannot be credited with improvement. The five unowned gold resources identified in Phase 15 also prevent a source-safe 28/32 exact-step claim. Readiness remains NOT_READY despite a valid CSV shape.

Resumed Phase 16 found that the repository `.env` held a working key but an inherited process key did not. The client now uses only `.env`. Two live pilot cases initially regressed because Vision returned `system_id` values that were actually a backup ID or a page title; strict system/resource schema filtering was added before the wider sample run. No raw key or `.env` content was logged or packaged.

The complete 32-case hybrid run preserved all statuses and raised exact step-array matches from 1 to 2 (cases 11 and 14). The position-independent missing/extra counts improved from 76/87 to 62/72, but 23 shared-step citation differences remain. It consumed 377 usage-bearing model responses (440,451 input and 19,296 output tokens; estimated $1.266820). A tracing audit found malformed Vision responses were counted by usage but not individually traced with tokens; the adapter now writes one trace per attempted API response. The exact-step release gate remains unmet, so the 518-case hybrid run is deferred rather than spending substantially more to produce a non-shippable artifact.

An independent second 518-case decision run produced a byte-identical CSV (SHA-256 `c7dc8b76fe328c8127d482397543a444d0784da47a72bd67b6c35d8dbf9147a9`). Diagnostic logging alone was suppressed on the repeat; no decision stage changed. The temporary repeat CSV was removed after verification.

Phase 17 cost iteration: the first `gpt-4o-mini` high-detail hybrid sample remained 32/32 statuses and 2/32 exact arrays but consumed 13,020,359 input tokens across 352 image responses, estimated $1.962913. The issue was image tile billing, not text-model pricing. The client now defaults mini image input to low detail and includes detail in its cache key; the fresh low-detail measurement is tracked separately in `phase17_validation.md`. This trades possible small-text recall for an enforceable cost bound and does not loosen the direct-ownership rule.

### Phase 17 earlier source-grounded iteration

The user's accuracy-first instruction superseded the low-detail experiment. RapidOCR and high-detail `gpt-4o-mini` now cross-check all 11 screenshots; the complete OCR text and schema-validated model disagreements are in `image_text_inventory.md`. `document_text_inventory.md` reproduces the four text-layer PDFs and the plain-text handover. The catalog opened all 94 evidence files with zero parser errors. Nested SQL replica copies, historical-email hashes, source categories, one-off versus recurring flows, exact trace-ID joins, explicit SQL `source_resource_id` joins, and backup verdict deduplication were tested without case-ID production rules.

The final 32-case sample measured **32/32 statuses** and **10/32 exact arrays**, improving the Phase 16 authenticated 2/32 array result while preserving status. The position-independent diff has 27 missing semantic steps, one extra, and 23 citation differences. Many missing verifications require account or anonymous analytics ownership not directly supplied by the evidence; gold also prefers older `evidence_92` citations over later `evidence_02` snapshots in several cases. We preserve temporal provenance and do not infer an owner from a case suffix or timestamp to close this gap. The 85% dual gate remains unmet: **NOT_READY**. See `phase17_validation.md`, `phase17_changes.md`, and `cases_01_02_03_04_31_audit.md` for reproducible traces and trade-offs.

### Phase 17 closure — source backtrace and final validation

An independent pass covered all 94 sources and every direct owner format: 716 SQL rows across 127 tables (including historical aliases), 544 JSON owner/resource pairs, and 713 structured log/TXT pairs, with zero extraction omissions. A case-level gold backtrace identified 26 missing semantic steps, zero extra steps, and zero remaining shared-step citation differences. Sixteen missing full IDs do not occur in evidence; thirteen are named only by ownerless activity rows and three do not occur in any participant input other than the public sample answer. The direct-owner calibration rejected time-only and numeric-suffix affiliation. Four cited gold files lack the literal target ID, including `evidence_54` for `account_001`; this is a source-provenance gap, not a reason to hardcode the public answer.

The final authenticated sample is **32/32 status** and **12/32 exact ordered step arrays**. The full output has 518 naturally sorted rows, 18,918/18,918 structural checks, 518/518 complete diagnostics, and 944 valid cited resources with no missing/unknown citation IDs. Twenty-four citations point to files collected after their audit cutoff, but all 24 cited resources have an extracted observation at or before that cutoff; this capture-versus-row timing distinction remains documented. Nine COMPLETE outputs have empty verification arrays and are explicitly flagged as an evidence-quality risk. The final full run recorded 266 `gpt-4o-mini` responses, 48,833 input and 22,160 output tokens; estimated usage cost is $0.020621. The regression suite has 410 passes and one intentionally retained exact-step hard-gate failure. **NOT_READY** for the 85% dual gate. See `phase17_validation.md`, `sample_gold_backtrace.md`, `step_diff_report.md`, `citation_audit.md`, and `usage_report.md`.

### Post-Phase 17 causal diagnosis of exact-step failures

`step_gap_diagnosis.md` compares the public sample with each case's saved extraction, derivation, state, policy, and step trace. All 26 residual differences are missing semantic steps: 13 targets occur only in ownerless activity rows, seven anonymous raw evidence records are omitted by the per-user extractor, three anonymous 404 records are extracted but cannot be affiliated in state reconstruction, and three full target IDs occur in no participant input. Zero missing steps reach a ResourceFact or policy verdict, so the apparent positional system and operation differences are array shifts, not a step-mapping defect. Cases 01, 02 and 04 match COMPLETE despite having zero policy verdicts; this is a vacuous-completeness risk.

The candidate timing repair was tested without public answer labels: among 60 full requests with exactly one account deletion in the five minutes before `reported_at`, 25 events had independently established owners and **none** belonged to the requester. The earlier nearest-event control was correct for only 71/212 evaluable requests. Neither temporal heuristic was put into production. Six offline diagnosis tests pass; the full suite now has **416 passes and one retained exact-step gate failure**. The public fit remains 32/32 statuses and 12/32 exact arrays; the 85% dual release gate remains **NOT_READY**.

### Case 01 process-signal follow-up

The user identified a stronger temporal clue than the first backtrace described. `activity_3342` claims deletion of `account_001` at 16:41:43, exactly **17 seconds** before case 01's reported time. `evidence_54` is a later SQL snapshot, captured before audit, with zero `account_001` rows in both primary and failover tables. This provides a plausible process-to-case candidate and a conditional negative snapshot, but neither source has an explicit `user_01` or case key. An offline counterfactual that attaches the activity to `user_01` emits the missing verification but cites `activity_3342`; matching the gold `evidence_54` citation also requires a closed-world SQL absence check. The production code was not changed because a time-only join failed 25/25 independently owned five-minute full-request controls, and the special process wording occurs only near public sample requests. `case01_process_trace.md` records the exact timeline, queries, counterfactual and trade-off.


### Scored-output review — 518-row source and plan audit

The assistant reviewed every original output row and every changed final row. The two scored files differ in only six Portuguese deletion requests; the reference is not a label oracle. The revised output changes **115/518 rows and 34 statuses** versus the old root, with **324 added and 228 removed steps**. Corrections cover explicit non-deletion scope, historical identifiers, persisted connector and attachment ownership, typed state flags, legal holds, catalog-visible aliases and phantom search records created from connector IDs. Source-backed examples and decisions are in `row_review_findings.md`; complete before/after rows are in `artifacts/csv/changed_rows.csv` and every reviewed case in `artifacts/csv/all_518_row_review.csv`.

The final 518 rows pass **19,440 structural checks**. The independent plan replay finds zero contradictions against 1,588 recorded policy verdicts, with two warning cases. Citation audit checks 1,010 sources, including three catalog-alias proofs, with no invalid resource references. All 518 traces are complete and the independent JSON/SQL/log owner scan finds no missed exactly owned resources within its documented scope. Production answer isolation finds zero issues across 70 reachable modules.

Tests: **502 passed, one existing hard gate failed**. Public sample: **32/32 status, 12/32 exact arrays**, compared with 13/32 before review; 25 missing semantic steps, four additional source-supported steps and zero shared-step citation differences. The added historical-phone attachment and catalog tombstone are retained because participant sources establish them; the output does not suppress evidence to fit examples. No new hidden score is available. The older 85% dual gate remains NOT_READY.

Thirty-two full rows carry explicit limits in the ledger, including 23 retrospective captures, six activity-only absence claims, the unresolved case_63 owner conflict, case_55's missing restore-block proof and case_430's separately established account ownership. The current run is described in `score_iteration_validation.md`, which supersedes historical current-run metrics above. This is a reviewable corrected submission, not proof of >28/30.
