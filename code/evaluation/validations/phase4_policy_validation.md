# Phase 4 — Policy Engine Validation

## Rule coverage matrix

| Rule | Category/action | Targets applied | Conflicts won |
|---|---|---:|---:|
| rule_01 | USER_PROFILE → DELETE | synthetic account | tested |
| rule_02 | SECONDARY_IDENTIFIER → DELETE | category alias | tested |
| rule_03 | SEARCH_INDEX_ENTRY → DELETE | search_index | tested |
| rule_04 | CACHE_ENTRY → DELETE | cache | tested |
| rule_05 | SUPPORT_MESSAGE → REDACT | support_tickets | tested |
| rule_06 | SUPPORT_ATTACHMENT → DELETE | support_attachment | tested |
| rule_07 | ANALYTICS_PROFILE → ANONYMIZE | analytics_export | tested |
| rule_08 | PRODUCT_TELEMETRY → ANONYMIZE | product_telemetry | tested |
| rule_09 | USER_EXPORT → DELETE | user_export | tested |
| rule_10 | MARKETING_PROFILE → DELETE | marketing_profile | tested |
| rule_11 | EMAIL_DELIVERY_LOG → REDACT | logs | tested |
| rule_12 | SECURITY_AUDIT_LOG → RETAIN | logs | tested |
| rule_13 | LEGAL_HOLD_RECORD → RETAIN | legal_hold | tested |
| rule_14 | BACKUP_ARCHIVE → RETAIN | backup_snapshot | tested |
| rule_15 | ACCOUNT_TOMBSTONE → REDACT | account_tombstone | tested |

The supplied CSV has no optional priority/system/retention columns; loader
defaults are deterministic and preserve the raw condition in `notes`.

## Conflict resolution log

Tests exercise tombstone specificity, system-specific precedence, strictest
treatment, explicit priority, shorter RETAIN expiry, and deterministic rule-id
ordering. Every multi-rule resolution records a precedence note.

## Compliance summary

Synthetic policy tests cover both compliant and non-compliant verdicts. Record
compliance is based on the required treatment and current state; flow and
restore verdicts use their explicit active/risk state.

## Fail-closed coverage

An unmapped category produces `DELETE_RECORD`, `is_in_compliance` only when the
current state is `ABSENT`, and the note
`no_matching_rule_fail_closed_to_delete`.

## Tombstone handling

An account tombstone always retains `user_id`, but `email_hash` remains a direct
identifier. A lingering hash produces `REDACT_RECORD`, the hash in
`pii_fields_to_redact`, and non-compliance. A fully redacted tombstone is
compliant and still emits a REDACT verdict.

## Retention expiry

A RETAIN rule with zero days upgrades to `DELETE_RECORD` at any later audit time
and records `retention_expired_upgraded_to_delete`. Equality at the requested
time is treated as expired by the evaluator.

## Failures found and fixes applied

- Added category aliases from the participant-facing rule names to the policy
  engine's system categories.
- Added compatibility for the actual four-column rules CSV while supporting
  optional metadata through dataclass defaults.
- Added explicit tombstone and fail-closed paths.

## Token usage

No LLM calls. Input tokens: 0. Output tokens: 0. Estimated cost: $0.00.

## Open questions for Phase 5

- How should an absent RETAIN record be represented in the allowed finding
  operations? The policy verdict marks it non-compliant; Phase 5 should emit a
  retention violation finding or verification plan consistent with samples.
- Confirm category aliases against all evidence-derived system/resource pairs.
- Decide whether `RETAIN` should become a verification-only action when already
  compliant.
