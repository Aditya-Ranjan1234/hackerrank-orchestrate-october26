# Phase 16 validation — optional OpenAI integration

## 1. Outcome and release gates

| Measure | Phase 15 baseline | Phase 16 measured | Required |
|---|---:|---:|---:|
| Sample status | 32/32 | 32/32 | 32/32 |
| Exact step arrays | 1/32 | 2/32 | ≥28/32 |
| Offline tests passing | 221 | 246 | ≥236 |
| Known failing tests | 2 | 2 | 0 release-gate failures |
| Usage-bearing API responses in full hybrid sample | 0 | 377 | Measured |

**NOT_READY.** The exact-step gate is still 6.25%, far below 85%. The two
failing tests are the unchanged hard exact-step gate and the frozen stale
same-system-proximity assertion; no test was weakened or deleted. Twenty-five
new mocked/offline tests pass. The repository `.env` credential was verified
with a live call and used for the 32-case hybrid measurement. The stale
process-level key was ignored.

## 2. Implemented call sites and fallback

| Purpose | Owner | Model | Guard |
|---|---|---|---|
| `system_id` | unresolved JSON records | `gpt-4o-mini` default | allowlisted label, confidence ≥0.8 |
| `flow_class` | ambiguous integration records | `gpt-4o-mini` default | flow/record schema, confidence ≥0.8 |
| `affiliation` | anonymous evidence row | `gpt-4o-mini` default | exact full-resource ID already owned in direct context |
| `primary_file` | competing same-resource/state citations | `gpt-4o-mini` default | selected ID among audit-eligible candidates |
| `image_pii` | PNG/JPEG evidence | `gpt-4o` | valid image, listed identifier and state schema |

No local key, malformed response, timeout, rejected credential, or invalid schema
returns to the rule-only result without crashing a case. Authentication errors
open a process-local circuit breaker; network/rate-limit failures retain bounded
retries. The frozen evidence registry remains unchanged; the pipeline invokes
Vision directly when enabled. The client reads `OPENAI_API_KEY` only from the
repository `.env`, not from the process environment. An explicit
`OPENAI_LLM_DISABLED=1` switch is used for offline tests.

## 3. Test and verification record

New tests cover missing key, cache hit/no second usage, malformed JSON,
timeout/network and 429 retries, authentication circuit breaker, corrupt and
non-image Vision input, disk-cache key separation, schema/allowlist checks,
exact-resource affiliation, audit-cutoff citation, mocked image extraction,
and the no-key 32-case status regression. Focused Phase 16 suite: **25/25**.
Full suite: **246 passed, 2 failed**, both pre-existing known failures. The
first run of the valid-PNG test exposed that Pillow was listed but not yet
installed locally; installing it in `.venv` cleared that environment error.

The earlier rejected-process-key sample completed rule-only at 32/32 statuses
and 1/32 exact arrays. A repeat rule-only sample had byte-identical SHA-256
`65a215ac0bc17a8fc7dad91c2e11ec9af0eb08fd2a41bb28667b167636cddb53`.
The authenticated hybrid sample finished at **32/32 statuses and 2/32 exact
arrays**, without replacing the full `output.csv`. Position-independent diff:
62 missing semantic identities, 72 extra identities, 23 citation differences;
positional dominant `SYSTEM_ID_MISMATCH` 93/425. Before the live run, two pilot
cases regressed from malformed Vision system labels; an allowlist guard restored
both. After that, the full sample had no status regression.

## 4. Iteration log

| Iteration | Change | Status | Exact arrays | Decision |
|---|---|---:|---:|---|
| 16a | client, cache, traces, prompts, four call sites, Vision | 32/32 | 1/32 | Live attempt rejected by API. |
| 16b | auth circuit breaker, packaged dependencies, mocked regressions | 32/32 | 1/32 | Avoid repeated doomed calls; no claim of improvement. |
| 16c | source and semantic-diff audit | 32/32 | 1/32 | No safe model-independent affiliation fix for ownerless gold rows. |
| 16d | residual-gap documentation | 32/32 | 1/32 | Stop without fabricating evidence; NOT_READY. |
| 16b resumed | load only repository `.env`; reject malformed Vision system labels | 32/32 | 2/32 | Live sample; one exact-array gain, no status loss. |
| 16c resumed | trace every usage-bearing API attempt | 32/32 | 2/32 | Accounting correction only; no decision change. |

## 5. Per-case regressions and residual gaps

Every sample case retains gold-correct status. `case_02`, `case_03`, `case_04`,
and Phase 12's recovery set `case_08`–`case_16`, `case_18`–`case_20`, and
`case_22` retain correct status. `case_11` and `case_14` have exact gold step
arrays; all other cases remain step mismatches. The full per-case missing/extra/citation
table and grounded diagnosis are in `phase15_validation.md` §§5, 9; the current
generated positional and semantic diff is `step_diff_report.md`.

At least five gold-required verifications in cases 01, 02, 03, 04 and 31 lack
a direct identity-to-full-resource link in the supplied evidence. These alone
cap evidence-safe exact-array coverage at 27/32 (<85%), even if all other
cases were repaired. A model's asserted ownership cannot be used as the only
provenance in a deletion audit. Cases 05–30 also contain mixed system-label,
flow-class, resource-extraction and citation gaps. The live resolver reduced
missing/extra semantic steps but did not fix the majority of these gaps. No
broad suppression or numeric-suffix joining was introduced.

## 6. Full dataset and package integrity

`output.csv` was regenerated in rule-only mode: **518 rows**, 518 unique IDs,
natural order, valid JSON step arrays, **zero validator errors and warnings**.
Its SHA-256 is
`016bc7b17e500ddd47316e3e5fa1f3d825627e099a3227b1c034d3e8a9a006ae`,
identical to the prior Phase 15 rule-only artifact. Sample IDs are separate
from the 518-case full output, so sample scoring uses a separate 32-case run.
The rebuilt `code.zip` contains 185 files including `code/requirements.txt`,
passes ZIP integrity checks, and contains no `.venv`, `.cache`, `.env`,
`__pycache__` or `.git` entries.

## 7. Actual token usage and cost

The 32-case hybrid run recorded **377 usage-bearing API responses**, **440,451
input tokens**, **19,296 output tokens**, estimated **$1.266820** using the
model-page rates in `usage_report.md`. Of these, 353 responses were `image_pii`
on `gpt-4o`, accounting for $1.265080 of the estimate. Calls that failed JSON
parsing still consumed tokens and are counted. See `llm_usage_audit.md` for
trace caveats and `usage_report.md` for the per-purpose table. No key value is
in source, output, or archive.

## 8. Remaining actions and ship readiness

**NOT_READY.** The key is valid and the hybrid behavior is now measured, but
the exact-step score is 2/32. The five source-grounding gaps above need either
additional direct ownership evidence or an explicitly approved change to the
ownership rule before 28/32 exact arrays can be honestly reached. A 518-case
hybrid run is deferred while the release gate is so far below target; the
518-row rule-only output remains structurally valid but not submission-ready.
Do not treat a valid CSV shape or measured API usage as release readiness.
