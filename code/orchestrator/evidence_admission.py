"""Request-time checks on parsed evidence before state reconstruction."""

from datetime import datetime, timezone
from copy import deepcopy

from agent.evidence.handlers.common import dt


def _parse_time(value):
    parsed = value if isinstance(value, datetime) else dt(value)
    if parsed is not None and parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _is_negative_lookup(record) -> bool:
    if record.state_at_evidence != "ABSENT":
        return False
    raw = record.raw_row
    if not isinstance(raw, dict):
        return False
    event = str(raw.get("event") or "").casefold()
    if not event:
        import re

        match = re.search(r"\bevent=([\w-]+)", str(raw.get("line") or ""), re.I)
        event = match.group(1).casefold() if match else ""
    return event.endswith("lookup_completed") and (
        str(raw.get("rows")) == "0"
        or str(raw.get("http_status")) == "404"
        or "rows=0" in str(raw.get("line") or "")
        or "http_status=404" in str(raw.get("line") or "")
    )


def exclude_stale_negative_lookups(evidence, requested_at) -> int:
    """A pre-request lookup miss cannot verify the later requested deletion.

    This changes only log query results. Snapshot rows and direct owner-bearing
    records retain their normal state timeline. Each exclusion is noted on the
    evidence object so the diagnostic trace explains the omitted claim.
    """
    requested = _parse_time(requested_at)
    if requested is None:
        return 0
    excluded = 0
    for item in evidence:
        if item.extraction_method != "regex-log":
            continue
        kept = []
        removed = 0
        for record in item.records:
            stamp = _parse_time(record.evidence_timestamp)
            if stamp is not None and stamp < requested and _is_negative_lookup(record):
                removed += 1
            else:
                kept.append(record)
        if removed:
            item.records = kept
            item.notes.append(f"stale_negative_lookup_before_request:{removed}")
            excluded += removed
    return excluded


def affiliate_absent_readbacks_from_later_owner(evidence, identity, audit_at) -> int:
    """Use a later direct owner row only to identify an earlier exact-ID 404.

    A post-audit record never supplies the audit-time state. The earlier
    ownerless ABSENT readback supplies that state. Both system and complete
    resource ID must agree, and the later owner must be explicit in its row.
    Query selectors, log mentions and model-only owner claims do not qualify.
    """
    cutoff = _parse_time(audit_at)
    if cutoff is None:
        return 0
    known_ids = {str(value) for value in getattr(identity, "all_user_ids", ())}
    known_emails = {str(value).strip().casefold() for value in getattr(identity, "all_emails", ())}
    direct_fields = {"user_id", "user_uuid", "customer_reference", "account_id", "email", "user_email", "customer_email", "owner_email"}
    future_owners = {}
    for item in evidence:
        if item.extraction_method not in {"json", "sqlite"}:
            continue
        for record in item.records_post_audit:
            stamp = _parse_time(record.evidence_timestamp)
            if stamp is None or stamp <= cutoff or not isinstance(record.raw_row, dict):
                continue
            owners = {str(value) if str(value) in known_ids else identity.primary_user_id
                      for key, value in record.raw_row.items()
                      if key.casefold() in direct_fields and value is not None
                      and (str(value) in known_ids or str(value).strip().casefold() in known_emails)}
            if len(owners) != 1 or None in owners:
                continue
            future_owners.setdefault((record.system_id, record.resource_id), set()).add((next(iter(owners)), item.file_id))
    joined = 0
    for item in evidence:
        additions = []
        for record in item.records:
            if record.user_ref or record.state_at_evidence != "ABSENT":
                continue
            stamp = _parse_time(record.evidence_timestamp)
            if stamp is None or stamp > cutoff:
                continue
            possible = future_owners.get((record.system_id, record.resource_id), set())
            normalized = {owner for owner, _ in possible}
            if len(normalized) != 1:
                continue
            owner = next(iter(normalized))
            if owner not in known_ids:
                continue
            linked = deepcopy(record)
            linked.user_ref = owner
            linked.raw_row = dict(record.raw_row)
            linked.raw_row["affiliation_source"] = sorted(file_id for _, file_id in possible)
            linked.raw_row["affiliation_method"] = "post_audit_direct_owner_exact_resource"
            additions.append(linked)
        if additions:
            item.records.extend(additions)
            item.notes.append(f"post_audit_direct_owner_exact_resource:{len(additions)}")
            joined += len(additions)
    return joined
