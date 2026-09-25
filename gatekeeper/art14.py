"""CRA Article 14 reporting clocks and report scaffolds.

Regulation (EU) 2024/2847, Art. 14 (applies from 11 September 2026): for an
actively exploited vulnerability the manufacturer notifies the CSIRT
designated as coordinator and ENISA, through the single reporting platform:
  (a) an early warning within 24 hours of becoming aware,
  (b) a vulnerability notification within 72 hours of becoming aware,
  (c) a final report no later than 14 days after a corrective or mitigating
      measure is available.
The scaffolds below lay out the fields Art. 14(2) asks for. They are drafts
for a responsible person to complete and submit; they are not legal advice.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

TODO = "⟨to complete⟩"


def _ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def _fmt(d: datetime | None) -> str:
    return d.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC") if d else "pending"


@dataclass
class Clock:
    signal: dict
    aware_at: datetime
    fix_available_at: datetime | None

    @property
    def early_warning_due(self) -> datetime:
        return self.aware_at + timedelta(hours=24)

    @property
    def notification_due(self) -> datetime:
        return self.aware_at + timedelta(hours=72)

    @property
    def final_report_due(self) -> datetime | None:
        return self.fix_available_at + timedelta(days=14) if self.fix_available_at else None

    def status(self, now: datetime) -> dict:
        sub = self.signal.get("submitted", {})

        def st(name: str, due: datetime | None) -> dict:
            if sub.get(name):
                return {"due": _fmt(due), "state": "submitted", "at": sub[name]}
            if due is None:
                return {"due": "pending", "state": "waiting_for_fix"}
            left = (due - now).total_seconds() / 3600
            return {"due": _fmt(due), "state": "overdue" if left < 0 else "open", "hours_left": round(left, 1)}

        return {"early_warning": st("early_warning", self.early_warning_due),
                "notification": st("notification", self.notification_due),
                "final_report": st("final_report", self.final_report_due)}


def load_signals(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [s for s in json.loads(path.read_text(encoding="utf-8")).get("signals", [])
            if s.get("type") == "actively_exploited"]


def kev_signals(findings, kev: dict, now: datetime) -> list[dict]:
    """A CISA KEV listing counts as awareness of active exploitation."""
    kev_ids = {v["cveID"]: v for v in kev.get("vulnerabilities", [])}
    out = []
    for f in findings:
        for i in [f.id, *f.aliases]:
            if i in kev_ids:
                out.append({"id": f"KEV-{i}", "type": "actively_exploited", "vulnerability": f.id,
                            "aware_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "source": f"CISA KEV (added {kev_ids[i].get('dateAdded')})"})
                break
    return out


def clocks(signals: list[dict], fixed_ids: set[str], release_time: datetime) -> list[Clock]:
    out = []
    for s in signals:
        fix = s.get("fix_available_at")
        fix_at = _ts(fix) if fix else (release_time if s["vulnerability"] in fixed_ids else None)
        out.append(Clock(s, _ts(s["aware_at"]), fix_at))
    return out


def drafts(clock: Clock, finding, product: dict) -> dict[str, str]:
    s = clock.signal
    ms = ", ".join(s.get("member_states", [])) or TODO
    head = (f"Product: {product.get('name')} {product.get('version')} — manufacturer: {product.get('manufacturer')}\n"
            f"Vulnerability: {s['vulnerability']}" + (f" ({', '.join(finding.aliases[:3])})" if finding else "") + "\n"
            f"Aware of active exploitation since: {_fmt(clock.aware_at)} (signal {s['id']}, source: {s.get('source', TODO)})\n"
            f"Recipients: CSIRT designated as coordinator + ENISA, via the single reporting platform (Art. 16)\n")
    sev = f"{finding.severity} ({finding.cvss})" if finding else s.get("severity", TODO)
    comp = f"{finding.component.name} {finding.component.version}" if finding else s.get("component", TODO)
    fixv = (f"upgrade {finding.component.name} to >= {finding.fixed_in[-1]}" if finding and finding.fixed_in
            else s.get("corrective_measure", "vulnerable version removed in this release" if clock.fix_available_at else TODO))
    return {
        "early_warning": (
            f"# Early warning — Art. 14(2)(a) — due {_fmt(clock.early_warning_due)}\n\n{head}\n"
            f"## Member States where the product has been made available\n{ms}\n\n"
            f"## Short description\nActive exploitation of {s['vulnerability']} in component {comp}. {TODO}\n"),
        "notification": (
            f"# Vulnerability notification — Art. 14(2)(b) — due {_fmt(clock.notification_due)}\n\n{head}\n"
            f"## General information about the product concerned\n{product.get('description', TODO)}\n\n"
            f"## General nature of the exploit and of the vulnerability\n{(finding.summary if finding else s.get('summary', TODO))}\n"
            f"Severity: {sev}\n\n"
            f"## Corrective or mitigating measures taken\n{fixv}. {TODO}\n\n"
            f"## Corrective or mitigating measures users can take\n{TODO}\n\n"
            f"## Sensitivity of the notified information\n{s.get('sensitivity', TODO)}\n"),
        "final_report": (
            f"# Final report — Art. 14(2)(c) — due {_fmt(clock.final_report_due)}\n\n{head}\n"
            f"## (i) Description of the vulnerability, including severity and impact\n"
            f"{(finding.summary if finding else s.get('summary', TODO))} Severity: {sev}. Impact: {TODO}\n\n"
            f"## (ii) Information on the malicious actor, where available\n{s.get('actor', TODO)}\n\n"
            f"## (iii) Security update or other corrective measures made available\n{fixv}; "
            f"corrective measure available since {_fmt(clock.fix_available_at)}.\n\n"
            f"## Users informed (Art. 14(8))\n{TODO}\n"),
    }
