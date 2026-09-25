---
name: art14-drafter
description: Use after a gate run that produced files in sample-app/release-evidence/art14/<signal>/ — completes every placeholder in early_warning.md, notification.md and final_report.md using gate.json and OSV data.
---

# Art. 14 Drafter

Activate when `sample-app/release-evidence/art14/` contains at least one signal directory with
draft report files.

## Steps

1. **Discover signal directories.**
   List `sample-app/release-evidence/art14/` and note every sub-directory (each is a CVE/signal).
   For each signal, identify which of `early_warning.md`, `notification.md`, `final_report.md`
   are present.

2. **Gather source data.**
   Read:
   - `sample-app/release-evidence/gate.json` — severity, score, affected versions, gate verdict
   - `sample-app/.gatekeeper/osv-cache/<signal>.json` — advisory summary, references, affected
   - `sample-app/gatekeeper.toml` — product name, version, release track, contact details
   - `sample-app/.gatekeeper/signals.json` — signal metadata (deadline fields, notified flag)

3. **Complete each placeholder.**
   For every file found in step 1, read it and replace every placeholder marked with
   angle-bracket `<to complete>` text using the data gathered in step 2.
   - Write factually and concisely; use exact values from the source files.
   - For any field where the required information is genuinely unavailable from the source files,
     replace the placeholder with `[needs human input: <reason>]`.
   - Never fabricate CVSS scores, dates, or affected versions.

4. **Add a "What users should do" section.**
   At the end of each completed document, append a `## What users should do` section with:
   - Recommended upgrade path (package and target version from OSV `fixed` range)
   - Interim mitigations if no fix is available
   - Where to find further information (OSV URL or NVD link from OSV references)

5. **Never mark as submitted.**
   Do not set any `submitted`, `sent`, or `notified` field to `true`. Leave status fields unchanged
   or add `[pending human review]` where a status must be written.

6. **Write the completed files back.**
   Overwrite each file in place using `write_file`. Do not create new directories.

7. **Summarise.**
   Report which files were updated, which placeholders remain as `[needs human input]`, and any
   Art. 14 deadlines parsed from `signals.json` in ISO 8601 UTC format.
