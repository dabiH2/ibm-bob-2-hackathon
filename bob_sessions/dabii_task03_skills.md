# Create three IBM Bob project skills under .bob/skills/, each a folder with a SKILL.md that has YAML front matter (name, description) followed by step-by-step instructions, following the IBM Bob skills documentation. 1) advisory-analyst: use when sample-app/release-evidence/gate.json contains a finding with reachability UNKNOWN or vex_status under_investigation. Steps: read the matching OSV record in sample-app/.gatekeeper/osv-cache/, identify the vulnerable functions or classes from the advisory text and references, search sample-app/app/ for their use, then write a proposed entry to sample-app/.gatekeeper/symbols.local.json in the format {"<CVE>": {"package": ..., "symbols": [...], "note": ...}}; only if a VEX override is really needed write it to sample-app/.gatekeeper/vex_overrides.json with status, a valid OpenVEX justification, author "bob/advisory-analyst" and reason; finally re-run python -m gatekeeper check sample-app --offline and report the new verdict. 2) art14-drafter: use after a gate run that produced files in sample-app/release-evidence/art14/<signal>/. Steps: complete every placeholder marked with the angle-bracket 'to complete' text in early_warning.md, notification.md and final_report.md using gate.json, the OSV summary, sample-app/gatekeeper.toml and sample-app/.gatekeeper/signals.json; write factually, mark anything unknowable as 'needs human input'; add a 'What users should do' section; never mark anything as submitted. 3) cra-evidence-pack: use when asked whether a release can ship. Steps: run the gate, read gate.json, summarise PASS or BLOCK with each blocking reason, list every Art. 14 deadline in UTC with hours left, and name which skill (advisory-analyst or art14-drafter) resolves each open item. Keep each SKILL.md under 60 lines. After creating them, list the three skills and confirm they are detected.

---

**Status:** active  **Date:** 2026-09-25

---

### 👤 User

Create three IBM Bob project skills under .bob/skills/, each a folder with a SKILL.md that has YAML front matter (name, description) followed by step-by-step instructions, following the IBM Bob skills documentation. 1) advisory-analyst: use when sample-app/release-evidence/gate.json contains a finding with reachability UNKNOWN or vex_status under_investigation. Steps: read the matching OSV record in sample-app/.gatekeeper/osv-cache/, identify the vulnerable functions or classes from the advisory text and references, search sample-app/app/ for their use, then write a proposed entry to sample-app/.gatekeeper/symbols.local.json in the format {"<CVE>": {"package": ..., "symbols": [...], "note": ...}}; only if a VEX override is really needed write it to sample-app/.gatekeeper/vex_overrides.json with status, a valid OpenVEX justification, author "bob/advisory-analyst" and reason; finally re-run python -m gatekeeper check sample-app --offline and report the new verdict. 2) art14-drafter: use after a gate run that produced files in sample-app/release-evidence/art14/<signal>/. Steps: complete every placeholder marked with the angle-bracket 'to complete' text in early_warning.md, notification.md and final_report.md using gate.json, the OSV summary, sample-app/gatekeeper.toml and sample-app/.gatekeeper/signals.json; write factually, mark anything unknowable as 'needs human input'; add a 'What users should do' section; never mark anything as submitted. 3) cra-evidence-pack: use when asked whether a release can ship. Steps: run the gate, read gate.json, summarise PASS or BLOCK with each blocking reason, list every Art. 14 deadline in UTC with hours left, and name which skill (advisory-analyst or art14-drafter) resolves each open item. Keep each SKILL.md under 60 lines. After creating them, list the three skills and confirm they are detected.

---

### 🤖 Assistant

> 🔧 called: use_skill, list_files



> 🔧 **use_skill** — create-skill

> 🔧 **list_files** — .bob

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — [-] Create .bob/skills/advisory-analyst/SKILL.md
[ ] Create .bob/skills/art14-drafter/SKILL.md
[ ] Create .bob/skills/cra-evidence-pack/SKILL.md
[ ] Confirm all three skills are detected


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — .bob/skills/advisory-analyst/SKILL.md

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — [x] Create .bob/skills/advisory-analyst/SKILL.md
[-] Create .bob/skills/art14-drafter/SKILL.md
[ ] Create .bob/skills/cra-evidence-pack/SKILL.md
[ ] Confirm all three skills are detected


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — ---
name: art14-drafter
description: Use after a gate run that produced files in sample-app/release-evidence/art14/<signal>/ — completes every placeholder in early_warning.md, notification.md and final_report.md using gate.json and OSV data.
---

# Art. 14 Drafter

Activate when `sample-app/release-evidence/art14/` contains at least one signal directory with
draft report files.

## Steps

1. **Discover signal directories.**
   List `sample-app/release-evidence/art14/` and note every sub-directory (each is a CVE/signal).
   For each signal, identify which of `early_warning.md`, `notification.md`, `final_report.md`
   are present.

2. **Gather source data.**
   Read:
   - `sample-app/release-evidence/gate.json` — severity, score, affected versions, gate verdict
   - `sample-app/.gatekeeper/osv-cache/<signal>.json` — advisory summary, references, affected
   - `sample-app/gatekeeper.toml` — product name, version, release track, contact details
   - `sample-app/.gatekeeper/signals.json` — signal metadata (deadline fields, notified flag)

