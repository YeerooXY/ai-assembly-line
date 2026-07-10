# Project Workspaces

The AI Assembly Line supports two project-storage models.

## Recommended: standalone product repository

Real products should normally keep their own plan and execution state beside their implementation code.

Example:

```text
snake--game/
  project_workspace.json

  assembly/
    web/
    contracts/
    prompts/
    tools/

    intake/
    planning_runs/
    context/

    generated/
      project_spec.json
      repo_plan.json
      task_batch_index.json
      task_backlog.json
      collaboration_state.json
      agent_prompts.json
      slots_db.json
      planning_runs_index.json

      task_batches/
      task_runs/

  src/
  tests/
  assets/
```

The product repository becomes self-contained:

```text
idea
  -> guided intake
  -> accepted project files
  -> task splitting
  -> Dispatch
  -> implementation changes
  -> task-run proof
```

The AI Assembly Line repository remains the reusable factory: schemas, prompts, viewer source, validators, templates, and export/sync tools.

## Optional: central registry mode

`projects/` remains available for:

- seed/demo workspaces
- monorepos
- local multi-project dashboards
- framework development and testing

The registry lives at:

```text
projects/index.json
```

A registry workspace looks like:

```text
projects/<project-id>/
  project_workspace.json
  intake/
  planning_runs/
  generated/
  context/
  prompts/
  repos/
```

Use:

```powershell
python tools\init_project_workspace.py snake-game --name "Snake Game"
```

only when a central registry workspace is actually desired.

Do not use the central registry as the default home for every real product. Future guided export tooling should install a versioned `assembly/` kit into the product repository instead.

## Core rule

```text
humans describe intent
AI creates structured workspace files
validators verify them
the static UI loads them
Dispatch launches one task at a time
```

Users should not be asked to manually invent paths or move JSON files around.
