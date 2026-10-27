# Source-only controls for anonymous resource affiliation

These controls use participant request inputs, `system_activity.csv`, the evidence manifest, and identifiers visible in evidence records. They do not read `sample_output.csv`, previous predictions, or hidden answers. Public sample answers are used separately for evaluation after the production rule is chosen.

## Account workflow timing

The account-owner veto index found 250 resource IDs with a unique owner visible through a current or historical identifier. For a request with exactly one account deletion across **all** outcome classes in the 30–90 minutes before `reported_at`, 26 of 26 independently owned candidates belonged to the requester. Requiring the unique winner to report `SUCCESS` left 14 of 14 known candidates correct. Five masked-owner folds produced 63 held-out known-owner matches, zero known-owner mistakes, and 100 ownerless candidates that could not be scored. These observations support a bounded correlation rule, not a claim that every ownerless candidate is correct or that `SUCCESS` proves deletion.

The rejected alternatives failed independent controls:

| Proposed join | Known correct | Known wrong | Decision |
|---|---:|---:|---|
| Unique account deletion 0–5 minutes before report | 0 | 25 | Reject |
| Filter to `SUCCESS` **before** testing 30–90-minute uniqueness | 42 | 48 | Reject |
| Unique account deletion 30–90 minutes before report, then check winner outcome | 14 | 0 | Allow only with owner and requester ambiguity vetoes |

## Analytics and cross-resource timing

An independent exact-owner index for `analytics_platform` contained 79 analytic resource IDs. Matching an account deletion with the sole analytic anonymization action in the following 90 minutes produced 10 evaluable owner-bearing pairs: **one same-owner pair and nine different-owner pairs**. Limiting the match to nearby activity-ID gaps did not help: a gap of at most five gave one same-owner and nine different-owner pairs among 10 evaluable pairs. Thus temporal or row-order proximity between account and analytic actions is not a safe subject link.

The anonymous analytic rows in the September 15 service export have null `customer_reference`, `email`, `email_hash`, and `phone`. Its anonymous 404 account lookups likewise have no profile or subject field. The September 26 lookup trace gives a unique trace ID per query, but the anonymous analytic query's `lookup_key` and subject fields are null; adjacent queries for named users carry **different** trace IDs. Batch co-occurrence cannot establish a same-person relationship.

## Negative SQL snapshots

The September 2 account replica SQL file contains seven rows across primary and failover tables. It has no declared population or resource scope. A target missing from those seven rows may be absent from the exported slice; the file alone does not establish absence from every account record. In the available 83 non-image manifest files, no account was observed present on both sides of this capture within 20 days, absent from the seven-row export, and free of an intervening lifecycle action. This check therefore supplied **no independent completeness proof** either way. A closed-world assertion would require source-declared coverage or a request-scoped query result.

## Consequence for the release gate

The agent keeps anonymous rows unassigned unless an exact subject/resource edge or a calibrated guarded workflow link exists. It does not manufacture an owner from numerical suffixes, batch order, temporal adjacency, a workflow `SUCCESS` claim, or a public answer. The residual exact-step gap is measured in `step_gap_diagnosis.md`; the hard 85% exact-array test remains active.
