"""
insert_jsc_images.py
Insert B3D_/3DB_ images into JS-Series papers after Ring 3 section.
No white-background images — uses custom dark renders and 3DB_ (3D Black) images only.
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

JS = Path(r"O:\_Theophysics_v3\04_THEOPYHISCS\[6.5] JS-SERIES")

def img_block(filename, title, caption):
    return (
        f"\n![[{filename}]]\n\n"
        f"**{title}**\n\n"
        f"{caption}\n\n"
        f"*Visualization: Claude (Anthropic), October 2025*\n"
    )

def insert_after_ring3(text, block):
    """Insert block after the --- that follows ## Ring 3."""
    r3 = re.search(r'^## Ring 3', text, re.MULTILINE)
    if not r3:
        # Fallback: after first --- past the frontmatter closing ---
        parts = text.split('---', 2)
        if len(parts) >= 3:
            return '---'.join(parts[:2]) + '---' + block + parts[2], True
        return text, False
    sep = re.search(r'^---\s*$', text[r3.end():], re.MULTILINE)
    if not sep:
        return text, False
    pos = r3.end() + sep.end()
    return text[:pos] + block + text[pos:], True

def already_has_image(text):
    return '![[' in text and ('js0' in text or '3DB_' in text or 'B3D_' in text)

