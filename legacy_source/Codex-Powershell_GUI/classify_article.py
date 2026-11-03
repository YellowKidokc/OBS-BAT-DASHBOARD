"""
Article Classifier — Top Bar Scoring
POF 2828 | faiththruphysics.com

Scans an article (HTML or MD) and scores it against the 20 taxonomy categories.
Outputs JSON matching the meta.json classification format.
Runs locally — no API calls, no cost.

Usage:
  python classify_article.py <path_to_article>
  python classify_article.py --gui
"""
import os, sys, re, json
from collections import Counter

# The 20 categories with their keyword signatures
TAXONOMY = {
    "physics": {
        "color": "#4a9eff",
        "keywords": ["force", "gravity", "mass", "energy", "momentum", "wave", "particle",
                     "quantum", "relativity", "thermodynamic", "entropy", "lagrangian",
                     "equation", "field", "spacetime", "photon", "electron", "neutrino",
                     "conservation", "symmetry", "newton", "einstein", "planck", "hamiltonian",
                     "gauge", "tensor", "metric", "curvature", "acceleration", "velocity"]
    },
    "theology": {
        "color": "#c87050",
        "keywords": ["god", "christ", "jesus", "scripture", "bible", "gospel", "church",
                     "faith", "prayer", "salvation", "sin", "redemption", "holy spirit",
                     "trinity", "resurrection", "baptism", "communion", "covenant",
                     "psalm", "prophet", "apostle", "genesis", "revelation", "sermon",
                     "doctrine", "orthodox", "protestant", "catholic", "worship"]
    },
    "math": {
        "color": "#a855f7",
        "keywords": ["theorem", "proof", "axiom", "lemma", "corollary", "derivation",
                     "lean", "lean4", "formal", "verify", "compile", "sorry",
                     "isomorphism", "homomorphism", "mapping", "bijection", "function",
                     "variable", "integral", "differential", "sigma", "delta", "lambda"]
    },
    "info-theory": {
        "color": "#3bb39a",
        "keywords": ["shannon", "information", "entropy", "signal", "noise", "channel",
                     "bandwidth", "encoding", "decoding", "bit", "byte", "capacity",
                     "compression", "redundancy", "logos", "data", "transmission"]
    },
    "consciousness": {
        "color": "#f59e0b",
        "keywords": ["consciousness", "observer", "measurement", "awareness", "qualia",
                     "hard problem", "subjective", "perception", "mind", "brain",
                     "neural", "cognitive", "attention", "experience", "phenomenal",
                     "von neumann", "wigner", "collapse", "decoherence"]
    },
    "trinity": {
        "color": "#d4af37",
        "keywords": ["trinity", "father", "son", "spirit", "triune", "triadic",
                     "three persons", "perichoresis", "homoousios", "nicene",
                     "three-fold", "threefold", "three observers"]
    },
    "grace": {
        "color": "#22c55e",
        "keywords": ["grace", "salvation", "atonement", "cross", "restoration",
                     "forgiveness", "mercy", "redemption", "justify", "sanctif",
                     "regenerat", "born again", "new creation", "reconcil", "charis"]
    },
    "entropy": {
        "color": "#ef4444",
        "keywords": ["entropy", "decay", "disorder", "decoherence", "second law",
                     "degradation", "collapse", "fragmentation", "decline", "erosion",
                     "corruption", "fall", "deteriorat", "dissipat"]
    },
    "justice": {
        "color": "#e879a0",
        "keywords": ["justice", "mercy", "judgment", "court", "law", "penalty",
                     "substitution", "helmholtz", "free energy", "offense", "verdict",
                     "punishment", "fairness", "equity", "rights"]
    },
    "free-will": {
        "color": "#8b5cf6",
        "keywords": ["free will", "choice", "determinism", "agency", "volition",
                     "libertarian", "compatibilist", "decision", "autonomy", "freedom",
                     "moral agent", "responsibility", "intention"]
    },
    "adversary": {
        "color": "#6b7280",
        "keywords": ["satan", "adversary", "enemy", "evil", "demonic", "spiritual warfare",
                     "temptat", "deception", "anti-", "counterfeit", "opposition",
                     "attack", "darkness", "principalit"]
    },
    "genesis": {
        "color": "#92400e",
        "keywords": ["genesis", "creation", "garden", "eden", "adam", "eve", "fall",
                     "original sin", "tree of knowledge", "flood", "noah", "babel",
                     "patriarch", "abraham", "covenant"]
    },
    "ten-laws": {
        "color": "#d4af37",
        "keywords": ["ten laws", "law 1", "law 2", "law 3", "law 4", "law 5",
                     "law 6", "law 7", "law 8", "law 9", "law 10",
                     "symmetry pair", "strong force", "weak force", "electromagnetic"]
    },
    "master-eq": {
        "color": "#f0c659",
        "keywords": ["master equation", "chi field", "product integral", "ten variables",
                     "chi =", "χ =", "dxdydt", "product structure", "coherence factor"]
    },
    "method": {
        "color": "#9a7c3a",
        "keywords": ["7q", "seven question", "bilateral audit", "falsif", "kill condition",
                     "methodology", "epistemol", "scientific method", "hypothesis",
                     "prediction", "test", "replicate", "peer review"]
    },
    "evidence": {
        "color": "#2dd4bf",
        "keywords": ["pear", "gcp", "global consciousness", "sigma", "p-value",
                     "correlation", "regression", "dataset", "empirical", "experiment",
                     "statistical", "confidence interval", "effect size", "sample size",
                     "significance", "r-squared", "chi-squared"]
    },
    "society": {
        "color": "#64748b",
        "keywords": ["moral decline", "civilization", "amish", "america", "culture",
                     "politic", "government", "institution", "trust", "civic",
                     "communit", "social", "historical", "1968", "phase transition"]
    },
    "cross-domain": {
        "color": "#e2725b",
        "keywords": ["cross-domain", "isomorphism", "mapping", "convergence", "bridge",
                     "dual projection", "structural", "parallel", "analogy",
                     "same equation", "both domains", "identical structure"]
    },
    "story": {
        "color": "#f5d0a9",
        "keywords": ["my story", "testimony", "personal", "journey", "i remember",
                     "growing up", "fence", "oklahoma", "david lowe", "when i was"]
    },
    "ai": {
        "color": "#60a5fa",
        "keywords": ["ai", "artificial intelligence", "machine learning", "llm",
                     "claude", "gemini", "gpt", "convergence", "david effect",
                     "multi-ai", "preference engine", "collaborat"]
    }
}

