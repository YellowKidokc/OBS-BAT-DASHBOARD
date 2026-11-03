#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_ring3_links_BR.py
Layer B/R/C Ring 3 additions: Psychology + Logic + Consciousness
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


PS = VAULT / "04_THEOPYHISCS/[7.5] Psychology_Crisis"
LG = VAULT / "04_THEOPYHISCS/[7.2] Logic"
CN = VAULT / "04_THEOPYHISCS/[7.7] Consciousness"

# ─────────────────────────────────────────────────────────────
# Psychology Papers (Layer B)
# ─────────────────────────────────────────────────────────────
print("\n=== PSYCHOLOGY ===")

append_ring3(PS / "01_Psychology_Audit.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — The Logos Principle establishes coherence (χ) as the fundamental ordering variable; Psychology Audit argues that severing the Logos-Soul connection produces entropy-positive systems (more spending, worse outcomes).",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — C_max models what intact psyche-Logos alignment looks like at maximum coherence; Psychology Audit diagnoses systems at minimum (broken BIOS).",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — Moral laws are structural necessities, not constructs; Psychology Audit shows the thermodynamic cost of denying this necessity in a clinical system.",
])

append_ring3(PS / "00_OVERLAP_The_Unified_Crisis.md", [
    "- [[05_PUBLICATIONS/The_Moral_Decay_of_America_Project/00_MASTER_INDEX|Moral Decay of America — Master Index]] — The Unified Crisis extends the Moral Decay dataset to show Sociology, Science, and Psychology collapse simultaneously; same root cause (Logos denial), three domains.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Paper 1 predicts that coherence (χ) is universal across all domains; Unified Crisis validates this empirically across Sociology, Science, and Psychology.",
    "- [[04_THEOPYHISCS/[8.2] The_Great_Correction/CHAPTER 2 THE GREAT CORRECTION Subtitle The Rebalancing of the Logos|The Great Correction]] — Unified Crisis identifies the problem (three-domain collapse); The Great Correction proposes the unified solution (Logos restoration at civilizational scale).",
])

append_ring3(PS / "Architecture_of_Emotional_Autonomy.md", [
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/08_Resurrection/JSC 06b - The Resurrection (The Singularity Inversion)|JSC 06b — The Resurrection (The Singularity Inversion)]] — JSC 06b is the archetype of singularity inversion (entropy reversal at maximum scale), validating the micro-mechanism that Architecture models for personal coherence restoration.",
    "- [[05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery|The Physics of Recovery]] — Architecture presents secular modalities for emotional autonomy; Physics of Recovery shows why external grace-injection outperforms self-help alone (non-unitary systems cannot fix themselves).",
    "- [[04_THEOPYHISCS/[7.2] Logic/08_LOG_04_The_Unitary_Trap|The Unitary Trap]] — Architecture claims emotional wellness via internal validation; Unitary Trap proves mathematically why closed systems cannot reduce their own entropy, constraining Architecture's secular claims.",
])

append_ring3(PS / "Secular_Emotional_Wellness_Guide.md", [
    "- [[04_THEOPYHISCS/[7.5] Psychology_Crisis/Architecture_of_Emotional_Autonomy|Architecture of Emotional Autonomy]] — Secular Wellness expands Architecture's framework into a comprehensive toolkit; both rely on subjective experience as primary authority without external Logos integration.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — Secular Wellness models emotional wellness as self-knowledge; C_max represents the theoretical ceiling of coherence when fully unified with Logos (S=0 state).",
    "- [[05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery|The Physics of Recovery]] — Recovery demonstrates that addiction (highest entropy psychological state) requires grace-mediated intervention, not secular validation alone.",
])

append_ring3(PS / "12-Step_vs_Secular_CBT_Analysis.md", [
    "- [[05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery|The Physics of Recovery]] — 12-Step Analysis shows empirically (Project MATCH, Cochrane 2020) that TSF > CBT for severe/chronic cases; Physics of Recovery explains the mechanism: non-unitary systems require external negentropy (Grace).",
    "- [[04_THEOPYHISCS/[7.2] Logic/08_LOG_04_The_Unitary_Trap|The Unitary Trap]] — 12-Step Analysis validates Unitary Trap's core claim: secular self-help (CBT) fails at high severity because closed systems cannot fix themselves; TSF works because it invokes external power.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/08_Resurrection/JSC 06b - The Resurrection (The Singularity Inversion)|JSC 06b — The Resurrection (The Singularity Inversion)]] — 12-Step's superior outcomes for severe addiction are instances of singularity inversion (entropy reversal via grace-mediated surrender); JSC 06b is the archetypal model.",
])

