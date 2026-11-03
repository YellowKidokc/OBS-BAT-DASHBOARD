#!/usr/bin/env python3
"""
UNIFIED EXCEL WRITER — All metrics, one workbook, one sheet per paper set
=========================================================================
Collects output from ALL pipeline stages (A through G + backend + truth engine)
and writes one Excel file. One row per paper. Every metric is a column.

Usage:
    python excel_writer.py output_folder/              # Scan folder for all JSON outputs
    python excel_writer.py output_folder/ -o results.xlsx
    python excel_writer.py output_folder/ --paper FP-007  # Single paper

Requires: pip install openpyxl
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    print("[ERROR] openpyxl not installed. Run: pip install openpyxl")
    sys.exit(1)


# ─── Column definitions ──────────────────────────────────────────────────────
# Each tuple: (column_header, json_path, source_stage, format)
# json_path uses dot notation: "scores.Q0_POSTURE" means json["scores"]["Q0_POSTURE"]

COLUMNS = [
    # ── Identity ──
    ("paper_id",              None,                              "ID",  "text"),
    ("paper_title",           None,                              "ID",  "text"),
    ("paper_type",            "paper_type",                      "A",   "text"),
    ("run_date",              None,                              "ID",  "text"),

    # ── Stage A: Preflight (local, free) ──
    ("word_count",            "word_count",                      "A",   "int"),
    ("char_count",            "char_count",                      "A",   "int"),
    ("paragraph_count",       "paragraph_count",                 "A",   "int"),
    ("sentence_count",        "sentence_count",                  "A",   "int"),
    ("avg_sentence_length",   "avg_sentence_length",             "A",   "float"),
    ("heading_count",         "heading_count",                   "A",   "int"),
    ("equation_count",        "equation_count",                  "A",   "int"),
    ("citation_count",        "citation_count",                  "A",   "int"),
    ("has_abstract",          "has_abstract",                    "A",   "bool"),
    ("has_frontmatter",       "has_frontmatter",                 "A",   "bool"),
    ("has_lagrangian",        "has_lagrangian",                  "A",   "bool"),

    # ── Stage B: Fruits + Chi (local, SBERT) ──
    ("axiom_coverage",        "axiom_coverage",                  "B",   "pct"),
    ("law_count",             "law_count",                       "B",   "int"),
    ("master_eq_vars_active", "master_eq_vars_active",           "B",   "int"),
    ("symmetry_pairs_active", "symmetry_pairs_active",           "B",   "int"),
    ("chi_field_present",     "chi_field_present",               "B",   "bool"),
    ("fruits_score",          "fruits_score",                    "B",   "pct"),
    ("sbert_similarity",      "sbert_similarity",                "B",   "pct"),
    ("orphan_claim_count",    "orphan_claim_count",              "B",   "int"),

    # ── Stage C: Truth Coherence (local, DeBERTa) ──
    ("claim_count",           "claim_count",                     "C",   "int"),
    ("claim_density",         "claim_density",                   "C",   "float"),
    ("internal_consistency",  "internal_consistency",            "C",   "pct"),
    ("coherence_score",       "coherence_score",                 "C",   "pct"),
    ("contradiction_count",   "contradiction_count",             "C",   "int"),
    ("strongest_claim",       "strongest_claim",                 "C",   "text"),
    ("weakest_claim",         "weakest_claim",                   "C",   "text"),

    # ── Stage D: 7Q+ Judge (OpenAI ~$0.04) ──
    ("Q0_posture",            "scores.Q0_POSTURE",               "D",   "pct"),
    ("Q1_identity",           "scores.Q1_IDENTITY",              "D",   "pct"),
    ("Q2_domain",             "scores.Q2_DOMAIN",                "D",   "pct"),
    ("Q3_assertion",          "scores.Q3_ASSERTION",             "D",   "pct"),
    ("Q4_evidence",           "scores.Q4_EVIDENCE",              "D",   "pct"),
    ("Q5_dependencies",       "scores.Q5_DEPENDENCIES",          "D",   "pct"),
    ("Q6_consequences",       "scores.Q6_CONSEQUENCES",          "D",   "pct"),
    ("Q7_falsification",      "scores.Q7_FALSIFICATION",         "D",   "pct"),
    ("T_score",               "T_score",                         "D",   "pct"),
    ("confidence",            "confidence",                      "D",   "text"),
    ("claim_type",            "type",                            "D",   "text"),
    ("PS",                    "evidence.PS",                     "D",   "pct"),
    ("ED",                    "evidence.ED",                     "D",   "pct"),
    ("EC",                    "evidence.EC",                     "D",   "pct"),
    ("CF",                    "evidence.CF",                     "D",   "pct"),
    ("E_final",               "evidence.E_final",                "D",   "pct"),
    ("why_penalty",           "evidence.why_penalty_active",     "D",   "bool"),
    ("claim_count_7q",        "claim_count",                     "D",   "int"),
    ("kill_count",            "kill_count",                      "D",   "int"),
    ("iso_status",            "iso_status",                      "D",   "text"),
    ("strongest_Q",           "strongest_Q",                     "D",   "text"),
    ("weakest_Q",             "weakest_Q",                       "D",   "text"),
    ("theory_resonance_D",    None,                              "D",   "int"),   # computed
    ("structural_D",          None,                              "D",   "int"),   # computed
    ("analogical_D",          None,                              "D",   "int"),   # computed

    # ── Stage E: Academic Review (OpenAI ~$0.03) ──
    ("citations_real",        "citation_check.all_real",         "E",   "bool"),
    ("suspect_citations",     None,                              "E",   "int"),   # computed
    ("missing_citations_E",   None,                              "E",   "int"),   # computed
    ("evidence_aligned",      "citation_check.evidence_claim_alignment.aligned", "E", "bool"),
    ("evidence_gaps",         None,                              "E",   "int"),   # computed
    ("math_correct",          "math_logic.math_correct",         "E",   "bool"),
    ("math_errors",           None,                              "E",   "int"),   # computed
    ("critical_math_errors",  None,                              "E",   "int"),   # computed
    ("logic_valid",           "math_logic.logic_valid",          "E",   "bool"),
    ("fallacy_count",         None,                              "E",   "int"),   # computed
    ("novelty_level",         "novelty_framing.novelty_level",   "E",   "text"),
    ("framing_honest",        "novelty_framing.framing_honest",  "E",   "bool"),
    ("framing_issues",        None,                              "E",   "int"),   # computed
    ("failure_count",         None,                              "E",   "int"),   # computed
    ("max_failure_severity",  None,                              "E",   "text"),  # computed
    ("publication_ready",     "publication_readiness.ready",     "E",   "bool"),
    ("blocker_count",         None,                              "E",   "int"),   # computed

    # ── Stage F: Extractor (OpenAI ~$0.03) ──
    ("axiom_ref_count",       None,                              "F",   "int"),   # computed
    ("axiom_missing_count",   None,                              "F",   "int"),   # computed
    ("missing_citations_F",   None,                              "F",   "int"),   # computed
    ("math_upgrade_diff",     "math_upgrade.difficulty",         "F",   "text"),
    ("cross_ref_count",       None,                              "F",   "int"),   # computed
    ("theory_resonance_F",    None,                              "F",   "int"),   # computed
    ("structural_F",          None,                              "F",   "int"),   # computed
    ("analogical_F",          None,                              "F",   "int"),   # computed
    ("isomorphic_imports",    None,                              "F",   "int"),   # computed
    ("physicist_score",       "triple_score.physicist.score",    "F",   "int"),
    ("philosopher_score",     "triple_score.philosopher.score",  "F",   "int"),
    ("editor_score",          "triple_score.editor.score",       "F",   "int"),
    ("triple_mean",           None,                              "F",   "float"), # computed

    # ── Backend: paper_metrics_engine ──
    ("backend_structure_score", "structure_score",               "BE",  "pct"),
    ("backend_citation_density","citation_density",              "BE",  "float"),
    ("backend_equation_density","equation_density",              "BE",  "float"),
    ("backend_heading_depth",  "heading_depth",                  "BE",  "int"),

    # ── Truth Engine ──
    ("te_truth_score",        "truth_score",                     "TE",  "pct"),
    ("te_grace_layer",        "grace_layer_score",               "TE",  "pct"),
    ("te_christ_vector",      "christ_vector_score",             "TE",  "pct"),
    ("te_word_hits",          "word_list_hits",                  "TE",  "int"),

    # ── Stage G: Computed ──
    ("composite_score",       None,                              "G",   "pct"),   # computed
    ("rank",                  None,                              "G",   "int"),   # computed
    ("status",                None,                              "G",   "text"),  # computed
    ("structural_echo_total", None,                              "G",   "int"),   # computed
    ("theory_register_count", None,                              "G",   "int"),   # computed

    # ── Cost tracking ──
    ("cost_D",                "_metadata.cost_usd",              "D$",  "money"),
    ("cost_E",                "_metadata.cost_usd",              "E$",  "money"),
    ("cost_F",                "_metadata.cost_usd",              "F$",  "money"),
    ("total_cost",            None,                              "G",   "money"), # computed
]


# ─── JSON path resolver ──────────────────────────────────────────────────────

def resolve_path(data, dotpath):
    """Resolve 'scores.Q0_POSTURE' → data['scores']['Q0_POSTURE']."""
    if not dotpath or not data:
        return None
    parts = dotpath.split(".")
    current = data
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


# ─── Computed fields ──────────────────────────────────────────────────────────

def compute_fields(stage_d, stage_e, stage_f, backend=None, truth_engine=None):
    """Compute derived fields that aren't directly in JSON."""
    c = {}

    # Stage D computed
    tr_d = stage_d.get("theory_resonance", [])
    c["theory_resonance_D"] = len(tr_d)
    c["structural_D"] = sum(1 for t in tr_d if t.get("mapping") == "STRUCTURAL")
    c["analogical_D"] = sum(1 for t in tr_d if t.get("mapping") == "ANALOGICAL")

    # Stage E computed
    cc = stage_e.get("citation_check", {})
    c["suspect_citations"] = len(cc.get("suspect_citations", []))
    c["missing_citations_E"] = len(cc.get("missing_citations", []))
    gaps = cc.get("evidence_claim_alignment", {}).get("gaps", [])
    c["evidence_gaps"] = len(gaps)

    ml = stage_e.get("math_logic", {})
    math_errs = ml.get("math_errors", [])
    c["math_errors"] = len(math_errs)
    c["critical_math_errors"] = sum(1 for e in math_errs if e.get("severity") == "critical")
    c["fallacy_count"] = len(ml.get("fallacies", []))

    nf = stage_e.get("novelty_framing", {})
    c["framing_issues"] = len(nf.get("framing_issues", []))

    cf = stage_e.get("critical_failures", [])
    c["failure_count"] = len(cf)
    severities = {"fatal": 3, "serious": 2, "moderate": 1}
    if cf:
        max_sev = max(severities.get(f.get("severity", ""), 0) for f in cf)
        c["max_failure_severity"] = {3: "fatal", 2: "serious", 1: "moderate"}.get(max_sev, "")
    else:
        c["max_failure_severity"] = ""

    pr = stage_e.get("publication_readiness", {})
    c["blocker_count"] = len(pr.get("blockers", []))

    # Stage F computed
    am = stage_f.get("axiom_mapping", {})
    c["axiom_ref_count"] = len(am.get("referenced", []))
    c["axiom_missing_count"] = len(am.get("missing", []))
    c["missing_citations_F"] = len(stage_f.get("missing_citations", []))
    c["cross_ref_count"] = len(stage_f.get("ft_cross_refs", []))

    tr_f = stage_f.get("theory_resonance", [])
    c["theory_resonance_F"] = len(tr_f)
    c["structural_F"] = sum(1 for t in tr_f if t.get("mapping") == "STRUCTURAL")
    c["analogical_F"] = sum(1 for t in tr_f if t.get("mapping") == "ANALOGICAL")
    c["isomorphic_imports"] = len(stage_f.get("isomorphic_imports", []))

    # Triple score
    ts = stage_f.get("triple_score", {})
    p_score = ts.get("physicist", {})
    ph_score = ts.get("philosopher", {})
    e_score = ts.get("editor", {})
    p_val = p_score.get("score", p_score) if isinstance(p_score, dict) else p_score
    ph_val = ph_score.get("score", ph_score) if isinstance(ph_score, dict) else ph_score
    e_val = e_score.get("score", e_score) if isinstance(e_score, dict) else e_score
    vals = [v for v in [p_val, ph_val, e_val] if isinstance(v, (int, float))]
    c["triple_mean"] = round(sum(vals) / len(vals), 1) if vals else 0

    # Stage G composite
    fruits = resolve_path(stage_f, "fruits_score") or 0
    coherence = resolve_path(stage_f, "coherence_score") or 0
    t_score = stage_d.get("T_score", 0) or 0
    triple_norm = (c["triple_mean"] / 100) if c["triple_mean"] else 0
    pub = 1.0 if pr.get("ready") else 0.0

    composite = (0.15 * fruits + 0.15 * coherence + 0.30 * t_score +
                 0.20 * triple_norm + 0.20 * pub)
    c["composite_score"] = round(composite, 3)

    if composite >= 0.7:
        c["status"] = "GREEN"
    elif composite >= 0.5:
        c["status"] = "YELLOW"
    else:
        c["status"] = "RED"

    c["structural_echo_total"] = c["structural_D"] + c["structural_F"]

    # Theory register: unique theories across D and F
    all_theories = set()
    for t in tr_d:
        all_theories.add(t.get("theory", ""))
    for t in tr_f:
        all_theories.add(t.get("theory", ""))
    all_theories.discard("")
    c["theory_register_count"] = len(all_theories)

    # Cost
    cost_d = resolve_path(stage_d, "_metadata.cost_usd") or 0
    cost_e = resolve_path(stage_e, "_metadata.cost_usd") or 0
    cost_f = resolve_path(stage_f, "_metadata.cost_usd") or 0
    c["cost_D"] = cost_d
    c["cost_E"] = cost_e
    c["cost_F"] = cost_f
    c["total_cost"] = round(cost_d + cost_e + cost_f, 4)

    return c


