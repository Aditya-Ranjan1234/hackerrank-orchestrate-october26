# Phase 17 validation — source backtrace and final candidate

**Historical Phase 17 snapshot.** The current regenerated 518-row candidate, sample score, model usage and readiness are documented in `workflow_affiliation_validation.md`; the measurements below are retained to show the earlier baseline and source investigation.

## Scope and evaluation boundary

The production runner reads participant inputs under `dataset/` and writes `output.csv`. The 32 labeled sample rows are used only by evaluation tools; they have been inspected repeatedly during development, so their score is a development-set result, not an unbiased estimate of hidden performance. The production import audit inspected 65 modules and found zero paths to `sample_output.csv` or a prior output file.

The user asked for another search of every supplied document. All 94 manifest paths exist and were opened (24 SQL, 28 JSON, 26 LOG, 4 PDF, 11 PNG, 1 TXT; 2,948,268 source bytes). The follow-up specifically looked for full resource IDs and exact current/historical user IDs, emails and email hashes in structured records, table rows, text lines and the original screenshot pixels. No dataset file was moved or rewritten.

## Extraction coverage and schema mapping

| Source | Independent source inventory | Production extraction | Omitted direct owner links |
|---|---:|---:|---:|
| SQL, 24 files / 127 tables | 186 exact owner-column rows + 530 nested JSON payload rows | 716 matched rows, concrete systems | 0 |
| JSON, 28 files | 544 direct owner/resource pairs | 544 direct pairs plus inherited record handling | 0 |
| LOG, 26 files | 674 exact structured owner/resource pairs | All 674; exact prior trace joins separately checked | 0 |
| TXT handover, 1 file | 39 owned six-column rows | 39 | 0 |
| PDF, 4 files | Four text layers and extracted tables | Four parsed, no scanned source | No file skipped |
| PNG, 11 files | All original pixels manually viewed; RapidOCR and high-detail `gpt-4o-mini` transcripts compared | Eleven parsed with strict schema and visible-ID corroboration | No file skipped |

The SQL inventory includes historical emails and hashes from `user_audit_log.csv`: adding them found 35 owner-bearing rows beyond the current-identity inventory. Generic replica tables use each row's `origin_system` and nested `record_json`, rather than a generic SQL system. The structured text inventory covers quoted fields, JSONL, multiple pipe formats, syslog, cloud-runtime messages, historical hashes and same-trace joins. The trace audit found zero conflicting owners or later-only owner signals across 421 trace groups; 71 resource lines had no owner signal and were not assigned by trace alone. JSON query selectors and lookup-start events do not become stored records.

Evidence: `dataset_catalog.md`, `schema_mapping_audit.md`, `json_owner_coverage.md`, `log_schema_coverage.md`, `log_trace_integrity.md`, `datapoint_extraction_map.md`, `document_text_inventory.md`, and `image_text_inventory.md`.

## Labeled sample result

The final sample candidate at `artifacts/csv/phase17_final_sample.csv` is byte-identical to the preceding citation-ranked candidate (SHA-256 `CAFEB7870C3E9259D7A587D5FA19C0CEE3194F03C551CC93D5462622747B13D2`). It matches **32/32 statuses (100%)** and **12/32 exact ordered step arrays (37.5%)**. Gold contains 193 steps; the agent emits 167. The position-independent diff has **26 missing semantic steps, zero extra semantic steps, and zero shared-step citation differences**. The 20 citation differences seen before contemporaneous-source ranking have been resolved. Positional system/resource mismatches in `step_diff_report.md` arise from the missing rows shifting the arrays, rather than a new Phase 6 system-name mapping rule.

`step_diff_report.md` gives every case result. `sample_gold_backtrace.md` traces each missing step to the cited source, other evidence occurrences, activity rows and request-time context. Four gold file citations name a file without the target resource ID: case_01/account_001, case_02/account_002 and case_04/account_004 cite `evidence_54`; case_31/account_4857 cites `evidence_51`. A negative snapshot can establish absence, but the requested resource and subject still need a justified link. Seventeen other gold file citations name the target without an owner on its literal row or line; PDF page layouts may need wider contextual reading and are labeled accordingly in the backtrace.

