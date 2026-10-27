# Phase 9 Inference Validation

## 1. Inference method coverage

| method | count derived | percentage |
|---|---:|---:|
| resource_id_match | 0 in the 518-case diagnostic run | 0% |
| system_time_proximity | 0 in the 518-case diagnostic run | 0% |

The synthetic unit suite exercises both methods; the production evidence records do not expose matching resource/system tuples for the affected cases under the audit cutoff.

## 2. Per-case recovery trace

No sample status mismatches were recovered by the expander. The before/after score remained 22/32 (68.75%). `code/orchestrator/debug_case.py` prints the derived-activity section for case-level investigation.

## 3. Derived-activity summary

The original activity CSV contains 4011 rows (the exact count is dataset-dependent at runtime). The full run added 0 derived rows, so the observed derivation rate was 0%. Unit fixtures confirm deterministic derivation and precedence.

## 4. Sample accuracy progression

- Phase 7 baseline: 24/32 (75%)
- Phase 8 failed fix: 16/32 (50%)
- Phase 8 recovery: 22/32 (68.75%)
- Phase 9: 22/32 (68.75%)

The 85% target was not reached.

## 5. Remaining mismatches

The remaining mismatches are not caused by double derivation. They arise because evidence rows and activity rows use different system/resource identifiers, so neither permitted inference signal is present. Fixing those cases would require a schema-level join or a Phase 3 policy change outside this task's scope.

## 6. Token usage

Phase 9 used 0 LLM calls, 0 input tokens, and 0 output tokens.

## 7. Open questions

- Should the ±24-hour window be tuned once a reliable system/resource join exists?
- Could proximity inference over-derive records and create phantom incomplete results?
- The sample remains below 85%; a Phase 10 dataset-join investigation is recommended before submission.
