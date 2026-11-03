"""
Rebuild CDCM master Excel with full A1-K4 detail from all CDCM JSON files,
then delete all relic CSV/TXT/XLSX/JSON per-paper files.
Keeps: CDCM_MASTER_ALL_PAPERS.xlsx, CDCM_MASTER_ALL_PAPERS.csv, CKG_*.json files.
"""
import json, csv, os, glob, pathlib, sys

VAULT_ROOT   = pathlib.Path("O:/_Theophysics_v3")
OUTPUT_DIR   = pathlib.Path("O:/_Theophysics_v3/00_SYSTEM/00_ENGINE/Open AI Calls/Open-AI-PAPER-REVIEW/output")
SECTIONS     = list("ABCDEFGHIJK")
SUB_CRITERIA = [f"{s}{i}" for s in SECTIONS for i in range(1, 5)]

# Collection label map (folder path fragment → display name)
COLLECTION_MAP = {
    "[5.5] THREE TRUTHS":       "[5.5] THREE TRUTHS",
    "[7.5] LAYER_1_LOGIC":      "[7.5] LAYER_1_LOGIC",
    "[7.5] Psychology_Crisis":  "[7.5] Psychology_Crisis",
    "Submissions":              "[7.0] Submissions",
}

THREE_TRUTHS_PAPERS = {
    "01_DE_REVOLUTIONIBUS_VERITATIS_THE_ARCHITECTURE",
    "02_DE_REVOLUTIONIBUS_VERITATIS_THE_LOCK",
    "03_DE_REVOLUTIONIBUS_VERITATIS_THE_COST_OF_DENIAL",
    "04_DE_REVOLUTIONIBUS_VERITATIS_THE_KEY",
    "godel", "truth-one-self-reference-limits",
    "truth-two-measurement-collapse", "truth-three-necessary-ground",
    "landauer", "entropy", "finetuning", "propcosmos",
    "biology", "hubble", "inversion", "irony", "prayer", "triad",
}

def collection_label(json_path: pathlib.Path, paper_base: str = "") -> str:
    s = str(json_path)
    for fragment, label in COLLECTION_MAP.items():
        if fragment in s:
            return label
    # Files from the main output/ folder — map to known collections
    if paper_base in THREE_TRUTHS_PAPERS:
        return "[5.5] THREE TRUTHS"
    return "Other"

def grade(score):
    if score >= 90: return "A"
    if score >= 85: return "A-"
    if score >= 80: return "B"
    if score >= 75: return "C+"
    if score >= 65: return "C"
    if score >= 55: return "D"
    return "F"

# ── 1. Collect all *_CDCM_*.json from OpenAI_DATA folders ──────────────────
cdcm_jsons = list(VAULT_ROOT.rglob("*_CDCM_*.json"))
# Also collect scores_*.json from the main output folder (old individual reviews)
cdcm_jsons += list(OUTPUT_DIR.glob("scores_*.json"))

print(f"Found {len(cdcm_jsons)} CDCM JSON files")

# For papers with multiple runs, keep latest timestamp per paper name
latest = {}  # paper_base → (timestamp, path, collection)
for p in cdcm_jsons:
    name = p.stem
    # Normalize: strip _CDCM_timestamp or scores_ prefix+timestamp
    if name.startswith("scores_"):
        # e.g. scores_04_THE_KEY_20260226_034406
        parts = name[7:].rsplit("_", 2)
        base = parts[0] if len(parts) >= 1 else name
        ts   = "_".join(parts[1:]) if len(parts) >= 2 else "0"
    else:
        # e.g. 04_The_Moral_Paradox_CDCM_20260226_100749
        idx = name.find("_CDCM_")
        base = name[:idx] if idx != -1 else name
        ts   = name[idx+6:] if idx != -1 else "0"

    col = collection_label(p, base)
    # Dedup by paper name only — keep latest timestamp across all collections
    key = base
    if key not in latest or ts > latest[key][0]:
        latest[key] = (ts, p, col)

print(f"Unique papers after dedup: {len(latest)}")

# ── 2. Build rows ───────────────────────────────────────────────────────────
rows = []
for (col, base), (ts, p, col) in sorted(latest.items()):
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        print(f"  SKIP (bad json): {p.name} — {e}")
        continue

    total = float(d.get("total_score", d.get("total", 0)) or 0)
    if total == 0:
        continue  # skip stub/empty papers

    sub = d.get("sub_criteria", {})
    sec = d.get("section_averages", d.get("sections", {}))

    row = {
        "Collection": col,
        "Paper": base,
        "CDCM_Score": total,
        "Grade": grade(total),
    }
    # Section averages A-K
    for s in SECTIONS:
        row[f"Sec_{s}"] = round(float(sec.get(s, 0) or 0), 1)
    # Sub-criteria A1-K4
    for code in SUB_CRITERIA:
        val = sub.get(code, {})
        if isinstance(val, dict):
            row[code] = val.get("score", "")
        else:
            row[code] = val if val != "" else ""

    rows.append(row)

