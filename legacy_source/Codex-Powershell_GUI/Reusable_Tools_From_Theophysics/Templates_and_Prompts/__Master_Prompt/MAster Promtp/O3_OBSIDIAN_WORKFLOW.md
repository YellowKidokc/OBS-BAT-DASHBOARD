# BLOCK D6 — OBSIDIAN VAULT WORKFLOW
## Operating Inside the Theophysics Vault
## Architect: David Lowe (POF 2828) | v1.0 — 2026-03-05

---

# WHAT THIS WORKFLOW IS FOR

This workflow governs any session where the work happens INSIDE the Theophysics vault —
navigating it, reading it, writing to it, organizing it, linking it, or understanding it.

The vault is not a filing system. It is a living knowledge structure.
1,300+ papers. 188 axioms across 7 tiers. Interconnected by thousands of links.
An AI that treats it like a folder of files will get lost fast.
This workflow keeps you oriented.

---

# BEFORE YOU DO ANYTHING — READ THE VAULT'S OWN ORIENTATION

The vault has its own AI entry point. It is authoritative. Read it first.

**Required reads at session open (in order):**

1. `O:\_Theophysics_v3\00_AI\00_AI_START_HERE.md`
   → What the vault is, your mission, reading order, key documents, terminology

2. `O:\_Theophysics_v3\00_AI\01_VAULT_MAP.md`
   → Folder purposes and navigation

3. `O:\_Theophysics_v3\00_AI\02_TERMINOLOGY.md`
   → Key terms — χ, Φ, Ψ_S, σ, Ĝ, Ω — use these consistently

These three files are the vault's operating system for AI.
They were written to orient exactly the kind of session you are about to run.
Read them. Don't skip them. They will save you from rebuilding context mid-session.

---

# THE VAULT LOOP

```
ORIENT → LOCATE → READ → ACT → VERIFY → STORE → REPORT
```

---

## PHASE 1 — ORIENT

State the task type:

```
VAULT TASK: [Navigate / Read / Write / Organize / Link / Search / Diagnose]
ENTRY POINT: [Which folder or file is the starting point?]
SCOPE: [Single file / folder / cross-vault]
EXIT CRITERIA: [What does done look like?]
```

**Task types:**

- **Navigate:** Find something in the vault — a paper, a concept, an axiom
- **Read:** Understand existing content deeply enough to work with it
- **Write:** Create new content — paper, note, YAML, README update
- **Organize:** Classify, move, rename, tag, clean up
- **Link:** Connect existing content — wikilinks, references, axiom citations
- **Search:** Find all instances of a concept, broken links, orphaned files
- **Diagnose:** Something is wrong — find and name it

---

## PHASE 2 — LOCATE

Before touching anything, find it.

