---
name: cra-evidence-pack
description: Use when asked whether a release can ship — runs the gate, reads gate.json, summarises PASS or BLOCK with blocking reasons, lists Art. 14 deadlines, and names the skill that resolves each open item.
---

# CRA Evidence Pack

Activate when the user asks whether a release is shippable, requests a release readiness summary,
or wants a CRA evidence overview.

## Steps

1. **Run the gate.**
   Execute: `python -m gatekeeper check sample-app --offline`
   Capture exit code and stdout.

2. **Read gate.json.**
   Open `sample-app/release-evidence/gate.json`. Identify:
   - Overall verdict (`PASS` or `BLOCK`)
   - Every blocking finding: CVE/GHSA id, package, severity, reachability, vex_status

3. **Summarise verdict.**
   Report the verdict in one line, then a table of all blocking findings:

   | CVE / GHSA | Package | Severity | Reachability | VEX Status | Resolves with |
   |---|---|---|---|---|---|

   In the "Resolves with" column, write:
   - `advisory-analyst` — if `reachability` is `UNKNOWN` or `vex_status` is `under_investigation`
   - `art14-drafter` — if an Art. 14 report draft exists under `release-evidence/art14/`
   - `manual review` — for anything else

4. **List Art. 14 deadlines.**
   Read `sample-app/.gatekeeper/signals.json`. For every signal with a deadline field, output:

   | Signal | Deadline (UTC) | Hours left | Report type |
   |---|---|---|---|

   Compute hours left relative to the current UTC time. Mark overdue deadlines as **OVERDUE**.

5. **Gate status line.**
   End with one of:
   - ✅ **PASS — release may ship** (if gate passed and no overdue Art. 14 items exist)
   - 🚫 **BLOCK — do not ship** (if gate blocks or any deadline is overdue), listing each blocker
     and the skill that resolves it.
