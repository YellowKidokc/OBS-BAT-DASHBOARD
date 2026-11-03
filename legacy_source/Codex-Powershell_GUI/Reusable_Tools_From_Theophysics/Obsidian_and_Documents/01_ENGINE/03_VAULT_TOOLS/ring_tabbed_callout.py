#!/usr/bin/env python3
"""
ring_tabbed_callout.py
======================
Wraps existing Ring 1 / Ring 2 / Ring 3 link sections into Obsidian tabbed callouts.

Uses the [!tabbed] callout CSS (already in vault snippets).

Modes:
    --test FILE       Process a single file (dry run, prints output)
    --batch N         Process first N files with ring sections (dry run)
    --apply           Actually write changes (requires --batch or --all)
    --all             Process entire vault
    --verify N        Verify N ring links resolve to real files
    --report          Show stats only

The script:
1. Finds files with Ring 2 / Ring 3 sections (## Ring 2 — ..., ## Ring 3 — ...)
2. Extracts Ring 1 from YAML frontmatter (depends_on / enables)
3. Wraps all three into a [!tabbed] callout block
4. Replaces the original sections in-place

Author: Claude Code
Date: 2026-03-10
"""

import sys
import os
import re
import argparse
import hashlib
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = Path("O:/_Theophysics_v3")

# Patterns to find existing ring sections
RING2_PATTERN = re.compile(
    r'^## Ring 2\s*[—–-]\s*Canonical Grounding\s*\n((?:.*\n)*?)(?=^## |^---|\Z)',
    re.MULTILINE
)
RING3_PATTERN = re.compile(
    r'^## Ring 3\s*[—–-]\s*Framework Connections\s*\n((?:.*\n)*?)(?=^## |^---|\Z)',
    re.MULTILINE
)

# Pattern to find the canonical hub footer
HUB_FOOTER = re.compile(r'^Canonical Hub:.*CANONICAL_INDEX.*$', re.MULTILINE)

SKIP_DIRS = {'.obsidian', '.git', 'node_modules', '__pycache__', '.claude'}
SKIP_FILES = {'CANONICAL_INDEX.md', 'CANONICAL_MAP.md', 'MASTER_INDEX.md',
              'NAVIGATION_GUIDE.md', 'SYSTEM_STATUS.md'}


def make_radio_name(filepath: Path) -> str:
    """Generate a unique radio button name from filepath to avoid tab conflicts."""
    h = hashlib.md5(str(filepath).encode()).hexdigest()[:8]
    return f"ring-{h}"


def extract_ring1_from_yaml(content: str) -> list:
    """Extract Ring 1 links from YAML frontmatter (depends_on + enables)."""
    links = []

    # Extract frontmatter
    if not content.startswith('---'):
        return links
    end = content.find('\n---', 3)
    if end == -1:
        return links
    fm = content[:end + 4]

    # Parse depends_on
    dep_match = re.findall(r'depends_on:\s*\n((?:\s+-\s+.+\n)*)', fm)
    if dep_match:
        for item in re.findall(r'-\s+(.+)', dep_match[0]):
            item = item.strip().strip('"\'')
            if item and item != '[]' and item != 'null':
                links.append(f"← {item}")

    # Also check inline format
    dep_inline = re.search(r'depends_on:\s*\[([^\]]*)\]', fm)
    if dep_inline and dep_inline.group(1).strip():
        for item in dep_inline.group(1).split(','):
            item = item.strip().strip('"\'')
            if item:
                links.append(f"← {item}")

    # Parse enables
    en_match = re.findall(r'enables:\s*\n((?:\s+-\s+.+\n)*)', fm)
    if en_match:
        for item in re.findall(r'-\s+(.+)', en_match[0]):
            item = item.strip().strip('"\'')
            if item and item != '[]' and item != 'null':
                links.append(f"→ {item}")

    en_inline = re.search(r'enables:\s*\[([^\]]*)\]', fm)
    if en_inline and en_inline.group(1).strip():
        for item in en_inline.group(1).split(','):
            item = item.strip().strip('"\'')
            if item:
                links.append(f"→ {item}")

    return links


