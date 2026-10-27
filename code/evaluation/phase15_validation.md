# Phase 15 closure validation

## 1. Stale tests and release gate

The prompt mislocated the obsolete proximity assertion. It is in frozen `code/tests/test_case03_regression.py:17-23`, not in the permitted `test_activity_expander.py`. The permitted file already tests the required opposite behavior (`test_p14_e1_no_unowned_same_system`, `test_p14_e7_no_method2_even_zero_window`, plus the new identical-time guard). Editing the frozen test or restoring Method 2 would violate the explicit scope and the Phase 13 provenance audit. The hard exact-step gate remains in place and fails as intended. Final pytest: **221 passed, 2 failed** (the hard gate and the frozen obsolete assertion); the eight new tests pass. It would be inaccurate to claim both failures resolved.

## 2. Post-Phase-14 step diff

Baseline: `SYSTEM_ID_MISMATCH` **116/539 (21.52%)** by position, with **0/32** exact arrays. After Phase 15: same nominal type **108/469 (23.03%)**, but semantic alignment finds **76 missing** and **87 extra** step identities plus **23 citation differences**. Insertion/removal of a step shifts later positions, so the positional system-ID count is not evidence of 108 independently wrong systems. See `step_diff_report.md` §1–3.

## 3. Fixes applied

- `json_handler.py`: inherit a visible parent resource ID for an ID-less nested JSON document; an explicit child ID still wins. Case_29's phantom JSON-path resource and three steps disappear.
- `steps/builder.py`: in an INCOMPLETE case, also append deduplicated verifications for compliant verdicts, with empty evidence citations. No new finding/remediation is invented.
- `orchestrator/step_diff.py`: report position-independent missing/extra/citation counts and regenerate the *current* 32-case sample on a no-argument call; the old CLI default silently used a Phase 12 snapshot. This is diagnostic only.

## 4. Iteration results

| Iteration | Sample status | Exact step arrays | Tests |
|---|---:|---:|---|
| 14 baseline | 32/32 | 0/32 | 213 pass, 2 fail |
| 15a: nested JSON ID | 32/32 | 0/32 | 2 new focused tests pass |
| 15b: mixed-case verification | 32/32 | 1/32 | 217 pass, 2 fail |
| 15c: semantic diagnostics | 32/32 | 1/32 | 221 pass, 2 fail |

Phase 15a reduced positional system-ID mismatches from 116 to 97. Phase 15b raised matching step counts from 1/32 to 7/32 and exact arrays to 1/32. The positional system-ID count then rose to 108 because newly inserted verification steps shifted the index comparison; semantic analysis is the correct interpretation.

## 5. Per-case gold comparison

All listed statuses match gold. M/E/C are counts of missing semantic step identities, extra semantic step identities, and citation differences on otherwise matching identities; step numbers and order are checked separately for exact match.

| Case | Status match | Exact steps | M | E | C |
|---|---|---|---:|---:|---:|
| case_01 | yes | no | 1 | 0 | 0 |
| case_02 | yes | no | 1 | 0 | 0 |
| case_03 | yes | no | 1 | 0 | 0 |
| case_04 | yes | no | 2 | 0 | 0 |
| case_05 | yes | no | 2 | 6 | 0 |
| case_06 | yes | no | 3 | 3 | 0 |
| case_07 | yes | no | 4 | 3 | 0 |
| case_08 | yes | no | 3 | 3 | 0 |
| case_09 | yes | no | 5 | 4 | 0 |
| case_10 | yes | no | 4 | 5 | 0 |
| case_11 | yes | no | 3 | 3 | 0 |
| case_12 | yes | no | 3 | 3 | 0 |
| case_13 | yes | no | 3 | 3 | 0 |
| case_14 | yes | **yes** | 0 | 0 | 0 |
| case_15 | yes | no | 3 | 9 | 0 |
| case_16 | yes | no | 5 | 9 | 0 |
| case_17 | yes | no | 3 | 9 | 0 |
| case_18 | yes | no | 5 | 3 | 0 |
| case_19 | yes | no | 0 | 9 | 0 |
| case_20 | yes | no | 5 | 3 | 0 |
| case_21 | yes | no | 2 | 0 | 1 |
| case_22 | yes | no | 6 | 6 | 0 |
| case_23 | yes | no | 1 | 0 | 1 |
| case_24 | yes | no | 0 | 6 | 2 |
| case_25 | yes | no | 2 | 0 | 1 |
| case_26 | yes | no | 1 | 0 | 4 |
| case_27 | yes | no | 2 | 0 | 4 |
| case_28 | yes | no | 2 | 0 | 4 |
| case_29 | yes | no | 1 | 0 | 3 |
| case_30 | yes | no | 1 | 0 | 3 |
| case_31 | yes | no | 1 | 0 | 0 |
| case_32 | yes | no | 1 | 0 | 0 |

