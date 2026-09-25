# IBM Bob playbook: tasks to run during the hackathon

**Who does what.** The deterministic core (`gatekeeper/`) was written before kickoff as non-AI scaffolding, which lablab allows. Everything in this playbook is the **AI-powered layer** and must be built **in IBM Bob, during the event**, using the hackathon account `ibm-coding-challenge-uat` (us-east).

**Budget.** 40 Bobcoins in total. The plan below uses about 32 and keeps about 8 in reserve.

**Evidence.** After **each** task, open Tasks → task header and screenshot the consumption summary as `bob_sessions/dabii_taskNN_<name>_summary.png`. Also export the task history to `bob_sessions/dabii_taskNN_<name>.md`.

**Format notes (from Bob docs, Sep 2026):**
- **Custom modes:** `.bob/custom_modes.yaml`, key `customModes`, with `slug`, `name`, `roleDefinition`, `whenToUse`, `customInstructions` and `groups`.
- **Skills:** `.bob/skills/<name>/SKILL.md`, with frontmatter `name` and `description`.
- **Rules:** `.bob/rules/*.md` and `.bob/rules-<mode-slug>/*.md`.
- **Hooks:** `.bob/settings.json` → `hooks.PreToolUse[].matcher` / `hooks[].command`. **Exit code 2 blocks.** This format is based on third-party docs, so let Bob check it against its own documentation.

---

## T01 — Read the law, map it to the code (Ask mode, doc understanding, ~2 coins)
Save the CRA PDF from EUR-Lex into `docs/regulation/CRA_2024-2847.pdf` first, then ask Bob:
> Read @docs/regulation/CRA_2024-2847.pdf and the @gatekeeper package. Write `docs/CRA_MAPPING.md`: a table that maps Art. 13(6), 13(8), Art. 14(1)–(2)(a)(b)(c), 14(8), Art. 16 and Annex I Part II (1)–(8) to what Gatekeeper produces (file / field), marking each as covered, partial or not covered. Quote at most one short phrase per article, and give article numbers.

## T02 — Custom mode "CRA Release Officer" (Agent mode, ~3 coins)
> Create `.bob/custom_modes.yaml` with a mode `cra-release-officer`.
> - **Role:** a release manager responsible for CRA compliance of fattura-lite.
> - **Tools:** `read`, `command`, `skill`, and `edit` restricted to `requirements.txt`, `app/**`, `.gatekeeper/*.json` and `release-evidence/**`.
> - **Instructions:**
>   1. Always run `python -m gatekeeper check sample-app --offline` first and read `release-evidence/gate.json`.
>   2. Never mark a vulnerability `not_affected` without an OpenVEX justification, an author and a reason.
>   3. Never submit anything to a CSIRT/ENISA. Only prepare drafts.
>   4. Finish by summarising the gate result and every Art. 14 deadline in UTC.
>
> Also add `.bob/rules-cra-release-officer/01-evidence.md` with those rules.

## T03 — Skills (Agent mode, ~5 coins)
> Create three project skills under `.bob/skills/`:
> 1. **`advisory-analyst`**
>    - Trigger: when gate.json has a finding with reachability `UNKNOWN`.
>    - Read the OSV record in `.gatekeeper/osv-cache/`, identify the vulnerable functions/classes, and search the code for their use.
>    - Write a proposed entry to `.gatekeeper/symbols.local.json` (`{"<CVE>": {"package":..., "symbols":[...], "note":...}}`).
>    - If a VEX override is needed, write one to `.gatekeeper/vex_overrides.json`, including `author: "bob/advisory-analyst"` and `reason`.
>    - Re-run the gate.
> 2. **`art14-drafter`**
>    - Complete every `⟨to complete⟩` in `release-evidence/art14/<signal>/*.md`, using gate.json, the OSV summary, `gatekeeper.toml` and the signal.
>    - Keep it factual and mark anything it cannot know as `⟨needs human input⟩`.
>    - Add a "What users should do" section.
> 3. **`cra-evidence-pack`**
>    - Run the gate, interpret gate.json, and open the HTML report.
>    - List exactly what blocks the release and which skill resolves each item.