def extract_text(filepath):
    """Extract readable text from HTML or Markdown."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if filepath.endswith('.html'):
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<[^>]+>', ' ', content)
        content = re.sub(r'&[a-z]+;', ' ', content)
    return content.lower()

def classify(text):
    """Score text against all 20 categories. Returns sorted list of {tag, pct, color}."""
    scores = {}
    for tag, info in TAXONOMY.items():
        count = 0
        for kw in info["keywords"]:
            count += len(re.findall(r'\b' + re.escape(kw), text))
        scores[tag] = count
    total = sum(scores.values())
    if total == 0:
        return []
    results = []
    for tag, count in scores.items():
        pct = round(count / total * 100)
        if pct >= 3:  # only include categories at 3% or above
            results.append({"tag": tag, "pct": pct, "color": TAXONOMY[tag]["color"]})
    results.sort(key=lambda x: x["pct"], reverse=True)
    # Normalize to 100%
    shown_total = sum(r["pct"] for r in results)
    if shown_total > 0 and shown_total != 100:
        factor = 100 / shown_total
        for r in results:
            r["pct"] = round(r["pct"] * factor)
        diff = 100 - sum(r["pct"] for r in results)
        if diff != 0 and results:
            results[0]["pct"] += diff
    return results

def classify_file(filepath):
    """Classify a file and return results."""
    text = extract_text(filepath)
    return classify(text)

def print_results(results, filepath):
    """Print classification results."""
    print(f"\n{'='*60}")
    print(f"  CLASSIFICATION: {os.path.basename(filepath)}")
    print(f"{'='*60}")
    for r in results:
        bar = "#" * (r["pct"] // 2)
        print(f"  {r['tag']:.<20} {r['pct']:>3}%  {bar}")
    print(f"{'='*60}")
    print(f"\n  JSON for meta.json:")
    print(f"  {json.dumps(results, indent=2)}")

def update_meta_json(meta_path, results):
    """Update an existing meta.json with classification results."""
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            meta = json.load(f)
    else:
        meta = {}
    meta["classification"] = results
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    print(f"\n  Updated: {meta_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python classify_article.py <article.html|article.md>")
        print("       python classify_article.py <article> --update-meta <meta.json>")
        sys.exit(1)
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)
    results = classify_file(filepath)
    print_results(results, filepath)
    if '--update-meta' in sys.argv:
        idx = sys.argv.index('--update-meta')
        if idx + 1 < len(sys.argv):
            update_meta_json(sys.argv[idx + 1], results)
