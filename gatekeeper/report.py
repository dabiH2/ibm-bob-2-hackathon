"""Self-contained HTML evidence report (no network, no external assets)."""
from __future__ import annotations

import html
import json
from pathlib import Path

CSS = """
:root{--bg:#f4f5f7;--card:#fff;--ink:#17202b;--mut:#5d6878;--line:#dce1e8;--pass:#12784a;--passbg:#e2f4ea;
--block:#b3261e;--blockbg:#fbe4e2;--warn:#8a5a00;--warnbg:#fbf0d6;--info:#2d4fbf;--infobg:#e6ecfc}
@media (prefers-color-scheme:dark){:root{--bg:#0f141a;--card:#161d26;--ink:#e3e9f1;--mut:#95a1b2;--line:#27313f;
--pass:#5fcf95;--passbg:#14301f;--block:#f2887f;--blockbg:#3a1916;--warn:#e7b24f;--warnbg:#342711;--info:#8aa4ff;--infobg:#1c2747}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;padding:24px 16px 48px}
.w{max-width:1100px;margin:0 auto;display:flex;flex-direction:column;gap:22px}
h1,h2{margin:0;line-height:1.2}h1{font-size:26px}h2{font-size:17px}
.mono{font-family:ui-monospace,Consolas,monospace;font-size:12.5px}.mut{color:var(--mut)}
.banner{display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;padding:18px 20px;border-radius:12px}
.banner.BLOCK{background:var(--blockbg);color:var(--block)}.banner.PASS{background:var(--passbg);color:var(--pass)}
.banner b{font-size:34px;letter-spacing:.04em}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.kpis>div{background:var(--card);padding:12px 14px}.kpis b{display:block;font-size:22px;font-variant-numeric:tabular-nums}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}
ul.r{margin:6px 0 0;padding-left:18px}
.clocks{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}@media(max-width:720px){.clocks{grid-template-columns:1fr}}
.clk{border:1px solid var(--line);border-radius:10px;padding:12px}.clk .t{font:600 20px/1.2 ui-monospace,Consolas,monospace;font-variant-numeric:tabular-nums;margin-top:4px}
.tb{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}
table{border-collapse:collapse;width:100%;min-width:820px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font:600 11px/1.2 ui-monospace,Consolas,monospace;text-transform:uppercase;letter-spacing:.05em;color:var(--mut)}
tr:last-child td{border-bottom:0}td:first-child{white-space:nowrap}.just{font:11px/1.3 ui-monospace,Consolas,monospace;color:var(--mut);margin-top:3px}
.chip{display:inline-block;font:600 11px/1 ui-monospace,Consolas,monospace;padding:4px 7px;border-radius:99px;white-space:nowrap}
.c-affected,.c-REACHABLE,.c-overdue,.c-CRITICAL,.c-HIGH{background:var(--blockbg);color:var(--block)}
.c-not_affected,.c-NOT_IMPORTED,.c-NOT_CALLED,.c-submitted,.c-fixed{background:var(--passbg);color:var(--pass)}
.c-under_investigation,.c-UNKNOWN,.c-MODERATE,.c-open{background:var(--warnbg);color:var(--warn)}
.c-LOW,.c-waiting_for_fix{background:var(--infobg);color:var(--info)}
.spark{display:flex;gap:4px;align-items:flex-end;height:40px;margin-top:6px}.spark i{display:block;width:14px;border-radius:3px 3px 0 0}
footer{color:var(--mut);font-size:12px}
"""

JS = """
const DATA=JSON.parse(document.getElementById('gk').textContent);
function tick(){document.querySelectorAll('[data-due]').forEach(el=>{const d=Date.parse(el.dataset.due);if(!d)return;
let s=Math.floor((d-Date.now())/1000),neg=s<0;s=Math.abs(s);const h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60;
el.textContent=(neg?'overdue by ':'')+h+'h '+String(m).padStart(2,'0')+'m '+String(x).padStart(2,'0')+'s';});}
tick();setInterval(tick,1000);
"""


def _e(s) -> str:
    return html.escape(str(s if s is not None else ""))


def _iso(due: str) -> str:
    return due[:16].replace(" ", "T") + ":00Z" if due != "pending" else ""


