# Production answer-leak audit

The audit follows local Python imports from `orchestrator.run`, then checks each reachable module for sample-answer paths and case-specific string literals.
Reachable modules: 70. Findings: 0.

## Reachable production modules

- `agent`
- `agent.evidence`
- `agent.evidence.cache`
- `agent.evidence.handlers`
- `agent.evidence.handlers.common`
- `agent.evidence.handlers.image_handler`
- `agent.evidence.handlers.json_handler`
- `agent.evidence.handlers.log_handler`
- `agent.evidence.handlers.pdf_handler`
- `agent.evidence.handlers.sql_handler`
- `agent.evidence.ir`
- `agent.evidence.registry`
- `agent.flows`
- `agent.flows.detector`
- `agent.flows.ir`
- `agent.flows.restore_risk`
- `agent.flows.retention`
- `agent.identity`
- `agent.llm`
- `agent.llm.cache`
- `agent.llm.client`
- `agent.llm.prompts`
- `agent.llm.prompts.affiliation`
- `agent.llm.prompts.flow_class`
- `agent.llm.prompts.primary_file`
- `agent.llm.prompts.system_id`
- `agent.llm.semantic_resolver`
- `agent.llm.tracer`
- `agent.llm.usage_tracker`
- `agent.policy`
- `agent.policy.category_map`
- `agent.policy.conflict_resolver`
- `agent.policy.engine`
- `agent.policy.ir`
- `agent.policy.retention_evaluator`
- `agent.policy.rules_loader`
- `agent.state`
- `agent.state.reconstructor`
- `agent.status`
- `agent.status.determinator`
- `agent.status.gates`
- `agent.status.ir`
- `agent.status.request_classifier`
- `agent.steps`
- `agent.steps.builder`
- `agent.steps.generator`
- `agent.steps.ir`
- `agent.steps.mapper`
- `agent.steps.ordering`
- `agent.steps.serializer`
- `orchestrator`
- `orchestrator.activity_expander`
- `orchestrator.audit_supervisor`
- `orchestrator.catalog_aliases`
- `orchestrator.completion_proof_gate`
- `orchestrator.csv_writer`
- `orchestrator.database_inspector`
- `orchestrator.diagnostic_logger`
- `orchestrator.evidence_admission`
- `orchestrator.evidence_time`
- `orchestrator.image_inspector`
- `orchestrator.image_transcriber`
- `orchestrator.log_inspector`
- `orchestrator.pdf_inspector`
- `orchestrator.phone_observations`
- `orchestrator.pipeline`
- `orchestrator.run`
- `orchestrator.source_owner_index`
- `orchestrator.validator`
- `orchestrator.workflow_affiliation`

## Static findings

None.

## Evaluation boundary

`sample_output.csv` is read by separate comparison and diagnostic commands. The production import graph must not reach those commands, and `orchestrator.run` only writes `output.csv`. Runtime read guards are covered in `test_no_gold_leak.py`.

The 32 supplied sample cases have been inspected repeatedly during development. Their accuracy is a development-set fit measure, not an unbiased estimate of hidden-case accuracy. The 486 other requests have no supplied answer labels; their structural and source-grounding checks cannot establish correctness against a hidden gold output.
