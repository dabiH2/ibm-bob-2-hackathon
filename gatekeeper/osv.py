"""Vulnerability lookup against OSV.dev, with an offline cache.

OSV data is licensed CC-BY 4.0 (https://osv.dev). GHSA and PYSEC records
describing the same issue are merged into one finding keyed by CVE.
"""
from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from .sbom import Component

OSV_BATCH = "https://api.osv.dev/v1/querybatch"
OSV_VULN = "https://api.osv.dev/v1/vulns/{id}"
_SEV_RANK = {"LOW": 1, "MODERATE": 2, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


@dataclass
class Finding:
    id: str                     # primary id (CVE if known)
    aliases: list[str]
    component: Component
    severity: str               # LOW / MODERATE / HIGH / CRITICAL / UNKNOWN
    summary: str
    fixed_in: list[str]
    cvss: str | None
    references: list[str] = field(default_factory=list)

    @property
    def rank(self) -> int:
        return _SEV_RANK.get(self.severity, 0)


def _post(url: str, payload: dict, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def _get(url: str, timeout: int = 30) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.load(r)


def _cache_file(cache: Path, c: Component) -> Path:
    return cache / f"{c.name}-{c.version}.json"


def fetch(components: list[Component], cache: Path, offline: bool) -> dict[Component, list[dict]]:
    """Return raw OSV records per component. Online results refresh the cache."""
    cache.mkdir(parents=True, exist_ok=True)
    out: dict[Component, list[dict]] = {}
    missing = []
    for c in components:
        f = _cache_file(cache, c)
        if offline:
            if not f.exists():
                raise FileNotFoundError(f"offline mode: no cached OSV data for {c.purl} ({f})")
            out[c] = json.loads(f.read_text(encoding="utf-8"))["vulns"]
        else:
            missing.append(c)
    if missing:
        res = _post(OSV_BATCH, {"queries": [
            {"package": {"name": c.name, "ecosystem": c.ecosystem}, "version": c.version} for c in missing]})
        for c, r in zip(missing, res["results"]):
            full = [_get(OSV_VULN.format(id=v["id"])) for v in r.get("vulns", [])]
            _cache_file(cache, c).write_text(json.dumps(
                {"package": c.name, "version": c.version, "ecosystem": c.ecosystem, "vulns": full}, indent=1),
                encoding="utf-8")
            out[c] = full
    return out


def _cvss_sev(vector: str) -> str:
    """Rough CVSS v3 base-severity bucket when the record has no label."""
    m = dict(p.split(":") for p in vector.split("/")[1:] if ":" in p)
    impact = sum({"H": 2, "L": 1}.get(m.get(k, "N"), 0) for k in ("C", "I", "A"))
    if m.get("AV") == "N" and m.get("AC") == "L" and m.get("PR") == "N" and impact >= 4:
        return "CRITICAL"
    return "HIGH" if impact >= 4 else "MODERATE" if impact >= 2 else "LOW"


def findings(raw: dict[Component, list[dict]]) -> list[Finding]:
    result: list[Finding] = []
    for comp, vulns in raw.items():
        groups: dict[str, list[dict]] = {}
        for v in vulns:
            ids = {v["id"], *v.get("aliases", [])}
            cve = sorted(i for i in ids if i.startswith("CVE-"))
            key = cve[0] if cve else v["id"]
            groups.setdefault(key, []).append(v)
        for key, recs in groups.items():
            aliases = sorted({i for r in recs for i in [r["id"], *r.get("aliases", [])]} - {key})
            sev = next((r.get("database_specific", {}).get("severity") for r in recs
                        if r.get("database_specific", {}).get("severity")), None)
            vec = next((s["score"] for r in recs for s in r.get("severity", []) if s.get("type", "").startswith("CVSS_V3")), None)
            if not sev:
                sev = _cvss_sev(vec) if vec else "UNKNOWN"
            fixed = sorted({e["fixed"] for r in recs for a in r.get("affected", [])
                            for rg in a.get("ranges", []) if rg.get("type") == "ECOSYSTEM"
                            for e in rg.get("events", []) if "fixed" in e})
            summary = next((r.get("summary") for r in recs if r.get("summary")), "") or \
                re.sub(r"\s+", " ", recs[0].get("details", ""))[:160]
            refs = [x["url"] for r in recs for x in r.get("references", [])[:3]]
            result.append(Finding(key, aliases, comp, sev.upper(), summary, fixed, vec, refs[:5]))
    result.sort(key=lambda f: (-f.rank, f.component.name, f.id))
    return result
