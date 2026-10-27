"""Read identity-linked resource observations from structured service logs.

Query/start events establish an exact trace owner but never establish record
presence. Only a resource-bearing observation can become a RecordState.
"""

import json
import re
from pathlib import Path

from ..ir import PIIHit, RecordState
from .common import dt, email_hashes


TS = re.compile(r"\b20\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z\b")
FIELD = re.compile(r'(?<![\w-])([A-Za-z_][\w-]*)[:=](?:"([^"]*)"|([^\s|,}\"]+))')
TAG = re.compile(r"\[([a-z][\w-]+_(?:service|platform|index|store|replica))\]")
BRACKET_TRACE = re.compile(r"\[(tr-[\w-]+)\]")
SYSLOG = re.compile(r"\bnode-[\w-]+\s+([a-z][\w-]+)\s+(tr-[\w-]+)\s+-\s+-")
OWNER_FIELDS = {
    "user_id", "user_uuid", "customer_reference", "subject_reference",
    "subject_ref", "customer_email", "owner_email", "requester_email",
    "email", "user_email", "email_hash", "hashed_email", "email_sha256",
    "lookup_key", "match_key", "subject_key",
    "matched_value", "correlation_key", "owner_key", "scan_key",
}
QUERY_FIELDS = {"lookup_key", "match_key", "subject_key", "correlation_key",
                "owner_key", "scan_key"}
STATES = {"PRESENT", "ABSENT", "REDACTED", "ANONYMIZED", "TOMBSTONE"}
NEGATIVE_RESULTS = {"NOT_FOUND", "MISSING", "DELETED", "MISS", "ABSENT"}
LOG_LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "WARNING", "ERROR"}


def _fields(line):
    """Parse quoted, unquoted and once-escaped key/value attributes."""
    normalized = line.replace('\\"', '"')
    normalized = re.sub(r'\bmessage="(?=[A-Za-z_][\w-]*=)', '', normalized)
    found = {name.casefold(): quoted if quoted != "" else bare or ""
             for name, quoted, bare in FIELD.findall(normalized)}
    if "{" in line:
        try:
            payload = json.loads(line[line.index("{"):])
        except json.JSONDecodeError:
            payload = None
        if isinstance(payload, dict):
            found.update({str(key).casefold(): value for key, value in payload.items()})
    # Key/value logs spell booleans as text, while JSON logs already carry
    # booleans. State reconstruction needs the same typed value from either
    # format before it can honor an explicit connector or restore setting.
    for key in ("enabled", "restore_allowed"):
        value = found.get(key)
        if isinstance(value, str) and value.casefold() in {"true", "false"}:
            found[key] = value.casefold() == "true"
    return found


def _event(line, number):
    fields = _fields(line)
    stamp_match = TS.search(line)
    stamp = dt(fields.get("timestamp") or fields.get("observed_at"))
    if stamp is None and stamp_match:
        stamp = dt(stamp_match.group(0))
    parts = [part.strip() for part in line.split("|")]
    if len(parts) >= 6 and parts[1].upper() in LOG_LEVELS:
        # Operations stream: timestamp | severity | service | trace | event | kv
        fields.setdefault("service", parts[2])
        fields.setdefault("trace_id", parts[3])
        fields.setdefault("event", parts[4].rstrip(":"))
    elif len(parts) == 6 and re.fullmatch(r"[a-z][a-z0-9_]*_\d+", parts[2]):
        # Compact readback table: timestamp | system | resource | type | state | owner
        fields.setdefault("system", parts[1])
        fields.setdefault("resource_id", parts[2])
        fields.setdefault("record_type", parts[3])
        fields.setdefault("result", parts[4])
        fields.setdefault("subject_reference", parts[5])
    tag = TAG.search(line)
    bracket_trace = BRACKET_TRACE.search(line)
    syslog = SYSLOG.search(line)
    if tag:
        fields.setdefault("service", tag.group(1))
    if bracket_trace:
        fields.setdefault("trace_id", bracket_trace.group(1))
    if syslog:
        fields.setdefault("service", syslog.group(1))
        fields.setdefault("trace_id", syslog.group(2))
    if "event" not in fields and bracket_trace:
        after = line[bracket_trace.end():].strip()
        event_match = re.match(r"([\w-]+)\s*:", after)
        if event_match:
            fields["event"] = event_match.group(1)
    # In record-lookup exports, service is the reader. The system is the actual
    # target of the observation and must win over the reader's service name.
    system = (fields.get("system_id") or fields.get("system") or
              fields.get("service") or fields.get("function"))
    trace = fields.get("trace_id") or fields.get("requestid") or ""
    return fields, stamp, str(system or ""), str(trace), number


def _owner_refs(fields, ids, emails, hashes):
    refs = set()
    for key in OWNER_FIELDS:
        value = fields.get(key)
        if value is None:
            continue
        candidate = str(value).strip()
        if candidate in ids:
            refs.add(candidate)
        elif candidate.casefold() in emails:
            refs.add(candidate.casefold())
        elif candidate.casefold() in hashes:
            refs.add(candidate.casefold())
    return refs


