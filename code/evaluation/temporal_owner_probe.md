# Temporal affiliation probe

This is a gold-free diagnostic. It reads request input times, manifest evidence, identities and activity rows; it never reads sample_output.csv or prior output.csv. A temporal match is only a candidate owner link.

Directly owned account resources discovered: 240; conflicting owners: 0. Numeric account/user suffix agreement: 1/240.

| Measure | Full 518-case input | 32-case sample input |
|---|---:|---:|
| candidate_count_1 | 10 | 0 |
| candidate_count_10 | 21 | 11 |
| candidate_count_2 | 25 | 0 |
| candidate_count_3 | 56 | 3 |
| candidate_count_4 | 66 | 4 |
| candidate_count_5 | 113 | 0 |
| candidate_count_6 | 118 | 4 |
| candidate_count_7 | 58 | 5 |
| candidate_count_8 | 39 | 2 |
| candidate_count_9 | 8 | 1 |
| nearest_known_other_owner_no_owned_action | 71 | 1 |
| nearest_owned_action | 71 | 3 |
| requests_with_any_account_action | 514 | 30 |
| requests_with_labeled_candidates | 432 | 26 |
| requests_with_owned_action | 212 | 10 |

## Known-owner counterexamples

Each row is a request with at least one directly owned account activity in its request-to-reported window, but the nearest action belongs to a different or unowned resource.
| Case | Canonical user | Window account actions | Nearest resource | Directly owned resource(s) |
|---|---|---:|---|---|
| case_44 | user_42 | 3 | account_7566 | account_2064 |
| case_51 | user_49 | 8 | account_9335 | account_3610 |
| case_65 | user_63 | 6 | account_9079 | account_5488 |
| case_66 | user_64 | 12 | account_9079 | account_1602 |
| case_68 | user_66 | 5 | account_994 | account_902 |
| case_69 | user_67 | 9 | account_994 | account_6138 |
| case_70 | user_68 | 10 | account_994 | account_6633 |
| case_71 | user_69 | 7 | account_1298 | account_1378 |
| case_72 | user_70 | 8 | account_1298 | account_7643 |
| case_77 | user_75 | 4 | account_5186 | account_9334 |
| case_80 | user_78 | 2 | account_9832 | account_4006 |
| case_82 | user_80 | 16 | account_1602 | account_4156 |
| case_83 | user_81 | 6 | account_2387 | account_2449 |
| case_85 | user_83 | 10 | account_2387 | account_4911 |
| case_86 | user_84 | 4 | account_8166 | account_8473 |
| case_88 | user_86 | 9 | account_8166 | account_868 |
| case_89 | user_87 | 6 | account_9051 | account_8764 |
| case_90 | user_88 | 9 | account_9051 | account_9673 |
| case_91 | user_89 | 10 | account_9051 | account_6075 |
| case_92 | user_90 | 3 | account_9334 | account_3609 |
| case_105 | user_103 | 5 | account_4514 | account_6345 |
| case_113 | user_111 | 6 | account_1785 | account_6697 |
| case_114 | user_112 | 6 | account_1785 | account_4833 |
| case_116 | user_114 | 5 | account_5785 | account_1823 |
| case_117 | user_115 | 5 | account_5785 | account_1220 |
| case_119 | user_117 | 3 | account_081 | account_8058 |
| case_120 | user_118 | 3 | account_081 | account_8656 |
| case_122 | user_120 | 5 | account_6750 | account_9580 |
| case_127 | user_125 | 7 | account_8819 | account_6805 |
| case_129 | user_127 | 4 | account_4833 | account_6673 |

A high hit rate here would still not turn reported_at into a direct ownership field. The requested-to-reported interval is a claim-supplied time window, and ambiguous windows must remain unresolved.
