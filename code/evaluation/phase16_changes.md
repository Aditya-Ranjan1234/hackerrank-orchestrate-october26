# Phase 16 grounded change ledger

## Change 1: Optional OpenAI adapter, cache and per-call trace
- **Iteration:** 16a
- **Fix ID:** llm-client
- **File:** `code/agent/llm/{client,cache,tracer}.py`
- **Grounded in:** `phase15_validation.md` §9: ambiguous system/citation decisions remain after deterministic extraction.
- **Problem:** No OpenAI transport, retry/fallback, or auditable call record existed.
- **Before:** no `agent.llm` package; image handler used only an optional stub.
- **After:** a key-gated Chat Completions adapter validates JSON, retries errors and malformed output, caches by prompt/model/temperature (plus image hash), and traces each enabled invocation under excluded `.cache`.
- **Tests added:** pending mocked client/cache tests.
- **Expected impact:** Controlled, auditable semantic calls; no crash without a key.
- **Verification:** pending.
- **LLM call site:** shared adapter, `gpt-4o-mini`; actual tokens measured per response.
- **Cost impact:** only actual calls, priced from current official model pages.

## Change 2: Evidence-constrained semantic resolvers and prompts
- **Iteration:** 16a
- **Fix ID:** llm-semantic-resolver
- **File:** `code/agent/llm/semantic_resolver.py`, `code/agent/llm/prompts/*.py`
- **Grounded in:** `phase15_validation.md` §9 cases 05–13 (system/flow), 21–32 (anonymous ownership and competing citations).
- **Problem:** The remaining choices are format-specific and some anonymous rows have no explicit owner.
- **Before:** only deterministic fallback classification and exact-resource joins.
- **After:** five bounded JSON prompts; schema/allowlist validation; fallback on malformed or low-confidence responses. Anonymous affiliation additionally requires a direct exact-resource owner in context, because a model assertion alone is not audit proof.
- **Tests added:** pending mocked resolver tests.
- **Expected impact:** Improve supported system/flow/citation decisions while rejecting guessed ownership.
- **Verification:** pending.
- **LLM call sites:** `system_id`, `flow_class`, `affiliation`, `primary_file`, and explicitly requested image `image_pii`; default `gpt-4o-mini`, Vision `gpt-4o`.
- **Cost impact:** response token usage tracked; full-run cost to be measured, not assumed.

## Change 3: Actual-token accounting
- **Iteration:** 16a
- **Fix ID:** llm-usage
- **File:** `code/agent/llm/usage_tracker.py`
- **Grounded in:** `phase15_validation.md` §7 records zero prior API usage and Phase 16 requires real per-call accounting.
- **Problem:** Earlier usage reports correctly showed zero but had no per-model live-call ledger.
- **Before:** static zero-usage sections.
- **After:** singleton records API-reported input/output tokens, groups by purpose/model, and estimates USD from current official model-page rates; unknown model rates remain explicitly unknown.
- **Tests added:** pending.
- **Expected impact:** No fabricated non-zero tokens; cache hits count zero.
- **Verification:** pending.
- **LLM call site:** all enabled calls.
- **Cost impact:** measured after execution.

## Change 4: Vision evidence adapter
- **Iteration:** 16a
- **Fix ID:** llm-image_pii
- **File:** `code/agent/evidence/handlers/image_handler.py`, `code/agent/llm/client.py`
- **Grounded in:** `phase15_validation.md` §9 image/format gaps and the Phase 2 image stub.
- **Problem:** Registry's default image branch produced no records.
- **Before:** `vlm_extract` returned deferred empty records without a VLM callback.
- **After:** a separately called `extract` maps schema-validated Vision records to `RecordState`; corrupt/non-image input fails closed. Registry and its frozen tests remain untouched.
- **Tests added:** `test_image_extracts_identity_linked_record`, `test_image_filters_unrelated_user`, `test_vision_rejects_non_image_and_corrupt`.
- **Expected impact:** Visible image rows become auditable only when Vision and exact listed identifier are available.
- **Verification:** Mocked tests pass; live Vision blocked pending a valid key.
- **LLM call site:** `image_pii`, `gpt-4o`, actual tokens measured per response.
- **Cost impact:** no successful live response yet.

