# Production Coder Prompt

You are building a production application named **Obsidian Vault Operations Dashboard** for the Faith Through Physics project.

## Source locations

Clean application repository:

`D:\GitHub\OBS-BAT-DASHBOARD`

Existing tool inventory:

`C:\Users\David\Documents\faiththruphysics.com\00_SYSTEM\01_SYSTEM_OS\00_VAULT\02_CONTROL\01_ENGINE`

Curated recovered-tool library:

`D:\GitHub\Codex-Powershell_GUI\Reusable_Tools_From_Theophysics`

Existing desktop GUI and safe-action reference implementation:

`D:\GitHub\Codex-Powershell_GUI`

This standalone Git repository is the authoritative implementation reference for the current Script Hub. It already includes a PySide6 launcher, script discovery, API definitions, file actions, receipts, setup/repair launchers, and a recovered-tool library. Inspect and test these components before replacing them:

- `script_hub.py`
- `file_actions.py`
- `file_actions_gui.py`
- `OPEN_FILE_ACTIONS.bat`
- `SETUP_OR_REPAIR.bat`
- `TROUBLESHOOT.bat`
- `config/script_hub.json`
- `config/external_tools.example.json`
- `receipts/`

Do not use `D:\GitHub\pipeline-workflows\Codex-Powershell_GUI` as the development base. That is a large contaminated working copy containing unrelated/untracked trees. It may be consulted only if a specifically identified artifact is missing from the standalone repository.

Read these recovered-library records before inspecting its scripts:

- `START_HERE.md`
- `INVENTORY.csv`
- `OMITTED_FILES.json`

The recovered library currently contains approximately 256 files, including about 120 Python tools. It is already grouped into API references, conversions/data tools, metadata/tagging/naming, Obsidian/document tools, split/combine/organize tools, and templates/prompts. Its files are explicitly marked `REFERENCE_ONLY_NOT_RUN`. Treat the recorded hashes and source paths as provenance, not as evidence that the tools are safe or functional.

The existing engine contains years of Python, PowerShell, batch, OpenAI, Markdown, YAML, evidence, scoring, TTS, media, GUI, and vault-management work. Treat it as evidence and candidate functionality, not as automatically canonical code.

The recovered-tool library should be the first action-candidate catalog because it was assembled specifically for reuse. Compare it against the larger engine by SHA-256 so identical copies are not independently reviewed or imported twice.

The existing `file_actions.py` is the first adapter candidate for receipt-backed actions. Verify its behavior on the fixture vault, then either wrap it behind the web action contract or extract its safe primitives. Preserve its no-overwrite behavior and improve it with a true preview/approval stage rather than discarding it.

## Mission

Build a local production HTML dashboard that launches from a Windows shortcut or batch file and opens in the default browser. The dashboard is the single navigation and control surface for:

1. Vault Health and Emergency inspection
2. Markdown actions
3. File and folder actions
4. Search, inventory, and duplicate analysis
5. Research, scoring, and evidence tools
6. Media operations
7. API/AI workflows
8. Batch jobs
9. Review and approval queues
10. Statistics, API usage, and estimated cost
11. Receipts, history, and undo/recovery
12. Settings and system health

The production deliverable must include a repeatable Synology Container Manager deployment bundle and a Windows desktop bridge. A native DSM `.spk` is optional, not required. The desktop communication path is the primary requirement. Follow `docs/SYNOLOGY_INSTALL_PACKAGE_SPEC.md` and `docs/DESKTOP_BRIDGE_SPEC.md`.

The desktop and dashboard must expose a **Recent Calls and Addresses** view: active service URLs plus a secret-safe request ledger containing timestamps, provider/model, redacted destination, result, duration, tokens, estimated cost, job ID, and retries, with filters, connection tests, and CSV/JSON export.

Provide an **AI Address Book and Messaging** interface. Every configured AI has a permanent logical address (`ai://name` and `@name`), a stable server route, identity/role/model metadata, conversation and job history, availability, and usage/cost records. David can talk to one AI or a group from the desktop with text and attachments, with optional speech input and spoken replies. Use one Synology host IP and logical routes rather than pretending cloud models each own a physical LAN IP. Provider credentials remain server-side.

