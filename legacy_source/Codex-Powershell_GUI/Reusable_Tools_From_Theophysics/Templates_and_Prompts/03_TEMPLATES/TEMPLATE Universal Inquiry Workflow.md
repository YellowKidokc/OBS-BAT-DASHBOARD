
# **TEMPLATE: Universal Inquiry Workflow**

Researcher
---
type: inquiry
question: ""
status: "draft"
created: {{date}}
updated: {{date}}
tags:
  - inquiry
  - research
  - logic
  - workflow
links:
  variables: []
  related_inquiries: []
  evidence_notes: []
  external_sources: []
---

# {{title}}

## 1. Clarify the Claim  
**Purpose:** Define the claim so precisely that it can be evaluated without interpretation.  
**Definition:** Clarifying a claim means identifying *exactly what is being asserted*, what the terms mean, and what would count as the claim being true or false.

**Your Entry:**  
- What is the core claim?  
- 
- What are the key terms?  
- 
- What would logically follow if the claim is true?  
- 
- What would logically follow if the claim is false?


---

## 2. Decompose the Claim Into Sub-Questions  

**Purpose:** Reduce the question into minimal independent components.  

**Definitions of sub-components:**

- **Definitional:** Requires clarifying terms, categories, or boundaries.  
- 
- **Mechanistic:** Requires explaining *how* something works.  
- 
- **Evidential:** Requires identifying observable or measurable phenomena.  
- 
- **Boundary Conditions:** Under what conditions the claim holds or fails.  
- 
- **Failure Modes:** Ways the claim breaks.  
- 
- **Invariants:** Qualities that must remain true across scenarios.



**Your Entry:**  
- Sub-question 1:  
- 
- Sub-question 2:  
- 
- Sub-question 3:  
- 

---

## 3. Identify Required Domains  
**Purpose:** Avoid category errors by assigning each sub-question to an academic discipline.  
Possible domains include:  

Physics, Mathematics, Theology, History, Psychology, Biology, Computer Science, etc.

**Your Entry:**  
- Domain Mapping Table:  
- 
  - Sub-question 1 →  
  - 
  - Sub-question 2 →  
  - 
  - Sub-question 3 →  

---

## 4. Define Standards of Evidence / Disproof  
**Purpose:** Make the evaluation standards explicit.  

### Examples of **acceptable evidence** by domain:
- **Physics:** reproducible measurement, invariants, conservation laws  
- 
- **Mathematics:** proofs, counterexamples, logical impossibility  
- 
- **History:** primary sources, textual consistency, archaeological evidence  
- 
- **Theology:** scriptural consistency, doctrinal invariance, experiential harmonics  
- 
- **Computer Science:** algorithmic complexity, correctness proofs, benchmarks


### Examples of **disproof standards**:
- Violation of a boundary condition  
- Logical contradiction  
- Empirical inconsistency  
- Predictive failure  
- Inability to derive necessary invariants  

**Your Entry:**  
- Evidence required:  
- Disproof criteria:  

---

## 5. Methodological Plan  
**Purpose:** Create an ordered workflow for answering the question.



### Example components:
- Define variables and constants  
- 
- Build equations or logical relations  
- 
- Identify known results  
- 
- Acquire evidence (datasets, manuscripts, experiments, computational proofs)  
- 
- Compare competing explanations  
- 
- Test invariance and sensitivity  
- 
- Construct final synthesis
- 

**Your Entry:**  
- Step 1 →  
- 
- Step 2 →  
- 
- Step 3 →  
- 

---

## 6. Known vs Unknown  
**Purpose:** Identify what is already established vs what requires research.  
Break it down into:

- **Known:**  
- 
- **Unknown:**  
- 
- **Assumptions:**  
- 
- **Unverifiable:**  
- 
- **Requires new theory:**  
- 

---

## 7. Preliminary Evaluation  
**Purpose:** Provide a structured, non-speculative judgment.

### Evaluate based on:
- Strength of evidence  
- 
- Logical coherence  
- 
- Competing explanations  
- 
- Simplicity vs assumption load  
- 
- Falsifiability  

**Your Entry:**  
- Supported elements:  
- 
- Weak elements:  
- 
- Contradictions or tensions:  
- 

---

## 8. Formal Summary  
**Purpose:** Produce a clean academic distillation.  
(This must be framed as a neutral, scholarly evaluation.)

**Your Summary:**  




---

# ADDITIONAL SECTIONS

## Evidence Notes (links)
List notes or files containing supporting or contradictory evidence.  


- [[evidence_note_1]]
    
- [[evidence_note_2]]
    



## External Sources Consulted  
This auto-populates your causal chain for DataView queries.

Format:  


