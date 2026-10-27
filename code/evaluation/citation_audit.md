# Output citation source audit

Checks the generated `output.csv` against the evidence manifest, activity IDs and identity audit IDs. It never opens `sample_output.csv`. For an evidence-file citation, the complete resource ID must be visible in that file's text, PDF extraction or local image OCR, or an exact visible artifact alias must be independently linked by a pre-audit catalog activity with compatible ownership. Generated log-line handles are accepted only when the cited line exists and contains an exact identifier for the case. Image OCR gaps can be false negatives and require visual review.
A separate count identifies citations to files captured after audit_at. Such files may contain older timestamped observations; their capture date alone does not tell whether the cited row reflects audit-time state. Review this count when applying the repository's evidence cutoff rule.

| Measure | Count |
|---|---:|
| cited_steps | 1010 |
| evidence_file_citations | 1010 |
| retrospectively_captured_file_citations | 23 |
| source_files_opened | 71 |
| verified_catalog_alias_citations | 3 |

Potential citation issues: 0.

| case | citation | resource | issue |
|---|---|---|---|