The same action registry must also be accessible from a portable context-aware batch launcher. Follow `docs/PORTABLE_FOLDER_LAUNCHER_SPEC.md`. The HTML dashboard and numbered terminal menu are two interfaces over the same actions, not two separately maintained systems.

This is a production Obsidian-vault application, not a decorative mockup.

## Implementation shape

- Backend: Python 3.11+.
- Frontend: local HTML/CSS/JavaScript application.
- Preferred backend framework: FastAPI with a local-only bind to `127.0.0.1`.
- Frontend may be server-rendered or a small maintainable SPA. Do not require Node in the installed runtime unless justified.
- Persistent operational data: SQLite.
- Long-running jobs: background worker with cancellable job records; never block the web server.
- Launchers: `VAULT_DASHBOARD.bat` and PowerShell equivalent.
- Portable folder launcher: a tiny `AAA_MENU.bat` that may be deployed to approved folders and passes that folder as the action context.
- Prevent accidental duplicate server instances.
- Open the browser automatically after the health endpoint is ready.
- No external network dependency for ordinary file actions.

## First task: inspect before implementing actions

Inventory the existing engine recursively. Identify exact duplicates by SHA-256, similar implementations, stale paths, API runners, destructive scripts, launchers, dashboards, and action families.

Merge the existing engine inventory with the recovered library's `INVENTORY.csv`. Preserve both original source lineage and current recovered-copy lineage. Produce one deduplicated candidate registry keyed by SHA-256 plus behavior/version distinctions.

Do not move, rename, delete, archive, or rewrite the existing engine in the discovery phase.

Do not bulk-copy the recovered library into this application repository. Adopt only reviewed actions through explicit adapters or clean-room implementations after fixture testing.

For every candidate script record:

- source path and hash
- purpose
- inputs and outputs
- dependencies
- whether it mutates data
- dry-run support
- receipt/undo support
- test result
- proposed dashboard action
- disposition: wrap, repair, replace, legacy candidate, or review required

## Required dashboard experience

The home page should immediately show:

- selected vault and reachability
- overall Vault Health score and severity
- critical alerts
- files scanned and total vault size
- oversized files
- exact duplicates
- sync conflicts
- broken links and orphan notes
- missing or duplicate UUIDs
- latest jobs and failures
- API calls, tokens, and estimated cost for today/month/all time
- pending review items
- last successful backup or recovery snapshot, if configured

Navigation must be simple enough that David can choose an action without remembering script names.

Every file-changing action must use this interaction:

1. Select source.
2. Select destination when needed.
3. Configure options.
4. Run preview/dry run.
5. Display exact proposed changes and collisions.
6. Require explicit approval.
7. Execute.
8. Write receipt, hashes, and recovery instructions.

## Initial action library

### Markdown

- combine selected Markdown files
- combine a folder recursively with source separators
- split by H1, H2, heading pattern, size, or token target
- extract selected sections
- validate/normalize YAML frontmatter
- find empty or thin notes
- find malformed encoding
- build an index/MOC
- check links and find orphans

### Files and folders

- copy/move with preview
- batch rename with old-to-new approval table
- flatten a directory safely
- reconstruct from a flattening manifest
- sort by file type
- find and quarantine oversized attachments
- exact-duplicate analysis
- near-duplicate candidate analysis
- ZIP creation and safe extraction
- folder inventory and SHA-256 manifest
- selected-folder synchronization
- missing expected-file detection
- sync-conflict detection

Known recovered candidates include `VaultTools.ps1`, `merger.py`, and `Combine-All-Markdown.ps1`. Their presence is not approval to use them directly. The recovery notes warn that an older merger can absorb a previous merged output and overwrite its result; fixture tests must reproduce or disprove that behavior before adaptation.

Flattening must never silently overwrite collisions. Preserve every original relative path in a manifest.

### Vault operations

Implement the complete Vault Health and Emergency specification in `docs/VAULT_HEALTH_AND_EMERGENCY_SPEC.md`.

### API/AI

