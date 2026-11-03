#!/usr/bin/env python3
"""
fix_broken_links_vault.py
Fix resolvable broken wikilinks across the entire vault by stem-matching.

Strategy:
  - Scan all .md files (excluding _ARCHIVE, .trash)
  - Find path-based wikilinks (containing /) that don't resolve
  - If exactly ONE vault file matches by stem: rewrite to new path
  - If ZERO or 2+ matches: skip (log as dead / ambiguous)

Usage:
    python fix_broken_links_vault.py --dry-run   # preview
    python fix_broken_links_vault.py --apply     # execute
    python fix_broken_links_vault.py --apply --folder 00_Canonical   # one folder only
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
# Top-level dirs to skip entirely when indexing AND scanning
SKIP_TOP  = {".trash", "_ARCHIVE", ".claude", "_INBOX"}
# Any path segment name that triggers a skip (for nested archives)
SKIP_SEGS = {"_ARCHIVE", ".trash"}
WIKILINK  = re.compile(r'\[\[([^\]|#\n]+?)(?:([|#][^\]\n]*?))?\]\]')

MANIFEST_PATH = VAULT / "_ARCHIVE" / f"manifest_fix_vault_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"


def is_skipped(f: Path) -> bool:
    """True if any path segment should be excluded."""
    parts = f.relative_to(VAULT).parts
    if parts[0] in SKIP_TOP:
        return True
    return any(seg in SKIP_SEGS for seg in parts[1:])


def build_vault_index():
    by_fullpath = {}          # normalized rel path (no ext, lowercase) -> Path
    by_stem     = defaultdict(list)  # lowercase stem -> [Path, ...]
    for f in VAULT.rglob("*.md"):
        if is_skipped(f):
            continue
        rel_no_ext = str(f.relative_to(VAULT).with_suffix("")).replace("\\", "/")
        by_fullpath[rel_no_ext.lower()] = f
        by_stem[f.stem.lower()].append(f)
    return by_fullpath, by_stem


def collect_fixes(scan_root: Path, by_fullpath, by_stem):
    fixable   = []   # (md_file, old_target, new_rel_path, alias)
    ambiguous = []   # (md_file, old_target, candidate_count)
    dead      = Counter()  # old_target -> instance count

    for md_file in sorted(scan_root.rglob("*.md")):
        if is_skipped(md_file):
            continue
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for m in WIKILINK.finditer(content):
            target = m.group(1).strip()
            alias  = m.group(2) or ""

            if "/" not in target:
                continue  # stem-only links resolve fine in Obsidian

            key = target.replace("\\", "/").lower()
            if key.endswith(".md"):
                key = key[:-3]

            if key in by_fullpath:
                continue  # still resolves — nothing to do

            stem = Path(key).stem
            candidates = by_stem.get(stem, [])

            if len(candidates) == 1:
                new_path = str(candidates[0].relative_to(VAULT)).replace("\\", "/")
                if new_path.endswith(".md"):
                    new_path = new_path[:-3]
                fixable.append((md_file, target, new_path, alias))
            elif len(candidates) > 1:
                ambiguous.append((md_file, target, len(candidates)))
            else:
                dead[target] += 1

    return fixable, ambiguous, dead


def apply_fixes(fixable, dry: bool, rows: list):
    by_file = defaultdict(list)
    for md_file, old_target, new_path, alias in fixable:
        by_file[md_file].append((old_target, new_path, alias))

    for md_file in sorted(by_file.keys()):
        changes = by_file[md_file]
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


def run(dry: bool, folder: str | None):
    rows = []
    scan_root = VAULT / folder if folder else VAULT

    print("=" * 70)
    print(f"Fix Broken Wikilinks — {'Vault-wide' if not folder else folder}")
    print(f"Mode: {'DRY-RUN' if dry else 'APPLY'} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    print("\nBuilding vault file index...")
    by_fullpath, by_stem = build_vault_index()
    print(f"  Indexed {len(by_fullpath)} files, {len(by_stem)} unique stems")

    print(f"\nScanning {scan_root.relative_to(VAULT) if folder else 'vault'} for broken path-based links...")
    fixable, ambiguous, dead = collect_fixes(scan_root, by_fullpath, by_stem)

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

    if not fixable:
        print("\n  Nothing to fix.")
        print("=" * 70)
        return

    print("\n" + "-" * 70)
    print("Applying fixes...")
    apply_fixes(fixable, dry, rows)

    print(f"\n  Total rewrites: {len(rows)}")

    if ambiguous:
        print(f"\n--- Ambiguous skipped ({len(ambiguous)} instances, top 15) ---")
        shown = set()
        count = 0
        for md_file, target, n in ambiguous:
            if target not in shown:
                shown.add(target)
                print(f"  [{n} candidates] {target}")
                count += 1
                if count >= 15:
                    break
        remaining = len({t for _, t, _ in ambiguous} - shown)
        if remaining:
            print(f"  ... and {remaining} more unique targets")

    print(f"\n--- Top 20 dead targets (no match) ---")
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
    p.add_argument("--folder",  default=None,
                   help="Scan only this top-level folder (e.g. 00_Canonical)")
    args = p.parse_args()
    run(dry=args.dry_run, folder=args.folder)


if __name__ == "__main__":
    main()
