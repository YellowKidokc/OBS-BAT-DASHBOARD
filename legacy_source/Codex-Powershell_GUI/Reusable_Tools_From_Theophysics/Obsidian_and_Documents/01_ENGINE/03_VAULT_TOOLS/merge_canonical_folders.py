#!/usr/bin/env python3
"""
Merge 00_Canonical into Canonical

Combines the two canonical folders into one organized location.
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict


def merge_canonical_folders(vault_root: str):
    """Merge 00_Canonical into Canonical"""

    vault_root = Path(vault_root)
    old_canonical = vault_root / "00_Canonical"
    new_canonical = vault_root / "Canonical"

    print("="*60)
    print("MERGING CANONICAL FOLDERS")
    print("="*60)
    print(f"Source: {old_canonical}")
    print(f"Target: {new_canonical}")
    print()

    if not old_canonical.exists():
        print("[!] 00_Canonical folder not found")
        return

    if not new_canonical.exists():
        print("[!] Canonical folder not found")
        return

    # Count files
    old_files = list(old_canonical.rglob("*.md"))
    new_files = list(new_canonical.rglob("*.md"))

    print(f"[*] Files in 00_Canonical: {len(old_files)}")
    print(f"[*] Files in Canonical: {len(new_files)}")
    print()

    # Create mapping of what to move where
    moves = []
    duplicates = []

    print("[*] Analyzing content...")

    for old_file in old_files:
        rel_path = old_file.relative_to(old_canonical)
        new_file = new_canonical / rel_path

        if new_file.exists():
            # Check if they're the same
            if old_file.stat().st_size == new_file.stat().st_size:
                duplicates.append(str(rel_path))
            else:
                # Different sizes - need to compare
                with open(old_file, 'rb') as f1, open(new_file, 'rb') as f2:
                    if f1.read() == f2.read():
                        duplicates.append(str(rel_path))
                    else:
                        # Different content - keep both with suffix
                        new_name = new_file.stem + "_from_00_Canonical" + new_file.suffix
                        new_target = new_file.parent / new_name
                        moves.append((old_file, new_target))
        else:
            moves.append((old_file, new_file))

    print(f"[+] Files to move: {len(moves)}")
    print(f"[+] Duplicate files (will skip): {len(duplicates)}")
    print()

    # Show some duplicates
    if duplicates:
        print("Sample duplicates (will skip):")
        for dup in duplicates[:10]:
            print(f"  - {dup}")
        if len(duplicates) > 10:
            print(f"  ... and {len(duplicates) - 10} more")
        print()

    # Confirm
    response = input(f"Move {len(moves)} files from 00_Canonical to Canonical? (y/n): ")
    if response.lower() != 'y':
        print("[!] Cancelled")
        return

    # Move files
    print("\n[*] Moving files...")
    moved = 0
    errors = 0

    for old_file, new_file in moves:
        try:
            # Create parent directory if needed
            new_file.parent.mkdir(parents=True, exist_ok=True)

            # Move file
            shutil.copy2(old_file, new_file)
            moved += 1

            if moved % 50 == 0:
                print(f"  Moved {moved}/{len(moves)} files...")
        except Exception as e:
            print(f"  [-] Error moving {old_file.name}: {e}")
            errors += 1

    print(f"\n[+] Moved {moved} files")
    if errors > 0:
        print(f"[-] Errors: {errors}")

    # Copy directories that don't exist in new canonical
    print("\n[*] Checking for missing directories...")
    for item in old_canonical.iterdir():
        if item.is_dir():
            target = new_canonical / item.name
            if not target.exists():
                print(f"  [*] Copying directory: {item.name}")
                shutil.copytree(item, target)

    # Summary
    print("\n" + "="*60)
    print("MERGE COMPLETE")
    print("="*60)
    print(f"[+] Total files now in Canonical: {len(list(new_canonical.rglob('*.md')))}")
    print()
    print("Next steps:")
    print("1. Verify merged content")
    print("2. Delete 00_Canonical folder if everything looks good")
    print(f"3. Run: rm -rf '{old_canonical}'")
    print()


if __name__ == '__main__':
    merge_canonical_folders('O:/_Theophysics_v3')
