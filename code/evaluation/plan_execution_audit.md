# Full output plan execution audit

Evaluation only. This source-backed replay checks all generated plans against their recorded policy obligations, simulates the listed remediation operations, and checks whether each final verification can pass. It does not read sample answers or hidden labels. It cannot certify undiscovered records or predict the HackerRank score.

Output: `output.csv`; cases: 518; policy verdicts: 1588; steps: 2894.
Cases with plan errors: 0; with warnings: 2.

## Error categories

| category | occurrences |
|---|---:|

## Warning categories

| category | occurrences |
|---|---:|
| complete_without_any_policy_obligation | 1 |
| complete_without_evidence_backed_verification | 1 |
| citation_lacks_directly_owned_extracted_record | 1 |

## Affected cases

| case | status | verdicts | steps | errors | warnings |
|---|---|---:|---:|---|---|
| case_63 | COMPLETE | 0 | 0 | — | complete_without_any_policy_obligation; complete_without_evidence_backed_verification |
| case_430 | COMPLETE | 2 | 2 | — | citation_lacks_directly_owned_extracted_record:evidence_68:account_6006 |
