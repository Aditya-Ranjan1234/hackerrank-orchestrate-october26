"""One high-detail mini-Vision pass per image; deterministic row validation/filtering."""
import json
import re
from pathlib import Path

RESOURCE = re.compile(r"^(?:account|order|support|search|analytics|export|backup|data_flow|audit_record|marketing|tombstone)_\d+$", re.I)
USER = re.compile(r"^(?:user_\d+|U\d+)$", re.I)
EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
SYSTEM_BY_PREFIX = {"account":"account_service", "order":"order_service",
                    "support":"support_platform", "search":"search_service",
                    "analytics":"analytics_platform", "export":"export_service",
                    "backup":"backup_service", "data_flow":"integration_service",
                    "audit_record":"security_service", "marketing":"marketing_platform",
                    "tombstone":"identity_service"}

# Chat Completions Structured Outputs, not the weaker JSON-object mode. The
# model proposes rows; exact-ID and source-admission checks remain local.
VISION_SCHEMA = {
    "name": "northstar_visible_evidence",
    "strict": True,
    "schema": {
        "type": "object", "additionalProperties": False, "required": ["records"],
        "properties": {
            "records": {
                "type": "array",
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["resource_id", "user_ref", "state_at_evidence", "pii_hits", "visible_text"],
                    "properties": {
                        "resource_id": {"type": "string"},
                        "user_ref": {"type": "string"},
                        "state_at_evidence": {"type": "string", "enum": ["PRESENT", "ABSENT", "REDACTED", "ANONYMIZED", "TOMBSTONE"]},
                        "visible_text": {"type": "string"},
                        "pii_hits": {
                            "type": "array", "items": {
                                "type": "object", "additionalProperties": False,
                                "required": ["field_path", "value_kind", "value"],
                                "properties": {
                                    "field_path": {"type": "string"},
                                    "value_kind": {"type": "string", "enum": ["email", "name", "phone", "email_hash", "user_id"]},
                                    "value": {"type": "string"},
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}

PROMPT = """Read this Northstar Shop evidence screenshot row by row, including selected-record header,
all table rows, and the right-hand detail pane. Return STRICT JSON with a records array.
Each record must have: resource_id, user_ref, state_at_evidence, pii_hits, visible_text.
resource_id must be an exact visible resource ID (such as account_123, search_456).
user_ref must be an exact visible user ID or email that belongs to THAT SAME table row,
or to the selected record in the detail pane. A search box, filter, caption, nearby
activity item, or a different row does NOT establish ownership. Never join by numeric
suffix, name similarity, or guesswork. Report no record for an ownerless resource.
Read the visible IDs literally; do not swap a resource ID and user ID, invent
an account ID from a marketing ID, or reinterpret a READY/Live/Healthy label as
an unknown state. Use PRESENT for a visibly existing ready/live record.
state_at_evidence is PRESENT, ABSENT, REDACTED, ANONYMIZED, or TOMBSTONE, based only
on visible state. pii_hits is an array of {field_path,value_kind,value} for visibly
linked email, name, phone, email_hash or user_id values; preserve the exact text.
visible_text is a short exact excerpt containing both resource_id and user_ref, or
the selected-record header and its detail-panel owner field. If the source has no
same-row/selected-record link, return {\"records\":[]}. No prose, no inferred fields."""


def transcribe_image(path, llm_client, prompt=None):
    """Cache is owned by LLMClient; validate model labels without gold-case data."""
    if llm_client is None or not llm_client.enabled:
        return {"records": [], "error": "vision_unavailable"}
    call_args={"model":"gpt-4o-mini", "max_tokens":2500, "detail":"high", "response_schema":VISION_SCHEMA}
    base_prompt=prompt or PROMPT
    raw=llm_client.call_vision(base_prompt, path, "image_transcript", **call_args)
    try: data=json.loads(raw)
    except (ValueError, TypeError): data=None
    if not isinstance(data,dict) or not isinstance(data.get("records"),list):
        retry=llm_client.call_vision(base_prompt+"\nRetry: return only the specified records array, using exact visible fields.",
                                     path,"image_transcript_retry",**call_args)
        try: data=json.loads(retry)
        except (ValueError,TypeError): data=None
    if not isinstance(data,dict) or not isinstance(data.get("records"),list):
        return {"records": [], "error": "vision_schema_failed_after_retry"}
    validated, rejected=_validate_rows(data["records"])
    candidate_refs={str(item.get("user_ref") or "").casefold() for item in data["records"] if isinstance(item,dict)}
    if rejected:
        correction=(base_prompt+"\nIMPORTANT CORRECTION: your previous response contained rows with "
                    "a missing literal resource/user pair, invalid ID, or invalid state. "
                    "Re-read the image. For EACH row, visible_text must include the exact "
                    "resource_id AND exact user_ref, copied from that same table row or "
                    "from the selected record header plus its owner detail. If either is "
                    "not visible, OMIT that row. PII value_kind must be email, name, phone, "
                    "email_hash, or user_id. Do not return linked order references as an "
                    "account or support record. Previous invalid rows: "
                    +json.dumps(rejected,ensure_ascii=False)[:1800])
        retry=llm_client.call_vision(correction,path,"image_transcript_retry",**call_args)
        try:
            second=json.loads(retry)
            if isinstance(second,dict) and isinstance(second.get("records"),list):
                candidate_refs.update(str(item.get("user_ref") or "").casefold() for item in second["records"] if isinstance(item,dict))
                more,_=_validate_rows(second["records"])
                validated.extend(more)
        except (ValueError,TypeError):
            pass
    # Same visible row may be repeated in table and detail pane; not two facts.
    distinct={}
    for row in validated:
        distinct[(row["system_id"],row["resource_id"],row["user_ref"])]=row
    return {"records":list(distinct.values()), "candidate_refs":sorted(candidate_refs-{''}), "error":None}


def _validate_rows(items):
    validated=[]; rejected=[]
    for item in items:
        if not isinstance(item,dict): continue
        rid=str(item.get("resource_id") or "").strip()
        ref=str(item.get("user_ref") or "").strip()
        state=str(item.get("state_at_evidence") or "").upper()
        excerpt=str(item.get("visible_text") or "")
        if not RESOURCE.fullmatch(rid) or not (USER.fullmatch(ref) or EMAIL.fullmatch(ref)):
            rejected.append(item); continue
        if state not in {"PRESENT","ABSENT","REDACTED","ANONYMIZED","TOMBSTONE"}:
            rejected.append(item); continue
        # Model self-quotation is an audit aid, not independent proof. Require
        # the two exact identifiers in it before admitting the row.
        if rid.casefold() not in excerpt.casefold() or ref.casefold() not in excerpt.casefold():
            rejected.append(item); continue
        hits=[]
        for hit in item.get("pii_hits",[]):
            if not isinstance(hit,dict) or hit.get("value_kind") not in {"email","name","phone","email_hash","user_id"}:
                continue
            if not isinstance(hit.get("value"),str) or not hit["value"].strip(): continue
            hits.append({"field_path":str(hit.get("field_path") or ""),
                         "value_kind":hit["value_kind"],"value":hit["value"]})
        validated.append({"system_id":SYSTEM_BY_PREFIX[rid.rsplit("_",1)[0].casefold()],
                          "resource_id":rid,"user_ref":ref.casefold() if "@" in ref else ref,
                          "state_at_evidence":state,"pii_hits":hits,"visible_text":excerpt})
    return validated,rejected


def scan_all_images(root, llm_client):
    root=Path(root)
    entries={}
    for path in sorted((root/"dataset/evidence/images").glob("*")):
        if path.suffix.lower() not in {".png",".jpg",".jpeg"}: continue
        entries[path.name]=transcribe_image(path,llm_client)
    target=root/"code/evaluation/image_transcripts.json"
    target.write_text(json.dumps(entries,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return entries


def top_content_crop(path,root):
    """Exclude blank screenshot footer; preserve native text resolution."""
    from PIL import Image
    import hashlib
    path=Path(path)
    directory=Path(root)/"code/.cache/image_crops"
    directory.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    target=directory/f"{digest}_top.png"
    if not target.is_file():
        with Image.open(path) as image:
            height=min(image.height,max(700,int(image.height*0.65)))
            image.crop((0,0,image.width,height)).save(target)
    return target


if __name__=="__main__":
    import sys
    root=Path(__file__).resolve().parents[2]
    sys.path.insert(0,str(root/"code"))
    from agent.llm.client import LLMClient
    result=scan_all_images(root,LLMClient(cache_dir=root/"code/.cache/llm_cache",
                                          traces_dir=root/"code/.cache/llm_traces"))
    print(f"Read {len(result)} images; validated {sum(len(v['records']) for v in result.values())} exact owner/resource rows; errors {sum(bool(v['error']) for v in result.values())}")
