# Assistant review of the 518 output rows

## Review boundary

The assistant read the action/verification plan for every original output row, inspected all distinct request-intent forms, reviewed every screenshot, read the four PDFs and the text handover, and reopened the raw records implicated in incorrect plans. Read-only scripts independently enumerated 1,839 JSON/SQL resource rows and 1,377 resource-bearing log events. They exposed exact field names, values, timestamps and aliases for review; neither previous predictions nor public sample answers supplied production labels. The existing runner was used to serialize and reproduce the source-backed corrections, not to declare its own previous answers correct.

`all_518_row_review.csv` records every case. `changed_rows.csv` contains exact added/removed steps, full before/after arrays, original/final status and output row number. A PASS on plan replay means the listed operations can satisfy the recorded visible obligations. It does not prove that an anonymous resource has no relationship to the requester or predict the hidden grader's score.

## Source-backed corrections

| Error found | Source and reasoning | Correction |
|---|---|---|
| Portuguese deletion requests classified as non-deletion | Fourteen request texts say permanent account exclusion. A sentence asking for identifier verification is supplementary. | Recognize deletion; audit the subject normally. |
| Non-deletion requests treated as deletion | Requests 533–542 include profile corrections, login reset, information copies, marketing-only removal and explicit negations. Eight had wrong statuses; two were already NOT_APPLICABLE. | Respect negation/scope, keep all ten NOT_APPLICABLE with empty steps. |
| Ghost search records with connector IDs | `activity_2956` identifies `data_flow_4227` as the connector and names `search_1474` separately. Equivalent source rows occur across 24 cases. | Remove the three search-record deletion steps for each connector ID; retain the actual connector and search obligations. |
| Disabled connectors treated as records to delete | SQLite `connector_subscriptions.enabled=0`, notably evidence_84/data_flow_4319, evidence_75/data_flow_3391 and evidence_72/data_flow_7452. | Normalize state flags and verify DATA_FLOW_DISABLED. |
| Restore blockers lost at schema boundaries | SQLite INTEGER/TEXT zero, nested JSON `restore_allowed=false`, and explicit log `restore_authorization_completed decision=deny` describe the same blocked access state. | Verify RESTORE_BLOCKED, rather than merely retaining a backup or treating it as live risk. |
| Support redaction claimed incomplete when contact fields were null | Five direct SQL support rows have all three requester fields explicitly null. Five message readbacks explicitly contain `[REDACTED]`. | Recognize the redacted state; do not repeat a remediation unless another direct identifier remains. |
| Legal holds scheduled for deletion | Supplied legal_service rows carry active retained-until/retention reasons; rule_13 requires RETAIN. Seven records used the unknown-category DELETE fallback. | Preserve the hold and verify presence. |
| Persisted connector configurations omitted | `connector_configurations.subject_selector` is a stored subscription field, unlike a transient search query. Across 91 raw rows and 61 resources, direct-owner crosschecks had no conflicts. | Exact subject matching only in the persisted configuration schema. |
| Attachments omitted or treated as support conversations | `ticket_attachments.uploaded_by` plus `storage_class=ticket_attachment`, and `attachment_pii_scan` with a filename, establish the artifact type. | Apply rule_06 DELETE instead of rule_05 REDACT. |
| Catalog aliases dismissed because the canonical ID was absent from pixels | activity_4007 links object_19 to the exact filename visible in evidence_46; activity_4009 links export_1842 to the statement reference in evidence_18; activity_4011 links tombstone_17 to the retained user reference in evidence_42. | Combine catalog ownership/canonical ID with independently visible artifact existence. Reject contradictory visible owners. |
| Historical phone-only ownership omitted | audit_279 proves user_11's previous number; evidence_01 line 25 reports that exact number in support_9538. The customer screen independently names the same support resource. | Exact full-number historical match, with country code retained and uniqueness required; delete the exclusive attachment. |
| Active-flow citations not eligible for current-source preference | A PRESENT configuration with `enabled=true` proves the separate ACTIVE flow state; the old citation filter recognized only INACTIVE flags. | Recognize typed active/restore states and prefer an already captured source when it proves the same fact. |

No source file was edited. No case ID, public answer row, prior output row or external submission is consulted by the production decision path. Evaluators can refer to case IDs to document the review.

## Decisions not guessed

- The marketing screenshot visibly names a different subject from the catalog link used by case_63. The review does not assign that person's marketing record to the requester. The existing empty COMPLETE result remains an unresolved evidence-quality issue, explicitly flagged in the all-row ledger.
- The backup screenshot for case_55 proves an archive exists, but does not explicitly prove restore access is blocked. Its retention-only verification is flagged; this review does not invent an access-denial state from a Healthy label.
- Workflow SUCCESS is not independently observed absence. Existing uncorroborated account checks stay marked in the per-row review, and no invented source ID is inserted.
- Some earlier timestamped observations were exported after audit_at. The candidate retains the repository's existing intrinsic-observation-time interpretation, prefers contemporaneous citations when possible, and flags every remaining retrospective citation. This remains a risk under the literal file-capture rule; it is not silently counted as proof of source availability.
- The new catalog aliases are admitted only when both the catalog event and artifact capture are before audit_at. Exact canonical/alias matching and conflicting-owner rejection prevent a generic near-text join.

## Verification scope

The final checks cover CSV shape, case coverage, step numbering/order and state vocabulary, finding citations, remediation-before-verification dependencies, policy obligations, final-state reachability, source-literal or catalog-alias citation support, and import isolation from answer files. A separate independent owner-field scan checks for JSON/SQL/log resources omitted from the final output. Tests and measured final counts are in `score_iteration_validation.md`; source gaps are kept visible rather than represented as passed hidden cases.
