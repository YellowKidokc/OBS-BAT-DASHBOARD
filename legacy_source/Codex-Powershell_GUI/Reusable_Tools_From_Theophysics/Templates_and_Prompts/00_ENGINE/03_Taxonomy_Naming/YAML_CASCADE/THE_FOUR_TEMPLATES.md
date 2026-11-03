# THE FOUR SCIENTIFIC TEMPLATES
## ARCHITECTURE: David Lowe & Opus
## IMPLEMENTATION: Gemini (Friendship Service)

Every scientific document is a structural combination of four fundamental moves:
**ESTABLISH**, **DERIVE**, **CHALLENGE**, and **CONNECT**.

This is the unified schema. It governs the YAML frontmatter for Obsidian, the output JSON for the OpenAI Vault Rater, and the rhetorical structure of every Logos Paper.

---

### THE UNIVERSAL SPINE (Level 1 & 3)
Always present, regardless of type.

```yaml
# LEVEL 1 � Context & Alignment
type: ESTABLISH | DERIVE | CHALLENGE | CONNECT
domain: [physics, theology, consciousness, moral, cross-domain, primordial]
law_alignment: [1-10]
status: [draft, tested, canonical, contested]

# ... [Level 2 activates here based on Type] ...

# LEVEL 3 � The Bottom Line
result: \"\"
vulnerability: \"\"
unlocks: \"\"
```

---

### TYPE 1: ESTABLISH (Ground + Declare)
\"Here is something new. Here is why it survives.\"
- **Use Case:** Axioms, core definitions, opening salvos.
- **Level 2 Activation:**
```yaml
death_conditions_survived: [] # [Self-Refutation, Infinite Regress, Empirical Contradiction, Logical Incoherence]
propagation_test_result: \"\"   # Does it survive Q0-Q12?
what_should_kill_it: \"\"       # The falsification criteria.
```

### TYPE 2: DERIVE (Chain)
\"From X, we get Y. Here's every link.\"
- **Use Case:** Theorems, proofs, Maxwell-style derivations.
- **Level 2 Activation:**
```yaml
source_nodes: []             # The established Axioms this relies on.
chain: \"\"                    # The logical steps.
weakest_link: \"\"             # The point most likely to snap under stress.
downstream_if_breaks: \"\"     # What dies if this fails?
```

### TYPE 3: CHALLENGE (Attack)
\"Here's what should kill this. Here's what happened when we tried.\"
- **Use Case:** Adversarial reviews, steelman objections, peer-review documents.
- **Level 2 Activation:**
```yaml
target_node: \"\"              # What are we attacking?
attack_vector: \"\"            # The specific methodology of the attack.
survived: true | false
damage_report: \"\"            # What broke, what held?
```

### TYPE 4: CONNECT (Bridge + Anchor)
\"These two things that shouldn't relate, do. Here's the shared structure.\"
- **Use Case:** Genesis-to-Quantum mappings, Fitts/Epstein analysis, Cross-Domain papers.
- **Level 2 Activation:**
```yaml
domain_a: \"\"                 # e.g., Theology (Genesis)
domain_b: \"\"                 # e.g., Physics (Quantum Mechanics)
isomorphism: \"\"              # The identical logical architecture.
constrains_predictions: true | false
empirical_anchor: \"\"         # The physical signature of the connection.
```



