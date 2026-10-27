"""Field-level sample step comparison; no production decision changes.

Usage: python code/orchestrator/step_diff.py [our_csv] [gold_csv]
"""
import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

FIELDS=("step_no","phase","system_id","resource_id","operation","state","evidence_id")
SEMANTIC_FIELDS=("phase","system_id","resource_id","operation","state")
TYPES={"phase":"PHASE_ORDER_MISMATCH","operation":"OPERATION_MISMATCH",
       "state":"STATE_MISMATCH","system_id":"SYSTEM_ID_MISMATCH",
       "resource_id":"RESOURCE_ID_MISMATCH","step_no":"STEP_NO_MISMATCH"}

@dataclass
class StepDiff:
    case_id:str
    our_status:str
    gold_status:str
    our_step_count:int
    gold_step_count:int
    status_match:bool
    step_array_match:bool
    mismatches:list[dict]

def classify_mismatch(field,our_val,gold_val):
    if field=="evidence_id":
        if our_val=="" and gold_val!="": return "EVIDENCE_ID_MISMATCH_SHOULD_CITE"
        if our_val!="" and gold_val=="": return "EVIDENCE_ID_MISMATCH_SHOULD_BE_EMPTY"
        return "EVIDENCE_ID_MISMATCH_WRONG_CITATION"
    return TYPES.get(field,"UNKNOWN")

def diff_case(our_row,gold_row):
    def get(row,key): return row[key] if isinstance(row,dict) else getattr(row,key)
    ours=json.loads(get(our_row,"steps_json") or "[]")
    gold=json.loads(get(gold_row,"steps_json") or "[]")
    mismatches=[]
    for index in range(max(len(ours),len(gold))):
        our_s=ours[index] if index<len(ours) else None
        gold_s=gold[index] if index<len(gold) else None
        if our_s is None or gold_s is None:
            mismatches.append({"step_index":index,"field":"step","our_value":our_s,
                               "gold_value":gold_s,"mismatch_type":"COUNT_MISMATCH"})
            continue
        for field in FIELDS:
            if our_s.get(field)!=gold_s.get(field):
                mismatches.append({"step_index":index,"field":field,
                                   "our_value":our_s.get(field),"gold_value":gold_s.get(field),
                                   "mismatch_type":classify_mismatch(field,our_s.get(field),gold_s.get(field))})
    return StepDiff(get(our_row,"case_id"),get(our_row,"deletion_status"),get(gold_row,"deletion_status"),
                    len(ours),len(gold),get(our_row,"deletion_status")==get(gold_row,"deletion_status"),
                    ours==gold,mismatches)

