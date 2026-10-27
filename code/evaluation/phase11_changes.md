# Phase 11 change record

The [Phase 10 grounding report](dataset_grounding_report.md) and [mismatch triage](mismatch_triage_report.md#grounded-root-cause-review) are the source for these changes. Expected status effects below are hypotheses from the kickoff; actual effects are from the 32-case rerun.

## Change 1: Remove numeric-suffix resource ownership

- **Fix ID:** A
- **File:** `code/agent/state/reconstructor.py:11-15`; audit in [phase11_suffix_inference_audit.md](phase11_suffix_inference_audit.md)
- **Grounded in:** [mismatch triage, cases 02, 03, 04, 21, 25, 28, 31](mismatch_triage_report.md#grounded-root-cause-review); [activity schema](dataset_grounding_report.md#system_activitycsv)
- **Problem:** `user_25` was affiliated with unrelated `audit_record_2025` solely because both ended in `025`. Activity has no `target_user_id` column.
- **Change:** Activity ownership now requires an explicit user reference or a bounded literal mention in the activity details. The expander's `_norm` was audited and already strict, so its ownership normalization needed no change.
- **Before:**
  ```python
  suffixes = {str(x).split("_")[-1].zfill(3) for x in ids}
  return any(rid.endswith(suffix) for suffix in suffixes)
  ```
- **After:**
  ```python
  if explicit: return explicit in ids
  return any(x and re.search(rf"(?<![\w@.-]){re.escape(x)}(?![\w@.-])", text, re.I) for x in ids)
  ```
- **Tests added:** `test_no_suffix_inference_in_reconstructor`, `test_no_suffix_inference_in_expander`, `test_strict_user_id_match_still_works`, `test_strict_email_match_still_works`.
- **Expected impact:** Seven phantom-resource mismatches should recover.
- **Verification:** Cases 02, 03, 04 recovered. Cases 21, 25, 28, 31 still have other extra facts. Twelve previously correct INCOMPLETE cases lost their only facts, so net sample accuracy fell.

## Change 2: Parse JSON snapshot timestamps

- **Fix ID:** B.1
- **File:** `code/agent/evidence/handlers/json_handler.py:7-28,44-56,78-79`
- **Grounded in:** [mismatch triage, cases 26 and 27](mismatch_triage_report.md#grounded-root-cause-review); [evidence_02 inventory](dataset_grounding_report.md#evidence-file-inventory)
- **Problem:** JSON facts used `evidence_timestamp=None`, so a September 17 snapshot could affect a September 15 audit, and older snapshots were not ordered correctly.
- **Change:** Parse priority fields and nested `captured_at` values into UTC timestamps. A pre-audit file mtime is used only when `audit_at` is supplied. Preserve `None` when no source time is established.
- **Before:**
  ```python
  out.append(RecordState("json", rid, user, state, hits, None, node))
  ```
- **After:**
  ```python
  ts = _own_timestamp(node) or inherited_ts
  record_ts = ts or (_timestamp(activity_time_lookup(rid)) if activity_time_lookup else None)
  out.append(RecordState(system, rid, user, state, hits, record_ts, node, source))
  ```
- **Tests added:** `test_json_handler_extracts_snapshot_at_field`, `test_json_handler_falls_back_to_mtime_when_pre_audit`, `test_json_handler_rejects_post_audit_mtime`, `test_nested_capture_time_overrides_file_export`.
- **Expected impact:** Old and post-audit snapshots for cases 26 and 27 should be ordered/excluded.
- **Verification:** Unit tests pass. Both cases remain INCOMPLETE in the full pipeline due additional facts and activity inference.

## Change 3: Attribute JSON records to their visible system

- **Fix ID:** B.2
- **File:** `code/agent/evidence/handlers/json_handler.py:30-36,51-56,79`; `code/agent/evidence/ir.py:22`
- **Grounded in:** [cross-file join analysis](dataset_grounding_report.md#cross-file-join-analysis) and [JSON snapshot inventory](dataset_grounding_report.md#evidence-file-inventory)
- **Problem:** Every JSON fact was labelled `system_id=json`, so it did not join an account/search/backup activity sharing its full resource ID.
- **Change:** Prefer an explicit `system_id`, `system`, or enclosing snapshot `data_store`; then use a known system name in the file ID or path. Record the source in `system_id_source`.
- **Before:**
  ```python
  RecordState("json", rid, user, state, hits, None, node)
  ```
- **After:**
  ```python
  system = explicit_system or inherited_system or fallback_system
  RecordState(system, rid, user, state, hits, record_ts, node, source)
  ```
- **Tests added:** `test_json_handler_propagates_system_id_from_filename`, `test_nested_capture_time_overrides_file_export`.
- **Expected impact:** Same-resource evidence and activity could now share a `(system_id, resource_id)` key.
- **Verification:** Unit tests pass; sample score did not improve, revealing additional extraction gaps.

## Change 4: Use exact-resource activity time only when JSON has no time

- **Fix ID:** B.3
- **File:** `code/orchestrator/activity_expander.py:17-21,40-44`; `code/agent/evidence/handlers/json_handler.py:78`
- **Grounded in:** [551 exact resource-ID overlaps](dataset_grounding_report.md#cross-file-join-analysis) and [Phase 10 zero-derivation explanation](phase10_grounding_validation.md#2-hallucination-audit)
- **Problem:** The expander substituted extraction time (October) for a missing evidence timestamp, rejecting it against September audit cutoffs.
- **Change:** Look up the latest pre-audit activity for the complete resource ID. A handler callback supports this lookup in isolation; the frozen registry does not pass one, so the expander applies the fallback to extracted records before downstream phases.
- **Before:**
  ```python
  ts = rec.evidence_timestamp or getattr(ev, "extracted_at", None)
  if not ts or (cutoff and ts > cutoff): continue
  ```
- **After:**
  ```python
  ts = rec.evidence_timestamp
  if ts is None: ts = lookup_activity_time_for_resource(rec.resource_id, activity_rows, cutoff)
  if ts: rec.evidence_timestamp = ts
  ```
- **Tests added:** `test_json_handler_uses_activity_time_when_missing`, `test_handler_activity_time_callback`.
- **Expected impact:** Enable exact-resource derivations where a snapshot lacks time.
- **Verification:** Unit tests pass. The sample now generates derived activities, but proximity also creates extra facts; the fallback does not prove a later snapshot existed at the earlier activity time.

## Change 5: Recognize inflected deletion intent

- **Fix ID:** C
- **File:** `code/agent/status/request_classifier.py:4-30`
- **Grounded in:** [case_12 request text](mismatch_triage_report.md#case_12), specifically “before deleting it”
- **Problem:** The substring `delete` is absent from `deleting`; `changed` matched the non-deletion list and made case_12 NOT_APPLICABLE.
- **Change:** Replace substrings with word-boundary stem regexes, retaining empty-text deletion default and deletion-wins-ties semantics.
- **Before:**
  ```python
  deletion = any(k in t for k in DELETION_KEYWORDS)
  non = any(k in t for k in NON_DELETION_KEYWORDS)
  return not non or deletion
  ```
- **After:**
  ```python
  deletion = any(r.search(text) for r in _DELETION_REGEX)
  non = any(r.search(text) for r in _NON_DELETION_REGEX)
  return not non or deletion
  ```
- **Tests added:** Six cases in `test_request_classifier_stems.py`, including `deleting` and export-only intent.
- **Expected impact:** Case_12 should remain applicable.
- **Verification:** It now returns COMPLETE rather than NOT_APPLICABLE, but gold is INCOMPLETE; missing evidence facts remain a separate issue.
