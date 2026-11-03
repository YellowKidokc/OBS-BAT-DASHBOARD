#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
canonical_outbound_linker.py

For each canonical theory file:
1. Extract its title/name variants
2. Search all key Theophysics artifacts for mentions
3. Add a "## Theophysics Applications" section with wikilinks to matching papers

Key paper folders searched:
  05_PUBLICATIONS/Logos_Papers/
  05_PUBLICATIONS/Normalized_Manuscript/
  04_THEOPYHISCS/[6.5] JS-SERIES/
  04_THEOPYHISCS/[7.0] Paper_2_Quantum_Bridge/
  04_THEOPYHISCS/[7.2] Logic/
  04_THEOPYHISCS/[7.5] LAYER_1_LOGIC/
  04_THEOPYHISCS/[7.5] Psychology_Crisis/
  04_THEOPYHISCS/[7.6] Protocols/
  04_THEOPYHISCS/[7.7] Consciousness/
  04_THEOPYHISCS/[8.2] The_Great_Correction/
  04_THEOPYHISCS/GENESIS TO QUANTUM The Seven-Article Series/
  04_THEOPYHISCS/THREE TRUTHS/
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os, re
from pathlib import Path

VAULT = Path("O:/_Theophysics_v3")
CANONICAL = VAULT / "00_Canonical"

# Key Theophysics artifact folders (these are the "load-bearing" papers)
ARTIFACT_FOLDERS = [
    VAULT / "05_PUBLICATIONS/Logos_Papers",
    VAULT / "05_PUBLICATIONS/Normalized_Manuscript",
    VAULT / "05_PUBLICATIONS/Chapter Archive",
    VAULT / "04_THEOPYHISCS/[6.5] JS-SERIES",
    VAULT / "04_THEOPYHISCS/[7.0] Paper_2_Quantum_Bridge",
    VAULT / "04_THEOPYHISCS/[7.2] Logic",
    VAULT / "04_THEOPYHISCS/[7.5] LAYER_1_LOGIC",
    VAULT / "04_THEOPYHISCS/[7.5] Psychology_Crisis",
    VAULT / "04_THEOPYHISCS/[7.6] Protocols",
    VAULT / "04_THEOPYHISCS/[7.7] Consciousness",
    VAULT / "04_THEOPYHISCS/[8.2] The_Great_Correction",
    VAULT / "04_THEOPYHISCS/GENESIS TO QUANTUM The Seven-Article Series",
    VAULT / "04_THEOPYHISCS/THREE TRUTHS",
    VAULT / "04_THEOPYHISCS/MASTER_EQUATION_10_LAWS" if False else None,  # skip — it's canonical source
]
ARTIFACT_FOLDERS = [f for f in ARTIFACT_FOLDERS if f is not None]

SKIP_CANONICAL = {
    'CANONICAL_INDEX.md', 'MASTER_INDEX.md', 'NAVIGATION_GUIDE.md',
    'SYSTEM_STATUS.md', 'THEORY_INTERCONNECTIONS.md', 'CANONICAL_MAP.md',
    'EXTRACTION_METHODOLOGY.md', 'EXTRACTION_REPORT_PHASE_1.md',
    'AXIOM_CANONICAL_MAPPING.md', 'theory_relationships.json',
    'AXIOMS_COMPENDIUM.md', 'AXIOM_AND_THEORY_LINKS.md',
    'READY_FOR_AXIOM_EXTRACTION.md',
}
SKIP_ARTIFACT_NAMES = {
    'DOMAIN_DASHBOARD.md', 'INDEX.md', '_INDEX.md',
    'AXIOMS_COMPENDIUM.md', 'DOMAIN_DASHBOARD.csv',
}

THEOPHYSICS_SECTION = "## Theophysics Applications"


def build_artifact_index() -> list[dict]:
    """
    Load all key Theophysics papers into memory.
    Returns list of {path, vault_rel, title, text_lower}
    """
    papers = []
    for folder in ARTIFACT_FOLDERS:
        if not folder.exists():
            continue
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if not d.startswith(('.', '__'))
                       and 'MAIN_PAPERS' not in d]
            for f in files:
                if not f.endswith('.md') or f in SKIP_ARTIFACT_NAMES:
                    continue
                fp = Path(root) / f
                vault_rel = str(fp.relative_to(VAULT)).replace('\\', '/')
                try:
                    text = fp.read_text(encoding='utf-8', errors='replace')
                except Exception:
                    continue
                # Extract H1 title or use filename
                h1 = re.search(r'^#\s+(.+)', text, re.MULTILINE)
                title = h1.group(1).strip() if h1 else f[:-3].replace('_', ' ')
                papers.append({
                    'path': fp,
                    'vault_rel': vault_rel,
                    'title': title,
                    'text_lower': text.lower(),
                })
    return papers


