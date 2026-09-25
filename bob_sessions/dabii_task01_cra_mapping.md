# Read the regulation PDF docs/regulation/CRA_2024-2847.pdf (Regulation (EU) 2024/2847, the Cyber Resilience Act) and the Python package in the gatekeeper/ folder. Then create docs/CRA_MAPPING.md containing a markdown table that maps each of these provisions to what Article 14 Gatekeeper produces (file name and field): Art. 13(6), Art. 13(8), Art. 14(1), Art. 14(2)(a), Art. 14(2)(b), Art. 14(2)(c), Art. 14(8), Art. 16, and Annex I Part II points (1) to (8). Columns: Provision | What the law requires (one sentence, max one short quote) | Gatekeeper output (file/field) | Status (covered / partial / not covered) | Gap or next step. Base every row on the actual PDF text and the actual code, do not invent articles. End with a short summary of the top 3 gaps.

---

**Status:** active  **Date:** 2026-09-25

---

### 👤 User

Read the regulation PDF docs/regulation/CRA_2024-2847.pdf (Regulation (EU) 2024/2847, the Cyber Resilience Act) and the Python package in the gatekeeper/ folder. Then create docs/CRA_MAPPING.md containing a markdown table that maps each of these provisions to what Article 14 Gatekeeper produces (file name and field): Art. 13(6), Art. 13(8), Art. 14(1), Art. 14(2)(a), Art. 14(2)(b), Art. 14(2)(c), Art. 14(8), Art. 16, and Annex I Part II points (1) to (8). Columns: Provision | What the law requires (one sentence, max one short quote) | Gatekeeper output (file/field) | Status (covered / partial / not covered) | Gap or next step. Base every row on the actual PDF text and the actual code, do not invent articles. End with a short summary of the top 3 gaps.

---

### 🤖 Assistant

> 🔧 called: read_file, list_files



> 🔧 **list_files** — gatekeeper

> 🔧 **read_file** — docs/regulation/CRA_2024-2847.pdf

### 🤖 Assistant

> 🔧 called: read_file, GetSymbolsOverview, GetSymbolsOverview, GetSymbolsOverview, GetSymbolsOverview, GetSymbolsOverview, GetSymbolsOverview, GetSymbolsOverview

Now let me read the key articles from the regulation PDF and all the gatekeeper source files in parallel:

> 🔧 **GetSymbolsOverview** — gatekeeper/sbom.py

> 🔧 **read_file** — docs/regulation/CRA_2024-2847.pdf

> 🔧 **GetSymbolsOverview** — gatekeeper/art14.py

> 🔧 **GetSymbolsOverview** — gatekeeper/vex.py

> 🔧 **GetSymbolsOverview** — gatekeeper/reach.py

> 🔧 **GetSymbolsOverview** — gatekeeper/gate.py

> 🔧 **GetSymbolsOverview** — gatekeeper/osv.py

> 🔧 **GetSymbolsOverview** — gatekeeper/report.py

### 🤖 Assistant

> 🔧 called: read_file, read_file, read_file, read_file, read_file, read_file, read_file, read_file



> 🔧 **read_file** — gatekeeper/gate.py

> 🔧 **read_file** — gatekeeper/art14.py

> 🔧 **read_file** — gatekeeper/report.py

> 🔧 **read_file** — gatekeeper/sbom.py

> 🔧 **read_file** — gatekeeper/osv.py

> 🔧 **read_file** — gatekeeper/vex.py

> 🔧 **read_file** — gatekeeper/reach.py

> 🔧 **read_file** — gatekeeper/__main__.py

### 🤖 Assistant

> 🔧 called: read_file

Now let me read the key CRA articles from the PDF:

> 🔧 **read_file** — docs/regulation/CRA_2024-2847.pdf

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — docs/regulation/CRA_2024-2847.pdf

### 🤖 Assistant

> 🔧 called: grep

Now let me find the actual Article 13, 14, 16, and Annex I Part II text:

> 🔧 **grep** — Article 13|Article 14|Article 16|Annex I

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — docs/regulation/CRA_2024-2847.pdf

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — docs/regulation/CRA_2024-2847.pdf

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — docs/regulation/CRA_2024-2847.pdf

### 🤖 Assistant

> 🔧 called: read_file

Now I have enough. Let me also quickly check Annex I Part II:

> 🔧 **read_file** — docs/regulation/CRA_2024-2847.pdf

### 🤖 Assistant

> 🔧 called: write_file

I now have everything I need. Let me write the mapping document:

> 🔧 **write_file** — docs/CRA_MAPPING.md

### 🤖 Assistant

[`docs/CRA_MAPPING.md`](docs/CRA_MAPPING.md) is written. Here's what the mapping is based on and what it found:

---

### What was read
| Source | Key evidence found |
|---|---|
| `CRA_2024-2847.pdf` lines 2177–2271 | Full Art. 14 text: three-stage notification (24 h / 72 h / 14 d), Art. 14(8) user-notification, Art. 14(1) CSIRT+ENISA obligation |
| `CRA_2024-2847.pdf` lines 2051–2056 | Art. 13(6): upstream component disclosure requirement |
| `CRA_2024-2847.pdf` lines 2061–2083 | Art. 13(8): support-period CVD policy obligation |
| `CRA_2024-2847.pdf` lines 2299–2356 | Art. 16: single reporting platform established by ENISA |
| `CRA_2024-2847.pdf` lines 3565–3593 | Annex I Part II (1)–(8): full vulnerability-handling requirements |
| `gatekeeper/art14.py` | Implements `Clock`, `drafts()` — generates the three Art. 14 report scaffolds |
| `gatekeeper/sbom.py` | Produces CycloneDX 1.5 `sbom.cdx.json` — covers Annex I Part II(1) |
| `gatekeeper/osv.py` | Fetches OSV.dev advisories → `Finding` objects with severity, fix versions |
| `gatekeeper/reach.py` | Static reachability analysis → `NOT_IMPORTED / NOT_CALLED / REACHABLE / UNKNOWN` |
| `gatekeeper/vex.py` | Emits OpenVEX 0.2.0 statements — covers Annex I Part II(2) action statements |
| `gatekeeper/gate.py` | Orchestrates the pipeline, writes `gate.json`, enforces policy thresholds |

### Top 3 gaps (from the document)
1. **No public advisory artefact** — Annex I Part II(4) & (8) require public disclosure of fixed-vuln info and user-facing advisory messages; Gatekeeper produces only internal VEX/reports.
2. **No CVD policy validation** — Annex I Part II(5) & Art. 13(8) require a published coordinated vulnerability disclosure policy with a contact address; Gatekeeper never checks for it.
3. **No upstream disclosure tracking** — Art. 13(6) requires notifying component maintainers; Gatekeeper identifies the affected component and fix version but never creates or tracks that notification.