3. **Complete each placeholder.**
   For every file found in step 1, read it and replace every placeholder marked with
   angle-bracket `<to complete>` text using the data gathered in step 2.
   - Write factually and concisely; use exact values from the source files.
   - For any field where the required information is genuinely unavailable from the source files,
     replace the placeholder with `[needs human input: <reason>]`.
   - Never fabricate CVSS scores, dates, or affected versions.

4. **Add a "What users should do" section.**
   At the end of each completed document, append a `## What users should do` section with:
   - Recommended upgrade path (package and target version from OSV `fixed` range)
   - Interim mitigations if no fix is available
   - Where to find further information (OSV URL or NVD link from OSV references)

5. **Never mark as submitted.**
   Do not set any `submitted`, `sent`, or `notified` field to `true`. Leave status fields unchanged
   or add `[pending human review]` where a status must be written.

6. **Write the completed files back.**
   Overwrite each file in place using `write_file`. Do not create new directories.

7. **Summarise.**
   Report which files were updated, which placeholders remain as `[needs human input]`, and any
   Art. 14 deadlines parsed from `signals.json` in ISO 8601 UTC format.


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — [x] Create .bob/skills/advisory-analyst/SKILL.md
[x] Create .bob/skills/art14-drafter/SKILL.md
[-] Create .bob/skills/cra-evidence-pack/SKILL.md
[ ] Confirm all three skills are detected


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — ---
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


### 🤖 Assistant

> 🔧 called: execute_command

Now verify all three are in place and check line counts:

> 🔧 **execute_command** — Get-ChildItem .bob\skills -Recurse -Filter SKILL.md | ForEach-Object { $lines = (Get-Content $_.FullName).Count; "$($_.FullName) — $lines lines" }

### 🤖 Assistant

> 🔧 called: read_file

`advisory-analyst` is 62 lines — two over the 60-line limit. Let me trim it:

> 🔧 **read_file** — .bob/skills/advisory-analyst/SKILL.md

### 🤖 Assistant

> 🔧 called: apply_diff



> 🔧 **apply_diff** — .bob/skills/advisory-analyst/SKILL.md

### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — Get-ChildItem .bob\skills -Recurse -Filter SKILL.md | ForEach-Object { $lines = (Get-Content $_.FullName).Count; "$($_.FullName.Split('\')[-2]) — $lines lines" }

### 🤖 Assistant

> 🔧 called: execute_command

All three are under 60 lines. Now confirm detection:

> 🔧 **execute_command** — Get-ChildItem .bob\skills -Directory | Select-Object -ExpandProperty Name

### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — Get-ChildItem .bob\skills -Recurse -Filter SKILL.md | ForEach-Object { $content = Get-Content $_.FullName -Raw; $name = [regex]::Match($content, 'name:\s*(.+)').Groups[1].Value.Trim(); $desc = [regex]::Match($content, 'description:\s*(.+)').Groups[1].Value.Trim(); "$name`n  desc: $desc`n  path: $($_.FullName.Replace('C:\Users\desim\repos\ibm-bob-2-hackathon\',''))`n" }

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — [x] Create .bob/skills/advisory-analyst/SKILL.md
[x] Create .bob/skills/art14-drafter/SKILL.md
[x] Create .bob/skills/cra-evidence-pack/SKILL.md
[x] Confirm all three skills are detected


### 🤖 Assistant

All three skills are created and detected. Here's the summary:

---

### Skills created under `.bob/skills/`

| Skill | Path | Lines | Activates when… |
|---|---|---|---|
| [`advisory-analyst`](.bob/skills/advisory-analyst/SKILL.md) | `.bob/skills/advisory-analyst/SKILL.md` | 42 | `gate.json` has a finding with `reachability: UNKNOWN` or `vex_status: under_investigation` |
| [`art14-drafter`](.bob/skills/art14-drafter/SKILL.md) | `.bob/skills/art14-drafter/SKILL.md` | 48 | A gate run has produced draft files in `release-evidence/art14/<signal>/` |
| [`cra-evidence-pack`](.bob/skills/cra-evidence-pack/SKILL.md) | `.bob/skills/cra-evidence-pack/SKILL.md` | 45 | Asked whether a release can ship |

**Detection confirmed** — all three directories exist under `.bob/skills/`, each with a valid `name` (lowercase-dash only, ≤64 chars) and a concrete `description` trigger. They will auto-activate in the next task session.

**Workflow each skill drives:**
- **`advisory-analyst`** → reads OSV cache → grep call sites in `app/` → writes `symbols.local.json` → optionally writes `vex_overrides.json` → re-runs gate
- **`art14-drafter`** → fills all `<to complete>` placeholders in the three Art. 14 report files → appends "What users should do" → never marks anything submitted
- **`cra-evidence-pack`** → runs gate → tables every blocker with its resolving skill → lists Art. 14 deadlines in UTC with hours remaining → emits a single ✅/🚫 ship decision