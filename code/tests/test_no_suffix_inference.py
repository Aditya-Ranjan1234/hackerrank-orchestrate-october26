from datetime import datetime, timezone
from types import SimpleNamespace
from agent.evidence.ir import ExtractedEvidence, RecordState
from agent.state.reconstructor import reconstruct
from orchestrator.activity_expander import expand_activities_for_user

IDENTITY=SimpleNamespace(primary_user_id="U005",all_user_ids={"U005"},all_emails={"u005@example.com"})
CUTOFF="2026-09-20T00:00:00Z"
def activity(**changes):
    base={"activity_id":"a1","event_time":"2026-09-15T00:00:00Z","event_type":"UPDATE_RECORD","source_system":"profile_service","target_system":"account_service","resource_id":"account_005","details":""}
    return base|changes
def evidence(ref):
    at=datetime(2026,9,15,tzinfo=timezone.utc)
    return ExtractedEvidence("e1","x","h",[RecordState("account_service","account_005",ref,"PRESENT",[],at,{})],"json",at)

def test_no_suffix_inference_in_reconstructor():
    assert reconstruct(IDENTITY,[],[activity()],CUTOFF)==[]

def test_no_suffix_inference_in_expander():
    rows=[activity(resource_id="backup_005")]
    assert expand_activities_for_user(rows,[],IDENTITY,CUTOFF)==rows

def test_strict_user_id_match_still_works():
    fact=reconstruct(IDENTITY,[],[activity(target_user_id="U005")],CUTOFF)[0]
    assert fact.user_id=="U005"

def test_strict_email_match_still_works():
    fact=reconstruct(IDENTITY,[evidence("u005@example.com")],[],CUTOFF)[0]
    assert fact.user_id=="U005"

