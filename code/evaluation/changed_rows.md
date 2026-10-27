# Changed output rows — source review

Compared with the preserved 21.6/30 root submission: **115 of 518 rows changed**, 403 unchanged. Row numbers include the CSV header (first data row is 2).

The assistant inspected all 518 original row plans, grouped recurring source errors, reopened the relevant source records, and checked the regenerated rows. Scripts enumerate, compare, and replay plans; they do not supply hidden answer labels. The ledger does not assert a new HackerRank score.

Full before/after JSON arrays and exact added/removed steps are in `artifacts/csv/changed_rows.csv`. Every case, including unchanged and unresolved cases, is in `artifacts/csv/all_518_row_review.csv`.

| CSV row | Case | Before → after | Step count | Reason |
|---:|---|---|---|---|
| 2 | case_33 | INCOMPLETE → INCOMPLETE | 3 → 6 | Exact catalog alias joins the canonical resource to a visible artifact; catalog identity and file existence jointly support the step |
| 3 | case_34 | INCOMPLETE → INCOMPLETE | 4 → 7 | Historical full phone number uniquely identifies the subject in an attachment scan; apply rule_06 DELETE |
| 6 | case_37 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 15 | case_46 | COMPLETE → COMPLETE | 1 → 2 | Exact catalog alias joins the canonical resource to a visible artifact; catalog identity and file existence jointly support the step |
| 18 | case_49 | INCOMPLETE → INCOMPLETE | 9 → 6 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 23 | case_54 | NOT_APPLICABLE → INCOMPLETE | 0 → 13 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 25 | case_56 | COMPLETE → INCOMPLETE | 1 → 4 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 26 | case_57 | INCOMPLETE → INCOMPLETE | 5 → 6 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation; Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction |
| 30 | case_61 | COMPLETE → INCOMPLETE | 0 → 3 | Exact catalog alias joins the canonical resource to a visible artifact; catalog identity and file existence jointly support the step |
| 31 | case_62 | INCOMPLETE → INCOMPLETE | 11 → 14 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 33 | case_64 | INCOMPLETE → COMPLETE | 7 → 5 | Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction; Explicitly null requester contact fields or [REDACTED] message readback prove compliance; remove redundant remediation |
| 37 | case_68 | INCOMPLETE → INCOMPLETE | 8 → 8 | Same obligation; citation now recognizes typed flow/restore state and prefers a contemporaneously captured source |
| 40 | case_71 | INCOMPLETE → INCOMPLETE | 8 → 8 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 54 | case_85 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 62 | case_93 | NOT_APPLICABLE → INCOMPLETE | 0 → 12 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 73 | case_104 | INCOMPLETE → INCOMPLETE | 10 → 13 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 78 | case_109 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 79 | case_110 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 81 | case_112 | INCOMPLETE → INCOMPLETE | 5 → 6 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation; Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction |
| 85 | case_116 | INCOMPLETE → INCOMPLETE | 8 → 8 | Same obligation; citation now recognizes typed flow/restore state and prefers a contemporaneously captured source |
| 88 | case_119 | INCOMPLETE → INCOMPLETE | 8 → 8 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 91 | case_122 | INCOMPLETE → INCOMPLETE | 8 → 8 | Same obligation; citation now recognizes typed flow/restore state and prefers a contemporaneously captured source |
| 100 | case_131 | INCOMPLETE → INCOMPLETE | 13 → 13 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 101 | case_132 | NOT_APPLICABLE → INCOMPLETE | 0 → 7 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 102 | case_133 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 114 | case_145 | INCOMPLETE → INCOMPLETE | 9 → 6 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 124 | case_155 | INCOMPLETE → INCOMPLETE | 5 → 6 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation; Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction |
| 127 | case_158 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 138 | case_169 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 140 | case_171 | NOT_APPLICABLE → INCOMPLETE | 0 → 5 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 144 | case_175 | INCOMPLETE → COMPLETE | 6 → 4 | SQLite zero means disabled connector; verify disabled rather than delete a configuration record |
| 148 | case_179 | INCOMPLETE → INCOMPLETE | 4 → 4 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 150 | case_181 | INCOMPLETE → INCOMPLETE | 10 → 7 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 172 | case_203 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted ticket_attachment uploaded_by exactly identifies the exclusive attachment owner; apply rule_06 DELETE |
| 173 | case_204 | INCOMPLETE → INCOMPLETE | 5 → 6 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation; Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction |
| 174 | case_205 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 178 | case_209 | INCOMPLETE → INCOMPLETE | 10 → 13 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 179 | case_210 | NOT_APPLICABLE → INCOMPLETE | 0 → 7 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 181 | case_212 | INCOMPLETE → INCOMPLETE | 5 → 8 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 182 | case_213 | INCOMPLETE → COMPLETE | 7 → 5 | Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction; Explicitly null requester contact fields or [REDACTED] message readback prove compliance; remove redundant remediation |
| 186 | case_217 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 189 | case_220 | INCOMPLETE → INCOMPLETE | 11 → 9 | Explicit legal-hold/retention evidence requires rule_13 RETAIN, not DELETE |
| 196 | case_227 | INCOMPLETE → INCOMPLETE | 7 → 7 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 198 | case_229 | INCOMPLETE → INCOMPLETE | 10 → 7 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 210 | case_241 | INCOMPLETE → INCOMPLETE | 9 → 6 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 218 | case_249 | NOT_APPLICABLE → INCOMPLETE | 0 → 12 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 223 | case_254 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 230 | case_261 | INCOMPLETE → INCOMPLETE | 10 → 8 | Explicit legal-hold/retention evidence requires rule_13 RETAIN, not DELETE |
| 232 | case_263 | INCOMPLETE → INCOMPLETE | 14 → 14 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 233 | case_264 | INCOMPLETE → COMPLETE | 7 → 5 | Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction; Explicitly null requester contact fields or [REDACTED] message readback prove compliance; remove redundant remediation |
| 244 | case_275 | INCOMPLETE → INCOMPLETE | 7 → 7 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 257 | case_288 | NOT_APPLICABLE → INCOMPLETE | 0 → 3 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 258 | case_289 | INCOMPLETE → INCOMPLETE | 9 → 6 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 266 | case_297 | INCOMPLETE → COMPLETE | 8 → 4 | SQLite zero means disabled connector; verify disabled rather than delete a configuration record; Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction; Explicitly null requester contact fields or [REDACTED] message readback prove compliance; remove redundant remediation |
| 270 | case_301 | INCOMPLETE → INCOMPLETE | 9 → 6 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 277 | case_308 | INCOMPLETE → INCOMPLETE | 5 → 6 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation; Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction |
| 280 | case_311 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted ticket_attachment uploaded_by exactly identifies the exclusive attachment owner; apply rule_06 DELETE |
| 286 | case_317 | INCOMPLETE → INCOMPLETE | 14 → 14 | Same obligation; citation now recognizes typed flow/restore state and prefers a contemporaneously captured source |
| 289 | case_320 | INCOMPLETE → INCOMPLETE | 8 → 8 | Same obligation; citation now recognizes typed flow/restore state and prefers a contemporaneously captured source |
| 290 | case_321 | INCOMPLETE → INCOMPLETE | 8 → 8 | Same obligation; citation now recognizes typed flow/restore state and prefers a contemporaneously captured source |
| 294 | case_325 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 296 | case_327 | NOT_APPLICABLE → COMPLETE | 0 → 2 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 304 | case_335 | INCOMPLETE → COMPLETE | 8 → 4 | SQLite zero means disabled connector; verify disabled rather than delete a configuration record; Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction; Explicitly null requester contact fields or [REDACTED] message readback prove compliance; remove redundant remediation |
| 306 | case_337 | INCOMPLETE → INCOMPLETE | 9 → 6 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 318 | case_349 | INCOMPLETE → INCOMPLETE | 9 → 6 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 322 | case_353 | INCOMPLETE → INCOMPLETE | 10 → 13 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 325 | case_356 | INCOMPLETE → INCOMPLETE | 10 → 13 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 328 | case_359 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted ticket_attachment uploaded_by exactly identifies the exclusive attachment owner; apply rule_06 DELETE |
| 330 | case_361 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 335 | case_366 | NOT_APPLICABLE → INCOMPLETE | 0 → 14 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 340 | case_371 | INCOMPLETE → INCOMPLETE | 8 → 8 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 342 | case_373 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 354 | case_385 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 366 | case_397 | INCOMPLETE → INCOMPLETE | 9 → 6 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 373 | case_404 | INCOMPLETE → INCOMPLETE | 10 → 13 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 374 | case_405 | NOT_APPLICABLE → INCOMPLETE | 0 → 7 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 376 | case_407 | INCOMPLETE → INCOMPLETE | 10 → 13 | Persisted ticket_attachment uploaded_by exactly identifies the exclusive attachment owner; apply rule_06 DELETE |
| 379 | case_410 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 388 | case_419 | INCOMPLETE → INCOMPLETE | 8 → 8 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 390 | case_421 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 400 | case_431 | INCOMPLETE → INCOMPLETE | 7 → 7 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 401 | case_432 | INCOMPLETE → INCOMPLETE | 10 → 8 | Explicit legal-hold/retention evidence requires rule_13 RETAIN, not DELETE |
| 402 | case_433 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 413 | case_444 | NOT_APPLICABLE → INCOMPLETE | 0 → 6 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 414 | case_445 | INCOMPLETE → INCOMPLETE | 9 → 6 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 424 | case_455 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted ticket_attachment uploaded_by exactly identifies the exclusive attachment owner; apply rule_06 DELETE |
| 429 | case_460 | INCOMPLETE → INCOMPLETE | 7 → 5 | Explicit legal-hold/retention evidence requires rule_13 RETAIN, not DELETE |
| 430 | case_461 | INCOMPLETE → INCOMPLETE | 10 → 13 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 432 | case_463 | INCOMPLETE → COMPLETE | 7 → 5 | Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction; Explicitly null requester contact fields or [REDACTED] message readback prove compliance; remove redundant remediation |
| 433 | case_464 | INCOMPLETE → COMPLETE | 7 → 5 | Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction; Explicitly null requester contact fields or [REDACTED] message readback prove compliance; remove redundant remediation |
| 438 | case_469 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 442 | case_473 | INCOMPLETE → INCOMPLETE | 10 → 8 | Explicit legal-hold/retention evidence requires rule_13 RETAIN, not DELETE |
| 445 | case_476 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 448 | case_479 | COMPLETE → INCOMPLETE | 1 → 4 | Persisted ticket_attachment uploaded_by exactly identifies the exclusive attachment owner; apply rule_06 DELETE |
| 449 | case_480 | COMPLETE → COMPLETE | 3 → 4 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 450 | case_481 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 451 | case_482 | INCOMPLETE → INCOMPLETE | 4 → 7 | Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 452 | case_483 | NOT_APPLICABLE → INCOMPLETE | 0 → 12 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 472 | case_503 | COMPLETE → INCOMPLETE | 1 → 4 | Persisted ticket_attachment uploaded_by exactly identifies the exclusive attachment owner; apply rule_06 DELETE |
| 474 | case_505 | INCOMPLETE → INCOMPLETE | 7 → 8 | Explicit legal-hold/retention evidence requires rule_13 RETAIN, not DELETE; Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation |
| 480 | case_511 | INCOMPLETE → INCOMPLETE | 7 → 5 | Explicit legal-hold/retention evidence requires rule_13 RETAIN, not DELETE |
| 484 | case_515 | INCOMPLETE → INCOMPLETE | 8 → 8 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 486 | case_517 | INCOMPLETE → INCOMPLETE | 11 → 8 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 491 | case_522 | NOT_APPLICABLE → INCOMPLETE | 0 → 5 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |
| 496 | case_527 | INCOMPLETE → INCOMPLETE | 13 → 13 | Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT |
| 498 | case_529 | INCOMPLETE → INCOMPLETE | 10 → 7 | SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record |
| 502 | case_533 | INCOMPLETE → NOT_APPLICABLE | 4 → 0 | Request authorizes correction/access/marketing-only action or explicitly rejects account deletion |
| 503 | case_534 | COMPLETE → NOT_APPLICABLE | 0 → 0 | Request authorizes correction/access/marketing-only action or explicitly rejects account deletion |
| 505 | case_536 | COMPLETE → NOT_APPLICABLE | 0 → 0 | Request authorizes correction/access/marketing-only action or explicitly rejects account deletion |
| 506 | case_537 | COMPLETE → NOT_APPLICABLE | 0 → 0 | Request authorizes correction/access/marketing-only action or explicitly rejects account deletion |
| 507 | case_538 | COMPLETE → NOT_APPLICABLE | 0 → 0 | Request authorizes correction/access/marketing-only action or explicitly rejects account deletion |
| 508 | case_539 | COMPLETE → NOT_APPLICABLE | 0 → 0 | Request authorizes correction/access/marketing-only action or explicitly rejects account deletion |
| 509 | case_540 | COMPLETE → NOT_APPLICABLE | 0 → 0 | Request authorizes correction/access/marketing-only action or explicitly rejects account deletion |
| 511 | case_542 | COMPLETE → NOT_APPLICABLE | 0 → 0 | Request authorizes correction/access/marketing-only action or explicitly rejects account deletion |
| 515 | case_546 | NOT_APPLICABLE → INCOMPLETE | 0 → 4 | Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it |

