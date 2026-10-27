# Phase 8 Recovery Validation

## 1. Regression postmortem

The Phase 7 matching tightening reduced sample status accuracy from 75% to 50%. The principal regression was that the dataset uses fields such as `customer_reference` and `ship_to_email`, while the allowlist only recognized conventional `user_id`/`email` fields. The original activity export also has no explicit `target_user_id`; it identifies operations through resource IDs and free-text details.

## 2. Recovery changes

- JSON matching now uses exact identifier values in any field, then extracts sibling PII fields when the record is tied to that identifier. Substring matching remains excluded.
- Log matching retains the required component tag and audit cutoff, while allowing exact identifier matches anywhere on the tagged line.
- Reconstruction enumerates activity-only resources, supports both actual dataset columns and generic `activity_time`/`op_type` names, applies the state machine, and overlays evidence with deterministic timestamp/file-id precedence.
- No LLM calls were made.

## 3. Validation results

| Check | Result |
|---|---|
| Existing regression suite | 121 passed |
| Pre-tightening sample | 24/32 (75.00%) |
| Tightening regression | 16/32 (50.00%) |
| Phase 8 recovery run | 22/32 (68.75%) |
| Sample output row count | 32 |

The target of 85% was not reached. Remaining mismatches are primarily cases where the activity export lacks an explicit user join and the synthetic resource naming convention does not uniquely identify the historical identity. This is documented rather than altering frozen Phase 7 orchestration or inventing evidence.

## 4. Conflict-resolution cases

The reconstructor tests cover delete, sync recreation, restore override, evidence-over-activity, activity-only records, and deterministic same-timestamp evidence selection. Post-audit evidence remains excluded from the audit-time state.

## 5. Handler coverage and cache

The prior Phase 2 handler matrix and cache validation remain valid. The phase-level suite remains green after the recovery edits. Cache behavior is content-hash based and the orchestrator clears the identity-filtered cache at case boundaries.

## 6. Token usage and open questions

Phase 8 LLM calls: 0; input tokens: 0; output tokens: 0. Open questions for Phase 9 are whether the dataset specification should expose an explicit activity-to-user key, and whether the remaining historical-resource joins belong in identity resolution or a dedicated dataset join layer.
