# Execution Workflow

This repo still uses a static, file-based workflow. Execution state is recorded as generated JSON, not as frontend-owned mutable state.

## Source files

- `generated/task_backlog.json` is the canonical task list.
- `generated/collaboration_state.json` overlays ownership, execution status, notes, and proof references.
- `contracts/collaboration_state.schema.json` defines actors and task assignment state.
- `contracts/task_run.schema.json` defines one executor completion report.
- `generated/task_runs/<task_id>.json` may hold detailed proof for one task execution run.

## Basic loop

1. Pick one task from `generated/task_backlog.json`.
2. Add or update one `task_assignments` entry in `generated/collaboration_state.json`.
3. Give the task JSON to `prompts/07-task-executor.md`.
4. Save the returned report as `generated/task_runs/<task_id>.json` or another stable run file.
5. Add a short proof reference to the task assignment in `generated/collaboration_state.json`.
6. Review the proof before treating the task as done.

## Status meanings

- `unclaimed`: no active owner; normally derived when no assignment record exists.
- `claimed`: an actor has taken responsibility but has not started visible work.
- `in_progress`: active implementation or verification is underway.
- `review`: implementation/proof exists and needs review.
- `done`: accepted proof exists.
- `blocked`: work cannot safely continue without a decision, dependency, or missing context.
- `released`: previously claimed work was released back to the pool.

## Validation

Run:

```powershell
python tools\validate_collaboration_state.py
```

For generated task batches, build the canonical backlog after every batch validates:

```powershell
python tools\validate_task_batches.py
python tools\build_task_backlog_from_batches.py
```

## Frontend

Open `web/assignments.html` from the static viewer. It renders task ownership and proof from files only. It does not claim, edit, lock, or write state.
