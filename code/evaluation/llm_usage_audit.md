# LLM usage audit
## Static scan
- code/agent/evidence/handlers/image_handler.py:93: VLM\( — INJECTED_CALLBACK_ONLY
- code/agent/llm/client.py:33: import openai — REAL_CALL_PATH
- code/agent/llm/client.py:33: from openai — REAL_CALL_PATH
- code/tests/.tmp/test_comment_pattern_classifie0/module.py:1: import openai — COMMENT_OR_DOCSTRING
- code/tests/.tmp/test_report_lists_env_and_patt0/code/module.py:1: import openai — REAL_CALL_PATH
- code/tests/test_audit_llm_usage.py:4: import openai — TEST_FIXTURE
- code/tests/test_audit_llm_usage.py:5: import openai — TEST_FIXTURE
- code/tests/test_audit_llm_usage.py:8: import openai — TEST_FIXTURE
- code/tests/test_evidence_handlers.py:28: VLM\( — TEST_FIXTURE
- code/tests/test_llm_client.py:27: import openai — TEST_FIXTURE
- code/tests/test_llm_semantic_resolver.py:19: LLM\( — TEST_FIXTURE
- code/tests/test_llm_semantic_resolver.py:25: LLM\( — TEST_FIXTURE
- code/tests/test_llm_semantic_resolver.py:29: LLM\( — TEST_FIXTURE
- code/tests/test_llm_semantic_resolver.py:33: LLM\( — TEST_FIXTURE
- code/tests/test_llm_semantic_resolver.py:37: LLM\( — TEST_FIXTURE
- code/tests/test_llm_semantic_resolver.py:47: LLM\( — TEST_FIXTURE
- code/tests/test_llm_semantic_resolver.py:54: LLM\( — TEST_FIXTURE
## Dynamic run log
- Per-case logs inspected: 550
- Per-case evidence VLM calls recorded (cache hits may be zero): 0
- The production registry dispatches images directly to OCR and the configured Vision client. Prompt-cache hits avoid repeat API calls.
## Environment variables
- Read by code: ['OPENAI_LLM_DISABLED', 'OPENAI_MAX_RETRIES', 'OPENAI_MODEL', 'OPENAI_TIMEOUT', 'ORCHESTRATOR_SKIP_EVIDENCE']
## Image handler
- direct OCR plus gpt-4o-mini Vision extraction
## Conclusion
The application uses the OpenAI SDK when a valid repository-local .env key is present; otherwise it runs source-grounded OCR/rules and records Vision unavailability. Actual token usage is tracked in usage_report.md. The static scan is not a substitute for dynamic usage tracking.
