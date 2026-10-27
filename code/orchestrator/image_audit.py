"""Write image-by-image OCR, owner/resource mappings, and Vision disagreement log."""
import csv
import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.evidence.handlers.image_handler import _ocr_records
try:
    from .image_inspector import image_metadata, run_tesseract
except ImportError:
    from image_inspector import image_metadata, run_tesseract


def write_report(root):
    root=Path(root)
    with (root/"dataset/user_identities.csv").open(encoding="utf-8-sig",newline="") as handle:
        identities=list(csv.DictReader(handle))
    with (root/"dataset/user_audit_log.csv").open(encoding="utf-8-sig",newline="") as handle:
        audit=list(csv.DictReader(handle))
    email_to_ids={}
    for row in identities:
        email_to_ids.setdefault(row["email"].casefold(),set()).add(row["user_id"])
    for row in audit:
        if row.get("field_name")=="email":
            for field in ("old_value","new_value"):
                if "@" in row.get(field,""):
                    email_to_ids.setdefault(row[field].casefold(),set()).add(row["user_id"])
    subject=SimpleNamespace(all_user_ids={r["user_id"] for r in identities},
                            all_emails=set(email_to_ids))
    transcript_path=root/"code/evaluation/image_transcripts.json"
    transcripts=json.loads(transcript_path.read_text(encoding="utf-8")) if transcript_path.is_file() else {}
    lines=["# Full screenshot text and ownership audit", "",
           "Local OCR text is shown verbatim below. Vision is `gpt-4o-mini` at high detail; its rows are schema-validated and compared to OCR. A filter/search term is not ownership. Identity mappings use current and historical email records, not a case-number suffix.", "",
           "| Image | OCR-linked resources | Vision-validated resources | Disagreement |",
           "|---|---:|---:|---:|"]
    detail=[]
    for path in sorted((root/"dataset/evidence/images").glob("*")):
        if path.suffix.lower() not in {".png",".jpg",".jpeg"}: continue
        text=run_tesseract(path)
        ocr=_ocr_records(text,subject)
        vision=transcripts.get(path.name,{"records":[]}).get("records",[])
        ocr_keys={(r.resource_id,r.user_ref.casefold()) for r in ocr}
        vision_keys={(r["resource_id"],r["user_ref"].casefold()) for r in vision}
        disagreement=len(ocr_keys^vision_keys)
        lines.append(f"| `{path.name}` | {len(ocr_keys)} | {len(vision_keys)} | {disagreement} |")
        meta=image_metadata(path)
        detail.extend(["",f"## {path.name}","",
                       f"Dimensions: {meta['dimensions'][0]}×{meta['dimensions'][1]}; OCR characters: {len(text)}; EXIF timestamp: {meta['exif_timestamp'] or 'none'}.","",
                       "| Resource | Exact visible owner | Canonical user ID(s) | Signal |",
                       "|---|---|---|---|"])
        for rid,ref in sorted(ocr_keys|vision_keys):
            users=[ref] if ref in subject.all_user_ids else sorted(email_to_ids.get(ref,set()))
            signal="OCR + Vision" if (rid,ref) in ocr_keys&vision_keys else "OCR only" if (rid,ref) in ocr_keys else "Vision only; review"
            detail.append(f"| `{rid}` | `{ref}` | {', '.join(users) or 'unresolved'} | {signal} |")
        if not ocr_keys and not vision_keys: detail.append("| — | — | — | No exact subject/resource row |")
        detail.extend(["","### OCR text (reading order)","","```text",text.strip() or "[no OCR text]","```"])
    report="\n".join(lines+detail)+"\n"
    target=root/"code/evaluation/image_text_inventory.md"
    target.write_text(report,encoding="utf-8")
    return target


if __name__=="__main__":
    root=Path(__file__).resolve().parents[2]
    print(write_report(root))
