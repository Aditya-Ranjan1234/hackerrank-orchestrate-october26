"""Deterministic identity resolution for deletion-audit cases.

The participant data exposes current identities plus field-level historical
changes. This module deliberately resolves only what the supplied data proves:
user_id ownership and historical email values. It does not invent merge/split
relationships that are not represented in the files.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import csv
from typing import Iterable


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _norm_email(value: str) -> str:
    return value.strip().casefold()


@dataclass(frozen=True)
class IdentityEvent:
    audit_id: str
    user_id: str
    event_time: datetime
    field_name: str
    old_value: str
    new_value: str


@dataclass
class IdentityBundle:
    requested_email: str
    primary_user_id: str | None
    all_user_ids: set[str] = field(default_factory=set)
    all_emails: set[str] = field(default_factory=set)
    request_email_kind: str = "UNKNOWN"
    matched_audit_ids: set[str] = field(default_factory=set)


class IdentityResolver:
    def __init__(self, identities_csv: Path, audit_csv: Path) -> None:
        self.identities: list[dict[str, str]] = list(csv.DictReader(identities_csv.open(encoding="utf-8-sig", newline="")))
        self.events: list[IdentityEvent] = []
        with audit_csv.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                self.events.append(
                    IdentityEvent(
                        audit_id=row["audit_id"],
                        user_id=row["user_id"],
                        event_time=_dt(row["event_time"]),
                        field_name=row["field_name"],
                        old_value=row["old_value"],
                        new_value=row["new_value"],
                    )
                )
        self._current_email_users: dict[str, set[str]] = {}
        for row in self.identities:
            email = _norm_email(row.get("email", ""))
            if email:
                self._current_email_users.setdefault(email, set()).add(row["user_id"])
        self._historical_email_users: dict[str, set[str]] = {}
        for event in self.events:
            if event.field_name != "email":
                continue
            for value in (event.old_value, event.new_value):
                email = _norm_email(value)
                if email:
                    self._historical_email_users.setdefault(email, set()).add(event.user_id)

    def resolve(self, email: str, audit_at: str | datetime) -> IdentityBundle:
        cutoff = _dt(audit_at) if isinstance(audit_at, str) else audit_at
        requested = _norm_email(email)
        current_matches = {
            row["user_id"]
            for row in self.identities
            if _norm_email(row.get("email", "")) == requested
            and self._email_visible_at(row["user_id"], requested, cutoff)
        }
        historical_matches = {
            user_id
            for user_id in self._historical_email_users.get(requested, set())
            if self._email_visible_at(user_id, requested, cutoff)
        }
        candidates = current_matches | historical_matches

        # Prefer a current identity when unique. Otherwise use the unique
        # historical owner visible by the audit cutoff.
        if len(current_matches) == 1:
            user_id = next(iter(current_matches))
            kind = "CURRENT"
        elif len(candidates) == 1:
            user_id = next(iter(candidates))
            kind = "HISTORICAL"
        else:
            return IdentityBundle(email, None)

        events = [e for e in self.events if e.user_id == user_id and e.event_time <= cutoff]
        emails: set[str] = set()
        # Include a current snapshot value only when it is supported as of the
        # cutoff. A later current snapshot must not contaminate an earlier audit.
        for row in self.identities:
            if row["user_id"] == user_id and row.get("email"):
                candidate = _norm_email(row["email"])
                if self._email_visible_at(user_id, candidate, cutoff):
                    emails.add(candidate)
        audit_ids: set[str] = set()
        for event in events:
            audit_ids.add(event.audit_id)
            if event.field_name == "email":
                for value in (event.old_value, event.new_value):
                    value = _norm_email(value)
                    if value:
                        emails.add(value)
        return IdentityBundle(
            requested_email=email,
            primary_user_id=user_id,
            all_user_ids={user_id},
            all_emails=emails,
            request_email_kind=kind,
            matched_audit_ids=audit_ids,
        )

    def _email_visible_at(self, user_id: str, email: str, cutoff: datetime) -> bool:
        """Return whether the email is evidenced for this user by cutoff.

        If there is no email history for a user, the current identity row is
        the only participant-facing evidence available and is accepted.
        """
        user_events = [
            e for e in self.events
            if e.user_id == user_id and e.field_name == "email" and e.event_time <= cutoff
        ]
        if not user_events:
            row = next((r for r in self.identities if r["user_id"] == user_id), None)
            return row is not None and _norm_email(row.get("email", "")) == email
        return any(
            email == _norm_email(value)
            for event in user_events
            for value in (event.old_value, event.new_value)
        )


def load_default_resolver(repo_root: Path) -> IdentityResolver:
    dataset = repo_root / "dataset"
    return IdentityResolver(dataset / "user_identities.csv", dataset / "user_audit_log.csv")
