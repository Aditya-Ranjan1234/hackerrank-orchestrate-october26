# Worklog index

The canonical, append-only Task 1–14 worklog is [`../../worklog.md`](../../worklog.md). It was read before Phase 14 and received per-change entries `14-14a-*` through `14-14d-M`. This index exists because the Phase 14 deliverable list explicitly names `code/evaluation/worklog.md`; it does not replace or truncate the canonical log.

Phase 14 result: Method 2 removed, exact-resource derivation retained, targeted evidence/state/policy fixes made, sample status improved 25/32 → 32/32, exact step arrays stayed 0/32, application LLM/VLM use remained zero. The hard sample-step gate fails and the frozen Phase 13 proximity assertion conflicts with the new invariant. See [`phase14_validation.md`](phase14_validation.md) for the full regression and residual-gap audit.

## Task ID: 15-15a-A
Kept the stale assertion in the frozen Phase 13 test file untouched; the permitted expander tests already assert no proximity derivation. Re-ran the post-Phase-14 gold diff (116/539 positional system-ID mismatches) and traced case_29's extra JSON-path resource to an ID-less nested document. Updated the JSON handler to inherit a visible parent resource ID and added two synthetic tests. Fresh-cache sample, full tests, and output metrics are pending.

## Task ID: 15-15b-B
Measured Phase 15a on fresh extraction: 32/32 sample statuses, 0/32 exact arrays, positional system-ID mismatches 116 → 97; two new tests pass. Traced case_29's missing account/security verification steps to `build_incomplete` omitting compliant verdicts. Added empty-citation compliant verifications and two deduplication tests; whole-sample validation pending.

## Task ID: 15-15c-C
Measured Phase 15b: 32/32 statuses, 1/32 exact arrays, 7/32 matching step counts, 217 tests passing with the same two known failures. Compared near-correct cases semantically: case_29 has 13 of 14 structural step identities, but its missing account verification lacks a proved subject join. Added position-independent diagnostic counts and made the no-argument step diff regenerate the current sample; added four focused tests. Kept latest-evidence citation semantics rather than prioritizing `evidence_92` solely to match gold.

## Task ID: 16-16a-A
Stopped the interrupted Phase 15 repeat process after verifying its identity. Confirmed a key is present without revealing it, installed the OpenAI SDK in this repository's `.venv`, and added an optional cached/traced/retrying client. Live calls and token usage pending.

## Task ID: 16-16a-B
Added bounded JSON prompt templates and schema-validated semantic resolvers. Anonymous affiliation requires independent exact-resource corroboration; model confidence alone is not accepted as ownership evidence. Tests and sample comparison pending.

## Task ID: 16-16a-C
Added an actual-usage tracker for model/purpose token counts and estimated cost from official model pages. No live calls claimed yet.

## Task ID: 16-16a-D
Added schema-filtered OpenAI Vision extraction behind the image handler; retained the old injected callback for frozen tests. Added corrupt-image rejection and mocked Vision tests. No successful live Vision call yet.

## Task ID: 16-16a-E
Wired the four semantic calls through JSON, reconstruction, policy and step building, with pipeline-level key gating. Added mocked client/cache/resolver tests. Initial offline suite: 239 pass, two pre-existing failures; full sample without key: 32/32 status in a new regression test. A live smoke request returned `AuthenticationError` with zero measured response tokens.

## Task ID: 16-16a-F
Added local `requirements.txt` and README environment instructions; documented that presence of a key is not proof of successful API use. Set pytest basetemp inside this repository but outside `code/.cache`, because existing fixture tests scan temporary source trees and archive files; the first basetemp choice under `.cache` produced two false fixture failures, then was corrected.

## Task ID: 16-16b-G
Confirmed two live attempts failed with `AuthenticationError`; added an authentication circuit breaker and a regression test. Ran a 32-case invalid-key sample: 32/32 statuses, 1/32 exact arrays, zero successful responses and tokens. Did not pretend the hybrid path had improved the step gap.

