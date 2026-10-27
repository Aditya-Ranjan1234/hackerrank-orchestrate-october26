# Source-only workflow affiliation calibration

This probe does not read `sample_output.csv`, `output.csv`, or a cached answer. Ownership labels come from exact current/historical identifiers in the supplied evidence. A unique timestamp candidate is a correlation, not proof of deletion state.

Directly owned account IDs across all manifest formats: 250.

| Delay before report | Candidate/outcome rule | Unique request windows | Independently owned | Correct owner | Other owner | Unresolved |
|---|---|---:|---:|---:|---:|---:|
| 0–5 min | all actions | 60 | 25 | 0 | 25 | 35 |
| 0–5 min | all actions; winner SUCCESS | 36 | 17 | 0 | 17 | 19 |
| 0–5 min | SUCCESS prefilter (rejected) | 36 | 17 | 0 | 17 | 19 |
| 20–100 min | all actions | 57 | 26 | 26 | 0 | 31 |
| 20–100 min | all actions; winner SUCCESS | 25 | 14 | 14 | 0 | 11 |
| 30–90 min | all actions | 57 | 26 | 26 | 0 | 31 |
| 30–90 min | all actions; winner SUCCESS | 25 | 14 | 14 | 0 | 11 |
| 30–90 min | SUCCESS prefilter (rejected) | 219 | 90 | 42 | 48 | 129 |
| 40–80 min | all actions | 57 | 26 | 26 | 0 | 31 |
| 40–80 min | all actions; winner SUCCESS | 25 | 14 | 14 | 0 | 11 |
| 45–75 min | all actions | 58 | 27 | 26 | 1 | 31 |
| 45–75 min | all actions; winner SUCCESS | 26 | 14 | 14 | 0 | 12 |

## Masked-owner control

A stable five-fold hash split hides one fifth of exact account-owner links at a time. The production eligibility and ambiguity gates are replayed against the reduced index. Known held-out links are then checked against their original source owners; truly ownerless candidates remain unscored.

| Fold | Derived | Known correct | Known wrong | Unresolved |
|---:|---:|---:|---:|---:|
| 0 | 37 | 16 | 0 | 21 |
| 1 | 32 | 12 | 0 | 20 |
| 2 | 32 | 12 | 0 | 20 |
| 3 | 31 | 12 | 0 | 19 |
| 4 | 31 | 11 | 0 | 20 |
| **Total** | **163** | **63** | **0** | **100** |

## Public sample request inputs: unresolved unique candidates

The public sample *requests* are used only to count source-side candidates. This is not a score against answers.

| Case | Activity | Account | Delay before report |
|---|---|---|---:|
| case_30 | activity_3465 | account_4163 | 64.3 min |

The production affiliator also vetoes directly owned accounts, competing eligible requesters and any account whose exact owner is another person. The source-only table therefore measures the timing signal before those extra gates.
