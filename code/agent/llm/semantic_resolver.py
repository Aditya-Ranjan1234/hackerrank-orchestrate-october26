"""Validate model suggestions against the bounded audit schema and source evidence."""

import json
from pathlib import Path

from .prompts.affiliation import AFFILIATION_PROMPT
from .prompts.flow_class import FLOW_CLASS_PROMPT
from .prompts.primary_file import PRIMARY_FILE_PROMPT
from .prompts.system_id import SYSTEM_ID_PROMPT

SYSTEMS={"account_service","order_service","support_platform","search_service","analytics_platform","log_service","backup_service","integration_service","security_service","export_service","cache_service","archive_service","marketing_platform","identity_service"}


def _parse(response):
    try:
        parsed=json.loads(response) if response is not None else None
        return parsed if isinstance(parsed,dict) else {}
    except (TypeError,ValueError):
        return {}


def _confident(result):
    try:
        return float(result.get("confidence",0))>=0.8
    except (TypeError,ValueError):
        return False


class SemanticResolver:
    def __init__(self,llm_client,diagnostic_logger=None):
        self.llm=llm_client
        self.logger=diagnostic_logger

    def infer_system_id(self,record_content,file_id,filename,fallback="unknown",case_id=None):
        prompt=SYSTEM_ID_PROMPT.format(record_json=json.dumps(record_content,default=str)[:2000],file_id=file_id,filename=filename)
        result=_parse(self.llm.call(prompt,"system_id",case_id=case_id))
        system=result.get("system_id")
        return system if system in SYSTEMS and _confident(result) else fallback

    def classify_flow_vs_record(self,record_content,resource_id,case_id=None):
        # A suggestive name is not proof of a live connector. Fail closed.
        fallback="record"
        prompt=FLOW_CLASS_PROMPT.format(record_json=json.dumps(record_content,default=str)[:2000],resource_id=resource_id)
        result=_parse(self.llm.call(prompt,"flow_class",case_id=case_id))
        label=result.get("classification")
        return label if label in {"flow","record"} and _confident(result) else fallback

    def affiliate_anonymous_record(self,record_content,identity_bundle,context_records,case_id=None):
        prompt=AFFILIATION_PROMPT.format(record_json=json.dumps(record_content,default=str)[:2000],user_ids=sorted(identity_bundle.all_user_ids),emails=sorted(identity_bundle.all_emails),email_hashes=sorted(getattr(identity_bundle,"all_email_hashes",[])),context_summary=json.dumps(context_records[:5],default=str)[:1500])
        result=_parse(self.llm.call(prompt,"affiliation",case_id=case_id))
        uid=result.get("user_id")
        rid=result.get("supporting_resource_id")
        if uid not in identity_bundle.all_user_ids or not rid or rid!=record_content.get("resource_id"):
            return None
        # A language-model assertion is not ownership evidence. Require the same
        # full resource ID in directly identity-owned context.
        if not any(x.get("resource_id")==rid and x.get("user_ref") in identity_bundle.all_user_ids for x in context_records):
            return None
        return uid if _confident(result) else None

    def select_primary_evidence_file(self,candidate_files,case_row,identity_bundle):
        if not candidate_files:return ""
        from datetime import datetime, timezone
        def parse(value):
            if not value:return None
            try:
                parsed=datetime.fromisoformat(str(value).replace("Z","+00:00"))
                return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
            except (TypeError,ValueError):return None
        cutoff=parse(case_row.audit_at)
        eligible=[f for f in candidate_files if not f.get("timestamp") or (parse(f["timestamp"]) and (cutoff is None or parse(f["timestamp"])<=cutoff))]
        if not eligible:return ""
        contemporaneous=[f for f in eligible if parse(f.get("captured_at")) and (cutoff is None or parse(f["captured_at"])<=cutoff)]
        if contemporaneous:eligible=contemporaneous
        fallback=max(eligible,key=lambda f:(str(f.get("timestamp") or ""),f["file_id"]))["file_id"]
        prompt=PRIMARY_FILE_PROMPT.format(file_list=json.dumps(eligible,default=str)[:2000],case_id=case_row.case_id,audit_at=case_row.audit_at,primary_user_id=identity_bundle.primary_user_id)
        result=_parse(self.llm.call(prompt,"primary_file",case_id=case_row.case_id))
        chosen=result.get("primary_file_id")
        return chosen if chosen in {f["file_id"] for f in eligible} and _confident(result) else fallback

    def extract_pii_from_image(self,image_path:Path,identity_bundle,case_id=None):
        from orchestrator.image_transcriber import PROMPT, VISION_SCHEMA, _validate_rows
        prompt=(PROMPT+"\nFor this second, focused inspection, look for exact owner identifiers "
                f"{sorted(identity_bundle.all_user_ids)} and {sorted(identity_bundle.all_emails)}. "
                "A filter/search term is not a record owner. Preserve the same strict schema.")
        records=[]
        for attempt in range(2):
            response=self.llm.call_vision(prompt,image_path,"image_pii_retry" if attempt else "image_pii",
                                          case_id=case_id,model="gpt-4o-mini",max_tokens=1600,
                                          detail="high",response_schema=VISION_SCHEMA)
            parsed=_parse(response).get("records")
            if isinstance(parsed,list):
                records,_=_validate_rows(parsed)
                if records:
                    break
            prompt += "\nRetry: read the selected record and rows literally; omit any ownerless resource."
        allowed={str(x).casefold() for x in identity_bundle.all_user_ids}|{str(x).casefold() for x in identity_bundle.all_emails}
        return [r for r in records if str(r["user_ref"]).casefold() in allowed]
