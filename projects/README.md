# Project Workspaces

`projects/` is the future home for user project workspaces.

The rule is simple:

```text
humans describe intent
AI creates structured workspace files
validators verify them
the static UI loads them
Dispatch launches one task at a time
```

Do not ask users to hand-place random JSON files in root `generated/`.

## Registry

The project registry lives at:

```text
projects/index.json
```

It lists available workspaces by project id and points at each workspace manifest.

## Workspace shape

A project workspace should look like this:

```text
projects/<project-id>/
  project_workspace.json
  README.md

  intake/
    intake_session.json
    project_intake.json

  planning_runs/

  generated/
    project_spec.json
    repo_plan.json
    task_batch_index.json
    task_backlog.json
    collaboration_state.json
    agent_prompts.json
    slots_db.json

    task_batches/
    task_runs/

  context/
    handoff.md
    repo-notes.md
    local-setup.md

  prompts/

  repos/
    <optional implementation repo or submodule>
```

## Guided creation

Use the initializer instead of creating folders by hand:

```powershell
python tools\init_project_workspace.py snake-game --name "Snake Game"
```

That creates the project workspace skeleton and updates `projects/index.json`.

Later UI work should load `projects/index.json`, let the user choose a project, then load that project's `project_workspace.json` and generated files.