|                                      |                         |                      |            |            |           |                                      |            |
| ------------------------------------ | ----------------------- | -------------------- | ---------- | ---------- | --------- | ------------------------------------ | ---------- |
| classification_uuid                  | classification_group    | classification_value | sort_order | is_default | is_active | description                          | updated_on |
| bfbcd3c3-2c5f-5e77-ae93-6dbbf97eca50 | cds_zone                | publish              | 1          | FALSE      | TRUE      | Ready for publication workflow       | 2/16/2026  |
| 357359e8-ba3b-559a-a1bf-8e0243058121 | cds_zone                | refine               | 2          | FALSE      | TRUE      | Refine and recheck                   | 2/16/2026  |
| 67d75114-4b3e-5593-9967-9323f4fbeac5 | cds_zone                | triage               | 3          | FALSE      | TRUE      | Needs focused remediation            | 2/16/2026  |
| df8990e7-aa51-5227-8f5e-22a1e96a6cef | cds_zone                | archive              | 4          | FALSE      | TRUE      | Archive or retire                    | 2/16/2026  |
| 145f16a6-ee8f-53dc-82ba-97e413d44527 | ckg_tier_classification | T1                   | 1          | FALSE      | TRUE      | Tier 1                               | 2/16/2026  |
| f3f4ab84-4554-5229-b6f7-824fa37a3fe0 | ckg_tier_classification | T2                   | 2          | FALSE      | TRUE      | Tier 2                               | 2/16/2026  |
| 6bb699bf-76f7-5701-a523-1cb7f1d104cd | ckg_tier_classification | T3                   | 3          | FALSE      | TRUE      | Tier 3                               | 2/16/2026  |
| 1e1f66e9-306b-5716-ba66-4234520dd9ab | ckg_tier_classification | T4                   | 4          | FALSE      | TRUE      | Tier 4                               | 2/16/2026  |
| a186a8db-8f57-58e2-86fb-4fa52a7e32b7 | ckg_tier_classification | T5                   | 5          | FALSE      | TRUE      | Tier 5                               | 2/16/2026  |
| 5baf0a7b-66cb-5465-ac96-5ea99b44b8af | claim_role              | axiom                | 1          | FALSE      | TRUE      | Foundational claim                   | 2/16/2026  |
| f14eb506-ceb5-5698-a166-475fcf82b339 | claim_role              | definition           | 2          | FALSE      | TRUE      | Definition with boundaries           | 2/16/2026  |
| e9740978-ea4c-51da-bf56-4965e0d6a5d3 | claim_role              | lemma                | 3          | FALSE      | TRUE      | Intermediate proposition             | 2/16/2026  |
| dde02ecc-a69c-5229-ab94-9be662cabda6 | claim_role              | hypothesis           | 4          | FALSE      | TRUE      | Testable claim                       | 2/16/2026  |
| 9fb8b4fc-6e89-58d0-917d-ae944b0057d3 | claim_role              | operationalization   | 5          | FALSE      | TRUE      | How a variable is measured           | 2/16/2026  |
| 5b2b1c82-633e-5ed1-8914-55a95ee7077f | claim_role              | dataset_fact         | 6          | FALSE      | TRUE      | Fact directly from dataset           | 2/16/2026  |
| 422f0710-a9c6-52b0-b60e-e423ccfffad2 | claim_role              | evidence_extract     | 7          | FALSE      | TRUE      | Verbatim extract from source         | 2/16/2026  |
| 291b85d1-8aaa-566f-9325-03fa290f68cc | claim_role              | result               | 8          | FALSE      | TRUE      | Computed or observed outcome         | 2/16/2026  |
| 6f510329-d34e-564b-80c0-8219795188e3 | claim_role              | interpretation       | 9          | FALSE      | TRUE      | Interpretation of results            | 2/16/2026  |
| ac2c6e21-a707-5f5e-84ee-ec412a6cdb21 | claim_role              | prediction           | 10         | FALSE      | TRUE      | Forward-looking claim                | 2/16/2026  |
| ec0ef792-2649-506e-bbaa-00e84858ace3 | claim_role              | observation          | 11         | FALSE      | TRUE      | Observed pattern                     | 2/16/2026  |
| cebe1408-5c9f-51e9-9853-0819872287ce | claim_strength          | proven               | 1          | FALSE      | TRUE      | Strongly established                 | 2/16/2026  |
| 60414818-99e9-5c0c-9b67-01ce6a9bfbbf | claim_strength          | strong               | 2          | FALSE      | TRUE      | Strong support                       | 2/16/2026  |
| 107fb7fb-b24c-5401-83ca-763ed0afca3e | claim_strength          | moderate             | 3          | FALSE      | TRUE      | Moderate support                     | 2/16/2026  |
| 08d01009-5b1f-53af-9dc9-b085f9d594ae | claim_strength          | weak                 | 4          | FALSE      | TRUE      | Weak support                         | 2/16/2026  |
| 5ad4bb98-12ee-55ea-9ca5-12e6fb9b1537 | claim_strength          | speculative          | 5          | FALSE      | TRUE      | Early exploration                    | 2/16/2026  |
| 4642a45d-8587-5be8-8ff4-67772a419e57 | constraint_logic_chain  | strong               | 1          | FALSE      | TRUE      | Strong logical chain                 | 2/16/2026  |
| b8f01bbc-0050-5dd5-8443-f0fbc1c2c4af | constraint_logic_chain  | moderate             | 2          | FALSE      | TRUE      | Moderate logical chain               | 2/16/2026  |
| 67fd2c41-1988-5bfa-91d3-ce517a31af62 | constraint_logic_chain  | weak                 | 3          | FALSE      | TRUE      | Weak logical chain                   | 2/16/2026  |
| ed4a9d54-4829-58e4-85cb-2419f40b1bde | layer                   | ai                   | 1          | FALSE      | TRUE      | AI collaboration layer               | 2/16/2026  |
| 7f60da69-894f-5766-8feb-f40a49aae0b0 | layer                   | system               | 2          | FALSE      | TRUE      | Knowledge architecture layer         | 2/16/2026  |
| 7cadfd0d-227d-5835-ac76-8abc07ad65f0 | layer                   | os                   | 3          | FALSE      | TRUE      | Operating workflow layer             | 2/16/2026  |
| bb4be787-d03c-5d02-be95-a71b0f8926f3 | layer                   | project              | 4          | FALSE      | TRUE      | Project execution layer              | 2/16/2026  |
| dc27fdec-e26d-5479-ab8d-f8fa654d9c56 | layer                   | meta                 | 5          | FALSE      | TRUE      | Meta-governance layer                | 2/16/2026  |
| 2264bd9f-9934-59a3-9a02-9ff954d9c3b6 | maturity                | seed                 | 1          | FALSE      | TRUE      | Initial idea                         | 2/16/2026  |
| 7688d7cd-b968-5541-9e5a-65d181a26219 | maturity                | developing           | 2          | FALSE      | TRUE      | Expanding and being tested           | 2/16/2026  |
| c6c46066-a4de-5db4-a579-2f99577e7be7 | maturity                | stable               | 3          | FALSE      | TRUE      | Reliable and internally coherent     | 2/16/2026  |
| 99c92b75-f847-52d2-bad9-3e86d61b5b6a | maturity                | mature               | 4          | FALSE      | TRUE      | Production quality                   | 2/16/2026  |
| ff128e36-172b-5dc6-952b-b6ca229b2bf8 | maturity                | legacy               | 5          | FALSE      | TRUE      | Historical reference                 | 2/16/2026  |
| 19756dbe-c8f5-53f7-bf5b-e2866139a2bf | project_priority        | critical             | 1          | FALSE      | TRUE      | Critical priority                    | 2/16/2026  |
| 8ede121e-a79e-517f-8dd5-57dcee75e996 | project_priority        | high                 | 2          | FALSE      | TRUE      | High priority                        | 2/16/2026  |
| a237d1f1-1323-5fb4-b631-f94f949556d5 | project_priority        | medium               | 3          | FALSE      | TRUE      | Medium priority                      | 2/16/2026  |
| 2888af73-ebdf-5c6f-a1ed-f1e28ff223db | project_priority        | low                  | 4          | FALSE      | TRUE      | Low priority                         | 2/16/2026  |
| 7ea4e657-c3d9-5c59-8752-1c637a44dfe4 | project_role            | core                 | 1          | FALSE      | TRUE      | Core dependency                      | 2/16/2026  |
| 25471f70-d749-5e63-95e4-dd151b361788 | project_role            | support              | 2          | FALSE      | TRUE      | Support material                     | 2/16/2026  |
| 9f438371-0560-5129-b051-f82cb87ce76f | project_role            | reference            | 3          | FALSE      | TRUE      | Background reference                 | 2/16/2026  |
| 9c3ed301-5189-531d-a240-9fb6f1b65902 | project_stage           | planning             | 1          | FALSE      | TRUE      | Planning stage                       | 2/16/2026  |
| d86c8e4a-2831-5099-88b4-42994ad318bc | project_stage           | drafting             | 2          | FALSE      | TRUE      | Drafting stage                       | 2/16/2026  |
| 72c1819c-ae62-59c5-b6d1-025633808a62 | project_stage           | review               | 3          | FALSE      | TRUE      | Review stage                         | 2/16/2026  |
| 125b4cdc-a6b3-5971-b0e2-7bb0c70ba857 | project_stage           | complete             | 4          | FALSE      | TRUE      | Completed stage                      | 2/16/2026  |
| 0254a7c3-d1a9-58fe-9c94-60064d89fc4f | sensitivity_adversarial | critical             | 1          | FALSE      | TRUE      | High adversarial sensitivity         | 2/16/2026  |
| e4abefc7-a2b4-568b-9b14-f41ad71dde7e | sensitivity_adversarial | strong               | 2          | FALSE      | TRUE      | Strong adversarial sensitivity       | 2/16/2026  |
| 744d5be6-9950-58d7-b4b3-2bfd0a07b5cf | sensitivity_adversarial | moderate             | 3          | FALSE      | TRUE      | Moderate adversarial sensitivity     | 2/16/2026  |
| 8dc0b667-70c2-51c9-a25b-bd72d6104210 | sensitivity_adversarial | weak                 | 4          | FALSE      | TRUE      | Low adversarial sensitivity          | 2/16/2026  |
| 70e0dc47-7008-5ec1-9e69-8e4309f91ba5 | sensitivity_topology    | hub                  | 1          | FALSE      | TRUE      | High centrality                      | 2/16/2026  |
| 65410ea6-bc7f-55b0-8351-6d7c5026375f | sensitivity_topology    | bridge               | 2          | FALSE      | TRUE      | Connects clusters                    | 2/16/2026  |
| 8885df37-406b-5e09-80bd-4dcbadb9f559 | sensitivity_topology    | leaf                 | 3          | FALSE      | TRUE      | Edge node                            | 2/16/2026  |
| f7f6d7fa-7340-5ffc-ab39-4bd26b719b1b | sensitivity_verdict     | load_bearing         | 1          | FALSE      | TRUE      | Critical structural element          | 2/16/2026  |
| b361a138-9593-5ced-a689-abfdd4c529e2 | sensitivity_verdict     | supporting           | 2          | FALSE      | TRUE      | Support element                      | 2/16/2026  |
| 11780355-5027-50a4-8759-ddd869b95956 | sensitivity_verdict     | optional             | 3          | FALSE      | TRUE      | Optional element                     | 2/16/2026  |
| eadf1f0a-064f-5961-994e-7e948b4f795a | sqi_alert               | green                | 1          | FALSE      | TRUE      | Healthy                              | 2/16/2026  |
| 13781635-7cd2-59d7-b94e-a0435b2c0b35 | sqi_alert               | yellow               | 2          | FALSE      | TRUE      | Needs attention                      | 2/16/2026  |
| e103fa88-c980-528e-9515-91dd5af46b02 | sqi_alert               | red                  | 3          | FALSE      | TRUE      | Critical issues                      | 2/16/2026  |
| 8ceba3a9-97ed-5622-9318-de152bc6cc92 | status                  | draft                | 1          | FALSE      | TRUE      | Early draft                          | 2/16/2026  |
| a0f9a05b-9e6d-5ec9-862d-4fa26c0fb0f2 | status                  | review               | 2          | FALSE      | TRUE      | In active review                     | 2/16/2026  |
| a0ef18ae-46c1-5d0d-a4bd-fffca6b624db | status                  | approved             | 3          | FALSE      | TRUE      | Approved baseline                    | 2/16/2026  |
| 3ac6b609-ddd8-54b0-95c0-928d1c0c7664 | status                  | validated            | 4          | FALSE      | TRUE      | Validated against checks             | 2/16/2026  |
| e5b05dde-c13d-598c-bdca-a8c3630efeda | status                  | published            | 5          | FALSE      | TRUE      | Externally published                 | 2/16/2026  |
| ff00768f-94bb-5be8-90c6-74f2f9048d25 | status                  | deprecated           | 6          | FALSE      | TRUE      | Kept only for historical trace       | 2/16/2026  |
| 5618842d-1869-5e34-baa9-a29eb40bd163 | status                  | canonical            | 7          | FALSE      | TRUE      | Legacy label; prefer approved        | 2/16/2026  |
| 6bf8401d-83ae-579b-b56c-659a55343964 | term_precision          | approved             | 1          | FALSE      | TRUE      | Approved and stable definition       | 2/16/2026  |
| 91c426c8-e628-5b69-aede-322b4996193c | term_precision          | working              | 2          | FALSE      | TRUE      | Working definition                   | 2/16/2026  |
| b87dbb83-5913-5330-afcc-040dc0918b0c | term_precision          | informal             | 3          | FALSE      | TRUE      | Informal shorthand                   | 2/16/2026  |
| fa658716-cfa1-51a4-b578-5f13e077af7f | tqd_band                | publication_ready    | 1          | FALSE      | TRUE      | 90-100                               | 2/16/2026  |
| 81897c93-da0d-5b14-8b80-f7a968235209 | tqd_band                | strong               | 2          | FALSE      | TRUE      | 75-89                                | 2/16/2026  |
| dea7db72-7ea2-5e83-93fa-07625edbf7ce | tqd_band                | solid_gaps           | 3          | FALSE      | TRUE      | 60-74                                | 2/16/2026  |
| 68338c79-e03d-537f-a46b-f91bffdac88b | tqd_band                | salvageable          | 4          | FALSE      | TRUE      | 40-59                                | 2/16/2026  |
| b47e7850-73f4-5613-b2a5-76c5c3d28572 | tqd_band                | fundamental_problems | 5          | FALSE      | TRUE      | <40                                  | 2/16/2026  |
| dfa76b69-805f-5674-b788-c9576e82520c | tsr_tier                | excellent            | 1          | FALSE      | TRUE      | Excellent                            | 2/16/2026  |
| c0e2af02-6ef5-50b8-9a72-32d5b7a2a3e6 | tsr_tier                | strong               | 2          | FALSE      | TRUE      | Strong                               | 2/16/2026  |
| bab5eb36-9d16-5bd6-a78d-32ae63117ff1 | tsr_tier                | good                 | 3          | FALSE      | TRUE      | Good                                 | 2/16/2026  |
| 891c92a2-18e3-5ef8-b70c-d5a1ca81aeda | tsr_tier                | developing           | 4          | FALSE      | TRUE      | Developing                           | 2/16/2026  |
| 37a91c42-81a4-58a3-9df2-22c2e7876085 | type                    | paper                | 1          | FALSE      | TRUE      | Long-form argument or manuscript     | 2/16/2026  |
| 6c0ec92f-8832-5945-9675-cd0c3c00b033 | type                    | model                | 2          | FALSE      | TRUE      | Formal model or equation-driven note | 2/16/2026  |
| baa94070-4e20-584f-843d-2075c6cde674 | type                    | concept              | 3          | FALSE      | TRUE      | Conceptual note                      | 2/16/2026  |
| 4ebee352-93ae-5ab1-9bca-fa61d8edff0f | type                    | definition           | 4          | FALSE      | TRUE      | Definition note                      | 2/16/2026  |
| a8552eb4-dcce-5dae-8065-647768a955d4 | type                    | note                 | 5          | FALSE      | TRUE      | General working note                 | 2/16/2026  |
| 4268c00d-6147-5889-8811-574d578fb5d6 | type                    | dataset              | 6          | FALSE      | TRUE      | Dataset or data-source note          | 2/16/2026  |
| b09f308f-5a94-56ae-9436-5b6216d04ce3 | type                    | evidence_extract     | 7          | FALSE      | TRUE      | Extract tied to a source             | 2/16/2026  |
| c5d7f4a0-6370-52d3-a336-637daa71fe0c | type                    | result               | 8          | FALSE      | TRUE      | Results from an analysis             | 2/16/2026  |
| a6c58660-bb48-5d3f-93d4-eaec2cd550c8 | type                    | interpretation       | 9          | FALSE      | TRUE      | Interpretive synthesis               | 2/16/2026  |