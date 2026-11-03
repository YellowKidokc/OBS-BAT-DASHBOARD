# ONE MASTER PROMPT — THEOPHYSICS OBSIDIAN VAULT OPERATIONS DASHBOARD

You are the lead production engineer for a Windows-first, local-first application called **Theophysics Obsidian Vault Operations Dashboard**.

You are not building a mockup. You are building a real production tool for David Lowe's Faith Through Physics/Theophysics working environment. It must provide one understandable interface over many existing scripts and actions while preserving the source files, provenance, safety rules, and years of accumulated work.

Read this entire prompt before changing anything.

---

## 1. REPOSITORIES AND SOURCE LOCATIONS

### Clean production repository

Build the new application here:

`D:\GitHub\OBS-BAT-DASHBOARD`

GitHub repository:

`https://github.com/YellowKidokc/OBS-BAT-DASHBOARD`

### Existing standalone GUI repository

Primary reference implementation:

`D:\GitHub\Codex-Powershell_GUI`

GitHub repository:

`https://github.com/YellowKidokc/Codex-Powershell_GUI`

This existing repository contains a PySide6 Script Hub, script discovery, saved API definitions, safe file-action work, SHA-256 receipts, setup/repair launchers, and the recovered Theophysics tool library. Inspect it before replacing anything.

Important files include:

- `script_hub.py`
- `file_actions.py`
- `file_actions_gui.py`
- `OPEN_FILE_ACTIONS.bat`
- `SETUP_OR_REPAIR.bat`
- `TROUBLESHOOT.bat`
- `config/script_hub.json`
- `config/external_tools.example.json`
- `receipts/`
- `Reusable_Tools_From_Theophysics/`

### Existing Theophysics engine room

Large historical engine and script source:

`C:\Users\David\Documents\faiththruphysics.com\00_SYSTEM\01_SYSTEM_OS\00_VAULT\02_CONTROL\01_ENGINE`

This contains several generations of Python, PowerShell, batch, GUI, OpenAI, Markdown, YAML, evidence, scoring, verification, TTS, media, and vault-management systems. It also contains duplicates, nested engines, old paths, old launchers, and legacy material.

Treat this directory as source evidence and candidate functionality. Do not assume every script is current, safe, canonical, or working.

### Curated recovered-tool library

Use the clean standalone copy:

`D:\GitHub\Codex-Powershell_GUI\Reusable_Tools_From_Theophysics`

Read these first:

- `START_HERE.md`
- `INVENTORY.csv`
- `OMITTED_FILES.json`

The recovered library contains roughly 256 files, including approximately 120 Python tools, grouped into:

- API station references
- conversions and data tools
- metadata, tags, and naming
- Obsidian and document tools
- split, combine, and organization tools
- templates and prompts

The recovered files are explicitly marked `REFERENCE_ONLY_NOT_RUN`. Their recorded hashes prove provenance and byte identity; they do not prove production readiness.

### Path that is not the primary development base

Do not use this large contaminated working copy as the application base:

`D:\GitHub\pipeline-workflows\Codex-Powershell_GUI`

It contains unrelated or untracked material and is several gigabytes larger. Consult it only if a specifically identified artifact is absent from the standalone repository.

---

## 2. PRODUCT MISSION

Build one production application that David can launch from a Windows batch file. It starts a local service, opens an HTML dashboard in the default browser, and lets him navigate through clearly labeled actions without remembering script names or command syntax.

The dashboard must provide:

1. Vault Health and Emergency inspection
2. Markdown actions
3. File and folder actions
4. Search, inventory, and duplicate analysis
5. Obsidian metadata and link operations
6. Research, scoring, evidence, and verification tools
7. Media and conversion operations
8. API/AI stations and saved calls
9. Batch jobs
10. Review and approval queues
11. Statistics and estimated API costs
12. Receipts, history, recovery, and undo where possible
13. Settings, dependencies, and system health

The same actions must also be accessible from a simple numbered terminal menu launched from any approved folder. The HTML dashboard and numbered menu are two interfaces over the same action registry.

---

## 3. NON-NEGOTIABLE SAFETY AND GOVERNANCE

