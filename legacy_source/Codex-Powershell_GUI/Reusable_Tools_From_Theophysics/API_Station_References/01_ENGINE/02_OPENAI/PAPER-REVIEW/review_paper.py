#!/usr/bin/env python3
"""
CDCM Adversarial Paper Review
==============================
Sends your paper to OpenAI for rigorous 44-criteria academic review.
Parses the structured A1-K4 response and outputs:
  - Full text report  (output/report_<paper>_<ts>.txt)
  - Structured JSON   (output/scores_<paper>_<ts>.json)
  - Excel-ready CSV   (output/scores_<paper>_<ts>.csv)

The CSV maps directly to the CDCM_final.xlsx OpenAI columns.

Usage:
    python review_paper.py              # Reviews first file in input/
    python review_paper.py --dry-run    # Cost estimate, no API call
    python review_paper.py --file myfile.md
"""

import os, sys, re, json, csv, time, pathlib, argparse, datetime, base64, mimetypes

SCRIPT_DIR  = pathlib.Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config.txt"
PROMPT_PATH = SCRIPT_DIR / "prompt.txt"
INPUT_DIR   = SCRIPT_DIR / "input"
OUTPUT_DIR  = SCRIPT_DIR / "output"

PRICING = {
    "gpt-4o":      (0.0025, 0.0100),
    "gpt-4o-mini": (0.00015, 0.0006),
    "gpt-4-turbo": (0.0100,  0.0300),
}

# All 44 sub-criteria codes in order
CRITERIA = [
    ("A1","Citation Quality",           "Source Existence & Verifiability"),
    ("A2","Citation Quality",           "Source Authority & Relevance"),
    ("A3","Citation Quality",           "Citation Formatting"),
    ("A4","Citation Quality",           "Citation Density & Distribution"),
    ("B1","Factual Accuracy",           "Empirical Claim Accuracy"),
    ("B2","Factual Accuracy",           "Historical/Contextual Accuracy"),
    ("B3","Factual Accuracy",           "Mathematical/Formal Accuracy"),
    ("B4","Factual Accuracy",           "Claim-Evidence Alignment"),
    ("C1","Logical Rigor",              "Deductive Validity"),
    ("C2","Logical Rigor",              "Inductive Strength"),
    ("C3","Logical Rigor",              "Absence of Fallacies"),
    ("C4","Logical Rigor",              "Argument Chain Integrity"),
    ("D1","Evidence Sufficiency",       "Claim Strength vs Evidence Weight"),
    ("D2","Evidence Sufficiency",       "Counter-Evidence Engagement"),
    ("D3","Evidence Sufficiency",       "Replication & Corroboration"),
    ("D4","Evidence Sufficiency",       "Statistical Rigor"),
    ("E1","Semantic Precision",         "Term Definition Consistency"),
    ("E2","Semantic Precision",         "Equivocation Detection"),
    ("E3","Semantic Precision",         "Domain Translation Fidelity"),
    ("E4","Semantic Precision",         "Hedging Calibration"),
    ("F1","Academic Convention",        "Abstract Quality"),
    ("F2","Academic Convention",        "Methodology Transparency"),
    ("F3","Academic Convention",        "Structure & Flow"),
    ("F4","Academic Convention",        "Peer Convention Compliance"),
    ("G1","Wording & Clarity",          "Prose Precision"),
    ("G2","Wording & Clarity",          "Jargon Accessibility"),
    ("G3","Wording & Clarity",          "Concision"),
    ("G4","Wording & Clarity",          "Tone Calibration"),
    ("H1","Cross-Domain Validity",      "Isomorphism vs Analogy Distinction"),
    ("H2","Cross-Domain Validity",      "Domain Boundary Respect"),
    ("H3","Cross-Domain Validity",      "Mapping Rigor"),
    ("H4","Cross-Domain Validity",      "Prediction Transfer"),
    ("I1","Falsifiability & Scope",     "Falsification Criteria Stated"),
    ("I2","Falsifiability & Scope",     "Scope Boundaries Declared"),
    ("I3","Falsifiability & Scope",     "Failure Mode Acknowledgment"),
    ("I4","Falsifiability & Scope",     "Testable Prediction Specificity"),
    ("J1","External Theory Usage",      "Theory Representation Accuracy"),
    ("J2","External Theory Usage",      "Scope Boundary Respect for Borrowed Theories"),
    ("J3","External Theory Usage",      "Integration vs Appropriation"),
    ("J4","External Theory Usage",      "Competing Interpretation Acknowledgment"),
    ("K1","Novelty Assessment",         "Conceptual Originality"),
    ("K2","Novelty Assessment",         "Nearest Existing Framework Distance"),
    ("K3","Novelty Assessment",         "Methodological Innovation"),
    ("K4","Novelty Assessment",         "Gap-Filling vs Gap-Creating"),
]