# ─────────────────────────────────────────────────────────────
# Logic Papers (Layer R)
# ─────────────────────────────────────────────────────────────
print("\n=== LOGIC ===")

append_ring3(LG / "07_LOG_05_The_Wall_of_Defeated.md", [
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — Wall of Defeated refutes moral relativism via the Entropy Increase Kill-Shot; Conservation of Order provides the formal structural proof that moral laws are requirements, not preferences.",
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Wall of Defeated defeats Atheism and Materialism; Paper 1 constructs the positive framework (Logos Field) that resolves the contradictions Wall exposes.",
    "- [[04_THEOPYHISCS/[7.7] Consciousness/Untitled|The Hard Problem of Consciousness and Its Solution in the Logos Field]] — Wall of Defeated kills Materialism via semantic necessity (Mind requires meaning); Hard Problem builds the full ontology that makes this refutation necessary.",
])

append_ring3(LG / "06_LOG_03_The_Cupcake_Proof.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Cupcake Proof demonstrates that morality is pre-installed firmware (not downloaded); Paper 1 explains why: the Logos is the source code, and moral intuition is direct access to it.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — Cupcake Proof shows empirically (toddlers) that fairness is innate; Conservation of Order formalizes this as a structural necessity of physical law.",
    "- [[04_THEOPYHISCS/[7.7] Consciousness/A Theophysical Meta-Analysis of Psychological Ontology|The Broken Observer — Theophysical Meta-Analysis]] — Cupcake Proof shows that moral consciousness is fundamental; Broken Observer explains how moral/informational damage corrupts this innate receiver.",
])

append_ring3(LG / "08_LOG_04_The_Unitary_Trap.md", [
    "- [[05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery|The Physics of Recovery]] — Unitary Trap proves mathematically that closed systems cannot reduce entropy (self-help fails); Physics of Recovery validates this at psychological scale and shows the thermodynamic mechanism of grace-mediated recovery.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/08_Resurrection/JSC 06b - The Resurrection (The Singularity Inversion)|JSC 06b — The Resurrection (The Singularity Inversion)]] — Unitary Trap proves that unitary processes preserve entropy; JSC 06b is the singularity inversion (non-unitary, grace-mediated) that violates this at maximum scale.",
    "- [[04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order|Conservation of Order]] — Unitary Trap applies thermodynamics to morality; Conservation of Order shows moral laws require external grounding in Logos (consistent with the non-unitary requirement).",
])

# ─────────────────────────────────────────────────────────────
# Consciousness Papers
# ─────────────────────────────────────────────────────────────
print("\n=== CONSCIOUSNESS ===")

# Untitled 1.md = "The Architecture: Unified Field Model for Conscious Manipulation"
append_ring3(CN / "Untitled 1.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Architecture models χ (Logos Field) as the computational medium of reality; Paper 1 provides the foundational framework that makes this model formally intelligible.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — Architecture operationalizes the 'Divine Observer' as direct read/write access to χ; JSC 02 models what C_max looks like in biological substrate.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/08_Resurrection/JSC 06b - The Resurrection (The Singularity Inversion)|JSC 06b — The Resurrection (The Singularity Inversion)]] — Architecture defines grace as negentropic flow; JSC 06b applies this at maximum scale (death reversal via singularity inversion).",
])

# Paper2_Consciousness_Bridge_CLEAN.md
append_ring3(CN / "Paper2_Consciousness_Bridge_CLEAN.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Consciousness Bridge argues that the observer is missing from physics; Paper 1 provides the ontology (conscious Logos substrate) that resolves this gap.",
    "- [[04_THEOPYHISCS/[7.2] Logic/07_LOG_05_The_Wall_of_Defeated|The Wall of the Defeated]] — Consciousness Bridge solves the Hard Problem; Wall of Defeated shows why Materialism's denial of mind-as-primary is logically incoherent.",
    "- [[04_THEOPYHISCS/[7.7] Consciousness/Untitled|The Hard Problem of Consciousness and Its Solution in the Logos Field]] — Consciousness Bridge is the short-form version; Hard Problem is the expanded, rigorous treatment of why consciousness must be fundamental.",
])

