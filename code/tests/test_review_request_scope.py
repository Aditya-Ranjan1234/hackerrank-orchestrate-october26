import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.status.request_classifier import is_deletion_request

@pytest.mark.parametrize('text',[
    'Please correct my phone number and leave the account active.',
    'Please replace my old telephone number with the new one.',
    'Stop promotional emails. I am not asking for deletion.',
    'I need help resetting my login. Do not close the account.',
    'Correct my name without removing any records.',
    'Remove me from marketing lists only. Keep my account.',
    'This is an information request, not a request to erase my data.',
    'Send a copy of my receipts. Leave my profile in place.',
    "Send my information, but don't delete or change anything.",
])
def test_non_deletion_scope(text):
    assert not is_deletion_request(text)

@pytest.mark.parametrize('text',[
    'Do not delete my invoices. Delete my account and profile.',
    'Unsubscribe me from marketing. Also permanently delete my account.',
    'Please delete my account. Keep the legally required invoices.',
])
def test_positive_deletion_in_separate_clause(text):
    assert is_deletion_request(text)