## Remaining evidence limits

PASS in the 518-row file means the listed actions and final checks satisfy the recorded visible obligations. It is not certification that every unlinked resource was discovered or that the hidden grader agrees. Retrospective captures, workflow-only absence claims, and unresolved ownership are marked per case.

| Case | Limit |
|---|---|
| case_55 | backup_present_but_screenshot_does_not_explicitly_prove_restore_block |
| case_63 | complete_without_any_policy_obligation; complete_without_evidence_backed_verification; catalog_marketing_owner_conflicts_with_visible_screenshot_owner; do_not_delete_another_subjects_record |
| case_64 | retrospective_capture_requires_review:evidence_06 |
| case_69 | retrospective_capture_requires_review:evidence_06 |
| case_70 | retrospective_capture_requires_review:evidence_06 |
| case_77 | retrospective_capture_requires_review:evidence_07 |
| case_81 | retrospective_capture_requires_review:evidence_07 |
| case_82 | retrospective_capture_requires_review:evidence_07 |
| case_103 | workflow_claim_not_independently_read_back |
| case_126 | retrospective_capture_requires_review:evidence_12 |
| case_152 | workflow_claim_not_independently_read_back |
| case_213 | retrospective_capture_requires_review:evidence_21 |
| case_215 | retrospective_capture_requires_review:evidence_21 |
| case_218 | retrospective_capture_requires_review:evidence_21 |
| case_219 | retrospective_capture_requires_review:evidence_21 |
| case_221 | retrospective_capture_requires_review:evidence_21 |
| case_274 | workflow_claim_not_independently_read_back |
| case_313 | retrospective_capture_requires_review:evidence_30 |
| case_314 | retrospective_capture_requires_review:evidence_30 |
| case_319 | retrospective_capture_requires_review:evidence_30 |
| case_322 | retrospective_capture_requires_review:evidence_30 |
| case_324 | retrospective_capture_requires_review:evidence_31 |
| case_326 | retrospective_capture_requires_review:evidence_31 |
| case_331 | retrospective_capture_requires_review:evidence_31 |
| case_343 | workflow_claim_not_independently_read_back |
| case_403 | workflow_claim_not_independently_read_back |
| case_430 | citation_lacks_directly_owned_extracted_record:evidence_68:account_6006 |
| case_463 | retrospective_capture_requires_review:evidence_44 |
| case_464 | retrospective_capture_requires_review:evidence_44 |
| case_467 | retrospective_capture_requires_review:evidence_44 |
| case_470 | retrospective_capture_requires_review:evidence_44 |
| case_512 | workflow_claim_not_independently_read_back |
