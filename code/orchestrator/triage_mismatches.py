"""Compare sample decisions with gold and cite their per-case diagnostic records."""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def _source_for_fact(fact, root=ROOT):
    evid=fact.get('evidence_id',''); rid=fact.get('resource_id','')
    if evid.startswith('activity_'):
        path=Path(root)/'dataset/system_activity.csv'
        if path.exists():
            with path.open(encoding='utf-8-sig',newline='') as f:
                for i,row in enumerate(csv.DictReader(f),2):
                    if row['activity_id']==evid: return f'dataset/system_activity.csv:L{i} (activity_id={evid})'
    elif evid.startswith('evidence_'):
        path=Path(root)/'dataset/evidence_files.csv'
        if path.exists():
            with path.open(encoding='utf-8-sig',newline='') as f:
                for i,row in enumerate(csv.DictReader(f),2):
                    if row['file_id']!=evid: continue
                    source=Path(root)/'dataset'/row['file_path']
                    if source.suffix=='.json' and source.exists():
                        for j,line in enumerate(source.read_text(encoding='utf-8').splitlines(),1):
                            if rid and rid in line: return f'dataset/{row["file_path"]}:L{j} (manifest evidence_files.csv:L{i})'
                    return f'dataset/evidence_files.csv:L{i} (file_id={evid})'
    return ''

