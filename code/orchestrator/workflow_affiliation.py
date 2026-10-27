"""Conservatively affiliate one unowned account workflow event to a request.

The report timestamp is used only as a correlation hint. It is never passed to
the status determinator, and the workflow's reported status is never read.
This rule is intentionally limited to a unique account DELETE across ALL
outcome classes inside a source-calibrated delay band. Only after finding
the unique action may its SUCCESS outcome be considered. Prefiltering by
SUCCESS produced false affiliations in independent owner controls.
"""

from copy import deepcopy
from datetime import datetime, timezone


MIN_REPORT_DELAY_SECONDS = 30 * 60
MAX_REPORT_DELAY_SECONDS = 90 * 60


def _dt(value):
    if isinstance(value, datetime):
        parsed = value
    else:
        try:
            parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except (TypeError, ValueError):
            return None
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)


def affiliate_unique_account_delete(activity_rows, identity, reported_at,
                                    requested_at, audit_at, evidence=(),
                                    known_account_owners=None,
                                    eligible_requester_count=None, trace=None):
    """Return originals plus at most one derived account deletion for a user.

    The caller has already run exact-resource evidence affiliation. Competing
    account deletes in the delay band cause abstention. Existing derived rows
    remain authoritative and are never replaced.
    """
    user = getattr(identity, "primary_user_id", None)
    report = _dt(reported_at)
    request = _dt(requested_at)
    cutoff = _dt(audit_at)
    expanded = list(activity_rows)
    def note(reason, candidates=()):
        if trace is not None:
            trace.append({"reason": reason,
                          "candidate_activity_ids": [row["activity_id"] for row in candidates]})
    if not user or not report or not request or not cutoff or report > cutoff:
        note("missing_identity_or_time")
        return expanded
    if eligible_requester_count is not None and eligible_requester_count != 1:
        note("ambiguous_requesters_at_report_time")
        return expanded
    ids = set(getattr(identity, "all_user_ids", ())) | set(getattr(identity, "all_emails", ()))
    if any(record.system_id == "account_service"
           and record.resource_id.startswith("account_") and record.user_ref in ids
           and (_dt(record.evidence_timestamp) is None
                or _dt(record.evidence_timestamp) <= cutoff)
           for source in evidence for record in source.records):
        note("already_has_directly_owned_account")
        return expanded
    known_account_owners = known_account_owners or {}
    candidates = []
    for row in activity_rows:
        if row.get("derived"):
            continue
        if row.get("target_user_id") or row.get("user_id"):
            continue
        if (row.get("source_system") != "deletion_worker"
                or row.get("target_system") != "account_service"
                or row.get("event_type") != "DELETE_RECORD"
                or not str(row.get("resource_id", "")).startswith("account_")):
            continue
        event_time = _dt(row.get("event_time"))
        if not event_time or not request <= event_time <= cutoff:
            continue
        delta = (report - event_time).total_seconds()
        owner = known_account_owners.get(row["resource_id"])
        if (MIN_REPORT_DELAY_SECONDS <= delta <= MAX_REPORT_DELAY_SECONDS
                and (not owner or owner in getattr(identity, "all_user_ids", ()))):
            candidates.append(row)
    if len(candidates) != 1:
        note("no_eligible_account_action" if not candidates else "competing_account_actions",
             candidates)
        return expanded
    winner = candidates[0]
    if str(winner.get("reported_result", "")).upper() != "SUCCESS":
        note("unique_action_not_successful", candidates)
        return expanded
    if any(row.get("original_activity_id") == winner.get("activity_id")
           and row.get("target_user_id") == user for row in activity_rows):
        note("exact_affiliation_already_present", candidates)
        return expanded
    derived = deepcopy(winner)
    derived["activity_id"] = f"{winner['activity_id']}::derived_report_window_for_{user}"
    derived["target_user_id"] = user
    derived["derived"] = True
    derived["original_activity_id"] = winner["activity_id"]
    derived["inference_method"] = "unique_calibrated_report_window"
    derived["details"] = f"{winner.get('details', '')} derived_for={user}"
    expanded.append(derived)
    note("derived_unique_calibrated_report_window", candidates)
    return expanded
