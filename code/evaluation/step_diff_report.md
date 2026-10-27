# Step-level gold diff

Source: `artifacts\csv\review_sample.csv` vs `D:\Hackerrank Orchestrate\hackerrank-orchestrate-october26\dataset\sample_output.csv`. Cases: 32. Exact step arrays: 12/32.

## 1. Aggregate mismatch counts
| mismatch_type | count | % of all mismatches |
|---|---:|---:|
| COUNT_MISMATCH | 27 | 16.88% |
| PHASE_ORDER_MISMATCH | 3 | 1.88% |
| OPERATION_MISMATCH | 29 | 18.12% |
| STATE_MISMATCH | 27 | 16.88% |
| SYSTEM_ID_MISMATCH | 36 | 22.50% |
| RESOURCE_ID_MISMATCH | 36 | 22.50% |
| EVIDENCE_ID_MISMATCH_SHOULD_CITE | 0 | 0.00% |
| EVIDENCE_ID_MISMATCH_SHOULD_BE_EMPTY | 1 | 0.62% |
| EVIDENCE_ID_MISMATCH_WRONG_CITATION | 1 | 0.62% |
| STEP_NO_MISMATCH | 0 | 0.00% |

### Position-independent diagnosis
| semantic difference | count |
|---|---:|
| MISSING_SEMANTIC_STEP | 25 |
| EXTRA_SEMANTIC_STEP | 4 |
| EVIDENCE_CITATION_DIFFERENCE | 0 |

### Every sample case
| case | status match | exact array | missing resource/operation steps | extra steps | citation differences |
|---|---|---|---:|---:|---:|
| case_01 | yes | no | 1 | 0 | 0 |
| case_02 | yes | no | 1 | 0 | 0 |
| case_03 | yes | no | 1 | 0 | 0 |
| case_04 | yes | no | 2 | 0 | 0 |
| case_05 | yes | yes | 0 | 0 | 0 |
| case_06 | yes | yes | 0 | 0 | 0 |
| case_07 | yes | no | 1 | 3 | 0 |
| case_08 | yes | no | 1 | 0 | 0 |
| case_09 | yes | yes | 0 | 0 | 0 |
| case_10 | yes | no | 1 | 0 | 0 |
| case_11 | yes | yes | 0 | 0 | 0 |
| case_12 | yes | yes | 0 | 0 | 0 |
| case_13 | yes | yes | 0 | 0 | 0 |
| case_14 | yes | yes | 0 | 0 | 0 |
| case_15 | yes | yes | 0 | 0 | 0 |
| case_16 | yes | yes | 0 | 0 | 0 |
| case_17 | yes | no | 0 | 1 | 0 |
| case_18 | yes | no | 2 | 0 | 0 |
| case_19 | yes | yes | 0 | 0 | 0 |
| case_20 | yes | no | 2 | 0 | 0 |
| case_21 | yes | no | 2 | 0 | 0 |
| case_22 | yes | no | 1 | 0 | 0 |
| case_23 | yes | no | 1 | 0 | 0 |
| case_24 | yes | yes | 0 | 0 | 0 |
| case_25 | yes | no | 2 | 0 | 0 |
| case_26 | yes | no | 1 | 0 | 0 |
| case_27 | yes | no | 1 | 0 | 0 |
| case_28 | yes | no | 2 | 0 | 0 |
| case_29 | yes | no | 1 | 0 | 0 |
| case_30 | yes | yes | 0 | 0 | 0 |
| case_31 | yes | no | 1 | 0 | 0 |
| case_32 | yes | no | 1 | 0 | 0 |

## 2. Dominant mismatch type
SYSTEM_ID_MISMATCH: 36/160 (22.50%).

## 3. Five largest per-case diffs

