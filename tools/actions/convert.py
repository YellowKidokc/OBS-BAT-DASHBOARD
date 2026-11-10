#!/usr/bin/env python3
"""File conversions. Never modifies or overwrites a source; outputs go to a new folder.

  convert.py excel2csv  PATH [--out DIR] [--apply]   workbook(s) -> one CSV per sheet + _book.json
  convert.py csv2excel  PATH [--out DIR] [--apply]   _book folder -> same workbook; folder of CSVs -> one workbook
  convert.py tomd       PATH [--out DIR] [--apply]   anything MarkItDown reads -> .md
  convert.py frommd     PATH --to FMT [--out DIR] [--apply]   .md -> docx/html/pdf/odt/rtf/epub/pptx/txt (pandoc)

PATH may be a file or a folder (folders are processed recursively).
Default output: <PATH's folder>/_converted/<action>_<timestamp>/ . Dry run unless --apply.
Lineage from legacy file_actions.py: unused() naming, sha256 receipts.
"""
from __future__ import annotations
import argparse, csv, datetime as dt, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

VERSION = "0.1.0"
EXCEL = {".xlsx", ".xlsm"}
LEGACY_XLS = {".xls"}
TO_MD = {".docx", ".pptx", ".xlsx", ".xls", ".pdf", ".html", ".htm", ".epub", ".csv", ".json", ".xml",
         ".txt", ".rtf", ".odt", ".ipynb", ".msg", ".zip", ".jpg", ".jpeg", ".png"}
FROM_MD = {"docx", "html", "pdf", "odt", "rtf", "epub", "pptx", "txt"}
SKIP_DIRS = {".git", ".obsidian", "_converted", "_flatten_manifests"}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def unused(path: Path) -> Path:
    if not path.exists():
        return path
    for n in range(1, 10000):
        c = path.with_name(f"{path.stem}_{n}{path.suffix}")
        if not c.exists():
            return c
    raise RuntimeError(f"No free name for {path}")


def safe(name: str, n: int = 80) -> str:
    return (re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip(" .") or "Sheet")[:n]


def files_in(path: Path, exts: set[str]) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in exts else []
    out = []
    for d, dn, fn in os.walk(path):
        dn[:] = sorted(x for x in dn if x not in SKIP_DIRS)
        out += [Path(d) / f for f in sorted(fn) if Path(f).suffix.lower() in exts and not f.startswith("~$")]
    return out


# ---------- Excel -> CSV ----------
def excel2csv(src: Path, out: Path, warn: list[str]) -> list[Path]:
    from openpyxl import load_workbook
    book_dir = unused(out / safe(src.stem))
    book_dir.mkdir(parents=True)
    wb = load_workbook(src, read_only=True, data_only=True)
    sheets, results = [], []
    formulas = _has_formulas(src)
    for i, ws in enumerate(wb.worksheets, 1):
        target = book_dir / f"{i:02d}_{safe(ws.title, 60)}.csv"
        with target.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            for row in ws.iter_rows(values_only=True):
                w.writerow(["" if v is None else v.isoformat() if hasattr(v, "isoformat") else v for v in row])
        sheets.append({"order": i, "title": ws.title, "csv": target.name, "state": getattr(ws, "sheet_state", "visible")})
        results.append(target)
    wb.close()
    meta = {"tool": "convert.py", "version": VERSION, "source": src.name, "source_sha256": sha256(src),
            "sheets": sheets, "formulas_present": formulas,
            "note": "CSV holds values only. Formulas, formatting, charts and merged cells are not carried."}
    (book_dir / "_book.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    if formulas:
        warn.append(f"{src.name}: has formulas - CSV keeps their last calculated VALUES only.")
    return results + [book_dir / "_book.json"]


def _has_formulas(src: Path) -> bool:
    try:
        from openpyxl import load_workbook
        wb = load_workbook(src, read_only=True, data_only=False)
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                if any(isinstance(v, str) and v.startswith("=") for v in row):
                    wb.close()
                    return True
        wb.close()
    except Exception:
        pass
    return False


# ---------- CSV -> Excel ----------
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?)?$")
NUM = re.compile(r"^-?\d+(\.\d+)?([eE][-+]?\d+)?$")


