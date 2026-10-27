import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.status.request_classifier import is_deletion_request
def test_delete(): assert is_deletion_request('Please delete my account')
def test_non_delete(): assert not is_deletion_request('Please export my data')
def test_ambiguous_delete_wins(): assert is_deletion_request('delete and export my data')
def test_empty_defaults_delete(): assert is_deletion_request('')
def test_other_deletion_words(): assert is_deletion_request('I want the right to be forgotten')
