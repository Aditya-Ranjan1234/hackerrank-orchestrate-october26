from types import SimpleNamespace as N
from orchestrator.catalog_aliases import catalog_record

IDENTITY=N(all_user_ids={'user_7'},all_emails={'a@example.test'})
def activity(system='object_storage',rid='object_9',alias='receipt_9.pdf'):
    return dict(activity_id='activity_test',event_type='LINK_RESOURCE_IDENTITY',source_system='data_catalog',target_system=system,
                resource_id=rid,event_time='2026-01-01T01:00:00Z',
                details=f'Attachment catalog confirmed {rid} ({alias}) belongs only to a@example.test and user_7; no other subject is linked.')
def parse(a,text,at='2026-01-02T00:00:00Z'):
    return catalog_record(a,text,IDENTITY,'2026-01-01T00:00:00Z',at)
def test_catalog_and_visible_filename_jointly_establish_attachment():
    r=parse(activity(),'Objects\nreceipt_9.pdf 384 KB Standard')
    assert (r.resource_id,r.user_ref,r.raw_row['document_kind'])==('object_9','user_7','support_attachment')
def test_catalog_does_not_prove_file_presence_by_itself():
    assert parse(activity(),'receipt_90.pdf') is None
def test_visible_conflicting_owner_blocks_join():
    assert parse(activity(),'receipt_9.pdf b@example.test') is None
def test_future_catalog_link_ignored():
    assert parse(activity(),'receipt_9.pdf','2026-01-01T00:30:00Z') is None
def test_unscoped_object_ownership_does_not_imply_exclusive_attachment():
    a=activity();a['details']=a['details'].replace('belongs only to','to')
    assert parse(a,'receipt_9.pdf') is None
def test_statement_alias_requires_visible_subject():
    a=activity('export_service','export_8','REF-8000')
    assert parse(a,'Statement REF-8000 user_7 a@example.test').raw_row['data_category']=='USER_EXPORT'
    assert parse(a,'Statement REF-8000') is None
def test_retained_stable_reference_has_no_direct_identifier():
    a=activity('identity_service','tombstone_9','user_7')
    r=parse(a,'Customer reference user_7 Retained reference')
    assert r.state_at_evidence=='REDACTED'
    assert parse(a,'user_7 Retained reference a@example.test') is None
