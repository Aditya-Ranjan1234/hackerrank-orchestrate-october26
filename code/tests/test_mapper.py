import sys
from pathlib import Path
from types import SimpleNamespace as N
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.steps.mapper import finding_for_trigger, remediation_for_trigger, verification_for_trigger, verification_for_compliant_verdict

def trig(kind):
    return N(trigger_kind=kind)
def verd(action):
    return N(required_action=action)
def test_remaining():
    assert finding_for_trigger(trig('REMAINING_RECORD'), verd('DELETE_RECORD'))[0] == 'REPORT_REMAINING_RECORD'
def test_redact():
    assert remediation_for_trigger(trig('EXPOSED_PII'), verd('REDACT_RECORD'))[0] == 'REDACT_RECORD'
def test_anonymize():
    assert remediation_for_trigger(trig('ANONYMIZATION_INCOMPLETE'), verd('ANONYMIZE_RECORD'))[0] == 'ANONYMIZE_RECORD'
def test_flow():
    assert verification_for_trigger(trig('ACTIVE_DATA_FLOW'), verd('DISABLE_DATA_FLOW'))[0] == 'VERIFY_DATA_FLOW_DISABLED'
def test_restore():
    assert verification_for_trigger(trig('RESTORE_RISK'), verd('BLOCK_RESTORE'))[0] == 'VERIFY_RESTORE_BLOCKED'
def test_compliant():
    assert verification_for_compliant_verdict('RETAIN')[0] == 'VERIFY_RECORD_PRESENT'
