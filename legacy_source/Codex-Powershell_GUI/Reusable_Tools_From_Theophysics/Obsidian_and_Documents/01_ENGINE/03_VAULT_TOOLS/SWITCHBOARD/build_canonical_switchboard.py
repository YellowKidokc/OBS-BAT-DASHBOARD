from __future__ import annotations

import csv
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parent.parent
IGNORE_ROOT = Path(r"O:\999_IGNORE\Obsidian Tools\Codex_Switchboard")
REGISTRY_DIR = IGNORE_ROOT / "01_REGISTRIES"
LINKBOARD_DIR = IGNORE_ROOT / "02_LINKBOARD"
NOTE_DIR = IGNORE_ROOT
DATE = "2026-03-10"
REVIEWER = "Codex"


CLAIMS = [
    {
        "claim_id": "CLM-ENT-001",
        "domain": "ENT",
        "claim_short": "Sin equals entropy",
        "claim_text": "Sin is the moral entropy dynamic of a closed system: disorder increases unless external grace opens the system.",
        "canonical_status": "forced_conclusion",
        "proof_class": "axiom+isomorphism",
        "priority": "critical",
        "falsification_path": "Show a closed moral system increasing coherence without external input.",
        "primary_pair": "(M,S)",
        "owner": "david",
        "created_at": DATE,
    },
    {
        "claim_id": "CLM-GRA-001",
        "domain": "GRA",
        "claim_short": "Grace is external negentropy",
        "claim_text": "Grace is an exogenous coupling term that reduces moral entropy and changes sign orientation; it is not merely ordinary thermodynamic energy.",
        "canonical_status": "forced_conclusion",
        "proof_class": "boundary_condition",
        "priority": "critical",
        "falsification_path": "Demonstrate self-generated sign flip or coherence gain in a fully closed system.",
        "primary_pair": "(G,R)",
        "owner": "david",
        "created_at": DATE,
    },
    {
        "claim_id": "CLM-OBS-001",
        "domain": "OBS",
        "claim_short": "Faith maps to observation",
        "claim_text": "Faith/observation is a structural measurement operator: actualization requires observer participation and maps to the observation pole of the framework.",
        "canonical_status": "forced_conclusion",
        "proof_class": "axiom+isomorphism",
        "priority": "critical",
        "falsification_path": "Show actualization occurs without any observer-dependent measurement term.",
        "primary_pair": "(E,F)",
        "owner": "david",
        "created_at": DATE,
    },
    {
        "claim_id": "CLM-OBS-002",
        "domain": "OBS",
        "claim_short": "Terminal observer required",
        "claim_text": "The von Neumann measurement chain cannot close regressively; at least one non-regressive terminal observer condition is required.",
        "canonical_status": "forced_conclusion",
        "proof_class": "logical_necessity",
        "priority": "critical",
        "falsification_path": "Provide a coherent closure model with no terminal observer condition.",
        "primary_pair": "(E,F)",
        "owner": "david",
        "created_at": DATE,
    },
    {
        "claim_id": "CLM-COH-001",
        "domain": "COH",
        "claim_short": "Coherence is conserved",
        "claim_text": "Micro-coherence is conserved while macro-coherence cannot self-increase; closed systems need external input to move toward higher order.",
        "canonical_status": "forced_conclusion",
        "proof_class": "property+theorem",
        "priority": "critical",
        "falsification_path": "Show a closed system producing net new coherence from internal rearrangement alone.",
        "primary_pair": "(Q,C)",
        "owner": "david",
        "created_at": DATE,
    },
    {
        "claim_id": "CLM-SYS-001",
        "domain": "SYS",
        "claim_short": "System must be open",
        "claim_text": "The framework requires an open system because closed systems decay and cannot receive grace, coherence restoration, or closure conditions.",
        "canonical_status": "forced_conclusion",
        "proof_class": "integration",
        "priority": "critical",
        "falsification_path": "Show the full equation closes and remains stable under a truly closed-system ontology.",
        "primary_pair": "(G,R)|(M,S)",
        "owner": "david",
        "created_at": DATE,
    },
    {
        "claim_id": "CLM-TIM-001",
        "domain": "TIM",
        "claim_short": "Time Wall is intentional",
        "claim_text": "The Time Wall is a self-consistency boundary: complete bifurcation at (T,K) would close the system and collapse the framework.",
        "canonical_status": "forced_conclusion",
        "proof_class": "consistency_boundary",
        "priority": "high",
        "falsification_path": "Produce a clean T/K bifurcation that preserves openness and avoids self-collapse.",
        "primary_pair": "(T,K)",
        "owner": "david",
        "created_at": DATE,
    },
    {
        "claim_id": "CLM-ISO-001",
        "domain": "ISO",
        "claim_short": "Structural isomorphism is the proof test",
        "claim_text": "The framework stands or falls on structural isomorphism: topology, falloff, boundary conditions, and conservation laws must survive substitution across registers.",
        "canonical_status": "proof_architecture",
        "proof_class": "falsifiability",
        "priority": "critical",
        "falsification_path": "Find a substitution point where the structure breaks under the criterion.",
        "primary_pair": "all_pairs",
        "owner": "david",
        "created_at": DATE,
    },
    {
        "claim_id": "CLM-CON-001",
        "domain": "CON",
        "claim_short": "Oxford convergence is independent confirmation",
        "claim_text": "Independent Oxford-adjacent thinkers converge on the same destination as the equation-driven route: 4 of 7 conclusions confirmed, 2 partial, 1 unique.",
        "canonical_status": "convergence",
        "proof_class": "independent_confirmation",
        "priority": "high",
        "falsification_path": "Show the cited convergence is misrepresented or not independent of the framework.",
        "primary_pair": "cross_framework",
        "owner": "david",
        "created_at": DATE,
    },
    {
        "claim_id": "CLM-EVD-001",
        "domain": "EVD",
        "claim_short": "Empirical anomalies fit the framework",
        "claim_text": "PEAR, GCP, and social-coherence datasets do not prove the framework, but they match the predicted direction of consciousness/coherence coupling.",
        "canonical_status": "evidence_layer",
        "proof_class": "empirical_support",
        "priority": "high",
        "falsification_path": "Replicate null results or show the datasets are statistical artifacts under stronger controls.",
        "primary_pair": "(E,F)|(Q,C)",
        "owner": "david",
        "created_at": DATE,
    },
    {
        "claim_id": "CLM-LAW-001",
        "domain": "LAW",
        "claim_short": "Ten Laws integrate the proof architecture",
        "claim_text": "The Ten Laws provide the paired operator map that distributes the framework across domains and ties individual claims back to the master equation.",
        "canonical_status": "integration",
        "proof_class": "law_mapping",
        "priority": "high",
        "falsification_path": "Show the law pairings fail to preserve the canonical variable architecture.",
        "primary_pair": "ten_laws",
        "owner": "david",
        "created_at": DATE,
    },
    {
        "claim_id": "CLM-AI-001",
        "domain": "AI",
        "claim_short": "AI alignment is an external-orientation problem",
        "claim_text": "Frontier AI alignment is structurally an attempt to impose an external orientation term on a system that cannot securely self-ground truth from inside its own optimization loop.",
        "canonical_status": "candidate_isomorphism",
        "proof_class": "ai_alignment_isomorphism",
        "priority": "high",
        "falsification_path": "Show a sufficiently capable system can reliably self-ground truth alignment without externally imposed orientation, constitutional constraints, or reward feedback.",
        "primary_pair": "(G,R)|(E,F)|(Q,C)",
        "owner": "david",
        "created_at": DATE,
    },
]


