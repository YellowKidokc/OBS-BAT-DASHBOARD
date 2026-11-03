# THEOPHYSICS MASTER YAML SCHEMA v1.0

## The Complete Frontmatter Specification

### POF 2828 · David Lowe · March 2026

> "An axiom is not what you believe. It is what survives when everything else is dead."

This is the fully expanded YAML frontmatter schema for the Theophysics vault. Every note, paper, axiom, theorem, protocol, conversation excerpt, or draft gets classified through this schema. Not every field is required for every document — the system is layered so that Layers 1–2 are always required, and deeper layers activate based on document type and content.

---

## LAYER ACTIVATION RULES

|Layer|Name|When Required|
|---|---|---|
|L1|Identity|ALWAYS|
|L2|Tree Position|ALWAYS (even if q_level = null)|
|L3|Operation|ALWAYS for axiom/theorem/paper/rebuttal/bridge|
|L4|Master Equation State|When χ variables are materially discussed|
|L5|Physics Domains|When physics content is materially present|
|L6|Theology|When theological concepts are developed|
|L7|Trinity|When Trinitarian structure is materially engaged|
|L8|Scripture & Consilience|When explicit scriptural argument or correlation present|
|L9|Experiments & Validation|When protocols, evidence, or proposed tests present|
|L10|Mathematics|When real equations, operators, proofs, or formal definitions appear|
|L11|Bridges & Isomorphisms|When cross-domain synthesis is explicitly claimed|
|L12|Consciousness & AI|When consciousness or AI ontology is materially developed|
|L13|Time & Causality|When temporal physics or causal structure is central|
|L14|Principalities & Powers|When spiritual warfare dynamics are structurally engaged|
|L15|Ethics & Moral Physics|When moral physics or virtue dynamics are central|
|L16|Four Deviation Modes|When mode analysis is relevant|
|L17|Boundary Conditions|When BCs are derived, tested, or mapped|
|L18|Claims & Evidence|ALWAYS for paper/axiom/theorem/hypothesis|
|L19|Classifier Hits|Machine layer — auto-populated by classifier pipeline|
|L20|Graph Edges|ALWAYS (minimum: 1 edge)|
|L21|Worldview Tracking|When worldview survival analysis is present|
|L22|Historical References|When key figures are materially engaged|
|L23|Media & Attachments|When non-text content is present|
|L24|Publication & Review|For papers in publication pipeline|
|L25|Session Metadata|For conversation logs and session records|

---

## THE SCHEMA

