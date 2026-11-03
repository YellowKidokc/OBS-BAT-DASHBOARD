# Vault Health and Emergency Specification

## Purpose

Provide a read-only inspection and emergency-response center for Obsidian vaults. It should tell David whether a vault is healthy, what requires attention, and what can be safely reviewed next. A scan must never modify the vault.

## Modes

### Quick Check

Fast checks suitable for every launch:

- vault path exists and is readable
- total files and size
- largest files
- files exceeding configured limits
- sync-conflict filenames
- malformed or unreadable text files
- obvious temporary/cache artifacts
- duplicate UUIDs
- latest scan comparison

### Full Health Scan

Complete read-only scan:

- file counts by extension and directory
- total and per-directory size
- oversized Markdown, image, audio, video, PDF, database, archive, and miscellaneous files
- exact duplicates by SHA-256
- same-name/different-content collisions
- possible near duplicates, clearly labeled as candidates
- broken internal links
- unresolved embeds and missing attachments
- orphan notes and unreferenced attachments
- empty notes and directories
- missing, invalid, or duplicate UUIDs
- invalid or inconsistent YAML frontmatter
- invalid filenames and path-length risks
- unsupported attachment extensions
- stale absolute paths and drive references
- sync conflicts
- nested `.obsidian` directories and possible nested vaults
- plugin/config health without exposing secrets
- generated/cache/build folders that may not belong in sync
- ZIP/database/CSV/media files that exceed configured limits
- recent unexpected growth since the last scan
- files changed during the scan

### Emergency Check

Optimized for “something is wrong now”:

- vault unavailable or only partially reachable
- sudden file-count or size loss/growth
- mass renames or moves compared with the last manifest
- large number of zero-byte files
- duplicate/sync-conflict explosion
- unreadable/corrupt-looking Markdown or YAML
- missing attachment spike
- changed `.obsidian` configuration
- plugin/config anomalies
- newest and largest unexpected files
- NAS/UNC disconnection
- active sync activity where detectable
- last known healthy snapshot and comparison

Emergency mode reports evidence and suggested containment steps. It must not automatically repair, delete, move, disable plugins, or restore files.

## Configurable size policy

Provide editable thresholds with sensible defaults and per-extension overrides. Example starting values only:

- Markdown: warning 5 MB, critical 20 MB
- Image: warning 20 MB, critical 50 MB
- Audio: warning 50 MB, critical 250 MB
- Video: warning 250 MB, critical 1 GB
- PDF: warning 50 MB, critical 250 MB
- CSV/database: warning 100 MB, critical 500 MB
- ZIP/archive: warning 100 MB, critical 1 GB

Do not label a file bad merely because it is large. Report why it may affect sync, indexing, backup, or repository performance.

## Health scoring

Show both an overall score and the underlying evidence. Never hide serious findings behind an average.

Severity levels:

- Critical: probable data-loss, corruption, inaccessible root, or widespread conflict
- High: likely operational failure or major sync/indexing impact
- Medium: structural issue requiring planned review
- Low: hygiene or optimization opportunity
- Information: inventory only

Score weights must be configurable and documented. Findings remain visible even if dismissed.

## Findings record

Every finding contains:

- stable finding ID
- scan ID and timestamp
- vault root
- severity
- category
- affected path(s)
- measured value and configured threshold
- why it matters
- evidence
- recommended next action
- whether the recommendation is read-only, reversible, or destructive
- status: new, acknowledged, resolved, ignored with reason
- first seen and last seen

## Baselines and statistics

Persist scan summaries so the dashboard can display:

- file count and bytes over time
- growth by extension
- health score over time
- new/resolved findings
- largest-file trend
- duplicate-byte trend
- sync-conflict trend
- scan duration

Allow comparison with any previous scan. Baselines are evidence, not restoration authority.

## Reviewable remediation

Health findings may open a separate proposed action, but never execute it directly. Examples:

- propose moving oversized media outside the vault
- propose quarantining an exact duplicate
- propose repairing YAML
- propose resolving a broken link
- propose renaming an invalid filename

The proposed action must go through preview, collision detection, approval, execution receipt, and recovery instructions.

## Reports

Export:

- human-readable HTML/Markdown report
- JSON machine record
- CSV findings table
- file/hash manifest when selected

Reports must redact secrets and avoid embedding file contents unless explicitly requested.
