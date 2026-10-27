from types import SimpleNamespace as N
from orchestrator.pipeline import _source_for_verdict


def test_restore_risk_cites_access_check_not_backup_snapshot():
    verdict=N(target_kind="restore_risk",system_id="backup_service",resource_id="backup_1")
    fact=N(system_id="backup_service",resource_id="backup_1",evidence_id="snapshot")
    risk=N(system_id="backup_service",resource_id="backup_1",evidence_id="access_check")
    assert _source_for_verdict(verdict,[fact],[],[risk]).evidence_id=="access_check"


def test_record_cites_record_evidence_even_with_same_resource_risk():
    verdict=N(target_kind="record",system_id="backup_service",resource_id="backup_1")
    fact=N(system_id="backup_service",resource_id="backup_1",evidence_id="snapshot")
    risk=N(system_id="backup_service",resource_id="backup_1",evidence_id="access_check")
    assert _source_for_verdict(verdict,[fact],[],[risk]).evidence_id=="snapshot"
