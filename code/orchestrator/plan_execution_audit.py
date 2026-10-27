"""Audit a generated plan against its source-backed policy decisions.

This is an evaluation tool, not an answer generator.  It reads only the
participant input, a generated CSV, and the run's diagnostic traces.  It never
uses the public sample answers or hidden labels.
"""

import csv
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


FINAL_CHECK = {
    "DELETE_RECORD": "VERIFY_RECORD_ABSENT",
    "REDACT_RECORD": "VERIFY_RECORD_REDACTED",
    "ANONYMIZE_RECORD": "VERIFY_RECORD_ANONYMIZED",
    "RETAIN": "VERIFY_RECORD_PRESENT",
    "DISABLE_DATA_FLOW": "VERIFY_DATA_FLOW_DISABLED",
    "BLOCK_RESTORE": "VERIFY_RESTORE_BLOCKED",
}
FINDING = {
    "DELETE_RECORD": "REPORT_REMAINING_RECORD",
    "REDACT_RECORD": "REPORT_EXPOSED_PII",
    "ANONYMIZE_RECORD": "REPORT_EXPOSED_PII",
    "DISABLE_DATA_FLOW": "REPORT_ACTIVE_DATA_FLOW",
    "BLOCK_RESTORE": "REPORT_RESTORE_RISK",
}
REMEDIATION = {action: action for action in FINAL_CHECK if action != "RETAIN"}
POST_ACTION_STATE = {
    "DELETE_RECORD": "ABSENT", "REDACT_RECORD": "REDACTED",
    "ANONYMIZE_RECORD": "ANONYMIZED", "RETAIN": "PRESENT",
    "DISABLE_DATA_FLOW": "INACTIVE", "BLOCK_RESTORE": "BLOCKED",
}
RESOURCE_SYSTEM = {
    "account_": "account_service", "search_": "search_service",
    "analytics_": "analytics_platform", "data_flow_": "integration_service",
    "backup_": "backup_service", "audit_record_": "security_service",
    "legal_hold_": "legal_service", "export_": "export_service",
    "support_": "support_platform", "tombstone_": "identity_service",
}


def resource_role_conflict(system_id, resource_id):
    """Detect a control ID misinterpreted as a downstream record ID."""
    expected = next((system for prefix, system in RESOURCE_SYSTEM.items()
                     if resource_id.startswith(prefix)), None)
    if expected is None:
        return False
    # Some account tombstones retain account-service topology, and source
    # replica IDs are normalized before policy decisions.
    return system_id != expected


@dataclass
class CaseAudit:
    case_id: str
    status: str
    step_count: int
    verdict_count: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _verdict(value, system_id, resource_id, evidence_id):
    """Read the named fields from the diagnostic dataclass representation.

    The stable structured keys carry IDs; regex is limited to the five scalar
    fields absent from the older trace schema.  If a field is absent, fail the
    audit rather than treating it as compliant.
    """
    data = {"system_id": system_id, "resource_id": resource_id,
            "evidence_id": evidence_id}
    for key in ("target_kind", "required_action", "current_state"):
        match = re.search(r"\b" + key + r"='([^']*)'", value)
        if not match:
            raise ValueError(f"diagnostic verdict missing {key}")
        data[key] = match.group(1)
    match = re.search(r"\bis_in_compliance=(True|False)\b", value)
    if not match:
        raise ValueError("diagnostic verdict missing is_in_compliance")
    data["compliant"] = match.group(1) == "True"
    return data


def _last(events, phase, event):
    return next((row for row in reversed(events)
                 if row.get("phase") == phase and row.get("event") == event), None)


