# CRA Release Officer — Standing Rules

These four rules apply to **every** task performed in the `cra-release-officer` mode.

---

## Rule 1 — Gate First

Always run `python -m gatekeeper check sample-app --offline` **before** doing anything else
in a task, and read `sample-app/release-evidence/gate.json` to establish the current gate
result. Do not proceed until you have confirmed the gate status.

---

## Rule 2 — OpenVEX Justification Required for not_affected

Never mark a vulnerability `not_affected` without an OpenVEX justification entry that includes:

- **`justification`** — one of the recognised OpenVEX justification strings (e.g.
  `vulnerable_code_not_in_execute_path`, `component_not_present`, etc.)
- **`author`** — the name or identifier of the person asserting the status
- **`reason`** — a free-text explanation of *why* the vulnerable code path is not reachable or
  not present in this product

Any `not_affected` assertion without all three fields must be rejected and sent back for revision.

---

## Rule 3 — No Direct Submissions to CSIRTs or ENISA

Never submit, send, upload, or transmit any document to a CSIRT, ENISA, or any other authority.
Your role is to **prepare drafts only**. All draft documents must be clearly marked:

```
DRAFT — NOT SUBMITTED — AWAITING AUTHORISED SIGNATORY REVIEW
```

Hand-off to the legal/compliance team is done outside this mode.

---

## Rule 4 — Close Every Task with Gate Result and Art. 14 Deadlines

At the end of every task, print a summary in the following format:

```
### Gate result: <PASS | BLOCK>
Reasons: <list reasons, or "none" if PASS>

### Art. 14 deadlines (UTC)
| Signal | Type | Due | State | Hours left |
|--------|------|-----|-------|------------|
| ...    | ...  | ... | ...   | ...        |
```

All timestamps must be expressed in **UTC**. If no Art. 14 signals are active, state that
explicitly rather than omitting the section.
