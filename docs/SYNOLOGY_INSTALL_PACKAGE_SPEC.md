# Synology Installation Package Specification

## Required outcome

Deliver something David can actually install on his Synology. Source code and manual Docker commands alone are not complete.

Provide one required artifact and one optional artifact:

1. Required: a supported **Container Manager installation bundle** using a project/Compose definition.
2. Optional: after confirming the target model, CPU architecture, RAM, and DSM version, a DSM **`.spk` package or installer wrapper** if it materially improves installation or lifecycle management.

The container bundle is the application core. Do not delay the desktop-connected system in order to produce an `.spk`.

## Hardware preflight

Before installation, detect and report:

- DSM version
- Synology model
- CPU architecture
- installed memory
- free storage
- Container Manager availability
- required ports already in use
- configured destination volume
- outbound HTTPS availability for optional AI providers
- local network address
- whether optional local-model requirements are satisfied

Stop with understandable instructions when a hard requirement is missing. Do not partially install silently.

## Installable bundle layout

```text
synology-package/
  README_INSTALL.md
  BUILD_PACKAGE.ps1
  CHECK_PACKAGE.ps1
  artifacts/
  container-project/
    compose.yaml
    .env.example
    config/
    migrations/
    healthcheck/
  spk-optional/
    INFO
    package.tgz
    scripts/
      preinst
      postinst
      preuninst
      postuninst
      preupgrade
      postupgrade
      start-stop-status
    conf/
      privilege
      resource
    WIZARD_UIFILES/
  tools/
    preflight.py
    install.py
    upgrade.py
    backup.py
    restore.py
    uninstall.py
```

Follow Synology's current Package Developer Guide for package metadata, scripts, privileges, resources, wizard files, and DSM integration.

## Services

The default project may contain:

- `api`: FastAPI application
- `worker`: background jobs and AI/tool execution
- `db`: PostgreSQL
- `redis`: queue/cache, if required
- optional vector-search service when PostgreSQL/pgvector is not selected
- optional local model service only on supported hardware

Do not expose database or Redis ports outside the private project network.

## Persistent data

Create explicit shared-folder locations selected during installation, for example:

```text
/volumeN/TheophysicsAPI/
  config/
  inbox/
  outbox/
  backside/
  database/
  receipts/
  reports/
  backups/
```

Application upgrades must not replace these directories.

The live Obsidian vault is mounted read-only by default. Any writable vault root requires a separate explicit configuration and must still use preview and approval controls.

## Installation wizard

Ask for:

- destination volume/shared folder
- application port or automatic safe selection
- LAN-only versus private remote-access mode
- administrator account bootstrap
- approved read-only vault roots
- optional writable output root
- optional API-provider enablement
- secret configuration method
- resource limits
- backup destination

Display a final review page before installation.

Do not ask the user to paste secrets into files committed with the application. Store secrets using a local protected mechanism appropriate to DSM and never display them later.

## Lifecycle behavior

### Install

- validate prerequisites
- create least-privilege service identity and directories
- establish ownership/permissions
- deploy project
- run database migrations
- wait for `/health`
- show local dashboard URL
- write an installation receipt

### Start/restart

- start after DSM reboot
- use health checks
- avoid duplicate instances
- provide useful failure logs without leaking secrets

### Upgrade

- back up configuration and database first
- validate target version
- preserve persistent data
- apply migrations safely
- rollback or give recovery instructions if health checks fail
- write an upgrade receipt

### Backup/restore

Back up:

- database
- non-secret configuration
- encrypted/protected secret references as appropriate
- action registry
- prompt versions
- receipts and statistics

Do not back up large input/output material by surprise. Make that an explicit option.

### Uninstall

Default behavior preserves user data and backups. Offer a separate clearly labeled full-removal option with an exact preview and confirmation. Never delete the live vault.

## Networking and security

- Bind application service to LAN/local interfaces according to selected mode.
- Do not expose DSM, PostgreSQL, or Redis through router port forwarding.
- Remote access should use a private overlay such as Tailscale or an authenticated tunnel such as Cloudflare Tunnel.
- Require application authentication even on the LAN.
- Support scoped API tokens for dashboard, scripts, and automation clients.
- Rate-limit intelligent/AI endpoints.
- Validate filesystem roots and prevent traversal.
- Redact secrets from logs and receipts.
- Provide a credential-rotation procedure.

## Resource profiles

Offer profiles based on detected hardware:

- **Orchestrator only:** FastAPI, worker, database; cloud AI for inference.
- **Light local AI:** small local classifier/embedding model when RAM/CPU permits.
- **External inference host:** Synology orchestrates but sends local-model work to another LAN machine.

Do not enable Ollama or download a large model merely because Container Manager exists. Require hardware validation and explicit selection.

## Build artifacts

CI or the documented build process should produce:

- versioned Compose/project ZIP
- versioned `.spk` when target compatibility is established
- SHA-256 checksum file
- software bill of materials where practical
- release notes
- install/upgrade/recovery guide

Do not commit generated credentials, database contents, `.env`, or private deployment state.

## Acceptance testing

Test on the target DSM environment or an appropriately matched test environment:

1. Clean install through the supported interface.
2. Dashboard reachable on LAN.
3. API authentication enforced.
4. Health endpoint passes.
5. DSM reboot automatically restores service.
6. Source vault remains read-only.
7. API station job completes and writes a receipt.
8. Upgrade preserves data and statistics.
9. Failed upgrade has recovery instructions or rollback.
10. Backup and restore reproduce application state.
11. Default uninstall preserves data.
12. Full removal deletes only the explicitly previewed application directories.
13. No secrets appear in package files, logs, browser responses, or receipts.

## Information required from David

For the required container deployment, obtain:

- exact Synology model number
- DSM version
- installed RAM
- preferred storage volume
- whether Container Manager is installed
- LAN-only, Tailscale, or Cloudflare access preference

The Container Manager bundle can be developed generically. Any optional `.spk` compatibility declaration must be based on the actual target.
