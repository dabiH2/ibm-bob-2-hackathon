"""Put the demo back in its starting state (vulnerable RC + fresh exploitation signal).

Usage:  python sample-app/demo/reset_demo.py [--hours-ago 3]
"""
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VULNERABLE_REQS = """# fattura-lite 1.4.0 — release candidate
PyYAML==5.3.1
requests==2.19.1
Jinja2==2.10
"""
VULNERABLE_CONFIG = '''"""Load tenant configuration files uploaded by customers."""
import yaml


def load_tenant_config(path):
    with open(path, encoding="utf-8") as fh:
        # Tenant files come from customer uploads, so this input is untrusted.
        return yaml.load(fh, Loader=yaml.FullLoader)
'''


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours-ago", type=float, default=3.0,
                    help="how long ago the manufacturer became aware of exploitation")
    a = ap.parse_args()
    aware = datetime.now(timezone.utc) - timedelta(hours=a.hours_ago)
    (ROOT / "requirements.txt").write_text(VULNERABLE_REQS, encoding="utf-8")
    (ROOT / "app" / "config.py").write_text(VULNERABLE_CONFIG, encoding="utf-8")
    gk = ROOT / ".gatekeeper"
    (gk / "signals.json").write_text(json.dumps({"signals": [{
        "id": "SIG-2026-0001",
        "type": "actively_exploited",
        "vulnerability": "CVE-2020-14343",
        "component": "pyyaml 5.3.1",
        "severity": "CRITICAL (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)",
        "summary": "Arbitrary code execution when untrusted YAML is loaded with FullLoader (PyYAML < 5.4).",
        "aware_at": aware.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "synthetic demo signal: customer SOC reported malicious tenant YAML uploads",
        "member_states": ["IT", "DE", "ES"],
        "sensitivity": "TLP:AMBER until the fix is released",
    }]}, indent=2), encoding="utf-8")
    for f in ("ledger.jsonl", "vex_overrides.json", "symbols.local.json"):
        (gk / f).unlink(missing_ok=True)
    print(f"demo reset: vulnerable RC restored, exploitation signal aware_at={aware:%Y-%m-%d %H:%M} UTC")


if __name__ == "__main__":
    main()
