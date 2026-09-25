# Extend `.github/workflows/gatekeeper.yml` (keep the existing gate job working): (1) on pull_request, upload `sample-app/release-evidence/` as a build artifact (actions/upload-artifact@v4, even if the gate fails) and post the gate summary line as a PR comment (use actions/github-script@v7, needs `pull-requests: write`); (2) add an optional job `bob-headless` that runs only when a `BOB_API_KEY` secret is configured (gate it via an env/if check, never echo the secret) and runs Bob Shell non-interactively with the `cra-evidence-pack` skill. If you are unsure of the exact Bob Shell CLI flags, put them in one clearly commented variable. Validate the YAML parses with python, do not touch other files, and give a 4-line summary.

---

**Status:** active  **Date:** 2026-09-25

---

### 👤 User

Extend `.github/workflows/gatekeeper.yml` (keep the existing gate job working): (1) on pull_request, upload `sample-app/release-evidence/` as a build artifact (actions/upload-artifact@v4, even if the gate fails) and post the gate summary line as a PR comment (use actions/github-script@v7, needs `pull-requests: write`); (2) add an optional job `bob-headless` that runs only when a `BOB_API_KEY` secret is configured (gate it via an env/if check, never echo the secret) and runs Bob Shell non-interactively with the `cra-evidence-pack` skill. If you are unsure of the exact Bob Shell CLI flags, put them in one clearly commented variable. Validate the YAML parses with python, do not touch other files, and give a 4-line summary.

---

### 🤖 Assistant

> 🔧 called: read_file, search_ibm_docs



> 🔧 **read_file** — .github/workflows/gatekeeper.yml

> 🔧 **search_ibm_docs** — bob

### 🤖 Assistant

> 🔧 called: search_ibm_docs, search_ibm_docs



> 🔧 **search_ibm_docs** — bob

> 🔧 **search_ibm_docs** — bob

### 🤖 Assistant

> 🔧 called: search_ibm_docs



> 🔧 **search_ibm_docs** — bob

### 🤖 Assistant

> 🔧 called: write_file

Now I have everything needed. The key facts from docs:
- Bob Shell env var: `BOBSHELL_API_KEY`
- Non-interactive flag: `bob -p "..."` with `--auth-method api-key`
- Accept license once: `--accept-license`
- File writes: `--yolo`
- Install on Linux: `curl -fsSL https://bob.ibm.com/download/bobshell.sh | bash`

The existing workflow already has `upload-artifact` in the `gate` job (line 17-19). The request says to add it on `pull_request` with `if: always()` — it's already there unconditionally. I need to:
1. Add a PR comment step to the `gate` job (after the gate run, `if: always()`)
2. Add the `bob-headless` job

> 🔧 **write_file** — .github/workflows/gatekeeper.yml

### 🤖 Assistant

> 🔧 called: execute_command

Now validate the YAML parses:

> 🔧 **execute_command** — python -c "import yaml; yaml.safe_load(open('.github/workflows/gatekeeper.yml')); print('YAML OK')"

### 🤖 Assistant

YAML parses cleanly. Here's the 4-line summary:

1. **`gate` job** — added `permissions: pull-requests: write` and a new `actions/github-script@v7` step (`if: always() && github.event_name == 'pull_request'`) that reads `gate.json` and posts the verdict as a PR comment; the existing `upload-artifact` step is untouched.
2. **`bob-headless` job** — gated by `if: ${{ secrets.BOB_API_KEY != '' }}` so it silently skips when the secret is absent; maps `BOB_API_KEY` → `BOBSHELL_API_KEY` (the env var Bob Shell reads) without ever echoing it.
3. **Bob Shell flags** (`--accept-license --auth-method api-key --yolo -p "..."`) are isolated in a single commented `BOB_CMD` variable — easy to adjust as the CLI evolves; the job also uploads a second evidence artifact post-run.
4. **Python validation** confirmed `YAML OK` — no other files were touched.

---

### 👤 User

One fix: GitHub Actions does not allow the `secrets` context in a job-level `if:` (the whole workflow fails to load with "Unrecognized named-value: 'secrets'"). Remove the job-level `if`, and instead add a first step `check` that sets output `enabled=true` only when `BOBSHELL_API_KEY` is non-empty (`[ -n "$BOBSHELL_API_KEY" ]`); guard the install, run and upload steps with `if: steps.check.outputs.enabled == 'true'`. Re-validate the YAML and stop.

---

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — .github/workflows/gatekeeper.yml

### 🤖 Assistant

> 🔧 called: apply_diff



> 🔧 **apply_diff** — .github/workflows/gatekeeper.yml

### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — python -c "import yaml; yaml.safe_load(open('.github/workflows/gatekeeper.yml')); print('YAML OK')"

### 🤖 Assistant

YAML OK. The job-level `if: ${{ secrets.BOB_API_KEY != '' }}` is gone. In its place, a first step `check` (id: `check`) runs unconditionally, tests `[ -n "$BOBSHELL_API_KEY" ]`, and writes `enabled=true/false` to `$GITHUB_OUTPUT`. The three subsequent steps — install, run, and upload-artifact — each carry `if: steps.check.outputs.enabled == 'true'`, so they're skipped silently when the secret is absent. The secret value is never echoed.