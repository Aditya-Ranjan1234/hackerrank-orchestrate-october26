# Trade-off index

The canonical, append-only decision record for all phases is [`../../tradeoff.md`](../../tradeoff.md). It was updated after each Phase 14 code change. This path is retained because the Phase 14 deliverable list explicitly names `code/evaluation/tradeoff.md`.

Phase 14's governing choice: exact full-resource and subject evidence replaced same-system time proximity. Literal 404, redaction, connector-disablement, backup-blocking, and tombstone fields can determine state only when ownership is independently proven. This recovered sample status accuracy to 32/32 but leaves exact steps at 0/32. We do not restore proximity, numeric-suffix ownership, or a Phase 6 count filter merely to imitate gold. The source-level rationale and per-change measurements are in [`phase14_changes.md`](phase14_changes.md) and [`phase14_validation.md`](phase14_validation.md).

## Phase 15a: nested resource identity
The case_29 gold diff showed an extra JSON-path resource under the visibly identified `search_1993` row. We carry a parent's explicit ID into an otherwise ID-less child, while preserving any explicit child ID. This fixes source attribution without changing the strict user-ownership rule. The nominal dominant system-ID mismatch is largely positional and does not justify rewriting system attribution. Results are recorded in `phase15_validation.md` after validation.

## Phase 15b: complete checks inside incomplete cases
Gold case_29 includes empty-citation verification for resources already compliant when other resources fail. The step builder now emits those checks in the INCOMPLETE path, with deduplication and no extra finding/remediation. This keeps case-level status independent of verification coverage. We do not manufacture a compliant verdict for a resource that lacks proved ownership.

## Phase 15c: semantic diagnostics over blind citation rewriting
The positional `SYSTEM_ID_MISMATCH` aggregate remains dominant after 15b, but matching by step identity shows near-correct cases whose main gap is a missing account resource or an older direct-readback citation. We preserve latest-evidence state/citation semantics rather than hard-code `evidence_92` priority from a small gold sample. The diff tool now reports semantic missing/extra/citation counts and no longer defaults to a stale Phase 12 output.

## Phase 16a: bounded OpenAI assistance
OpenAI assistance is optional, cached, traced and token-counted. Model output proposes a system, flow class, or citation, but all values are schema/allowlist-checked. An anonymous affiliation is rejected unless the same full resource ID is independently owned in the supplied context; guessing ownership would make a privacy audit unsound. The default model is the requested `gpt-4o-mini`; actual API availability and spending must be verified, not inferred from the presence of a key.

### Change 4 — Vision is opt-in and source-bound
Image evidence uses a validated PNG/JPEG input and a structured Vision response. It is not silently treated as an empty successful extraction: no key or corrupt bytes yield an explicit empty result. This avoids inventing PII but can miss image-only cases offline.

### Change 5 — Semantic suggestions do not outrank provenance
The four resolver calls are at the phase that owns each ambiguity. Anonymous affiliation needs an existing direct full-resource join; a model guess is not enough. Citation choices are limited to same-resource, same-state, audit-eligible files. This may cap sample accuracy but preserves the privacy-audit evidence standard.

### Change 6 — Reproducible optional dependency
The SDK is installed in `.venv` and specified in `requirements.txt`; the key is read only from the environment. The configured key currently fails authentication, so the validated result is rule-only, not a claimed hybrid improvement.

### Change 7 — Stop retries on credential failure
Network and 429 failures deserve bounded exponential retries; a rejected key does not. One `AuthenticationError` disables the client for that run, preserving throughput and preventing thousands of doomed calls. This does not suppress transient retry logic.

### Change 8 — Include dependencies in the submission archive
The existing packager archives `code/` but not root `requirements.txt`, so a mirrored `code/requirements.txt` is shipped. Temporary pytest files stay inside the repository but outside ignored/excluded source trees, keeping filesystem-fixture tests meaningful.

### Change 9 — Flow decisions require the winning raw row
A resource name like `data_flow_1` is not proof that a connector is active. The flow classifier now sees the winning evidence row and is invoked only for PRESENT rows with actual raw content. This trades possible missed sparse connector evidence for fewer false active-flow claims.

### Phase 16 closure — integrity over an unsupported gold join
The rejected key blocks hybrid validation. Independently, five sample gold verifications lack a direct owner-to-full-resource proof; their removal from strict evidence-based scoring caps exact matches at 27/32. We will not waive provenance or disable the hard gate to claim readiness. The 518-row artifact is structurally valid but remains a diagnostic, not an approved submission.

### Resumed Phase 16 — local `.env` authority and Vision schema
The user's verified repository `.env` supersedes a stale inherited process key. The SDK receives only the `.env` credential; tests can disable live calls without providing another key. First live image responses showed that a self-reported user reference does not make a malformed `system_id` usable: a backup ID and a page title were emitted as systems. The strict system allowlist rejects those records, sacrificing speculative coverage to prevent a false deletion finding.

### Resumed Phase 16 — count every usage-bearing response
The full hybrid sample consumed 377 API responses, including responses that failed JSON parsing and were retried. Counting only accepted JSON would understate actual token use. The usage tracker already counted those responses; tracing now records each attempt with its own tokens. Historical traces from before this fix cannot be treated as a complete billing ledger, so `usage_report.md` is the authoritative measurement for that sample run.

### Phase 17 — inventory before ownership change
The typed catalog opens every supplied file, not just its manifest row. SQL ownership columns and PDF table rows are parsed, but a resource is attributed only when an exact subject identifier appears in the same source row. Case 03's shared log file has the user and anonymous analytics resource on different lines, so it is not a safe join. Five no-link cases still imply a 27/32 evidence-safe upper bound unless new direct evidence is supplied.

