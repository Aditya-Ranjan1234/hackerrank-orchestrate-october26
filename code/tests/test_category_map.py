import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.policy.category_map import category_for
def test_system_lookup(): assert category_for('account_service','x')=='account'
def test_table_lookup(): assert category_for('x','x',table_name='support_attachments')=='support_attachment'
def test_file_prefix_lookup(): assert category_for('x','x',file_id='evidence_backup_1')=='backup_snapshot'
def test_unknown_fallback(): assert category_for('unknown','x')=='unknown'
