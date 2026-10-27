# Full-run workflow derivation audit

This source-only audit reads `output.csv` and the same run's diagnostic traces; it does not read `sample_output.csv`. A workflow result is a claim, so COMPLETE verifications that cite only an activity require scrutiny.

| Measure | Count |
|---|---:|
| decision_already_has_directly_owned_account | 34 |
| decision_ambiguous_requesters_at_report_time | 419 |
| decision_competing_account_actions | 7 |
| decision_derived_unique_calibrated_report_window | 23 |
| decision_no_eligible_account_action | 4 |
| decision_unique_action_not_successful | 31 |
| derived_account_actions | 23 |
| derived_actions_with_steps | 23 |
| derived_case_status_INCOMPLETE | 23 |

## Derived account actions

| Case | Account | Original activity | Status | Step operations | Citations |
|---|---|---|---|---|---|
| case_62 | account_7119 | activity_3795 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_78 | account_8754 | activity_3302 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_102 | account_2056 | activity_3411 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_103 | account_4070 | activity_3322 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_152 | account_8854 | activity_2872 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_194 | account_660 | activity_2474 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_212 | account_418 | activity_2425 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_234 | account_2614 | activity_2184 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_242 | account_3905 | activity_2348 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_274 | account_6575 | activity_1904 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_282 | account_9763 | activity_2065 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_284 | account_8322 | activity_1957 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_325 | account_2595 | activity_1640 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_334 | account_2255 | activity_1444 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_343 | account_1949 | activity_1532 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_373 | account_8684 | activity_1156 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_402 | account_3370 | activity_1159 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_403 | account_1246 | activity_1093 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_428 | account_2157 | activity_849 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_454 | account_3024 | activity_566 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_492 | account_3589 | activity_368 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_500 | account_5738 | activity_173 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
| case_512 | account_445 | activity_225 | INCOMPLETE | VERIFY_RECORD_ABSENT |  |