## T04 — Hooks: Bob refuses to ship a blocked release (Agent mode, ~3 coins)
> Create `.bob/hooks/release_gate.py`:
> - It reads the hook JSON on stdin.
> - If the tool call is a shell command containing `git push` or `git tag`, it runs `python -m gatekeeper check sample-app --offline`.
> - On BLOCK it prints the reasons to stderr and exits **2**.
> - Otherwise it exits 0.
>
> Register it in `.bob/settings.json` under `hooks.PreToolUse` with a matcher for the command-execution tool. Check the schema against your own documentation before writing it. Add a `Stop` hook that appends one line per finished task to `.gatekeeper/bob_tasks.jsonl` (timestamp, mode, and the result of a final gate run).

## T05 — THE DEMO: prepare release 1.4.1 (mode `cra-release-officer`, parallel subagents, ~8 coins)
Run `python sample-app/demo/reset_demo.py` first, then ask:
> We received signal SIG-2026-0001: CVE-2020-14343 is being actively exploited against fattura-lite. Prepare release 1.4.1. Run three subagents **in parallel**:
> - (a) **remediation:** upgrade the vulnerable dependencies to their fixed versions, replace unsafe YAML loading with `yaml.safe_load`, bump the version to 1.4.1 in `gatekeeper.toml`, and run the tests.
> - (b) **advisory-analyst:** triage any `UNKNOWN` finding.
> - (c) **art14-drafter:** complete the early warning and the vulnerability notification.
>
> When all three are done, re-run the gate and show me the HTML report. Try `git tag v1.4.1` only if the gate passes.

**Record your screen.** This is the 90-second core of the video: BLOCK → three subagents working in parallel → PASS, with the Art. 14 clocks visible.

## T06 — CI (Agent mode, ~3 coins)
First run `gh auth refresh -s workflow` (your gh token lacks the `workflow` scope), then:
> Move `docs/ci/gatekeeper.yml` to `.github/workflows/gatekeeper.yml` and extend it. On a pull request, upload `release-evidence/` as an artifact and post the gate summary as a PR comment. Add an optional job that runs Bob Shell headless (`bob` non-interactive mode, check the flags in the docs) with the `cra-evidence-pack` skill, but only when a `BOB_API_KEY` secret is configured.

## T07 — Lessons Ledger (Agent mode, ~4 coins)
> Create skill `lessons-curator`:
> - It reads `.gatekeeper/ledger.jsonl` and `.gatekeeper/bob_tasks.jsonl`.
> - It finds root causes that recur (for example, unsafe deserialisation, or unpinned or outdated HTTP clients).
> - For each one, it writes or updates a rule in `.bob/rules/20-lessons.md`, citing the ledger runs that justify it.
>
> Then demonstrate it by asking in a new task: "add an endpoint that imports tenant settings from an uploaded YAML file". Bob should use `safe_load` without being told.

## T08 — Submission text (Ask mode, ~2 coins)
> Draft `docs/SUBMISSION.md`: a Problem & Solution statement and an IBM Bob Usage Statement, **each at most 500 words**. Use the numbers from `release-evidence/gate.json` and `.gatekeeper/ledger.jsonl`, and list every Bob feature used, with the matching task numbers in `bob_sessions/`.

---

## Metrics to show (before and after)
| | Manual (typical) | Gatekeeper + Bob |
|---|---|---|
| SBOM + advisory triage for one release | about 1 day | under 1 min (gate) + 1 Bob task |
| False alarms a reviewer has to read | 12 advisories | 5 affected, 7 with a VEX justification |
| Art. 14 deadline tracking | calendar and memory | computed and blocking |
| First drafts of the 3 Art. 14 reports | 2–4 h | generated, then completed by the Bob drafter |

*Measure your own manual baseline once, for example with a stopwatch on T01–T05, and put your real numbers here.*
