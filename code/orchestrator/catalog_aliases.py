"""Join explicit catalog aliases to visible artifacts, without suffix inference.

The catalog supplies identity and the canonical resource ID; the document or
screen supplies existence. Neither source alone supplies both facts.
"""
import re
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from agent.evidence.ir import RecordState, PIIHit

LINK=re.compile(r"(?:linked|confirmed)\s+(\w+)\s+\(([^)]+)\)\s+(?:to|belongs only to)\s+(.+)",re.I)
EMAIL=re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
USER=re.compile(r"(?<![\w-])user_\d+(?![\w-])")

def _dt(value):
    return datetime.fromisoformat(str(value).replace('Z','+00:00'))

@lru_cache(maxsize=64)
def artifact_text(path):
    path=Path(path)
    if path.suffix.lower()=='.pdf':
        import pdfplumber
        with pdfplumber.open(path) as document:
            return '\n'.join(page.extract_text() or '' for page in document.pages)
    if path.suffix.lower() in {'.png','.jpg','.jpeg'}:
        from .image_inspector import run_tesseract
        return run_tesseract(path)
    return ''

def catalog_record(activity,text,identity,captured_at,audit_at):
    """Return a source-backed alias row, or abstain on conflict/unsupported type."""
    if (activity.get('event_type')!='LINK_RESOURCE_IDENTITY'
            or activity.get('source_system')!='data_catalog'):
        return None
    try:
        if _dt(activity['event_time'])>_dt(audit_at) or _dt(captured_at)>_dt(audit_at):return None
    except (KeyError,ValueError,TypeError):return None
    match=LINK.search(activity.get('details',''))
    if not match:return None
    rid,alias,owner_text=match.groups()
    if rid!=activity.get('resource_id') or alias==rid:return None
    if not re.search(r'(?<![\w.-])'+re.escape(alias)+r'(?![\w.-])',text,re.I):return None
    ids=set(identity.all_user_ids);emails={x.casefold() for x in identity.all_emails}
    owner_ids=set(USER.findall(owner_text));owner_emails={x.casefold() for x in EMAIL.findall(owner_text)}
    if not owner_ids & ids or owner_ids-ids or owner_emails-emails:return None
    # A selected artifact must not silently override a conflicting visible owner.
    visible_ids=set(USER.findall(text));visible_emails={x.casefold() for x in EMAIL.findall(text)}
    if visible_ids-ids or visible_emails-emails:return None
    system=activity.get('target_system');kind='';state='PRESENT'
    if system=='object_storage' and 'belongs only to' in activity['details'] and alias.lower().endswith(('.pdf','.png','.jpg','.jpeg')):
        kind='support_attachment'
    elif system=='export_service' and (visible_ids & ids or visible_emails & emails):
        kind='user_export'
    elif (system=='identity_service' and rid.startswith('tombstone_')
          and alias in ids and 'retained reference' in text.casefold()
          and not visible_emails and not re.search(r'\+\d[\d ()-]{6,}\d',text)):
        kind='account_tombstone';state='REDACTED'
    else:return None
    user=sorted(owner_ids & ids)[0]
    hits=[PIIHit('catalog.subject','user_id',user)]
    hits.extend(PIIHit('document.email','email',email) for email in sorted(visible_emails & emails))
    raw={'catalog_activity_id':activity['activity_id'],'catalog_alias':alias,
         'source_alias_verified':True,'document_kind':kind,
         'data_category':{'user_export':'USER_EXPORT','account_tombstone':'ACCOUNT_TOMBSTONE',
                          'support_attachment':'SUPPORT_ATTACHMENT'}[kind]}
    return RecordState(system,rid,user,state,hits,_dt(captured_at),raw)

def add_catalog_artifacts(root,evidence,manifest,activities,identity,audit_at):
    sources={m['file_id']:m for m in manifest}
    links=[a for a in activities if a.get('event_type')=='LINK_RESOURCE_IDENTITY']
    added=[]
    for ev in evidence:
        source=sources[ev.file_id]
        path=Path(root)/'dataset'/source['file_path']
        if path.suffix.lower() not in {'.pdf','.png','.jpg','.jpeg'}:continue
        text=artifact_text(str(path))
        for activity in links:
            record=catalog_record(activity,text,identity,source['captured_at'],audit_at)
            if record and not any(r.system_id==record.system_id and r.resource_id==record.resource_id for r in ev.records):
                ev.records.append(record)
                added.append({'file_id':ev.file_id,'resource_id':record.resource_id,
                              'activity_id':activity['activity_id'],'alias':record.raw_row['catalog_alias']})
    return added
