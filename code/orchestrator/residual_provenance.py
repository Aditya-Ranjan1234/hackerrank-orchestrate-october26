"""Diagnose missing sample steps without feeding sample gold into production."""
from collections import Counter
import csv
import json
import re
from datetime import datetime
from pathlib import Path

from .pipeline import load_datasets
from .pdf_inspector import inspect_pdf
from .image_inspector import run_tesseract


def _rows(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as handle:
        return {row["case_id"]:row for row in csv.DictReader(handle)}


def _identity_step(step):
    return tuple(step.get(key) for key in ("phase","system_id","resource_id","operation","state"))


def missing_steps(ours,gold):
    current=Counter(map(_identity_step,ours))
    expected=Counter(map(_identity_step,gold))
    return list((expected-current).elements())


def _source_lines(path):
    suffix=path.suffix.lower()
    if suffix==".pdf":
        parsed=inspect_pdf(path)
        for page in parsed["pages"]:
            for number,line in enumerate(page["text"].splitlines(),1):
                yield f"p{page['page']}:{number}",line
            for table_no,table in enumerate(page["tables"],1):
                for row_no,row in enumerate(table,1):
                    yield f"p{page['page']}:table{table_no}:row{row_no}"," ".join(str(value or "") for value in row)
    else:
        text=run_tesseract(path) if suffix in {".png",".jpg",".jpeg"} else path.read_text(encoding="utf-8-sig",errors="replace")
        for number,line in enumerate(text.splitlines(),1):
            yield str(number),line


def inventory_sources(root):
    root=Path(root)
    return [(path.relative_to(root).as_posix(),list(_source_lines(path)))
            for path in sorted((root/"dataset/evidence").rglob("*")) if path.is_file()]


def source_hits(resource_id,owner_refs,sources):
    pattern=re.compile(r"(?<![\w-])"+re.escape(resource_id)+r"(?![\w-])",re.I)
    hits=[]
    for name,lines in sources:
        for location,line in lines:
            if pattern.search(line):
                owner=any(ref and ref.casefold() in line.casefold() for ref in owner_refs)
                hits.append((name,location,owner))
    return hits


def write_report(root,sample_output=None):
    root=Path(root)
    ours=_rows(sample_output or root/"code/.cache/step_diff_current_sample.csv")
    gold=_rows(root/"dataset/sample_output.csv")
    cases=_rows(root/"dataset/sample_deletion_requests.csv")
    datasets=load_datasets(root)
    sources=inventory_sources(root)
    lines=["# Residual missing-step source audit", "",
           "Diagnostic only: gold is used to choose what to inspect, never by the production agent. Exact full-resource occurrences are counted in all 94 evidence files, including OCR and PDF tables. A same-line owner is a candidate join, not automatically sufficient proof; an owner elsewhere in the same file is not a join.", "",
           "| Case | Missing resource / operation | Source occurrences | Same-line subject hits | Source locations |",
           "|---|---|---:|---:|---|"]
    totals=Counter(); no_occurrence_cases=set(); direct_activity_owner_links=0; missing_without_source=[]
    for case_id,gold_row in gold.items():
        if case_id not in ours: continue
        identity=datasets.resolver.resolve(cases[case_id]["email"],cases[case_id]["audit_at"])
        refs=set(identity.all_user_ids)|set(identity.all_emails)
        for phase,system,resource,operation,state in missing_steps(
                json.loads(ours[case_id]["steps_json"]),json.loads(gold_row["steps_json"])):
            hits=source_hits(resource,refs,sources)
            owned=sum(1 for _,_,has_owner in hits if has_owner)
            category="no_occurrence" if not hits else "same_line_candidate" if owned else "ownerless_occurrence"
            totals[category]+=1
            if not hits:
                no_occurrence_cases.add(case_id)
                missing_without_source.append((case_id,resource))
                direct_activity_owner_links+=any(
                    row.get("resource_id")==resource and any(ref and ref.casefold() in str(row.get("details","")).casefold() for ref in refs)
                    for row in datasets.activities)
            places=", ".join(f"`{name}:{location}`" for name,location,_ in hits[:4]) or "—"
            if len(hits)>4: places+=f" (+{len(hits)-4} more)"
            lines.append(f"| {case_id} | `{system}/{resource}` `{operation}` | {len(hits)} | {owned} | {places} |")
    lines.extend(["", "## Classification totals", ""])
    lines.extend(f"- {category}: {count}" for category,count in sorted(totals.items()))
    lines.extend([f"- Distinct cases with a gold target absent from every evidence file: {len(no_occurrence_cases)}.",
                  f"- Those no-occurrence targets with a direct subject identifier in their activity details: {direct_activity_owner_links}."])
    lines.extend(["", "A zero occurrence means the supplied evidence files contain no literal full resource ID. It does not prove the resource never existed. Activity logs are a separate, often ownerless source and cannot by themselves establish which requester owned a target.","",
                  f"Under the agent's strict evidence-to-owner rule, these {len(no_occurrence_cases)} distinct no-occurrence cases cannot have exact gold step arrays without additional direct ownership evidence. Even if every other case matched, that rule implies a conditional ceiling of {len(gold)-len(no_occurrence_cases)}/{len(gold)} exact arrays; this is a provenance constraint, not a proof that the gold answers are false.",""])
    with (root/"dataset/deletion_requests.csv").open(encoding="utf-8-sig",newline="") as handle:
        all_requests=list(csv.DictReader(handle))+list(cases.values())
    def stamp(value): return datetime.fromisoformat(value.replace("Z","+00:00"))
    lines += ["## Why activity time alone cannot supply ownership", "",
              "For each missing full ID, this diagnostic counts requests whose `requested_at` to `reported_at` window overlaps an activity for that ID. `reported_at` is a claim and this calculation is not used by the agent. Even one temporal candidate would not be a direct ownership field.", "",
              "| Case | Resource ID | Pre-audit activity rows | Minimum overlapping requests per activity |",
              "|---|---|---:|---:|"]
    for case_id,resource in sorted(set(missing_without_source)):
        audit=stamp(cases[case_id]["audit_at"])
        activities=[row for row in datasets.activities if row.get("resource_id")==resource
                    and row.get("event_time") and stamp(row["event_time"])<=audit]
        counts=[sum(stamp(request["requested_at"])<=stamp(row["event_time"])<=stamp(request["reported_at"])
                    for request in all_requests) for row in activities]
        lines.append(f"| {case_id} | `{resource}` | {len(activities)} | {min(counts) if counts else 'n/a'} |")
    lines.append("")
    target=root/"code/evaluation/residual_step_provenance.md"
    target.write_text("\n".join(lines),encoding="utf-8")
    return target,totals


if __name__=="__main__":
    print(write_report(Path(__file__).resolve().parents[2]))
