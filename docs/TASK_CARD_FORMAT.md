# Task Card Format

A task card is the smallest useful planning unit in `task_backlog.json`.

It should be small enough for one person or agent to complete without owning the whole project, but large enough to produce a meaningful, reviewable change.

## Purpose

Task cards prevent vague planning output such as:

```text
Build the backend.
Build the frontend.
Add multiplayer.
```

Instead, every task should make ownership, boundaries, dependencies, and proof of completion explicit.

## Required task qualities

A good task is:

- **small** — one clear change, not an epic
- **owned** — assigned to one lane or role
- **bounded** — lists allowed repo area or files when possible
- **dependency-aware** — states what must exist first
- **verifiable** — includes concrete proof of done
- **parallel-safe** — avoids unnecessary file overlap with other tasks
- **traceable** — maps back to the accepted intake/project spec

## Recommended fields

Use fields that match the current task contract when generating machine-readable output. The planning text should still cover these concepts even if the schema names differ.

```json
{
  "id": "define-realtime-event-contract",
  "title": "Define shared realtime game event contract",
  "owner_role": "Protocol Agent",
  "lane": "shared-contract",
  "repo_target": "car-game-protocol",
  "depends_on": [],
  "allowed_areas": [
    "docs/",
    "shared/contracts/"
  ],
  "inputs": [
    "accepted project_intake.json",
    "repo_plan.json"
  ],
  "outputs": [
    "docs/network-events.md"
  ],
  "summary": "Define the minimal client/server events required for the first playable multiplayer game loop.",
  "acceptance_criteria": [
    "Room lifecycle events are listed.",
    "Guess submission and result events are listed.",
    "Timer/final-chance events are listed.",
    "Each event includes sender, payload, and expected receiver behavior."
  ],
  "verification": [
    "Contract document exists and is referenced by both client and backend tasks.",
    "No implementation task invents events outside the contract without updating it."
  ],
  "handoff_notes": "Backend and client tasks should start from this contract before implementation."
}
```

## Field guidance

### `id`

Use stable task IDs. Dependencies should reference IDs, not titles.

### `title`

Use an action-oriented title:

```text
Good: Define room lifecycle WebSocket events
Bad: WebSocket stuff
```

### `lane`

Use lanes that allow parallel work. Common lanes:

- `shared-contract`
- `client-ui`
- `backend-game-state`
- `tests-verification`
- `docs-devex`

### `repo_target` / `allowed_areas`

Make file ownership clear enough to avoid two people editing the same files unnecessarily.

### `depends_on`

Dependencies should be minimal. Too many dependencies serialize the whole project; too few create merge chaos.

### `acceptance_criteria`

Acceptance criteria must be observable. Avoid vague criteria like `works well`.

### `verification`

Verification should tell a reviewer how to prove the task is done:

- run a command
- inspect a file
- execute a manual flow
- check a contract reference
- run tests
- verify no forbidden files changed

## Task sizing

Prefer tasks that fit in one focused implementation session.

Split a task when:

- it touches unrelated repo areas
- it needs multiple people to coordinate
- it mixes contract design and implementation
- it mixes UI and backend behavior before a contract exists
- it cannot be verified with a clear proof step

Do not split a task when the pieces cannot be tested or reviewed independently.

## Parallel-work rule

For two or more workers, create shared contract tasks first, then split client/backend/core/test work around those contracts.

Example split:

```text
T-001 shared-contract: Define game event contract
T-002 backend-game-state: Implement room creation using T-001
T-003 client-ui: Implement room join UI using T-001
T-004 tests-verification: Add integration scenario for room join
```

This allows backend and client work to proceed in parallel without inventing incompatible APIs.
