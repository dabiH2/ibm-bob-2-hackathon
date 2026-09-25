"""Build a CycloneDX 1.5 SBOM from a Python requirements file."""
from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

_REQ = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*==\s*([A-Za-z0-9._+!-]+)")


@dataclass(frozen=True)
class Component:
    name: str      # normalised distribution name (PEP 503)
    version: str
    ecosystem: str = "PyPI"

    @property
    def purl(self) -> str:
        return f"pkg:pypi/{self.name}@{self.version}"


def normalise(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_requirements(path: Path) -> tuple[list[Component], list[str]]:
    """Return pinned components and a list of warnings for unpinned lines.

    CRA Annex I Part II(1) asks for an SBOM covering at least top-level
    dependencies, so unpinned requirements are reported rather than guessed.
    """
    comps: list[Component] = []
    warnings: list[str] = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith(("-", "--")):
            continue
        m = _REQ.match(line)
        if m:
            comps.append(Component(normalise(m.group(1)), m.group(2)))
        else:
            warnings.append(f"{path.name}:{n}: not pinned with '==' ({line}); version cannot be attested")
    return comps, warnings


def cyclonedx(components: list[Component], product: dict) -> dict:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{uuid.uuid4()}",
        "version": 1,
        "metadata": {
            "timestamp": now,
            "tools": {"components": [{"type": "application", "name": "article14-gatekeeper"}]},
            "component": {
                "type": "application",
                "name": product.get("name", "unknown"),
                "version": product.get("version", "0.0.0"),
                "supplier": {"name": product.get("manufacturer", "unknown")},
            },
        },
        "components": [
            {"type": "library", "name": c.name, "version": c.version, "purl": c.purl, "bom-ref": c.purl}
            for c in components
        ],
    }


def write(sbom: dict, out: Path) -> Path:
    out.write_text(json.dumps(sbom, indent=2), encoding="utf-8")
    return out
