"""Source-literal citation check for generated steps; never reads sample gold."""

import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

from .image_inspector import run_tesseract
from .pdf_inspector import inspect_pdf
from agent.identity import load_default_resolver
from agent.evidence.handlers.common import email_hashes


IDENTIFIER = re.compile(r"(?<![\w-])([a-z][a-z0-9]*(?:_[a-z0-9]+)*_\d+)(?![\w-])", re.I)


def _capture_after_audit(captured_at, audit_at):
    if not captured_at or not audit_at:
        return False
    try:
        captured = datetime.fromisoformat(captured_at.replace("Z", "+00:00"))
        cutoff = datetime.fromisoformat(audit_at.replace("Z", "+00:00"))
        return captured > cutoff
    except ValueError:
        return False


def _rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def _visible_resource_ids(path):
    if path.suffix.casefold() in {".png", ".jpg", ".jpeg"}:
        text = run_tesseract(path)
    elif path.suffix.casefold() == ".pdf":
        parsed = inspect_pdf(path)
        text = "\n".join(
            page["text"] + "\n" + "\n".join(" ".join(str(cell or "") for cell in row)
                                                 for table in page["tables"] for row in table)
            for page in parsed["pages"]
        )
    else:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    return {match.group(1).casefold() for match in IDENTIFIER.finditer(text)}


def _verified_log_line_handle(path, citation, resource, identity):
    if identity is None or path.suffix.casefold() not in {".log", ".txt"}:
        return False
    match = re.fullmatch(re.escape(citation) + r"_line_(\d+)", resource)
    if not match:
        return False
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    number = int(match.group(1))
    if number < 1 or number > len(lines):
        return False
    line = lines[number - 1]
    id_match = any(re.search(r"(?<![\w-])" + re.escape(str(value)) + r"(?![\w-])", line)
                   for value in identity.all_user_ids)
    email_match = any(re.search(r"(?<![\w@.+-])" + re.escape(str(value)) + r"(?![\w@.+-])", line, re.I)
                      for value in identity.all_emails)
    hash_match = any(re.search(r"(?<!\w)" + re.escape(str(value)) + r"(?!\w)", line, re.I)
                     for value in email_hashes(identity))
    return bool(id_match or email_match or hash_match)


def audit_citations(root, output_csv=None):
    root = Path(root)
    output_csv = Path(output_csv) if output_csv else root / "output.csv"
    manifest = {row["file_id"]: row for row in _rows(root / "dataset/evidence_files.csv")}
    activities = {row["activity_id"]: row for row in _rows(root / "dataset/system_activity.csv")}
    identity_audits = {row["audit_id"] for row in _rows(root / "dataset/user_audit_log.csv")}
    requests_path = root / "dataset/deletion_requests.csv"
    requests = {row["case_id"]: row for row in _rows(requests_path)} if requests_path.is_file() else {}
    resolver = load_default_resolver(root) if requests else None
    visible = {}
    problems = []
    counts = Counter()
    for case in _rows(output_csv):
        request = requests.get(case["case_id"])
        identity = resolver.resolve(request["email"], request["audit_at"]) if resolver and request else None
        for step in json.loads(case["steps_json"]):
            citation = step.get("evidence_id") or ""
            if not citation:
                continue
            counts["cited_steps"] += 1
            resource = str(step.get("resource_id") or "")
            if citation in manifest:
                counts["evidence_file_citations"] += 1
                row = manifest[citation]
                if request and _capture_after_audit(row.get("captured_at"), request.get("audit_at")):
                    counts["retrospectively_captured_file_citations"] += 1
                path = (root / "dataset" / row["file_path"]).resolve()
                if citation not in visible:
                    visible[citation] = _visible_resource_ids(path) if path.is_file() else set()
                if resource.casefold() not in visible[citation] and _verified_log_line_handle(path, citation, resource, identity):
                    counts["verified_log_line_handles"] += 1
                elif resource.casefold() not in visible[citation]:
                    from .catalog_aliases import catalog_record, artifact_text
                    alias_proof=False
                    if identity is not None and request and path.suffix.lower() in {'.pdf','.png','.jpg','.jpeg'}:
                        text=artifact_text(str(path))
                        alias_proof=any(
                            (record:=catalog_record(a,text,identity,row['captured_at'],request['audit_at'])) is not None
                            and record.resource_id==resource and record.system_id==step['system_id']
                            for a in activities.values() if a.get('resource_id')==resource)
                    if alias_proof:
                        counts['verified_catalog_alias_citations']+=1
                    else:
                        problems.append((case["case_id"], citation, resource, "resource_id_not_visible_in_cited_file"))
            elif citation in activities:
                counts["activity_citations"] += 1
                if resource != activities[citation].get("resource_id"):
                    problems.append((case["case_id"], citation, resource, "activity_resource_id_mismatch"))
            elif citation in identity_audits:
                counts["identity_audit_citations"] += 1
            else:
                problems.append((case["case_id"], citation, resource, "unknown_citation_id"))
    counts["source_files_opened"] = len(visible)
    return counts, problems


def write_report(root, output_csv=None):
    counts, problems = audit_citations(root, output_csv)
    target = Path(root) / "code/evaluation/citation_audit.md"
    lines = [
        "# Output citation source audit", "",
        "Checks the generated `output.csv` against the evidence manifest, activity IDs and identity audit IDs. It never opens `sample_output.csv`. For an evidence-file citation, the complete resource ID must be visible in that file's text, PDF extraction or local image OCR, or an exact visible artifact alias must be independently linked by a pre-audit catalog activity with compatible ownership. Generated log-line handles are accepted only when the cited line exists and contains an exact identifier for the case. Image OCR gaps can be false negatives and require visual review.",
        "A separate count identifies citations to files captured after audit_at. Such files may contain older timestamped observations; their capture date alone does not tell whether the cited row reflects audit-time state. Review this count when applying the repository's evidence cutoff rule.",
        "", "| Measure | Count |", "|---|---:|",
        *[f"| {key} | {value} |" for key, value in sorted(counts.items())],
        "", f"Potential citation issues: {len(problems)}.",
        "", "| case | citation | resource | issue |", "|---|---|---|---|",
        *[f"| {case} | `{citation}` | `{resource}` | {kind} |" for case, citation, resource, kind in problems[:100]],
        "",
    ]
    target.write_text("\n".join(lines), encoding="utf-8")
    return target, counts, problems


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    target, counts, problems = write_report(root)
    print(f"{counts['cited_steps']} citations; {len(problems)} potential issues; report={target}")
    raise SystemExit(bool(problems))
