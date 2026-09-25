# Set up the IBM Bob configuration for this repo, in two parts. PART 1 - custom mode: create .bob/custom_modes.yaml with a mode slug cra-release-officer, name 'CRA Release Officer', roleDefinition: a release manager responsible for EU Cyber Resilience Act (Regulation (EU) 2024/2847) compliance of the fattura-lite product in sample-app/. whenToUse: preparing a release, triaging vulnerabilities, drafting Art. 14 reports. groups: read, command, skill, and edit restricted by fileRegex to requirements.txt, sample-app/app/**, sample-app/gatekeeper.toml, sample-app/.gatekeeper/*.json and sample-app/release-evidence/**. customInstructions: (1) always run 'python -m gatekeeper check sample-app --offline' first and read sample-app/release-evidence/gate.json; (2) never mark a vulnerability not_affected without an OpenVEX justification plus author and reason; (3) never submit anything to a CSIRT or ENISA, only prepare drafts; (4) finish every task with the gate result and each Art. 14 deadline in UTC. Also write those four rules to .bob/rules-cra-release-officer/01-evidence.md. PART 2 - release hook: create .bob/hooks/release_gate.py (Python stdlib only) that reads the hook event JSON from stdin; if the tool call is a shell command containing 'git push' or 'git tag', it runs 'python -m gatekeeper check sample-app --offline' from the repo root, and when the gate result is BLOCK it prints the blocking reasons to stderr and exits with code 2, otherwise exits 0. Register it in .bob/settings.json under hooks.PreToolUse with a matcher for the command-execution tool, and add a Stop hook that appends one JSON line per finished task (timestamp and final gate result) to sample-app/.gatekeeper/bob_tasks.jsonl. Check the exact hooks and custom-mode schema against the IBM Bob documentation before writing, and add a unit test tests/test_release_hook.py that feeds sample JSON on stdin and checks exit code 2 on BLOCK and 0 for a non-git command. Run the tests at the end.

---

**Status:** active  **Date:** 2026-09-25

---

### 👤 User

Set up the IBM Bob configuration for this repo, in two parts. PART 1 - custom mode: create .bob/custom_modes.yaml with a mode slug cra-release-officer, name 'CRA Release Officer', roleDefinition: a release manager responsible for EU Cyber Resilience Act (Regulation (EU) 2024/2847) compliance of the fattura-lite product in sample-app/. whenToUse: preparing a release, triaging vulnerabilities, drafting Art. 14 reports. groups: read, command, skill, and edit restricted by fileRegex to requirements.txt, sample-app/app/**, sample-app/gatekeeper.toml, sample-app/.gatekeeper/*.json and sample-app/release-evidence/**. customInstructions: (1) always run 'python -m gatekeeper check sample-app --offline' first and read sample-app/release-evidence/gate.json; (2) never mark a vulnerability not_affected without an OpenVEX justification plus author and reason; (3) never submit anything to a CSIRT or ENISA, only prepare drafts; (4) finish every task with the gate result and each Art. 14 deadline in UTC. Also write those four rules to .bob/rules-cra-release-officer/01-evidence.md. PART 2 - release hook: create .bob/hooks/release_gate.py (Python stdlib only) that reads the hook event JSON from stdin; if the tool call is a shell command containing 'git push' or 'git tag', it runs 'python -m gatekeeper check sample-app --offline' from the repo root, and when the gate result is BLOCK it prints the blocking reasons to stderr and exits with code 2, otherwise exits 0. Register it in .bob/settings.json under hooks.PreToolUse with a matcher for the command-execution tool, and add a Stop hook that appends one JSON line per finished task (timestamp and final gate result) to sample-app/.gatekeeper/bob_tasks.jsonl. Check the exact hooks and custom-mode schema against the IBM Bob documentation before writing, and add a unit test tests/test_release_hook.py that feeds sample JSON on stdin and checks exit code 2 on BLOCK and 0 for a non-git command. Run the tests at the end.

---

### 🤖 Assistant

> 🔧 called: use_skill, use_skill



> 🔧 **use_skill** — configure-hooks

> 🔧 **use_skill** — create-mode

### 🤖 Assistant

> 🔧 called: list_files, glob

Both skills loaded. Now let me explore the repo structure and check for existing settings files before writing anything.

> 🔧 **list_files** — .

> 🔧 **glob** — .bob/**/*

