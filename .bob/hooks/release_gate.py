"""
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
