"""Bounded mini-model tool-planning loop for ambiguous, already-extracted evidence.

Tools only re-read repository evidence. Their output is diagnostic, never a new
ResourceFact: admission into the audit remains the source-grounded handlers.
"""

import json
from collections import defaultdict
from pathlib import Path

from .database_inspector import inspect_database, ownership_rows
from .image_inspector import run_tesseract
from .log_inspector import inspect_log
from .pdf_inspector import inspect_pdf

TOOL_FOR_SUFFIX = {".png": "inspect_image", ".jpg": "inspect_image", ".jpeg": "inspect_image",
                   ".json": "inspect_json", ".sql": "inspect_sql", ".log": "inspect_log", ".txt": "inspect_log",
                   ".pdf": "inspect_pdf"}
PLAN_SCHEMA = {
    "name": "northstar_audit_tool_plan", "strict": True,
    "schema": {"type": "object", "additionalProperties": False,
               "required": ["tool", "file_id", "reason"],
               "properties": {"tool": {"type": "string", "enum": ["inspect_image", "inspect_json", "inspect_sql", "inspect_log", "inspect_pdf", "stop"]},
                              "file_id": {"type": "string"}, "reason": {"type": "string"}}},
}


def review_candidates(evidence):
    """Only source anomalies and incompatible claims deserve another read."""
    candidates = set()
    by_resource = defaultdict(list)
    for item in evidence:
        if any(note in {"missing_file", "unsupported_extension", "vision_candidate_without_owned_record",
                        "vision_schema_failed_after_retry", "vlm_json_parse_failed_twice"}
               for note in item.notes):
            candidates.add(item.file_id)
        for rec in item.records:
            if rec.system_id in {"unknown", "image"}:
                candidates.add(item.file_id)
            by_resource[(rec.system_id, rec.resource_id, rec.user_ref.casefold())].append((item.file_id, rec.state_at_evidence))
    for claims in by_resource.values():
        if len({state for _, state in claims}) > 1:
            candidates.update(file_id for file_id, _ in claims)
    return sorted(candidates)


def _execute(tool, path, identity):
    identifiers = set(identity.all_user_ids) | set(identity.all_emails) | set(getattr(identity, "all_email_hashes", ()))
    if tool == "inspect_json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        exact = []
        def walk(node, prefix="$", parent=None):
            if isinstance(node, dict):
                for key, value in node.items():
                    walk(value, f"{prefix}.{key}", key)
            elif isinstance(node, list):
                for number, value in enumerate(node):
                    walk(value, f"{prefix}[{number}]", parent)
            elif isinstance(node, str) and node.casefold().strip("<>") in {str(x).casefold() for x in identifiers}:
                exact.append({"field_path": prefix, "field_name": parent, "value": node})
        walk(data)
        return {"exact_identifier_fields": exact[:40], "exact_identifier_count": len(exact)}
    if tool == "inspect_image":
        text = run_tesseract(path)
        return {"ocr_text": text[:6000], "ocr_characters": len(text)}
    if tool == "inspect_sql":
        schema = inspect_database(path)
        matches = ownership_rows(path, identifiers)
        return {"tables": schema["tables"], "notes": schema["notes"],
                "exact_owner_rows": [{"table": row["table"], "resource_id": row["resource_id"],
                                      "owner_columns": row["columns"]} for row in matches[:30]]}
    if tool == "inspect_log":
        report = inspect_log(path)
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        matched = [line[:500] for line in lines if any(str(identifier).casefold() in line.casefold() for identifier in identifiers)]
        return {"line_count": report["line_count"], "formats": report["formats"],
                "identifier_lines": matched[:12], "identifier_line_count": len(matched)}
    if tool == "inspect_pdf":
        report = inspect_pdf(path)
        return {"page_count": report["page_count"], "pages": [
            {"page": page["page"], "text": page["text"][:2400], "tables": page["tables"][:5],
             "scanned": page["scanned"]} for page in report["pages"]]}
    raise ValueError("unrecognized review tool")


def supervise_evidence(case_id, evidence, manifest, identity, root, llm_client, max_rounds=2):
    """Let mini choose read-only tools; reject nonexistent or format-incompatible plans."""
    by_id = {row["file_id"]: row for row in manifest}
    candidates = [file_id for file_id in review_candidates(evidence) if file_id in by_id]
    if not candidates:
        return []
    evidence_root = (Path(root) / "dataset" / "evidence").resolve()
    history = []
    used = set()
    for _ in range(max(0, min(max_rounds, 3))):
        available = [file_id for file_id in candidates if file_id not in used]
        if not available:
            break
        compact = [{"file_id": file_id, "tool": TOOL_FOR_SUFFIX.get(Path(by_id[file_id]["file_path"]).suffix.casefold()),
                    "notes": next((e.notes for e in evidence if e.file_id == file_id), [])}
                   for file_id in available[:12]]
        if llm_client is not None and llm_client.enabled:
            prompt = ("Choose one read-only evidence inspection tool for an ambiguous deletion audit. "
                      "Only choose a listed file and its listed tool; stop if no useful inspection remains. "
                      "The tool result does not authorize inventing a resource owner. Return JSON only. "
                      f"Candidates: {json.dumps(compact)}. Previous tool results: {json.dumps(history[-1:], default=str)[:2600]}")
            raw = llm_client.call(prompt, "audit_tool_plan", case_id=case_id,
                                  model="gpt-4o-mini", max_tokens=220, response_schema=PLAN_SCHEMA)
            try:
                plan = json.loads(raw)
            except (ValueError, TypeError):
                plan = {}
            if isinstance(plan, dict) and plan.get("tool") == "stop":
                break
            if not isinstance(plan, dict):
                plan = {}
            file_id, tool = plan.get("file_id"), plan.get("tool")
        else:
            file_id = available[0]
            tool = TOOL_FOR_SUFFIX.get(Path(by_id[file_id]["file_path"]).suffix.casefold())
        if file_id not in available or tool != TOOL_FOR_SUFFIX.get(Path(by_id[file_id]["file_path"]).suffix.casefold()):
            history.append({"file_id": str(file_id), "error": "rejected_unlisted_or_wrong_tool"})
            file_id = available[0]
            tool = TOOL_FOR_SUFFIX.get(Path(by_id[file_id]["file_path"]).suffix.casefold())
            if tool is None:
                break
        used.add(file_id)
        path = (Path(root) / "dataset" / by_id[file_id]["file_path"]).resolve()
        if not path.is_relative_to(evidence_root) or not path.is_file():
            history.append({"file_id": file_id, "tool": tool, "error": "missing_or_outside_evidence_root"})
            continue
        try:
            result = _execute(tool, path, identity)
            history.append({"file_id": file_id, "tool": tool, "result": result})
        except (OSError, ValueError, RuntimeError) as exc:
            history.append({"file_id": file_id, "tool": tool, "error": type(exc).__name__})
    return history
