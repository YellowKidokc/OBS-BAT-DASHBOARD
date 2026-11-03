#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
canonical_downloader.py  v2

For each stub .md in 00_Canonical:
1. Use existing url: frontmatter field OR auto-generate Wikipedia URL from filename
2. Fetch FULL article via Wikipedia ?action=raw (wikitext)
3. Convert wikitext to clean markdown
4. Write canonical 7-section format back to file

Usage: python canonical_downloader.py [--dry-run] [--limit N] [--only-with-url]
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os, re, csv, time, json, argparse
from pathlib import Path
from urllib.parse import quote, urlparse
import urllib.request

VAULT = Path("O:/_Theophysics_v3")
CANONICAL = VAULT / "00_Canonical"
CSV_PATH = VAULT / "00_SYSTEM/00_ENGINE/canonical_urls.csv"
LOG_PATH = VAULT / "00_SYSTEM/00_ENGINE/download_log.csv"

USER_AGENT = "Theophysics-Vault-Bot/1.0 (research)"
FRONTMATTER_RE = re.compile(r'^(---\s*\n.*?\n---\s*\n)', re.DOTALL)

# Manual title overrides for known mismatches
TITLE_ALIASES = {
    'shannon_information_theory':       'Shannon entropy',
    'lambda-cdm_model':                 'Lambda-CDM model',
    'de_sitter_space':                  'De Sitter space',
    'holevo_bound':                     "Holevo's theorem",
    'margolus-levitin_theorem':         'Margolus–Levitin theorem',
    'noisy-channel_coding_theorem':     'Noisy-channel coding theorem',
    'computational_universe_(lloyd)':   'Programming the Universe',
    'digital_physics_(zuse,_fredkin)':  'Digital physics',
    'integrated_information_theory_(tononi)': 'Integrated information theory',
    'orch_or_(penrose-hameroff)':       'Orchestrated objective reduction',
    'participatory_anthropic_principle_(pap)': 'Participatory anthropic principle',
    'fmri_moral_judgment_(greene)':     'Joshua Greene (psychologist)',
    'chalmers':                         'David Chalmers',
    'von_neumann':                      'John von Neumann',
    'libet_experiments':                'Neuroscience of free will',
    'split-brain_studies':              'Split-brain',
    'global_consciousness_project':     'Global Consciousness Project',
    'algorithmic_information_theory':   'Algorithmic information theory',
    'einstein\'s_general_theory_of_relativity': 'General relativity',
}


def stem_to_wiki_title(stem: str) -> str:
    """Convert filename stem to Wikipedia article title."""
    key = stem.lower()
    if key in TITLE_ALIASES:
        return TITLE_ALIASES[key]
    # Strip common prefixes
    title = re.sub(r'^(TH_[A-Za-z_]+__|Quantum_Dimensions__)', '', stem)
    title = title.replace('_', ' ').replace('-', ' ')
    title = re.sub(r'\s*\(.*?\)\s*$', '', title)  # remove trailing (Author)
    title = re.sub(r'\s+', ' ', title).strip()
    return title


def strip_wikitext(wikitext: str) -> str:
    """Convert Wikipedia wikitext to clean plain text / markdown."""
    text = wikitext

    # Remove references
    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<ref[^>]*/>', '', text)

    # Remove comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    # Remove templates except keep their text content in some cases
    # Simple templates like {{short description|...}} → remove
    # Nested template removal (iterative)
    for _ in range(6):
        text = re.sub(r'\{\{[^{}]*\}\}', '', text)

    # Remove tables
    text = re.sub(r'\{\|.*?\|\}', '', text, flags=re.DOTALL)

    # Convert section headers to markdown
    text = re.sub(r'^====\s*(.*?)\s*====', r'#### \1', text, flags=re.MULTILINE)
    text = re.sub(r'^===\s*(.*?)\s*===', r'### \1', text, flags=re.MULTILINE)
    text = re.sub(r'^==\s*(.*?)\s*==', r'## \1', text, flags=re.MULTILINE)

    # Convert wikilinks: [[target|text]] → text, [[target]] → target
    text = re.sub(r'\[\[(?:File|Image|Category):[^\]]+\]\]', '', text)
    text = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', text)
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)

    # Convert external links: [url text] → text, [url] → url
    text = re.sub(r'\[https?://\S+\s+([^\]]+)\]', r'\1', text)
    text = re.sub(r'\[https?://\S+\]', '', text)

    # Bold/italic
    text = re.sub(r"'{3}(.*?)'{3}", r'**\1**', text)
    text = re.sub(r"'{2}(.*?)'{2}", r'*\1*', text)

    # HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&nbsp;', ' ').replace('&ndash;', '–').replace('&mdash;', '—')

    # Clean up blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)

    return text.strip()


