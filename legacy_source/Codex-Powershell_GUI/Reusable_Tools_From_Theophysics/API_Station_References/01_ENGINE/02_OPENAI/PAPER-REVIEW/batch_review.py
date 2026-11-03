#!/usr/bin/env python3
"""
CDCM Batch Paper Review
========================
Runs the CDCM 44-criteria review on every .md file in a folder.
Saves report, JSON scores, CSV, and populated Excel to OpenAI_DATA/.

Usage:
    python batch_review.py --folder "O:/path/to/papers"
    python batch_review.py --folder "O:/path/to/papers" --dry-run
"""

import os, sys, re, json, csv, time, pathlib, argparse, datetime, shutil, base64, mimetypes

sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR  = pathlib.Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config.txt"
PROMPT_PATH = SCRIPT_DIR / "prompt.txt"
CDCM_TEMPLATE = pathlib.Path("C:/Users/lowes/OneDrive/Desktop/CDCM_final.xlsx")

PRICING = {
    "gpt-4o":      (0.0025, 0.0100),
    "gpt-4o-mini": (0.00015, 0.0006),
    "gpt-4-turbo": (0.0100,  0.0300),
}

CRITERIA = [
    ("A1","Citation Quality","Source Existence & Verifiability"),
    ("A2","Citation Quality","Source Authority & Relevance"),
    ("A3","Citation Quality","Citation Formatting"),
    ("A4","Citation Quality","Citation Density & Distribution"),
    ("B1","Factual Accuracy","Empirical Claim Accuracy"),
    ("B2","Factual Accuracy","Historical/Contextual Accuracy"),
    ("B3","Factual Accuracy","Mathematical/Formal Accuracy"),
    ("B4","Factual Accuracy","Claim-Evidence Alignment"),
    ("C1","Logical Rigor","Deductive Validity"),
    ("C2","Logical Rigor","Inductive Strength"),
    ("C3","Logical Rigor","Absence of Fallacies"),
    ("C4","Logical Rigor","Argument Chain Integrity"),
    ("D1","Evidence Sufficiency","Claim Strength vs Evidence Weight"),
    ("D2","Evidence Sufficiency","Counter-Evidence Engagement"),
    ("D3","Evidence Sufficiency","Replication & Corroboration"),
    ("D4","Evidence Sufficiency","Statistical Rigor"),
    ("E1","Semantic Precision","Term Definition Consistency"),
    ("E2","Semantic Precision","Equivocation Detection"),
    ("E3","Semantic Precision","Domain Translation Fidelity"),
    ("E4","Semantic Precision","Hedging Calibration"),
    ("F1","Academic Convention","Abstract Quality"),
    ("F2","Academic Convention","Methodology Transparency"),
    ("F3","Academic Convention","Structure & Flow"),
    ("F4","Academic Convention","Peer Convention Compliance"),
    ("G1","Wording & Clarity","Prose Precision"),
    ("G2","Wording & Clarity","Jargon Accessibility"),
    ("G3","Wording & Clarity","Concision"),
    ("G4","Wording & Clarity","Tone Calibration"),
    ("H1","Cross-Domain Validity","Isomorphism vs Analogy Distinction"),
    ("H2","Cross-Domain Validity","Domain Boundary Respect"),
    ("H3","Cross-Domain Validity","Mapping Rigor"),
    ("H4","Cross-Domain Validity","Prediction Transfer"),
    ("I1","Falsifiability & Scope","Falsification Criteria Stated"),
    ("I2","Falsifiability & Scope","Scope Boundaries Declared"),
    ("I3","Falsifiability & Scope","Failure Mode Acknowledgment"),
    ("I4","Falsifiability & Scope","Testable Prediction Specificity"),
    ("J1","External Theory Usage","Theory Representation Accuracy"),
    ("J2","External Theory Usage","Scope Boundary Respect for Borrowed Theories"),
    ("J3","External Theory Usage","Integration vs Appropriation"),
    ("J4","External Theory Usage","Competing Interpretation Acknowledgment"),
    ("K1","Novelty Assessment","Conceptual Originality"),
    ("K2","Novelty Assessment","Nearest Existing Framework Distance"),
    ("K3","Novelty Assessment","Methodological Innovation"),
    ("K4","Novelty Assessment","Gap-Filling vs Gap-Creating"),
]

