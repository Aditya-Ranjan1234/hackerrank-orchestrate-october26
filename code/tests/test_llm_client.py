import json
from types import SimpleNamespace as N

from agent.llm.client import LLMClient
from agent.llm.usage_tracker import UsageTracker


class FakeSDK:
    def __init__(self, replies):
        self.replies=list(replies); self.calls=0
        self.chat=N(completions=N(create=self.create))

    def create(self, **kwargs):
        self.calls+=1
        value=self.replies.pop(0)
        if isinstance(value,Exception): raise value
        return N(choices=[N(message=N(content=value))],usage=N(prompt_tokens=7,completion_tokens=3))


def test_no_key_disables_calls(monkeypatch,tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY","wrong-process-key")
    client=LLMClient(tmp_path/"cache",tmp_path/"traces",env_file=tmp_path/"missing.env")
    assert not client.enabled and client.call("JSON please","system_id") is None


def test_repo_env_file_overrides_conflicting_process_key(monkeypatch,tmp_path):
    import openai
    seen=[]
    monkeypatch.delenv("OPENAI_LLM_DISABLED",raising=False)
    monkeypatch.setenv("OPENAI_API_KEY","wrong-process-key")
    local_file=tmp_path/".env"
    local_file.write_text('OPENAI_API_KEY="correct-local-key"\n',encoding="utf-8")
    monkeypatch.setattr(openai,"OpenAI",lambda **kwargs: seen.append(kwargs["api_key"]) or FakeSDK(['{"ok":true}']))
    client=LLMClient(tmp_path/"cache",tmp_path/"traces",env_file=local_file)
    assert client.enabled and seen==["correct-local-key"]
    assert client.call("Return JSON","system_id")=='{"ok":true}'


def test_success_and_cache_hit_no_second_usage(tmp_path,monkeypatch):
    monkeypatch.setenv("OPENAI_MAX_RETRIES","1")
    sdk=FakeSDK(['{"system_id":"account_service"}'])
    client=LLMClient(tmp_path/"cache",tmp_path/"traces",sdk_client=sdk)
    before=UsageTracker.instance().totals()
    assert json.loads(client.call("JSON please","system_id"))["system_id"]=="account_service"
    assert client.call("JSON please","system_id") is not None
    assert sdk.calls==1
    assert UsageTracker.instance().totals()[0]==before[0]+1
    assert len(list((tmp_path/"traces").glob("*.json")))==2


def test_malformed_json_retries_then_falls_back(tmp_path,monkeypatch):
    monkeypatch.setenv("OPENAI_MAX_RETRIES","2")
    sdk=FakeSDK(["not json","still not json"])
    client=LLMClient(tmp_path/"cache",tmp_path/"traces",sdk_client=sdk,sleeper=lambda _:None)
    before=UsageTracker.instance().totals()
    assert client.call("JSON please","flow_class") is None
    assert sdk.calls==2
    traces=[json.loads(path.read_text(encoding="utf-8")) for path in (tmp_path/"traces").glob("*.json")]
    assert len(traces)==2 and all(not t["success"] and t["input_tokens"]==7 and t["output_tokens"]==3 for t in traces)
    assert UsageTracker.instance().totals()[0]==before[0]+2


def test_timeout_and_network_error_retry(tmp_path,monkeypatch):
    monkeypatch.setenv("OPENAI_MAX_RETRIES","2")
    sdk=FakeSDK([TimeoutError("timeout"),ConnectionError("network")])
    client=LLMClient(tmp_path/"cache",tmp_path/"traces",sdk_client=sdk,sleeper=lambda _:None)
    assert client.call("JSON please","system_id") is None and sdk.calls==2


def test_rate_limit_retry_then_success(tmp_path,monkeypatch):
    monkeypatch.setenv("OPENAI_MAX_RETRIES","2")
    sdk=FakeSDK([RuntimeError("429 rate limit"),'{"classification":"record"}'])
    client=LLMClient(tmp_path/"cache",tmp_path/"traces",sdk_client=sdk,sleeper=lambda _:None)
    assert client.call("JSON please","flow_class")=='{"classification":"record"}'
    assert sdk.calls==2


def test_authentication_error_circuit_breaks(tmp_path,monkeypatch):
    monkeypatch.setenv("OPENAI_MAX_RETRIES","3")
    AuthenticationError=type("AuthenticationError",(Exception,),{})
    sdk=FakeSDK([AuthenticationError("invalid key")])
    client=LLMClient(tmp_path/"cache",tmp_path/"traces",sdk_client=sdk,sleeper=lambda _:None)
    assert client.call("JSON please","system_id") is None
    assert not client.enabled and sdk.calls==1


def test_vision_rejects_non_image_and_corrupt(tmp_path):
    sdk=FakeSDK([])
    client=LLMClient(tmp_path/"cache",tmp_path/"traces",sdk_client=sdk)
    bad=tmp_path/"bad.png";bad.write_bytes(b"not an image")
    assert client.call_vision("JSON please",bad) is None
    bad.write_bytes(b"\x89PNG\r\n\x1a\nnot a valid PNG")
    assert client.call_vision("JSON please",bad) is None
    assert client.call_vision("JSON please",tmp_path/"missing.png") is None
    assert sdk.calls==0


def test_vision_sends_valid_png_to_mocked_sdk(tmp_path,monkeypatch):
    from PIL import Image
    monkeypatch.setenv("OPENAI_MAX_RETRIES","1")
    path=tmp_path/"valid.png";Image.new("RGB",(2,2),(255,0,0)).save(path)
    sdk=FakeSDK(['{"records":[]}'])
    client=LLMClient(tmp_path/"cache",tmp_path/"traces",sdk_client=sdk)
    assert client.call_vision("Return JSON",path)=='{"records":[]}'
    assert sdk.calls==1


def test_vision_transcript_uses_server_strict_schema_and_separate_cache(tmp_path):
    from PIL import Image
    from orchestrator.image_transcriber import VISION_SCHEMA
    path=tmp_path/"visible.png"
    Image.new("RGB",(2,2),(255,255,255)).save(path)
    class CapturingSDK(FakeSDK):
        def __init__(self):
            super().__init__(['{"records":[]}', '{"records":[]}'])
            self.formats=[]
        def create(self, **kwargs):
            self.formats.append(kwargs["response_format"])
            return super().create(**kwargs)
    sdk=CapturingSDK()
    client=LLMClient(tmp_path/"cache",tmp_path/"traces",sdk_client=sdk)
    client.call_vision("Read rows",path,response_schema=VISION_SCHEMA)
    client.call_vision("Read rows",path,response_schema=VISION_SCHEMA)
    client.call_vision("Read rows",path)
    assert sdk.calls==2
    assert sdk.formats[0]=={"type":"json_schema","json_schema":VISION_SCHEMA}
    assert sdk.formats[1]=={"type":"json_object"}
