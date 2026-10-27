# Ghost Data Audit Agent — A Concrete Plan

## 0. The Trap Doors (Where Most Teams Will Lose Points)

Before architecture, internalize these — they are the line between a top-quartile and bottom-quartile submission:

1. **`reported_status` is a lie by definition.** The brief explicitly says "Reported workflow statuses and operation results are claims." Never propagate `reported_status=COMPLETE` into your `deletion_status`. The agent's job is to *disprove* the claim using primary evidence.
2. **Identity ≠ email.** A user may have changed email N times. If you only audit the email in `deletion_requests.csv`, you will miss records still tied to historical emails (search indexes, exports, logs love old emails). Resolve to a `user_id` and enumerate **every** email that user_id has ever owned.
3. **Time is a first-class axis.** A backup taken *before* deletion is a restore risk. A backup taken *after* is not. A sync job scheduled to run *after* `audit_at` is `ACTIVE` even if the data is currently gone. The agent must reconstruct state **as of `audit_at`**, not "now."
4. **Tombstones are not failures — but only if PII is actually scrubbed.** A retained `user_id` reference is allowed; `email`, `name`, `phone`, **`email_hash`** are not. Email hash is the sneakiest one — teams will leave it in tombstones and lose points silently.
5. **Ordering is graded.** Phase order is fixed (FINDING → REMEDIATION → VERIFICATION). Within a phase, the operation order is the table order (so `REPORT_REMAINING_RECORD` before `REPORT_EXPOSED_PII` before `REPORT_ACTIVE_DATA_FLOW` before `REPORT_RESTORE_RISK`). Within the same operation, sort by `(system_id, resource_id)` ascending. One misordered pair = a sequence-accuracy hit.
6. **`evidence_id` rules differ by phase × status.** `COMPLETE` cases: every VERIFICATION step must cite a real `file_id`/`activity_id`/`audit_id`. `INCOMPLETE` cases: FINDING steps cite evidence; REMEDIATION and VERIFICATION steps use `""`. Putting evidence on a remediation step in an INCOMPLETE case is a field-level error.
7. **`NOT_APPLICABLE` ≠ missing row.** The row must still be emitted with `[]` as `steps_json`. The user might have requested data export, asked a question, or referenced an email that maps to no `user_id` at all.
8. **Sync recreation flips COMPLETE → INCOMPLETE.** Even if every record is gone *now*, an active flow that can copy the data back makes the deletion INCOMPLETE until `DISABLE_DATA_FLOW` is proposed.
9. **Retention is a positive verification.** If policy says "retain orders for 7 years," the correct step is `VERIFY_RECORD_PRESENT` (state=PRESENT) on the order record — *not* `VERIFY_RECORD_ABSENT`. Teams will reflexively write ABSENT and fail retained-record cases.
10. **`audit_at` is the snapshot.** Anything that happened *after* `audit_at` is irrelevant. Anything reported *before* `audit_at` but not actually executed *by* `audit_at` is still a finding.

---

## 1. System Architecture

The agent is a **deterministic orchestrator with LLM as a per-evidence extractor**, not an LLM that reasons end-to-end. LLM non-determinism is the enemy of grader accuracy.

```
┌─────────────────────────────────────────────────────────────┐
│                    deletion_audit_agent                       │
│                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐ │
│  │ Identity     │──▶│ Evidence     │──▶│ State            │ │
│  │ Resolver     │   │ Ingester     │   │ Reconstructor    │ │
│  └──────────────┘   │ (LLM+cache)  │   │ (deterministic)  │ │
│         │            └──────────────┘   └────────┬─────────┘ │
│         │                                         │           │
│         ▼                                         ▼           │
│  ┌──────────────┐                        ┌──────────────────┐│
│  │ user_id+     │                        │ Policy Engine    ││
│  │ all emails   │                        │ (deletion_rules) ││
│  │ all user_ids │                        └────────┬─────────┘│
│  └──────────────┘                                 │          │
│                                                   ▼          │
│                          ┌──────────────────────────────┐   │
│                          │ Status Determinator (deterministic)│   │
│                          │ COMPLETE / INCOMPLETE / N/A   │   │
│                          └──────────┬───────────────────┘   │
│                                     ▼                        │
│                          ┌──────────────────────────────┐   │
│                          │ Step Generator (strict order) │   │
│                          └──────────┬───────────────────┘   │
│                                     ▼                        │
│                          ┌──────────────────────────────┐   │
│                          │ Self-Validator (schema+rules)│   │
│                          └──────────┬───────────────────┘   │
│                                     ▼                        │
│                              output.csv (518 rows)            │
└─────────────────────────────────────────────────────────────┘
```