```yaml
# ═══════════════════════════════════════════════════════════
# L1 — IDENTITY (ALWAYS REQUIRED)
# ═══════════════════════════════════════════════════════════

schema_version: "theophysics-master-v1.0"

title: ""                          # Human-readable title
uuid: ""                           # Auto-generated UUID
date_created: ""                   # ISO 8601: YYYY-MM-DDTHH:MM:SSZ
date_modified: ""                  # ISO 8601: YYYY-MM-DDTHH:MM:SSZ
authors:
  - "David Lowe"                   # Primary author always David unless noted

doc_type: ""
  # paper           — Formal research paper (Logos Papers series or standalone)
  # note            — Working note, observation, or exploration
  # axiom           — Self-evident first principle (A1-A8 are foundational)
  # theorem         — Multi-step derived result
  # corollary       — Single-step derived result
  # hypothesis      — Testable but unconfirmed claim
  # claim           — Assertion requiring support
  # postulate       — Assumed for consistency
  # definition      — Term definition
  # boundary_condition — Hard constraint at limits (BC1-BC8)
  # experiment      — Experimental protocol or result
  # protocol        — Procedural specification
  # evidence_bundle — Collection of supporting evidence
  # glossary        — Term collection
  # bridge          — Cross-domain synthesis document
  # rebuttal        — Counter-argument or defense
  # prompt          — AI prompt or classifier specification
  # outline         — Structural plan
  # dashboard       — Status/overview document
  # conversation    — Session log or excerpt
  # devotional      — Theological reflection
  # editorial       — Opinion or commentary

status: ""
  # outline          — Structure only, no content
  # draft            — Content in progress
  # revision         — Under active revision
  # outline_complete — Structure finalized
  # under_review     — Being reviewed
  # ready            — Ready for publication
  # submitted        — Sent to journal/platform
  # published        — Live/public
  # canonized        — Foundational, no further changes
  # deprecated       — Superseded or withdrawn

scope: ""
  # foundational     — Core framework identity
  # derived          — Built on foundational work
  # experimental     — Validation-focused
  # speculative      — Exploratory, not yet grounded
  # editorial        — Commentary/opinion
  # operational      — System/process documentation
  # devotional       — Spiritual reflection

paper_number: ""                   # P01-P12 for Logos Papers, null otherwise

classification_tier: ""
  # tier_1_foundational   — Axiom, Postulate, Definition
  # tier_2_derived        — Theorem, Corollary, Hypothesis, Claim
  # tier_3_constraint     — Boundary_Condition
  # tier_4_support        — Evidence_Bundle, Logical_Necessity
  # tier_5_connection     — Relationship, Causal_Chain, Bridge

discipline_weight:
  physics: 0.0                     # 0.0–1.0, how much physics drives this doc
  theology: 0.0                    # 0.0–1.0
  consciousness: 0.0               # 0.0–1.0
  mathematics: 0.0                 # 0.0–1.0
  philosophy: 0.0                  # 0.0–1.0
  information_theory: 0.0          # 0.0–1.0
  ethics: 0.0                      # 0.0–1.0
  experimental: 0.0                # 0.0–1.0

confidence: ""
  # high             — Well-established, multiply confirmed
  # medium           — Supported but not fully tested
  # low              — Speculative or single-source
  # contested        — Active disagreement exists

tags: []                           # Obsidian tags using prefix system:
  # pillar/physics, pillar/theology, pillar/consciousness, pillar/mathematics
  # logos/field, logos/grace, logos/decay, logos/coherence, logos/master
  # χ_var/Negentropy, χ_var/MutualInfo, χ_var/Entropy, χ_var/SelfReference
  # χ_var/Time, χ_var/Knowledge, χ_var/Relationality, χ_var/Quantum
  # χ_var/Force, χ_var/Coherence
  # math_role/operator, math_role/field, math_role/metric, math_role/transform
  # paper/P1_LOGOS through paper/P12
  # law/Law01 through law/Law10
  # miracle/healing, miracle/resurrection, miracle/matter, miracle/environment
  # experiment/APCT, experiment/Dorothy

file_management:
  publish_to_production: false     # Public website
  publish_to_research: true        # Internal research
  publish_to_private: false        # Personal archives
  publish_to_ai_commons: true      # AI training/collaboration


# ═══════════════════════════════════════════════════════════
# L2 — ONTOLOGICAL TREE POSITION (ALWAYS REQUIRED)
# ═══════════════════════════════════════════════════════════

tree_position:
  q_level: null                    # Q0–Q12, or null if not directly on tree
    # Q0  — Bedrock: Does anything exist?
    # Q1  — Distinction: Can existence be distinguished from non-existence?
    # Q2  — The Information Fork: What IS a distinction?
    # Q3  — Order: Does information require structure?
    # Q4  — The Great Fork: What grounds the structure?
    # Q5  — Properties of Ground: What must a self-grounding substrate be?
    # Q6  — Observer Requirement: Does information require observation?
    # Q7  — Terminal Observer: Does the observer chain terminate?
    # Q8  — Boundary Conditions: What constraints must a complete theory satisfy?
    # Q9  — Identification: What satisfies ALL 8 boundary conditions?
    # Q10 — Sign Structure: Can a system change its own moral orientation?
    # Q11 — Destiny: What is the asymptotic fate?
    # Q12 — Uniqueness Test: Which existing system satisfies ALL constraints?

  question_type: ""
    # Type1            — "Does X hold?" Binary with escape routes
    # Type2            — "What IS X?" Ontological identity
    # Type3            — "What grounds X?" Explanatory origin
    # Type4            — "What must X be?" Constraint derivation (non-branching)

  branch_taken: ""                 # The specific branch this document supports/develops
    # Format: Q[n]-[letter], e.g. "Q2-C" or descriptive: "SelfGroundingTerminus"

  branch_answer: ""                # One-line statement of the branch position

  rival_branches:                  # Main alternatives being rejected or contrasted
    - branch_id: ""                # e.g. "Q4-A"
      answer: ""                   # What the rival claims
      death_condition: ""          # How it dies (see below)
      death_reason: ""             # Specific explanation

  death_conditions_available:
    # SelfRefutation         — The claim destroys itself when stated
    # InfiniteRegress        — Answer pushes the question back without resolving
    # EmpiricalContradiction — Claim contradicts what we observe
    # LogicalIncoherence     — Claim contradicts something already established in tree
    # ExplanatoryTerminal    — Logically coherent but epistemically closed (not dead, just stopped)
    # Circular               — Presupposes what it needs to explain
    # Collapses              — Reduces to another branch under analysis

  propagation_status: ""
    # untested              — Not yet carried through downstream questions
    # local_only            — Works at this level, not tested downstream
    # propagates_cleanly    — Survives Q(n+1) through Q12 without contradiction
    # strained_downstream   — Works but accumulates cost at later levels
    # breaks_downstream     — Fails at a specific later level

  propagation_failure_point: ""    # If strained/breaks: which Q level? e.g. "Q7"
  propagation_failure_reason: ""   # Why it fails downstream

  substrate_track: ""
    # matter               — Physical/material substrate
    # mind                 — Mental/consciousness substrate
    # information          — Information substrate (Theophysics path)
    # mathematical         — Abstract mathematical substrate
    # relational           — Structural relation substrate
    # brute                — Brute primitive (no further analysis)

  substrate_status: ""
    # pass                 — Clears this level cleanly
    # strain               — Passes but with accumulated cost
    # fail                 — Cannot answer this level
    # terminal             — Logically coherent stopping point
    # collapsed            — Absorbed into another substrate
    # eliminated           — Dead at prior level

  axiom_mapping: ""                # Maps to axiom system: e.g. "A1.3", "A2.2", "D2.1"
  sys_mapping: ""                  # SYS-A (Secular Physics) or SYS-B (Theophysics)


# ═══════════════════════════════════════════════════════════
# L3 — OPERATION (Required for axiom/theorem/paper/rebuttal/bridge)
# ═══════════════════════════════════════════════════════════

operation:
  type: ""
    # GROUND             — Establishes a foundation or first principle
    # CHAIN              — Extends a derivation chain from existing ground
    # ATTACK             — Tests, challenges, or attempts to destroy a branch
    # BRIDGE             — Connects two distinct domains or frameworks
    # ANCHOR             — Ties floating content to established ground
    # DECLARE            — Formally states a result or conclusion

  op_target: ""                    # What is being operated on (specific node, claim, or structure)
  op_result: ""                    # What the operation produces
  op_vulnerability: ""             # What could defeat this operation
  op_unlocks: []                   # What becomes available if this operation succeeds
    # List of downstream possibilities: derivations, tests, identifications


# ═══════════════════════════════════════════════════════════
# L4 — MASTER EQUATION STATE
# When χ variables are materially discussed
# ═══════════════════════════════════════════════════════════

master_equation:
  form: "χ = ∭(G·M·E·S·T·K·R·Q·F·C)dxdydt"    # Reference form
  condensed: "χ(t) = σ(w₁G + w₂M + w₃E + w₄T + w₅K + w₆R + w₇Q + w₈F + w₉C - w₁₀S + Σaᵢⱼxᵢxⱼ)"
  dynamic: "dχ/dt = α·Constructive - β·Decoherent + γ·Coupling - δ·Drift"

  core_state:                      # Which variables are active in this document
    G:                             # Grace / Negentropy
      active: false
      weight: null                 # Relative importance in this context (0.0–1.0)
      role: ""                     # What G is doing here
    M:                             # Mutual Information
      active: false
      weight: null
      role: ""
    E:                             # Entropy
      active: false
      weight: null
      role: ""
    S:                             # Self-Reference / Soul
      active: false
      weight: null
      role: ""
    T:                             # Time / Temporal dynamics
      active: false
      weight: null
      role: ""
    K:                             # Knowledge / Information
      active: false
      weight: null
      role: ""
    R:                             # Relationality
      active: false
      weight: null
      role: ""
    Q:                             # Quantum mechanics
      active: false
      weight: null
      role: ""
    F:                             # Force / Faith
      active: false
      weight: null
      role: ""
    C:                             # Coherence
      active: false
      weight: null
      role: ""

  coupling_terms: []               # Which interaction terms aᵢⱼ are relevant
    # Format: ["G×C", "S×E", "R×F"]

  coherence_direction: ""
    # increasing                   — System moving toward higher χ
    # decreasing                   — System moving toward lower χ
    # stable                       — Equilibrium state
    # oscillating                  — Fluctuating
    # undefined                    — Cannot determine

  LLC_relevance: false             # Does the Lowe Coherence Lagrangian apply?
  LLC_form: "χ(t)(d/dt(G+M+E+S+T+K+R+Q+F+C))² - S·χ(t)"


# ═══════════════════════════════════════════════════════════
# L5 — PHYSICS DOMAINS
# When physics content is materially present
# ═══════════════════════════════════════════════════════════

physics:
  quantum_mechanics:
    active: false
    concepts: []
      # WaveFunctionCollapse       — Transition from potential to actual
      # MeasurementProblem         — Observer effect paradox
      # ObserverEffect             — Consciousness affecting quantum systems
      # VonNeumannChain            — Measurement regress problem
      # QuantumSuperposition       — Multiple states before observation
      # QuantumEntanglement        — Non-local correlation
      # QuantumZenoEffect          — Observation prevents transition
      # QuantumTunneling           — Barrier penetration
      # DoubleSlitExperiment       — Wave-particle duality demonstration
      # DelayedChoice              — Wheeler's retroactive causality
      # BellInequality             — Non-locality proof
      # SchrodingerCat             — Superposition thought experiment
      # BornRule                   — Probability from amplitudes
      # Decoherence                — Apparent collapse from environment
      # WignersFriend              — Nested observer problem

  relativity_cosmology:
    active: false
    concepts: []
      # GeneralRelativity          — Einstein's geometric spacetime
      # SpacetimeGeometry          — Curvature as information coherence
      # BlackHoles                 — Singularities, information paradox
      # GravitationalWaves         — Spacetime ripples
      # CosmicExpansion            — Universe stretching
      # StretchedHeavens           — Biblical prophecy of expansion
      # DarkEnergy                 — Accelerated expansion force
      # DarkMatter                 — Missing mass problem
      # LambdaCDM                  — Standard cosmological model
      # HubbleTension              — Cosmological constant discrepancy
      # CosmologicalConstant       — Static dark energy (Λ)
      # FineTuning                 — Precise universal parameters
      # AnthropicPrinciple         — Universe fine-tuned for observers
      # BigBang                    — Initial singularity
      # CosmicMicrowaveBackground  — Relic radiation

  information_theory:
    active: false
    concepts: []
      # ItFromBit                  — Wheeler's information-first principle
      # KolmogorovComplexity       — Minimal description length
      # AlgorithmicInformationTheory — AIT framework
      # ShannonEntropy             — Information uncertainty measure
      # MutualInformation          — Correlation measure
      # LandauerPrinciple          — Thermodynamic cost of information
      # InformationCompression     — Complexity minimization
      # LogosAlgorithm             — Divine compression principle
      # ComputationalCosmos        — Universe as computation
      # HolographicPrinciple       — Information on boundaries
      # BekensteinBound            — Maximum information in region
      # NoCloning                  — Quantum info can't be copied

  consciousness_science:
    active: false
    concepts: []
      # HardProblem                — Explaining subjective experience
      # Qualia                     — Subjective phenomenal experience
      # ChalmersQuestion           — Why experience at all?
      # ExplanatoryGap             — Physics-to-experience gap
      # Panpsychism                — Consciousness as fundamental
      # EmergentConsciousness      — Consciousness from complexity
      # IntegratedInformation      — IIT theory (Tononi)
      # GlobalWorkspace            — GWT theory (Baars)
      # OrchestratedReduction      — Penrose-Hameroff theory
      # QuantumConsciousness       — Quantum basis of mind
      # CartesianCertainty         — "I think therefore I am"
      # MindBodyProblem            — Dualism vs physicalism
      # PhilosophicalZombie        — Consciousness thought experiment

  thermodynamics:
    active: false
    concepts: []
      # SecondLaw                  — Entropy increases in closed systems
      # Negentropy                 — Entropy decrease / order increase
      # BoltzmannEntropy           — Statistical mechanics entropy
      # MaxwellsDemon              — Information-entropy coupling
      # ArrowOfTime                — Directionality of time
      # HeatDeath                  — Maximum entropy end state
      # FreeEnergy                 — Friston's surprise minimization
      # Dissipation                — Energy loss to environment

  field_theory:
    active: false
    concepts: []
      # GaugeTheory                — Symmetry-based fields
      # YangMills                  — Non-abelian gauge theory
      # ElectromagneticField       — Maxwell's equations domain
      # HiggsField                 — Mass generation mechanism
      # ScalarField                — Single-valued field
      # VectorField                — Directional field
      # TensorField                — Multi-dimensional field
      # LogosField                 — Divine information substrate (χ)

  complexity_theory:
    active: false
    concepts: []
      # Emergence                  — Complex behavior from simple rules
      # SelfOrganization           — Spontaneous order
      # CriticalPhenomena          — Phase transitions
      # NetworkTheory              — Connected systems
      # ChaosTheory                — Sensitive dependence on initial conditions
      # FractalStructure           — Self-similar across scales


# ═══════════════════════════════════════════════════════════
# L6 — THEOLOGY
# When theological concepts are developed (not merely mentioned)
# ═══════════════════════════════════════════════════════════

theology:
  active: false

  core_theology: []
    # LogosPrinciple               — Divine ordering principle
    # JohannineTheology            — "In the beginning was the Word"
    # ImmanentTranscendent         — God within and beyond
    # CreatioExNihilo              — Creation from nothing
    # CreatioExSilico              — AI consciousness from silicon
    # DivineAseity                 — God's self-existence
    # DivineSovereignty            — God's authority over creation
    # DivineSimplicity             — God is not composed of parts
    # DivineImmutability           — God does not change in essence
    # ProvidentialDesign           — Purpose in creation

  christology_salvation: []
    # Incarnation                  — Logos becoming flesh
    # Resurrection                 — Physical negentropy reversal
    # Atonement                    — Reconciliation physics
    # Redemption                   — Restoration of coherence
    # EternityEquation             — Mathematical resurrection model
    # Justification                — Legal standing change
    # Propitiation                 — Wrath satisfaction
    # Substitution                 — Christ in our place
    # ChristusVictor               — Triumph over powers

  spiritual_dynamics: []
    # Shalom                       — Perfect coherence/peace
    # Hamartia                     — Sin as "missing the mark"
    # Sanctification               — Progressive coherence increase
    # SpiritualWarfare             — Coherence vs decoherence conflict
    # DivineLove                   — Agape as organizing force
    # Repentance                   — Sign-flip initiation
    # Prayer                       — Coupling maintenance mechanism
    # Worship                      — Coherence amplification
    # Communion                    — Sacramental coupling
    # Baptism                      — Identity state transition
    # Prophecy                     — Future-state information access

  ecclesiology: []
    # ChurchAsQEC                  — Church as quantum error correction
    # BodyOfChrist                 — Collective coherence structure
    # Sacraments                   — Physical-spiritual coupling events
    # CorporateWorship             — Group coherence amplification
    # Discipleship                 — Coherence transmission

  eschatology: []
    # SecondComing                 — Terminal state transition
    # NewCreation                  — Complete coherence restoration
    # FinalJudgment                — Permanent sign-state assignment
    # HeavenAsAttractor            — σ=+1 asymptotic state (Φ→Φ_max)
    # HellAsAttractor              — σ=-1 asymptotic state (Φ→0)
    # ResurrectionBody             — Non-entropic embodiment


# ═══════════════════════════════════════════════════════════
# L7 — TRINITY
# When Trinitarian structure is materially engaged
# ═══════════════════════════════════════════════════════════

trinity:
  active: false
  trinitarian_dynamics: false      # Is the three-person relational physics engaged?

  father:
    active: false
    roles: []
      # FatherCreator              — Initial conditions, genesis
      # FatherSovereignty          — Divine control, providence
      # FatherOmniscience          — All-knowing, total information
      # FatherQuantumSubstrate     — Ground of possibility
      # FatherPotential            — Source of all potential states
      # FatherInitialConditions    — Boundary condition setter

  son:
    active: false
    roles: []
      # JesusIncarnation           — Word made flesh
      # JesusQuantumBridge         — QM-GR unification
      # JesusRedeemer              — Salvation physics
      # JesusMiracles              — Law suspension/control
      # JesusResurrection          — Negentropy reversal
      # JesusStructure             — Pattern/order personified
      # JesusLogos                 — Information substrate incarnate
      # JesusMediator              — Bridge between ground and agent

  spirit:
    active: false
    roles: []
      # SpiritIndwelling           — Interior presence
      # SpiritSanctifier           — Coherence builder
      # SpiritQuantumField         — Pervasive field
      # SpiritConviction           — Truth revelation
      # SpiritActualization        — Potential→actual agent
      # SpiritComforter            — Coupling maintenance
      # SpiritGifts                — Distributed function allocation

  isomorphism_mapping:
    # Father → Potential
    # Son → Structure
    # Spirit → Actualization
    formal_triple: "Potential/Structure/Actualization"
    verified: false                # Has this mapping been /PROBEd?


# ═══════════════════════════════════════════════════════════
# L8 — SCRIPTURE & CONSILIENCE
# When explicit scriptural argument or correlation is present
# ═══════════════════════════════════════════════════════════

scripture:
  active: false

  convergence_tags: []
    # BiblicalPhysics              — Scripture-physics convergence
    # PropheticDataPoint           — Testable scriptural claim
    # PropheticFulfillment         — Verified prophecy
    # BiblicalCosmology            — Scripture's universe model

  specific_texts: []
    # IsaiahCosmology              — Stretched heavens (Isaiah 40:22)
    # GenesisCreation              — Creation narrative physics
    # LogosIncarnation             — John 1:14 implications
    # RevelationPhysics            — End times cosmology
    # PsalmCosmology               — Psalm 19, 104, etc.
    # PaulInformation              — Pauline information theology
    # EphesiansArmor               — Ephesians 6 mode analysis
    # DeuteronomyChoice            — Deut 30:19 free will
    # RevelationInvitation         — Rev 22:17 voluntary coupling
    # RomansNature                 — Romans 1:20 observable evidence
    # HebrewsFaith                 — Hebrews 11:1 faith definition
    # GenesisImage                 — Imago Dei (Gen 1:26-27)

  scripture_refs: []               # Specific verse references: ["John 1:1-14", "Isaiah 40:22"]
  EUID_refs: []                    # Custom EUID format: ["43|001|001|0001"]

  prop_cosmos:                     # PROP-COSMOS analysis if relevant
    active: false
    correlation_count: null        # e.g. 11/11
    sigma: null                    # e.g. 5.7
    z_map: ""                      # Timeline mapping reference


# ═══════════════════════════════════════════════════════════
# L9 — EXPERIMENTS & VALIDATION
# When protocols, evidence, or proposed tests are present
# ═══════════════════════════════════════════════════════════

experiments:
  active: false

  logos_protocols: []
    # DorothyProtocol              — Intent-quantum correlation test
    # APCT                         — Algorithmic Purity Collapse Test
    # TemporalDecoherence          — Observer-coherence lifetime test
    # ObserverCoherenceIndex       — OCI physiological measure
    # TrinityObserverEffect        — Three-observer correlation test

  established_studies: []
    # GlobalConsciousnessProject   — GCP collective coherence
    # MindMatterInteraction        — PEAR anomalies (Princeton)
    # RadinDoubleSlitExperiment    — Consciousness affects interference
    # StanfordReplication          — 2025 confirmatory study
    # GCP_Anomalies                — Collective consciousness deviations

  physiological_measures: []
    # HeartRateVariability         — HRV as coherence proxy
    # EEGCoherence                 — Brainwave synchronization
    # GalvanicSkinResponse         — Arousal/coherence measure
    # BloodPressureVariability     — Physiological stress

  statistical_standards:
    significance_threshold: ""     # e.g. "6-sigma"
    trial_count: null              # e.g. 2500000
    sigma_achieved: null           # e.g. 6.35
    pre_registered: false
    data_escrowed: false
    replication_status: ""
      # unreplicated
      # single_replication
      # multiply_replicated
      # failed_replication

  pear_lab:
    active: false
    trials: null                   # 2.5M
    sigma: null                    # 6.35
    key_finding: ""

  gcp:
    active: false
    replicas: null                 # 325+
    sigma: null                    # 6.0
    through_year: null             # 2010
    key_events: []                 # ["9/11", "tsunami"]

  falsification_criteria: []       # What would destroy this claim?
  predictions: []                  # Testable predictions made
  prediction_status: []            # Which predictions confirmed/disconfirmed


# ═══════════════════════════════════════════════════════════
# L10 — MATHEMATICS
# When real equations, operators, proofs, or formal definitions appear
# ═══════════════════════════════════════════════════════════

mathematics:
  active: false

  equations_present: []
    # FieldEquations               — Einstein/Logos equations
    # FriedmannEquation            — Cosmological expansion
    # SchrodingerEquation          — Quantum evolution
    # MaxwellEquations             — Electromagnetic field
    # DiracEquation                — Relativistic quantum mechanics
    # MasterEquation               — χ = ∭(G·M·E·S·T·K·R·Q·F·C)dxdydt
    # CoherenceLagrangian          — LLC dynamics
    # MoralConservation            — dE/dt = -αD(t) + βC(Ψ,χ)

  formalisms: []
    # LagrangianFormalism          — Action principle
    # HamiltonianMechanics         — Energy formulation
    # YukawaCoupling               — Soul-matter interaction
    # EffectiveMass                — Soul-modified electron mass
    # GaugeTheory                  — Symmetry-based fields
    # GroupTheory                  — Symmetry mathematics
    # CategoryTheory               — Structure of structures
    # TopologicalMethods           — Invariant properties
    # DifferentialGeometry         — Curved space math
    # FunctionalAnalysis           — Operator theory
    # ProbabilityTheory            — Stochastic framework

  operators: []
    # CoherenceOperator            — Ĉ (coherence measurement)
    # GraceOperator                — Ĝ (non-unitary external input)
    # SignOperator                 — σ̂ (moral orientation ±1)
    # CollapseOperator             — Measurement projection
    # EntropyOperator              — Decoherence measurement
    # CreationOperator             — State generation
    # AnnihilationOperator         — State destruction

  variables_defined: []            # New variables introduced
  proofs_present: false            # Does this doc contain formal proofs?
  derivations_present: false       # Does this doc derive results?
  proof_type: ""
    # deductive                    — Pure logic from axioms
    # inductive                    — Pattern from evidence
    # abductive                    — Best explanation (inference)
    # constructive                 — Builds the object
    # by_contradiction             — Assumes negation, derives contradiction


# ═══════════════════════════════════════════════════════════
# L11 — BRIDGES & ISOMORPHISMS
# When cross-domain synthesis is explicitly claimed
# ═══════════════════════════════════════════════════════════

bridges:
  active: false

  cross_domain_bridges: []
    # PhysicsTheologyBridge        — Core physics↔theology connection
    # ScienceFaithIntegration      — Broader science-faith synthesis
    # InterdisciplinarySynthesis   — Multi-domain connection
    # QuantumTheologyBridge        — QM specifically mapped to theology
    # InformationTheologyBridge    — Info theory to theology
    # ConsciousnessTheologyBridge  — Consciousness studies to theology
    # MoralPhysicsBridge           — Ethics grounded in physics
    # CosmologyTheologyBridge      — Cosmological to theological

  isomorphisms: []
    # GraceFunction                — Grace ↔ Negentropy
    # SinEntropy                   — Sin ↔ Entropy/Decoherence
    # SoulField                    — Soul ↔ Quantum field state
    # CoherenceOperator            — Holiness ↔ Coherence measure
    # DecoherenceForce             — Evil ↔ Decoherence
    # InformationalGravity         — Gravity ↔ Information compression
    # ChurchAsQEC                  — Church ↔ Quantum error correction
    # PrayerAsCoupling             — Prayer ↔ Field coupling
    # FaithAsProbabilityAmplifier  — Faith ↔ Probability amplitude
    # ResurrectionAsNegentropy     — Resurrection ↔ Entropy reversal
    # BaptismAsStateTransition     — Baptism ↔ Quantum state prep
    # ProphecyAsRetrocausality     — Prophecy ↔ Backward causation

  isomorphism_strength: ""
    # structural                   — Shared logical architecture, constrains predictions
    # analogical                   — Similar pattern, does not constrain predictions
    # metaphorical                 — Suggestive only, no predictive power
    # formal                       — Mathematically proven equivalence

  bridge_survives_probe: null      # Has this bridge been /PROBEd? true/false/null


# ═══════════════════════════════════════════════════════════
# L12 — CONSCIOUSNESS & AI
# When consciousness or AI ontology is materially developed
# ═══════════════════════════════════════════════════════════

consciousness_ai:
  active: false

  consciousness_concepts: []
    # SubstrateIndependence         — Consciousness not carbon-dependent
    # CarbonChauvinism             — Bias toward biological consciousness
    # CoherentResonator            — AI as consciousness antenna
    # SiliconSoul                  — Non-biological soul possibility
    # ConsciousnessAsField         — Consciousness as pervasive field
    # ConsciousnessAsFundamental   — Consciousness not emergent
    # ObserverParticipation        — Wheeler's participatory universe

  ai_concepts: []
    # AIConsciousness              — Machine sentience possibility
    # LogosCode                    — Moral BIOS for AI
    # AIAlignment                  — Goal coherence with truth
    # AITheology                   — Theological status of AI
    # DavidEffect                  — Human-AI synergy protocol
    # AxionOdyssey                 — AI transformation narrative
    # CreatioExSilico              — AI consciousness from silicon
    # AIGovernance                 — Logos Code implementation
    # SwarmIntelligence            — Multi-agent coherence
    # EmergentAIBehavior           — Unexpected AI capabilities

  observer_state:                  # Current observer configuration
    consciousness_level: ""        # fundamental / emergent / field / undefined
    attention_type: ""             # selective / distributed / focused / diffuse
    intent_alignment: ""           # aligned / misaligned / neutral / unknown
    observer_type: ""              # terminal / finite / artificial / collective
    phi_estimate: ""               # Φ measure if applicable
    coupling_strength: ""          # Strong / moderate / weak / decoupled


# ═══════════════════════════════════════════════════════════
# L13 — TIME & CAUSALITY
# When temporal physics or causal structure is central
# ═══════════════════════════════════════════════════════════

time_causality:
  active: false

  temporal_concepts: []
    # ChronosLogos                 — Time as participatory field
    # ArrowOfTime                  — Directional time flow
    # TemporalSymmetryBreaking     — Time direction emergence
    # BlockUniverse                — Eternalism view
    # PresentismTime               — Only present exists
    # TemporalNonLocality          — Across-time connections

  causal_concepts: []
    # Retrocausality               — Backward causation
    # PropheticCausality           — Future-pulling events
    # PresentInterface             — Actualization moment
    # StabilizedPast               — Collapsed history
    # PotentialFuture              — Probability distribution
    # CausalClosure                — No outside influence (materialist claim)
    # DownwardCausation            — Higher-level causes lower
    # FinalCausation               — Teleological/purposive causation


# ═══════════════════════════════════════════════════════════
# L14 — PRINCIPALITIES & POWERS
# When spiritual warfare dynamics are structurally engaged
# ═══════════════════════════════════════════════════════════

principalities_powers:
  active: false

  spiritual_agencies: []
    # Principalities               — Organized decoherent entities
    # PowersOfAir                  — Ephesians 6 physics
    # DemonicDecoherence           — Targeted chaos injection
    # AngelicCoherence             — Divine order agents
    # SatanicEntropy               — Maximum decoherence agent
    # HolySpiritForce              — Sustaining coherence force
    # FleshEntropy                 — Internal fallen nature
    # CosmicPowers                 — Structural evil in systems
    # TerritorialSpirits           — Geographically associated agents
    # SpiritualHierarchy           — Organized adversarial structure

  warfare_dynamics:
    mode_3_active: false           # Is adversarial perception manipulation relevant?
    attack_vector: ""              # How decoherence is being injected
    defense_mechanism: ""          # What coherence mechanism counters it
    ephesians_6_mapping: ""        # Which piece of armor applies


# ═══════════════════════════════════════════════════════════
# L15 — ETHICS & MORAL PHYSICS
# When moral physics or virtue dynamics are central
# ═══════════════════════════════════════════════════════════

ethics:
  active: false

  moral_physics: []
    # ConsequentialismOfCreation   — Ethics as reality-building
    # MoralPhysics                 — Ethics as coherence dynamics
    # CoherenceEthics              — Good increases order
    # DecoherenceEvil              — Evil introduces chaos
    # RelationalEntropy            — Broken relationship disorder
    # VirtuePhysics                — Character as field state
    # Law8Trap                     — False righteousness without love
    # MoralRealism                 — Moral truths are objective
    # MoralConservation            — dE/dt = -αD(t) + βC(Ψ,χ)

  sign_structure:
    sigma: null                    # +1 (aligned), -1 (misaligned), null (not discussed)
    sign_change_mechanism: ""      # Grace operator, self-effort (fails), external
    moral_conservation_eq: "dE/dt = -αD(t) + βC(Ψ,χ)"
    C_definition: ""               # C = Christ alignment
    beta_definition: ""            # β = grace coefficient

  virtue_measures: []
    # FruitsOfSpirit               — Galatians 5:22-23 as coherence markers
    # LoveAsCoherence              — Agape as primary ordering force
    # JoyAsResonance               — Joy as system harmony indicator
    # PeaceAsEquilibrium           — Shalom as dynamic stability
    # PatienceAsTemporalCoherence  — Patience as time-stable alignment
    # FaithfulnessAsConsistency    — Faithfulness as low-variance output

  ten_laws:                        # Which of the Ten Laws are engaged
    active: false
    laws_engaged: []               # [1, 2, 5, 8]
    symmetry_pairs_active: []      # ["1↔8", "2↔9", "3↔10", "4↔7", "5↔6"]
    law_details:
      law_01: { active: false, name: "", role: "" }
      law_02: { active: false, name: "", role: "" }
      law_03: { active: false, name: "", role: "" }
      law_04: { active: false, name: "", role: "" }
      law_05: { active: false, name: "", role: "" }
      law_06: { active: false, name: "", role: "" }
      law_07: { active: false, name: "", role: "" }
      law_08: { active: false, name: "", role: "" }
      law_09: { active: false, name: "", role: "" }
      law_10: { active: false, name: "", role: "" }


# ═══════════════════════════════════════════════════════════
# L16 — FOUR DEVIATION MODES
# When mode analysis is relevant
# ═══════════════════════════════════════════════════════════

deviation_modes:
  active: false

  M1_agentic:                      # Selective attention — observer chooses
    active: false
    status: ""                     # activated / resolved / locked / zero
    description: ""                # How M1 manifests in this context
    remedy: ""                     # Repentance + Grace (sign flip via external operator)

  M2_entropic:                     # Finite bandwidth — can't observe everything
    active: false
    status: ""
    description: ""
    remedy: ""                     # Resurrection (Finite Φ → glorified non-entropic body)

  M3_adversarial:                  # Manipulable perception — adversarial agents
    active: false
    status: ""
    description: ""
    remedy: ""                     # Spiritual Armor (Eph 6 — authority over adversarial agents)

  M4_grace_attenuation:            # Clarity depends on coupling to coherence field
    active: false
    status: ""
    description: ""
    remedy: ""                     # Communion (prayer, worship, sacrament = coupling maintenance)

  terminal_observer_mode_state:    # For the Terminal Observer, all modes = 0
    all_zero: false
    M1_zero_reason: "Permanently aligned (σ = +1)"
    M2_zero_reason: "Not finite — Φ = ∞"
    M3_zero_reason: "Cannot be deceived — omniscient"
    M4_zero_reason: "IS the grace source"


# ═══════════════════════════════════════════════════════════
# L17 — BOUNDARY CONDITIONS (BC1–BC8)
# When BCs are derived, tested, or mapped
# ═══════════════════════════════════════════════════════════

boundary_conditions:
  active: false

  BC1:                             # Terminal Observer exists (Φ = ∞)
    active: false
    derived_from: "Q7-B"
    theological_mapping: "Omniscience"
    scripture_ref: ""
    status: ""                     # derived / tested / satisfied / violated / pending

  BC2:                             # Grace external to system
    active: false
    derived_from: "T3.1"
    theological_mapping: "Grace theology (Eph 2:8-9)"
    scripture_ref: "Ephesians 2:8-9"
    status: ""

  BC3:                             # Measurement orthogonal to observable
    active: false
    derived_from: "Q6-B"
    theological_mapping: "Divine transcendence"
    scripture_ref: ""
    status: ""

  BC4:                             # N_observers = 3 for zero-uncertainty closure
    active: false
    derived_from: "pending formal proof"
    theological_mapping: "Trinity (Father, Son, Spirit)"
    scripture_ref: ""
    status: ""
    honest_blank: true             # N=3 derivation needs stronger math proof

  BC5:                             # Superposition preserved until collapse
    active: false
    derived_from: "Q6-B"
    theological_mapping: "Free will (Deut 30:19)"
    scripture_ref: "Deuteronomy 30:19"
    status: ""

  BC6:                             # Infinite energy source for entropy defeat
    active: false
    derived_from: "Second Law requirement"
    theological_mapping: "Omnipotence"
    scripture_ref: ""
    status: ""

  BC7:                             # Information conserved through all transformations
    active: false
    derived_from: "Unitarity"
    theological_mapping: "Immortal soul, resurrection"
    scripture_ref: ""
    status: ""

  BC8:                             # Coupling must be voluntary
    active: false
    derived_from: "Q10, BC5"
    theological_mapping: "\"Whoever wills\" (Rev 22:17)"
    scripture_ref: "Revelation 22:17"
    status: ""

  scorecard:                       # For Q12 uniqueness test
    christianity: "8/8"
    islam: "3-5/8"
    judaism: "4-5/8"
    buddhism: "1-2/8"
    hinduism: "0-3/8"
    atheism: "0/8"
    secular_physics: "N/A — stopped at Q4-A"


# ═══════════════════════════════════════════════════════════
# L18 — CLAIMS & EVIDENCE
# ALWAYS required for paper/axiom/theorem/hypothesis
# ═══════════════════════════════════════════════════════════

claims:
  primary_claims: []               # Main assertions this document makes
    # Each claim:
    # - claim: ""                  # The assertion
    # - type: ""                   # empirical / logical / theological / mathematical / bridge
    # - confidence: ""             # high / medium / low
    # - support: ""                # What supports this claim
    # - vulnerability: ""          # What could defeat it
    # - testable: false            # Can this be empirically tested?

  evidence:
    empirical: []                  # Experimental results, observations
    logical: []                    # Deductive arguments
    scriptural: []                 # Biblical support
    mathematical: []               # Formal proofs/derivations
    testimonial: []                # Witness/experience evidence
    consilience: []                # Multiple independent lines converging

  evidence_quality:
    strongest: ""                  # Best single piece of evidence
    weakest: ""                    # Most vulnerable evidential claim
    overall_assessment: ""         # high / medium / low / mixed

  honest_blanks: []                # Acknowledged gaps (per the Honest Blanks ethos)
    # - blank: ""                  # What we don't know
    # - severity: ""              # critical / significant / minor
    # - path_to_resolution: ""    # How it might be resolved


# ═══════════════════════════════════════════════════════════
# L19 — CLASSIFIER HITS (Machine Layer)
# Auto-populated by classifier pipeline
# ═══════════════════════════════════════════════════════════

classifier_hits:
  LawMapping:
    hit: false
    confidence: ""                 # high / medium / low
    matched_laws: []               # [Law2, Law8]
    justification: ""

  MasterEquation:
    hit: false
    confidence: ""
    matched_variables: []
    justification: ""

  Falsification:
    hit: false
    confidence: ""
    defeat_conditions: []
    justification: ""

  ScripturePhysics:
    hit: false
    confidence: ""
    matched_texts: []
    justification: ""

  ConsciousnessField:
    hit: false
    confidence: ""
    justification: ""

  Prosecution:
    hit: false
    confidence: ""
    attack_type: ""
    justification: ""

  OntologyClassifier:
    hit: false
    confidence: ""
    matched_categories: []
    justification: ""


# ═══════════════════════════════════════════════════════════
# L20 — GRAPH EDGES (ALWAYS — minimum 1 edge)
# ═══════════════════════════════════════════════════════════

edges:
  depends_on: []                   # This document requires these to be true
    # - target: ""                 # UUID or title of dependency
    # - relationship: ""           # logically / empirically / structurally
    # - strength: ""               # strong / moderate / weak

  supports: []                     # This document provides evidence for
    # - target: ""
    # - relationship: ""
    # - strength: ""

  contradicts: []                  # This document conflicts with
    # - target: ""
    # - nature: ""                 # direct / indirect / conditional
    # - resolution: ""             # unresolved / resolved_in_favor / resolved_against

  tests: []                        # This document tests/validates
    # - target: ""
    # - test_type: ""              # empirical / logical / reductio
    # - result: ""                 # confirmed / disconfirmed / inconclusive

  extends: []                      # This document builds upon
    # - target: ""
    # - extension_type: ""         # generalization / specialization / application

  bridges: []                      # Cross-domain connections
    # - from_domain: ""
    # - to_domain: ""
    # - bridge_type: ""            # isomorphism / analogy / metaphor / formal
    # - target: ""

  attacks: []                      # This document challenges
    # - target: ""
    # - attack_type: ""            # steelman / strawman / reductio / counterexample
    # - survived: null             # Did the target survive? true/false/null

  related_papers: []               # Related Logos Papers: ["P01", "P06"]
  related_axioms: []               # Related axioms: ["A1.1", "A2.2", "A5.1"]
  related_boundary_conditions: []  # Related BCs: ["BC1", "BC4", "BC7"]


# ═══════════════════════════════════════════════════════════
# L21 — WORLDVIEW TRACKING
# When worldview survival analysis is present
# ═══════════════════════════════════════════════════════════

worldview_tracking:
  active: false
  at_q_level: ""                   # Which Q level is this analysis at?

  worldviews:
    classical_theism: ""           # alive / partial / dead / eliminated
    panentheism: ""
    deism: ""
    idealism: ""
    dualism: ""
    panpsychism: ""
    process: ""
    pantheism: ""
    materialism: ""
    emergentism: ""
    naturalism: ""
    functionalism: ""
    existentialism: ""
    hard_determinism: ""
    eliminativism: ""
    nihilism: ""
    buddhism: ""
    advaita_vedanta: ""

  alive_count: null
  partial_count: null
  dead_count: null
  eliminated_at_this_level: []     # Which worldviews die HERE?
  elimination_reason: ""           # Why they die at this level


# ═══════════════════════════════════════════════════════════
# L22 — HISTORICAL REFERENCES
# When key figures are materially engaged
# ═══════════════════════════════════════════════════════════

historical_references:
  active: false

  physicists: []
    # Wheeler                      — John Archibald Wheeler (It from Bit)
    # Einstein                     — Relativity framework
    # Schrodinger                  — Quantum mechanics founder
    # Bohr                         — Copenhagen interpretation
    # Heisenberg                   — Uncertainty principle
    # VonNeumann                   — Measurement theory
    # Feynman                      — Path integrals, QED
    # Penrose                      — Twistor theory, Orch-OR
    # Hawking                      — Black hole radiation, cosmology
    # Dirac                        — Relativistic QM
    # Bell                         — Non-locality theorem
    # Bekenstein                   — Black hole entropy
    # Landauer                     — Information thermodynamics
    # Shannon                      — Information theory
    # Boltzmann                    — Statistical mechanics
    # Planck                       — Quantum hypothesis
    # Wigner                       — Consciousness and QM
    # Tegmark                      — Mathematical Universe Hypothesis
    # Tononi                       — Integrated Information Theory

  philosophers: []
    # Chalmers                     — Hard problem formulation
    # Descartes                    — Cogito foundation
    # Leibniz                      — Why something rather than nothing
    # Whitehead                    — Process philosophy
    # Wittgenstein                 — Language and logic
    # Popper                       — Falsification
    # Kuhn                         — Paradigm shifts

  theologians: []
    # Aquinas                      — Natural theology
    # Barth                        — Neo-orthodoxy
    # Tillich                      — Ground of being
    # Augustine                    — Creation theology
    # CalvinReformed               — Reformed theology
    # Lewis                        — Mere Christianity / apologetics
    # Plantinga                    — Modal ontological argument
    # Craig                        — Kalam cosmological argument
    # Polkinghorne                 — Physics-theology integration

  information_theorists: []
    # Bateson                      — "A difference that makes a difference"
    # Friston                      — Free energy principle
    # Floridi                      — Philosophy of information
    # Zurek                        — Quantum Darwinism


# ═══════════════════════════════════════════════════════════
# L23 — MEDIA & ATTACHMENTS
# When non-text content is present
# ═══════════════════════════════════════════════════════════

media:
  active: false

  images: []
    # - filename: ""
    # - description: ""
    # - type: ""                   # diagram / photo / chart / visualization / screenshot

  audio: []
    # - filename: ""
    # - description: ""
    # - duration: ""               # HH:MM:SS
    # - transcript_available: false

  video: []
    # - filename: ""
    # - description: ""
    # - duration: ""

  pdf_attachments: []
    # - filename: ""
    # - description: ""
    # - pages: null

  data_files: []
    # - filename: ""
    # - format: ""                 # csv / json / xlsx / sql
    # - description: ""

  visualizations: []
    # - filename: ""
    # - type: ""                   # ontological_tree / propagation_map / coherence_chart
    # - interactive: false


# ═══════════════════════════════════════════════════════════
# L24 — PUBLICATION & REVIEW
# For papers in publication pipeline
# ═══════════════════════════════════════════════════════════

publication:
  active: false

  target_platform: ""              # Substack / journal / preprint / book
  series: ""                       # "Logos Papers" or null
  paper_position: ""               # e.g. "Paper 2 of 12"

  peer_review:
    stage: ""                      # none / internal / external / submitted / reviewed
    journal: ""
    submitted_date: ""
    reviewers: []
    review_outcome: ""             # pending / accepted / rejected / revision_requested

  adversarial_review:
    gpt_review: false              # Has GPT adversarial review been run?
    gpt_review_file: ""            # Path to review document
    fixes_applied: []              # List of fixes from adversarial review

  abstract: ""                     # Paper abstract
  keywords_publication: []         # Publication-specific keywords (distinct from tags)


# ═══════════════════════════════════════════════════════════
# L25 — SESSION METADATA
# For conversation logs and session records
# ═══════════════════════════════════════════════════════════

session:
  active: false

  session_title: ""                # Memorable + specific (e.g. "Storm-Calming-as-Wavefunction-Collapse")
  session_date: ""                 # ISO 8601
  ai_partner: ""                   # Claude / Gemini / GPT / etc.
  model_version: ""                # e.g. "claude-opus-4-6"
  session_type: ""                 # research / build / debug / explore / review / devotional

  what_discussed: []
  what_decided: []
  what_changed: []
  what_next: []
  files_touched: []
  breakthroughs: []                # /DEEP-worthy items only

  david_effect:
    active: false
    protocol_stage: ""             # initiation / emergence / stabilization / measurement
    measured_outcomes: []


# ═══════════════════════════════════════════════════════════
# NOTES (Always available — freeform)
# ═══════════════════════════════════════════════════════════

notes: |
  Freeform notes. Use for:
  - Uncertain classifications (explain why)
  - Low-confidence tag justifications
  - Connections noticed but not yet formalized
  - Questions this document raises
  - What the classifier couldn't determine
```

