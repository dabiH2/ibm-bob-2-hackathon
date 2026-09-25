"""Static reachability: is the vulnerable code actually used by the product?

For each finding it records one of four verdicts, with evidence:
  NOT_IMPORTED  - the component is never imported by product code
  NOT_CALLED    - imported, but none of the known vulnerable symbols are used
  REACHABLE     - a known vulnerable symbol is referenced (file:line evidence)
  UNKNOWN       - imported, and nobody has mapped this advisory to symbols yet
                  (this is the gap the Bob "advisory analyst" subagent fills)
"""
from __future__ import annotations

import ast
import json
from dataclasses import dataclass, field
from pathlib import Path

from .osv import Finding

# distribution name -> top-level import names, where they differ
IMPORT_NAMES = {"pyyaml": ["yaml"], "beautifulsoup4": ["bs4"], "pillow": ["PIL"],
                "python-dateutil": ["dateutil"], "scikit-learn": ["sklearn"]}

NOT_IMPORTED, NOT_CALLED, REACHABLE, UNKNOWN = "NOT_IMPORTED", "NOT_CALLED", "REACHABLE", "UNKNOWN"


@dataclass
class Use:
    symbol: str
    file: str
    line: int


@dataclass
class Verdict:
    finding: Finding
    level: str
    evidence: list[Use] = field(default_factory=list)
    note: str = ""


def import_names(dist: str) -> list[str]:
    return IMPORT_NAMES.get(dist, [dist.replace("-", "_")])


def load_symbol_map(*paths: Path) -> dict[str, dict]:
    merged: dict[str, dict] = {}
    for p in paths:
        if p and p.exists():
            merged.update({k: v for k, v in json.loads(p.read_text(encoding="utf-8")).items()
                           if not k.startswith("_")})
    return merged


class _Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.alias: dict[str, str] = {}      # local name -> dotted target
        self.imports: set[str] = set()       # top-level modules imported
        self.uses: list[tuple[str, int]] = []

    def visit_Import(self, node: ast.Import) -> None:
        for a in node.names:
            top = a.name.split(".")[0]
            self.imports.add(top)
            if a.asname:
                self.alias[a.asname] = a.name
            else:
                self.alias[top] = top
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module and node.level == 0:
            self.imports.add(node.module.split(".")[0])
            for a in node.names:
                self.alias[a.asname or a.name] = f"{node.module}.{a.name}"
        self.generic_visit(node)

    def _dotted(self, node: ast.AST) -> str | None:
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name) and node.id in self.alias:
            return ".".join([self.alias[node.id], *reversed(parts)])
        return None

    def visit_Attribute(self, node: ast.Attribute) -> None:
        d = self._dotted(node)
        if d:
            self.uses.append((d, node.lineno))
            return  # don't double-count inner parts of the chain
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Load) and node.id in self.alias:
            self.uses.append((self.alias[node.id], node.lineno))


def scan(src_root: Path) -> tuple[set[str], list[Use]]:
    imports: set[str] = set()
    uses: list[Use] = []
    for f in sorted(src_root.rglob("*.py")):
        if any(p in {".venv", "venv", "node_modules", "tests"} for p in f.parts):
            continue
        try:
            tree = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        except SyntaxError:
            continue
        v = _Visitor()
        v.visit(tree)
        imports |= v.imports
        rel = f.relative_to(src_root).as_posix()
        uses += [Use(s, rel, ln) for s, ln in v.uses]
    return imports, uses


def analyse(findings: list[Finding], src_root: Path, symbol_map: dict[str, dict]) -> list[Verdict]:
    imports, uses = scan(src_root)
    out = []
    for f in findings:
        names = import_names(f.component.name)
        if not any(n in imports for n in names):
            out.append(Verdict(f, NOT_IMPORTED, note=f"no import of {'/'.join(names)} in {src_root.name}/"))
            continue
        entry = next((symbol_map[k] for k in [f.id, *f.aliases] if k in symbol_map), None)
        if not entry:
            out.append(Verdict(f, UNKNOWN, note="no vulnerable-symbol mapping for this advisory yet"))
            continue
        syms = entry["symbols"]
        hits = [u for u in uses if any(u.symbol == s or u.symbol.startswith(s + ".") for s in syms)]
        if hits:
            out.append(Verdict(f, REACHABLE, hits, entry.get("note", "")))
        else:
            out.append(Verdict(f, NOT_CALLED, note=f"none of {', '.join(syms)} referenced"))
    return out
