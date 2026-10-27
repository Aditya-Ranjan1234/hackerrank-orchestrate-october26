from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.flows.detector import FlowDetector
from agent.evidence.ir import ResourceFact

class I:
    primary_user_id="user_1"; all_user_ids={"user_1"}; all_emails={"a@example.com"}
def row(op="SYNC_RECORD", rid="flow1", details="user_1", **kw):
    d={"activity_id":rid,"event_time":"2026-01-10T00:00:00Z","event_type":op,"source_system":"account_service","target_system":"search_service","resource_id":rid,"details":details}; d.update(kw); return d
def fact(state="PRESENT", system="account_service", rid="account_1"):
    return ResourceFact(system,rid,"user_1",state,set(),"e",None,[])
def test_f1_active_recurring_can_recreate():
    f=FlowDetector.build_flows(I(),[],[fact()], [row(schedule="cron")], "2026-02-01T00:00:00Z")[0]
    assert f.is_active_at_audit and f.can_recreate_at_audit
def test_f2_recurring_without_last_run_is_active():
    f=FlowDetector.build_flows(I(),[],[fact()], [row(schedule="cron", last_run_at=None)], "2026-02-01T00:00:00Z")[0]
    assert f.is_active_at_audit
def test_f3_disabled_is_inactive():
    f=FlowDetector.build_flows(I(),[],[fact()], [row(schedule="cron"),row("DISABLE_DATA_FLOW", "flow1")], "2026-02-01T00:00:00Z")[0]
    assert not f.is_active_at_audit and f.schedule.is_disabled
def test_f4_empty_source_is_recorded_but_cannot_recreate():
    f=FlowDetector.build_flows(I(),[],[], [row(schedule="cron")], "2026-02-01T00:00:00Z")[0]
    assert f.is_active_at_audit and not f.can_recreate_at_audit
def test_f5_completed_one_time_export_is_inactive():
    f=FlowDetector.build_flows(I(),[],[fact()], [row("CREATE_EXPORT", "export1", schedule="one_time", last_run_at="2026-01-10T00:00:00Z")], "2026-02-01T00:00:00Z")[0]
    assert not f.is_active_at_audit
def test_f6_index_is_treated_as_flow():
    f=FlowDetector.build_flows(I(),[],[fact(system="account_service")], [row("INDEX_RECORD", "idx1", schedule="cron")], "2026-02-01T00:00:00Z")[0]
    assert f.target_system_id=="search_service" and f.is_active_at_audit
def test_flow_order_is_deterministic():
    rows=[row(rid="b",schedule="cron"),row(rid="a",schedule="cron")]
    a=FlowDetector.build_flows(I(),[],[fact()],rows,"2026-02-01T00:00:00Z")
    b=FlowDetector.build_flows(I(),[],[fact()],list(reversed(rows)),"2026-02-01T00:00:00Z")
    assert [x.flow_id for x in a]==[x.flow_id for x in b]

def test_one_off_replication_checkpoint_is_not_active_flow():
    checkpoint=row("SYNC_RECORD", "account_1", "user_1; final checkpoint",
                   target_system="account_replication_cluster")
    flows=FlowDetector.build_flows(I(),[],[fact()], [checkpoint], "2026-02-01T00:00:00Z")
    assert len(flows)==1
    assert not flows[0].is_active_at_audit
    assert not flows[0].can_recreate_at_audit

def test_scheduled_replication_remains_active_flow():
    checkpoint=row("SYNC_RECORD", "account_1", "user_1; final checkpoint",
                   schedule="cron", target_system="account_replication_cluster")
    flows=FlowDetector.build_flows(I(),[],[fact()], [checkpoint], "2026-02-01T00:00:00Z")
    assert len(flows)==1 and flows[0].is_active_at_audit