### Phase 17 — OCR-first and mini-Vision
OCR is free and deterministic when the external Tesseract program exists. On this host it does not, so cached `gpt-4o-mini` is the fallback. A shorter JSON-only prompt reduces output tokens; the model cannot invent ownership. We use EXIF/source timestamps, not filesystem `mtime`, because all evidence files were copied after their audit times. The verified repository `.env` remains the only credential source, notwithstanding the older pasted instruction suggesting a process environment key.

### Phase 17 — artifact organization without broken paths
Historical generated CSVs now live in `artifacts/csv/`. Canonical phase validation report paths remain where earlier instructions and scripts expect them, with an NTFS hardlink collection at `code/evaluation/validations/`. This duplicates archive entries but prevents broken references and preserves mandatory filenames. Root `output.csv` and dataset inputs are intentionally unmoved.

### Phase 17 — image-detail cost inversion
The first mini-Vision run cost $1.962913, worse than Phase 16's $1.266820, because mini's high-detail tile rate is much larger in tokens. `low` detail makes cost bounded by one base image charge, but it may not read tiny screenshot text. We therefore separate high/low cache keys and measure the low-detail sample rather than extrapolating from text-token prices. No `gpt-4o` fallback is used.

### Phase 17 — accuracy-first OCR and provenance-safe overlaps
The user's accuracy-first instruction superseded the low-detail default. RapidOCR now reads all 11 screenshots locally, with high-detail `gpt-4o-mini` transcription cross-checked against visible rows. The model may clarify layout but may not invent a subject/resource pair; OCR/model disagreements remain in `image_text_inventory.md`. All four text-layer PDFs and the plain-text handover are reproduced in `document_text_inventory.md`.

An identity-owned SQL row's literal `source_resource_id` can bind its parent resource to a user; matching suffixes, nearby timestamps and file-level co-mentions cannot. Physical replicas are canonicalized to one logical verdict while preserving source-table PII risk. An unscheduled completed SYNC is not an active flow, and access/identity-link activities cannot seed a PRESENT record state. Source-typed attachment and contact-lookup rows use the supplied DELETE rules rather than broad support/analytics defaults. A missing deletion marker means the replica row survives. Timestamp-prefixed JSON logs join only matching trace IDs, and a restore-risk finding cites the risk evidence before a coexisting backup snapshot.

The sample improved from 2/32 exact arrays in Phase 16 to 10/32, with 32/32 statuses. The remaining missing owner links and older-gold-citation choices are documented, not hardcoded into production. The 85% dual gate is unmet, so a 518-row structural pass must not be described as ship readiness.

## Phase 17 continuation: strict mini-Vision and source-safe audit tools

The complete source manifest is checked on every case, with content/identity/audit-aware local caching and separate OCR/model response caching; this is point-in-time evidence, not live Northstar API access. `gpt-4o-mini` now reads full screenshots using strict JSON Schema and bounded retries. Accepted ownership requires literal OCR corroboration, or a second independent Vision agreement when OCR is empty. The model may plan two read-only source inspections on anomalies, but cannot create a ResourceFact from its own assertion. JSON selector/lookup fields no longer confer ownership. This favors a defensible audit over matching gold steps by numeric suffix or weak temporal correlation. SQL coverage is documented for all 24 files/127 table instances in `schema_mapping_audit.md`.

## Phase 17 final trade-off

The canonical detailed trade-off record is the repository-root `tradeoff.md`. The final 32-case sample has no shared-step citation mismatch or extra semantic step; 26 required semantic steps lack an auditable subject-to-resource link. Sixteen full target IDs are absent from evidence and three are absent from every participant input except the public sample answer. Source-only temporal and suffix probes showed high false-affiliation risk, so the agent leaves these links unresolved. The 518-row output has 24 later-captured citations whose cited rows are pre-audit and nine COMPLETE rows without verification; both remain visible quality risks. The 85% exact-step release gate is not met.


## Scored-output row review — source obligations before sample fit

The assistant reviewed all 518 original plans and every changed final row. The result changes 115 rows (34 statuses), adding 324 steps and removing 228. The 21.9 reference differs from the old 21.6 root in only six Portuguese-request rows; it is a prior prediction, not a label source. The exact before/after ledger and all-row evidence-limit ledger are retained under artifacts/csv/.

The corrections preserve several distinctions that the earlier implementation collapsed: a persisted connector subject_selector is an owner field while a search query is not; a connector ID in a SYNC event is not a search record; an exclusive attachment requires DELETE rather than conversation REDACT; SQL zero is a state flag rather than an unknown type; an active legal hold requires RETAIN. Intent handling now respects explicit negation and marketing-only scope, and recognizes the Portuguese deletion wording. Historical phones join by the complete number, retaining country code and requiring unique ownership; no last-ten-digit guess is permitted.

Catalog ownership and visual existence can corroborate each other even when the canonical resource ID is absent from the pixels. Three such exact alias joins passed the capture-time and conflicting-owner checks. The marketing screenshot's owner conflicts with its catalog entry and is deliberately left unresolved. The phone-only attachment is also supported by identity history and the selected customer screenshot.

These source facts add four semantic steps absent from the public sample and lower exact-array matches from 13/32 to 12/32; all 32 statuses remain correct. We retain the evidence rather than suppress it to fit public answers. The existing exact-array gate still fails and no hidden-score improvement is claimed. Twenty-three retrospective citations, six activity-only absence proof gaps, case_55's unproved restore block, case_63's empty completion and case_430's separate owner join are explicit review limitations. The row replay proves consistency only with recorded obligations, not universal correctness. See code/evaluation/score_iteration_validation.md and row_review_findings.md.
