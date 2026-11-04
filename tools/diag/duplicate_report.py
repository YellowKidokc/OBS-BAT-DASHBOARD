#!/usr/bin/env python3
"""DUPLICATE_REPORT - quick "how messy is this folder" check.

  duplicate_report.py FOLDER [--min-bytes 1]

Groups byte-identical files by SHA-256 (size pre-filter, so only same-size
files are hashed), reports wasted space, and lists same-name/different-content
collisions. Read-only. Report only - nothing here authorises deletion.
"""
from __future__ import annotations
import argparse, hashlib, os, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _common import write_report  # noqa: E402

SKIP = {".git", ".obsidian", "node_modules", "__pycache__", ".trash"}


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def human(b: float) -> str:
    for u in ("B", "KB", "MB", "GB"):
        if b < 1024:
            return f"{b:.0f} {u}" if u == "B" else f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.2f} TB"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--min-bytes", type=int, default=1)
    a = ap.parse_args(argv)
    root = Path(a.folder).resolve()
    by_size, by_name, n = defaultdict(list), defaultdict(set), 0
    for d, dn, fn in os.walk(root):
        dn[:] = [x for x in dn if x not in SKIP]
        for f in fn:
            p = Path(d) / f
            try:
                s = p.stat().st_size
            except OSError:
                continue
            n += 1
            if s >= a.min_bytes:
                by_size[s].append(p)
            by_name[f.lower()].add((s, p))
    groups = defaultdict(list)
    for s, ps in by_size.items():
        if len(ps) > 1:
            for p in ps:
                try:
                    groups[(s, sha(p))].append(p)
                except OSError:
                    pass
    fams = sorted(((s, ps) for (s, _), ps in groups.items() if len(ps) > 1), key=lambda x: -x[0] * (len(x[1]) - 1))
    wasted = sum(s * (len(ps) - 1) for s, ps in fams)
    collide = sorted((name, ps) for name, ps in by_name.items() if len({s for s, _ in ps}) > 1)
    rel = lambda p: p.relative_to(root).as_posix()
    md = [f"# DUPLICATE_REPORT", "", f"Folder: `{root}`", "",
          f"**{n:,} files · {len(fams):,} duplicate families · {sum(len(ps) for _, ps in fams):,} files involved · {human(wasted)} redundant**", "",
          "> Equal hashes prove equal bytes; they do not decide which copy is canonical. Nothing here authorises deletion.", "",
          "## Duplicate families (largest waste first)", ""]
    for s, ps in fams[:150]:
        md += [f"### {ps[0].name} — {len(ps)} copies × {human(s)} ({human(s * (len(ps) - 1))} redundant)", ""] + [f"- `{rel(p)}`" for p in sorted(ps)] + [""]
    if len(fams) > 150:
        md.append(f"… {len(fams) - 150} more families.\n")
    md += [f"## Same name, different content ({len(collide)})", "", "Same filename, different bytes: possible divergent versions.", ""]
    for name, ps in collide[:100]:
        md += [f"- **{name}**: " + "; ".join(f"`{rel(p)}` ({human(s)})" for s, p in sorted(ps, key=lambda x: -x[0])[:6])]
    report = write_report("duplicate_report", "\n".join(md))
    print(f"{n:,} files, {len(fams)} duplicate families, {human(wasted)} redundant, {len(collide)} name collisions.\nReport: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
