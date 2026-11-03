#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_ring3_links.py
Execute all Ring 3 additions planned by vault-link agents for JS-SERIES and Layer C.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import re
from pathlib import Path

VAULT = Path("O:/_Theophysics_v3")
modified = 0
errors = 0

def append_ring3(fp: Path, new_links: list[str]):
    """Append new links to existing Ring 3 section, avoiding duplicates."""
    global modified, errors
    try:
        text = fp.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  ERROR reading {fp.name}: {e}")
        errors += 1
        return

    if 'ckg_evaluation' not in text:
        print(f"  SKIP (no CKG): {fp.name}")
        return

    # Find existing Ring 3 section end
    r3_pattern = re.compile(r'(## Ring 3[^\n]*\n)(.*?)(?=\n## |\n---|\Z)', re.DOTALL)
    match = r3_pattern.search(text)

    # Filter out links already present
    to_add = []
    for link in new_links:
        # Extract path from wikilink for dedup check
        path_match = re.search(r'\[\[([^\]|]+)', link)
        if path_match:
            path_key = path_match.group(1).split('|')[0].strip()
            if path_key not in text:
                to_add.append(link)
        else:
            to_add.append(link)

    if not to_add:
        print(f"  SKIP (all links exist): {fp.name}")
        return

    additions = '\n'.join(to_add)

    if match:
        # Append inside existing Ring 3 section
        insert_pos = match.end()
        new_text = text[:insert_pos].rstrip() + '\n' + additions + '\n' + text[insert_pos:]
    else:
        # Append Ring 3 section at end
        new_text = text.rstrip() + f'\n\n## Ring 3 — Framework Connections\n\n{additions}\n'

    fp.write_text(new_text, encoding='utf-8')
    modified += 1
    print(f"  UPDATED ({len(to_add)} links): {fp.name}")

# ─────────────────────────────────────────────────────────────
# JS-SERIES Ring 3 additions
# ─────────────────────────────────────────────────────────────
JS = VAULT / "04_THEOPYHISCS/[6.5] JS-SERIES"

print("\n=== JS-SERIES ===")

append_ring3(JS / "01_Setup_12_Cliffs/JSC 00 - The Setup (The 12 Cliffs).md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The 12 unsolved cliffs catalogued here are precisely the barriers the formal Logos Principle proof resolves; JSC 00 is the empirical diagnostic that the formal proof answers.",
    "- [[04_THEOPYHISCS/GENESIS TO QUANTUM The Seven-Article Series/00_GENESIS TO QUANTUM|Genesis to Quantum — Series Hub]] — Both series establish the physics foundation before applying it to a specific event; JSC 00 and GTQ share the same opening diagnostic frame.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/02_Incarnation/JSC 01 - The Physics of Incarnation|JSC 01 — The Physics of Incarnation]] — JSC 00 establishes the 12 cliffs that make incarnation structurally necessary; JSC 01 is the first resolution event.",
])

append_ring3(JS / "02_Incarnation/JSC 01 - The Physics of Incarnation.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The Logos Principle formally proves Logos must exist as an ordering principle; JSC 01 models the specific event where that principle entered spacetime as a localized physical system.",
    "- [[04_THEOPYHISCS/GENESIS TO QUANTUM The Seven-Article Series/00_GENESIS TO QUANTUM|Genesis to Quantum — Series Hub]] — GTQ Article 1 (Why Time Is Grace) establishes time as a grace-gradient field; JSC 01's localization event is the moment the Logos entered that time-field as a bounded information object.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/01_Setup_12_Cliffs/JSC 00 - The Setup (The 12 Cliffs)|JSC 00 — The Setup (12 Cliffs)]] — JSC 00 frames the 12 unsolved problems that demand an incarnation-class solution; JSC 01 is the first answer.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — The Bekenstein-bounded localization event in JSC 01 is the prerequisite for the C_max state modeled in JSC 02; you cannot have C_max without first having a finite localized system.",
])

