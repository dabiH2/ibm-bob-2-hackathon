# Vulnerability notification — Art. 14(2)(b) — due 2026-09-28 14:54 UTC

Product: fattura-lite 1.4.1 — manufacturer: Dabii Systems (demo, fictional product)
Vulnerability: CVE-2020-14343
Aware of active exploitation since: 2026-09-25 14:54 UTC (signal SIG-2026-0001, source: synthetic demo signal: customer SOC reported malicious tenant YAML uploads)
Recipients: CSIRT designated as coordinator + ENISA, via the single reporting platform (Art. 16)

## General information about the product concerned
Microservice that validates e-invoices and forwards them to an e-invoicing gateway. Sold to SMEs in IT, DE and ES.

## General nature of the exploit and of the vulnerability
Arbitrary code execution when untrusted YAML is loaded with FullLoader (PyYAML < 5.4).
The vulnerability arises because `yaml.load()` with `FullLoader` deserialises arbitrary Python
constructors present in the YAML stream. Tenant-supplied YAML invoice data reaches this code path
directly; no authentication bypass is required once a tenant account exists.
Severity: CRITICAL (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)

## Corrective or mitigating measures taken
Upgraded pyyaml from 5.3.1 to 6.0.2 and replaced `yaml.load(fh, Loader=yaml.FullLoader)` with
`yaml.safe_load(fh)` in `app/config.py`. The corrective measure was included in release 1.4.1,
available since 2026-09-25 17:59 UTC.

## Corrective or mitigating measures users can take
- Upgrade to fattura-lite 1.4.1 or later (ships pyyaml 6.0.2).
- If immediate upgrade is not possible: restrict or disable the YAML invoice-upload endpoint at the
  network perimeter (WAF/API gateway rule) until the patch can be applied.
- Rotate any secrets or credentials that may have been exposed if exploitation is suspected.

## Sensitivity of the notified information
TLP:AMBER until the fix is released

## What users should do
- **Upgrade immediately** to fattura-lite 1.4.1 or later.
- **Further information**: https://osv.dev/vulnerability/CVE-2020-14343
  and https://nvd.nist.gov/vuln/detail/CVE-2020-14343

Status: [pending human review]
