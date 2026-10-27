"""Full evidence-file inventory. Run: python code/orchestrator/dataset_catalog.py."""
import json
import csv
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

try:
    from .database_inspector import inspect_database
    from .database_inspector import ownership_rows
    from .pdf_inspector import inspect_pdf
    from .image_inspector import inspect_image
    from .log_inspector import inspect_log
except ImportError:
    from database_inspector import inspect_database
    from database_inspector import ownership_rows
    from pdf_inspector import inspect_pdf
    from image_inspector import inspect_image
    from log_inspector import inspect_log

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))


def json_field_paths(data):
    paths = set()
    def walk(value, prefix="$"):
        if isinstance(value, dict):
            for key, child in value.items():
                path = f"{prefix}.{key}"
                paths.add(path)
                walk(child, path)
        elif isinstance(value, list):
            for child in value:
                walk(child, prefix + "[]")
    walk(data)
    return sorted(paths)


def catalog_file(path, root=None, llm_client=None):
    path = Path(path)
    root = Path(root) if root else ROOT
    info = {"path": path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path),
            "bytes": path.stat().st_size, "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
            "type": path.suffix.lower().lstrip("."), "details": {}, "error": None}
    try:
        if info["type"] == "sql":
            info["details"] = inspect_database(path)
        elif info["type"] == "pdf":
            info["details"] = inspect_pdf(path)
        elif info["type"] in {"png", "jpg", "jpeg"}:
            info["details"] = inspect_image(path, llm_client)
        elif info["type"] in {"log", "txt"}:
            info["details"] = inspect_log(path)
        elif info["type"] == "json":
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            fields = json_field_paths(data)
            info["details"] = {"top_level_keys": sorted(data) if isinstance(data, dict) else [],
                "record_counts": {k: len(v) for k, v in data.items() if isinstance(v, list)} if isinstance(data, dict) else {"root": len(data) if isinstance(data, list) else 1},
                "field_paths": fields,
                "identity_fields": [p for p in fields if p.rsplit(".",1)[-1].casefold() in {"user_id","user_uuid","customer_reference","subject_reference","email","customer_email","requester_email","owner_email","email_hash"}],
                "resource_fields": [p for p in fields if p.rsplit(".",1)[-1].casefold() in {"resource_id","id","account_id","order_id"}],
                "time_fields": [p for p in fields if any(t in p.rsplit(".",1)[-1].casefold() for t in ("_at","timestamp","time"))],
                "state_fields": [p for p in fields if p.rsplit(".",1)[-1].casefold() in {"state","status","deleted","redacted","anonymized","enabled","restore_allowed"}],
                "sample": str(data)[:200]}
        else:
            info["details"] = {"notes": ["unknown format"]}
    except Exception as exc:
        info["error"] = f"{type(exc).__name__}: {exc}"
    return info


def catalog_dataset(root=None, llm_client=None):
    root = Path(root) if root else ROOT
    return [catalog_file(p, root, llm_client) for p in sorted((root / "dataset/evidence").rglob("*")) if p.is_file()]