# ─── File discovery ───────────────────────────────────────────────────────────

def discover_paper_outputs(folder):
    """Find all paper output sets in a folder. Groups by paper stem."""
    folder = Path(folder)
    papers = {}

    suffixes = {
        "_7Q_JUDGE.json": "D",
        "_ACADEMIC.json": "E",
        "_EXTRACTOR.json": "F",
        "_CKG.json": "CKG",
        "_DOMAINS.json": "DOMAIN",
        "_CDCM.json": "REVIEW",
    }

    for f in folder.iterdir():
        if not f.is_file() or not f.suffix == ".json":
            continue
        for suffix, stage in suffixes.items():
            if f.name.endswith(suffix):
                stem = f.name[:-len(suffix)]
                if stem not in papers:
                    papers[stem] = {}
                papers[stem][stage] = f
                break

    return papers


# ─── Row builder ──────────────────────────────────────────────────────────────

def build_row(paper_stem, files, run_date=None):
    """Build one row of data for a paper."""
    stage_d = load_json(files.get("D"))
    stage_e = load_json(files.get("E"))
    stage_f = load_json(files.get("F"))

    computed = compute_fields(stage_d, stage_e, stage_f)

    row = {}
    row["paper_id"] = paper_stem
    row["paper_title"] = paper_stem.replace("_", " ").replace("-", " ")
    row["run_date"] = run_date or datetime.now().strftime("%Y-%m-%d")

    # Resolve all JSON paths
    stage_map = {"A": {}, "B": {}, "C": {}, "D": stage_d, "E": stage_e,
                 "F": stage_f, "BE": {}, "TE": {}, "D$": stage_d,
                 "E$": stage_e, "F$": stage_f}

    for col_name, json_path, source, fmt in COLUMNS:
        if col_name in row:
            continue

        # Check computed first
        if col_name in computed:
            row[col_name] = computed[col_name]
            continue

        # Resolve from JSON
        if json_path and source in stage_map:
            val = resolve_path(stage_map[source], json_path)
            if val is not None:
                row[col_name] = val
                continue

        # Default
        if fmt == "int":
            row[col_name] = 0
        elif fmt in ("float", "pct", "money"):
            row[col_name] = 0.0
        elif fmt == "bool":
            row[col_name] = False
        else:
            row[col_name] = ""

    return row


