#!/usr/bin/env python3
"""
tag_stats.py — Tag analytics + KWIC semantic analysis for Theophysics vault

Generates:  O:/_Theophysics_v3/00_AI/TAG_DASHBOARD.md

Usage:
    python tag_stats.py                      # full run (may take 2-3 min on large vault)
    python tag_stats.py --fast               # skip KWIC — summary table only (seconds)
    python tag_stats.py --vault PATH         # override vault root
    python tag_stats.py --keyword grace      # extra KWIC for specific word
    python tag_stats.py --keyword grace --keyword logos  # multiple extras
    python tag_stats.py --window 80          # KWIC context window (default 60)
    python tag_stats.py --top 30             # only detail top N tags by usage

Statistics computed per tag (15):
  1.  file_count         — files with this tag
  2.  paper_count        — subset with paper: frontmatter field
  3.  density_pct        — file_count / total_tagged_files * 100
  4.  top_cotags         — top 5 co-occurring tags
  5.  co_domain_dist     — which taxonomy domains those co-tags come from
  6.  layer_hits         — which of 9 framework layers co-occur with this tag
  7.  orphan_count       — files with matching keywords but tag NOT applied
  8.  keyword_hits       — total keyword matches across corpus
  9.  avg_cotag_count    — avg total tags per file (files that have this tag)
  10. before_top10       — top 10 non-stopwords 60 words BEFORE keyword
  11. after_top10        — top 10 non-stopwords 60 words AFTER keyword
  12. semantic_collocates— words disproportionately more common near keyword (lift)
  13. first_date         — earliest date: frontmatter in files with this tag
  14. series_coverage    — paper series breakdown (JS-Series, Logos, etc.)
  15. co_tag_exclusives  — tags that ONLY appear alongside this one
"""

import sys
import io
import os
import re
import argparse
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
TAXONOMY_FILE = SCRIPT_DIR / "tags_taxonomy.yaml"
DEFAULT_VAULT = Path(r"O:\_Theophysics_v3")
DEFAULT_OUTPUT = DEFAULT_VAULT / "00_AI" / "TAG_DASHBOARD.md"

FRAMEWORK_LAYERS = [
    "formal-proof", "meta-framework", "physics-layer", "jesus-coherence",
    "psychology-layer", "civilization-layer", "scripture-layer",
    "evidence-layer", "rebuttal-layer",
]

SKIP_DIRS = {".git", "__pycache__", "999_IGNORE", "node_modules",
             ".obsidian", "_OFFLOAD", "OFFLOAD"}

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should", "may",
    "might", "shall", "that", "this", "these", "those", "it", "its", "as",
    "by", "with", "from", "into", "through", "during", "before", "after",
    "above", "below", "between", "each", "more", "most", "other", "some",
    "such", "than", "then", "there", "they", "their", "them", "so", "if",
    "when", "where", "which", "who", "how", "what", "why", "not", "no",
    "can", "all", "one", "also", "about", "up", "out", "any", "just",
    "we", "he", "she", "you", "i", "me", "my", "our", "your", "his", "her",
    "s", "t", "ve", "re", "ll", "d", "m", "p", "g", "x", "th",
}


# ── TAXONOMY LOADING ──────────────────────────────────────────────────────────

