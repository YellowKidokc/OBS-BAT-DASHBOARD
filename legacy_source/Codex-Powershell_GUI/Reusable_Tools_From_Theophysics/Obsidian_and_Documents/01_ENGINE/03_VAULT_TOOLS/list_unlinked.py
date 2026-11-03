#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os, re
from pathlib import Path

VAULT = Path("O:/_Theophysics_v3")
CANONICAL = VAULT / "00_Canonical"

SKIP = {
    'CANONICAL_INDEX.md','MASTER_INDEX.md','NAVIGATION_GUIDE.md','SYSTEM_STATUS.md',
    'THEORY_INTERCONNECTIONS.md','CANONICAL_MAP.md','EXTRACTION_METHODOLOGY.md',
    'EXTRACTION_REPORT_PHASE_1.md','AXIOM_CANONICAL_MAPPING.md','AXIOMS_COMPENDIUM.md',
    'AXIOM_AND_THEORY_LINKS.md','READY_FOR_AXIOM_EXTRACTION.md','theory_relationships.json',
}

THEOPHYSICS_SECTION = "## Theophysics Applications"

results = []

for root, dirs, files in os.walk(CANONICAL):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in sorted(files):
        if not f.endswith('.md') or f in SKIP: continue
        if f.startswith('DOMAIN_DASHBOARD') or f.startswith('_INDEX'): continue
        fp = Path(root) / f
        try:
            content = fp.read_text(encoding='utf-8', errors='replace')
        except: continue
        if THEOPHYSICS_SECTION.lower() in content.lower(): continue

        # Get domain from path
        rel = fp.relative_to(CANONICAL)
        parts = rel.parts
        domain = parts[0] if len(parts) > 1 else 'ROOT'

        # Get H1 title
        h1 = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        title = h1.group(1).strip() if h1 else f[:-3].replace('_',' ')

        # Has URL?
        has_url = 'url:' in content[:500]

        # Content length (rough body size)
        body = re.sub(r'^---.*?---', '', content, flags=re.DOTALL).strip()
        body_len = len(body)

        results.append({
            'domain': domain,
            'file': f,
            'title': title,
            'has_url': has_url,
            'body_len': body_len,
            'path': str(fp.relative_to(VAULT)),
        })

# Sort by domain then body length desc
results.sort(key=lambda x: (x['domain'], -x['body_len']))

print(f"Unlinked canonical files: {len(results)}\n")
print(f"{'Domain':<35} {'Body':>6}  {'URL':>3}  File")
print('-'*90)
for r in results:
    url_flag = 'Y' if r['has_url'] else '-'
    print(f"{r['domain']:<35} {r['body_len']:>6}  {url_flag:>3}  {r['file']}")