Of the **26 missing semantic steps**, 16 target full IDs occur in none of the 94 evidence files and 10 target records appear with no matching subject identifier in their structured record. Of those 16, thirteen appear only in ownerless `system_activity.csv` rows; three have no full-ID occurrence in *any* participant input other than the public sample answer: `case_04/account_004`, `case_18/audit_record_6645`, and `case_20/audit_record_5569`. This is a precise source-coverage observation. It does not assert that the sample answer is false or that a supplied file is missing.

Concrete backtrace examples:

- `case_01`: `evidence_54` has `account_005` and three unrelated accounts, with no `account_001`. `activity_3342` names `account_001` 17 seconds before a reported completion, but has no user or case field.
- `case_03`: `evidence_94` lines 42–43 and `activity_3852` name `analytics_9406`; the lookup key and direct identifier fields are null. A nearby `user_43` security line has a different trace ID.
- `case_04`: `analytics_901` is in `evidence_56` with null identifiers. The gold `account_004` target appears in neither evidence nor activity.
- `case_21`: `evidence_92` shows `account_6440` as a 404 result and `analytics_5335` as anonymized, both without subject fields. Their state is visible; their case ownership is not.
- `case_24`: `evidence_92` was captured before the audit cutoff and confirms the same state as the retrospective `evidence_02` bundle. Preferring it as citation removed a source-selection mismatch without altering state.

## Inference checks and rejected shortcuts

The independent, gold-free `temporal_owner_probe.md` tests reported-time proximity using directly owned account resources. Across 212 evaluable full requests, the nearest account activity belonged to the requester in only 71 (33.5%). Numeric account/user suffixes agree for only 1 of 240 directly owned account resources. These rates do not justify attaching anonymous records to a person by time, case number or suffix. A model suggestion cannot override a missing exact owner/correlation link. The 32 sample labels were not used as a production resource mapping table.

## Full 518-case candidate

The final `output.csv` has 518 unique, naturally sorted rows (136 COMPLETE, 366 INCOMPLETE, 16 NOT_APPLICABLE), SHA-256 `3914BEF9080E7372D59D601CAADF0BD3152EF430B2F1C1D3B3DC8F997A38A3A2`. The structural validator passed **18,918/18,918 checks**, with zero errors and warnings. All **518/518** case diagnostics completed without pipeline errors. Each case enumerated all 94 manifest entries, for 48,692 manifest dispatches. The controlled tool loop inspected 23 sources in 14 cases; the activity expander recorded 1,023 per-case derivations.

The citation audit checked 944 cited steps (896 file and 48 activity citations) and found zero unknown IDs or cited resources absent from their cited files. Twenty-four cited files were collected after their case's audit cutoff; a separate row check found an at-or-before-audit observation for all 24. This remains a provenance nuance because the repository's evidence rule also discusses file capture time. Nine COMPLETE rows have empty verification arrays (`case_61`, `case_63`, `case_534`, `case_536`, `case_537`, `case_538`, `case_539`, `case_540`, `case_542`); they are structurally valid but lack a resource-level proof step. These quality risks are not hidden by the validator's green result. See `citation_audit.md` and `runtime_diagnostics_summary.md`.

## Tests and model usage

The full regression suite has **410 passing tests and one failing release-gate test**: `test_p14_hard_gate_full_sample_pipeline` requires at least 28/32 exact arrays and observes 12/32. All parser, source-coverage, provenance, cache, Vision, orchestration and structural tests pass. The hard gate was neither skipped nor weakened. Focused checks for the latest source audits also pass.

The final full run recorded **266 actual `gpt-4o-mini` responses**, **48,833 input tokens**, **22,160 output tokens**, and an estimated **$0.020621** under the repository's pricing table. Cache hits consumed no API tokens. The exact per-purpose and per-request figures are in `usage_report.md`. The `.env` credential stayed inside the repository, was not printed, and is excluded from packaging.

## Readiness and next evidence requirement

**NOT_READY** for the requested 85% dual gate: status exceeds it, but exact arrays reach 37.5% rather than 85%. The remaining sample differences are 26 absent resource verifications and no extra or citation-only differences. Under the current exact-owner rule, 14 distinct sample cases with an evidence-absent target create a conditional upper bound of 18/32 exact arrays even if all other cases matched. Reaching 28/32 without guessing would require a participant-visible case/user-to-resource correlation for the ownerless and absent targets, or an explicit change in the expected verification semantics. The output and archive are reviewable candidate artifacts, not a claim of hidden-set accuracy or a passed release gate.
