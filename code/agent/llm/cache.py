"""Prompt/response cache; all files live under the repository-local .cache."""

import hashlib
import json
from pathlib import Path


class LLMCache:
    def __init__(self, directory: Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def key(prompt: str, model: str, temperature: float, image_hash: str = "") -> str:
        payload = json.dumps([prompt, model, temperature, image_hash], ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def get(self, key: str) -> str | None:
        path = self.directory / f"{key}.json"
        if not path.is_file():
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))["response"]
            return value if isinstance(value, str) else None
        except (OSError, ValueError, KeyError):
            return None

    def set(self, key: str, response: str) -> None:
        path = self.directory / f"{key}.json"
        path.write_text(json.dumps({"response": response}, ensure_ascii=False), encoding="utf-8")