### 🤖 Assistant

> 🔧 called: list_files, list_files



> 🔧 **list_files** — tests

> 🔧 **list_files** — sample-app

### 🤖 Assistant

> 🔧 called: list_files, list_files



> 🔧 **list_files** — sample-app/.gatekeeper

> 🔧 **list_files** — sample-app/release-evidence

### 🤖 Assistant

> 🔧 called: read_file, read_file

Good — no `.bob/` directory yet, and the target files exist. Now let me read the existing tests file to understand the test conventions, and check the gatekeeper module for what `check` outputs:

> 🔧 **read_file** — sample-app/release-evidence/gate.json

> 🔧 **read_file** — tests/test_gatekeeper.py

### 🤖 Assistant

> 🔧 called: update_todo_list

Now I have everything I need. Let me set up the todo list and create all files:

> 🔧 **update_todo_list** — 
[-] Create .bob/ directory structure and custom_modes.yaml
[ ] Create .bob/rules-cra-release-officer/01-evidence.md
[ ] Create .bob/hooks/release_gate.py
[ ] Create/update .bob/settings.json with PreToolUse and Stop hooks
[ ] Create tests/test_release_hook.py
[ ] Run tests


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — .bob/custom_modes.yaml

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Create .bob/ directory structure and custom_modes.yaml
[-] Create .bob/rules-cra-release-officer/01-evidence.md
[ ] Create .bob/hooks/release_gate.py
[ ] Create/update .bob/settings.json with PreToolUse and Stop hooks
[ ] Create tests/test_release_hook.py
[ ] Run tests


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — .bob/rules-cra-release-officer/01-evidence.md

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Create .bob/ directory structure and custom_modes.yaml
[x] Create .bob/rules-cra-release-officer/01-evidence.md
[-] Create .bob/hooks/release_gate.py
[ ] Create/update .bob/settings.json with PreToolUse and Stop hooks
[ ] Create tests/test_release_hook.py
[ ] Run tests


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
release_gate.py — Bob PreToolUse / Stop hook (Python stdlib only).

PreToolUse behaviour:
  - Reads the hook event JSON from stdin.
  - If the tool is a shell command containing 'git push' or 'git tag',
    runs 'python -m gatekeeper check sample-app --offline' from the repo root.
  - If the gate result is BLOCK, writes the blocking reasons to stderr
    and exits with code 2 (blocks the tool call).
  - Otherwise exits 0 (allow).

Stop behaviour:
  - Appends one JSON line to sample-app/.gatekeeper/bob_tasks.jsonl with
    the UTC timestamp and the final gate result read from gate.json.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _repo_root(cwd: str) -> Path:
    """Return the workspace root supplied by Bob in the event payload."""
    return Path(cwd)


def _run_gate(repo_root: Path) -> dict:
    """Run the gatekeeper check and return the parsed gate.json dict."""
    subprocess.run(
        [sys.executable, "-m", "gatekeeper", "check", "sample-app", "--offline"],
        cwd=str(repo_root),
        check=False,  # gate returns exit 1 on BLOCK; we don't want to raise
    )
    gate_path = repo_root / "sample-app" / "release-evidence" / "gate.json"
    return json.loads(gate_path.read_text())


def handle_pre_tool_use(event: dict) -> None:
    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input", {})

    # Only intercept shell command execution tools
    if tool_name not in ("execute_command", "Bash"):
        return

    command = tool_input.get("command", "")
    if not ("git push" in command or "git tag" in command):
        return

    cwd = event.get("cwd", os.getcwd())
    repo_root = _repo_root(cwd)

    result = _run_gate(repo_root)

    if result.get("gate") == "BLOCK":
        reasons = result.get("reasons", [])
        sys.stderr.write("CRA release gate: BLOCK\n")
        for reason in reasons:
            sys.stderr.write(f"  • {reason}\n")
        sys.stderr.write(
            "Resolve all blocking findings before pushing or tagging a release.\n"
        )
        sys.exit(2)