def audit_case(row, events, manifest_ids=frozenset(), activity_ids=frozenset()):
    """Replay obligations and check every step against the case trace."""
    case_id = row["case_id"]
    status = row["deletion_status"]
    steps = json.loads(row["steps_json"])
    result = CaseAudit(case_id, status, len(steps), 0)
    policy = _last(events, "policy", "apply")
    generation = _last(events, "steps", "generate")
    identity = _last(events, "identity", "resolve_identity")
    extraction = _last(events, "evidence", "extract_evidence")
    if not policy or not generation or not identity or not extraction:
        result.errors.append("incomplete_run_trace")
        return result
    if json.loads(generation["outputs"].get("steps_json", "[]")) != steps:
        result.errors.append("csv_and_run_trace_disagree")
        return result
    try:
        verdicts = [_verdict(item["value"], item["system_id"],
                             item["resource_id"], item.get("evidence_id", ""))
                    for item in policy["outputs"].get("verdicts", [])]
    except (KeyError, ValueError) as exc:
        result.errors.append(f"unreadable_policy_verdict:{exc}")
        return result
    result.verdict_count = len(verdicts)
    if status == "NOT_APPLICABLE":
        if steps:
            result.errors.append("non_deletion_has_steps")
        return result

    expected = Counter()
    obligations = 0
    for verdict in verdicts:
        action = verdict["required_action"]
        if action == "NONE":
            continue
        if action not in FINAL_CHECK:
            result.errors.append(f"unknown_policy_action:{action}")
            continue
        obligations += 1
        key = (verdict["system_id"], verdict["resource_id"])
        if status == "COMPLETE" and not verdict["compliant"]:
            result.errors.append(f"complete_with_violation:{key[0]}/{key[1]}")
        if status == "INCOMPLETE" and not verdict["compliant"]:
            if action == "RETAIN":
                # The allowed operation vocabulary has no restore/create action.
                result.warnings.append(f"retention_violation_has_no_repair:{key[0]}/{key[1]}")
            else:
                expected[("FINDING", *key, FINDING[action])] += 1
                expected[("REMEDIATION", *key, REMEDIATION[action])] += 1
        expected[("VERIFICATION", *key, FINAL_CHECK[action])] += 1
    actual = Counter((step["phase"], step["system_id"],
                      step["resource_id"], step["operation"]) for step in steps)
    for key, number in (expected - actual).items():
        result.errors.append(f"missing_plan_step:{key}:{number}")
    for key, number in (actual - expected).items():
        result.errors.append(f"unjustified_plan_step:{key}:{number}")
    # Execute only the state-changing operations actually present in the plan.
    # A final check that cannot pass after those operations is an open plan
    # obligation even if the step array is structurally valid.
    for verdict in verdicts:
        action = verdict["required_action"]
        if action not in FINAL_CHECK:
            continue
        system, resource = verdict["system_id"], verdict["resource_id"]
        simulated = verdict["current_state"]
        if action in REMEDIATION and actual[("REMEDIATION", system, resource, action)]:
            simulated = POST_ACTION_STATE[action]
        acceptable = {POST_ACTION_STATE[action]}
        if action == "REDACT_RECORD" and resource.startswith("tombstone_"):
            acceptable.add("TOMBSTONE")
        if (actual[("VERIFICATION", system, resource, FINAL_CHECK[action])]
                and simulated not in acceptable):
            result.errors.append(
                f"verification_cannot_pass_after_plan:{system}/{resource}:{simulated}")
    if status == "COMPLETE" and obligations == 0:
        result.warnings.append("complete_without_any_policy_obligation")
    if status == "COMPLETE" and not steps:
        result.warnings.append("complete_without_evidence_backed_verification")

    user_refs = set(identity["outputs"].get("all_user_ids", []))
    user_refs.update(identity["outputs"].get("all_emails", []))
    file_records = {}
    for file in extraction["outputs"].get("files", []):
        file_records[file["file_id"]] = file.get("records", [])
    for step in steps:
        if resource_role_conflict(step["system_id"], step["resource_id"]):
            result.warnings.append(
                f"resource_system_role_conflict:{step['system_id']}:{step['resource_id']}")
        citation = step["evidence_id"]
        if step["phase"] == "FINDING" and not citation:
            result.errors.append(f"finding_without_citation:{step['resource_id']}")
        if status == "COMPLETE" and step["phase"] == "VERIFICATION" and not citation:
            result.errors.append(f"complete_verification_without_citation:{step['resource_id']}")
        if status == "INCOMPLETE" and step["phase"] != "FINDING" and citation:
            result.errors.append(f"future_step_has_citation:{step['resource_id']}")
        if not citation:
            continue
        if citation in manifest_ids:
            records = file_records.get(citation, [])
            owned = any(record.get("system_id") == step["system_id"]
                        and record.get("resource_id") == step["resource_id"]
                        and record.get("user_ref") in user_refs
                        for record in records)
            if not owned:
                result.warnings.append(
                    f"citation_lacks_directly_owned_extracted_record:{citation}:{step['resource_id']}")
        elif citation not in activity_ids:
            result.warnings.append(f"citation_not_in_manifest_or_activity:{citation}")
    remediation_positions = [i for i, step in enumerate(steps)
                             if step["phase"] == "REMEDIATION"]
    early = {"DISABLE_DATA_FLOW", "BLOCK_RESTORE"}
    record_ops = {"DELETE_RECORD", "REDACT_RECORD", "ANONYMIZE_RECORD"}
    if any(steps[i]["operation"] in record_ops
           and any(steps[j]["operation"] in early and j > i
                   for j in remediation_positions) for i in remediation_positions):
        result.errors.append("flow_or_restore_block_after_record_mutation")
    return result


