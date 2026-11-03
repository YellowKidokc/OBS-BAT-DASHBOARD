#!/usr/bin/env python3
"""Safe, receipt-backed file conversions for the Codex Script Hub."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import shutil
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
RECEIPTS = APP_DIR / "receipts"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def unused(path: Path) -> Path:
    """Never overwrite: add an incrementing suffix when a target exists."""
    if not path.exists():
        return path
    for number in range(1, 10000):
        candidate = path.with_name(f"{path.stem}_{number}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not find an unused output name for {path}")


def write_receipt(action: str, source: Path, outputs: list[Path], warnings: list[str]) -> Path:
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc)
    row = {
        "timestamp": stamp.isoformat(),
        "action": action,
        "source": str(source.resolve()),
        "source_sha256": sha256(source) if source.is_file() else None,
        "outputs": [
            {"path": str(path.resolve()), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in outputs if path.is_file()
        ],
        "warnings": warnings,
        "status": "completed",
    }
    name = f"{stamp:%Y%m%dT%H%M%S}-{action}.json"
    target = unused(RECEIPTS / name)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, target)
    with (RECEIPTS / "file-actions.jsonl").open("a", encoding="utf-8") as log:
        log.write(json.dumps(row, ensure_ascii=False) + "\n")
    return target


def excel_to_csv(source: Path, output: Path) -> tuple[list[Path], list[str]]:
    from openpyxl import load_workbook

    output.mkdir(parents=True, exist_ok=True)
    workbook = load_workbook(source, read_only=True, data_only=True)
    results: list[Path] = []
    for sheet in workbook.worksheets:
        safe = "".join(c if c.isalnum() or c in "-_ " else "_" for c in sheet.title).strip() or "Sheet"
        target = unused(output / f"{source.stem}__{safe}.csv")
        with target.open("w", newline="", encoding="utf-8-sig") as stream:
            writer = csv.writer(stream)
            writer.writerows(sheet.iter_rows(values_only=True))
        results.append(target)
    workbook.close()
    return results, []


def csv_to_excel(source: Path, output: Path) -> tuple[list[Path], list[str]]:
    from openpyxl import Workbook

    output.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = source.stem[:31] or "Sheet1"
    with source.open("r", newline="", encoding="utf-8-sig", errors="replace") as stream:
        sample = stream.read(8192)
        stream.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
        except csv.Error:
            dialect = csv.excel
        for row in csv.reader(stream, dialect):
            sheet.append(row)
    target = unused(output / f"{source.stem}.xlsx")
    workbook.save(target)
    return [target], []


def combine_markdown(source: Path, output: Path) -> tuple[list[Path], list[str]]:
    output.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in source.rglob("*.md") if path.is_file())
    if not files:
        raise ValueError("No Markdown files were found in the selected folder")
    target = unused(output / f"{source.name or 'markdown'}__combined.md")
    sections = []
    for path in files:
        relative = path.relative_to(source).as_posix()
        sections.append(f"<!-- SOURCE: {relative} | SHA256: {sha256(path)} -->\n\n{path.read_text(encoding='utf-8-sig', errors='replace').rstrip()}")
    target.write_text("\n\n---\n\n".join(sections) + "\n", encoding="utf-8")
    return [target], []


def inventory(source: Path, output: Path) -> tuple[list[Path], list[str]]:
    output.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in source.rglob("*") if path.is_file())
    target = unused(output / f"{source.name or 'folder'}__inventory.csv")
    with target.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(["relative_path", "extension", "bytes", "modified_utc", "sha256"])
        for path in files:
            writer.writerow([
                path.relative_to(source).as_posix(), path.suffix.lower(), path.stat().st_size,
                dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat(), sha256(path),
            ])
    return [target], []


def safe_copy(source: Path, output: Path) -> tuple[list[Path], list[str]]:
    output.mkdir(parents=True, exist_ok=True)
    target = unused(output / source.name)
    shutil.copy2(source, target)
    if sha256(source) != sha256(target):
        target.unlink(missing_ok=True)
        raise IOError("The copied file failed SHA-256 verification")
    return [target], []


ACTIONS = {
    "excel-to-csv": (excel_to_csv, "file"),
    "csv-to-excel": (csv_to_excel, "file"),
    "combine-markdown": (combine_markdown, "folder"),
    "folder-inventory": (inventory, "folder"),
    "verified-copy": (safe_copy, "file"),
}


def execute(action: str, source: Path, output: Path) -> dict:
    handler, kind = ACTIONS[action]
    if kind == "file" and not source.is_file():
        raise ValueError("This action requires an input file")
    if kind == "folder" and not source.is_dir():
        raise ValueError("This action requires an input folder")
    outputs, warnings = handler(source.resolve(), output.resolve())
    receipt = write_receipt(action, source, outputs, warnings)
    return {"action": action, "outputs": [str(p) for p in outputs], "receipt": str(receipt), "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=sorted(ACTIONS))
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(execute(args.action, args.source, args.output), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
