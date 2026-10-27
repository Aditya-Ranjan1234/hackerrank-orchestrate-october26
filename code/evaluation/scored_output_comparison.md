# Comparison of the two scored submissions

The scores are user-reported HackerRank totals: 21.6/30 for the previous root output and 21.9/30 for the external reference. No per-case grading feedback or hidden answers were supplied. The external file was read only; byte-preserving copies of both inputs are in `artifacts/csv/scored_21_6_root.csv` and `artifacts/csv/scored_21_9_reference.csv`.

The external file starts with a non-CSV title line, `output-AR copy`. Analysis removed that line in a separate `scored_21_9_normalized.csv`; the original was not rewritten. The normalized content has the required header and 518 cases. It is unknown whether the extra title line was present in the file actually submitted to HackerRank.

Exactly **six rows differ**; the other **512 are semantically identical**, including ordered step arrays.

| Case | Root 21.6 status / steps | Reference 21.9 status / steps |
|---|---|---|
| case_54 | NOT_APPLICABLE / 0 | INCOMPLETE / 10 |
| case_93 | NOT_APPLICABLE / 0 | INCOMPLETE / 12 |
| case_132 | NOT_APPLICABLE / 0 | INCOMPLETE / 7 |
| case_171 | NOT_APPLICABLE / 0 | INCOMPLETE / 3 |
| case_210 | NOT_APPLICABLE / 0 | INCOMPLETE / 7 |
| case_249 | NOT_APPLICABLE / 0 | INCOMPLETE / 12 |

All six requests explicitly ask in Portuguese for permanent account deletion. The previous classifier missed `exclusão` while treating the follow-up request to verify identifiers as a non-deletion intent. The same request wording occurs in fourteen full-input cases; the correction is applied to all fourteen, not just the six externally changed rows. The reference adds 51 steps across its six changed rows. Its remaining cases preserve all other root-output weaknesses, so the 21.9 file is not a source of correct labels for the other 512 cases.

The root output had 136 COMPLETE, 366 INCOMPLETE, and 16 NOT_APPLICABLE cases, with 2,798 steps. The normalized reference had 136 COMPLETE, 372 INCOMPLETE, and 10 NOT_APPLICABLE cases, with 2,849 steps. Both parsed files pass the structural validator; this does not establish semantic correctness.

SHA-256 of the scored root snapshot: `D7D0038F725481EF0D0B4F8F95C1B49BC32FC8B09C3D7B5C00DA151AA03E303B`.

SHA-256 of the external source bytes: `8C30AAD04C93BED7A989F8196B79709232ABB0458748459803EF1414C0BF6A4F`.

The subsequent review used the participant sources, not either submission as a label oracle. The corrected rows and their exact before/after steps are documented in `changed_rows.md` and `artifacts/csv/changed_rows.csv`. A new hidden score cannot be measured locally.
