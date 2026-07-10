# AI Assembly Line

## AI agent entrypoint — mandatory

When a user presents a rough product idea, **do not begin product design from this README**.

Before replying, read:

1. `AGENTS.md`
2. `docs/AI_START_HERE.md`
3. `prompts/08-project-workspace-initializer.md`
4. `prompts/00-intake-interviewer.md`

When repository state is not established, the first response must contain only:

- a short acknowledgement
- compact intake status
- one A/B/C question asking whether the project is greenfield, already has a product repository, or is planning-only

Then stop.

Do not invent a title, MVP, game loop, feature list, stack, architecture, repository layout, or tasks before the corresponding guided answers are accepted.

This first-turn rule takes precedence over all descriptive material below.

## What this repository is

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

This framework keeps reusable:

- schemas
- guided role prompts
- validators and builders
- repository bootstrap tooling
- the static read-only viewer
- lifecycle documentation

## Role routing

Use repository artifacts and PR state to choose the active role:

| State | Active role |
|---|---|
| Repository state unknown | Repository Bootstrap Agent |
| Repository ready, intake incomplete | Intake Interviewer |
| Requirements PR merged | Planning Agent |
| Planning PR merged | Task Splitter |
| Task backlog merged | Dispatch / Task Executor |
| Framework maintenance request | Normal repository engineering |
| Repository review request | Remote-review workflow |

See `docs/AI_START_HERE.md` for the mandatory response envelopes and lifecycle gates.

## Current scope

The framework supports:

- repository selection and readiness checks
- one-question guided requirements intake
- requirements/bootstrap PR handoff
- planning artifacts in a separate planning PR
- task batching and canonical backlog creation in a separate task-decomposition PR
- file-based collaboration state
- one-task Dispatch context
- static read-only project views

It does not yet provide:

- GitHub repository creation through an API
- authentication
- a hosted mutable dashboard
- databases or realtime synchronization
- autonomous task claiming
- background agent orchestration

## Greenfield workflow

### 1. Establish repository state

The first guided question is:

```text
A. Greenfield — this project needs a new product repository
B. Existing repository — a product repository already exists
C. Planning-only — continue intake without creating a repository yet
```

The agent must stop after this question on the first turn.

### 2. Verify the product repository

For repository-first execution, the product repository must have:

- an initial commit
- a default branch
- branch creation access
- pull-request access

When the connected agent cannot create repositories, it should provide exact repository settings and then verify the resulting URL.

### 3. Install the reusable kit

The agent should perform repository writes itself when possible. When local execution is necessary, it must provide one fully resolved shell-specific copy-paste block with no placeholders, following `prompts/08-project-workspace-initializer.md`.

The local installer is:

```text
tools/bootstrap_product_repository.py
```

It creates:

```text
product-repo/
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

In guided mode, the Intake Interviewer asks exactly one high-impact question per turn. It does not fill in the rest of the MVP automatically.

When blocking questions are answered, the requirements/bootstrap PR contains the accepted requirement state, including:

```text
assembly/intake/project_intake.json
assembly/requirements/REQUIREMENTS.md
assembly/context/handoff.md
```

See:

- `docs/GUIDED_REPOSITORY_BOOTSTRAP.md`
- `docs/PROJECT_INTAKE_WORKFLOW.md`
- `prompts/08-project-workspace-initializer.md`
- `prompts/00-intake-interviewer.md`

## Planning stage

After the requirements PR merges, start a fresh Planning Agent context from merged repository files.

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

See `prompts/00-planning-agent.md` and `docs/PLANNING_RUN_WORKFLOW.md`.

## Task-decomposition stage

After the planning PR merges, start a fresh Task Splitter context.

The task-decomposition PR produces:

```text
assembly/generated/task_batch_index.json
assembly/generated/task_batches/*.json
assembly/generated/task_backlog.json
assembly/generated/collaboration_state.json
```

See `prompts/06-task-splitter.md` and `docs/TASK_GENERATION_WORKFLOW.md`.

## Static viewer

The viewer is read-only and renders committed repository artifacts rather than inventing workflow state.

Serve a bootstrapped product repository from its root:

```powershell
python -m http.server 8000
```

Open:

```text
http://localhost:8000/assembly/web/
```

Pages that require later-stage artifacts remain incomplete until their owning PR is merged.

## Repository map

```text
AGENTS.md       mandatory repository-aware AI contract
docs/           lifecycle, routing, and role workflows
prompts/        guided agent role prompts
contracts/      machine-readable artifact contracts
tools/          validators, builders, and bootstrap tooling
web/            static read-only viewer
generated/      framework dogfooding state
planning_runs/  framework planning-run workspace
projects/       optional demos/monorepo registry mode
```

Central `projects/` registry mode is not the normal home for real products.

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

For explicit repository review, start with:

- `docs/AI_CONTEXT.md`
- `generated/review_manifest.json`

For a new product idea, start with `docs/AI_START_HERE.md` instead.