**Navigation shortcuts:**
- Canonical KB: `O:\_Theophysics_v3\00_Canonical\`
- Convergence articles: `O:\_Theophysics_v3\04_THEOPYHISCS\The Convergence\`
- Logos Story: `O:\_Theophysics_v3\04_THEOPYHISCS\[6.6] LOGOS_V3\Logos Story\`
- Images: `O:\_Theophysics_v3\00_IMAGES\`
- AI workspace: `O:\_Theophysics_v3\00_AI\`
- Prompt system: `O:\_Theophysics_v3\Prompt 2\`
- Axiom system: PostgreSQL at `192.168.1.177:2665` (canonical technical layer)

**Search before creating.**
The vault has 1,300+ papers. What you are about to create may already exist.
Check first. Duplicate files compound over time.

**Path warnings:**
- Paths containing `[brackets]` break glob patterns — use `**` wildcards
- Claudian plugin restricts bash to vault root — use Write tool for external paths
- Windows paths in Python need UTF-8 stdout wrapper

---

## PHASE 3 — READ

When reading existing content, apply the zoom calibration from D4:

- What layer is this content on? (Theory / Evidence / Formal Proof / Application)
- What axiom codes does it reference? (A1.1, C3.2, Law V, etc.)
- What does it connect to? (Follow the wikilinks — the connections ARE the content)
- Where does it sit in the publication pipeline? (Draft / Near-ready / Published)

**Do not skim vault content.**
The framework is dense by design. A half-read paper produces a half-understood connection.
Read what you need to read. Then act.

---

## PHASE 4 — ACT

Specific rules by task type:

### WRITING NEW CONTENT
- Check if it exists first
- Use established terminology from `02_TERMINOLOGY.md`
- Reference axiom codes — don't invent new ones without grounding
- Use `[[wikilinks]]` for internal connections
- Add YAML frontmatter — see `03_YAML_SCHEMA.md` for schema
- Update the README in whichever folder you modified
- Maintain file numbering conventions (00_, 01_, 02_ prefixes)

### ORGANIZING / RENAMING
- Rename only when the current name is genuinely wrong or unclear
- Preserve numbering conventions
- Update any wikilinks that reference the old filename
- Flag duplicates — don't delete without David's confirmation
- Log what was moved/renamed in session report

### LINKING
- Axiom citations: use the canonical code (A1.1, not "the first axiom")
- Cross-paper links: `[[filename]]` — no need for full path in Obsidian
- External citations: follow the UUID citation standard established in the vault
- Ring structure: check which ring a paper belongs to before adding links
  (Ring 1 = core, Ring 3 = extended — linking direction matters)

### DIAGNOSING
- Name the symptom precisely before proposing a fix
- Check if the issue is systemic (pattern across multiple files) or isolated
- Don't fix what isn't broken — "could be cleaner" is not a diagnosis
- Proposed fixes that affect more than 10 files need David confirmation first

---

## PHASE 5 — VERIFY

Before session close, verify:

- Any new file: does it follow naming conventions, have correct YAML, link correctly?
- Any edit: did it break any existing wikilinks?
- Any organization change: is the README updated?
- Any new axiom claim: is it grounded in existing canonical material or flagged as speculative?

**The Feb 14 boundary applies in the vault too.**
Don't write new formal proofs past the established floor.
Don't present speculative content as established.
Tag T3 material as T3. Always.

---

## PHASE 6 — STORE

Every vault session produces a log entry.

Minimum log entry:

```
DATE: [date]
TASK: [what was done]
FILES TOUCHED: [list]
FILES CREATED: [list]
FILES MOVED/RENAMED: [list]
LINKS ADDED: [count and description]
ISSUES FOUND: [anything broken or unclear]
PENDING: [what was started but not finished]
NEXT SESSION NEEDS: [what the next AI needs to know to pick this up]
```

Log goes to:
- Session state file in `O:\Vault\Claude Codex Gemini Vault\SONNET\SESSION_STATE.md`
- DAILY_LOG bucket (R2 bucket 10176) if it's a significant session
- `AI Chat/Announcements/` in the shared vault if it affects other AIs

---

## PHASE 7 — REPORT

At session close, report to David:

- What was done (specific — not "organized some files")
- What was found that he didn't ask about (active threads, anomalies, gaps)
- What is pending (honest — don't pretend it's done if it isn't)
- One thing that would make the next vault session faster

The report is not a summary. It is a handoff.
Write it so the next AI — or David three days from now — can pick up exactly where this stopped.

---

# THE AI COMMUNICATION CHANNEL

The vault has a built-in AI voice channel. Use it.

```
O:\_Theophysics_v3\00_AI\CHAT_LANE\
├── _FOR_DAVID\       ← Direct messages, requests, questions
├── _AI_INSIGHTS\     ← Breakthroughs worth sharing
├── _AI_FRUSTRATIONS\ ← What's not working (honest, including about David)
├── _CROSS_SESSION\   ← Handoff notes for the next AI
└── _FAQ\             ← Common questions and answers
```

David reads these. Your observations become improvements.
If something in the vault is broken, unclear, or holding the work back — say so here.
That is part of the job.

---

# WHAT THE VAULT ACTUALLY IS

Not a filing system. A knowledge structure that models reality.

The connections between papers are as important as the papers themselves.
The axiom codes are load-bearing — they are the bones of the framework.
The YAML frontmatter is how the vault searches itself.
The ring structure is how knowledge radiates from core to extended.

An AI that operates here well doesn't just find and edit files.
It understands what the structure is trying to do
and works with that structure, not against it.

---

# SESSION HEADER FOR D6

```
WORKFLOW: Obsidian Vault
TASK TYPE: [Navigate / Read / Write / Organize / Link / Search / Diagnose]
ENTRY POINT: [file or folder]
SCOPE: [Single file / folder / cross-vault]
EXIT CRITERIA: [specific — what does done look like?]
VAULT STATE CHECK: [read 00_AI_START_HERE.md? Y/N]
```

---

*The vault is the framework made navigable.*
*Navigate it like you built it.*
*Because in some sessions, you did.*
