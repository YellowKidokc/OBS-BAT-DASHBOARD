# Obsidian Vault Operations Dashboard

Production control surface for the Faith Through Physics Obsidian vault and its automation engine.

This repository is the clean implementation and handoff location. The existing engine remains the source inventory until its actions are tested and deliberately adopted.

## Product goal

Double-click one launcher and open a local HTML dashboard in the default browser. From the dashboard David can inspect vault health, preview and run approved file actions, launch research/API workflows, review job history, and see operational statistics and estimated API costs.

## Core rules

- Local-first and Windows-friendly.
- Dry-run by default.
- Never silently overwrite or delete a file.
- Every mutating job produces a manifest and recovery instructions.
- Existing scripts are inspected and wrapped before replacements are invented.
- API output is a draft until human approval.
- API keys never enter the repository, browser bundle, prompt files, or logs.

## Start here

### Working read-only folder snapshot

On Windows, drag a vault or parent folder onto `FOLDER_SNAPSHOT.bat`. Python 3.11+
with the Windows `py` launcher is required. The launcher opens a self-contained
HTML report and saves JSON alongside it under local application data. No package
installation or internet access is required. The Windows launcher itself still
needs verification on a Windows machine.

For several non-overlapping vaults, use:

```sh
python tools/folder_snapshot.py /path/to/vault-one /path/to/vault-two --output /path/outside-vaults/new-report --open
python -m unittest discover -s tests -v
```

The report includes expandable folders, dot-prefixed and empty folders, counts,
sizes, capture parameters, and visible scan errors. System folders are shown as
excluded boundaries by default; `--include-system` includes their metadata.
Links/junctions are not traversed. File contents are never embedded. A snapshot
is not an atomic backup. Reports contain local paths: review before sharing.

This is the first standalone snapshot slice. Health diagnostics, snapshot
comparison, search/filtering, large-tree paging, and modifying actions remain
unimplemented; the wider specifications below describe future work.

Give [`PRODUCTION_CODER_PROMPT.md`](PRODUCTION_CODER_PROMPT.md) to the implementation agent.

Supporting requirements:

- [`docs/FOLDER_SNAPSHOT_SPEC.md`](docs/FOLDER_SNAPSHOT_SPEC.md)

- [`docs/VAULT_HEALTH_AND_EMERGENCY_SPEC.md`](docs/VAULT_HEALTH_AND_EMERGENCY_SPEC.md)
- [`docs/PRODUCT_ARCHITECTURE.md`](docs/PRODUCT_ARCHITECTURE.md)
- [`docs/API_STATION_SCAFFOLDER_SPEC.md`](docs/API_STATION_SCAFFOLDER_SPEC.md)
- [`docs/PORTABLE_FOLDER_LAUNCHER_SPEC.md`](docs/PORTABLE_FOLDER_LAUNCHER_SPEC.md)
- [`docs/SYNOLOGY_INSTALL_PACKAGE_SPEC.md`](docs/SYNOLOGY_INSTALL_PACKAGE_SPEC.md)
- [`docs/DESKTOP_BRIDGE_SPEC.md`](docs/DESKTOP_BRIDGE_SPEC.md)

## Existing engine to inventory

`C:\Users\David\Documents\faiththruphysics.com\00_SYSTEM\01_SYSTEM_OS\00_VAULT\02_CONTROL\01_ENGINE`

Curated reusable-tool recovery library:

`D:\GitHub\Codex-Powershell_GUI\Reusable_Tools_From_Theophysics`

The recovery library contains its own SHA-256 inventory and adaptation notes. Its contents are reference candidates, not verified production actions.

Existing GUI and safe-action implementation:

`D:\GitHub\Codex-Powershell_GUI`

This standalone repository is the primary implementation reference. Do not develop against the much larger `D:\GitHub\pipeline-workflows\Codex-Powershell_GUI` working copy.

Do not reorganize that directory as part of initial dashboard development.
