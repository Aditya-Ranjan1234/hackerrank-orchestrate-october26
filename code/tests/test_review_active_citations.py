from types import SimpleNamespace as N
from orchestrator.pipeline import _evidence_confirms_verdict, _contemporaneous_file

def test_present_connector_with_enabled_flag_proves_active_flow():
    rec=N(state_at_evidence='PRESENT',raw_row={'enabled':True})
    verdict=N(target_kind='flow',current_state='ACTIVE')
    assert _evidence_confirms_verdict(rec,verdict)
    rec.raw_row['enabled']=False
    assert not _evidence_confirms_verdict(rec,verdict)

def test_present_backup_with_restore_allowed_proves_risk():
    assert _evidence_confirms_verdict(N(state_at_evidence='PRESENT',raw_row={'restore_allowed':True}),N(target_kind='restore_risk',current_state='RISKY'))

def test_current_capture_preferred_over_later_export_of_same_state():
    candidates=[{'file_id':'before','timestamp':'2026-01-01T00:00:00Z','captured_at':'2026-01-01T00:00:00Z'},
                {'file_id':'after','timestamp':'2026-01-01T01:00:00Z','captured_at':'2026-01-03T00:00:00Z'}]
    assert _contemporaneous_file(candidates,'2026-01-02T00:00:00Z')=='before'
