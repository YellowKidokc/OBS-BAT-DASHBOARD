"""
Restore CDCM master Excel from session data (all source JSONs were cleaned).
Contains complete section averages A-K for all 32 reviewed papers.
"""
import csv, pathlib
OUTPUT_DIR = pathlib.Path("O:/_Theophysics_v3/00_SYSTEM/00_ENGINE/Open AI Calls/Open-AI-PAPER-REVIEW/output")
SECTIONS   = list("ABCDEFGHIJK")

# All known papers: (collection, paper, score, {A:x, B:x, ...})
PAPERS = [
    ("[5.5] THREE TRUTHS", "01_DE_REVOLUTIONIBUS_VERITATIS_THE_ARCHITECTURE", 86.1,
     dict(A=8.0,B=8.5,C=7.0,D=7.0,E=7.5,F=7.5,G=7.0,H=7.0,I=7.0,J=7.0,K=7.5)),
    ("[5.5] THREE TRUTHS", "02_DE_REVOLUTIONIBUS_VERITATIS_THE_LOCK", 73.0,
     dict(A=7.5,B=8.25,C=7.0,D=7.0,E=7.0,F=7.5,G=7.0,H=6.5,I=7.0,J=7.0,K=7.5)),
    ("[5.5] THREE TRUTHS", "03_DE_REVOLUTIONIBUS_VERITATIS_THE_COST_OF_DENIAL", 70.9,
     dict(A=5.0,B=6.75,C=6.0,D=5.0,E=6.0,F=5.75,G=6.0,H=5.5,I=5.0,J=5.0,K=6.0)),
    ("[5.5] THREE TRUTHS", "04_DE_REVOLUTIONIBUS_VERITATIS_THE_KEY", 63.7,
     dict(A=7.0,B=7.5,C=6.0,D=5.0,E=5.0,F=5.5,G=5.0,H=4.5,I=5.0,J=5.0,K=5.5)),
    ("[5.5] THREE TRUTHS", "godel", 76.5,
     dict(A=6.5,B=8.25,C=7.5,D=5.75,E=6.5,F=7.0,G=7.25,H=6.0,I=5.5,J=6.5,K=6.0)),
    ("[5.5] THREE TRUTHS", "truth-one-self-reference-limits", 76.3,
     dict(A=7.0,B=7.5,C=6.0,D=5.0,E=6.0,F=6.0,G=6.5,H=5.25,I=4.5,J=5.75,K=5.5)),
    ("[5.5] THREE TRUTHS", "truth-two-measurement-collapse", 61.0,
     dict(A=5.0,B=5.75,C=4.5,D=4.0,E=5.0,F=5.5,G=5.5,H=4.5,I=3.5,J=4.0,K=4.5)),
    ("[5.5] THREE TRUTHS", "truth-three-necessary-ground", 44.4,
     dict(A=5.0,B=4.0,C=3.5,D=3.0,E=4.5,F=4.5,G=4.75,H=3.75,I=3.25,J=3.5,K=4.25)),
    ("[5.5] THREE TRUTHS", "landauer", 17.6,
     dict(A=0.0,B=1.25,C=3.0,D=0.25,E=3.0,F=2.0,G=3.25,H=1.75,I=0.25,J=1.0,K=1.5)),
    ("[5.5] THREE TRUTHS", "entropy", 16.3,
     dict(A=0.0,B=1.5,C=2.25,D=0.0,E=3.0,F=1.0,G=3.25,H=2.0,I=0.25,J=1.25,K=2.0)),
    ("[5.5] THREE TRUTHS", "finetuning", 15.4,
     dict(A=0.0,B=1.25,C=2.5,D=0.25,E=2.25,F=1.25,G=2.75,H=2.0,I=0.25,J=1.25,K=1.5)),
    ("[5.5] THREE TRUTHS", "propcosmos", 13.0,
     dict(A=0.0,B=1.5,C=2.0,D=0.0,E=2.0,F=1.5,G=2.0,H=2.0,I=0.0,J=0.0,K=1.5)),
    ("[7.5] Psychology_Crisis", "12-Step_vs_Secular_CBT_Analysis", 83.6,
     dict(A=8.0,B=8.5,C=7.0,D=7.5,E=7.5,F=7.75,G=7.75,H=7.25,I=6.5,J=7.0,K=6.75)),
    ("[7.5] Psychology_Crisis", "Secular_Emotional_Wellness_Guide", 80.1,
     dict(A=7.0,B=8.0,C=7.0,D=7.0,E=7.5,F=7.5,G=7.25,H=7.0,I=6.5,J=7.0,K=6.5)),
    ("[7.5] Psychology_Crisis", "Architecture_of_Emotional_Autonomy", 79.4,
     dict(A=7.0,B=7.75,C=7.0,D=6.5,E=7.5,F=7.5,G=7.75,H=7.0,I=6.5,J=6.75,K=6.5)),
    ("[7.5] Psychology_Crisis", "00_OVERLAP_The_Unified_Crisis", 52.2,
     dict(A=5.0,B=5.0,C=5.0,D=4.0,E=5.0,F=4.75,G=5.0,H=4.5,I=3.75,J=4.5,K=4.5)),
    ("[7.5] Psychology_Crisis", "01_Psychology_Audit", 48.8,
     dict(A=5.0,B=4.75,C=4.0,D=4.0,E=4.5,F=4.5,G=4.75,H=4.25,I=3.5,J=4.25,K=4.5)),
    ("[7.5] LAYER_1_LOGIC", "04_The_Moral_Paradox", 79.9,
     dict(A=7.0,B=8.0,C=7.0,D=7.0,E=7.0,F=7.5,G=7.25,H=7.0,I=6.5,J=7.0,K=7.0)),
    ("[7.5] LAYER_1_LOGIC", "03_Trans-Domain_Structural_Invariants", 79.5,
     dict(A=7.0,B=7.75,C=7.0,D=7.0,E=7.0,F=7.5,G=6.75,H=7.0,I=6.5,J=7.0,K=7.5)),
    ("[7.5] LAYER_1_LOGIC", "Crisis_of_Intelligibility_Axiom_of_Logos", 61.2,
     dict(A=5.5,B=6.5,C=5.0,D=5.0,E=6.0,F=5.5,G=6.0,H=5.5,I=4.5,J=5.0,K=5.5)),
    ("[7.5] LAYER_1_LOGIC", "01_Informational_Ground", 60.7,
     dict(A=5.5,B=6.5,C=5.0,D=5.0,E=6.0,F=5.5,G=6.0,H=5.0,I=4.5,J=5.0,K=5.5)),
    ("[7.5] LAYER_1_LOGIC", "02_Crisis_of_Intelligibility", 59.6,
     dict(A=5.0,B=6.5,C=5.0,D=5.0,E=5.5,F=5.25,G=5.75,H=5.25,I=4.5,J=5.25,K=5.5)),
    ("[7.5] LAYER_1_LOGIC", "02_Relational_Primitives", 48.0,
     dict(A=5.5,B=3.75,C=4.0,D=3.0,E=4.5,F=5.5,G=5.5,H=4.0,I=3.5,J=4.0,K=5.0)),
    ("[7.0] Submissions", "Original_Triad_Outline", 77.8,
     dict(A=7.0,B=7.75,C=7.25,D=6.0,E=7.25,F=7.0,G=7.25,H=7.0,I=6.0,J=6.5,K=7.0)),
    ("[7.0] Submissions", "Formal_Theory_Presentation_Strategy", 69.2,
     dict(A=7.0,B=7.0,C=6.0,D=6.0,E=6.0,F=6.5,G=6.0,H=5.5,I=5.5,J=5.5,K=6.5)),
    ("[7.0] Submissions", "Original_Psychology_Draft", 68.4,
     dict(A=6.5,B=7.0,C=6.0,D=5.5,E=6.0,F=6.5,G=6.5,H=5.5,I=5.5,J=5.5,K=6.5)),
    ("[7.0] Submissions", "MANUSCRIPT_Thermodynamics_of_Social_Collapse", 66.3,
     dict(A=6.5,B=6.75,C=6.0,D=5.5,E=6.0,F=6.5,G=6.0,H=5.5,I=4.75,J=5.0,K=6.0)),
    ("[7.0] Submissions", "Proposal_Relational_Coherence", 62.7,
     dict(A=6.5,B=6.5,C=5.0,D=5.0,E=6.0,F=5.5,G=6.0,H=5.0,I=5.0,J=5.0,K=6.0)),
    ("[7.0] Submissions", "MANUSCRIPT_The_Physics_of_Recovery", 62.6,
     dict(A=6.5,B=6.5,C=5.0,D=5.0,E=6.0,F=6.0,G=6.0,H=5.0,I=4.5,J=5.0,K=6.0)),
    ("[7.0] Submissions", "MANUSCRIPT_The_Trinity_Mechanism", 55.8,
     dict(A=5.5,B=5.75,C=5.0,D=4.0,E=5.5,F=5.5,G=5.75,H=4.5,I=3.5,J=4.5,K=5.25)),
    ("[7.0] Submissions", "MANUSCRIPT_The_Resurrection_Physics", 47.5,
     dict(A=5.5,B=3.75,C=4.0,D=3.0,E=5.0,F=5.0,G=5.0,H=4.0,I=3.5,J=4.0,K=4.5)),
    ("[7.0] Submissions", "Original_Social_Decline_Draft", 46.3,
     dict(A=3.0,B=4.75,C=4.0,D=4.0,E=4.5,F=4.5,G=4.75,H=4.0,I=4.0,J=4.0,K=4.25)),
    # [7.6] Protocols (avg 70.3)
    ("[7.6] Protocols", "P11-Protocols-Validation Final ALL", 75.2,
     dict(A=7.5,B=7.0,C=6.0,D=6.0,E=6.5,F=7.5,G=7.5,H=6.0,I=7.0,J=6.0,K=7.5)),
    ("[7.6] Protocols", "11_Experimental_Protocols", 68.6,
     dict(A=6.5,B=7.5,C=6.0,D=5.5,E=6.0,F=6.5,G=6.0,H=5.5,I=6.0,J=5.0,K=6.0)),
    ("[7.6] Protocols", "14_David_Effect_Protocol", 67.0,
     dict(A=6.5,B=6.5,C=6.0,D=5.5,E=6.0,F=7.0,G=6.5,H=5.5,I=4.8,J=5.5,K=6.0)),
    # [8.2] The_Great_Correction (avg 50.8)
    ("[8.2] The_Great_Correction", "Notes Gemini", 62.4,
     dict(A=6.5,B=6.5,C=5.0,D=5.0,E=5.5,F=6.0,G=6.0,H=5.2,I=4.5,J=5.0,K=6.0)),
    ("[8.2] The_Great_Correction", "Untitled", 49.7,
     dict(A=4.5,B=5.0,C=4.0,D=4.0,E=4.5,F=4.5,G=4.8,H=4.2,I=4.2,J=4.2,K=5.2)),
    ("[8.2] The_Great_Correction", "CHAPTER 2 THE GREAT CORRECTION", 40.4,
     dict(A=2.8,B=3.8,C=4.0,D=3.0,E=4.0,F=3.5,G=4.0,H=3.5,I=3.5,J=3.5,K=4.5)),
    # [7.7] Consciousness (avg 64.0, 6 of 7 scored — Consciousness quantum.md too large)
    ("[7.7] Consciousness", "Consciousness", 75.0,
     dict(A=7.5,B=7.0,C=7.25,D=6.0,E=7.0,F=7.0,G=7.25,H=6.0,I=5.5,J=6.0,K=6.5)),
    ("[7.7] Consciousness", "A Theophysical Meta-Analysis of Psychological Ontology", 70.0,
     dict(A=7.0,B=7.0,C=6.0,D=5.5,E=6.5,F=6.5,G=6.5,H=6.0,I=5.5,J=5.5,K=6.5)),
    ("[7.7] Consciousness", "Paper2_Consciousness_Bridge_EXPANDED", 65.7,
     dict(A=6.5,B=7.5,C=5.0,D=5.0,E=6.0,F=6.0,G=6.5,H=5.0,I=5.5,J=5.5,K=6.0)),
    ("[7.7] Consciousness", "Untitled_Consciousness", 61.5,
     dict(A=6.0,B=6.5,C=5.0,D=5.0,E=6.0,F=5.75,G=6.0,H=5.0,I=4.5,J=5.0,K=5.5)),
    ("[7.7] Consciousness", "Paper2_Consciousness_Bridge_CLEAN", 58.2,
     dict(A=5.0,B=6.5,C=5.0,D=4.0,E=5.5,F=5.5,G=5.75,H=4.75,I=4.5,J=5.0,K=6.0)),
    ("[7.7] Consciousness", "Untitled 1_Consciousness", 52.5,
     dict(A=6.0,B=5.0,C=4.5,D=4.0,E=5.0,F=5.5,G=5.0,H=4.5,I=3.5,J=3.75,K=4.5)),
    # [7.2] Logic (avg 54.8)
    ("[7.2] Logic", "08_LOG_04_The_Unitary_Trap", 60.8,
     dict(A=6.5,B=6.5,C=5.0,D=5.0,E=5.0,F=6.0,G=6.0,H=4.5,I=4.5,J=5.0,K=5.5)),
    ("[7.2] Logic", "06_LOG_03_The_Cupcake_Proof", 58.4,
     dict(A=5.0,B=6.0,C=5.0,D=5.0,E=5.5,F=5.25,G=5.75,H=5.0,I=4.5,J=5.0,K=5.25)),
    ("[7.2] Logic", "07_LOG_05_The_Wall_of_Defeated", 45.2,
     dict(A=4.5,B=4.0,C=4.0,D=3.0,E=4.5,F=4.5,G=4.75,H=4.0,I=3.5,J=3.75,K=4.25)),
    # [6.8] Moral_Decay (avg 69.5)
    ("[6.8] Moral_Decay", "Moral_Collapse_Framework", 80.8,
     dict(A=7.5,B=7.75,C=7.0,D=7.0,E=7.0,F=7.5,G=7.0,H=7.0,I=7.0,J=7.0,K=7.5)),
    ("[6.8] Moral_Decay", "The_Moral_Paradox_Ontological_Tensions", 79.0,
     dict(A=7.0,B=8.0,C=7.0,D=6.5,E=7.0,F=7.5,G=7.25,H=7.0,I=6.5,J=7.0,K=6.5)),
    ("[6.8] Moral_Decay", "THE COHERENCE METRIC", 70.5,
     dict(A=6.5,B=7.0,C=6.0,D=5.0,E=6.5,F=6.75,G=7.5,H=6.0,I=6.5,J=5.5,K=6.0)),
    ("[6.8] Moral_Decay", "THE COMPLETE SOCIAL DECLINE PAPER OUTLINE", 69.2,
     dict(A=7.0,B=6.75,C=6.0,D=5.5,E=6.0,F=6.5,G=6.5,H=5.5,I=6.0,J=5.5,K=6.5)),
    ("[6.8] Moral_Decay", "FORMAL_THESIS_Moral_Coherence_Analysis", 64.9,
     dict(A=6.5,B=7.0,C=5.5,D=5.25,E=6.0,F=6.0,G=6.0,H=5.0,I=5.0,J=5.0,K=6.0)),
    ("[6.8] Moral_Decay", "THE AMERICAN COHERENCE COLLAPSE", 63.0,
     dict(A=6.5,B=6.5,C=5.0,D=4.5,E=5.5,F=6.5,G=6.5,H=5.25,I=5.25,J=5.0,K=5.5)),
    ("[6.8] Moral_Decay", "LAUNCH_STRATEGY_AND_INTEGRATION_PLAN", 58.8,
     dict(A=5.0,B=6.0,C=5.0,D=5.0,E=5.5,F=5.5,G=5.75,H=5.25,I=4.5,J=4.75,K=5.5)),
    # [6.5] JS-SERIES (avg 54.2, 7 scored 1 error)
    ("[6.5] JS-SERIES", "AXIOM_STATUS_REPORT", 71.8,
     dict(A=6.5,B=7.5,C=6.0,D=6.5,E=6.5,F=6.75,G=6.5,H=6.0,I=5.5,J=6.5,K=6.0)),
    ("[6.5] JS-SERIES", "Trinity as quantum entanglement 3", 56.0,
     dict(A=4.5,B=6.5,C=5.0,D=4.0,E=5.0,F=5.5,G=6.0,H=4.5,I=3.5,J=4.75,K=6.0)),
    ("[6.5] JS-SERIES", "To My Fellow Intelligences", 54.1,
     dict(A=6.5,B=4.75,C=5.0,D=4.0,E=5.0,F=5.5,G=5.0,H=4.5,I=3.5,J=4.0,K=5.0)),
    ("[6.5] JS-SERIES", "The Transcendent Algorithm", 54.0,
     dict(A=7.5,B=5.0,C=4.0,D=4.0,E=5.0,F=5.5,G=5.0,H=4.5,I=3.5,J=4.0,K=5.0)),
    ("[6.5] JS-SERIES", "The-Physics-of-Resurrection-A-Deeper-Analysis", 53.8,
     dict(A=5.0,B=5.0,C=5.0,D=4.0,E=5.0,F=5.25,G=5.5,H=4.5,I=4.0,J=4.5,K=5.25)),
    ("[6.5] JS-SERIES", "JS-SERIES_GOLD_CONTENT_COMPILED", 51.8,
     dict(A=5.0,B=5.75,C=4.0,D=4.0,E=5.0,F=4.5,G=5.5,H=4.5,I=3.5,J=4.0,K=5.25)),
    ("[6.5] JS-SERIES", "The Physics of Resurrection 2", 38.0,
     dict(A=4.5,B=3.0,C=3.0,D=3.0,E=3.5,F=4.5,G=4.0,H=3.25,I=2.75,J=3.0,K=3.25)),
    # [7.0] Quantum_Bridge (avg 66.3)
    ("[7.0] Quantum_Bridge", "SESSION_SUMMARY", 70.7,
     dict(A=6.0,B=7.5,C=6.0,D=6.5,E=6.0,F=7.0,G=6.0,H=6.0,I=6.0,J=6.0,K=6.0)),
    ("[7.0] Quantum_Bridge", "BARRIER_1_OBSERVER_PROBLEM", 70.2,
     dict(A=6.5,B=7.5,C=6.0,D=5.0,E=6.5,F=6.0,G=6.5,H=6.0,I=6.0,J=6.0,K=7.0)),
    ("[7.0] Quantum_Bridge", "ALL_5_BARRIERS_STORY_VISUAL", 57.9,
     dict(A=4.5,B=6.5,C=5.0,D=4.5,E=5.0,F=5.0,G=5.5,H=5.0,I=5.0,J=5.0,K=6.0)),
    # [6.6] Normalized_Manuscript (avg 52.8 — book chapters, not standalone papers)
    ("[6.6] Normalized_Manuscript", "01_Chapter_1", 65.5,
     dict(A=5.5,B=7.5,C=6.0,D=5.0,E=6.0,F=5.75,G=6.5,H=5.25,I=4.5,J=5.75,K=6.25)),
    ("[6.6] Normalized_Manuscript", "11_Chapter_11", 62.3,
     dict(A=6.5,B=6.0,C=5.0,D=5.0,E=5.5,F=6.0,G=5.5,H=5.25,I=5.25,J=5.25,K=6.25)),
    ("[6.6] Normalized_Manuscript", "04_Chapter_4", 60.8,
     dict(A=6.5,B=6.0,C=5.0,D=5.0,E=5.5,F=5.5,G=5.75,H=5.25,I=4.5,J=5.0,K=5.5)),
    ("[6.6] Normalized_Manuscript", "03_Chapter_3", 59.5,
     dict(A=5.5,B=6.0,C=5.0,D=5.0,E=5.5,F=5.5,G=5.75,H=5.25,I=4.5,J=5.0,K=5.5)),
    ("[6.6] Normalized_Manuscript", "07_Chapter_7", 59.5,
     dict(A=6.5,B=6.5,C=5.0,D=4.0,E=5.5,F=5.5,G=5.5,H=5.0,I=4.5,J=5.0,K=5.0)),
    ("[6.6] Normalized_Manuscript", "00_Table_of_Contents", 59.1,
     dict(A=5.5,B=5.75,C=5.0,D=5.0,E=5.5,F=5.5,G=5.75,H=5.25,I=4.5,J=5.0,K=5.25)),
    ("[6.6] Normalized_Manuscript", "05_Chapter_5", 58.9,
     dict(A=5.0,B=6.0,C=5.0,D=5.0,E=5.5,F=5.25,G=5.75,H=5.25,I=4.5,J=5.25,K=5.5)),
    ("[6.6] Normalized_Manuscript", "09_Chapter_9", 54.1,
     dict(A=5.5,B=5.0,C=5.0,D=4.0,E=5.0,F=5.5,G=5.5,H=4.5,I=3.5,J=4.5,K=5.25)),
    ("[6.6] Normalized_Manuscript", "08_Chapter_8", 52.0,
     dict(A=5.5,B=5.0,C=4.0,D=4.0,E=5.0,F=5.5,G=5.5,H=4.5,I=3.5,J=4.0,K=5.0)),
    ("[6.6] Normalized_Manuscript", "06_Chapter_6", 51.2,
     dict(A=4.5,B=5.0,C=5.0,D=4.0,E=5.0,F=4.5,G=5.0,H=4.5,I=3.5,J=4.0,K=5.0)),
    ("[6.6] Normalized_Manuscript", "12_Chapter_12", 51.0,
     dict(A=5.0,B=4.75,C=4.0,D=4.0,E=5.0,F=5.0,G=5.0,H=4.5,I=4.0,J=4.5,K=5.0)),
    ("[6.6] Normalized_Manuscript", "10_Chapter_10", 47.4,
     dict(A=5.5,B=3.75,C=4.0,D=3.0,E=4.5,F=5.5,G=5.0,H=4.0,I=3.5,J=4.0,K=4.5)),
    ("[6.6] Normalized_Manuscript", "00_Prologue", 43.2,
     dict(A=3.0,B=4.75,C=4.0,D=3.0,E=4.5,F=4.0,G=4.5,H=3.5,I=3.5,J=3.5,K=4.25)),
    ("[6.6] Normalized_Manuscript", "00_Tone_Guide", 15.5,
     dict(A=0.0,B=1.5,C=2.0,D=0.5,E=2.0,F=2.0,G=2.0,H=2.0,I=0.0,J=2.0,K=2.0)),
    # [6.2] 07_Apologetics (avg 62.3, 5 scored 3 errors)
    ("[6.2] Apologetics", "Church_Debris_Audit_Denominational_Fragmentation", 71.4,
     dict(A=7.0,B=8.0,C=6.0,D=6.25,E=6.0,F=6.5,G=6.0,H=6.0,I=5.5,J=6.0,K=6.0)),
    ("[6.2] Apologetics", "A-GUIDE-TO-GOOD-BIBLE-READING", 67.2,
     dict(A=6.0,B=7.0,C=6.0,D=5.5,E=6.5,F=6.0,G=6.5,H=5.5,I=5.5,J=5.25,K=5.5)),
    ("[6.2] Apologetics", "AI free will divine benevolence", 66.5,
     dict(A=6.5,B=7.0,C=6.0,D=5.0,E=6.0,F=6.5,G=6.5,H=5.5,I=4.5,J=5.5,K=6.0)),
    ("[6.2] Apologetics", "The-Perversion-of-the-Word", 58.1,
     dict(A=5.0,B=6.0,C=5.0,D=4.5,E=5.5,F=5.5,G=5.75,H=5.25,I=4.5,J=4.75,K=5.25)),
    ("[6.2] Apologetics", "Identity-and-worth", 48.4,
     dict(A=5.0,B=5.0,C=4.0,D=3.75,E=4.5,F=4.5,G=4.75,H=4.25,I=3.5,J=3.75,K=4.25)),
    # [6.2] Moral_Decline_Series_Substack (avg 63.9)
    ("[6.2] Substack", "10_10_The_Declaration_Severing_from_the_Source", 72.5,
     dict(A=7.0,B=8.0,C=6.0,D=6.25,E=6.0,F=6.5,G=7.0,H=6.0,I=5.5,J=6.0,K=6.5)),
    ("[6.2] Substack", "02_10_Anatomy_of_a_Phase_Transition", 69.2,
     dict(A=6.5,B=7.0,C=6.0,D=6.0,E=6.5,F=6.0,G=6.5,H=6.0,I=5.5,J=5.75,K=5.5)),
    ("[6.2] Substack", "03_10_Semantic_Precursor_Language_Fails_First", 68.7,
     dict(A=6.5,B=7.0,C=6.0,D=5.5,E=6.5,F=6.0,G=6.5,H=6.0,I=5.5,J=6.0,K=5.5)),
    ("[6.2] Substack", "05_10_Spiritual_Psychological_Collapse", 66.2,
     dict(A=6.5,B=7.5,C=6.0,D=5.0,E=6.0,F=6.0,G=6.5,H=5.5,I=4.5,J=5.0,K=5.5)),
    ("[6.2] Substack", "08_10_Economic_Physical_Lag", 65.5,
     dict(A=6.5,B=7.5,C=6.0,D=5.0,E=6.0,F=6.0,G=6.0,H=5.5,I=4.5,J=5.0,K=5.0)),
    ("[6.2] Substack", "09_10_The_Constitutional_Unraveling", 61.8,
     dict(A=6.0,B=7.25,C=5.0,D=5.0,E=5.5,F=5.5,G=5.75,H=5.25,I=4.5,J=5.0,K=5.25)),
    ("[6.2] Substack", "04_10_Cognitive_Decline_SAT_Turnover", 59.4,
     dict(A=5.0,B=6.75,C=5.0,D=5.0,E=5.5,F=5.5,G=5.75,H=5.25,I=4.5,J=4.75,K=4.75)),
    ("[6.2] Substack", "07_10_Familial_Disintegration_Divorce_Revolution", 59.1,
     dict(A=5.0,B=6.75,C=5.0,D=5.0,E=5.5,F=5.25,G=5.5,H=5.25,I=4.5,J=4.5,K=5.25)),
    ("[6.2] Substack", "06_10_Moral_Collapse_Violence_Distrust", 58.6,
     dict(A=5.0,B=6.5,C=5.0,D=4.5,E=5.5,F=5.25,G=5.75,H=5.25,I=4.5,J=4.75,K=5.25)),
    ("[6.2] Substack", "01_10_Conclusion_Predictive_Framework", 57.6,
     dict(A=5.0,B=5.75,C=5.0,D=5.0,E=5.25,F=5.25,G=5.5,H=5.0,I=4.5,J=5.0,K=5.25)),
    # [5.6] Scientific method (avg 50.7 — mix of methodology papers and operational dashboards)
    ("[5.6] Scientific method", "04_STUDY_Comparative_Evaluation", 70.9,
     dict(A=6.5,B=7.5,C=6.5,D=5.75,E=6.0,F=6.5,G=6.5,H=5.5,I=6.0,J=6.25,K=6.0)),
    ("[5.6] Scientific method", "03_METRICS_Defense_Depth", 66.6,
     dict(A=6.5,B=6.75,C=6.0,D=5.0,E=6.0,F=6.0,G=6.5,H=5.5,I=5.5,J=5.75,K=5.5)),
    ("[5.6] Scientific method", "04_APPLICATION_Theophysics_Audit", 66.5,
     dict(A=6.5,B=6.5,C=6.0,D=5.0,E=6.0,F=6.0,G=6.5,H=5.5,I=5.5,J=5.75,K=6.0)),
    ("[5.6] Scientific method", "03_METRICS_Theory_Evaluation", 66.3,
     dict(A=6.5,B=6.5,C=6.0,D=5.0,E=6.0,F=6.0,G=6.0,H=5.5,I=5.5,J=6.0,K=6.0)),
    ("[5.6] Scientific method", "01_RESEARCH_PROMPTS_Fragmentation_Data", 59.0,
     dict(A=5.0,B=6.0,C=5.5,D=4.5,E=5.5,F=5.25,G=5.75,H=5.25,I=4.5,J=5.25,K=5.25)),
    ("[5.6] Scientific method", "02_METHODOLOGY_AIRLOCK", 51.2,
     dict(A=5.5,B=5.0,C=5.0,D=3.5,E=5.0,F=5.0,G=5.5,H=4.0,I=3.25,J=3.5,K=4.5)),
    ("[5.6] Scientific method", "05_SYNTHESIS_Architectural_Intent", 48.8,
     dict(A=3.5,B=5.5,C=5.0,D=3.0,E=5.0,F=5.25,G=5.0,H=4.0,I=3.0,J=3.5,K=5.0)),
    ("[5.6] Scientific method", "00_MANIFESTO_The_Scientific_Method_Redux", 44.4,
     dict(A=3.0,B=4.5,C=4.0,D=3.0,E=4.5,F=4.5,G=4.75,H=4.0,I=3.5,J=4.0,K=4.5)),
    ("[5.6] Scientific method", "SCI_02_Manifesto_Public", 34.5,
     dict(A=2.0,B=3.75,C=3.0,D=2.0,E=4.0,F=3.75,G=4.0,H=3.0,I=2.5,J=3.0,K=3.5)),
    ("[5.6] Scientific method", "SciMethod_Dashboard", 28.2,
     dict(A=0.0,B=3.0,C=4.0,D=0.5,E=4.0,F=3.0,G=4.5,H=3.25,I=0.5,J=2.5,K=3.0)),
    ("[5.6] Scientific method", "Scientific theory_dashboard", 21.4,
     dict(A=0.0,B=1.75,C=3.25,D=0.5,E=3.25,F=2.5,G=3.5,H=2.25,I=0.5,J=1.5,K=2.5)),
    # MASTER_EQUATION (avg 49.7, 4 scored — 5 ERR due to heavy math notation)
    ("[MASTER] Master Equation", "Master Eq Spiritual components", 62.1,
     dict(A=5.5,B=7.0,C=5.75,D=5.5,E=5.5,F=5.5,G=5.5,H=4.5,I=5.0,J=5.0,K=5.25)),
    ("[MASTER] Master Equation", "STRUCTURAL_ANALYSIS_RESULTS", 60.4,
     dict(A=6.5,B=6.5,C=5.0,D=5.0,E=5.5,F=6.25,G=6.0,H=4.5,I=3.5,J=5.25,K=5.0)),
    ("[MASTER] Master Equation", "Z2_Mirror_Pairs_Symmetry_Table", 49.9,
     dict(A=4.5,B=4.75,C=4.0,D=4.5,E=5.0,F=4.5,G=5.0,H=4.5,I=3.5,J=4.0,K=5.0)),
    ("[MASTER] Master Equation", "MA-00_Master-Equation", 26.5,
     dict(A=0.0,B=2.75,C=2.75,D=1.25,E=2.75,F=3.5,G=3.75,H=2.5,I=2.25,J=2.5,K=3.25)),
]

