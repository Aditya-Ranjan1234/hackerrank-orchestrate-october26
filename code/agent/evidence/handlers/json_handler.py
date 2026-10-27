"""Extract identity-linked rows and their source snapshot metadata from JSON."""
import json
from datetime import datetime, timezone
from pathlib import Path
from ..ir import RecordState, PIIHit
from .common import email_hashes

TIMESTAMP_FIELD_PRIORITY=("observed_at","recorded_at","snapshot_at","snapshot_time","as_of","as_of_date","exported_at","created_at","timestamp","generated_at","captured_at")
SYSTEM_FIELDS=("system_id","system","data_store")
# A matching identifier in a selector/query is not proof that the row stores
# that person's data. These fields designate record ownership in the supplied
# JSON schemas; lookup_value and subject_selector intentionally do not.
OWNER_ID_FIELDS={"user_id","user_uuid","customer_id","customer_reference",
                 "subject_reference","owner_user_id","subject_user_id","target_user_id",
                 "user_ref","account_owner_id"}

def _email(value): return value.strip().casefold().strip("<>")

def _timestamp(value):
    if value is None or value=="": return None
    if isinstance(value,(int,float)):
        try: return datetime.fromtimestamp(value,timezone.utc)
        except (ValueError,OverflowError,OSError): return None
    try:
        parsed=datetime.fromisoformat(str(value).replace("Z","+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except (ValueError,TypeError): return None

def _own_timestamp(node):
    if not isinstance(node,dict): return None
    for field in TIMESTAMP_FIELD_PRIORITY:
        if field in node:
            parsed=_timestamp(node[field])
            if parsed: return parsed
    return None

def _path_system(path,file_id):
    import re
    match=re.match(r"evidence_(.+?_(?:service|platform|store|index))_",file_id)
    if match: return match.group(1),"filename"
    for part in path.parts:
        if re.fullmatch(r"[a-z][a-z0-9_]*_(?:service|platform|store|index)",part): return part,"path"
    return "json","path"

def extract(path:Path,file_id:str,known_ids=(),audit_at=None,activity_time_lookup=None,llm_resolver=None,case_id=None,include_post_audit=False):
    path=Path(path)
    identities=known_ids if hasattr(known_ids,"all_user_ids") else None
    ids=set(identities.all_user_ids) if identities else set(known_ids)
    emails={_email(x) for x in identities.all_emails} if identities else set()
    hashes=email_hashes(identities) if identities else set()
    data=json.loads(path.read_text(encoding="utf-8-sig"))
    default_ts=_own_timestamp(data)
    cutoff=_timestamp(audit_at)
    if default_ts is None and cutoff:
        mtime=datetime.fromtimestamp(path.stat().st_mtime,timezone.utc)
        if mtime<=cutoff: default_ts=mtime
    fallback_system, fallback_source=_path_system(path,file_id)
    out=[]; post=[]
    def visit(node,prefix="$",row=0,inherited_ts=default_ts,inherited_system=None,inherited_resource_id=None,inherited_collection=None):
        if isinstance(node,dict):
            ts=_own_timestamp(node) or inherited_ts
            own_resource_id=next((str(node[key]) for key in ("id","resource_id","account_id") if node.get(key) is not None),None)
            resource_id=own_resource_id or inherited_resource_id or prefix
            explicit_system=next((str(node[k]) for k in SYSTEM_FIELDS if node.get(k)),None)
            system=explicit_system or inherited_system or fallback_system
            source="explicit" if explicit_system or inherited_system else fallback_source
            collection=node.get("collection") or inherited_collection
            # A selector stored on a connector configuration identifies the
            # configured subject. A transient lookup/query selector does not.
            connector_selector=(collection=="connector_configurations"
                                and system=="integration_service"
                                and str(node.get("resource_id") or "").startswith("data_flow_"))
            attachment_uploader=(collection=="ticket_attachments"
                                 and system in {"support_platform","support_service"}
                                 and str(node.get("resource_id") or "").startswith("support_")
                                 and node.get("storage_class")=="ticket_attachment")
            hits=[]; user=""
            for key,value in node.items():
                if not isinstance(value,str): continue
                name=key.casefold().strip()
                owner_field=(name in OWNER_ID_FIELDS
                             or (connector_selector and name=="subject_selector")
                             or (attachment_uploader and name=="uploaded_by"))
                if owner_field and value in ids:
                    if not ("result" in node and name=="subject_reference"):
                        hits.append(PIIHit(f"{prefix}.{key}","user_id",value,source_row=row))
                    user=value
                elif owner_field and _email(value) in emails:
                    normalized=_email(value)
                    if not ("result" in node and name=="subject_reference"):
                        hits.append(PIIHit(f"{prefix}.{key}","email",normalized,source_row=row))
                    user=user or normalized
                elif owner_field and value.casefold() in hashes:
                    if not ("result" in node and name=="subject_reference"):
                        hits.append(PIIHit(f"{prefix}.{key}","email_hash",value,source_row=row))
                    user=user or (getattr(identities,"primary_user_id",None) or value)
                elif "email" in name and name not in {"email_hash","email_sha256","hashed_email"} and _email(value) in emails:
                    hits.append(PIIHit(f"{prefix}.{key}","email",_email(value),source_row=row)); user=user or _email(value)
                elif ("hash" in name) and value.casefold() in hashes:
                    hits.append(PIIHit(f"{prefix}.{key}","email_hash",value,source_row=row)); user=user or (getattr(identities,"primary_user_id",None) or value)
            if user:
                for key,value in node.items():
                    if not isinstance(value,str): continue
                    name=key.casefold().strip()
                    if "email" in name and name not in {"email_hash","email_sha256","hashed_email"}:
                        hits.append(PIIHit(f"{prefix}.{key}","email",_email(value),source_row=row))
                    elif name in {"name","full_name","first_name","last_name","display_name"}:
                        hits.append(PIIHit(f"{prefix}.{key}","name",value,source_row=row))
                    elif "phone" in name or "mobile" in name or "telephone" in name:
                        hits.append(PIIHit(f"{prefix}.{key}","phone",value,source_row=row))
                    elif name in {"email_hash","email_sha256","hashed_email"}:
                        hits.append(PIIHit(f"{prefix}.{key}","email_hash",value,source_row=row))
                rid=resource_id
                record_ts=ts or (_timestamp(activity_time_lookup(rid)) if activity_time_lookup else None)
                result=str(node.get("result") or "").strip().upper()
                state=("ABSENT" if node.get("deleted") is True or result in {"NOT_FOUND","MISSING","DELETED"}
                       else result if result in {"REDACTED","ANONYMIZED","TOMBSTONE"}
                       else "PRESENT")
                if system=="support_platform" and node.get("resource_id","").startswith("support_"):
                    contact_fields=("requester_email","requester_name","requester_phone")
                    if (all(key in node and node[key] is None for key in contact_fields)
                            or (node.get("message_text")=="[REDACTED]" and not any(h.value_kind in {"email","name","phone","email_hash"} for h in hits))):
                        state="REDACTED"
                if system=="identity_service" and rid.startswith("tombstone_") and node.get("account_status")=="DELETED":
                    if all(key in node and node[key] is None for key in ("name","email","phone","email_hash")):
                        state="REDACTED"
                record=RecordState(system,rid,user,state,hits,record_ts,node,source)
                if llm_resolver is not None:
                    resolve_record_system(record,llm_resolver,file_id,path,case_id)
                (post if cutoff and ts and ts>cutoff else out).append(record)
            elif not user and node.get("status_code")==404 and node.get("profile") is None and node.get("resource_id"):
                # Ownership is intentionally unresolved here. The reconstructor
                # may join this readback only by a previously proven full ID.
                (post if cutoff and ts and ts>cutoff else out).append(RecordState(system,str(node["resource_id"]),"","ABSENT",[],ts,node,source))
            for key,value in node.items():
                nested_system=key if prefix=="$.service_exports" and key.endswith(("_service","_platform")) else (system if explicit_system or inherited_system else None)
                visit(value,f"{prefix}.{key}",row,ts,nested_system,own_resource_id or inherited_resource_id,collection)
        elif isinstance(node,list):
            for i,value in enumerate(node): visit(value,f"{prefix}[{i}]",i,inherited_ts,inherited_system,inherited_resource_id,inherited_collection)
    visit(data)
    return (out,post) if include_post_audit else out


def resolve_record_system(record,llm_resolver,file_id,path,case_id=None):
    """Use the model only for a genuinely unresolved JSON system, not explicit metadata."""
    if record.system_id != "json":
        return record
    system=llm_resolver.infer_system_id(record.raw_row,file_id,Path(path).name,fallback="json",case_id=case_id)
    if system!="json":
        record.system_id=system
        record.system_id_source="llm"
    return record
