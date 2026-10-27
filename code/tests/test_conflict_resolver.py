import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.policy.ir import PolicyRule
from agent.policy.conflict_resolver import resolve
def r(i,cat='x',act='RETAIN',sysid=None,p=0,days=None): return PolicyRule(i,cat,sysid,act,retention_period_days=days,priority=p)
def test_tombstone_specific(): assert resolve([r('a','account'),r('t','account_tombstone')],'account_tombstone')[0].rule_id=='t'
def test_system_specific(): assert resolve([r('g','x'),r('s','x',sysid='account_service')],'x')[0].rule_id=='s'
def test_strictest(): assert resolve([r('r','x','RETAIN'),r('d','x','DELETE')],'x')[0].rule_id=='d'
def test_priority(): assert resolve([r('a','x','REDACT',p=1),r('b','x','REDACT',p=2)],'x')[0].rule_id=='b'
def test_shorter_retain(): assert resolve([r('a','x','RETAIN',days=30),r('b','x','RETAIN',days=90)],'x')[0].rule_id=='a'
