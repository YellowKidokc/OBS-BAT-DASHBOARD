#!/usr/bin/env python3
"""
BATCH CLEANUP ALL THEORIES
===========================
Clean all theory papers in the canonical library in one go.

Usage:
  python cleanup_all_theories.py
  python cleanup_all_theories.py --dry-run
  python cleanup_all_theories.py --limit 10
  python cleanup_all_theories.py --pattern "TH_Consciousness"

This will:
  1. Find all .md files in O:\_Theophysics_v3\00_CANONICAL\TH_*\
  2. Clean each one (output as {name}_CLEAN.md)
  3. Generate summary report
  4. Show before/after statistics
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from paper_cleanup_tool import cleanup_paper, extract_metadata_from_content


def find_theory_files(root: Path, pattern: str = None, limit: int = None) -> list:
    """Find all theory markdown files to clean."""
    files = []

    # Pattern: O:\_Theophysics_v3\00_CANONICAL\TH_*\General\*.md
    base = root / "00_CANONICAL"

    if not base.exists():
        print(f"[ERROR] Canonical directory not found: {base}")
        return files

    for theory_dir in sorted(base.glob("TH_*")):
        if not theory_dir.is_dir():
            continue

        for md_file in theory_dir.rglob("*.md"):
            # Skip already-cleaned files
            if "_CLEAN" in md_file.name:
                continue

            # Apply pattern filter
            if pattern and pattern.lower() not in md_file.parent.name.lower():
                continue

            files.append(md_file)

            if limit and len(files) >= limit:
                return files

    return files


def run_batch_cleanup(root: Path, dry_run: bool = False, limit: int = None, pattern: str = None):
    """Run cleanup on all theories."""

    print(f"\n{'='*70}")
    print(f"  BATCH CLEANUP ALL THEORIES")
    print(f"{'='*70}\n")

    # Find files
    files = find_theory_files(root, pattern=pattern, limit=limit)

    if not files:
        print("  [ERROR] No theory files found to clean.")
        return

    print(f"  Found {len(files)} theory files to clean")
    if limit:
        print(f"  (Limited to {limit})")
    if pattern:
        print(f"  (Matching pattern: {pattern})")

    print(f"\n  {'='*70}\n")

    # Statistics
    stats = {
        "total": len(files),
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "original_size": 0,
        "cleaned_size": 0,
        "size_reduction": 0,
    }

    category_stats = defaultdict(int)
    failed_files = []

    # Process each file
    for idx, file_path in enumerate(files, 1):
        rel_path = file_path.relative_to(root)
        category = file_path.parent.parent.name  # TH_*

        print(f"  [{idx:2d}/{len(files)}] {rel_path}")

        if dry_run:
            print(f"       [DRY-RUN] Would clean this file")
            stats["skipped"] += 1
            continue

        # Check if already cleaned
        clean_path = file_path.parent / f"{file_path.stem}_CLEAN{file_path.suffix}"
        if clean_path.exists():
            print(f"       [SKIP] Already cleaned → {clean_path.name}")
            stats["skipped"] += 1
            continue

        # Run cleanup
        try:
            success, result = cleanup_paper(file_path)

            if success:
                output_path = Path(result)

                # Get file sizes
                original_size = file_path.stat().st_size
                cleaned_size = output_path.stat().st_size
                reduction = original_size - cleaned_size

                stats["success"] += 1
                stats["original_size"] += original_size
                stats["cleaned_size"] += cleaned_size
                stats["size_reduction"] += reduction
                category_stats[category] += 1

                pct = round((reduction / original_size * 100), 1) if original_size > 0 else 0
                print(f"       ✅ {output_path.name}")
                print(f"          Size: {original_size:,} → {cleaned_size:,} bytes ({pct}% reduction)")

            else:
                print(f"       ❌ {result}")
                stats["failed"] += 1
                failed_files.append((file_path.name, result))

        except Exception as e:
            print(f"       ❌ Exception: {e}")
            stats["failed"] += 1
            failed_files.append((file_path.name, str(e)))

    # Summary
    print(f"\n{'='*70}")
    print(f"  SUMMARY")
    print(f"{'='*70}\n")

    print(f"  Total files:      {stats['total']}")
    print(f"  ✅ Cleaned:       {stats['success']}")
    print(f"  ⏭️  Skipped:       {stats['skipped']}")
    print(f"  ❌ Failed:        {stats['failed']}")

    if stats["success"] > 0:
        print(f"\n  Size Statistics:")
        print(f"  Original total:   {stats['original_size']:,} bytes")
        print(f"  Cleaned total:    {stats['cleaned_size']:,} bytes")
        print(f"  Reduction:        {stats['size_reduction']:,} bytes ({round(stats['size_reduction']/stats['original_size']*100, 1)}%)")

    if category_stats:
        print(f"\n  By Category:")
        for cat in sorted(category_stats.keys()):
            print(f"    {cat}: {category_stats[cat]}")

    if failed_files:
        print(f"\n  Failed Files:")
        for fname, reason in failed_files:
            print(f"    ❌ {fname}")
            print(f"       {reason[:80]}")

    print(f"\n{'='*70}\n")

    if dry_run:
        print("  [DRY-RUN MODE] No files were actually cleaned. Run without --dry-run to proceed.\n")

    # Exit code
    if stats["failed"] > 0:
        sys.exit(1)


def main():
    """CLI entry point."""

    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print(__doc__)
        sys.exit(0)

    # Parse args
    dry_run = "--dry-run" in sys.argv
    limit = None
    pattern = None

    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        if idx + 1 < len(sys.argv):
            try:
                limit = int(sys.argv[idx + 1])
            except ValueError:
                print("[ERROR] --limit requires integer argument")
                sys.exit(1)

    if "--pattern" in sys.argv:
        idx = sys.argv.index("--pattern")
        if idx + 1 < len(sys.argv):
            pattern = sys.argv[idx + 1]

    # Root directory
    root = Path(r"O:\_Theophysics_v3")

    if not root.exists():
        print(f"[ERROR] Root directory not found: {root}")
        sys.exit(1)

    # Run
    run_batch_cleanup(root, dry_run=dry_run, limit=limit, pattern=pattern)


if __name__ == "__main__":
    main()
