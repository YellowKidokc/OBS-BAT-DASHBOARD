# Phase One inventory (read-only)

`inventory.py` is standard-library Python 3.9 or newer. It reads files and hashes them. It never writes to the folders it scans, and it refuses to write its reports inside a scanned folder.

## On Windows

Double-click `RUN_INVENTORY_WINDOWS.bat`. It scans `D:\GitHub\Codex-Powershell_GUI` and the `01_ENGINE` engine folder, then writes reports to `reports\phase1\windows_YYYYMMDD\`. A missing path is skipped with a warning.

## Outputs

| File | Contents |
|---|---|
| `ENGINE_INVENTORY.csv` | One row per file: path, size, SHA-256, modified time, language, purpose, dependencies, whether it deletes, moves or writes, dry-run and receipt support, network, GUI/CLI, stale-path hits, secret references, risk and suggested disposition |
| `EXACT_DUPLICATE_GROUPS.csv` | Byte-identical files grouped by hash, with every location kept |
| `SIMILAR_IMPLEMENTATIONS.md` | Script filenames that exist with different contents |
| `STALE_PATHS.csv` | Every line with an `O:`, `Z:`, old vault version, LAN IP, UNC or absolute Windows path |
| `DESTRUCTIVE_SCRIPT_REPORT.md` | Delete, move and rename call sites with line numbers |
| `INVENTORY_REPORT.html` | Visual report: built by `python visualize.py REPORT_DIR`; offline, self-contained |
| `SUMMARY.json` | Counts |
| `SCAN_ERRORS.csv` | Files that could not be read |

The classification comes from pattern matching (a heuristic), not from running anything. Suggested dispositions are starting points for review, not decisions.

Credential-looking values are redacted in every report (v0.2.0+). Files that look like they hold a key get no purpose text and no stale-path context.
