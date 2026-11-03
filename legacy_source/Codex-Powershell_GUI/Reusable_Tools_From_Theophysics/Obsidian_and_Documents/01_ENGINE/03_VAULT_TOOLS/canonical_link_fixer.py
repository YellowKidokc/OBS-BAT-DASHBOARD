#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
canonical_link_fixer.py

For each .md theory file in 00_Canonical:
1. Build a file index: filename_stem -> vault-relative path
2. Find "Related Theories" section
3. Parse all link targets (markdown or wikilink format)
4. Convert to Obsidian wikilinks [[vault_path|Display Name]]
5. Remove self-links, duplicates, broken external paths
6. Ensure canonical hub link is present

Usage: python canonical_link_fixer.py
"""

import os
import re
from pathlib import Path

VAULT_ROOT = Path("O:/_Theophysics_v3")
CANONICAL_DIR = VAULT_ROOT / "00_Canonical"
CANONICAL_HUB = "00_Canonical/CANONICAL_INDEX"

# These files won't have their Related Theories section modified
SKIP_FILES = {
    'CANONICAL_INDEX.md', 'MASTER_INDEX.md', 'NAVIGATION_GUIDE.md',
    'SYSTEM_STATUS.md', 'THEORY_INTERCONNECTIONS.md', 'CANONICAL_MAP.md',
    'AXIOM_CANONICAL_MAPPING.md', 'CANONICAL_MAP.json', 'EXTRACTION_METHODOLOGY.md',
    'EXTRACTION_REPORT_PHASE_1.md', 'MASTER_INDEX.md', 'SYSTEM_STATUS.md',
    'THEORY_INTERCONNECTIONS.md', 'theory_relationships.json',
    'AXIOMS_COMPENDIUM.md', 'AXIOM_AND_THEORY_LINKS.md', 'INDEX.md',
    'READY_FOR_AXIOM_EXTRACTION.md', 'README_RESTRUCTURING.md',
    'RESTRUCTURING_STATUS.md', 'TEN_LAWS_CANONICAL_EQUATIONS.md',
}


def display_name(stem: str) -> str:
    """Convert a filename stem to a readable display name."""
    return stem.replace('_', ' ').replace('-', ' ')


def build_file_index() -> dict:
    """
    Build map: stem_lower -> vault_relative_path_no_ext
    e.g. "hard_problem_of_consciousness" -> "00_Canonical/TH_Consciousness/General/Hard_Problem_of_Consciousness"
    """
    index = {}
    for root, dirs, files in os.walk(CANONICAL_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if not file.endswith('.md'):
                continue
            full = Path(root) / file
            vault_rel = full.relative_to(VAULT_ROOT).as_posix()
            vault_rel_no_ext = vault_rel[:-3]  # strip .md
            stem = file[:-3]
            key = stem.lower()
            if key not in index:
                index[key] = (vault_rel_no_ext, stem)
    return index


def extract_link_targets(body: str) -> list:
    """
    Extract (display_text_or_None, path_stem) from a Related Theories body.
    Handles:
    - - [display](path.md)
    - - [[path|display]] or [[path]]
    - bare lines (ignored)
    """
    results = []
    for line in body.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Markdown link: [display](path)
        m = re.match(r'[-*]?\s*\[([^\]]*)\]\(([^)]+)\)', line)
        if m:
            disp = m.group(1).strip() or None
            path = m.group(2).strip()
            stem = Path(path.replace('\\', '/')).stem
            if stem:
                results.append((disp, stem))
            continue

        # Wikilink: [[path|display]] or [[path]]
        m = re.match(r'[-*]?\s*\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]', line)
        if m:
            path = m.group(1).strip()
            disp = m.group(2).strip() if m.group(2) else None
            stem = Path(path.replace('\\', '/')).stem
            if stem:
                results.append((disp, stem))
            continue

    return results


def fix_related_section(content: str, self_stem: str, file_index: dict):
    """
    Find and rewrite Related Theories section with proper wikilinks.
    Returns (new_content, changed: bool).
    """
    pattern = re.compile(
        r'(##\s*Related Theories[^\n]*\n)(.*?)(?=\n##\s|\Z)',
        re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(content)
    if not match:
        return content, False

    header = match.group(1)
    old_body = match.group(2)

    targets = extract_link_targets(old_body)

    seen = set()
    links = []
    self_lower = self_stem.lower()

    for disp, stem in targets:
        stem_lower = stem.lower()
        if stem_lower == self_lower:          # remove self-links
            continue
        if stem_lower in seen:                # remove duplicates
            continue
        if stem_lower not in file_index:      # skip broken/external paths
            continue
        seen.add(stem_lower)
        vault_path, orig_stem = file_index[stem_lower]
        d = disp if disp else display_name(orig_stem)
        links.append(f"- [[{vault_path}|{d}]]")

    if not links:
        new_body = "\n*No related theories found in canonical index*\n"
    else:
        new_body = '\n' + '\n'.join(links) + '\n'

    new_section = header + new_body
    new_content = content[:match.start()] + new_section + content[match.end():]
    changed = (new_body.strip() != old_body.strip())
    return new_content, changed


def process_all():
    file_index = build_file_index()
    print(f"Indexed {len(file_index)} canonical files\n")

    changed = 0
    errors = 0
    skipped = 0

    for root, dirs, files in os.walk(CANONICAL_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in sorted(files):
            if not file.endswith('.md'):
                continue
            if file in SKIP_FILES or file.startswith('DOMAIN_DASHBOARD'):
                skipped += 1
                continue

            full_path = Path(root) / file
            stem = file[:-3]

            try:
                with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()

                new_content, was_changed = fix_related_section(content, stem, file_index)

                if was_changed:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    changed += 1
                    rel = full_path.relative_to(VAULT_ROOT)
                    print(f"  FIXED: {rel}")

            except Exception as e:
                errors += 1
                print(f"  ERROR: {full_path}: {e}")

    print(f"\n--- Summary ---")
    print(f"  Files fixed:   {changed}")
    print(f"  Errors:        {errors}")
    print(f"  Skipped:       {skipped}")


if __name__ == '__main__':
    process_all()
