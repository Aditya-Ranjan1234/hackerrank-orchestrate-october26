from .ir import Step
from .mapper import *
from contextvars import ContextVar
from contextlib import contextmanager

_citation_context=ContextVar("citation_context",default=None)

@contextmanager
def citation_context(resolver,case_row,identity):
 token=_citation_context.set((resolver,case_row,identity))
 try: yield
 finally: _citation_context.reset(token)

def _step(phase,v,op,state,evidence):
 context=_citation_context.get()
 candidates=getattr(v,"candidate_files",[])
 if evidence and phase in {"FINDING","VERIFICATION"} and context and len(candidates)>1:
  selected=context[0].select_primary_evidence_file(candidates,context[1],context[2])
  if selected in {x["file_id"] for x in candidates}: evidence=selected
 return Step(0,phase,v.system_id,v.resource_id,op,state,evidence)
class StepBuilder:
 @staticmethod
 def build_complete(decision,verdicts):
  out=[]; seen=set()
  for v in verdicts:
   if not v.is_in_compliance or v.required_action=="NONE":continue
   op,state=verification_for_compliant_verdict(v.required_action)
   if op and (v.system_id,v.resource_id,op) not in seen:
    if not v.evidence_id: raise ValueError("COMPLETE verification requires evidence_id")
    out.append(_step("VERIFICATION",v,op,state,v.evidence_id));seen.add((v.system_id,v.resource_id,op))
  return out
 @staticmethod
 def build_incomplete(decision,verdicts):
  out=[]
  for t in decision.incomplete_triggers:
   v=next((x for x in verdicts if x.winning_rule_id==t.verdict_id and x.system_id==t.system_id and x.resource_id==t.resource_id),None) or next(x for x in verdicts if x.system_id==t.system_id and x.resource_id==t.resource_id)
   fop,fs=finding_for_trigger(t,v)
   if fop:
    if not v.evidence_id:raise ValueError("INCOMPLETE finding requires evidence_id")
    out.append(_step("FINDING",v,fop,fs,v.evidence_id))
   rop,rs=remediation_for_trigger(t,v)
   if rop:out.append(_step("REMEDIATION",v,rop,rs,""))
   vop,vs=verification_for_trigger(t,v);out.append(_step("VERIFICATION",v,vop,vs,""))
  seen={(s.system_id,s.resource_id,s.operation) for s in out if s.phase=="VERIFICATION"}
  for v in verdicts:
   if not v.is_in_compliance or v.required_action=="NONE":continue
   op,state=verification_for_compliant_verdict(v.required_action)
   if op and (v.system_id,v.resource_id,op) not in seen:
    out.append(_step("VERIFICATION",v,op,state,""))
    seen.add((v.system_id,v.resource_id,op))
  return out
 @staticmethod
 def build_not_applicable():return []