def render(result: dict, ledger: list[dict]) -> str:
    g = result["gate"]
    p = result["product"]
    c = result["counts"]
    reasons = "".join(f"<li>{_e(r)}</li>" for r in result["reasons"]) or "<li>No blocking issues.</li>"
    clocks = ""
    for a in result["art14"]:
        cells = ""
        for k, label in (("early_warning", "Early warning · 24 h"), ("notification", "Notification · 72 h"),
                         ("final_report", "Final report · fix + 14 d")):
            st = a[k]
            live = f'<div class="t" data-due="{_e(_iso(st["due"]))}">{_e(st["due"])}</div>' if st["state"] == "open" else \
                f'<div class="t">{_e(st.get("at", st["due"]))}</div>'
            cells += (f'<div class="clk"><div class="mut">{label}</div>{live}'
                      f'<div class="mut mono">due {_e(st["due"])}</div> <span class="chip c-{_e(st["state"])}">{_e(st["state"])}</span></div>')
        clocks += (f'<div class="card"><h2>Art. 14 clock · {_e(a["vulnerability"])}</h2>'
                   f'<p class="mut">Signal {_e(a["signal"])} · source: {_e(a["source"])} · drafts in <span class="mono">art14/{_e(a["signal"])}/</span></p>'
                   f'<div class="clocks">{cells}</div></div>')
    if not clocks:
        clocks = '<div class="card"><h2>Art. 14 clocks</h2><p class="mut">No actively exploited vulnerability signalled.</p></div>'
    rows = ""
    for f in result["findings"]:
        ev = "<br>".join(_e(x) for x in f["evidence"]) or '<span class="mut">—</span>'
        rows += (f'<tr><td class="mono">{_e(f["id"])}</td><td>{_e(f["package"])} <span class="mono mut">{_e(f["version"])}</span></td>'
                 f'<td><span class="chip c-{_e(f["severity"])}">{_e(f["severity"])}</span></td>'
                 f'<td><span class="chip c-{_e(f["reachability"])}">{_e(f["reachability"])}</span></td>'
                 f'<td class="mono">{ev}</td>'
                 f'<td><span class="chip c-{_e(f["vex_status"])}">{_e(f["vex_status"])}</span>'
                 f'{"<div class=just>" + _e(f["justification"].replace("_", " ")) + "</div>" if f["justification"] else ""}</td>'
                 f'<td class="mono">{_e(", ".join(f["fixed_in"][-1:]))}</td><td>{_e(f["summary"])}</td></tr>')
    hist = ledger[-20:]
    top = max([len(h.get("reasons", [])) for h in hist] + [1])
    spark = "".join(
        f'<i title="{_e(h["ts"])} {_e(h["gate"])} ({len(h.get("reasons", []))} blocking)" '
        f'style="height:{6 + 34 * len(h.get("reasons", [])) / top:.0f}px;background:var(--{"block" if h["gate"] == "BLOCK" else "pass"})"></i>'
        for h in hist)
    payload = json.dumps(result).replace("</", "<\\/")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gatekeeper · {_e(p.get('name'))} {_e(p.get('version'))}</title><style>{CSS}</style></head><body><div class="w">
<header><div class="mut mono">ARTICLE 14 GATEKEEPER · CRA (EU) 2024/2847 release evidence</div>
<h1>{_e(p.get('name'))} {_e(p.get('version'))}</h1><div class="mut">Manufacturer: {_e(p.get('manufacturer'))} · checked {_e(result['checked_at'])}{' · offline cache' if result['offline'] else ''}</div></header>
<div class="banner {g}"><div><b>{g}</b><div>{'Release blocked until the items below are resolved.' if g == 'BLOCK' else 'Evidence pack complete for this release.'}</div></div>
<div><div class="mut" style="color:inherit">Blocking reasons</div><ul class="r">{reasons}</ul></div></div>
<div class="kpis"><div><span class="mut">Components</span><b>{result['components']}</b></div>
<div><span class="mut">Advisories</span><b>{len(result['findings'])}</b></div>
<div><span class="mut">Affected</span><b>{c['affected']}</b></div>
<div><span class="mut">Not affected (VEX)</span><b>{c['not_affected']}</b></div>
<div><span class="mut">Under investigation</span><b>{c['under_investigation']}</b></div>
<div><span class="mut">Gate history</span><div class="spark">{spark}</div></div></div>
{clocks}
<div><h2 style="margin-bottom:8px">Advisories, reachability and VEX</h2><div class="tb"><table>
<thead><tr><th>Advisory</th><th>Component</th><th>Severity</th><th>Reachability</th><th>Evidence</th><th>VEX</th><th>Fixed in</th><th>Summary</th></tr></thead>
<tbody>{rows or '<tr><td colspan=8 class=mut>No known vulnerabilities in the SBOM.</td></tr>'}</tbody></table></div></div>
<div class="card"><h2>Evidence pack</h2><p class="mono">sbom.cdx.json · vex.openvex.json · gate.json · art14/&lt;signal&gt;/(early_warning|notification|final_report).md</p>
<p class="mut">Drafts for a responsible person to complete and submit via the CRA single reporting platform. Not legal advice. Vulnerability data: OSV.dev (CC-BY 4.0); exploitation data: CISA KEV.</p></div>
<footer>Generated by article14-gatekeeper · deterministic core, driven by IBM Bob agents</footer></div>
<script type="application/json" id="gk">{payload}</script><script>{JS}</script></body></html>"""


def write(result: dict, out: Path, ledger_file: Path) -> Path:
    ledger = [json.loads(l) for l in ledger_file.read_text(encoding="utf-8").splitlines() if l.strip()] \
        if ledger_file.exists() else []
    f = out / "index.html"
    f.write_text(render(result, ledger), encoding="utf-8")
    return f
