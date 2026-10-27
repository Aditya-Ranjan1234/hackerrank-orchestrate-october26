import sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.evidence.handlers.log_handler import extract

IDENTITY=SimpleNamespace(all_user_ids={'user_1'},all_emails=set(),primary_user_id='user_1')
def read(tmp_path,system,payload):
    p=tmp_path/'source.log'
    p.write_text(f'2026-01-01T00:00:00Z [{system}] user_id=user_1 resource_id=item_1 '+payload,encoding='utf8')
    return extract(p,'evidence_fixture',IDENTITY,'2026-01-02T00:00:00Z')[0][0]

def test_explicit_redacted_message_is_readback_not_exposure(tmp_path):
    assert read(tmp_path,'support_platform','event=message_read message_text="[REDACTED]"').state_at_evidence=='REDACTED'

def test_redacted_body_does_not_hide_contact_email(tmp_path):
    assert read(tmp_path,'support_platform','event=message_read message_text="[REDACTED]" email=x@example.test').state_at_evidence=='PRESENT'

def test_attachment_scan_preserves_attachment_category(tmp_path):
    assert read(tmp_path,'support_platform','event=attachment_pii_scan file=receipt.pdf').raw_row['record_type']=='SUPPORT_ATTACHMENT'

def test_restore_denial_blocks_access(tmp_path):
    assert read(tmp_path,'backup_service','event=restore_authorization_completed decision=deny').raw_row['restore_allowed'] is False

def test_restore_eligibility_records_live_risk(tmp_path):
    assert read(tmp_path,'backup_service','event=restore_candidate_evaluated eligible=true deletion_block=false').raw_row['restore_allowed'] is True