EVIDENCE = [
    {
        "evidence_id": "EVD-DOC-001",
        "evidence_type": "canonical_doc",
        "title": "Canonical Framing",
        "source_path": r"O:\_Theophysics_v3\00_SYSTEM\CANONICAL_FRAMING.md",
        "anchor_kind": "framework_control",
        "canonical_role": "settled_claims",
        "summary": "Defines the seven forced conclusions, isomorphism criterion, Time Wall, Oxford convergence, and experimental dataset framing.",
        "status": "canonical",
    },
    {
        "evidence_id": "EVD-DOC-002",
        "evidence_type": "equation_doc",
        "title": "Ten Laws Equations",
        "source_path": r"O:\_Theophysics_v3\00_Canonical\01_CORE\MASTER_EQUATION\02_TEN_LAWS\_TEN_LAWS_EQUATIONS.md",
        "anchor_kind": "law_map",
        "canonical_role": "operator_distribution",
        "summary": "Provides the law-level operator map and symmetry architecture for the ten-law system.",
        "status": "canonical",
    },
    {
        "evidence_id": "EVD-DOC-003",
        "evidence_type": "html_registry",
        "title": "Structural Isomorphism Hub",
        "source_path": r"O:\_Theophysics_v3\00_Canonical\01_CORE\MASTER_EQUATION\structural-isomorphism.html",
        "anchor_kind": "proof_hub",
        "canonical_role": "isomorphism_index",
        "summary": "Primary structural-isomorphism anchor referenced by the vault instructions.",
        "status": "canonical",
    },
    {
        "evidence_id": "EVD-AXM-001",
        "evidence_type": "axiom",
        "title": "P3.2 Coherence Conservation",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\024_P3.2_Coherence-Conservation.md",
        "anchor_kind": "formal_axiom",
        "canonical_role": "coherence_property",
        "summary": "States that micro-coherence is conserved in closed systems.",
        "status": "canonical",
    },
    {
        "evidence_id": "EVD-AXM-002",
        "evidence_type": "axiom",
        "title": "T3.1 Coherence Cannot Self-Increase",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\025_T3.1_Coherence-Cannot-Self-Increase.md",
        "anchor_kind": "formal_theorem",
        "canonical_role": "open_system_requirement",
        "summary": "Shows macro-coherence cannot self-increase without external input.",
        "status": "canonical",
    },
    {
        "evidence_id": "EVD-AXM-003",
        "evidence_type": "axiom",
        "title": "LN5.1 Chi Requires Observer For Actualization",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\044_LN5.1_Chi-Requires-Observer-For-Actualization.md",
        "anchor_kind": "logical_necessity",
        "canonical_role": "observer_requirement",
        "summary": "States that chi remains potential without observer participation.",
        "status": "canonical",
    },
    {
        "evidence_id": "EVD-AXM-004",
        "evidence_type": "axiom",
        "title": "LN6.1 Terminal Observer Necessity",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\055_LN6.1_Terminal-Observer-Necessity.md",
        "anchor_kind": "logical_necessity",
        "canonical_role": "measurement_chain_closure",
        "summary": "Requires a non-regressive terminal observer to close the measurement chain.",
        "status": "canonical",
    },
    {
        "evidence_id": "EVD-AXM-005",
        "evidence_type": "axiom",
        "title": "BC1 Terminal Observer Exists",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\058_BC1_Terminal-Observer-Exists.md",
        "anchor_kind": "boundary_condition",
        "canonical_role": "terminal_observer",
        "summary": "Boundary condition asserting terminal observer existence.",
        "status": "canonical",
    },
    {
        "evidence_id": "EVD-AXM-006",
        "evidence_type": "axiom",
        "title": "BC2 Grace External To System",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\059_BC2_Grace-External-To-System.md",
        "anchor_kind": "boundary_condition",
        "canonical_role": "external_grace",
        "summary": "Defines grace as external informational input that reduces moral entropy.",
        "status": "canonical",
    },
    {
        "evidence_id": "EVD-AXM-007",
        "evidence_type": "axiom",
        "title": "EV15.1 Biblical Prophecy Validation",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\110_EV15.1_Biblical-Prophecy-Validation.md",
        "anchor_kind": "empirical_axiom",
        "canonical_role": "prophecy_dataset",
        "summary": "Axiomized empirical bridge for fulfilled-prophecy validation.",
        "status": "canonical",
    },
    {
        "evidence_id": "EVD-AXM-008",
        "evidence_type": "axiom",
        "title": "EV15.2 GCP Correlation",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\111_EV15.2_GCP-Correlation.md",
        "anchor_kind": "empirical_axiom",
        "canonical_role": "global_consciousness_dataset",
        "summary": "Records claimed GCP significance for collective attention and RNG deviation.",
        "status": "contested_evidence",
    },
    {
        "evidence_id": "EVD-AXM-009",
        "evidence_type": "axiom",
        "title": "EV15.3 PEAR Lab Results",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\112_EV15.3_PEAR-Lab-Results.md",
        "anchor_kind": "empirical_axiom",
        "canonical_role": "pear_dataset",
        "summary": "Records PEAR human-machine interaction results as suggestive evidence.",
        "status": "contested_evidence",
    },
    {
        "evidence_id": "EVD-AXM-010",
        "evidence_type": "axiom",
        "title": "EV15.4 Social Coherence 5.7 Sigma",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\113_EV15.4_Social-Coherence-5.7-Sigma.md",
        "anchor_kind": "empirical_axiom",
        "canonical_role": "social_coherence_dataset",
        "summary": "Records group-coherence studies as social-scale evidence.",
        "status": "evidence",
    },
    {
        "evidence_id": "EVD-AXM-011",
        "evidence_type": "axiom",
        "title": "PROT18.3 Grace Negentropy Detection",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\127_PROT18.3_Grace-Negentropy-Detection.md",
        "anchor_kind": "protocol",
        "canonical_role": "test_protocol",
        "summary": "Detection protocol for grace-negentropy signatures.",
        "status": "protocol",
    },
    {
        "evidence_id": "EVD-AXM-012",
        "evidence_type": "axiom",
        "title": "PROT18.4 Social Coherence Monitoring",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\128_PROT18.4_Social-Coherence-Monitoring.md",
        "anchor_kind": "protocol",
        "canonical_role": "monitoring_protocol",
        "summary": "Monitoring protocol for social coherence effects.",
        "status": "protocol",
    },
    {
        "evidence_id": "EVD-AXM-013",
        "evidence_type": "axiom",
        "title": "PRED18.2 GCP Event Prediction",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\131_PRED18.2_GCP-Event-Prediction.md",
        "anchor_kind": "prediction",
        "canonical_role": "forecast_test",
        "summary": "Prediction layer for future GCP-type event deviations.",
        "status": "prediction",
    },
    {
        "evidence_id": "EVD-AXM-014",
        "evidence_type": "axiom",
        "title": "FALS18.2 Grace Falsification",
        "source_path": r"O:\_Theophysics_v3\00_AXIOMS\01_AXIOMS_CLEAN\SEQUENTIAL_001-190\133_FALS18.2_Grace-Falsification.md",
        "anchor_kind": "falsification",
        "canonical_role": "failure_test",
        "summary": "Explicit falsification route for grace-related claims.",
        "status": "falsification",
    },
    {
        "evidence_id": "EVD-ISO-001",
        "evidence_type": "isomorphism",
        "title": "ISO-003 Entropy / Sin",
        "source_path": r"O:\_Theophysics_v3\05_EVIDENCE_ENGINE\Isomorphism\ISO-003_Entropy_Sin.md",
        "anchor_kind": "structural_isomorphism",
        "canonical_role": "entropy_sin_mapping",
        "summary": "Maps thermodynamic entropy to moral disorder as a closed-system topology.",
        "status": "testing",
    },
    {
        "evidence_id": "EVD-ISO-002",
        "evidence_type": "isomorphism",
        "title": "ISO-010 Observer Participation",
        "source_path": r"O:\_Theophysics_v3\05_EVIDENCE_ENGINE\Isomorphism\ISO-010_Observer_Participation.md",
        "anchor_kind": "structural_isomorphism",
        "canonical_role": "observer_mapping",
        "summary": "Maps observer participation across physics and theology frames.",
        "status": "candidate",
    },
    {
        "evidence_id": "EVD-ISO-003",
        "evidence_type": "isomorphism",
        "title": "ISO-013 Grace Operator",
        "source_path": r"O:\_Theophysics_v3\05_EVIDENCE_ENGINE\Isomorphism\ISO-013_Grace_Operator.md",
        "anchor_kind": "structural_isomorphism",
        "canonical_role": "grace_operator_mapping",
        "summary": "Frames grace as an operator-level intervention rather than metaphorical overlay.",
        "status": "candidate",
    },
    {
        "evidence_id": "EVD-ISO-004",
        "evidence_type": "isomorphism",
        "title": "ISO-019 Boundary Conditions",
        "source_path": r"O:\_Theophysics_v3\05_EVIDENCE_ENGINE\Isomorphism\ISO-019_Boundary_Conditions.md",
        "anchor_kind": "structural_isomorphism",
        "canonical_role": "boundary_mapping",
        "summary": "Boundary-condition mapping for closure, openness, and system constraints.",
        "status": "candidate",
    },
    {
        "evidence_id": "EVD-ISO-005",
        "evidence_type": "isomorphism",
        "title": "ISO-021 Falsifiability Architecture",
        "source_path": r"O:\_Theophysics_v3\05_EVIDENCE_ENGINE\Isomorphism\ISO-021_Falsifiability_Architecture.md",
        "anchor_kind": "falsifiability",
        "canonical_role": "test_architecture",
        "summary": "Formalizes how the framework lives or dies by testable structure rather than rhetoric.",
        "status": "candidate",
    },
    {
        "evidence_id": "EVD-ISO-006",
        "evidence_type": "isomorphism",
        "title": "ISO-022 Ten Laws Integration",
        "source_path": r"O:\_Theophysics_v3\05_EVIDENCE_ENGINE\Isomorphism\ISO-022_Ten_Laws_Integration.md",
        "anchor_kind": "integration",
        "canonical_role": "law_integration",
        "summary": "Connects isomorphism work back into the ten-law operator architecture.",
        "status": "candidate",
    },
    {
        "evidence_id": "EVD-ISO-007",
        "evidence_type": "isomorphism",
        "title": "ISO-023 Consilience",
        "source_path": r"O:\_Theophysics_v3\05_EVIDENCE_ENGINE\Isomorphism\ISO-023_Consilience.md",
        "anchor_kind": "convergence",
        "canonical_role": "consilience",
        "summary": "Aggregates cross-domain convergence logic for the framework.",
        "status": "candidate",
    },
    {
        "evidence_id": "EVD-SYN-001",
        "evidence_type": "synthesis_note",
        "title": "Alignment Problem as Inadvertent Theology",
        "source_path": r"O:\_Theophysics_v3\05_EVIDENCE_ENGINE\07_SYNTHESIS_NOTES\ALIGNMENT_PROBLEM_AS_INADVERTENT_THEOLOGY_2026-03-10.md",
        "anchor_kind": "ai_alignment_synthesis",
        "canonical_role": "alignment_grace_mapping",
        "summary": "Preserves the claim that RLHF, constitutions, and reward models behave like engineered external orientation terms.",
        "status": "candidate",
    },
    {
        "evidence_id": "EVD-SYN-002",
        "evidence_type": "synthesis_note",
        "title": "FP Alignment Isomorphism Map",
        "source_path": r"O:\_Theophysics_v3\05_EVIDENCE_ENGINE\07_SYNTHESIS_NOTES\FP_ALIGNMENT_ISOMORPHISM_MAP_2026-03-10.md",
        "anchor_kind": "fp_alignment_map",
        "canonical_role": "fp17_scaffold",
        "summary": "Maps 14 of 16 FP papers into direct or strong AI-alignment isomorphism territory.",
        "status": "active",
    },
]


