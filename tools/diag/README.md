# Diagnostics: read-only instruments

None of these change anything. Each one writes a Markdown report to `%USERPROFILE%\VaultOps\reports\<tool>\` (or `%VAULTOPS_HOME%`). It also overwrites `<tool>_LATEST.md` each run, so the AI that picks up tomorrow always knows where to look.

| Launcher | When | What it tells you |
|---|---|---|
| `VAULT_PULSE.bat` | Morning | What's new, modified, deleted and moved/renamed since the last pulse, and what was touched in the last 24 h. Flags mass deletions (CRITICAL), mass renames, empty notes, sync-conflict copies and `.obsidian` changes. The first run only records a baseline. Set `VAULTOPS_VAULT` to skip typing the path. |
| `REPO_READY.bat` | Before handing a repo to an AI | GO / GO with warnings / NO-GO. Checks uncommitted changes, an unpushed or never-pushed branch, merge/rebase in progress, behind remote, stashes, other floating branches and open PRs. Add `--tests` to run the test suite. |
| `BRANCH_AUDIT.bat` | Weekly, or after a batch of AI tasks | Every branch across every repo under a folder (default `D:\GitHub`): LANDED / IN REVIEW / FLOATING / FLOATING + STALE / ABANDONED? / EMPTY / LOCAL ONLY. |
| `DUPLICATE_REPORT.bat` | On demand | Exact duplicate families, wasted space, and same-name/different-content collisions. |

For PR states, install the GitHub CLI and run `gh auth login`. Without it, branches that were squash-merged show as FLOATING, and the report says so.

Exit codes for scripting: `REPO_READY` returns 0 for GO, 1 for warnings and 2 for NO-GO. `VAULT_PULSE` returns 1 when there's a CRITICAL flag.