def load_json(path):
    """Load JSON file, return empty dict if missing."""
    if path is None or not Path(path).exists():
        return {}
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, Exception):
        return {}


# ─── Excel writer ─────────────────────────────────────────────────────────────

# Stage colors for header grouping
STAGE_COLORS = {
    "ID":  "D9E2F3",  # light blue
    "A":   "E2EFDA",  # light green
    "B":   "E2EFDA",
    "C":   "E2EFDA",
    "D":   "FCE4D6",  # light orange
    "E":   "FCE4D6",
    "F":   "FCE4D6",
    "BE":  "F2F2F2",  # light gray
    "TE":  "F2F2F2",
    "G":   "D6E4FC",  # light purple
    "D$":  "FFF2CC",  # light yellow
    "E$":  "FFF2CC",
    "F$":  "FFF2CC",
}

STATUS_COLORS = {
    "GREEN":  "92D050",
    "YELLOW": "FFC000",
    "RED":    "FF4444",
}


def write_excel(rows, output_path):
    """Write all paper rows to one Excel workbook."""
    wb = Workbook()
    ws = wb.active
    ws.title = "ALL_METRICS"

    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin'),
    )

    # ── Headers ──
    for col_idx, (col_name, _, source, _) in enumerate(COLUMNS, 1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.font = Font(bold=True, size=9)
        cell.alignment = Alignment(horizontal='center', wrap_text=True)
        cell.border = thin_border

        color = STAGE_COLORS.get(source, "FFFFFF")
        cell.fill = PatternFill(start_color=color, end_color=color, fill_type='solid')

    # ── Data rows ──
    for row_idx, row_data in enumerate(rows, 2):
        for col_idx, (col_name, _, source, fmt) in enumerate(COLUMNS, 1):
            val = row_data.get(col_name, "")

            # Format
            if fmt == "bool" and isinstance(val, bool):
                val = "Y" if val else "N"
            elif fmt == "pct" and isinstance(val, (int, float)):
                val = round(val, 3)
            elif fmt == "money" and isinstance(val, (int, float)):
                val = round(val, 4)

            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = Font(size=9)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

            # Color status cells
            if col_name == "status" and val in STATUS_COLORS:
                c = STATUS_COLORS[val]
                cell.fill = PatternFill(start_color=c, end_color=c, fill_type='solid')
                cell.font = Font(size=9, bold=True, color="FFFFFF")

    # ── Column widths ──
    for col_idx, (col_name, _, _, _) in enumerate(COLUMNS, 1):
        width = max(len(col_name) + 2, 10)
        if "text" in col_name or "claim" in col_name:
            width = 25
        ws.column_dimensions[get_column_letter(col_idx)].width = min(width, 30)

    # ── Freeze panes (header + paper_id) ──
    ws.freeze_panes = "B2"

    # ── Auto-filter ──
    ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}{len(rows) + 1}"

    # ── Save ──
    wb.save(output_path)
    print(f"\n[EXCEL] Wrote {len(rows)} papers x {len(COLUMNS)} columns → {output_path}")