## Change 5: Four scoped call-site integrations
- **Iteration:** 16a
- **Fix ID:** llm-system_id/affiliation/flow_class/primary_file
- **File:** `code/agent/evidence/handlers/json_handler.py`, `code/agent/state/reconstructor.py`, `code/agent/policy/engine.py`, `code/agent/steps/builder.py`, `code/orchestrator/pipeline.py`
- **Grounded in:** `phase15_validation.md` §9 cases 08 (generic JSON), 11/15/18/20 (flow shape), 21–30 (competing citations), and 01–04/31 (unsupported ownership).
- **Problem:** The deterministic pipeline cannot resolve certain genuinely ambiguous labels/citations; anonymous rows also tempt unsupported attribution.
- **Before:** unresolved JSON stayed `json`; unknown flow shapes stayed records; latest file was cited; anonymous records lacked a model review.
- **After:** only unresolved JSON labels, ambiguous integration records, directly corroborated anonymous rows and multiple same-resource/same-state citations reach the resolver. The pipeline leaves the rule-only path unchanged when no key is set.
- **Tests added:** schema/allowlist/ownership/citation resolver tests, rule-only full-sample status regression.
- **Expected impact:** Correct supported system, flow and citation decisions; no fabricated ownership.
- **Verification:** Offline sample preserves 32/32 statuses; live sample unverified because the configured key returned `AuthenticationError`.
- **LLM call sites:** `system_id`, `affiliation`, `flow_class`, `primary_file`; default `gpt-4o-mini`.
- **Cost impact:** no successful live response yet.

## Change 6: Local dependency and operator instructions
- **Iteration:** 16a
- **Fix ID:** llm-setup
- **File:** `requirements.txt`, `README.md`
- **Grounded in:** Phase 16 environment and submission requirements.
- **Problem:** The OpenAI SDK was not installed or documented.
- **Before:** no pinned dependency list for the optional hybrid path.
- **After:** `openai>=1.0.0` and existing test/PDF dependencies are listed; README explains environment, fallback, traces and ownership limitations.
- **Tests added:** not applicable.
- **Expected impact:** Reproducible local setup without a committed secret.
- **Verification:** SDK installed into repository `.venv`; authenticated live call remains blocked.
- **LLM call site:** none.
- **Cost impact:** zero.

## Change 7: Authentication circuit breaker
- **Iteration:** 16b
- **Fix ID:** llm-auth-fallback
- **File:** `code/agent/llm/client.py`, `code/orchestrator/pipeline.py`
- **Grounded in:** live Phase 16 `system_id` smoke and sample traces under `code/.cache/llm_traces/`, each reporting `AuthenticationError`; 32-case sample comparison remained 32/32 status and 1/32 exact arrays.
- **Problem:** Retrying an invalid key per ambiguous record would generate repeated doomed calls and prolong the full run.
- **Before:** every failure retried up to `OPENAI_MAX_RETRIES`; downstream stages could continue to see a non-null resolver after auth failure.
- **After:** authentication/permission errors disable the client for that process, and the pipeline drops the resolver before state reconstruction. Transient network/rate-limit errors still retry.
- **Tests added:** `test_authentication_error_circuit_breaks` plus mocked timeout/rate-limit tests.
- **Expected impact:** One failed auth attempt at most per process, deterministic rule-only continuation.
- **Verification:** 32-case invalid-key run completed at 32/32 status, 1/32 exact arrays; API responses/tokens 0.
- **LLM call site:** shared adapter, not a new semantic purpose.
- **Cost impact:** no response-token cost on the rejected request.

## Change 8: Packaged dependencies and source-safe tests
- **Iteration:** 16b
- **Fix ID:** llm-package-test
- **File:** `code/requirements.txt`, `code/tests/test_llm_*.py`, `code/tests/test_image_handler_vision.py`
- **Grounded in:** `repackage.py` includes `code/` but not root `requirements.txt`; first offline run with pytest basetemp under `code/.cache` falsely broke existing filesystem-fixture tests.
- **Problem:** The submission archive otherwise omits its dependency manifest; a temp fixture inside an excluded directory cannot be scanned by existing tests.
- **Before:** only root requirements; `.cache` basetemp used during the first trial.
- **After:** a mirrored `code/requirements.txt` will enter the archive; tests use repository-local `.tmp-tests` outside excluded trees.
- **Tests added:** 23 mocked/offline tests across the four new test files.
- **Expected impact:** Reproducible zip without credentials; truthful 244-pass/2-known-fail suite rather than fixture-path artifacts.
- **Verification:** 23 focused tests pass; full suite 244 pass, two pre-existing known failures after installing the specified Pillow dependency in `.venv`.
- **LLM call site:** none; mock-only tests.
- **Cost impact:** zero.

