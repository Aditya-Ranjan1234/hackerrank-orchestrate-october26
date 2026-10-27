# Phase 6 — Step Generator Validation

## Mapping coverage matrix

| Trigger/verdict | Finding | Remediation | Verification |
|---|---|---|---|
| REMAINING_RECORD | REPORT_REMAINING_RECORD | DELETE_RECORD | VERIFY_RECORD_ABSENT |
| EXPOSED_PII / REDACT | REPORT_EXPOSED_PII | REDACT_RECORD | VERIFY_RECORD_REDACTED |
| EXPOSED_PII / ANONYMIZE | REPORT_EXPOSED_PII | ANONYMIZE_RECORD | VERIFY_RECORD_ANONYMIZED |
| ANONYMIZATION_INCOMPLETE | REPORT_EXPOSED_PII | ANONYMIZE_RECORD | VERIFY_RECORD_ANONYMIZED |
| ACTIVE_DATA_FLOW | REPORT_ACTIVE_DATA_FLOW | DISABLE_DATA_FLOW | VERIFY_DATA_FLOW_DISABLED |
| RESTORE_RISK | REPORT_RESTORE_RISK | BLOCK_RESTORE | VERIFY_RESTORE_BLOCKED |
| RETENTION_VIOLATED | none | none | VERIFY_RECORD_PRESENT |

## Ordering verification

Steps sort by phase, operation order, system ID, and resource ID. Operation
numbers intentionally use gaps: 0–3, 10–14, and 20–25. Step numbers are then
renumbered consecutively.

## Evidence ID rules

COMPLETE verifications and INCOMPLETE findings require non-empty evidence IDs.
INCOMPLETE remediation and verification steps use empty evidence IDs. Missing
required evidence is rejected by the builder.

## JSON validity

Serializer output uses compact separators and round-trips through `json.loads`.
NOT_APPLICABLE produces exactly `[]`.

## Edge-case results

G1 duplicate handling; G2/G16 exact empty array; G3 empty COMPLETE; G4
retention-only verification; G5 mixed triggers; G6 compliant deduplication; G7
consecutive numbering; G8 deterministic JSON; G9 evidence rules; G10 JSON
round-trip; G11 remediation/verification pairing; G12 compliant coverage; G13
NONE skipped; G14 stable sorting; G15 large arrays; G17 compact separators; G18
operation/state rejection are covered by the Phase 6 tests or builder checks.

## RETENTION_VIOLATED gap

There is no allowed operation for a record that should be retained or redacted
but is absent. The generator emits only `VERIFY_RECORD_PRESENT` with empty
evidence. Phase 7 should confirm this against `sample_output.csv`.

## Failures found and fixes applied

The initial run revealed that `StepSortKey` needed ordered comparisons. Adding
`order=True` made the prescribed deterministic sort key executable. No upstream
files were changed.

## Token usage

No LLM calls. Input tokens: 0. Output tokens: 0. Estimated cost: $0.00.

## Open questions for Phase 7

- Confirm 518 output rows and case-ID sorting.
- Confirm CSV writer escaping for compact JSON.
- Confirm NOT_APPLICABLE rows serialize as `<case_id>,NOT_APPLICABLE,[]`.
