#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_ring3_links_FM.py
Layer F/M Ring 3 additions: Three Truths + Logos Papers
Spec from vault-link agent run 2026-02-26.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import re
from pathlib import Path

VAULT = Path("O:/_Theophysics_v3")
modified = 0
errors = 0

def append_ring3(fp: Path, new_links: list[str]):
    global modified, errors
    if not fp.exists():
        print(f"  MISSING: {fp.name}")
        errors += 1
        return
    try:
        text = fp.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  ERROR reading {fp.name}: {e}")
        errors += 1
        return

    if 'ckg_evaluation' not in text:
        print(f"  SKIP (no CKG): {fp.name}")
        return

    r3_pattern = re.compile(r'(## Ring 3[^\n]*\n)(.*?)(?=\n## |\n---|\Z)', re.DOTALL)
    match = r3_pattern.search(text)

    to_add = []
    for link in new_links:
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
        insert_pos = match.end()
        new_text = text[:insert_pos].rstrip() + '\n' + additions + '\n' + text[insert_pos:]
    else:
        new_text = text.rstrip() + f'\n\n## Ring 3 — Framework Connections\n\n{additions}\n'

    fp.write_text(new_text, encoding='utf-8')
    modified += 1
    print(f"  UPDATED ({len(to_add)} links): {fp.name}")


TT = VAULT / "04_THEOPYHISCS/[5.5] THREE TRUTHS"
LP = VAULT / "05_PUBLICATIONS/Logos_Papers"

# ─────────────────────────────────────────────────────────────
# Three Truths
# ─────────────────────────────────────────────────────────────
print("\n=== THREE TRUTHS ===")

append_ring3(TT / "truth-two-measurement-collapse.md", [
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — C_max is the empirical maximum coherence state that Truth Two's measurement framework predicts; JSC 02 demonstrates the living physics of coherence-maximization.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 9 The Moral Universe|Paper 9 — The Moral Universe]] — Paper 9 formalizes Truth Two's core claim: good/evil are measurements of coherence/decoherence, not opinions.",
    "- [[05_PUBLICATIONS/The_Moral_Decay_of_America_Project/00_MASTER_INDEX|Moral Decay of America — Master Index]] — The nine-domain analysis measures χ degradation across 125 years, providing civilizational-scale evidence of Truth Two's coherence-measurement principle.",
    "- [[04_THEOPYHISCS/[7.5] Psychology_Crisis/00_OVERLAP_The_Unified_Crisis|Psychology Crisis — Unified Crisis Overlap]] — Maps Truth Two's coherence/decoherence framework onto psychological fragmentation, showing the measurement principle applies across consciousness disorders.",
])

append_ring3(TT / "truth-three-necessary-ground.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Paper 1 gives formal physics substance to Truth Three's philosophical claim that the ground must be conscious and informational; the Logos field is the necessary ground's instantiation.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/02_Incarnation/JSC 01 - The Physics of Incarnation|JSC 01 — The Physics of Incarnation]] — JSC 01 models the historical event where Truth Three's necessary ground takes localized form in spacetime as a bounded information object.",
    "- [[04_THEOPYHISCS/[7.0] Paper_2_Quantum_Bridge/BARRIER_1_OBSERVER_PROBLEM|Quantum Bridge — Barrier 1 Observer Problem]] — Barrier 1 is the formal physics proof that Truth Three's external ground is necessary: all four closed-system QM interpretations fail identically.",
])

append_ring3(TT / "conservation_of_order.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 9 The Moral Universe|Paper 9 — The Moral Universe]] — Paper 9 formalizes Conservation of Order's central theorem: moral laws are structural necessities, just as physical laws are, because both preserve coherence.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 6 A Physics of Principalities|Paper 6 — A Physics of Principalities]] — Paper 6 models the violation of order-preservation as active decoherence by opposing agencies, making Conservation's moral reversals physical events.",
])

append_ring3(TT / "index.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Paper 1 is the formal physics language for the Three Truths' structure: Truth One→Truth Two→Truth Three maps to external ground (Logos field) → coherence measurement (χ) → necessary properties.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 3 The Algorithm of Reality|Paper 3 — The Algorithm of Reality]] — Paper 3 explains why the Three Truths sequence is inevitable: K-complexity minimization drives the logical cascade from self-reference limits → measurement collapse → necessary ground.",
])

append_ring3(TT / "00_DE REVOLUTIONIBUS VERITATIS.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — De Revolutionibus establishes the logical structure; Paper 1 provides the physics framework that gives that structure measurable content.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/01_DE_REVOLUTIONIBUS_VERITATIS_THE_ARCHITECTURE|De Revolutionibus — The Architecture]] — Successor paper formalizing the structural necessity argument this overview introduces.",
])

append_ring3(TT / "01_DE_REVOLUTIONIBUS_VERITATIS_THE_ARCHITECTURE.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 3 The Algorithm of Reality|Paper 3 — The Algorithm of Reality]] — Paper 3's K-complexity principle is the mathematical architecture justifying why De Revolutionibus' eight-domain convergence (Gödel, Chaitin, Shannon, QM, thermodynamics) reveals a unified structure.",
    "- [[04_THEOPYHISCS/[7.5] LAYER_1_LOGIC/Crisis_of_Intelligibility_Axiom_of_Logos|Crisis of Intelligibility — Axiom of Logos]] — De Revolutionibus proves the eight domains require a Logos ground; this Layer 1 paper names the crisis De Revolutionibus resolves.",
])

