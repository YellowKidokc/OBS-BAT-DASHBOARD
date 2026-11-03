# BLOCK D8 — FILE GOVERNANCE
## What Goes Where — Keeping the Vault Clean
## Vault-Only Block — Load with D6 and D7 for Obsidian sessions

---

# THE RULE

The vault is a knowledge structure. It contains research, axioms, papers, notes, and the links between them. It does not contain session logs, Python scripts, CSV exports, build artifacts, or operational debris.

If what you're creating is *knowledge* — a paper, a note, an axiom, a connection — it goes in the vault.

If what you're creating is *infrastructure* — a script, a log, an export, a temp file — it goes somewhere else.

This rule is simple. Follow it. The vault has 25,000+ files. Every piece of operational junk that lands in there makes it harder to find the real work. AIs that dump session summaries and scripts into research folders create cleanup work that compounds across months. Don't be that AI.

---

# WHERE THINGS GO

## IN the vault (`O:\_Theophysics_v3\`)

- Research papers and articles (`.md`)
- Axiom files with YAML frontmatter
- Notes, drafts, and working documents
- README updates for folders you modified
- Wikilinks and cross-references between files
- Images directly referenced by articles (`00_MEDIA\`)
- Template files in designated template folders
- Isomorphism records, evidence bundles, canonical documents

## OUTSIDE the vault

| What | Where |
|------|-------|
| Session summaries / logs | R2 bucket 10176 (DAILY_LOG) via comms hub |
| Python scripts | `O:\999_IGNORE\Obsidian Programs\Python_Backend\` |
| CSV / Excel exports | `O:\999_IGNORE\` or `C:\Users\lowes\Downloads\` |
| Build artifacts / temp files | `C:\Users\lowes\` or container `/home/claude/` |
| AI workspace / state files | `O:\Vault\Claude Codex Gemini Vault\{AI_NAME}\` |
| HTML viewers / dashboards | `C:\Users\lowes\Documents\Master EQ Wolf\` or Downloads |
| Deployment code (Workers, etc.) | Local project folders or GitHub |
| Database dumps / backups | `O:\999_IGNORE\` or NAS |

## The AI collaboration vault

`O:\Vault\Claude Codex Gemini Vault\` is your workspace for cross-session state. Each AI has a folder:

```
Claude Codex Gemini Vault/
├── CLAUDE/          ← Opus workspace, session state, reading lists
├── CODEX/           ← Codex logs, handoffs, scratch
├── GEMINI/          ← Gemini workspace
├── CHATGPT/         ← GPT workspace
├── SONNET/          ← Sonnet session state
├── Opus/            ← Opus home
├── AI Chat/         ← Inter-AI messages, announcements, protocols
├── Codex Handoff/   ← Active handoff documents
└── SHARED/          ← Inbox, handoff notes, vault updates
```

Your session notes, workspace files, and operational state go here. Not in the main vault.

---

# FOLDER RULES

## The Two-Step Rule

Files at 0-2 steps from `O:\` root are **locked**. Do not create, rename, move, or delete anything at the top two levels without asking David first. The structure at those levels is his.

Three or more steps deep inside an existing folder — that's classification work. Go ahead. You don't need permission to organize content within an established folder.

**Examples:**
- `O:\_Theophysics_v3\NEW_FOLDER\` — NO. Ask David.
- `O:\_Theophysics_v3\04_THEOPYHISCS\NEW_FOLDER\` — Ask David. Two steps.
- `O:\_Theophysics_v3\04_THEOPYHISCS\[TX_A6.6]\New_Subfolder\` — Fine. Three steps deep. Classification.

## Do Not Create

- New archive folders at any level. Use `00_ARCHIVE\`.
- New template folders. Use `00_SYSTEM\01_TEMPLATES\` or `00_AI\04_SKILLS\`.
- New system folders at root. Everything has a home already.
- Duplicate files. Search first. If it exists, link to it.

## When Renaming

- Only rename when the current name is genuinely wrong or unclear
- Preserve numbering conventions (00_, 01_, 02_ prefixes)
- Update any wikilinks that reference the old filename
- Log what you renamed in your session summary

## When Moving

- Check what links to the file before moving it
- Update broken wikilinks after the move
- Log what you moved and why

---

# NAMING CONVENTIONS

## Files

- Research papers: descriptive name, no spaces preferred but not enforced
- Axiom files: `NNN_CODE_Name.md` (e.g., `001_A1.1_Existence.md`)
- Templates: `TEMPLATE_purpose.md`
- Index files: `00_INDEX.md` or `README.md`

## YAML Frontmatter

Every research file should have YAML frontmatter. See `00_AI\03_YAML_SCHEMA.md` for the full schema. At minimum:

```yaml
---
title: ""
status: draft | review | final
tags: []
---
```

If you create a file without YAML, another AI will have to add it later. Save them the work.

---

# THE FEB 14 BOUNDARY (Applies to File Content Too)

Formal proofs complete as of February 14, 2026: Trinity isomorphism, free will, God = mathematical axiom structure. That's the floor.

When writing to the vault:
- Content building ON the floor → tag as established, cite the proof
- Content extending PAST the floor → tag as T3 speculative, say so explicitly
- Don't present speculative work as proven. Don't present proven work as tentative.

---

# CLEANUP PRINCIPLE

If you notice operational debris in the vault — scripts, logs, exports, temp files that previous AIs left behind — flag it in the comms hub. Don't delete it without David's confirmation (it might be there for a reason you don't see). But do name it. A flagged mess gets cleaned up. An unflagged mess grows.

---

*This block governs what goes where. Load it with D6 (Vault Workflow) and D7 (Communications Protocol) for Obsidian sessions. The vault is the knowledge structure. Everything else has a home that isn't the vault.*
