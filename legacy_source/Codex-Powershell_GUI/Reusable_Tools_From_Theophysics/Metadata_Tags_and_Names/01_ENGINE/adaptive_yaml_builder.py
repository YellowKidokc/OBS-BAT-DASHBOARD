#!/usr/bin/env python3
"""
adaptive_yaml_builder.py

Suggestion-based YAML frontmatter builder for large schemas.
- Learns frequently used values per field
- Carries forward selected tags automatically
- Walks row-by-row with "done with this row?"
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = SCRIPT_DIR / "adaptive_yaml_schema.yaml"
MEMORY_PATH = SCRIPT_DIR / "adaptive_yaml_memory.json"
TAXONOMY_PATH = SCRIPT_DIR / "tags_taxonomy.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8", errors="ignore")) or {}
    return data if isinstance(data, dict) else {}


def load_memory() -> dict[str, Any]:
    if not MEMORY_PATH.exists():
        return {"field_usage": {}, "field_last": {}, "carry_forward_tags": []}
    try:
        obj = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
        if not isinstance(obj, dict):
            raise ValueError("memory must be object")
        obj.setdefault("field_usage", {})
        obj.setdefault("field_last", {})
        obj.setdefault("carry_forward_tags", [])
        return obj
    except Exception:
        return {"field_usage": {}, "field_last": {}, "carry_forward_tags": []}


def save_memory(mem: dict[str, Any]) -> None:
    MEMORY_PATH.write_text(json.dumps(mem, indent=2), encoding="utf-8")


def flatten_taxonomy_tags() -> list[str]:
    data = load_yaml(TAXONOMY_PATH)
    domains = data.get("domains", {})
    out: list[str] = []
    if isinstance(domains, dict):
        for _, cats in domains.items():
            if not isinstance(cats, dict):
                continue
            for _, tags in cats.items():
                if isinstance(tags, list):
                    out.extend([str(t).strip() for t in tags if str(t).strip()])
    return sorted(set(out))


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            raw = text[3:end]
            body = text[end + 4 :].lstrip("\n")
            fm = yaml.safe_load(raw) or {}
            if isinstance(fm, dict):
                return fm, body
    return {}, text


def dump_frontmatter(fm: dict[str, Any], body: str) -> str:
    y = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{y}\n---\n\n{body}"


def pick_target(arg: str | None) -> Path:
    if arg:
        p = Path(arg)
    else:
        raw = input("Target markdown file path: ").strip()
        p = Path(raw)
    if not p.exists() or not p.is_file():
        raise SystemExit(f"Target file not found: {p}")
    return p


def as_list(v: Any) -> list[str]:
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    if isinstance(v, str) and v.strip():
        return [v.strip()]
    return []


def update_usage(mem: dict[str, Any], field: str, values: list[str]) -> None:
    fu = mem.setdefault("field_usage", {}).setdefault(field, {})
    for v in values:
        fu[v] = int(fu.get(v, 0)) + 1
    mem.setdefault("field_last", {})[field] = values


def get_options(field_cfg: dict[str, Any], taxonomy_tags: list[str]) -> list[str]:
    src = str(field_cfg.get("options_source", ""))
    if src == "taxonomy_tags":
        return taxonomy_tags
    opts = field_cfg.get("options", [])
    if isinstance(opts, list):
        return [str(x).strip() for x in opts if str(x).strip()]
    return []


def top_usage(mem: dict[str, Any], field: str) -> list[str]:
    fu = mem.get("field_usage", {}).get(field, {})
    if not isinstance(fu, dict):
        return []
    items = sorted(fu.items(), key=lambda kv: (-int(kv[1]), kv[0]))
    return [k for k, _ in items]


def build_suggestions(field: str, selected: list[str], options: list[str], mem: dict[str, Any], limit: int = 12) -> list[str]:
    seen = set()
    out: list[str] = []

    def add(v: str):
        if v and v not in seen:
            seen.add(v)
            out.append(v)

    for x in selected:
        add(x)
    for x in as_list(mem.get("field_last", {}).get(field, [])):
        add(x)
    for x in top_usage(mem, field):
        add(x)
    for x in options:
        add(x)

    return out[:limit]


def row_loop_list(field_cfg: dict[str, Any], fm: dict[str, Any], mem: dict[str, Any], taxonomy_tags: list[str]) -> list[str]:
    name = str(field_cfg["name"])
    prompt = str(field_cfg.get("prompt", name))
    carry_forward = bool(field_cfg.get("carry_forward", False))
    selected = as_list(fm.get(name, []))

    if carry_forward and name == "tags":
        cf = as_list(mem.get("carry_forward_tags", []))
        selected = sorted(set(selected).union(cf))

    options = get_options(field_cfg, taxonomy_tags)

    while True:
        suggestions = build_suggestions(name, selected, options, mem, int(field_cfg.get("max_suggestions", 14)))
        print("\n" + "=" * 72)
        print(f"ROW: {name}")
        print(prompt)
        print("Selected:", selected if selected else "[]")
        print("Suggestions:")
        for i, s in enumerate(suggestions, 1):
            mark = "x" if s in selected else " "
            print(f"  {i:>2}. [{mark}] {s}")
        print("Commands: numbers toggle | +value add | -value remove | /text search | done")

        cmd = input("> ").strip()
        if cmd == "" or cmd.lower() == "done":
            done = input(f"Done with row '{name}'? [Y/n]: ").strip().lower()
            if done in ("", "y", "yes"):
                break
            continue

        if cmd.startswith("/"):
            q = cmd[1:].strip().lower()
            if q:
                filtered = [o for o in options if q in o.lower()][:20]
                if filtered:
                    print("Matches:")
                    for i, o in enumerate(filtered, 1):
                        print(f"  {i:>2}. {o}")
                else:
                    print("No matches.")
            continue

        if cmd.startswith("+"):
            v = cmd[1:].strip()
            if v and v not in selected:
                selected.append(v)
            continue

        if cmd.startswith("-"):
            v = cmd[1:].strip()
            selected = [x for x in selected if x != v]
            continue

        nums = re.findall(r"\d+", cmd)
        if nums:
            for n in nums:
                idx = int(n) - 1
                if 0 <= idx < len(suggestions):
                    val = suggestions[idx]
                    if val in selected:
                        selected.remove(val)
                    else:
                        selected.append(val)
            selected = sorted(set(selected))
            continue

        print("Unrecognized command.")

    selected = sorted(set([x for x in selected if x]))
    update_usage(mem, name, selected)
    if carry_forward and name == "tags":
        mem["carry_forward_tags"] = selected
    return selected


def row_loop_scalar(field_cfg: dict[str, Any], fm: dict[str, Any], mem: dict[str, Any]) -> str:
    name = str(field_cfg["name"])
    prompt = str(field_cfg.get("prompt", name))
    current = str(fm.get(name, field_cfg.get("default", "")) or "")
    last = as_list(mem.get("field_last", {}).get(name, []))
    default = last[0] if last else current

    while True:
        print("\n" + "=" * 72)
        print(f"ROW: {name}")
        print(prompt)
        print(f"Current: {current!r}")
        if default:
            print(f"Suggested default: {default!r}")
        raw = input("Value (Enter keeps suggested/current): ").strip()
        val = raw if raw else (default if default else current)
        done = input(f"Done with row '{name}'? [Y/n]: ").strip().lower()
        if done in ("", "y", "yes"):
            update_usage(mem, name, [val] if val else [])
            return val


def main() -> int:
    target_arg = sys.argv[1] if len(sys.argv) > 1 else None
    target = pick_target(target_arg)

    schema = load_yaml(SCHEMA_PATH)
    fields = schema.get("fields", []) if isinstance(schema.get("fields", []), list) else []
    if not fields:
        raise SystemExit(f"No fields found in schema: {SCHEMA_PATH}")

    taxonomy_tags = flatten_taxonomy_tags()
    mem = load_memory()

    raw = target.read_text(encoding="utf-8", errors="ignore")
    fm, body = parse_frontmatter(raw)

    print(f"\nAdaptive YAML Builder\nTarget: {target}\n")

    for field_cfg in fields:
        if not isinstance(field_cfg, dict) or "name" not in field_cfg:
            continue
        name = str(field_cfg["name"])
        kind = str(field_cfg.get("kind", "list"))

        if kind == "list":
            fm[name] = row_loop_list(field_cfg, fm, mem, taxonomy_tags)
        else:
            fm[name] = row_loop_scalar(field_cfg, fm, mem)

    target.write_text(dump_frontmatter(fm, body), encoding="utf-8")
    save_memory(mem)

    print("\nSaved frontmatter and updated suggestion memory.")
    print(f"Memory: {MEMORY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
