# Phase 17 change register

## Change 1: Complete typed evidence inventory
- **Iteration:** 17a; **Fix ID:** inventory
- **Files:** `code/orchestrator/{dataset_catalog,database_inspector,pdf_inspector,image_inspector,log_inspector}.py`
- **Grounded in:** [dataset_catalog.md](dataset_catalog.md) and [datapoint_extraction_map.md](datapoint_extraction_map.md).
- **Problem:** Prior CSV inventory listed non-CSV evidence without opening it.
- **Before:** Evidence formats were inferred from file names only.
- **After:** Each of 94 files is opened through a type-specific inspector; SQL schema/rows, PDF pages/tables, image metadata/OCR, log formats, and JSON keys/counts are recorded.
- **Tests:** `test_dataset_catalog.py`, `test_database_inspector.py`, `test_pdf_inspector.py`, `test_log_inspector.py`.
- **Expected impact:** Source-complete provenance; no invented affiliations.
- **Verification:** 94/94 opened, zero parser errors after installing missing `pdfplumber` in the local venv. Rule-only status 32/32.
- **Cost impact:** $0 API cost for inventory without Vision.

## Change 2: Exact ownership audit of five cap cases
- **Iteration:** 17a; **Fix ID:** audit-case_01-02-03-04-31
- **File:** `code/orchestrator/dataset_catalog.py` (`audit_gap_cases`).
- **Grounded in:** [cases_01_02_03_04_31_audit.md](cases_01_02_03_04_31_audit.md).
- **Problem:** The proposed 27/32 cap had not been checked against every SQL table, PDF table, JSON/log line, and image.
- **Before:** Five unsupported targets were documented from selected files.
- **After:** Exact identifier/resource scans cover all machine-readable files; all 11 PNGs were visually inspected. Case 03's same-file co-mention is explicitly rejected as a same-row link.
- **Tests:** `test_five_gap_audit_has_no_unverified_join`, `test_exact_reference_never_uses_numeric_suffix`.
- **Expected impact:** No step-array gain unless a new direct link is discovered.
- **Verification:** Zero new direct links for the five cases; 27/32 upper bound remains conditional on the supplied evidence and strict ownership rule.
- **Cost impact:** $0 API cost.

## Change 3: OCR-first image extraction and mini-Vision
- **Iteration:** 17c; **Fix ID:** cost-optimization
- **Files:** `code/agent/evidence/handlers/image_handler.py`, `code/agent/llm/{client.py,prompts/image_pii.py}`, `code/orchestrator/pipeline.py`.
- **Grounded in:** [datapoint_extraction_map.md](datapoint_extraction_map.md) §PNG and Phase 16's 353 `gpt-4o` image responses costing $1.265080.
- **Problem:** Every image triggered expensive Vision even when OCR might suffice.
- **Before:** Default image model `gpt-4o`; images extracted only when LLM enabled.
- **After:** EXIF audit cutoff, local OCR with same-line exact joins, then cached `gpt-4o-mini` Vision fallback; OCR runs with or without API access. Shorter output schema removes reasoning prose.
- **Tests:** `test_image_ocr_pipeline.py`, legacy Vision handler tests.
- **Expected impact:** Lower cost and possible visible-row ownership, no unsupported subject inference.
- **Verification:** 9 legacy handler tests and 20 new tests pass; rule-only status 32/32. Live mini-Vision measurement recorded in phase17_validation.md.
- **Cost impact:** Measured in usage_report.md; Tesseract binary absent, so no OCR savings on this host.

## Change 4: Schema/table and format-aware handler integration
- **Iteration:** 17b; **Fix ID:** ownership-wire-structured
- **Files:** `code/agent/evidence/handlers/{sql,pdf,log}_handler.py`.
- **Grounded in:** [dataset_catalog.md](dataset_catalog.md) table/column, PDF table and structured-log inventories.
- **Problem:** SQL omitted known ownership columns, PDF tables were not row-scanned, and JSONL logs lacked field parsing.
- **Before:** SQL used a narrower column set; PDFs searched page text; logs used generic regex/pipe paths.
- **After:** SQL uses inspector's explicit ownership-column set with exact equality; PDF table rows and JSON-lines structured fields are parsed. No suffix joins.
- **Tests:** New inspector tests and existing evidence tests; sample status 32/32.
- **Expected impact:** More grounded resource facts in full dataset, without altering the five unsupported links.
- **Verification:** 32/32 rule-only statuses; 1/32 exact rule-only arrays, no improvement claim.
- **Cost impact:** $0 API cost; additional local parsing only.

## Change 5: In-repository organization with compatibility paths
- **Iteration:** 17e; **Fix ID:** artifact-organization
- **Files:** `artifacts/csv/`, `code/evaluation/validations/`, `code/orchestrator/gold_validation.py` (historical baseline path).
- **Grounded in:** User request to group validation reports and CSVs, and `gold_validation.py`'s hard-coded historical baseline.
- **Problem:** 17 intermediate sample CSVs cluttered the repository root; phase reports were mixed with other evaluation documents.
- **Before:** Historical CSVs at root; all evaluation documents in one flat folder.
- **After:** Historical CSVs grouped under `artifacts/csv/`; validation reports collected under `code/evaluation/validations/` while required canonical report paths remain available.
- **Tests:** Full suite, gold validator and archive integrity after organization.
- **Expected impact:** No decision change; easier submission handoff.
- **Verification:** Recorded in phase17_validation.md.
- **Cost impact:** $0.

