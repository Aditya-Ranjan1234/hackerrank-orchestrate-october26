# Northstar Shop Deletion Audit Agent — Design Tradeoffs

This document records the important implementation decisions made through Phase 5.

## Deterministic orchestration

Identity resolution, state reconstruction, flow detection, policy, status, and
future step generation are deterministic Python. This protects grader accuracy,
reproducibility, and auditability. Optional model assistance is confined to
ambiguous evidence extraction; no model calls have been used so far.

## Reported status is excluded

`reported_status` is not consulted by the status determinator. It is explicitly
a workflow claim, not proof. The determinator uses request intent, identity,
cutoff times, and policy verdicts. S5 and S17 test this independence.

## Empty request text defaults to deletion

An empty `request_text` is treated as deletion intent because every row in
`deletion_requests.csv` is in deletion-audit scope. Only explicit non-deletion
keywords produce `NOT_APPLICABLE`. This avoids discarding system-generated
requests with empty text fields and is tested as S11.

## Ambiguous keywords favor deletion

If text contains both deletion and non-deletion keywords, deletion wins. A
request such as “delete my data and export a copy” still authorizes deletion;
the export is contextual. This is tested as S18.

## Cutoff-aware historical identity

Current and historical identifiers are resolved through the supplied identity
tables, while `audit_at` prevents future identity events from affecting an
earlier snapshot. Ambiguous unsupported histories fail conservatively rather
than inventing ownership or merge relationships.

## Evidence cache and evidence precedence

Evidence extraction is cached by SHA-256 file content so the same evidence can
serve multiple cases. When direct evidence at or before the cutoff conflicts
with an activity claim, evidence wins and the conflict is recorded. Post-audit
events are preserved separately for later flow analysis and cannot rewrite the
historical state.

## Active flows require recreation capability

A flow may be active while `can_recreate_at_audit` is false if its source has no
data for the user. Such a flow is retained in the audit facts but does not
trigger disabling. This avoids unnecessary remediation while preserving future
risk context.

## Retention boundary

`retention_expires_at <= audit_at` means retention has expired. The strict
boundary prevents data from being retained beyond its stated allowance and is
tested in the flow/policy phases.

## Policy conflict precedence

Conflicts resolve by tombstone specificity, system specificity, strictest
treatment (`DELETE > ANONYMIZE > REDACT > RETAIN`), explicit priority, earlier
retention expiry, and finally rule ID. Strict treatment prevents a permissive
rule from hiding personal data; conflict notes preserve the explanation.

## Tombstone privacy

Tombstones may retain stable `user_id` linkage, but direct identifiers including
`email_hash` must be removed. This supports retained references without leaving
recoverable identity data and explicitly covers the email-hash trap.

## Fail-closed unknown categories

Unknown categories default to `DELETE_RECORD` and record
`no_matching_rule_fail_closed_to_delete`. This is safer than silently treating
unknown data as compliant, although a new category may be over-deleted until
its policy mapping is added.

## Over-deletion is incomplete

A missing RETAIN record or an absent record that should have been REDACTED is
`INCOMPLETE` with `RETENTION_VIOLATED`. Deletion must respect scope; over-
deletion must not silently pass. Phase 6 must represent this finding without
inventing an unsafe restore operation.

## Frozen phases and regression gates

Each phase freezes upstream files and adds tests, reports, usage data, and a
worklog entry before the next phase begins. This makes regressions attributable
and preserves the submission trace, at the cost of requiring compatible
interfaces or adapters for later improvements.

## Submission hygiene

The virtual environment, caches, logs, reports, and tests remain inside the
repository. Final archives must explicitly exclude datasets, caches, virtual
environments, and credentials. This follows the challenge contract and the
user's restriction against moving work outside the repository.

## Current status

Phases 1–5 are implemented. The regression suite passes 73 tests, with zero
LLM/VLM calls recorded. Phase 6 remains responsible for converting policy and
status facts into ordered `steps_json` without changing upstream decisions.

## Phase 6 step-generation choices

Operation numbers intentionally use gaps: findings 0–3, remediation 10–14,
and verification 20–25. This keeps the sort key monotonic and leaves room for
future operations without renumbering existing ones.

