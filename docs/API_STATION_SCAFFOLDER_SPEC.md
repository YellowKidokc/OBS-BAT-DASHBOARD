# API Station Scaffolder Specification

## Goal

Provide a batch launcher and dashboard action that creates a complete, reusable API-workflow folder. After setup, David should normally need to do only three things:

1. Put source material in `INBOX` or a selected call's `input` folder.
2. Fill out or select `prompt.md`.
3. Double-click `RUN.bat` or click Run in the dashboard.

The station handles request assembly, output naming, provenance, validation, cost records, and failure recovery.

## Launchers

Provide:

- `CREATE_API_STATION.bat`
- `CREATE_API_STATION.ps1`
- equivalent **New API Station** dashboard action

The batch launcher should call maintained Python code rather than duplicating scaffolding logic in batch syntax.

## Setup questions

The generator asks for:

- station name
- parent destination
- API provider
- default model
- single-file or batch default
- default prompt template
- expected output extension
- whether each input receives an independent request
- optional maximum concurrency

Show the proposed path and settings before creation. Never overwrite an existing station. If the name exists, stop or propose a distinct name.

## Generated layout

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

`BACKSIDE` contains machinery and operational records. `INBOX` and `OUTBOX` remain simple user-facing doors.

## Saved calls

Each named job lives under:

```text
BACKSIDE/calls/CALL_NAME/
  call.yaml
  prompt.md
  input/
  output/
  receipts/
```

The dashboard must support:

- create call from template
- duplicate call without copying secrets or previous outputs
- rename a call through a reviewed operation
- run one test item
- preview assembled prompt and attachments
- run pending items
- retry failed items
- skip outputs already completed for the same source hash and prompt version
- export a call package without credentials

## Configuration

`station.yaml` contains non-secret configuration:

```yaml
station_version: 1
station_id: generated-uuid
name: example
provider: openai
model: configurable-model-name
mode: one-request-per-input
max_concurrency: 1
input_extensions: [.md, .txt, .json, .csv]
output_extension: .md
prompt_files:
  - prompt.system.md
  - prompt.md
  - prompt.output-contract.md
draft_status: api-draft-review-required
```

Model names and pricing are configuration data, not permanent source-code constants.

## Credential handling

- Never write a real API key into the station.
- `.env.example` contains only variable names and instructions.
- Prefer `OPENAI_API_KEY` or the relevant provider environment variable.
- The runner checks credential presence without printing its value.
- Redact authorization headers and secrets from logs, errors, receipts, and browser responses.
- Exports and ZIP packages exclude `.env` and other local secret files.

## Run lifecycle

For every input item:

1. Calculate source SHA-256.
2. Record prompt-component hashes and resolved prompt version.
3. Validate configuration.
4. Estimate input size and warn about configured limits.
5. In dry-run mode, stop here and write a preview receipt.
6. Submit the request.
7. Save the raw provider response separately from the cleaned output.
8. Validate output against the configured contract.
9. Record model, tokens, latency, retry count, and provider request ID when available.
10. Calculate estimated cost using the versioned pricing table.
11. Write an immutable completion receipt.
12. Move or mark the input as processed only according to configured policy; never delete it.

Partial batch failure must not discard successful outputs or blindly repeat them.

## Output naming

Default output naming should retain the source stem and avoid collisions:

`SOURCE_STEM__CALL_NAME__YYYYMMDD-HHMMSS.ext`

Receipts connect source hash, prompt version, call configuration, raw response, and final output.

## Prompt editing

The dashboard provides editors for:

- default system contract
- main task prompt
- output contract
- per-call override

It must show the exact resolved prompt before execution. Prompt history is versioned and previous versions remain inspectable.

## Statistics

Each station reports:

- pending, completed, failed, and review-required items
- calls by provider/model
- input/output/cached/reasoning tokens when available
- estimated cost by run/day/month/all time
- average latency
- validation failures
- retries
- prompt version performance

## Generated-station acceptance test

Automated tests must create a temporary station and verify:

- exact folder structure
- no credential exists in generated files
- dry run sends no network request
- input and prompt hashes appear in the receipt
- an existing destination is not overwritten
- mocked success creates raw response, output, and receipt
- mocked failure preserves input and creates a failure record
- rerun does not duplicate a completed source/prompt combination
- paths with spaces work on Windows
- generated `RUN.bat` resolves its own directory correctly
