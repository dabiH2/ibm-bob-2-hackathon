# Early warning — Art. 14(2)(a) — due 2026-09-26 14:54 UTC

Product: fattura-lite 1.4.1 — manufacturer: Dabii Systems (demo, fictional product)
Vulnerability: CVE-2020-14343
Aware of active exploitation since: 2026-09-25 14:54 UTC (signal SIG-2026-0001, source: synthetic demo signal: customer SOC reported malicious tenant YAML uploads)
Recipients: CSIRT designated as coordinator + ENISA, via the single reporting platform (Art. 16)

## Member States where the product has been made available
IT, DE, ES

## Short description
Active exploitation of CVE-2020-14343 in component pyyaml 5.3.1.
Attackers are uploading maliciously crafted YAML documents via the tenant invoice-upload endpoint.
When the application parses these documents using `yaml.load()` with `FullLoader`, arbitrary Python
objects can be instantiated, enabling remote code execution within the service process.
A corrective measure (upgrade to pyyaml >= 6.0.2, using `yaml.safe_load()`) was made available in
release 1.4.1 on 2026-09-25 17:59 UTC. Affected versions of fattura-lite are all releases shipping
pyyaml < 5.4 (prior to 1.4.1).

## What users should do
- **Upgrade immediately** to fattura-lite 1.4.1 or later, which ships pyyaml 6.0.2 and removes the
  vulnerable call site.
- **Interim mitigation** (if upgrade is not immediately possible): block multipart/form-data YAML
  uploads at the API gateway or WAF until the upgraded release is deployed.
- **Further information**: https://osv.dev/vulnerability/CVE-2020-14343
  and https://nvd.nist.gov/vuln/detail/CVE-2020-14343

Status: [pending human review]