`RETENTION_VIOLATED` emits only `VERIFY_RECORD_PRESENT`. The allowed operation
table has no safe finding or remediation operation for an over-deleted retained
or redacted record; inventing one would violate the strict grader contract.
This remains a Phase 7 review question.

`ANONYMIZATION_INCOMPLETE` uses `REPORT_EXPOSED_PII` for the finding and
`ANONYMIZE_RECORD` for remediation. The finding describes identifiers still
exposed, while the remediation preserves the distinction between redaction and
irreversible anonymization.

## Post-Phase 7 Phase 2 unfreeze decision

The Phase 2 freeze was surgically lifted only for JSON/log matching because the
sample failures were predominantly phantom records. Exact field allowlists,
structured log tags, and cache-boundary isolation were chosen over patching the
status layer: the evidence layer is the correct owner of false matches.

The stricter iteration preserved all 121 tests but regressed sample status
accuracy to 50%, so it is recorded as an unsuccessful fix iteration. This is a
deliberate tradeoff: maintaining an honest measured result is safer than
claiming a quality improvement that the sample comparison disproves.

## Phase 8 recovery iteration

- Exact-value JSON matching was broadened to support the dataset's `customer_reference` and shipment-specific fields, while still rejecting substring matches. This is a measured rollback of the earlier allowlist, because the allowlist caused a 75% to 50% regression.
- Tagged log lines remain mandatory, but matching is allowed across the structured line so valid operational records are not lost when the export uses free-text payloads.
- Activity-only tuples are reconstructed because the real CSV has no `target_user_id`. A documented resource-suffix fallback supports the synthetic `user_01`/`account_001` convention; it is intentionally conservative and remains an open question for a production schema.
- The recovery reached 22/32 (68.75%) and did not change frozen orchestration/status/steps code. The residual gap is documented rather than hidden.
## Phase 9 activity inference

The activity expander was placed at the orchestrator boundary rather than unfreezing Phase 3. This preserves the tested reconstructor, flow detector, and restore-risk contracts while allowing derived rows to be processed through the normal pipeline. Resource-ID inference has precedence over time proximity to avoid duplicate facts. The implementation produced no full-run derivations because the supplied evidence keys do not overlap activity keys; that limitation is documented rather than inventing a weaker join.
## Phase 10 grounding audit

We added observation and trace tooling without changing the deletion decisions. Raw CSV and evidence inventories showed that the Phase 9 claim of no overlapping resource IDs was incorrect. Record timestamps must come from source snapshots rather than extraction time; numeric resource suffixes cannot establish ownership. The diagnostic logger cites actual input rows and records both input and output of each phase, while the audit scanner separates optional injected VLM callbacks and test fixtures from production API paths. These findings define a narrow, evidence-backed Phase 11 repair instead of tuning the proximity window against an invalid timestamp basis.
## Phase 11 strict ownership versus coverage

Removing numeric-suffix ownership prevents false attribution of unrelated resources, as shown by cases 02–04. It also revealed that several correct statuses had depended on that unsupported inference because the evidence registry supplies only user IDs to the JSON handler. We keep strict ownership and record the regression rather than reintroducing a guessed join. JSON timestamp and system metadata are now carried from nested snapshots, but the frozen registry still prevents email-only rows from entering the IR. Phase 12 should repair that explicit interface and validate proximity inference against real records before packaging for submission.

## Phase 12 identity-aware extraction and cache

We preserved the actual `extract_file` API and passed the existing full identity object through to JSON instead of inventing the kickoff's hypothetical registry/manifest API. The handlers remain identity-aware, so the cache now keys on file bytes, identity, and audit cutoff; identity-agnostic extraction would reduce cache cardinality but requires a broader refactor. Structured log trace joins and serialized SQL payload parsing are grounded in literal trace IDs, resource IDs, and JSON keys, not numeric suffixes. The log expansion recovered true cases but also exposed a false positive in case 03; keeping this visible is preferable to tuning a case-specific exception. Scanned images remain unprocessed without a VLM. Sample accuracy is 25/32, so Phase 12 is not submission-ready.

