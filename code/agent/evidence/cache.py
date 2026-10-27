import hashlib, json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from .ir import ExtractedEvidence, RecordState, PIIHit

def file_hash(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def cache_key(data: bytes, identity=None, audit_at=None) -> str:
    """Identity-aware key; file_hash remains the hash of the original bytes."""
    payload={"file_hash":file_hash(data),"identity":{
        "primary_user_id":getattr(identity,"primary_user_id",None),
        "all_user_ids":sorted(getattr(identity,"all_user_ids",()) or ()),
        "all_emails":sorted(str(v).strip().casefold() for v in (getattr(identity,"all_emails",()) or ())),
        "all_email_hashes":sorted(str(v).strip().casefold() for v in (getattr(identity,"all_email_hashes",()) or ())),
    },"audit_at":audit_at.isoformat() if isinstance(audit_at,datetime) else audit_at}
    return hashlib.sha256(json.dumps(payload,sort_keys=True).encode("utf-8")).hexdigest()
def cache_path(root: Path, digest: str) -> Path: return root / "code" / ".cache" / "evidence" / f"{digest}.json"

def _jsonable(obj):
    if isinstance(obj, datetime): return obj.isoformat()
    if isinstance(obj, list): return [_jsonable(x) for x in obj]
    if isinstance(obj, dict): return {k: _jsonable(v) for k,v in obj.items()}
    return obj

def save(root: Path, evidence: ExtractedEvidence, key: str | None = None) -> None:
    path = cache_path(root, key or evidence.file_hash); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(asdict(evidence)), sort_keys=True), encoding="utf-8")

def load(root: Path, digest: str) -> ExtractedEvidence | None:
    path = cache_path(root, digest)
    if not path.exists(): return None
    d = json.loads(path.read_text(encoding="utf-8"))
    def rec(x):
        return RecordState(x["system_id"], x["resource_id"], x["user_ref"], x["state_at_evidence"],
            [PIIHit(**h) for h in x.get("pii_hits", [])], datetime.fromisoformat(x["evidence_timestamp"]) if x.get("evidence_timestamp") else None, x.get("raw_row", {}), x.get("system_id_source","explicit"))
    return ExtractedEvidence(d["file_id"], d["file_path"], d["file_hash"], [rec(x) for x in d["records"]], d["extraction_method"], datetime.fromisoformat(d["extracted_at"]), d.get("llm_call_count", 0), d.get("llm_tokens_in", 0), d.get("llm_tokens_out", 0), [rec(x) for x in d.get("records_post_audit", [])], d.get("notes", []))

def clear_cache(root: Path) -> None:
    folder = root / "code" / ".cache" / "evidence"
    if folder.exists():
        for p in folder.glob("*.json"): p.unlink()
