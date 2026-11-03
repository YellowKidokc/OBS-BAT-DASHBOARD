# Taxonomy Registry Files

This folder now holds four registry files used by YAML frontmatter, Excel mapping, and lint checks:

- `PROJECT_REGISTRY.csv`: project IDs and project metadata.
- `TAG_REGISTRY_MASTER.csv`: approved tags, axis, usage rules, and stable UUIDs.
- `TARGET_WORDS_HIERARCHY.csv`: target words with hierarchical keys, domain buckets, and UUIDs.
- `CLASSIFICATION_LEVELS.csv`: enum-style values for `type`, `layer`, `status`, `claim_role`, quality bands, and related fields.

## How to use

1. In YAML, reference IDs from registries:
   - `project_id` and `project_ids` must exist in `PROJECT_REGISTRY.csv`.
   - `tags` should come from `TAG_REGISTRY_MASTER.csv`.
   - classification fields (for example `status`, `maturity`, `claim_role`) should come from `CLASSIFICATION_LEVELS.csv`.
2. For term-heavy notes, map `target_words` and `target_word_uuids` using `TARGET_WORDS_HIERARCHY.csv`.
3. Keep IDs stable. Rename display text when needed, but do not rotate UUIDs unless creating a new entity.

## Regeneration

Regenerate all three non-project registries with:

```bash
python O:/_Theophysics_v3/00_SYSTEM/01_ENGINE/scripts/generate_taxonomy_registries.py
```

This script is deterministic and uses UUIDv5, so repeated runs preserve IDs for the same keys.


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

