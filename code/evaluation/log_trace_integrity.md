# Structured log trace integrity

Source-only check of all manifest-listed `.log` files against current and historical exact identifiers. It does not read `sample_output.csv` or a prior agent output. A trace with multiple canonical people, an owner signal only after a resource line, or an identifier seen only in unstructured text is flagged. Ownerless resource lines are held apart; a trace ID alone is not an owner.

| Measure | Count |
|---|---:|
| conflicting_trace_owners | 0 |
| identity_only_in_unstructured_text | 0 |
| log_files | 26 |
| resource_lines | 686 |
| resource_lines_with_only_later_owner_signal | 0 |
| resource_lines_without_owner_signal | 71 |
| trace_groups | 421 |
| traces_with_known_identity | 380 |

Integrity issues: 0.

This is a source-integrity screen. It does not prove that every structured query refers to a stored record; the evidence handler and state reconstruction apply their own event and time rules.
