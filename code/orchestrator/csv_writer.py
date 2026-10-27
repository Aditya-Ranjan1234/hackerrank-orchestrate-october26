import csv,re
from pathlib import Path
def natural_sort_key(case_id):
 return tuple(int(x) if x.isdigit() else x for x in re.split(r'(\d+)',case_id))
def write_output(rows,path):
 rows=sorted(rows,key=lambda x:natural_sort_key(x[0]))
 with Path(path).open('w',encoding='utf-8',newline='') as f:
  w=csv.writer(f,quoting=csv.QUOTE_MINIMAL,lineterminator='\n');w.writerow(['case_id','deletion_status','steps_json']);w.writerows(rows)