## Change 9: Source-backed flow classification
- **Iteration:** 16c
- **Fix ID:** llm-flow_class-raw-source
- **File:** `code/agent/state/reconstructor.py`, `code/agent/policy/engine.py`
- **Grounded in:** `phase15_validation.md` §9 cases 11/15/18/20 have flow-shape gaps; inspection of the initial Phase 16 policy call showed it passed only state and notes, not the winning row needed to distinguish a connector from a static record.
- **Problem:** A model given only `data_flow_` and notes could confidently guess a live flow from its name.
- **Before:** the policy's `flow_class` prompt received a synthesized `{system_id,resource_id,state,notes}` summary.
- **After:** reconstruction attaches the winning evidence's raw row to the fact; policy calls the resolver only for PRESENT integration records with that row. ABSENT and timeline-only facts cannot become active flows by model suggestion.
- **Tests added:** `test_flow_classification_uses_visible_raw_row_only`, `test_reconstructor_exposes_winning_raw_evidence_to_policy`.
- **Expected impact:** Reduce false active-flow suggestions while making legitimate connector evidence available.
- **Verification:** mock tests pass; the authenticated sample remained 32/32 status, and case_11's flow step array became exact. Overall exact arrays rose only to 2/32.
- **LLM call site:** existing `flow_class`, default `gpt-4o-mini`.
- **Cost impact:** narrower call set; actual responses currently zero.

## Change 10: Repository-local credential is authoritative
- **Iteration:** 16b resumed
- **Fix ID:** llm-local-env-only
- **File:** `code/agent/llm/client.py`, `requirements.txt`, `code/requirements.txt`, `README.md`
- **Grounded in:** two `AuthenticationError` traces with the inherited process key, followed by a successful bounded `system_id` call using the distinct repository `.env` key (116 input/54 output tokens).
- **Problem:** A stale process-level `OPENAI_API_KEY` shadowed the verified local credential.
- **Before:** `OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))`.
- **After:** `python-dotenv` reads only the repository `.env`; the key is passed explicitly to `OpenAI`, and a conflicting process key is ignored. `OPENAI_LLM_DISABLED=1` remains an offline-test switch, not an alternate credential source.
- **Tests added:** `test_repo_env_file_overrides_conflicting_process_key`; missing-local-key test now supplies an absent fixture file.
- **Expected impact:** Live hybrid calls use the user's verified key without copying or exposing it.
- **Verification:** direct test succeeded even with a deliberately invalid process key; one response used 120 input/54 output tokens. Mocked Phase 16 tests: 24 passed before Vision guard.
- **LLM call site:** shared client, no new purpose.
- **Cost impact:** real usage is tracked from responses; `.env` is excluded from `code.zip`.

## Change 11: Reject malformed Vision system labels
- **Iteration:** 16b resumed
- **Fix ID:** llm-image-schema-guard
- **File:** `code/agent/llm/semantic_resolver.py`
- **Grounded in:** live `case_01`/`case_02` Vision traces: two responses labeled `system_id` as `backup_9287` or `Northstar Shop`, not service IDs; both cases regressed from COMPLETE to INCOMPLETE.
- **Problem:** Identity-matching image text alone was accepted as a ResourceFact even when the model confused a visible title or resource ID with the system field.
- **Before:** Vision filtering checked user reference and state but not `system_id`, nonempty `resource_id`, or `pii_hits` shape.
- **After:** only allowlisted system IDs, nonempty resource IDs, list-shaped hits, listed user refs and valid states become records.
- **Tests added:** `test_image_rejects_title_or_resource_as_system_id`.
- **Expected impact:** Remove these two unsupported image facts without suppressing valid service-labeled images.
- **Verification:** pilot recovered case_01/02 to COMPLETE; full hybrid sample preserved 32/32 statuses and raised exact arrays from 1/32 to 2/32.
- **LLM call site:** existing `image_pii`, `gpt-4o`.
- **Cost impact:** no extra API calls for cached responses.

## Change 12: Per-attempt trace of usage-bearing failures
- **Iteration:** 16c resumed
- **Fix ID:** llm-trace-completeness
- **File:** `code/agent/llm/client.py`, `code/tests/test_llm_client.py`
- **Grounded in:** the 32-case hybrid run recorded 377 usage-bearing responses, but old traces contained 15 `image_pii` TypeError failures with zero tokens despite the usage tracker counting model responses. The final sample used 440,451 input and 19,296 output tokens.
- **Problem:** a malformed or empty JSON response could be billed and retried, yet only the final failure trace was written with zero tokens.
- **Before:** one final failure trace per retry group, with zero token fields.
- **After:** each API attempt writes its own trace; a response that fails parsing retains its raw content, token counts, latency and error type. Transport errors still have zero response tokens.
- **Tests added:** expanded `test_malformed_json_retries_then_falls_back` to require two failure traces with 7/3 tokens each and two usage records.
- **Expected impact:** future trace-derived usage matches the per-process tracker even on malformed responses; decision output is unchanged.
- **Verification:** full offline suite 246 passing, the same hard-gate and frozen-proximity failures. No second live 32-case run was made merely for tracing; historical traces remain incomplete for those 15 attempts, while the sample's usage report retains actual API response counts.
- **LLM call site:** shared adapter, no new purpose.
- **Cost impact:** no additional calls from the code change.
