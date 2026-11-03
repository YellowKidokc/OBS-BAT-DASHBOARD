#!/usr/bin/env python3
"""Phase One read-only inventory (ONE_MASTER_PROMPT section 5).

Never modifies scanned roots: files are opened read-only, and the output
directory is refused if it lies inside any scanned root.
Stdlib only, Python 3.9+, Windows/Linux.

Usage:
  python inventory.py --root LABEL=PATH [--root LABEL=PATH ...] --out DIR
"""
from __future__ import annotations
import argparse, csv, hashlib, json, os, re, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.0"
SCRIPT_EXT = {".py": "python", ".ps1": "powershell", ".psm1": "powershell",
              ".bat": "batch", ".cmd": "batch", ".sh": "shell", ".js": "javascript",
              ".ts": "typescript", ".vbs": "vbscript", ".ahk": "autohotkey"}
TEXT_EXT = set(SCRIPT_EXT) | {".md", ".txt", ".yaml", ".yml", ".json", ".csv",
                              ".toml", ".ini", ".cfg", ".html", ".css", ".xml"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}
MAX_TEXT = 5 * 1024 * 1024

STALE = [
    ("drive_O", re.compile(r"\bO:[\\/]")),
    ("drive_Z", re.compile(r"\bZ:[\\/]")),
    ("old_vault_version", re.compile(r"_Theophysics_v[0-3]\b")),
    ("lan_ip", re.compile(r"\b192\.168\.\d{1,3}\.\d{1,3}\b")),
    ("unc_path", re.compile(r"\\\\[A-Za-z0-9_.-]+\\[A-Za-z0-9_$.-]+")),
    ("abs_windows_path", re.compile(r"\b[A-Za-z]:\\\\?[A-Za-z0-9_]")),
]
DELETE = re.compile(r"os\.remove\(|os\.unlink\(|\.unlink\(|shutil\.rmtree|\bos\.rmdir|Remove-Item|"
                    r"^\s*(?:@?del|erase|rd|rmdir)\s", re.I | re.M)
MOVE = re.compile(r"shutil\.move|os\.rename|os\.replace|\.rename\(|\.replace\(\s*[A-Za-z_]*path|"
                  r"Move-Item|Rename-Item|^\s*(?:move|ren|rename)\s", re.I | re.M)
WRITE = re.compile(r"open\([^)]*['\"][wa]b?\+?['\"]|\.write_text\(|\.write_bytes\(|Set-Content|"
                   r"Out-File|Add-Content|Copy-Item|shutil\.copy|>\s*\"?%", re.I | re.M)
DRYRUN = re.compile(r"dry[-_ ]?run|--preview|WhatIf", re.I)
RECEIPT = re.compile(r"receipt|manifest", re.I)
SECRET_REF = re.compile(r"api[_-]?key|OPENAI_API_KEY|ANTHROPIC_API_KEY|Authorization|Bearer", re.I)
SECRET_LITERAL = re.compile(r"sk-[A-Za-z0-9_-]{20,}|(?:api[_-]?key|token|secret)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]", re.I)
NETWORK = re.compile(r"requests\.|httpx|urllib\.request|openai|anthropic|Invoke-RestMethod|Invoke-WebRequest|curl ", re.I)
GUI = re.compile(r"PySide|PyQt|tkinter|customtkinter|Windows\.Forms|fastapi|flask", re.I)
CLI = re.compile(r"argparse|sys\.argv|click\b|typer\b|param\s*\(|%~?1", re.I)
PY_IMPORT = re.compile(r"^\s*(?:from\s+([A-Za-z_][\w.]*)\s+import|import\s+([A-Za-z_][\w.]*))", re.M)
DOCSTRING = re.compile(r'^\s*(?:#![^\n]*\n)?\s*(?:"""|\'\'\')(.*?)(?:"""|\'\'\')', re.S)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(p: Path) -> str | None:
    try:
        if p.stat().st_size > MAX_TEXT:
            return None
        return p.read_bytes().decode("utf-8", errors="replace")
    except OSError:
        return None


def purpose(text: str, ext: str) -> str:
    if ext == ".py":
        m = DOCSTRING.match(text)
        if m:
            return " ".join(m.group(1).split())[:200]
    for line in text.splitlines()[:15]:
        s = line.strip().lstrip("#").lstrip("REM").lstrip(":").strip()
        if len(s) > 12 and not s.startswith(("!", "@echo", "import", "from", "<#", "param")):
            return s[:200]
    return ""