### case_29: ours INCOMPLETE (13), gold INCOMPLETE (14)
Our steps:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 4,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_3954",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 12,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 13,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```
Gold steps:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 4,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_7012",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_3954",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 12,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 13,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 14,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```
Differences:
```json
[
  {
    "step_index": 8,
    "field": "system_id",
    "our_value": "search_service",
    "gold_value": "account_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 8,
    "field": "resource_id",
    "our_value": "search_1993",
    "gold_value": "account_7012",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 9,
    "field": "system_id",
    "our_value": "security_service",
    "gold_value": "search_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 9,
    "field": "resource_id",
    "our_value": "audit_record_3954",
    "gold_value": "search_1993",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 9,
    "field": "operation",
    "our_value": "VERIFY_RECORD_PRESENT",
    "gold_value": "VERIFY_RECORD_ABSENT",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 9,
    "field": "state",
    "our_value": "PRESENT",
    "gold_value": "ABSENT",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 10,
    "field": "system_id",
    "our_value": "support_platform",
    "gold_value": "security_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 10,
    "field": "resource_id",
    "our_value": "support_5281",
    "gold_value": "audit_record_3954",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 10,
    "field": "operation",
    "our_value": "VERIFY_RECORD_REDACTED",
    "gold_value": "VERIFY_RECORD_PRESENT",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 10,
    "field": "state",
    "our_value": "REDACTED",
    "gold_value": "PRESENT",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 11,
    "field": "system_id",
    "our_value": "analytics_platform",
    "gold_value": "support_platform",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 11,
    "field": "resource_id",
    "our_value": "analytics_5208",
    "gold_value": "support_5281",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 11,
    "field": "operation",
    "our_value": "VERIFY_RECORD_ANONYMIZED",
    "gold_value": "VERIFY_RECORD_REDACTED",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 11,
    "field": "state",
    "our_value": "ANONYMIZED",
    "gold_value": "REDACTED",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 12,
    "field": "system_id",
    "our_value": "integration_service",
    "gold_value": "analytics_platform",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 12,
    "field": "resource_id",
    "our_value": "data_flow_3827",
    "gold_value": "analytics_5208",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 12,
    "field": "operation",
    "our_value": "VERIFY_DATA_FLOW_DISABLED",
    "gold_value": "VERIFY_RECORD_ANONYMIZED",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 12,
    "field": "state",
    "our_value": "DISABLED",
    "gold_value": "ANONYMIZED",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 13,
    "field": "step",
    "our_value": null,
    "gold_value": {
      "step_no": 14,
      "phase": "VERIFICATION",
      "system_id": "integration_service",
      "resource_id": "data_flow_3827",
      "operation": "VERIFY_DATA_FLOW_DISABLED",
      "state": "DISABLED",
      "evidence_id": ""
    },
    "mismatch_type": "COUNT_MISMATCH"
  }
]
```

### case_28: ours COMPLETE (4), gold COMPLETE (6)
Our steps:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_9265",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_2351",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_2337",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_838",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": "evidence_92"
  }
]
```
Gold steps:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_5482",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_9265",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_2351",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_6077",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_2337",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_838",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": "evidence_92"
  }
]
```
Differences:
```json
[
  {
    "step_index": 0,
    "field": "system_id",
    "our_value": "security_service",
    "gold_value": "account_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 0,
    "field": "resource_id",
    "our_value": "audit_record_9265",
    "gold_value": "account_5482",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 0,
    "field": "operation",
    "our_value": "VERIFY_RECORD_PRESENT",
    "gold_value": "VERIFY_RECORD_ABSENT",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 0,
    "field": "state",
    "our_value": "PRESENT",
    "gold_value": "ABSENT",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 1,
    "field": "system_id",
    "our_value": "support_platform",
    "gold_value": "security_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 1,
    "field": "resource_id",
    "our_value": "support_2351",
    "gold_value": "audit_record_9265",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 1,
    "field": "operation",
    "our_value": "VERIFY_RECORD_REDACTED",
    "gold_value": "VERIFY_RECORD_PRESENT",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 1,
    "field": "state",
    "our_value": "REDACTED",
    "gold_value": "PRESENT",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 2,
    "field": "system_id",
    "our_value": "integration_service",
    "gold_value": "support_platform",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 2,
    "field": "resource_id",
    "our_value": "data_flow_2337",
    "gold_value": "support_2351",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 2,
    "field": "operation",
    "our_value": "VERIFY_DATA_FLOW_DISABLED",
    "gold_value": "VERIFY_RECORD_REDACTED",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 2,
    "field": "state",
    "our_value": "DISABLED",
    "gold_value": "REDACTED",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 3,
    "field": "system_id",
    "our_value": "backup_service",
    "gold_value": "analytics_platform",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 3,
    "field": "resource_id",
    "our_value": "backup_838",
    "gold_value": "analytics_6077",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 3,
    "field": "operation",
    "our_value": "VERIFY_RESTORE_BLOCKED",
    "gold_value": "VERIFY_RECORD_ANONYMIZED",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 3,
    "field": "state",
    "our_value": "BLOCKED",
    "gold_value": "ANONYMIZED",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 4,
    "field": "step",
    "our_value": null,
    "gold_value": {
      "step_no": 5,
      "phase": "VERIFICATION",
      "system_id": "integration_service",
      "resource_id": "data_flow_2337",
      "operation": "VERIFY_DATA_FLOW_DISABLED",
      "state": "DISABLED",
      "evidence_id": "evidence_92"
    },
    "mismatch_type": "COUNT_MISMATCH"
  },
  {
    "step_index": 5,
    "field": "step",
    "our_value": null,
    "gold_value": {
      "step_no": 6,
      "phase": "VERIFICATION",
      "system_id": "backup_service",
      "resource_id": "backup_838",
      "operation": "VERIFY_RESTORE_BLOCKED",
      "state": "BLOCKED",
      "evidence_id": "evidence_92"
    },
    "mismatch_type": "COUNT_MISMATCH"
  }
]
```

### case_18: ours INCOMPLETE (12), gold INCOMPLETE (14)
Our steps:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 4,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 12,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```
Gold steps:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 4,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_5521",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_6645",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 12,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 13,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 14,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```
Differences:
```json
[
  {
    "step_index": 8,
    "field": "system_id",
    "our_value": "search_service",
    "gold_value": "account_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 8,
    "field": "resource_id",
    "our_value": "search_4013",
    "gold_value": "account_5521",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 9,
    "field": "system_id",
    "our_value": "support_platform",
    "gold_value": "search_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 9,
    "field": "resource_id",
    "our_value": "support_5569",
    "gold_value": "search_4013",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 9,
    "field": "operation",
    "our_value": "VERIFY_RECORD_REDACTED",
    "gold_value": "VERIFY_RECORD_ABSENT",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 9,
    "field": "state",
    "our_value": "REDACTED",
    "gold_value": "ABSENT",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 10,
    "field": "system_id",
    "our_value": "analytics_platform",
    "gold_value": "security_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 10,
    "field": "resource_id",
    "our_value": "analytics_037",
    "gold_value": "audit_record_6645",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 10,
    "field": "operation",
    "our_value": "VERIFY_RECORD_ANONYMIZED",
    "gold_value": "VERIFY_RECORD_PRESENT",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 10,
    "field": "state",
    "our_value": "ANONYMIZED",
    "gold_value": "PRESENT",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 11,
    "field": "system_id",
    "our_value": "integration_service",
    "gold_value": "support_platform",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 11,
    "field": "resource_id",
    "our_value": "data_flow_4890",
    "gold_value": "support_5569",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 11,
    "field": "operation",
    "our_value": "VERIFY_DATA_FLOW_DISABLED",
    "gold_value": "VERIFY_RECORD_REDACTED",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 11,
    "field": "state",
    "our_value": "DISABLED",
    "gold_value": "REDACTED",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 12,
    "field": "step",
    "our_value": null,
    "gold_value": {
      "step_no": 13,
      "phase": "VERIFICATION",
      "system_id": "analytics_platform",
      "resource_id": "analytics_037",
      "operation": "VERIFY_RECORD_ANONYMIZED",
      "state": "ANONYMIZED",
      "evidence_id": ""
    },
    "mismatch_type": "COUNT_MISMATCH"
  },
  {
    "step_index": 13,
    "field": "step",
    "our_value": null,
    "gold_value": {
      "step_no": 14,
      "phase": "VERIFICATION",
      "system_id": "integration_service",
      "resource_id": "data_flow_4890",
      "operation": "VERIFY_DATA_FLOW_DISABLED",
      "state": "DISABLED",
      "evidence_id": ""
    },
    "mismatch_type": "COUNT_MISMATCH"
  }
]
```

### case_07: ours INCOMPLETE (6), gold INCOMPLETE (4)
Our steps:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "object_storage",
    "resource_id": "object_19",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_46"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_001",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_58"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "object_storage",
    "resource_id": "object_19",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_001",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "object_storage",
    "resource_id": "object_19",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_001",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  }
]
```
Gold steps:
```json
[
  {
    "evidence_id": "evidence_58",
    "operation": "REPORT_REMAINING_RECORD",
    "phase": "FINDING",
    "resource_id": "support_001",
    "state": "PRESENT",
    "step_no": 1,
    "system_id": "support_platform"
  },
  {
    "evidence_id": "",
    "operation": "DELETE_RECORD",
    "phase": "REMEDIATION",
    "resource_id": "support_001",
    "state": "ABSENT",
    "step_no": 2,
    "system_id": "support_platform"
  },
  {
    "evidence_id": "",
    "operation": "VERIFY_RECORD_ABSENT",
    "phase": "VERIFICATION",
    "resource_id": "account_007",
    "state": "ABSENT",
    "step_no": 3,
    "system_id": "account_service"
  },
  {
    "evidence_id": "",
    "operation": "VERIFY_RECORD_ABSENT",
    "phase": "VERIFICATION",
    "resource_id": "support_001",
    "state": "ABSENT",
    "step_no": 4,
    "system_id": "support_platform"
  }
]
```
Differences:
```json
[
  {
    "step_index": 0,
    "field": "system_id",
    "our_value": "object_storage",
    "gold_value": "support_platform",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 0,
    "field": "resource_id",
    "our_value": "object_19",
    "gold_value": "support_001",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 0,
    "field": "evidence_id",
    "our_value": "evidence_46",
    "gold_value": "evidence_58",
    "mismatch_type": "EVIDENCE_ID_MISMATCH_WRONG_CITATION"
  },
  {
    "step_index": 1,
    "field": "phase",
    "our_value": "FINDING",
    "gold_value": "REMEDIATION",
    "mismatch_type": "PHASE_ORDER_MISMATCH"
  },
  {
    "step_index": 1,
    "field": "operation",
    "our_value": "REPORT_REMAINING_RECORD",
    "gold_value": "DELETE_RECORD",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 1,
    "field": "state",
    "our_value": "PRESENT",
    "gold_value": "ABSENT",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 1,
    "field": "evidence_id",
    "our_value": "evidence_58",
    "gold_value": "",
    "mismatch_type": "EVIDENCE_ID_MISMATCH_SHOULD_BE_EMPTY"
  },
  {
    "step_index": 2,
    "field": "phase",
    "our_value": "REMEDIATION",
    "gold_value": "VERIFICATION",
    "mismatch_type": "PHASE_ORDER_MISMATCH"
  },
  {
    "step_index": 2,
    "field": "system_id",
    "our_value": "object_storage",
    "gold_value": "account_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 2,
    "field": "resource_id",
    "our_value": "object_19",
    "gold_value": "account_007",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 2,
    "field": "operation",
    "our_value": "DELETE_RECORD",
    "gold_value": "VERIFY_RECORD_ABSENT",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 3,
    "field": "phase",
    "our_value": "REMEDIATION",
    "gold_value": "VERIFICATION",
    "mismatch_type": "PHASE_ORDER_MISMATCH"
  },
  {
    "step_index": 3,
    "field": "operation",
    "our_value": "DELETE_RECORD",
    "gold_value": "VERIFY_RECORD_ABSENT",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 4,
    "field": "step",
    "our_value": {
      "step_no": 5,
      "phase": "VERIFICATION",
      "system_id": "object_storage",
      "resource_id": "object_19",
      "operation": "VERIFY_RECORD_ABSENT",
      "state": "ABSENT",
      "evidence_id": ""
    },
    "gold_value": null,
    "mismatch_type": "COUNT_MISMATCH"
  },
  {
    "step_index": 5,
    "field": "step",
    "our_value": {
      "step_no": 6,
      "phase": "VERIFICATION",
      "system_id": "support_platform",
      "resource_id": "support_001",
      "operation": "VERIFY_RECORD_ABSENT",
      "state": "ABSENT",
      "evidence_id": ""
    },
    "gold_value": null,
    "mismatch_type": "COUNT_MISMATCH"
  }
]
```

