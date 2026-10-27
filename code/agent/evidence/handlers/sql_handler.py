import sqlite3, json
from pathlib import Path
from ..ir import RecordState, PIIHit
from .common import EMAIL, PHONE, hit, email_hashes
TABLE_TO_SYSTEM={"accounts":"account_service","orders":"order_service","support_tickets":"support_service","search_index":"search_service","analytics":"analytics_platform"}

def _state_flag(value):
    """Preserve the meaning of SQLite INTEGER booleans on state fields only."""
    if isinstance(value, bool): return value
    if isinstance(value, int) and value in (0, 1): return bool(value)
    if isinstance(value, str):
        normalized=value.strip().casefold()
        if normalized in {"0", "false"}: return False
        if normalized in {"1", "true"}: return True
    return value

def _pii_kind(name):
    name=name.casefold()
    if "hash" in name and "email" in name: return "email_hash"
    if "email" in name: return "email"
    if "phone" in name or "mobile" in name or "telephone" in name: return "phone"
    if name=="name" or name.endswith("_name") or name in {"full_name","display_name"}: return "name"
    return None

def _embedded_state(resource_id, embedded, hits):
    if not isinstance(embedded,dict): return "PRESENT"
    if embedded.get("deleted") is True or str(embedded.get("state","")).upper()=="ABSENT": return "ABSENT"
    if embedded.get("anonymized") is True or str(embedded.get("state","")).upper()=="ANONYMIZED": return "ANONYMIZED"
    if resource_id.startswith("tombstone_") and str(embedded.get("account_status","")).upper()=="DELETED":
        return "TOMBSTONE" if any(h.value_kind in {"email","name","phone","email_hash"} for h in hits) else "REDACTED"
    if str(embedded.get("state","")).upper()=="REDACTED": return "REDACTED"
    if (all(key in embedded and embedded[key] is None
            for key in ("requester_email", "requester_name", "requester_phone"))
            and not any(h.value_kind in {"email","name","phone","email_hash"} for h in hits)):
        return "REDACTED"
    if embedded.get("message_text")=="[REDACTED]" and all(embedded.get(k) is None for k in ("requester_email","requester_name","requester_phone")):
        return "REDACTED"
    return "PRESENT"

def infer_system(table, raw):
    """Use explicit origin first, then schema family; never a case-number suffix."""
    explicit=raw.get("system_id") or raw.get("origin_system")
    if explicit: return str(explicit)
    if table in TABLE_TO_SYSTEM: return TABLE_TO_SYSTEM[table]
    families=(("customer_profiles","account_service"),
              ("customer_search_documents","search_service"),
              ("search_documents","search_service"),
              ("customer_analytics_profiles","analytics_platform"),
              ("backup_restore_entries","backup_service"),
              ("connector_subscriptions","integration_service"),
              ("customer_exports","export_service"),
              ("security_audit_records","security_service"),
              ("support_records","support_platform"))
    return next((system for prefix,system in families if table.startswith(prefix)),"sql")