def grade(s):
    if s>=90: return "A"
    if s>=85: return "A-"
    if s>=80: return "B"
    if s>=75: return "C+"
    if s>=65: return "C"
    if s>=55: return "D"
    return "F"

sec_cols = [f"Sec_{s}" for s in SECTIONS]
fields   = ["Collection", "Paper", "CDCM_Score", "Grade"] + sec_cols

rows = []
for col, paper, score, secs in sorted(PAPERS, key=lambda x: x[2], reverse=True):
    row = {"Collection": col, "Paper": paper, "CDCM_Score": score, "Grade": grade(score)}
    for s in SECTIONS:
        row[f"Sec_{s}"] = secs.get(s, "")
    rows.append(row)

# Write CSV
csv_path = OUTPUT_DIR / "CDCM_MASTER_ALL_PAPERS.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print(f"CSV: {csv_path}  ({len(rows)} papers)")

# Write XLSX
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter

    def fill(s):
        if s>=80: return "27AE60"
        if s>=70: return "E67E22"
        if s>=55: return "E74C3C"
        return "95A5A6"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "CDCM Scores"
    hf = PatternFill("solid", fgColor="1A252F")
    hfont = Font(color="FFFFFF", bold=True, size=9)
    for ci, h in enumerate(fields, 1):
        c = ws.cell(row=1, column=ci, value=h)
        c.fill = hf; c.font = hfont
        c.alignment = Alignment(horizontal="center")

    for ri, row in enumerate(rows, 2):
        sv = float(row["CDCM_Score"])
        for ci, field in enumerate(fields, 1):
            val = row.get(field)
            if field not in ("Collection","Paper","Grade"):
                try: val = float(val) if val not in (None,"") else None
                except: val = None
            c = ws.cell(row=ri, column=ci, value=val)
            if field == "CDCM_Score":
                c.fill = PatternFill("solid", fgColor=fill(sv))
                c.font = Font(bold=True, color="FFFFFF", size=9)
            elif field in sec_cols and val is not None:
                v = float(val)
                if v>=7:   c.fill = PatternFill("solid", fgColor="D5F5E3")
                elif v>=5: c.fill = PatternFill("solid", fgColor="FDEBD0")
                else:      c.fill = PatternFill("solid", fgColor="FADBD8")

    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 52
    ws.column_dimensions["C"].width = 12
    ws.column_dimensions["D"].width = 7
    for i in range(5, len(fields)+1):
        ws.column_dimensions[get_column_letter(i)].width = 7
    ws.freeze_panes = "E2"
    xlsx_path = OUTPUT_DIR / "CDCM_MASTER_ALL_PAPERS.xlsx"
    wb.save(xlsx_path)
    print(f"XLSX: {xlsx_path}")
except ImportError:
    print("openpyxl not installed")

print(f"\n{'Score':>7}  {'Grade':>5}  {'Collection':<28}  Paper")
print("-"*85)
for r in rows:
    if r['CDCM_Score'] > 0:
        print(f"  {r['CDCM_Score']:>5.1f}  {r['Grade']:>5}  {r['Collection']:<28}  {r['Paper']}")