**Why this shape:** The LLM only writes to a structured intermediate representation (per-evidence parsed facts). Every status decision, every step ordering, every evidence citation is produced by deterministic code from that IR. Reruns are byte-identical. Cost is bounded.

---

## 2. Identity Resolution — The Algorithm

This is the foundation. Get it wrong and every downstream step is poisoned.

### Input
- `case.email` (from deletion_requests.csv)
- `user_identities.csv` (current email → user_id)
- `user_audit_log.csv` (historical changes: email_added, email_removed, user_merged, user_split, etc.)

### Output (per case)
```python
IdentityBundle:
    primary_user_id: str                    # canonical user_id at audit_at
    all_user_ids: set[str]                  # including merged/split siblings
    all_emails: set[str]                    # every email ever owned
    email_history: list[(email, valid_from, valid_to, source_audit_id)]
    request_email_kind: CURRENT | HISTORICAL | UNKNOWN
```

### Algorithm
```
1. Look up case.email in user_identities.csv
   - If found: primary_user_id = match; request_email_kind = CURRENT
   - If not found: search user_audit_log for any row mentioning case.email
       - If found: primary_user_id = that row's user_id; kind = HISTORICAL
       - If not found anywhere: kind = UNKNOWN  (likely NOT_APPLICABLE — see §10 E1)
2. Pull all user_audit_log rows where user_id = primary_user_id (or that mention primary_user_id)
3. Walk the audit log chronologically; for each row with effective_time ≤ audit_at:
   - email_added → add (email, valid_from=row_time, valid_to=∞)
   - email_removed → close valid_to on the matching email
   - user_merged → absorb the other user_id into all_user_ids; pull that user's email history too
   - user_split → both user_ids remain related (the new user_id may still hold shared history)
4. all_emails = union of all email_history.email values
5. Sort all_emails ascending — this matters for deterministic step ordering later
```

