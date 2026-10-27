from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.flows.restore_risk import RestoreRiskAnalyzer
class I:
    primary_user_id="user_1"; all_user_ids={"user_1"}; all_emails={"a@example.com"}
def delete(): return {"activity_id":"del","event_time":"2026-02-01T00:00:00Z","event_type":"DELETE_RECORD","target_system":"account_service","resource_id":"account_1","details":"deleted user_1"}
def backup(rid, time, **kw):
    d={"activity_id":rid,"event_time":time,"event_type":"BACKUP","source_system":"account_service","resource_id":rid,"details":"user_1","backup_type":"snapshot"}; d.update(kw); return d
AUDIT="2026-03-01T00:00:00Z"
def test_b1_post_deletion_backup_not_risk():
    r=RestoreRiskAnalyzer.build_risks(I(),[],[],[delete(),backup("b1","2026-02-02T00:00:00Z")],AUDIT)[0]; assert not r.is_risk_at_audit and "post_deletion_backup" in r.notes
def test_b2_expired_retention_not_risk():
    r=RestoreRiskAnalyzer.build_risks(I(),[],[],[delete(),backup("b2","2026-01-01T00:00:00Z",retention="1d")],AUDIT)[0]; assert not r.is_risk_at_audit and "retention_expired" in r.notes
def test_b3_destroyed_key_blocks():
    r=RestoreRiskAnalyzer.build_risks(I(),[],[],[delete(),backup("b3","2026-01-01T00:00:00Z",details="user_1 key_destroyed")],AUDIT)[0]; assert r.is_blocked and not r.is_risk_at_audit
def test_b4_base_only_is_risk():
    rs=RestoreRiskAnalyzer.build_risks(I(),[],[],[delete(),backup("base","2026-01-01T00:00:00Z"),backup("increment","2026-02-02T00:00:00Z")],AUDIT); assert rs[0].is_risk_at_audit and not rs[1].is_risk_at_audit
def test_b5_multiple_backups_each_risk():
    rs=RestoreRiskAnalyzer.build_risks(I(),[],[],[delete(),backup("b1","2026-01-01T00:00:00Z"),backup("b2","2026-01-15T00:00:00Z")],AUDIT); assert len(rs)==2 and all(x.is_risk_at_audit for x in rs)
def test_b6_no_deletion_has_no_risks():
    assert RestoreRiskAnalyzer.build_risks(I(),[],[],[backup("b1","2026-01-01T00:00:00Z")],AUDIT)==[]
def test_b7_block_restore():
    rs=RestoreRiskAnalyzer.build_risks(I(),[],[],[delete(),backup("b1","2026-01-01T00:00:00Z"),{"event_time":"2026-02-10T00:00:00Z","event_type":"BLOCK_RESTORE","resource_id":"b1"}],AUDIT); assert rs[0].is_blocked and not rs[0].is_risk_at_audit
def test_b10_equal_expiry_is_expired():
    r=RestoreRiskAnalyzer.build_risks(I(),[],[],[delete(),backup("b1","2026-02-01T00:00:00Z",retention="28d")],AUDIT)[0]; assert not r.is_risk_at_audit
