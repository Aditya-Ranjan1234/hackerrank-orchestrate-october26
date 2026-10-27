# Structured-log boolean regression

The workflow affiliation change was followed by a full 518-case run and a comparison against the saved pre-iteration output. Twenty-three cases gained account verification checks through the new bounded affiliation rule. Four **other** cases changed their plan without an account derivation: `case_233`, `case_292`, `case_324`, and `case_463`. Their `data_flow_*` resource switched between a record deletion plan and an active-flow disable plan, even though the source readback said `enabled=false`.

## First failed link

The structured log handler parsed `enabled=false` and `restore_allowed=false` as the strings `"false"`. `reconstructor.py` checks for the Boolean values `is False` / `is True` before attaching `connector_disabled_by_evidence` or restore-access notes. The absent connector note sent a `PRESENT` integration resource into `PolicyEngine`'s model-only flow-versus-record classifier. A model type suggestion could then be treated as an **ACTIVE** flow without an active-state observation. The source log already had the stronger fact, so the model should not make this decision.

Source examples are `evidence_79` for `data_flow_6754`, `evidence_76` for `data_flow_5598`, `evidence_73` for `data_flow_4769`, and `evidence_44` for `data_flow_8024`. The original lines carry `connector_config_read_completed` or `connector_config_loaded`, a full resource ID and `enabled=false`; their owners are resolved through exact structured identifiers. The files are listed in `dataset/evidence_files.csv`.

## Change and focused verification

`log_handler._fields` now converts only exact textual `true`/`false` values for `enabled` and `restore_allowed` into Booleans. JSON Boolean values remain unchanged; unexpected words remain text. The extractor fingerprint includes the handler source, so the evidence disk cache is invalidated automatically for log and text files when this parser changes. The new `test_log_boolean_fields.py` first failed all four tests against the old parser and then passed after the fix. It tests quoted and escaped flags, enabled/disabled flows, and both allowed and blocked restores, with a fake model that fails if an explicit connector flag is sent to model classification.

The direct four-case replay after the fix produced `VERIFY_DATA_FLOW_DISABLED` for each relevant connector and zero pipeline errors. `case_324` became COMPLETE because the false active-flow finding was its only recorded violation. The public 32-case replay remained **32/32 statuses and 13/32 exact arrays**, with zero row changes against the previous sample candidate. This is a source-format repair, not a sample-specific operation override.