## Task ID: 16-16b-H
Mirrored dependency manifest under `code/` so the existing packager includes it without changing frozen Phase 7 packaging code. Re-ran focused mocked tests (20 pass) and full suite (241 pass; hard exact-step gate and frozen proximity assertion remain the two failures). Added/maintained source-safe in-repository pytest temp directory.

## Task ID: 16-16c-I
Audited the flow-classification prompt and found it lacked the winning row. Passed that row from reconstruction and guarded the policy call to PRESENT evidence-backed integration records. Added mocked tests for raw-row delivery and ABSENT non-promotion. API authentication remains unavailable; no hybrid metric is claimed.

## Task ID: 16-16c-J
Added a valid-PNG mocked SDK transport test. The first full run exposed Pillow absent from the pre-existing `.venv`; installed the already-listed dependency locally and reran the suite: 244 pass, the same two frozen/release-gate failures. The Vision path is now exercised with real image-byte validation but mocked API transport.

## Task ID: 16-16d-K
Regenerated the 518-case rule-only output (518 unique IDs, zero validator errors/warnings, unchanged SHA-256), confirmed the sample was byte-identical across three runs and remained 32/32 status, 1/32 exact steps, and rebuilt the credential-excluding archive. Recorded 0 successful API responses/tokens and NOT_READY; no ownership heuristic or release-gate weakening was introduced.

## Task ID: 16-resume-A
After the user's clarification, proved the inherited process key differed from the repository `.env` without printing either. A bounded call with the `.env` key succeeded. Updated the client to read only that file and added an offline disable switch plus credential-precedence test. The first two live cases exposed malformed Vision `system_id` values and both status regressions; added strict output validation and a synthetic regression test before proceeding.

## Task ID: 16-resume-B
Reran the two pilot cases from cache and recovered both COMPLETE statuses. The 32-case hybrid sample finished at 32/32 statuses and 2/32 exact arrays; `case_11` was the new exact match. Actual sample usage: 377 usage-bearing responses, 440,451 input tokens, 19,296 output tokens, estimated $1.266820. Semantic diff improved from 76 missing/87 extra steps to 62 missing/72 extra, but remains far below the 28/32 gate. Audited traces, found malformed-response token traces incomplete, and changed the client to trace every API attempt; full offline suite 246 pass, two existing failures.

## Task ID: 17-17a-A
Built five type-specific evidence inspectors and a 94-file catalog. Installed missing `pdfplumber` and `pytesseract` Python packages only in `.venv`; the external Tesseract executable remains unavailable. Catalog now has zero parser errors. Added inspector tests and the datapoint extraction map. Rule-only status 32/32; no API calls for this inventory.

## Task ID: 17-17a-B
Ran exact subject/resource audit for cases 01/02/03/04/31 across SQL rows, PDF tables, JSON/log lines, and all 11 visually inspected PNGs. No new direct link found; the case 03 file-level co-mention is not a same-row link. Documented the conditional 27/32 upper bound under strict ownership. API cost $0.

## Task ID: 17-17b-C
Integrated explicit SQL ownership columns, PDF table rows, and JSON-lines log fields into the permitted evidence handlers. Existing and new handler tests pass; rule-only sample remains 32/32 statuses and 1/32 exact arrays. No unsupported suffix/proximity ownership was added.

## Task ID: 17-17c-D
Added EXIF-aware, OCR-first image extraction and cached `gpt-4o-mini` fallback with a shorter same-row prompt. The local host lacks Tesseract, so fallback is active. Added mocked tests for OCR precedence, no-text fallback, EXIF cutoff, exact-ID matching, mini default, and cost projection. A live 32-case hybrid measurement is in progress; measured totals are recorded after completion, never inferred from projections.

## Task ID: 17-17e-E
Grouped 17 historical sample CSVs under `artifacts/csv/` and 17 phase validation reports under `code/evaluation/validations/` using hardlinks, retaining canonical report paths and root `output.csv`. Updated the gold validator's optional historical baseline path. Full offline suite so far: 266 pass, two unchanged failures (hard exact-step gate and frozen proximity assertion); two more new tests were added afterward and await rerun.

