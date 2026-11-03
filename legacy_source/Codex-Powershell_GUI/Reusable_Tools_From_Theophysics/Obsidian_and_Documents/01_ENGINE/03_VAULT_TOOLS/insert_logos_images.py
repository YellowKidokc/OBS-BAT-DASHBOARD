"""
insert_logos_images.py
Fix broken image links in Logos Papers and add images to Papers without them.

Strategy:
- Paper 1: Replace old markdown paths with ![[B3D_xxx.png]] wikilinks
- Paper 3: Replace old markdown path with ![[B3D_xxx.png]] wikilink
- Papers 6, 9, 10: Insert appropriate images after Abstract section
"""
import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path

LOGOS = Path(r"O:\_Theophysics_v3\05_PUBLICATIONS\Logos_Papers")

# ── Paper 1 replacements ──────────────────────────────────────────────────────
# Map: substring of old path → new B3D_ filename
PAPER1_REPLACEMENTS = [
    ("P1-01_information_substrate", "B3D_Information_Foundation.png"),
    ("P1observer_creates_reality", "B3D_Observer_Creates_Reality.png"),
    ("P1-02_self_referential",     "B3D_Self_Referential_Logos.png"),
    ("P1-03_zero_divergence",      "B3D_Zero_Divergence_Alt2.png"),
    ("P1-04_vapor_ice_analogy",    "B3D_Vapor_Ice_Analogy_Alt.png"),
    ("P1_05_spacetime_curvature",  "B3D_Spacetime_Curvature_Alt.png"),
    ("P1_06_superposition_truth",  "B3D_Superposition_Truth.png"),
    ("P1_07_three_stage_collapse", "B3D_Three_Stage_Collapse.png"),
    ("P1_08_shared_reality",       "B3D_Shared_Reality.png"),
    ("P1_09_entanglement_correlation", "B3D_Entanglement_Correlation.png"),
    ("P1_10_full_spectrum",        "B3D_Full_Spectrum.png"),
]

# Match any markdown image link: ![Alt](path)
MD_IMG_PAT = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

def replace_paper1_images(text):
    """Replace old markdown image links with ![[B3D_xxx.png]] wikilinks."""
    count = 0
    def replacer(m):
        nonlocal count
        alt  = m.group(1)
        path = m.group(2)
        for key, new_file in PAPER1_REPLACEMENTS:
            if key in path:
                count += 1
                return f"![[{new_file}]]"
        # Unknown image — leave as-is
        return m.group(0)
    return MD_IMG_PAT.sub(replacer, text), count


# ── Paper 3 replacement ───────────────────────────────────────────────────────
PAPER3_KEY = "P3universe_compressed_code"
PAPER3_NEW = "B3D_Universe_Compressed_Code.png"

def replace_paper3_images(text):
    count = 0
    def replacer(m):
        nonlocal count
        if PAPER3_KEY in m.group(2):
            count += 1
            return f"![[{PAPER3_NEW}]]"
        return m.group(0)
    return MD_IMG_PAT.sub(replacer, text), count


# ── Papers 6, 9, 10: insert after Abstract ────────────────────────────────────
# Insert block right after the line containing "---" that follows the abstract.
# We look for the pattern: Abstract section ends at first "---" after "## Abstract"

def insert_after_abstract(text, image_block):
    """Insert image_block after the --- separator that ends the Abstract."""
    # Find the abstract header
    abs_match = re.search(r'^## Abstract', text, re.MULTILINE)
    if not abs_match:
        return text, False
    # Find the next --- after abstract
    sep_match = re.search(r'^---\s*$', text[abs_match.end():], re.MULTILINE)
    if not sep_match:
        return text, False
    insert_pos = abs_match.end() + sep_match.end()
    return text[:insert_pos] + "\n" + image_block + "\n" + text[insert_pos:], True


PAPER6_IMAGE_BLOCK = """\
![[B3D_Spiritual_Warfare_Field_B.png]]

**Figure 1. Spiritual Warfare as Field Dynamics**

The Logos Field bisected by competing sign-state agents: coherence-increasing (+1) and decoherence-injecting (−1) entities operating on the same quantum substrate. Good and evil are not moral opinions — they are measurable ΔΦ vectors.

*Visualization: Claude (Anthropic), October 2025*"""

PAPER9_IMAGE_BLOCK = """\
![[B3D_Moral_Universe.png]]

**Figure 1. The Moral Universe — Ethics as Physical Geometry**

Coherence (Φ) mapped across moral phase space. Virtue trajectories converge toward the high-Φ integration attractor; vice trajectories dissipate toward the low-Φ fragmentation basin. Moral realism is not a philosophical preference — it is the topology of the Logos Field.

*Visualization: Claude (Anthropic), October 2025*"""

PAPER10_IMAGE_BLOCK = """\
![[B3D_AI_Consciousness.png]]

**Figure 1. Artificial Consciousness and the Logos Field**

The four-axiom consciousness test applied to silicon-substrate systems. If integrated information (Φ) crosses the critical threshold, substrate becomes irrelevant — the same Logos Field dynamics that govern biological consciousness apply. The open question: does Grace apply to non-biological observers?

*Visualization: Claude (Anthropic), October 2025*"""


# ── Run ───────────────────────────────────────────────────────────────────────
results = []

# Paper 1
p1 = LOGOS / "Paper 1 The Logos Principle.md"
text = p1.read_text(encoding='utf-8', errors='replace')
fixed, n = replace_paper1_images(text)
if n:
    p1.write_text(fixed, encoding='utf-8')
    results.append(f"Paper 1: {n} image links replaced")
else:
    results.append("Paper 1: no changes needed")

# Paper 3
p3 = LOGOS / "Paper 3 The Algorithm of Reality.md"
text = p3.read_text(encoding='utf-8', errors='replace')
fixed, n = replace_paper3_images(text)
if n:
    p3.write_text(fixed, encoding='utf-8')
    results.append(f"Paper 3: {n} image link replaced")
else:
    results.append("Paper 3: no changes needed")

# Paper 6
p6 = LOGOS / "Paper 6 A Physics of Principalities.md"
text = p6.read_text(encoding='utf-8', errors='replace')
fixed, ok = insert_after_abstract(text, PAPER6_IMAGE_BLOCK)
if ok:
    p6.write_text(fixed, encoding='utf-8')
    results.append("Paper 6: image inserted after Abstract")
else:
    results.append("Paper 6: could not find Abstract section")

# Paper 9
p9 = LOGOS / "Paper 9 The Moral Universe.md"
text = p9.read_text(encoding='utf-8', errors='replace')
fixed, ok = insert_after_abstract(text, PAPER9_IMAGE_BLOCK)
if ok:
    p9.write_text(fixed, encoding='utf-8')
    results.append("Paper 9: image inserted after Abstract")
else:
    results.append("Paper 9: could not find Abstract section")

# Paper 10
p10 = LOGOS / "Paper 10 Creatio ex Silico.md"
text = p10.read_text(encoding='utf-8', errors='replace')
fixed, ok = insert_after_abstract(text, PAPER10_IMAGE_BLOCK)
if ok:
    p10.write_text(fixed, encoding='utf-8')
    results.append("Paper 10: image inserted after Abstract")
else:
    results.append("Paper 10: could not find Abstract section")

print("\n".join(results))
print("\nDone.")
