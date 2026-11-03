# Windows Desktop Bridge Specification

## Primary outcome

David should experience the Synology API as a desktop assistant, not as a server he must repeatedly visit and inspect.

The Windows desktop bridge remains connected to the Synology and provides:

- system-tray status
- native Windows notifications
- approval requests
- job progress and completion alerts
- vault-health and emergency alerts
- API cost warnings
- drag/drop submission
- context-folder submission
- quick actions
- one-click opening of the relevant dashboard page

## Architecture

```text
Windows tray client
    | HTTPS + authenticated WebSocket/SSE
    v
Synology FastAPI service
    |
    +-- jobs
    +-- approvals
    +-- notifications
    +-- health findings
    +-- AI/tool routing
```

Use HTTPS requests for commands and an authenticated WebSocket for bidirectional real-time events when practical. Server-Sent Events plus normal HTTPS requests is an acceptable simpler fallback. Do not use unauthenticated LAN broadcast messages.

## Desktop application

Preferred implementation:

- Python or .NET Windows tray application
- signed installer when release maturity permits
- starts with Windows only after David opts in
- single-instance behavior
- local encrypted/protected credential storage
- no API key embedded in source or configuration committed to Git
- automatic reconnect with bounded backoff
- visible offline/degraded state

The desktop client does not need to contain the whole dashboard. It is a bridge, notification center, launcher, and quick-action interface. Detailed work opens the local HTML dashboard.

## Tray menu

Suggested menu:

- Synology status
- Open dashboard
- Submit file
- Submit folder
- New prompt/API call
- Recent jobs
- Pending approvals
- Vault quick health check
- Emergency health check
- Pause notifications
- Settings
- Exit

## Desktop notifications

Support event types:

- job accepted
- job progress milestone
- approval required
- job complete
- job failed
- API budget threshold reached
- NAS/API offline
- NAS/API restored
- critical vault-health finding
- sync-conflict spike
- oversized file detected
- backup overdue or failed

Notifications should include concise context and safe buttons such as:

- Open
- Approve preview
- Reject
- Retry
- View receipt

High-risk approvals must open the full preview rather than approve directly from a toast.

## Submitting work

David should be able to:

- drag a file onto the tray/client window
- choose a folder
- right-click a file/folder and choose a registered action when shell integration is enabled
- launch `AAA_MENU.bat` from the working folder
- type or paste a prompt
- choose a saved API station/call

The desktop client uploads files only when necessary. For paths on a shared NAS mount, it may submit a validated NAS-relative reference instead. The server must reject arbitrary client-supplied filesystem paths outside approved roots.

Before upload show file count, bytes, destination station, and privacy/provider route.

## Authentication and pairing

Provide an explicit pairing flow:

1. Administrator creates a short-lived pairing code from the dashboard.
2. Desktop client enters/scans the code.
3. Server issues a revocable device credential with limited scopes.
4. Desktop stores it using Windows-protected credential storage.
5. Dashboard lists paired devices, last seen, scopes, and revocation control.

Do not reuse the OpenAI provider key as a desktop authentication token.

Recommended scopes include:

- read status
- submit jobs
- upload inputs
- view own jobs
- receive notifications
- request approvals
- approve low-risk previews
- administer devices

## Real-time event contract

Every event should contain:

- event ID
- event type
- timestamp
- job/finding/approval ID
- severity
- short title
- short message
- allowed user actions
- dashboard deep link
- schema version

Clients acknowledge received events. Important missed events remain in the server inbox and appear after reconnect.

## Offline behavior

- Queue optional local submissions only with David's permission.
- Clearly label queued versus sent work.
- Never duplicate a job after reconnect; use idempotency keys.
- Cache only minimal metadata.
- Do not cache sensitive vault contents by default.
- Display last successful contact and server health.

## Statistics shown on desktop

Compact view:

- NAS online/offline
- active jobs
- pending approvals
- latest critical health count
- API spending today/month
- last backup
- last completed job

Detailed statistics remain in the web dashboard.

## Installation and updates

Provide:

- `INSTALL_DESKTOP_BRIDGE.bat` or standard installer
- Start Menu entry
- optional startup registration
- repair option
- clean uninstall
- update check compatible with the selected distribution method

Uninstall removes local credentials and app state only after confirmation. It must not remove Synology jobs, receipts, or vault data.

## Acceptance tests

1. Pair a clean Windows client with the Synology.
2. Restart the desktop and confirm automatic reconnect.
3. Restart the Synology service and confirm offline/restored notifications.
4. Submit a file and receive accepted, progress, and completion events.
5. Receive an approval request, open the exact preview, approve, and receive the receipt.
6. Reject an approval and prove no mutation occurred.
7. Disconnect during a job and receive missed completion after reconnect.
8. Repeated reconnect does not duplicate the job.
9. Revoke the device and prove further requests fail.
10. Verify secrets and provider keys never appear in desktop logs or traffic payloads.
