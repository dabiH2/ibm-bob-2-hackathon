"""OpenVEX v0.2.0 statements derived from reachability verdicts.

Human or agent overrides (e.g. a Bob subagent that has read the advisory and
the code) live in .gatekeeper/vex_overrides.json and always win over the
automatic statement. Every override must carry an author and a reason.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .reach import NOT_CALLED, NOT_IMPORTED, REACHABLE, UNKNOWN, Verdict

VALID_STATUS = {"not_affected", "affected", "fixed", "under_investigation"}
VALID_JUSTIFICATION = {"component_not_present", "vulnerable_code_not_present",
                       "vulnerable_code_not_in_execute_path",
                       "vulnerable_code_cannot_be_controlled_by_adversary",
                       "inline_mitigations_already_exist"}


def auto_statement(v: Verdict) -> dict:
    f = v.finding
    base = {"vulnerability": {"name": f.id, "aliases": f.aliases},
            "products": [{"@id": f.component.purl}]}
    if v.level == NOT_IMPORTED:
        return {**base, "status": "not_affected", "justification": "vulnerable_code_not_in_execute_path",
                "impact_statement": f"{f.component.name} is declared but never imported by product code ({v.note})."}
    if v.level == NOT_CALLED:
        return {**base, "status": "not_affected", "justification": "vulnerable_code_not_in_execute_path",
                "impact_statement": f"{f.component.name} is imported, but {v.note}."}
    if v.level == REACHABLE:
        where = ", ".join(f"{u.file}:{u.line} ({u.symbol})" for u in v.evidence[:5])
        fix = f"Upgrade {f.component.name} to >= {f.fixed_in[-1]}." if f.fixed_in else "No fixed version published; apply a mitigation."
        return {**base, "status": "affected", "action_statement": fix,
                "impact_statement": f"Vulnerable code referenced at {where}."}
    return {**base, "status": "under_investigation",
            "impact_statement": "Component is imported; advisory not yet mapped to vulnerable symbols."}


def load_overrides(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for key, o in data.items():
        if key.startswith("_"):
            continue
        if o.get("status") not in VALID_STATUS:
            raise ValueError(f"override {key}: invalid status {o.get('status')!r}")
        if o["status"] == "not_affected" and o.get("justification") not in VALID_JUSTIFICATION:
            raise ValueError(f"override {key}: not_affected needs a valid OpenVEX justification")
        if not o.get("author") or not o.get("reason"):
            raise ValueError(f"override {key}: author and reason are required")
        out[key] = o
    return out


def statements(verdicts: list[Verdict], overrides: dict[str, dict]) -> list[dict]:
    result = []
    for v in verdicts:
        s = auto_statement(v)
        key = f"{v.finding.id}@{v.finding.component.name}"
        o = overrides.get(key) or overrides.get(v.finding.id)
        if o:
            s = {k: val for k, val in s.items() if k in ("vulnerability", "products")}
            s.update({k: o[k] for k in ("status", "justification", "impact_statement", "action_statement") if k in o})
            s["status_notes"] = f"override by {o['author']}: {o['reason']}"
        result.append(s)
    return result


def document(stmts: list[dict], author: str) -> dict:
    return {"@context": "https://openvex.dev/ns/v0.2.0",
            "@id": f"https://openvex.dev/docs/public/vex-{uuid.uuid4()}",
            "author": author,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "version": 1,
            "statements": stmts}
