from .ir import CategoryMap
SYSTEM_TO_CATEGORY_DEFAULT={"account_service":"account","account_service_tombstone":"account_tombstone","order_service":"orders","support_service":"support_tickets","support_platform":"support_tickets","search_service":"search_index","analytics_service":"analytics_export","analytics_platform":"analytics_export","log_service":"logs","security_service":"logs","backup_service":"backup_snapshot","email_hash_index":"search_index"}
TABLE_NAME_TO_CATEGORY={"accounts":"account","account_tombstones":"account_tombstone","orders":"orders","support_tickets":"support_tickets","support_attachments":"support_attachment","search_index":"search_index","analytics_exports":"analytics_export","audit_logs":"logs","application_logs":"logs","backups":"backup_snapshot"}
FILE_ID_PREFIX_TO_CATEGORY={"evidence_account_":"account","evidence_tombstone_":"account_tombstone","evidence_order_":"orders","evidence_support_":"support_tickets","evidence_attachment_":"support_attachment","evidence_search_":"search_index","evidence_analytics_":"analytics_export","evidence_log_":"logs","evidence_backup_":"backup_snapshot"}
RECORD_TYPE_TO_CATEGORY={
    "USER_PROFILE":"account", "SECONDARY_IDENTIFIER":"account",
    "SEARCH_INDEX_ENTRY":"search_index", "CACHE_ENTRY":"cache",
    "SUPPORT_MESSAGE":"support_tickets", "SUPPORT_ATTACHMENT":"support_attachment",
    "ANALYTICS_PROFILE":"analytics_export", "PRODUCT_TELEMETRY":"product_telemetry",
    "USER_EXPORT":"user_export", "MARKETING_PROFILE":"marketing_profile",
    "EMAIL_DELIVERY_LOG":"logs", "SECURITY_AUDIT_LOG":"logs",
    "LEGAL_HOLD_RECORD":"legal_hold", "BACKUP_ARCHIVE":"backup_snapshot",
    "ACCOUNT_TOMBSTONE":"account_tombstone",
}
def category_for(system_id,resource_id, file_id=None, table_name=None):
    if system_id=="identity_service" and resource_id.startswith("tombstone_"): return "account_tombstone"
    if system_id=="legal_service" and resource_id.startswith("legal_hold_"): return "legal_hold"
    if system_id=="export_service" and resource_id.startswith("export_"): return "user_export"
    if table_name in TABLE_NAME_TO_CATEGORY:return TABLE_NAME_TO_CATEGORY[table_name]
    if file_id:
        for prefix,cat in FILE_ID_PREFIX_TO_CATEGORY.items():
            if file_id.startswith(prefix):return cat
    return SYSTEM_TO_CATEGORY_DEFAULT.get(system_id,CategoryMap.fallback_for_unknown(system_id))
