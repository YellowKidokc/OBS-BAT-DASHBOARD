#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_urls.py
Scan all .md files in 00_Canonical, extract frontmatter urls,
classify files as stub vs. has_content, output a CSV ready for bulk download.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os, re, csv
from pathlib import Path

VAULT = Path("O:/_Theophysics_v3")
CANONICAL = VAULT / "00_Canonical"
OUT_CSV = VAULT / "00_SYSTEM/00_ENGINE/canonical_urls.csv"

# Patterns
FRONTMATTER = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)
URL_FIELD = re.compile(r'^url:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)

STUB_MARKERS = {'Not found.', 'Not found', 'Theory overview not found.', 'Unknown Theory'}

def is_stub(content: str) -> bool:
    """True if file has no real body content."""
    # Remove frontmatter
    body = FRONTMATTER.sub('', content).strip()
    # Remove semantic labels block
    body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)
    body = re.sub(r'<details.*?</details>', '', body, flags=re.DOTALL)
    body = re.sub(r'%%---.*?%%', '', body, flags=re.DOTALL)
    body = re.sub(r'%%tag::.*', '', body)
    # Remove headers and Related Theories section
    body = re.sub(r'## Related Theories.*', '', body, flags=re.DOTALL)
    body = re.sub(r'^#+.*$', '', body, flags=re.MULTILINE)
    body = body.strip()

    if not body:
        return True
    # Check for stub markers
    for marker in STUB_MARKERS:
        if marker in body:
            return True
    # If remaining body is very short, probably a stub
    if len(body) < 150:
        return True
    return False

rows = []
total = stub_with_url = stub_no_url = has_content = 0
skip = {'DOMAIN_DASHBOARD.md', 'CANONICAL_INDEX.md', 'MASTER_INDEX.md',
        'NAVIGATION_GUIDE.md', 'SYSTEM_STATUS.md', 'THEORY_INTERCONNECTIONS.md',
        'CANONICAL_MAP.md', 'AXIOMS_COMPENDIUM.md', 'INDEX.md',
        'TEN_LAWS_CANONICAL_EQUATIONS.md'}

for root, dirs, files in os.walk(CANONICAL):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in sorted(files):
        if not f.endswith('.md') or f in skip:
            continue
        fp = Path(root) / f
        rel = str(fp.relative_to(VAULT))
        try:
            text = fp.read_text(encoding='utf-8', errors='replace')
        except:
            continue

        total += 1
        url_match = URL_FIELD.search(text)
        url = url_match.group(1).strip() if url_match else ''
        stub = is_stub(text)

        if stub and url:
            stub_with_url += 1
            rows.append({'path': rel, 'url': url, 'status': 'stub_has_url', 'filename': f})
        elif stub and not url:
            stub_no_url += 1
            rows.append({'path': rel, 'url': '', 'status': 'stub_no_url', 'filename': f})
        else:
            has_content += 1

print(f"Total theory files scanned: {total}")
print(f"  Has content:        {has_content}")
print(f"  Stub + has URL:     {stub_with_url}  ← downloadable")
print(f"  Stub + no URL:      {stub_no_url}  ← need manual sourcing")
print(f"\nDownloadable stubs: {stub_with_url}")

# Write CSV
with open(OUT_CSV, 'w', newline='', encoding='utf-8') as fh:
    writer = csv.DictWriter(fh, fieldnames=['path','filename','url','status'])
    writer.writeheader()
    writer.writerows(rows)

print(f"\nCSV written to: {OUT_CSV}")
print(f"Rows: {len(rows)}")

# Show sample URLs
print("\nSample downloadable URLs:")
for r in [x for x in rows if x['status'] == 'stub_has_url'][:20]:
    print(f"  {r['url']}")
