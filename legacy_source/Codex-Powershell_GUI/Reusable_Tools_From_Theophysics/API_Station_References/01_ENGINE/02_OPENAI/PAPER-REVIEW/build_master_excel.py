"""
Build a master CDCM Excel file from all batch summary JSONs across the vault.
"""
import json
import csv
import os
from pathlib import Path

VAULT_ROOT = Path("O:/_Theophysics_v3")
OUTPUT_DIR = Path("O:/_Theophysics_v3/00_SYSTEM/00_ENGINE/Open AI Calls/Open-AI-PAPER-REVIEW/output")

SECTIONS = list("ABCDEFGHIJK")

# Folder collection names for each batch summary
BATCH_SOURCES = [
    {
        "folder": "[5.5] THREE TRUTHS",
        "json": VAULT_ROOT / "04_THEOPYHISCS/THREE TRUTHS/[5.5] MAIN_PAPERS/OpenAI_DATA/CDCM_BATCH_SUMMARY_20260226_024014.json",
    },
    {
        "folder": "[7.5] Psychology_Crisis",
        "json": VAULT_ROOT / "04_THEOPYHISCS/[7.5] Psychology_Crisis/[7.5] MAIN_PAPERS/OpenAI_DATA/CDCM_BATCH_SUMMARY_20260226_100806.json",
    },
    {
        "folder": "[7.5] LAYER_1_LOGIC",
        "json": VAULT_ROOT / "04_THEOPYHISCS/[7.5] LAYER_1_LOGIC/[7.5] MAIN_PAPERS/OpenAI_DATA/CDCM_BATCH_SUMMARY_20260226_100820.json",
    },
    {
        "folder": "[7.0] Submissions",
        "json": VAULT_ROOT / "05_PUBLICATIONS/Submissions/[7.0] MAIN_PAPERS/OpenAI_DATA/CDCM_BATCH_SUMMARY_20260226_101114.json",
    },
]

# Use most-recent scores for key papers (overrides from individual runs)
OVERRIDES = {
    "[86.1] 01_DE_REVOLUTIONIBUS_VERITATIS_THE_ARCHITECTURE.md": 86.1,
    "[73.0] 02_DE_REVOLUTIONIBUS_VERITATIS_THE_LOCK.md": 73.0,
    "[70.9] 03_DE_REVOLUTIONIBUS_VERITATIS_THE_COST_OF_DENIAL.md": 70.9,
    "[63.7] 04_DE_REVOLUTIONIBUS_VERITATIS_THE_KEY.md": 63.7,
    "[76.5] godel.md": 76.5,
    "[76.3] truth-one-self-reference-limits.md": 76.3,
    "[61.0] truth-two-measurement-collapse.md": 61.0,
}

# Grade helper
def grade(score):
    if score >= 90: return "A"
    if score >= 85: return "A-"
    if score >= 80: return "B"
    if score >= 75: return "C+"
    if score >= 65: return "C"
    if score >= 55: return "D"
    return "F"

rows = []

for source in BATCH_SOURCES:
    json_path = source["json"]
    folder_name = source["folder"]
    if not json_path.exists():
        print(f"  WARNING: not found: {json_path}")
        continue
    with open(json_path, "r", encoding="utf-8") as f:
        papers = json.load(f)
    for p in papers:
        paper_name = p["paper"]
        total = p.get("total", 0)
        secs = p.get("sections", {})
        # Apply override if available (use current renamed filename score)
        for override_name, override_score in OVERRIDES.items():
            # Match by base name (strip [score] prefix)
            base = paper_name.replace(".md", "")
            override_base = override_name.split("] ", 1)[-1].replace(".md", "") if "] " in override_name else override_name.replace(".md", "")
            if base == override_base:
                total = override_score
                break
        row = {
            "Collection": folder_name,
            "Paper": paper_name,
            "CDCM_Score": total,
            "Grade": grade(total),
        }
        for s in SECTIONS:
            row[s] = secs.get(s, "")
        rows.append(row)

# Sort by score descending
rows.sort(key=lambda x: float(x["CDCM_Score"] or 0), reverse=True)

# Write master CSV
csv_path = OUTPUT_DIR / "CDCM_MASTER_ALL_PAPERS.csv"
fieldnames = ["Collection", "Paper", "CDCM_Score", "Grade"] + SECTIONS
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Master CSV written: {csv_path}")
print(f"Total papers: {len(rows)}")
print()
print(f"{'Score':>7}  {'Grade':>5}  {'Collection':<30}  Paper")
print("-" * 90)
for r in rows:
    if float(r['CDCM_Score'] or 0) > 0:
        print(f"  {r['CDCM_Score']:>5.1f}  {r['Grade']:>5}  {r['Collection']:<30}  {r['Paper']}")

# Try to write XLSX if openpyxl available
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "CDCM Scores"

    # Color scale for scores
    def score_color(score):
        s = float(score or 0)
        if s >= 80: return "2ECC71"   # green
        if s >= 70: return "F39C12"   # orange
        if s >= 55: return "E67E22"   # dark orange
        return "E74C3C"               # red

    # Header row
    headers = fieldnames
    header_fill = PatternFill("solid", fgColor="2C3E50")
    header_font = Font(color="FFFFFF", bold=True)
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    # Data rows
    for row_idx, r in enumerate(rows, 2):
        score_val = float(r["CDCM_Score"] or 0)
        fill_color = score_color(score_val)
        row_fill = PatternFill("solid", fgColor=fill_color + "44")  # light tint
        for col, field in enumerate(fieldnames, 1):
            val = r[field]
            if val == "":
                val = None
            elif field == "CDCM_Score":
                val = float(val) if val else 0
            elif field in SECTIONS:
                val = float(val) if val else None
            cell = ws.cell(row=row_idx, column=col, value=val)
            if field == "CDCM_Score" and score_val > 0:
                cell.fill = PatternFill("solid", fgColor=fill_color)
                cell.font = Font(bold=True, color="FFFFFF")

    # Column widths
    ws.column_dimensions["A"].width = 28  # Collection
    ws.column_dimensions["B"].width = 52  # Paper
    ws.column_dimensions["C"].width = 12  # Score
    ws.column_dimensions["D"].width = 8   # Grade
    for i, s in enumerate(SECTIONS, 5):
        ws.column_dimensions[get_column_letter(i)].width = 6

    # Freeze top row
    ws.freeze_panes = "A2"

    xlsx_path = OUTPUT_DIR / "CDCM_MASTER_ALL_PAPERS.xlsx"
    wb.save(xlsx_path)
    print(f"\nMaster XLSX written: {xlsx_path}")

except ImportError:
    print("\nopenpyxl not installed — CSV only. Install with: pip install openpyxl")