- Source:  
    URL:  
    Claim supported/contradicted:  
    Notes:
    



## Causal Chain Reconstruction  
**Purpose:** Document how each piece of evidence shaped your evaluation.

```

Cause → Effect → Implication → Influence on final evaluation

```

---

# META LINKS  
- Related inquiries:  
- Variables extracted:  
- Tags for domain cross-mapping:  


---

# 2. EXPLANATORY DEFINITIONS (Put in a separate Obsidian note)

Create a note `Definitions/Inquiry-Definitions.md`:


---
type: definitions
tags: [definitions, methodology]
---

# Inquiry Definitions

## Ontological Claim
A statement about what fundamentally exists or can exist.

## Epistemic Claim
A statement about what can be known or justified.

## Definitional Question
A question requiring precise meaning or boundaries for terms.

## Mechanistic Question
“How does this work?” — explanation of structure or causal process.

## Evidential Question
“What would we empirically observe if this were true?”

## Boundary Condition
A constraint defining when a model or claim holds.

## Invariant
A property that must remain true across all valid cases.

## Falsification
A condition or observation that would demonstrate the claim is false.

## Methodological Plan
A stepwise research design that allows the claim to be evaluated.






---
## Cross-Reference Index

### Related Papers
- {{related_papers}}

### Evidence Bundles
Located in:
D:\THEOPHYSICS_MASTER\02_LIBRARY\Evidence_Bundles
- {{evidence_bundles}}

### Core Reference
D:\THEOPHYSICS_MASTER\02_LIBRARY\10_CORE_REFERENCE  
D:\THEOPHYSICS_MASTER\02_LIBRARY\Core Reference  
- {{core_references}}

### Glossary
D:\THEOPHYSICS_MASTER\02_LIBRARY\Glossary  
- {{glossary_terms}}

### Theory Dependencies
D:\THEOPHYSICS_MASTER\02_LIBRARY\05_THEORIES_LIBRARY  
- {{theory_dependencies}}

### Maps / Media
- Podcast: {{media.podcast}}
- TTS: {{media.tts_audio}}
- Maps: {{media.maps_drive}}
- Diagrams: {{media.diagrams}}
---

---

# 3. DATAVIEW INTEGRATION

Create a DataView dashboard note: `Dashboards/Inquiry-Logic-Checker.md`.

````markdown
```dataview
TABLE question, status, file.ctime as Created, file.mtime as Updated
FROM #inquiry
SORT file.mtime DESC



Now add logic flow checks:

```markdown
```dataview
TABLE 
  (length(links.evidence_notes) > 0) AS "Has Evidence?",
  (length(links.variables) > 0) AS "Variables Extracted?",
  (status) AS "Status"
FROM #inquiry
WHERE type = "inquiry"
SORT file.name ASC



You can also write a “contradiction detector”:

```markdown
```dataview
TABLE 
  Summary as Summary,
  (contains(lower(Summary), "contradiction")) AS Contains_Contradiction
FROM #inquiry




---

# 4. SUMMARY PAGE TEMPLATE  
Create a second template: `Templates/Inquiry-Summary.md`.

```markdown
---
type: inquiry_summary
inquiry: ""
tags: [summary, inquiry]
---

# Summary of Inquiry: {{title}}

## Core Question  
{{inquiry_question}}

## Judgment  
- Supported elements  
- Weak elements  
- Inconclusive areas  

## Evidence Map  
```dataview
TABLE source, claim, notes
FROM #evidence
WHERE contains(file.inlinks, this.inquiry)


## Causal Chain Snapshot

```dataview
LIST causal_chain
FROM #inquiry
WHERE file.name = this.inquiry




---

# 5. INTERLINKING LOGIC  
Each inquiry note includes:

- A list of evidence notes  
- A list of variables  
- A causal chain  
- A summary section  
- Cross-links to definitions  

Dataview can automatically detect:

- Missing definitions  
- Missing variables  
- Missing evidence  
- Logical contradictions in summaries  
- Inquiry notes that disagree with one another  

---

# 6. WHAT I CAN DO NEXT  
I can build:

- A **Logic-Flow Checker Plugin Spec** (for future automation)  
- A **Causal-Graph Generator** using DataViewJS  
- Automatic **cross-inquiry contradiction detection**  
- A full **semantic RAG layer** integrated into your Obsidian vault  
- A version designed specifically for **Paper 1 / Paper 2 / Master Equation**  

---

If you want, I can now:

### A) Generate the DataviewJS scripts for:
- detecting contradictions  
- verifying methodological completeness  
- mapping causal chains across inquiries  

### B) Generate a full example using one of your live questions  
(e.g., “Did I mathematically prove Jesus?”)

Which direction do you want to go next?


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

