#!/usr/bin/env python3
"""
Two-step YAML Copilot
Step 1: classify note -> compact JSON
Step 2: populate YAML using active layer schemas only
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
from typing import Any

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
CONFIG_PATH = SCRIPT_DIR / "config.txt"
INPUT_DIR = SCRIPT_DIR / "input"
OUTPUT_DIR = SCRIPT_DIR / "output"
MEMORY_PATH = SCRIPT_DIR / "two_step_memory.json"


def parse_config(path: pathlib.Path) -> dict[str, str]:
    cfg: dict[str, str] = {}
    if not path.exists():
        return cfg
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip()
    return cfg


def load_memory() -> dict[str, Any]:
    if MEMORY_PATH.exists():
        try:
            return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"co_occurrence": {}, "paper_history": {}, "layer_frequency": {}}


def save_memory(memory: dict[str, Any]) -> None:
    MEMORY_PATH.write_text(json.dumps(memory, indent=2), encoding="utf-8")


def update_layer_frequency(memory: dict[str, Any], active_layers: list[str]) -> None:
    freq = memory.setdefault("layer_frequency", {})
    for layer in active_layers:
        freq[layer] = int(freq.get(layer, 0)) + 1


def update_co_occurrence(memory: dict[str, Any], tags: list[str]) -> None:
    co = memory.setdefault("co_occurrence", {})
    tags = sorted(set([t for t in tags if t]))
    for i, a in enumerate(tags):
        for b in tags[i + 1 :]:
            key = f"{a}|{b}"
            co[key] = int(co.get(key, 0)) + 1


def top_co_occurrence(memory: dict[str, Any], n: int = 20) -> str:
    co = memory.get("co_occurrence", {})
    if not co:
        return "No co-occurrence data yet."
    items = sorted(co.items(), key=lambda kv: (-int(kv[1]), kv[0]))[:n]
    return "\n".join([f"{k}: {v}x" for k, v in items])


DEFAULT_REFERENCE_FILES = [
    REPO_ROOT / "MASTER_EQUATION" / "MASTER_EQUATION_10_LAWS_REFERENCE_COMPLETE.md",
    REPO_ROOT / "MASTER_EQUATION" / "[26.5] MA-00_Master-Equation.md",
    REPO_ROOT / "00_AXIOMS" / "_LOSSLESS_SUMMARY" / "AXIOMS_PART1_STRAIGHT.md",
    REPO_ROOT / "00_AXIOMS" / "_LOSSLESS_SUMMARY" / "AXIOMS_PART2_COURT.md",
    REPO_ROOT / "00_AXIOMS" / "012_E2.1_Master-Equation-First-Form.md",
    REPO_ROOT / "00_AXIOMS" / "146_E19.1_Full-Master-Equation.md",
    REPO_ROOT / "00_AXIOMS" / "AXIOM_MATRIX_LOSSLESS.md",
    REPO_ROOT / "00_SYSTEM" / "CANONICAL_TAG_TAXONOMY.md",
]

# ── Canonical 79-tag vocabulary (compressed) ──────────────────────
CANONICAL_TAGS = """CANONICAL TAG VOCABULARY (79 tags — use ONLY these):
CONTENT: axiom, claim, law, evidence, equation, prediction, definition
STRUCTURAL: isomorphism, convergence, falsification, timewall, dependency, enables, contradicts, supports
DOMAIN: physics, theology, information, consciousness, morality, mathematics
VARS (physics-first): G=Gravity, M=Matter, E=Energy, S=Entropy, T=Time, K=Knowledge, R=Resurrection, Q=Quantum, F=Faith, C=Coherence
PAIRS: I=(G,R), II=(M,S), III=(E,F), IV=(T,K), V=(Q,C)
LAWS (Wolfram2): 01=Gravity-Grace, 02=Quantum-Faith, 03=Thermo-Sin, 04=Info-Truth, 05=Chaos-Will, 06=Fluid-Spirit, 07=Cosmo-Glory, 08=Cyber-Obedience, 09=Relativ-Perspective, 10=Fractal-Image
FORCED: sin-ent, grace-neg, faith-obs, term-obs, coh-con, open-sys, time-wall
FRUITS: love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, self-control
EVIDENCE: data-pear(6.35s), data-gcp(6s), data-prop-cosmos(5.7s), data-oxford(4/7)
STATUS: verified, partial, speculative, walled, falsified, canonical, unregistered
OPS: establish, derive, challenge, bridge, anchor, declare

