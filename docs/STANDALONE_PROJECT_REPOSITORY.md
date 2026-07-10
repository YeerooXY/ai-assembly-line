# Standalone Product Repository Mode

## Decision

Real product projects should normally keep their planning state, execution state, viewer snapshot, and implementation code in the product repository itself.

The AI Assembly Line repository is the reusable framework, not the storage location for every generated project.

## Recommended layout

```text
product-repository/
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
      task_backlog.json
      task_batch_index.json
      collaboration_state.json
      agent_prompts.json
      slots_db.json
      planning_runs_index.json

      task_batches/
      task_runs/

  src/
  tests/
```

Paths in `project_workspace.json` are relative to the repository root. For example:

```json
{
  "paths": {
    "generated": {
      "project_spec": "assembly/generated/project_spec.json",
      "repo_plan": "assembly/generated/repo_plan.json",
      "task_backlog": "assembly/generated/task_backlog.json",
      "task_batch_index": "assembly/generated/task_batch_index.json",
      "task_batches_dir": "assembly/generated/task_batches",
      "collaboration_state": "assembly/generated/collaboration_state.json",
      "agent_prompts": "assembly/generated/agent_prompts.json",
      "slots_db": "assembly/generated/slots_db.json",
      "planning_runs_index": "assembly/generated/planning_runs_index.json",
      "task_runs_dir": "assembly/generated/task_runs"
    }
  }
}
```

## Viewer resolution order

When no explicit project is requested, the viewer resolves state in this order:

1. Explicit `?workspace=<relative-json-path>`.
2. Explicit `?project=<project-id>` through `projects/index.json`.
3. Auto-detected standalone workspace:
   - `../../project_workspace.json`
   - `../project_workspace.json`
4. Default/first project from `projects/index.json`.
5. Root `generated/*.json` seed fallback.

An explicit project/workspace request fails clearly rather than silently switching to unrelated state.

## Serving a standalone repository

From the product repository root:

```powershell
python -m http.server 8000
```

For an `assembly/web/` viewer snapshot, open:

```text
http://localhost:8000/assembly/web/
```

The viewer stays static and read-only. Git/PR access remains the write boundary.

## Why not submodules as the default

A copied, versioned project kit works immediately after a normal clone. Submodules remain optional for unusual repository layouts, but should not be required for the planning UI.

A later sync tool should update the installed framework snapshot through a reviewable PR.
