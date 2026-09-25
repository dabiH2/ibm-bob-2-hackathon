"""Run the full pipeline and decide PASS / BLOCK for a release candidate."""
from __future__ import annotations

import json
import tomllib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from . import art14, osv, reach, sbom, vex

PKG_DATA = Path(__file__).parent / "data"
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
SEV_ORDER = ["LOW", "MODERATE", "HIGH", "CRITICAL"]

DEFAULT_POLICY = {"block_severity": "HIGH", "block_under_investigation": True,
                  "block_unpinned": True, "block_overdue_art14": True}


def load_config(project: Path) -> dict:
    cfg_file = project / "gatekeeper.toml"
    cfg = tomllib.loads(cfg_file.read_text(encoding="utf-8")) if cfg_file.exists() else {}
    cfg.setdefault("product", {"name": project.name, "version": "0.0.0", "manufacturer": "unknown"})
    cfg.setdefault("scan", {})
    cfg["scan"].setdefault("requirements", "requirements.txt")
    cfg["scan"].setdefault("source", ".")
    cfg["policy"] = {**DEFAULT_POLICY, **cfg.get("policy", {})}
    return cfg


def _kev(project: Path, offline: bool) -> dict:
    local = project / ".gatekeeper" / "kev.json"
    if not offline:
        try:
            with urllib.request.urlopen(KEV_URL, timeout=30) as r:
                data = json.load(r)
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_text(json.dumps(data), encoding="utf-8")
            return data
        except OSError:
            pass
    if local.exists():
        return json.loads(local.read_text(encoding="utf-8"))
    return {"vulnerabilities": []}


def run(project: Path, out: Path, offline: bool = False, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    cfg = load_config(project)
    pol, product = cfg["policy"], cfg["product"]
    gk = project / ".gatekeeper"
    out.mkdir(parents=True, exist_ok=True)

    # 1. SBOM
    comps, unpinned = sbom.parse_requirements(project / cfg["scan"]["requirements"])
    bom = sbom.cyclonedx(comps, product)
    sbom.write(bom, out / "sbom.cdx.json")

    # 2. Vulnerabilities
    raw = osv.fetch(comps, gk / "osv-cache", offline)
    finds = osv.findings(raw)

    # 3. Reachability
    symbols = reach.load_symbol_map(PKG_DATA / "vuln_symbols.json", gk / "symbols.local.json")
    verdicts = reach.analyse(finds, project / cfg["scan"]["source"], symbols)

    # 4. Exploitation signals + Art. 14 clocks
    signals = art14.load_signals(gk / "signals.json") + art14.kev_signals(finds, _kev(project, offline), now)
    current_ids = {f.id for f in finds} | {a for f in finds for a in f.aliases}
    fixed_ids = {s["vulnerability"] for s in signals if s["vulnerability"] not in current_ids}
    clocks = art14.clocks(signals, fixed_ids, now)

    # 5. VEX (automatic + reviewed overrides), plus "fixed" for signalled vulns no longer present
    stmts = vex.statements(verdicts, vex.load_overrides(gk / "vex_overrides.json"))
    for vid in sorted(fixed_ids):
        stmts.append({"vulnerability": {"name": vid}, "products": [{"@id": f"pkg:generic/{product['name']}@{product['version']}"}],
                      "status": "fixed", "impact_statement": "Vulnerable component version no longer present in this release."})
    (out / "vex.openvex.json").write_text(json.dumps(vex.document(stmts, product.get("manufacturer", "unknown")), indent=2), encoding="utf-8")

    # 6. Art. 14 drafts
    by_id = {f.id: f for f in finds}
    art_dir = out / "art14"
    clock_rows = []
    for c in clocks:
        d = art_dir / c.signal["id"]
        d.mkdir(parents=True, exist_ok=True)
        for name, text in art14.drafts(c, by_id.get(c.signal["vulnerability"]), product).items():
            draft_path = d / f"{name}.md"
            if not draft_path.exists():
                draft_path.write_text(text, encoding="utf-8")
        clock_rows.append({"signal": c.signal["id"], "vulnerability": c.signal["vulnerability"],
                           "source": c.signal.get("source"), **c.status(now)})

    # 7. Decision
    threshold = SEV_ORDER.index(pol["block_severity"].upper())
    reasons = []
    status_of = {(s["vulnerability"]["name"], s["products"][0]["@id"]): s for s in stmts}
    rows = []
    for v in verdicts:
        s = status_of[(v.finding.id, v.finding.component.purl)]
        sev_i = SEV_ORDER.index(v.finding.severity) if v.finding.severity in SEV_ORDER else threshold
        blocking = (s["status"] == "affected" and sev_i >= threshold) or \
                   (s["status"] == "under_investigation" and pol["block_under_investigation"])
        if blocking:
            reasons.append(f"{v.finding.id} in {v.finding.component.name} {v.finding.component.version}: "
                           f"{s['status']} ({v.finding.severity})")
        rows.append({"id": v.finding.id, "aliases": v.finding.aliases, "package": v.finding.component.name,
                     "version": v.finding.component.version, "severity": v.finding.severity,
                     "summary": v.finding.summary, "fixed_in": v.finding.fixed_in, "reachability": v.level,
                     "evidence": [f"{u.file}:{u.line} {u.symbol}" for u in v.evidence[:5]],
                     "vex_status": s["status"], "justification": s.get("justification"),
                     "blocking": blocking})
    if unpinned and pol["block_unpinned"]:
        reasons += [f"SBOM: {w}" for w in unpinned]
    for c in clock_rows:
        for k in ("early_warning", "notification", "final_report"):
            if c[k]["state"] == "overdue" and pol["block_overdue_art14"]:
                reasons.append(f"Art. 14 {k.replace('_', ' ')} for {c['vulnerability']} is overdue")

    result = {"gate": "BLOCK" if reasons else "PASS", "checked_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
              "product": product, "components": len(comps), "findings": rows, "reasons": reasons,
              "art14": clock_rows, "warnings": unpinned, "offline": offline,
              "counts": {k: sum(1 for r in rows if r["vex_status"] == k)
                         for k in ("affected", "not_affected", "under_investigation")}}
    (out / "gate.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    # 8. Lessons Ledger: one line per run, so trends and repeat offenders are visible
    gk.mkdir(exist_ok=True)
    with (gk / "ledger.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": result["checked_at"], "gate": result["gate"], "version": product.get("version"),
                             "reasons": reasons, "counts": result["counts"]}) + "\n")
    return result
