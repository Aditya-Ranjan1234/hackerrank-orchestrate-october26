# Current candidate validation — workflow affiliation and log state

## Evaluation boundary

The production runner reads only participant-facing inputs in `dataset/` and does not import the public sample answer or a previous prediction. The public 32-case comparison is a repeatedly inspected **development** result, not an unbiased estimate of the 518 unlabeled requests. The final `output.csv` was regenerated from all 518 rows of `dataset/deletion_requests.csv` after both changes below.

## Change 1: bounded account workflow affiliation

An account action without a subject is affiliated only when the request has exactly one eligible account deletion **across all outcomes** 30–90 minutes before its workflow report time. The winning action must then say `SUCCESS`; a known other-person owner, a directly owned account already in evidence, a competing requester, a competing action, or an out-of-window event blocks the inference. `reported_status` is never read; `reported_at` stays outside status determination and model tools. The original activity is retained, and the derived row is visible in the case diagnostic.

The rule was calibrated without sample answers: 26/26 independently owned unique 30–90-minute actions belonged to the requester, including 14/14 successful winners. Five masked-owner folds recovered 63 known held-out owners with zero known-owner mistakes; 100 genuinely ownerless candidates remained unscored. A five-minute join was correct in 0/25 known-owner controls. Filtering by `SUCCESS` *before* uniqueness was correct in only 42/90 known-owner controls and was removed. A nearby account-to-analytics pairing was correct in only 1/10 known-owner controls and was rejected. See `workflow_affiliation_probe.md` and `anonymous_affiliation_controls.md`.

The final full run added 23 derived account actions and 23 future `VERIFY_RECORD_ABSENT` checks, each with an empty citation. Six otherwise COMPLETE cases became INCOMPLETE because the workflow action lacked an independent readback; a `SUCCESS` claim is not a proof of absence. The workflow output audit found **zero COMPLETE verifications citing only the inferred activity**.

## Change 2: typed structured-log flags

The first full-run comparison exposed four unrelated `data_flow_*` plans changing between record deletion and flow disable. Their source logs explicitly said `enabled=false`, but the handler had stored the token as text. The state layer therefore missed the disabled-flow signal and asked the model to classify the resource. `log_handler._fields` now converts exact textual Booleans for `enabled` and `restore_allowed`; all other values are left alone. The handler fingerprint invalidated the affected disk-cache entries on the next run. See `log_boolean_regression.md` for the raw source and direct four-case replay.

The corrected full run changed six more cases from INCOMPLETE to COMPLETE after recognizing explicitly disabled connectors. The changed account and connector cases are different sets: relative to the saved pre-iteration output, 12 status rows and 39 ordered step arrays changed. The final status distribution is 136 COMPLETE, 366 INCOMPLETE, and 16 NOT_APPLICABLE. These full-input cases have no public answer labels; the transitions are source-grounded quality checks, not measured accuracy gains.

## Public sample and residual step gap

The sample matches **32/32 statuses (100%)** and **13/32 exact ordered step arrays (40.625%)**, up from 12/32 exact arrays before the bounded workflow rule. Case 30 gained a source-linked future account check, and no previously exact array changed. The typed-log fix changed zero public sample rows. Of 193 gold steps, 168 are present and 25 semantic steps are missing; there are zero extra steps and zero citation differences among shared steps. `step_diff_report.md` and `step_gap_diagnosis.md` trace every residual. The positional system/resource differences arise from the missing rows shifting array positions.

Twelve remaining steps have only ownerless activity, seven have an anonymous raw record omitted by per-user extraction, three have an extracted but unaffiliated anonymous record, and three expected full resource IDs occur nowhere in participant inputs outside the public answer. The September batch's null owner fields, the low-precision temporal pairing controls, and the case 01 negative-snapshot scope issue are recorded in `anonymous_affiliation_controls.md` and `case01_process_trace.md`. The agent abstains rather than inventing user-to-resource edges.

## Full-run and regression checks

| Check | Result |
|---|---:|
| Root `output.csv` data rows, unique and naturally sorted | 518/518 |
| Structural validation | 18,864/18,864; zero errors or warnings |
| Complete per-case diagnostics | 518/518; zero pipeline issues |
| Manifest files considered per case | 94 |
| Expected manifest dispatches | 48,692 |
| Cited steps checked | 952; zero unknown or missing-resource citations |
| Production modules in answer-leak audit | 68; zero findings |
| Account workflow derivations / activity-only COMPLETE citations | 23 / 0 |
| Full pytest suite | 443 passed; one retained exact-array hard-gate failure |

The hard gate requires at least 28/32 exact public arrays and currently observes 13/32. It was not skipped or weakened. The suite was run with its temporary directory inside this repository. Five new typed-log tests cover connector and restore flags, quoted/escaped values, and model bypass when the source already states the flag.

## Model usage and remaining quality risks

The final 518-case run made 10 fresh `gpt-4o-mini` API responses for evidence-file selection: 1,634 input and 805 output tokens, estimated at $0.000728 using the repository's rate table. Other model decisions reused local cache entries; cache hits are not billed or counted as fresh calls. `usage_report.md` has the final run's per-model totals and historic development usage. The key stayed in the repository-local `.env` and is excluded from the archive.

Nine COMPLETE rows still have no resource verification because no subject-linked resource fact was found. Twenty-nine cited files were captured after their case's audit cutoff, although the cited observations carry pre-cutoff row timestamps; this retrospective provenance requires stricter source-availability review. The citation audit reports these separately from invalid IDs. These are visible limitations, not structural-validator errors.

**Readiness against the requested 85% dual accuracy gate: NOT_READY.** The root CSV is a complete, structurally valid 518-row candidate, but the public exact-array threshold is unmet. No hidden-set score is available.
