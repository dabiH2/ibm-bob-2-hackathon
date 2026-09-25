"""CLI: python -m gatekeeper check <project> [--out DIR] [--offline] [--json]

Exit codes: 0 = PASS, 1 = BLOCK, 2 = error. Designed to be called by a
CI job, a git hook, a Bob hook, or `bob run` in headless mode.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__, gate, report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="gatekeeper", description="CRA Article 14 release gate")
    ap.add_argument("--version", action="version", version=__version__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="build the evidence pack and decide PASS/BLOCK")
    c.add_argument("project", type=Path)
    c.add_argument("--out", type=Path, help="evidence pack folder (default <project>/release-evidence)")
    c.add_argument("--offline", action="store_true", help="use cached OSV/KEV data only")
    c.add_argument("--json", action="store_true", help="print gate.json to stdout")
    a = ap.parse_args(argv)
    try:
        out = a.out or a.project / "release-evidence"
        res = gate.run(a.project, out, offline=a.offline)
        page = report.write(res, out, a.project / ".gatekeeper" / "ledger.jsonl")
    except Exception as e:  # noqa: BLE001 - CLI boundary
        print(f"gatekeeper: error: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"GATE {res['gate']}  {res['product']['name']} {res['product']['version']}  "
              f"({res['components']} components, {len(res['findings'])} advisories, "
              f"{res['counts']['affected']} affected, {res['counts']['not_affected']} not affected, "
              f"{res['counts']['under_investigation']} under investigation)")
        for r in res["reasons"]:
            print(f"  - {r}")
        for clk in res["art14"]:
            print(f"  Art.14 {clk['vulnerability']}: early warning {clk['early_warning']['state']} "
                  f"(due {clk['early_warning']['due']}), notification {clk['notification']['state']}, "
                  f"final report {clk['final_report']['state']}")
        print(f"  report: {page}")
    return 0 if res["gate"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