WEIGHTS = {"A":0.12,"B":0.14,"C":0.16,"D":0.12,"E":0.10,
           "F":0.08,"G":0.08,"H":0.10,"I":0.10,"J":0.06,"K":0.06}

SKIP_FILES = {"README.md", "index.md", "downloads.md"}


def parse_config():
    cfg = {}
    if CONFIG_PATH.exists():
        for line in CONFIG_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                cfg[k.strip()] = v.strip()
    return cfg


def read_prompt():
    lines = PROMPT_PATH.read_text(encoding="utf-8").splitlines()
    return "\n".join(l for l in lines if not l.strip().startswith("#")).strip()


def estimate_tokens(text):
    return max(1, len(text) // 4)


def parse_response(text):
    scores, comments = {}, {}
    pattern = re.compile(
        r'^([A-K]\d):\s*(\d+(?:\.\d+)?)\s*[—\-–]\s*[^|]+\|\s*Comment:\s*(.+)',
        re.MULTILINE
    )
    for m in pattern.finditer(text):
        code = m.group(1).upper()
        scores[code]   = min(10.0, max(0.0, float(m.group(2))))
        comments[code] = m.group(3).strip()
    if len(scores) < 10:
        for m in re.finditer(r'^([A-K]\d):\s*(\d+(?:\.\d+)?)', text, re.MULTILINE):
            code = m.group(1).upper()
            if code not in scores:
                scores[code] = float(m.group(2))
    return scores, comments


def compute_sections(scores):
    out = {}
    for letter in "ABCDEFGHIJK":
        vals = [scores[f"{letter}{i}"] for i in range(1,5) if f"{letter}{i}" in scores]
        if vals:
            out[letter] = round(sum(vals)/len(vals), 2)
    return out


def compute_total(section_avgs):
    return round(sum(avg * WEIGHTS.get(l, 0) * 10 for l, avg in section_avgs.items()), 1)


def save_outputs(paper_name, reply, scores, comments, section_avgs, total, out_dir, model):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Text report
    (out_dir / f"{paper_name}_CDCM_{ts}.txt").write_text(reply, encoding="utf-8")

    # JSON
    payload = {
        "paper": paper_name, "model": model, "timestamp": ts,
        "total_score": total, "section_averages": section_avgs,
        "sub_criteria": {c: {"score": scores.get(c), "comment": comments.get(c,"")}
                         for c,_,_ in CRITERIA},
    }
    (out_dir / f"{paper_name}_CDCM_{ts}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # CSV
    csv_path = out_dir / f"{paper_name}_CDCM_{ts}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["#","SECTION","SUB-CRITERION","OPENAI_SCORE","OPENAI_NOTES"])
        for code, section, criterion in CRITERIA:
            w.writerow([code, section, criterion, scores.get(code,""), comments.get(code,"")])
        w.writerow([])
        w.writerow(["SECTION_AVERAGES"])
        for l, avg in section_avgs.items():
            w.writerow([l, avg])
        w.writerow(["TOTAL_WEIGHTED_SCORE", total])

    # Populated Excel
    if CDCM_TEMPLATE.exists():
        try:
            import openpyxl
            xl_out = out_dir / f"{paper_name}_CDCM_{ts}.xlsx"
            shutil.copy(CDCM_TEMPLATE, xl_out)
            wb = openpyxl.load_workbook(xl_out)
            ws = wb["Paper_Grade"]
            openai_col = notes_col = None
            for row in ws.iter_rows(min_row=1, max_row=10):
                for cell in row:
                    v = str(cell.value or "").strip().upper()
                    if v == "OPENAI": openai_col = cell.column
                    if "OPENAI NOTES" in v: notes_col = cell.column
            if openai_col and notes_col:
                for row in ws.iter_rows(min_row=6, max_row=ws.max_row):
                    code = str(row[0].value or "").strip().upper()
                    if len(code)==2 and code[0].isalpha() and code[1].isdigit() and code in scores:
                        try:
                            ws.cell(row=row[0].row, column=openai_col).value = scores[code]
                            ws.cell(row=row[0].row, column=notes_col).value = comments.get(code,"")
                        except: pass
            ws["C3"] = paper_name
            ws["G3"] = datetime.date.today().isoformat()
            wb.save(xl_out)
        except Exception as e:
            print(f"  Excel save skipped: {e}")

    return ts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    folder = pathlib.Path(args.folder)
    out_dir = folder / "OpenAI_DATA"
    papers  = sorted(p for p in folder.glob("*.md") if p.name not in SKIP_FILES)

    if not papers:
        sys.exit("No .md files found.")

    cfg         = parse_config()
    api_key     = cfg.get("OPENAI_API_KEY","")
    model       = cfg.get("MODEL","gpt-4o")
    max_tokens  = int(cfg.get("MAX_TOKENS","4096"))
    temperature = float(cfg.get("TEMPERATURE","0"))
    prompt_text = read_prompt()

    print("=" * 60)
    print(f"  CDCM Batch Review — {len(papers)} papers")
    print(f"  Model: {model}  |  Output: OpenAI_DATA/")
    print("=" * 60)

    total_est_cost = 0.0
    for p in papers:
        text = p.read_text(encoding="utf-8", errors="replace")
        est = estimate_tokens(prompt_text + text)
        ir, or_ = PRICING.get(model, (0.0025, 0.01))
        cost = (est/1000)*ir + (max_tokens/1000)*or_
        total_est_cost += cost
        print(f"  {p.name:<55} ~{est:,} tokens  ${cost:.4f}")

    print(f"\n  ESTIMATED TOTAL COST: ${total_est_cost:.4f}")
    print("=" * 60)

    if args.dry_run:
        print("\nDRY RUN complete. No API calls made.")
        return

    if not api_key or api_key.startswith("sk-PASTE"):
        sys.exit("ERROR: No API key in config.txt")

    try:
        import openai
    except ImportError:
        sys.exit("ERROR: pip install openai")

    client = openai.OpenAI(api_key=api_key)

    results = []
    for i, paper_path in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] {paper_path.name}")
        text = paper_path.read_text(encoding="utf-8", errors="replace")
        messages = [{"role":"user","content":[
            {"type":"text","text": prompt_text},
            {"type":"text","text": f"\n--- PAPER: {paper_path.name} ---\n{text}"},
        ]}]

        try:
            t0 = time.time()
            resp = client.chat.completions.create(
                model=model, messages=messages,
                temperature=temperature, max_tokens=max_tokens
            )
            elapsed = time.time() - t0
            reply   = resp.choices[0].message.content

            scores, comments = parse_response(reply)
            section_avgs     = compute_sections(scores)
            total            = compute_total(section_avgs)
            grade = ("A+" if total>=95 else "A" if total>=90 else "B+" if total>=85
                     else "B" if total>=80 else "C+" if total>=75 else "C" if total>=70 else "D")

            save_outputs(paper_path.stem, reply, scores, comments, section_avgs, total, out_dir, model)

            print(f"  Score: {total}/100  Grade: {grade}  ({elapsed:.1f}s)")
            for l, avg in section_avgs.items():
                flag = "PASS" if avg>=7 else "WEAK" if avg>=5 else "FAIL"
                print(f"    {l}: {avg}  [{flag}]")

            results.append({"paper": paper_path.name, "total": total, "grade": grade,
                             "sections": section_avgs})
            time.sleep(1)

        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({"paper": paper_path.name, "total": None, "grade": "ERR", "error": str(e)})

    # Summary
    print("\n" + "=" * 60)
    print("  BATCH SUMMARY")
    print("=" * 60)
    for r in sorted(results, key=lambda x: x.get("total") or 0, reverse=True):
        score = r.get("total")
        print(f"  {r['grade']}  {score or 'ERR':>5}  {r['paper']}")

    summary_path = out_dir / f"CDCM_BATCH_SUMMARY_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    summary_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Summary saved: {summary_path.name}")


if __name__ == "__main__":
    main()
