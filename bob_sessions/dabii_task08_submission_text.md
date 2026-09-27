# Update `docs/SUBMISSION.md` (the lablab submission text). Keep its structure, but: (1) replace the ⟨⟩ placeholders you can fill from evidence: read `sample-app/release-evidence/gate.json`, `sample-app/.gatekeeper/ledger.jsonl` and the task exports in `bob_sessions/` (T01, T02+T04, T03, T04b, T05, T05b, T06, T07, T07b); Bobcoins so far: 8.43 across 9 tasks. Leave ⟨manual baseline⟩ and ⟨m⟩ minutes as placeholders (not measured yet). (2) Correct facts to match the evidence: after the fix the gate reports 6 advisories, 0 affected; before, 5 affected. (3) In the IBM Bob Usage section, name each Bob feature with its bob_sessions task file, and mention the hook demo (T04b), the draft-overwrite bug Bob found and fixed (T05b) and the safe_load lesson applied unprompted (T07b). (4) Keep EACH statement at most 500 words; count them with python and print the counts. Do not modify other files.

---

**Status:** active  **Date:** 2026-09-25

---

### 👤 User

Update `docs/SUBMISSION.md` (the lablab submission text). Keep its structure, but: (1) replace the ⟨⟩ placeholders you can fill from evidence: read `sample-app/release-evidence/gate.json`, `sample-app/.gatekeeper/ledger.jsonl` and the task exports in `bob_sessions/` (T01, T02+T04, T03, T04b, T05, T05b, T06, T07, T07b); Bobcoins so far: 8.43 across 9 tasks. Leave ⟨manual baseline⟩ and ⟨m⟩ minutes as placeholders (not measured yet). (2) Correct facts to match the evidence: after the fix the gate reports 6 advisories, 0 affected; before, 5 affected. (3) In the IBM Bob Usage section, name each Bob feature with its bob_sessions task file, and mention the hook demo (T04b), the draft-overwrite bug Bob found and fixed (T05b) and the safe_load lesson applied unprompted (T07b). (4) Keep EACH statement at most 500 words; count them with python and print the counts. Do not modify other files.

---

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[-] Read all evidence files to gather facts
[ ] Count words in current SUBMISSION.md sections
[ ] Update SUBMISSION.md with corrected facts and evidence
[ ] Verify word counts per section ≤ 500 words


### 🤖 Assistant

> 🔧 called: read_file, list_files



> 🔧 **list_files** — bob_sessions

> 🔧 **read_file** — docs/SUBMISSION.md

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob_sessions/dabii_task04b_hook_blocks_tag.md

> 🔧 **read_file** — sample-app/release-evidence/gate.json

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob_sessions/dabii_task07b_safe_load_demo.md

> 🔧 **read_file** — bob_sessions/dabii_task05b_draft_fix.md

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob_sessions/dabii_task05_release_1-4-1.md

> 🔧 **read_file** — sample-app/.gatekeeper/ledger.jsonl

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob_sessions/dabii_task02_mode_and_hooks.md

> 🔧 **read_file** — bob_sessions/dabii_task01_cra_mapping.md

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob_sessions/dabii_task06_ci_headless.md

> 🔧 **read_file** — bob_sessions/dabii_task03_skills.md

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — bob_sessions/dabii_task07_lessons_curator.md

### 🤖 Assistant

> 🔧 called: execute_command

Now I have all the evidence I need. Let me count words in the current sections and then write the updated file.

> 🔧 **execute_command** — python -c "
import re

text = open('docs/SUBMISSION.md', encoding='utf-8').read()

# Split by ## headers
sections = re.split(r'^(##[^\n]+)', text, flags=re.MULTILINE)
# sections[0] = content before first ##, then alternating header/content

parts = []
# Header block (title + short desc etc)
header_block = sections[0].strip()
parts.append(('Preamble / Title block', header_block))

i = 1
while i < len(sections):
    if sections[i].startswith('##'):
        heading = sections[i].strip()
        content = sections[i+1].strip() if i+1 < len(sections) else ''
        parts.append((heading, content))
        i += 2
    else:
        i += 1

print('Section word counts (current file):')
print('-' * 55)
for name, body in parts:
    words = len(body.split())
    print(f'{words:4d}  {name[:60]}')
