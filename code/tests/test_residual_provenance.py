from orchestrator.residual_provenance import missing_steps,source_hits


def test_missing_semantic_step_ignores_only_citation_difference():
    step={"phase":"VERIFICATION","system_id":"account_service","resource_id":"account_1",
          "operation":"VERIFY_RECORD_ABSENT","state":"ABSENT","evidence_id":"a"}
    assert missing_steps([{**step,"evidence_id":"b"}],[step])==[]


def test_source_hits_require_full_resource_id():
    sources=[("a.sql",[("1","account_10 user_1"),("2","account_1 user_1")])]
    assert source_hits("account_1",{"user_1"},sources)==[("a.sql","2",True)]
