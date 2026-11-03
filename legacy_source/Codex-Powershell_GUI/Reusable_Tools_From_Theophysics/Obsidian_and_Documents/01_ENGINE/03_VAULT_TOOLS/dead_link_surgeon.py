"""
dead_link_surgeon.py
Converts dead PATH-style wikilinks to plain text.
[[dead/path/to/File|Display]] → Display
[[dead/path/to/File]]         → File  (basename only)

Only touches links with "/" in them that cannot be resolved.
Bare-word links (no slash) are left untouched — Quartz resolves by basename.
"""
import re
from pathlib import Path

VAULT   = Path("O:/_Theophysics_v3")
SCAN    = ["04_THEOPYHISCS", "05_PUBLICATIONS"]
DRY_RUN = False   # set True to preview only

link_pat = re.compile(r'\[\[([^\]|#\[]+?)(?:\|([^\]]*))?\]\]')

def resolves(raw: str) -> bool:
    t = VAULT / raw
    return t.exists() or Path(str(t) + ".md").exists()

def fix_line(text: str) -> tuple[str, int]:
    count = 0
    def replace(m):
        nonlocal count
        raw     = m.group(1).strip()
        display = (m.group(2) or "").strip()
        if "/" not in raw:
            return m.group(0)          # bare-word — leave alone
        if resolves(raw):
            return m.group(0)          # valid path — leave alone
        count += 1
        if display:
            return display             # [[path|Display]] → Display
        # [[path/to/File]] → File
        return Path(raw).stem
    return link_pat.sub(replace, text), count

files_changed = 0
links_fixed   = 0
sample = []

for sd in SCAN:
    for fp in sorted((VAULT / sd).rglob("*.md")):
        try:
            original = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        fixed, n = fix_line(original)
        if n:
            links_fixed += n
            files_changed += 1
            if len(sample) < 5:
                sample.append((str(fp.relative_to(VAULT)), n))
            if not DRY_RUN:
                fp.write_text(fixed, encoding="utf-8")

mode = "DRY RUN" if DRY_RUN else "APPLIED"
print(f"[{mode}] Dead path links fixed: {links_fixed:,} across {files_changed:,} files")
print("\nSample files changed:")
for path, n in sample:
    print(f"  {n:4d} links  {path}")
