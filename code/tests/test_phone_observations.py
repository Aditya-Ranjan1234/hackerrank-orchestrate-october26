from types import SimpleNamespace as N
from datetime import datetime,timezone
from agent.evidence.ir import ExtractedEvidence
from orchestrator.phone_observations import normalize_phone,phone_owners,add_phone_observations

def test_full_international_number_keeps_country_code():
    assert normalize_phone('+81 90 1234 5678')=='819012345678'
    assert normalize_phone('+91 90 1234 5678')!='819012345678'
    assert normalize_phone('ref-819012345678')==''

def test_phone_audit_recovers_old_number_but_rejects_future_event():
    event=dict(field_name='phone',user_id='user_8',event_time='2026-01-01T00:00:00Z',old_value='+1 202 555 0001',new_value='+1 202 555 0002')
    assert phone_owners([],[event],'2026-01-02T00:00:00Z')['12025550001']=={'user_8'}
    assert not phone_owners([],[event],'2025-12-01T00:00:00Z')

def test_phone_attachment_observation_requires_unique_owner(tmp_path):
    (tmp_path/'dataset').mkdir();p=tmp_path/'dataset/evidence.log'
    p.write_text('2026-01-02T00:00:00Z [support_platform] resource_id=support_9 event=attachment_pii_scan matched_value="+1 202 555 0001" file=receipt.pdf')
    m=[dict(file_id='evidence_test',file_path='evidence.log')]
    def evidence():return ExtractedEvidence('evidence_test','evidence.log','hash',[],'regex-log',datetime.now(timezone.utc))
    identity=N(all_user_ids={'user_8'},all_emails=set())
    people=[dict(user_id='user_8',phone='+1 202 555 0001',updated_at='2026-01-01T00:00:00Z')]
    ev=evidence();links=add_phone_observations(tmp_path,[ev],m,people,[],identity,'2026-01-03T00:00:00Z')
    assert len(links)==1 and ev.records[0].raw_row['record_type']=='SUPPORT_ATTACHMENT'
    assert ev.records[0].pii_hits[0].value_kind=='phone'
    people.append(dict(people[0],user_id='user_9'));ev=evidence()
    assert not add_phone_observations(tmp_path,[ev],m,people,[],identity,'2026-01-03T00:00:00Z')