def classify(p: Path, text: str | None) -> dict:
    ext = p.suffix.lower()
    r = {"language": SCRIPT_EXT.get(ext, ext.lstrip(".") or "none"),
         "is_script": ext in SCRIPT_EXT}
    keys = ["purpose", "dependencies", "deletes", "moves_renames", "writes", "dry_run_support",
            "receipt_support", "network", "gui_cli", "stale_path_hits", "secret_ref",
            "secret_literal", "risk", "suggested_disposition"]
    r.update({k: "" for k in keys})
    if text is None:
        return r
    r["purpose"] = purpose(text, ext)
    if ext == ".py":
        mods = sorted({(a or b).split(".")[0] for a, b in PY_IMPORT.findall(text)})
        r["dependencies"] = ";".join(mods)
    r["deletes"] = "Y" if DELETE.search(text) else "N"
    r["moves_renames"] = "Y" if MOVE.search(text) else "N"
    r["writes"] = "Y" if WRITE.search(text) else "N"
    r["dry_run_support"] = "Y" if DRYRUN.search(text) else "N"
    r["receipt_support"] = "Y" if RECEIPT.search(text) else "N"
    r["network"] = "Y" if NETWORK.search(text) else "N"
    r["gui_cli"] = "+".join(x for x, rx in (("GUI", GUI), ("CLI", CLI)) if rx.search(text)) or "none"
    r["stale_path_hits"] = sum(len(rx.findall(text)) for _, rx in STALE[:5])
    r["secret_ref"] = "Y" if SECRET_REF.search(text) else "N"
    r["secret_literal"] = "Y" if SECRET_LITERAL.search(text) else "N"
    if not r["is_script"]:
        r["risk"] = "n/a"
        r["suggested_disposition"] = "KEEP AS REFERENCE"
    elif r["deletes"] == "Y":
        r["risk"] = "DESTRUCTIVE"
        r["suggested_disposition"] = "UNKNOWN — REVIEW REQUIRED"
    elif r["moves_renames"] == "Y":
        r["risk"] = "MUTATING (move/rename)"
        r["suggested_disposition"] = "REPAIR" if r["dry_run_support"] == "N" else "WRAP"
    elif r["writes"] == "Y":
        r["risk"] = "WRITES"
        r["suggested_disposition"] = "WRAP" if r["receipt_support"] == "Y" else "REPAIR"
    else:
        r["risk"] = "READ-ONLY (heuristic)"
        r["suggested_disposition"] = "CANONICAL CANDIDATE"
    if r["stale_path_hits"]:
        r["suggested_disposition"] = "REPAIR" if r["risk"] != "DESTRUCTIVE" else r["suggested_disposition"]
    return r