# ─── Theory Resonance Register (Sheet 2) ─────────────────────────────────────

def build_theory_register(all_stage_d, all_stage_f):
    """Build master theory resonance register across all papers."""
    register = {}  # theory_name -> {domain, papers, structural, analogical}

    for paper_stem, d_data in all_stage_d.items():
        for tr in d_data.get("theory_resonance", []):
            theory = tr.get("theory", "")
            if not theory:
                continue
            if theory not in register:
                register[theory] = {
                    "domain": tr.get("domain", tr.get("source_domain", "")),
                    "papers": [],
                    "structural": 0,
                    "analogical": 0,
                }
            register[theory]["papers"].append(paper_stem)
            if tr.get("mapping") == "STRUCTURAL":
                register[theory]["structural"] += 1
            elif tr.get("mapping") == "ANALOGICAL":
                register[theory]["analogical"] += 1

    for paper_stem, f_data in all_stage_f.items():
        for tr in f_data.get("theory_resonance", []):
            theory = tr.get("theory", "")
            if not theory:
                continue
            if theory not in register:
                register[theory] = {
                    "domain": tr.get("source_domain", ""),
                    "papers": [],
                    "structural": 0,
                    "analogical": 0,
                }
            if paper_stem not in register[theory]["papers"]:
                register[theory]["papers"].append(paper_stem)
            if tr.get("mapping") == "STRUCTURAL":
                register[theory]["structural"] += 1
            elif tr.get("mapping") == "ANALOGICAL":
                register[theory]["analogical"] += 1

    return register