## Task ID: 17-17d-F
First fresh mini-Vision hybrid run preserved 32/32 statuses and 2/32 arrays but cost $1.962913 across 352 image responses because high-detail mini images consumed 13,020,359 input tokens. Official OpenAI image-token rules explained the inversion. Switched mini default to low detail and included detail in the cache key; 19 focused image/client tests pass. Low-detail live rerun is in progress. This is an explicit cost-versus-small-text-fidelity tradeoff, not a claimed accuracy gain.

## Task ID: 17-continuation — source backtrace and candidate validation

The canonical detailed worklog is the repository-root `worklog.md`. This continuation searched all 94 evidence files and other participant inputs, repaired structured log extraction, checked 716/716 SQL owner rows, 544/544 JSON pairs and 713/713 structured text pairs, and removed 20 sample citation differences by preferring contemporaneous sources. The final sample is 32/32 statuses and 12/32 exact step arrays; the full 518-row output passes 18,918 structural checks. The suite has 410 passes and one retained exact-step release-gate failure. Full-run usage: 266 gpt-4o-mini responses, 48,833 input and 22,160 output tokens, estimated $0.020621. `phase17_validation.md` gives the per-case source backtrace, 24 retrospective capture citations, nine COMPLETE rows without verifications, and NOT_READY decision.


---
Task ID: 20
Agent: Codex (GPT-6)
Task: Assistant review of all 518 scored output rows, source corrections and change ledger

Work Log:
- Preserved both scored inputs byte-for-byte; compared all rows and found only six differences, all Portuguese deletion requests. Normalized the external title preamble in a separate analysis copy.
- Read every original output plan and request-intent form; reviewed all 11 screenshots, four PDFs, text handover, operational/identity records and deletion rules. Independently enumerated 1,839 JSON/SQL rows and 1,377 resource-bearing log events.
- Corrected request scope, typed SQL/log states, persistent owner fields, attachment categories, legal retention, and control-ID/record-ID confusion. Added exact catalog-alias and full historical-phone corroboration with conflicting-owner rejection.
- Regenerated all 518 cases; after the final historical-phone addition, replayed its sole eligible full-input case through the current pipeline with the full request population. No status or step was hand-assigned from a prior output or public answer.
- Inspected all 115 changed final row plans. Wrote changed_rows.csv with exact before/after arrays and all_518_row_review.csv with final states and unresolved evidence limitations.
- Ran structural, plan-replay, independent owner-coverage, citation, complete-trace and production leakage checks. Added 59 passing tests; retained the existing failing exact-step gate.
- Updated validation, evaluation, trade-offs, usage, README and submission records; rebuilt code.zip with the source-backed corrections and reports.

Stage Summary:
- Output: 518 rows, 2,894 steps; 134 COMPLETE / 374 INCOMPLETE / 10 NOT_APPLICABLE. Relative to the old root: 115 changed rows, 34 status changes, 403 unchanged; 324 added and 228 removed steps.
- Validation: 19,440/19,440 structural checks; 518 plan replays, zero plan-error cases, two warning cases; 1,010 valid citation references; 518 complete traces and zero pipeline errors; 70 reachable production modules and zero answer-leak findings.
- Tests: 502 passing, one pre-existing exact-step gate failing. Public sample: 32/32 statuses and 12/32 exact arrays; 25 missing semantic steps, four source-supported extra steps, zero shared-step citation differences.
- Fresh final-run application usage: 47 gpt-4o-mini calls, 7,701 input and 3,829 output tokens. Final case replay and sample: zero fresh calls. Assistant reasoning usage is separate and not counted by the application.
- Open limits: 32 rows explicitly flagged; one empty COMPLETE, 23 retrospective citations, six workflow-only absence gaps, backup access proof and a separate owner-join dependency. Hidden score unmeasured; >28/30 is not established. NOT_READY for the older 85% exact-array gate.
- Canonical output SHA-256: ed5af1b6733958a82d12b2d5ff0390ce39132a9ced0b062b870e3de0dbc3f20b.
