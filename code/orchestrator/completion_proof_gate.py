"""Keep an uncorroborated workflow claim from proving a COMPLETE audit."""

from dataclasses import replace


def guard_unverified_completion(decision, facts, verdicts, activities):
    """Return (decision, gaps); a gap becomes an INCOMPLETE future check.

    The bounded time rule can link an action to a person, but SUCCESS is still
    only a workflow claim. If a directly observed resource later corroborates
    the state, its ResourceFact cites that evidence and this gate does nothing.
    """
    if decision.deletion_status != "COMPLETE":
        return decision, []
    inferred_ids = {row.get("activity_id") for row in activities
                    if row.get("inference_method") == "unique_calibrated_report_window"}
    obligated = {(verdict.system_id, verdict.resource_id) for verdict in verdicts
                 if verdict.target_kind == "record" and verdict.required_action != "NONE"}
    gaps = sorted({(fact.system_id, fact.resource_id, fact.evidence_id)
                   for fact in facts
                   if fact.evidence_id in inferred_ids
                   and (fact.system_id, fact.resource_id) in obligated
                   and any("timeline-only" in note for note in fact.notes)})
    if not gaps:
        return decision, []
    detail = ",".join(resource for _, resource, _ in gaps)
    return replace(decision, deletion_status="INCOMPLETE",
                   audit_trail=[*decision.audit_trail,
                                f"unverified_workflow_account_requires_future_check:{detail}"]), gaps