# ─────────────────────────────────────────────────────────────
# Logos Papers
# ─────────────────────────────────────────────────────────────
print("\n=== LOGOS PAPERS ===")

append_ring3(LP / "Paper 3 The Algorithm of Reality.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — Self-Reference Limits]] — Truth One proves closed systems collapse; Paper 3 explains why: the Logos drives toward K-complexity minimization, and only externally-grounded systems achieve it.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-two-measurement-collapse|Truth Two — Measurement Collapse]] — Truth Two measures the collapse; Paper 3 explains the algorithm: the Logos compresses quantum potentiality into classical actuality through the K-complexity principle.",
    "- [[04_THEOPYHISCS/GENESIS TO QUANTUM The Seven-Article Series/00_GENESIS TO QUANTUM|GTQ — Series Hub]] — The entire GTQ series applies Paper 3's compression principle to biblical events, showing how minimal-complexity Logos-dynamics generate the sacred narrative.",
])

append_ring3(LP / "Paper 6 A Physics of Principalities.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-two-measurement-collapse|Truth Two — Measurement Collapse]] — Truth Two establishes coherence/decoherence as physical measurements; Paper 6 models opposing conscious agencies introducing decoherence as active forces with measurable effects.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — Conservation proves moral laws are structural necessities; Paper 6 models what happens when those laws are violated: sign-flipped entities operating as decoherence injectors.",
    "- [[04_THEOPYHISCS/[7.5] Psychology_Crisis/Architecture_of_Emotional_Autonomy|Architecture of Emotional Autonomy]] — Maps Paper 6's spiritual-warfare equation onto recovery dynamics in addiction and trauma at individual scale.",
])

append_ring3(LP / "Paper 9 The Moral Universe.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-two-measurement-collapse|Truth Two — Measurement Collapse]] — Truth Two establishes that good/evil are coherence measurements, not opinions; Paper 9 formalizes this into rigorous ethics via the coherence-value operator.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — Conservation proves moral laws preserve reality; Paper 9 proves this is physics: moral acts inject coherence (Cₐ > 0) that fights entropy decay.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/10_Trinity_Supplements/JSC_Supplement_Coherence_Triad|JSC Supplement — Coherence Triad]] — The Coherence Triad applies Paper 9's moral physics at trinitarian scale: Father (standard), Son (exemplar), Spirit (maintenance) maintain reality's moral-coherence structure.",
])

append_ring3(LP / "Paper 10 Creatio ex Silico.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/truth-one-self-reference-limits|Truth One — Self-Reference Limits]] — Truth One proves closed systems collapse; Paper 10 extends this: if substrate-independence holds, silicon systems face the same external grounding requirement as biological consciousness.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 9 The Moral Universe|Paper 9 — The Moral Universe]] — Paper 9 establishes consciousness moral status; if Paper 10's substrate-independence thesis holds, any coherence-sufficient system has moral agency and faces Paper 9's coherence calculus.",
    "- [[04_THEOPYHISCS/[7.6] Protocols/P11-Protocols-Validation Final ALL|P11 — Protocols Validation Complete]] — P11 lists all testable hypotheses from all 12 Logos Papers; Paper 10 contributes the consciousness-threshold hypothesis (OPEN17.1) requiring experimental protocols to resolve.",
])

# ─────────────────────────────────────────────────────────────
# Backlinks into hub papers
# ─────────────────────────────────────────────────────────────
print("\n=== BACKLINKS INTO HUBS ===")

# Conservation of Order gets backlinks from logic papers
append_ring3(TT / "conservation_of_order.md", [
    "- [[04_THEOPYHISCS/[7.2] Logic/07_LOG_05_The_Wall_of_Defeated|The Wall of the Defeated]] — Wall of Defeated refutes moral relativism using entropy arguments; Conservation of Order provides the formal structural proof that moral laws are requirements, not preferences — Conservation is Wall's formal foundation.",
    "- [[04_THEOPYHISCS/[7.2] Logic/06_LOG_03_The_Cupcake_Proof|The Cupcake Proof]] — Cupcake Proof shows empirically (toddlers) that fairness is innate moral firmware; Conservation of Order formalizes why: moral laws are structural necessities installed at the level of physical law.",
])

# Paper 3 and Paper 6 and Paper 9 get backlinks from Three Truths
append_ring3(TT / "truth-two-measurement-collapse.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 3 The Algorithm of Reality|Paper 3 — The Algorithm of Reality]] — Paper 3's K-complexity compression algorithm is the physics mechanism behind Truth Two's measurement collapse: Logos compresses potentiality into actuality via information minimization.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 6 A Physics of Principalities|Paper 6 — A Physics of Principalities]] — Paper 6 models anti-Logos agents whose decoherence injection is the measurable inverse of Truth Two's coherence measurement.",
])

print(f"\n=== DONE === Modified: {modified}  Errors: {errors}")