### Edge cases (named)
- **E1 — Email not in any file.** No `user_id` resolves. If `request_text` is empty or doesn't mention "delete", emit `NOT_APPLICABLE, []`. If `request_text` clearly asks for deletion but no account exists, this is a *vacuous complete* — the safest interpretation per the brief's spirit is `NOT_APPLICABLE` (no deletion authorized because there's no account to delete). Confirm against `sample_output.csv` if a sample covers this.
- **E2 — Historical email only.** Resolve via audit_log, never miss this. Some evidence files may reference the historical email directly (logs, exports).
- **E3 — Email reused by another user.** Two `user_id` rows share an email at different times. Use `valid_from/valid_to` windows intersected with `audit_at` to pick the correct user_id.
- **E4 — Merge or split in audit log.** Both user_ids must be audited because records may persist under the old id.
- **E5 — Case email has different case/whitespace.** Normalize (lowercase, trim) before lookup; audit_log entries may be inconsistently cased.
- **E6 — Email hash present in identities (rare but possible).** If the case row is itself a hash, hash every candidate email with the same algorithm and match.

---

## 3. Evidence Ingestion — Per File Type

You'll see PDFs, images, JSON, SQLite SQL exports, and log files. Treat each differently. **Cache every extraction result keyed by `file_id` + a content hash**, so re-runs are free.

### File-type handlers

| Type | Strategy | Output IR |
|---|---|---|
| **JSON** | `json.load`, walk keys, extract any field containing email/name/phone/user_id | list of `(path, value, kind)` |
| **SQLite SQL** | Load into in-memory `sqlite3`, run targeted queries: `SELECT * FROM <table> WHERE email IN (?, ...) OR user_id IN (?, ...)` | rows keyed by table+PK |
| **Logs (text)** | Regex for email/phone patterns + LLM extraction for lines mentioning a known user_id or email | structured events with `(ts, system, op, target_user_id, target_email, fields)` |
| **PDF** | `pdfplumber` for text + tables; if scanned (no text layer), route to VLM with a structured prompt | `(page, table_row, field, value)` |
| **Images** | VLM with a schema-constrained prompt: "Return JSON listing every visible field containing PII; do not transcribe non-PII" | same as PDF |
| **CSV exports inside evidence** | Direct `csv.DictReader` | rows |

### LLM extraction prompt pattern (the part that matters)
- Force JSON output via `response_format`/tool call. **Reject and retry** if the schema doesn't validate against a Pydantic model.
- Provide the *resolved identity bundle* in the prompt — "these are the emails and user_ids you are looking for; report only matches" — so the LLM doesn't hallucinate unrelated emails.
- Ask for `as_of_state` per record: `PRESENT` / `ABSENT` / `REDACTED` / `ANONYMIZED`, plus the timestamp of the evidence.
- For PDFs/images, also ask: "List every field name that contains a direct identifier (email, name, phone, email_hash)." This directly feeds `REPORT_EXPOSED_PII`.

### Caching key
```
cache_key = sha256(file_bytes) + "::" + sha256(identity_bundle_json)
```
The identity bundle is part of the key because the same evidence file may be reused across cases with different identity bundles — but the *extraction* doesn't depend on identity bundle, only the *filtering* does. So actually cache on file hash only, and filter deterministically after the cache hit.

---

## 4. State Reconstruction at `audit_at`

For every `(system_id, resource_id, user_id_or_email)` triple, compute the state at `audit_at`. This is the time machine.

### Inputs
- `system_activity.csv` (deletion ops, sync runs, exports, backups, restores, indexing)
- Extracted evidence facts (from §3)
- `user_audit_log.csv` (for historical identifiers)

### Per-resource state machine
```
state = INITIAL
for each activity row affecting this resource, ordered by activity_time ASC:
    if activity_time > audit_at: break
    match activity_type:
        case 'CREATE'   → state = PRESENT
        case 'DELETE'   → state = ABSENT (or TOMBSTONE if tombstoned)
        case 'REDACT'   → state = REDACTED
        case 'ANONYMIZE'→ state = ANONYMIZED
        case 'SYNC'     → if source has data and target was ABSENT → state = PRESENT
        case 'RESTORE'  → state = PRESENT (override prior DELETE)
        case 'EXPORT'   → creates a copy elsewhere (record the copy in a separate resource)
        case 'BACKUP'   → record a backup snapshot at this time (see §5)
        case 'INDEX'    → creates a search-index copy
```

### Conflict resolution
- **Activity log vs evidence file** — evidence wins. The brief says activity results are claims. If `system_activity` says `DELETE` succeeded at T1 but the evidence file with `file_id=evidence_42` (timestamped T2 > T1) shows the record still present, the state at `audit_at` is `PRESENT`.
- **Two evidence files, different timestamps** — use the one closest to `audit_at` but ≤ audit_at. Files with timestamp > audit_at are inadmissible for state at audit_at (they may be cited as proof of post-audit recreation, which is a *flow* finding, not a *record* finding).
- **Two evidence files, same timestamp, conflicting** — prefer the more authoritative system (e.g., the system's own export beats a log scrape).

### Output
A list of `ResourceFacts`:
```python
ResourceFact:
    system_id: str
    resource_id: str           # stable identifier (e.g., "account_005", "order_8821")
    user_id: str               # which historical id this is tied to
    state_at_audit: PRESENT | ABSENT | REDACTED | ANONYMIZED | TOMBSTONE
    direct_pii_present: set[str]   # subset of {email, name, phone, email_hash}
    evidence_id: str          # the file_id/activity_id/audit_id proving this
    evidence_timestamp: datetime
    retention_required: bool
    retention_required_fields: set[str]
```

---

## 5. Active Data Flows & Restore Risks

These are the ghosts that turn a "COMPLETE" into an "INCOMPLETE."

### Active data flow detection
A flow is `ACTIVE` at `audit_at` if **all** are true:
1. It exists in `system_activity.csv` (or evidence) with `op_type` in {SYNC, EXPORT, INDEX, IMPORT}.
2. Its last scheduled run was at time T_run ≤ audit_at (so it has executed before audit_at).
3. Its next scheduled run is at T_next, where T_next > audit_at **OR** the schedule is recurring (the brief treats recurring schedules as ongoing).
4. Its source system still contains (or could contain, given any user in scope) the user's data at audit_at.
5. It is not in a `DISABLED` state per a recorded activity row.

Edge cases:
- **F1** Sync ran between deletion and audit and *recreated* the record → both `REPORT_REMAINING_RECORD` (on the recreated record) AND `REPORT_ACTIVE_DATA_FLOW` (on the sync job). These are two findings, two operations, ordered per the table.
- **F2** Sync is scheduled but never ran before audit_at → still `ACTIVE` because the schedule exists. (Confirm against samples — if samples say otherwise, relax to "ran at least once.")
- **F3** Sync source is empty for this user → flow not ACTIVE for this user (no data to copy).
- **F4** Flow was DISABLED before audit_at → not ACTIVE; no finding needed. Optionally verify `VERIFY_DATA_FLOW_DISABLED`.

### Restore risk detection
A backup is a restore risk at `audit_at` if:
1. `backup_time < deletion_time` (backup contains pre-deletion state), AND
2. The backup is still within its retention window at `audit_at`, AND
3. The restore path is not blocked (no `BLOCK_RESTORE` activity recorded before audit_at).

Edge cases:
- **B1** Backup taken *after* deletion → no risk from this backup.
- **B2** Backup retention expired at T_exp < audit_at → no risk (the backup is gone).
- **B3** Backup is encrypted and the key is destroyed → effectively blocked; emit `BLOCK_RESTORE` as already done if activity log confirms, else propose it.
- **B4** Incremental backups: a base backup taken before deletion + an incremental taken after deletion may still restore pre-deletion state via the base. Treat the base as a restore risk.
- **B5** Multiple backups: enumerate each as a separate resource (`backup_001`, `backup_002`) — each gets its own finding/remediation/verification.

---

## 6. Policy Engine — `deletion_rules.csv`

This file dictates the required treatment per data category. Parse it once into a lookup table.

```
rules_lookup[(category, system_id?)] → {
    required_treatment: DELETE | REDACT | ANONYMIZE | RETAIN,
    retainable_fields: set[str],       # which fields may remain after redaction
    retention_period: timedelta | None
}
```

### Application
For each `ResourceFact`, find its category (from a system→category map, derived from evidence or a system catalog inferred from `system_activity.csv`):
- `required_treatment == DELETE` and `state != ABSENT` → REPORT_REMAINING_RECORD (PRESENT); plan DELETE_RECORD.
- `required_treatment == REDACT` and `state in {PRESENT, TOMBSTONE}` and `direct_pii_present ∩ redactable_fields != ∅` → REPORT_EXPOSED_PII; plan REDACT_RECORD (with the specific fields named in an internal note, though the spec doesn't require field names in steps_json — keep them in the audit trail).
- `required_treatment == ANONYMIZE` and `state != ANONYMIZED` → REPORT_REMAINING_RECORD (PRESENT, since data still links to user); plan ANONYMIZE_RECORD.
- `required_treatment == RETAIN` and `state == PRESENT` → no finding; verification step is `VERIFY_RECORD_PRESENT`. If absent, that's a *compliance* finding (a different kind of failure — flag in evaluation but the spec's taxonomy doesn't have a "should be present, is missing" finding, so emit VERIFY_RECORD_PRESENT as a verification *proving* presence only if it actually is present).
- For tombstoned accounts specifically: `user_id` may remain; `email, name, phone, email_hash` must be gone. If any remain → `REPORT_EXPOSED_PII` + `REDACT_RECORD`.

### Edge cases
- **P1** Rule specifies retention period "7 years" — if `requested_at + 7y < audit_at`, retention has expired and the record should be deleted; otherwise retained.
- **P2** Multiple rules apply to the same record (e.g., a support ticket with both PII and audit-trail requirements) — apply the strictest (DELETE > ANONYMIZE > REDACT > RETAIN). Document this precedence in your README.
- **P3** No rule matches a category — fail closed: treat as DELETE (safe default) and log a warning in `evaluation/`.
- **P4** Tombstone rule may differ from raw account rule — handle tombstone category explicitly.

---

## 7. Status Determination — Decision Tree

This is the single most important function. Make it pure, deterministic, and unit-tested.

```
def determine_status(facts, flows, restore_risks, identity_bundle, request):
    # NOT_APPLICABLE gate
    if not identity_bundle.primary_user_id:
        return NOT_APPLICABLE                       # no account → no deletion authorized
    if not is_deletion_request(request.request_text):
        return NOT_APPLICABLE                       # e.g., "export my data" or "verify my account"

    # INCOMPLETE triggers (any one flips to INCOMPLETE)
    remaining   = [f for f in facts if should_be_absent(f) and f.state == PRESENT]
    exposed_pii = [f for f in facts if f.state in {PRESENT, TOMBSTONE}
                   and f.direct_pii_present & redactable_fields(f) != ∅]
    not_anon    = [f for f in facts if f.required_treatment == ANONYMIZE and f.state != ANONYMIZED]
    active_flow = [fl for fl in flows if fl.is_active_at(audit_at)]
    restore_risk= [r for r in restore_risks if r.is_risk_at(audit_at)]

    if remaining or exposed_pii or not_anon or active_flow or restore_risk:
        return INCOMPLETE

    # COMPLETE gate — every retained record is still present (retention compliance)
    retained_missing = [f for f in facts if f.required_treatment == RETAIN and f.state != PRESENT]
    if retained_missing:
        # Records that should be retained are gone — still INCOMPLETE
        # (deletion went too far). Spec doesn't have a status for "over-deleted";
        # treat as INCOMPLETE with a finding that retention was violated.
        return INCOMPLETE

    return COMPLETE
```

### Edge cases
- **S1** All records gone, sync active → INCOMPLETE (active flow).
- **S2** All records gone, sync disabled, backup risk → INCOMPLETE (restore risk).
- **S3** Tombstone redacted properly, but email_hash lingers in tombstone → INCOMPLETE (exposed PII).
- **S4** Account never existed but request asked for deletion → NOT_APPLICABLE (no account to delete; cannot prove a negative beyond the absence of an identity).
- **S5** `reported_status = PARTIALLY_COMPLETE` but everything is actually done and no active flow → COMPLETE.
- **S6** `request_text = "close my account but keep my orders per your retention policy"` → orders must remain; treat as RETAIN; COMPLETE only if orders are still PRESENT and PII in them is redacted per rules.
- **S7** A backup contains the data, but the backup retention expired at `T_exp < audit_at` and the backup file is verified absent → not a restore risk; potentially COMPLETE.
- **S8** A sync job ran *after* audit_at and recreated data → that post-audit event is *not* a finding at audit_at (state at audit_at is what's graded), but if the schedule was active *at* audit_at, the flow finding stands.
- **S9** Audit_at < requested_at → malformed case; emit NOT_APPLICABLE with empty steps (cannot audit a deletion not yet requested at audit time).
- **S10** Two distinct user_ids resolved from the case email (e.g., post-merge both are still in audit log) — both must be fully clean for COMPLETE.

---

## 8. Step Generation — The Ordering Rules

This is where sequence-accuracy points live. The ordering is *strict* and *mechanical* — write a sort key, don't try to be clever.

### Sort key within a case
```
sort_key(step) = (
    PHASE_ORDER[step.phase],            # FINDING=0, REMEDIATION=2, VERIFICATION=3 (yes, leave a gap)
    OP_ORDER[(phase, operation)],       # per the table order, NOT alphabetical
    step.system_id,                     # ascending
    step.resource_id,                   # ascending, lexicographic
)
```

The operation order **must mirror the table in the brief**:

| Phase | Op order |
|---|---|
| FINDING | REPORT_REMAINING_RECORD → REPORT_EXPOSED_PII → REPORT_ACTIVE_DATA_FLOW → REPORT_RESTORE_RISK |
| REMEDIATION | DISABLE_DATA_FLOW → BLOCK_RESTORE → DELETE_RECORD → REDACT_RECORD → ANONYMIZE_RECORD |
| VERIFICATION | VERIFY_RECORD_ABSENT → VERIFY_RECORD_PRESENT → VERIFY_RECORD_REDACTED → VERIFY_RECORD_ANONYMIZED → VERIFY_DATA_FLOW_DISABLED → VERIFY_RESTORE_BLOCKED |

### Per-status step construction

**COMPLETE** — only VERIFICATION, each must cite evidence:
- For every record that should be ABSENT (per rules): `VERIFY_RECORD_ABSENT, state=ABSENT, evidence_id=<real>`
- For every record that should be RETAINED: `VERIFY_RECORD_PRESENT, state=PRESENT, evidence_id=<real>`
- For every tombstone properly redacted: `VERIFY_RECORD_REDACTED, state=REDACTED, evidence_id=<real>`
- For every record that should be ANONYMIZED: `VERIFY_RECORD_ANONYMIZED, state=ANONYMIZED, evidence_id=<real>`
- For every flow that should be disabled: `VERIFY_DATA_FLOW_DISABLED, state=DISABLED, evidence_id=<real>`
- For every backup that should be blocked: `VERIFY_RESTORE_BLOCKED, state=BLOCKED, evidence_id=<real>`

**INCOMPLETE** — three blocks:
1. FINDING block (cite evidence):
   - One `REPORT_REMAINING_RECORD` per record that should be absent but is PRESENT.
   - One `REPORT_EXPOSED_PII` per record that is PRESENT/TOMBSTONE with redactable fields still present. *(Per the table, EXPOSED_PII is a separate finding from REMAINING_RECORD — emit both if both apply to the same resource. Confirm against sample_output.)*
   - One `REPORT_ACTIVE_DATA_FLOW` per active flow.
   - One `REPORT_RESTORE_RISK` per risky backup.
2. REMEDIATION block (evidence_id=""):
   - One `DISABLE_DATA_FLOW` per active flow.
   - One `BLOCK_RESTORE` per risky backup.
   - One `DELETE_RECORD` per record that should be absent and is PRESENT.
   - One `REDACT_RECORD` per record with remaining PII (after any DELETE on the same resource if both apply — see G2 below).
   - One `ANONYMIZE_RECORD` per record that should be anonymized and isn't.
3. VERIFICATION block (evidence_id=""):
   - For every proposed remediation, the matching verification:
     - DELETE_RECORD → VERIFY_RECORD_ABSENT
     - REDACT_RECORD → VERIFY_RECORD_REDACTED
     - ANONYMIZE_RECORD → VERIFY_RECORD_ANONYMIZED
     - DISABLE_DATA_FLOW → VERIFY_DATA_FLOW_DISABLED
     - BLOCK_RESTORE → VERIFY_RESTORE_BLOCKED
   - PLUS: for records that are *already* in the correct state (e.g., a record that's already absent, a tombstone already redacted, a flow already disabled), emit VERIFY steps too — the spec says "the checks that must pass afterward," and proving that already-correct things remain correct is part of a complete audit.

**NOT_APPLICABLE** — `steps_json = []` (empty array literal, not empty string).

### Edge cases
- **G1** Same resource has both a remaining-record finding and an exposed-PII finding → emit *both* findings (they're different operations per the table), then *both* remediations (DELETE_RECORD + REDACT_RECORD)? This is contradictory — you can't both delete and redact the same record. Resolve: if the required treatment is DELETE, only emit REMAINING_RECORD + DELETE_RECORD. If REDACT (tombstone or retention), emit EXPOSED_PII + REDACT_RECORD. So they don't co-occur on the same resource in practice. The taxonomy is constructed to avoid this.
- **G2** Same resource requires DELETE_RECORD (because raw record present) AND the same resource also has PII in a backup of itself — different `resource_id`s (the live record vs. the backup copy), so no conflict.
- **G3** Empty `steps_json` for COMPLETE is **wrong** — COMPLETE requires at least one VERIFY step per the brief's wording ("include only verification steps proving the current state"). If you genuinely have nothing to verify (e.g., no records ever existed), reconsider whether this is actually NOT_APPLICABLE.
- **G4** A system has no relevant records for the user → no findings, no verifications for that system. Don't pad.
- **G5** `steps_json` must be valid JSON. Use `json.dumps(steps, separators=(",", ":"))` and verify with `json.loads` before writing. The grader parses as JSON.
- **G6** Don't include trailing whitespace or BOM in the CSV. Don't quote `steps_json` unless your CSV writer insists; if it does, use RFC 4180 quoting (double quotes, doubled inner quotes).
- **G7** `case_id` output must be sorted ascending across the file (518 rows). Don't trust input order.

---

## 9. Self-Validator — Catch Your Own Mistakes Before the Grader Does

A pre-submit validator that re-reads `output.csv` and enforces every rule:

```
for each row:
    assert case_id is non-empty
    assert deletion_status in {COMPLETE, INCOMPLETE, NOT_APPLICABLE}
    steps = json.loads(steps_json)
    assert isinstance(steps, list)
    if status == NOT_APPLICABLE:
        assert steps == []
        continue
    assert all(s["step_no"] == i+1 for i, s in enumerate(steps))   # consecutive
    assert phases non-decreasing in {FINDING, REMEDIATION, VERIFICATION}
    assert operations respect per-phase table order
    assert (system_id, resource_id) ascending within (phase, operation)
    if status == COMPLETE:
        assert all(s.phase == VERIFICATION for s in steps)
        assert all(s.evidence_id != "" for s in steps)   # must cite
    if status == INCOMPLETE:
        for s in steps:
            if s.phase == FINDING: assert s.evidence_id != ""
            else:                  assert s.evidence_id == ""
    assert every (system_id, operation) tuple is allowed per the table
```

Plus a *coverage* check: every `(case_id, system_id, resource_id)` that the determinator flagged must appear in the steps; nothing extra.

---

## 10. Edge Case Catalog (Comprehensive)

| ID | Edge case | Handling |
|---|---|---|
| **E1** | Email in case row not found anywhere | NOT_APPLICABLE, `[]` |
| **E2** | Email is historical (replaced) | Resolve via audit_log; include old email in `all_emails` |
| **E3** | Email reused by two user_ids | Pick user_id whose ownership window contains `audit_at` |
| **E4** | Merge in audit_log | Treat both user_ids as same identity |
| **E5** | Email case/whitespace mismatch | Normalize before lookup |
| **E6** | Email hash in case row | Hash candidate emails and match |
| **T1** | `audit_at < requested_at` | NOT_APPLICABLE (audit before request) |
| **T2** | `audit_at < reported_at` but reported claims COMPLETE | Trust evidence at audit_at; likely INCOMPLETE |
| **T3** | Backup before deletion still in retention | REPORT_RESTORE_RISK |
| **T4** | Sync scheduled to run after audit_at | Active flow (per brief) |
| **T5** | Reported COMPLETE before actual deletion completed | INCOMPLETE |
| **T6** | Sync recreated data, then re-deleted before audit_at | Still INCOMPLETE (flow is active) |
| **R1** | Tombstone with `email_hash` lingering | REPORT_EXPOSED_PII + REDACT_RECORD |
| **R2** | Child record (orders) with shipping address | Apply rules to that record's category |
| **R3** | Backup expired/rotated | No restore risk |
| **R4** | Search index entry stale | REPORT_REMAINING_RECORD + DELETE_RECORD |
| **R5** | Immutable analytics export | DELETE_RECORD or ANONYMIZE_RECORD; cannot REDACT |
| **R6** | Logs with plaintext email | REDACT_RECORD (logs usually retained) |
| **R7** | Support attachment PDF with ID image | DELETE_RECORD (the file itself) |
| **F1** | Sync ran between deletion and audit, recreated | Both REMAINING_RECORD and ACTIVE_DATA_FLOW |
| **F2** | Sync scheduled but never ran | ACTIVE if recurring; otherwise check samples |
| **F3** | Flow disabled before audit_at | No finding; optionally VERIFY_DATA_FLOW_DISABLED |
| **F4** | Encrypted backup, key destroyed | Effectively blocked; emit VERIFY_RESTORE_BLOCKED if proven |
| **S1–S10** | See §7 | See §7 |
| **G1–G7** | See §8 | See §8 |
| **X1** | Evidence file referenced but missing on disk | Log in `evaluation/`; fall back to activity log (still a claim) — treat record as PRESENT (fail-safe for the user) |
| **X2** | Two evidence files contradict | Use timestamp ≤ audit_at closest; if equal, prefer system's own export |
| **X3** | `system_activity` row missing `activity_id` | Use `file_id` or `audit_id` from related rows; never empty evidence_id on COMPLETE |
| **X4** | Case row has duplicate `case_id` | Deduplicate, warn |
| **X5** | Output row count ≠ 518 | Validator refuses to write; investigate |
| **X6** | `steps_json` exceeds CSV cell size | Still fine; CSV has no hard limit, but ensure proper escaping |

---

## 11. Cost & Token Efficiency

518 cases × multiple systems × multiple evidence files = potentially 10k+ LLM calls if naive. Target: **≤ 1 call per evidence file, once**, plus optional batching.

### Strategy
1. **Pre-process evidence once.** Walk `evidence_files.csv` once, extract all PII mentions per file, cache by file hash. Subsequent case runs read from cache — 0 LLM calls.
2. **Filter post-extraction.** Don't send the case's identity bundle to the LLM; instead extract *all* emails/user_ids mentioned in the file, then filter in Python. This lets one extraction serve every case.
3. **Batch hard cases.** If a single PDF mentions many users, extract all in one call with a list output schema.
4. **Model tiering.** Use a cheap/fast model for extraction (Haiku-class); escalate to a stronger model only for genuinely ambiguous evidence (e.g., handwritten image, conflicting signals). Escalation rate should be <5%.
5. **No LLM for status/step generation.** Pure deterministic Python. This alone cuts token cost by ~90% vs. an LLM-everything approach.
6. **No LLM for identity resolution.** Pure Python on the CSVs.
7. **Cache prompt-response pairs** to `evaluation/usage_report.md` source data, so reruns for iteration are free.

### `evaluation/usage_report.md` schema
- Per model: provider, model name, # calls, input tokens, output tokens, total tokens, avg tokens/call, estimated cost.
- Overall: totals + per-case average (total / 518).
- Methodology: "Extraction LLM calls + 0 status/step LLM calls (deterministic)."

---

## 12. Evaluation Harness (Required in `evaluation/`)

The brief mandates `evaluation/evaluation_report.md` with: case-level status accuracy, step/field accuracy, sequence accuracy, ≥3 self-created cases, failures found + improvements made. Build this **before** final submission:

1. **Sample-derived tests.** `sample_deletion_requests.csv` + `sample_output.csv` = your gold set. Run your agent on samples, diff outputs programmatically (status, steps as JSON, sequence), produce a confusion matrix.
2. **Adversarial self-cases (≥3).** Hand-author cases targeting each trap:
   - A case where tombstone has `email_hash` lingering (tests R1).
   - A case where sync recreated data between deletion and audit (tests F1, T6).
   - A case where backup expired before audit_at (tests T3, R3, S7).
   - A NOT_APPLICABLE case with no matching user_id (tests E1, S4).
   - A case with merged user_ids (tests E4).
3. **Sequence-accuracy linter.** Run §9's validator on every output row; report any violations.
4. **Failure log.** As you iterate, every bug you fix goes into `evaluation_report.md` under "failures found and improvements made" with before/after.
5. **Identity-resolution unit tests.** A separate test file feeding synthetic audit_logs to the identity resolver and asserting the bundle.

---

## 13. Deliverable Checklist

- [ ] `code.zip` containing:
  - [ ] `README.md` — architecture, run instructions, design decisions, precedence rules
  - [ ] `agent/` — the orchestrator + modules (identity, evidence, state, policy, status, steps, validator)
  - [ ] `prompts/` — the LLM extraction prompts (versioned, schema-validated)
  - [ ] `config/` — model config, cache path, output path (no API keys)
  - [ ] `evaluation/evaluation_report.md` — case/step/sequence accuracy, ≥3 self-cases, failures+improvements
  - [ ] `evaluation/usage_report.md` — per-model and overall token usage + cost
  - [ ] `scripts/` — reproducible run scripts (`run_all.py`, `validate.py`)
- [ ] `output.csv` — exactly 518 rows, sorted by `case_id`, `steps_json` valid JSON
- [ ] `chat_transcript` — the development conversation
- [ ] AI interview prep — be ready to defend every design choice in §0–§10

---

## 14. What to Do Next

I'd suggest the following execution order when you're ready to build:

1. **Scaffold the repo** with the §1 architecture; stub every module with a typed signature.
2. **Build identity resolution + sample validator first.** Run against `sample_deletion_requests.csv`; you should be able to score 100% on identity-only sub-checks before touching LLMs.
3. **Build the deterministic state machine + policy engine.** Run against samples using *only* `system_activity.csv` and the CSVs — skip evidence files initially. This gives you a baseline accuracy.
4. **Add evidence ingestion.** Start with JSON + SQLite (cheapest), then logs, then PDFs, then images. Re-run samples after each addition.
5. **Tune the step generator + self-validator.** This is where the last 10–20% of points live.
6. **Run the full 518**, write the evaluation report, package, submit.
