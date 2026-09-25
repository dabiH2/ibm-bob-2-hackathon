"""Forward validated invoices to the e-invoicing gateway."""
import requests

GATEWAY = "https://gateway.example.invalid/api/v1/invoices"


class GatewayClient:
    def __init__(self, token):
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {token}"

    def submit(self, invoice_xml, dry_run=True):
        if dry_run:
            return {"status": "dry-run", "bytes": len(invoice_xml)}
        resp = self.session.post(GATEWAY, data=invoice_xml, timeout=10,
                                 headers={"Content-Type": "application/xml"})
        resp.raise_for_status()
        return resp.json()