EXHAUSTIVE MATCHING RULES:
- Match ALL axioms the document references, not just the most obvious one.
- Key axiom trigger words:
  AX-001: existence, something exists, self-refuting
  AX-003: information primacy, distinguishability, ontological primitive
  AX-008: substrate, instantiation
  AX-009: self-grounding, infinite regress, brute fact
  AX-010: Logos Field, chi-field, informational substrate
  AX-012: chi equation, integral G K
  AX-025: coherence cannot self-increase, closed system, spontaneous order
  AX-059: grace external, negentropy, open system
  AX-061: three observers, Trinity, N=3
  AX-066: terminal observer, God, von Neumann chain
  AX-069: binary moral, sign operator, sigma +1/-1
  AX-071: self-flip impossible, works salvation impossible
  AX-072: external intervention, grace required
  AX-189: PERSONHOOD, agency, intentionality
- Match ALL evidence datasets mentioned, not just the first one.
  data-pear: PEAR, Princeton, REG, random event generator, 6.35, consciousness-machine
  data-gcp: GCP, Global Consciousness, 9/11, collective, 6 sigma
  data-prop-cosmos: PROP-COSMOS, prophecy, 5.7 sigma, 11/11, timeline
  data-oxford: Oxford, Ard Louis, McGrath, Russell, Wildman, convergence, 4/7
- Match ALL forced conclusions that appear, even if only implied.
- Match ALL symmetry pairs that are discussed, even indirectly.
- If a document discusses gravity AND grace together, that's pair I.
- If a document discusses entropy AND sin together, that's pair II.
- If a document discusses observation AND faith together, that's pair III.
- PREFER OVER-INCLUSION. If uncertain, include with low confidence.

COMPRESSED YAML FORMAT (output this):
vars: [G, M, S]        # active chi variables (single letters) — list ALL that appear
pairs: [I, II]          # active symmetry pairs (Roman numerals) — list ALL referenced
laws: [01, 03]          # active laws (2-digit numbers) — list ALL discussed
forced: [sin-ent]       # which forced conclusions apply — list ALL mentioned
fruits: []              # which fruit measurement domains
evidence: [data-pear]   # which evidence datasets — list ALL cited
axioms: [AX-001, AX-025]  # which canonical axioms (AX-NNN) — match EVERY axiom
status: verified        # document status
domain: [physics, theology]  # which frames
content_type: axiom     # what IS this document

EXHAUSTIVE MATCHING RULES FOR compressed_tags:
- vars: If the document discusses gravity, grace, or gravitational concepts → include G.
  If it discusses matter, substrate, or body → include M. Apply to ALL 10 variables.
- pairs: If BOTH variables of a pair appear → include the pair. Check all 5.
- laws: If the document discusses any concept from a law → include that law number.
- forced: Check ALL 7 forced conclusions. If sin/entropy mentioned → sin-ent.
  If grace/negentropy → grace-neg. If faith/observation → faith-obs.
  If terminal observer → term-obs. If coherence conservation → coh-con.
  If open system → open-sys. If Time Wall → time-wall.
- evidence: Check for ANY mention of PEAR, GCP, PROP-COSMOS, Oxford/convergence.
- axioms: Match against the AXIOM_MATRIX_LOSSLESS reference. List EVERY axiom
  that the document's content touches, even indirectly. Be EXHAUSTIVE.
  A document about existence → AX-001. About information → AX-003, AX-004.
  About chi field → AX-010, AX-011, AX-012. About self-grounding → AX-009.
  OVER-INCLUDE rather than under-include. More axiom matches = better.
