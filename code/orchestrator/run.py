import csv,sys
from pathlib import Path
from types import SimpleNamespace as N
from .pipeline import load_datasets,run_case
from .csv_writer import write_output
from .validator import validate_output
from agent.llm.usage_tracker import UsageTracker

def _usage_path(root,input_csv,output_csv):
 if Path(input_csv).resolve()==(root/'dataset/deletion_requests.csv').resolve() and Path(output_csv).resolve()==(root/'output.csv').resolve():
  return root/'code/evaluation/usage_report.md'
 return root/'code/.cache/usage_report_non_submission.md'

def _validation_path(root,input_csv,output_csv):
 if _usage_path(root,input_csv,output_csv)==root/'code/evaluation/usage_report.md':
  return root/'code/evaluation/phase7_orchestrator_validation.md'
 return root/'code/.cache/validator_non_submission.md'

def main(input_csv,output_csv):
 root=Path(__file__).resolve().parents[2]; data=load_datasets(root); results=[]
 with Path(input_csv).open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
 data.active_case_rows=rows
 for row in rows:results.append(run_case(N(**row),data))
 UsageTracker.instance().request_count=len(results)
 write_output([(r.case_id,r.deletion_status,r.steps_json) for r in results],output_csv)
 UsageTracker.instance().write_report(_usage_path(root,input_csv,output_csv))
 report=validate_output(output_csv,input_csv);report.write_to(_validation_path(root,input_csv,output_csv))
 failed=[r for r in results if r.errors]
 if failed:
  report.add_fatal(f'{len(failed)} cases had pipeline errors; first={failed[0].case_id}:{failed[0].errors[:2]}')
  report.write_to(_validation_path(root,input_csv,output_csv))
 print(f'Wrote {output_csv} with {len(results)} rows. Validation: {report.passed_count}/{report.total_checks} checks passed.')
 if report.errors:print('First 5 errors:',report.errors[:5])
 return report
if __name__=='__main__':
 report=main(Path(sys.argv[1]) if len(sys.argv)>1 else Path('dataset/deletion_requests.csv'),
             Path(sys.argv[2]) if len(sys.argv)>2 else Path('output.csv'))
 raise SystemExit(1 if report.errors else 0)