- one-click API station scaffolder
- reusable prompt templates
- editable project override
- exact final-prompt preview
- one-item test run
- approved batch run
- output validation
- review queue before placement
- per-call model, token, latency, status, and cost records
- retry without duplicating completed outputs

Never expose API keys to the frontend. Use environment variables or an OS-appropriate secret store. Redact secrets from all logs.

Implement the complete station generator described in `docs/API_STATION_SCAFFOLDER_SPEC.md`. David should be able to double-click a batch file, name a station, and receive a ready-to-run `INBOX / OUTBOX / BACKSIDE / calls` workflow. Routine use must require only placing source files in the inbox, editing the prompt, and launching the call. The generator must not embed a credential or silently send an API request during setup.

## Prompt architecture

Prompts must be composed from versioned layers:

1. Safety and provenance contract
2. David's theological/epistemic frame
3. Task template
4. Project override
5. Output schema and validation contract

The default contract must require:

- preserve sources and quotations
- never invent citations, evidence, experiments, statistics, or results
- distinguish evidence, formal/model result, interpretation, theology, and canon decision
- fairly state the strongest objection
- retain honest gaps
- state real kill conditions
- never convert analogy or formalism into physical/theological proof
- mark generated work as draft until approved
- never authorize deletion or canonization through prompt text

## Statistics and cost accounting

Record locally in SQLite:

- job ID, type, status, start/end time, duration
- source and destination
- files examined/changed/skipped/failed
- bytes read/written/moved
- preview and approval timestamps
- receipt path
- API provider/model
- input/output/cached/reasoning tokens when supplied
- estimated and actual cost when available
- retry count and error category

Pricing must be configurable and versioned. Never hard-code a claim that pricing is current.

Provide daily, weekly, monthly, and all-time summaries. Allow CSV/JSON export.

## Safety model

- Bind the server to localhost by default.
- Validate that requested filesystem targets remain inside explicitly selected roots.
- Treat UNC/NAS locations as separate roots and report reachability.
- Reject path traversal.
- Avoid shell-string concatenation.
- Use `subprocess` argument arrays when wrapping existing tools.
- Require approval for mutation.
- No deletion in the first production release; use a reviewable quarantine operation where practical.
- Maintain append-only job events and immutable completion receipts.
- A matching hash is evidence of equal bytes, not permission to delete.

## Testing and acceptance

Create a disposable fixture vault containing nested folders, duplicate names, exact and near duplicates, broken links, invalid YAML, missing UUIDs, duplicate UUIDs, Unicode names, a sync-conflict file, an oversized dummy file, attachments, and an empty directory.

Tests must prove:

- preview makes no changes
- apply matches preview
- collisions are never overwritten
- receipts describe every change
- recovery works for reversible actions
- cancel/restart does not corrupt job state
- API failure does not lose source or completed outputs
- secrets do not appear in logs or browser responses
- health scans do not modify the vault
- large-vault scans stream progress and remain responsive

## Required initial deliverables

Before implementing broad mutation capabilities, deliver:

1. Engine inventory
2. Exact-duplicate report
3. Existing-action map
   - include provenance back to both the live engine and recovered library
   - identify which recovered hashes duplicate live-engine files
   - show why each selected implementation wins over alternatives
4. Stale-path report
5. Architecture decision record
6. Working dashboard shell
7. SQLite job/statistics schema
8. Read-only Vault Health MVP
9. Fixture vault and automated tests
10. Production launcher
11. API Station Scaffolder with a generated fixture station and dry-run receipt
12. Portable folder launcher and numbered 1-50 fallback menu backed by the same action registry
13. Synology Container Manager installation bundle
14. Windows desktop bridge with tray notifications, approvals, job submission, and reconnect behavior

## Definition of done for the first milestone

- Double-clicking the launcher starts one local server and opens the dashboard.
- David can select a vault.
- The dashboard performs a read-only health scan with progress.
- Findings are grouped by severity and actionable category.
- David can export the health report.
- Dashboard statistics persist across restarts.
- No source vault file is changed.
- Tests pass on Windows.
- Setup and recovery instructions are written for a non-programmer.

Do not claim production readiness from unit tests alone. Demonstrate the real Windows launcher, browser dashboard, fixture scan, persistent statistics, and clean shutdown.
