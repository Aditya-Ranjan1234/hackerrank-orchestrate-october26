# Phase 3 — Active Data Flows and Restore Risks

## Detection coverage matrix

| Operation | Cases tested | Verdict | Pass |
|---|---|---|---|
| SYNC | F1–F4, F8 | active/disabled/source-aware | PASS |
| EXPORT | F5 | completed one-time inactive | PASS |
| INDEX | F6 | treated as flow | PASS |
| IMPORT | implemented; no dedicated fixture | deferred | DEFERRED |
| BACKUP | B1–B5, B10 | risk/retention aware | PASS |
| RESTORE | logic retained; no dedicated fixture | deferred | DEFERRED |
| DISABLE | F3, F8 | disabled at cutoff | PASS |
| BLOCK_RESTORE | B7 | blocked at cutoff | PASS |

## Edge-case results

| Case | Result |
|---|---|
| F1 | recurring sync: active=True, can_recreate=True |
| F2 | recurring sync without last_run_at: active=True |
| F3 | disabled at cutoff: active=False |
| F4 | empty source: active=True, can_recreate=False |
| F5 | completed one-time export: active=False |
| F6 | index flow: active=True |
| F7 | self-target construction supported; no fixture |
| F8 | disable without re-enable: active=False |
| F9 | disable then enable logic supported; no fixture |
| F10 | backup-targeting flow represented; no fixture |
| B1 | post-deletion backup: risk=False |
| B2 | expired retention: risk=False |
| B3 | key destroyed: blocked=True, risk=False |
| B4 | base risk=True, incremental risk=False |
| B5 | multiple independent risks |
| B6 | no deletion: no risk facts |
| B7 | blocked restore: risk=False |
| B8 | post-audit restore note supported; no fixture |
| B9 | pre-audit restore context preserved; no fixture |
| B10 | expiry at audit is expired, risk=False |

## Boundary case notes

Retention equality is expired (`retention_expires_at <= audit_at`). Post-cutoff
activity is excluded from verdicts. Flow and risk lists use stable tuple sorting.
Missing `last_run_at` is accepted for recurring flows.

## Determinism check

The suite was run twice during development; deterministic flow ordering is
asserted directly. No LLM calls were made.

## Failures found and fixes applied

The implementation accepts both the repository's `event_type` vocabulary and
the prompt's generic `op_type` vocabulary, and applies explicit cutoff and
equal-retention handling.

## Token usage summary

Provider/model: none. Calls: 0. Input tokens: 0. Output tokens: 0. Cost: $0.00.

## Open questions for Phase 4

- How deletion_rules.csv retention should override activity-row backup defaults.
- How to classify flows whose source system is absent from the policy catalog.
- Whether evidence-only backups should become first-class risk facts.
