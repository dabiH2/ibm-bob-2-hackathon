# Submission text (lablab form)

**Title:** Article 14 Gatekeeper

**Short description:** A release gate for the EU Cyber Resilience Act. IBM Bob 2.0 agents build the evidence pack, prove which vulnerabilities your code actually reaches, draft the 24 h / 72 h / 14-day reports, and block the release until you're compliant.

**Tags:** IBM Bob, Cyber Resilience Act, DevSecOps, SBOM, VEX, Release Management, Compliance, Agents

## Problem & Solution
Since 11 September 2026, every manufacturer selling software with digital elements in the EU must report actively exploited vulnerabilities under Article 14 of the Cyber Resilience Act. The deadlines are fixed: an early warning within 24 hours, a notification within 72 hours, and a final report within 14 days of a fix being available. Getting it wrong costs up to €15 million or 2.5% of global turnover.

Today this is a manual release chore spread across tools. Someone runs a scanner and gets dozens of advisories. They read each one to guess whether the product is really affected, and paste the findings into a spreadsheet. Then they draft reports in a Word template, while tracking the legal deadlines in a calendar. In our demo product (fattura-lite), 12 advisories came back before the fix and 5 touched code the product actually runs — both CVE-2020-14343 (CRITICAL, pyyaml 5.3.1, reachable at `config.py:8`) and CVE-2018-18074 (HIGH, requests 2.19.1, reachable at `gateway_client.py:9`) were blocking. Every false alarm costs reviewer time, and every missed dependency or deadline is a compliance failure.

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

**Impact on the demo product:**
- The release went from BLOCK to PASS: before the fix, 5 advisories were affected and the gate was BLOCK; after, the gate reports 6 advisories and 0 affected (gate: PASS, checked 2026-09-25T18:20:47Z).
- Time to resolution: about 5 minutes from Bob's first gate run to PASS and the release tag (timed second run, `bob_sessions/dabii_task05c_timed_take2.md`).
- Both due Article 14 drafts (early warning and notification) were completed with deadlines computed to the minute, and the 14-day final-report clock started at the fix. By hand, all 12 advisories must be read and every report typed.

**Limits:** Python/pip only; static reachability; the drafts are for a responsible person to submit, not legal advice.

## IBM Bob Usage
IBM Bob 2.0 is the core of the solution, not an add-on. Evidence for every task is in `bob_sessions/`.

- **Document understanding (T01 — `dabii_task01_cra_mapping.md`):** Bob read the full Cyber Resilience Act PDF and mapped Articles 13, 14 and 16 and Annex I Part II to what the gate produces, in `docs/CRA_MAPPING.md`.
- **Custom mode (T02 — `dabii_task02_mode_and_hooks.md`):** `cra-release-officer`, with a role definition, restricted edit permissions and mode-specific rules. Examples: never mark "not affected" without a justification and an author; never submit to authorities, only prepare drafts.
- **Skills (T03 — `dabii_task03_skills.md`; T07 — `dabii_task07_lessons_curator.md`):**
  - `advisory-analyst` reads an OSV record and the codebase, then proposes vulnerable-symbol mappings and VEX overrides.
  - `art14-drafter` completes the Article 14 report drafts.
  - `cra-evidence-pack` runs and explains the gate.
  - `lessons-curator` turns the gate ledger into Bob rules (T07).
- **Hooks — PreToolUse and Stop (T02 + T04 — `dabii_task02_mode_and_hooks.md`):** a PreToolUse hook blocks `git push` and `git tag` while the gate is BLOCK. A Stop hook logs every Bob task to the ledger.
- **Hook demo (T04b — `dabii_task04b_hook_blocks_tag.md`):** Bob was asked to run `git tag v1.4.2-rc` directly with the gate in BLOCK state. First the mode rules refused; then the PreToolUse hook blocked the command independently, printing the CVE list to stderr and exiting with code 2 — proving two independent layers of defence.
- **Agent mode with parallel subagents (T05 — `dabii_task05_release_1-4-1.md`):** remediation, advisory triage and report drafting ran at the same time. Bob then re-ran the gate and tagged the release only after PASS.
- **Draft-overwrite bug found and fixed (T05b — `dabii_task05b_draft_fix.md`):** after the art14-drafter completed `early_warning.md`, a subsequent gate run silently overwrote the completed draft with the empty scaffold. Bob identified the root cause in `gatekeeper/gate.py`, applied a guard (`if not path.exists()`), added a regression test, and re-completed the drafts — all in one session.
- **CI and headless use (T06 — `dabii_task06_ci_headless.md`):** a GitHub Actions workflow runs the gate on every pull request, with an optional headless Bob Shell job. A human review caught three workflow bugs in Bob's draft (a `secrets` context in a job-level `if`, a missing `contents: read`, a wrong `gate.json` key), which were fixed before merging.
- **safe_load applied unprompted (T07b — `dabii_task07b_safe_load_demo.md`):** Bob was asked to add a new YAML-import endpoint without any security constraints in the prompt. It applied `yaml.safe_load()` without being asked, citing the workspace lesson learned from CVE-2020-14343 — the rule written by the `lessons-curator` in T07.

- **Submission (T08 — `dabii_task08_submission_text.md`):** Bob drafted this text from `gate.json`, the gate ledger and the task exports in `bob_sessions/`.

**Budget:** 11.38 of 40 Bobcoins across 11 tasks.

**Division of labour:** the deterministic core was written before kickoff as non-AI scaffolding. All agent behaviour (mode, skills, hooks and subagent orchestration) was built with Bob during the event.
