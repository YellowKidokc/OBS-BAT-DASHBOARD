#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move clear quarantine files from 00_Canonical to 00_Canonical/_QUARANTINE/"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os, re, csv, shutil
from pathlib import Path
from datetime import datetime

VAULT = Path("O:/_Theophysics_v3")
CANONICAL = VAULT / "00_Canonical"
QUARANTINE = CANONICAL / "_QUARANTINE"
LOG = VAULT / "00_SYSTEM/00_ENGINE/quarantine_log.csv"

QUARANTINE.mkdir(exist_ok=True)

# Exact filenames to quarantine regardless of location
EXACT_NAMES = {
    'README_RESTRUCTURING.md',
    'RESTRUCTURING_STATUS.md',
    'THEORY_RELATIONSHIPS.md',
    'REVISION_04_RELEASE_SEQUENCE.md',
    'Body Mass Measurement Device.md',
    'abuse statistical techniques.md',
}

# Patterns for quarantine
PATTERNS = [
    r'^LOGOS_V3_REV4_SHORT_LOSSLESS_',   # archived lossless bundles
    r'^LOGOS_V3_REV4_LONG_LOSSLESS_',    # archived long bundles
]

# Sentence-format stubs (these are statements, not theory articles)
SENTENCE_STUBS = {
    'a material particle has non-zero rest mass.md',
    'a non-material subatomic particle always travels at the speed of light.md',
    'An induced electric current always tends to cancel the field change that caused it.md',
    'electric field lines can begin or end inside a region of space only when there is charge in that region.md',
    'electric field lines.md',
    'electromagnetic wave polarization.md',
    'Einstein\'s first postulate of special relativity.md',
    'Einstein\'s second postulate of special relativity.md',
    'a ray is an imaginary line along the direction of travel of the wave.md',
    'disks, and information media.md',
    'Doppler effect for electromagnetic waves.md',
    'degenerate quantum states.md',
    'dynamics of a sound wave.md',
    'dynamics of mechanical waves.md',
    'electric field line fringing.md',
    'coherent waves.md',
    'diffraction of light waves.md',
    'conservative force, field.md',
}

def should_quarantine(fp: Path) -> str | None:
    name = fp.name
    if name in EXACT_NAMES: return 'exact_name'
    if name in SENTENCE_STUBS: return 'sentence_stub'
    for pat in PATTERNS:
        if re.match(pat, name): return 'archived_bundle'
    return None

log_rows = []
moved = 0

for root, dirs, files in os.walk(CANONICAL):
    dirs[:] = [d for d in dirs if not d.startswith('_QUARANTINE')]
    for f in files:
        fp = Path(root) / f
        reason = should_quarantine(fp)
        if not reason:
            continue

        # Build quarantine subpath preserving domain context
        rel = fp.relative_to(CANONICAL)
        dest = QUARANTINE / rel
        dest.parent.mkdir(parents=True, exist_ok=True)

        # Avoid overwrite
        if dest.exists():
            dest = dest.with_stem(dest.stem + f'_{datetime.now().strftime("%H%M%S")}')

        shutil.move(str(fp), str(dest))
        moved += 1
        print(f"  MOVED [{reason}]: {rel}")
        log_rows.append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'source': str(fp.relative_to(VAULT)),
            'destination': str(dest.relative_to(VAULT)),
            'reason': reason,
        })

write_header = not LOG.exists()
with open(LOG, 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['date','source','destination','reason'])
    if write_header: writer.writeheader()
    writer.writerows(log_rows)

print(f"\nMoved {moved} files to _QUARANTINE/")
print(f"Log: {LOG}")
