"""Check that the runnable audit pipeline cannot import sample-answer tooling.

The sample answer is allowed in evaluation commands.  This audit starts at the
production CLI, follows local Python imports, and checks its dependency closure.
It does not treat a successful sample comparison as an unbiased held-out score.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path


CODE_ROOT = Path(__file__).resolve().parents[1]
EVALUATION_MODULES = frozenset(
    {
        "orchestrator.dataset_catalog",
        "orchestrator.gold_validation",
        "orchestrator.leakage_audit",
        "orchestrator.residual_provenance",
        "orchestrator.sample_compare",
        "orchestrator.step_diff",
        "orchestrator.triage_mismatches",
    }
)
_GOLD_FILE = re.compile(r"(?:^|[/\\])(?:sample_output(?:_phase\d+)?\.csv|gold_validation_report\.md)(?:$|[/\\])", re.I)
_CASE_LITERAL = re.compile(r"\bcase_\d{2,}\b", re.I)


@dataclass(frozen=True)
class LeakageFinding:
    module: str
    line: int
    kind: str
    value: str


def module_files(code_root: Path = CODE_ROOT) -> dict[str, Path]:
    """Return the local import names available under the runnable code root."""
    files: dict[str, Path] = {}
    for top in ("agent", "orchestrator"):
        for path in (code_root / top).rglob("*.py"):
            parts = path.relative_to(code_root).with_suffix("").parts
            name = ".".join(parts[:-1] if parts[-1] == "__init__" else parts)
            files[name] = path
    return files


def _local_imports(module: str, tree: ast.AST, available: set[str], is_package: bool = False) -> set[str]:
    found: set[str] = set()
    package = module.split(".") if is_package else module.split(".")[:-1]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            candidates = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = ".".join(package[: len(package) - node.level + 1] + ([node.module] if node.module else [])) if node.level else (node.module or "")
            candidates = [base] + [f"{base}.{alias.name}" for alias in node.names if alias.name != "*"]
        else:
            continue
        for candidate in candidates:
            components = candidate.split(".")
            for end in range(1, len(components) + 1):
                prefix = ".".join(components[:end])
                if prefix in available:
                    found.add(prefix)
    return found


def inspect_tree(module: str, tree: ast.AST) -> list[LeakageFinding]:
    findings: list[LeakageFinding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        value = node.value
        if _GOLD_FILE.search(value):
            findings.append(LeakageFinding(module, node.lineno, "gold_file_literal", value))
        if _CASE_LITERAL.search(value):
            findings.append(LeakageFinding(module, node.lineno, "case_specific_literal", value))
    return findings


def audit_production(code_root: Path = CODE_ROOT, entrypoint: str = "orchestrator.run") -> tuple[list[str], list[LeakageFinding]]:
    paths = module_files(code_root)
    if entrypoint not in paths:
        raise ValueError(f"Unknown production entrypoint: {entrypoint}")
    visited: set[str] = set()
    findings: list[LeakageFinding] = []
    queue = [entrypoint]
    while queue:
        module = queue.pop()
        if module in visited:
            continue
        visited.add(module)
        if module in EVALUATION_MODULES:
            findings.append(LeakageFinding(module, 0, "evaluation_module_imported", module))
        tree = ast.parse(paths[module].read_text(encoding="utf-8"), filename=str(paths[module]))
        findings.extend(inspect_tree(module, tree))
        queue.extend(_local_imports(module, tree, set(paths), paths[module].name == "__init__.py") - visited)
    return sorted(visited), sorted(findings, key=lambda x: (x.module, x.line, x.kind))


def write_report(root: Path = CODE_ROOT.parent) -> Path:
    modules, findings = audit_production(root / "code")
    report = root / "code/evaluation/leakage_audit.md"
    lines = [
        "# Production answer-leak audit",
        "",
        "The audit follows local Python imports from `orchestrator.run`, then checks each reachable module for sample-answer paths and case-specific string literals.",
        f"Reachable modules: {len(modules)}. Findings: {len(findings)}.",
        "",
        "## Reachable production modules",
        "",
        *[f"- `{name}`" for name in modules],
        "",
        "## Static findings",
        "",
        *([f"- `{f.module}:{f.line}` `{f.kind}`: `{f.value}`" for f in findings] or ["None."]),
        "",
        "## Evaluation boundary",
        "",
        "`sample_output.csv` is read by separate comparison and diagnostic commands. The production import graph must not reach those commands, and `orchestrator.run` only writes `output.csv`. Runtime read guards are covered in `test_no_gold_leak.py`.",
        "",
        "The 32 supplied sample cases have been inspected repeatedly during development. Their accuracy is a development-set fit measure, not an unbiased estimate of hidden-case accuracy. The 486 other requests have no supplied answer labels; their structural and source-grounding checks cannot establish correctness against a hidden gold output.",
        "",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    modules, findings = audit_production()
    path = write_report()
    print(f"{len(modules)} production modules; {len(findings)} findings; report={path}")
    raise SystemExit(bool(findings))
