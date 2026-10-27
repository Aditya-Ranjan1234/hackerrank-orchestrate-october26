from agent.status.request_classifier import is_deletion_request

def test_deleting_recognized_as_deletion(): assert is_deletion_request("I am deleting my account")
def test_deleted_recognized_as_deletion(): assert is_deletion_request("My account was deleted but I still see records")
def test_deletion_recognized_as_deletion(): assert is_deletion_request("Requesting deletion per GDPR")
def test_anonymise_british_spelling(): assert is_deletion_request("Please anonymise my records")
def test_export_still_not_deletion(): assert not is_deletion_request("I want to export my data")
def test_ambiguous_deletion_wins(): assert is_deletion_request("Delete then export to me")

def test_portuguese_deletion_outweighs_verification_instruction():
    request = "Solicito a exclusão permanente da conta. Verifiquem os identificadores anteriores."
    assert is_deletion_request(request)
    assert is_deletion_request(request.replace("exclusão", "exclusao"))


def test_portuguese_verification_only_is_not_deletion():
    assert not is_deletion_request("Verifiquem os identificadores anteriores da minha conta.")
