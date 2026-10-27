"""One local trace per invocation, including cache hits and failed calls."""

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class LLMTrace:
    cache_key: str
    purpose: str
    model: str
    case_id: str | None
    success: bool
    cache_hit: bool
    prompt: str
    response: str | None
    input_tokens: int
    output_tokens: int
    latency_ms: float
    error: str | None = None


class LLMTracer:
    def __init__(self, directory: Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def write(self, trace: LLMTrace) -> Path:
        path = self.directory / f"{uuid.uuid4().hex}.json"
        payload = {**asdict(trace), "timestamp": datetime.now(timezone.utc).isoformat()}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