## 6. Regression check

Cases 02, 03, 04 retain gold-correct status. The Phase 12 recovery set (08–16, 18–20, 22) also retains gold-correct status. Their exact arrays are *not* all correct; see §5. No status regression occurred during Phase 15. The two frozen-method tests remain reported in §1.

## 7. Token usage

Application LLM/VLM calls: **0**. Input tokens: **0**. Output tokens: **0**. All new logic and tests are deterministic Python.

## 8. Ship readiness

**NOT_READY.** The status gate passes (32/32), but the exact-step gate is only **1/32**, below 28/32. The hard-gate test continues to fail. The frozen obsolete proximity test is a separate scope conflict. A 518-row structural check, determinism check, and archive check are recorded below after final execution; they cannot override the exact-step failure.

## 9. Residual step gaps — per-case root-cause audit

The descriptions below are based on the current position-independent diff and per-case diagnostic traces in `code/.cache/diagnostics/`; the cited gold-only tuple is a diagnostic, not authority to invent missing ownership. The five independently checked no-join cases (01, 02, 03, 04, 31) cap strict exact-array coverage at **27/32**, below the 28/32 gate, even if every other case were repaired. The source-level no-join audit is in `phase14_validation.md` §9. A higher score requires externally corroborated identity-to-resource linkage or an explicitly authorized relaxation of the ownership invariant; neither is available in this phase.

