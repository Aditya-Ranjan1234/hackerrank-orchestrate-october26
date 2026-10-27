"""Apply manifest capture time only when a record has no intrinsic timestamp."""
from datetime import datetime, timezone


def _parse(value):
    if isinstance(value,datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    try:
        parsed=datetime.fromisoformat(str(value).replace("Z","+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except (ValueError,TypeError):
        return None


def apply_manifest_capture(evidence,manifest_row,audit_at):
    captured=_parse(manifest_row.get("captured_at"))
    cutoff=_parse(audit_at)
    if captured is None:
        return evidence
    retained=[]
    for record in evidence.records:
        if record.evidence_timestamp is None:
            record.evidence_timestamp=captured
            if cutoff and captured>cutoff:
                evidence.records_post_audit.append(record)
                continue
        retained.append(record)
    evidence.records=retained
    return evidence
