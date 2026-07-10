# Repository-First Project Lifecycle

The normal AI Assembly Line workflow starts with a product repository, not with a project folder inside the framework repository.

`ai-assembly-line` is the reusable workflow kit. A product repository owns its accepted requirements, planning artifacts, task state, implementation, and proof.

## Core rule

```text
chat is temporary
Git is durable
pull requests are the approval boundary
merged files are the source of truth
```

A fresh web-AI conversation must be able to resume from repository files without relying on earlier chat history.

## Lifecycle

```text
rough idea
  -> create or select repository
  -> initialize default branch
  -> guided requirements
  -> requirements/bootstrap PR
  -> merge
  -> planning
  -> planning PR
  -> merge
  -> task splitting
  -> task-split PR
  -> merge
  -> read-only dashboard and Dispatch
  -> implementation PRs
  -> task-run proof and review
```

Repository creation is not a pull request. A greenfield repository must first exist and have an initialized default branch, usually through a README or equivalent first commit. After that, every durable workflow change should normally arrive through a PR.

## Repository readiness gate

Planning must not begin until the selected repository is ready.

The repository gate is open when all of these are true:

- the repository exists
- the user or connected agent can read it
- the default branch exists and has at least one commit
- branches can be created
- pull requests can be opened
- the repository owner/name and default branch are known

When the connected tool cannot create a repository, the AI should prepare the exact repository name, owner, visibility, and initialization choices, ask the user to create it, then verify the returned repository URL before continuing.

## Durable project layout

Recommended product-repository layout:

```text
product-repository/
  project_workspace.json
  README.md
  src/
  tests/

  assembly/
    intake/
      project_intake.json

    requirements/
      REQUIREMENTS.md

    planning_runs/

    generated/
      project_spec.json
      repo_plan.json
      agent_prompts.json
      slots_db.json
      task_batch_index.json
      task_backlog.json
      collaboration_state.json
      planning_runs_index.json
      task_batches/
      task_runs/

    context/
      handoff.md
      repository-notes.md

    prompts/
    contracts/
    tools/
    web/
```

The framework repository should not gain a new `projects/<id>/` folder whenever somebody starts a real product. Central registry mode remains useful for demos, monorepos, local dashboards, and framework tests, but it is not the default greenfield flow.

## Reviewable setup PRs

A normal greenfield project has three planning-stage PRs before implementation work begins.

### PR 1: bootstrap and requirements

Creates the project workspace and persists accepted intake.

Typical files:

```text
project_workspace.json
assembly/intake/project_intake.json
assembly/requirements/REQUIREMENTS.md
assembly/context/handoff.md
assembly/generated/collaboration_state.json
```

This PR must not invent a task backlog.

### PR 2: planning package

Adds the accepted product and repository design.

Typical files:

```text
assembly/generated/project_spec.json
assembly/generated/repo_plan.json
assembly/generated/agent_prompts.json
assembly/generated/slots_db.json
assembly/generated/planning_runs_index.json
assembly/planning_runs/<run-id>/...
```

The final task backlog is intentionally excluded so a large plan can be split in a fresh context.

### PR 3: task decomposition

Adds validated executable work.

Typical files:

```text
assembly/generated/task_batch_index.json
assembly/generated/task_batches/*.json
assembly/generated/task_backlog.json
assembly/generated/collaboration_state.json
```

After this PR is merged, Dispatch can become active.

Small projects may combine planning and task decomposition, but the guided default keeps them separate.

## Artifact-derived phase gates

The dashboard should derive project state from merged artifacts and open PRs.

| Gate | Evidence | Unlocks |
|---|---|---|
| Repository ready | accessible initialized repository and default branch | requirements intake |
| Requirements accepted | merged `project_intake.json` and requirements document | planning |
| Planning accepted | merged `project_spec.json` and `repo_plan.json` | task splitting |
| Task split accepted | merged batch index, task batches, canonical backlog, collaboration state | Dispatch |
| Dispatch ready | valid backlog and collaboration state | task execution |

An open PR places the corresponding phase in `review`. Missing or invalid prerequisite artifacts block the next phase.

`contracts/project_lifecycle.schema.json` defines a normalized derived snapshot for UI and tooling. It is not intended to become a second manually maintained source of truth.

## Web UI responsibility

The web UI is primarily read-only. It should:

- identify the selected repository
- show repository readiness
- display the current lifecycle phase and blockers
- render merged requirements, specs, repository plans, task batches, and execution state
- show relevant open planning PRs
- offer guided actions such as Continue Requirements, Start Planning, Split Tasks, or Open Dispatch

Persistent changes are made by an AI workflow on a branch and reviewed through a PR. The browser should not silently invent or persist canonical planning state.

## Context handoff rule

Each stage must be restartable in a fresh chat.

- Requirements reads repository metadata and any saved intake state.
- Planning reads merged requirements and repository contents.
- Task splitting reads the merged planning package.
- Dispatch reads the merged canonical backlog and collaboration state.
- Executors read exactly one task plus dependency and repository context.

The repository is the handoff mechanism between tabs and agents.

## Compatibility modes

The viewer continues to support:

- standalone product-repository mode
- central `projects/index.json` registry mode
- root generated-state seed/demo mode

Only standalone repository-first mode is the recommended default for a real greenfield product.
