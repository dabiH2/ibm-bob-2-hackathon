"""Endpoint: import tenant settings from an uploaded YAML file."""
import io
import yaml


def import_tenant_settings(file_obj, existing: dict | None = None) -> dict:
    """Parse *file_obj* (a file-like object) as YAML and merge into *existing*.

    Returns the merged settings dict.
    Raises ValueError for non-mapping documents or YAML parse errors.
    """
    try:
        data = yaml.safe_load(file_obj)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Tenant settings file must be a YAML mapping at the top level.")

    merged = dict(existing or {})
    merged.update(data)
    return merged


def import_tenant_settings_bytes(raw: bytes, existing: dict | None = None) -> dict:
    """Convenience wrapper that accepts raw bytes instead of a file object."""
    return import_tenant_settings(io.BytesIO(raw), existing)
