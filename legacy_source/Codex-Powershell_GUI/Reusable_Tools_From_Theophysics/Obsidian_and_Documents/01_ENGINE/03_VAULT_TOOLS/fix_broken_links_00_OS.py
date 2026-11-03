#!/usr/bin/env python3
"""
fix_broken_links_00_OS.py
Fix resolvable broken wikilinks in 00_OS by stem-matching against the vault.

Strategy:
  - Scan 00_OS for path-based wikilinks (contain /)
  - Check if the target path still exists in the vault
  - If not, search by filename stem across the whole vault
  - If exactly ONE match: rewrite the link to the new path
  - If ZERO or 2+ matches: skip (report as unfixable)

Usage:
    python fix_broken_links_00_OS.py --dry-run   # preview changes
    python fix_broken_links_00_OS.py --apply     # execute
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

VAULT      = Path("O:/_Theophysics_v3")
OS_DIR     = VAULT / "00_OS"
SKIP_DIRS  = {".trash", "_ARCHIVE"}
WIKILINK   = re.compile(r'\[\[([^\]|#\n]+?)(?:([|#][^\]\n]*?))?\]\]')

MANIFEST_PATH = VAULT / "_ARCHIVE" / f"manifest_fix_00OS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"


def build_vault_index():
    """Return (by_fullpath, by_stem) indexes over active vault files."""
    by_fullpath = {}   # normalized relative path (no ext) -> Path
    by_stem     = defaultdict(list)  # lowercase stem -> [Path, ...]

    for f in VAULT.rglob("*.md"):
        parts = f.relative_to(VAULT).parts
        if parts[0] in SKIP_DIRS:
            continue
        rel_no_ext = str(f.relative_to(VAULT).with_suffix("")).replace("\\", "/")
        key = rel_no_ext.lower()
        by_fullpath[key] = f
        by_stem[f.stem.lower()].append(f)

    return by_fullpath, by_stem


def collect_fixes(by_fullpath, by_stem):
    """
    Scan 00_OS for broken path-based wikilinks.
    Returns:
        fixable  : list of (md_file, old_target, new_rel_path, alias_suffix)
        ambiguous: list of (md_file, old_target, candidate_count)
        dead     : Counter of old_target -> instance count
    """
    fixable   = []
    ambiguous = []
    dead      = Counter()

    for md_file in sorted(OS_DIR.rglob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for m in WIKILINK.finditer(content):
            target = m.group(1).strip()
            alias  = m.group(2) or ""   # "|display" or "#anchor" or ""

            if "/" not in target:
                continue  # stem-only links are fine — Obsidian resolves them

            key = target.replace("\\", "/").lower()
            if key.endswith(".md"):
                key = key[:-3]

            if key in by_fullpath:
                continue  # still resolves — nothing to do

            stem = Path(key).stem
            candidates = by_stem.get(stem, [])

            if len(candidates) == 1:
                new_path = str(candidates[0].relative_to(VAULT)).replace("\\", "/")
                # Strip .md extension to match Obsidian wikilink convention
                if new_path.endswith(".md"):
                    new_path = new_path[:-3]
                fixable.append((md_file, target, new_path, alias))

            elif len(candidates) > 1:
                ambiguous.append((md_file, target, len(candidates)))

            else:
                dead[target] += 1

    return fixable, ambiguous, dead


def apply_fixes(fixable, dry: bool, rows: list):
    """Rewrite links file-by-file, grouped by source file."""
    # Group fixes by file
    by_file = defaultdict(list)
    for md_file, old_target, new_path, alias in fixable:
        by_file[md_file].append((old_target, new_path, alias))

    for md_file, changes in sorted(by_file.items()):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            print(f"  ERROR reading {md_file}")
            continue

        new_content = content
        file_changed = False

        for old_target, new_path, alias in changes:
            old_link = f"[[{old_target}{alias}]]"
            new_link = f"[[{new_path}{alias}]]"

            if old_link in new_content:
                new_content = new_content.replace(old_link, new_link)
                file_changed = True
                rel = str(md_file.relative_to(VAULT))
                tag = "[DRY-RUN]" if dry else "[APPLY]  "
                print(f"  {tag} {rel}")
                print(f"           {old_target}")
                print(f"        -> {new_path}")
                rows.append({
                    "file":       rel,
                    "old_target": old_target,
                    "new_target": new_path,
                })

        if file_changed and not dry:
            md_file.write_text(new_content, encoding="utf-8")


def run(dry: bool):
    rows = []
    print("=" * 70)
    print("Fix Broken Wikilinks — 00_OS")
    print(f"Mode: {'DRY-RUN' if dry else 'APPLY'} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    print("\nBuilding vault file index...")
    by_fullpath, by_stem = build_vault_index()
    print(f"  Indexed {len(by_fullpath)} files, {len(by_stem)} unique stems")

    print("\nScanning 00_OS for broken path-based links...")
    fixable, ambiguous, dead = collect_fixes(by_fullpath, by_stem)

    # Deduplicate fixable (same file+target may appear multiple times)
    seen = set()
    unique_fixable = []
    for item in fixable:
        k = (item[0], item[1])
        if k not in seen:
            seen.add(k)
            unique_fixable.append(item)
    fixable = unique_fixable

    print(f"\n  Fixable   (single stem match): {len(fixable)}")
    print(f"  Ambiguous (2+ candidates):     {len(ambiguous)}")
    print(f"  Dead      (no match at all):   {sum(dead.values())} instances, {len(dead)} unique targets")

    print("\n" + "-" * 70)
    print("Applying fixes...")
    apply_fixes(fixable, dry, rows)

    print(f"\n  Total rewrites: {len(rows)}")

    if ambiguous:
        print(f"\n--- Ambiguous (skipped, {len(ambiguous)} instances) ---")
        for md_file, target, n in ambiguous[:20]:
            print(f"  [{n} candidates] {target}")
        if len(ambiguous) > 20:
            print(f"  ... and {len(ambiguous) - 20} more")

    print(f"\n--- Top 20 dead (no match, left untouched) ---")
    for tgt, count in dead.most_common(20):
        print(f"  {count:4d}  {tgt}")

    if rows and not dry:
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["file", "old_target", "new_target"])
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
