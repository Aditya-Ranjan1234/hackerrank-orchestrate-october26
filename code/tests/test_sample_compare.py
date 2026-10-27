from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from orchestrator.sample_compare import compare
def files(tmp_path,a,b):
 h='case_id,deletion_status,steps_json\n';(tmp_path/'a.csv').write_text(h+a);(tmp_path/'b.csv').write_text(h+b);return tmp_path/'a.csv',tmp_path/'b.csv'
def test_status(tmp_path):assert compare(*files(tmp_path,'case_1,COMPLETE,[]\n','case_1,INCOMPLETE,[]\n')).status_accuracy==0
def test_steps(tmp_path):assert compare(*files(tmp_path,'case_1,COMPLETE,[]\n','case_1,COMPLETE,[]\n')).sequence_accuracy==1
def test_missing(tmp_path):assert compare(*files(tmp_path,'','case_1,COMPLETE,[]\n')).missing==['case_1']
