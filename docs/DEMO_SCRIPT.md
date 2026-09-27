# Demo video script — 3:00 max (the judges stop at 3:00), at least 90 s of live demo

Record at 1920×1080 with Bob IDE on the left and the report in a browser on the right. Set the IDE font to 16 pt or more, narrate throughout, and export as MP4.
Before recording, run `python sample-app/demo/reset_demo.py --hours-ago 3`.

| Time | Screen | Narration (about 150 wpm) |
|---|---|---|
| 0:00–0:15 | Title card: "Article 14 Gatekeeper" plus the three clocks 24 h · 72 h · 14 d | "Since the eleventh of September, any company selling software in the EU has 24 hours to report an actively exploited vulnerability. Most teams find out they're late from a spreadsheet." |
| 0:15–0:30 | The fattura-lite repo; the signal `SIG-2026-0001` in `.gatekeeper/signals.json` | "Here's fattura-lite, an e-invoicing service. A customer's SOC tells us a PyYAML flaw is being exploited through tenant uploads. The clock started three hours ago." |
| 0:30–0:55 | Bob, mode **CRA Release Officer**, prompt from T05. Show the `git tag` attempt refused by the hook | "I ask Bob to prepare release 1.4.1. First, Bob's hook refuses to tag: the gate says BLOCK. The CRITICAL CVE is reachable at config.py line 8, and it gives the real file and line, not just 'you have a vulnerable package'." |
| 0:55–1:45 | **Three subagents in parallel**: remediation, advisory analyst, Art. 14 drafter. Split view of their progress | "Bob fans out three subagents at once. One upgrades the dependencies and swaps in safe_load. One triages advisories nobody has mapped yet, and writes a VEX justification with its name on it. One drafts the early warning and the notification from the regulation's own fields. Of twelve advisories, only five actually touch our code. The other seven get a signed 'not affected' instead of a reviewer's afternoon." |
| 1:45–2:15 | The gate turns **PASS**; the HTML report with the 24 h / 72 h countdowns and the final-report clock starting | "Re-run: PASS. The release unblocks. The legal clock keeps going: the early warning is still due in 21 hours, and fixing the bug has started the 14-day final-report clock. Missing any of these blocks the next release too." |
| 2:15–2:35 | Lessons Ledger: `.bob/rules/20-lessons.md`, then a new task where Bob uses `safe_load` unprompted | "Every gate run goes into a ledger. Bob turns repeat causes into rules, so the next time someone loads YAML, Bob writes safe code without being told." |
| 2:35–2:50 | `bob_sessions/` screenshots, CI run on GitHub, the Bobcoin total | "All of it is on IBM Bob 2.0: a custom mode, four skills, hooks, parallel subagents, a regulation PDF read natively, and a headless run in CI, using about 11 of 40 Bobcoins." |
| 2:50–3:00 | End card: repo URL and "Days of evidence work → minutes. Deadlines you can't miss." | "Article 14 Gatekeeper: ship fixes, not fines." |

**Before/after numbers to show on screen.** Measure the "before" column once, by hand, with a stopwatch.
- Triage of 12 advisories: every one read by hand → under 1 minute, with file:line evidence
- Advisories needing human reading: 12 → 5
- Art. 14 drafts: typed from a template by hand → generated and completed by Bob in about 5 minutes