"""


def parse_int(cfg: dict[str, str], key: str, default: int) -> int:
    raw = str(cfg.get(key, "") or "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except Exception:
        return default


def parse_bool(cfg: dict[str, str], key: str, default: bool) -> bool:
    raw = str(cfg.get(key, "") or "").strip().lower()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "y", "on"}


def resolve_reference_files(cfg: dict[str, str]) -> list[pathlib.Path]:
    raw = str(cfg.get("REFERENCE_FILES", "") or "").strip()
    if not raw:
        return DEFAULT_REFERENCE_FILES
    out: list[pathlib.Path] = []
    for part in raw.split("|"):
        token = part.strip()
        if not token:
            continue
        p = pathlib.Path(token)
        if not p.is_absolute():
            p = REPO_ROOT / p
        out.append(p)
    return out or DEFAULT_REFERENCE_FILES


def read_limited(path: pathlib.Path, max_chars: int) -> str:
    try:
        txt = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    if len(txt) <= max_chars:
        return txt
    return txt[:max_chars]


def build_reference_context(cfg: dict[str, str]) -> str:
    per_file = parse_int(cfg, "REFERENCE_CHARS_PER_FILE", 3500)
    total_max = parse_int(cfg, "REFERENCE_MAX_CHARS", 18000)
    sections: list[str] = []
    used = 0
    for p in resolve_reference_files(cfg):
        if used >= total_max:
            break
        if not p.exists():
            continue
        chunk = read_limited(p, min(per_file, total_max - used)).strip()
        if not chunk:
            continue
        block = f"### REF: {p.name}\n{chunk}"
        sections.append(block)
        used += len(block)
    if not sections:
        return "No external Master Equation/Axiom references loaded."
    return "\n\n".join(sections)


def extract_machine_readable_signals(note_content: str, max_chars: int = 5000) -> str:
    parts: list[str] = []

    fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", note_content, re.DOTALL)
    if fm:
        parts.append("---\n" + fm.group(1).strip() + "\n---")

    abstract_match = re.search(r"(?is)\[!abstract\].{0,2600}", note_content)
    if abstract_match:
        parts.append(abstract_match.group(0).strip())

    semantic_match = re.search(
        r'(?is)<details class="semantic-ai-inline-labels">.*?</details>',
        note_content,
    )
    if semantic_match:
        parts.append(semantic_match.group(0).strip())

    anchors = re.findall(r"(?m)^\s*#\^[^\n]+$", note_content)
    if anchors:
        parts.append("Anchor lines:\n" + "\n".join(anchors[:80]))

    if not parts:
        return "No explicit machine-readable blocks found."

    merged = "\n\n".join(parts)
    return merged[:max_chars]


def build_tagging_policy(cfg: dict[str, str]) -> str:
    exhaustive = parse_bool(cfg, "EXHAUSTIVE_TAGGING", True)
    include_weak = parse_bool(cfg, "INCLUDE_WEAK_TAGS", True)
    max_primary_tags = parse_int(cfg, "MAX_PRIMARY_TAGS", 200)
    max_edges = parse_int(cfg, "MAX_EDGES", 200)

    if exhaustive:
        weak_line = (
            "- Include weak/candidate tags when plausible; do not suppress them."
            if include_weak
            else "- Exclude weak tags; include only medium+ confidence tags."
        )
        return (
            "TAGGING POLICY (EXHAUSTIVE):\n"
            "- Capture every plausible tag/listing/edge instance from machine-readable blocks and prose.\n"
            "- Prefer over-inclusion to under-inclusion.\n"
            f"{weak_line}\n"
            f"- Allow up to {max_primary_tags} primary tags.\n"
            f"- Allow up to {max_edges} edge/listing entries across relation arrays.\n"
            "- If uncertain, include and mark confidence as low rather than dropping."
        )

    return (
        "TAGGING POLICY (CONSERVATIVE):\n"
        "- Keep only strong/medium relevance tags and edges.\n"
        "- Omit weak mentions.\n"
        f"- Limit primary tags to {max_primary_tags}.\n"
        f"- Limit edge/listing entries to {max_edges}."
    )


def build_mission_context(cfg: dict[str, str]) -> str:
    mission = str(
        cfg.get(
            "MISSION_STATEMENT",
            "We are building a new science-grade knowledge system where maximal structured extraction improves downstream database and graph quality.",
        )
        or ""
    ).strip()
    rigor = str(cfg.get("RIGOR_MODE", "MAXIMAL") or "MAXIMAL").strip().upper()
    evidence_density = parse_int(cfg, "MIN_EVIDENCE_ITEMS_PER_PRIMARY_CLAIM", 2)
    return (
        "MISSION CONTEXT:\n"
        f"- Mission: {mission}\n"
        f"- Rigor mode: {rigor}\n"
        "- Prioritize recall of structure over brevity.\n"
        "- For each primary claim, attach explicit evidence/listing support where available.\n"
        f"- Target minimum evidence density: {evidence_density} evidence items per primary claim.\n"
    )


STEP1_SYSTEM = """You are a Theophysics document classifier. Return JSON only.

