from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.state.reconstructor import reconstruct
from agent.state.reconstructor import _logical_system
from agent.evidence.ir import ExtractedEvidence, RecordState, PIIHit
from datetime import datetime, timezone

class I:
    primary_user_id="user_1"; all_user_ids={"user_1"}; all_emails={"a@example.com"}
def activity(op, resource="account_1", details="user_1"):
    return {"activity_id":"a1","event_time":"2026-01-01T00:00:00Z","event_type":op,"source_system":"x","target_system":"account_service","resource_id":resource,"details":details}
def ev(state="PRESENT", resource="account_1", ts=None):
    return ExtractedEvidence("e","x","h",[RecordState("account_service",resource,"user_1",state,[],ts,{})],"json",datetime.now(timezone.utc))
def test_simple_delete():
    assert reconstruct(I(),[],[activity("DELETE_RECORD")],"2026-02-01T00:00:00Z")[0].state_at_audit=="ABSENT"
def test_sync_recreation():
    assert reconstruct(I(),[],[activity("DELETE_RECORD"),activity("SYNC_RECORD")],"2026-02-01T00:00:00Z")[0].state_at_audit=="PRESENT"
def test_restore_override():
    assert reconstruct(I(),[],[activity("DELETE_RECORD"),activity("RESTORE_BACKUP")],"2026-02-01T00:00:00Z")[0].state_at_audit=="PRESENT"
def test_evidence_wins():
    facts=reconstruct(I(),[ev("PRESENT",ts=datetime(2026,1,2,tzinfo=timezone.utc))],[activity("DELETE_RECORD")],"2026-02-03T00:00:00Z")
    assert facts[0].state_at_audit=="PRESENT" and "evidence_PRESENT" in facts[0].notes[0]

def test_replica_timeline_uses_logical_record_without_duplicate_fact():
    sync=activity("SYNC_RECORD")
    sync["target_system"]="account_replication_cluster"
    facts=reconstruct(I(),[ev("PRESENT",ts=datetime(2026,1,2,tzinfo=timezone.utc))],
                      [sync],"2026-02-03T00:00:00Z")
    assert [(f.system_id,f.resource_id) for f in facts]==[("account_service","account_1")]

def test_nonmatching_replica_resource_is_not_relabelled():
    assert _logical_system("account_replication_cluster","order_1")=="account_replication_cluster"

def test_identity_link_and_restore_check_are_not_record_state_evidence():
    link=activity("LINK_RESOURCE_IDENTITY",resource="object_19",details="user_1 owns object_19")
    check=activity("CHECK_RESTORE_ACCESS",resource="backup_1",details="user_1 can restore")
    assert reconstruct(I(),[],[link,check],"2026-02-01T00:00:00Z")==[]
