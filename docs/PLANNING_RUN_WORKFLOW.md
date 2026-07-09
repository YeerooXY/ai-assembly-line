# Planning Run Workflow

This repository supports a repeatable manual planning-run workflow for turning a rough software idea into structured planning artifacts.

## Workflow

1. Create a planning run folder:

   ```powershell
   python tools\init_planning_run.py <run-slug>
   ```

2. Open `planning_runs/<run-slug>/input-idea.md` and write or paste the rough idea.
3. Run the initializer again to refresh `planning_runs/<run-slug>/planning-run.md` with the current idea embedded in the prompt:

   ```powershell
   python tools\init_planning_run.py <run-slug>
   ```

4. Copy the generated prompt from `planning_runs/<run-slug>/planning-run.md`.
5. Paste that prompt into a web AI or Codex-style tool.
6. Save the returned planning artifacts into `planning_runs/<run-slug>/outputs/`.
7. Validate the saved outputs:

   ```powershell
   python tools\validate_planning_run.py planning_runs\<run-slug>
   ```

8. Review the artifacts and mark them accepted or rejected in `planning_runs/<run-slug>/review-notes.md`.

## Human-In-The-Loop Rules

- Generated outputs are drafts until a human accepts them.
- Unsafe automation-oriented ideas must be safely reinterpreted into the nearest safe planning-only scope or explicitly rejected.
- This workflow does not call AI APIs, run autonomous agents, or implement the planned software.
- The workflow is file-based and intended for manual review and acceptance.

## Required Planning Artifacts

Every planning run must produce the same artifact types:

- `project_spec.json`
- `repo_plan.json`
- `task_backlog.json`
- `agent_prompts.json`
- `slots_db.json`

## Expected Run Folder Layout

```text
planning_runs/<run-slug>/
  input-idea.md
  planning-run.md
  review-notes.md
  outputs/
    project_spec.json
    repo_plan.json
    task_backlog.json
    agent_prompts.json
    slots_db.json
```

## Review Outcome

Reviewers should confirm:

- the rough idea was interpreted safely
- the artifact set is structurally valid
- repo targets and task dependencies are coherent
- prompts and slots align with the proposed repo split
- the plan is useful enough to accept, revise, or reject
