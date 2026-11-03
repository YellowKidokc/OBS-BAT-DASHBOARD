#!/usr/bin/env python3
"""Validate Logos paper YAML frontmatter against schema."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "03_Taxonomy_Naming" / "LOGOS_PAPERS_SCHEMA_V1.yaml"


def extract_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    raw = text[3:end]
    data = yaml.safe_load(raw) or {}
    return data if isinstance(data, dict) else {}


def ensure_list(value):
    return value if isinstance(value, list) else []


def validate(doc: dict, schema: dict) -> list[str]:
    errs: list[str] = []

    for req in schema.get("required", []):
        if req not in doc:
            errs.append(f"missing required field: {req}")

    status = str(doc.get("status", ""))
    allowed_status = schema.get("enums", {}).get("status", [])
    if status and status not in allowed_status:
        errs.append(f"status invalid: {status}")

    paper_number = str(doc.get("paper_number", ""))
    if paper_number and not re.fullmatch(r"P\d{2}", paper_number):
        errs.append("paper_number must match P##")

    cf = ensure_list(doc.get("core_framework", []))
    cmin = schema.get("constraints", {}).get("core_framework_min", 1)
    cmax = schema.get("constraints", {}).get("core_framework_max", 2)
    if len(cf) < cmin or len(cf) > cmax:
        errs.append(f"core_framework count must be {cmin}-{cmax}")

    kw = ensure_list(doc.get("keywords", []))
    kmin = schema.get("constraints", {}).get("keywords_min", 3)
    kmax = schema.get("constraints", {}).get("keywords_max", 5)
    kw_nonempty = [k for k in kw if str(k).strip()]
    if len(kw_nonempty) < kmin or len(kw_nonempty) > kmax:
        errs.append(f"keywords count must be {kmin}-{kmax} non-empty items")

    allowed = schema.get("allowed", {})
    for field in ["core_framework", "isomorphisms", "theology", "trinity", "experiments", "scripture", "mathematics", "bridges"]:
        vals = ensure_list(doc.get(field, []))
        a = set(allowed.get(field, []))
        bad = [v for v in vals if v not in a]
        if bad:
            errs.append(f"{field} has unknown values: {', '.join(map(str, bad))}")

    physics = doc.get("physics", {}) if isinstance(doc.get("physics", {}), dict) else {}
    p_allowed = schema.get("physics_allowed", {})
    for domain, domain_allowed in p_allowed.items():
        vals = ensure_list(physics.get(domain, []))
        bad = [v for v in vals if v not in set(domain_allowed)]
        if bad:
            errs.append(f"physics.{domain} has unknown values: {', '.join(map(str, bad))}")

    pr = doc.get("peer_review", {}) if isinstance(doc.get("peer_review", {}), dict) else {}
    stage = str(pr.get("stage", ""))
    allowed_stage = schema.get("enums", {}).get("peer_review_stage", [])
    if stage and stage not in allowed_stage:
        errs.append(f"peer_review.stage invalid: {stage}")

    return errs


def validate_file(path: Path, schema: dict) -> tuple[bool, list[str]]:
    try:
        data = extract_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception as exc:
        return False, [f"read error: {exc}"]
    if not data:
        return False, ["no YAML frontmatter found"]
    errors = validate(data, schema)
    return len(errors) == 0, errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="Markdown file or folder")
    args = ap.parse_args()

    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    target = Path(args.target)
    files = [target] if target.is_file() else sorted(target.rglob("*.md"))

    failed = 0
    for fp in files:
        ok, errors = validate_file(fp, schema)
        if ok:
            print(f"PASS {fp}")
        else:
            failed += 1
            print(f"FAIL {fp}")
            for e in errors:
                print(f"  - {e}")

    print(f"\nChecked: {len(files)} | Failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
