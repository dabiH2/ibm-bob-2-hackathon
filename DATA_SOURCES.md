# Data sources

Hackathon rule: no client data, no confidential data, no personal information, and nothing from social media. Public web data only where its terms allow commercial use.

| Source | URL | License / terms | Used for |
|---|---|---|---|
| OSV.dev vulnerability database | https://osv.dev · https://api.osv.dev | CC-BY 4.0 (attribution: OSV.dev and the upstream GHSA/PyPA advisories) | Advisory lookup; cached records in `sample-app/.gatekeeper/osv-cache/` |
| CISA Known Exploited Vulnerabilities catalog | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | US Government public data (CC0 1.0 on data.gov) | Exploitation signal; 25-entry offline subset in `sample-app/.gatekeeper/kev.json` |
| Regulation (EU) 2024/2847 (Cyber Resilience Act) | https://eur-lex.europa.eu/eli/reg/2024/2847/oj | EUR-Lex reuse policy (Commission Decision 2011/833/EU) | Article references; PDF read by Bob (document understanding) |
| *fattura-lite* demo product, exploitation signal, tenant data | this repository | MIT, synthetic (written by the author) | Demo target |

No personal data is processed. The e-invoicing gateway URL uses the reserved `.invalid` domain, and every submission runs in dry-run mode.