def name_variants(stem: str) -> list[str]:
    """
    Generate search terms for a canonical theory filename stem.
    Returns list of lowercase strings to search for.
    """
    variants = set()
    base = stem
    # Strip common prefixes
    base = re.sub(r'^(TH_[A-Za-z_]+__|Quantum_Dimensions__|Law_\d+_\w+__)', '', base)
    base = re.sub(r'_\([^)]+\)$', '', base)   # trailing (Author)

    clean = base.replace('_', ' ').replace('-', ' ').strip()
    if clean:
        variants.add(clean.lower())
        # Also try without trailing numbers/spaces
        variants.add(re.sub(r'\s+\d+$', '', clean).lower().strip())

    # Key abbreviations
    abbrevs = {
        'integrated information theory': ['iit'],
        'orchestrated objective reduction': ['orch-or', 'orch or'],
        'hard problem of consciousness': ['hard problem'],
        'quantum mechanics': ['qm'],
        'general relativity': ['gr', 'general relativity'],
        'bell\'s theorem': ["bell's theorem", 'bell theorem'],
        'holographic principle': ['holographic principle', 'ads/cft', 'ads-cft'],
        'free energy principle': ['free energy principle'],
        'shannon entropy': ['shannon entropy', 'shannon information'],
        'kolmogorov complexity': ['kolmogorov complexity'],
        'global consciousness project': ['gcp'],
        'global workspace theory': ['gwt', 'global workspace'],
    }
    for key_term, abbr_list in abbrevs.items():
        if key_term in clean.lower():
            variants.update(abbr_list)

    return [v for v in variants if len(v) >= 6]


def find_matching_papers(variants: list[str], papers: list[dict]) -> list[dict]:
    """Find papers whose text contains any of the search variants as whole words."""
    matches = []
    for paper in papers:
        tl = paper['text_lower']
        for v in variants:
            # Require word boundary match to avoid false positives
            pattern = r'\b' + re.escape(v) + r'\b'
            if re.search(pattern, tl):
                matches.append(paper)
                break
    return matches


def has_theophysics_section(content: str) -> bool:
    return THEOPHYSICS_SECTION.lower() in content.lower()


def add_theophysics_section(content: str, matches: list[dict]) -> str:
    """Add or update the Theophysics Applications section."""
    links = []
    for p in matches:
        vr = p['vault_rel']
        vr_no_ext = vr[:-3] if vr.endswith('.md') else vr
        title = p['title']
        links.append(f"- [[{vr_no_ext}|{title}]]")

    section_text = f"\n{THEOPHYSICS_SECTION}\n\n" + '\n'.join(links) + '\n'

    # Replace existing section if present
    pattern = re.compile(
        r'\n' + re.escape(THEOPHYSICS_SECTION) + r'[^\n]*\n.*?(?=\n##\s|\Z)',
        re.DOTALL | re.IGNORECASE
    )
    if pattern.search(content):
        return pattern.sub(section_text, content)

    # Otherwise insert before Related Theories or append
    rt_match = re.search(r'\n## Related Theories', content, re.IGNORECASE)
    if rt_match:
        return content[:rt_match.start()] + section_text + content[rt_match.start():]

    return content.rstrip() + '\n' + section_text


def process_all(dry_run: bool = False):
    print("Loading Theophysics artifact index...")
    papers = build_artifact_index()
    print(f"  Loaded {len(papers)} artifact papers from {len(ARTIFACT_FOLDERS)} folders\n")

    linked = 0
    no_match = 0
    skipped = 0
    errors = 0

    for root, dirs, files in os.walk(CANONICAL):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in sorted(files):
            if not f.endswith('.md') or f in SKIP_CANONICAL:
                continue
            if f.startswith('DOMAIN_DASHBOARD') or f.startswith('_INDEX'):
                skipped += 1
                continue

            fp = Path(root) / f
            stem = f[:-3]
            variants = name_variants(stem)
            if not variants:
                skipped += 1
                continue

            try:
                content = fp.read_text(encoding='utf-8', errors='replace')
            except Exception as e:
                errors += 1
                continue

            matches = find_matching_papers(variants, papers)

            if not matches:
                no_match += 1
                continue

            new_content = add_theophysics_section(content, matches)
            if new_content == content:
                skipped += 1
                continue

            linked += 1
            rel = str(fp.relative_to(VAULT))
            print(f"  LINKED ({len(matches)} papers): {rel}")
            for m in matches:
                print(f"    → {m['title']}")

            if not dry_run:
                fp.write_text(new_content, encoding='utf-8')

    print(f"\n--- Summary ---")
    print(f"  Files linked:    {linked}")
    print(f"  No matches:      {no_match}")
    print(f"  Skipped:         {skipped}")
    print(f"  Errors:          {errors}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    process_all(dry_run=args.dry_run)
