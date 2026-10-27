"""Owner vetoes must use all source formats and abstain on conflicting aliases."""

import csv
from pathlib import Path

from agent.evidence.ir import ExtractedEvidence, RecordState
from orchestrator.source_owner_index import known_account_owners


def _csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def _dataset(root, sources):
    folder = root / "dataset"
    _csv(folder / "user_identities.csv",
         ("user_id", "email", "email_hash"),
         (("user_a", "new@example.test", ""),
          ("user_b", "other@example.test", ""),
          ("user_c", "shared@example.test", ""),
          ("user_d", "shared@example.test", "")))
    _csv(folder / "user_audit_log.csv",
         ("audit_id", "user_id", "event_time", "field_name", "old_value", "new_value"),
         (("audit_1", "user_a", "2026-01-01T00:00:00Z", "email",
           "old@example.test", "new@example.test"),))
    _csv(folder / "evidence_files.csv", ("file_id", "file_path"), sources)
    return folder


def test_text_handover_links_historical_email_without_case_number(tmp_path):
    folder = _dataset(tmp_path, (("file_1", "evidence/handover.txt"),))
    source = folder / "evidence/handover.txt"
    source.parent.mkdir(parents=True)
    source.write_text(
        "2026-01-03T12:00:00Z | account_service | account_101 | USER_PROFILE | "
        "NOT_FOUND | OLD@EXAMPLE.TEST\n", encoding="utf-8")
    assert known_account_owners(str(tmp_path))["account_101"] == "user_a"


def test_shared_alias_does_not_establish_account_owner(tmp_path):
    folder = _dataset(tmp_path, (("file_1", "evidence/records.json"),))
    source = folder / "evidence/records.json"
    source.parent.mkdir(parents=True)
    source.write_text(
        '{"system_id":"account_service","records":['
        '{"resource_id":"account_102","email":"shared@example.test"},'
        '{"resource_id":"account_103","email":"other@example.test"}]}',
        encoding="utf-8")
    owners = known_account_owners(str(tmp_path))
    assert "account_102" not in owners
    assert owners["account_103"] == "user_b"


def test_pdf_and_image_formats_enter_veto_index(tmp_path, monkeypatch):
    folder = _dataset(tmp_path, (("file_pdf", "evidence/page.pdf"),
                                 ("file_png", "evidence/screen.png")))
    for name in ("page.pdf", "screen.png"):
        path = folder / "evidence" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"synthetic fixture")
    from orchestrator import source_owner_index as module
    monkeypatch.setattr(module.pdf_handler, "extract",
                        lambda *args: ([RecordState("account_service", "account_104",
                                                    "old@example.test", "PRESENT")], []))
    monkeypatch.setattr(module.image_handler, "extract",
                        lambda *args: ExtractedEvidence("file_png", "screen.png", "", [
                            RecordState("account_service", "account_105", "other@example.test",
                                        "PRESENT")], "ocr", None))
    owners = known_account_owners(str(tmp_path))
    assert owners["account_104"] == "user_a"
    assert owners["account_105"] == "user_b"