## Phase 13 diff before unfreeze

The user hypothesized a systematic Phase 6 defect because exact steps match 0/32. The diff instead shows extra/missing step identities (716 count mismatches; only 32 position-independent exact overlaps) and seven status failures rooted in derived activity affiliation. A Phase 6 count filter would merely suppress evidence-backed or erroneously inferred facts without fixing ownership. The necessary activity-expander decision point is explicitly frozen in Phase 13, so we chose transparent diagnostics and a NOT_READY gate over an unauthorized or case-specific patch.

## Phase 14a exact-resource ownership only

Removed the ±24h same-system derivation because `phase13_case03_regression_audit.md` showed it affiliated an unrelated cache operation to case 03. Exact full-resource evidence matches remain; the proposed file-ID match is accepted only for the explicit `evidence_<resource_id>` convention, not arbitrary substrings. This intentionally loses weak same-system-only signals. The first sample pass cut generated steps from 885 to 312, but status remains 25/32 and exact steps 0/32; the measured result is recorded without claiming recovery.

The Phase 9 tests that required proximity were rewritten in the explicitly allowed `test_activity_expander.py` because they codified the unsafe heuristic. A Phase 13 diagnostic test in frozen `test_case03_regression.py` also codifies it; that test now fails, and we will not edit a file the user expressly froze. Case 03's remaining finding is a separate security-audit-log retention mapping gap.

A Phase 14b security-audit retention mapping was tested because `dataset/deletion_rules.csv:13` says RETAIN. It made case 03 COMPLETE but also made case 14 incorrectly COMPLETE because the pipeline had no restore-risk fact for its backup. We reverted that isolated policy change rather than accept a regression or invent a case-specific exception.

Phase 14c emits explicit 404/null-profile JSON readbacks without assigning an owner. The accepted trade-off is that a separate exact full-resource join is necessary before using them in a person's audit; absence of a name or email is not itself proof that the row belongs to the requester. This is grounded in the `account_5684` readback in `evidence_92` and will be guarded in the reconstructor.

The reconstructor now admits blank-owner ABSENT readbacks only when earlier direct evidence established the same `(system_id, resource_id)` for the identity. This is stricter than the prompt's proposed substring file-ID relation and prevents a global 404 list from being assigned to everyone. Case 26's account state correctly changes to ABSENT, but other flow, retention, and redaction states keep its case status wrong.

Two synthetic tests guard the blank-owner join against cross-user contamination and nonmatching resource IDs. Position-independent exact step overlap improved from 32 to 45; that is material progress in evidence fidelity, although the whole-case gates remain unsatisfied.

Phase 14c now carries explicit backup restore-access status into state notes from literal `restore_allowed` or `BACKUP_ARCHIVE | ACTIVE/BLOCKED` evidence. This does not infer risk from backup existence. It enables the conditional policy engine to distinguish case 14's restorable backup from blocked backups in `evidence_92`.

The paired policy change handles security audit retention and backup restore checks from literal evidence state. It recovers cases 03, 21, and 25 without sacrificing case 14, reaching 28/32 status accuracy. The trade-off is a targeted rule-ID selection (`rule_12`) because the existing loader aliases two different log rules to the same `logs` category; this is narrower than changing the frozen loader. Exact step arrays remain 0/32, so the result is not release-ready.

Phase 14c now distinguishes explicit redaction (`null` contact fields or literal `[REDACTED]` text), redacted tombstones, and disabled connectors from generic PRESENT. The evidence is directly visible in the service export and tombstone snapshot. The trade-off is strict shape-specific handling: it will not infer redaction or flow-disablement merely because an identifier is absent, and it will not assign anonymous analytics rows to a user without a proven resource join. Sample verification is pending.

With a fresh development evidence cache, the shape-specific change recovered case 31 but left cases 26–28 wrong: their support facts were now REDACTED, yet `support_platform` still fell into unknown-category DELETE. The direct platform-to-ticket category alias follows the supplied SUPPORT_MESSAGE redaction rule. This accepts the risk that other support-platform resources may need a more specific future category; the mapping is no broader than the existing support-service category.

