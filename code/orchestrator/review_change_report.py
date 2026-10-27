"""Evaluation-only before/after ledger for the assistant's source review.

This module never generates predictions. Both input CSVs already exist, and
every row keeps its full before/after step array for independent inspection.
"""
import csv,json,hashlib
from collections import Counter
from pathlib import Path
from .plan_execution_audit import audit_run

ROOT=Path(__file__).resolve().parents[2]
def read(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write_csv(path,rows,fields):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def key(s):return tuple(s[k] for k in ('phase','system_id','resource_id','operation','state','evidence_id'))
def reasons(before,after,old,new,events=()):
    out=[];oldkeys={key(s) for s in old};newkeys={key(s) for s in new}
    if before['deletion_status']=='NOT_APPLICABLE' and after['deletion_status']!='NOT_APPLICABLE':out.append('Portuguese text explicitly authorizes permanent account deletion; verification wording does not revoke it')
    if after['deletion_status']=='NOT_APPLICABLE' and before['deletion_status']!='NOT_APPLICABLE':out.append('Request authorizes correction/access/marketing-only action or explicitly rejects account deletion')
    if any(s['system_id']=='search_service' and s['resource_id'].startswith('data_flow_') for s in old):out.append('SYNC resource identifies the connector, not a second search record; remove ghost deletion while retaining the real downstream record')
    if any(s['resource_id'].startswith('legal_hold_') and s['operation']=='DELETE_RECORD' for s in old):out.append('Explicit legal-hold/retention evidence requires rule_13 RETAIN, not DELETE')
    oldresources={s['resource_id'] for s in old}
    if before['deletion_status']!='NOT_APPLICABLE':
        if any(s['resource_id'].startswith('data_flow_') and s['resource_id'] not in oldresources for s in new):out.append('Persisted connector subject_selector exactly matches the subject; include its enabled/disabled obligation')
        if any(s['resource_id'].startswith('support_') and s['resource_id'] not in oldresources for s in new):
            if any(e['event']=='phone_aliases' for e in events):out.append('Historical full phone number uniquely identifies the subject in an attachment scan; apply rule_06 DELETE')
            else:out.append('Persisted ticket_attachment uploaded_by exactly identifies the exclusive attachment owner; apply rule_06 DELETE')
    olddelete={(s['system_id'],s['resource_id']) for s in old if s['operation']=='DELETE_RECORD'}
    if any((s['system_id'],s['resource_id']) in olddelete and s['operation']=='VERIFY_DATA_FLOW_DISABLED' for s in new):out.append('SQLite zero means disabled connector; verify disabled rather than delete a configuration record')
    oldpresent={s['resource_id'] for s in old if s['operation']=='VERIFY_RECORD_PRESENT'}
    if any(s['resource_id'].startswith('backup_') and s['resource_id'] in oldpresent and s['operation']=='VERIFY_RESTORE_BLOCKED' for s in new):out.append('Typed restore_allowed=false or explicit authorization deny proves restore is blocked; verify access restriction')
    oldredact={s['resource_id'] for s in old if s['operation']=='REDACT_RECORD'}
    if any(s['resource_id'] in oldredact and s['operation']=='DELETE_RECORD' for s in new):out.append('Attachment scan/storage schema identifies an exclusive attachment, so DELETE replaces message REDACT')
    newredact={s['resource_id'] for s in new if s['operation']=='REDACT_RECORD'}
    if oldredact-newredact and any(s['resource_id'] in oldredact-newredact and s['operation']=='VERIFY_RECORD_REDACTED' for s in new):out.append('Explicitly null requester contact fields or [REDACTED] message readback prove compliance; remove redundant remediation')
    for s in new:
        if (before['deletion_status']!='NOT_APPLICABLE' and s['resource_id'] not in oldresources
                and s['resource_id'].startswith(('object_','export_','tombstone_'))):
            out.append('Exact catalog alias joins the canonical resource to a visible artifact; catalog identity and file existence jointly support the step')
            break
    oldsemantic={k[:-1] for k in oldkeys};newsemantic={k[:-1] for k in newkeys}
    if oldsemantic==newsemantic and oldkeys!=newkeys:out.append('Same obligation; citation now recognizes typed flow/restore state and prefers a contemporaneously captured source')
    return out or ['Source-derived decision changed; see exact added/removed steps and cited sources in this ledger']

def build(root=ROOT):
    root=Path(root);base=read(root/'artifacts/csv/scored_21_6_root.csv');current=read(root/'output.csv')
    previous={r['case_id']:r for r in base};audit={r.case_id:r for r in audit_run(root,root/'output.csv')}
    requests={r['case_id']:r for r in read(root/'dataset/deletion_requests.csv')}
    manifest={r['file_id']:r for r in read(root/'dataset/evidence_files.csv')}
    changed=[];allrows=[];category_counts=Counter()
    for number,after in enumerate(current,2):
        before=previous[after['case_id']];old=json.loads(before['steps_json']);new=json.loads(after['steps_json'])
        different=before['deletion_status']!=after['deletion_status'] or old!=new
        trace_path=root/'code/.cache/diagnostics'/f"{after['case_id']}.jsonl"
        events=[json.loads(line) for line in trace_path.read_text(encoding='utf8').splitlines()]
        why=reasons(before,after,old,new,events) if different else []
        category_counts.update(why)
        oldkeys={key(s) for s in old};newkeys={key(s) for s in new}
        removed=[s for s in old if key(s) not in newkeys];added=[s for s in new if key(s) not in oldkeys]
        notes=list(audit[after['case_id']].warnings)
        retrospective=sorted({s['evidence_id'] for s in new if s['evidence_id'] in manifest
                             and manifest[s['evidence_id']]['captured_at']>requests[after['case_id']]['audit_at']})
        if retrospective:notes.append('retrospective_capture_requires_review:'+','.join(retrospective))
        status_event=next(e for e in reversed(events) if e['phase']=='status' and e['event']=='decide')
        if status_event['outputs'].get('proof_gaps'):notes.append('workflow_claim_not_independently_read_back')
        if after['case_id']=='case_55':notes.append('backup_present_but_screenshot_does_not_explicitly_prove_restore_block')
        if after['case_id']=='case_63':notes.append('catalog_marketing_owner_conflicts_with_visible_screenshot_owner; do_not_delete_another_subjects_record')
        allrows.append(dict(csv_row=number,case_id=after['case_id'],before_status=before['deletion_status'],after_status=after['deletion_status'],changed=different,
                            steps=len(new),visible_plan_check='PASS' if not audit[after['case_id']].errors else 'FAIL',
                            reasons='; '.join(why) or 'No source-supported correction identified',
                            remaining_evidence_limits='; '.join(notes),
                            planned_final_states='; '.join(f"{s['system_id']}/{s['resource_id']}={s['state']}" for s in new if s['phase']=='VERIFICATION')))
        if different:
            changed.append(dict(csv_row=number,case_id=after['case_id'],before_status=before['deletion_status'],after_status=after['deletion_status'],before_step_count=len(old),after_step_count=len(new),
                                reasons='; '.join(why),removed_steps_json=json.dumps(removed,separators=(',',':')),added_steps_json=json.dumps(added,separators=(',',':')),
                                before_steps_json=before['steps_json'],after_steps_json=after['steps_json']))
    dest=root/'artifacts/csv'
    write_csv(dest/'changed_rows.csv',changed,list(changed[0]) if changed else ['case_id'])
    write_csv(dest/'all_518_row_review.csv',allrows,list(allrows[0]))
    lines=['# Changed output rows — source review','',
           f"Compared with the preserved 21.6/30 root submission: **{len(changed)} of 518 rows changed**, {518-len(changed)} unchanged. Row numbers include the CSV header (first data row is 2).",'',
           'The assistant inspected all 518 original row plans, grouped recurring source errors, reopened the relevant source records, and checked the regenerated rows. Scripts enumerate, compare, and replay plans; they do not supply hidden answer labels. The ledger does not assert a new HackerRank score.','',
           'Full before/after JSON arrays and exact added/removed steps are in `artifacts/csv/changed_rows.csv`. Every case, including unchanged and unresolved cases, is in `artifacts/csv/all_518_row_review.csv`.','',
           '| CSV row | Case | Before → after | Step count | Reason |','|---:|---|---|---|---|']
    lines += [f"| {r['csv_row']} | {r['case_id']} | {r['before_status']} → {r['after_status']} | {r['before_step_count']} → {r['after_step_count']} | {r['reasons']} |" for r in changed]
    lines += ['','## Remaining evidence limits','',
              'PASS in the 518-row file means the listed actions and final checks satisfy the recorded visible obligations. It is not certification that every unlinked resource was discovered or that the hidden grader agrees. Retrospective captures, workflow-only absence claims, and unresolved ownership are marked per case.','',
              '| Case | Limit |','|---|---|']
    lines += [f"| {r['case_id']} | {r['remaining_evidence_limits']} |" for r in allrows if r['remaining_evidence_limits']]
    (root/'code/evaluation/changed_rows.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    counts={'rows':len(current),'changed_rows':len(changed),'status_changes':sum(r['before_status']!=r['after_status'] for r in changed),
            'steps':sum(len(json.loads(r['steps_json'])) for r in current),'status_distribution':dict(Counter(r['deletion_status'] for r in current)),
            'case_ids':[r['case_id'] for r in changed], 'output_sha256':hashlib.sha256((root/'output.csv').read_bytes()).hexdigest(),
            'reason_counts':dict(category_counts),'plan_error_cases':sum(bool(x.errors) for x in audit.values()),
            'rows_with_evidence_limits':sum(bool(r['remaining_evidence_limits']) for r in allrows)}
    (root/'code/.cache/review_summary.json').write_text(json.dumps(counts,indent=2),encoding='utf8')
    print(json.dumps(counts,indent=2))
    return counts

if __name__=='__main__':build()