LINKS = [
    ("CLM-ENT-001", "EVD-DOC-001", "supports", 0.98, 0.98, "Canonical framing lists sin=entropy as a forced conclusion."),
    ("CLM-ENT-001", "EVD-AXM-002", "supports", 0.93, 0.91, "Closed-system coherence cannot self-increase, which is the entropy-side engine of the claim."),
    ("CLM-ENT-001", "EVD-ISO-001", "supports", 0.90, 0.86, "ISO-003 supplies the structural entropy/sin swap test."),
    ("CLM-GRA-001", "EVD-DOC-001", "supports", 0.98, 0.98, "Canonical framing lists grace as external negentropy."),
    ("CLM-GRA-001", "EVD-AXM-006", "supports", 0.95, 0.93, "BC2 defines grace as external informational input acting on moral entropy."),
    ("CLM-GRA-001", "EVD-ISO-003", "supports", 0.84, 0.79, "Grace operator mapping strengthens the operator-level reading."),
    ("CLM-GRA-001", "EVD-AXM-011", "method", 0.72, 0.68, "PROT18.3 defines a detection route rather than a direct proof."),
    ("CLM-OBS-001", "EVD-DOC-001", "supports", 0.96, 0.96, "Canonical framing forces faith=observation."),
    ("CLM-OBS-001", "EVD-AXM-003", "supports", 0.91, 0.88, "LN5.1 ties actualization to observer participation."),
    ("CLM-OBS-001", "EVD-ISO-002", "supports", 0.86, 0.80, "Observer-participation isomorphism extends the mapping across domains."),
    ("CLM-OBS-002", "EVD-DOC-001", "supports", 0.97, 0.97, "Canonical framing lists terminal observer as a forced conclusion."),
    ("CLM-OBS-002", "EVD-AXM-004", "supports", 0.95, 0.92, "LN6.1 states the non-regressive terminal observer requirement explicitly."),
    ("CLM-OBS-002", "EVD-AXM-005", "supports", 0.89, 0.87, "BC1 converts the necessity into a boundary condition."),
    ("CLM-COH-001", "EVD-DOC-001", "supports", 0.96, 0.96, "Canonical framing lists coherence conservation as a forced conclusion."),
    ("CLM-COH-001", "EVD-AXM-001", "supports", 0.93, 0.90, "P3.2 states coherence conservation at the micro level."),
    ("CLM-COH-001", "EVD-AXM-002", "supports", 0.95, 0.92, "T3.1 states that macro-coherence cannot self-increase."),
    ("CLM-SYS-001", "EVD-DOC-001", "supports", 0.98, 0.98, "Canonical framing explicitly says the system must be open."),
    ("CLM-SYS-001", "EVD-AXM-002", "supports", 0.93, 0.90, "Open-system requirement follows from inability of closed systems to self-increase coherence."),
    ("CLM-SYS-001", "EVD-AXM-006", "supports", 0.91, 0.88, "BC2 supplies the external-input mechanism needed by the open system."),
    ("CLM-SYS-001", "EVD-ISO-004", "supports", 0.80, 0.75, "Boundary-condition isomorphism supports the open/closed system distinction."),
    ("CLM-TIM-001", "EVD-DOC-001", "supports", 0.99, 0.99, "Time Wall is declared a settled self-consistency boundary in canonical framing."),
    ("CLM-ISO-001", "EVD-DOC-001", "supports", 0.99, 0.99, "Canonical framing defines the isomorphism criterion as the falsification test."),
    ("CLM-ISO-001", "EVD-DOC-003", "context", 0.84, 0.82, "The structural-isomorphism hub is the central navigation object for the proof architecture."),
    ("CLM-ISO-001", "EVD-ISO-005", "supports", 0.93, 0.88, "ISO-021 formalizes the falsifiability architecture."),
    ("CLM-ISO-001", "EVD-ISO-007", "supports", 0.82, 0.76, "Consilience record shows cross-domain convergence under the same architecture."),
    ("CLM-CON-001", "EVD-DOC-001", "supports", 0.95, 0.94, "Canonical framing contains the Oxford convergence scorecard."),
    ("CLM-CON-001", "EVD-ISO-007", "context", 0.76, 0.71, "Consilience work is adjacent support for independent convergence logic."),
    ("CLM-EVD-001", "EVD-DOC-001", "supports", 0.92, 0.90, "Canonical framing names the experimental datasets and their significance."),
    ("CLM-EVD-001", "EVD-AXM-008", "supports", 0.82, 0.73, "GCP is one empirical anomaly pillar for consciousness/coherence coupling."),
    ("CLM-EVD-001", "EVD-AXM-009", "supports", 0.80, 0.71, "PEAR is a second empirical anomaly pillar for consciousness coupling."),
    ("CLM-EVD-001", "EVD-AXM-010", "supports", 0.86, 0.78, "Social coherence studies add a macro-scale anomaly layer."),
    ("CLM-EVD-001", "EVD-AXM-013", "predicts", 0.70, 0.66, "Prediction layer extends empirical support into future tests."),
    ("CLM-EVD-001", "EVD-AXM-014", "falsifies", 0.74, 0.72, "Grace falsification route keeps the empirical claim accountable."),
    ("CLM-LAW-001", "EVD-DOC-002", "supports", 0.96, 0.95, "Ten Laws equations are the operator backbone for the law-level system."),
    ("CLM-LAW-001", "EVD-ISO-006", "supports", 0.87, 0.82, "ISO-022 connects the laws to the isomorphism architecture."),
    ("CLM-LAW-001", "EVD-DOC-001", "context", 0.76, 0.74, "Canonical framing names the canonical variable order and symmetry pairs that the laws distribute."),
    ("CLM-AI-001", "EVD-SYN-001", "supports", 0.89, 0.84, "The alignment note states the external-orientation problem directly in AI terms."),
    ("CLM-AI-001", "EVD-SYN-002", "supports", 0.86, 0.82, "The FP alignment map shows that the claim is distributed across the existing paper stack."),
    ("CLM-AI-001", "EVD-ISO-003", "supports", 0.78, 0.73, "Grace-operator framing supports the external-orientation interpretation."),
    ("CLM-AI-001", "EVD-ISO-005", "supports", 0.76, 0.71, "Falsifiability architecture supplies the test language for alignment-drift claims."),
    ("CLM-AI-001", "EVD-AXM-006", "context", 0.72, 0.69, "BC2 provides the core external-input pattern being mapped into alignment."),
]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def render_markdown_table(fieldnames: list[str], rows: list[dict[str, object]]) -> str:
    header = "| " + " | ".join(fieldnames) + " |"
    divider = "|---" * len(fieldnames) + "|"
    body = [
        "| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fieldnames) + " |"
        for row in rows
    ]
    return "\n".join([header, divider] + body)