append_ring3(JS / "03_Coherence/JSC 02 - The Coherence of Christ (C_max).md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The Logos Principle establishes coherence (χ) as the fundamental ordering variable; C_max is the empirical maximum of that variable instantiated in a biological system.",
    "- [[05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery|The Physics of Recovery]] — Recovery models the restoration of coherence from C_low toward C_higher; JSC 02's C_max establishes the theoretical ceiling and the mechanism that makes restoration possible.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/02_Incarnation/JSC 01 - The Physics of Incarnation|JSC 01 — The Physics of Incarnation]] — The localization event (JSC 01) is the precondition for C_max; once Logos is bounded in flesh, its coherence state must be characterized.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/07_Crucifixion/JSC 06 - The Crucifixion (Universal Entropy Sink)|JSC 06 — The Crucifixion]] — The Crucifixion's thermodynamic argument requires C_max as its precondition: only a S=0 system can serve as a universal entropy sink.",
])

# Will Current - actual filename has unicode character
wc_file = JS / "04_Will_Current/JSC 03 - The Will Current (W_ϕ).md"
if not wc_file.exists():
    # try alternate name from ls output
    wc_file = JS / "04_Will_Current/JSC 03 - The Will Current (W_).md"
append_ring3(wc_file, [
    "- [[04_THEOPYHISCS/GENESIS TO QUANTUM The Seven-Article Series/00_GENESIS TO QUANTUM|Genesis to Quantum — Series Hub]] — GTQ Article 3 (Free Will in Two Frames) establishes free will as a frame-dependent phenomenon; JSC 03's W_μ is the formalization of that will-as-physical-force where Christ has C_max.",
    "- [[04_THEOPYHISCS/[7.0] Paper_2_Quantum_Bridge/BARRIER_1_OBSERVER_PROBLEM|Barrier 1 — The Observer Problem]] — The Observer Problem establishes that consciousness must be causally effective; W_μ is the formal operator that makes that causal effectiveness computable.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — W_μ's magnitude is determined by coherence level; JSC 02's C_max is the source of the maximal W_μ described here.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/05_Temptation/JSC 04 - The Temptation (Coherence Under Pressure)|JSC 04 — The Temptation]] — The Temptation tests whether an adversarial field can deflect W_μ; JSC 03 defines the current, JSC 04 stress-tests its stability.",
])

append_ring3(JS / "05_Temptation/JSC 04 - The Temptation (Coherence Under Pressure).md", [
    "- [[04_THEOPYHISCS/[7.6] Protocols/11_Experimental_Protocols|Experimental Validation Protocols]] — The Temptation is a natural-experiment case for adversarial stability: maximum entropic pressure applied to C_max; Protocol 3 maps directly onto this event.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — JSC 02 establishes what C_max means physically; JSC 04 provides the empirical proof-of-stability: C_max cannot be externally destroyed.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/06_Transfiguration/JSC 05 - The Transfiguration (De-Localization Event)|JSC 05 — The Transfiguration]] — After the Temptation proves inviolability, the Transfiguration demonstrates the consequence: C_max stored as coherent biophotonic energy becomes visible.",
])

append_ring3(JS / "06_Transfiguration/JSC 05 - The Transfiguration (De-Localization Event).md", [
    "- [[04_THEOPYHISCS/GENESIS TO QUANTUM The Seven-Article Series/00_GENESIS TO QUANTUM|Genesis to Quantum — Series Hub]] — GTQ Article 2 (The First Quantum State) establishes the pre-creation state as pure superposition; the Transfiguration is a momentary partial return to that de-localized photonic state within spacetime.",
    "- [[04_THEOPYHISCS/[7.0] Paper_2_Quantum_Bridge/BARRIER_1_OBSERVER_PROBLEM|Barrier 1 — The Observer Problem]] — The Transfiguration is a measurement event: the three witnesses constitute the minimal observer set required for collapse; this directly engages the observer problem.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/07_Crucifixion/JSC 06 - The Crucifixion (Universal Entropy Sink)|JSC 06 — The Crucifixion]] — The stored biophotonic coherence demonstrated at the Transfiguration is the same energy reservoir that makes the Crucifixion's Landauer cost payable.",
])

append_ring3(JS / "07_Crucifixion/JSC 06 - The Crucifixion (Universal Entropy Sink).md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The Logos Principle establishes that coherence violation (sin) has a measurable thermodynamic cost; the Crucifixion is where that cost is paid in full for all violations in the system.",
    "- [[04_THEOPYHISCS/[7.6] Protocols/11_Experimental_Protocols|Experimental Validation Protocols]] — The Crucifixion's thermodynamic argument (Landauer cost of entropy erasure) is the same physics the Protocol series probes at micro-scale.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — Only a C_max system (S=0) can serve as a universal entropy sink; JSC 02 is the prerequisite that makes this thermodynamic argument hold.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/08_Resurrection/JSC 06b - The Resurrection (The Singularity Inversion)|JSC 06b — The Resurrection]] — The Crucifixion pays the entropy cost; the Resurrection is the negentropic consequence — the singularity inversion Landauer's erasure makes possible.",
])

