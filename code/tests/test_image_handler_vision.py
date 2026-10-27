from types import SimpleNamespace as N

from agent.evidence.handlers.image_handler import extract
from PIL import Image, ImageDraw


class FakeVision:
    enabled=True
    def __init__(self,result):self.result=result;self.calls=0
    def call_vision(self,*args,**kwargs):self.calls+=1;return self.result


IDENTITY=N(all_user_ids={"U1"},all_emails={"a@example.com"})


def _png(tmp_path,text=""):
    path=tmp_path/"screen.png"
    image=Image.new("RGB",(300,100),"white")
    if text: ImageDraw.Draw(image).text((20,30),text,fill="black")
    image.save(path)
    return path


def test_image_extracts_identity_linked_record(tmp_path):
    path=_png(tmp_path,"account_1 U1")
    vision=FakeVision('{"records":[{"system_id":"account_service","resource_id":"account_1","user_ref":"U1","state_at_evidence":"PRESENT","page":1,"visible_text":"account_1 U1","pii_hits":[{"field_path":"Email","value_kind":"email","value":"a@example.com"}]}]}')
    result=extract(path,"ev1",IDENTITY,llm_client=vision)
    assert 1<=vision.calls<=3 and result.records[0].resource_id=="account_1"
    assert any(hit.value_kind=="email" for hit in result.records[0].pii_hits)


def test_image_filters_unrelated_user(tmp_path):
    path=_png(tmp_path)
    vision=FakeVision('{"records":[{"system_id":"account_service","resource_id":"account_2","user_ref":"U2","state_at_evidence":"PRESENT","pii_hits":[]}]}')
    result=extract(path,"ev1",IDENTITY,llm_client=vision)
    assert result.records==[]


def test_image_rejects_title_or_resource_as_system_id(tmp_path):
    path=_png(tmp_path)
    for label in ("Northstar Shop","backup_9287"):
        vision=FakeVision('{"records":[{"system_id":"'+label+'","resource_id":"backup_9287","user_ref":"U1","state_at_evidence":"PRESENT","pii_hits":[{"field_path":"Email","value_kind":"email","value":"a@example.com"}]}]}')
        assert extract(path,"ev1",IDENTITY,llm_client=vision).records==[]
