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

Give [`PRODUCTION_CODER_PROMPT.md`](PRODUCTION_CODER_PROMPT.md) to the implementation agent.

Supporting requirements:

- [`docs/VAULT_HEALTH_AND_EMERGENCY_SPEC.md`](docs/VAULT_HEALTH_AND_EMERGENCY_SPEC.md)
- [`docs/PRODUCT_ARCHITECTURE.md`](docs/PRODUCT_ARCHITECTURE.md)

## Existing engine to inventory

`C:\Users\David\Documents\faiththruphysics.com\00_SYSTEM\01_SYSTEM_OS\00_VAULT\02_CONTROL\01_ENGINE`

Curated reusable-tool recovery library:

`D:\GitHub\pipeline-workflows\Codex-Powershell_GUI\Reusable_Tools_From_Theophysics`

The recovery library contains its own SHA-256 inventory and adaptation notes. Its contents are reference candidates, not verified production actions.

Do not reorganize that directory as part of initial dashboard development.