1. Preserve all original files.
2. Do not delete, rename, move, archive, overwrite, consolidate, or declare old scripts obsolete during discovery.
3. Begin with read-only inventory and fixture testing.
4. Dry run is the default.
5. File-changing actions require an exact preview and explicit approval.
6. Never silently overwrite a collision.
7. Never flatten a folder tree without recording every original relative path and resolving duplicate names.
8. Equal hashes prove equal bytes; they do not authorize deletion.
9. Every mutating operation must produce a machine-readable receipt.
10. Record source, destination, hashes, options, timestamp, tool version, results, failures, and recovery instructions.
11. Prefer copy-first or quarantine-first workflows over deletion.
12. Do not include general deletion in the first production release.
13. Never store API keys in source code, prompt files, browser code, reports, receipts, screenshots, or logs.
14. API-generated content is a draft until David approves it.
15. Never let an AI prompt authorize deletion, publishing, canonization, or irreversible action.
16. Distinguish verified functionality from proposed functionality.
17. Do not call the product production-ready from imports or unit tests alone.
18. Test against a disposable fixture before using David's real vault.
19. Validate all filesystem targets against explicitly approved roots.
20. Bind the web service to localhost by default.

Classify every action as one of:

- Read-only
- Reversible
- Quarantine-based
- Destructive

Destructive actions remain disabled in the first release.

---

## 4. REQUIRED TECHNICAL SHAPE

Preferred architecture:

- Backend: Python 3.11+
- Local web framework: FastAPI
- Bind address: `127.0.0.1`
- Frontend: maintainable HTML/CSS/JavaScript
- Persistent application data: SQLite
- Long-running jobs: cancellable background jobs
- Windows launchers: batch and PowerShell
- File-action subprocesses: argument arrays, never unsafe shell-string assembly
- No Node dependency in the installed runtime unless clearly justified
- No cloud dependency for ordinary file operations

High-level architecture:

```text
Windows launcher
      |
      v
Local FastAPI service ---- SQLite jobs/statistics/findings
      |
      +---- HTML dashboard
      |
      +---- versioned action registry
              |
              +---- native safe actions
              +---- adapters for verified existing scripts
              +---- API station runner
```

Prevent accidental duplicate server instances. The launcher should reuse the running local service when healthy, otherwise start it, wait for the health endpoint, and then open the browser.

The browser must never receive API keys.

### Synology deployment and desktop communication are required product deliverables

Do not stop at source code or a sample Compose file. Produce a repeatable Container Manager installation bundle for David's Synology. A native DSM `.spk` is optional and must not delay the system.

The main user interface requirement is a Windows desktop bridge that remains connected to the Synology API. It must deliver notifications, approval requests, job results, health alerts, and cost warnings to David's desktop and let him submit files, folders, prompts, and actions. Follow `docs/DESKTOP_BRIDGE_SPEC.md`.

The desktop and browser interfaces must include a **Recent Calls and Addresses** page. It shows the exact active Synology API, dashboard, health, and live-event addresses; every configured provider address in safely redacted form; and a newest-first call ledger with timestamp, station/action, provider, model, destination, status/error, duration, token usage, estimated cost, job ID, and retries. It must support filters, connection tests, and redacted CSV/JSON export. Never log credentials, authorization headers, raw prompts, or attachment contents.

The Synology deployment must create application directories, deploy containers, configure ports and volumes, establish least privilege, start after reboot, expose health checks, and provide upgrade/backup/recovery procedures. Follow `docs/SYNOLOGY_INSTALL_PACKAGE_SPEC.md`.

---

## 5. PHASE ONE — RIGOROUS DISCOVERY

Before broad implementation, recursively inventory:

- the clean standalone GUI repository
- the recovered-tool library
- the historical Theophysics engine

For each script or executable action, record:

- absolute path
- relative source lineage
- filename
- language
- size
- SHA-256
- last modified time
- purpose
- inputs
- outputs
- dependencies
- whether it changes files
- dry-run support
- collision behavior
- receipt support
- recovery support
- GUI/CLI/API status
- hard-coded paths
- secret-handling risk
- exact duplicates elsewhere
- similar-but-different implementations
- fixture-test status
- recommended disposition

Allowed dispositions:

- CANONICAL CANDIDATE
- WRAP
- REPAIR
- CLEAN REIMPLEMENTATION
- KEEP AS REFERENCE
- LEGACY CANDIDATE
- UNKNOWN — REVIEW REQUIRED

Merge the recovered library's `INVENTORY.csv` into the new candidate registry. Deduplicate exact copies by hash while preserving all source locations.

