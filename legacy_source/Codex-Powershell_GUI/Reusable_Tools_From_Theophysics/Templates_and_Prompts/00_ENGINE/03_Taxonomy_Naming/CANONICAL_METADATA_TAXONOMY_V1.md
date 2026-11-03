# Canonical Metadata Taxonomy v1

Location: 00_ENGINE/03_Taxonomy_Naming

## Rule of separation
- `tag` = broad grouping/filtering
- `field` = stable property/state
- `edge` = relationship between entities

## 1) Tag Families (coarse navigation only)
Keep tags controlled and small.

Allowed families:
- `type/*` (paper, note, axiom, claim, evidence, dashboard)
- `domain/*` (physics, theology, mathematics, consciousness, information-theory)
- `pillar/*` (physics, theology, mathematics, consciousness, information-theory, philosophy)
- `series/*` (logos-papers, genesis-to-quantum, etc.)
- `workflow/*` (drafting, review, validation, publish)
- `audience/*` (general, technical, academic)

Disallowed patterns:
- Free-form one-off tags for state (`ready`, `approved`, `high-risk`) -> use fields.
- Relationship tags (`depends-on-A1.3`) -> use edges.

## 2) Fields (stable typed metadata)

### Paper-level (required)
- `uuid: string`
- `title: string`
- `type: paper|note|axiom|claim|evidence|dashboard`
- `series: string`
- `paper_number: int|null`
- `status: draft|active|review|final|archived`
- `created: YYYY-MM-DD`
- `updated: YYYY-MM-DD`
- `file_path: string`

### Review / Validation
- `review_status: unreviewed|ai-reviewed|human-reviewed|approved|rejected`
- `readiness_score: number (0-100)`
- `publication_eligible: true|false`
- `risk_level: low|medium|high|critical`
- `confidence_tier: low|medium|high`

### Claim-level (when present)
- `claim_id: string`
- `claim_type: theorem|hypothesis|axiom|definition|observation|inference`
- `evidence_count: int`
- `contradiction_open: true|false`
- `stress_test_status: not-started|in-progress|passed|failed`

### AI provenance
- `ai_processed: true|false`
- `ai_model: string`
- `ai_run_id: string`
- `ai_generated_at: ISO datetime`

## 3) Edges (relationships)
Use explicit arrays (or sidecar graph table) instead of tags.

Core edge types:
- `depends_on`
- `supports`
- `contradicts`
- `extends`
- `tests`
- `falsifies`
- `derived_from`
- `replaces`
- `bridges`

Example edge block:

```yaml
edges:
  depends_on: ["A1.3", "D1.1"]
  supports: ["CLM-00231"]
  contradicts: ["CLM-00988"]
```

## 4) Minimal frontmatter template
```yaml
---
uuid: ""
title: ""
type: paper
series: ""
paper_number: null
status: draft
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"

# Coarse navigation only
tags:
  - type/paper
  - domain/physics
  - pillar/physics

# Stable state fields
review_status: unreviewed
readiness_score: 0
publication_eligible: false
risk_level: medium
confidence_tier: medium

# Optional claim metadata
claim_id: ""
claim_type: ""
evidence_count: 0
contradiction_open: false
stress_test_status: not-started

# Provenance
ai_processed: false
ai_model: ""
ai_run_id: ""
ai_generated_at: ""

# Graph relationships
edges:
  depends_on: []
  supports: []
  contradicts: []
  extends: []
  tests: []
  falsifies: []
  derived_from: []
  replaces: []
  bridges: []
---
```

## 5) Enforcement guidance
- If a value can change over lifecycle state -> `field`.
- If it names another node -> `edge`.
- If it is only for broad filtering/search -> `tag`.

## 6) Migration priority
1. Freeze tag families.
2. Move status/risk/readiness out of tags into fields.
3. Convert relationship tags into `edges`.
4. Keep YAML human-readable; move heavy machine metadata to sidecar JSON when needed.
