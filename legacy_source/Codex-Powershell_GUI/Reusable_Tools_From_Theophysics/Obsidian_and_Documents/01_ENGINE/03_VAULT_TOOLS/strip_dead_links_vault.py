#!/usr/bin/env python3
"""
strip_dead_links_vault.py
Remove broken path-based wikilinks from all vault files.

For each [[path/to/File|alias]] that doesn't resolve:
  - If alias present:  [[path/to/File|alias]] → alias
  - If no alias:       [[path/to/File Name]]  → File Name   (stem only)
  - Ambiguous (2+ candidates) are also stripped.
  - Stem-only [[File]] links are untouched (Obsidian resolves these).

Usage:
    python strip_dead_links_vault.py --dry-run
    python strip_dead_links_vault.py --apply
"""

import argparse
import csv
import io
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

VAULT     = Path("O:/_Theophysics_v3")
SKIP_TOP  = {".trash", "_ARCHIVE", ".claude", "_INBOX"}
SKIP_SEGS = {"_ARCHIVE", ".trash"}
WIKILINK  = re.compile(r'\[\[([^\]\n]+)\]\]')

MANIFEST_PATH = VAULT / "_ARCHIVE" / f"manifest_strip_dead_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"


def is_skipped(f: Path) -> bool:
    parts = f.relative_to(VAULT).parts
    if parts[0] in SKIP_TOP:
        return True
    return any(seg in SKIP_SEGS for seg in parts[1:])


def build_vault_index():
    by_fullpath = {}
    by_stem     = defaultdict(list)
    for f in VAULT.rglob("*.md"):
        if is_skipped(f):
            continue
        rel_no_ext = str(f.relative_to(VAULT).with_suffix("")).replace("\\", "/")
        by_fullpath[rel_no_ext.lower()] = f
        by_stem[f.stem.lower()].append(f)
    return by_fullpath, by_stem


def parse_wikilink(inner: str):
    """
    Parse the content between [[ and ]].
    Returns (target, display_text) where display_text is the alias if present,
    otherwise the stem of the target path.
    """
    # Split on first | to get target vs alias
    if "|" in inner:
        target, alias = inner.split("|", 1)
        display = alias.strip() or Path(target.strip().replace("\\", "/")).stem
    else:
        target = inner
        # Strip anchor (#...) from target for path resolution
        target_no_anchor = target.split("#")[0]
        display = Path(target_no_anchor.strip().replace("\\", "/")).stem
    return target.strip(), display


def strip_file(md_file: Path, by_fullpath, by_stem, dry: bool, rows: list) -> int:
    try:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return 0

    # Pass 1: collect unique replacements (dedup — same link may appear many times)
    replacements = {}  # full_match -> display_text
    for m in WIKILINK.finditer(content):
        inner = m.group(1)
        target, display = parse_wikilink(inner)

        if "/" not in target:
            continue  # stem-only — fine

        # Strip anchor from target path for lookup
        target_path = target.split("#")[0].strip()
        key = target_path.replace("\\", "/").lower()
        if key.endswith(".md"):
            key = key[:-3]

        if key in by_fullpath:
            continue  # resolves — leave it

        stem = Path(key).stem
        candidates = by_stem.get(stem, [])
        if len(candidates) == 1:
            continue  # fixable — skip (handled by fix script)

        full_match = m.group(0)
        if full_match not in replacements:
            replacements[full_match] = display

    if not replacements:
        return 0

    # Pass 2: apply each unique replacement exactly once
    new_content = content
    rel = str(md_file.relative_to(VAULT))
    for full_match, replacement in replacements.items():
        new_content = new_content.replace(full_match, replacement)
        rows.append({"file": rel, "old_link": full_match, "replacement": replacement})

    if not dry:
        md_file.write_text(new_content, encoding="utf-8")

    return len(replacements)


def run(dry: bool):
    rows = []
    print("=" * 70)
    print("Strip Dead Wikilinks — Vault-wide")
    print(f"Mode: {'DRY-RUN' if dry else 'APPLY'} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    print("\nBuilding vault file index...")
    by_fullpath, by_stem = build_vault_index()
    print(f"  Indexed {len(by_fullpath)} files, {len(by_stem)} unique stems")

    print("\nScanning vault...")
    total_links = 0
    total_files = 0

    all_files = sorted(VAULT.rglob("*.md"))
    for i, md_file in enumerate(all_files):
        if is_skipped(md_file):
            continue
        n = strip_file(md_file, by_fullpath, by_stem, dry, rows)
        if n:
            total_links += n
            total_files += 1
        if (i + 1) % 500 == 0:
            print(f"  ... {i+1}/{len(all_files)} files scanned, {total_links} stripped so far", flush=True)

    print(f"\n  Links stripped: {total_links}")
    print(f"  Files modified: {total_files}")

    if rows and not dry:
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["file", "old_link", "replacement"])
            w.writeheader()
            w.writerows(rows)
        print(f"\nManifest: {MANIFEST_PATH}")

    print("\n" + "=" * 70)
    if dry:
        print("Re-run with --apply to execute.")


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply",   action="store_true")
    args = p.parse_args()
    run(dry=args.dry_run)


if __name__ == "__main__":
    main()
