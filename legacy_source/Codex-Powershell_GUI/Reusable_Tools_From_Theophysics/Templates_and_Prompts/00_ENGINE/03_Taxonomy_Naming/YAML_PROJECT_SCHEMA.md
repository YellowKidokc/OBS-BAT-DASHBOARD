# YAML Project Schema

## Purpose
Link every claim-bearing note to one or more projects while enforcing:
- `claim_role`
- `evidence_links`
- `falsification_test`

## Required Project Fields
```yaml
project_id: PRJ-THEO-0001
project_ids: [PRJ-THEO-0001, PRJ-THEO-0002]
project_role: core
project_stage: drafting
project_priority: high
```

## Core Claim Fields
```yaml
claim_role: hypothesis
evidence_links: []
falsification_test: ""
```

## Rules
1. If `claim_role` exists, note must include at least one valid project ID.
2. Every project ID must exist in `PROJECT_REGISTRY.csv`.
3. `project_role` allowed values:
   - `core`
   - `support`
   - `reference`
4. `project_stage` and `project_priority` should match values used in the registry workflow.
5. `evidence_links` should be present for all claim-bearing notes.
6. `falsification_test` should be non-empty for hypothesis-like claims.

## Notes
- Keep `project_id` as the primary project.
- Use `project_ids` for secondary project links.
- Keep IDs stable across renames.


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

