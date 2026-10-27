"""Small OpenAI Chat Completions adapter with cache, retry, trace and fallback."""

import base64
import hashlib
import json
import os
import time
from pathlib import Path

from .cache import LLMCache
from .tracer import LLMTrace, LLMTracer
from .usage_tracker import UsageTracker


class LLMClient:
    def __init__(self, cache_dir=None, traces_dir=None, sdk_client=None, sleeper=time.sleep, env_file=None):
        self.model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        self.timeout = max(1, int(os.environ.get("OPENAI_TIMEOUT", "30")))
        self.max_retries = max(1, min(5, int(os.environ.get("OPENAI_MAX_RETRIES", "3"))))
        self.cache = LLMCache(Path(cache_dir or "code/.cache/llm_cache"))
        self.tracer = LLMTracer(Path(traces_dir or "code/.cache/llm_traces"))
        self._sleep = sleeper
        self._client = sdk_client
        self.env_file = Path(env_file) if env_file is not None else Path(__file__).resolve().parents[3] / ".env"
        # The repository-local .env is the sole credential source. In particular,
        # a stale process-level OPENAI_API_KEY must never silently override it.
        from dotenv import dotenv_values
        local_key = dotenv_values(self.env_file).get("OPENAI_API_KEY") if self.env_file.is_file() else None
        if os.environ.get("OPENAI_LLM_DISABLED") == "1":
            local_key = None
        if self._client is None and local_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=local_key, timeout=self.timeout, max_retries=0)
            except (ImportError, ValueError):
                self._client = None

    @property
    def enabled(self):
        return self._client is not None

    def _call(self, prompt, purpose, case_id, model, temperature, max_tokens, image_bytes=None, mime=None, detail="high", response_schema=None):
        if not self.enabled:
            return None
        model = model or self.model
        image_hash = hashlib.sha256(image_bytes).hexdigest() if image_bytes else ""
        schema_key = json.dumps(response_schema, sort_keys=True) if response_schema else ""
        key = self.cache.key(prompt + (f"|image_detail={detail}" if image_bytes else "") + schema_key, model, temperature, image_hash)
        cached = self.cache.get(key)
        if cached is not None:
            self.tracer.write(LLMTrace(key,purpose,model,case_id,True,True,prompt,cached,0,0,0))
            return cached
        content = [{"type":"text","text":prompt}]
        if image_bytes:
            uri = f"data:{mime};base64,{base64.b64encode(image_bytes).decode('ascii')}"
            content.append({"type":"image_url","image_url":{"url":uri,"detail":detail}})
        last_error = None
        for attempt in range(self.max_retries):
            started = time.monotonic()
            value = None
            ti = to = 0
            try:
                revised = content if attempt == 0 else [{**content[0],"text":prompt+"\nReturn only a valid JSON object with the required fields."},*content[1:]]
                response = self._client.chat.completions.create(
                    model=model, temperature=temperature, max_tokens=max_tokens,
                    messages=[{"role":"user","content":revised}],
                    response_format=({"type":"json_schema","json_schema":response_schema}
                                     if response_schema else {"type":"json_object"}),
                )
                value = response.choices[0].message.content
                usage = getattr(response,"usage",None)
                ti = int(getattr(usage,"prompt_tokens",0) or 0)
                to = int(getattr(usage,"completion_tokens",0) or 0)
                UsageTracker.instance().record(purpose,model,ti,to,case_id)
                if not isinstance(json.loads(value),dict):
                    raise ValueError("LLM response was not a JSON object")
                self.cache.set(key,value)
                self.tracer.write(LLMTrace(key,purpose,model,case_id,True,False,prompt,value,ti,to,(time.monotonic()-started)*1000))
                return value
            except (Exception,) as exc:
                last_error = type(exc).__name__
                self.tracer.write(LLMTrace(key,purpose,model,case_id,False,False,prompt,value,ti,to,(time.monotonic()-started)*1000,last_error))
                if last_error in {"AuthenticationError", "PermissionDeniedError"}:
                    # Retrying an invalid key across thousands of evidence rows
                    # cannot succeed; make the rest of this run rule-only.
                    self._client = None
                    break
                if attempt < self.max_retries-1:
                    self._sleep(min(2 ** attempt, 4))
        return None

    def call(self,prompt,call_purpose,case_id=None,model=None,temperature=0.0,max_tokens=500,response_schema=None):
        if response_schema is not None:
            return self._call(prompt,call_purpose,case_id,model,temperature,max_tokens,response_schema=response_schema)
        return self._call(prompt,call_purpose,case_id,model,temperature,max_tokens)

    def call_vision(self,prompt,image_path,call_purpose="image_pii",case_id=None,model="gpt-4o-mini",max_tokens=500,detail=None,response_schema=None):
        path=Path(image_path)
        try:
            data=path.read_bytes()
        except OSError:
            return None
        if data.startswith(b"\x89PNG\r\n\x1a\n"):
            mime="image/png"
        elif data.startswith(b"\xff\xd8\xff"):
            mime="image/jpeg"
        else:
            return None
        if len(data)>10_000_000:
            return None
        try:
            from PIL import Image
            with Image.open(path) as image: image.verify()
        except (ImportError, OSError, ValueError):
            return None
        if response_schema is not None:
            return self._call(prompt,call_purpose,case_id,model,0.0,max_tokens,data,mime,detail or "high",response_schema=response_schema)
        return self._call(prompt,call_purpose,case_id,model,0.0,max_tokens,data,mime,detail or "high")
