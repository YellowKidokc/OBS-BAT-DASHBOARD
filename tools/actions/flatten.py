#!/usr/bin/env python3
"""Flatten a folder tree into its root, then remove the folders left empty.

Safety (ONE_MASTER_PROMPT §3, §11):
- Dry run by default; --apply is required to change anything.
- Never overwrites: name collisions get ` (2)`, ` (3)`... suffixes.
- Every move is recorded in a manifest (original relative path, new name,
  size, SHA-256) written BEFORE the first move and finalized after.
- Folders are removed only if completely empty (os.rmdir, never recursive).
  A folder that still holds anything (hidden files included) is kept and reported.
- `.obsidian`, `.git` and the manifest folder are skipped entirely.
- `--undo MANIFEST` moves every file back to its original path.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, os, sys
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"
SKIP = {".obsidian", ".git", "_flatten_manifests"}
MANIFEST_DIR = "_flatten_manifests"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def unique_name(name: str, taken: set[str]) -> str:
    stem, ext = os.path.splitext(name)
    cand, n = name, 2
    while cand.lower() in taken:
        cand, n = f"{stem} ({n}){ext}", n + 1
    taken.add(cand.lower())
    return cand


def plan(root: Path):
    taken = {p.name.lower() for p in root.iterdir() if p.is_file()}
    moves, dirs = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        dirnames[:] = sorted(x for x in dirnames if x not in SKIP)
        if d == root:
            continue
        dirs.append(d)
        for fn in sorted(filenames):
            src = d / fn
            new = unique_name(fn, taken)
            moves.append({"original": src.relative_to(root).as_posix(), "new_name": new,
                          "renamed": "Y" if new != fn else "N", "size_bytes": src.stat().st_size})
    return moves, dirs


def flatten(root: Path, apply: bool) -> int:
    moves, dirs = plan(root)
    renamed = sum(m["renamed"] == "Y" for m in moves)
    total = sum(m["size_bytes"] for m in moves)
    print(f"Folder: {root}")
    print(f"Files to move up: {len(moves)}  ({total:,} bytes)   name collisions renamed: {renamed}")
    print(f"Subfolders: {len(dirs)}  (only ones left completely empty will be removed)")
    for m in moves[:40]:
        flag = "  [RENAMED]" if m["renamed"] == "Y" else ""
        print(f"  {m['original']}  ->  {m['new_name']}{flag}")
    if len(moves) > 40:
        print(f"  ... and {len(moves) - 40} more (all listed in the manifest)")
    if not apply:
        print("\nDRY RUN - nothing changed. Re-run with --apply to do it.")
        return 0
    if not moves and not dirs:
        print("Nothing to do.")
        return 0
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    mdir = root / MANIFEST_DIR
    mdir.mkdir(exist_ok=True)
    manifest = mdir / f"flatten_{stamp}.csv"
    fields = ["original", "new_name", "renamed", "size_bytes", "sha256", "status"]
    for m in moves:
        m["sha256"] = sha256(root / m["original"])
        m["status"] = "planned"
    write(manifest, fields, moves)  # written before any move
    failures = 0
    for m in moves:
        src, dst = root / m["original"], root / m["new_name"]
        try:
            if dst.exists():
                raise FileExistsError(f"{dst.name} appeared during run")
            os.rename(src, dst)  # same volume: atomic, no copy
            m["status"] = "moved"
        except OSError as e:
            m["status"] = f"FAILED: {e}"
            failures += 1
    write(manifest, fields, moves)
    removed, kept = [], []
    for d in sorted(dirs, key=lambda p: len(p.parts), reverse=True):
        try:
            os.rmdir(d)  # fails if anything is inside
            removed.append(d.relative_to(root).as_posix())
        except OSError:
            kept.append(d.relative_to(root).as_posix())
    receipt = {"tool": "flatten.py", "version": VERSION, "root": str(root), "timestamp": stamp,
               "files_moved": sum(m["status"] == "moved" for m in moves), "failures": failures,
               "renamed": renamed, "folders_removed": removed, "folders_kept_not_empty": kept,
               "manifest": manifest.name,
               "recovery": f'python flatten.py --undo "{manifest}"'}
    (mdir / f"flatten_{stamp}_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"\nMoved {receipt['files_moved']} files, {failures} failures. "
          f"Removed {len(removed)} empty folders, kept {len(kept)} non-empty.")
    print(f"Manifest: {manifest}\nUndo: {receipt['recovery']}")
    return 1 if failures else 0


def undo(manifest: Path, apply: bool) -> int:
    root = manifest.parent.parent
    rows = list(csv.DictReader(manifest.open(encoding="utf-8")))
    todo = [r for r in rows if r["status"] == "moved"]
    print(f"Restore {len(todo)} files under {root}")
    if not apply:
        for r in todo[:40]:
            print(f"  {r['new_name']}  ->  {r['original']}")
        print("\nDRY RUN - nothing changed. Re-run with --apply to restore.")
        return 0
    bad = 0
    for r in todo:
        src, dst = root / r["new_name"], root / r["original"]
        if not src.exists() or dst.exists() or sha256(src) != r["sha256"]:
            print(f"  SKIP {r['new_name']} (missing, changed since flatten, or target exists)")
            bad += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        os.rename(src, dst)
        r["status"] = "restored"
    write(manifest, list(rows[0].keys()), rows)
    print(f"Restored {len(todo) - bad}, skipped {bad}.")
    return 1 if bad else 0


def write(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Flatten a folder safely (dry run by default).")
    ap.add_argument("folder", nargs="?")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--undo", metavar="MANIFEST")
    a = ap.parse_args(argv)
    if a.undo:
        return undo(Path(a.undo).resolve(), a.apply)
    if not a.folder:
        ap.error("folder is required")
    root = Path(a.folder).resolve()
    if not root.is_dir():
        print(f"Not a folder: {root}", file=sys.stderr)
        return 2
    if root == Path(root.anchor) or root == Path.home():
        print("Refusing to flatten a drive root or home folder.", file=sys.stderr)
        return 2
    return flatten(root, a.apply)


if __name__ == "__main__":
    raise SystemExit(main())
