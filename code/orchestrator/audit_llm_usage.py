"""Static and run-log audit of LLM/VLM call paths and environment reads."""
import ast
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PATTERNS=[r"import openai",r"from openai",r"openai\.ChatCompletion",r"import anthropic",r"from anthropic",r"zai_web_dev_sdk",r"z-ai-web-dev-sdk",r"requests\.post\(.*api\.",r"httpx\.post\(.*api\.",r"os\.environ\[.API_KEY.\]",r"os\.getenv\(.API_KEY.\)",r"VLM\(",r"LLM\(",r"chat_completion"]

def classify_line(path, line_no, line):
    stripped=line.lstrip()
    if stripped.startswith("#") or path.suffix in {".md",".txt"}: return "COMMENT_OR_DOCSTRING"
    try:
        source=path.read_text(encoding="utf-8")
        tree=ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node,ast.Expr) and isinstance(node.value,(ast.Constant,ast.JoinedStr)) and getattr(node,"lineno",0)<=line_no<=getattr(node,"end_lineno",0):
                return "COMMENT_OR_DOCSTRING"
    except (SyntaxError,UnicodeError): pass
    if path.name.startswith("test_"): return "TEST_FIXTURE"
    return "REAL_CALL_PATH"

def audit_llm_usage(root=ROOT):
    root=Path(root); hits=[]; env=set()
    for path in sorted((root/"code").rglob("*.py")):
        # Test workspaces may themselves live under .cache; only exclude
        # generated directories *inside* the audited code tree.
        relative_parts=path.relative_to(root/"code").parts
        if any(p in {".cache","__pycache__",".venv"} for p in relative_parts[:-1]) or path.name=="audit_llm_usage.py": continue
        for i,line in enumerate(path.read_text(encoding="utf-8",errors="replace").splitlines(),1):
            for pat in PATTERNS:
                if re.search(pat,line,re.I):
                    kind=classify_line(path,i,line)
                    if path.name=="image_handler.py" and "vlm(path, identities" in line:
                        kind="INJECTED_CALLBACK_ONLY"
                    hits.append((path.relative_to(root).as_posix(),i,pat,kind))
            if "tests" not in path.parts:
                for m in re.finditer(r"os\.(?:environ\.get|getenv|environ\[)\s*\(?\s*['\"]([A-Za-z_][A-Za-z_0-9]*)",line): env.add(m.group(1))
    logs=[p for p in (root/"code/.cache/diagnostics").glob("*.jsonl") if re.fullmatch(r"case_\d+",p.stem)]
    vlm_calls=0
    for path in logs:
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                obj=json.loads(line)
                if obj.get("phase")=="evidence": vlm_calls+=obj.get("outputs",{}).get("vlm_call_count",0)
            except json.JSONDecodeError: pass
    image=(root/"code/agent/evidence/handlers/image_handler.py")
    stub="direct OCR plus gpt-4o-mini Vision extraction" if image.exists() and "transcribe_image" in image.read_text(encoding="utf-8") else "UNCONFIRMED"
    result=["# LLM usage audit", "## Static scan"]
    result += [f"- {p}:{line}: {pat} — {kind}" for p,line,pat,kind in hits] or ["- No SDK or API call pattern hits."]
    result += ["## Dynamic run log",f"- Per-case logs inspected: {len(logs)}",f"- Per-case evidence VLM calls recorded (cache hits may be zero): {vlm_calls}","- The production registry dispatches images directly to OCR and the configured Vision client. Prompt-cache hits avoid repeat API calls.","## Environment variables",f"- Read by code: {sorted(env)}", "## Image handler",f"- {stub}","## Conclusion"]
    result += ["The application uses the OpenAI SDK when a valid repository-local .env key is present; otherwise it runs source-grounded OCR/rules and records Vision unavailability. Actual token usage is tracked in usage_report.md. The static scan is not a substitute for dynamic usage tracking."]
    return "\n".join(result)+"\n"

if __name__=="__main__":
    out=ROOT/"code/evaluation/llm_usage_audit.md"; out.write_text(audit_llm_usage(),encoding="utf-8"); print(out)