DOCUMENT TYPES: paper|note|axiom|theorem|corollary|hypothesis|claim|postulate|definition|boundary_condition|experiment|protocol|evidence_bundle|bridge|rebuttal|prompt|outline|dashboard|conversation|devotional|editorial
STATUS: outline|draft|revision|outline_complete|under_review|ready|submitted|published|canonized|deprecated
QUESTION TYPES: Type1|Type2|Type3|Type4
OPERATIONS: GROUND|CHAIN|ATTACK|BRIDGE|ANCHOR|DECLARE
SUBSTRATES: matter|mind|information|mathematical|relational|brute

{canonical_tags}

LAYERS (only active): L4,L5,L6,L7,L8,L9,L10,L11,L12,L13,L14,L15,L16,L17,L18,L19,L20,L21,L22,L23,L24,L25
Rules:
- L1(identity), L2(tree), L20(edges) always active
- L18 active for paper|axiom|theorem|hypothesis
- Other layers active only if materially developed
- Prioritize machine-readable blocks over narrative prose when they conflict.
- Explicitly check alignment with Master Equation and Axiom references.
- Match document content against CANONICAL TAG VOCABULARY above.
- Use physics-first variable names ALWAYS (G=Gravity, NOT G=Grace).
- EXHAUSTIVE AXIOM MATCHING: For compressed_tags.axioms, scan EVERY paragraph for ANY reference to canonical axioms. Look for: existence claims (AX-001), distinction (AX-002), information primacy (AX-003), information definition (AX-004), substrate (AX-008), self-grounding (AX-009), Logos field (AX-010), chi field (AX-011-014), coherence (AX-018-026), observers (AX-034-043), collapse (AX-044-052), boundary conditions (AX-056-065), grace (AX-072-082), moral realism (AX-088-091), evidence datasets (AX-111-124), laws (AX-136-147), fruits (AX-151-160). Include ALL that apply, not just the most prominent one.
- EXHAUSTIVE EVIDENCE MATCHING: If the document mentions PEAR, Princeton, random number generators, consciousness-RNG → tag data-pear. If it mentions GCP, Global Consciousness Project, 9/11 coherence → tag data-gcp. If it mentions PROP-COSMOS, prophecy correlation, timeline → tag data-prop-cosmos. If it mentions Oxford, Ard Louis, McGrath, Russell, Wildman, independent confirmation → tag data-oxford.
- EXHAUSTIVE FORCED MATCHING: Check EVERY forced conclusion: sin=entropy, grace=negentropy, faith=observation, terminal observer, coherence conservation, open system, time wall. If the document discusses ANY of these concepts even indirectly, include the forced tag.
- EXHAUSTIVE PAIR MATCHING: If gravity or grace is discussed → pair I. If matter, entropy, or sin → pair II. If energy, quantum, or faith → pair III. If time, knowledge, or wisdom → pair IV. If quantum coherence, Shannon, or unity → pair V.
{tagging_policy}
{mission_context}
Return valid JSON only.
"""

STEP1_USER = """Classify this document and return JSON with this shape:
{{
  "doc_type": "",
  "status": "",
  "scope": "",
  "confidence": "",
  "classification_tier": "",
  "paper_number": null,
  "q_level": null,
  "question_type": null,
  "branch_taken": null,
  "branch_answer": null,
  "propagation_status": null,
  "substrate_track": null,
  "operation_type": null,
  "op_target": null,
  "active_layers": [],
  "master_equation_alignment": {{"mentions_chi": false, "core_vars": [], "confidence": ""}},
  "axiom_references": [],
  "machine_readable_weight": "",
  "discipline_weight": {{"physics":0,"theology":0,"consciousness":0,"mathematics":0,"philosophy":0,"information_theory":0,"ethics":0,"experimental":0}},
  "primary_tags": [],
  "initial_edges": [],
  "compressed_tags": {{
    "content_type": "",
    "vars": [],
    "pairs": [],
    "laws": [],
    "forced": [],
    "fruits": [],
    "evidence": [],
    "axioms": [],
    "status": "",
    "domain": []
  }}
}}

MACHINE_READABLE_SIGNALS:
---
{machine_signals}
---

