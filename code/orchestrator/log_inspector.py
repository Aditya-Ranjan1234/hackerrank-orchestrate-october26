"""Detect structured log variants and expose fields for inventory/audit."""
import json
import re
from pathlib import Path

KV = re.compile(r"(?:^|\s)([A-Za-z_][\w-]*)=([^\s]+)")


def inspect_log(path):
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    counts = {"jsonl": 0, "key_value": 0, "pipe": 0, "free_text": 0}
    keys = set()
    for line in lines:
        if "{" in line:
            try:
                value = json.loads(line[line.index("{"):])
                if isinstance(value, dict):
                    counts["jsonl"] += 1; keys.update(value)
                    continue
            except json.JSONDecodeError:
                pass
        found = KV.findall(line)
        if found:
            counts["key_value"] += 1; keys.update(k for k, _ in found)
        elif line.count("|") >= 4:
            counts["pipe"] += 1
        else:
            counts["free_text"] += 1
    return {"line_count": len(lines), "formats": counts, "fields": sorted(keys),
            "first_lines": lines[:20], "last_lines": lines[-20:]}
