"""Pre-submission check for the IBM Bob 2.0 Hackathon (lablab.ai).

Run from the repo root:  python scripts/submission_check.py
Every rule below comes from the official event page / guide. Exit code 0 only
when nothing is FAIL. It never changes anything; it only reports.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECRET_PATTERNS = [
    (r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "private key"),
    (r"\bgh[pousr]_[A-Za-z0-9]{30,}\b", "GitHub token"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key"),
    (r"(?i)\b(api[_-]?key|secret|password|bearer)\b\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "hard-coded credential"),
]
results: list[tuple[str, str, str]] = []


def check(name: str, ok: bool | None, detail: str = "") -> None:
    results.append(("PASS" if ok else "WARN" if ok is None else "FAIL", name, detail))


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'’-]+\b", text))


def git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return ""


def main() -> int:
    # 1. Bob evidence
    shots = sorted((ROOT / "bob_sessions").glob("*.png"))
    check("bob_sessions/ has task-summary PNGs", len(shots) > 0, f"{len(shots)} PNG(s)")
    bad = [s.name for s in shots if not re.match(r"^[a-z0-9]+_task\d{2}_[a-z0-9_-]+_summary\.png$", s.name)]
    check("PNG names follow <member>_taskNN_<name>_summary.png", not bad or None, ", ".join(bad[:5]))
    check("Bob config present (.bob/)", (ROOT / ".bob").is_dir() or None,
          "custom_modes.yaml / skills / settings.json come from playbook T02-T04")

    # 2. Licence and data
    lic = ROOT / "LICENSE"
    check("MIT LICENSE", lic.exists() and "MIT License" in lic.read_text(encoding="utf-8"))
    ds = ROOT / "DATA_SOURCES.md"
    check("DATA_SOURCES.md lists sources", ds.exists() and ds.read_text(encoding="utf-8").count("|") > 10)

    # 3. Secrets in tracked files (credentials in the repo deactivate the account)
    tracked = [ROOT / p for p in git("ls-files").splitlines()] or \
        [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    hits = []
    for p in tracked:
        if p.suffix.lower() in {".png", ".jpg", ".pdf", ".mp4", ".zip"} or not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pat, label in SECRET_PATTERNS:
            if re.search(pat, text):
                hits.append(f"{p.relative_to(ROOT)} ({label})")
    check("no credentials in tracked files", not hits, "; ".join(hits[:5]))
    env_tracked = [p for p in git("ls-files").splitlines() if re.search(r"(^|/)\.env", p)]
    check("no .env files tracked", not env_tracked, ", ".join(env_tracked))

    # 4. Statements (each <= 500 words)
    sub = ROOT / "docs" / "SUBMISSION.md"
    if sub.exists():
        text = sub.read_text(encoding="utf-8")
        parts = re.split(r"^## ", text, flags=re.M)
        for title in ("Problem & Solution", "IBM Bob Usage"):
            body = next((p for p in parts if p.startswith(title)), None)
            if body is None:
                check(f"statement '{title}' present", False, "section missing in docs/SUBMISSION.md")
            else:
                n = words(body.split("\n", 1)[1] if "\n" in body else "")
                check(f"statement '{title}' <= 500 words", 0 < n <= 500, f"{n} words")
        check("no unfinished placeholders in SUBMISSION.md", "⟨" not in text and "TODO" not in text or None)
    else:
        check("docs/SUBMISSION.md exists", False, "playbook T08")

    # 5. Product works
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=ROOT,
                       capture_output=True, text=True)
    check("unit tests pass", r.returncode == 0, (r.stderr.strip().splitlines() or [""])[-1])

    # 6. Repo state
    check("working tree committed", git("status", "--porcelain").strip() == "" or None,
          "uncommitted changes" if git("status", "--porcelain").strip() else "")
    vis = ""
    try:
        vis = subprocess.run(["gh", "repo", "view", "--json", "visibility", "-q", ".visibility"], cwd=ROOT,
                             capture_output=True, text=True, timeout=30).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    check("repository is PUBLIC", vis == "PUBLIC" if vis else None, vis or "gh not available")
    unpushed = git("log", "--oneline", "@{u}..").strip()
    check("all commits pushed", not unpushed or None, f"{len(unpushed.splitlines())} unpushed" if unpushed else "")

    # 7. Media (checked if present in submission/)
    media = ROOT / "submission"
    vids = list(media.glob("*.mp4")) if media.exists() else []
    check("demo video (MP4, <= 3 min) in submission/", bool(vids) or None, "keep it out of git if > 50 MB")
    check("slides PDF in submission/", bool(list(media.glob("*.pdf"))) if media.exists() else None)
    check("cover image in submission/", bool(list(media.glob("cover*.png"))) if media.exists() else None)

    width = max(len(n) for _, n, _ in results)
    for status, name, detail in results:
        print(f"[{status}] {name.ljust(width)}  {detail}")
    fails = sum(1 for s, _, _ in results if s == "FAIL")
    print(f"\n{fails} FAIL, {sum(1 for s, _, _ in results if s == 'WARN')} WARN, "
          f"{sum(1 for s, _, _ in results if s == 'PASS')} PASS")
    json.dump([dict(zip(("status", "check", "detail"), r)) for r in results],
              open(ROOT / "submission_check.json", "w", encoding="utf-8"), indent=2)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
