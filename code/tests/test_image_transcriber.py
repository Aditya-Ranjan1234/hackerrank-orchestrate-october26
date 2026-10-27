from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from orchestrator.image_transcriber import transcribe_image


class Vision:
    enabled=True
    def __init__(self,payload): self.payload=payload; self.calls=[]
    def call_vision(self,*args,**kwargs): self.calls.append((args,kwargs)); return self.payload


def test_transcript_maps_visible_row_with_mini_high():
    model=Vision('{"records":[{"resource_id":"search_428","user_ref":"user_13","state_at_evidence":"PRESENT","pii_hits":[{"field_path":"Email","value_kind":"email","value":"g.silva76@gmail.com"}],"visible_text":"search_428 Gabriel Silva g.silva76@gmail.com user_13"}]}')
    result=transcribe_image("fake.png",model)
    assert result["records"][0]["system_id"]=="search_service"
    assert model.calls[0][1]["model"]=="gpt-4o-mini" and model.calls[0][1]["detail"]=="high"


def test_transcript_rejects_ownerless_and_cross_row_claims():
    model=Vision('{"records":[{"resource_id":"search_428","user_ref":"user_13","state_at_evidence":"PRESENT","pii_hits":[],"visible_text":"search_428 only"},{"resource_id":"search_1874","user_ref":"user_13","state_at_evidence":"PRESENT","pii_hits":[],"visible_text":"search_1874 different user"}]}')
    assert transcribe_image("fake.png",model)["records"]==[]


def test_transcript_rejects_unrecognized_resource_and_duplicates():
    row='{"resource_id":"backup_1","user_ref":"a@example.com","state_at_evidence":"PRESENT","pii_hits":[],"visible_text":"backup_1 a@example.com"}'
    model=Vision('{"records":['+row+','+row+',{"resource_id":"header","user_ref":"a@example.com","state_at_evidence":"PRESENT","pii_hits":[],"visible_text":"header a@example.com"}]}')
    records=transcribe_image("fake.png",model)["records"]
    assert len(records)==1 and records[0]["system_id"]=="backup_service"


def test_transcript_malformed_response_fails_closed():
    model=Vision("not json")
    assert transcribe_image("fake.png",model)["error"]=="vision_schema_failed_after_retry"
    assert len(model.calls)==2


def test_transcript_retries_invalid_visible_pair_once():
    class CorrectingVision(Vision):
        def call_vision(self,*args,**kwargs):
            self.calls.append((args,kwargs))
            visible="search_428 user_13" if len(self.calls)==2 else "search_428"
            return '{"records":[{"resource_id":"search_428","user_ref":"user_13","state_at_evidence":"PRESENT","pii_hits":[],"visible_text":"'+visible+'"}]}'
    model=CorrectingVision("")
    result=transcribe_image("fake.png",model)
    assert len(model.calls)==2 and len(result["records"])==1


def test_transcript_retries_malformed_json_then_accepts_valid_rows():
    class RepairingVision(Vision):
        def call_vision(self,*args,**kwargs):
            self.calls.append((args,kwargs))
            if len(self.calls)==1:
                return "broken"
            return '{"records":[{"resource_id":"search_428","user_ref":"user_13","state_at_evidence":"PRESENT","pii_hits":[],"visible_text":"search_428 user_13"}]}'
    model=RepairingVision("")
    output=transcribe_image("fake.png",model)
    assert output["error"] is None and len(output["records"])==1
    assert all(call[1]["response_schema"]["strict"] for call in model.calls)
