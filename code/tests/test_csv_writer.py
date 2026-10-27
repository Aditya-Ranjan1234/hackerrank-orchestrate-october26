import csv
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from orchestrator.csv_writer import write_output,natural_sort_key
def test_escape(tmp_path):
 p=tmp_path/'o.csv';write_output([('case_1','COMPLETE','[{"a":1,"b":2}]')],p);assert list(csv.DictReader(p.open()))[0]['steps_json'].startswith('[{')
def test_natural():
 p=tmp_path/'o.csv' if False else None
 assert sorted(['case_001','case_010','case_100','case_011'],key=natural_sort_key)==['case_001','case_010','case_011','case_100']
def test_bom(tmp_path):
 p=tmp_path/'o.csv';write_output([],p);assert p.read_bytes()[:3]!=b'\xef\xbb\xbf'
def test_newline(tmp_path):
 p=tmp_path/'o.csv';write_output([('case_1','NOT_APPLICABLE','[]')],p);assert p.read_bytes().endswith(b'\n')