def _rows(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as f: return {r["case_id"]:r for r in csv.DictReader(f)}

def classify_divergence(yours,gold,log_entries=()):
    if yours==gold: return "STEPS_MISMATCH"
    if yours=="NOT_APPLICABLE" or gold=="NOT_APPLICABLE": return "WRONG_NA"
    if yours=="INCOMPLETE" and gold=="COMPLETE": return "OVER_DELETED"
    if yours=="COMPLETE" and gold=="INCOMPLETE": return "UNDER_DELETED"
    return "UNKNOWN"

def triage_one(case_id,out,gold,log_dir):
    path=Path(log_dir)/f"{case_id}.jsonl"
    result={"case_id":case_id,"your_status":out["deletion_status"],"gold_status":gold["deletion_status"],"divergence_type":classify_divergence(out["deletion_status"],gold["deletion_status"]),"failing_phase":"UNDETERMINED","failing_decision":"","grounded_in":"","proposed_fix":"Inspect cited upstream records.","hallucination_audit":"UNDETERMINED"}
    if not path.exists(): result.update(failing_phase="NO_LOG",failing_decision="NO DIAGNOSTIC LOG — rerun with logger enabled",hallucination_audit="NO_LOG"); return result
    entries=[json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x]
    crashes=[e for e in entries if e.get("outputs",{}).get("errors")]
    if crashes:
        error=crashes[0]; result.update(failing_phase=error['phase'],failing_decision="PIPELINE_CRASH: "+str(error['outputs']['errors'][0]),grounded_in=error['grounded_in'],proposed_fix="Repair this phase exception and rerun.")
    else:
        typ=result['divergence_type']; identity=next((e for e in entries if e['event']=='resolve_identity'),None)
        state=next((e for e in entries if e['event']=='reconstruct'),None)
        policy=next((e for e in entries if e['event']=='apply'),None)
        status=next((e for e in entries if e['event']=='decide'),None)
        try: os=json.loads(out['steps_json']); gs=json.loads(gold['steps_json'])
        except (KeyError,ValueError): os=[]; gs=[]
        if typ=="WRONG_NA":
            source=identity if identity and not identity['outputs'].get('primary_user_id') else status
            result['proposed_fix']="Check request intent and identity history against cited case/identity rows."
        elif typ=="OVER_DELETED":
            source=policy or state
            extra=[s for s in os if (s.get('operation'),s.get('resource_id')) not in {(x.get('operation'),x.get('resource_id')) for x in gs}]
            if extra:
                resource=extra[0].get('resource_id'); facts=state['outputs'].get('facts',[]) if state else []
                fact=next((f for f in facts if f.get('resource_id')==resource),None)
                if fact:
                    source=state
                    result['failing_decision']=f"extra step {extra[0]['operation']} for {resource}; fact={fact}"
                    result['grounded_in']=_source_for_fact(fact) or state['grounded_in']
            result['proposed_fix']="Review the extra resource's activity/evidence join and policy category; compare cited source ID to gold steps."
        elif typ=="UNDER_DELETED":
            source=state or policy
            missing=[s for s in gs if (s.get('operation'),s.get('resource_id')) not in {(x.get('operation'),x.get('resource_id')) for x in os}]
            if missing: result['failing_decision']=f"missing gold step {missing[0].get('operation')} for {missing[0].get('resource_id')}"
            result['proposed_fix']="Inspect the missing gold resource in evidence and activity exports, then repair its join."
        else:
            source=next((e for e in entries if e['event']=='generate'),None)
            result['proposed_fix']="Compare step operations, resource IDs, and evidence IDs."
        if source:
            result['failing_phase']=source['phase']; result['grounded_in']=result['grounded_in'] or source['grounded_in']
            result['failing_decision']=result['failing_decision'] or source['decision']
        if typ=="WRONG_NA":
            path=ROOT/'dataset/sample_deletion_requests.csv'
            if path.exists():
                with path.open(encoding='utf-8-sig',newline='') as f:
                    for i,row in enumerate(csv.DictReader(f),2):
                        if row['case_id']==case_id: result['grounded_in']=f'dataset/sample_deletion_requests.csv:L{i}'; result['failing_decision']+=f"; request_text={row['request_text']}"; break
    result['hallucination_audit']="GROUNDED_CITATION_PRESENT" if result['grounded_in'] else "HALLUCINATION_SUSPECTED"
    if "timeline-only: no matching evidence record" in result['failing_decision']:
        result['hallucination_audit']="HALLUCINATION_SUSPECTED: source row exists but user affiliation is inferred"
    if "'system_id': 'json'" in result['failing_decision']:
        result['hallucination_audit']="HALLUCINATION_SUSPECTED: source row exists but audit-time timestamp and system are lost"
    return result

def triage(output_csv,sample_csv,log_dir=None):
    out,gold=_rows(output_csv),_rows(sample_csv); log_dir=Path(log_dir or ROOT/"code/.cache/diagnostics")
    items=[]
    for case_id,g in gold.items():
        o=out.get(case_id)
        if o is None: items.append({"case_id":case_id,"your_status":"MISSING","gold_status":g['deletion_status'],"divergence_type":"MISSING","failing_phase":"NO_OUTPUT","grounded_in":"","hallucination_audit":"NO_LOG","failing_decision":"No output row","proposed_fix":"Run the sample input."}); continue
        try: steps_differ=json.loads(o['steps_json'])!=json.loads(g['steps_json'])
        except (ValueError,KeyError): steps_differ=True
        if o['deletion_status']!=g['deletion_status'] or steps_differ:
            items.append(triage_one(case_id,o,g,log_dir))
    mismatches=[x for x in items if x['your_status']!=x['gold_status']]
    lines=["# Mismatch triage report",f"Compared: {output_csv} vs {sample_csv}",f"Status mismatches: {len(mismatches)} / {len(gold)}",f"Step differences including status matches: {len(items)}", "## Summary table", "| case_id | yours | gold | divergence | candidate phase |", "|---|---|---|---|---|"]
    lines += [f"| {x['case_id']} | {x['your_status']} | {x['gold_status']} | {x['divergence_type']} | {x['failing_phase']} |" for x in mismatches]
    lines += ["## Per-case details"]
    for x in mismatches:
        lines += [f"### {x['case_id']}",f"- Your status: {x['your_status']}; gold: {x['gold_status']}; divergence: {x['divergence_type']}",f"- Candidate phase: {x['failing_phase']}",f"- Decision: {x['failing_decision']}",f"- Grounded in: {x['grounded_in'] or 'NONE'}",f"- Audit: {x['hallucination_audit']}",f"- Proposed fix: {x['proposed_fix']}"]
    lines += ["## Aggregate",f"- By divergence: {dict(Counter(x['divergence_type'] for x in mismatches))}",f"- By candidate phase: {dict(Counter(x['failing_phase'] for x in mismatches))}","## Phase 11 decision","These phase labels are candidates from the trace, not proof of root cause. Inspect source rows behind each extra or missing resource before changing frozen modules."]
    return "\n".join(lines)+"\n"

if __name__=="__main__":
    report=triage(sys.argv[1],sys.argv[2]); path=ROOT/"code/evaluation/mismatch_triage_report.md"; path.write_text(report,encoding="utf-8"); print(path)
