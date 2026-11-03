---
title: "Evidence Engine Operating Spec"
status: canonical-draft
created: 2026-03-09
---

# Purpose
Create a path-independent claim-evidence system that survives tool changes, file moves, and AI session loss.

# Core Model
- Claims are entities (`claim_id`)
- Evidence items are entities (`evidence_id`)
- Links are explicit assertions (`link_id`) connecting claim <-> evidence
- Files are artifacts and can move without breaking links

# Non-Negotiable Rules
1. IDs are permanent. Paths are metadata.
2. No claim exists without a `claim_id`.
3. No evidence exists without an `evidence_id`.
4. No support assertion exists outside the switchboard.
5. Every link has relation + confidence + rationale.

# Minimal Tables
1. Claims Register
- `claim_id, domain, claim_short, claim_text, status, created_at`

2. Evidence Register
- `evidence_id, evidence_type, title, source_path, source_hash, extracted_at`

3. Linkboard (Switchboard)
- `link_id, claim_id, evidence_id, relation, weight_0_1, confidence_0_1, rationale, reviewed_at`

4. Artifact Map
- `artifact_id, evidence_id, source_path, source_hash, last_seen_at`

# ID Scheme
- Claims: `CLM-{DOMAIN}-{NNN}`
- Evidence: `EVD-{TYPE}-{NNN}`
- Links: `LNK-{NNNN}`

# Workflow
1. Ingest exports into inbox.
2. Normalize rows into claims/evidence registers.
3. Generate or update stable IDs.
4. Wire links in linkboard.
5. Publish report: strongest-supported claims, weakest links, open wounds.

# Done Definition
- 100% of claims have IDs
- 100% of evidence rows have IDs + hashes
- 100% of claim/evidence assertions are in linkboard
- report generated with top supports + top contradictions + unresolved claims
