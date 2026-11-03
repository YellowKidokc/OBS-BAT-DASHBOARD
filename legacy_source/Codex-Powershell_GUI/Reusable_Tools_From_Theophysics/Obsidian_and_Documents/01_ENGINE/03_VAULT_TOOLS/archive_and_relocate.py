#!/usr/bin/env python3
"""
archive_and_relocate.py
Vault Curation — Archive + Glossary Relocation
2026-03-02

Usage:
    python archive_and_relocate.py --dry-run    # preview all moves
    python archive_and_relocate.py --apply      # execute
    python archive_and_relocate.py --apply --skip-yaml-taxonomy  # skip YAML_TAXONOMY move
"""

import argparse
import csv
import io
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Force UTF-8 output on Windows consoles
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Paths ──────────────────────────────────────────────────────────────────────
VAULT_ROOT = Path("O:/_Theophysics_v3")
SYSTEM_DIR = VAULT_ROOT / "00_SYSTEM"
LEGACY_DIR = SYSTEM_DIR / "90_LEGACY"
ARCHIVE_DEST = VAULT_ROOT / "_ARCHIVE" / "00_SYSTEM_LEGACY_20260302"
REFERENCE_DIR = SYSTEM_DIR / "04_REFERENCE"
GLOSSARY_SRC = REFERENCE_DIR / "Glossary"
GLOSSARY_DEST = VAULT_ROOT / "00_Canonical" / "Glossary"
YAML_TAX_SRC = REFERENCE_DIR / "YAML_TAXONOMY"
YAML_TAX_DEST = SYSTEM_DIR / "02_GOVERNANCE" / "YAML_TAXONOMY"

# Subfolders to archive from 90_LEGACY (keep _manifests in place)
LEGACY_SUBFOLDERS = [
    "_root_docs",
    "Live_Examples",
    "Scoring_Validation",
    "Structure",
    "05_WORKFLOW",
    "YAML",
]

MANIFEST_PATH = VAULT_ROOT / "_ARCHIVE" / f"manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"


def log(msg, dry=False):
    prefix = "[DRY-RUN] " if dry else "[APPLY]   "
    print(prefix + msg)


def count_items(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for _ in path.rglob("*"))


def move_dir(src: Path, dest: Path, dry: bool, manifest_rows: list):
    if not src.exists():
        log(f"SKIP (not found): {src}", dry)
        return

    if dest.exists():
        log(f"SKIP (dest already exists): {dest}", dry)
        return

    item_count = count_items(src)
    log(f"MOVE  {src}\n          → {dest}  ({item_count} items)", dry)

    for item in src.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src.parent)
            manifest_rows.append({
                "action": "move",
                "source": str(item),
                "destination": str(dest.parent / rel),
                "type": "file",
            })

    if not dry:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))


def fix_wikilinks(vault_root: Path, old_fragment: str, new_fragment: str, dry: bool) -> int:
    """
    Find-and-replace old_fragment → new_fragment in all .md files under vault_root.
    Returns count of files changed.
    """
    changed = 0
    for md_file in vault_root.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if old_fragment in content:
            new_content = content.replace(old_fragment, new_fragment)
            log(f"LINK-FIX  {md_file.relative_to(vault_root)}", dry)
            if not dry:
                md_file.write_text(new_content, encoding="utf-8")
            changed += 1
    return changed


def remove_if_empty(path: Path, dry: bool):
    if not path.exists():
        return
    remaining = list(path.iterdir())
    if not remaining:
        log(f"RMDIR (empty): {path}", dry)
        if not dry:
            path.rmdir()
    else:
        log(f"SKIP rmdir (not empty, {len(remaining)} items remain): {path}", dry)


