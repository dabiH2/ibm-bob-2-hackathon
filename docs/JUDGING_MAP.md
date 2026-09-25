# Judging map — Article 14 Gatekeeper

The four official criteria from the lablab event page. No weights are published, so treat them as equal.
Scores are an honest self-assessment, estimated for when the Bob layer (playbook T01–T08) is done. Revisit them after T05.

| Criterion | Official wording | Est. score | Status |
|---|---|---|---|
| Application of Technology | How complete and well thought-out the project is, with a clear application of IBM Bob 2.0 | 4 → 5 after T02–T05 | Depends on the Bob tasks |
| Presentation | The clarity and effectiveness of the project presentation | 4 | Script and cover ready |
| Business Value | Impact and practical value on a high-priority issue | 5 | Strongest |
| Originality | Uniqueness and creativity of the solution and of how it applies Bob 2.0 | 4.5 | Strong |

---

## 1. Application of Technology
**Why it's strong.** Bob is the operator, not decoration. The brief names Agent mode, parallel tasks, subagents and document understanding, and all four appear in T05 (three parallel subagents) and T01 (Bob reads the CRA PDF). On top of those:
- custom mode `cra-release-officer` (T02)
- skills (T03, T07)
- hooks that block a non-compliant `git push` or `git tag` (T04)
- headless Bob in CI (T06)

May's winner, Pedigree, showed custom modes, MCP and Skills; this covers more of Bob's feature set.

**Evidence judges can check.**
- `bob_sessions/` screenshots for T01–T08
- the `.bob/` configs
- the working gate with passing tests
- the CI workflow

**Risk.** The deterministic core was written before kickoff (allowed, and disclosed). If the Bob layer is thin, the project reads as "a Python tool with some Bob sprinkled on".

**Actions.**
- Make T05 the centrepiece of the video.
- Spend Bobcoins on subagents and hooks first.
- Keep the division-of-labour sentence in the Bob Usage Statement.

## 2. Presentation
**Why it's strong.** The story has natural drama: a legal clock ticking, then a red BLOCK, then a green PASS minutes later. The HTML report has live countdowns and file:line evidence. The cover (`submission/cover.png`) and the second-by-second script (`docs/DEMO_SCRIPT.md`) are ready.

**Risk.** CRA jargon (VEX, SBOM, Art. 14(2)(b)) loses judges in the first 20 seconds, and they watch many screen recordings.

**Actions.**
- Open with one plain line: "24 hours to report, or up to €15M in fines".
- Show the three clocks before any acronym.
- Put the before/after numbers on screen as captions, not only in the narration.
- Keep the video to 3:00 or less, with at least 90 s of live demo.

## 3. Business Value
**Why it's strong.**
- The reporting duty has applied since 11 Sep 2026, to every manufacturer selling software with digital elements in the EU, and the penalties are real.
- The judges are mostly senior engineers from regulated or security-heavy companies (AmEx, PayPal, Prudential, Palo Alto Networks, Walmart, Uber). This is their problem.
- It cuts review noise: of 12 advisories, only 5 needed a human.

**Risk.** The time-saved claims stay estimates until they are measured.

**Actions.**
- Time the manual baseline once with a stopwatch (run sheet, Sat 15:30).
- Put the real numbers into `docs/SUBMISSION.md`, `docs/DEMO_SCRIPT.md` and the slides. Measured numbers beat claimed ones.

## 4. Originality
**Why it's strong.** None of May's 503 projects did CRA compliance, and this one stays clear of the crowded categories (onboarding, repo explainers). What makes it different:
- clocks that keep running after the fix (the 14-day final report starts when the fix ships)
- a hook that makes Bob itself refuse to ship a non-compliant release
- a Lessons Ledger that turns past failures into Bob rules

**Risk.** It follows the same pattern as May's winner (an EU regulation plus a release gate), so a judge could see it as a remix.

**Actions.**
- Name the difference in the pitch: "May's winner proved where AI code came from. We prove whether you're allowed to ship it."
- Lean on what Pedigree didn't have: parallel subagents, the ticking clocks, and self-improvement through the ledger.

---

## Priority if time or Bobcoins run short
1. **T05 on camera.** It carries Application of Technology and Presentation.
2. **The measured baseline.** It carries Business Value.
3. **The pitch line against May's winner.** It carries Originality.
4. Everything else.