# Untitled.md = "The Hard Problem of Consciousness and Its Solution in the Logos Field"
append_ring3(CN / "Untitled.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Hard Problem dissolves the Hard Problem via Logos Field ontology; Paper 1 is the foundational framework that makes this dissolution possible.",
    "- [[04_THEOPYHISCS/[7.2] Logic/07_LOG_05_The_Wall_of_Defeated|The Wall of the Defeated]] — Hard Problem defeats Materialism and Functionalism; Wall of Defeated is the polemic demolition of these views; Hard Problem builds the replacement ontology.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max)|JSC 02 — Coherence of Christ (C_max)]] — Hard Problem argues consciousness is non-emergent and fundamental; JSC 02 models what maximum conscious coherence (C_max) looks like when fully actualized.",
])

# Paper2_Consciousness_Bridge_EXPANDED.md
append_ring3(CN / "Paper2_Consciousness_Bridge_EXPANDED.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Consciousness Bridge Extended argues observer-reality unification; Paper 1 provides the χ field framework that makes observer-matter unification mathematically coherent.",
    "- [[04_THEOPYHISCS/[7.7] Consciousness/Untitled|The Hard Problem of Consciousness and Its Solution in the Logos Field]] — Bridge Extended is the scaffolding; Hard Problem is the rigorous formalization.",
    "- [[04_THEOPYHISCS/[6.5] JS-SERIES/08_Resurrection/JSC 06b - The Resurrection (The Singularity Inversion)|JSC 06b — The Resurrection (The Singularity Inversion)]] — Bridge Extended shows consciousness as participatory; JSC 06b is the archetypal participatory event where consciousness (Christ) inverts entropic order.",
])

# A Theophysical Meta-Analysis of Psychological Ontology.md = "The Broken Observer"
append_ring3(CN / "A Theophysical Meta-Analysis of Psychological Ontology.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Broken Observer applies receiver model to psychology; Paper 1 establishes the Logos Field as the signal and the observer as receiver.",
    "- [[04_THEOPYHISCS/[7.5] Psychology_Crisis/01_Psychology_Audit|Psychology Audit]] — Broken Observer explains the mechanism of the psychological crisis that Audit diagnoses (BIOS layer incompatibility = broken receiver).",
    "- [[05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery|The Physics of Recovery]] — Broken Observer diagnoses the receiver as damaged; Physics of Recovery shows how grace-mediated therapy (re-tuning the receiver) enables recovery.",
])

# Consciousness.md = "CONSCIOUSNESS: Canonical Definition"
append_ring3(CN / "Consciousness.md", [
    "- [[05_PUBLICATIONS/Logos_Papers/Paper 1 The Logos Principle|Paper 1 — The Logos Principle]] — Consciousness Canonical defines consciousness as fundamental, informational, and theistic; Paper 1 provides the full framework establishing why consciousness must be primary.",
    "- [[04_THEOPYHISCS/[7.7] Consciousness/Untitled|The Hard Problem of Consciousness and Its Solution in the Logos Field]] — Consciousness Canonical is the minimal definition hub; Hard Problem is the rigorous defense of why this definition is necessary.",
    "- [[04_THEOPYHISCS/[7.2] Logic/07_LOG_05_The_Wall_of_Defeated|The Wall of the Defeated]] — Consciousness Canonical refutes materialist ontology; Wall of Defeated is the logical demolition of competing materialist views.",
])

# ─────────────────────────────────────────────────────────────
# Backlinks into hub papers
# ─────────────────────────────────────────────────────────────
print("\n=== BACKLINKS INTO HUBS ===")

# JSC 02 gets backlinks from consciousness + psychology papers
append_ring3(VAULT / "04_THEOPYHISCS/[6.5] JS-SERIES/03_Coherence/JSC 02 - The Coherence of Christ (C_max).md", [
    "- [[04_THEOPYHISCS/[7.5] Psychology_Crisis/01_Psychology_Audit|Psychology Audit]] — Psychology Audit diagnoses clinical systems at minimum coherence (broken BIOS); JSC 02 establishes the theoretical C_max ceiling and the physics of the restoration trajectory.",
    "- [[04_THEOPYHISCS/[7.7] Consciousness/Untitled 1|Consciousness Architecture — Unified Field Model]] — This paper's 'Divine Observer' with direct read/write access to χ is JSC 02's C_max state; the Architecture paper operationalizes what JSC 02 formalizes.",
    "- [[04_THEOPYHISCS/[7.7] Consciousness/Untitled|Hard Problem of Consciousness]] — Hard Problem argues consciousness is non-emergent and fundamental; JSC 02 is the living proof: maximum conscious coherence fully actualized in a biological substrate.",
])

