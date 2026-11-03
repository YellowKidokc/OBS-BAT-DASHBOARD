#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os, re
from pathlib import Path

VAULT = Path("O:/_Theophysics_v3")

# Build full canonical file index (with and without .md extension)
canonical_files = set()
for root, dirs, files in os.walk(VAULT / "00_Canonical"):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in files:
        if f.endswith('.md'):
            rel = (Path(root) / f).relative_to(VAULT).as_posix()
            canonical_files.add(rel)        # with .md
            canonical_files.add(rel[:-3])   # without .md

print(f"Canonical file index: {len(canonical_files)//2} files\n")

# Scan 04_THEOPYHISCS for [[00_Canonical/...]] wikilinks
pattern = re.compile(r'\[\[00_Canonical/([^\]|#\n]+)')
total = valid = broken = 0
broken_examples = []
source_files_with_broken = set()

SKIP_DIRS = {'.', '__pycache__', '_site', '_PENDING_DELETE'}

for root, dirs, files in os.walk(VAULT / "04_THEOPYHISCS"):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in SKIP_DIRS]
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = Path(root) / f
        try:
            text = fp.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        for m in pattern.finditer(text):
            raw = m.group(1).strip().rstrip('\\').strip()
            target = "00_Canonical/" + raw
            total += 1
            if target in canonical_files:
                valid += 1
            else:
                broken += 1
                rel_src = str(fp.relative_to(VAULT))
                source_files_with_broken.add(rel_src)
                if len(broken_examples) < 30:
                    broken_examples.append((rel_src, target))

print(f"Total [[00_Canonical/...]] refs in 04_THEOPYHISCS: {total}")
print(f"  Valid:  {valid}")
print(f"  Broken: {broken}")
print(f"  Source files with broken links: {len(source_files_with_broken)}")
print(f"\nSample broken links (first 20):")
for src, tgt in broken_examples[:20]:
    print(f"  SRC: {src}")
    print(f"  TGT: {tgt}")
    print()