def handle_stop(event: dict) -> None:
    cwd = event.get("cwd", os.getcwd())
    repo_root = _repo_root(cwd)

    gate_path = repo_root / "sample-app" / "release-evidence" / "gate.json"
    try:
        gate_result = json.loads(gate_path.read_text()).get("gate", "UNKNOWN")
    except (OSError, json.JSONDecodeError):
        gate_result = "UNKNOWN"

    record = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "gate": gate_result,
    }

    tasks_file = repo_root / "sample-app" / ".gatekeeper" / "bob_tasks.jsonl"
    tasks_file.parent.mkdir(parents=True, exist_ok=True)
    with tasks_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def main() -> None:
    raw = sys.stdin.read()
    event = json.loads(raw)
    hook_event = event.get("hook_event_name", "")

    if hook_event == "PreToolUse":
        handle_pre_tool_use(event)
    elif hook_event == "Stop":
        handle_stop(event)


if __name__ == "__main__":
    main()


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Create .bob/ directory structure and custom_modes.yaml
[x] Create .bob/rules-cra-release-officer/01-evidence.md
[x] Create .bob/hooks/release_gate.py
[-] Create/update .bob/settings.json with PreToolUse and Stop hooks
[ ] Create tests/test_release_hook.py
[ ] Run tests


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — {
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "execute_command",
        "hooks": [
          {
            "type": "command",
            "command": "python .bob/hooks/release_gate.py",
            "timeout": 60
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .bob/hooks/release_gate.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Create .bob/ directory structure and custom_modes.yaml
[x] Create .bob/rules-cra-release-officer/01-evidence.md
[x] Create .bob/hooks/release_gate.py
[x] Create/update .bob/settings.json with PreToolUse and Stop hooks
[-] Create tests/test_release_hook.py
[ ] Run tests


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
tests/test_release_hook.py

Unit tests for .bob/hooks/release_gate.py.

These tests inject synthetic gate.json fixtures and feed hook event JSON on
stdin, then assert on the exit code rather than on real gatekeeper output.
The tests monkey-patch _run_gate to avoid requiring a live gatekeeper run.
"""

import json
import sys
import types
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
# Make sure the hook is importable without installing it
sys.path.insert(0, str(ROOT / ".bob" / "hooks"))

import release_gate  # noqa: E402  (side-effect-free at import time)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BLOCK_GATE = {
    "gate": "BLOCK",
    "reasons": [
        "CVE-2020-14343 in pyyaml 5.3.1: affected (CRITICAL)",
        "CVE-2018-18074 in requests 2.19.1: affected (HIGH)",
    ],
}

PASS_GATE = {
    "gate": "PASS",
    "reasons": [],
}


def _pre_tool_event(command: str, tool_name: str = "execute_command") -> str:
    return json.dumps(
        {
            "session_id": "test-session",
            "cwd": str(ROOT),
            "hook_event_name": "PreToolUse",
            "tool_name": tool_name,
            "tool_input": {"command": command},
            "tool_use_id": "test-tool-use",
        }
    )


def _stop_event() -> str:
    return json.dumps(
        {
            "session_id": "test-session",
            "cwd": str(ROOT),
            "hook_event_name": "Stop",
            "last_assistant_message": "Done.",
        }
    )


# ---------------------------------------------------------------------------
# PreToolUse tests
# ---------------------------------------------------------------------------


class TestPreToolUseBlock(unittest.TestCase):
    """gate result is BLOCK + command contains 'git push' → exit 2."""

    def test_git_push_blocks_on_block_gate(self):
        with (
            patch.object(release_gate, "_run_gate", return_value=BLOCK_GATE),
            patch("sys.stdin", StringIO(_pre_tool_event("git push origin main"))),
            patch("sys.stderr", new_callable=StringIO) as mock_err,
            self.assertRaises(SystemExit) as ctx,
        ):
            release_gate.main()

        self.assertEqual(ctx.exception.code, 2)
        err_output = mock_err.getvalue()
        self.assertIn("BLOCK", err_output)
        self.assertIn("CVE-2020-14343", err_output)

    def test_git_tag_blocks_on_block_gate(self):
        with (
            patch.object(release_gate, "_run_gate", return_value=BLOCK_GATE),
            patch("sys.stdin", StringIO(_pre_tool_event("git tag v1.4.0"))),
            patch("sys.stderr", new_callable=StringIO),
            self.assertRaises(SystemExit) as ctx,
        ):
            release_gate.main()

        self.assertEqual(ctx.exception.code, 2)


class TestPreToolUseAllow(unittest.TestCase):
    """Non-git commands and PASS gates must not exit with code 2."""

    def test_non_git_command_exits_0(self):
        """A command that does not contain 'git push' or 'git tag' must pass through."""
        with (
            patch.object(release_gate, "_run_gate", return_value=BLOCK_GATE) as mock_gate,
            patch("sys.stdin", StringIO(_pre_tool_event("ls -la"))),
        ):
            # Should return normally without raising SystemExit
            release_gate.main()

        # _run_gate must NOT have been called for a non-git command
        mock_gate.assert_not_called()

    def test_git_push_passes_on_pass_gate(self):
        """PASS gate must not block even for 'git push'."""
        with (
            patch.object(release_gate, "_run_gate", return_value=PASS_GATE),
            patch("sys.stdin", StringIO(_pre_tool_event("git push origin main"))),
        ):
            release_gate.main()  # must not raise

    def test_non_execute_tool_ignored(self):
        """A tool that is not execute_command must not trigger the gate check."""
        event = json.dumps(
            {
                "session_id": "test-session",
                "cwd": str(ROOT),
                "hook_event_name": "PreToolUse",
                "tool_name": "write_file",
                "tool_input": {"path": "foo.txt", "content": "git push"},
                "tool_use_id": "test-tool-use",
            }
        )
        with (
            patch.object(release_gate, "_run_gate", return_value=BLOCK_GATE) as mock_gate,
            patch("sys.stdin", StringIO(event)),
        ):
            release_gate.main()

        mock_gate.assert_not_called()

    def test_git_fetch_is_not_blocked(self):
        """'git fetch' does not match 'git push' or 'git tag', must not block."""
        with (
            patch.object(release_gate, "_run_gate", return_value=BLOCK_GATE) as mock_gate,
            patch("sys.stdin", StringIO(_pre_tool_event("git fetch --all"))),
        ):
            release_gate.main()

        mock_gate.assert_not_called()


# ---------------------------------------------------------------------------
# Stop hook tests
# ---------------------------------------------------------------------------


class TestStopHook(unittest.TestCase):
    def test_stop_appends_jsonl_line(self):
        import tempfile
        import shutil

        tmp = Path(tempfile.mkdtemp())
        try:
            # Create the minimal directory structure the hook expects
            gate_dir = tmp / "sample-app" / "release-evidence"
            gate_dir.mkdir(parents=True)
            (gate_dir / "gate.json").write_text(json.dumps(PASS_GATE))

            gatekeeper_dir = tmp / "sample-app" / ".gatekeeper"
            gatekeeper_dir.mkdir(parents=True)

            stop_event = json.dumps(
                {
                    "session_id": "test-session",
                    "cwd": str(tmp),
                    "hook_event_name": "Stop",
                    "last_assistant_message": "All done.",
                }
            )

            with patch("sys.stdin", StringIO(stop_event)):
                release_gate.main()

            tasks_file = gatekeeper_dir / "bob_tasks.jsonl"
            self.assertTrue(tasks_file.exists(), "bob_tasks.jsonl was not created")

            lines = tasks_file.read_text().splitlines()
            self.assertEqual(len(lines), 1)

            record = json.loads(lines[0])
            self.assertIn("timestamp", record)
            self.assertEqual(record["gate"], "PASS")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_stop_appends_multiple_lines(self):
        import tempfile
        import shutil

        tmp = Path(tempfile.mkdtemp())
        try:
            gate_dir = tmp / "sample-app" / "release-evidence"
            gate_dir.mkdir(parents=True)
            gatekeeper_dir = tmp / "sample-app" / ".gatekeeper"
            gatekeeper_dir.mkdir(parents=True)

            for gate_result in (BLOCK_GATE, PASS_GATE):
                (gate_dir / "gate.json").write_text(json.dumps(gate_result))
                stop_event = json.dumps(
                    {
                        "session_id": "test-session",
                        "cwd": str(tmp),
                        "hook_event_name": "Stop",
                        "last_assistant_message": "Done.",
                    }
                )
                with patch("sys.stdin", StringIO(stop_event)):
                    release_gate.main()

            tasks_file = gatekeeper_dir / "bob_tasks.jsonl"
            lines = tasks_file.read_text().splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0])["gate"], "BLOCK")
            self.assertEqual(json.loads(lines[1])["gate"], "PASS")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Create .bob/ directory structure and custom_modes.yaml
[x] Create .bob/rules-cra-release-officer/01-evidence.md
[x] Create .bob/hooks/release_gate.py
[x] Create/update .bob/settings.json with PreToolUse and Stop hooks
[x] Create tests/test_release_hook.py
[-] Run tests


### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — python -m pytest tests/test_release_hook.py -v 2>&1

### 🤖 Assistant

> 🔧 called: execute_command

All 8 tests pass. Let me also verify the existing gatekeeper tests are unaffected:

> 🔧 **execute_command** — python -m pytest tests/test_gatekeeper.py -v 2>&1

### 🤖 Assistant

> 🔧 called: update_todo_list

All 17 tests pass (8 new + 9 existing). Let me mark the work complete:

> 🔧 **update_todo_list** — 
[x] Create .bob/ directory structure and custom_modes.yaml
[x] Create .bob/rules-cra-release-officer/01-evidence.md
[x] Create .bob/hooks/release_gate.py
[x] Create/update .bob/settings.json with PreToolUse and Stop hooks
[x] Create tests/test_release_hook.py
[x] Run tests


### 🤖 Assistant

Everything is in place. Here's what was created and how each piece works:

---

## What was built

### Part 1 — Custom Mode

**[`.bob/custom_modes.yaml`](.bob/custom_modes.yaml)**
Defines the `cra-release-officer` mode with:
- `groups`: `read`, `execute`, `skill`, and a restricted `edit` group whose `fileRegex` covers `requirements.txt`, `sample-app/app/**`, `sample-app/gatekeeper.toml`, `sample-app/.gatekeeper/*.json`, and `sample-app/release-evidence/**` — nothing else is writable.
- `customInstructions` encoding the four rules: gate-first, OpenVEX requirement, no CSIRT/ENISA submissions, and close every task with gate result + Art. 14 deadlines in UTC.

> **Note on group names:** the schema uses `execute` (not `command`) for shell access — that's the group that maps to `execute_command`. Using `command` would silently grant nothing.

**[`.bob/rules-cra-release-officer/01-evidence.md`](.bob/rules-cra-release-officer/01-evidence.md)**
The four standing rules written as a human-readable policy document, referenced from Bob's rules directory.

---

### Part 2 — Release Hook

**[`.bob/hooks/release_gate.py`](.bob/hooks/release_gate.py)**
Pure Python stdlib. Handles two Bob events from the same script:

| Event | Trigger | Action |
|---|---|---|
| `PreToolUse` | `execute_command` tool with `git push` or `git tag` in the command | Runs gatekeeper; exits 2 (blocks) if `BLOCK`; exits 0 otherwise |
| `Stop` | End of any task | Reads `gate.json` and appends `{"timestamp": "…Z", "gate": "PASS/BLOCK"}` to `sample-app/.gatekeeper/bob_tasks.jsonl` |

**[`.bob/settings.json`](.bob/settings.json)**
Registers the hook for both events:
- `PreToolUse` matcher: `execute_command` — timeout 60 s (enough for an offline gatekeeper run)
- `Stop` — no matcher (runs after every task), timeout 30 s

---

### Tests

**[`tests/test_release_hook.py`](tests/test_release_hook.py)** — 8 tests, all passing:

| Test | Assertion |
|---|---|
| `test_git_push_blocks_on_block_gate` | exit 2, BLOCK + CVE in stderr |
| `test_git_tag_blocks_on_block_gate` | exit 2 |
| `test_non_git_command_exits_0` | exits 0, `_run_gate` never called |
| `test_git_push_passes_on_pass_gate` | exits 0 on PASS gate |
| `test_non_execute_tool_ignored` | `write_file` tool skipped, gate not called |
| `test_git_fetch_is_not_blocked` | `git fetch` is not push/tag, gate not called |
| `test_stop_appends_jsonl_line` | JSONL file created with timestamp + gate |
| `test_stop_appends_multiple_lines` | two consecutive Stop events produce two appended lines |