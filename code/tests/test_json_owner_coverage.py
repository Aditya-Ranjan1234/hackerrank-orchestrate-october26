from orchestrator.json_owner_coverage import _source_rows


def test_direct_owner_and_full_resource_pair_is_counted():
    source = {"resource_id": "account_42", "customer_reference": "user_1"}
    assert list(_source_rows(source, {"user_1": "user_1"})) == [("account_42", {"user_1"})]


def test_lookup_selector_and_actor_are_not_record_owners():
    source = {"resource_id": "account_42", "subject_selector": "user_1",
              "lookup_value": "user_1", "uploaded_by": "user_1"}
    assert list(_source_rows(source, {"user_1": "user_1"})) == []
