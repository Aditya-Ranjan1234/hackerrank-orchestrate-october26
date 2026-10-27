import json
def to_steps_json(steps):
 out=json.dumps([{"step_no":s.step_no,"phase":s.phase,"system_id":s.system_id,"resource_id":s.resource_id,"operation":s.operation,"state":s.state,"evidence_id":s.evidence_id} for s in steps],separators=(",",":")); json.loads(out); return out