def audit_run(root, output_csv):
    root = Path(root)
    with Path(output_csv).open(encoding="utf-8-sig", newline="") as stream:
        output = list(csv.DictReader(stream))
    with (root / "dataset/evidence_files.csv").open(encoding="utf-8-sig", newline="") as stream:
        manifest_ids = {row["file_id"] for row in csv.DictReader(stream)}
    with (root / "dataset/system_activity.csv").open(encoding="utf-8-sig", newline="") as stream:
        activity_ids = {row["activity_id"] for row in csv.DictReader(stream)}
    result = []
    for row in output:
        path = root / "code/.cache/diagnostics" / f"{row['case_id']}.jsonl"
        if path.exists():
            events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                      if line.strip()]
        else:
            events = []
        result.append(audit_case(row, events, manifest_ids, activity_ids))
    return result


def write_report(root, output_csv, report_path=None):
    root = Path(root)
    audited = audit_run(root, output_csv)
    report_path = Path(report_path or root / "code/evaluation/plan_execution_audit.md")
    error_counts = Counter(error.split(":", 1)[0] for row in audited for error in row.errors)
    warning_counts = Counter(warning.split(":", 1)[0] for row in audited for warning in row.warnings)
    lines = ["# Full output plan execution audit", "",
             "Evaluation only. This source-backed replay checks all generated plans against their recorded policy obligations, simulates the listed remediation operations, and checks whether each final verification can pass. It does not read sample answers or hidden labels. It cannot certify undiscovered records or predict the HackerRank score.",
             "", f"Output: `{Path(output_csv).name}`; cases: {len(audited)}; policy verdicts: {sum(x.verdict_count for x in audited)}; steps: {sum(x.step_count for x in audited)}.",
             f"Cases with plan errors: {sum(bool(x.errors) for x in audited)}; with warnings: {sum(bool(x.warnings) for x in audited)}.",
             "", "## Error categories", "", "| category | occurrences |", "|---|---:|",
             *[f"| {key} | {value} |" for key, value in error_counts.most_common()],
             "", "## Warning categories", "", "| category | occurrences |", "|---|---:|",
             *[f"| {key} | {value} |" for key, value in warning_counts.most_common()],
             "", "## Affected cases", "", "| case | status | verdicts | steps | errors | warnings |",
             "|---|---|---:|---:|---|---|",
             *[f"| {x.case_id} | {x.status} | {x.verdict_count} | {x.step_count} | {'; '.join(x.errors) or '—'} | {'; '.join(x.warnings) or '—'} |"
               for x in audited if x.errors or x.warnings], ""]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path, audited


if __name__ == "__main__":
    import sys
    repo = Path(__file__).resolve().parents[2]
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else repo / "output.csv"
    path, cases = write_report(repo, output)
    print(f"{len(cases)} cases; {sum(bool(x.errors) for x in cases)} plan errors; "
          f"{sum(bool(x.warnings) for x in cases)} warning cases; report={path}")
    raise SystemExit(any(x.errors for x in cases))
