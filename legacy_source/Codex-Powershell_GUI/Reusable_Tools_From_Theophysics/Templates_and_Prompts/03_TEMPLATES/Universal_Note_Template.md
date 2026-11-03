---
# ---------------------------------------------------------
# CORE (Stable)
# ---------------------------------------------------------
uuid: "{{date:YYYYMMDDHHmmss}}"
title: "{{title}}"
status: draft # draft, review, canonical, archive
epistemic_role: Claim # Axiom, Definition, Claim, Hypothesis, Evidence, Theory, Law
primary_domain: Physics # The dominant constraint family

# ---------------------------------------------------------
# CLASSIFICATION (Lenses)
# ---------------------------------------------------------
classification:
  domains: [Physics, Mathematics, Information]
  ckg_tier: 2 # 1:Foundations, 2:Propositions, 3:Constraints, 4:Support, 5:Linkages
  statistical_rating: 5.0 # (5.0 - 9.0)

# ---------------------------------------------------------
# EVALUATION (Maturity Metrics)
# ---------------------------------------------------------
ckg_evaluation:
  subscores:
    clarity: 5
    formality: 5
    evidence: 5
    testability: 5
    integration: 5
    risk_control: 5
  raw_score: 30
  final_score: 6.2 # Auto-calculated: 5.0 + 0.4 * (raw/10)
  last_evaluated: "{{date:YYYY-MM-DD}}"
  evaluator_version: "1.1"

# ---------------------------------------------------------
# MODULES (Optional/Expandable)
# ---------------------------------------------------------
modules:
  ai:
    processing_prompt: |
      You are evaluating structural completeness... (Paste full contract from 00_OS/04_AI_CONTRACTS here)
  trace:
    semantic_trace: [] # Stores machine-readable span-level justifications
---

# {{title}}

## Summary
> [Short description of the unit]

## Content
{{cursor}}

## Links
- **Source:** [[Source Paper or Thread]]
- **Parent CKG:** OVERVIEW
- **Domain MOC:** Primary_Domain
---


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