def build_link_rows() -> list[dict[str, object]]:
    rows = []
    for index, (claim_id, evidence_id, relation, weight, confidence, rationale) in enumerate(LINKS, start=1):
        rows.append(
            {
                "link_id": f"LNK-CAN-{index:03d}",
                "claim_id": claim_id,
                "evidence_id": evidence_id,
                "relation": relation,
                "weight_0_1": f"{weight:.2f}",
                "confidence_0_1": f"{confidence:.2f}",
                "rationale": rationale,
                "reviewer": REVIEWER,
                "reviewed_at": DATE,
            }
        )
    return rows


def build_claims_markdown(claim_rows: list[dict[str, object]]) -> str:
    fields = ["claim_id", "domain", "claim_short", "canonical_status", "proof_class", "priority", "primary_pair"]
    table = render_markdown_table(fields, claim_rows)
    return f"""---
title: "Claims Register"
status: active
updated: {DATE}
purpose: "Canonical claim layer for the evidence switchboard."
---

# Claims Register

## Canonical Claims

{table}

Notes:
- `claim_id` is permanent.
- These rows are the curated switchboard claims, not the full future universe of claims.
- The claim texts and falsification paths live in `CANONICAL_CLAIMS_MASTER.csv`.
"""


def build_evidence_markdown(evidence_rows: list[dict[str, object]]) -> str:
    fields = ["evidence_id", "evidence_type", "title", "anchor_kind", "canonical_role", "status"]
    table = render_markdown_table(fields, evidence_rows)
    return f"""---
title: "Evidence Register"
status: active
updated: {DATE}
purpose: "Curated evidence anchors for the canonical switchboard."
---

# Evidence Register

## Curated Evidence Anchors

{table}

## Generated Master Registry (2026-03-09 Pass 2)

- Evidence rows: `1167`
- Link rows: `1167`
- Source manifest: `03_EXPORTS_INBOX/2026-03-09/_AGGREGATED_EXCEL_PASS2/_MANIFEST/copied_files_manifest.csv`
- Master CSV: `01_REGISTRIES/EVIDENCE_FILES_MASTER.csv`
- Master workbook: `01_REGISTRIES/EVIDENCE_FILES_MASTER.xlsx`
- Detachable links: `02_LINKBOARD/EVIDENCE_LINKS_MASTER.csv`
- Build summary: `04_REPORTS/evidence_registry_build_summary.json`

Contract:
- Keep evidence rows immutable.
- Use curated anchors for claim wiring.
- Keep bucket/path links separate from claim links.
"""