- **01:** Gold verifies `account_001`; the supplied account evidence/activity does not directly bind that full ID to this identity. The agent therefore emits no account fact.
- **02:** Gold verifies `account_002`; as in 01, direct user ownership is absent. Numeric suffix correlation is not admissible evidence.
- **03:** Gold additionally verifies anonymous `analytics_9406`; its user fields are null. Current two steps match semantically, but the third would require an unsupported join.
- **04:** Gold verifies `account_004` and `analytics_901`; the account ID lacks a direct identity-owned evidence row at audit time. The analytics gap needs separate extraction/provenance review, but the missing account verification alone blocks exact match.
- **05:** The agent attributes `account_005` to `account_failover_replica` and `sql` instead of gold's `account_service`, producing duplicate finding/remediation tuples. A generic failover-table/system mapping needs more provenance than this single case.
- **06:** `search_001` is emitted under generic `sql` rather than `search_service`; the gold finding/remediation/verification triple uses the latter. This traces to SQL table-system attribution.
- **07:** The agent finds `object_19` in `object_storage`, while gold expects `support_001` in `support_platform`. These are different resources, so a simple system rename would be incorrect.
- **08:** The resource `export_001` is found, but generic JSON fallback labels it `json` rather than `export_service`. A file/content-level system signal is needed.
- **09:** The backup `backup_4978` is treated as a generic SQL record to delete, whereas gold treats it as a restore risk requiring BLOCK_RESTORE. The table/system and literal restore-allowed flag need a grounded policy path.
- **10:** A support-replica line identifier (`evidence_61_line_4`) competes with gold's `support_002` resource. This is a log resource-ID extraction issue, not an ordering fix.
- **11:** The exact `data_flow_9522` resource is found, but classified as a remaining record rather than active data flow; the policy lacks a flow interpretation for this evidence shape.
- **12:** An `evidence_01_line_73` account-log resource is extra while gold expects `analytics_9914`. The resource mismatch spans extraction and policy, not step sorting.
- **13:** `support_4218` is present in both, but the agent requests redaction while gold requests outright deletion. The treatment/category distinction must be resolved from the applicable evidence and rule.
- **14:** Exact array matches gold; no residual step gap.
- **15:** `data_flow_9846` is classified as a record to delete rather than an active flow; additional line-level resources inflate the array. Generic suppression would hide evidence without fixing classification.
- **16:** `account_994` is duplicated under `account_replication_cluster` and `sql`; the gold account/search resource systems are missing. The cross-table provenance and deduplication need a scoped SQL repair.
- **17:** The agent emits an account-log line and tombstone finding, while gold expects a backup restore-risk triple. This requires source-state and policy reconciliation.
- **18:** `data_flow_4890` is present but treated as a deletable record, not an active flow; another gold tuple is also absent. The same flow-shape gap appears in 11/15/20.
- **19:** All eight gold identities are present, but nine extra line-level/security/resource steps remain. Removing them wholesale would risk suppressing legitimate evidence in other cases.
- **20:** `data_flow_1770` is classified as record deletion instead of DISABLE_DATA_FLOW; other gold tuples are absent. Flow semantics, not phase ordering, dominate.
- **21:** Gold has account/analytics verifications lacking a direct audit-time ownership link; one shared step cites a different evidence file. This combines missing facts and citation selection.
- **22:** Gold's analytics/search tuples are emitted under generic `sql` with record-deletion policy, not the expected system/treatment. Six gold tuples are missing and six alternatives are extra.
- **23:** Gold verifies `account_410`; the agent has no proved account fact. The shared search finding cites an older/different file than gold.
- **24:** The agent adds six replication/flow steps absent from gold, although all gold structural identities are present. Two shared steps cite a different evidence file. A blanket filter would be unsupported.
- **25:** Gold requires `account_3136` and `analytics_1895` verifications; those anonymous readbacks lack direct ownership. One shared step has an evidence-ID difference.
- **26:** The only missing identity is anonymous `analytics_4566`; four shared verification citations differ (`evidence_02` snapshot versus gold's `evidence_92` readback). Both files corroborate the same states but the existing latest-evidence rule chooses the snapshot.
- **27:** Anonymous `account_3866` and `analytics_4574` are not affiliated from null-field rows; four otherwise matching citations choose `evidence_02` instead of gold's `evidence_92`.
- **28:** Anonymous `account_5482` and `analytics_6077` are not affiliated; four matching citations differ on snapshot versus readback file IDs.
- **29:** All findings/remediations now have correct structural tuples after the nested-ID fix, but gold additionally verifies ownerless `account_7012`; three findings cite `evidence_02` instead of gold's `evidence_92`.
- **30:** Gold additionally verifies ownerless `account_4163`; three shared findings have the same snapshot/readback citation difference as 29.
- **31:** Gold verifies `account_4857`, but the cited account evidence does not contain that full ID tied to the identity. Other steps match semantically.
- **32:** Gold verifies `account_8858`; the agent has no corresponding directly attributed account fact, leaving one missing verification.

### Final artifact checks

The regenerated `output.csv` has **518 rows**, **518 unique case IDs**, exact coverage of `dataset/deletion_requests.csv`, natural case-ID ordering, and parseable JSON step arrays. There were **zero per-case pipeline errors**. The existing structural validator reported **zero errors and zero warnings** (its own check counter is zero, so independent row/coverage/parse checks were also performed). SHA-256 of `output.csv`: `016bc7b17e500ddd47316e3e5fa1f3d825627e099a3227b1c034d3e8a9a006ae`. Independent gold validation: 32/32 statuses, 1/32 exact arrays, no status regressions against Phase 14. The second full run and archive rebuild are pending and will be recorded explicitly.