def _read(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as handle:
        return {r["case_id"]:r for r in csv.DictReader(handle)}

def semantic_counts(our_steps,gold_steps):
    """Compare step identities without cascading positional shifts."""
    ours={tuple(s.get(f) for f in SEMANTIC_FIELDS):s for s in our_steps}
    gold={tuple(s.get(f) for f in SEMANTIC_FIELDS):s for s in gold_steps}
    counts=Counter({"MISSING_SEMANTIC_STEP":len(gold.keys()-ours.keys()),
                    "EXTRA_SEMANTIC_STEP":len(ours.keys()-gold.keys())})
    counts["EVIDENCE_CITATION_DIFFERENCE"]=sum(ours[k].get("evidence_id")!=gold[k].get("evidence_id") for k in ours.keys()&gold.keys())
    return counts

def build_report(ours_path,gold_path,report_path=None):
    ours=_read(ours_path);gold=_read(gold_path)
    diffs=[diff_case(ours[cid],row) for cid,row in sorted(gold.items()) if cid in ours]
    counts=Counter(m["mismatch_type"] for d in diffs for m in d.mismatches)
    total=sum(counts.values());dominant=counts.most_common(1)[0] if counts else ("NONE",0)
    labels=("COUNT_MISMATCH","PHASE_ORDER_MISMATCH","OPERATION_MISMATCH","STATE_MISMATCH",
            "SYSTEM_ID_MISMATCH","RESOURCE_ID_MISMATCH","EVIDENCE_ID_MISMATCH_SHOULD_CITE",
            "EVIDENCE_ID_MISMATCH_SHOULD_BE_EMPTY","EVIDENCE_ID_MISMATCH_WRONG_CITATION","STEP_NO_MISMATCH")
    lines=["# Step-level gold diff", "",f"Source: `{ours_path}` vs `{gold_path}`. Cases: {len(diffs)}. Exact step arrays: {sum(d.step_array_match for d in diffs)}/{len(diffs)}.","",
           "## 1. Aggregate mismatch counts","| mismatch_type | count | % of all mismatches |","|---|---:|---:|"]
    lines += [f"| {label} | {counts[label]} | {100*counts[label]/total if total else 0:.2f}% |" for label in labels]
    semantic=Counter()
    for cid in gold.keys()&ours.keys():
        semantic.update(semantic_counts(json.loads(ours[cid]["steps_json"]),json.loads(gold[cid]["steps_json"])))
    lines += ["", "### Position-independent diagnosis", "| semantic difference | count |", "|---|---:|"]
    lines += [f"| {label} | {semantic[label]} |" for label in ("MISSING_SEMANTIC_STEP","EXTRA_SEMANTIC_STEP","EVIDENCE_CITATION_DIFFERENCE")]
    lines += ["", "### Every sample case", "| case | status match | exact array | missing resource/operation steps | extra steps | citation differences |", "|---|---|---|---:|---:|---:|"]
    for d in diffs:
        case_semantic=semantic_counts(json.loads(ours[d.case_id]["steps_json"]),json.loads(gold[d.case_id]["steps_json"]))
        lines.append(f"| {d.case_id} | {'yes' if d.status_match else 'no'} | {'yes' if d.step_array_match else 'no'} | {case_semantic['MISSING_SEMANTIC_STEP']} | {case_semantic['EXTRA_SEMANTIC_STEP']} | {case_semantic['EVIDENCE_CITATION_DIFFERENCE']} |")
    lines += ["",f"## 2. Dominant mismatch type\n{dominant[0]}: {dominant[1]}/{total} ({100*dominant[1]/total if total else 0:.2f}%).",
              "", "## 3. Five largest per-case diffs"]
    # Position-independent overlap distinguishes a misordered but otherwise
    # correct array from a genuinely different set of resources/operations.
    shared=our_total=gold_total=0
    for cid in gold:
        if cid not in ours: continue
        left={tuple(s.get(f) for f in FIELDS if f!="step_no") for s in json.loads(ours[cid]["steps_json"])}
        right={tuple(s.get(f) for f in FIELDS if f!="step_no") for s in json.loads(gold[cid]["steps_json"])}
        shared+=len(left&right);our_total+=len(left);gold_total+=len(right)
    for d in sorted(diffs,key=lambda x:(-len(x.mismatches),x.case_id))[:5]:
        lines += ["",f"### {d.case_id}: ours {d.our_status} ({d.our_step_count}), gold {d.gold_status} ({d.gold_step_count})",
                  "Our steps:","```json",json.dumps(json.loads(ours[d.case_id]["steps_json"]),indent=2),"```",
                  "Gold steps:","```json",json.dumps(json.loads(gold[d.case_id]["steps_json"]),indent=2),"```",
                  "Differences:","```json",json.dumps(d.mismatches,indent=2),"```"]
    hypothesis={"COUNT_MISMATCH":"Check upstream verdict count before changing `steps/builder.py`.",
                "SYSTEM_ID_MISMATCH":"Likely upstream system attribution, not Phase 6.",
                "RESOURCE_ID_MISMATCH":"Likely upstream resource attribution, not Phase 6.",
                "OPERATION_MISMATCH":"Inspect `steps/mapper.py` only after aligning resources.",
                "STATE_MISMATCH":"Inspect `steps/builder.py` state mapping after aligning resources.",
                "PHASE_ORDER_MISMATCH":"Inspect `steps/ordering.py` after aligning step sets."}
    lines += ["","## 4. Hypothesis",hypothesis.get(dominant[0],"Inspect evidence citation and step alignment before a Phase 6 unfreeze."),
              f"Position-independent exact step identities shared: {shared}; ours: {our_total}; gold: {gold_total}. This excludes `step_no` and does not treat shifted positions as mapping errors.",
              "","## 5. Recommendation","Compare step identities independent of index, then trace the first incorrect verdict. A positional mismatch can be caused by upstream extra/missing resources; do not assume Phase 6 is defective from 0 exact arrays alone.",""]
    if report_path: Path(report_path).write_text("\n".join(lines),encoding="utf-8")
    return diffs,counts

if __name__=="__main__":
    import sys
    root=Path(__file__).resolve().parents[2]
    if len(sys.argv)>1:
        ours=Path(sys.argv[1])
    else:
        # The old default pointed at a stale Phase 12 snapshot. Build a current
        # 32-case sample without modifying the full submission CSV.
        from types import SimpleNamespace
        sys.path.insert(0,str(root/"code"))
        from orchestrator.pipeline import load_datasets,run_case
        from orchestrator.csv_writer import write_output
        ours=root/"code/.cache/step_diff_current_sample.csv"
        ours.parent.mkdir(parents=True,exist_ok=True)
        with (root/"dataset/sample_deletion_requests.csv").open(encoding="utf-8-sig",newline="") as handle:
            cases=list(csv.DictReader(handle))
        datasets=load_datasets(root)
        datasets.active_case_rows=cases
        results=[run_case(SimpleNamespace(**row),datasets) for row in cases]
        write_output([(r.case_id,r.deletion_status,r.steps_json) for r in results],ours)
    gold=Path(sys.argv[2]) if len(sys.argv)>2 else root/"dataset/sample_output.csv"
    diffs,counts=build_report(ours,gold,root/"code/evaluation/step_diff_report.md")
    print(f"{sum(d.step_array_match for d in diffs)}/{len(diffs)} exact step arrays; dominant={counts.most_common(1)}")
