from types import SimpleNamespace
from agent.evidence.registry import extract_file
from agent.evidence.handlers import image_handler


def test_registry_images_use_real_ocr_handler_not_empty_placeholder(tmp_path,monkeypatch):
    from PIL import Image
    path=tmp_path/"dataset/evidence/test.png"
    path.parent.mkdir(parents=True)
    Image.new("RGB",(20,20),"white").save(path)
    monkeypatch.setattr(image_handler,"run_tesseract",lambda _:"account_1 user_1 a@example.com")
    identity=SimpleNamespace(all_user_ids={"user_1"},all_emails={"a@example.com"})
    result=extract_file(tmp_path,"ev","evidence/test.png",identity,"2026-02-01T00:00:00Z")
    assert result.file_path=="evidence/test.png"
    assert [(record.system_id,record.resource_id) for record in result.records]==[("account_service","account_1")]
