# Viewer Page Roles

The static viewer has overlapping pages on purpose, but each page has a different job.

## Primary workflow page

### Dispatch

`web/dispatch.html` is the primary "what can I do next?" page.

Use it to:

- see tasks grouped by topological dependency wave
- find green/available tasks whose dependencies are done
- avoid locked, blocked, waiting, and done tasks
- open one task's detail panel
- copy the full one-task execution context into a fresh AI chat
- copy raw task JSON when needed

Dispatch does not claim, lock, edit, or write task state. It only renders source-of-truth files and produces copyable context.

## Audit/status page

### Assignments

`web/assignments.html` is the audit and status page for file-based collaboration state.

Use it to:

- inspect actors
- inspect assignment records
- inspect proof references
- preview/copy/download replacement `generated/collaboration_state.json` through the static helper

Assignments remains file-based. It does not write directly to the repo.

## Generation/validation page

### Task Batches

`web/task-batches.html` is the generation and validation page for batch-created task files.

Use it to:

- inspect `generated/task_batch_index.json`
- inspect generated batch file readiness
- validate dependency graph shape before merging task batches into the canonical backlog

Once batches are accepted and merged into `generated/task_backlog.json`, Dispatch becomes the primary page for picking the next task.