def build_switchboard_markdown(link_rows: list[dict[str, object]]) -> str:
    fields = [
        "link_id",
        "claim_id",
        "evidence_id",
        "relation",
        "weight_0_1",
        "confidence_0_1",
        "reviewer",
        "reviewed_at",
    ]
    table = render_markdown_table(fields, link_rows)
    return f"""---
title: "Claim-Evidence Switchboard"
status: active
updated: {DATE}
purpose: "Curated claim-to-evidence wiring layer for canonical framework claims."
---

# Claim-Evidence Switchboard

## Curated Links

{table}

Rules:
- This is the canonical claim-wiring layer.
- `EVIDENCE_LINKS_MASTER.csv` remains the inventory/path linkboard.
- `CLAIM_EVIDENCE_LINKS_CURATED.csv` is the claim-proof switchboard.
- File moves do not break curated links if the anchor path is updated in the evidence register.
"""


def main() -> None:
    claim_rows = CLAIMS
    evidence_rows = EVIDENCE
    link_rows = build_link_rows()

    NOTE_DIR.mkdir(parents=True, exist_ok=True)

    write_csv(
        REGISTRY_DIR / "CANONICAL_CLAIMS_MASTER.csv",
        [
            "claim_id",
            "domain",
            "claim_short",
            "claim_text",
            "canonical_status",
            "proof_class",
            "priority",
            "falsification_path",
            "primary_pair",
            "owner",
            "created_at",
        ],
        claim_rows,
    )
    write_csv(
        REGISTRY_DIR / "CURATED_EVIDENCE_ANCHORS.csv",
        [
            "evidence_id",
            "evidence_type",
            "title",
            "source_path",
            "anchor_kind",
            "canonical_role",
            "summary",
            "status",
        ],
        evidence_rows,
    )
    write_csv(
        LINKBOARD_DIR / "CLAIM_EVIDENCE_LINKS_CURATED.csv",
        [
            "link_id",
            "claim_id",
            "evidence_id",
            "relation",
            "weight_0_1",
            "confidence_0_1",
            "rationale",
            "reviewer",
            "reviewed_at",
        ],
        link_rows,
    )

    (REGISTRY_DIR / "CLAIMS_REGISTER.md").write_text(build_claims_markdown(claim_rows), encoding="utf-8")
    (REGISTRY_DIR / "EVIDENCE_REGISTER.md").write_text(build_evidence_markdown(evidence_rows), encoding="utf-8")
    (LINKBOARD_DIR / "CLAIM_EVIDENCE_SWITCHBOARD.md").write_text(build_switchboard_markdown(link_rows), encoding="utf-8")
    (NOTE_DIR / "README.md").write_text(
        "# Codex Switchboard Data\n\n"
        "This folder stores generated switchboard CSV and JSON artifacts for Codex work.\n\n"
        "Human-readable markdown views still live inside `O:\\_Theophysics_v3\\05_EVIDENCE_ENGINE`.\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(claim_rows)} claims, {len(evidence_rows)} evidence anchors, and {len(link_rows)} curated links.")


if __name__ == "__main__":
    main()