"


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Read all evidence files to gather facts
[x] Count words in current SUBMISSION.md sections
[-] Update SUBMISSION.md with corrected facts and evidence
[ ] Verify word counts per section ≤ 500 words


### 🤖 Assistant

> 🔧 called: write_file

Key facts gathered from evidence:
- **Before fix**: 5 affected, gate BLOCK (CVE-2020-14343 in pyyaml 5.3.1 + CVE-2018-18074 in requests 2.19.1), from ledger
- **After fix**: 0 affected, 6 not_affected (all jinja2, NOT_IMPORTED), gate PASS
- **Total advisories**: 12 mentioned in current text is wrong — ledger shows before: 5 affected + 7 not_affected = 12 total; after: 0 affected + 6 not_affected = 6. The "12 advisories, 5 touched code" is correct from ledger rows 1-3 (5+7=12). After fix: 6 total, 0 affected. So correct: "12 advisories, 5 affected; after fix, 6 advisories, 0 affected."
- **Bobcoins**: 8.43 across 9 tasks
- **T04b**: hook demo blocking `git tag`
- **T05b**: draft-overwrite bug Bob found and fixed
- **T07b**: safe_load applied unprompted

> 🔧 **write_file** — docs/SUBMISSION.md

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Read all evidence files to gather facts
[x] Count words in current SUBMISSION.md sections
[x] Update SUBMISSION.md with corrected facts and evidence
[-] Verify word counts per section ≤ 500 words


### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — python -c "
import re

text = open('docs/SUBMISSION.md', encoding='utf-8').read()

# Split by ## headers
sections = re.split(r'^(##[^\n]+)', text, flags=re.MULTILINE)

parts = []
header_block = sections[0].strip()
parts.append(('Preamble / Title block', header_block))

i = 1
while i < len(sections):
    if sections[i].startswith('##'):
        heading = sections[i].strip()
        content = sections[i+1].strip() if i+1 < len(sections) else ''
        parts.append((heading, content))
        i += 2
    else:
        i += 1

print('Section word counts (updated file):')
print('-' * 60)
all_ok = True
for name, body in parts:
    words = len(body.split())
    flag = '  OK' if words <= 500 else '  EXCEEDS 500'
    if words > 500:
        all_ok = False
    print(f'{words:4d}  {name[:60]}{flag}')

print('-' * 60)
print('All sections within 500 words:', all_ok)
"


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Read all evidence files to gather facts
[x] Count words in current SUBMISSION.md sections
[x] Update SUBMISSION.md with corrected facts and evidence
[x] Verify word counts per section ≤ 500 words


### 🤖 Assistant

[`docs/SUBMISSION.md`](docs/SUBMISSION.md) is updated. Here are the section word counts from Python:

```
Section word counts (updated file):
------------------------------------------------------------
  65  Preamble / Title block  OK
 450  ## Problem & Solution  OK
 414  ## IBM Bob Usage  OK
------------------------------------------------------------
All sections within 500 words: True
```

**Changes made:**

**Problem & Solution**
- Named the product (fattura-lite) and gave the exact CVEs blocking before the fix: CVE-2020-14343 (CRITICAL, pyyaml 5.3.1, `config.py:8`) and CVE-2018-18074 (HIGH, requests 2.19.1, `gateway_client.py:9`)
- Replaced the `⟨fill after T05⟩` impact block with evidence-backed facts: before = 5 affected, gate BLOCK; after = 6 advisories total, 0 affected, gate PASS (timestamp from `gate.json`)
- `⟨m⟩ minutes` and `⟨manual baseline⟩` left as instructed

**IBM Bob Usage**
- Every bullet now names its `bob_sessions/` file
- Hooks split into creation (T02+T04) and the live demo (T04b): mode rules refused first, PreToolUse hook blocked independently at the OS level with CVE list to stderr
- New T05b bullet: Bob found the draft-overwrite bug in `gate.py`, applied the `if not path.exists()` guard, added a regression test, re-completed drafts — all in one session
- New T07b bullet: Bob added the YAML-import endpoint using `yaml.safe_load()` without being prompted, citing the workspace lesson from CVE-2020-14343
- Budget updated to **8.43 Bobcoins across 9 tasks**; removed the placeholder T08 "Submission" bullet