### case_22: ours INCOMPLETE (7), gold INCOMPLETE (8)
Our steps:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_05"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_05"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_3482",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  }
]
```
Gold steps:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_05"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_05"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_4990",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_3482",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  }
]
```
Differences:
```json
[
  {
    "step_index": 4,
    "field": "system_id",
    "our_value": "search_service",
    "gold_value": "account_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 4,
    "field": "resource_id",
    "our_value": "search_8911",
    "gold_value": "account_4990",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 5,
    "field": "system_id",
    "our_value": "security_service",
    "gold_value": "search_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 5,
    "field": "resource_id",
    "our_value": "audit_record_3482",
    "gold_value": "search_8911",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 5,
    "field": "operation",
    "our_value": "VERIFY_RECORD_PRESENT",
    "gold_value": "VERIFY_RECORD_ABSENT",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 5,
    "field": "state",
    "our_value": "PRESENT",
    "gold_value": "ABSENT",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 6,
    "field": "system_id",
    "our_value": "analytics_platform",
    "gold_value": "security_service",
    "mismatch_type": "SYSTEM_ID_MISMATCH"
  },
  {
    "step_index": 6,
    "field": "resource_id",
    "our_value": "analytics_4440",
    "gold_value": "audit_record_3482",
    "mismatch_type": "RESOURCE_ID_MISMATCH"
  },
  {
    "step_index": 6,
    "field": "operation",
    "our_value": "VERIFY_RECORD_ANONYMIZED",
    "gold_value": "VERIFY_RECORD_PRESENT",
    "mismatch_type": "OPERATION_MISMATCH"
  },
  {
    "step_index": 6,
    "field": "state",
    "our_value": "ANONYMIZED",
    "gold_value": "PRESENT",
    "mismatch_type": "STATE_MISMATCH"
  },
  {
    "step_index": 7,
    "field": "step",
    "our_value": null,
    "gold_value": {
      "step_no": 8,
      "phase": "VERIFICATION",
      "system_id": "analytics_platform",
      "resource_id": "analytics_4440",
      "operation": "VERIFY_RECORD_ANONYMIZED",
      "state": "ANONYMIZED",
      "evidence_id": ""
    },
    "mismatch_type": "COUNT_MISMATCH"
  }
]
```

## 4. Hypothesis
Likely upstream system attribution, not Phase 6.
Position-independent exact step identities shared: 168; ours: 172; gold: 193. This excludes `step_no` and does not treat shifted positions as mapping errors.

## 5. Recommendation
Compare step identities independent of index, then trace the first incorrect verdict. A positional mismatch can be caused by upstream extra/missing resources; do not assume Phase 6 is defective from 0 exact arrays alone.