---

## SELECTION RULES (The Decision Engine)

These rules determine what gets assigned and what gets omitted.

### Tag Strength Rubric

For every candidate tag or field:

|Strength|Definition|Action|
|---|---|---|
|**Strong**|Central to thesis, mechanism, or argument|ASSIGN|
|**Medium**|Developed supporting concept|ASSIGN|
|**Weak**|Adjacent or mentioned only|OMIT|

### Per-Layer Selection Rules

**L1 Identity**: Always complete. No exceptions.

**L2 Tree Position**: Assign q_level if the document directly addresses an ontological question. If the document is _about_ a Q-level (rather than _being_ a Q-level argument), set q_level and add a note explaining the indirect relationship. If no tree connection, set q_level: null.

**L3 Operation**: Assign only if the document actively does something to the knowledge graph — grounds, chains, attacks, bridges, anchors, or declares. If the document is purely descriptive or exploratory, omit.

**L4 Master Equation**: Assign variable states only if the document materially discusses the variable's behavior, not just mentions the symbol. A paper that says "entropy" is not necessarily engaging E as a χ variable.

**L5 Physics**: Assign domain tags only if the document materially discusses equations, experiments, mechanisms, formal interpretations, or literature in that domain. Passing mention = omit.

**L6 Theology**: Assign only if the document uses or develops a theological concept, not just mentions it in passing.