def extract(path: Path, file_id: str, identities):
    from orchestrator.database_inspector import OWNER_COLUMNS
    db=sqlite3.connect(":memory:"); db.executescript(path.read_text(encoding="utf-8")); out=[]
    wanted={x.casefold() for x in identities.all_emails}|set(identities.all_user_ids)|email_hashes(identities)
    for (table,) in db.execute("select name from sqlite_master where type='table'"):
        cols=[r[1] for r in db.execute(f'pragma table_info("{table}")')]; candidates=[c for c in cols if c.casefold() in OWNER_COLUMNS or c.casefold() in {"email_sha256","hashed_email"}]
        for rownum,row in enumerate(db.execute(f'select * from "{table}"')):
            raw=dict(zip(cols,row)); matches=[(c,str(raw[c])) for c in candidates if str(raw[c]).casefold() in wanted]
            nested_hits=[]; embedded_record=None
            def scan(value,prefix):
                if isinstance(value,dict):
                    collection=raw.get("collection_name") or raw.get("collection")
                    connector_selector=(prefix=="record_json"
                                        and collection=="connector_configurations"
                                        and raw.get("origin_system")=="integration_service"
                                        and str(raw.get("resource_id") or "").startswith("data_flow_"))
                    attachment_uploader=(prefix=="record_json"
                                         and collection=="ticket_attachments"
                                         and raw.get("origin_system") in {"support_platform","support_service"}
                                         and str(raw.get("resource_id") or "").startswith("support_")
                                         and value.get("storage_class")=="ticket_attachment")
                    owned=any(isinstance(child,str) and
                              (((key.casefold() in OWNER_COLUMNS or
                                  (connector_selector and key.casefold()=="subject_selector") or
                                  (attachment_uploader and key.casefold()=="uploaded_by"))
                                 and child.casefold() in wanted)
                               or ("hash" in key.casefold() and child.casefold() in wanted))
                              for key,child in value.items())
                    for key,child in value.items():
                        field=key.casefold();field_path=f"{prefix}.{key}"
                        if isinstance(child,str):
                            normalized=child.casefold()
                            identifier=((field in OWNER_COLUMNS or
                                         (connector_selector and field=="subject_selector") or
                                         (attachment_uploader and field=="uploaded_by"))
                                        and normalized in wanted) or ("hash" in field and normalized in wanted)
                            if identifier:
                                kind=("email_hash" if "hash" in field else "email"
                                      if "email" in field or "@" in child else "user_id")
                                nested_hits.append((field_path,child,kind))
                            elif owned and (kind:=_pii_kind(field)):
                                nested_hits.append((field_path,child,kind))
                        scan(child,field_path)
                elif isinstance(value,list):
                    for index,child in enumerate(value): scan(child,f"{prefix}[{index}]")
            for col,value in raw.items():
                if isinstance(value,str) and value.lstrip().startswith(("{","[")):
                    try:
                        parsed=json.loads(value)
                        if col=="record_json" and isinstance(parsed,dict): embedded_record=parsed
                        scan(parsed,col)
                    except json.JSONDecodeError: pass
            if nested_hits:
                matches.extend((path,value) for path,value,kind in nested_hits if kind in {"user_id","email","email_hash"} and value.casefold() in wanted)
            if not matches: continue
            user=next((v for c,v in matches if c.casefold() in {"user_id","user_uuid","customer_id","account_id"} and v in identities.all_user_ids),None) or (getattr(identities,"primary_user_id",None) or matches[0][1]); hs=[]
            for c,v in raw.items():
                kind=_pii_kind(c)
                if kind and v is not None: hs.append(PIIHit(c,kind,str(v).casefold() if kind=="email" else str(v),source_row=rownum))
            hs += [PIIHit(path,kind,value.casefold() if kind=="email" else value,source_row=rownum) for path,value,kind in nested_hits]
            rid=str(raw.get("id", raw.get("resource_id", raw.get("account_id", f"{table}_{rownum}"))))
            from .json_handler import _timestamp
            ts=next((_timestamp(raw.get(field)) for field in ("captured_at","updated_at","created_at","indexed_at","timestamp","as_of") if _timestamp(raw.get(field))),None)
            # Generic replica tables keep the business state inside record_json.
            # Surface only explicit state/retention fields; owner identification
            # still comes from the exact row or nested identifier scan above.
            if embedded_record is not None:
                for field in ("enabled", "restore_allowed", "retained_until", "retention_reason"):
                    if field not in raw and field in embedded_record:
                        raw[field]=embedded_record[field]
            for field in ("enabled", "restore_allowed"):
                if field in raw: raw[field]=_state_flag(raw[field])
            raw["_source_table"]=table
            out.append(RecordState(infer_system(table,raw),rid,user,_embedded_state(rid,embedded_record if embedded_record is not None else raw,hs),hs,ts,raw))
    db.close(); return out
