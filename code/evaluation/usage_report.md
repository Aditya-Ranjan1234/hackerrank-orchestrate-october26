# Usage Report

The final Phase 17 section at the end of this file is the measured, current
518-request run that produced root `output.csv`. Earlier phase sections are
historical runs and do not describe the current model usage. The final run
uses warmed content/prompt caches, so cache hits have no new API tokens.

## Phase 2 — Evidence Ingestion

Provider/model: none. The Phase 2 implementation used deterministic parsers
and an offline fake-VLM test stub. Model calls: 0; input tokens: 0; output
tokens: 0; estimated cost: $0.00.

## Phase 3 — Active Flows and Restore Risks

Provider/model: none. Deterministic activity analysis only. Model calls: 0;
input tokens: 0; output tokens: 0; estimated cost: $0.00.

## Phase 6 — Step Generator

Provider/model: none. Pure deterministic operation mapping, validation, ordering,
and serialization. Model calls: 0; input tokens: 0; output tokens: 0; estimated
cost: $0.00.

## Phase 5 — Status Determinator

Provider/model: none. Pure deterministic classification and gating. Model calls:
0; input tokens: 0; output tokens: 0; estimated cost: $0.00.

## Phase 4 — Policy Engine

Provider/model: none. Pure deterministic rules and conflict resolution. Model
calls: 0; input tokens: 0; output tokens: 0; estimated cost: $0.00.

## Historical Phase 7 full-dataset run (no LLM)

Cases processed: 518. Total LLM calls: 0. Total tokens: 0. Average tokens per
case: 0. Total estimated cost: $0.00. Average cost per case: $0.00.

## Per-phase totals

| Phase | LLM calls | Input | Output | Total | Cost USD |
|---|---:|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 | 0 | 0 |
| 4 | 0 | 0 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 | 0 | 0 |
| TOTAL | 0 | 0 | 0 | 0 | 0 |

Historical methodology: extraction LLM calls (Phase 2 only if VLM was needed)
plus zero status/step LLM calls. Cache hit rate after the first identical
extraction run: 100%. That earlier diagnostic run used the no-VLM path.
## Phase 8 — Recovery iteration

- Model: none (deterministic recovery)
- LLM calls: 0
- Input tokens: 0
- Output tokens: 0
- Notes: No external APIs, credentials, or VLM calls used.
## Phase 10 — Dataset grounding and audit

- LLM/VLM calls during the 32-case sample and 518-case full run: 0.
- Input tokens: 0; output tokens: 0; API keys required: none.
- See `llm_usage_audit.md` for static call-path classification and dynamic trace counts.
## Phase 11 — Evidence-backed fixes

- LLM/VLM calls: 0.
- Input tokens: 0; output tokens: 0; API keys required: none.
- Deterministic Python changes only; sample result remains below submission target.
# Phase 12 usage

Phase 12 evidence extraction and gold validation used no live LLM or VLM. Calls: 0; input tokens: 0; output tokens: 0. The image handler remained stubbed.

# Phase 13 usage

Step diff, case tracing, and triage used no application LLM or VLM. Calls: 0; input tokens: 0; output tokens: 0.

# Phase 14 usage

Activity inference, evidence/state/policy interpretation, 32-case validation, and the full deterministic run invoked no application LLM or VLM. Calls: 0; input tokens: 0; output tokens: 0; estimated model cost: $0.00. No API keys were used.

## Phase 16 — OpenAI application usage

Historical authenticated 32-case sample, as recorded in `phase16_validation.md`.
Only actual API responses count as calls; cache hits cost zero tokens.

| Purpose | Model | Calls | Input tokens | Output tokens | Estimated USD |
|---|---|---:|---:|---:|---:|
| **Total** | gpt-4o-mini / gpt-4o | **377** | **440451** | **19296** | **$1.266820** |

Rates: https://developers.openai.com/api/docs/models/gpt-4o-mini and https://developers.openai.com/api/docs/models/gpt-4o. Unknown model rates are not silently priced at zero.

## Phase 17 — OpenAI application usage

Only actual API responses count as calls; cache hits cost zero tokens. Provider: OpenAI.

| Purpose | Model | Calls | Input tokens | Output tokens | Estimated USD |
|---|---|---:|---:|---:|---:|
| primary_file | gpt-4o-mini | 47 | 7701 | 3829 | $0.003453 |
| **Total** | | **47** | **7701** | **3829** | **$0.003453** |

Rates: https://developers.openai.com/api/docs/models/gpt-4o-mini and https://developers.openai.com/api/docs/models/gpt-4o. Unknown model rates are not silently priced at zero.

Requests in run: 518. Average input tokens/request: 14.87; average output tokens/request: 7.39; average total tokens/request: 22.26; estimated cost/request: $0.000007.


## Scored-output review — current submitted-file provenance

The Phase 17 table immediately above describes the final 518-case regeneration for this review: **47 fresh gpt-4o-mini responses**, **7,701 input**, **3,829 output**, **11,530 total tokens**. These were citation-selection calls; existing vision and semantic cache entries were reused. The subsequent complete-pipeline replay of the single newly phone-linked case and the final 32-case sample both recorded **0 fresh calls and 0 tokens**. This section reports fresh application usage for the final output, not cumulative historical development charges or Codex assistant reasoning. No key value is included in any report or submission archive.