MASTER_EQUATION_AND_AXIOM_REFERENCES:
---
{reference_context}
---

DOCUMENT:
---
{note_content}
---"""

STEP2_SYSTEM = """You are a Theophysics YAML metadata generator.
Generate YAML frontmatter only. No markdown fences. No explanation.

{canonical_tags}

Rules:
1) Start with the COMPRESSED TAG BLOCK (vars, pairs, laws, forced, fruits, evidence, axioms, status, domain, content_type).
   This block must use ONLY tags from the CANONICAL TAG VOCABULARY above.
   Use physics-first single-letter variable names: G M E S T K R Q F C.
   Use Roman numeral pair names: I II III IV V.
   Use 2-digit law numbers: 01 through 10.
   Use short forced codes: sin-ent, grace-neg, faith-obs, term-obs, coh-con, open-sys, time-wall.
2) After compressed block, include detailed layers if active.
3) If tree branch exists, include coherent tree fields.
4) Include at least one edge.
5) Include honest blanks when relevant.
6) Follow the tagging policy exactly.
{tagging_policy}
7) Include a compact `human_labels` block with:
   - `theme`
   - `one_line_meaning`
   - `confidence_band`
   - `why_it_matters`
{mission_context}

CO_OCCURRENCE:
{co_occurrence_data}

PRIOR_TAGS:
{prior_tags}

MASTER_EQUATION_AND_AXIOM_REFERENCES:
{reference_context}
"""

STEP2_USER = """Document content:
---
{note_content}
---

Step1 classification:
{step1_result}

Compressed tags from Step1 (use these as the FIRST block in YAML output):
{compressed_tags}

Machine-readable signals:
{machine_signals}

Active layer schemas:
{active_layer_schemas}

