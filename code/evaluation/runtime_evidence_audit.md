# Runtime evidence and agent-tool audit

## What a normal run reads

The default orchestrator loops through **all 94 rows** of `dataset/evidence_files.csv` for each request. A separate filesystem check found 94 unique listed paths, 94 actual files, zero missing, and zero unlisted evidence files. The 518-request dataset therefore makes 48,692 manifest dispatches in a complete run. This is local, point-in-time evidence processing, **not** a real-time connection to Northstar production systems. `ORCHESTRATOR_SKIP_EVIDENCE=1` is an explicit diagnostic shortcut and must not be used for a submission run.

| Source type | Files | Active parser and ID linkage |
|---|---:|---|
| SQL | 24 | In-memory SQLite; 127 table instances. Exact owner columns and nested `record_json` identifiers; per-row `origin_system` for generic replica tables. The inventory identity sweep yielded 681 exact-linked rows and zero generic-system results. |
| JSON | 28 | Recursive record walk with exact owner/reference fields, email/hash normalization, inherited resource IDs only from visible parents, row timestamps and state flags. Query `subject_selector`/`lookup_value` are not owners. |
| LOG | 26 | Structured key/value and timestamp-prefixed JSON, exact trace-ID joins, pre/post-audit separation. |
| TXT | 1 | Same structured log route; plain-text handover context is inspected. |
| PDF | 4 | `pdfplumber` text and tables. All supplied PDFs have text layers; a scanned page now renders locally with `pypdfium2` and passes through OCR/strict Vision. |
| PNG | 11 | Full-screenshot RapidOCR plus high-detail `gpt-4o-mini` strict-schema row extraction. Exact literal owner and resource IDs are cross-checked. |

See `dataset_catalog.md`, `schema_mapping_audit.md`, `document_text_inventory.md`, and `image_text_inventory.md` for file-by-file/schema/page/visible-text details.

All 11 PNGs were also visually checked at original resolution. The backup and export consoles show four direct row-level ID/email pairs each; the selected side pane repeats one of those rows, not an extra record. The search console shows a query email in the search box and two distinct result rows: only `search_428` has the in-scope `user_13` and matching email, while `search_1874` has a different email and no subject reference. The security explorer has six literal `audit_record_*`/`user_03` rows but no `analytics_9406`. The object-storage browser shows filenames without customer-owner columns; the deleted-account reference shows `user_17` but no full account resource ID. These examples explain why OCR, Vision, and table/schema ownership are combined instead of promoting every visible mention to a fact.

## What is cached

- Every non-image source is re-read for a content hash. The parsed, identity-filtered evidence is cached under `code/.cache/evidence/` using file bytes, identity bundle, audit cutoff and extractor fingerprint. A changed file, person, cutoff or parser code misses the cache.
- Image OCR is cached by image bytes and OCR implementation. Vision responses are cached by prompt, model, temperature, image bytes, detail level and strict schema. Cache hits skip API calls; they do not replace the source manifest.
- Scanned PDF page PNGs are locally cached by PDF content hash and page number. All `.cache` data are excluded from the submission archive.

## Agent supervision and anti-hallucination boundaries

`gpt-4o-mini` performs the visual/semantic proposals and chooses source-inspection tools on anomalous evidence. Its read-only audit loop is capped at two rounds and can inspect only a manifest-listed JSON, SQL, log/TXT, PDF, or image file through the matching local tool. Wrong paths/tools are rejected; malformed plans fall back to a real local inspection. Tool results are written to per-case diagnostics, not converted directly into deletion facts.

Vision requests use server-enforced strict JSON Schema. The API adapter has up to three transport/JSON attempts (configured by `OPENAI_MAX_RETRIES`, capped at five); a malformed/invalid image transcript gets a separate corrective pass, and the focused image fallback is also bounded. A model row must contain literal full resource and owner IDs in its visible excerpt. When OCR reads the image, both IDs must also occur in OCR; with empty OCR, an independent second Vision reading must agree on the pair. This reduces hallucinated joins but can omit genuine faint text, which is logged rather than guessed.

The state/policy/step phases remain deterministic over admitted facts. An email in a note, a filter value, a shared file, a numeric suffix, or a nearby timestamp is **not** sufficient ownership. If one file fails to parse, other files still produce facts; the failed file is named, and a CLI run with any case error exits nonzero. The structural validator separately checks row shape and ordering. The sample gold comparison and hard 85% dual gate are recorded in `phase17_validation.md`; structural validity alone does not imply exact gold steps.
