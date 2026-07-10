# Repository-Connected Agent PR Workflow

AI Assembly Line uses Git pull requests as the persistence and approval boundary between guided web-AI stages.

```text
chat is temporary
Git is durable
pull requests are reviewable
merged files are authoritative
```

## Why this exists

Requirements, planning, and task splitting may happen in different browser tabs or fresh AI conversations. No stage may require hidden chat memory from the previous stage.

Each role must reconstruct context from the selected product repository and persist its results on a branch.

## Shared role protocol

For repository-connected stages:

1. Identify the selected product repository and default branch.
2. Read `project_workspace.json`.
3. Verify the lifecycle prerequisites for the role.
4. Resolve all artifact paths from the workspace manifest.
5. Create or reuse one stage branch.
6. Write only stage-owned files.
7. Commit progress to that branch.
8. Run available validators.
9. Inspect the final diff.
10. Open one PR against the default branch.
11. Return the PR link, changed files, validation, blockers, and next lifecycle action.

## Branch conventions

Recommended branch names:

```text
ai/requirements-<project-id>
ai/planning-<run-id>
ai/task-split-<run-id>
ai/task-<task-id>
```

Branches may use another safe repository convention, but the stage and project/task identity should remain recognizable.

## Context recovery

A fresh AI conversation must be able to continue by reading:

- the default branch for merged source of truth
- the stage branch for in-progress output
- the workspace manifest for paths
- open PR metadata when available

For a large task split, the batch index and existing batch files on the branch replace conversational memory.

## Role-owned files

### Requirements role

Owns the accepted intake and requirements/bootstrap files. It must not create architecture or executable tasks prematurely.

### Planning role

Owns project specification, repo plan, role prompts, planned slots, and planning-run trace. In the normal flow it must not create final task batches or backlog.

### Task Splitter

Owns the task batch index, task batch files, canonical task backlog, and task-related coordination updates. It must not redesign the accepted architecture.

### Task Executor

Owns implementation changes for one selected task plus its task-run proof. It must not broaden scope into unrelated tasks.

## PR state

Opening a PR does not accept an artifact.

- branch files = proposed state
- open PR = reviewable proposed state
- merged PR = accepted repository state
- closed/unmerged PR = rejected or abandoned proposal

The read-only viewer should normally display merged state and may later show open PR proposals separately.

## Validation

Each stage should run the validators relevant to the paths it changed.

Planning normally runs:

```powershell
python assembly\tools\validate_planning_run.py assembly\planning_runs\<run-id>
```

Task splitting normally runs:

```powershell
python assembly\tools\validate_task_batches.py
python assembly\tools\build_task_backlog_from_batches.py
python assembly\tools\validate_task_batches.py
python assembly\tools\validate_collaboration_state.py
```

Exact command prefixes depend on the workspace layout. Resolve them from `project_workspace.json` and the installed tools path.

## No-write fallback

When repository write access is unavailable, the agent may return complete files with exact repository-root-relative paths and proposed PR metadata.

This fallback must not ask the human to invent paths, merge partial JSON manually, or reconstruct missing context from memory.
