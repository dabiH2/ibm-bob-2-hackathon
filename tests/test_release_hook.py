"""
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
