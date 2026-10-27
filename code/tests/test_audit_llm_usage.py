from orchestrator.audit_llm_usage import audit_llm_usage, classify_line

def test_comment_pattern_classified(tmp_path):
    p=tmp_path/'module.py'; p.write_text('# import openai\n',encoding='utf-8')
    assert classify_line(p,1,'# import openai')=='COMMENT_OR_DOCSTRING'

def test_report_lists_env_and_pattern(tmp_path):
    code=tmp_path/'code'; code.mkdir(); (code/'module.py').write_text('import openai\nimport os\nx=os.getenv("MY_API_KEY")\n',encoding='utf-8')
    report=audit_llm_usage(tmp_path)
    assert 'REAL_CALL_PATH' in report and 'MY_API_KEY' in report
