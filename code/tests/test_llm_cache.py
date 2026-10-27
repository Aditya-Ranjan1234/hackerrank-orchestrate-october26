from agent.llm.cache import LLMCache


def test_key_is_stable_and_prompt_sensitive():
    assert LLMCache.key("x","gpt-4o-mini",0)==LLMCache.key("x","gpt-4o-mini",0)
    assert LLMCache.key("x","gpt-4o-mini",0)!=LLMCache.key("y","gpt-4o-mini",0)


def test_key_separates_model_temperature_and_image():
    key=LLMCache.key("x","gpt-4o-mini",0)
    assert key!=LLMCache.key("x","gpt-4o",0)
    assert key!=LLMCache.key("x","gpt-4o-mini",0.2)
    assert key!=LLMCache.key("x","gpt-4o-mini",0,"image-digest")


def test_disk_round_trip(tmp_path):
    cache=LLMCache(tmp_path)
    assert cache.get("a") is None
    cache.set("a",'{"ok":true}')
    assert LLMCache(tmp_path).get("a")=='{"ok":true}'
