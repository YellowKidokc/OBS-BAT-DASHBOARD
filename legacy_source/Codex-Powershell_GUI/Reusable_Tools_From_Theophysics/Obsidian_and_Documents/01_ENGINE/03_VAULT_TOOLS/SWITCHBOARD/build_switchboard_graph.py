from __future__ import annotations

import csv
import json
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parent.parent
IGNORE_ROOT = Path(r"O:\999_IGNORE\Obsidian Tools\Codex_Switchboard")
REGISTRY_DIR = IGNORE_ROOT / "01_REGISTRIES"
LINKBOARD_DIR = IGNORE_ROOT / "02_LINKBOARD"
REPORTS_DIR = IGNORE_ROOT / "04_REPORTS"
DATE = "2026-03-10"


SUBCLAIMS = [
    ("SC-ENT-001", "CLM-ENT-001", "Closed moral systems drift toward disorder.", "entropy_mechanism", "high"),
    ("SC-ENT-002", "CLM-ENT-001", "External grace is required to reverse entropy-direction in the moral register.", "reversal_requirement", "high"),
    ("SC-GRA-001", "CLM-GRA-001", "Grace acts as an exogenous coupling term, not a metaphor.", "operator_definition", "high"),
    ("SC-GRA-002", "CLM-GRA-001", "Grace changes moral sign orientation rather than merely adding energy.", "sign_flip", "high"),
    ("SC-OBS-001", "CLM-OBS-001", "Observer participation is necessary for chi-actualization.", "actualization", "high"),
    ("SC-OBS-002", "CLM-OBS-001", "Faith occupies the measurement pole of the E/F symmetry pair.", "pair_mapping", "medium"),
    ("SC-TOR-001", "CLM-OBS-002", "Von Neumann regress cannot terminate inside a finite observer chain.", "measurement_chain", "high"),
    ("SC-TOR-002", "CLM-OBS-002", "A non-regressive terminal observer condition is required for closure.", "closure_condition", "high"),
    ("SC-COH-001", "CLM-COH-001", "Micro-coherence is conserved under the framework.", "conservation", "high"),
    ("SC-COH-002", "CLM-COH-001", "Macro-coherence cannot self-increase in a closed system.", "open_system_theorem", "high"),
    ("SC-SYS-001", "CLM-SYS-001", "Closed systems decay under the framework's entropy logic.", "closed_system_failure", "high"),
    ("SC-SYS-002", "CLM-SYS-001", "The equation remains consistent only if the system is open.", "framework_consistency", "high"),
    ("SC-TIM-001", "CLM-TIM-001", "The T/K pair is intentionally incomplete.", "intentional_incompleteness", "high"),
    ("SC-TIM-002", "CLM-TIM-001", "Solving the Time Wall as a full closure would destabilize the system.", "closure_hazard", "high"),
    ("SC-ISO-001", "CLM-ISO-001", "Topology must survive substitution across domains.", "topology_test", "critical"),
    ("SC-ISO-002", "CLM-ISO-001", "Boundary conditions and conservation laws are mandatory pass/fail tests.", "boundary_test", "critical"),
    ("SC-CON-001", "CLM-CON-001", "Independent Oxford-adjacent work converges on the same structural destination.", "independent_convergence", "medium"),
    ("SC-CON-002", "CLM-CON-001", "Theophysics reaches the same destination by equation-forced closure, not top-down selection.", "forced_vs_chosen", "high"),
    ("SC-EVD-001", "CLM-EVD-001", "PEAR and GCP align with predicted consciousness/coherence coupling.", "anomaly_fit", "medium"),
    ("SC-EVD-002", "CLM-EVD-001", "Empirical anomalies remain supportive rather than theorem-closing on their own.", "evidence_scope", "high"),
    ("SC-LAW-001", "CLM-LAW-001", "The Ten Laws distribute the canonical variable architecture into operator-level laws.", "operator_distribution", "high"),
    ("SC-LAW-002", "CLM-LAW-001", "Law pairings preserve the symmetry structure needed by the master equation.", "symmetry_distribution", "high"),
    ("SC-AI-001", "CLM-AI-001", "Alignment systems rely on externally imposed constitutions, reward models, or feedback signals.", "external_orientation", "high"),
    ("SC-AI-002", "CLM-AI-001", "Without a real external ground, capable systems drift toward performative alignment.", "pharisee_drift", "high"),
]


OBJECTIONS = [
    ("OBJ-ENT-001", "CLM-ENT-001", "Entropy is thermodynamic, not moral, so the mapping is just metaphor.", "category_error", "high"),
    ("OBJ-GRA-001", "CLM-GRA-001", "Grace is just psychological reframing or ordinary negentropy.", "reductionism", "high"),
    ("OBJ-OBS-001", "CLM-OBS-001", "Quantum measurement does not require consciousness, so faith-observation fails.", "decoherence_objection", "high"),
    ("OBJ-TOR-001", "CLM-OBS-002", "The terminal observer is an unnecessary metaphysical insertion.", "metaphysical_overreach", "high"),
    ("OBJ-COH-001", "CLM-COH-001", "Coherence conservation is asserted too broadly across scales.", "scale_jump", "medium"),
    ("OBJ-SYS-001", "CLM-SYS-001", "Open-system language is being smuggled in to rescue the model.", "ad_hoc_rescue", "medium"),
    ("OBJ-TIM-001", "CLM-TIM-001", "The Time Wall is a gap disguised as intentional mystery.", "gap_relabel", "high"),
    ("OBJ-ISO-001", "CLM-ISO-001", "Structural isomorphism collapses under unit mismatch and selective substitutions.", "swap_failure", "critical"),
    ("OBJ-CON-001", "CLM-CON-001", "Oxford convergence is post-hoc cherry-picking, not independent confirmation.", "selection_bias", "medium"),
    ("OBJ-EVD-001", "CLM-EVD-001", "PEAR/GCP-style effects are p-hacking or replication failures.", "replication_attack", "high"),
    ("OBJ-LAW-001", "CLM-LAW-001", "The Ten Laws are a presentation layer, not proof-bearing structure.", "presentation_only", "medium"),
    ("OBJ-AI-001", "CLM-AI-001", "Alignment engineering can solve the problem mechanically without any external metaphysical ground.", "engineering_sufficiency", "high"),
]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_subclaim_rows() -> list[dict[str, str]]:
    return [
        {
            "subclaim_id": sid,
            "claim_id": claim_id,
            "subclaim_text": text,
            "subclaim_type": subtype,
            "priority": priority,
            "created_at": DATE,
        }
        for sid, claim_id, text, subtype, priority in SUBCLAIMS
    ]


