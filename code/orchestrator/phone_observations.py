"""Exact historical-phone joins for typed source fields; never last-N matching."""
import re
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from agent.evidence.ir import RecordState,PIIHit
from agent.evidence.handlers.log_handler import _event,_state

def normalize_phone(value):
    value=str(value or '').strip()
    if not re.fullmatch(r'\+?[0-9][0-9 ()-]{6,}[0-9]',value):return ''
    return re.sub(r'\D','',value)

def phone_owners(identities,audits,audit_at):
    cutoff=datetime.fromisoformat(str(audit_at).replace('Z','+00:00'))
    out=defaultdict(set)
    for row in identities:
        try:visible=datetime.fromisoformat(row['updated_at'].replace('Z','+00:00'))<=cutoff
        except (KeyError,ValueError):visible=False
        if visible and (value:=normalize_phone(row.get('phone'))):out[value].add(row['user_id'])
    for row in audits:
        if row.get('field_name')!='phone':continue
        try:visible=datetime.fromisoformat(row['event_time'].replace('Z','+00:00'))<=cutoff
        except (KeyError,ValueError):visible=False
        if visible:
            for field in ('old_value','new_value'):
                if value:=normalize_phone(row.get(field)):out[value].add(row['user_id'])
    return out

@lru_cache(maxsize=64)
def _events(path):
    return [_event(line,n) for n,line in enumerate(Path(path).read_text(encoding='utf8').splitlines())]

def add_phone_observations(root,evidence,manifest,identities,audits,identity,audit_at):
    owners=phone_owners(identities,audits,audit_at)
    wanted={phone:next(iter(users)) for phone,users in owners.items()
            if len(users)==1 and users & set(identity.all_user_ids)}
    cutoff=datetime.fromisoformat(str(audit_at).replace('Z','+00:00'));sources={m['file_id']:m for m in manifest};links=[]
    for ev in evidence:
        path=Path(root)/'dataset'/sources[ev.file_id]['file_path']
        if path.suffix not in {'.log','.txt'}:continue
        for fields,ts,system,trace,row in _events(str(path)):
            rid=fields.get('resource_id');event=str(fields.get('event',''))
            if not rid or not system or not ts or ts>cutoff or event.endswith('_started'):continue
            matches=[(key,value,wanted[phone]) for key,value in fields.items()
                     if key in {'phone','requester_phone','customer_phone','matched_value'}
                     and (phone:=normalize_phone(value)) in wanted]
            if not matches:continue
            users={user for _,_,user in matches}
            if len(users)!=1:continue
            user=next(iter(users))
            if any(r.resource_id==rid and r.system_id==system and r.user_ref==user for r in ev.records):continue
            raw=dict(fields,source_row=row,phone_owner_exact=True)
            if event=='attachment_pii_scan' and fields.get('file'):raw['record_type']='SUPPORT_ATTACHMENT'
            hits=[PIIHit(f'line[{row+1}].{key}','phone',str(value),source_row=row) for key,value,_ in matches]
            ev.records.append(RecordState(system,str(rid),user,_state(fields,system),hits,ts,raw))
            links.append({'file_id':ev.file_id,'resource_id':rid,'source_row':row+1,'user_id':user})
    return links
