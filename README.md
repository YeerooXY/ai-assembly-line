# AI Assembly Line

`ai-assembly-line` is a human-in-the-loop framework for turning a software idea into reviewable requirements, a structured plan, parallel-safe tasks, and one-task execution context.

It is the **factory**, not the permanent home of every project.

```text
idea
  -> product repository
  -> requirements/bootstrap PR
  -> planning PR
  -> task-decomposition PR
  -> read-only project view + Dispatch
  -> implementation PRs
```

## Core rule

```text
chat is temporary
Git is durable
pull requests are the approval boundary
merged files are authoritative
```

A real product keeps its accepted requirements, plans, tasks, execution state, proof, and implementation in its own repository.

This repository keeps reusable:

- schemas
- guided prompts
- validators and builders
- the static read-only viewer
- repository bootstrap tooling
- workflow documentation

## Current scope

The framework currently supports:

- guided repository selection/readiness
- guided requirements intake
- planning artifacts
- task batching and canonical backlog creation
- file-based collaboration state
- one-task Dispatch context
- static read-only project views
- repository-first PR handoffs

It does not yet provide:

- GitHub repository creation through an API
- authentication
- a hosted mutable dashboard
- databases or realtime synchronization
- autonomous task claiming
- background agent orchestration

## Greenfield start

### 1. Create or select the product repository

The repository must have:

- an initial commit
- a default branch
- branch creation access
- pull-request access

When the connected agent cannot create repositories, it should guide the user through the exact owner/name/visibility settings and verify the resulting URL.

### 2. Create a bootstrap branch

Example:

```powershell
git -C ..\my-product checkout -b assembly/bootstrap-my-product
```

### 3. Install the reusable kit

From this repository:

```powershell
python tools\bootstrap_product_repository.py `
  --target ..\my-product `
  --project-id my-product `
  --name "My Product" `
  --repository-full-name owner/my-product `
  --visibility private
```

This installs a curated kit under:

```text
my-product/
  project_workspace.json
  assembly/
    kit_manifest.json
    intake/
    requirements/
    planning_runs/
    generated/
    context/
    prompts/
    contracts/
    tools/
    web/
```

It does not create fake accepted plans or tasks.

### 4. Complete guided intake

The Repository Bootstrap Agent and Intake Interviewer produce:

```text
assembly/intake/project_intake.json
assembly/requirements/REQUIREMENTS.md
assembly/context/handoff.md
```

Then they open the requirements/bootstrap PR.

See:

- `docs/GUIDED_REPOSITORY_BOOTSTRAP.md`
- `prompts/08-project-workspace-initializer.md`
- `contracts/repository_bootstrap.schema.json`
- `contracts/project_intake.schema.json`

## Planning stage

After the requirements PR merges, start a fresh Planning Agent context from repository files.

The planning PR produces:

```text
assembly/generated/project_spec.json
assembly/generated/repo_plan.json
assembly/generated/agent_prompts.json
assembly/generated/slots_db.json
assembly/generated/planning_runs_index.json
assembly/planning_runs/<run-id>/
```

It deliberately does not produce the final task backlog.

See:

- `prompts/00-planning-agent.md`
- `docs/PLANNING_RUN_WORKFLOW.md`
- `tools/init_planning_run.py`
- `tools/validate_planning_run.py`

## Task-decomposition stage

After the planning PR merges, start a fresh Task Splitter context.

The task-decomposition PR produces:

```text
assembly/generated/task_batch_index.json
assembly/generated/task_batches/*.json
assembly/generated/task_backlog.json
assembly/generated/collaboration_state.json
```

See:

- `prompts/06-task-splitter.md`
- `docs/TASK_GENERATION_WORKFLOW.md`
- `tools/validate_task_batches.py`
- `tools/build_task_backlog_from_batches.py`

## Static viewer

The viewer is read-only and renders repository artifacts rather than inventing workflow state.

For this framework repository:

```powershell
python -m http.server 8000
```

Open:

```text
http://localhost:8000/web/
```

For a bootstrapped product repository:

```powershell
python -m http.server 8000
```

Open:

```text
http://localhost:8000/assembly/web/
```

Useful pages include:

- Overview
- Repository Plan
- Planning Runs
- Task Batches
- Backlog
- Dispatch
- Assignments
- Verification

Pages that require later-stage artifacts will remain incomplete until the corresponding PR is merged.

## Repository map

```text
contracts/       machine-readable artifact contracts
docs/            lifecycle and role workflows
prompts/         guided agent role prompts
tools/           validators, builders, and bootstrap tooling
web/             static read-only viewer
generated/       framework dogfooding state
planning_runs/   framework planning-run workspace
projects/        optional registry mode for demos/monorepos only
```

Central `projects/` registry mode remains available for framework development, demos, and monorepos. It is not the normal home for real products.

## Validation

Run:

```powershell
python tools\validate_seed.py
python tools\validate_task_batches.py
python tools\validate_collaboration_state.py
python tools\validate_project_workspaces.py
python tools\build_planning_runs_index.py
node --check web\*.js
git diff --check
```

For a bootstrapped product repository, use the copied tools under `assembly/tools/`.

## Remote review

Start with:

- `docs/AI_CONTEXT.md`
- `docs/EXTERNAL_REVIEW_PROMPT.md`
- `generated/review_manifest.json`

The review manifest is intentionally curated. It lists the workflow-defining files rather than every source file and no longer includes domain-specific demonstration projects.