append_ring3(JS / "08_Resurrection/JSC 06b - The Resurrection (The Singularity Inversion).md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The Logos Principle predicts that maximum coherence once established cannot be permanently destroyed by entropy; the Resurrection is the empirical validation of that prediction at biological scale.",
    "- [[05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery|The Physics of Recovery]] — Recovery is a micro-scale singularity inversion: addiction = maximum entropy in a personal system; grace-mediated recovery mirrors the R_J factor at individual scale; JSC 06b is the archetype.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/07_Crucifixion/JSC 06 - The Crucifixion (Universal Entropy Sink)|JSC 06 — The Crucifixion]] — The Resurrection's negentropic state is only physically possible after the Landauer cost at the Crucifixion has been fully paid; JSC 06 → JSC 06b is a single thermodynamic sequence.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/09_Ascension/JSC 07 - The Ascended State (Higher-Dimensional Transition)|JSC 07 — The Ascended State]] — The Resurrection establishes the negentropic body; the Ascension is the next phase transition of that same body into higher-dimensional space.",
])

append_ring3(JS / "09_Ascension/JSC 07 - The Ascended State (Higher-Dimensional Transition).md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The Logos Principle posits the Logos-Field as a higher-dimensional substrate from which 4D spacetime is projected; the Ascension is the physical return of Christ's localized form to that substrate.",
    "- [[04_THEOPYHISCS/GENESIS TO QUANTUM The Seven-Article Series/00_GENESIS TO QUANTUM|Genesis to Quantum — Series Hub]] — GTQ Article 7 (The Eraser and the Cross) establishes the relationship between observer collapse and higher-dimensional information; JSC 07's transition to the Logos-Field closes the same loop.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/02_Incarnation/JSC 01 - The Physics of Incarnation|JSC 01 — The Physics of Incarnation]] — The Incarnation is a localization event — Logos entering 4D; the Ascension is the inverse: the resurrected localized form transitioning back to the higher-dimensional Logos-Field; these two papers bracket the entire arc.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/08_Resurrection/JSC 06b - The Resurrection (The Singularity Inversion)|JSC 06b — The Resurrection]] — The Ascension is the next phase transition of the negentropic body established at the Resurrection.",
])

append_ring3(JS / "10_Trinity_Supplements/JSC_Supplement_The_Trinity_Mechanism.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Paper 1 formally derives the three-part wave-collapse structure (potential → collapse → coherence maintenance) from information theory; JSC_Supplement_The_Trinity_Mechanism shows the same structure in theological terms.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/00_DE REVOLUTIONIBUS VERITATIS|De Revolutionibus Veritatis]] — Book V's Trinity analysis (Three Categories of Spiritual Reality) is the formal exposition of what this supplement models as the wave-collapse mechanism.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — The Son as 'collapsed state' (this supplement) requires C_max to be achievable; JSC 02 provides the coherence physics that makes the collapse-to-C_max story formally consistent.",
])

append_ring3(JS / "10_Trinity_Supplements/JSC_Supplement_Father.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The Father as infinite creative potential maps to the Logos-Field's infinite information substrate formally derived in Paper 1; the Father IS the Logos in its unlocalized, uncollapsed state.",
    "- [[04_THEOPYHISCS/GENESIS TO QUANTUM The Seven-Article Series/00_GENESIS TO QUANTUM|Genesis to Quantum — Series Hub]] — GTQ Article 2 (The First Quantum State) models the pre-creation state as pure superposition — the Father's domain; this supplement and GTQ Article 2 describe the same physics from theological and cosmological frames.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/10_Trinity_Supplements/JSC_Supplement_The_Trinity_Mechanism|JSC Supplement — The Trinity Mechanism]] — The Father as wave-function potential (this supplement) is the first element of the three-part mechanism analyzed in JSC_Supplement_The_Trinity_Mechanism.",
])