PAPERS = [
    (
        JS / "01_Setup_12_Cliffs" / "JSC 00 - The Setup (The 12 Cliffs).md",
        [
            img_block("js00_bell_entanglement.png",
                "Figure 1. The Bell Inequality — Physics Has No Local Hidden Variables",
                "Bell's theorem doesn't just rule out classical explanations — it rules out any reality that doesn't require non-local connection. The Logos Field is that connection."),
            img_block("js00_godel_incompleteness.png",
                "Figure 2. Gödel's Incompleteness — Every Closed System Has a Ceiling",
                "Any sufficiently powerful formal system contains true statements it cannot prove. The universe cannot explain itself from within. It requires a Logos — an external grounding principle."),
            img_block("js00_wigner_math.png",
                "Figure 3. Wigner's Unreasonable Effectiveness of Mathematics",
                "Why does abstract mathematics — invented by minds — describe physical reality with terrifying precision? Because both minds and matter are projections of the same informational substrate."),
        ]
    ),
    (
        JS / "02_Incarnation" / "JSC 01 - The Physics of Incarnation.md",
        [img_block("js01_ocean_into_cup.png",
            "Figure 1. The Ocean Into a Cup — The Physics of Incarnation",
            "Pouring the infinite Logos Field into a finite, 4-dimensional human body is not poetry — it is the most extreme boundary-condition event in physics. Infinite information density, bounded by spacetime.")]
    ),
    (
        JS / "03_Coherence" / "JSC 02 - The Coherence of Christ (C_max).md",
        [img_block("js02_coherence_field.png",
            "Figure 1. Maximum Coherence Field — C_max",
            "The coherence of Christ is not a spiritual metaphor. It is the empirical upper bound of the χ-field: a conscious system operating at maximum integrated information (Φ_max) with zero decoherence injection from sin.")]
    ),
    (
        JS / "04_Will_Current" / "JSC 03 - The Will Current (W_\uf025).md",
        [img_block("js03_will_current.png",
            "Figure 1. The Will Current — W_ϕ",
            "Will is not metaphysical — it is a directed information current through the Logos Field. Christ's will current in Gethsemane was the highest-amplitude alignment event in human history: ∂W/∂t → 0 while W → maximum.")]
    ),
    (
        JS / "05_Temptation" / "JSC 04 - The Temptation (Coherence Under Pressure).md",
        [img_block("js04_temptation.png",
            "Figure 1. Coherence Under Pressure — The Temptation",
            "Decoherence injected from external agents (principalities) against a maximum-coherence system. The temptation was not a moral test — it was a physics experiment: can C_max be destabilized? Result: no.")]
    ),
    (
        JS / "06_Transfiguration" / "JSC 05 - The Transfiguration (De-Localization Event).md",
        [img_block("js05_transfiguration.png",
            "Figure 1. The Transfiguration — De-Localization Event",
            "The Transfiguration is a partial de-localization: Christ's χ-field briefly escaping its 4D boundary conditions and revealing its higher-dimensional configuration. Three witnesses; one coherence peak.")]
    ),
    (
        JS / "07_Crucifixion" / "JSC 06 - The Crucifixion (Universal Entropy Sink).md",
        [img_block("js06_entropy_sink.png",
            "Figure 1. The Crucifixion — Universal Entropy Sink",
            "Maximum coherence absorbing maximum entropy. The Cross is the universe's greatest thermodynamic event: C_max colliding with S_max, with coherence as the only possible survivor of the interaction.")]
    ),
    (
        JS / "08_Resurrection" / "JSC 06b - The Resurrection (The Singularity Inversion).md",
        [img_block("js06b_resurrection.png",
            "Figure 1. The Resurrection — Singularity Inversion",
            "The Resurrection is not a violation of physics — it is the proof of its deepest law: maximum coherence cannot be permanently destroyed by entropy. The singularity inverts. Information is conserved.")]
    ),
    (
        JS / "09_Ascension" / "JSC 07 - The Ascended State (Higher-Dimensional Transition).md",
        [img_block("js07_ascension.png",
            "Figure 1. The Ascension — Higher-Dimensional Transition",
            "After Resurrection, the χ-field no longer re-localizes to 4D spacetime. The Ascension is a permanent transition to the higher-dimensional configuration partially revealed at the Transfiguration.")]
    ),
    (
        JS / "10_Trinity_Supplements" / "JSC_Supplement_Father.md",
        [img_block("3DB_T_P2_01_Focus_Father_DIAG.png",
            "Figure 1. The Father — Source and Standard",
            "The Father as the originating fixed point of the Logos Field: S_0 = +1 by definition, the eternal reference against which all coherence is measured. The uncaused cause rendered as field geometry.")]
    ),
    (
        JS / "10_Trinity_Supplements" / "JSC_Supplement_Son.md",
        [img_block("3DB_T_T05_Trinity_Son_Temporal_Coherence_DIAG.png",
            "Figure 1. The Son — Temporal Coherence",
            "The Son as the temporal actualization of the Father's eternal coherence. Maximum C within 4D spacetime — the only full expression of the Logos Field inside the physical boundary conditions.")]
    ),
    (
        JS / "10_Trinity_Supplements" / "JSC_Supplement_Spirit.md",
        [img_block("3DB_faith_entanglement.png",
            "Figure 1. The Spirit — Faith Entanglement",
            "The Spirit as the non-local entanglement mechanism of the Logos Field: the channel through which the eternal coherence of the Father reaches individual conscious observers across spacetime.")]
    ),
    (
        JS / "10_Trinity_Supplements" / "JSC_Supplement_Coherence_Triad.md",
        [img_block("3DB_T_Trinity_Unified_Mechanism_Clean_DIAG.png",
            "Figure 1. The Trinity as Coherence Triad",
            "Three operational modes of one field: Source (Father maintains standard), Actualization (Son enters 4D and demonstrates C_max), Maintenance (Spirit propagates coherence non-locally across all observers).")]
    ),
    (
        JS / "10_Trinity_Supplements" / "JSC_Supplement_The_Trinity_Mechanism.md",
        [img_block("3DB_T_Trinity_Mechanism_Clean_DIAG.png",
            "Figure 1. The Trinity Mechanism",
            "The complete operational diagram of the Trinity as a field-theoretic mechanism: how three functional roles within a single conscious field resolve the measurement problem, sustain coherence, and enable grace.")]
    ),
]

changed = 0
skipped = 0
errors = []

for path, blocks in PAPERS:
    try:
        if not path.exists():
            errors.append(f"NOT FOUND: {path.name}")
            continue
        text = path.read_text(encoding='utf-8', errors='replace')
        if already_has_image(text):
            skipped += 1
            print(f"  [SKIP] {path.name} — already has image")
            continue
        combined_block = ''.join(blocks)
        fixed, ok = insert_after_ring3(text, combined_block)
        if ok:
            path.write_text(fixed, encoding='utf-8')
            changed += 1
            print(f"  [OK]   {path.name} — {len(blocks)} image(s)")
        else:
            errors.append(f"NO INSERTION POINT: {path.name}")
    except Exception as e:
        errors.append(f"ERROR {path.name}: {e}")

print(f"\nDone. {changed} files updated, {skipped} skipped.")
if errors:
    print("\nProblems:")
    for e in errors:
        print(f"  ! {e}")