The support alias brought sample status to 32/32, but exact step arrays remain 0/32. We added synthetic state/policy guards in the only unfrozen test file. We will not fabricate missing resource ownership merely to match gold step arrays.

An executable Phase 14 sample hard gate is intentionally retained even though it currently fails on exact steps. This makes the unmet acceptance criterion visible to future runs. A passing suite obtained by skipping or weakening that assertion would misrepresent readiness.

The Phase 14d audit found a source-grounding ceiling for the step gate: gold asks for account verifications in cases 01, 02, 04, and 31 even though the cited evidence files do not contain those full account resource IDs, and for case 03's anonymous analytics readback without a user identifier. The activity rows also lack a target user. Supplying those five step arrays would require new ownership semantics or external corroboration; restoring numeric-suffix or same-time attribution would reintroduce the false positives this phase removed. Therefore we keep the stronger ownership invariant and label the package NOT_READY despite 32/32 statuses.

Phase 15a traces case_29's extra JSON-path resource to a nested document whose parent visibly carries `search_1993`. The handler now inherits only a visible ancestor ID and lets a child override it. This is a source-grounded correction, not a gold-case exception. We leave the stale proximity assertion in frozen `test_case03_regression.py` untouched, because reintroducing proximity to make a test pass would violate the proven ownership invariant.

Phase 15b adds compliant-resource verifications to INCOMPLETE step arrays because gold case_29 explicitly contains them. They cite no evidence in that path, matching the existing incomplete-verification convention. A resource without a grounded verdict is still not invented.

Phase 15c adds semantic step diagnostics because positional system-ID differences are inflated by inserted/missing steps. It also makes the diff tool regenerate current sample output by default, instead of silently reading Phase 12. We do not globally prefer an older `evidence_92` readback over a later evidence snapshot just to match sample citation IDs; the audit's temporal provenance rule has priority.

Phase 16 adds optional OpenAI semantic assistance, but retains evidence-constrained decisions. Caching and tracing make calls auditable and repeatable. The model is not allowed to invent anonymous record ownership from a case number, numeric suffix, or proximity; an exact resource-ID owner must already be visible. Actual model usage and cost will be reported from API responses, not the existence of a configured key.
## Phase 16 — optional semantic resolution

The OpenAI path is an optional, auditable assistant for unresolved labels, flow class, directly corroborated anonymous records, competing citations and image evidence. It cannot create user ownership from numeric similarity or model confidence alone. This protects the evidence standard even where gold expects an ownerless record. Calls are cached and traced locally; a failed key leaves the rule-only pipeline intact. See `code/evaluation/phase16_changes.md` for per-change rationale.

The verified repository `.env` is now the sole API-key source; the stale inherited process key is ignored. Strict Vision system-ID validation removed two pilot false positives. The completed hybrid sample preserved 32/32 statuses but reached only 2/32 exact arrays, at an estimated $1.266820 in response-token cost. A full 518-case hybrid run is deferred because the exact-step release gate remains far below 28/32 and model-only ownership would be unsafe.

## Phase 17 — exhaustive sources, conservative ownership, lower-cost Vision

The 94-file inventory now parses SQL tables/rows, PDF text/tables, image metadata, structured logs and JSON. Exact same-row subject/resource evidence remains the ownership standard: a same-file mention, numeric suffix or model confidence cannot bind an anonymous resource to a requester. This preserves audit defensibility even though five sample gold resources remain unsupported. The external Tesseract executable is unavailable on this host, but local RapidOCR reads all 11 screenshots and high-detail `gpt-4o-mini` provides a cross-check; filesystem copy time is not used as evidence time. Historical sample CSVs were moved inside `artifacts/csv/`, while phase validation reports are grouped via hardlinks to preserve their required canonical paths. Detailed choices and measured effects are in `code/evaluation/phase17_changes.md` and `code/evaluation/phase17_validation.md`.

The first high-detail mini-Vision sample cost $1.962913, disproving the simple “mini is cheaper” assumption for these large screenshots. A low-detail experiment cost less but lost small-text confidence. Since the user explicitly prioritized accuracy over cost, **high-detail `gpt-4o-mini` is the final default**; detail level is part of the cache key so experiments do not contaminate each other. RapidOCR provides a second, local reading of all 11 screenshots. A model-only row that contradicts visible text is rejected, not promoted to ownership.