append_ring3(JS / "10_Trinity_Supplements/JSC_Supplement_Coherence_Triad.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — The Self-Reference Limits]] — This supplement's argument (civilizational decoherence → external Logos injection as only solution) is Truth 1 applied at civilizational scale; the Coherence Triad is the restoration mechanism Truth 1 makes structurally necessary.",
    "- [[05_PUBLICATIONS/The_Moral_Decay_of_America_Project/00_MASTER_INDEX|Moral Decay of America — Master Index]] — The civilizational decoherence this supplement identifies as requiring Trinity-structured restoration is precisely what the Moral Decay project documents with nine-domain data.",
    "- [[05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery|The Physics of Recovery]] — The individual-scale recovery mechanism in Physics of Recovery is the personal-domain instance of the same Coherence Triad restoration this supplement formalizes at civilizational scale.",
])

# ─────────────────────────────────────────────────────────────
# Layer C — Great Correction Ring 3 additions
# ─────────────────────────────────────────────────────────────
GC = VAULT / "04_THEOPYHISCS/[8.2] The_Great_Correction"

print("\n=== GREAT CORRECTION ===")

append_ring3(GC / "CHAPTER 2 THE GREAT CORRECTION Subtitle The Rebalancing of the Logos.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — The Self-Reference Limits]] — The Great Correction is Truth 1 (closed systems collapse) operating at civilizational scale; the Lagrangian rebalancing is what Truth 1's logic structurally requires.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — The Lagrangian rebalancing formalizes the same structural necessity Conservation of Order proves: moral laws are not preferences but requirements for persistence.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The Logos field whose divergence this paper warns against is formally defined here; Paper 1 is the formal backbone of the Correction's diagnosis.",
    "- [[05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery|The Physics of Recovery]] — The Great Correction at civilizational scale mirrors the same restoration mechanism Physics of Recovery models at individual scale — same grace injection physics, different substrate.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/07_Crucifixion/JSC 06 - The Crucifixion (Universal Entropy Sink)|JSC 06 — The Crucifixion]] — The Crucifixion is the archetypal Correction event — maximum entropy absorbed, system reset; the Great Correction follows the same thermodynamic pattern at civilizational scale.",
])

append_ring3(GC / "Notes Gemini.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — The Self-Reference Limits]] — The authorship/agency question maps to Truth 1: the AI as closed system cannot self-attribute; human observer is the required open-system input.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The Logos-field teleology discussed here is formally structured in Paper 1; the 'force pulling toward completion' is the χ gradient.",
    "- [[04_THEOPYHISCS/[7.2] Logic/06_LOG_03_The_Cupcake_Proof|The Cupcake Proof]] — The moral intuition of 'who deserves the credit' is the same innate moral grammar the Cupcake Proof demonstrates is pre-installed, not culturally constructed.",
])

append_ring3(GC / "Untitled.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — The Self-Reference Limits]] — This executive summary operationalizes Truth 1 at civilizational and cosmic scale through the Master Equation.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — The Great Schism described here (GR vs QM) maps to the same crisis Conservation of Order identifies: the absence of a unifying moral-structural ground.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The Logos Field (χ) introduced in this executive summary is the subject of Paper 1's formal derivation.",
])

# ─────────────────────────────────────────────────────────────
# Moral Decay — top-level and theoretical framework
# ─────────────────────────────────────────────────────────────
MD = VAULT / "05_PUBLICATIONS/The_Moral_Decay_of_America_Project"

print("\n=== MORAL DECAY PROJECT ===")

append_ring3(MD / "00_MASTER_INDEX.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — The Self-Reference Limits]] — This index organizes the empirical demonstration of Truth 1 operating at civilizational scale across American history.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The coherence framework organizing this project is a civilizational application of the Logos Principle.",
    "- [[04_THEOPYHISCS/[7.6] Protocols/11_Experimental_Protocols|Experimental Validation Protocols]] — The nine-domain coherence metric this project measures maps to the validation protocols seeking 6-sigma verification of coherence claims.",
])

append_ring3(MD / "01_Introduction.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — The introduction's central puzzle (why virtue is costly) is what Conservation of Order proves: order requires active maintenance against entropy's default.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — The Self-Reference Limits]] — The observation that 'left unconstrained, behavior fragments' is Truth 1 stated narratively.",
    "- [[05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery|The Physics of Recovery]] — The Fruits of the Spirit identified as coherence requirements here are operationalized at individual psychological scale in Physics of Recovery.",
])

