"""Track actual API response usage; estimates never masquerade as measured tokens."""

from collections import defaultdict
from pathlib import Path

# USD per million tokens, from official model pages (October 2026).
PRICING = {"gpt-4o-mini": (0.15, 0.60), "gpt-4o": (2.50, 10.00)}


class UsageTracker:
    _instance = None

    def __init__(self):
        self.calls: list[tuple[str, str, int, int, str | None]] = []
        self.request_count: int | None = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def record(self, purpose: str, model: str, input_tokens: int, output_tokens: int, case_id=None):
        self.calls.append((purpose, model, int(input_tokens), int(output_tokens), case_id))

    def totals(self):
        return len(self.calls), sum(x[2] for x in self.calls), sum(x[3] for x in self.calls)

    def estimated_cost(self):
        return sum((a * PRICING[m][0] + b * PRICING[m][1]) / 1_000_000
                   for _, m, a, b, _ in self.calls if m in PRICING)

    def write_report(self, path: Path):
        path = Path(path)
        grouped = defaultdict(lambda: [0, 0, 0])
        for purpose, model, ti, to, _ in self.calls:
            row = grouped[(purpose, model)]
            row[0] += 1; row[1] += ti; row[2] += to
        lines = ["## Phase 17 — OpenAI application usage", "", "Only actual API responses count as calls; cache hits cost zero tokens. Provider: OpenAI.", "", "| Purpose | Model | Calls | Input tokens | Output tokens | Estimated USD |", "|---|---|---:|---:|---:|---:|"]
        for (purpose, model), (calls, ti, to) in sorted(grouped.items()):
            rates = PRICING.get(model)
            cost = f"${(ti*rates[0]+to*rates[1])/1_000_000:.6f}" if rates else "unknown rate"
            lines.append(f"| {purpose} | {model} | {calls} | {ti} | {to} | {cost} |")
        calls, ti, to = self.totals()
        lines += [f"| **Total** | | **{calls}** | **{ti}** | **{to}** | **${self.estimated_cost():.6f}** |", "", "Rates: https://developers.openai.com/api/docs/models/gpt-4o-mini and https://developers.openai.com/api/docs/models/gpt-4o. Unknown model rates are not silently priced at zero.", ""]
        if self.request_count:
            count=self.request_count
            lines += [f"Requests in run: {count}. Average input tokens/request: {ti/count:.2f}; average output tokens/request: {to/count:.2f}; average total tokens/request: {(ti+to)/count:.2f}; estimated cost/request: ${self.estimated_cost()/count:.6f}.", ""]
        path.parent.mkdir(parents=True, exist_ok=True)
        prior = path.read_text(encoding="utf-8") if path.exists() else ""
        # Replace only the current Phase 17 section on rerun; preserve earlier phases.
        marker = "## Phase 17 — OpenAI application usage"
        if marker in prior:
            prior = prior[:prior.index(marker)].rstrip() + "\n\n"
        path.write_text(prior + "\n".join(lines), encoding="utf-8")