## Phase 17 — logical records, source types, and ghost prevention

Physical failover/read/replication targets are normalized to one logical resource verdict when the full resource ID agrees. The original table and evidence file remain in the audit trail, and a PII-bearing replica is preferred over a clean primary copy when both have the same timestamp. This prevents duplicate remediation steps without hiding replica ghosts. A one-off SYNC checkpoint is not an active flow unless recurrence or a future run is explicit.

Support attachments and secondary-identifier contact lookups follow their source category, not the broad platform default: an attachment is deleted under `SUPPORT_ATTACHMENT`, while a shared support conversation can be redacted under `SUPPORT_MESSAGE`. A missing deletion marker means the row survives, not that it is absent. Timestamp-prefixed JSON logs join a start-event subject to a completed resource only through the exact trace ID; an unrelated trace cannot confer ownership.

`source_resource_id` is an admissible cross-schema join because it contains a literal full ID in an identity-owned SQL row. Number similarity and neighboring timestamps are not admissible. Identity-link and restore-access activities describe metadata/access, not current record presence; only state-changing operations seed a ResourceFact. Backup record and restore-risk views are deduplicated into one restore obligation, and finding citations prefer the evidence source corresponding to the verdict kind.

The sample gold sometimes cites older `evidence_92` despite a later `evidence_02` snapshot. We retain latest-at-audit provenance rather than globally prefer the gold citation. The remaining exact-step deficit is primarily missing owner links and these citation differences, not an excuse to invent or hardcode case resources. The release gate remains visible and red; a structurally valid `output.csv` is not deemed submission-ready.

## Phase 17 continuation — model-supervised tools without model-authored facts

Every case re-enumerates the local 94-file evidence manifest, but extraction and high-detail mini-Vision are cached by source/prompt/identity/audit inputs. This preserves changed-file invalidation while avoiding thousands of identical model calls. The source is a point-in-time dataset, not a live Northstar connection; claiming real-time system state would be misleading. `gpt-4o-mini` now receives a strict server-enforced schema for full-screenshot row mapping, with bounded retries. A single Vision excerpt is not proof: local OCR must show both literal IDs, or an OCR-empty image needs a second independent Vision agreement.

The new mini-planned audit loop chooses from a short allowlist of read-only JSON/SQL/log/PDF/image tools when an extraction is anomalous or evidence states conflict. The orchestrator checks the chosen file and tool against the manifest and confines paths to `dataset/evidence/`; a malformed plan falls back to a real local read, not an invented finding. Diagnostic results do not silently become policy facts. We prefer this separation over letting the model create a user–resource link from a nearby timestamp, query selector, common numeric suffix or same-file co-mention.

The 24 SQL files contain 127 table instances and 681 exact-identity-linked rows across concrete systems. Generic replica tables take `origin_system` from each owned row, not the physical replica table name. JSON `lookup_value` and `subject_selector` are query context, not stored owner fields; treating them as owners was a ghost-data risk. The full structural validator now counts successful checks and the submission ZIP includes `requirements.txt`. Accuracy and known gaps are measured separately in `code/evaluation/phase17_validation.md`; a green structural check alone does not authorize submission.

## Phase 17 continuation — stale lookups and evaluation boundary

A `lookup_started` event describes an attempted read; it does not prove that a record exists. The log handler now retains its trace context but emits a record only from a completed event. A 404 lookup that predates the deletion request cannot verify the later audit state, so the orchestrator excludes that negative result while recording the exclusion in the evidence notes. The source showed a March 404 query becoming an extra September account verification. This generic request-time rule removed that ghost and raised exact sample arrays from 10/32 to 11/32 without changing 32/32 statuses.

