"""Inspect supplied data without interpreting its deletion semantics."""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def _show(value, limit=160):
    s = str(value).replace("\n", "\\n")
    return s[:limit] + ("…" if len(s) > limit else "")

def inspect_csv(path: Path) -> str:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        cols = reader.fieldnames or []
        rows = list(reader)
    malformed = [(i+2, r) for i,r in enumerate(rows) if None in r or any(r.get(c) is None for c in cols)]
    lines = [f"### {path.name}", f"columns: {cols}", f"row_count: {len(rows)}", "first_5_rows:"]
    lines += [f"- line {i+2}: {_show(row, 400)}" for i,row in enumerate(rows[:5])]
    lines += ["distinct_values_per_column:"]
    for col in cols:
        values = Counter(str(r.get(col) or "") for r in rows)
        lines.append(f"- {col}: distinct={len(values)} first_10_sorted={sorted(values)[:10]} top_10_by_frequency={values.most_common(10)}")
    lines += ["null_counts:"]
    lines += [f"- {col}: {sum(not r.get(col) or str(r.get(col)).strip().lower() in {'null','none'} for r in rows)}" for col in cols]
    lines += [f"malformed_rows: {len(malformed)}"]
    lines += [f"- line {i}: {_show(row,400)}" for i,row in malformed[:20]]
    return "\n".join(lines)