def render_catalog(entries):
    counts = Counter(e["type"] for e in entries)
    lines = ["# Phase 17 evidence catalog", "", f"Files opened: **{len(entries)}**; bytes: **{sum(e['bytes'] for e in entries):,}**.", "",
             "| Type | Count |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(counts.items())]
    lines += ["", "## Every evidence file", "", "| File | Bytes | Modified (UTC) | Extracted datapoints / parser result |", "|---|---:|---|---|"]
    for entry in entries:
        detail = entry["details"]
        if entry["error"]:
            summary = "ERROR: " + entry["error"]
        elif entry["type"] == "sql":
            summary = "; ".join(f"{t['name']} ({t['row_count']} rows; columns {', '.join(t['columns'])}; owner columns {', '.join(t['ownership_columns']) or 'none'})" for t in detail["tables"]) or ", ".join(detail["notes"])
        elif entry["type"] == "pdf":
            summary = f"{detail['page_count']} pages; " + "; ".join(f"p{p['page']}: {p['text_length']} chars, {p['table_count']} tables, scanned={p['scanned']}, text={p['text'][:100].replace(chr(10),' ')}" for p in detail["pages"])
        elif entry["type"] in {"png", "jpg", "jpeg"}:
            summary = f"{detail['dimensions']} {detail['format']}; OCR chars={len(detail['ocr_text'])}; method={detail['method']}; EXIF={detail['exif_timestamp']}"
        elif entry["type"] in {"log", "txt"}:
            summary = f"{detail['line_count']} lines; formats={detail['formats']}; fields={','.join(detail['fields'])}; first={str(detail['first_lines'][:1])[:120]}; last={str(detail['last_lines'][-1:])[:120]}"
        elif entry["type"] == "json":
            summary = f"keys={','.join(detail['top_level_keys'])}; list lengths={detail['record_counts']}; identity={detail['identity_fields']}; resource={detail['resource_fields']}; time={detail['time_fields']}; state={detail['state_fields']}; paths={detail['field_paths']}"
        else:
            summary = str(detail)
        lines.append(f"| `{entry['path']}` | {entry['bytes']} | {entry['mtime']} | {summary.replace('|', '/')} |")
    return "\n".join(lines) + "\n"


def main(root=None):
    root = Path(root) if root else ROOT
    entries = catalog_dataset(root)
    target = root / "code/evaluation/dataset_catalog.md"
    target.write_text(render_catalog(entries), encoding="utf-8")
    print(f"Cataloged {len(entries)} files; errors: {sum(bool(e['error']) for e in entries)}; wrote {target}")
    return entries


GAP_TARGETS = {"case_01": "account_001", "case_02": "account_002",
               "case_03": "analytics_9406", "case_04": "account_004",
               "case_31": "account_4857"}


def audit_gap_cases(root=None):
    """Search every parseable source for direct exact subject/resource links."""
    from types import SimpleNamespace
    from agent.identity import load_default_resolver
    root = Path(root) if root else ROOT
    with (root / "dataset/sample_deletion_requests.csv").open(encoding="utf-8-sig", newline="") as f:
        cases = {r["case_id"]: r for r in csv.DictReader(f)}
    with (root / "dataset/evidence_files.csv").open(encoding="utf-8-sig", newline="") as f:
        manifest = list(csv.DictReader(f))
    resolver = load_default_resolver(root)
    lines = ["# Phase 17 deep ownership audit", "", "Exact full-resource and same-row/line identity checks across all 94 evidence files. File-level co-mention alone is not ownership.", ""]
    findings = {}
    for cid, target in GAP_TARGETS.items():
        row = cases[cid]
        identity = resolver.resolve(row["email"], row["audit_at"])
        identifiers = set(identity.all_user_ids) | set(identity.all_emails)
        target_files = []; subject_files = []; direct = []
        for item in manifest:
            path = root / "dataset" / item["file_path"]
            if not path.is_file():
                continue
            if path.suffix.lower() == ".sql":
                text = path.read_text(encoding="utf-8", errors="replace")
                matched = ownership_rows(path, identifiers)
                if matched:
                    subject_files.append(item["file_id"])
                for match in matched:
                    if match["resource_id"] == target:
                        direct.append((item["file_id"], match["table"], ",".join(match["columns"])))
            elif path.suffix.lower() == ".pdf":
                parsed = inspect_pdf(path)
                text = "\n".join(p["text"] for p in parsed["pages"])
                for p in parsed["pages"]:
                    for table in p["tables"]:
                        for cells in table:
                            joined = " ".join(str(c or "") for c in cells)
                            if target in joined and any(_exact_ref(i, joined) for i in identifiers):
                                direct.append((item["file_id"], f"page {p['page']} table", "exact identifier"))
            elif path.suffix.lower() in {".json", ".log", ".txt"}:
                text = path.read_text(encoding="utf-8-sig", errors="replace")
            else:
                continue  # Images are inspected visually and by OCR/Vision separately.
            if _exact_ref(target, text):
                target_files.append(item["file_id"])
            if any(_exact_ref(i, text) for i in identifiers):
                subject_files.append(item["file_id"])
            for n, line in enumerate(text.splitlines(), 1):
                if _exact_ref(target, line) and any(_exact_ref(i, line) for i in identifiers):
                    direct.append((item["file_id"], f"line {n}", "exact identifier"))
        findings[cid] = {"target": target, "direct": sorted(set(direct)),
                         "target_files": sorted(set(target_files)), "subject_files": sorted(set(subject_files))}
        lines += [f"## {cid}: {target}", "", f"Identity IDs: {', '.join(sorted(identity.all_user_ids))}; emails: {', '.join(sorted(identity.all_emails))}.",
                  f"Files with target ID: {', '.join(findings[cid]['target_files']) or 'none'}.",
                  f"Files with a subject identifier: {', '.join(findings[cid]['subject_files']) or 'none'}.",
                  f"Direct same-row/line ownership: {findings[cid]['direct'] or 'none'}.",
                  "Verdict: " + ("new direct signal; inspect before wiring" if direct else "no direct signal in machine-readable sources"), ""]
    lines += ["## Source-level adjudication of the five gold-only targets", "",
              "| Cases | Gold-required target | Source check | Result |", "|---|---|---|---|",
              "| 01, 02, 04 | `account_001`, `account_002`, `account_004`; gold cites `evidence_54` | `dataset/evidence/databases/customer_accounts_failover_replica_20260902.sql:13` has `account_005`, not any of these targets. No exact SQL owner row across the inventory. | No supplied ownership row. |",
              "| 03 | `analytics_9406` | `dataset/evidence/logs/resource_lookup_trace_20260926_103856.log:42-43` lists the target with null lookup key, customer reference, email, phone, and hash. The case subject appears elsewhere in that file. | File co-mention is not a join. |",
              "| 31 | `account_4857`; gold cites `evidence_51` | `dataset/evidence/records/customer_data_snapshot_bundle_20260915.json:4-10` has an empty `customer_profiles.records` list and no target ID. | An empty collection is not an identity-specific absent record. |", "",
              "## Image cross-check", "", "All 11 source PNGs were read by local RapidOCR and high-detail mini-Vision; the exact OCR text is in image_text_inventory.md. None supplies an exact same-row owner link for account_001, account_002, account_004, analytics_9406, or account_4857. The security-audit screenshot shows user_03 with audit records but not analytics_9406. The external Tesseract executable is unavailable, but RapidOCR works locally. A Vision assertion without independent corroboration is not ownership evidence.", "",
              "## Scope and inference limit", "", "SQL row/column equality, PDF table rows, and exact JSON/log line co-occurrence are checked. A line co-occurrence is a candidate, not automatic proof; file-level co-occurrence is explicitly rejected. This audit cannot prove the absence of data outside the supplied export. The five named gaps cap evidence-safe exact arrays at 27/32 if no new direct link is supplied.", ""]
    target = root / "code/evaluation/cases_01_02_03_04_31_audit.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    return findings


def _exact_ref(value, text):
    return bool(re.search(r"(?<![\w@.+-])" + re.escape(value) + r"(?![\w@.+-])", text, re.I))


if __name__ == "__main__":
    main()
