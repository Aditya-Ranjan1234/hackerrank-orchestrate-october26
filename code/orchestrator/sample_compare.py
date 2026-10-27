import csv,json
from dataclasses import dataclass,field
@dataclass
class ComparisonReport:
 total:int=0;status_matches:int=0;step_count_matches:int=0;sequence_matches:int=0;field_matches:int=0;field_total:int=0;missing:list[str]=field(default_factory=list);mismatches:list[str]=field(default_factory=list)
 @property
 def status_accuracy(self):return self.status_matches/self.total if self.total else 0
 @property
 def step_count_accuracy(self):return self.step_count_matches/self.total if self.total else 0
 @property
 def sequence_accuracy(self):return self.sequence_matches/self.total if self.total else 0
 @property
 def field_level_accuracy(self):return self.field_matches/self.field_total if self.field_total else 0
def compare(output_csv,sample_csv):
 def read(p):
  with open(p,encoding='utf-8',newline='') as f:return {r['case_id']:r for r in csv.DictReader(f)}
 out,gold=read(output_csv),read(sample_csv);r=ComparisonReport(total=len(gold))
 for cid,g in gold.items():
  if cid not in out:r.missing.append(cid);continue
  o=out[cid];r.status_matches+=o['deletion_status']==g['deletion_status'];os,gs=json.loads(o['steps_json']),json.loads(g['steps_json']);r.step_count_matches+=len(os)==len(gs);r.sequence_matches+=os==gs
  for a,b in zip(os,gs):
   for k in ['step_no','phase','system_id','resource_id','operation','state','evidence_id']:r.field_total+=1;r.field_matches+=a.get(k)==b.get(k)
 return r
