import csv
import os
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace as N
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.identity import load_default_resolver
from agent.evidence.registry import extract_file,manifest
from agent.evidence.ir import ExtractedEvidence
from agent.state.reconstructor import reconstruct
from agent.flows.detector import FlowDetector
from agent.flows.restore_risk import RestoreRiskAnalyzer
from agent.policy.rules_loader import load_rules
from agent.policy.engine import PolicyEngine
from agent.status.determinator import StatusDeterminator
from agent.steps.generator import StepGenerator
from agent.steps.serializer import to_steps_json
from agent.steps.builder import citation_context
from agent.llm.client import LLMClient
from agent.llm.semantic_resolver import SemanticResolver
from agent.evidence.handlers import json_handler
from .activity_expander import expand_activities_for_user
from .workflow_affiliation import affiliate_unique_account_delete
from .source_owner_index import known_account_owners
from .completion_proof_gate import guard_unverified_completion
from agent.status.request_classifier import is_deletion_request
from .diagnostic_logger import DiagnosticLogger
from .evidence_time import apply_manifest_capture
from .evidence_admission import exclude_stale_negative_lookups, affiliate_absent_readbacks_from_later_owner
from .audit_supervisor import supervise_evidence
from .catalog_aliases import add_catalog_artifacts
from .phone_observations import add_phone_observations

def _source_for_verdict(verdict, facts, flows, risks):
 primary={"record":facts,"flow":flows,"restore_risk":risks}.get(verdict.target_kind,[])
 for group in (primary,facts,flows,risks):
  source=next((x for x in group if x.system_id==verdict.system_id and x.resource_id==verdict.resource_id),None)
  if source is not None: return source
 return None

def _canonical_citation(evidence_id, activity_ids):
 """Derived activity rows cite their original CSV row in public steps."""
 if not evidence_id or "::derived_" not in evidence_id:
  return evidence_id or ""
 original=evidence_id.split("::derived_",1)[0]
 return original if original in activity_ids else ""

def _contemporaneous_file(candidates,audit_at):
 """Prefer a source captured by audit time when it confirms the same state."""
 cutoff=datetime.fromisoformat(str(audit_at).replace('Z','+00:00'))
 available=[]
 for source in candidates:
  captured=source.get('captured_at')
  if not captured:continue
  try: timestamp=datetime.fromisoformat(str(captured).replace('Z','+00:00'))
  except (ValueError,TypeError):continue
  if timestamp<=cutoff:available.append(source)
 if not available:return None
 return max(available,key=lambda source:(str(source.get('timestamp') or ''),source['file_id']))['file_id']

def _evidence_confirms_verdict(record,verdict):
 """A backup or connector outcome is recorded in fields, not record state."""
 if record.state_at_evidence==verdict.current_state:return True
 raw=record.raw_row or {}
 result=str(raw.get('result') or '').upper()
 if verdict.target_kind=='restore_risk' and verdict.current_state=='BLOCKED':
  return raw.get('restore_allowed') is False or result=='BLOCKED'
 if verdict.target_kind=='flow' and verdict.current_state=='INACTIVE':
  return raw.get('enabled') is False or result=='DISABLED'
 if verdict.target_kind=='flow' and verdict.current_state=='ACTIVE':
  return raw.get('enabled') is True or result=='ACTIVE'
 if verdict.target_kind=='restore_risk' and verdict.current_state=='RISKY':
  return raw.get('restore_allowed') is True or result=='ACTIVE'
 return False
@dataclass
class CaseResult:case_id:str;deletion_status:str;steps_json:str;errors:list[str]
@dataclass
class Datasets:
 root:Path;resolver:object;identities:list;audits:list;activities:list;rules:list;manifest:list
def load_datasets(root):
 ds=root/'dataset'
 def rows(p):
  with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
 return Datasets(root,load_default_resolver(root),rows(ds/'user_identities.csv'),rows(ds/'user_audit_log.csv'),rows(ds/'system_activity.csv'),load_rules(ds/'deletion_rules.csv'),manifest(root))
