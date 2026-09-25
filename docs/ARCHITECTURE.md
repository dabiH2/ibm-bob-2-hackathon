# Architecture

```mermaid
flowchart LR
  subgraph Inputs
    R[requirements.txt] --> S
    SRC[app/*.py]
    SIG[.gatekeeper/signals.json<br/>exploitation intake]
    KEV[(CISA KEV)]
    OSV[(OSV.dev)]
  end
  S[sbom.py<br/>CycloneDX 1.5] --> O[osv.py<br/>merge GHSA/PYSEC by CVE]
  OSV --> O
  O --> RE[reach.py<br/>AST import + symbol use]
  SRC --> RE
  RE --> V[vex.py<br/>OpenVEX 0.2.0 + reviewed overrides]
  SIG --> A[art14.py<br/>24h / 72h / fix+14d clocks + drafts]
  KEV --> A
  V --> G{gate.py<br/>policy}
  A --> G
  G -->|exit 0 / 1| OUT[release-evidence/<br/>sbom · vex · gate.json · art14/*.md · index.html]
  G --> L[.gatekeeper/ledger.jsonl<br/>Lessons Ledger]

  subgraph Bob[IBM Bob 2.0 agent layer]
    M[mode: cra-release-officer]
    AA[skill: advisory-analyst] -->|symbols.local.json · vex_overrides.json| RE
    AD[skill: art14-drafter] -->|completes drafts| OUT
    LC[skill: lessons-curator] -->|.bob/rules/20-lessons.md| M
    H[hook: PreToolUse git push/tag] -->|exit 2 on BLOCK| G
  end
  L --> LC
```

## Design choices
- **Deterministic core, agentic edges.** Decisions that must be auditable are pure functions of their inputs: which versions ship, which advisories apply, and which deadlines are running. Bob handles the judgement work: mapping a new advisory to code, writing the justification, drafting the reports and fixing the code. Every Bob judgement lands in a reviewed JSON file that includes an author and a reason, and it can be rolled back.
- **Blocks on uncertainty.** An advisory nobody has mapped yet (`UNKNOWN`) is treated as `under_investigation`, and that blocks the release. The gate never assumes "not affected".
- **Clocks survive the fix.** Removing the vulnerable version starts the 14-day final-report clock. The 24 h and 72 h obligations stay open until they are marked submitted in `signals.json`.
- **No dependencies.** It uses only the Python ≥ 3.11 standard library, runs offline from cache, and returns the decision as an exit code, so it fits a git hook, CI or a Bob hook alike.
