from types import SimpleNamespace
from pathlib import Path
from PIL import Image
from agent.evidence.handlers import image_handler
from orchestrator.image_inspector import post_audit_exif

IDENTITY = SimpleNamespace(all_user_ids={"U1"}, all_emails={"a@example.com"})


def _png(tmp_path):
    path = tmp_path / "sample.png"
    Image.new("RGB", (20, 20), "white").save(path)
    return path


class Vision:
    enabled = True
    def __init__(self): self.calls = []
    def call_vision(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return '{"records":[{"system_id":"account_service","resource_id":"account_1","user_ref":"U1","state_at_evidence":"PRESENT","pii_hits":[{"field_path":"Email","value_kind":"email","value":"a@example.com"}],"visible_text":"account_1 U1"}]}'


def test_ocr_owner_is_cross_checked_by_vision(tmp_path, monkeypatch):
    monkeypatch.setattr(image_handler, "run_tesseract", lambda _: "account_1 U1")
    vision = Vision()
    result = image_handler.extract(_png(tmp_path), "ev", IDENTITY, llm_client=vision)
    assert result.extraction_method == "ocr_plus_vision" and len(result.records) == 1
    assert result.records[0].resource_id == "account_1" and len(vision.calls) == 1


def test_ocr_and_vision_same_row_do_not_create_ghost_duplicate(tmp_path, monkeypatch):
    monkeypatch.setattr(image_handler, "run_tesseract", lambda _: "account_1 U1")
    class AbsentVision(Vision):
        def call_vision(self,*args,**kwargs):
            self.calls.append((args,kwargs))
            return '{"records":[{"system_id":"account_service","resource_id":"account_1","user_ref":"U1","state_at_evidence":"ABSENT","pii_hits":[],"visible_text":"account_1 U1"}]}'
    result=image_handler.extract(_png(tmp_path),"ev",IDENTITY,llm_client=AbsentVision())
    assert len(result.records)==1 and result.records[0].state_at_evidence=="ABSENT"


def test_no_tesseract_text_falls_back_to_mini_vision(tmp_path, monkeypatch):
    monkeypatch.setattr(image_handler, "run_tesseract", lambda _: "")
    vision = Vision()
    result = image_handler.extract(_png(tmp_path), "ev", IDENTITY, llm_client=vision)
    assert result.records[0].user_ref == "U1" and result.records[0].pii_hits[0].value == "a@example.com" and len(vision.calls) == 2


def test_model_ownership_claim_without_ocr_subject_is_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(image_handler, "run_tesseract", lambda _: "account_1")
    vision = Vision()
    result = image_handler.extract(_png(tmp_path), "ev", IDENTITY, llm_client=vision)
    assert result.records == []
    assert any(note.startswith("vision_rows_lacking_independent_corroboration") for note in result.notes)


def test_missing_tesseract_executable_returns_empty(tmp_path, monkeypatch):
    import pytesseract
    from orchestrator.image_inspector import run_tesseract
    monkeypatch.setattr(pytesseract, "image_to_string", lambda _: (_ for _ in ()).throw(OSError("not installed")))
    assert run_tesseract(_png(tmp_path)) == ""


def test_ocr_without_same_row_owner_uses_vision_fallback(tmp_path, monkeypatch):
    monkeypatch.setattr(image_handler, "run_tesseract", lambda _: "account_1\nU1")
    vision = Vision()
    result = image_handler.extract(_png(tmp_path), "ev", IDENTITY, llm_client=vision)
    assert len(result.records) == 1 and len(vision.calls) == 1


def test_exif_post_audit_is_excluded(tmp_path):
    path = tmp_path / "future.jpg"
    image = Image.new("RGB", (20, 20), "white")
    exif = image.getexif(); exif[36867] = "2027:01:01 00:00:00"
    image.save(path, exif=exif)
    assert post_audit_exif(path, "2026-09-01T00:00:00Z")
    assert image_handler.extract(path, "ev", IDENTITY, "2026-09-01T00:00:00Z").records == []


def test_ocr_exact_id_not_prefix():
    assert image_handler._ocr_records("account_10 U10", IDENTITY) == []


def test_ocr_multiple_resource_ids_on_one_row_is_ambiguous():
    assert image_handler._ocr_records("account_1 account_2 U1",IDENTITY)==[]


def test_ocr_collects_phone_and_email_from_same_owned_row():
    records=image_handler._ocr_records("account_1 U1 a@example.com +1 555 123 4567",IDENTITY)
    assert len(records)==1
    assert {h.value_kind for h in records[0].pii_hits}>={"user_id","email","phone"}


def test_ocr_selected_header_links_to_unique_adjacent_owner():
    text="Support console\nsupport_1 - Customer\nPriority high\na@example.com\nConversation"
    records=image_handler._ocr_records(text,IDENTITY)
    assert [(r.resource_id,r.user_ref) for r in records]==[("support_1","a@example.com")]


def test_ocr_selected_header_rejects_competing_owner():
    text="support_1 - Customer\na@example.com b@example.com"
    identity=SimpleNamespace(all_user_ids={"U1"},all_emails={"a@example.com","b@example.com"})
    assert image_handler._ocr_records(text,identity)==[]


def test_ocr_does_not_join_other_email_row_to_selected_detail():
    text="search_1874 stranger@example.com score 4.12\nemail a@example.com"
    assert image_handler._ocr_records(text,IDENTITY)==[]


def test_real_search_screenshot_does_not_assign_nearby_other_email():
    source=Path(__file__).resolve().parents[2]/"dataset/evidence/images/search_index_inspector_20260901.png"
    subject=SimpleNamespace(all_user_ids={"user_13"},all_emails={"g.silva76@gmail.com"})
    records=image_handler._ocr_records(image_handler.run_tesseract(source),subject)
    assert {r.resource_id for r in records}=={"search_428"}


def test_real_support_screenshot_selected_header_maps_to_owner():
    source=Path(__file__).resolve().parents[2]/"dataset/evidence/images/support_ticket_console_20260524.png"
    subject=SimpleNamespace(all_user_ids={"user_22"},all_emails={"kagyeman8947@fastmail.com"})
    records=image_handler._ocr_records(image_handler.run_tesseract(source),subject)
    assert {(r.system_id,r.resource_id) for r in records}=={("support_platform","support_1034")}


def test_client_vision_default_is_mini(tmp_path):
    from agent.llm.client import LLMClient
    path = _png(tmp_path)
    client = LLMClient(tmp_path / "cache", tmp_path / "traces", sdk_client=Vision())
    called = []
    client._call = lambda *args: called.append(args) or '{"records":[]}'
    assert client.call_vision("JSON", path) == '{"records":[]}'
    assert called[0][3] == "gpt-4o-mini"


def test_high_detail_is_the_default_when_accuracy_has_priority(tmp_path):
    from agent.llm.client import LLMClient
    client=LLMClient(tmp_path / "cache",tmp_path / "traces",sdk_client=Vision())
    args=[]
    client._call=lambda *a: args.append(a) or '{"records":[]}'
    client.call_vision("read every visible row",_png(tmp_path))
    assert args[0][-1]=="high" and args[0][3]=="gpt-4o-mini"


def test_inventory_uses_mini_only_when_ocr_empty(tmp_path, monkeypatch):
    from orchestrator import image_inspector
    monkeypatch.setattr(image_inspector, "run_tesseract", lambda _: "")
    vision = Vision()
    result = image_inspector.inspect_image(_png(tmp_path), vision)
    assert result["method"] == "vision" and vision.calls[0][1]["model"] == "gpt-4o-mini"


def test_low_detail_and_high_detail_have_separate_cache_entries(tmp_path):
    from agent.llm.client import LLMClient
    class SDK:
        def __init__(self):
            self.calls = []
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))
        def create(self, **kwargs):
            self.calls.append(kwargs)
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='{"records":[]}'))],
                                   usage=SimpleNamespace(prompt_tokens=3, completion_tokens=2))
    sdk = SDK(); path = _png(tmp_path)
    client = LLMClient(tmp_path / "cache", tmp_path / "traces", sdk_client=sdk)
    client.call_vision("find rows", path)
    client.call_vision("find rows", path)
    client.call_vision("find rows", path, detail="low")
    assert len(sdk.calls) == 2
    assert sdk.calls[0]["messages"][0]["content"][1]["image_url"]["detail"] == "high"
    assert sdk.calls[1]["messages"][0]["content"][1]["image_url"]["detail"] == "low"
