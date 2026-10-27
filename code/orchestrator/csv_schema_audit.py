"""Read-only structure check for every supplied CSV, isolated from production."""

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SPECS = {
    "deletion_requests.csv": ("case_id", "email", "requested_at", "reported_status", "reported_at", "audit_at", "request_text"),
    "sample_deletion_requests.csv": ("case_id", "email", "requested_at", "reported_status", "reported_at", "audit_at", "request_text"),
    "sample_output.csv": ("case_id", "deletion_status", "steps_json"),
    "output.csv": ("case_id", "deletion_status", "steps_json"),
    "user_identities.csv": ("user_id", "name", "email", "phone", "email_hash", "updated_at"),
    "user_audit_log.csv": ("audit_id", "user_id", "event_time", "field_name", "old_value", "new_value"),
    "system_activity.csv": ("activity_id", "event_time", "event_type", "source_system", "target_system", "resource_id", "reported_result", "details"),
    "deletion_rules.csv": ("rule_id", "data_category", "condition", "required_action"),
    "evidence_files.csv": ("file_id", "file_path", "origin", "captured_at"),
}
KEYS = {
    "deletion_requests.csv": "case_id",
    "sample_deletion_requests.csv": "case_id",
    "sample_output.csv": "case_id",
    "user_identities.csv": "user_id",
    "user_audit_log.csv": "audit_id",
    "system_activity.csv": "activity_id",
    "deletion_rules.csv": "rule_id",
    "evidence_files.csv": "file_id",
}
TIME_FIELDS = {"requested_at", "reported_at", "audit_at", "updated_at", "event_time", "captured_at"}
EVIDENCE_SUFFIXES = {".sql", ".json", ".log", ".txt", ".pdf", ".png", ".jpg", ".jpeg"}


@dataclass
class CSVCheck:
    name: str
    headers: tuple[str, ...]
    rows: int
    malformed_rows: int
    duplicate_keys: int
    invalid_timestamps: int
    errors: list[str]


def check_csv(path: Path, expected: tuple[str, ...], key: str | None = None) -> CSVCheck:
    if not path.is_file():
        return CSVCheck(path.name, (), 0, 0, 0, 0, ["missing_file"])
    errors = []
    malformed = duplicate = bad_time = count = 0
    seen = set()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        headers = tuple(reader.fieldnames or ())
        if headers != expected:
            errors.append("schema_mismatch")
        if len(headers) != len(set(headers)):
            errors.append("duplicate_header")
        for row in reader:
            count += 1
            if None in row or any(value is None for value in row.values()):
                malformed += 1
            if key and key in row:
                value = row[key]
                if value in seen:
                    duplicate += 1
                seen.add(value)
            for field in TIME_FIELDS.intersection(row):
                value = row[field]
                if value:
                    try:
                        datetime.fromisoformat(value.replace("Z", "+00:00"))
                    except ValueError:
                        bad_time += 1
    if malformed:
        errors.append(f"malformed_rows:{malformed}")
    if duplicate:
        errors.append(f"duplicate_keys:{duplicate}")
    if bad_time:
        errors.append(f"invalid_timestamps:{bad_time}")
    return CSVCheck(path.name, headers, count, malformed, duplicate, bad_time, errors)


def audit_dataset(root: Path) -> tuple[list[CSVCheck], list[str]]:
    root = Path(root)
    checks = [check_csv(root / "dataset" / name, expected, KEYS.get(name)) for name, expected in SPECS.items()]
    errors = [f"{check.name}:{error}" for check in checks for error in check.errors]
    manifest = root / "dataset/evidence_files.csv"
    if manifest.is_file():
        evidence_root = (root / "dataset/evidence").resolve()
        with manifest.open(encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                source = (root / "dataset" / str(row.get("file_path") or "")).resolve()
                if not source.is_relative_to(evidence_root):
                    errors.append(f"manifest_outside_evidence_root:{row.get('file_id')}")
                elif not source.is_file():
                    errors.append(f"manifest_missing_file:{row.get('file_id')}")
                elif source.suffix.casefold() not in EVIDENCE_SUFFIXES:
                    errors.append(f"manifest_unsupported_extension:{row.get('file_id')}")
    return checks, errors


def write_report(root: Path) -> Path:
    checks, errors = audit_dataset(root)
    path = Path(root) / "code/evaluation/csv_schema_audit.md"
    lines = [
        "# Dataset CSV schema audit", "",
        "Read-only checks of all nine supplied CSV files: exact column order, row shape, unique primary keys where applicable, ISO timestamps, and manifest paths. This report records no request or answer values.",
        "",
        "| CSV | rows | columns | malformed rows | duplicate keys | invalid times | result |",
        "|---|---:|---|---:|---:|---:|---|",
    ]
    for check in checks:
        result = ", ".join(check.errors) if check.errors else "PASS"
        lines.append(f"| `{check.name}` | {check.rows} | {', '.join(check.headers)} | {check.malformed_rows} | {check.duplicate_keys} | {check.invalid_timestamps} | {result} |")
    lines.extend(["", f"Manifest/path and schema errors: {len(errors)}.", *[f"- {error}" for error in errors], ""])
    lines.extend([
        "The production loader reads `deletion_requests.csv`, `user_identities.csv`, `user_audit_log.csv`, `system_activity.csv`, `deletion_rules.csv`, and `evidence_files.csv`. `sample_output.csv` and the blank `output.csv` are outside the production input set. The former is used only by evaluation commands; the latter is the submission destination/template.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    checks, errors = audit_dataset(root)
    path = write_report(root)
    print(f"{len(checks)} CSV schemas; {len(errors)} errors; report={path}")
    raise SystemExit(bool(errors))
