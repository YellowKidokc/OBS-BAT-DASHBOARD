# Portable Folder Launcher Specification

## Recovered design lineage

The earlier Theophysics engine already implemented this idea:

- `01_ENGINE/scripts/vault_scaffold_builder.py` generated `AAA_MENU.bat` files.
- The batch launcher used `%~dp0` as the active context folder.
- `01_ENGINE/scripts/AAA/run_aaa.ps1` and `MASTER_MENU.ps1` presented actions.
- `81_OPENAI_BLANK/_LAUNCH_TEMPLATE.bat` was intended to be copied into arbitrary folders.

Inspect these sources and preserve the context-folder behavior. Remove stale hard-coded `O:` fallbacks in the production implementation.

## User experience

David may deploy a small launcher named `AAA_MENU.bat` into selected folders. From any such folder he can double-click it and receive:

```text
THEOPHYSICS VAULT ACTIONS
Context: C:\current\folder

[D] Open HTML Dashboard here
[1] Vault quick health check
[2] Full vault health scan
[3] Combine Markdown in this folder
...
[50] Advanced/custom action
[0] Exit
```

The normal action should take no more than three or four decisions:

1. Select action number.
2. Confirm or adjust source/destination.
3. Preview proposed work.
4. Approve or cancel.

Safe read-only actions may require fewer steps. File-changing actions may never skip preview and approval.

## One registry, two interfaces

The numbered menu and HTML dashboard must read the same versioned action registry. Do not hard-code separate action implementations into PowerShell.

Each action registry entry includes:

- stable numeric ID from 1 through 50
- machine action key
- display name and short help
- category
- read-only/reversible/quarantine/destructive classification
- accepted context type
- option schema
- preview requirement
- implementation adapter
- enabled/disabled state and reason

Numbers remain stable across releases. Retired actions leave a reserved ID instead of renumbering everything David already knows.

## Thin launcher

`AAA_MENU.bat` must be a small redirector only. It should:

1. Capture its folder using `%~dp0`.
2. Locate the installed dashboard/CLI through a machine-level user configuration or a safe upward search.
3. Pass the context folder as a quoted argument.
4. Offer a useful repair message if the engine cannot be found.
5. Contain no API key, business logic, or destructive command.

Do not hard-code a historical drive such as `O:` or `Z:`.

## Dashboard behavior

Choosing `D` starts or reuses the single local dashboard server and opens a context URL similar to:

`http://127.0.0.1:PORT/?context=CONTEXT_TOKEN`

Do not put the raw unrestricted filesystem path into a remotely accessible URL. The backend should issue a short-lived local context token or otherwise validate the selected root.

The dashboard must visibly display the context folder and never silently substitute another root.

## Terminal fallback

The terminal menu must remain usable if the browser dashboard is unavailable. It calls the same Python action service/CLI and writes jobs to the same SQLite database, statistics, receipts, and review queue.

It supports:

- number selection
- category view
- search by action name
- favorites/recent actions
- `? NUMBER` for help
- `D` for dashboard
- `H` for health summary
- `R` for recent receipts
- `0` to exit

## Launcher deployment tool

Provide a dashboard action and command-line tool that can deploy launchers to explicitly selected folders.

Required modes:

- current folder only
- selected folders
- immediate child folders
- recursive deployment under an approved root
- update previously deployed launchers
- remove only launchers verified as managed copies

Before recursive deployment, show:

- resolved approved root
- exact target folders
- existing `AAA_MENU.bat` collisions
- how many create/update/skip operations are proposed
- launcher version and SHA-256

Require approval. Never replace an unrelated file with the same name.

Write a deployment manifest containing every target, prior state, installed hash, version, timestamp, and result. Removal must use this manifest plus current-hash verification. If a deployed launcher was edited, flag it for review rather than deleting it.

## Suggested initial stable menu

The exact registry may evolve, but reserve coherent number ranges:

- 1-5: health and emergency
- 6-15: Markdown actions
- 16-25: files and folders
- 26-30: metadata and Obsidian
- 31-35: media and conversion
- 36-42: API/AI stations and calls
- 43-47: research/scoring/evidence
- 48-50: dashboard, receipts, settings/advanced

The menu should show only enabled actions by default while retaining stable numbers.

## Acceptance tests

- Launcher works from a path containing spaces and Unicode.
- Context equals the launcher directory.
- Dashboard and CLI receive the same context.
- Missing engine produces repair instructions without changing the folder.
- Recursive deployment requires preview and approval.
- Existing unrelated `AAA_MENU.bat` is never overwritten.
- Managed launcher update produces a receipt.
- Removal refuses a launcher whose hash no longer matches the managed version.
- Action numbers resolve identically in the dashboard and CLI.
- A file-changing action cannot bypass preview through the terminal interface.