def run(dry: bool, skip_yaml_taxonomy: bool):
    manifest_rows = []

    print("=" * 70)
    print(f"Vault Curation — Archive + Glossary Relocation")
    print(f"Mode: {'DRY-RUN' if dry else 'APPLY'}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # ── Action 1: Archive 90_LEGACY subfolders ─────────────────────────────────
    print("\n── Action 1: Archive 90_LEGACY subfolders ──")
    if not LEGACY_DIR.exists():
        print(f"ERROR: 90_LEGACY not found at {LEGACY_DIR}")
        sys.exit(1)

    for folder_name in LEGACY_SUBFOLDERS:
        src = LEGACY_DIR / folder_name
        dest = ARCHIVE_DEST / folder_name
        move_dir(src, dest, dry, manifest_rows)

    # Verify what remains in 90_LEGACY
    if LEGACY_DIR.exists():
        remaining = [x.name for x in LEGACY_DIR.iterdir()]
        log(f"90_LEGACY remaining after moves: {remaining}", dry)

    # ── Action 2: Move Glossary ────────────────────────────────────────────────
    print("\n── Action 2: Move Glossary → 00_Canonical/Glossary ──")
    if not GLOSSARY_SRC.exists():
        print(f"ERROR: Glossary source not found at {GLOSSARY_SRC}")
        sys.exit(1)

    if GLOSSARY_DEST.exists():
        print(f"ERROR: Glossary destination already exists: {GLOSSARY_DEST}")
        print("       Resolve manually before running --apply.")
        sys.exit(1)

    glossary_count = count_items(GLOSSARY_SRC)
    log(f"Glossary files to move: {glossary_count}", dry)
    move_dir(GLOSSARY_SRC, GLOSSARY_DEST, dry, manifest_rows)

    # Fix wikilinks
    print("\n── Action 3: Fix wikilinks (Glossary path) ──")
    old_frag = "00_SYSTEM/04_REFERENCE/Glossary/"
    new_frag = "00_Canonical/Glossary/"
    changed = fix_wikilinks(VAULT_ROOT, old_frag, new_frag, dry)
    log(f"Wikilink files updated: {changed}", dry)

    # Also fix bare wikilinks without path prefix that reference Glossary subfolder
    # e.g. [[Glossary/SomeTerm]] — these don't need a path fix, skip

    # ── Action 4 (optional): Move YAML_TAXONOMY ───────────────────────────────
    if not skip_yaml_taxonomy:
        print("\n── Action 4: Move YAML_TAXONOMY → 02_GOVERNANCE ──")
        if not YAML_TAX_SRC.exists():
            log(f"SKIP: YAML_TAXONOMY not found at {YAML_TAX_SRC}", dry)
        else:
            move_dir(YAML_TAX_SRC, YAML_TAX_DEST, dry, manifest_rows)

    # ── Cleanup: remove 04_REFERENCE if empty ─────────────────────────────────
    print("\n── Action 5: Clean up 04_REFERENCE if empty ──")
    if not skip_yaml_taxonomy:
        remove_if_empty(REFERENCE_DIR, dry)

    # ── Write manifest ─────────────────────────────────────────────────────────
    if manifest_rows:
        if not dry:
            MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["action", "source", "destination", "type"])
                writer.writeheader()
                writer.writerows(manifest_rows)
            log(f"Manifest written: {MANIFEST_PATH}", dry)
        else:
            log(f"Manifest would be written to: {MANIFEST_PATH}", dry)

    print("\n" + "=" * 70)
    print(f"Done. {len(manifest_rows)} file entries logged.")
    if dry:
        print("Re-run with --apply to execute.")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Vault archive and glossary relocation tool.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Preview all actions, no changes")
    mode.add_argument("--apply", action="store_true", help="Execute all moves")
    parser.add_argument(
        "--skip-yaml-taxonomy",
        action="store_true",
        help="Skip moving YAML_TAXONOMY to 02_GOVERNANCE",
    )
    args = parser.parse_args()

    dry = args.dry_run
    run(dry=dry, skip_yaml_taxonomy=args.skip_yaml_taxonomy)


if __name__ == "__main__":
    main()
