# Post-Phase 7 Fix Iteration — Phase 2 Matching

## Diagnosis

The original 8 sample status mismatches were predominantly Gold COMPLETE versus
our INCOMPLETE, confirming phantom records. A first cache-boundary fix improved
the sample to 75% (24/32). The stricter JSON/log allowlist implementation was
then tested against the full suite and the sample; it preserved 121 passing
tests but reduced sample status accuracy to 50%.

## Changes made

- JSON extraction now limits matching to explicit PII field names and exact
  identity values.
- Log extraction now requires a structured component tag and allowlisted
  key/value identifiers.
- The orchestrator clears identity-filtered Phase 2 cache data at case
  boundaries to prevent cross-case leakage.

## Result and decision

The unit contract remains green (`121 passed`), but the end-to-end target is not
met. The remaining issue is broader than free-text JSON/log matching: the state
reconstructor and evidence-to-resource mapping still need a participant-data
aware resource/category join. This iteration is therefore documented as a
regression requiring further investigation, not accepted as a quality gain.

## Submission impact

`output.csv` was regenerated with 518 rows and passes structural validation.
The sample accuracy limitation is recorded in `evaluation_report.md` and
README.md. No LLM calls were used.