def _preferred_ref(refs, identities):
    ids = sorted(ref for ref in refs if ref in identities.all_user_ids)
    if ids:
        return ids[0]
    emails = sorted(ref for ref in refs if "@" in ref)
    if emails:
        return emails[0]
    return getattr(identities, "primary_user_id", None) or sorted(refs)[0]


def _state(fields, system):
    explicit = str(fields.get("state") or "").upper()
    result = str(fields.get("result") or "").upper()
    if str(fields.get("rows") or "") == "0" or str(fields.get("http_status") or "") == "404" or result in NEGATIVE_RESULTS:
        return "ABSENT"
    if explicit in STATES:
        return explicit
    if result in STATES:
        return result
    if (system == "support_platform" and fields.get("message_text") == "[REDACTED]"
            and all(str(fields.get(key, "")).casefold() in {"", "null", "none", "[redacted]"}
                    for key in ("requester_email", "requester_name", "requester_phone",
                                "email", "name", "phone", "email_hash"))):
        return "REDACTED"
    if (system == "analytics_platform" and str(fields.get("direct_identifiers") or "") == "0"
            and all(str(fields.get(key, "null")).casefold() in {"null", "none", ""}
                    for key in ("email", "phone", "email_hash"))):
        return "ANONYMIZED"
    return "PRESENT"


def _pii_hits(fields, state, event, ref, row, known_hashes):
    if state == "ABSENT":
        return []
    out = []
    for key, value in fields.items():
        if value is None:
            continue
        value = str(value).strip()
        if value.casefold() in {"", "null", "none", "[redacted]"}:
            continue
        if key in QUERY_FIELDS and value.casefold() in known_hashes:
            out.append(PIIHit(f"line[{row+1}].{key}", "email_hash",
                              value.casefold(), source_row=row))
            continue
        if key in QUERY_FIELDS or (key == "subject_reference" and event == "record_lookup"):
            continue
        kind = None
        if key in {"email", "customer_email", "user_email", "owner_email", "requester_email", "matched_value"} and "@" in value:
            kind = "email"
        elif key in {"name", "full_name", "requester_name", "first_name", "last_name"}:
            kind = "name"
        elif key in {"phone", "requester_phone", "mobile"}:
            kind = "phone"
        elif key in {"email_hash", "hashed_email", "email_sha256"}:
            kind = "email_hash"
        elif key in {"user_id", "user_uuid", "customer_reference", "subject_reference", "subject_ref"} and value == ref:
            kind = "user_id" if "@" not in value else "email"
        if kind:
            out.append(PIIHit(f"line[{row+1}].{key}", kind,
                              value.casefold() if kind == "email" else value,
                              source_row=row))
    return out


def extract(path: Path, file_id: str, identities, audit_at=None):
    """Return pre-audit and post-audit observations without cross-user joins."""
    cutoff = dt(audit_at) if isinstance(audit_at, str) else audit_at
    out, post = [], []
    trace_owner = {}
    trace_sources = {}
    known_ids = {str(value) for value in identities.all_user_ids}
    known_emails = {str(value).strip().casefold() for value in identities.all_emails}
    known_hashes = email_hashes(identities)
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    for i, line in enumerate(lines):
        fields, stamp, system, trace, _ = _event(line, i)
        direct = _owner_refs(fields, known_ids, known_emails, known_hashes)
        if trace and fields.get("source"):
            trace_sources.setdefault(trace, str(fields["source"]))
        if trace and direct:
            for ref in direct:
                trace_owner.setdefault(trace, []).append((stamp, ref))
        resource = str(fields.get("resource_id") or "").strip()
        event = str(fields.get("event") or "").casefold()
        if event.endswith("_started"):
            continue
        if not resource:
            # Keep the original minimal tagged-line behavior for plain log
            # fixtures; real structured source rows need a full resource ID.
            if not TAG.search(line) or not direct:
                continue
            resource = f"{file_id}_line_{i+1}"
        if not system:
            continue
        refs = set(direct)
        if trace:
            refs.update(ref for owner_stamp, ref in trace_owner.get(trace, [])
                        if owner_stamp is None or stamp is None or owner_stamp <= stamp)
        if not refs:
            continue
        ref = _preferred_ref(refs, identities)
        state = _state(fields, system)
        raw = dict(fields)
        raw["line"] = line
        raw["source_row"] = i
        raw["event"] = event
        if event == "attachment_pii_scan" and fields.get("file"):
            raw["record_type"] = "SUPPORT_ATTACHMENT"
        if event == "restore_authorization_completed" and str(fields.get("decision", "")).casefold() == "deny":
            raw["restore_allowed"] = False
        if (event == "restore_candidate_evaluated"
                and str(fields.get("eligible", "")).casefold() == "true"
                and str(fields.get("deletion_block", "")).casefold() == "false"):
            raw["restore_allowed"] = True
        if trace in trace_sources:
            raw["trace_source"] = trace_sources[trace]
        record = RecordState(system, resource, ref, state,
                             _pii_hits(fields, state, event, ref, i,
                                       known_hashes), stamp, raw)
        (post if cutoff and stamp and stamp > cutoff else out).append(record)
    return out, post
