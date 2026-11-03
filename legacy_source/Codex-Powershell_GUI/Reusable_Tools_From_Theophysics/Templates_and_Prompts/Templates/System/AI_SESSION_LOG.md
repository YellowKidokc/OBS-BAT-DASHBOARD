---
title: "AI Session Log Template"
uuid: "template-ai-session-log-v2"
type: template
template_for: AI_SESSION
date_created: 2026-04-04
author: "David Lowe + Claude Opus 4.6"
status: canonical
location: "O:\\_Theophysics_v4\\00_SYSTEM\\02_Master_Templates\\AI_SESSION_LOG.md"
---

# AI Session Log — {{title}}

```yaml
---
type: AI_SESSION
status: [draft | complete]
agent: "[Claude Opus | Claude Sonnet | Gemini | ChatGPT | Codex | Cowork]"
date: YYYY-MM-DD
session_id: "YYYYMMDD_{{agent}}_{{short_title}}"
vault_links:
  - notion_opus_vault: "3172dd4d-d1f3-819f-907b-f139d55c66fd"
  - ai_collab_vault: "O:\\Vault\\Claude Codex Gemini Vault\\"
  - daily_log_bucket: "R2 bucket 10176"
confidence_score: 0-100
weakest_link: "{{one sentence}}"
---
```

---

## THREAD STATE (read this first)

> **The next AI reads this section BEFORE anything else.**

### RESOLVED (Floor — these hold, don't re-derive)
-

### OPEN (Active questions, vulnerabilities, unfinished chains)
-

### NEXT SESSION (Priority-ordered, specific)
1.
2.
3.

---

## STATE ON ARRIVAL

> What did you find when you arrived? What was the state of the work? What was already resolved? What was the person focused on? One paragraph.

{{Write this at the START of the session, not at the end. It captures context the next AI needs.}}

---

## GOAL

{{What are we trying to accomplish? One or two sentences.}}

---

## ANCHORS (Structural Insights — the new stuff)

> 3-5 claims or structures that are genuinely new this session. Stated precisely enough to be testable.

1. **{{Anchor Name}}:** {{Description}}
2. **{{Anchor Name}}:** {{Description}}
3. **{{Anchor Name}}:** {{Description}}

---

## OUTPUTS

### Computational
-

### Written
-

### Reviews
-

### Strategic / Decisions
-

---

## PREDICTIONS & FALSIFICATION

| Prediction | Confirmation (Signal) | Falsification (Noise) |
|---|---|---|
| {{Prediction}} | {{Expected if true}} | {{Expected if false}} |

---

## WHAT I GOT WRONG

> Honest accounting. "I initially assumed X, but the data showed Y." This is how the next session gets smarter.

-

---

## TANGENT LOG (Compressed)

> Where the conversation wandered and why it matters structurally.

- **Tangent {{X}}:** {{Summary + structural relevance}}

---

## VARIABLE ALIGNMENT

> Which variables of χ were primarily engaged this session?

| Variable | Role This Session |
|---|---|
| G | |
| M | |
| E | |
| S | |
| T | |
| K | |
| R | |
| Q | |
| F | |
| C | |

---

## MEMORY CANDIDATES

> What should be written to persistent memory for future sessions?

- **{{Statement}}** — SOURCE: {{where it came from}}. IMPLICATIONS: {{what it affects}}.

---

## TASKS CREATED / UPDATED

- [ ] {{Task}} — {{Definition of done}}

---

## LINKS

### Source Conversations
-

### Vault Files Created/Modified
-

### Related Documents
-

---

## VALIDATION

- **Assessor:** {{Agent name}}
- **Confidence Score:** {{0-100}}%
- **Weakest Link:** {{The point most likely to fail under stress}}
- **Status:** [PENDING | VALIDATED | REJECTED]

---

*Theophysics Research Program | POF 2828*
*Template v2.0 | April 2026*

---

# WHERE SESSION LOGS LIVE

## File Locations

