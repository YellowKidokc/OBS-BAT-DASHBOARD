#!/usr/bin/env python3
"""
tag_workbench.py

Unified launcher for YAML tagging/classification workflows:
1) Taxonomy tags + images (yaml_tagger.py)
2) Excel code classifications (excel_tagger.py)
3) Full pass: tags/images -> excel classifications
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
YAML_TAGGER = ENGINE_DIR / "yaml_tagger.py"
EXCEL_TAGGER = ENGINE_DIR / "excel_tagger.py"


def run_cmd(args: list[str]) -> int:
    print("\n[run]", " ".join(f'"{a}"' if " " in a else a for a in args))
    return subprocess.call(args)


def pick_file_from_folder(folder: Path) -> Path | None:
    files = sorted(folder.glob("*.md"))
    if not files:
        files = sorted(folder.rglob("*.md"))[:200]
    if not files:
        print(f"No markdown files found in {folder}")
        return None

    print("\nPick file:")
    for i, f in enumerate(files, 1):
        print(f"  {i:>3}. {f}")

    while True:
        raw = input("File number (or Enter to cancel): ").strip()
        if not raw:
            return None
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(files):
                return files[idx]
        print("Invalid choice.")


def resolve_target(path_arg: str | None) -> Path | None:
    if not path_arg:
        raw = input("\nTarget file or folder (blank = current folder): ").strip()
        path = Path(raw) if raw else Path(".")
    else:
        path = Path(path_arg)

    if path.is_file():
        return path
    if path.is_dir():
        return pick_file_from_folder(path)

    alt = path.with_suffix(".md")
    if alt.exists():
        return alt
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="Target markdown file or folder")
    ap.add_argument("--mode", choices=["tags", "codes", "full"], help="Run mode")
    args = ap.parse_args()

    if not YAML_TAGGER.exists() or not EXCEL_TAGGER.exists():
        print("Missing required scripts in engine folder.")
        return 1

    mode = args.mode
    if not mode:
        print("\nTag Workbench")
        print("  1) Tags + images (taxonomy)")
        print("  2) Excel code classifications")
        print("  3) Full pass (tags/images -> codes)")
        raw = input("Choose 1/2/3: ").strip()
        mode = {"1": "tags", "2": "codes", "3": "full"}.get(raw)
        if not mode:
            print("Canceled.")
            return 0

    target = resolve_target(args.target)
    if not target:
        print("No valid target selected.")
        return 1

    py = sys.executable

    if mode == "tags":
        return run_cmd([py, str(YAML_TAGGER), str(target)])

    if mode == "codes":
        return run_cmd([py, str(EXCEL_TAGGER), "--file", str(target)])

    rc1 = run_cmd([py, str(YAML_TAGGER), str(target)])
    if rc1 != 0:
        print("Tag phase failed; stopping.")
        return rc1

    rc2 = run_cmd([py, str(EXCEL_TAGGER), "--file", str(target)])
    if rc2 != 0:
        print("Code classification phase failed.")
        return rc2

    print("\nDone. Full pass completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