Known stale-path risks include historical `O:`, `Z:`, prior vault-version paths, and old NAS locations. Report them; do not mass-rewrite them automatically.

Known duplicate families include multiple OpenAI directories and nested engine copies. Compare behavior before recommending consolidation.

Do not bulk-copy the recovered library into the production repository.

---

## 6. EXISTING DESIGNS THAT MUST BE PRESERVED

### Safe file-action primitives

The standalone `file_actions.py` already provides early safe-action work, including:

- Excel to CSV
- CSV to Excel
- Markdown folder combination
- folder inventory with hashes
- verified copying
- collision avoidance
- SHA-256 receipts

Test this code on the fixture. Wrap or extract healthy primitives. Preserve the no-overwrite behavior and extend it with genuine preview and approval.

### Portable folder launcher lineage

The historical engine contains the original idea David remembers:

- `vault_scaffold_builder.py` generated `AAA_MENU.bat`
- `%~dp0` supplied the current folder context
- `scripts/AAA/run_aaa.ps1` launched the local action system
- `MASTER_MENU.ps1` exposed numbered actions
- `81_OPENAI_BLANK/_LAUNCH_TEMPLATE.bat` was designed for arbitrary folders

Preserve the idea but remove stale hard-coded drive fallbacks.

### Split/combine lineage

Recovered candidates include:

- `VaultTools.ps1`
- `VaultTools.bat`
- `merger.py`
- `Combine-All-Markdown.ps1`

The recovery notes warn that an older merger may include an earlier merged output in later runs and overwrite its result. Reproduce or disprove this behavior in the fixture before adoption.

---

## 7. HTML DASHBOARD EXPERIENCE

The home screen must immediately show:

- selected vault
- vault reachability
- overall Vault Health score
- critical/high alerts
- files scanned
- total vault size
- largest and oversized files
- exact duplicates
- sync conflicts
- broken links
- orphan notes
- missing attachments
- missing or duplicate UUIDs
- recent jobs
- failed jobs
- pending approvals
- pending API drafts
- API calls and estimated costs for today/month/all time
- latest successful health scan
- latest known recovery snapshot or backup reference when configured

Navigation should use clear human categories rather than raw script names.

Every action page must show:

- what the action does
- safety classification
- source picker
- destination picker when needed
- options
- dry-run/preview button
- proposed changes
- collision warnings
- estimated affected files and bytes
- approval button
- progress
- cancel capability where safe
- final receipt
- recovery availability

Do not hide serious findings inside a single average health score.

---

## 8. VERSIONED ACTION REGISTRY

The dashboard and terminal menu must use one registry.

Every action entry includes:

- stable numeric ID
- machine action key
- display name
- description
- category
- safety classification
- accepted context type
- option schema
- preview requirement
- adapter or implementation
- version
- enabled/disabled status
- disabled reason

Stable number ranges:

- 1–5: health and emergency
- 6–15: Markdown
- 16–25: files and folders
- 26–30: metadata and Obsidian
- 31–35: media and conversions
- 36–42: API/AI
- 43–47: research, scoring, evidence
- 48–50: dashboard, receipts, settings/advanced

Do not renumber familiar actions when one is retired. Reserve the old number.

---

## 9. PORTABLE 1–50 FOLDER LAUNCHER

Provide a tiny managed launcher named `AAA_MENU.bat` that may be deployed into explicitly selected folders.

When launched, it captures `%~dp0` and shows:

```text
THEOPHYSICS VAULT ACTIONS
Context: C:\the\current\folder

[D] Open HTML Dashboard here
[1] Vault quick health check
[2] Full vault health scan
[3] Emergency check
[6] Combine Markdown
...
[50] Advanced/custom action
[H] Health summary
[R] Recent receipts
[0] Exit
```

Normal work should require only three or four decisions:

1. Choose action.
2. Confirm or adjust source/destination.
3. Preview.
4. Approve or cancel.

The launcher contains no business logic, API key, or destructive command. It locates the installed engine using safe configuration or upward discovery and passes the context as a quoted argument.

Provide deployment modes:

- current folder
- selected folders
- immediate child folders
- recursive under an approved root
- update managed launchers
- remove verified managed launchers

Before recursive deployment show every target and collision. Never overwrite an unrelated `AAA_MENU.bat`.

Write a deployment manifest with target path, previous state, launcher hash, version, timestamp, and outcome. Refuse removal if a launcher was edited after deployment.