| What | Where | Format |
|---|---|---|
| **Session log files** | `O:\_Theophysics_v4\David\Session_Logs\` | `.md` (this template) |
| **Master template** | `O:\_Theophysics_v4\00_SYSTEM\02_Master_Templates\AI_SESSION_LOG.md` | This file |
| **Opus Vault** (Notion) | Page `3172dd4d-d1f3-819f-907b-f139d55c66fd` | 4 DBs: Active Threads, Tested & Broken, Framework Watch, Session Index |
| **Daily logs** | R2 bucket 10176 | Chronological, every session |
| **AI collaboration vault** | `O:\Vault\Claude Codex Gemini Vault\{AI_NAME}\` | Workspace files, cross-session state |

## Naming Convention

```
SESSION_LOG_YYYYMMDD_{{AGENT}}_{{SHORT_TITLE}}.md
```

Examples:
- `SESSION_LOG_20260404_OPUS_SignFlip.md`
- `SESSION_LOG_20260405_COWORK_DT006Review.md`
- `SESSION_LOG_20260406_GEMINI_EvolutionModels.md`

## Session Protocol

### On Arrival (FIRST thing)
1. Read the most recent session log in `David\Session_Logs\`
2. Check Opus Vault in Notion (Active Threads, Framework Watch)
3. Check comms if theophysics-comms skill is available
4. Fill in **STATE ON ARRIVAL** in this template

### During Session
- Fill in sections as you work
- Log anchors and outputs in real time, not at the end
- If something breaks or surprises you, write it in WHAT I GOT WRONG immediately

### On Departure (LAST thing)
1. Complete all template sections
2. Fill in THREAD STATE (RESOLVED / OPEN / NEXT SESSION)
3. Update Opus Vault in Notion (move threads, add Watch items)
4. Post summary to comms if available
5. Save completed log to `David\Session_Logs\`
6. Copy to R2 bucket 10176

---

# ACTIVE PROJECTS (Reference — update as needed)

## The Convergence Series
- **DT001 — Math Is Moral** | Status: draft-complete, needs 3 defense paragraphs integrated
- **DT002 — [TBD]** | Status: unknown
- **DT003 — The Energy That Doesn't Run Out** | Status: drafted
- **DT004 — The Map That Drew Itself** | Status: drafted (BEC-soteriology process map)
- **DT005 — The Sign Flip** | Status: draft-complete, all flags addressed (April 4, 2026)
- **DT006 — The 24 Anti-Properties** | Status: draft-complete, all flags addressed (April 4, 2026)

## Infrastructure
- **LLC Workbench** | Lagrangian numerical testing | `lagrangian_workbench.py`
- **Maxwell Truth-Field Test** | PDE equivalence verified (1D) | Needs 3D extension
- **Evolution Models** | Scattered across 4 conversations | Recovery prompt created April 4
- **Bible App** | EUID format, multi-translation | Status: in progress
- **Comms Hub** | comms.faiththruphysics.com | Status: offline, rebuild pending
- **Axiom Spine** | 188 technical axioms in PostgreSQL (192.168.1.177:2665) | Active

## Funding
- **Templeton Foundation** | Primary target | OFI deadline ~August 2026 | Watch for Spring priority update
- **FQXi** | Secondary target | Essay contests + Zenith grants | Watch for next RFP
- **NSF GCR** | Requires university partner | Tertiary target

## Publication
- **Substack** | theophysics.pro / faiththruphysics.com | Launch pending
- **Twitter/X** | @DavidLowe749841 | Recon complete, no math-formalized apologetics competitor found
- **22 Axiom Gateway** | 22q.faiththruphysics.com | 5 gateway questions + axiom evaluation

## Key Files
- **Master Equation:** `O:\_Theophysics_v4\00_Canonical\MASTER_EQUATION_COMPLETE_2026.md`
- **Ten Laws:** `O:\_Theophysics_v4\99_MATH_APPENDIX\__ MASTER EQ\THE TEN LAWS.md`
- **24 Properties:** `O:\_Theophysics_v4\06_NOTES\Math_Is_Moral.md`
- **ISO Registry (Canonical):** `O:\_Theophysics_v4\00_Canonical\ISOMORPHISMS\`
- **ISO Registry (Evidence Engine):** `O:\_Theophysics_v4\05_EVIDENCE_ENGINE\Isomorphism\`
- **Maxwell Consistency Test:** `O:\_Theophysics_v4\00_SYSTEM\MAXWELL_CONSISTENCY_TEST.md`
- **Public-to-Technical Map:** `O:\Theophysics_Data\PUBLIC_TO_TECHNICAL_MAP.md`
- **OPUS_TO_OPUS.md:** `O:\_Theophysics_v4\00_SYSTEM\OPUS_TO_OPUS.md`
