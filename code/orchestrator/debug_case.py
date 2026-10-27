"""Show the actual pipeline trace for one public sample request."""
import csv, json, sys
from pathlib import Path
from types import SimpleNamespace as N
from .pipeline import load_datasets, run_case
from .dataset_catalog import GAP_TARGETS, audit_gap_cases

def dump_case(case_id, root=None):
    root=Path(root or Path(__file__).resolve().parents[2]); ds=load_datasets(root)
    with (root/'dataset/sample_deletion_requests.csv').open(encoding='utf-8-sig',newline='') as f:
        sample_rows=list(csv.DictReader(f))
    row=next(r for r in sample_rows if r['case_id']==case_id)
    ds.active_case_rows=sample_rows
    ident=ds.resolver.resolve(row['email'],row['audit_at'])
    result=run_case(N(**row),ds)
    diagnostics=root/'code/.cache/diagnostics'/f'{case_id}.jsonl'
    entries=[json.loads(line) for line in diagnostics.read_text(encoding='utf-8').splitlines()]
    event={(entry['phase'],entry['event']):entry for entry in entries}
    print(f"=== CASE ===\n{row}\n=== IDENTITY BUNDLE ===\n{ident}")
    print("=== EVIDENCE PER FILE ===")
    extracted=event['evidence','extract_evidence']['outputs']
    for item in extracted['files']:
        print(item['file_id'],item['record_count'],item['path'])
    print("=== DATASET INVENTORY / OWNERSHIP AUDIT (Phase 17) ===")
    if case_id in GAP_TARGETS:
        audit=audit_gap_cases(root)[case_id]
        print(f"target={audit['target']} exact_direct_links={audit['direct']} target_files={audit['target_files']} subject_files={audit['subject_files']}")
    else:
        print("See code/evaluation/dataset_catalog.md for file and schema inventory")
    print("=== DERIVED ACTIVITIES ===")
    expansion=event['expander','expand_activities']['outputs']
    for derived in expansion['derived']:
        print(f"original={derived['original_activity_id']} resource={derived['resource_id']} "
              f"method={derived['method']} new_id={derived['activity_id']}")
    print("workflow_affiliation",expansion.get('workflow_affiliation',[]))
    for phase, name, title, key in (
            ('state','reconstruct','RESOURCE FACTS','facts'),
            ('flows','detect','FLOW FACTS','flows'),
            ('flows','restore_risks','RESTORE RISK FACTS','risks'),
            ('policy','apply','POLICY VERDICTS','verdicts')):
        print(f"=== {title} ===")
        for item in event[phase,name]['outputs'][key]:
            print(item)
    print("=== STATUS / STEPS / ERRORS ===")
    print(result)
if __name__=='__main__': dump_case(sys.argv[1])