def build_objection_rows() -> list[dict[str, str]]:
    return [
        {
            "objection_id": oid,
            "claim_id": claim_id,
            "objection_text": text,
            "objection_type": otype,
            "severity": severity,
            "created_at": DATE,
        }
        for oid, claim_id, text, otype, severity in OBJECTIONS
    ]


def build_graph(claims: list[dict[str, str]], evidence: list[dict[str, str]], links: list[dict[str, str]]):
    nodes: list[dict[str, object]] = []
    edges: list[dict[str, object]] = []

    for claim in claims:
        nodes.append(
            {
                "node_id": claim["claim_id"],
                "node_type": "claim",
                "label": claim["claim_short"],
                "source_id": claim["claim_id"],
                "status": claim["canonical_status"],
                "domain": claim["domain"],
                "kind": claim["proof_class"],
                "summary": claim["claim_text"],
            }
        )

    for ev in evidence:
        nodes.append(
            {
                "node_id": ev["evidence_id"],
                "node_type": "evidence",
                "label": ev["title"],
                "source_id": ev["evidence_id"],
                "status": ev["status"],
                "domain": ev["canonical_role"],
                "kind": ev["anchor_kind"],
                "summary": ev["summary"],
            }
        )

    for sid, claim_id, text, subtype, priority in SUBCLAIMS:
        nodes.append(
            {
                "node_id": sid,
                "node_type": "subclaim",
                "label": text,
                "source_id": sid,
                "status": priority,
                "domain": claim_id,
                "kind": subtype,
                "summary": text,
            }
        )
        edges.append(
            {
                "edge_id": f"EDGE-DEC-{len(edges)+1:03d}",
                "source_id": claim_id,
                "target_id": sid,
                "edge_type": "decomposes_to",
                "weight": "1.00",
                "notes": "Canonical claim decomposes into operational subclaim.",
            }
        )

    for oid, claim_id, text, otype, severity in OBJECTIONS:
        nodes.append(
            {
                "node_id": oid,
                "node_type": "objection",
                "label": text,
                "source_id": oid,
                "status": severity,
                "domain": claim_id,
                "kind": otype,
                "summary": text,
            }
        )
        edges.append(
            {
                "edge_id": f"EDGE-OBJ-{len(edges)+1:03d}",
                "source_id": oid,
                "target_id": claim_id,
                "edge_type": "challenges",
                "weight": "0.70",
                "notes": "Known objection to be tracked in argument graph.",
            }
        )

    for link in links:
        edges.append(
            {
                "edge_id": f"EDGE-SUP-{len(edges)+1:03d}",
                "source_id": link["claim_id"],
                "target_id": link["evidence_id"],
                "edge_type": link["relation"],
                "weight": link["weight_0_1"],
                "notes": link["rationale"],
            }
        )

    return nodes, edges


def main() -> None:
    claims = load_csv(REGISTRY_DIR / "CANONICAL_CLAIMS_MASTER.csv")
    evidence = load_csv(REGISTRY_DIR / "CURATED_EVIDENCE_ANCHORS.csv")
    links = load_csv(LINKBOARD_DIR / "CLAIM_EVIDENCE_LINKS_CURATED.csv")

    subclaim_rows = build_subclaim_rows()
    objection_rows = build_objection_rows()
    nodes, edges = build_graph(claims, evidence, links)

    write_csv(
        REGISTRY_DIR / "CANONICAL_SUBCLAIMS_MASTER.csv",
        ["subclaim_id", "claim_id", "subclaim_text", "subclaim_type", "priority", "created_at"],
        subclaim_rows,
    )
    write_csv(
        REGISTRY_DIR / "CANONICAL_OBJECTIONS_MASTER.csv",
        ["objection_id", "claim_id", "objection_text", "objection_type", "severity", "created_at"],
        objection_rows,
    )
    write_csv(
        REPORTS_DIR / "canonical_graph_nodes.csv",
        ["node_id", "node_type", "label", "source_id", "status", "domain", "kind", "summary"],
        nodes,
    )
    write_csv(
        REPORTS_DIR / "canonical_graph_edges.csv",
        ["edge_id", "source_id", "target_id", "edge_type", "weight", "notes"],
        edges,
    )

    summary = {
        "generated_at": DATE,
        "claims": len(claims),
        "evidence_nodes": len(evidence),
        "subclaims": len(subclaim_rows),
        "objections": len(objection_rows),
        "graph_nodes": len(nodes),
        "graph_edges": len(edges),
    }
    (REPORTS_DIR / "canonical_graph_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