def run_case(case_row,datasets):
 # The workflow's report time is a bounded correlation hint for activity
 # affiliation. The status claim never enters the pipeline; neither field
 # reaches status determination or the model through the projected case row.
 reported_time_hint=getattr(case_row,'reported_at',None)
 case_row=N(case_id=case_row.case_id,email=case_row.email,
            requested_at=case_row.requested_at,audit_at=case_row.audit_at,
            request_text=case_row.request_text)
 errors=[]; identity=None; evidence=[]; facts=[]; flows=[]; risks=[]; verdicts=[]; expanded_activity_rows=datasets.activities
 if not hasattr(datasets,"_llm_client"):
  datasets._llm_client=LLMClient(datasets.root/'code/.cache/llm_cache',datasets.root/'code/.cache/llm_traces')
 llm_resolver=SemanticResolver(datasets._llm_client) if datasets._llm_client.enabled else None
 case_ref=f"dataset/deletion_requests.csv:case_id={case_row.case_id}"
 with DiagnosticLogger(case_row.case_id,datasets.root) as logger:
  logger.log('identity','start',case_ref,'resolve request identity',{'email':case_row.email,'audit_at':case_row.audit_at},{})
  try: identity=datasets.resolver.resolve(case_row.email,case_row.audit_at)
  except Exception as e:
   errors.append(f'identity_resolution_failed: {e}'); identity=N(primary_user_id=None,all_user_ids=set(),all_emails=set())
  logger.log('identity','resolve_identity',f"dataset/user_identities.csv:email={case_row.email}",f"primary_user_id={identity.primary_user_id}",{}, {'primary_user_id':identity.primary_user_id,'all_user_ids':sorted(identity.all_user_ids),'all_emails':sorted(identity.all_emails)})
  logger.log('evidence','start',f"dataset/evidence_files.csv:rows=2-{len(datasets.manifest)+1}",'extract manifest files',{'manifest_count':len(datasets.manifest)},{})
  if os.environ.get('ORCHESTRATOR_SKIP_EVIDENCE')=='1':
   errors.append('evidence_skipped_diagnostic_mode')
  else:
   for source in datasets.manifest:
    try:
     item=extract_file(datasets.root,source['file_id'],source['file_path'],identity,
                       case_row.audit_at,llm_client=datasets._llm_client,case_id=case_row.case_id)
     if any(note in {"missing_file","unsupported_extension"} for note in item.notes):
      errors.append(f"evidence_unavailable:{source['file_id']}:{','.join(item.notes)}")
     if Path(item.file_path).suffix.lower()=='.json' and llm_resolver is not None:
      for record in item.records:
       try: json_handler.resolve_record_system(record,llm_resolver,item.file_id,item.file_path,case_row.case_id)
       except Exception as exc: errors.append(f"system_resolution_failed:{item.file_id}:{type(exc).__name__}")
     apply_manifest_capture(item,source,case_row.audit_at)
    except Exception as exc:
     errors.append(f"evidence_extraction_failed:{source['file_id']}:{type(exc).__name__}")
     item=ExtractedEvidence(source['file_id'],source['file_path'],'',[],'error',
                            datetime.now(timezone.utc),notes=[f"extraction_error:{type(exc).__name__}"])
    evidence.append(item)
  try:
   catalog_links=add_catalog_artifacts(datasets.root,evidence,datasets.manifest,datasets.activities,identity,case_row.audit_at)
   phone_links=add_phone_observations(datasets.root,evidence,datasets.manifest,datasets.identities,datasets.audits,identity,case_row.audit_at)
  except Exception as exc:
   errors.append(f'catalog_alias_failed:{type(exc).__name__}');catalog_links=[];phone_links=[]
  if catalog_links:
   logger.log('evidence','catalog_aliases','dataset/system_activity.csv','exact visible artifact aliases',{}, {'links':catalog_links})
  if phone_links:
   logger.log('evidence','phone_aliases','dataset/user_audit_log.csv','exact typed phone aliases',{}, {'links':phone_links})
  stale_lookups=exclude_stale_negative_lookups(evidence,case_row.requested_at)
  post_audit_owner_joins=affiliate_absent_readbacks_from_later_owner(evidence,identity,case_row.audit_at)
  if not datasets._llm_client.enabled: llm_resolver=None
  logger.log('evidence','extract_evidence',f"dataset/evidence_files.csv:rows=2-{len(datasets.manifest)+1}",f"{sum(len(e.records) for e in evidence)} records",{}, {'files':[{'file_id':e.file_id,'path':e.file_path,'record_count':len(e.records),'records':[{'system_id':r.system_id,'resource_id':r.resource_id,'user_ref':r.user_ref,'state':r.state_at_evidence} for r in e.records]} for e in evidence if e.records], 'vlm_call_count':sum(e.llm_call_count for e in evidence), 'stale_negative_lookups_excluded':stale_lookups, 'post_audit_exact_owner_joins':post_audit_owner_joins, 'errors':list(errors)})
  try:
   review=supervise_evidence(case_row.case_id,evidence,datasets.manifest,identity,datasets.root,datasets._llm_client)
   if review:
    logger.log('evidence_review','tool_loop',f"dataset/evidence_files.csv:rows=2-{len(datasets.manifest)+1}",
               f"read_only_inspections={len(review)}",{}, {'tool_results':review})
  except Exception as e:
   errors.append(f'evidence_review_failed: {type(e).__name__}')
  logger.log('expander','start',f"dataset/system_activity.csv:rows=2-{len(datasets.activities)+1}",'infer activity affiliation',{'activity_count':len(datasets.activities)},{})
  workflow_trace=[]
  try:
   expanded_activity_rows=expand_activities_for_user(datasets.activities,evidence,identity,case_row.audit_at)
   account_owners=known_account_owners(str(datasets.root))
   eligible_count=None
   active_cases=getattr(datasets,'active_case_rows',None)
   if active_cases is not None:
    if not hasattr(datasets,'_eligible_report_users'):
     eligible={}
     directly_owned_users=set(account_owners.values())
     for candidate in active_cases:
      get=lambda key: candidate.get(key) if isinstance(candidate,dict) else getattr(candidate,key,None)
      if not is_deletion_request(get('request_text')):continue
      candidate_identity=datasets.resolver.resolve(get('email'),get('audit_at'))
      if not candidate_identity.primary_user_id or set(candidate_identity.all_user_ids)&directly_owned_users:continue
      eligible.setdefault(get('reported_at'),set()).add(candidate_identity.primary_user_id)
     datasets._eligible_report_users=eligible
    eligible_count=len(datasets._eligible_report_users.get(reported_time_hint,set()))
   expanded_activity_rows=affiliate_unique_account_delete(
    expanded_activity_rows,identity,reported_time_hint,case_row.requested_at,case_row.audit_at,
    evidence,account_owners,eligible_count,workflow_trace)
  except Exception as e: errors.append(f'activity_expansion_failed: {e}')
  derived=[a for a in expanded_activity_rows if a.get('derived')]
  logger.log('expander','expand_activities',f"dataset/system_activity.csv:rows=2-{len(datasets.activities)+1}",f"derived={len(derived)}",{}, {'derived_count':len(derived),'derived':[{'activity_id':a.get('activity_id'),'original_activity_id':a.get('original_activity_id'),'method':a.get('inference_method'),'resource_id':a.get('resource_id')} for a in derived], 'workflow_affiliation':workflow_trace, 'errors':list(errors)})
  activity_ref=f"dataset/system_activity.csv:rows=2-{len(datasets.activities)+1}"
  logger.log('state','start',activity_ref,'reconstruct audit time states',{'activity_count':len(expanded_activity_rows)},{})
  try: facts=reconstruct(identity,evidence,expanded_activity_rows,case_row.audit_at,llm_resolver=llm_resolver,case_id=case_row.case_id)
  except Exception as e: errors.append(f'state_reconstruction_failed: {e}')
  logger.log('state','reconstruct',activity_ref,f"facts={len(facts)}",{}, {'facts':[{'system_id':f.system_id,'resource_id':f.resource_id,'state':f.state_at_audit,'evidence_id':f.evidence_id,'notes':f.notes} for f in facts], 'errors':list(errors)})
  logger.log('flows','start',activity_ref,'detect active flows',{}, {})
  try: flows=FlowDetector.build_flows(identity,evidence,facts,expanded_activity_rows,case_row.audit_at)
  except Exception as e: errors.append(f'flow_detection_failed: {e}')
  logger.log('flows','detect',activity_ref,f"flows={len(flows)}",{}, {'flows':[str(x) for x in flows], 'errors':list(errors)})
  logger.log('flows','restore_start',activity_ref,'detect restore risks',{}, {})
  try: risks=RestoreRiskAnalyzer.build_risks(identity,evidence,facts,expanded_activity_rows,case_row.audit_at)
  except Exception as e: errors.append(f'restore_risk_failed: {e}')
  logger.log('flows','restore_risks',activity_ref,f"risks={len(risks)}",{}, {'risks':[str(x) for x in risks], 'errors':list(errors)})
  logger.log('policy','start',f"dataset/deletion_rules.csv:rows=2-{len(datasets.rules)+1}",'apply rules',{'facts':len(facts),'flows':len(flows),'risks':len(risks)},{})
  try:
   verdicts=PolicyEngine(datasets.rules,llm_resolver,case_row.case_id).apply(facts,flows,risks,case_row.requested_at,case_row.audit_at)
   activity_ids={row.get('activity_id') for row in datasets.activities}
   manifest_by_id={row['file_id']:row for row in datasets.manifest}
   for v in verdicts:
    source=_source_for_verdict(v,facts,flows,risks)
    raw_citation=getattr(source,'evidence_id','') if source else ''
    v.evidence_id=_canonical_citation(raw_citation,activity_ids)
    if raw_citation and not v.evidence_id:
     errors.append(f'unresolved_derived_activity_citation:{raw_citation}')
    if v.evidence_id:
     candidates={}
     for ev in evidence:
      for rec in ev.records:
       if (rec.system_id,rec.resource_id)!=(v.system_id,v.resource_id):continue
       if rec.user_ref not in identity.all_user_ids and rec.user_ref not in identity.all_emails:continue
       if not _evidence_confirms_verdict(rec,v):continue
       candidates[ev.file_id]={'file_id':ev.file_id,'timestamp':rec.evidence_timestamp.isoformat() if rec.evidence_timestamp else None,'captured_at':manifest_by_id.get(ev.file_id,{}).get('captured_at'),'state':rec.state_at_evidence,'resource_id':rec.resource_id}
     v.candidate_files=sorted(candidates.values(),key=lambda x:x['file_id'])
     preferred=_contemporaneous_file(v.candidate_files,case_row.audit_at)
     if preferred:v.evidence_id=preferred
  except Exception as e: errors.append(f'policy_engine_failed: {e}'); verdicts=[]
  logger.log('policy','apply',f"dataset/deletion_rules.csv:rows=2-{len(datasets.rules)+1}",f"verdicts={len(verdicts)}",{}, {'verdicts':[{'system_id':v.system_id,'resource_id':v.resource_id,'value':str(v),'evidence_id':getattr(v,'evidence_id','')} for v in verdicts], 'errors':list(errors)})
  logger.log('status','start',case_ref,'determine status',{}, {})
  proof_gaps=[]
  try:
   decision=StatusDeterminator().decide(case_row,identity,verdicts)
   decision,proof_gaps=guard_unverified_completion(decision,facts,verdicts,expanded_activity_rows)
  except Exception as e: errors.append(f'status_determination_failed: {e}'); decision=N(case_id=case_row.case_id,deletion_status='INCOMPLETE',incomplete_triggers=[])
  logger.log('status','decide',case_ref,decision.deletion_status,{}, {'status':decision.deletion_status,'triggers':[str(x) for x in decision.incomplete_triggers], 'proof_gaps':proof_gaps, 'errors':list(errors)})
  logger.log('steps','start',case_ref,'build steps',{}, {})
  try:
   if llm_resolver is not None:
    with citation_context(llm_resolver,case_row,identity): steps=StepGenerator.generate(case_row,decision,verdicts)
   else: steps=StepGenerator.generate(case_row,decision,verdicts)
   steps_json=to_steps_json(steps)
  except Exception as e: errors.append(f'step_generation_failed: {e}'); steps_json='[]'
  logger.log('steps','generate',case_ref,f"steps={len(__import__('json').loads(steps_json))}",{}, {'steps_json':steps_json,'errors':list(errors)})
  return CaseResult(case_row.case_id,decision.deletion_status,steps_json,errors)