# Section weights matching CDCM_final.xlsx Paper_Grade sheet
WEIGHTS = {
    "A": 0.12, "B": 0.14, "C": 0.16,
    "D": 0.12, "E": 0.10, "F": 0.08,
    "G": 0.08, "H": 0.10, "I": 0.10,
    "J": 0.06, "K": 0.06,
}


# ---------------------------------------------------------------------------
#  Config & helpers
# ---------------------------------------------------------------------------

def parse_config(path):
    cfg = {}
    if not path.exists():
        return cfg
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, _, v = line.partition("=")
            cfg[k.strip()] = v.strip()
    return cfg


def read_prompt(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    content = [l for l in lines if not l.strip().startswith("#")]
    return "\n".join(content).strip()


def load_paper(paper_path):
    ext = paper_path.suffix.lower()
    if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        mime = mimetypes.guess_type(str(paper_path))[0] or "image/png"
        b64 = base64.b64encode(paper_path.read_bytes()).decode("ascii")
        return None, ("image", mime, b64)
    return paper_path.read_text(encoding="utf-8", errors="replace"), None


def estimate_tokens(text):
    return max(1, len(text) // 4)


def format_cost(model, inp, out):
    if model not in PRICING:
        return f"(no pricing data for {model})"
    ir, or_ = PRICING[model]
    ic = (inp / 1000) * ir
    oc = (out / 1000) * or_
    return (f"  Model: {model}\n"
            f"  Input : ~{inp:,} tokens  ${ic:.6f}\n"
            f"  Output: ~{out:,} tokens  ${oc:.6f}\n"
            f"  TOTAL : ${ic+oc:.6f}")


# ---------------------------------------------------------------------------
#  Response parser
# ---------------------------------------------------------------------------

def parse_response(text):
    """Extract A1-K4 scores and comments from the structured response."""
    scores = {}
    comments = {}

    # Pattern: A1: 7 — Description | Comment: text
    pattern = re.compile(
        r'^([A-K]\d):\s*(\d+(?:\.\d+)?)\s*[—\-–]\s*[^|]+\|\s*Comment:\s*(.+)',
        re.MULTILINE
    )
    for m in pattern.finditer(text):
        code  = m.group(1).upper()
        score = float(m.group(2))
        note  = m.group(3).strip()
        scores[code]   = min(10.0, max(0.0, score))
        comments[code] = note

    # Fallback: simpler "A1: 7" pattern if comment format differs
    if len(scores) < 10:
        simple = re.compile(r'^([A-K]\d):\s*(\d+(?:\.\d+)?)', re.MULTILINE)
        for m in simple.finditer(text):
            code = m.group(1).upper()
            if code not in scores:
                scores[code] = float(m.group(2))

    return scores, comments


def compute_section_averages(scores):
    sections = {}
    for letter in "ABCDEFGHIJK":
        vals = [scores[f"{letter}{i}"] for i in range(1, 5)
                if f"{letter}{i}" in scores]
        if vals:
            sections[letter] = round(sum(vals) / len(vals), 2)
    return sections


def compute_weighted_total(section_avgs):
    total = 0.0
    for letter, avg in section_avgs.items():
        w = WEIGHTS.get(letter, 0.0)
        total += avg * w * 10  # scale 0-10 → 0-100
    return round(total, 1)


def extract_summary_section(text):
    """Pull out the post-scoring summary block."""
    summary = {}

    # 1. THREE most critical failures
    m = re.search(
        r'THREE most critical failures.*?[:]\s*(.+?)(?=\n\d\.|\Z)',
        text, re.IGNORECASE | re.DOTALL
    )
    if m:
        summary["failures"] = m.group(1).strip()[:600]

    # 2. THREE revisions — capture the full block including sub-bullets
    m = re.search(
        r'THREE specific revisions.*?[:]\s*(.+?)(?=\n\d\.|\Z)',
        text, re.IGNORECASE | re.DOTALL
    )
    if m:
        block = m.group(1).strip()
        summary["revisions_all"] = block[:800]
        # Also split into individual revisions
        for label, key in [("Revision 1", "revision_1"), ("Revision 2", "revision_2"), ("Revision 3", "revision_3")]:
            rm = re.search(rf'{label}.*?[:]\s*(.+?)(?=Revision [23]|\Z)', block, re.IGNORECASE | re.DOTALL)
            if rm:
                summary[key] = rm.group(1).strip()[:300]

    # Fallback: old "single revision" format
    if "revision_1" not in summary:
        m = re.search(
            r'single revision.*?[:]\s*(.+?)(?=\n\d\.|\Z)',
            text, re.IGNORECASE | re.DOTALL
        )
        if m:
            summary["revision_1"] = m.group(1).strip()[:300]

    # 3. Surprisingly well
    m = re.search(
        r'paper does surprisingly well.*?[:]\s*(.+?)(?=\n\d\.|\Z)',
        text, re.IGNORECASE | re.DOTALL
    )
    if m:
        summary["strength"] = m.group(1).strip()[:300]

    # 4. CLOSEST REPRESENTATION
    m = re.search(
        r'CLOSEST REPRESENTATION.*?[:]\s*(.+?)(?=\n\d\.|\Z)',
        text, re.IGNORECASE | re.DOTALL
    )
    if m:
        block = m.group(1).strip()
        summary["closest_representation"] = block[:600]
        for label, key in [("Closest 1", "closest_1"), ("Closest 2", "closest_2"), ("Closest 3", "closest_3")]:
            rm = re.search(rf'{label}.*?[:—]\s*(.+?)(?=Closest [23]|\Z)', block, re.IGNORECASE | re.DOTALL)
            if rm:
                summary[key] = rm.group(1).strip()[:250]

    # 5. KEY CHARACTERISTICS
    m = re.search(
        r'KEY CHARACTERISTICS.*?[:]\s*(.+?)(?=\n\d\.|\Z)',
        text, re.IGNORECASE | re.DOTALL
    )
    if m:
        summary["key_characteristics"] = m.group(1).strip()[:600]

    # 6. NOVELTY MAP
    m = re.search(
        r'NOVELTY MAP.*?[:]\s*(.+?)(?=\n\d\.|\Z)',
        text, re.IGNORECASE | re.DOTALL
    )
    if m:
        summary["novelty_map"] = m.group(1).strip()[:500]

    # Legacy keys for backward compat
    summary["summary_1"] = summary.get("failures", "")
    summary["summary_2"] = summary.get("revisions_all", summary.get("revision_1", ""))
    summary["summary_3"] = summary.get("strength", "")
    summary["summary_4"] = summary.get("novelty_map", "")

    return summary


# ---------------------------------------------------------------------------
#  Output writers
# ---------------------------------------------------------------------------

def save_text(text, paper_name, model):
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    p = OUTPUT_DIR / f"report_{paper_name}_{ts}.txt"
    p.write_text(text, encoding="utf-8")
    return p


def save_json(scores, comments, section_avgs, total, paper_name, model, summary):
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    p = OUTPUT_DIR / f"scores_{paper_name}_{ts}.json"
    payload = {
        "paper": paper_name,
        "model": model,
        "timestamp": ts,
        "total_score": total,
        "section_averages": section_avgs,
        "sub_criteria": {
            code: {"score": scores.get(code), "comment": comments.get(code, "")}
            for code, _, _ in CRITERIA
        },
        "summary": summary,
    }
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def save_csv(scores, comments, section_avgs, total, paper_name, model):
    """CSV with one row per sub-criterion — paste OPENAI column into CDCM Excel."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    p = OUTPUT_DIR / f"scores_{paper_name}_{ts}.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["#", "SECTION", "SUB-CRITERION", "OPENAI_SCORE", "OPENAI_NOTES"])
        for code, section, criterion in CRITERIA:
            w.writerow([
                code,
                section,
                criterion,
                scores.get(code, ""),
                comments.get(code, ""),
            ])
        w.writerow([])
        w.writerow(["SECTION_AVERAGES"])
        for letter, avg in section_avgs.items():
            w.writerow([letter, avg])
        w.writerow(["TOTAL_WEIGHTED_SCORE", total])
    return p


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="CDCM Adversarial Paper Review")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--file", type=str, help="Specific file in input/ to review")
    args = parser.parse_args()

    cfg        = parse_config(CONFIG_PATH)
    api_key    = cfg.get("OPENAI_API_KEY", "")
    model      = cfg.get("MODEL", "gpt-4o")
    max_tokens = int(cfg.get("MAX_TOKENS", "4096") or "4096")
    temperature = float(cfg.get("TEMPERATURE", "0"))

    if not api_key or api_key.startswith("sk-PASTE"):
        if not args.dry_run:
            sys.exit("ERROR: No API key in config.txt")

    # Find paper
    if args.file:
        paper_path = INPUT_DIR / args.file
    else:
        papers = sorted(INPUT_DIR.glob("*"))
        papers = [p for p in papers if p.is_file() and p.name != ".gitkeep"]
        if not papers:
            sys.exit("ERROR: No files in input/. Drop your paper there first.")
        paper_path = papers[0]

    paper_name = paper_path.stem
    prompt_text = read_prompt(PROMPT_PATH)
    paper_text, image_data = load_paper(paper_path)

    print("=" * 60)
    print("  CDCM Adversarial Paper Review")
    print("=" * 60)
    print(f"  Paper : {paper_path.name}")
    print(f"  Model : {model}")
    print(f"  Temp  : {temperature}")

    # Build messages
    if image_data:
        _, mime, b64 = image_data
        content = [
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
        ]
    else:
        content = [
            {"type": "text", "text": prompt_text},
            {"type": "text", "text": f"\n--- PAPER: {paper_path.name} ---\n{paper_text}"},
        ]
    system_msg = (
        "You are a rigorous academic peer reviewer evaluating papers for scholarly quality "
        "across citation accuracy, logical rigor, evidence sufficiency, semantic precision, "
        "and cross-domain validity. You evaluate papers on any subject — including philosophy, "
        "theology, physics, mathematics, and interdisciplinary work — using only the structured "
        "scoring rubric provided by the user. You do not endorse or oppose the paper's conclusions; "
        "you assess its academic quality and provide numerical scores with mandatory comments."
    )
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": content},
    ]

    est_in = estimate_tokens(prompt_text + (paper_text or ""))
    print(f"  Est. input tokens: ~{est_in:,}")
    print("=" * 60)

    if args.dry_run:
        print("\n-- DRY RUN --")
        print(format_cost(model, est_in, max_tokens))
        print("\nPrompt preview (500 chars):")
        print(prompt_text[:500])
        return

    try:
        import openai
    except ImportError:
        sys.exit("ERROR: Run: pip install openai")

    client = openai.OpenAI(api_key=api_key)
    print("\nSending to OpenAI for review...")
    t0 = time.time()

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except openai.AuthenticationError:
        sys.exit("ERROR: Invalid API key.")
    except openai.APIError as e:
        sys.exit(f"ERROR: {e}")

    elapsed = time.time() - t0
    reply = resp.choices[0].message.content
    usage = resp.usage

    # Parse response
    scores, comments = parse_response(reply)
    section_avgs = compute_section_averages(scores)
    total = compute_weighted_total(section_avgs)
    summary = extract_summary_section(reply)

    # Save outputs
    txt_path  = save_text(reply, paper_name, model)
    json_path = save_json(scores, comments, section_avgs, total, paper_name, model, summary)
    csv_path  = save_csv(scores, comments, section_avgs, total, paper_name, model)

    # Print results
    print(f"\nResponse received in {elapsed:.1f}s")
    print("=" * 60)
    print(f"\n  TOTAL WEIGHTED SCORE: {total}/100")
    grade = ("A+" if total>=95 else "A" if total>=90 else "B+" if total>=85
             else "B" if total>=80 else "C+" if total>=75 else "C" if total>=70 else "D")
    print(f"  GRADE: {grade}")
    print()
    print("  Section Averages (0-10):")
    for letter, avg in section_avgs.items():
        flag = "  PASS" if avg >= 7 else "  WEAK" if avg >= 5 else "  FAIL"
        print(f"    {letter}: {avg:5.1f}{flag}")

    # Cost
    in_tok  = usage.prompt_tokens if usage else est_in
    out_tok = usage.completion_tokens if usage else 0
    print(f"\n--- Cost ---\n{format_cost(model, in_tok, out_tok)}")

    # Print revision suggestions
    if summary.get("revision_1") or summary.get("revision_2") or summary.get("revision_3"):
        print("\n--- Top 3 Revisions to Improve Score ---")
        for i, key in enumerate(["revision_1", "revision_2", "revision_3"], 1):
            val = summary.get(key, "")
            if val:
                print(f"  [{i}] {val[:200]}")
    elif summary.get("revision_1"):
        print(f"\n--- Revision ---\n  {summary['revision_1'][:200]}")

    # Print closest representation
    if summary.get("closest_1") or summary.get("closest_2") or summary.get("closest_3"):
        print("\n--- Closest Representations ---")
        for i, key in enumerate(["closest_1", "closest_2", "closest_3"], 1):
            val = summary.get(key, "")
            if val:
                print(f"  [{i}] {val[:180]}")

    # Print key characteristics
    if summary.get("key_characteristics"):
        print("\n--- Key Characteristics ---")
        for line in summary["key_characteristics"].split("\n"):
            line = line.strip()
            if line:
                print(f"  {line[:180]}")

    print(f"\nSaved:")
    print(f"  Full report : {txt_path.name}")
    print(f"  JSON scores : {json_path.name}")
    print(f"  Excel CSV   : {csv_path.name}")
    print("\nOpen the CSV and paste the OPENAI_SCORE column into CDCM_final.xlsx")
    print("=" * 60)


if __name__ == "__main__":
    main()
