# Product Architecture

## Principle

The dashboard is a control plane. File actions remain small, testable units registered behind one stable interface.

```text
Windows launcher
      |
      v
Local FastAPI server ---- SQLite statistics / jobs / findings
      |
      +---- HTML dashboard
      |
      +---- action registry
              |
              +---- native safe actions
              +---- adapters for verified legacy scripts
              +---- API prompt workflows
```

## Suggested packages

```text
obsidian_dashboard/
  app/
    api/
    web/
    jobs/
    stats/
    health/
    actions/
    prompts/
    security/
  config/
  migrations/
  tests/
  launchers/
  docs/
```

## Action contract

Every action implements:

- metadata and version
- accepted source/destination types
- option schema
- `preview()`
- `validate_preview()`
- `apply(approved_preview_id)`
- receipt generation
- recovery capability declaration
- progress and cancellation hooks

An action must declare whether it is read-only, reversible, quarantine-based, or destructive. Destructive actions are not enabled in the first release.

## Production boundaries

- The browser never receives API keys.
- The backend binds to localhost by default.
- The selected vault is never assumed from the current working directory.
- Existing engine scripts run only through explicit adapters with known inputs and outputs.
- Statistics and receipts are application data and should not be silently written into the selected vault.
- Canonization, publishing, and deletion require separate human authority and are outside automatic dashboard authority.
