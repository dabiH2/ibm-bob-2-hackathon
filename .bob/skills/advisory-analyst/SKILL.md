---
name: advisory-analyst
description: Use when sample-app/release-evidence/gate.json contains a finding with reachability UNKNOWN or vex_status under_investigation — analyses the OSV advisory, searches call sites, and writes symbol or VEX overrides.
---

# Advisory Analyst

## Steps

1. **Read `gate.json`.**
   Open `sample-app/release-evidence/gate.json`; note each CVE/GHSA id and package for findings
   where `reachability` is `UNKNOWN` or `vex_status` is `under_investigation`.

2. **Read the OSV record.**
   Open `sample-app/.gatekeeper/osv-cache/<package>-<version>.json` (one file per component; find the record whose `id` or `aliases` match). Extract `summary`, `affected[].ranges`,
   `affected[].ecosystem_specific.imports`, and `references` patch/advisory URLs.

3. **Identify vulnerable symbols.**
   From the advisory and references, list the specific functions, classes, or module paths that are
   vulnerable (e.g. `deserialize`, `parse`, `load`).

4. **Search the application source.**
   Use `grep` to search `sample-app/app/` for each symbol. Record every file and line number that
   imports or calls it.

5. **Write the symbols entry.**
   Merge into `sample-app/.gatekeeper/symbols.local.json` (preserve existing keys):
   ```json
   {"<id>": {"package": "<ecosystem>:<name>", "symbols": ["<sym>"], "note": "<rationale>"}}
   ```

6. **VEX override (only if conclusive).**
   Only if steps 3–4 prove the symbol is unreachable or the fix is already applied, append to
   `sample-app/.gatekeeper/vex_overrides.json`:
   ```json
   {"<id>": {"status": "not_affected", "justification": "<OpenVEX string>",
             "author": "bob/advisory-analyst", "reason": "<evidence>"}}
   ```

7. **Re-run the gate.**
   Execute: `python -m gatekeeper check sample-app --offline`
   Report the new verdict, updated `reachability`, and any remaining open findings.