def scan(roots: list[tuple[str, Path]], out: Path) -> None:
    rows, stale_rows, errors = [], [], []
    for label, root in roots:
        print(f"Scanning {label}: {root}", flush=True)
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                p = Path(dirpath) / fn
                try:
                    st = p.stat()
                    digest = sha256(p)
                except OSError as e:
                    errors.append({"path": str(p), "error": str(e)})
                    continue
                text = read_text(p) if p.suffix.lower() in TEXT_EXT else None
                row = {"source_label": label, "absolute_path": str(p),
                       "relative_path": p.relative_to(root).as_posix(), "filename": fn,
                       "size_bytes": st.st_size, "sha256": digest,
                       "modified_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(timespec="seconds")}
                row.update(classify(p, text))
                rows.append(row)
                if text:
                    for i, line in enumerate(text.splitlines(), 1):
                        for kind, rx in STALE:
                            for m in rx.finditer(line):
                                stale_rows.append({"source_label": label, "relative_path": row["relative_path"],
                                                   "line": i, "kind": kind, "match": m.group(0),
                                                   "context": line.strip()[:160]})
                                break
    by_hash = defaultdict(list)
    for r in rows:
        by_hash[r["sha256"]].append(r)
    for r in rows:
        r["exact_duplicate_count"] = len(by_hash[r["sha256"]])
    stem_map = defaultdict(set)
    for r in rows:
        if r["is_script"]:
            stem_map[r["filename"].lower()].add(r["sha256"])
    similar = {k: v for k, v in stem_map.items() if len(v) > 1}

    out.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    write_csv(out / "ENGINE_INVENTORY.csv", fields, rows)
    dup_rows = [{"group": gi, "sha256": h, "copies": len(g), "size_bytes": g[0]["size_bytes"],
                 "source_label": r["source_label"], "relative_path": r["relative_path"]}
                for gi, (h, g) in enumerate(sorted(((h, g) for h, g in by_hash.items() if len(g) > 1),
                                                   key=lambda x: -len(x[1])), 1) for r in g]
    write_csv(out / "EXACT_DUPLICATE_GROUPS.csv",
              ["group", "sha256", "copies", "size_bytes", "source_label", "relative_path"], dup_rows)
    write_csv(out / "STALE_PATHS.csv", ["source_label", "relative_path", "line", "kind", "match", "context"], stale_rows)
    write_csv(out / "SCAN_ERRORS.csv", ["path", "error"], errors)
    write_destructive(out / "DESTRUCTIVE_SCRIPT_REPORT.md", rows)
    write_similar(out / "SIMILAR_IMPLEMENTATIONS.md", similar, rows)
    write_summary(out, roots, rows, dup_rows, stale_rows, errors)
    print(f"Done: {len(rows)} files, {len(dup_rows)} duplicate entries, {len(stale_rows)} stale-path hits -> {out}")


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def grep_lines(path: str, rx) -> list[str]:
    text = read_text(Path(path)) or ""
    return [f"{i}: {l.strip()[:140]}" for i, l in enumerate(text.splitlines(), 1) if rx.search(l)][:8]


def write_destructive(path, rows):
    lines = ["# Destructive Script Report", "",
             "Heuristic static scan. A hit means the code *can* delete, move, or rename; it does not prove it runs that path.",
             "No script was executed.", ""]
    for title, key, rx in (("Deletes files/folders", "deletes", DELETE),
                           ("Moves or renames", "moves_renames", MOVE)):
        hits = [r for r in rows if r["is_script"] and r[key] == "Y"]
        lines += [f"## {title} ({len(hits)})", ""]
        for r in sorted(hits, key=lambda r: r["relative_path"]):
            lines.append(f"### `{r['source_label']}/{r['relative_path']}`")
            lines.append(f"dry-run: {r['dry_run_support']} · receipts: {r['receipt_support']}")
            lines.append("```")
            lines += grep_lines(r["absolute_path"], re.compile(rx.pattern, re.I)) or ["(multi-line match)"]
            lines += ["```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_similar(path, similar, rows):
    lines = ["# Similar Implementations", "",
             "Script filenames that occur with **different** content. Compare behavior before consolidating.", ""]
    for name in sorted(similar):
        lines.append(f"## `{name}` — {len(similar[name])} variants")
        for r in sorted((r for r in rows if r["filename"].lower() == name), key=lambda r: r["sha256"]):
            lines.append(f"- `{r['sha256'][:12]}` {r['size_bytes']} B · {r['modified_utc']} · `{r['source_label']}/{r['relative_path']}`")
        lines.append("")
    if not similar:
        lines.append("_None found._")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_summary(out, roots, rows, dup_rows, stale_rows, errors):
    by_lang = defaultdict(int)
    for r in rows:
        if r["is_script"]:
            by_lang[r["language"]] += 1
    summary = {
        "tool": "tools/inventory/inventory.py", "version": VERSION,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "roots": {l: str(p) for l, p in roots},
        "files": len(rows), "bytes": sum(r["size_bytes"] for r in rows),
        "scripts_by_language": dict(sorted(by_lang.items())),
        "exact_duplicate_groups": len({d["group"] for d in dup_rows}),
        "stale_path_hits": len(stale_rows),
        "stale_path_files": len({(s["source_label"], s["relative_path"]) for s in stale_rows}),
        "scripts_that_delete": sum(1 for r in rows if r["is_script"] and r["deletes"] == "Y"),
        "scripts_that_move_rename": sum(1 for r in rows if r["is_script"] and r["moves_renames"] == "Y"),
        "possible_secret_literals": [r["relative_path"] for r in rows if r["secret_literal"] == "Y"],
        "scan_errors": len(errors),
    }
    (out / "SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", action="append", required=True, help="LABEL=PATH (repeatable)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    roots = []
    for spec in a.root:
        label, _, path = spec.partition("=")
        if not path:
            ap.error(f"--root must be LABEL=PATH, got {spec!r}")
        p = Path(path).resolve()
        if not p.is_dir():
            print(f"WARNING: skipping unreachable root {label}: {p}", file=sys.stderr)
            continue
        roots.append((label, p))
    if not roots:
        print("No reachable roots.", file=sys.stderr)
        return 2
    out = Path(a.out).resolve()
    for _, p in roots:
        if out == p or p in out.parents:
            print(f"Refusing: output {out} is inside scanned root {p}.", file=sys.stderr)
            return 2
    scan(roots, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
