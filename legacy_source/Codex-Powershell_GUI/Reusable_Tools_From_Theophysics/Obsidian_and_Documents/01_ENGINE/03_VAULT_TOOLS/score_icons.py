#!/usr/bin/env python3
"""
score_icons.py — Assign number emoji icons to vault files based on frontmatter score.
Updates obsidian-icon-folder/data.json without renaming any files or breaking links.

Emoji mapping (tens digit of score):
  100    → 🔟
  90-99  → 9️⃣
  80-89  → 8️⃣
  70-79  → 7️⃣
  60-69  → 6️⃣
  50-59  → 5️⃣
  40-49  → 4️⃣
  30-39  → 3️⃣
  20-29  → 2️⃣
  10-19  → 1️⃣
  0-9    → 0️⃣
  no score → untouched

Usage: python score_icons.py
       python score_icons.py --dry-run   (preview without writing)
"""

import sys
import io
import os
import json
import re
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

VAULT_ROOT = r"O:\_Theophysics_v3"
SCAN_DIR   = os.path.join(VAULT_ROOT, "04_THEOPYHISCS")
DATA_JSON  = os.path.join(VAULT_ROOT, ".obsidian", "plugins", "obsidian-icon-folder", "data.json")

EMOJI_MAP = {
    10: "🔟",
    9:  "9️⃣",
    8:  "8️⃣",
    7:  "7️⃣",
    6:  "6️⃣",
    5:  "5️⃣",
    4:  "4️⃣",
    3:  "3️⃣",
    2:  "2️⃣",
    1:  "1️⃣",
    0:  "0️⃣",
}


def score_to_emoji(score):
    if score is None:
        return None
    try:
        s = float(score)
    except (ValueError, TypeError):
        return None
    if s >= 100:
        return EMOJI_MAP[10]
    if s < 0:
        return None
    tens = int(s) // 10
    return EMOJI_MAP.get(tens)


def extract_score(filepath):
    """Extract numeric score from YAML frontmatter (score, grade, or rating key)."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read(2000)
    except Exception:
        return None

    if not content.startswith('---'):
        return None

    end = content.find('\n---', 3)
    if end == -1:
        return None

    frontmatter = content[3:end]

    # Check top-level keys first (cdcm_score is 0-100 scale)
    for key in ('cdcm_score', 'score', 'grade', 'rating'):
        m = re.search(rf'^{key}\s*:\s*([\d.]+)', frontmatter, re.MULTILINE | re.IGNORECASE)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                continue

    # Fall back to ckg_evaluation.raw_score (also 0-100 scale)
    m = re.search(r'raw_score\s*:\s*(\d+)', frontmatter, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass

    return None


def to_vault_path(filepath):
    """Convert absolute path to vault-relative path with forward slashes."""
    rel = os.path.relpath(filepath, VAULT_ROOT)
    return rel.replace('\\', '/')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    args = parser.parse_args()

    with open(DATA_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assigned = 0
    skipped  = 0
    by_emoji = {}

    for root, dirs, files in os.walk(SCAN_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for fname in files:
            if not fname.endswith('.md'):
                continue

            fpath = os.path.join(root, fname)
            score = extract_score(fpath)
            emoji = score_to_emoji(score)

            if emoji is None:
                skipped += 1
                continue

            vault_path = to_vault_path(fpath)
            data[vault_path] = emoji
            assigned += 1
            by_emoji[emoji] = by_emoji.get(emoji, 0) + 1

    # Summary
    print(f"\n{'DRY RUN — ' if args.dry_run else ''}Score Icons Summary")
    print(f"{'='*40}")
    print(f"Files assigned: {assigned}")
    print(f"Files skipped (no score): {skipped}")
    print(f"\nBreakdown by tier:")
    for emoji in ["🔟", "9️⃣", "8️⃣", "7️⃣", "6️⃣", "5️⃣", "4️⃣", "3️⃣", "2️⃣", "1️⃣", "0️⃣"]:
        count = by_emoji.get(emoji, 0)
        if count:
            print(f"  {emoji}  {count} files")

    if not args.dry_run:
        with open(DATA_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nWritten to: {DATA_JSON}")
        print("Restart Obsidian (or toggle the plugin off/on) to see icons.")
    else:
        print("\n[Dry run — data.json not modified]")


if __name__ == '__main__':
    main()
