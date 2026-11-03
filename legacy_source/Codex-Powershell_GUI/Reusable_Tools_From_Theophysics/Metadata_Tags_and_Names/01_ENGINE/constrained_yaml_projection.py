#!/usr/bin/env python3
"""
constrained_yaml_projection.py

Starter scaffold for YAML Plugin V2.

This script is intentionally conservative:
- loads the v2 schema
- parses a markdown note
- extracts frontmatter and body
- returns a structured placeholder projection payload

The scoring, alias matching, and full ontology loading stages still need implementation.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "yaml_plugin_v2_schema.yaml"


@dataclass
class ProjectionResult:
    source_file: str
    mode: str
    frontmatter_present: bool
    title: str | None = None
    entity_type: str | None = None
    domain: list[str] = field(default_factory=list)
    kept: list[dict[str, Any]] = field(default_factory=list)
    removed: list[dict[str, Any]] = field(default_factory=list)
    ambiguous: list[dict[str, Any]] = field(default_factory=list)
    missing_but_expected: list[str] = field(default_factory=list)


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def parse_markdown(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
      return {}, text

    end = text.find("\n---", 3)
    if end == -1:
      return {}, text

    raw = text[3:end]
    body = text[end + 4 :].lstrip("\n")
    frontmatter = yaml.safe_load(raw) or {}
    if not isinstance(frontmatter, dict):
      frontmatter = {}
    return frontmatter, body


def project_fields(frontmatter: dict[str, Any], mode: str) -> ProjectionResult:
    result = ProjectionResult(
        source_file="",
        mode=mode,
        frontmatter_present=bool(frontmatter),
        title=frontmatter.get("title"),
        entity_type=frontmatter.get("entity_type"),
        domain=frontmatter.get("domain", []) if isinstance(frontmatter.get("domain"), list) else [],
    )

    for field_name in ["id", "title", "entity_type", "domain", "claim_type", "proof_status"]:
        if field_name in frontmatter:
            result.kept.append(
                {
                    "field": field_name,
                    "value": frontmatter[field_name],
                    "reason": "existing_frontmatter",
                    "support_band": "explicit",
                }
            )
        else:
            result.missing_but_expected.append(field_name)

    return result


def write_sidecars(result: ProjectionResult, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    classification_path = output_dir / f"{stem}.classification.json"
    audit_path = output_dir / f"{stem}.audit.md"

    classification_path.write_text(json.dumps(asdict(result), indent=2), encoding="utf-8")

    audit = [
        f"# YAML Projection Audit",
        "",
        f"- Source: `{result.source_file}`",
        f"- Mode: `{result.mode}`",
        f"- Frontmatter present: `{result.frontmatter_present}`",
        "",
        "## Kept",
    ]

    if result.kept:
        for item in result.kept:
            audit.append(f"- `{item['field']}` kept as `{item['support_band']}` via `{item['reason']}`")
    else:
        audit.append("- none")

    audit.extend(["", "## Removed"])
    if result.removed:
        for item in result.removed:
            audit.append(f"- `{item['field']}` removed: {item['reason']}")
    else:
        audit.append("- none")

    audit.extend(["", "## Ambiguous"])
    if result.ambiguous:
        for item in result.ambiguous:
            audit.append(f"- `{item['field']}` ambiguous: {item['reason']}")
    else:
        audit.append("- none")

    audit.extend(["", "## Missing But Expected"])
    if result.missing_but_expected:
        for field_name in result.missing_but_expected:
            audit.append(f"- `{field_name}`")
    else:
        audit.append("- none")

    audit_path.write_text("\n".join(audit) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Starter scaffold for YAML Plugin V2")
    parser.add_argument("target", help="Markdown file to inspect")
    parser.add_argument("--mode", choices=["strict", "assisted", "discovery"], default="assisted")
    parser.add_argument("--output-dir", default=str(ROOT / "yaml_plugin_v2_output"))
    args = parser.parse_args()

    _schema = load_yaml(SCHEMA_PATH)
    target = Path(args.target)
    frontmatter, _body = parse_markdown(target)
    result = project_fields(frontmatter, args.mode)
    result.source_file = str(target)

    output_dir = Path(args.output_dir)
    write_sidecars(result, output_dir, target.stem)

    print(json.dumps(asdict(result), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
