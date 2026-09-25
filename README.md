# Article 14 Gatekeeper

**A release gate for the EU Cyber Resilience Act, driven by IBM Bob 2.0 agents.**

Since **11 September 2026**, manufacturers of products with digital elements sold in the EU must report every *actively exploited* vulnerability. The reports go to their CSIRT and to ENISA, on a fixed schedule (Regulation (EU) 2024/2847, Art. 14):

| Report | Deadline |
|---|---|
| Early warning | 24 h after becoming aware |
| Vulnerability notification | 72 h after becoming aware |
| Final report | 14 days after a fix is available |

Most teams today assemble this evidence by hand, across a scanner, a spreadsheet and a Word template. That takes days, and a missed dependency or deadline can cost up to €15M or 2.5% of turnover.

Article 14 Gatekeeper produces the evidence pack for every release candidate and **blocks the release** until the pack is complete:

- **SBOM** in CycloneDX 1.5
- **Vulnerabilities** from OSV.dev, merged across GHSA and PYSEC and keyed by CVE
- **Reachability** that flags only the vulnerable code the product actually uses, with file:line evidence
- **VEX** in OpenVEX v0.2.0, with a justification for every "not affected"
- **Art. 14 clocks** that start from an exploitation signal (a CISA KEV listing or your own intake), with the 24 h / 72 h / 14 d deadlines computed for you
- **Art. 14 drafts**: early warning, notification and final report, following the fields of Art. 14(2)
- **Gate decision** as an exit code (0 = PASS, 1 = BLOCK) and a one-page HTML report
- **Lessons Ledger**: every gate run is logged, and repeat causes become Bob rules

## How IBM Bob runs it
The Python core is deterministic and has no AI. **IBM Bob 2.0 is the operator**:

- **Custom mode:** `cra-release-officer`
- **Skills:**
  - `cra-evidence-pack`
  - `advisory-analyst`, which maps new advisories to vulnerable symbols and proposes VEX with a stated reason
  - `art14-drafter`, which completes the report drafts
  - `lessons-curator`
- **Parallel subagents:** remediation, advisory triage and report drafting run at the same time
- **Document understanding:** Bob reads the regulation PDF to cite articles
- **Hooks:** `git push` / `git tag` is refused while the gate is BLOCK
- **Headless mode:** `bob` runs in CI

See [`docs/BOB_PLAYBOOK.md`](docs/BOB_PLAYBOOK.md) and the evidence in [`bob_sessions/`](bob_sessions/).

## Quick start (no install, Python ≥ 3.11, stdlib only)
```bash
python sample-app/demo/reset_demo.py          # vulnerable RC + exploitation signal 3 h ago
python -m gatekeeper check sample-app --offline
# -> GATE BLOCK: CVE-2020-14343 (pyyaml, CRITICAL, reachable at app/config.py:8), CVE-2018-18074 (requests, HIGH)
#    Art.14 early warning due in ~21 h; report: sample-app/release-evidence/index.html
```
Apply the fix, either by hand or by letting Bob do it (Playbook task T05):
```bash
# requirements.txt: PyYAML==6.0.2, requests==2.33.0 ; app/config.py: yaml.safe_load(fh)
python -m gatekeeper check sample-app --offline
# -> GATE PASS; the final-report clock starts (fix + 14 days); the early warning is still due
```
Drop `--offline` to query OSV.dev and CISA KEV live.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Repository
| Path | What it is |
|---|---|
| `gatekeeper/` | Deterministic core: `sbom`, `osv`, `reach`, `vex`, `art14`, `gate`, `report` |
| `sample-app/` | *fattura-lite*, a fictional e-invoicing microservice used as the demo product |
| `.bob/` | Bob custom mode, skills, hooks and rules (built with Bob during the hackathon) |
| `bob_sessions/` | Required IBM Bob task-summary screenshots |
| `docs/` | Architecture, playbook, CRA mapping |

## Limits
- Covers Python (pip requirements) only.
- Reachability is static and import/symbol-based.
- A dependency that is declared but never imported is treated as not in the execute path.
- The drafts are for a responsible person to complete and submit. They are not legal advice.

## Data and licences
MIT. Vulnerability data comes from OSV.dev (CC-BY 4.0). Exploitation data comes from the CISA KEV catalog. Regulation text comes from EUR-Lex. The demo product and its exploitation signal are synthetic. See [`DATA_SOURCES.md`](DATA_SOURCES.md).