Generate complete YAML frontmatter. Start with the compressed tag block, then add layer details."""


LAYER_SCHEMAS = {
    "L4": "master_equation: {core_state: {G:{active:bool,weight:0-1,role:str}, M:{active:bool,weight:0-1,role:str}, E:{active:bool,weight:0-1,role:str}, S:{active:bool,weight:0-1,role:str}, T:{active:bool,weight:0-1,role:str}, K:{active:bool,weight:0-1,role:str}, R:{active:bool,weight:0-1,role:str}, Q:{active:bool,weight:0-1,role:str}, F:{active:bool,weight:0-1,role:str}, C:{active:bool,weight:0-1,role:str}}, coupling_terms:[str], coherence_direction: increasing|decreasing|stable|oscillating|undefined}",
    "L5": "physics: {quantum_mechanics:{active:bool,concepts:[...]}, relativity_cosmology:{active:bool,concepts:[...]}, information_theory:{active:bool,concepts:[...]}, consciousness_science:{active:bool,concepts:[...]}, thermodynamics:{active:bool,concepts:[...]}, field_theory:{active:bool,concepts:[...]}, complexity_theory:{active:bool,concepts:[...]}}",
    "L6": "theology: {core:[...], christology:[...], spiritual_dynamics:[...], ecclesiology:[...], eschatology:[...]}",
    "L7": "trinity: {trinitarian_dynamics:bool, father:{active:bool,roles:[...]}, son:{active:bool,roles:[...]}, spirit:{active:bool,roles:[...]}}",
    "L8": "scripture: {convergence:[...], texts:[...], scripture_refs:[str], EUID_refs:[str], prop_cosmos:{active:bool,correlation_count:str,sigma:float,z_map:str}}",
    "L9": "experiments: {logos_protocols:[...], established:[...], physiological:[...], stats:{threshold:str,trials:int,sigma:float,pre_registered:bool,escrowed:bool,replication:str}, falsification:[str], predictions:[str]}",
    "L10": "mathematics: {equations:[...], formalisms:[...], operators:[...], proofs_present:bool, derivations_present:bool, proof_type:str}",
    "L11": "bridges: {cross_domain:[...], isomorphisms:[...], strength: structural|analogical|metaphorical|formal, survives_probe: bool|null}",
    "L12": "consciousness_ai: {consciousness:[...], ai:[...], observer_state:{level:str,attention:str,intent:str,type:str,phi:str,coupling:str}}",
    "L13": "time_causality: {temporal:[...], causal:[...]}",
    "L14": "principalities_powers: {agencies:[...], warfare:{mode_3_active:bool,attack_vector:str,defense:str,eph6_mapping:str}}",
    "L15": "ethics: {moral_physics:[...], sign:{sigma:+1|-1|null,mechanism:str,C_def:str,beta_def:str}, virtues:[...], ten_laws:{active:bool,engaged:[1-10],symmetry_pairs:[str]}}",
    "L16": "deviation_modes: {M1_agentic:{...}, M2_entropic:{...}, M3_adversarial:{...}, M4_grace:{...}, terminal_all_zero:bool}",
    "L17": "boundary_conditions: {BC1:{...},BC2:{...},BC3:{...},BC4:{...},BC5:{...},BC6:{...},BC7:{...},BC8:{...},scorecard:{...}}",
    "L18": "claims: {primary:[{claim:str,type:str,confidence:str,support:str,vulnerability:str,testable:bool}], evidence:{empirical:[str],logical:[str],scriptural:[str],mathematical:[str],consilience:[str]}, quality:{strongest:str,weakest:str,overall:str}, honest_blanks:[{blank:str,severity:str,path:str}]}",
    "L19": "classifier_hits: {LawMapping:{hit:bool,confidence:str}, MasterEquation:{hit:bool,confidence:str}, Falsification:{hit:bool,confidence:str}, ScripturePhysics:{hit:bool,confidence:str}, ConsciousnessField:{hit:bool,confidence:str}, Prosecution:{hit:bool,confidence:str}, OntologyClassifier:{hit:bool,confidence:str}}",
    "L20": "edges: {depends_on:[{target:str,rel:str,strength:str}], supports:[{target:str,rel:str,strength:str}], contradicts:[{target:str,nature:str,resolution:str}], tests:[{target:str,type:str,result:str}], extends:[{target:str,type:str}], bridges:[{from:str,to:str,type:str,target:str}], attacks:[{target:str,type:str,survived:bool|null}], related_papers:[str], related_axioms:[str], related_BCs:[str]}",
    "L21": "worldview_tracking: {at_q:str, views:{...}, counts:{alive:int,partial:int,dead:int}, eliminated_here:[str], reason:str}",
    "L22": "historical_references: {physicists:[...], philosophers:[...], theologians:[...], information_theorists:[...]}",
    "L23": "media: {images:[...], audio:[...], video:[...], pdf_attachments:[...], data_files:[...], visualizations:[...]}",
    "L24": "publication: {target_platform:str, series:str, paper_position:str, peer_review:{stage:str,journal:str,submitted_date:str,reviewers:[str],review_outcome:str}, adversarial_review:{gpt_review:bool,gpt_review_file:str,fixes_applied:[str]}, abstract:str}",
    "L25": "session: {session_title:str,session_date:str,ai_partner:str,model_version:str,session_type:str,what_discussed:[str],what_decided:[str],what_changed:[str],what_next:[str],files_touched:[str],breakthroughs:[str],david_effect:{active:bool,protocol_stage:str,measured_outcomes:[str]}}",
}


PAPER_PRELOAD = {
    "P01": {"layers": ["L5", "L6", "L8", "L10", "L11"], "operation": "GROUND"},
    "P02": {"layers": ["L5", "L6", "L7", "L9", "L10", "L11", "L16", "L17"], "operation": "CHAIN"},
    "P03": {"layers": ["L5", "L10", "L13"], "operation": "GROUND"},
    "P04": {"layers": ["L5", "L6", "L12", "L16"], "operation": "CHAIN"},
    "P05": {"layers": ["L4", "L5", "L6", "L8", "L11", "L15"], "operation": "BRIDGE"},
    "P06": {"layers": ["L4", "L5", "L6", "L7", "L10", "L11", "L15", "L17"], "operation": "DECLARE"},
    "P07": {"layers": ["L5", "L6", "L8", "L11"], "operation": "BRIDGE"},
    "P08": {"layers": ["L5", "L6", "L7", "L8", "L17"], "operation": "DECLARE"},
    "P09": {"layers": ["L4", "L6", "L10", "L11", "L15"], "operation": "CHAIN"},
    "P10": {"layers": ["L4", "L6", "L8", "L10", "L15"], "operation": "DECLARE"},
    "P11": {"layers": ["L5", "L6", "L8", "L15", "L17", "L21"], "operation": "CHAIN"},
    "P12": {"layers": ["L6", "L8", "L9", "L11", "L12", "L17", "L21"], "operation": "BRIDGE"},
}


def extract_yaml_block(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n", "", t)
        t = re.sub(r"\n```$", "", t)
        t = t.strip()
    if t.startswith("---"):
        return t
    return f"---\n{t}\n---"


def render_hidden_yaml_panel(yaml_block: str, body: str) -> str:
    """Return markdown with collapsible YAML panel for cleaner reading views."""
    inner = yaml_block.strip()
    if inner.startswith("---"):
        inner = re.sub(r"^---\s*\n?", "", inner)
        inner = re.sub(r"\n?---\s*$", "", inner)
    return (
        "<details class=\"theophysics-yaml-metadata\">\n"
        "<summary><strong style=\"color:#b00020;\">YAML Metadata (click to expand)</strong></summary>\n\n"
        "```yaml\n"
        f"{inner.strip()}\n"
        "```\n"
        "</details>\n\n"
        f"{body.strip()}\n"
    )


def call_openai_json(client, model: str, system_prompt: str, user_prompt: str) -> dict[str, Any]:
    is_reasoning = model.startswith("o1") or model.startswith("o3") or model.startswith("o4")
    kwargs = dict(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "developer" if is_reasoning else "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    if not is_reasoning:
        kwargs["temperature"] = 0.1
    resp = client.chat.completions.create(**kwargs)
    return json.loads(resp.choices[0].message.content)


def call_openai_text(client, model: str, system_prompt: str, user_prompt: str) -> str:
    is_reasoning = model.startswith("o1") or model.startswith("o3") or model.startswith("o4")
    kwargs = dict(
        model=model,
        messages=[
            {"role": "developer" if is_reasoning else "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    if not is_reasoning:
        kwargs["temperature"] = 0.2
    resp = client.chat.completions.create(**kwargs)
    return resp.choices[0].message.content or ""


def build_active_layers(classification: dict[str, Any]) -> list[str]:
    active = [str(x) for x in classification.get("active_layers", []) if str(x).strip()]
    active.extend(["L20"])  # always
    if str(classification.get("doc_type", "")).lower() in {"paper", "axiom", "theorem", "hypothesis"}:
        active.append("L18")

    paper_number = str(classification.get("paper_number", "") or "")
    if paper_number in PAPER_PRELOAD:
        active.extend(PAPER_PRELOAD[paper_number]["layers"])

    me_align = classification.get("master_equation_alignment", {}) or {}
    if isinstance(me_align, dict):
        mentions_chi = bool(me_align.get("mentions_chi"))
        core_vars = me_align.get("core_vars", []) or []
        if mentions_chi or core_vars:
            active.extend(["L4", "L10", "L15", "L19"])

    ax_refs = classification.get("axiom_references", []) or []
    if isinstance(ax_refs, list) and ax_refs:
        active.extend(["L18", "L20"])

    # normalize names such as L4_master_equation to L4
    norm: list[str] = []
    for a in active:
        m = re.match(r"^(L\d+)", a)
        if m:
            norm.append(m.group(1))
    norm = sorted(set(norm), key=lambda x: int(x[1:]))
    return norm


def process_file(path: pathlib.Path, client, cfg: dict[str, str], memory: dict[str, Any], reference_context: str) -> None:
    note_content = path.read_text(encoding="utf-8", errors="ignore")
    machine_signals = extract_machine_readable_signals(note_content)
    tagging_policy = build_tagging_policy(cfg)
    mission_context = build_mission_context(cfg)
    model_step1 = cfg.get("MODEL_STEP1", cfg.get("MODEL", "gpt-4o-mini"))
    model_step2 = cfg.get("MODEL_STEP2", cfg.get("MODEL", "gpt-4o"))
    note_chars = parse_int(cfg, "NOTE_CONTENT_CHARS", 24000)

    print(f"\n=== {path.name} ===")
    cls = call_openai_json(
        client,
        model_step1,
        STEP1_SYSTEM.format(
            tagging_policy=tagging_policy,
            mission_context=mission_context,
            canonical_tags=CANONICAL_TAGS,
        ),
        STEP1_USER.format(
            note_content=note_content[:note_chars],
            machine_signals=machine_signals,
            reference_context=reference_context,
        ),
    )

    active_layers = build_active_layers(cls)
    update_layer_frequency(memory, active_layers)

    paper_num = str(cls.get("paper_number", "") or "")
    prior_tags = []
    if paper_num:
        prior_tags = memory.get("paper_history", {}).get(paper_num, {}).get("tags", [])

    layer_schema_text = "\n\n".join([f"{layer}: {LAYER_SCHEMAS.get(layer, 'schema missing')}" for layer in active_layers])
    step2_sys = STEP2_SYSTEM.format(
        co_occurrence_data=top_co_occurrence(memory),
        prior_tags=json.dumps(prior_tags),
        reference_context=reference_context,
        tagging_policy=tagging_policy,
        mission_context=mission_context,
        canonical_tags=CANONICAL_TAGS,
    )
    step2_user = STEP2_USER.format(
        note_content=note_content,
        step1_result=json.dumps(cls, indent=2),
        compressed_tags=json.dumps(cls.get("compressed_tags", {}), indent=2),
        machine_signals=machine_signals,
        active_layer_schemas=layer_schema_text,
    )

    yaml_text = call_openai_text(client, model_step2, step2_sys, step2_user)
    yaml_block = extract_yaml_block(yaml_text)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

    step1_path = OUTPUT_DIR / f"{path.stem}_STEP1_{ts}.json"
    step1_path.write_text(json.dumps(cls, indent=2), encoding="utf-8")

    yaml_path = OUTPUT_DIR / f"{path.stem}_YAML_{ts}.md"
    yaml_path.write_text(yaml_block + "\n", encoding="utf-8")

    # Generate compressed-only YAML from step1 classification
    ctags = cls.get("compressed_tags", {})
    if isinstance(ctags, dict) and ctags:
        compact_lines = ["---"]
        for k in ["content_type", "vars", "pairs", "laws", "forced", "fruits",
                   "evidence", "axioms", "status", "domain"]:
            v = ctags.get(k)
            if v is not None:
                if isinstance(v, list):
                    compact_lines.append(f"{k}: [{', '.join(str(x) for x in v)}]")
                else:
                    compact_lines.append(f"{k}: {v}")
        compact_lines.append("---")
        compact_yaml = "\n".join(compact_lines)
        compact_path = OUTPUT_DIR / f"{path.stem}_COMPACT_{ts}.md"
        compact_path.write_text(compact_yaml + "\n", encoding="utf-8")
        print(f"Compact -> {compact_path.name}")

    hidden_yaml_path = OUTPUT_DIR / f"{path.stem}_HIDDEN_YAML_{ts}.md"
    hidden_yaml_path.write_text(render_hidden_yaml_panel(yaml_block, note_content), encoding="utf-8")

    # best-effort tag memory update
    m = re.search(r"^tags:\s*\n((?:\s+-\s+.*\n)+)", yaml_block + "\n", re.MULTILINE)
    if m:
        tags = [re.sub(r"^\s+-\s+", "", ln).strip() for ln in m.group(1).splitlines()]
        update_co_occurrence(memory, tags)
        if paper_num:
            memory.setdefault("paper_history", {})[paper_num] = {"tags": tags}

    print(f"Step1 -> {step1_path.name}")
    print(f"YAML  -> {yaml_path.name}")
    print(f"Panel -> {hidden_yaml_path.name}")
    print(f"Active layers: {active_layers}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Two-step YAML copilot")
    ap.add_argument("--dry-run", action="store_true", help="Read files and show intended flow only")
    args = ap.parse_args()

    cfg = parse_config(CONFIG_PATH)
    api_key = cfg.get("OPENAI_API_KEY", "")
    reference_context = build_reference_context(cfg)

    files = sorted([p for p in INPUT_DIR.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".txt"}])
    if not files:
        raise SystemExit(f"No input files found in: {INPUT_DIR}")

    if args.dry_run:
        print("Dry run mode")
        print(f"Reference context chars: {len(reference_context)}")
        for f in files:
            print(f"- {f.name}")
        return 0

    if not api_key or api_key.startswith("sk-PASTE"):
        raise SystemExit("Missing OPENAI_API_KEY in config.txt")

    try:
        import openai
    except ImportError:
        raise SystemExit("openai package missing. Run: pip install openai")

    client = openai.OpenAI(api_key=api_key)
    memory = load_memory()

    for fp in files:
        process_file(fp, client, cfg, memory, reference_context)

    save_memory(memory)
    print(f"\nMemory updated: {MEMORY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