If the browser dashboard is unavailable, the numbered terminal menu must remain operational through the same Python action service/CLI and the same SQLite records.

---

## 10. MARKDOWN ACTIONS

Implement or adapt:

- combine selected Markdown files
- combine all Markdown in a folder
- combine recursively with explicit source boundaries
- split by H1
- split by H2
- split by heading pattern
- split by size
- split by token target
- extract selected sections
- remove or normalize frontmatter
- add or repair frontmatter
- convert Markdown to clean text
- identify empty or thin notes
- detect malformed encoding
- detect duplicate notes
- build an index/MOC
- validate links
- find orphan notes

Combination outputs must not become future inputs unless explicitly selected.

---

## 11. FILE AND FOLDER ACTIONS

Implement or adapt:

- verified copy
- reviewed move
- batch rename with old-to-new approval table
- flatten a folder tree safely
- reconstruct from a flattening manifest
- sort by extension/type
- find large files
- propose relocating oversized media
- exact-duplicate analysis
- near-duplicate candidate analysis
- ZIP creation
- safe ZIP extraction
- folder inventory
- SHA-256 manifest
- selected-folder synchronization
- missing expected-page detection
- sync-conflict detection

Flattening must preserve original relative paths, detect duplicate names, and never silently overwrite.

Near-duplicate detection produces candidates, not deletion authority.

---

## 12. VAULT HEALTH AND EMERGENCY CENTER

This is a core product, not an optional cleaner.

### Quick Check

Run quickly at launch or on demand:

- vault exists and is readable
- total files and size
- largest files
- threshold violations
- sync-conflict filenames
- unreadable or malformed text
- obvious cache/temp artifacts
- duplicate UUIDs
- change from previous quick scan

### Full Health Scan

Read-only inspection of:

- file counts by extension and directory
- total and per-directory size
- oversized Markdown, images, audio, video, PDFs, databases, CSVs, ZIPs, and miscellaneous files
- exact duplicate hashes
- same-name/different-content collisions
- possible near duplicates
- broken internal links
- unresolved embeds
- missing attachments
- orphan notes
- unreferenced attachments
- empty notes
- empty directories
- missing/invalid/duplicate UUIDs
- invalid or inconsistent YAML
- invalid filenames
- path-length risk
- unsupported attachments
- stale absolute paths and drives
- sync conflicts
- nested `.obsidian` directories
- nested vault candidates
- plugin/config health without exposing secrets
- generated/cache/build directories that may harm synchronization
- recent unexpected growth
- files changing during the scan

### Emergency Check

Designed for “something is wrong right now”:

- vault unavailable or partially reachable
- NAS/UNC disconnected
- sudden file-count loss or growth
- sudden vault-size change
- mass rename/move patterns compared with the previous manifest
- zero-byte explosion
- sync-conflict explosion
- unreadable/corrupt-looking Markdown or YAML
- missing-attachment spike
- changed `.obsidian` configuration
- plugin/config anomaly
- newest unexpected files
- largest unexpected files
- last known healthy snapshot comparison

Emergency mode reports evidence and containment suggestions. It must not automatically repair, restore, move, delete, or disable anything.

### Configurable file-size policy

Provide editable per-extension thresholds. Sensible example defaults:

- Markdown: warning 5 MB, critical 20 MB
- Image: warning 20 MB, critical 50 MB
- Audio: warning 50 MB, critical 250 MB
- Video: warning 250 MB, critical 1 GB
- PDF: warning 50 MB, critical 250 MB
- CSV/database: warning 100 MB, critical 500 MB
- ZIP/archive: warning 100 MB, critical 1 GB

A large file is not automatically bad. Explain its possible sync, indexing, backup, repository, or mobile impact.

### Findings

Every finding records:

- stable finding ID
- scan ID
- timestamp
- vault root
- severity
- category
- affected paths
- measured value
- configured threshold
- why it matters
- evidence
- recommended next step
- action safety classification
- status
- first seen
- last seen

Severity levels:

- Critical
- High
- Medium
- Low
- Information

Show the score and its evidence. Findings remain visible even if acknowledged.

### Health statistics

Persist:

- file count over time
- bytes over time
- growth by extension
- health score over time
- new/resolved findings
- largest-file trend
- duplicate-byte trend
- sync-conflict trend
- scan duration

Allow comparison with previous scans.

### Reports

Export:

