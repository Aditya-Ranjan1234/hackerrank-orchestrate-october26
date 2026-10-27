import csv,json
from dataclasses import dataclass,field
from pathlib import Path
from .csv_writer import natural_sort_key
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.steps.ordering import OPERATION_ORDER,ALLOWED_STATE
@dataclass
class ValidationReport:
 errors:list[str]=field(default_factory=list);warnings:list[str]=field(default_factory=list);checks:int=0
 @property
 def passed_count(self):return self.checks-len(self.errors)
 @property
 def total_checks(self):return self.checks
 def add_ok(self):self.checks+=1
 def add_error(self,x):self.errors.append(x);self.checks+=1
 def add_fatal(self,x):self.errors.append('FATAL:'+x);self.checks+=1
 def add_warn(self,x):self.warnings.append(x);self.checks+=1
 def write_to(self,path):Path(path).write_text('# Phase 7 Validator\n\n'+f'Checks: {self.passed_count}/{self.total_checks}\n\nErrors:\n'+'\n'.join('- '+x for x in self.errors)+'\n\nWarnings:\n'+'\n'.join('- '+x for x in self.warnings),encoding='utf-8')
def validate_output(output_csv,deletion_requests_csv):
 r=ValidationReport();output=Path(output_csv)
 if not output.exists():r.add_fatal('output_csv_missing');return r
 r.add_ok()
 with output.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
 with Path(deletion_requests_csv).open(encoding='utf-8',newline='') as f: requests=list(csv.DictReader(f))
 if len(rows)!=len(requests):r.add_fatal(f'row_count_mismatch: expected {len(requests)}, got {len(rows)}')
 else:r.add_ok()
 ids=[x['case_id'] for x in rows]; req={x['case_id'] for x in requests}
 if set(ids)!=req:r.add_error('case_id_set_mismatch')
 else:r.add_ok()
 if ids!=sorted(ids,key=natural_sort_key):r.add_error('case_id_not_sorted')
 else:r.add_ok()
 for row in rows:_validate_row(row,r)
 return r
def _validate_row(row,r):
 status=row.get('deletion_status');
 if status not in {'COMPLETE','INCOMPLETE','NOT_APPLICABLE'}:r.add_error(f"{row.get('case_id')}:bad_status");return
 r.add_ok()
 try:steps=json.loads(row.get('steps_json',''))
 except Exception:r.add_error(f"{row.get('case_id')}:invalid_json");return
 r.add_ok()
 if not isinstance(steps,list):r.add_error(f"{row.get('case_id')}:steps_not_array");return
 r.add_ok()
 if status=='NOT_APPLICABLE':
  if steps!=[]:r.add_error(f"{row['case_id']}:not_applicable_not_empty")
  else:r.add_ok()
  return
 for i,s in enumerate(steps):
  if not isinstance(s,dict):r.add_error(f"{row['case_id']}:step_not_object");continue
  if set(s)!=set(['step_no','phase','system_id','resource_id','operation','state','evidence_id']):r.add_error(f"{row['case_id']}:wrong_keys")
  else:r.add_ok()
  if s.get('step_no')!=i+1:r.add_error(f"{row['case_id']}:step_number")
  else:r.add_ok()
  if s.get('operation') not in OPERATION_ORDER:r.add_error(f"{row['case_id']}:operation")
  else:
   r.add_ok()
   if ALLOWED_STATE[s['operation']]!=s.get('state'):r.add_error(f"{row['case_id']}:state")
   else:r.add_ok()
  if status=='COMPLETE' and (s.get('phase')!='VERIFICATION' or not s.get('evidence_id')):r.add_error(f"{row['case_id']}:complete_evidence_phase")
  else:r.add_ok()
  if status=='INCOMPLETE' and ((s.get('phase')=='FINDING' and not s.get('evidence_id')) or (s.get('phase')!='FINDING' and s.get('evidence_id')!='')):r.add_error(f"{row['case_id']}:evidence_rule")
  else:r.add_ok()
 phases=[{'FINDING':0,'REMEDIATION':1,'VERIFICATION':2}.get(s.get('phase'),99) for s in steps if isinstance(s,dict)]
 if phases!=sorted(phases):r.add_error(f"{row['case_id']}:phase_order")
 else:r.add_ok()
