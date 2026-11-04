#!/usr/bin/env python3
"""VAULT_PULSE - what changed in the vault since you last looked.

  vault_pulse.py VAULT [--hours 24]

First run records a baseline (path, size, mtime, SHA-256 for small text files)
under %USERPROFILE%\\VaultOps\\state\\. Every later run compares against it:
NEW, MODIFIED, DELETED, MOVED/RENAMED (same content at a new path), plus
anything touched in the last N hours. Bursts are flagged: many deletions,
mass renames, zero-byte files, sync-conflict copies, .obsidian config changes.
The vault is only read.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, re, sys, time
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _common import vaultops_home, write_report  # noqa: E402

SKIP = {".git", ".trash", "node_modules", "__pycache__", ".obsidian/cache"}
HASH_MAX = 5 * 1024 * 1024
CONFLICT = re.compile(r"conflict|\(\d+\)\.\w+$|sync-conflict|\.sync-", re.I)


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def scan(vault: Path, prev: dict) -> dict:
    snap = {}
    for d, dn, fn in os.walk(vault):
        dn[:] = [x for x in dn if x not in SKIP]
        for f in fn:
            p = Path(d) / f
            try:
                st = p.stat()
            except OSError:
                continue
            rel = p.relative_to(vault).as_posix()
            old = prev.get(rel)
            if old and old["size"] == st.st_size and old["mtime"] == int(st.st_mtime):
                snap[rel] = old  # unchanged: reuse hash, fast
                continue
            snap[rel] = {"size": st.st_size, "mtime": int(st.st_mtime),
                         "sha": sha(p) if st.st_size <= HASH_MAX else f"size:{st.st_size}"}
    return snap


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vault")
    ap.add_argument("--hours", type=float, default=24)
    a = ap.parse_args(argv)
    vault = Path(a.vault).resolve()
    if not vault.is_dir():
        print(f"Vault not reachable: {vault}")
        return 2
    state_dir = vaultops_home() / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(str(vault).lower().encode()).hexdigest()[:12]
    state = state_dir / f"pulse_{key}.json"
    prev_doc = json.loads(state.read_text(encoding="utf-8")) if state.exists() else None
    prev = prev_doc["files"] if prev_doc else {}
    t0 = time.time()
    snap = scan(vault, prev)
    took = time.time() - t0
    cutoff = time.time() - a.hours * 3600
    now = dt.datetime.now()

    new = sorted(set(snap) - set(prev)) if prev_doc else []
    gone = sorted(set(prev) - set(snap)) if prev_doc else []
    modified = sorted(k for k in set(snap) & set(prev) if snap[k]["sha"] != prev[k]["sha"])
    # moves: a deleted path whose content reappears at a new path
    by_sha_new = {}
    for k in new:
        by_sha_new.setdefault(snap[k]["sha"], []).append(k)
    moved = []
    for k in gone:
        s = prev[k]["sha"]
        if not s.startswith("size:") and by_sha_new.get(s):
            moved.append((k, by_sha_new[s].pop(0)))
    moved_from, moved_to = {m[0] for m in moved}, {m[1] for m in moved}
    new = [k for k in new if k not in moved_to]
    gone = [k for k in gone if k not in moved_from]
    recent = sorted((k for k, v in snap.items() if v["mtime"] >= cutoff), key=lambda k: -snap[k]["mtime"])

    flags = []
    if prev_doc:
        n_prev = len(prev)
        if gone and len(gone) >= max(25, n_prev * 0.02):
            flags.append(("CRITICAL", f"{len(gone)} files deleted since last pulse ({len(gone) / max(n_prev, 1):.1%} of vault)"))
        if len(moved) >= 50:
            flags.append(("HIGH", f"{len(moved)} files moved/renamed - mass reorganisation or a sync tool at work?"))
        if any(k.startswith(".obsidian/") for k in modified + new + gone):
            flags.append(("MEDIUM", "Obsidian configuration changed (.obsidian/) - plugins/settings"))
    zero = [k for k in recent if snap[k]["size"] == 0 and k.endswith(".md")]
    if zero:
        flags.append(("HIGH" if len(zero) > 10 else "MEDIUM", f"{len(zero)} recently touched notes are EMPTY (0 bytes)"))
    conf = [k for k in (new if prev_doc else recent) if CONFLICT.search(Path(k).name)]
    if conf:
        flags.append(("HIGH", f"{len(conf)} possible sync-conflict copies"))

    flags.sort(key=lambda f: ["CRITICAL", "HIGH", "MEDIUM", "LOW"].index(f[0]))
    folders = Counter(k.split("/")[0] if "/" in k else "(root)" for k in recent)
    total = sum(v["size"] for v in snap.values())
    prev_total = sum(v["size"] for v in prev.values()) if prev_doc else None
    since = prev_doc["taken"] if prev_doc else None

    def lst(title, items, fmt=lambda x: f"- `{x}`", cap=60):
        if not items:
            return []
        return [f"### {title} ({len(items)})", ""] + [fmt(i) for i in items[:cap]] + ([f"- … {len(items) - cap} more"] if len(items) > cap else []) + [""]

    md = [f"# VAULT_PULSE — {now:%Y-%m-%d %H:%M}", "", f"Vault: `{vault}`", "",
          f"**{len(snap):,} files · {total / 1e9:.2f} GB**" + (f" (Δ {len(snap) - len(prev):+,} files, {(total - prev_total) / 1e6:+.1f} MB since {since})" if prev_doc else " — first run: baseline recorded, change detection starts next run."), "",
          f"Scan took {took:.1f}s.", ""]
    md += ["## Flags", ""] + ([f"- **{s}** — {m}" for s, m in flags] or ["- None. Nothing unusual."]) + [""]
    if prev_doc:
        md += [f"## Since last pulse ({since})", "",
               f"| New | Modified | Deleted | Moved/renamed |", "|---|---|---|---|",
               f"| {len(new)} | {len(modified)} | {len(gone)} | {len(moved)} |", ""]
        md += lst("New", new) + lst("Modified", modified) + lst("Deleted", gone) + lst("Moved / renamed", moved, lambda m: f"- `{m[0]}` → `{m[1]}`")
    md += [f"## Touched in the last {a.hours:g} hours ({len(recent)})", ""]
    md += [f"| Folder | Files |", "|---|---|"] + [f"| {f} | {n} |" for f, n in folders.most_common(15)] + [""]
    md += lst("Most recent", recent, lambda k: f"- {dt.datetime.fromtimestamp(snap[k]['mtime']):%m-%d %H:%M}  `{k}`", 40)
    md += lst("Empty notes", zero) + lst("Sync-conflict candidates", conf)
    md += ["---", "Not checked: change_log entries (no change_log source configured for this tool yet)."]

    state.write_text(json.dumps({"vault": str(vault), "taken": f"{now:%Y-%m-%d %H:%M}", "files": snap}), encoding="utf-8")
    report = write_report("vault_pulse", "\n".join(md))
    print(f"{len(snap):,} files. " + (f"New {len(new)}, modified {len(modified)}, deleted {len(gone)}, moved {len(moved)} since {since}." if prev_doc else "Baseline recorded."))
    print(f"Touched in last {a.hours:g}h: {len(recent)}")
    for s, m in flags:
        print(f"  [{s}] {m}")
    print(f"Report: {report}")
    return 1 if any(s == "CRITICAL" for s, _ in flags) else 0


if __name__ == "__main__":
    raise SystemExit(main())
