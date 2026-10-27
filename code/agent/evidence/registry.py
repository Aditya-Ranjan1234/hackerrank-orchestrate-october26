from datetime import datetime, timezone
from pathlib import Path
import csv
from functools import lru_cache
from .ir import ExtractedEvidence, RecordState, PIIHit
from .cache import file_hash, cache_key, load, save
from .handlers import json_handler, sql_handler, log_handler, pdf_handler, image_handler
TABLE_TO_SYSTEM=sql_handler.TABLE_TO_SYSTEM

@lru_cache(maxsize=None)
def extractor_fingerprint(ext):
    """Invalidate identity-aware evidence cache when extraction code changes."""
    source = {".json": json_handler, ".sql": sql_handler,
              ".log": log_handler, ".txt": log_handler,
              ".pdf": pdf_handler, ".png": image_handler,
              ".jpg": image_handler, ".jpeg": image_handler}.get(ext)
    paths = [Path(__file__), Path(__file__).parent / "handlers/common.py"]
    if source is not None:
        paths.append(Path(source.__file__))
    inspector = {".sql": "database_inspector.py", ".pdf": "pdf_inspector.py",
                 ".log": "log_inspector.py", ".txt": "log_inspector.py",
                 ".png": "image_inspector.py", ".jpg": "image_inspector.py",
                 ".jpeg": "image_inspector.py"}.get(ext)
    if inspector:
        paths.append(Path(__file__).resolve().parents[2] / "orchestrator" / inspector)
    if ext==".pdf":
        paths.extend([Path(image_handler.__file__),
                      Path(__file__).resolve().parents[2]/"orchestrator/image_transcriber.py",
                      Path(__file__).resolve().parents[2]/"orchestrator/image_inspector.py"])
    return file_hash(b"".join(p.read_bytes() for p in paths if p.is_file()))

def extract_file(root: Path, file_id: str, file_path: str, identities=None, audit_at=None, vlm=None,llm_client=None,case_id=None):
    path=root/"dataset"/file_path; data=path.read_bytes() if path.exists() else b""; digest=file_hash(data)
    if path.suffix.lower() in {".png",".jpg",".jpeg"}:
        image=image_handler.extract(path,file_id,identities,audit_at,llm_client,case_id)
        image.file_path=file_path
        return image
    key=file_hash((cache_key(data,identities,audit_at)+extractor_fingerprint(path.suffix.lower())).encode("ascii"))
    cached=load(root,key) if path.exists() else None
    if cached: return cached
    now=datetime.now(timezone.utc); notes=[]
    if not path.exists(): return ExtractedEvidence(file_id,file_path,digest,[],"missing",now,notes=["missing_file"])
    ext=path.suffix.lower(); post=[]; method=ext[1:]
    if ext==".json": records,post=json_handler.extract(path,file_id,identities if identities else (),audit_at,include_post_audit=True)
    elif ext==".sql": records=sql_handler.extract(path,file_id,identities)
    elif ext in {".log",".txt"}: records,post=log_handler.extract(path,file_id,identities,audit_at); method="regex-log"
    elif ext==".pdf": records,notes=pdf_handler.extract(path,file_id,identities,audit_at,llm_client,case_id); method="pdfplumber"
    else: records=[]; notes=["unsupported_extension"]
    evidence=ExtractedEvidence(file_id,file_path,digest,records,method,now,records_post_audit=post,notes=notes); save(root,evidence,key); return evidence

def manifest(root: Path):
    with (root/"dataset/evidence_files.csv").open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f))