def fetch_wiki_raw(title: str) -> tuple[str, str] | tuple[None, None]:
    """
    Fetch full Wikipedia article wikitext.
    Returns (clean_text, canonical_url) or (None, None).
    """
    enc_title = quote(title.replace(' ', '_'))
    raw_url = f"https://en.wikipedia.org/wiki/{enc_title}?action=raw"
    canon_url = f"https://en.wikipedia.org/wiki/{enc_title}"

    req = urllib.request.Request(raw_url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            if resp.status == 200:
                raw = resp.read().decode('utf-8', errors='replace')
                if raw.startswith('#REDIRECT'):
                    # Follow redirect
                    m = re.search(r'\[\[([^\]]+)\]\]', raw)
                    if m:
                        return fetch_wiki_raw(m.group(1))
                    return None, None
                return strip_wikitext(raw), canon_url
    except Exception:
        pass
    return None, None


def split_into_sections(text: str) -> dict:
    """Split markdown text into sections by ## headers."""
    sections = {}
    current = 'overview'
    buf = []

    for line in text.split('\n'):
        m = re.match(r'^(#{1,4})\s+(.+)', line)
        if m and m.group(1) in ('##', '###'):
            sections[current] = '\n'.join(buf).strip()
            current = m.group(2).lower()
            buf = [line]
        else:
            buf.append(line)
    sections[current] = '\n'.join(buf).strip()
    return sections


def get_sec(sections: dict, *keys) -> str:
    for k in keys:
        for sec_k, val in sections.items():
            if k.lower() in sec_k.lower() and val.strip():
                return val
    return '*Not found in source article.*'


def build_canonical_md(title: str, clean_text: str, url: str, frontmatter: str) -> str:
    """
    Build canonical markdown from full clean article text.
    Preserves the complete Wikipedia article content with canonical hub links.
    """
    # Update frontmatter
    if 'url:' not in frontmatter:
        fm = frontmatter.rstrip().rstrip('---').rstrip()
        fm += f'\nurl: "{url}"\nsource: Wikipedia\ndownloaded: 2026-02-26\n---\n'
    else:
        fm = frontmatter

    # Extract first paragraph as "overview" (text before the first ## heading)
    first_h2 = re.search(r'\n##\s', clean_text)
    if first_h2:
        intro = clean_text[:first_h2.start()].strip()
        body  = clean_text[first_h2.start():]
    else:
        intro = clean_text
        body  = ''

    return f"""{fm}# {title}

> [[00_Canonical/CANONICAL_INDEX|Canonical Index]] | [[00_Canonical/MASTER_INDEX|Master Index]] | [[00_Canonical/NAVIGATION_GUIDE|Navigation Guide]]

## Overview

{intro}

{body}

---

## Related Theories

*See [[00_Canonical/THEORY_INTERCONNECTIONS|Theory Interconnections]] for semantic links.*

---
*Source: [{title}]({url})*
*Downloaded: 2026-02-26 | Theophysics Canonical Knowledge Base*
"""


def process_row(row: dict, dry_run: bool, log_rows: list) -> str:
    path = VAULT / row['path']
    url = row['url'].strip()
    stem = path.stem

    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except FileNotFoundError:
        return 'FILE_NOT_FOUND'

    fm_match = FRONTMATTER_RE.match(text)
    frontmatter = fm_match.group(1) if fm_match else '---\ntitle: ""\n---\n'

    # Determine Wikipedia title
    clean_text, canon_url = None, None

    if 'wikipedia.org' in url:
        parts = urlparse(url)
        wiki_title = parts.path.split('/wiki/')[-1].replace('_', ' ')
        clean_text, canon_url = fetch_wiki_raw(wiki_title)
    elif url and url not in ('', 'null', 'None'):
        # Non-Wikipedia — skip for now
        log_rows.append({'path': row['path'], 'status': 'NON_WIKI_URL', 'url': url})
        return 'NON_WIKI_URL'

    if not clean_text:
        wiki_title = stem_to_wiki_title(stem)
        clean_text, canon_url = fetch_wiki_raw(wiki_title)

    if not clean_text:
        log_rows.append({'path': row['path'], 'status': 'NOT_FOUND', 'url': url or stem})
        return 'NOT_FOUND'

    display_title = canon_url.split('/wiki/')[-1].replace('_', ' ') if canon_url else stem
    new_content = build_canonical_md(display_title, clean_text, canon_url, frontmatter)

    if dry_run:
        log_rows.append({'path': row['path'], 'status': 'DRY_RUN', 'url': canon_url})
        return f'DRY_RUN ({len(new_content):,} chars)'

    path.write_text(new_content, encoding='utf-8')
    log_rows.append({'path': row['path'], 'status': 'DOWNLOADED', 'url': canon_url})
    return f'OK ({len(new_content):,} chars)'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--only-with-url', action='store_true')
    args = parser.parse_args()

    with open(CSV_PATH, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    stubs = [r for r in rows if 'stub' in r['status']]
    if args.only_with_url:
        stubs = [r for r in stubs if r['url']]
    if args.limit:
        stubs = stubs[:args.limit]

    print(f"Processing {len(stubs)} stubs {'(DRY RUN)' if args.dry_run else ''}\n")

    log_rows = []
    counts: dict = {}

    for i, row in enumerate(stubs, 1):
        fname = Path(row['path']).name
        print(f"  [{i}/{len(stubs)}] {fname}", end=' ... ', flush=True)
        result = process_row(row, args.dry_run, log_rows)
        print(result)
        key = result.split()[0]
        counts[key] = counts.get(key, 0) + 1
        time.sleep(0.4)

    # Append to log
    write_header = not LOG_PATH.exists()
    with open(LOG_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['path', 'status', 'url'])
        if write_header:
            writer.writeheader()
        writer.writerows(log_rows)

    print(f"\n--- Summary ---")
    for k, v in sorted(counts.items()):
        print(f"  {k:15s}: {v}")
    print(f"\nLog: {LOG_PATH}")


if __name__ == '__main__':
    main()