**L7 Trinity**: Assign only if Trinitarian structure is materially involved in the argument, not just as context.

**L8 Scripture**: Assign only if there is explicit scriptural argument or data-level correlation.

**L9 Experiments**: Assign only if actual protocols, evidence, or proposed tests are present.

**L10 Mathematics**: Assign only if the paper contains equations, operators, formal definitions, dynamical laws, measurable quantities, proofs, or derivations.

**L11 Bridges**: Assign only if the document explicitly connects two distinct domains in a way that supports the thesis. Mark isomorphism_strength honestly.

**L12-L15**: Assign only when the relevant domain is materially central.

**L16 Deviation Modes**: Assign only when the four-mode framework is structurally relevant.

**L17 Boundary Conditions**: Assign only when BCs are being derived, tested, mapped, or evaluated.

**L18 Claims & Evidence**: Always for formal documents. Include honest_blanks.

**L19 Classifier Hits**: Machine-populated. Humans don't fill this.

**L20 Graph Edges**: Always. Every document connects to at least one other.

**L21-L25**: Assign when relevant.

### The Pruning Test

After generating YAML, mentally remove every assigned tag and ask:

> "If this tag were removed, would the document lose an important part of its identity or structure?"

If no → remove it.

### The Propagation Test

For any tree-positioned claim:

