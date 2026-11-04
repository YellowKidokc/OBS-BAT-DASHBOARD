#!/usr/bin/env python3
"""Bring a folder "in house": verified copy into the managed workspace.

The original is only read. Every copied file is SHA-256 checked against its
source; any mismatch fails the run. Prints the workspace copy's path on the
last line of stdout (so batch files can capture it) and writes a receipt.

Workspace root: %VAULTOPS_WORKSPACE% if set, else ~/VaultOps/WORKSPACE.
Each intake gets its own folder: <name>__YYYYMMDD-HHMMSS (never reused).
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, sys
from datetime import datetime
from pathlib import Path

SKIP = {".git"}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def workspace_root() -> Path:
    return Path(os.environ.get("VAULTOPS_WORKSPACE") or Path.home() / "VaultOps" / "WORKSPACE").resolve()


def intake(src: Path, dry: bool) -> Path | None:
    ws = workspace_root()
    if ws == src or src in ws.parents or ws in src.parents:
        raise SystemExit(f"Refusing: source and workspace overlap ({src} / {ws}).")
    files = [Path(d) / f for d, dn, fn in os.walk(src) for f in fn
             if not (dn.__setitem__(slice(None), [x for x in dn if x not in SKIP]))]
    total = sum(f.stat().st_size for f in files)
    free = shutil.disk_usage(ws if ws.exists() else ws.anchor).free
    dest = ws / f"{src.name}__{datetime.now():%Y%m%d-%H%M%S}"
    print(f"Bring in house: {src}\n  -> {dest}\n  {len(files)} files, {total:,} bytes (free: {free:,})", file=sys.stderr)
    if total > free * 0.9:
        raise SystemExit("Not enough free space in the workspace.")
    if dry:
        return None
    dest.mkdir(parents=True)
    rows, bad = [], 0
    for f in files:
        rel = f.relative_to(src)
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, out)
        h1, h2 = sha256(f), sha256(out)
        ok = h1 == h2
        bad += not ok
        rows.append({"path": rel.as_posix(), "bytes": f.stat().st_size, "sha256": h1, "verified": ok})
    for d, dn, _ in os.walk(src):  # keep empty folders too
        dn[:] = [x for x in dn if x not in SKIP]
        for x in dn:
            (dest / Path(d, x).relative_to(src)).mkdir(parents=True, exist_ok=True)
    meta = ws / "_receipts"
    meta.mkdir(exist_ok=True)
    (meta / f"{dest.name}.json").write_text(json.dumps(
        {"action": "inhouse_copy", "source": str(src), "copy": str(dest), "files": len(rows),
         "bytes": total, "failures": bad, "timestamp": datetime.now().isoformat(timespec="seconds"),
         "note": "Original untouched. Delete this copy when done; the source is the authority.",
         "items": rows}, indent=1), encoding="utf-8")
    if bad:
        raise SystemExit(f"{bad} files failed hash verification. Copy kept for inspection at {dest}.")
    print(f"Verified {len(rows)} files.", file=sys.stderr)
    return dest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Verified copy of a folder into the VaultOps workspace.")
    ap.add_argument("folder")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    src = Path(a.folder).resolve()
    if not src.is_dir():
        print(f"Not a folder: {src}", file=sys.stderr)
        return 2
    dest = intake(src, a.dry_run)
    if dest:
        print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
