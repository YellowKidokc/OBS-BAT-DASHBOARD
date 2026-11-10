# Folder snapshot and overview

## Purpose

Give David one page showing the complete captured folder structure across selected
vault roots. Start with compact, expandable headings so the overview remains usable
without displaying every file at once. This extends the read-only health scan;
it does not create a second scanner or a separate authoritative paper registry.

## Capture contract

- Record selected roots, capture time, scan mode, thresholds, inclusion/exclusion
  rules, hash policy, and scanner version. Display these under expandable “Scan parameters.”
- Include dot-prefixed folders, empty folders, and nested vault boundaries in the
  inventory even when Obsidian hides them. Mark dot-prefixed names explicitly;
  do not infer that every such folder was hidden by our visibility switcher.
- Inventory `.obsidian` and `.git` as folder boundaries by default without reading
  their configuration contents. Display any excluded descendants and the reason.
  Provide an explicit metadata-only option to inventory their descendants.
- Do not follow symlinks, junctions, or other reparse points by default. Record
  them as boundaries. Report inaccessible paths and files changed during capture.
- Record per-folder direct and recursive file counts, child-folder count, bytes,
  and associated health findings. Avoid double counting overlapping selected roots.
- A capture is not atomic. Show start/end timestamps and completeness; an unreadable
  folder must not be represented as an empty, healthy folder.
- Store snapshot metadata outside scanned roots, excluding the output location
  if it falls under a selected root. Never modify scanned files.
- A snapshot is an inventory, not a content backup or restoration guarantee.

## One-page interaction

- Show each selected vault/root as a section, with its immediate folders as
  compact headings. Each heading shows name, counts, size, hidden-name state,
  and the highest-severity finding when present.
- Clicking a heading expands its child folders and file inventory in place.
  Load or page large branches on demand; collapsing affects display only.
- Use consistent widths, spacing, and aligned summary fields. Reflow into fewer
  columns on narrower screens. Expanding one branch must not expand every branch.
- Provide search, hidden-folder and findings filters, collapse all, and a clear
  indication when a filter hides results. Include full paths for ambiguous names.
- Preserve expansion state while reviewing the same snapshot. Keyboard users
  can expand/collapse headings and see focus; communicate expanded state.
- Keep the entire captured hierarchy reachable on this page. Do not force the
  entire hierarchy into a single screen or shrink text to make it fit.
- Separate “Captured at” from any current live information. A displayed snapshot
  must not silently change to reflect later filesystem operations.

## Comparison and operations

Compare two chosen snapshots for additions, removals, size changes, visibility-name
changes, and possible moves. Without persistent IDs or other sufficient evidence,
label inferred moves as candidates rather than confirmed identity matches.

Folder actions can open existing preview workflows: combine selected Markdown
files into a new output, move a folder out to a selected destination, or change
managed folder visibility. Clarify the action and its parameters before execution.
Do not wire these controls to unverified legacy scripts.

Every modifying action needs collision checks, a preview of affected paths,
explicit execution, an operation manifest, and recovery instructions under the
dashboard's existing rules. Preserve originals by default when combining files.
Do not treat a snapshot as permission to restore or overwrite current files.

When the paper registry is connected, changes to managed folder paths must be
reported to its owner. Do not promise preservation of ordinary Obsidian links or
third-party plugin links until tested. Registry integration remains unimplemented.

## Acceptance checks

Use a test tree containing two vaults, a dot-prefixed chapter, `.obsidian`, an
empty folder, duplicate folder names, a deep branch, a link/junction, and an
inaccessible directory where the platform allows one.

1. Capture metadata without changing the source tree. All included folders are
   reachable through expansion, including hidden and empty folders.
2. Exclusions, boundaries, errors, and incomplete results remain visible.
3. Folder totals agree with the underlying manifest; overlapping roots do not
   inflate totals. A large branch is paged without losing access to entries.
4. Keyboard expansion, filters, narrow-screen reflow, and collapse all work.
5. After a test rename or move, the old capture remains unchanged. A new capture
   and comparison show the difference with appropriate identity uncertainty.
6. Viewing or expanding the report never launches a modifying operation.

Status: requirements recorded; snapshot scanner and UI have not been implemented
or validated by this document.