def typed(v: str):
    if v == "":
        return None
    if NUM.match(v) and not (len(v) > 1 and v.startswith("0") and not v.startswith("0.")) and len(v) < 16:
        return float(v) if any(c in v for c in ".eE") else int(v)
    if ISO.match(v):
        try:
            return dt.datetime.fromisoformat(v)
        except ValueError:
            pass
    return v  # leading-zero codes, long IDs, dates stay text exactly as written


def read_csv(p: Path):
    with p.open("r", newline="", encoding="utf-8-sig", errors="replace") as f:
        sample = f.read(8192)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
        except csv.Error:
            dialect = csv.excel
        yield from csv.reader(f, dialect)


def csv2excel_group(csvs: list[tuple[str, Path]], target: Path, states: list[str] | None = None) -> Path:
    from openpyxl import Workbook
    wb = Workbook()
    wb.remove(wb.active)
    used = set()
    for title, p in csvs:
        t = safe(title, 31).replace("[", "(").replace("]", ")")
        base, n = t, 2
        while t.lower() in used:
            t = f"{base[:28]}~{n}"
            n += 1
        used.add(t.lower())
        ws = wb.create_sheet(t)
        for row in read_csv(p):
            ws.append([typed(v) for v in row])
        if states and states[len(used) - 1] in ("hidden", "veryHidden"):
            ws.sheet_state = states[len(used) - 1]
    target = unused(target)
    wb.save(target)
    return target


def csv2excel(src: Path, out: Path, warn: list[str]) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    if src.is_file():
        return [csv2excel_group([(src.stem, src)], out / f"{safe(src.stem)}.xlsx")]
    results = []
    books = [Path(d) for d, _, fn in os.walk(src) if "_book.json" in fn]
    for b in books:  # round trip: rebuild the original workbook
        meta = json.loads((b / "_book.json").read_text(encoding="utf-8"))
        present = [s for s in sorted(meta["sheets"], key=lambda s: s["order"]) if (b / s["csv"]).exists()]
        csvs = [(s["title"], b / s["csv"]) for s in present]
        missing = len(meta["sheets"]) - len(csvs)
        if missing:
            warn.append(f"{b.name}: {missing} sheet CSV(s) missing; rebuilt without them.")
        stem = Path(meta.get("source", b.name)).stem
        results.append(csv2excel_group(csvs, out / f"{safe(stem)}.xlsx", [s.get("state", "visible") for s in present]))
    loose = [p for p in files_in(src, {".csv", ".tsv"}) if not any(b in p.parents for b in books)]
    by_folder: dict[Path, list[Path]] = {}
    for p in loose:
        by_folder.setdefault(p.parent, []).append(p)
    for folder, ps in by_folder.items():
        name = safe(folder.name if folder != src else src.name)
        results.append(csv2excel_group([(p.stem, p) for p in ps], out / f"{name}.xlsx"))
    return results


# ---------- anything -> Markdown ----------
def tomd(src: Path, out: Path, root: Path, warn: list[str]) -> list[Path]:
    from markitdown import MarkItDown
    md = MarkItDown()
    rel = src.relative_to(root).parent if root.is_dir() else Path()
    target = unused(out / rel / f"{src.stem}.md")
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        text = md.convert(str(src)).text_content
    except Exception as e:
        hint = ' - run: pip install "markitdown[all]"' if "MissingDependency" in str(e) else ""
        warn.append(f"{src.name}: could not convert ({type(e).__name__}: {str(e)[:120]}){hint}")
        return []
    if not text.strip():
        warn.append(f"{src.name}: produced empty Markdown (scanned PDF or image-only file? needs OCR).")
    header = f"---\nconverted_from: \"{src.name}\"\nsource_sha256: {sha256(src)}\nconverter: markitdown\nconverted: {dt.date.today()}\n---\n\n"
    target.write_text(header + text, encoding="utf-8")
    return [target]


# ---------- Markdown -> other ----------
def pandoc() -> str | None:
    return shutil.which("pandoc")


def pdf_engine() -> str | None:
    for e in ("xelatex", "pdflatex", "lualatex", "wkhtmltopdf", "weasyprint", "typst"):
        if shutil.which(e):
            return e
    return None