# Stories
stories = MD / "01_Stories"
append_ring3(stories / "01_Samuel_1900.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — Samuel's world illustrates peak coherence: the story embodies what Conservation of Order means when moral-structural constraints are fully operative.",
    "- [[05_PUBLICATIONS/The_Moral_Decay_of_America_Project/00_MASTER_INDEX|Moral Decay — Master Index]] — Samuel's chapter establishes the civilizational baseline (χ ≈ 1.0) against which all subsequent decline is measured.",
])

append_ring3(stories / "04_Thomas_1974.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — The Self-Reference Limits]] — Thomas's world is the narrative face of Truth 1: the moment when civilizational closed-system collapse became visible in lived experience.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — The constraint removal Thomas lives through (no-fault divorce, sexual revolution, trust collapse) is Conservation of Order in reverse.",
    "- [[05_PUBLICATIONS/The_Moral_Decay_of_America_Project/01_Decade_Analysis/1968-1973_Phase_Transition|1968-1973 Phase Transition]] — Thomas's chapter is the narrative embodiment of the phase-transition data this analysis quantifies.",
])

append_ring3(stories / "06_Jacob_2025.md", [
    "- [[04_THEOPYHISCS/[8.2] The_Great_Correction/CHAPTER 2 THE GREAT CORRECTION Subtitle The Rebalancing of the Logos|The Great Correction]] — Jacob in 2025 sits at the exact moment the Great Correction is beginning; his choice to enter a church is the Logos-alignment the Correction paper prescribes.",
    "- [[05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery|The Physics of Recovery]] — Jacob's crisis (loneliness, disconnection, screen saturation) is the individual-scale decoherence state that Physics of Recovery models as requiring external negentropy injection.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — The Self-Reference Limits]] — Jacob's world is Truth 1 at maximum visibility: a civilization so closed to external coupling that AI companions are a billion-dollar industry.",
])

# Theoretical framework
tf = MD / "02_Theoretical_Framework"

append_ring3(tf / "02_Foundations/Introduction_The_Crisis_of_Intelligibility.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Paper 1 is the formal response to the Crisis of Intelligibility named here; the Logos Principle is the theorem that resolves the self-contradiction of materialist science.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — The Self-Reference Limits]] — Gödel's Incompleteness (cited here as the Zombie Science diagnosis) is the first of Truth 1's five proofs; this introduction and Truth 1 are co-diagnostics of the same crisis.",
])

append_ring3(tf / "02_Foundations/Foundations_of_Persistence_TDSI.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — TDSI is the multi-domain formalization of exactly what Conservation of Order proves at the level of a single moral law.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — The Self-Reference Limits]] — The Sacrificial Asymmetry Axiom (FA-F1) is Truth 1 applied to repair: closed systems cannot self-restore; Grace is the required external input.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/07_Crucifixion/JSC 06 - The Crucifixion (Universal Entropy Sink)|JSC 06 — The Crucifixion]] — The Crucifixion is the maximum-cost instance of FA-F1: the asymmetric entropy-absorption event TDSI predicts must exist.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Paper 1 formally derives the Logos field that TDSI's invariants are expressions of.",
])

# Core papers
cp = tf / "03_Core_Papers"
for fname, links in [
    ("01_PAPER_The_Coherence_Metric.md", [
        "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — The Self-Reference Limits]] — The 1968-1973 collapse documented here is the empirical 9-domain demonstration that Truth 1's closed-system prediction holds at civilizational scale.",
        "- [[04_THEOPYHISCS/[7.6] Protocols/11_Experimental_Protocols|Experimental Validation Protocols]] — The falsifiability structure and measurement criteria here parallel the validation protocol architecture; this is the social-domain instance of framework validation.",
    ]),
]:
    fp = cp / fname
    if fp.exists():
        append_ring3(fp, links)

# ─────────────────────────────────────────────────────────────
# Backlinks into Hub Papers
# ─────────────────────────────────────────────────────────────
print("\n=== HUB PAPER BACKLINKS ===")

