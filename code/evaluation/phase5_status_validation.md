# Phase 5 — Status Determinator Validation

## Gate coverage matrix

| Gate | Cases | Statuses/triggers | Pass |
|---|---|---|---|
| not_applicable_gate | S4, S6, S8, S11 | NO_USER_ID, NOT_A_DELETION_REQUEST, AUDIT_BEFORE_REQUEST | PASS |
| incomplete_triggers | S1–S3, S12–S14, S17 | flow, restore, PII, retention, remaining record | PASS |
| complete_gate | S5, S7, S9, S15, S18 | COMPLETE and boundary behavior | PASS |

## Edge-case results

S1 ACTIVE_DATA_FLOW; S2 RESTORE_RISK; S3 EXPOSED_PII; S4 NO_USER_ID;
S5 COMPLETE despite PARTIALLY_COMPLETE claim; S6 NOT_A_DELETION_REQUEST;
S7 COMPLETE with retention language; S8 AUDIT_BEFORE_REQUEST; S9 equal-time
boundary proceeds; S10 offending record produces INCOMPLETE; S11 empty text
defaults to deletion; S12 NONE flow does not trigger; S13 RETENTION_VIOLATED;
S14 REDACT/ABSENT becomes RETENTION_VIOLATED; S15 COMPLETE; S16 deterministic
with fixed clock; S17 reported COMPLETE does not hide failure; S18 deletion wins
over export ambiguity.

## NOT_APPLICABLE breakdown

Synthetic coverage includes one case each for `NO_USER_ID`,
`NOT_A_DELETION_REQUEST`, and `AUDIT_BEFORE_REQUEST`. Empty request text is
treated as deletion intent and does not produce NOT_APPLICABLE.

## INCOMPLETE breakdown

Covered trigger kinds: `ACTIVE_DATA_FLOW`, `RESTORE_RISK`, `EXPOSED_PII`,
`REMAINING_RECORD`, `RETENTION_VIOLATED`, and `ANONYMIZATION_INCOMPLETE` via
the trigger mapper. Trigger output is sorted by target kind, system, resource.

## reported_status independence

S5 and S17 vary `reported_status` while holding evidence-backed verdicts fixed.
The resulting status follows policy verdicts only; reported workflow status is
never read by the determinator.

## Determinism

The fixed-clock determinism test produces byte-equivalent StatusDecision values.
The full suite was rerun after the final gate cleanup.

## Failures found and fixes applied

- Corrected a test fixture argument ordering for the NO_USER_ID case.
- Simplified `complete_gate` to explicitly reject NOT_APPLICABLE conditions.

## Token usage

No LLM calls. Input tokens: 0. Output tokens: 0. Estimated cost: $0.00.

## Open questions for Phase 6

- Confirm how Phase 6 should render over-deleted REDACT/ABSENT verdicts.
- Confirm whether a RETAIN-compliant record receives only VERIFY_RECORD_PRESENT.
- NOT_APPLICABLE output must use the exact empty JSON array `[]`.
