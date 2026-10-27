import json
from pathlib import Path
from orchestrator.dataset_catalog import catalog_file, catalog_dataset, render_catalog, audit_gap_cases, _exact_ref

ROOT = Path(__file__).resolve().parents[2]


def test_catalog_json_keys_and_counts(tmp_path):
    path = tmp_path / "sample.json"
    path.write_text(json.dumps({"users": [{"user_id": "U1"}], "meta": {}}), encoding="utf-8")
    entry = catalog_file(path, tmp_path)
    assert entry["details"]["record_counts"] == {"users": 1}
    assert "$.users[].user_id" in entry["details"]["identity_fields"]


def test_nested_json_features_are_enumerated(tmp_path):
    path = tmp_path / "nested.json"
    path.write_text(json.dumps({"records": [{"resource_id": "account_1", "state": "ABSENT", "snapshot_at": "2026-01-01"}]}), encoding="utf-8")
    details = catalog_file(path, tmp_path)["details"]
    assert "$.records[].resource_id" in details["resource_fields"]
    assert "$.records[].state" in details["state_fields"]
    assert "$.records[].snapshot_at" in details["time_fields"]


def test_catalog_unknown_format(tmp_path):
    path = tmp_path / "sample.bin"
    path.write_bytes(b"one")
    assert catalog_file(path, tmp_path)["details"]["notes"] == ["unknown format"]


def test_catalog_walks_every_file(tmp_path):
    folder = tmp_path / "dataset/evidence/records"
    folder.mkdir(parents=True)
    (folder / "a.json").write_text("{}", encoding="utf-8")
    (folder / "b.json").write_text("[]", encoding="utf-8")
    entries = catalog_dataset(tmp_path)
    assert len(entries) == 2 and all(e["error"] is None for e in entries)


def test_catalog_report_deterministic_without_mtime_change(tmp_path):
    path = tmp_path / "a.json"
    path.write_text("{}", encoding="utf-8")
    assert render_catalog([catalog_file(path, tmp_path)]) == render_catalog([catalog_file(path, tmp_path)])


def test_exact_reference_never_uses_numeric_suffix():
    assert not _exact_ref("user_1", "user_10")
    assert _exact_ref("user_1", "subject=user_1")


def test_five_gap_audit_has_no_unverified_join():
    result = audit_gap_cases(ROOT)
    assert set(result) == {"case_01", "case_02", "case_03", "case_04", "case_31"}
    assert all(not item["direct"] for item in result.values())


def test_registry_invalidates_evidence_cache_after_extractor_revision(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from agent.evidence import registry
    folder = tmp_path / "dataset"; folder.mkdir()
    (folder / "source.json").write_text('{"resource_id":"account_1","email":"a@example.com"}', encoding="utf-8")
    identity = SimpleNamespace(primary_user_id="U1", all_user_ids={"U1"}, all_emails={"a@example.com"}, all_email_hashes=set())
    monkeypatch.setattr(registry, "extractor_fingerprint", lambda _: "revision_a")
    registry.extract_file(tmp_path, "ev", "source.json", identity)
    registry.extract_file(tmp_path, "ev", "source.json", identity)
    assert len(list((tmp_path / "code/.cache/evidence").glob("*.json"))) == 1
    monkeypatch.setattr(registry, "extractor_fingerprint", lambda _: "revision_b")
    registry.extract_file(tmp_path, "ev", "source.json", identity)
    assert len(list((tmp_path / "code/.cache/evidence").glob("*.json"))) == 2
