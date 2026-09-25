"""Load tenant configuration files uploaded by customers."""
import yaml


def load_tenant_config(path):
    with open(path, encoding="utf-8") as fh:
        # Tenant files come from customer uploads, so this input is untrusted.
        return yaml.safe_load(fh)
