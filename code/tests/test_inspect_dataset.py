from pathlib import Path
from orchestrator.inspect_dataset import inspect_csv, inspect_evidence_file, _jaccard

def test_malformed_csv_continues(tmp_path):
    p=tmp_path/'bad.csv'; p.write_text('a,b\n1,2,3\n4,5\n',encoding='utf-8')
    report=inspect_csv(p)
    assert 'row_count: 2' in report and 'malformed_rows: 1' in report

def test_missing_evidence_reported(tmp_path):
    assert 'FILE_MISSING' in inspect_evidence_file(tmp_path/'absent.json')

def test_jaccard_measures_real_overlap():
    assert _jaccard({'r1','r2'},{'r2','r3'})==(1,2,2,0.333333)