# Paper 1 — The Logos Principle
append_ring3(VAULT / "05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle.md", [
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/02_Incarnation/JSC 01 - The Physics of Incarnation|JSC 01 — The Physics of Incarnation]] — JSC 01 models the specific spacetime event where the Logos formally derived here entered physical reality as a bounded information object.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — C_max is the empirical maximum of the χ variable formally introduced here; JSC 02 is the living proof-of-concept for Paper 1's central theorem.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/08_Resurrection/JSC 06b - The Resurrection (The Singularity Inversion)|JSC 06b — The Resurrection]] — The Resurrection is the empirical validation at biological scale of Paper 1's prediction: maximum coherence cannot be permanently destroyed by entropy.",
    "- [[04_THEOPYHISCS/[8.2] The_Great_Correction/CHAPTER 2 THE GREAT CORRECTION Subtitle The Rebalancing of the Logos|The Great Correction]] — The Great Correction applies Paper 1's Logos-field dynamics to civilizational-scale entropy diagnosis and correction.",
    "- [[05_PUBLICATIONS/The_Moral_Decay_of_America_Project/00_MASTER_INDEX|Moral Decay of America — Master Index]] — This project is a civilizational application of Paper 1's Logos Principle, measuring χ divergence across nine domains over 125 years.",
])

# Three Truths — Truth 1
append_ring3(VAULT / "04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits.md", [
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/10_Trinity_Supplements/JSC_Supplement_Coherence_Triad|JSC Supplement — Coherence Triad]] — The Coherence Triad supplement applies Truth 1's closed-system conclusion at civilizational scale and identifies the Trinity-structured restoration as the only valid solution.",
    "- [[05_PUBLICATIONS/The_Moral_Decay_of_America_Project/00_MASTER_INDEX|Moral Decay of America — Master Index]] — The Moral Decay project is the largest empirical demonstration of Truth 1: nine domains of civilizational collapse correlated at R̄=0.986, exactly what closed-system thermodynamics predicts.",
    "- [[04_THEOPYHISCS/[8.2] The_Great_Correction/CHAPTER 2 THE GREAT CORRECTION Subtitle The Rebalancing of the Logos|The Great Correction]] — The Great Correction is Truth 1's logical resolution at civilizational scale: the correction that closed-system dynamics structurally demand.",
])

# Experimental Protocols
append_ring3(VAULT / "04_THEOPYHISCS/[7.6] Protocols/11_Experimental_Protocols.md", [
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/07_Crucifixion/JSC 06 - The Crucifixion (Universal Entropy Sink)|JSC 06 — The Crucifixion]] — The Crucifixion is the maximum-scale instance of the Landauer entropy erasure this protocol tests at micro-scale; the same physics, different magnitude.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/05_Temptation/JSC 04 - The Temptation (Coherence Under Pressure)|JSC 04 — The Temptation]] — The Temptation is a natural-experiment case study for Protocol 3's adversarial stability hypothesis: C_max holds under maximum adversarial pressure.",
    "- [[05_PUBLICATIONS/The_Moral_Decay_of_America_Project/00_MASTER_INDEX|Moral Decay of America — Master Index]] — The nine-domain coherence metric in this project generates the social-scale datasets that experimental protocols predict should show 6-sigma framework validation.",
])

# Physics of Recovery
recovery = VAULT / "05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery.md"
append_ring3(recovery, [
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — C_max is the theoretical ceiling that makes recovery meaningful; the restoration pathway in Physics of Recovery is movement toward the coherence state JSC 02 defines as achievable.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/08_Resurrection/JSC 06b - The Resurrection (The Singularity Inversion)|JSC 06b — The Resurrection]] — The Resurrection is the archetype of the micro-scale singularity inversion that recovery represents; same R_J factor, different scale.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/10_Trinity_Supplements/JSC_Supplement_Coherence_Triad|JSC Supplement — Coherence Triad]] — The Coherence Triad's civilizational restoration mechanism is the macro-scale version of the individual recovery mechanism modeled here.",
    "- [[04_THEOPYHISCS/[8.2] The_Great_Correction/CHAPTER 2 THE GREAT CORRECTION Subtitle The Rebalancing of the Logos|The Great Correction]] — The Great Correction at civilizational scale is the same restoration physics as individual recovery; both require external Logos injection to reverse entropy accumulation.",
])

print(f"\n=== DONE === Modified: {modified}  Errors: {errors}")
