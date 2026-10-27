from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class FlowSchedule:
    schedule_kind: str = "manual"
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
    recurrence_interval: timedelta | None = None
    is_disabled: bool = False

@dataclass
class FlowFact:
    flow_id: str
    system_id: str
    target_system_id: str
    resource_id: str
    user_ref: str
    schedule: FlowSchedule
    is_active_at_audit: bool
    evidence_id: str
    evidence_timestamp: datetime | None
    source_has_user_data: bool
    can_recreate_at_audit: bool
    notes: list[str] = field(default_factory=list)

@dataclass
class RestoreRiskFact:
    backup_id: str
    system_id: str
    resource_id: str
    backup_time: datetime
    deletion_time: datetime | None
    retention_expires_at: datetime | None
    is_blocked: bool
    is_risk_at_audit: bool
    evidence_id: str
    evidence_timestamp: datetime | None
    notes: list[str] = field(default_factory=list)