def extract_ring_section(content: str, pattern: re.Pattern) -> tuple:
    """Extract a ring section. Returns (match_object, bullet_lines)."""
    m = pattern.search(content)
    if not m:
        return None, []

    section_body = m.group(1)
    # Extract bullet lines
    bullets = []
    for line in section_body.strip().split('\n'):
        line = line.strip()
        if line.startswith('- '):
            bullets.append(line)
        elif line and not line.startswith('#'):
            bullets.append(f"- {line}")
    return m, bullets


def build_tabbed_callout(ring1_lines: list, ring2_lines: list, ring3_lines: list,
                         radio_name: str) -> str:
    """Build the [!tabbed] callout markdown block."""
    parts = []
    parts.append("> [!tabbed]")

    tabs = []
    if ring1_lines:
        tabs.append(("Ring 1 · Local", ring1_lines))
    if ring2_lines:
        tabs.append(("Ring 2 · Canonical", ring2_lines))
    if ring3_lines:
        tabs.append(("Ring 3 · Framework", ring3_lines))

    if not tabs:
        return ""

    for i, (label, lines) in enumerate(tabs):
        checked = ' checked' if i == 0 else ''
        parts.append(f'> <label>{label}<input type="radio" name="{radio_name}"{checked} /></label>')
        parts.append(">")
        for line in lines:
            parts.append(f"> > {line}")
        parts.append(">")

    return "\n".join(parts)


