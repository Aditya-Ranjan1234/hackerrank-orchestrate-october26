"""Extract only identity-owned resource rows from PDF; never invent page IDs."""
from pathlib import Path
import re
import hashlib

from ..ir import RecordState, PIIHit
from .common import email_hashes

RESOURCE=re.compile(r"(?<![\w-])(?:account|order|support|search|analytics|export|backup|data_flow|audit_record|marketing|tombstone)_\d+(?![\w-])",re.I)
SYSTEM={"account":"account_service","order":"order_service","support":"support_platform",
        "search":"search_service","analytics":"analytics_platform","export":"export_service",
        "backup":"backup_service","data_flow":"integration_service",
        "audit_record":"security_service","marketing":"marketing_platform","tombstone":"identity_service"}


def _refs(text,identities):
    known=set(identities.all_user_ids)|set(identities.all_emails)|email_hashes(identities)
    return sorted((ref for ref in known if ref and re.search(r"(?<![\w@.+-])"+re.escape(ref)+r"(?![\w@.+-])",text,re.I)),key=len,reverse=True)


def _record(resource,ref,page_no,source,document_kind=""):
    kind="email_hash" if re.fullmatch(r"[0-9a-f]{64}",ref,re.I) else "email" if "@" in ref else "user_id"
    prefix=resource.rsplit("_",1)[0].casefold()
    hit=PIIHit(f"page[{page_no}]",kind,ref.casefold() if kind=="email" else ref,source_page=page_no)
    return RecordState(SYSTEM[prefix],resource,ref.casefold() if kind=="email" else ref,
                       "PRESENT",[hit],None,{"source_text":source,"document_kind":document_kind})


def _render_page(path, number):
    """Render a scanned source page into a content-keyed local PNG."""
    import pypdfium2 as pdfium
    digest=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    folder=Path(__file__).resolve().parents[4]/"code/.cache/pdf_pages"
    target=folder/f"{digest}_page_{number}.png"
    if not target.is_file():
        folder.mkdir(parents=True,exist_ok=True)
        document=pdfium.PdfDocument(str(path))
        try:
            image=document[number-1].render(scale=2.0).to_pil()
            image.save(target)
        finally:
            document.close()
    return target


def extract(path:Path,file_id:str,identities,audit_at=None,llm_client=None,case_id=None):
    from orchestrator.pdf_inspector import inspect_pdf
    try: parsed=inspect_pdf(path)
    except ImportError: return [],["pdfplumber unavailable"]
    all_text="\n".join(page["text"] for page in parsed["pages"])
    title=parsed["pages"][0]["text"].splitlines()[0].casefold() if parsed["pages"] and parsed["pages"][0]["text"] else ""
    if "register" in title and "retain until" in all_text.casefold():
        return [],parsed["notes"]+["retention_register_context_only"]
    document_kind="support_attachment" if "attachment" in path.stem.casefold() else ""
    records=[]; seen=set()
    for page in parsed["pages"]:
        number=page["page"]
        if page["scanned"]:
            try:
                from . import image_handler
                rendered=_render_page(path,number)
                visual=image_handler.extract(rendered,file_id,identities,audit_at,llm_client,case_id)
                for record in visual.records:
                    record.raw_row={**(record.raw_row or {}),"pdf_page":number}
                    for hit in record.pii_hits:
                        hit.source_page=number
                    records.append(record)
                parsed["notes"].append(f"scanned_page_{number}_routed_to_ocr_vision")
                parsed["notes"].extend(visual.notes)
            except (ImportError,OSError,ValueError,RuntimeError) as exc:
                parsed["notes"].append(f"scanned_page_{number}_render_failed:{type(exc).__name__}")
            continue
        lines=page["text"].splitlines()
        # Direct same-line or table-row joins outrank document-level context.
        for line in lines:
            for rid in set(RESOURCE.findall(line)):
                for ref in _refs(line,identities):
                    key=(rid,ref)
                    if key not in seen:
                        records.append(_record(rid,ref,number,line,document_kind));seen.add(key)
        for table in page["tables"]:
            for cells in table:
                row=" ".join(str(cell or "") for cell in cells)
                for rid in set(RESOURCE.findall(row)):
                    for ref in _refs(row,identities):
                        key=(rid,ref)
                        if key not in seen:
                            records.append(_record(rid,ref,number,row,document_kind));seen.add(key)
        # A form/report with exactly one resource and one subject is a selected
        # record; a multi-resource page is not evidence of every cross-product.
        resources=set(RESOURCE.findall(page["text"]))
        refs=_refs(page["text"],identities)
        if len(resources)==1 and len(refs)==1:
            rid=next(iter(resources));ref=refs[0];key=(rid,ref)
            if key not in seen:
                records.append(_record(rid,ref,number,page["text"],document_kind));seen.add(key)
    if not any("render_failed" in note for note in parsed["notes"]):
        parsed["notes"]=[note for note in parsed["notes"] if note!="scanned, needs Vision"]
    return records,parsed["notes"]
