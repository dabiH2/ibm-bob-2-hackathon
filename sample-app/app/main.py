"""Tiny CLI entry point: validate and forward one invoice (dry run by default)."""
import sys

from app.config import load_tenant_config
from app.gateway_client import GatewayClient
from app.render import summary


def main(cfg_path, invoice_path):
    cfg = load_tenant_config(cfg_path)
    with open(invoice_path, encoding="utf-8") as fh:
        xml = fh.read()
    print(summary({"number": cfg.get("next_number", 1), "customer": cfg.get("tenant", "?"), "total": "0.00"}))
    print(GatewayClient(cfg.get("token", "demo")).submit(xml, dry_run=True))


if __name__ == "__main__":
    main(*sys.argv[1:3])