At the Phase 17 closure, the production runner projected each case to `case_id`, `email`, `requested_at`, `audit_at`, and `request_text`. The later workflow-affiliation iteration captures `reported_at` as a bounded time-correlation hint before that projection. Neither `reported_at` nor `reported_status` reaches status determination or model tools, and `reported_status` is never read. A static import-closure audit and a runtime read guard verify that sample answers and prior output are outside the production input path. Evaluation tools may compare to the sample answer, but repeated use of those 32 labels makes the sample a development set. We report its exact fit separately from the unlabeled 518-case structural audit and do not claim an unbiased hidden score.

A later owner-bearing JSON/SQL row can identify an earlier ownerless 404 only when the complete resource ID and system match. We use the later row solely for affiliation and keep the earlier readback's ABSENT state and timestamp. This recovers a real cross-snapshot link without converting future PRESENT data into an earlier PRESENT claim. Query selectors and model-only owner assertions cannot make this join.

Source citations must be verifiable independently of status and step shape. The citation audit treats an `evidence_*_line_N` handle as a real log record only when line N exists and names the exact resolved subject. A Phase 9 `activity_*::derived_*` identifier is an internal row; the public finding now cites the original `activity_id` from `system_activity.csv`. The audit does not read sample answers, so it can check all 518 outputs without gold leakage.

The remaining 16 missing sample targets with no literal occurrence span 14 cases. Of those, three have no pre-audit activity for the target; the others' activity times overlap 5–12 open request windows in the supplied requests. Assigning those activities to a person by time or case suffix would be speculative. The strict ownership rule implies a conditional 18/32 exact-array ceiling, below the 28/32 release gate. We keep the gate failing and request additional owner/correlation evidence rather than manufacture a match.

An independent scan of all 26 structured logs checked 421 trace groups for conflicting canonical users, unstructured-only identifiers, and a resource event whose only owner appeared later. None occurred in this source snapshot; 71 resource lines had no owner signal. We retain the exact trace join while keeping those ownerless lines out of per-person facts. The report and tests make this source-specific confidence check reproducible without consulting sample answers.

The SQL parser's own count of 681 linked rows under current identities could have hidden omissions. A separate exact-column query found 159 direct owner rows and a nested-JSON traversal found 522 more, with zero omissions. Extending this independent audit to historical emails and hashes raised coverage to 716 linked rows (186 direct and 530 nested), again with zero omissions. This still does not prove every possible semantic owner field, so the complete table/column inventory remains part of the audit.

## Phase 17 source backtrace and citation provenance

The user was right to ask for another search. A source-only audit found a real coverage defect in structured logs: the prior parser missed quoted resource IDs, six-column operations-stream events and nested cloud-runtime messages. The revised parser recovers all 673 independently identified direct owner/resource pairs in 26 logs, preserves exact same-trace ownership and does not turn query-start events into stored records. It also restores the prior historical email-hash PII signal. JSON readbacks now recover all 544 independently observed direct owner/resource pairs across 28 files. These changes improve hidden-case source coverage even though the 32 labeled sample cases keep the same statuses and semantic step count.

A case-by-case gold backtrace revealed 20 citation differences caused by choosing a retrospective September 17 bundle when a September 15 captured service export confirmed the same audit-time state. A strict rule that discarded all retrospectively captured files made the sample worse, because those bundles also contain valid historical rows. We therefore changed only citation ranking: prefer a file captured by audit time for the same resource and state, and retain the retrospective file when no contemporaneous source exists. The deterministic fallback and the model selector use the same provenance boundary. This removed all 20 citation differences without changing status or fabricating facts; exact arrays improved from 11/32 to 12/32.

The remaining 26 missing semantic steps are traced in code/evaluation/sample_gold_backtrace.md. Sixteen full resource IDs are absent from all 94 evidence files; ten occur as ownerless records. We manually reopened all 11 original screenshots and checked PDF text/tables, SQL, JSON and logs. A nearby activity is not a sufficient owner link: on 212 full-dataset requests with a directly known account action, choosing the account action nearest the request's reported time was correct only 71 times. Numeric account/user suffixes agreed in only 1 of 240 directly owned account resources. Some sample gold citations also name files without the full resource ID, such as evidence_54 for account_001. We keep the 85% exact-step gate red rather than introduce a case-number or time-based join that the data does not justify. The 32 labeled sample cases have been repeatedly inspected and are a development set, not an unbiased hidden evaluation.