def process_file(filepath: Path, dry_run: bool = True) -> dict:
    """Process a single file. Returns result dict."""
    result = {
        'file': str(filepath.relative_to(VAULT_ROOT)),
        'changed': False,
        'ring1_count': 0,
        'ring2_count': 0,
        'ring3_count': 0,
        'already_tabbed': False,
        'errors': [],
    }

    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            content = filepath.read_text(encoding='utf-16')
        except Exception as e:
            result['errors'].append(f"Read error: {e}")
            return result

    # Skip if already tabbed
    if '[!tabbed]' in content:
        result['already_tabbed'] = True
        return result

    # Extract existing ring sections
    r2_match, ring2_lines = extract_ring_section(content, RING2_PATTERN)
    r3_match, ring3_lines = extract_ring_section(content, RING3_PATTERN)

    # Extract Ring 1 from YAML
    ring1_lines = extract_ring1_from_yaml(content)

    # Need at least one ring section to proceed
    if not ring2_lines and not ring3_lines:
        return result

    result['ring1_count'] = len(ring1_lines)
    result['ring2_count'] = len(ring2_lines)
    result['ring3_count'] = len(ring3_lines)

    # Build tabbed callout
    radio_name = make_radio_name(filepath)
    tabbed = build_tabbed_callout(ring1_lines, ring2_lines, ring3_lines, radio_name)

    if not tabbed:
        return result

    # Remove old ring sections and insert tabbed callout
    new_content = content

    # Remove Ring 3 first (it's usually after Ring 2)
    if r3_match:
        # Remove the header + body
        start = r3_match.start()
        end = r3_match.end()
        new_content = new_content[:start] + new_content[end:]

    # Recalculate Ring 2 position after Ring 3 removal
    r2_match_new, _ = extract_ring_section(new_content, RING2_PATTERN)
    if r2_match_new:
        start = r2_match_new.start()
        end = r2_match_new.end()
        # Insert tabbed callout where Ring 2 was
        new_content = new_content[:start] + tabbed + "\n\n" + new_content[end:]
    elif r2_match:
        # Ring 2 was found originally but position shifted — find it again
        start = r2_match.start()
        end = r2_match.end()
        new_content = content  # reset
        # Remove both and insert tabbed where Ring 2 starts
        # Remove Ring 3 first
        if r3_match:
            new_content = new_content[:r3_match.start()] + new_content[r3_match.end():]
        # Now remove Ring 2 and insert tabbed
        r2_again = RING2_PATTERN.search(new_content)
        if r2_again:
            new_content = new_content[:r2_again.start()] + tabbed + "\n\n" + new_content[r2_again.end():]
    else:
        # No Ring 2 existed, only Ring 3 — insert before where Ring 3 was
        # new_content already has Ring 3 removed, insert tabbed before the --- separator
        sep = re.search(r'^---\s*$', new_content[len(new_content)//2:], re.MULTILINE)
        if sep:
            pos = len(new_content)//2 + sep.start()
            new_content = new_content[:pos] + "\n" + tabbed + "\n\n" + new_content[pos:]
        else:
            new_content = new_content.rstrip() + "\n\n" + tabbed + "\n"

    # Clean up excess blank lines
    new_content = re.sub(r'\n{4,}', '\n\n\n', new_content)

    if new_content != content:
        result['changed'] = True
        if not dry_run:
            filepath.write_text(new_content, encoding='utf-8')

    return result


def verify_links(n: int = 10):
    """Verify that Ring 2/3 wikilinks resolve to actual files."""
    link_pattern = re.compile(r'\[\[00_Canonical/([^\]|#]+)')

    all_links = []
    for md_file in VAULT_ROOT.rglob("*.md"):
        if any(skip in str(md_file) for skip in SKIP_DIRS):
            continue
        try:
            content = md_file.read_text(encoding='utf-8', errors='replace')
        except:
            continue

        # Only check lines in Ring 2/3 sections
        in_ring = False
        for line in content.split('\n'):
            if 'Ring 2' in line or 'Ring 3' in line:
                in_ring = True
                continue
            if line.startswith('## ') and in_ring:
                in_ring = False
            if in_ring:
                for m in link_pattern.finditer(line):
                    target = m.group(1).strip()
                    if target.endswith('.md'):
                        target_path = VAULT_ROOT / "00_Canonical" / target
                    else:
                        target_path = VAULT_ROOT / "00_Canonical" / (target + ".md")
                    # Also try without .md
                    target_path2 = VAULT_ROOT / "00_Canonical" / target

                    resolved = target_path.exists() or target_path2.exists()
                    source = str(md_file.relative_to(VAULT_ROOT))
                    all_links.append({
                        'source': source,
                        'target': f"00_Canonical/{target}",
                        'resolved': resolved,
                        'target_path': str(target_path),
                    })

        if len(all_links) >= n * 5:  # collect plenty
            break

    # Report
    valid = [l for l in all_links if l['resolved']]
    broken = [l for l in all_links if not l['resolved']]

    print(f"\n{'='*70}")
    print(f"RING LINK VERIFICATION")
    print(f"{'='*70}")
    print(f"Total ring links checked: {len(all_links)}")
    print(f"Valid:  {len(valid)}")
    print(f"Broken: {len(broken)}")

    if broken:
        print(f"\nBroken links (first {min(n, len(broken))}):")
        for b in broken[:n]:
            print(f"  SRC: {b['source']}")
            print(f"  TGT: {b['target']}")
            # Try to find close matches
            target_stem = Path(b['target']).stem
            close = list((VAULT_ROOT / "00_Canonical").rglob(f"*{target_stem}*"))
            if close:
                print(f"  SUGGESTION: {close[0].relative_to(VAULT_ROOT)}")
            print()
    else:
        print("\nAll ring links resolve correctly!")

    return broken


def find_ring_files():
    """Find all files with Ring 2 or Ring 3 sections."""
    files = []
    for md_file in VAULT_ROOT.rglob("*.md"):
        rel = str(md_file.relative_to(VAULT_ROOT))
        if any(skip in rel for skip in SKIP_DIRS):
            continue
        if md_file.name in SKIP_FILES:
            continue
        try:
            content = md_file.read_text(encoding='utf-8', errors='replace')
        except:
            continue
        if RING2_PATTERN.search(content) or RING3_PATTERN.search(content):
            files.append(md_file)
    return files


def main():
    parser = argparse.ArgumentParser(description="Ring Tabbed Callout Wrapper")
    parser.add_argument("--test", type=str, help="Test on a single file (dry run)")
    parser.add_argument("--batch", type=int, help="Process first N ring files (dry run)")
    parser.add_argument("--apply", action="store_true", help="Actually write changes")
    parser.add_argument("--all", action="store_true", help="Process entire vault")
    parser.add_argument("--verify", type=int, default=0, help="Verify N ring links")
    parser.add_argument("--report", action="store_true", help="Stats only")
    args = parser.parse_args()

    if args.verify:
        verify_links(args.verify)
        return

    if args.test:
        target = Path(args.test)
        if not target.exists():
            # Try relative to vault
            target = VAULT_ROOT / args.test
        if not target.exists():
            # Try glob
            matches = list(VAULT_ROOT.rglob(f"*{args.test}*"))
            if matches:
                target = matches[0]
            else:
                print(f"File not found: {args.test}")
                return

        print(f"Testing on: {target.relative_to(VAULT_ROOT)}")
        result = process_file(target, dry_run=True)
        print(f"  Changed: {result['changed']}")
        print(f"  Ring 1: {result['ring1_count']} links")
        print(f"  Ring 2: {result['ring2_count']} links")
        print(f"  Ring 3: {result['ring3_count']} links")
        if result['already_tabbed']:
            print(f"  Already tabbed — skipping")
        if result['errors']:
            print(f"  Errors: {result['errors']}")

        # Show the transformed output
        if result['changed']:
            content = target.read_text(encoding='utf-8')
            radio_name = make_radio_name(target)
            ring1 = extract_ring1_from_yaml(content)
            _, ring2 = extract_ring_section(content, RING2_PATTERN)
            _, ring3 = extract_ring_section(content, RING3_PATTERN)
            tabbed = build_tabbed_callout(ring1, ring2, ring3, radio_name)
            print(f"\n--- TABBED CALLOUT PREVIEW ---\n")
            print(tabbed)
            print(f"\n--- END PREVIEW ---")
        return

    # Find all files with ring sections
    print("Scanning vault for files with Ring sections...")
    ring_files = find_ring_files()
    print(f"Found {len(ring_files)} files with Ring 2/3 sections.")

    if args.report:
        # Count by directory
        from collections import Counter
        dirs = Counter()
        for f in ring_files:
            rel = f.relative_to(VAULT_ROOT)
            dirs[rel.parts[0]] += 1
        print("\nBy top-level folder:")
        for d, c in dirs.most_common():
            print(f"  {d}: {c}")
        return

    # Determine targets
    if args.batch:
        targets = ring_files[:args.batch]
    elif args.all:
        targets = ring_files
    else:
        parser.print_help()
        return

    dry_run = not args.apply
    mode = "DRY RUN" if dry_run else "APPLYING"
    print(f"\n{mode} — Processing {len(targets)} files...\n")

    changed = 0
    skipped = 0
    errors = []

    for i, fp in enumerate(targets, 1):
        result = process_file(fp, dry_run=dry_run)
        if result['changed']:
            changed += 1
            print(f"  [{i:4d}/{len(targets)}] ✓ {result['file']}  "
                  f"R1:{result['ring1_count']} R2:{result['ring2_count']} R3:{result['ring3_count']}")
        elif result['already_tabbed']:
            skipped += 1
        elif result['errors']:
            errors.append(result)

        if i % 50 == 0 and not args.batch:
            print(f"  ... {i}/{len(targets)} processed, {changed} changed")

    print(f"\n{'─'*70}")
    print(f"Processed:  {len(targets)}")
    print(f"Changed:    {changed}")
    print(f"Skipped:    {skipped} (already tabbed)")
    print(f"Errors:     {len(errors)}")
    if errors:
        for e in errors[:10]:
            print(f"  {e['file']}: {e['errors']}")
    print(f"{'─'*70}")
    if dry_run:
        print("DRY RUN — no files written. Use --apply to write.")


if __name__ == "__main__":
    main()
