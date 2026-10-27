import csv
from pathlib import Path
from .ir import PolicyRule
REQUIRED={"rule_id","data_category","required_action"}
def _treatment(value): return {"DELETE":"DELETE","REDACT":"REDACT","ANONYMIZE":"ANONYMIZE","RETAIN":"RETAIN"}[value.strip().upper()]
def load_rules(path: Path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f); missing=REQUIRED-set(reader.fieldnames or [])
        if missing: raise ValueError("missing required columns: "+", ".join(sorted(missing)))
        out=[]; seen=set()
        for row in reader:
            rid=row["rule_id"]
            if rid in seen: raise ValueError(f"duplicate rule_id: {rid}")
            seen.add(rid); action=_treatment(row["required_action"])
            category=row["data_category"].strip().casefold()
            aliases={"user_profile":"account","secondary_identifier":"account","search_index_entry":"search_index","cache_entry":"cache","support_message":"support_tickets","support_attachment":"support_attachment","analytics_profile":"analytics_export","product_telemetry":"product_telemetry","user_export":"user_export","marketing_profile":"marketing_profile","email_delivery_log":"logs","security_audit_log":"logs","legal_hold_record":"legal_hold","backup_archive":"backup_snapshot","account_tombstone":"account_tombstone"}
            out.append(PolicyRule(rid,aliases.get(category,category),None,action,notes=row.get("condition", "")))
    return out