The follow-up scan also checked every other participant CSV, excluding the gold answers and blank answer template. Thirteen of the sixteen evidence-absent target IDs occur only in ownerless system activity; three have no full-ID occurrence in any participant input: case_04/account_004, case_18/audit_record_6645 and case_20/audit_record_5569. This is a precise coverage finding, not a claim that source files are missing or that the gold answers are wrong. We preserve the source-only boundary instead of using sample labels as a production mapping table.

The final full-output provenance audit found 24 citations to files collected after the case's audit cutoff. In each, the extracted cited resource has an at-or-before-audit observation; source capture and observed row time are therefore tracked separately. The repository's literal file-capture cutoff rule may still treat those citations as inadmissible, so they remain a documented submission risk. Nine COMPLETE full-run rows have no verification steps because no owned resource was established. They are flagged as an evidence-quality risk rather than filled with a guessed account ID. The 518-row CSV is structurally valid, but the 12/32 exact sample step score and retained hard-gate failure keep the candidate NOT_READY.

## Post-Phase 17 — distinguish missing facts from step-generation defects

The public step diff's dominant positional `SYSTEM_ID_MISMATCH` is a consequence of missing rows shifting later array positions. A phase-by-phase diagnostic shows that all 26 missing semantic steps disappear before policy: 13 have only ownerless activity, seven are anonymous raw evidence filtered during case extraction, three are extracted anonymous 404 readbacks with no independent owner, and three IDs do not occur in participant inputs at all. Changing Phase 6 mappings or filling steps from sample answers would hide this upstream provenance gap. No production behavior was changed.

We also tested a stronger time shortcut against independently owned account resources in the 518-request input. A unique deletion event in the five minutes before a request's reported time identified the requester in **0/25** verifiable controls. This makes a plausible time-based case affiliation unsound even when the event is unique. The production agent continues to require a full resource/identity or explicit correlation link. The trade-off is lower public exact-step fit in exchange for avoiding wrong-person deletion audit claims. See `code/evaluation/step_gap_diagnosis.md` for the reproducible trace.

The case 01 follow-up shows why a blanket dismissal of time context was too coarse. `activity_3342` is a unique event 17 seconds before case 01's reported time, and a later account SQL snapshot has no `account_001`. We now document it as a strong retrieval candidate. We do not promote the timestamp to an owner key: directly owned full-request controls refute time-only affiliation, while the distinctive completion wording has no comparable full-request controls. A second, independent capability would be needed to cite the SQL snapshot for a missing row: an audited closed-world anti-join after the resource is securely affiliated. See `code/evaluation/case01_process_trace.md`.

## Current iteration — calibrated workflow affiliation and counterexample control

The five-minute nearest-event rule remains rejected: 0/25 independently owned unique candidates matched the requester. A seemingly safer rule that first removed FAILED and PARTIAL account actions was also rejected after a gold-free control found only 42/90 independently owned unique SUCCESS candidates matched the requester; 48 belonged to another person. Outcome filtering must happen **after** uniqueness across all account deletion outcomes. In a 30–90-minute report-delay window, 26/26 source-owned unique actions matched the requester, including 14/14 whose winning outcome was SUCCESS. A five-fold masked-owner control recovered 63/63 known held-out owners with zero wrong, while leaving 100 ownerless candidate derivations unscored. These are source-only controls, not hidden-answer accuracy.

The production rule now uses `reported_at` only for this bounded affiliation. It requires one account deletion across every outcome, a SUCCESS result for that unique winner, request/audit time bounds, no conflicting eligible requester at the report time, no directly owned primary account for the subject, and no direct other-person owner for the candidate ID. Direct owners are indexed from JSON, SQL, logs, the text handover, PDF rows and local image OCR, including historical aliases. Identifiers are joined by exact full value; conflicting aliases are omitted. `reported_status` remains unread and the projected case sent to status determination and model tools excludes both report fields. Per-case traces show the derived activity or an explicit abstention reason.

