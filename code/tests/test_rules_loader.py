from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.policy.rules_loader import load_rules
def test_valid_loader(tmp_path):
 p=tmp_path/'r.csv'; p.write_text('rule_id,data_category,condition,required_action\nr1,USER_PROFILE,Always,DELETE\n'); assert load_rules(p)[0].required_treatment=='DELETE'
def test_malformed_loader(tmp_path):
 p=tmp_path/'r.csv'; p.write_text('rule_id,data_category\nr1,x\n')
 try: load_rules(p); assert False
 except ValueError as e: assert 'required_action' in str(e)
def test_zero_optional_defaults(tmp_path):
 p=tmp_path/'r.csv'; p.write_text('rule_id,data_category,condition,required_action\nr1,x,,RETAIN\n'); assert load_rules(p)[0].retention_period_days is None
