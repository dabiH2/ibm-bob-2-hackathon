# Create a Bob skill `lessons-curator` in `.bob/skills/lessons-curator/SKILL.md` (same front-matter format as the other skills in `.bob/skills/`). The skill must: (1) read `sample-app/.gatekeeper/ledger.jsonl` (gate runs) and `sample-app/.gatekeeper/bob_tasks.jsonl` (Bob tasks); (2) find root causes that recur across runs, e.g. unsafe deserialisation (yaml.load) or outdated/unpinned HTTP clients; (3) for each, write or update a rule in `.bob/rules/20-lessons.md`, citing the ledger run timestamps that justify it. Then apply the skill once right now to the current ledger and write `.bob/rules/20-lessons.md`. Keep it concise; do not modify any other files. Finish with a 5-line summary.

---

**Status:** active  **Date:** 2026-09-25

---

### 👤 User

Create a Bob skill `lessons-curator` in `.bob/skills/lessons-curator/SKILL.md` (same front-matter format as the other skills in `.bob/skills/`). The skill must: (1) read `sample-app/.gatekeeper/ledger.jsonl` (gate runs) and `sample-app/.gatekeeper/bob_tasks.jsonl` (Bob tasks); (2) find root causes that recur across runs, e.g. unsafe deserialisation (yaml.load) or outdated/unpinned HTTP clients; (3) for each, write or update a rule in `.bob/rules/20-lessons.md`, citing the ledger run timestamps that justify it. Then apply the skill once right now to the current ledger and write `.bob/rules/20-lessons.md`. Keep it concise; do not modify any other files. Finish with a 5-line summary.

---

### 🤖 Assistant

> 🔧 called: use_skill, list_files



> 🔧 **use_skill** — create-skill

> 🔧 **list_files** — .bob/skills

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — sample-app/.gatekeeper/ledger.jsonl

> 🔧 **read_file** — .bob/skills/advisory-analyst/SKILL.md

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — sample-app/.gatekeeper/bob_tasks.jsonl

### 🤖 Assistant

> 🔧 called: update_todo_list

Now I have everything I need. Let me write both files.

> 🔧 **update_todo_list** — [-] Write .bob/skills/lessons-curator/SKILL.md
[ ] Write .bob/rules/20-lessons.md based on current ledger data


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — .bob/skills/lessons-curator/SKILL.md

### 🤖 Assistant

> 🔧 called: update_todo_list

Now apply the skill to produce the rules file:

> 🔧 **update_todo_list** — [x] Write .bob/skills/lessons-curator/SKILL.md
[-] Write .bob/rules/20-lessons.md based on current ledger data


### 🤖 Assistant

> 🔧 called: execute_command

**Analysis of the ledger data:**

- **BLOCK runs (ledger):** 3 runs — `2026-09-25T18:11:52Z`, `2026-09-25T18:12:54Z`, `2026-09-25T18:13:27Z`
- **PASS runs (ledger):** 1 run — `2026-09-25T18:14:35Z`
- **Recurring BLOCK reasons (all 3 BLOCK runs):**
  1. `CVE-2020-14343 in pyyaml 5.3.1` — CRITICAL — `yaml.load()` without safe loader (unsafe deserialisation)
  2. `CVE-2018-18074 in requests 2.19.1` — HIGH — outdated/unpinned HTTP client

> 🔧 **execute_command** — New-Item -ItemType Directory -Path ".bob\rules" -Force | Out-Null; Write-Host "ok"

### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — .bob/rules/20-lessons.md

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — [x] Write .bob/skills/lessons-curator/SKILL.md
[x] Write .bob/rules/20-lessons.md based on current ledger data


### 🤖 Assistant

---

**5-line summary:**

1. **Skill created** at [`.bob/skills/lessons-curator/SKILL.md`](.bob/skills/lessons-curator/SKILL.md) with correct frontmatter, matching the existing workspace skill format.
2. **Ledger analysed:** 3 BLOCK runs and 1 PASS run found in [`ledger.jsonl`](sample-app/.gatekeeper/ledger.jsonl); `bob_tasks.jsonl` confirmed the same pattern (2 BLOCK, 4 PASS across task invocations).
3. **2 recurring root causes** identified: unsafe YAML deserialisation (`yaml.load` without `SafeLoader`, CVE-2020-14343, CRITICAL) and an outdated/unpinned HTTP client (`requests 2.19.1`, CVE-2018-18074, HIGH) — both appeared in all 3 BLOCK ledger runs.
4. **Rules written** to [`.bob/rules/20-lessons.md`](.bob/rules/20-lessons.md) — one H2 section per root cause, each with an actionable one-sentence rule and the ledger timestamps as evidence.
5. **Highest-severity finding:** CVE-2020-14343 (pyyaml unsafe deserialisation, CRITICAL); resolution is to replace all `yaml.load()` calls with `yaml.safe_load()` and pin `pyyaml ≥ 5.4`.