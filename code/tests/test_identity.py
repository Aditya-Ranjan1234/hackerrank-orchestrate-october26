from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from agent.identity import IdentityResolver


def test_current_email_resolves():
    resolver = IdentityResolver(ROOT / "dataset/user_identities.csv", ROOT / "dataset/user_audit_log.csv")
    with (ROOT / "dataset/deletion_requests.csv").open(encoding="utf-8", newline="") as handle:
        case = next(csv.DictReader(handle))
    bundle = resolver.resolve(case["email"], case["audit_at"])
    assert bundle.primary_user_id is not None
    assert bundle.request_email_kind == "CURRENT"
    assert case["email"].casefold() in bundle.all_emails


def test_unknown_email_is_unresolved():
    resolver = IdentityResolver(ROOT / "dataset/user_identities.csv", ROOT / "dataset/user_audit_log.csv")
    bundle = resolver.resolve("not-a-real-user@example.invalid", "2026-10-01T00:00:00Z")
    assert bundle.primary_user_id is None
    assert bundle.all_emails == set()


def test_historical_email_is_included_for_a_known_user():
    resolver = IdentityResolver(ROOT / "dataset/user_identities.csv", ROOT / "dataset/user_audit_log.csv")
    event = next(e for e in resolver.events if e.field_name == "email")
    old_email = event.old_value
    bundle = resolver.resolve(old_email, "2026-10-01T00:00:00Z")
    assert bundle.primary_user_id == event.user_id
    assert bundle.request_email_kind == "HISTORICAL"
    assert old_email.casefold() in bundle.all_emails


def test_audit_cutoff_excludes_later_identity_events():
    resolver = IdentityResolver(ROOT / "dataset/user_identities.csv", ROOT / "dataset/user_audit_log.csv")
    event = next(e for e in resolver.events if e.field_name == "email")
    before = resolver.resolve(event.old_value, "2024-01-01T00:00:00Z")
    after = resolver.resolve(event.old_value, "2026-12-31T00:00:00Z")
    assert before.primary_user_id is None
    assert event.old_value.casefold() not in before.all_emails
    assert event.old_value.casefold() in after.all_emails