## Change 6: Bound mini-Vision image detail and isolate its cache
- **Iteration:** 17d; **Fix ID:** cost-optimization-detail
- **File:** `code/agent/llm/client.py` (`_call`, `call_vision`).
- **Grounded in:** First Phase 17 live run: 352 `gpt-4o-mini` high-detail image calls consumed 13,020,359 input tokens, 16,432 output tokens and an estimated **$1.962913**, despite preserving only 2/32 exact arrays. [Official image-token rules](https://developers.openai.com/api/docs/guides/images-vision#calculating-costs) specify a 2,833-token base plus 5,667 per high-detail tile for mini, versus one base charge for `low`.
- **Problem:** Merely replacing `gpt-4o` with `gpt-4o-mini` did not reduce cost; the client's fixed `detail=high` made the smaller model more expensive for these screenshots.
- **Before:** Image URL always carried `detail: high`; cache key omitted detail.
- **After:** Mini defaults to `detail: low`, with explicit override available; image detail joins the cache key so old high-detail answers cannot masquerade as low-detail results.
- **Tests added:** `test_low_detail_and_high_detail_have_separate_cache_entries`, `test_client_vision_default_is_mini`.
- **Expected impact:** At most one mini base-token charge per image call; lower text-reading fidelity is possible and must be measured, not assumed.
- **Verification:** 19 focused client/image tests pass; 32-case low-detail run in progress.
- **Cost impact:** Estimated reduction from $1.96 to <$0.50 per fresh 32-case run, subject to actual usage.

## Change 7: Accuracy-first screenshot transcription with local OCR
- **Iteration:** 17f; **Fix ID:** image-grounding.
- **Files:** `code/agent/evidence/handlers/image_handler.py`, `code/orchestrator/image_transcriber.py`, `code/orchestrator/image_audit.py`, `code/orchestrator/image_inspector.py`, `code/agent/llm/client.py`.
- **Grounded in:** `image_text_inventory.md` contains verbatim OCR for all 11 screenshots and the model/OCR disagreements.
- **Problem:** Low-detail mini-Vision missed small table text; mini also hallucinated/swapped some IDs.
- **Change:** Use repository-local RapidOCR, spatial row joins, and one cached high-detail `gpt-4o-mini` transcript per image. Accept model rows only when identifiers/resource/state are visible and schema-valid. The `gpt-4o-mini` image default is high detail because the user's accuracy preference supersedes the earlier cost choice.
- **Tests added:** Real-image isolation and transcript validation in `test_image_ocr_pipeline.py` and `test_image_transcriber.py`.
- **Expected impact:** Preserve visible ownership without assigning search/filter text or a neighboring row to the subject.
- **Verification:** 11/11 images transcribed and cross-checked; rejected hallucinated account and swapped analytics IDs. See `image_text_inventory.md`.

## Change 8: Nested SQL replicas and hashed identifiers
- **Iteration:** 17g; **Fix ID:** database-ghosts.
- **Files:** `code/agent/evidence/handlers/{common,sql,json,log,pdf}_handler.py`, `code/agent/state/reconstructor.py`.
- **Grounded in:** `customer_data_read_replica_20260921.sql` contains JSON-encoded copies in multiple tables; `service_events_ap_south_20260915.log` has an exact historical-email SHA-256 contact lookup.
- **Problem:** Flat-column-only SQL matching missed nested owner/PII, and a clean primary copy could mask a PII-bearing replica at the same timestamp.
- **Change:** Parse nested `record_json`, derive hashes of known historical/current emails, retain source table, choose the PII-bearing SQL copy on a same-file/timestamp tie, and preserve log source order for same-second readbacks.
- **Tests added:** `test_sql_replica_ghosts.py` and hash/readback tests in `test_document_and_restore_semantics.py`.
- **Expected impact:** Detect actual replica ghosts without broad text substring matches.
- **Verification:** Synthetic two-copy ghost and historical hash tests pass; case 03's completed 404 remains ABSENT.

## Change 9: Document/resource and restore evidence semantics
- **Iteration:** 17h; **Fix ID:** document-state-provenance.
- **Files:** `code/agent/evidence/handlers/{pdf,log}_handler.py`, `code/agent/flows/restore_risk.py`.
- **Grounded in:** The retention register is context, not a user-owned row; a backup access check explicitly says it can still be restored.
- **Problem:** Page-number placeholder resources and identity-only lookup lines became ghost facts; access checks were missed.
- **Change:** Require a visible full resource ID and same-row/selected-document subject in PDFs, drop context-only registers/lookup lines, and treat affirmative exact-owner restore checks as risk signals.
- **Tests added:** `test_document_and_restore_semantics.py`.
- **Verification:** Case 09 restore risk recovered; case 21 context-only PDF no longer creates a phantom resource.

## Change 10: Physical replicas and one-off synchronization
- **Iteration:** 17i; **Fix ID:** duplicate-logical-resource.
- **Files:** `code/agent/state/reconstructor.py`, `code/agent/flows/detector.py`.
- **Grounded in:** `system_activity.csv` replica checkpoint rows for `account_005`, `account_994`, `account_5334`; gold diff showed duplicate logical-account and active-flow steps.
- **Problem:** Physical replica targets were treated as separate user resources; a completed unscheduled SYNC was treated as an active recurring mechanism.
- **Change:** Canonicalize replica topology to the resource's logical system while retaining source evidence, and require recurrence or a future next run for an active flow.
- **Tests added:** Replica and one-off/recurring flow cases in `test_state_reconstructor.py` and `test_flow_detector.py`.
- **Verification:** Exact arrays rose from 3/32 to 5/32, statuses remained 32/32.

## Change 11: Source-typed support attachments and contact indexes
- **Iteration:** 17j; **Fix ID:** conditional-category-mapping.
- **Files:** `code/agent/evidence/handlers/{pdf,log}_handler.py`, `code/agent/policy/engine.py`, `code/agent/state/reconstructor.py`.
- **Grounded in:** `delivery_correction_attachment.pdf` is an attachment; the handover pipe row explicitly labels `SUPPORT_ATTACHMENT`; the log says `source=legacy_contact_index` and `marker_found=false`; the analytics log says `event=contact_lookup_completed`.
- **Problem:** All support-platform rows inherited message REDACT and all analytics-platform rows inherited profile ANONYMIZE, even when the row was an attachment or secondary-identifier lookup. A missing deletion marker was incorrectly interpreted as an absent row.
- **Change:** Preserve document/category/trace-source fields and apply the corresponding supplied DELETE rule. Interpret `marker_found=false` as a surviving row; normalize support replica to logical support platform.
- **Tests added:** Category, document, and trace tests in `test_policy_engine.py` and `test_document_and_restore_semantics.py`.
- **Verification:** Exact arrays rose from 5/32 to 7/32; cases 12 and 13 now match exactly, case 10's support ghost is correctly reported.

## Change 12: Exact foreign-key joins, no metadata-as-state
- **Iteration:** 17k; **Fix ID:** explicit-reference-and-state-ops.
- **Files:** `code/agent/evidence/handlers/sql_handler.py`, `code/orchestrator/activity_expander.py`, `code/agent/state/reconstructor.py`.
- **Grounded in:** `customer_search_primary_20260910.sql:9` carries the requester's email and exact `source_resource_id=account_006`. `LINK_RESOURCE_IDENTITY`/`CHECK_RESTORE_ACCESS` events do not say a resource is currently present.
- **Problem:** The explicit SQL source reference was ignored, while metadata/access events invented PRESENT facts for object/tombstone/backup resources.
- **Change:** Parse `indexed_at`, derive an activity owner only from an exact `source_resource_id`, and restrict timeline state transitions to state-changing operations.
- **Tests added:** Exact-reference and negative lookalike tests in `test_activity_expander.py`; metadata-op test in `test_state_reconstructor.py`.
- **Verification:** Foreign-key change raised exact arrays from 7/32 to 8/32. Metadata-op final sample result is in `phase17_validation.md`.

## Change 13: One backup, one restore obligation
- **Iteration:** 17l; **Fix ID:** backup-overlap.
- **File:** `code/agent/policy/engine.py`.
- **Grounded in:** Case 14's gold diff: duplicate finding/remediation/verification for `backup_3870`; case 09 had an extra `VERIFY_RECORD_PRESENT` for its risky backup.
- **Problem:** A snapshot ResourceFact and an access-check RestoreRiskFact independently emitted steps for the same backup.
- **Change:** Select the latest risk per `(system_id, resource_id)` and let that risk supersede a backup record verdict; never suppress an unrelated resource.
- **Tests added:** `test_backup_snapshot_and_restore_risk_emit_one_obligation`.
- **Verification:** Exact arrays rose from 8/32 to 9/32 (case 14 recovered), all statuses still 32/32.

## Change 14: Timestamp-prefixed JSON logs and provenance priority
- **Iteration:** 17m; **Fix ID:** structured-log-trace-and-citation.
- **Files:** `code/agent/evidence/handlers/log_handler.py`, `code/orchestrator/log_inspector.py`, `code/orchestrator/pipeline.py`.
- **Grounded in:** `structured_service_events_eu_west_20260918.log:24-28,82-86` encodes a start event with subject and an exact trace-ID completed readback with resource/state. Case 09's step diff showed an otherwise-correct restore-risk finding citing the backup snapshot rather than the access-check evidence.
- **Problem:** The JSON parser required `{` at column 1, missed all timestamp-prefixed objects and their trace ownership. Citation selection always preferred a record fact, even for a restore-risk verdict.
- **Change:** Parse the JSON suffix, carry an exact trace owner only to completed resource events, interpret 404/zero rows as ABSENT, and select evidence source by verdict kind before fallback.
- **Tests added:** `test_jsonl_trace_joins_exact_completed_resource_but_not_started_event`, `test_pipeline_provenance.py`.
- **Verification:** The five-step case 09 shape is recovered; final citation and sample metrics appear in `phase17_validation.md`.

## Change 15: Full document and residual-source inventories
- **Iteration:** 17n; **Fix ID:** audit-traceability.
- **Files:** `code/orchestrator/{document_audit,residual_provenance}.py`, `code/evaluation/{document_text_inventory,residual_step_provenance}.md`.
- **Grounded in:** User request to read all documents and to explain why exact arrays still fail.
- **Problem:** A catalog snippet did not show all PDF/table/TXT text, and the remaining 27 semantic gaps had not been classified across the complete evidence collection.
- **Change:** Publish each of the four PDFs page by page with every extracted table row, plus the plain-text handover. Search every evidence file, including screenshot OCR, for each missing gold resource ID and exact same-line owner candidate. This is evaluation-only; gold never enters production decisions.
- **Tests added:** `test_document_audit.py`, `test_residual_provenance.py`.
- **Verification:** All four PDFs have text layers; 27 missing semantic steps classify into 16 with no literal target in any evidence file and 11 with only ownerless target occurrences; zero same-line subject hits.

## Change 16: Brief-compliant archive evaluation paths
- **Iteration:** 17o; **Fix ID:** submission-layout.
- **Files:** `code/orchestrator/repackage.py`, `code/tests/test_triage_mismatches.py`.
- **Grounded in:** `problem_statement.md:133-158` requires `evaluation/evaluation_report.md` and `evaluation/usage_report.md` inside `code.zip`.
- **Problem:** Earlier ZIPs stored those files only under `code/evaluation/`.
- **Change:** Keep the runnable `code/` layout and add root-level `evaluation/` aliases in ZIP/TAR. Secrets, caches and virtualenv remain excluded.
- **Tests added:** `test_archive_exposes_required_evaluation_path`.
- **Verification:** Focused package test passes; final archive integrity check appears in `phase17_validation.md`.

## Change 17: Manifest-time cutoff for timestamp-less evidence
- **Iteration:** 17p; **Fix ID:** post-audit-image-ghost.
- **Files:** `code/orchestrator/evidence_time.py`, `code/orchestrator/pipeline.py`.
- **Grounded in:** `dataset/evidence_files.csv` has a `captured_at` for every screenshot, while the PNGs have no EXIF timestamp and `image_handler` produced records with `evidence_timestamp=None`.
- **Problem:** A post-audit screenshot or PDF could be used as if it proved a resource present at the earlier audit time.
- **Change:** For records without an intrinsic row/page timestamp, apply the manifest capture time. Move only such post-audit records to `records_post_audit`; preserve a genuine earlier intrinsic timestamp even if the file was copied later.
- **Tests added:** Three pre/post/intrinsic-time tests in `test_evidence_time.py`.
- **Verification:** Focused tests pass; the next sample/full run measures the release impact.

## Change 18: Direct image registry dispatch
- **Iteration:** 17q; **Fix ID:** remove-image-placeholder.
- **Files:** `code/agent/evidence/registry.py`, `code/orchestrator/pipeline.py`.
- **Grounded in:** Registry image dispatch previously returned an empty `ExtractedEvidence` and depended on a second pipeline-only replacement, despite real OCR/Vision extraction existing in `image_handler.py`.
- **Problem:** A direct registry caller saw placeholder-empty image evidence, and the two-stage pipeline made it easy to skip image extraction accidentally.
- **Change:** Dispatch PNG/JPEG files directly to the real OCR/Vision handler with the shared `gpt-4o-mini` client. Keep the manifest-relative file path and apply the same capture-time guard afterward.
- **Tests added:** `test_registry_image_dispatch.py`.
- **Verification:** Seven focused registry/image/time tests pass; current sample result is measured after this wiring change.

## Change 19: Strict full-image Vision, bounded repair and corroboration
- **Iteration:** 17r; **Fix ID:** vision-schema-and-ghost-guard.
- **Files:** `code/agent/llm/{client,semantic_resolver}.py`, `code/orchestrator/image_transcriber.py`, `code/agent/evidence/handlers/image_handler.py`.
- **Grounded in:** The previous client requested `json_object`, which guarantees syntax but not the required row schema; malformed transcript JSON returned immediately. The global pass read only a top crop despite full screenshots, and a model's own `visible_text` was not independent ownership proof.
- **Change:** Request OpenAI strict `json_schema` for both global and focused Vision paths; retry malformed/schema output with a distinct prompt; read the complete image. Require both literal IDs in local OCR before admitting a Vision row, or a second independent Vision agreement when OCR is empty. The callback-only compatibility path uses the same exact-row validator.
- **Tests:** Strict request format/cache separation, malformed retry, focused Vision, OCR-empty double reading, and rejection of a model-only uncorroborated owner.
- **Verification:** The first strict/full-image sample stayed at 32/32 statuses and 10/32 exact arrays. The final run after the JSON-owner change is reported in `phase17_validation.md`.

## Change 20: Model-planned, read-only audit tool loop
- **Iteration:** 17s; **Fix ID:** bounded-agent-supervision.
- **Files:** `code/orchestrator/audit_supervisor.py`, `code/orchestrator/pipeline.py`.
- **Grounded in:** The pipeline previously made one linear pass, leaving evidence conflicts or malformed Vision rows without an explicit diagnostic reinspection route.
- **Change:** Detect source anomalies, ask `gpt-4o-mini` to select from an allowlist of JSON/SQL/log/PDF/image inspectors using strict schema, execute at most two read-only inspections, and log source excerpts. Reject unlisted paths/tools and fall back to a real local inspection on invalid model plans. Tool results never directly create ResourceFacts.
- **Tests:** `test_audit_supervisor.py` covers conflict planning, strict schema, wrong-tool rejection, malformed-plan fallback, cross-table SQL, missing/outside paths, and no-anomaly/no-call behavior.
- **Verification:** 24 focused supervisor/schema tests passed. The first strict/full-image sample preserved 32/32 status and 10/32 exact arrays.

## Change 21: Exact JSON ownership fields, not query selectors
- **Iteration:** 17t; **Fix ID:** ghost-selector.
- **File:** `code/agent/evidence/handlers/json_handler.py`.
- **Grounded in:** JSON inventory includes `subject_selector` and `lookup_value` containing exact `user_*` values; the old handler treated any matching string field as ownership.
- **Change:** Match user IDs only in explicit owner/reference fields observed in the source schemas. An ID in a filter, lookup or note does not affiliate the resource. Email and hash checks remain exact and field-scoped.
- **Tests:** `test_json_selector_and_lookup_are_not_record_ownership` checks both the rejected selector and accepted `subject_reference`.
- **Verification:** Focused handler tests pass; sample/full-run effect is measured in `phase17_validation.md`.

## Change 22: SQL mapping inventory and honest structural validator
- **Iteration:** 17u; **Fix ID:** coverage-and-validator.
- **Files:** `code/orchestrator/schema_mapping_audit.py`, `code/orchestrator/validator.py`, `code/evaluation/schema_mapping_audit.md`.
- **Grounded in:** The 518-row run printed `0/0 checks passed` because the validator only incremented its counter on failures/warnings; it was structurally valid but the summary was misleading.
- **Change:** Count successful row/step checks, guard malformed step types, and produce a per-table SQL mapping ledger for every SQL file and exact-identity-linked record.
- **Tests:** Two schema-mapping coverage tests and existing validator/packaging tests.
- **Verification:** Independent check on the 518-row CSV: 17,748/17,748 checks, zero errors/warnings. SQL inventory: 24 files, 127 table instances, 681 exact-linked records, zero extracted generic-system rows.

## Change 23: Runnable archive and current usage audit
- **Iteration:** 17v; **Fix ID:** submission-integrity.
- **Files:** `code/orchestrator/{repackage,audit_llm_usage}.py`, `README.md`, `tradeoff.md`, `code/evaluation/datapoint_extraction_map.md`.
- **Grounded in:** Archive excluded `requirements.txt` although README requires it; an old usage-audit script still claimed the production image path was a zero-call placeholder.
- **Change:** Include the dependency manifest in `code.zip` and update documentation/usage-path description to reflect local RapidOCR plus live strict Vision. Keep `.env`, caches and virtualenv excluded.
- **Tests:** Packaging integrity test and final archive audit are recorded in `phase17_validation.md`.

## Change 24: Per-file error isolation and nonzero fatal exit
- **Iteration:** 17w; **Fix ID:** no-placeholder-extraction-fallback.
- **Files:** `code/orchestrator/{pipeline,run}.py`.
- **Grounded in:** The previous list-comprehension wrapped all 94 evidence extractions in one try/except: one corrupt source could erase every valid fact for that case. The runner did not fail the process when case-level pipeline errors existed.
- **Change:** Isolate every manifest file, retain all successful extractions, record an explicit empty error artifact only for the broken file, and mark missing/unsupported sources as case errors. The CLI writes diagnostic output but exits nonzero when any case has errors; no partial audit is called ready.
- **Tests:** `test_one_bad_evidence_file_does_not_erase_other_extractions` and full-run zero-error inspection.
- **Verification:** Focused test passed; final 518-case result in `phase17_validation.md`.

## Change 25: Actual scanned-PDF Vision route
- **Iteration:** 17x; **Fix ID:** scanned-pdf-no-placeholder.
- **Files:** `code/agent/evidence/{handlers/pdf_handler,registry}.py`, `requirements.txt`.
- **Grounded in:** All four supplied PDFs have text layers, but the scanned-page branch previously returned only a “needs Vision” note and no attempted rendering/inspection.
- **Change:** Render a low-text page to a content-keyed PNG with `pypdfium2`, pass it through the same OCR/strict mini-Vision image handler, and preserve the original PDF page number on each hit. Successful routing replaces the old deferred note; rendering failures remain explicit. Include the renderer dependency and its source files in the PDF cache fingerprint.
- **Tests:** Forced scanned-page test on an existing repository PDF, verifying a real PNG is rendered and sent to the image route without creating or modifying a source PDF.
- **Verification:** Focused PDF suite and final full suite are recorded in `phase17_validation.md`; all supplied PDFs still follow the text/table path.

## Change 26: Preserve the full-run token ledger
- **Iteration:** 17y; **Fix ID:** usage-report-isolation.
- **Files:** `code/orchestrator/{pipeline,run}.py`.
- **Grounded in:** `run_case` registered an atexit write of `usage_report.md` in every process. A subsequent sample/debug/pytest process could overwrite the required 518-case usage ledger with its own partial calls.
- **Change:** Remove the side effect from `run_case`; the CLI writes usage explicitly. Only the canonical full-dataset input/output pair writes `code/evaluation/usage_report.md`; exploratory runs write a separate cache-local report.
- **Tests:** `test_sample_run_cannot_overwrite_submission_usage_report`.
- **Verification:** The completed 518-case ledger remains intact after the final sample and regression runs.

## Change 27: Keep sample answers and reported claims outside production
- **Iteration:** 17z; **Fix ID:** answer-leak-boundary.
- **Files:** `code/orchestrator/{leakage_audit,pipeline,step_diff}.py`, `code/tests/test_no_gold_leak.py`, `code/evaluation/leakage_audit.md`.
- **Grounded in:** The request to verify an unbiased boundary; `sample_output.csv` exists alongside runnable inputs, and `deletion_requests.csv` carries `reported_status` as an unproven claim.
- **Problem:** A full `case_row` was passed to every phase and the sample comparator shared the orchestrator package. A correct result alone could not prove no answer file was read.
- **Change:** Project each request to five authorized fields at `run_case` entry. Walk the production import closure for answer-reading modules, case-specific literals and answer-file paths; guard answer-file reads at runtime. Add a per-case semantic table to the evaluation-only step diff.
- **Tests:** Five answer-boundary tests, including a request whose reported fields raise on access.
- **Verification:** 65 reachable production modules, zero static findings; guarded production case completed without attempting an answer-file read. The sample remains a repeatedly inspected development set, not a hidden unbiased score.

## Change 28: Remove stale negative lookup ghosts
- **Iteration:** 17aa; **Fix ID:** pre-request-query-state.
- **Files:** `code/agent/evidence/handlers/log_handler.py`, `code/orchestrator/evidence_admission.py`, `code/orchestrator/pipeline.py`, `code/tests/test_evidence_admission.py`.
- **Grounded in:** `dataset/evidence/logs/resource_lookup_trace_20260310_061801.log:2-3` has a `lookup_started` event and 404 miss months before the September deletion request. It was generating an extra September account verification.
- **Problem:** A query start became PRESENT and its old 404 completion became an audit-time ABSENT fact for a resource that was not otherwise affiliated.
- **Change:** Start events retain trace context without creating records. Exclude only pre-request negative log lookups from reconstruction, with an explicit evidence note; preserve fresh completed lookups and positive source rows.
- **Tests:** Five synthetic event/admission tests and the prior structured-log tests.
- **Verification:** Status stayed 32/32 and exact ordered sample arrays rose from 10/32 to 11/32. The extra semantic step disappeared.

## Change 29: Preserve later JSON owners for exact resource affiliation
- **Iteration:** 17ab; **Fix ID:** cross-time-owner-join.
- **Files:** `code/agent/evidence/{handlers/json_handler,registry}.py`, `code/orchestrator/{evidence_admission,pipeline}.py`, `code/tests/test_evidence_admission.py`.
- **Grounded in:** `dataset/evidence/records/service_resource_export_20260915_114455.json:13-17` has an ownerless 404 for `account_3866`; `dataset/evidence/records/customer_data_snapshot_bundle_20260917.json:524-528` later gives that *same complete ID* an explicit `customer_reference` and email. The earlier JSON extractor dropped all post-audit owned rows.
- **Problem:** The later row could not establish ownership of the earlier readback because it never entered `records_post_audit`.
- **Change:** Preserve post-audit JSON rows separately. Allow a later JSON/SQL row with an explicit matching owner field to affiliate an earlier ownerless ABSENT readback only when system and full resource ID agree. The earlier readback remains the sole source of audit-time state; future state is not promoted.
- **Tests:** Five synthetic exact-join, selector-rejection, system/ID collision, model-only rejection and JSON-registry separation tests.
- **Verification:** A targeted real-source case gained the missing account ABSENT verification with `evidence_92`; whole-sample impact and remaining citation differences are measured in `phase17_validation.md`.

## Change 30: Check all CSV schemas and fix a path-relative test audit
- **Iteration:** 17ac; **Fix ID:** dataset-schema-coverage.
- **Files:** `code/orchestrator/{csv_schema_audit,audit_llm_usage}.py`, `code/tests/test_csv_schema_audit.py`, `code/evaluation/csv_schema_audit.md`.
- **Grounded in:** All nine supplied CSV schemas needed a common shape check. A full pytest run found `audit_llm_usage` skipped every source when pytest's temporary root itself lived under `code/.cache`.
- **Problem:** Absolute path-component exclusion produced a false zero-call static audit in nested workspaces.
- **Change:** Check exact headers, row shape, duplicate keys, timestamps and manifest paths. Apply exclusion only to generated directories *inside* the audited code tree.
- **Tests:** Three CSV schema tests and the existing LLM-audit fixture test.
- **Verification:** Nine CSVs pass with zero schema/path errors; focused LLM-audit tests pass.

## Change 31: Keep diagnostic no-evidence mode out of submission
- **Iteration:** 17ad; **Fix ID:** fail-closed-diagnostic-mode.
- **Files:** `code/orchestrator/pipeline.py`, `code/tests/test_pipeline.py`, `README.md`.
- **Grounded in:** The runner accepts `ORCHESTRATOR_SKIP_EVIDENCE=1`, which previously returned fallback rows while the structural CSV validator could still pass.
- **Problem:** A developer could mistake a validly shaped no-evidence CSV for an evidence-backed audit.
- **Change:** Mark every skipped-evidence case with an explicit error. The existing CLI fatal-error gate exits nonzero, while still writing the diagnostic CSV for investigation.
- **Tests:** `test_skip_evidence_mode_is_marked_fatal_for_submission`.
- **Verification:** Focused pipeline regression and final full suite appear in `phase17_validation.md`.

## Change 32: Verify every output citation against supplied sources
- **Iteration:** 17ae; **Fix ID:** citation-provenance.
- **Files:** `code/orchestrator/{citation_audit,pipeline}.py`, `code/tests/{test_citation_audit,test_pipeline}.py`, `code/evaluation/citation_audit.md`.
- **Grounded in:** An independent audit of the 518-row candidate found 18 finding citations such as `activity_3755::derived_0002_for_user_35`; no such IDs exist in `system_activity.csv`. Another 129 alerts were generated log-line handles, which are meaningful only if their cited lines and subjects can be checked.
- **Problem:** Structurally valid nonempty citations could still point to an internal derived ID or an unverifiable source line.
- **Change:** Canonicalize derived IDs to their original CSV activity IDs before step building; fail the case if the original is absent. The evaluation-only citation audit accepts synthetic log-line handles only when line N exists and contains an exact resolved user ID, email or hash. Other file citations require a visible full resource ID.
- **Tests:** Three citation-audit fixtures and `test_derived_activity_citation_resolves_to_original_source_row`.
- **Verification:** The pre-fix 907-citation audit reduced from 147 alerts to 18 after verifying 129 genuine log-line handles. The final rerun measures whether all 18 internal activity citations are removed.

## Change 33: Quantify ambiguity of missing ownership joins
- **Iteration:** 17af; **Fix ID:** residual-source-adjudication.
- **Files:** `code/orchestrator/residual_provenance.py`, `code/evaluation/residual_step_provenance.md`.
- **Grounded in:** The 26 remaining semantic sample gaps include 16 resource IDs absent from all 94 evidence files. Time-only affiliation had produced false facts in Phase 14.
- **Problem:** The existence of a matching activity ID might be mistaken for an identity-specific join even though `system_activity.csv` has no subject column.
- **Change:** In evaluation only, count how many supplied request windows overlap each missing target's pre-audit activity. The result is diagnostic and is never passed to production.
- **Verification:** Three targets have no pre-audit activity row; every other listed target's activity overlaps 5–12 requests. Fourteen distinct sample cases still lack a literal evidence-file target, implying the conditional 18/32 exact-array ceiling under strict ownership.

## Change 34: Screen every structured log trace for ghost ownership

- **Iteration:** 17ag; **Fix ID:** trace-integrity-audit.
- **Files:** `code/orchestrator/log_trace_integrity.py`, `code/tests/test_log_trace_integrity.py`, `code/evaluation/log_trace_integrity.md`, `README.md`.
- **Grounded in:** The log handler joins a request's subject to a resource by exact trace ID. Shared trace IDs, unstructured mentions or a later-only owner signal would undermine that join even when a resource ID is literal.
- **Problem:** Unit fixtures proved individual formats, but the 26 supplied log files had no independent source-wide trace collision and temporal-order screen.
- **Change:** Read every manifest-listed log, resolve current and historical exact identifiers to canonical users, and report conflicting trace owners, unstructured-only identity signals, future-only owner signals and ownerless resource lines. This tool is evaluation-only and does not change production affiliation.
- **Tests:** Three synthetic disagreement, future-only and same-time trace tests pass.
- **Verification:** 26 logs, 421 trace groups and 686 resource lines inspected; zero integrity issues. Seventy-one resource lines have no owner signal and remain ineligible for ownership by trace alone.

## Change 35: Cross-check SQL extraction against an independent owner query

- **Iteration:** 17ah; **Fix ID:** sql-direct-row-coverage.
- **Files:** `code/orchestrator/schema_mapping_audit.py`, `code/tests/test_schema_mapping_audit.py`, `code/evaluation/schema_mapping_audit.md`.
- **Grounded in:** The prior 681-row count came from the production SQL extractor itself and could not reveal an owner-bearing row that extractor skipped.
- **Problem:** A passing table inventory did not independently verify direct exact-column row coverage across varying SQL schemas.
- **Change:** Query every table through the separate database inspector for exact user/email/hash values and require each resulting `(table, resource_id)` to appear in the production extractor's output. Serialized JSON owner rows remain covered by the existing nested parser inventory.
- **Tests:** The mapping audit test now asserts zero direct-owner omissions.
- **Verification:** 24 SQL files, 127 table instances, 159 direct-owner rows found independently, zero missed; production extractor yielded 681 linked rows including nested JSON ownership, with zero generic-system rows.

## Change 36: Cover owner-bearing JSON readback rows

- **Iteration:** 17ai; **Fix ID:** json-readback-schema.
- **Files:** code/agent/evidence/handlers/json_handler.py, code/orchestrator/json_owner_coverage.py, code/tests/test_json_readback_schema.py, code/tests/test_json_owner_coverage.py.
- **Grounded in:** An independent traversal found 71 exact owner/resource pairs omitted from 28 JSON sources; subject_reference may contain an email, and several rows use recorded_at or result instead of older schema fields.
- **Change:** Match exact current/historical email or hash in owner fields, parse recorded_at, and map explicit negative/redacted/anonymized outcomes. Preserve post-audit rows outside audit-time state; a readback query subject is affiliation, not stored PII.
- **Verification:** 544/544 independently observed direct JSON owner/resource pairs now extracted; zero conflicting owners. Focused synthetic tests pass.

## Change 37: Parse all supplied structured log encodings

- **Iteration:** 17aj; **Fix ID:** log-schema-coverage.
- **Files:** code/agent/evidence/handlers/log_handler.py, code/orchestrator/log_schema_coverage.py, code/tests/test_log_schema_formats.py, code/tests/test_log_schema_coverage.py.
- **Grounded in:** The original handler missed quoted resource_id fields and mistook operations-stream pipes for compact readback tables. It also missed nested cloud runtime messages, syslog component/trace pairs and explicit system fields in record-lookup exports.
- **Change:** Parse key/value, JSONL, pipe, bracket, syslog and once-escaped cloud messages as structured events. Link only exact prior same-trace owner fields; skip query starts as presence; separate post-audit observations. Retain trace source category and recognized historical email hashes.
- **Verification:** The independent source parser finds 673 eligible direct owner/resource pairs across all 26 logs; production extracts all 673. Eleven format tests and two source-audit tests pass. After fixing a compact-security-row and trace-source regression, the 32-case sample returned to 32/32 statuses and 11/32 exact arrays.

## Change 38: Rank citations by contemporaneous source capture

- **Iteration:** 17ak; **Fix ID:** contemporaneous-citation.
- **Files:** code/orchestrator/pipeline.py, code/agent/llm/semantic_resolver.py, code/tests/test_citation_provenance_rank.py.
- **Grounded in:** The sample backtrace found 20 shared steps citing evidence_02, a bundle captured September 17, while a directly owned service export evidence_92 was captured before the September 15 audit cutoff. Both sources described the same state.
- **Change:** Carry manifest capture time with same-state citation candidates. Prefer a source captured by audit time when available, and constrain the model's candidate set to that group. If none exists, a retrospective source with a pre-audit row remains available; state reconstruction is unchanged.
- **Verification:** 20/20 shared-step citation differences disappeared and exact sample arrays rose from 11/32 to 12/32; status remained 32/32. A strict whole-file discard probe dropped exact arrays to 10/32, so it was rejected. Four provenance tests pass.

## Change 39: Backtrack every sample step and reject time-only ownership

- **Iteration:** 17al; **Fix ID:** source-backtrace.
- **Files:** code/orchestrator/sample_gold_backtrace.py, code/orchestrator/temporal_owner_probe.py, code/tests/test_sample_gold_backtrace.py, code/evaluation/sample_gold_backtrace.md, code/evaluation/temporal_owner_probe.md.
- **Grounded in:** The user asked to search all supplied documents and explain why the sample answer differs. The 26 missing semantic steps needed citation-by-citation source checks, including the original screenshot pixels and source table rows.
- **Change:** Generate a case-level diagnostic using sample answers only in an evaluation module. Check exact resource and owner in each cited JSON record, SQL/log row, PDF text/table and OCR image; enumerate other appearances and activity rows. Separately test reported-time inference without reading gold.
- **Verification:** Sixteen missing full IDs have no occurrence in 94 evidence files; ten are present but ownerless. All 11 original screenshots were visually reviewed. On the full 518-case input, the nearest account action matched a directly proven owner in only 71/212 evaluable requests, so time-only attribution remains prohibited. The current sample has 32/32 statuses, 12/32 exact arrays, 26 missing semantic steps and zero citation differences.

## Change 40: Preserve exact historical email hashes in log evidence

- **Iteration:** 17am; **Fix ID:** log-hash-regression.
- **Files:** code/agent/evidence/handlers/log_handler.py.
- **Grounded in:** The full regression suite detected that the new structured parser linked a hash-bearing analytics row but omitted its known historical email hash PIIHit.
- **Change:** Retain exact known email hashes in structured query/correlation fields as log PII while excluding ordinary query emails from stored-record PII. Precompute known identifiers and hashes once per file.
- **Verification:** The prior historical-hash regression and 11 log-format tests pass. The full-suite result is recorded in phase17_validation.md.

## Change 41: Scan every participant input for missing gold target IDs

- **Iteration:** 17an; **Fix ID:** full-input-backtrace.
- **Files:** code/orchestrator/sample_gold_backtrace.py, code/tests/test_sample_gold_backtrace.py, code/evaluation/sample_gold_backtrace.md.
- **Grounded in:** The user asked for another search of all supplied documents before treating a sample target as unsupported. The earlier backtrace counted evidence files and activity rows but did not tabulate the remaining participant CSVs together.
- **Change:** The evaluation-only backtrace now checks full identifier boundaries across every other participant input CSV, excluding the gold answer and blank answer template. It also includes exact known email hashes as owner signals in the cited record. The production pipeline and ownership rule are unchanged.
- **Verification:** Of 16 missing gold target IDs absent from all 94 evidence files, 13 occur only in ownerless system activity and three occur nowhere else in the participant inputs: case_04/account_004, case_18/audit_record_6645 and case_20/audit_record_5569. Five focused backtrace tests pass. This proves a source-coverage limit for those exact IDs without asserting how the gold generator reasoned.

## Change 42: Include the plain-text handover in independent owner coverage

- **Iteration:** 17ao; **Fix ID:** handover-coverage.
- **Files:** code/orchestrator/log_schema_coverage.py, code/tests/test_log_schema_coverage.py, code/evaluation/log_schema_coverage.md, code/evaluation/datapoint_extraction_map.md, README.md.
- **Grounded in:** The 94-file manifest includes one `.txt` shift handover that the production registry dispatches to the log handler, but the independent log coverage counter previously omitted it.
- **Change:** Parse its six-field pipe rows separately in the source-only audit, then compare exact owner/resource pairs against production extraction. The production handler and case pipeline remain unchanged.
- **Verification:** 39/39 directly owned handover rows are extracted; combined structured text coverage is 712/712 pairs over 26 logs and one TXT file. Three source-audit fixture tests pass.

## Change 43: Independently verify serialized SQL ownership

- **Iteration:** 17ap; **Fix ID:** sql-nested-owner-coverage.
- **Files:** code/orchestrator/schema_mapping_audit.py, code/tests/test_schema_mapping_audit.py, code/evaluation/schema_mapping_audit.md, code/evaluation/datapoint_extraction_map.md.
- **Grounded in:** The prior independent SQL check covered 159 direct owner-column rows but did not independently test the many generic replica tables whose user reference appears inside `record_json`.
- **Change:** A separate in-memory SQLite traversal decodes every `*_json` payload and searches exact ownership fields, excluding free-text notes. It compares each source table/resource pair to the production extractor without using sample answers.
- **Verification:** 522 nested exact-owner rows plus 159 direct rows across 127 table instances, zero omissions and zero generic-system production rows. Three focused schema-audit tests pass, including a note-only false-owner fixture.

## Change 44: Extend the SQL source audit to historical aliases

- **Iteration:** 17aq; **Fix ID:** sql-historical-coverage.
- **Files:** code/orchestrator/schema_mapping_audit.py, code/evaluation/schema_mapping_audit.md, code/evaluation/datapoint_extraction_map.md, README.md.
- **Grounded in:** The first nested SQL check used only the current identity CSV. Real cases also resolve old emails and email hashes from user_audit_log.csv, so the source-wide coverage count understated historical-only rows.
- **Change:** Include both old and new audited email/hash values and exact SHA-256 hashes of known emails in the independent SQL inventory. The production SQL parser is unchanged.
- **Verification:** Coverage rises from 681 to 716 exact-owner rows (186 direct and 530 nested), a gain of 35 historical-alias rows. Independent and production row sets still agree with zero omissions and zero generic-system rows; focused schema tests remain green.

## Change 45: Cross-check hashed identifiers in structured text

- **Iteration:** 17ar; **Fix ID:** log-historical-hash-coverage.
- **Files:** code/orchestrator/log_schema_coverage.py, code/tests/test_log_schema_coverage.py, code/evaluation/log_schema_coverage.md, code/evaluation/datapoint_extraction_map.md, README.md.
- **Grounded in:** The text-source audit included historical emails but its expected-pair index omitted their SHA-256 hashes and explicit email_hash audit events. The production parser already recognizes those exact values.
- **Change:** Extend the independent index with current/historical hashes and allow explicit hash ownership fields. The production handler is unchanged.
- **Verification:** One additional direct log pair is found and extracted. Structured text coverage is 713/713 (674 log, 39 TXT), with zero missing pairs; four source-audit fixture tests pass.

## Change 46: Separate evidence capture time from row observation time

- **Iteration:** 17as; **Fix ID:** temporal-citation-audit.
- **Files:** code/orchestrator/citation_audit.py, code/tests/test_citation_audit.py, code/evaluation/citation_audit.md.
- **Grounded in:** A previous full candidate cited 207 files captured after the corresponding audit cutoff. A later export can contain an older timestamped row, so file capture and row observation need separate reporting.
- **Change:** Count citations whose manifest capture time follows audit_at, while retaining the existing independent literal-resource and citation-ID checks. The production decision and citation ranking are unchanged.
- **Verification:** The final 518-row candidate has 24 later-captured file citations, down from 207 in the previous candidate. A separate per-case `ExtractedEvidence` check found an at-or-before-audit observation for every one of the 24 cited resources. The citation audit reports zero unknown or resource-absent citations; four focused tests pass. The literal file-capture cutoff remains a documented provenance question.

## Change 47: Surface COMPLETE rows without verification

- **Iteration:** 17at; **Fix ID:** unverified-complete-diagnostic.
- **Files:** code/orchestrator/runtime_diagnostics_audit.py, code/tests/test_runtime_diagnostics_audit.py, code/evaluation/runtime_diagnostics_summary.md.
- **Grounded in:** The final 518-row output passed every CSV shape check, but some COMPLETE rows had no cited verification step. A green schema validator should not obscure that evidence-quality risk.
- **Change:** Count COMPLETE rows with an empty steps array in the gold-free full-run diagnostic report. The agent does not synthesize a guessed resource step.
- **Verification:** 518/518 complete case traces, 48,692 expected manifest dispatches, zero pipeline errors, and nine COMPLETE rows without verification. The focused synthetic runtime audit passes; the full regression suite retains only the exact-step release-gate failure.
