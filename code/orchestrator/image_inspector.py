"""Local OCR-first image inspection with explicit Vision fallback."""
import json
import hashlib
import statistics
from functools import lru_cache
from datetime import datetime, timezone
from pathlib import Path

INVENTORY_PROMPT = 'Transcribe visible exact user IDs, emails, resource IDs and system titles only. Return JSON {"user_ids":[],"emails":[],"resource_ids":[],"systems":[]}. Do not infer ownership.'


@lru_cache(maxsize=1)
def _rapidocr_engine():
    from rapidocr_onnxruntime import RapidOCR
    return RapidOCR()


def run_tesseract(path):
    """Return spatially grouped OCR rows; cache by image and extractor version."""
    path=Path(path)
    cache_root=Path(__file__).resolve().parents[2]/"code/.cache/ocr"
    key=hashlib.sha256(path.read_bytes()+Path(__file__).read_bytes()).hexdigest()
    target=cache_root/f"{key}.json"
    if target.is_file():
        try: return json.loads(target.read_text(encoding="utf-8"))["text"]
        except (ValueError,KeyError,OSError): pass
    text=""
    try:
        result,_=_rapidocr_engine()(str(path))
        if result:
            tokens=[];heights=[]
            for box,value,confidence in result:
                if confidence<0.65: continue
                xs=[float(point[0]) for point in box];ys=[float(point[1]) for point in box]
                tokens.append((sum(ys)/len(ys),min(xs),str(value)))
                heights.append(max(ys)-min(ys))
            tolerance=max(8,0.55*statistics.median(heights)) if heights else 8
            rows=[]
            for y,x,value in sorted(tokens):
                if not rows or abs(y-rows[-1][0])>tolerance:
                    rows.append((y,[(x,value)]))
                else:
                    rows[-1][1].append((x,value))
            text="\n".join(" ".join(value for _,value in sorted(cells)) for _,cells in rows)
    except Exception:
        # OCR dependencies can raise format-specific LoadImageError on a
        # truncated/corrupt image; that file must not crash the case pipeline.
        pass
    if not text:
        try:
            import pytesseract
            from PIL import Image
            with Image.open(path) as image: text=pytesseract.image_to_string(image)
        except (ImportError,OSError,RuntimeError):
            text=""
    cache_root.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps({"text":text},ensure_ascii=False),encoding="utf-8")
    return text


def image_metadata(path):
    from PIL import Image
    with Image.open(path) as image:
        exif = image.getexif()
        stamp = exif.get(36867) or exif.get(306)
        return {"dimensions": image.size, "format": image.format, "exif_timestamp": stamp}


def post_audit_exif(path, audit_at):
    if not audit_at:
        return False
    stamp = image_metadata(path)["exif_timestamp"]
    if not stamp:
        return False
    try:
        observed = datetime.strptime(stamp, "%Y:%m:%d %H:%M:%S").replace(tzinfo=timezone.utc)
        cutoff = datetime.fromisoformat(audit_at.replace("Z", "+00:00")) if isinstance(audit_at, str) else audit_at
        return observed > cutoff
    except (ValueError, TypeError):
        return False


def inspect_image(path, llm_client=None, prompt=None, audit_at=None):
    meta = image_metadata(path)
    if post_audit_exif(path, audit_at):
        return {**meta, "ocr_text": "", "vision": None, "method": "post_audit_exif"}
    ocr = run_tesseract(path)
    if ocr.strip():
        return {**meta, "ocr_text": ocr, "vision": None, "method": "ocr"}
    vision = None
    if llm_client is not None and llm_client.enabled:
        raw = llm_client.call_vision(prompt or INVENTORY_PROMPT, path, "image_inventory", model="gpt-4o-mini", max_tokens=250)
        try:
            vision = json.loads(raw) if raw else None
        except (ValueError, TypeError):
            vision = None
    return {**meta, "ocr_text": ocr, "vision": vision, "method": "vision" if vision else "no_text"}
