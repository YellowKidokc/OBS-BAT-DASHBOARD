#!/usr/bin/env python3
"""
file_loose_papers.py
Move stray single papers out of vault root / folder roots.

Usage:
    python file_loose_papers.py --dry-run
    python file_loose_papers.py --apply
"""

import argparse
import csv
import io
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

VAULT = Path("O:/_Theophysics_v3")
NOTES      = VAULT / "06_NOTES"
GLOSSARY   = VAULT / "00_Canonical/Glossary"
TH_MATH    = VAULT / "00_Canonical/TH_Mathematics"
STUB_ARCH  = VAULT / "_ARCHIVE/STUBS_20260302"

MANIFEST_PATH = VAULT / "_ARCHIVE" / f"manifest_loose_papers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# ── Move table ─────────────────────────────────────────────────────────────────
# (source_relative, dest_dir, new_filename_or_None)
MOVES = [
    # Named papers → _Waiting_To_Review
    ("04_THEOPYHISCS/Father_as_Source_Field.md",          NOTES, None),
    ("04_THEOPYHISCS/Heaven-Hell-as-Attractor-States.md", NOTES, None),
    ("04_THEOPYHISCS/The Grace Factor.md",                NOTES, None),
    ("04_THEOPYHISCS/__Math Is Moral.md",                 NOTES, "Math_Is_Moral.md"),
    ("04_THEOPYHISCS/Visual Narrative.md",                NOTES, None),
    ("04_THEOPYHISCS/THEOPHYSICS_MASTER_PAPER.md",        NOTES, None),
    ("04_THEOPYHISCS/THEOPHYSICS_WELCOME 1.md",           NOTES, None),
    ("04_THEOPYHISCS/ONE-PAGE-FUNDER-SUMMARY.md",         NOTES, None),

    # Papers from 00_Canonical root
    ("00_Canonical/__It from Bit from Logos.md",                      NOTES, "It_from_Bit_from_Logos.md"),
    ("00_Canonical/__John Archibald Wheeler said It from Bit.md",     NOTES, "Wheeler_It_from_Bit.md"),

    # Untitled papers (renamed) → _Waiting_To_Review
    ("04_THEOPYHISCS/Untitled 1.md",  NOTES, "Epistemic-Bridges-Strategic-Framework.md"),
    ("04_THEOPYHISCS/Untitled 2.md",  NOTES, "The-Recursive-Cosmology.md"),
    ("04_THEOPYHISCS/Untitled 3.md",  NOTES, "The-Moral-Paradox.md"),
    ("04_THEOPYHISCS/Untitled 5.md",  NOTES, "The-Open-Door.md"),
    ("[52.5] Untitled 1.md",          NOTES, "The-Architecture-UFM.md"),
    ("06_NOTES/Untitled 1.md",        NOTES, "Quantum-Realm-Brainstorm.md"),

    # Glossary entry hiding in 04_THEOPYHISCS — already exists in Glossary, archive duplicate
    ("04_THEOPYHISCS/Observer.md",          STUB_ARCH, "Observer_DUPE.md"),

    # Wikipedia reference note
    ("04_THEOPYHISCS/Z2_Symmetry_Group.md", TH_MATH,  None),

    # Archive: stubs, web system docs, empty scraps
    ("04_THEOPYHISCS/Untitled.md",              STUB_ARCH, None),
    ("04_THEOPYHISCS/Untitled 4.md",            STUB_ARCH, None),
    ("02_DRAFTING/The..md",                     STUB_ARCH, None),
    ("06_NOTES/Untitled.md",                    STUB_ARCH, None),
    ("06_NOTES/Untitled 2.md",                  STUB_ARCH, None),
    ("04_THEOPYHISCS/site_map.md",              STUB_ARCH, None),
    ("04_THEOPYHISCS/_WEB_DEPLOY_PIPELINE.md",  STUB_ARCH, None),
]


def log(msg, dry):
    print(("[DRY-RUN] " if dry else "[APPLY]   ") + msg)


def move_file(src: Path, dest_dir: Path, new_name: str | None, dry: bool, rows: list):
    if not src.exists():
        log(f"SKIP (not found): {src.relative_to(VAULT)}", dry)
        return
    fname = new_name or src.name
    dest = dest_dir / fname
    # Collision avoidance: prefix with parent folder name
    if dest.exists():
        stem = Path(fname).stem
        suffix = Path(fname).suffix
        prefix = src.parent.name
        fname = f"{prefix}__{stem}{suffix}"
        dest = dest_dir / fname
    if dest.exists():
        log(f"SKIP (dest exists after dedup): {dest.relative_to(VAULT)}", dry)
        return
    action = "RENAME+MOVE" if new_name and new_name != src.name else "MOVE"
    log(f"{action}  {src.relative_to(VAULT)}\n          -> {dest.relative_to(VAULT)}", dry)
    rows.append({"action": action, "source": str(src), "destination": str(dest)})
    if not dry:
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))


def run(dry: bool):
    rows = []
    print("=" * 70)
    print("File Loose Papers — Vault Curation")
    print(f"Mode: {'DRY-RUN' if dry else 'APPLY'} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    for rel_src, dest_dir, new_name in MOVES:
        src = VAULT / rel_src
        move_file(src, dest_dir, new_name, dry, rows)

    print()
    print(f"Total moves: {len(rows)}")

    if rows and not dry:
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["action", "source", "destination"])
            w.writeheader()
            w.writerows(rows)
        log(f"Manifest: {MANIFEST_PATH}", dry)

    print("=" * 70)
    if dry:
        print("Re-run with --apply to execute.")


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = p.parse_args()
    run(dry=args.dry_run)


if __name__ == "__main__":
    main()