def inspect_evidence_file(path: Path) -> str:
    if not path.exists(): return f"### {path.name}\nFILE_MISSING: {path}"
    ext = path.suffix.lower(); lines=[f"### {path.name}", f"path: {path}", f"bytes: {path.stat().st_size}"]
    if ext == ".json":
        try:
            obj=json.loads(path.read_text(encoding="utf-8-sig"))
            lines += [f"top_level_type: {type(obj).__name__}", f"top_level_keys: {list(obj) if isinstance(obj,dict) else 'n/a'}", f"sample: {_show(obj,600)}"]
        except (ValueError, UnicodeError) as exc: lines.append(f"PARSE_ERROR: {exc}")
    elif ext == ".sql":
        content=path.read_text(encoding="utf-8", errors="replace")
        creates=re.findall(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[\w"`]+',content,re.I)
        inserts=re.findall(r'INSERT\s+INTO[^;]+;',content,re.I|re.S)
        lines += [f"CREATE_TABLE: {creates[:20]}", f"sample_INSERT: {[_show(x,250) for x in inserts[:3]]}"]
    elif ext in {".log",".txt"}:
        content=path.read_text(encoding="utf-8",errors="replace").splitlines()
        lines += [f"line_count: {len(content)}", "first_20_lines:"] + [f"- {_show(x,400)}" for x in content[:20]] + ["last_20_lines:"] + [f"- {_show(x,400)}" for x in content[-20:]]
    elif ext == ".pdf":
        try:
            import pdfplumber
            with pdfplumber.open(path) as pdf: lines += [f"pages: {len(pdf.pages)}", f"first_page_text: {_show(pdf.pages[0].extract_text() or '',1000) if pdf.pages else ''}", f"first_page_tables: {len(pdf.pages[0].extract_tables()) if pdf.pages else 0}"]
        except Exception as exc: lines.append(f"PDF_INSPECTION_ERROR: {exc}")
    elif ext in {".png",".jpg",".jpeg"}:
        try:
            from PIL import Image
            with Image.open(path) as image: lines.append(f"dimensions: {image.size}")
        except Exception as exc: lines.append(f"IMAGE_INSPECTION_ERROR: {exc}")
    else: lines.append("unsupported_extension")
    return "\n".join(lines)

def _jaccard(a,b):
    a,b=set(a)-{"", "null", "None"},set(b)-{"", "null", "None"}
    return len(a&b),len(a),len(b),round(len(a&b)/len(a|b),6) if a|b else 0

def _json_fields(node, result):
    if isinstance(node,dict):
        for k,v in node.items():
            if isinstance(v,(str,int)) and (k in {"resource_id","system_id","data_store","target_user_id","user_id","user_ref","customer_reference"}): result.setdefault(k,set()).add(str(v))
            _json_fields(v,result)
    elif isinstance(node,list):
        for v in node: _json_fields(v,result)

def inspect_all(datasets_dir: Path) -> str:
    datasets_dir=Path(datasets_dir); chunks=["# Dataset grounding report", f"dataset_root: {datasets_dir.resolve()}"]
    csv_paths=sorted(datasets_dir.glob("*.csv"))
    for path in csv_paths:
        chunks.append(inspect_csv(path))
        if path.name in {"deletion_rules.csv","evidence_files.csv"}:
            chunks.append(f"#### Full rows: {path.name}\n" + "\n".join(f"- line {i+2}: {row}" for i,row in enumerate(csv.DictReader(path.open(encoding="utf-8-sig",newline="")))))
        if path.name=="sample_output.csv":
            chunks.append("#### Gold statuses\n" + "\n".join(f"- {r['case_id']}: {r['deletion_status']}" for r in csv.DictReader(path.open(encoding="utf-8-sig",newline=""))))
    manifest_path=datasets_dir/"evidence_files.csv"
    manifest=list(csv.DictReader(manifest_path.open(encoding="utf-8-sig",newline=""))) if manifest_path.exists() else []
    chunks.append("## Evidence file inventory")
    json_values={}
    for row in manifest:
        path=datasets_dir/row["file_path"]
        chunks.append(f"#### {row['file_id']}\n"+inspect_evidence_file(path))
        if path.suffix.lower()==".json" and path.exists():
            try: _json_fields(json.loads(path.read_text(encoding="utf-8-sig")),json_values)
            except (ValueError,UnicodeError): pass
    activities=list(csv.DictReader((datasets_dir/"system_activity.csv").open(encoding="utf-8-sig",newline="")))
    identities=list(csv.DictReader((datasets_dir/"user_identities.csv").open(encoding="utf-8-sig",newline="")))
    keys={"activity.resource_id vs JSON resource_id":({r.get('resource_id','') for r in activities},json_values.get('resource_id',set())),
          "activity target/source system vs JSON system_id/data_store":({r.get('target_system','') for r in activities}|{r.get('source_system','') for r in activities},json_values.get('system_id',set())|json_values.get('data_store',set())),
          "activity.target_user_id vs identities.user_id":({r.get('target_user_id','') for r in activities},{r.get('user_id','') for r in identities}),
          "activity.target_user_id vs JSON user refs":({r.get('target_user_id','') for r in activities},json_values.get('user_ref',set())|json_values.get('user_id',set())|json_values.get('customer_reference',set()))}
    chunks.append("## Cross-file join analysis\nObserved JSON scalar fields only; non-JSON evidence is separately inventoried above.")
    for name,(a,b) in keys.items():
        common,na,nb,j=_jaccard(a,b); chunks.append(f"- {name}: intersection={common}, left={na}, right={nb}, Jaccard={j}; examples={sorted((set(a)&set(b))-{''})[:20]}")
    chunks.append("## Actual activity columns and distincts")
    for col in ("event_type","source_system","target_system","resource_id","target_user_id"):
        chunks.append(f"- {col}: distinct={len({r.get(col,'') for r in activities})}, first_20={sorted({r.get(col,'') for r in activities})[:20]}")
    chunks.append(f"- target_user_id null_count={sum(not r.get('target_user_id') or r.get('target_user_id')=='null' for r in activities)}")
    return "\n\n".join(chunks)+"\n"

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--file"); parser.add_argument("--evidence"); args=parser.parse_args()
    if args.file: print(inspect_csv(ROOT/"dataset"/args.file)); return
    if args.evidence:
        rows=list(csv.DictReader((ROOT/"dataset/evidence_files.csv").open(encoding="utf-8-sig",newline="")))
        row=next((r for r in rows if r['file_id']==args.evidence or Path(r['file_path']).name==args.evidence),None)
        print(inspect_evidence_file(ROOT/"dataset"/(row['file_path'] if row else args.evidence))); return
    report=inspect_all(ROOT/"dataset"); out=ROOT/"code/evaluation/dataset_grounding_report.md"; out.write_text(report,encoding="utf-8"); print(out)
if __name__=="__main__": main()