def write_theory_register(wb, register):
    """Write theory resonance register as Sheet 2."""
    ws = wb.create_sheet("THEORY_REGISTER")

    headers = ["Theory", "Domain", "Paper Count", "Papers", "Structural", "Analogical", "Total"]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = Font(bold=True, size=9)
        cell.fill = PatternFill(start_color="D6E4FC", end_color="D6E4FC", fill_type='solid')

    sorted_theories = sorted(register.items(),
                             key=lambda x: x[1]["structural"] + len(x[1]["papers"]),
                             reverse=True)

    for row, (theory, info) in enumerate(sorted_theories, 2):
        ws.cell(row=row, column=1, value=theory)
        ws.cell(row=row, column=2, value=info["domain"])
        ws.cell(row=row, column=3, value=len(info["papers"]))
        ws.cell(row=row, column=4, value=", ".join(info["papers"]))
        ws.cell(row=row, column=5, value=info["structural"])
        ws.cell(row=row, column=6, value=info["analogical"])
        ws.cell(row=row, column=7, value=info["structural"] + info["analogical"])

    # Column widths
    widths = [35, 25, 12, 50, 12, 12, 10]
    for col, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(col)].width = w

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:G{len(sorted_theories) + 1}"


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Write all pipeline metrics to one Excel workbook"
    )
    parser.add_argument("folder", help="Folder containing JSON output files")
    parser.add_argument("-o", "--output", default=None,
                        help="Output Excel path (default: OPERATOR_2_RESULTS.xlsx)")
    parser.add_argument("--paper", default=None,
                        help="Process only this paper stem")

    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        print(f"[ERROR] Not a directory: {folder}")
        sys.exit(1)

    output_path = args.output or str(folder / "OPERATOR_2_RESULTS.xlsx")

    # Discover paper outputs
    papers = discover_paper_outputs(folder)
    if not papers:
        print(f"[ERROR] No paper outputs found in {folder}")
        sys.exit(1)

    if args.paper:
        if args.paper in papers:
            papers = {args.paper: papers[args.paper]}
        else:
            print(f"[ERROR] Paper '{args.paper}' not found. Available: {list(papers.keys())}")
            sys.exit(1)

    print(f"[EXCEL] Found {len(papers)} papers in {folder}")

    # Build rows
    rows = []
    all_stage_d = {}
    all_stage_f = {}

    for stem in sorted(papers.keys()):
        files = papers[stem]
        print(f"  Processing: {stem} ({', '.join(files.keys())})")
        row = build_row(stem, files)
        rows.append(row)

        # Collect for theory register
        if "D" in files:
            all_stage_d[stem] = load_json(files["D"])
        if "F" in files:
            all_stage_f[stem] = load_json(files["F"])

    # Write main sheet
    write_excel(rows, output_path)

    # Add theory register as Sheet 2
    if all_stage_d or all_stage_f:
        register = build_theory_register(all_stage_d, all_stage_f)
        if register:
            from openpyxl import load_workbook
            wb = load_workbook(output_path)
            write_theory_register(wb, register)

            # Rank papers on main sheet
            ws = wb["ALL_METRICS"]
            rank_col = None
            for col_idx, (col_name, _, _, _) in enumerate(COLUMNS, 1):
                if col_name == "rank":
                    rank_col = col_idx
                    break
            if rank_col:
                composites = []
                comp_col = None
                for col_idx, (col_name, _, _, _) in enumerate(COLUMNS, 1):
                    if col_name == "composite_score":
                        comp_col = col_idx
                        break
                if comp_col:
                    for row_idx in range(2, len(rows) + 2):
                        val = ws.cell(row=row_idx, column=comp_col).value or 0
                        composites.append((row_idx, val))
                    composites.sort(key=lambda x: x[1], reverse=True)
                    for rank, (row_idx, _) in enumerate(composites, 1):
                        ws.cell(row=row_idx, column=rank_col, value=rank)

            wb.save(output_path)
            print(f"[EXCEL] Added theory register ({len(register)} theories)")

    print(f"\n[DONE] {output_path}")


if __name__ == "__main__":
    main()