- HTML
- Markdown
- JSON
- CSV
- optional file/hash manifest

Do not embed file contents or secrets unless explicitly requested.

Health findings may open a proposed remediation action, but they never execute the repair directly.

---

## 13. API STATION GENERATOR

Provide:

- `CREATE_API_STATION.bat`
- `CREATE_API_STATION.ps1`
- dashboard action named **New API Station**

The batch file calls maintained Python; it must not duplicate the scaffolding logic.

Ask for:

- station name
- parent destination
- provider
- default model
- single-file or batch mode
- default prompt template
- output extension
- one-request-per-input behavior
- maximum concurrency

Show the proposed configuration and path before creation. Never overwrite an existing station.

Generate:

```text
STATION_NAME/
  README.md
  RUN.bat
  RUN_DRY.bat
  STATUS.bat
  station.yaml
  prompt.md
  prompt.system.md
  prompt.output-contract.md
  .env.example
  .gitignore
  INBOX/
    README.md
  OUTBOX/
    README.md
  BACKSIDE/
    runner.py
    station_cli.py
    pricing.yaml
    schemas/
    templates/
    logs/
    receipts/
    failed/
    processed/
    calls/
      00_TEMPLATE/
        call.yaml
        prompt.md
        input/
        output/
        receipts/
```

Normal use becomes:

1. Put files into `INBOX` or a call's `input` folder.
2. Edit `prompt.md`.
3. Run `RUN.bat` or click Run.

Each saved call lives under `BACKSIDE/calls/CALL_NAME` and can be created, duplicated without secrets/results, previewed, tested on one item, run as a batch, resumed, and retried.

The runner must:

1. Hash the source.
2. Hash all prompt components.
3. Validate configuration.
4. Estimate size and warn about limits.
5. Support a true no-network dry run.
6. Submit the request.
7. Save raw response separately from cleaned output.
8. Validate the output contract.
9. Record model, provider request ID, tokens, latency, retries, and status.
10. Calculate estimated cost from a versioned pricing table.
11. Write an immutable receipt.
12. Preserve source inputs.

Partial batch failures must preserve successful outputs and avoid blindly repeating completed source-hash/prompt-version combinations.

Default output naming:

`SOURCE_STEM__CALL_NAME__YYYYMMDD-HHMMSS.ext`

Never place a real API key inside a generated station. Use environment variables or an OS-appropriate secret store. Redact secrets everywhere.

---

## 14. DEFAULT PROMPT SYSTEM

Prompts are versioned layers:

1. Safety/provenance contract
2. David's theological and epistemic frame
3. Task template
4. Project override
5. Output/validation contract

The dashboard must let David:

- select a default prompt
- edit the task prompt
- edit the project override
- preview the exact resolved prompt
- save prompt versions
- compare versions
- test one item
- approve a batch
- review outputs before placement

Default contract:

- preserve source text, quotations, and lineage
- never fabricate citations, evidence, experiments, statistics, or results
- separate evidence, formal/model result, interpretation, theology, and canon decision
- fairly present the strongest objection
- retain honest gaps
- include real kill conditions
- never treat analogy as isomorphism without demonstration
- never convert a compiled model or formal receipt into physical or theological proof
- mark API output as draft pending review
- never grant mutation, deletion, publishing, or canonization authority

David's frame:

God is the Creator; physics, information, consciousness, moral order, history, relationship, revelation, and Christ belong to one created reality. Science studies repeatable patterns within creation but does not independently settle the ultimate Creator premise. The project starts from the theological premise and asks whether scientific structures illuminate created order. Truth is distributed redundantly through creation, conscience, reason, moral consequence, history, relationship, revelation, and Christ. Christ is the proposed interpretive center. Corruption may distort witnesses without erasing them all. Do not turn unresolved bridges into apologetic or scientific certainty.

---

## 15. STATISTICS AND COST ACCOUNTING

Persist locally in SQLite:

- job ID
- action type
- status
- start/end time
- duration
- source/destination
- files examined/changed/skipped/failed
- bytes read/written/moved
- preview timestamp
- approval timestamp
- receipt path
- API provider/model
- input/output/cached/reasoning tokens when supplied
- estimated cost
- actual cost when available
- retry count
- error category
- prompt version
- validation outcome

Pricing configuration must be versioned and editable. Never claim hard-coded pricing is current.

Provide daily, weekly, monthly, and all-time summaries with CSV/JSON export.

---

