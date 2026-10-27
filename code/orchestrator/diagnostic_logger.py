"""Per-case JSONL audit trace with mandatory source citations."""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import time

@dataclass
class LogEntry:
    case_id: str
    phase: str
    event: str
    grounded_in: str
    decision: str
    inputs: dict
    outputs: dict
    timestamp: str
    elapsed_ms: float

class DiagnosticLogger:
    def __init__(self, case_id: str, root: Path | None = None):
        self.case_id=case_id
        self.path=(Path(root) if root else Path(__file__).resolve().parents[2])/"code/.cache/diagnostics"/f"{case_id}.jsonl"
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.f=self.path.open("w",encoding="utf-8")
        self.t0=time.perf_counter()

    def log(self, phase, event, grounded_in, decision, inputs, outputs):
        if not grounded_in or not str(grounded_in).strip():
            raise ValueError(f"diagnostic log entry lacks grounded_in: {event}")
        entry=LogEntry(self.case_id,phase,event,str(grounded_in),str(decision),inputs,outputs,datetime.now(timezone.utc).isoformat(),round((time.perf_counter()-self.t0)*1000,3))
        self.f.write(json.dumps(asdict(entry),ensure_ascii=False,sort_keys=True,default=str)+"\n")
        self.f.flush()

    def close(self):
        if not self.f.closed: self.f.close()

    def __enter__(self): return self
    def __exit__(self,*_): self.close()
