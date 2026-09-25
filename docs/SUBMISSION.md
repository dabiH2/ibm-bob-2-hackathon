# Submission text (lablab form)

**Title:** Article 14 Gatekeeper

**Short description:** A release gate for the EU Cyber Resilience Act. IBM Bob 2.0 agents build the evidence pack, prove which vulnerabilities your code actually reaches, draft the 24 h / 72 h / 14-day reports, and block the release until you're compliant.

**Tags:** IBM Bob, Cyber Resilience Act, DevSecOps, SBOM, VEX, Release Management, Compliance, Agents

## Problem & Solution
Since 11 September 2026, every manufacturer selling software with digital elements in the EU must report actively exploited vulnerabilities under Article 14 of the Cyber Resilience Act. The deadlines are fixed: an early warning within 24 hours, a notification within 72 hours, and a final report within 14 days of a fix being available. Getting it wrong costs up to €15 million or 2.5% of global turnover.

Today this is a manual release chore spread across tools. Someone runs a scanner and gets dozens of advisories. They read each one to guess whether the product is really affected, and paste the findings into a spreadsheet. Then they draft reports in a Word template, while tracking the legal deadlines in a calendar. In our demo product, 12 advisories came back and only 5 touched code the product actually runs. Every false alarm costs reviewer time, and every missed dependency or deadline is a compliance failure.

Article 14 Gatekeeper turns that chore into a release gate:

1. A deterministic core builds a CycloneDX SBOM, pulls advisories from OSV.dev, and merges duplicate GHSA and PYSEC records by CVE.
2. It statically proves reachability, giving file:line evidence for every vulnerable symbol the product uses.
3. It emits OpenVEX: every "not affected" carries a justification.
4. Signals of exploitation, from CISA KEV or the manufacturer's own intake, start the Article 14 clocks and generate draft reports that follow the fields of Art. 14(2).
5. The gate returns PASS or BLOCK as an exit code, so it works in CI, in git hooks and inside the IDE.

IBM Bob 2.0 is the operator. In the custom CRA Release Officer mode, Bob runs three subagents in parallel:
- one fixes the vulnerable code and dependencies,
- one maps advisories nobody has mapped yet to vulnerable symbols and writes a reviewed VEX justification,
- one completes the regulatory drafts.

A Bob hook refuses `git tag` while the gate says BLOCK. A Lessons Ledger records every gate run, and Bob turns causes that recur into rules, so the same class of mistake is not repeated.

**Impact on the demo product:** ⟨fill after T05⟩
- The release went from BLOCK to PASS in ⟨m⟩ minutes.
- Advisories needing human reading dropped from 12 to 5.
- All three Article 14 drafts were produced with deadlines computed to the minute, against ⟨manual baseline⟩ by hand.

**Limits:** Python/pip only; static reachability; the drafts are for a responsible person to submit, not legal advice.

## IBM Bob Usage
IBM Bob 2.0 is the core of the solution, not an add-on. Evidence for every task is in `bob_sessions/`.

- **Document understanding (T01):** Bob read the full Cyber Resilience Act PDF and mapped Articles 13, 14 and 16 and Annex I Part II to what the gate produces, in `docs/CRA_MAPPING.md`.
- **Custom mode (T02):** `cra-release-officer`, with a role definition, restricted edit permissions and mode-specific rules. Examples: never mark "not affected" without a justification and an author; never submit to authorities, only prepare drafts.
- **Skills (T03, T07):**
  - `advisory-analyst` reads an OSV record and the codebase, then proposes vulnerable-symbol mappings and VEX overrides.
  - `art14-drafter` completes the Article 14 report drafts.
  - `cra-evidence-pack` runs and explains the gate.
  - `lessons-curator` turns the gate ledger into Bob rules.
- **Hooks (T04):** a PreToolUse hook blocks `git push` and `git tag` while the gate is BLOCK. A Stop hook logs every Bob task to the ledger.
- **Agent mode with parallel subagents (T05):** remediation, advisory triage and report drafting ran at the same time. Bob then re-ran the gate and tagged the release only after PASS.
- **CI and headless use (T06):** a GitHub Actions workflow runs the gate on every pull request, with an optional headless Bob Shell job.
- **Submission (T08):** Bob drafted this text from `gate.json` and the ledger.

**Budget:** ⟨N⟩ of 40 Bobcoins across ⟨k⟩ tasks.

**Division of labour:** the deterministic core was written before kickoff as non-AI scaffolding. All agent behaviour (mode, skills, hooks and subagent orchestration) was built with Bob during the event.
