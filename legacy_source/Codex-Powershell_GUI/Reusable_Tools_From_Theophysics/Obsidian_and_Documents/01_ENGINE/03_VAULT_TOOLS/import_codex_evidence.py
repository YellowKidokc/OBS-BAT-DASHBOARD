#!/usr/bin/env python3
"""
import_codex_evidence.py
Import CODEX EXCEL and 07_Evidence_Extracts into the vault.

Usage:
    python import_codex_evidence.py --dry-run
    python import_codex_evidence.py --apply
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

VAULT        = Path("O:/_Theophysics_v3")
CODEX_SRC    = Path("C:/Users/lowes/OneDrive/Desktop/Folders/CODEX EXCEL")
EVIDENCE_SRC = Path("C:/Users/lowes/OneDrive/Desktop/Folders/07_Evidence_Extracts")

# Destinations
APOLOGETICS  = VAULT / "04_THEOPYHISCS/[6.2] 07_Apologetics/CODEX_EXCEL"
TH_PHIL_EV   = VAULT / "00_Canonical/TH_Philosophy/Evidence_Extracts"

MANIFEST_PATH = VAULT / "_ARCHIVE" / f"manifest_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# Tools extensions / filenames that go into Tools/
TOOL_EXTS    = {".py", ".xlsx", ".xls", ".txt", ".jsx"}
TOOL_DIRS    = {"_out"}


def log(msg, dry):
    print(("[DRY-RUN] " if dry else "[APPLY]   ") + msg)


def copy_file(src: Path, dest: Path, dry: bool, rows: list):
    if not src.exists():
        log(f"SKIP (not found): {src}", dry)
        return
    if dest.exists():
        log(f"SKIP (exists): {dest.relative_to(VAULT)}", dry)
        return
    log(f"COPY  {src.name}  ->  {dest.relative_to(VAULT)}", dry)
    rows.append({"source": str(src), "destination": str(dest)})
    if not dry:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dest))


def copy_dir(src_dir: Path, dest_dir: Path, dry: bool, rows: list):
    """Recursively copy a subdirectory."""
    for item in src_dir.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src_dir)
            dest = dest_dir / rel
            copy_file(item, dest, dry, rows)


def classify_codex_file(f: Path) -> str:
    """Return 'session', 'tool', or 'root' for a CODEX EXCEL file."""
    name = f.name
    # Dated session files
    if name.startswith("2026-") and f.suffix == ".md":
        return "session"
    # Tool files by extension or directory
    if f.suffix.lower() in TOOL_EXTS:
        return "tool"
    # README stays at root
    return "root"


def run(dry: bool):
    rows = []
    print("=" * 70)
    print("Import CODEX EXCEL + 07_Evidence_Extracts into Vault")
    print(f"Mode: {'DRY-RUN' if dry else 'APPLY'} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # ── 07_Evidence_Extracts → 00_Canonical/TH_Philosophy/Evidence_Extracts ──
    print(f"\n── Evidence Extracts → {TH_PHIL_EV.relative_to(VAULT)} ──")
    ev_files = sorted(EVIDENCE_SRC.glob("*.md"))
    log(f"{len(ev_files)} files to copy", dry)
    for f in ev_files:
        copy_file(f, TH_PHIL_EV / f.name, dry, rows)

    # ── CODEX EXCEL ───────────────────────────────────────────────────────────
    print(f"\n── CODEX EXCEL → {APOLOGETICS.relative_to(VAULT)} ──")

    sessions_dest = APOLOGETICS / "Sessions"
    tools_dest    = APOLOGETICS / "Tools"

    for item in CODEX_SRC.iterdir():
        # Handle _out/ subdirectory → Tools/_out/
        if item.is_dir() and item.name in TOOL_DIRS:
            log(f"DIR {item.name} → Tools/{item.name}/", dry)
            copy_dir(item, tools_dest / item.name, dry, rows)
            continue
        if not item.is_file():
            continue

        cls = classify_codex_file(item)
        if cls == "session":
            dest = sessions_dest / item.name
        elif cls == "tool":
            dest = tools_dest / item.name
        else:
            dest = APOLOGETICS / item.name

        copy_file(item, dest, dry, rows)

    print()
    print(f"Total files: {len(rows)}")

    if rows and not dry:
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["source", "destination"])
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
    g.add_argument("--apply",   action="store_true")
    p.parse_args()
    args = p.parse_args()
    run(dry=args.dry_run)


if __name__ == "__main__":
    main()
