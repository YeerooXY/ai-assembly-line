# Live Decisions

Status: draft recovery log. Final acceptance occurs through the requirements/bootstrap pull request.

## Persistence status

- Active branch: `<bootstrap-or-intake-branch>`
- Last persisted decision: none
- Unsaved accepted decisions: 0

## Decision log

Add one entry immediately after each accepted answer and commit it before asking the next question.

### D-001 — <topic>

- Status: accepted
- Choice: <A/B/C/recommended/hybrid/custom>
- Accepted requirement: <concise statement>
- User-supplied constraints: <only material constraints; use `none` when absent>
- Supersedes: none
- Source: guided intake

## Revision rules

- Never rewrite history silently.
- When a decision changes, mark the old entry `superseded` and add a new entry.
- Do not record unchosen options as requirements.
- Mark reconstructed decisions `unverified` until the user confirms them.
- Keep this file human-readable; keep structured session state in `intake_session.json`.
