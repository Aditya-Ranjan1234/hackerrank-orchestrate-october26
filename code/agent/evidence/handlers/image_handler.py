import json
import re
from datetime import datetime, timezone
from pathlib import Path

from ..cache import file_hash
from ..ir import ExtractedEvidence, PIIHit, RecordState

def run_tesseract(path):
    from orchestrator.image_inspector import run_tesseract as inspect_ocr
    return inspect_ocr(path)


def post_audit_exif(path, audit_at):
    from orchestrator.image_inspector import post_audit_exif as inspect_exif
    return inspect_exif(path, audit_at)

RESOURCE = re.compile(r"\b(?:account|order|support|search|analytics|export|backup|data_flow|audit_record|marketing|tombstone)_\d+\b", re.I)
SYSTEM_BY_PREFIX = {"account":"account_service", "order":"order_service", "support":"support_platform", "search":"search_service", "analytics":"analytics_platform", "export":"export_service", "backup":"backup_service", "data_flow":"integration_service", "audit_record":"security_service", "marketing":"marketing_platform"}


def _ocr_records(text, identities):
    """Conservative same-line subject/resource joins from OCR text."""
    records = []
    known = sorted(set(identities.all_user_ids) | set(identities.all_emails), key=len, reverse=True)
    lines=text.splitlines()
    for index,line in enumerate(lines):
        resources={match.group(0) for match in RESOURCE.finditer(line)}
        if len(resources)!=1:
            continue
        rid=next(iter(resources))
        for identifier in known:
            boundary = r"(?<![\w@.+-])" + re.escape(identifier) + r"(?![\w@.+-])"
            if re.search(boundary, line, re.I):
                kind = "email" if "@" in identifier else "user_id"
                ref = identifier.casefold() if kind == "email" else identifier
                pii=[PIIHit("ocr_row",kind,ref,source_page=1)]
                for uid in identities.all_user_ids:
                    if uid!=ref and re.search(r"(?<![\w-])"+re.escape(uid)+r"(?![\w-])",line):
                        pii.append(PIIHit("ocr_row","user_id",uid,source_page=1))
                for email in re.findall(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",line):
                    if email.casefold() in {e.casefold() for e in identities.all_emails} and (kind!="email" or email.casefold()!=ref):
                        pii.append(PIIHit("ocr_row","email",email.casefold(),source_page=1))
                for phone in re.findall(r"\+\d[\d ()-]{6,}\d",line):
                    pii.append(PIIHit("ocr_row","phone",phone,source_page=1))
                records.append(RecordState(SYSTEM_BY_PREFIX.get(rid.rsplit("_",1)[0], "image"), rid, ref, "PRESENT",
                    pii, None, {"ocr_line": line}, "ocr"))
                break
        else:
            # Selected-record headers can place the resource on one line and
            # its sole owner in the adjacent detail card. Do not cross a
            # second resource or join across a table of multiple subjects.
            if index<18 and "@" not in line:
                context=[]
                for following in lines[index+1:index+7]:
                    if RESOURCE.search(following): break
                    context.append(following)
                refs=[ref for ref in identities.all_emails if any(re.search(r"(?<![\w@.+-])"+re.escape(ref)+r"(?![\w@.+-])",part,re.I) for part in context)]
                if len(refs)==1:
                    ref=refs[0].casefold()
                    records.append(RecordState(SYSTEM_BY_PREFIX.get(rid.rsplit("_",1)[0],"image"),rid,ref,"PRESENT",
                        [PIIHit("ocr_selected_record","email",ref,source_page=1)],None,
                        {"ocr_line":line,"owner_context":context},"ocr"))
    distinct={}
    for record in records:
        key=(record.system_id,record.resource_id,record.user_ref.casefold())
        if key not in distinct or len(record.pii_hits)>len(distinct[key].pii_hits):
            distinct[key]=record
    return list(distinct.values())

def vlm_extract(path, identities, vlm=None):
    if vlm is None:
        # Compatibility entry point for callers outside the registry. The
        # production registry calls extract(), which combines OCR and Vision.
        from ...llm.client import LLMClient
        from ...llm.usage_tracker import UsageTracker
        from orchestrator.image_transcriber import transcribe_image
        client=LLMClient()
        if not client.enabled:
            return [],0,0,0,["vision_unavailable"]
        if not Path(path).is_file():
            return [],0,0,0,["missing_file"]
        usage=UsageTracker.instance()
        before=usage.totals()
        transcript=transcribe_image(path,client)
        after=usage.totals()
        allowed={str(ref).casefold() for ref in identities.all_user_ids}|{str(ref).casefold() for ref in identities.all_emails}
        rows=[item for item in transcript["records"] if item["user_ref"].casefold() in allowed]
        return rows,after[0]-before[0],after[1]-before[1],after[2]-before[2],([transcript["error"]] if transcript["error"] else [])
    for attempt in range(2):
        try:
            from orchestrator.image_transcriber import _validate_rows
            data=json.loads(vlm(path, identities, strict=attempt==1))
            if not isinstance(data,dict) or not isinstance(data.get("records"),list):
                raise ValueError("invalid_vlm_schema")
            valid,_=_validate_rows(data["records"])
            allowed={str(ref).casefold() for ref in identities.all_user_ids}|{str(ref).casefold() for ref in identities.all_emails}
            return [row for row in valid if row["user_ref"].casefold() in allowed],attempt+1,0,0,[]
        except (ValueError,TypeError,KeyError): pass
    return [],2,0,0,["vlm_json_parse_failed_twice"]


def extract(path: Path, file_id: str, identities, audit_at=None, llm_client=None, case_id=None):
    """Read image through Vision when configured; otherwise fail closed."""
    path=Path(path)
    now=datetime.now(timezone.utc)
    if not path.is_file():
        return ExtractedEvidence(file_id,str(path),"",[],"missing",now,notes=["missing_file"])
    digest=file_hash(path.read_bytes())
    try:
        if post_audit_exif(path,audit_at):
            return ExtractedEvidence(file_id,str(path),digest,[],"post_audit_exif",now,notes=["post_audit_exif"])
    except (OSError,ImportError):
        pass
    ocr_text=run_tesseract(path)
    ocr_records=_ocr_records(ocr_text,identities) if ocr_text.strip() else []
    if llm_client is None or not llm_client.enabled:
        return ExtractedEvidence(file_id,str(path),digest,ocr_records,"tesseract" if ocr_records else "image_no_vlm",now,
                                 notes=[] if ocr_records else ["ocr_without_exact_row" if ocr_text.strip() else "tesseract_empty_or_unavailable","vision_unavailable"])
    from ...llm.semantic_resolver import SemanticResolver
    from ...llm.usage_tracker import UsageTracker
    from orchestrator.image_transcriber import PROMPT, transcribe_image
    usage=UsageTracker.instance()
    before=usage.totals()
    transcript=transcribe_image(path,llm_client)
    allowed={str(ref).casefold() for ref in identities.all_user_ids}|{str(ref).casefold() for ref in identities.all_emails}
    raw=[item for item in transcript["records"] if item["user_ref"].casefold() in allowed]
    rejected_vision_rows=0
    if raw and ocr_text.strip():
        # The model's visible_text is its own assertion. Independently require
        # both literal identifiers to occur in the local OCR of this image.
        corroborated=[item for item in raw if item["resource_id"].casefold() in ocr_text.casefold()
                      and item["user_ref"].casefold() in ocr_text.casefold()]
        rejected_vision_rows=len(raw)-len(corroborated)
        raw=corroborated
    elif raw:
        # If OCR cannot see the image at all, require a second, differently
        # worded Vision pass to agree on the exact subject/resource pair.
        verify=transcribe_image(path,llm_client,PROMPT+"\nIndependent second reading: list only exact same-row or selected-card subject/resource pairs. Do not reuse a guessed pair.")
        verified={(item["resource_id"],item["user_ref"]) for item in verify["records"]}
        corroborated=[item for item in raw if (item["resource_id"],item["user_ref"]) in verified]
        rejected_vision_rows=len(raw)-len(corroborated)
        raw=corroborated
    # Per-subject Vision is a bounded fallback only where the global pass or
    # local OCR actually saw this subject but did not validate an owned row.
    candidates=set(transcript.get("candidate_refs",()))
    mentioned=any(re.search(r"(?<![\w@.+-])"+re.escape(ref)+r"(?![\w@.+-])",ocr_text,re.I)
                  for ref in allowed if ref)
    fallback_used=False
    if not raw and not ocr_records and (candidates & allowed or mentioned):
        raw=SemanticResolver(llm_client).extract_pii_from_image(path,identities,case_id)
        fallback_used=True
    if fallback_used and raw:
        if ocr_text.strip():
            verified=[item for item in raw if item["resource_id"].casefold() in ocr_text.casefold()
                      and item["user_ref"].casefold() in ocr_text.casefold()]
        else:
            second=transcribe_image(path,llm_client,PROMPT+"\nIndependent verification of the focused reading: copy only exact same-row subject/resource pairs.")
            pairs={(item["resource_id"],item["user_ref"]) for item in second["records"]}
            verified=[item for item in raw if (item["resource_id"],item["user_ref"]) in pairs]
        rejected_vision_rows+=len(raw)-len(verified)
        raw=verified
    records=list(ocr_records)
    for item in raw:
        hits=[]
        for hit in item.get("pii_hits",[]):
            if not isinstance(hit,dict) or hit.get("value_kind") not in {"email","name","phone","email_hash","user_id"}:
                continue
            hits.append(PIIHit(str(hit.get("field_path", "")),hit["value_kind"],str(hit.get("value", "")),source_page=item.get("page")))
        suggested=RecordState(str(item["system_id"]),str(item["resource_id"]),str(item["user_ref"]),item["state_at_evidence"],hits,None,item,"vlm")
        same=next((r for r in records if (r.system_id,r.resource_id)==
                   (suggested.system_id,suggested.resource_id)),None)
        if same:
            same.state_at_evidence=suggested.state_at_evidence
            existing={(h.field_path,h.value_kind,h.value) for h in same.pii_hits}
            same.pii_hits.extend(h for h in suggested.pii_hits if (h.field_path,h.value_kind,h.value) not in existing)
        else:
            records.append(suggested)
    after=usage.totals()
    review_notes=[]
    if rejected_vision_rows:
        review_notes.append(f"vision_rows_lacking_independent_corroboration:{rejected_vision_rows}")
    if transcript.get("error"):
        review_notes.append(str(transcript["error"]))
    if (candidates & allowed) and not raw and not ocr_records:
        review_notes.append("vision_candidate_without_owned_record")
    if not records:
        review_notes.append("no_identity_linked_image_records")
    return ExtractedEvidence(file_id,str(path),digest,records,"ocr_plus_vision" if ocr_records else "openai_vision",now,
                             after[0]-before[0],after[1]-before[1],after[2]-before[2],notes=review_notes)