def frommd(src: Path, out: Path, root: Path, fmt: str, warn: list[str]) -> list[Path]:
    rel = src.relative_to(root).parent if root.is_dir() else Path()
    target = unused(out / rel / f"{src.stem}.{'txt' if fmt == 'txt' else fmt}")
    target.parent.mkdir(parents=True, exist_ok=True)
    args = [pandoc(), str(src), "-f", "markdown+wikilinks_title_after_pipe+tex_math_dollars", "-o", str(target),
            "--resource-path", str(src.parent)]
    if fmt in ("html", "epub"):
        args += ["--metadata", f"title={src.stem}"]
    if fmt == "html":
        args += ["--standalone", "--embed-resources", "--mathml"]
    elif fmt == "txt":
        args += ["-t", "plain"]
    elif fmt == "pdf":
        args += ["--pdf-engine", pdf_engine()]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        warn.append(f"{src.name}: pandoc failed: {r.stderr.strip()[:200]}")
        return []
    if r.stderr.strip():
        warn.append(f"{src.name}: {r.stderr.strip()[:160]}")
    return [target]


# ---------- driver ----------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Safe file conversions (dry run by default).")
    ap.add_argument("action", choices=["excel2csv", "csv2excel", "tomd", "frommd"])
    ap.add_argument("path")
    ap.add_argument("--to", choices=sorted(FROM_MD))
    ap.add_argument("--out")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)
    src = Path(a.path).resolve()
    if not src.exists():
        print(f"Not found: {src}", file=sys.stderr)
        return 2
    base = src.parent if src.is_file() else src
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = Path(a.out).resolve() if a.out else base / "_converted" / f"{a.action}{'_' + a.to if a.to else ''}_{stamp}"
    warn: list[str] = []

    if a.action == "excel2csv":
        items = files_in(src, EXCEL)
        legacy = files_in(src, LEGACY_XLS)
        if legacy:
            warn.append(f"{len(legacy)} old .xls file(s) skipped - open and Save As .xlsx first (or use 'tomd').")
    elif a.action == "csv2excel":
        items = [src]
    elif a.action == "tomd":
        try:
            import markitdown  # noqa: F401
        except ImportError:
            print('MarkItDown is not installed. Run:  pip install "markitdown[all]"', file=sys.stderr)
            return 2
        items = files_in(src, TO_MD - {".md"})
    else:
        if not a.to:
            ap.error("frommd needs --to FORMAT")
        if not pandoc():
            print("pandoc is not installed. Run:  winget install --id JohnMacFarlane.Pandoc", file=sys.stderr)
            return 2
        if a.to == "pdf" and not pdf_engine():
            print("PDF needs a PDF engine (none found). Easiest: winget install --id Typst.Typst  "
                  "- or convert to html/docx and print to PDF.", file=sys.stderr)
            return 2
        items = files_in(src, {".md", ".markdown"})

    label = {"excel2csv": "workbooks", "csv2excel": "folder/file", "tomd": "files", "frommd": "Markdown files"}[a.action]
    print(f"{a.action}: {len(items)} {label} from {src}\nOutput folder: {out}")
    for p in items[:30]:
        print(f"  {p.relative_to(base) if p != base else p.name}")
    if len(items) > 30:
        print(f"  ... and {len(items) - 30} more")
    for w in warn:
        print(f"  WARNING: {w}")
    if not items:
        print("Nothing to convert.")
        return 0
    if not a.apply:
        print("\nDRY RUN - nothing written. Re-run with --apply.")
        return 0

    out.mkdir(parents=True, exist_ok=True)
    outputs, shown = [], len(warn)
    for p in items:
        if a.action == "excel2csv":
            try:
                outputs += excel2csv(p, out, warn)
            except Exception as e:
                warn.append(f"{p.name}: {type(e).__name__}: {e}")
        elif a.action == "csv2excel":
            outputs += csv2excel(p, out, warn)
        elif a.action == "tomd":
            outputs += tomd(p, out, src, warn)
        else:
            outputs += frommd(p, out, src, a.to, warn)
    receipt = {"tool": "convert.py", "version": VERSION, "action": a.action, "format": a.to,
               "source": str(src), "timestamp": stamp,
               "inputs": [{"path": str(p), "sha256": sha256(p)} for p in items if p.is_file()],
               "outputs": [{"path": str(o.relative_to(out)), "sha256": sha256(o), "bytes": o.stat().st_size} for o in outputs],
               "warnings": warn, "note": "Sources were only read. Delete this output folder to undo."}
    (out / "_receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {len(outputs)} files to {out}")
    for w in warn[shown:]:
        print(f"  WARNING: {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