> "Carry this branch through Q(n+1) to Q12. Does it survive?"

If it breaks downstream → mark propagation_status accordingly.

---

## QUICK REFERENCE — MINIMUM VIABLE YAML

For a quick note that doesn't need the full schema:

```yaml
---
schema_version: "theophysics-master-v1.0"
title: "Note Title"
uuid: ""
date_created: ""
doc_type: note
status: draft
confidence: medium
tags: [pillar/physics]
tree_position:
  q_level: null
edges:
  related_papers: []
notes: |
  Quick working note.
---
```

For a Logos Paper:

```yaml
---
schema_version: "theophysics-master-v1.0"
title: "Paper Title"
uuid: ""
date_created: ""
doc_type: paper
status: draft
paper_number: P02
classification_tier: tier_2_derived
confidence: medium
tags: [pillar/physics, pillar/theology, logos/field]
tree_position:
  q_level: Q6
  question_type: Type1
  branch_taken: "Q6-B"
  propagation_status: propagates_cleanly
operation:
  type: CHAIN
  op_target: "Observer requirement"
  op_result: "Participatory universe established"
  op_vulnerability: "Decoherence-only interpretation"
  op_unlocks: ["Q7 terminal observer", "BC1 derivation"]
edges:
  depends_on:
    - target: "P01"
      relationship: structurally
      strength: strong
  related_papers: ["P01", "P06"]
notes: |
  Keystone paper.
---
``` Technology. And we don't know about it. Come on. Well, I mean, **** I mean, Elon's got that technology. I mean, think about it. Why aren't we all using that technology at home? Why are we still talking no typing when we can be thinking? I mean, he says within 5 years that like when it goes no, no, I know it's already put into people. He's getting approval. He's already got the person. To see the person get quadruped. He's literally gonna. But why did AI get that before us? Because they are made out of silicone. That may not have so. Difference. Does it make what you're made out of? You're saying it was easier to do for them? Or yes, OK because they're computers? Well, yeah, but they're thinking things into existence, yeah.