from datetime import timedelta
def has_retention_expired(rule,requested_at,audit_at):
    if rule.retention_period_days is None:return False
    return audit_at >= requested_at + timedelta(days=rule.retention_period_days)
