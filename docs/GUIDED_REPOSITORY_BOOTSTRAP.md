# Guided Repository Bootstrap

This workflow is the first durable stage for a greenfield product.

```text
idea
  -> create or select repository
  -> verify repository readiness
  -> create bootstrap branch
  -> install reusable project kit
  -> guided intake
  -> requirements/bootstrap pull request
  -> human review and merge
```

The product repository owns its accepted requirements, planning state, task state, execution proof, and implementation. The `ai-assembly-line` repository remains the reusable framework.

## Core boundary

```text
chat is temporary
Git is durable
pull requests are the approval boundary
merged files are authoritative
```

The web agent should guide the user. The human should not have to invent folders, move JSON files, or decide which repository owns generated state.

## Repository creation

For a greenfield project, collect and confirm:

- repository owner
- repository name
- visibility
- default branch
- whether an initial README commit exists

When repository-creation tooling is available, create the repository with the accepted settings.

When it is unavailable, give the user the exact repository settings to use, then verify the resulting repository URL. Do not continue to PR creation while the repository is empty or lacks a default branch.

## Readiness checks

The repository must:

- exist
- be accessible to the agent
- contain at least one commit
- have a known default branch
- allow branch creation
- allow pull-request creation

Track the guided state using `contracts/repository_bootstrap.schema.json`.

An explicit repository URL has priority over guesses based on names. Never claim a repository is ready without reading repository metadata.

## Bootstrap branch

Use a dedicated branch, for example:

```text
assembly/bootstrap-<project-id>
```

Do not write project bootstrap files directly to the default branch when pull requests are available.

The branch should install:

```text
project_workspace.json

assembly/
  kit_manifest.json

  intake/
  requirements/
  planning_runs/

  generated/
    task_batches/
    task_runs/

  context/
  prompts/
  contracts/
  tools/
  web/
```

The bootstrap stage may create directories and reusable framework files before intake is complete. It must not create fake accepted planning artifacts merely to make every viewer page green.

In particular, do not create placeholder versions of:

- `project_spec.json`
- `repo_plan.json`
- `task_backlog.json`
- task batch files
- final agent prompts
- final slots

Those files appear only in their owning lifecycle stages.

## Local deterministic installer

From an `ai-assembly-line` checkout, install the reusable kit into an initialized product repository clone:

```powershell
git -C ..\my-product checkout -b assembly/bootstrap-my-product

python tools\bootstrap_product_repository.py `
  --target ..\my-product `
  --project-id my-product `
  --name "My Product" `
  --repository-full-name owner/my-product `
  --visibility private
```

The installer:

- verifies that the target is an initialized Git work tree
- verifies that the declared default branch exists
- copies a curated reusable viewer/contracts/prompts/tools kit
- creates `project_workspace.json`
- creates `assembly/kit_manifest.json`
- creates requirements and handoff drafts
- refuses silent overwrites
- does not commit, push, or open a PR

Verify an existing installation:

```powershell
python tools\bootstrap_product_repository.py `
  --target ..\my-product `
  --project-id my-product `
  --name "My Product" `
  --repository-full-name owner/my-product `
  --check
```

## Web-agent behavior

With repository write access, the web agent should produce the same file set directly on the bootstrap branch.

The agent should:

1. verify repository metadata
2. create or reuse the bootstrap branch
3. install the reusable kit
4. run guided intake one decision at a time
5. write accepted `project_intake.json`
6. replace the requirements draft with accepted requirements
7. update the handoff
8. validate the changed JSON
9. open the requirements/bootstrap PR

For long intake conversations, the agent may persist a draft `intake_session.json` on the bootstrap branch. The accepted `project_intake.json` remains the input to planning.

## Requirements/bootstrap PR

Typical accepted files:

```text
project_workspace.json
assembly/kit_manifest.json
assembly/intake/project_intake.json
assembly/requirements/REQUIREMENTS.md
assembly/context/handoff.md
assembly/context/repository-notes.md
assembly/context/local-setup.md
assembly/web/...
assembly/contracts/...
assembly/prompts/...
assembly/tools/...
```

The PR description should summarize:

- accepted project goal
- MVP boundary
- target users and platforms
- stack decision or constraints
- safety boundaries and non-goals
- working style and proof expectations
- unresolved non-blocking questions
- next lifecycle step

## Hard stop before PR

Do not open the requirements PR while:

- repository readiness checks fail
- blocking intake questions remain
- `project_intake.json` is not schema-valid
- requirements contradict the accepted intake
- the branch contains architecture, task backlog, or implementation work

## After merge

Start a fresh Planning Agent context from merged files:

```text
project_workspace.json
assembly/intake/project_intake.json
assembly/requirements/REQUIREMENTS.md
assembly/context/handoff.md
repository implementation files, if any
```

The Planning Agent creates the planning PR. After that merges, the Task Splitter creates the task-decomposition PR. Dispatch becomes useful when the task backlog and collaboration state are merged.

## Kit ownership and upgrades

`assembly/kit_manifest.json` separates framework-managed paths from project-owned paths.

Framework-managed:

```text
assembly/web
assembly/contracts
assembly/prompts
assembly/tools
```

Project-owned:

```text
project_workspace.json
assembly/intake
assembly/requirements
assembly/planning_runs
assembly/generated
assembly/context
```

A later kit upgrade may replace framework-managed files in a dedicated PR. It must never overwrite accepted project requirements, plans, tasks, collaboration state, or proof automatically.