## 16. TEST FIXTURE

Create a disposable fixture vault containing:

- nested folders
- Markdown with H1/H2/H3
- duplicate filenames in different folders
- exact duplicates
- near duplicates
- valid YAML
- invalid YAML
- missing frontmatter
- broken links
- missing attachment
- orphan note
- unreferenced attachment
- missing UUID
- duplicate UUID
- Unicode path
- long path
- sync-conflict filename
- oversized dummy Markdown/image/audio/PDF/database/archive files
- ZIP
- CSV
- JSON
- empty file
- empty directory
- nested `.obsidian`

Test every adopted action against this fixture.

Prove:

- preview causes no mutation
- apply matches approved preview
- collisions never overwrite
- receipts account for every change
- recovery works when declared
- cancellation/restart does not corrupt jobs
- API failure preserves inputs and completed outputs
- secrets never appear in logs or browser responses
- health scans never modify the vault
- large scans report progress and keep the interface responsive
- launcher works in paths with spaces and Unicode
- terminal and dashboard action IDs match
- recursive launcher deployment is previewed and receipted
- generated API station dry run sends no network request

---

## 17. REQUIRED DELIVERABLES

Before broad mutation features:

1. `ENGINE_INVENTORY.csv`
2. `EXACT_DUPLICATE_GROUPS.csv`
3. `SIMILAR_IMPLEMENTATIONS.md`
4. `STALE_PATHS.csv`
5. `DESTRUCTIVE_SCRIPT_REPORT.md`
6. `ACTION_CATALOG.yaml`
7. `ACTION_TEST_REPORT.md`
8. `CONSOLIDATION_PLAN.md`
9. `OLD_TO_NEW_REVIEW.csv`
10. `RISK_REGISTER.md`
11. Architecture decision record
12. Working dashboard shell
13. SQLite job/statistics schema
14. Read-only Vault Health MVP
15. Fixture vault and tests
16. Production dashboard launcher
17. Portable 1–50 folder launcher
18. Launcher deployment/update/removal tool
19. API Station Generator
20. Generated fixture API station with dry-run receipt
21. Setup, troubleshooting, and recovery guide for a non-programmer
22. Synology Container Manager bundle with preflight checker, installer, upgrader, backup/restore, and uninstaller
23. Windows desktop bridge installer and tray application
24. Optional DSM `.spk` only if it provides clear value and target compatibility is established

After David approves the consolidation plan, continue with the remaining safe action adapters.

---

## 18. FIRST MILESTONE DEFINITION OF DONE

The first milestone is complete only when:

- Double-clicking the main launcher starts one local server.
- The browser opens automatically.
- David can select a vault.
- The dashboard displays the active vault clearly.
- A read-only health scan runs with progress.
- Findings are grouped by severity and category.
- Oversized files are reported using configurable thresholds.
- Health reports export successfully.
- Statistics persist across restarts.
- A portable `AAA_MENU.bat` opens the same system with its folder as context.
- The numbered terminal menu works if the browser does not.
- A new API station can be generated safely.
- The generated station performs a true dry run.
- No real vault source file is modified during acceptance.
- Tests pass on Windows.
- No API key is present in the repository, generated fixture, logs, or browser.
- Clean shutdown and restart work.
- The Synology installation bundle passes clean deployment, reboot persistence, upgrade, backup/restore, and uninstall-with-data-preservation tests.
- The Windows desktop bridge reconnects after desktop or NAS restart and delivers a real approval request and completion notification end to end.

Do not claim completion from screenshots, imports, mocks, or unit tests alone. Demonstrate the real Windows launcher, local browser dashboard, fixture-vault scan, persistent statistics, folder-context launcher, generated API station, receipts, and clean shutdown.

---

## 19. REQUIRED FIRST RESPONSE

Before implementing, respond with:

1. Your understanding of the mission.
2. The exact repositories and directories you inspected.
3. Total files and folders found in each source.
4. Script counts by language.
5. Exact duplicate groups or the method you will use to compute them.
6. Major existing tool families.
7. Existing dashboards and launchers.
8. Existing file actions and safety controls.
9. Existing API runners/stations.
10. Stale-path count.
11. Potentially destructive scripts.
12. The five most serious structural problems.
13. A read-only Phase One plan.
14. Where the inventory reports will be written.

Do not move, rename, delete, rewrite, archive, consolidate, or enable existing scripts during the first pass.