def load_taxonomy():
    try:
        import yaml
    except ImportError:
        print("PyYAML required:  pip install pyyaml"); sys.exit(1)
    if not TAXONOMY_FILE.exists():
        print(f"Missing: {TAXONOMY_FILE}"); sys.exit(1)
    with open(TAXONOMY_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("domains", {}), data.get("auto_detect", {})


def build_tag_to_domain(domains):
    m = {}
    for domain, cats in domains.items():
        for tags in cats.values():
            for tag in tags:
                m[tag] = domain
    return m


def build_all_taxonomy_tags(domains):
    return {t for cats in domains.values() for tags in cats.values() for t in tags}


# ── VAULT SCANNING (ONE PASS) ─────────────────────────────────────────────────

def parse_frontmatter(content):
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            return content[3:end].strip(), content[end + 4:].lstrip("\n"), True
    return "", content, False


def extract_list_field(fm_block, field):
    """Extract a YAML list field from frontmatter block text."""
    items = []
    in_field = False
    for line in fm_block.split("\n"):
        if re.match(rf"^{field}\s*:", line):
            in_field = True
            inline = re.search(r"\[(.+)\]", line)
            if inline:
                return [v.strip().strip("\"'") for v in inline.group(1).split(",") if v.strip()]
        elif in_field:
            m = re.match(r"^\s+-\s+(.+)", line)
            if m:
                items.append(m.group(1).strip().strip("\"'"))
            elif line.strip() and not line.startswith(" "):
                in_field = False
    return items


def extract_scalar_field(fm_block, field):
    m = re.search(rf"^{field}\s*:\s*(.+)$", fm_block, re.MULTILINE)
    return m.group(1).strip().strip("\"'") if m else ""


def detect_series(path_str):
    p = path_str.lower()
    if "js-series" in p or "/jsc" in p:    return "JS-Series"
    if "logos_papers" in p or "logos papers" in p: return "Logos Papers"
    if "chapter_archive" in p or "chapter archive" in p: return "Chapter Archive"
    if "three_truths" in p or "three truths" in p: return "Three Truths"
    if "canonical" in p:                    return "Canonical KB"
    return "Other"


KWIC_BODY_LIMIT = 30_000   # chars — caps how much body text is tokenized for KWIC
                           # canonical KB Wikipedia articles can be 100-500KB; cap prevents slowdown

def scan_vault(vault_root):
    """One-pass scan. Returns list of paper dicts."""
    papers = []

    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = Path(root) / fname
            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            fm_block, body, had_fm = parse_frontmatter(content)
            if not had_fm:
                continue

            tags = extract_list_field(fm_block, "tags")
            paper_id = extract_scalar_field(fm_block, "paper")
            date_val = extract_scalar_field(fm_block, "date")

            body_lower = body.lower()
            papers.append({
                "path": str(fpath),
                "name": fname,
                "tags": tags,
                "paper": paper_id,
                "date": date_val,
                "series": detect_series(str(fpath)),
                "body": body[:KWIC_BODY_LIMIT],           # capped for KWIC tokenization
                "body_lower": body_lower[:KWIC_BODY_LIMIT], # pre-lowercased for keyword search
                "body_lower_full": body_lower,            # full body for orphan detection
            })

    return papers


# ── PRE-BUILD SHARED INDEXES ──────────────────────────────────────────────────

def tokenize(text):
    return re.findall(r"[a-zA-Z']{2,}", text.lower())


def build_corpus_index(papers):
    """
    Pre-tokenize everything once.
    Returns:
        corpus_tokens  — flat Counter of all tokens
        paper_tokens   — list of (paper, [tokens]) pairs
        corpus_total   — total token count (non-stopword)
    """
    print("  Building corpus index (one-time)...")
    corpus_freq = Counter()
    paper_tokens = []
    for paper in papers:
        toks = [w for w in tokenize(paper["body"]) if w not in STOPWORDS and len(w) > 2]
        corpus_freq.update(toks)
        paper_tokens.append(toks)
    corpus_total = sum(corpus_freq.values())
    return corpus_freq, paper_tokens, corpus_total


def build_keyword_index(keyword, paper_tokens):
    """
    Build before/after word lists for a keyword across all papers.
    Returns before_counter, after_counter, hit_count, snippet positions.
    """
    kw_lower = keyword.lower()
    before_words = []
    after_words = []
    hits = 0
    window = 60  # set at call site if needed

    for toks in paper_tokens:
        for i, w in enumerate(toks):
            if kw_lower in w:
                hits += 1
                b = toks[max(0, i - window): i]
                a = toks[i + 1: i + 1 + window]
                before_words.extend(b)
                after_words.extend(a)

    return Counter(before_words), Counter(after_words), hits


def kwic_snippets(keyword, papers, max_snippets=5):
    """Get raw text snippets (not tokenized) for readability."""
    kw_lower = keyword.lower()
    snippets = []
    for paper in papers:
        if kw_lower not in paper["body_lower"]:
            continue
        words = paper["body"].split()
        for j, w in enumerate(words):
            if kw_lower in w.lower():
                start = max(0, j - 8)
                end = min(len(words), j + 9)
                snip = " ".join(words[start:end])
                snippets.append(f"[{paper['name']}] …{snip}…")
                break  # one per paper
        if len(snippets) >= max_snippets:
            break
    return snippets


# ── STATISTICS ENGINE ─────────────────────────────────────────────────────────

def compute_all_stats(papers, paper_tokens, corpus_freq, corpus_total,
                      domains, auto_kw, tag_to_domain, window=60, skip_kwic=False,
                      kwic_tag_limit=30):
    """
    Compute all statistics in an efficient multi-pass structure.
    Returns dict: tag → stats dict.
    """
    total_files = len(papers)
    all_taxonomy_tags = build_all_taxonomy_tags(domains)

    # --- Pass 1: per-tag file sets + co-tag counts ---
    print("  Pass 1: tag file grouping...")
    tag_papers = defaultdict(list)  # tag → [paper]
    for paper in papers:
        for tag in paper["tags"]:
            tag_papers[tag].append(paper)

    # --- Pass 2: orphan detection (keyword search on pre-lowercased bodies) ---
    print("  Pass 2: orphan detection...")
    tag_orphans = {}
    for tag in all_taxonomy_tags:
        kw_list = auto_kw.get(tag, [])
        if not isinstance(kw_list, list) or not kw_list:
            tag_orphans[tag] = 0
            continue
        count = 0
        for paper in papers:
            if tag not in paper["tags"]:
                if any(kw.lower() in paper["body_lower_full"] for kw in kw_list):
                    count += 1
        tag_orphans[tag] = count

    # --- Pass 3: keyword hit counts ---
    print("  Pass 3: keyword hit counts...")
    tag_kw_hits = {}
    for tag in all_taxonomy_tags:
        kw_list = auto_kw.get(tag, [])
        if not isinstance(kw_list, list) or not kw_list:
            tag_kw_hits[tag] = 0
            continue
        hits = 0
        for paper in papers:
            for kw in kw_list:
                hits += paper["body_lower_full"].count(kw.lower())
        tag_kw_hits[tag] = hits

    # --- Pass 4: co-tag exclusives ---
    print("  Pass 4: co-tag exclusives...")
    tag_file_sets = {tag: set(p["path"] for p in plist)
                     for tag, plist in tag_papers.items()}

    # --- Build stats per tag ---
    print("  Assembling per-tag stats...")
    stats = {}
    target_tags = all_taxonomy_tags | set(tag_papers.keys())

    # Determine which tags to run KWIC for (expensive — cap to top N by usage)
    usage_counter = Counter(t for p in papers for t in p["tags"])
    kwic_eligible = {t for t, _ in usage_counter.most_common(kwic_tag_limit)}

    for tag in sorted(target_tags):
        tagged = tag_papers.get(tag, [])
        file_count = len(tagged)
        paper_count = sum(1 for p in tagged if p["paper"])
        density = round(file_count / total_files * 100, 2) if total_files else 0

        # Co-tags
        cotag_c = Counter()
        for p in tagged:
            for t in p["tags"]:
                if t != tag:
                    cotag_c[t] += 1
        top_cotags = cotag_c.most_common(5)

        # Co-domain distribution
        co_domain = Counter(tag_to_domain.get(t, "Unknown") for t, _ in top_cotags)

        # Framework layer hits
        layer_hits = [L for L in FRAMEWORK_LAYERS
                      if any(L in p["tags"] for p in tagged)]

        # Avg co-tag count
        avg_cotag = round(sum(len(p["tags"]) for p in tagged) / file_count, 1) if file_count else 0

        # Dates
        dates = [p["date"] for p in tagged if p["date"] and len(p["date"]) >= 4]
        first_date = min(dates) if dates else "—"

        # Series breakdown
        series_c = Counter(p["series"] for p in tagged)

        # Co-tag exclusives
        tagged_set = tag_file_sets.get(tag, set())
        exclusives = [
            t for t, paths in tag_file_sets.items()
            if t != tag and paths and paths.issubset(tagged_set) and len(paths) >= 2
        ][:5]

        # KWIC (skip in --fast mode)
        primary_kw = None
        before_top = after_top = collocates = snippets_list = []
        kwic_hits = 0

        if not skip_kwic and tag in kwic_eligible:
            kw_list = auto_kw.get(tag, [])
            primary_kw = (kw_list[0] if isinstance(kw_list, list) and kw_list
                          else tag.replace("-", " "))

            before_c, after_c, kwic_hits = build_keyword_index(primary_kw, paper_tokens)
            before_top = [(w, n) for w, n in before_c.most_common(12)
                          if w not in STOPWORDS][:10]
            after_top = [(w, n) for w, n in after_c.most_common(12)
                         if w not in STOPWORDS][:10]

            # Semantic collocates (lift)
            combined = before_c + after_c
            near_total = sum(combined.values())
            if near_total > 0 and corpus_total > 0:
                lifts = []
                for word, count in combined.items():
                    if word in STOPWORDS or len(word) < 3:
                        continue
                    near_rate = count / near_total
                    corp_rate = corpus_freq.get(word, 1) / corpus_total
                    lift = near_rate / corp_rate
                    if count >= 2:
                        lifts.append((word, round(lift, 2), count))
                lifts.sort(key=lambda x: -x[1])
                collocates = lifts[:12]

            snippets_list = kwic_snippets(primary_kw, papers)

        stats[tag] = {
            "file_count":        file_count,
            "paper_count":       paper_count,
            "density_pct":       density,
            "top_cotags":        top_cotags,
            "co_domain_dist":    dict(co_domain),
            "layer_hits":        layer_hits,
            "orphan_count":      tag_orphans.get(tag, 0),
            "keyword_hits":      tag_kw_hits.get(tag, 0),
            "avg_cotag_count":   avg_cotag,
            "before_top10":      before_top,
            "after_top10":       after_top,
            "semantic_collocates": collocates,
            "first_date":        first_date,
            "series_coverage":   dict(series_c),
            "co_tag_exclusives": exclusives,
            "kwic_keyword":      primary_kw,
            "kwic_total_hits":   kwic_hits,
            "kwic_snippets":     snippets_list,
        }

    return stats


# ── DASHBOARD GENERATION ──────────────────────────────────────────────────────

def md_table(headers, rows):
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def generate_dashboard(stats, tag_to_domain, papers, vault_root,
                       extra_kwic=None, paper_tokens=None, corpus_freq=None,
                       corpus_total=0, window=60, skip_kwic=False):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_files = len(papers)
    total_tagged = sum(1 for p in papers if p["tags"])
    all_used = Counter(t for p in papers for t in p["tags"])

    L = []
    def a(s=""): L.append(s)

    # Header
    a("---")
    a("title: Tag Analytics Dashboard")
    a(f"generated: {now}")
    a("tags: [dashboard, analytics]")
    a("---")
    a()
    a("# Tag Analytics Dashboard")
    a(f"*Generated: {now}*")
    a()

    # Corpus overview
    a("## Corpus Overview")
    a()
    rows = [
        ["Total .md files scanned", total_files],
        ["Files with frontmatter tags", total_tagged],
        ["Unique tags in use", len(all_used)],
        ["Total tag assignments", sum(all_used.values())],
        ["Vault root", f"`{vault_root}`"],
        ["KWIC window", f"±{window} words"],
    ]
    a(md_table(["Stat", "Value"], rows))
    a()

    # Top tags
    a("### Top 25 Tags by Usage")
    a()
    rows = []
    for rank, (tag, count) in enumerate(all_used.most_common(25), 1):
        domain = tag_to_domain.get(tag, "—")
        s = stats.get(tag, {})
        pct = s.get("density_pct", "—")
        rows.append([rank, f"`{tag}`", count, f"{pct}%", domain])
    a(md_table(["Rank", "Tag", "Files", "Density", "Domain"], rows))
    a()

    # Live Dataview
    a("## Live Queries (Dataview)")
    a()
    a("### Most-tagged files")
    a("```dataview")
    a("TABLE length(tags) as \"Tags\", file.mtime as \"Modified\"")
    a("FROM \"\"")
    a("WHERE tags AND length(tags) > 0")
    a("SORT length(tags) DESC")
    a("LIMIT 25")
    a("```")
    a()
    a("### Files with images")
    a("```dataview")
    a("TABLE images, length(images) as \"Images\"")
    a("FROM \"\"")
    a("WHERE images AND length(images) > 0")
    a("SORT length(images) DESC")
    a("```")
    a()
    a("### Recently tagged")
    a("```dataview")
    a("TABLE tags, file.mtime as \"Modified\"")
    a("FROM \"\"")
    a("WHERE tags AND length(tags) > 0")
    a("SORT file.mtime DESC")
    a("LIMIT 20")
    a("```")
    a()

    # Full summary table
    a("## All Tags — Summary Table")
    a()
    a("*Sorted by file count. Orphans = files with matching keywords but tag not applied.*")
    a()
    rows = []
    for tag, s in sorted(stats.items(), key=lambda x: -x[1]["file_count"]):
        top_co = s["top_cotags"][0][0] if s["top_cotags"] else "—"
        rows.append([
            f"`{tag}`",
            s["file_count"],
            s["paper_count"],
            f"{s['density_pct']}%",
            s["orphan_count"],
            s["keyword_hits"],
            f"`{top_co}`",
            s["first_date"],
        ])
    a(md_table(
        ["Tag", "Files", "Papers", "Density", "Orphans", "Kw Hits", "Top Co-Tag", "First Date"],
        rows
    ))
    a()

    if skip_kwic:
        a("> *KWIC analysis skipped (--fast mode). Re-run without --fast for semantic context.*")
        a()

    # Per-tag detail
    a("---")
    a()
    a("## Per-Tag Detail")
    a()

    for tag, s in sorted(stats.items(), key=lambda x: -x[1]["file_count"]):
        if s["file_count"] == 0:
            continue
        domain = tag_to_domain.get(tag, "Unknown")
        a(f"### `{tag}`")
        a(f"*Domain: {domain}*")
        a()

        # Core stats
        core_rows = [
            ["1. File count",               s["file_count"]],
            ["2. Paper count (paper: field)",s["paper_count"]],
            ["3. Density",                  f"{s['density_pct']}%"],
            ["4. Avg tags per file",         s["avg_cotag_count"]],
            ["7. Orphan candidates",         s["orphan_count"]],
            ["8. Keyword hits in corpus",    s["keyword_hits"]],
            ["13. Earliest dated file",      s["first_date"]],
        ]
        a(md_table(["Stat", "Value"], core_rows))
        a()

        # Co-tags
        if s["top_cotags"]:
            a("**Top co-occurring tags:**")
            a()
            a(md_table(["Tag", "Shared Files"],
                       [[f"`{t}`", n] for t, n in s["top_cotags"]]))
            a()

        # Layer coverage
        if s["layer_hits"]:
            a(f"**Framework layers:** {', '.join(f'`{L}`' for L in s['layer_hits'])}")
            a()

        # Series
        if s["series_coverage"]:
            parts = [f"{k}: {v}" for k, v in sorted(s["series_coverage"].items())]
            a(f"**Series:** {' | '.join(parts)}")
            a()

        # Exclusives
        if s["co_tag_exclusives"]:
            a(f"**Tightly coupled:** {', '.join(f'`{t}`' for t in s['co_tag_exclusives'])}")
            a()

        # KWIC
        if not skip_kwic and s["kwic_keyword"]:
            kw = s["kwic_keyword"]
            hits = s["kwic_total_hits"]
            a(f"**KWIC** — keyword: *\"{kw}\"*, {hits} hits, ±{window} words")
            a()

            if s["before_top10"]:
                b_str = " → ".join(f"`{w}`({n})" for w, n in s["before_top10"][:8])
                a(f"*Before:* {b_str}")
                a()
            if s["after_top10"]:
                a_str = " → ".join(f"`{w}`({n})" for w, n in s["after_top10"][:8])
                a(f"*After:* {a_str}")
                a()

            if s["semantic_collocates"]:
                a("**Semantic collocates (lift ratio vs. corpus):**")
                a()
                a(md_table(["Word", "Lift", "Hits"],
                           [[f"`{w}`", f"{lift}x", cnt]
                            for w, lift, cnt in s["semantic_collocates"][:10]]))
                a()

            if s["kwic_snippets"]:
                a("<details>")
                a(f"<summary>Example occurrences ({len(s['kwic_snippets'])} shown)</summary>")
                a()
                for snip in s["kwic_snippets"]:
                    a(f"> {snip}")
                    a()
                a("</details>")
                a()

        # Dataview query
        a("```dataview")
        a(f"LIST file.mtime")
        a(f"FROM \"\"")
        a(f"WHERE contains(tags, \"{tag}\")")
        a(f"SORT file.mtime DESC")
        a("```")
        a()
        a("---")
        a()

    # Extra KWIC keywords
    if extra_kwic:
        a("## Custom KWIC Analysis")
        a()
        for kd in extra_kwic:
            kw = kd["keyword"]
            a(f"### Keyword: \"{kw}\"")
            a(f"*{kd['hits']} corpus hits, ±{window} words*")
            a()
            if kd["before"]:
                a(f"**Before:** {' → '.join(f'`{w}`({n})' for w, n in kd['before'][:8])}")
                a()
            if kd["after"]:
                a(f"**After:** {' → '.join(f'`{w}`({n})' for w, n in kd['after'][:8])}")
                a()
            if kd["collocates"]:
                a("**Semantic collocates:**")
                a()
                a(md_table(["Word", "Lift", "Hits"],
                           [[f"`{w}`", f"{lift}x", cnt]
                            for w, lift, cnt in kd["collocates"][:12]]))
                a()
            if kd["snippets"]:
                a("<details><summary>Examples</summary>")
                a()
                for s in kd["snippets"]:
                    a(f"> {s}")
                    a()
                a("</details>")
                a()

    return "\n".join(L)


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Theophysics tag analytics")
    parser.add_argument("--vault",   default=str(DEFAULT_VAULT))
    parser.add_argument("--output",  default=str(DEFAULT_OUTPUT))
    parser.add_argument("--keyword", action="append", default=[],
                        help="Extra keyword(s) for custom KWIC (repeatable)")
    parser.add_argument("--window",  type=int, default=60)
    parser.add_argument("--top",     type=int, default=None,
                        help="Only show detail for top N tags by usage")
    parser.add_argument("--fast",    action="store_true",
                        help="Skip KWIC — summary table only (much faster)")
    args = parser.parse_args()

    vault_root = Path(args.vault)
    output_path = Path(args.output)

    print(f"[1/5] Loading taxonomy from {TAXONOMY_FILE.name}")
    domains, auto_kw = load_taxonomy()
    tag_to_domain = build_tag_to_domain(domains)

    print(f"[2/5] Scanning vault: {vault_root}")
    papers = scan_vault(vault_root)
    print(f"      {len(papers)} files with frontmatter")

    corpus_freq, paper_tokens, corpus_total = None, None, 0
    if not args.fast:
        print("[3/5] Building corpus token index...")
        corpus_freq, paper_tokens, corpus_total = build_corpus_index(papers)
        print(f"      {corpus_total:,} non-stopword tokens indexed")
    else:
        print("[3/5] Skipping corpus index (--fast mode)")

    # KWIC tag limit: use --top if given, else default 30
    kwic_limit = args.top if args.top else 30

    print("[4/5] Computing statistics...")
    stats = compute_all_stats(
        papers, paper_tokens, corpus_freq, corpus_total,
        domains, auto_kw, tag_to_domain,
        window=args.window, skip_kwic=args.fast,
        kwic_tag_limit=kwic_limit,
    )

    # Extra KWIC keywords
    extra_kwic = []
    for kw in args.keyword:
        print(f"      Extra KWIC: '{kw}'")
        before_c, after_c, hits = build_keyword_index(kw, paper_tokens)
        combined = before_c + after_c
        near_total = sum(combined.values())
        lifts = []
        if near_total > 0 and corpus_total > 0:
            for word, count in combined.items():
                if word in STOPWORDS or len(word) < 3:
                    continue
                lift = (count / near_total) / (corpus_freq.get(word, 1) / corpus_total)
                if count >= 2:
                    lifts.append((word, round(lift, 2), count))
            lifts.sort(key=lambda x: -x[1])
        extra_kwic.append({
            "keyword":   kw,
            "hits":      hits,
            "before":    [(w, n) for w, n in before_c.most_common(10) if w not in STOPWORDS],
            "after":     [(w, n) for w, n in after_c.most_common(10) if w not in STOPWORDS],
            "collocates": lifts[:12],
            "snippets":  kwic_snippets(kw, papers),
        })

    # If --top, trim detail section
    if args.top:
        usage = Counter(t for p in papers for t in p["tags"])
        top_tags = {t for t, _ in usage.most_common(args.top)}
        stats = {t: s for t, s in stats.items() if t in top_tags}

    print("[5/5] Generating dashboard...")
    content = generate_dashboard(
        stats, tag_to_domain, papers, vault_root,
        extra_kwic=extra_kwic,
        paper_tokens=paper_tokens,
        corpus_freq=corpus_freq,
        corpus_total=corpus_total,
        window=args.window,
        skip_kwic=args.fast,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print()
    print(f"Dashboard written: {output_path}")
    print(f"  Tags analyzed:   {len(stats)}")
    print(f"  Files scanned:   {len(papers)}")
    print(f"  Output size:     {len(content) // 1024} KB")


if __name__ == "__main__":
    main()