The event's SUCCESS result is still a claim about state. A separate completion-proof gate checks whether the inferred account has an independent evidence readback. If an activity-only compliant account would otherwise make the case COMPLETE, the agent instead marks it INCOMPLETE and emits a future `VERIFY_RECORD_ABSENT` step with an empty citation. Two full-input pilots changed from activity-cited COMPLETE to that proof-seeking result with zero pipeline errors; the public sample score was unchanged. This conservative status rule protects the brief's requirement that a COMPLETE verification cite actual evidence.

This recovered the missing account verification in one public sample case without changing any previously exact array: 32/32 statuses and 13/32 exact arrays versus 12/32 before the iteration. The 25 residual semantic steps all fail before policy/step construction. Three required full resource IDs occur nowhere in participant inputs outside the public answer; several others are anonymous records with no source owner. We keep the 85% exact-array gate failing and do not turn a model assertion, numeric suffix, file-order position or nearest event into an owner. Case 01's 17-second action falls outside the calibrated band. Its later SQL export contains no `account_001`, but lacks a declared complete account scope, so a global absence anti-join would not justify a citation.

## Current iteration — source booleans precede model classification

The first full-run comparison exposed four unrelated connector plans flipping between DELETE_RECORD and DISABLE_DATA_FLOW. Their cited structured logs explicitly said `enabled=false`, but the log parser kept that token as the string `"false"`; state reconstruction expected a Boolean. This left the source fact untyped and let `gpt-4o-mini` decide whether the resource was a flow. A confident type label then implied an active flow even though the readback said disabled. The repair is at the parsing boundary: convert only explicit textual `true`/`false` for `enabled` and `restore_allowed` to Booleans, as JSON logs already do. Ambiguous values remain available for model-assisted interpretation. Five synthetic tests cover both connector states, both restore states and escaped log syntax. See `code/evaluation/log_boolean_regression.md` for the source trace and direct full-input replay.

An additional source-only control tested whether an owned account deletion can carry its owner to a nearby anonymous analytics anonymization. Within 90 minutes, one of 10 evaluable owner-bearing pairs had the same user and nine belonged to different users; small activity-ID gaps gave the same 1/10 result. We therefore reject this apparently convenient way to fill the remaining sample steps. The observed 30–90-minute account report join remains limited to the uniquely calibrated account action and only produces a future check when deletion state lacks an independent readback. See `code/evaluation/anonymous_affiliation_controls.md`.


## Scored-output row review — source obligations before sample fit

The assistant reviewed all 518 original plans and every changed final row. The result changes 115 rows (34 statuses), adding 324 steps and removing 228. The 21.9 reference differs from the old 21.6 root in only six Portuguese-request rows; it is a prior prediction, not a label source. The exact before/after ledger and all-row evidence-limit ledger are retained under artifacts/csv/.

The corrections preserve several distinctions that the earlier implementation collapsed: a persisted connector subject_selector is an owner field while a search query is not; a connector ID in a SYNC event is not a search record; an exclusive attachment requires DELETE rather than conversation REDACT; SQL zero is a state flag rather than an unknown type; an active legal hold requires RETAIN. Intent handling now respects explicit negation and marketing-only scope, and recognizes the Portuguese deletion wording. Historical phones join by the complete number, retaining country code and requiring unique ownership; no last-ten-digit guess is permitted.

Catalog ownership and visual existence can corroborate each other even when the canonical resource ID is absent from the pixels. Three such exact alias joins passed the capture-time and conflicting-owner checks. The marketing screenshot's owner conflicts with its catalog entry and is deliberately left unresolved. The phone-only attachment is also supported by identity history and the selected customer screenshot.

These source facts add four semantic steps absent from the public sample and lower exact-array matches from 13/32 to 12/32; all 32 statuses remain correct. We retain the evidence rather than suppress it to fit public answers. The existing exact-array gate still fails and no hidden-score improvement is claimed. Twenty-three retrospective citations, six activity-only absence proof gaps, case_55's unproved restore block, case_63's empty completion and case_430's separate owner join are explicit review limitations. The row replay proves consistency only with recorded obligations, not universal correctness. See code/evaluation/score_iteration_validation.md and row_review_findings.md.
