from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class PIIHit:
    field_path: str
    value_kind: str
    value: str
    source_page: int | None = None
    source_row: int | None = None

@dataclass
class RecordState:
    system_id: str
    resource_id: str
    user_ref: str
    state_at_evidence: str
    pii_hits: list[PIIHit] = field(default_factory=list)
    evidence_timestamp: datetime | None = None
    raw_row: dict[str, Any] = field(default_factory=dict)
    system_id_source: str = "explicit"

@dataclass
class ExtractedEvidence:
    file_id: str
    file_path: str
    file_hash: str
    records: list[RecordState]
    extraction_method: str
    extracted_at: datetime
    llm_call_count: int = 0
    llm_tokens_in: int = 0
    llm_tokens_out: int = 0
    records_post_audit: list[RecordState] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

@dataclass
class ResourceFact:
    system_id: str
    resource_id: str
    user_id: str
    state_at_audit: str
    direct_pii_present: set[str]
    evidence_id: str
    evidence_timestamp: datetime | None
    notes: list[str] = field(default_factory=list)

# Backward-compatible name used by the Phase 2 contract for an individual
# extracted evidence record.
EvidenceFact = RecordState