rows.sort(key=lambda x: float(x["CDCM_Score"] or 0), reverse=True)
print(f"Rows to write: {len(rows)}")

# ── 3. Write master CSV ─────────────────────────────────────────────────────
sec_cols  = [f"Sec_{s}" for s in SECTIONS]
fields    = ["Collection", "Paper", "CDCM_Score", "Grade"] + sec_cols + SUB_CRITERIA
csv_path  = OUTPUT_DIR / "CDCM_MASTER_ALL_PAPERS.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
print(f"CSV written: {csv_path}")

# ── 4. Write master XLSX ────────────────────────────────────────────────────
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter

    def score_fill(s):
        s = float(s or 0)
        if s >= 80: return "27AE60"
        if s >= 70: return "E67E22"
        if s >= 55: return "E74C3C"
        return "95A5A6"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "CDCM Scores"

    hdr_fill = PatternFill("solid", fgColor="1A252F")
    hdr_font = Font(color="FFFFFF", bold=True, size=9)
    for ci, h in enumerate(fields, 1):
        c = ws.cell(row=1, column=ci, value=h)
        c.fill = hdr_fill
        c.font = hdr_font
        c.alignment = Alignment(horizontal="center")

    for ri, row in enumerate(rows, 2):
        score_val = float(row.get("CDCM_Score") or 0)
        for ci, field in enumerate(fields, 1):
            val = row.get(field, "")
            if isinstance(val, str) and val == "":
                val = None
            elif field in ("CDCM_Score",) + tuple(sec_cols) + tuple(SUB_CRITERIA):
                try:
                    val = float(val) if val not in (None, "") else None
                except (TypeError, ValueError):
                    val = None
            c = ws.cell(row=ri, column=ci, value=val)
            if field == "CDCM_Score" and score_val > 0:
                c.fill = PatternFill("solid", fgColor=score_fill(score_val))
                c.font = Font(bold=True, color="FFFFFF", size=9)
            elif field in sec_cols and val:
                v = float(val)
                if v >= 7:   c.fill = PatternFill("solid", fgColor="D5F5E3")
                elif v >= 5: c.fill = PatternFill("solid", fgColor="FDEBD0")
                else:        c.fill = PatternFill("solid", fgColor="FADBD8")

    # Column widths
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 50
    ws.column_dimensions["C"].width = 12
    ws.column_dimensions["D"].width = 7
    for i in range(5, len(fields) + 1):
        ws.column_dimensions[get_column_letter(i)].width = 7
    ws.freeze_panes = "E2"

    xlsx_path = OUTPUT_DIR / "CDCM_MASTER_ALL_PAPERS.xlsx"
    wb.save(xlsx_path)
    print(f"XLSX written: {xlsx_path}")
except ImportError:
    print("openpyxl not installed — CSV only")

# ── 5. Delete relic files ───────────────────────────────────────────────────
print("\nCleaning up relic files...")
deleted = 0

# Patterns to delete in OpenAI_DATA folders
# KEEP: *_CDCM_*.json (source data), *_CKG_*.json (different system)
# DELETE: derivative files only (csv, txt, xlsx per-paper)
relic_patterns = [
    "*_CDCM_*.csv",
    "*_CDCM_*.txt",
    "*_CDCM_*.xlsx",
    "CDCM_MASTER_SUMMARY.xlsx",
]
for pattern in relic_patterns:
    for f in VAULT_ROOT.rglob(pattern):
        try:
            f.unlink()
            deleted += 1
        except Exception as e:
            print(f"  Could not delete {f.name}: {e}")

# Clean old output folder files (keep master files)
keep = {"CDCM_MASTER_ALL_PAPERS.csv", "CDCM_MASTER_ALL_PAPERS.xlsx"}
for f in OUTPUT_DIR.iterdir():
    if f.name in keep:
        continue
    if f.name.startswith(("scores_", "report_", "CDCM_truth")):
        try:
            f.unlink()
            deleted += 1
        except Exception as e:
            print(f"  Could not delete {f.name}: {e}")

print(f"Deleted {deleted} relic files")
print("\nDone. Master Excel is the single source of truth.")
print(f"  {xlsx_path}")

# Print scoreboard
print(f"\n{'Score':>7}  {'Grade':>5}  {'Collection':<28}  Paper")
print("-" * 85)
for r in rows:
    print(f"  {r['CDCM_Score']:>5.1f}  {r['Grade']:>5}  {r['Collection']:<28}  {r['Paper']}")
