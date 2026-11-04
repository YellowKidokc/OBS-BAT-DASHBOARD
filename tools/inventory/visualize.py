#!/usr/bin/env python3
"""Build a self-contained visual report from inventory.py output.

  python visualize.py REPORT_DIR      ->  REPORT_DIR/INVENTORY_REPORT.html

Reads ENGINE_INVENTORY.csv, EXACT_DUPLICATE_GROUPS.csv, STALE_PATHS.csv and
SUMMARY.json. Nothing is fetched from the network; the page works offline.
No file contents are embedded, only the metadata the inventory already holds.
"""
from __future__ import annotations
import csv, json, re, sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

STOP = set("""the a an and or of to in for on with from by is are be this that it as at
into py ps1 bat md txt json yaml yml csv cmd script scripts file files run using use
usr bin env python3 python utf coding import def class return none true false new
not all any one two get set main init self via based tool tools v1 v2 v3 de""".split())


def group_of(row) -> str:
    parts = row["relative_path"].split("/")
    if len(parts) == 1:
        return f'{row["source_label"]}: (root)'
    g = parts[0]
    if g in {"Reusable_Tools_From_Theophysics", "01_ENGINE", "legacy_source", "Codex-Powershell_GUI"} and len(parts) > 2:
        g = parts[0] + "/" + parts[1]
        if parts[1] in {"Reusable_Tools_From_Theophysics", "01_ENGINE"} and len(parts) > 3:
            g = parts[1] + "/" + parts[2]
    return f'{row["source_label"]}: {g}'


def tokens(text: str):
    for t in re.findall(r"[A-Za-z][A-Za-z]{2,}", re.sub(r"([a-z])([A-Z])", r"\1 \2", text)):
        t = t.lower()
        if t not in STOP and "redacted" not in t:
            yield t


def build(d: Path) -> dict:
    inv = list(csv.DictReader((d / "ENGINE_INVENTORY.csv").open(encoding="utf-8")))
    stale = list(csv.DictReader((d / "STALE_PATHS.csv").open(encoding="utf-8")))
    summary = json.loads((d / "SUMMARY.json").read_text(encoding="utf-8"))
    for r in inv:
        r["group"] = group_of(r)
        r["size_bytes"] = int(r["size_bytes"] or 0)

    groups = defaultdict(lambda: {"files": 0, "bytes": 0, "scripts": 0, "lang": Counter(), "risk": Counter(),
                                  "dup_files": 0, "stale_files": 0, "kw": Counter()})
    for r in inv:
        g = groups[r["group"]]
        g["files"] += 1
        g["bytes"] += r["size_bytes"]
        if r["is_script"] == "True":
            g["scripts"] += 1
            g["lang"][r["language"]] += 1
            g["risk"][r["risk"]] += 1
            g["kw"].update(tokens(r["filename"].rsplit(".", 1)[0] + " " + r["purpose"]))
        if int(r.get("exact_duplicate_count") or 1) > 1:
            g["dup_files"] += 1
        if int(r.get("stale_path_hits") or 0) > 0:
            g["stale_files"] += 1

    # duplicate families + overlap between groups
    by_hash = defaultdict(list)
    for r in inv:
        by_hash[r["sha256"]].append(r)
    fams, overlap = [], Counter()
    for h, rs in by_hash.items():
        if len(rs) < 2:
            continue
        gs = sorted({r["group"] for r in rs})
        for a, b in combinations(gs, 2):
            overlap[(a, b)] += 1
        fams.append({"name": rs[0]["filename"], "copies": len(rs), "bytes": rs[0]["size_bytes"],
                     "wasted": rs[0]["size_bytes"] * (len(rs) - 1), "groups": len(gs),
                     "paths": [f'{r["source_label"]}/{r["relative_path"]}' for r in rs][:12]})
    fams.sort(key=lambda f: (-f["wasted"], -f["copies"]))
    deg = Counter()
    for (a, b), n in overlap.items():
        deg[a] += n
        deg[b] += n
    top = [g for g, _ in deg.most_common(14)]
    matrix = [[overlap.get(tuple(sorted((a, b))), 0) if a != b else None for b in top] for a in top]

    # same filename, different content
    names = defaultdict(set)
    for r in inv:
        if r["is_script"] == "True" and r["filename"].lower() not in {"__init__.py"}:
            names[r["filename"].lower()].add(r["sha256"])
    variants = sorted(((n, len(s)) for n, s in names.items() if len(s) > 1), key=lambda x: -x[1])[:25]

    kinds = Counter(s["kind"] for s in stale)
    stale_files = Counter(f'{s["source_label"]}/{s["relative_path"]}' for s in stale if s["kind"] != "abs_windows_path")
    targets = Counter()
    for s in stale:
        if s["kind"] in ("drive_O", "drive_Z", "old_vault_version"):
            m = re.match(r"([A-Za-z]:[\\/]+[^\\/\s\"']+)", s["context"] or "")
            targets[(m.group(1) if m else s["match"]).replace("\\\\", "\\")] += 1

    kw = Counter()
    for g in groups.values():
        kw.update(g["kw"])

    scripts = [{"p": f'{r["source_label"]}/{r["relative_path"]}', "g": r["group"], "l": r["language"],
                "b": r["size_bytes"], "r": r["risk"], "d": r["suggested_disposition"], "dr": r["dry_run_support"],
                "rc": r["receipt_support"], "n": r["network"], "ui": r["gui_cli"],
                "s": int(r["stale_path_hits"] or 0), "x": int(r.get("exact_duplicate_count") or 1),
                "sec": r["secret_literal"], "m": r["modified_utc"][:10], "u": r["purpose"][:140]}
               for r in inv if r["is_script"] == "True"]

    return {
        "summary": summary,
        "groups": sorted(({"name": k, "files": v["files"], "bytes": v["bytes"], "scripts": v["scripts"],
                           "lang": dict(v["lang"]), "risk": dict(v["risk"]), "dup": v["dup_files"],
                           "stale": v["stale_files"], "kw": [w for w, _ in v["kw"].most_common(8)]}
                          for k, v in groups.items()), key=lambda g: -g["files"]),
        "families": fams[:60],
        "wasted_total": sum(f["wasted"] for f in fams),
        "overlap": {"labels": top, "matrix": matrix},
        "variants": variants,
        "stale_kinds": dict(kinds),
        "stale_top": stale_files.most_common(20),
        "stale_targets": targets.most_common(12),
        "keywords": kw.most_common(40),
        "dispositions": dict(Counter(s["d"] for s in scripts)),
        "scripts": scripts,
    }


def main(argv) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 2
    d = Path(argv[0]).resolve()
    data = build(d)
    tpl = (Path(__file__).with_name("report_template.html")).read_text(encoding="utf-8")
    blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    out = d / "INVENTORY_REPORT.html"
    out.write_text(tpl.replace("/*__DATA__*/null", blob), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
