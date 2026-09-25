"""End-to-end tests on a temporary copy of the demo product (offline, no network)."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gatekeeper import gate, reach, sbom  # noqa: E402


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.proj = self.tmp / "sample-app"
        shutil.copytree(ROOT / "sample-app", self.proj)
        subprocess.run([sys.executable, str(self.proj / "demo" / "reset_demo.py")], check=True, capture_output=True)
        self.now = datetime.now(timezone.utc)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_gate(self, now=None):
        return gate.run(self.proj, self.proj / "release-evidence", offline=True, now=now or self.now)

    def apply_fix(self):
        (self.proj / "requirements.txt").write_text("PyYAML==6.0.2\nrequests==2.33.0\nJinja2==2.10\n")
        cfg = self.proj / "app" / "config.py"
        cfg.write_text(cfg.read_text().replace("yaml.load(fh, Loader=yaml.FullLoader)", "yaml.safe_load(fh)"))


class TestSBOM(Base):
    def test_pinned_and_unpinned(self):
        req = self.tmp / "r.txt"
        req.write_text("PyYAML==5.3.1\nflask>=2\n# c\n")
        comps, warns = sbom.parse_requirements(req)
        self.assertEqual([c.purl for c in comps], ["pkg:pypi/pyyaml@5.3.1"])
        self.assertEqual(len(warns), 1)


class TestReachability(Base):
    def test_verdicts(self):
        res = self.run_gate()
        by = {(f["id"], f["package"]): f for f in res["findings"]}
        self.assertEqual(by[("CVE-2020-14343", "pyyaml")]["reachability"], reach.REACHABLE)
        self.assertIn("config.py", by[("CVE-2020-14343", "pyyaml")]["evidence"][0])
        self.assertEqual(by[("CVE-2018-18074", "requests")]["reachability"], reach.REACHABLE)
        self.assertEqual(by[("CVE-2026-25645", "requests")]["reachability"], reach.NOT_CALLED)
        self.assertTrue(all(f["reachability"] == reach.NOT_IMPORTED for f in res["findings"] if f["package"] == "jinja2"))


class TestGate(Base):
    def test_blocks_vulnerable_rc(self):
        res = self.run_gate()
        self.assertEqual(res["gate"], "BLOCK")
        self.assertTrue(any("CVE-2020-14343" in r for r in res["reasons"]))
        clk = res["art14"][0]
        self.assertEqual(clk["early_warning"]["state"], "open")
        self.assertEqual(clk["final_report"]["state"], "waiting_for_fix")
        for name in ("early_warning", "notification", "final_report"):
            self.assertTrue((self.proj / "release-evidence" / "art14" / "SIG-2026-0001" / f"{name}.md").exists())
        vexdoc = json.loads((self.proj / "release-evidence" / "vex.openvex.json").read_text())
        self.assertEqual(vexdoc["@context"], "https://openvex.dev/ns/v0.2.0")

    def test_passes_after_fix_and_starts_final_report_clock(self):
        self.apply_fix()
        res = self.run_gate()
        self.assertEqual(res["gate"], "PASS", res["reasons"])
        clk = res["art14"][0]
        self.assertEqual(clk["final_report"]["state"], "open")
        self.assertAlmostEqual(clk["final_report"]["hours_left"], 14 * 24, delta=0.2)
        self.assertEqual(res["counts"]["affected"], 0)

    def test_overdue_early_warning_blocks_even_after_fix(self):
        self.apply_fix()
        res = self.run_gate(now=self.now + timedelta(hours=30))
        self.assertEqual(res["gate"], "BLOCK")
        self.assertTrue(any("early warning" in r for r in res["reasons"]))

    def test_unknown_advisory_blocks_until_mapped(self):
        """The Bob advisory-analyst loop: UNKNOWN blocks, a reviewed symbol mapping unblocks."""
        self.apply_fix()
        req = self.proj / "requirements.txt"
        req.write_text(req.read_text() + "demo-lib==1.0.0\n")
        (self.proj / ".gatekeeper" / "osv-cache" / "demo-lib-1.0.0.json").write_text(json.dumps({"vulns": [{
            "id": "GHSA-demo-0001", "aliases": ["CVE-2099-0001"], "summary": "Synthetic test advisory",
            "database_specific": {"severity": "MODERATE"},
            "affected": [{"ranges": [{"type": "ECOSYSTEM", "events": [{"introduced": "0"}, {"fixed": "1.0.1"}]}]}]}]}))
        (self.proj / "app" / "extra.py").write_text("import demo_lib\ndemo_lib.safe_helper()\n")
        res = self.run_gate()
        self.assertEqual(res["gate"], "BLOCK")
        self.assertTrue(any("under_investigation" in r for r in res["reasons"]))
        (self.proj / ".gatekeeper" / "symbols.local.json").write_text(json.dumps(
            {"CVE-2099-0001": {"package": "demo-lib", "symbols": ["demo_lib.parse_untrusted"]}}))
        res = self.run_gate()
        self.assertEqual(res["gate"], "PASS", res["reasons"])

    def test_art14_draft_not_overwritten_on_rerun(self):
        """gate.py must preserve existing Art.14 drafts; only create if absent."""
        # Run once to create the scaffold files
        self.run_gate()
        draft = self.proj / "release-evidence" / "art14" / "SIG-2026-0001" / "early_warning.md"
        self.assertTrue(draft.exists(), "scaffold should have been created on first run")
        # Write custom text into the file — simulating work done by art14-drafter
        custom_text = "CUSTOM COMPLETED DRAFT — must survive re-run"
        draft.write_text(custom_text, encoding="utf-8")
        # Re-run the gate
        self.run_gate()
        # The custom text must be intact
        self.assertEqual(draft.read_text(encoding="utf-8"), custom_text,
                         "gate.py must not overwrite an existing Art.14 draft file")

    def test_invalid_override_is_rejected(self):
        (self.proj / ".gatekeeper" / "vex_overrides.json").write_text(json.dumps(
            {"CVE-2020-14343": {"status": "not_affected", "justification": "trust me"}}))
        with self.assertRaises(ValueError):
            self.run_gate()

    def test_ledger_records_each_run(self):
        self.run_gate()
        self.apply_fix()
        self.run_gate()
        lines = (self.proj / ".gatekeeper" / "ledger.jsonl").read_text().splitlines()
        self.assertEqual([json.loads(l)["gate"] for l in lines], ["BLOCK", "PASS"])


class TestCLI(Base):
    def test_exit_codes(self):
        cmd = [sys.executable, "-m", "gatekeeper", "check", str(self.proj), "--offline"]
        self.assertEqual(subprocess.run(cmd, cwd=ROOT, capture_output=True).returncode, 1)
        self.apply_fix()
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((self.proj / "release-evidence" / "index.html").exists())


if __name__ == "__main__":
    unittest.main()