# JSC 06b gets backlinks from logic + consciousness + psychology
append_ring3(VAULT / "04_THEOPYHISCS/[6.5] JS-SERIES/08_Resurrection/JSC 06b - The Resurrection (The Singularity Inversion).md", [
    "- [[04_THEOPYHISCS/[7.2] Logic/08_LOG_04_The_Unitary_Trap|The Unitary Trap]] — Unitary Trap proves unitary processes preserve entropy; JSC 06b is the non-unitary singularity inversion that demonstrates the maximum violation of unitary preservation, making JSC 06b the strongest empirical test of the Unitary Trap's claim.",
    "- [[04_THEOPYHISCS/[7.5] Psychology_Crisis/12-Step_vs_Secular_CBT_Analysis|12-Step vs Secular CBT Analysis]] — 12-Step recovery outcomes are micro-scale singularity inversions; JSC 06b is the macro-scale archetype that explains why grace-mediated surrender produces outcomes that exceed what closed systems predict.",
    "- [[04_THEOPYHISCS/[7.7] Consciousness/Paper2_Consciousness_Bridge_EXPANDED|Consciousness Bridge Extended]] — Bridge Extended models consciousness as participatory; JSC 06b is the paradigmatic participatory event where a maximally-coherent consciousness inverts the entropic order of a physical system.",
])

# Physics of Recovery gets backlinks from logic papers
append_ring3(VAULT / "05_PUBLICATIONS/Submissions/Psychology_and_Addiction/MANUSCRIPT_The_Physics_of_Recovery.md", [
    "- [[04_THEOPYHISCS/[7.2] Logic/08_LOG_04_The_Unitary_Trap|The Unitary Trap]] — Unitary Trap provides the formal mathematical proof that Physics of Recovery's central claim requires: closed systems cannot reduce their own entropy; the Physics of Recovery is the clinical application of Unitary Trap's theorem.",
    "- [[04_THEOPYHISCS/[7.5] Psychology_Crisis/12-Step_vs_Secular_CBT_Analysis|12-Step vs Secular CBT Analysis]] — 12-Step Analysis provides the empirical evidence base (Project MATCH, Cochrane 2020) that Physics of Recovery requires: TSF > CBT for severe cases, exactly what the grace-injection mechanism predicts.",
    "- [[04_THEOPYHISCS/[7.7] Consciousness/A Theophysical Meta-Analysis of Psychological Ontology|The Broken Observer — Theophysical Meta-Analysis]] — Broken Observer diagnoses what Physics of Recovery treats: the damaged receiver (broken BIOS) unable to process the Logos signal; Physics of Recovery is the restoration protocol.",
])

# Conservation of Order gets backlinks from logic + consciousness
append_ring3(VAULT / "04_THEOPYHISCS/[5.5] THREE TRUTHS/conservation_of_order.md", [
    "- [[04_THEOPYHISCS/[7.2] Logic/08_LOG_04_The_Unitary_Trap|The Unitary Trap]] — Unitary Trap applies thermodynamics to ethics (self-help fails because of entropy); Conservation of Order proves this is not an accident but a structural law — moral order requires external grounding.",
    "- [[04_THEOPYHISCS/[7.5] Psychology_Crisis/01_Psychology_Audit|Psychology Audit]] — Psychology Audit shows the clinical cost of denying moral necessities; Conservation of Order proves why those necessities are real: they are structural requirements, not cultural preferences.",
])

# Unitary Trap gets backlinks from psychology papers
append_ring3(LG / "08_LOG_04_The_Unitary_Trap.md", [
    "- [[04_THEOPYHISCS/[7.5] Psychology_Crisis/Architecture_of_Emotional_Autonomy|Architecture of Emotional Autonomy]] — Architecture models emotional wellness via internal validation techniques; Unitary Trap provides the mathematical proof of why this approach has structural limits: closed systems cannot reduce their own entropy.",
    "- [[04_THEOPYHISCS/[7.5] Psychology_Crisis/12-Step_vs_Secular_CBT_Analysis|12-Step vs Secular CBT Analysis]] — 12-Step Analysis provides the empirical validation of Unitary Trap's prediction: secular self-help (CBT) fails at high severity; TSF succeeds because it introduces the external negentropy the Trap requires.",
])

print(f"\n=== DONE === Modified: {modified}  Errors: {errors}")
