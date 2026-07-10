# AI Assembly Line

`ai-assembly-line` is the seed repository for a human-in-the-loop multi-agent software assembly line.

Its first job is not autonomous execution. Its first job is project decomposition and static, file-based coordination:

- rough idea -> guided project intake
- guided project intake -> structured project specification
- structured project specification -> repo split
- repo split -> microtask backlog
- microtask backlog -> role-specific prompt pack
- planning artifacts -> verification rules
- task backlog + collaboration state -> dispatchable one-task execution context

## Phase 0 Goal

Build the planning kernel and the first "spec compiler":

`rough idea -> safe, structured project specification`

This repository is intentionally limited to intake, planning, contracts, prompts, file-based execution coordination, and read-only presentation scaffolding.

It does not include:

- authentication
- databases
- realtime sync
- live dashboards
- background agent orchestration
- autonomous task claiming

## Source of Truth

The system works from strict files, not inferred structure.

The source-of-truth layers are:

1. Product spec
   - human-readable: `PROJECT_SPEC.md`
   - reusable template: `PROJECT_SPEC_TEMPLATE.md`
   - machine-readable: `generated/project_spec.json`
2. Intake and data schemas
   - `contracts/project_intake.schema.json`
   - `contracts/*.schema.json`
3. API contract
   - `contracts/api_contract.openapi.yaml`
4. Canonical generated planning state
   - `generated/repo_plan.json`
   - `generated/task_backlog.json`
   - `generated/task_batch_index.json`
   - `generated/task_batches/*.json`
   - `generated/agent_prompts.json`
   - `generated/slots_db.json`
5. File-based execution coordination state
   - `generated/collaboration_state.json`
   - `generated/task_runs/*.json`
6. Derived planning-run index
   - `generated/planning_runs_index.json`

## Frontend Rule

Any frontend built from this repository must render the current product spec and contract-defined generated artifacts.

It must not invent:

- intake structure
- task structure
- repo structure
- prompt structure
- slot structure
- contract structure
- hidden workflow state

The future frontend is allowed to consume only source-of-truth material from:

- `PROJECT_SPEC.md`
- `generated/*.json`
- `contracts/*.schema.json`
- `contracts/api_contract.openapi.yaml`
- `docs/*.md`
- `prompts/*.md`

Rule: the frontend must render generated state and must not invent intake, task, repo, prompt, slot, execution, or contract structure.

## Read-Only Viewer

The first frontend lives in `web/` as a static multi-page read-only viewer.

Open it in one of two ways:

```powershell
python -m http.server 8000
```

Then visit `http://localhost:8000/web/`.

Or open any page in `web/` directly and use the page's file loader to select the required generated JSON files for that page.

The viewer pages are:

- `web/index.html`
- `web/repos.html`
- `web/backlog.html`
- `web/dispatch.html`
- `web/assignments.html`
- `web/task-batches.html`
- `web/prompts.html`
- `web/slots.html`
- `web/planning-runs.html`
- `web/verification.html`

Page roles:

- Dispatch is the primary "what can I do next?" page for selecting available tasks and copying one-task execution context.
- Assignments is the audit/status page for collaboration state, actors, assignment records, and proof references.
- Task Batches is the generation/validation page for batch-created tasks before they are merged into the canonical backlog.

See `docs/VIEWER_PAGE_ROLES.md` for the detailed page split.

The generated sources remain:

- `generated/project_spec.json`
- `generated/repo_plan.json`
- `generated/task_backlog.json`
- `generated/task_batch_index.json`
- `generated/task_batches/*.json`
- `generated/collaboration_state.json`
- `generated/task_runs/*.json`
- `generated/agent_prompts.json`
- `generated/slots_db.json`
- `generated/planning_runs_index.json`

The viewer displays:

- project overview
- repository split and repo ownership
- task backlog grouped by repo target
- task dispatch grouped by topological dependency wave, availability, and execution status
- assignment/audit state for actors, task ownership, notes, and proof references
- task batch files, copy-paste workflow readiness, task nodes, and dependency graph checks
- agent prompts
- slot board
- planning-run scaffold and output completeness
- verification rules, source-of-truth notes, proof requirements, and raw contract files

The viewer intentionally does not do the following yet:

- editing
- backend APIs
- authentication
- realtime sync
- mutable workflow state
- direct task claiming or locking
- frontend-owned intake, task, repo, prompt, slot, planning-run, execution, or contract models

## Initial Public Surface

The first public-facing web output should be read-only and contract-driven.

It should display:

- project name
- product goal
- repo split
- agent roles
- task backlog
- dispatchable available-task view
- assignment/proof status
- contract files
- prompt pack
- task batch index and generated batch files
- planning-run index
- verification rules

## Repository Map

- `PROJECT_SPEC.md`: current repo-level phase-0 specification
- `PROJECT_SPEC_TEMPLATE.md`: reusable template for future planning runs
- `PRODUCT_RULES.md`: hard rules and safety boundaries
- `docs/`: public overview, workflow, intake workflow, roles, task format, verification rules
- `docs/PROJECT_INTAKE_WORKFLOW.md`: interactive intake workflow for turning rough ideas into structured intake records
- `docs/EXTERNAL_REVIEW_PROMPT.md`: fresh-clone external reviewer prompt
- `docs/EXECUTION_WORKFLOW.md`: static file-based task assignment, execution, proof, and review workflow
- `docs/PLANNING_RUN_WORKFLOW.md`: manual planning-run workflow
- `docs/TASK_CREATION_GUIDE.md`: generic schema-aligned guide for creating implementation-ready task records
- `docs/TASK_GENERATION_WORKFLOW.md`: workflow for splitting accepted plans into task batches
- `docs/VIEWER_PAGE_ROLES.md`: role split for Dispatch, Assignments, and Task Batches viewer pages
- `contracts/`: schemas and OpenAPI contract
- `contracts/project_intake.schema.json`: schema for guided project intake records
- `contracts/collaboration_state.schema.json`: schema for file-based actors, task assignment state, proof references, and audit events
- `contracts/task_run.schema.json`: schema for one executor completion/proof report
- `contracts/task_batch_index.schema.json` and `contracts/task_batch.schema.json`: schemas for copy-paste task generation batches
- `generated/`: canonical machine-readable planning and execution coordination artifacts for the current seed state
- `generated/collaboration_state.json`: file-based execution ownership, status, notes, and proof overlay for the canonical backlog
- `generated/task_runs/`: optional detailed per-task executor proof reports
- `generated/planning_runs_index.json`: derived index of manual planning-run folders and output completeness
- `examples/coc-base-builder/`: example decomposition for a safe base layout planner
- `planning_runs/`: manual planning-run folders and review artifacts
- `prompts/`: copy-paste role prompts and task-splitting prompts, including the intake interviewer
- `tools/validate_seed.py`: repository JSON validation utility
- `tools/validate_collaboration_state.py`: validates file-based execution coordination state and task-run references
- `tools/init_planning_run.py`: manual planning-run folder initializer
- `tools/validate_planning_run.py`: planning-run output validator
- `tools/build_planning_runs_index.py`: derives `generated/planning_runs_index.json` from `planning_runs/`
- `tools/build_task_backlog_from_batches.py`: merges validated task batches into the canonical task backlog
- `tools/sync_and_check.ps1`: local helper for pulling GitHub-side changes and running validation checks
- `web/`: static multi-page read-only viewer over generated state

## Remote AI Review

For remote AI or web-only review environments, start with:

- `docs/AI_CONTEXT.md`
- `docs/EXTERNAL_REVIEW_PROMPT.md`
- `generated/review_manifest.json`

These files provide review entry points for the current repository state. The manifest lists the files to inspect directly; the repository no longer maintains a generated single-file context pack.

## Project Intake

Project intake is the first real user-facing workflow.

The Intake Interviewer asks focused questions about:

- project goal
- MVP boundary
- target users
- stack preference or stack recommendation
- local tools, paths, SDKs, and configuration
- existing repository state
- humans/AI agents working in parallel
- working style and proof expectations
- safety boundaries and non-goals

The intake output is a `project_intake.json` record conforming to `contracts/project_intake.schema.json`.

See `docs/PROJECT_INTAKE_WORKFLOW.md` and `prompts/00-intake-interviewer.md`.

## Planning Runs

The first planning workflow after intake is a manual planning run:

1. initialize a run folder with `python tools/init_planning_run.py <run-slug>`
2. write the rough idea or intake summary into `planning_runs/<run-slug>/input-idea.md`
3. refresh and copy the generated prompt from `planning_runs/<run-slug>/planning-run.md`
4. paste it into a web AI or Codex-style tool
5. save the returned JSON artifacts into `planning_runs/<run-slug>/outputs/`
6. validate them with `python tools/validate_planning_run.py planning_runs/<run-slug>`
7. review and accept or reject the plan

See `docs/PLANNING_RUN_WORKFLOW.md` and `planning_runs/README.md`.

Planning runs can also be indexed for read-only review:

```powershell
python tools/build_planning_runs_index.py
```

This writes `generated/planning_runs_index.json`, which records each run's scaffold status and which required output files are present. The local sync helper runs this automatically before validation. The static viewer renders this index on `web/planning-runs.html` without editing or inventing planning-run state.

## Validation

Run:

```powershell
python tools/validate_seed.py
python tools/validate_collaboration_state.py
```

Planning run outputs can be validated separately with:

```powershell
python tools/validate_planning_run.py planning_runs\<run-slug>
```

Task batch outputs can be validated separately with:

```powershell
python tools\validate_task_batches.py
```

The validator:

- fails clearly when required generated and contract files are missing
- parses every JSON file in the repository
- reports each valid JSON file
- reports parse failures clearly
- schema-validates the canonical generated artifacts when `jsonschema` is available
- runs dependency-light consistency checks across generated planning artifacts
- optionally parses `contracts/api_contract.openapi.yaml` when `PyYAML` is available

The task-batch validator checks `generated/task_batch_index.json`, every generated batch under `generated/task_batches/`, task dependency references, blocking references, cycle safety, and topological batch order.

For fresh-clone external review instructions, see `docs/EXTERNAL_REVIEW_PROMPT.md`.
The static viewer reads contract files directly for the Verification page, but this is still read-only documentation and not an implemented backend or live API.

## Current Use

This repository is currently a Phase 0 intake and planning kernel with static file-based dispatch/coordination views.

Start here:
- `docs/PROJECT_INTAKE_WORKFLOW.md`
- `prompts/00-intake-interviewer.md`
- `PROJECT_SPEC.md`
- `PRODUCT_RULES.md`
- `generated/`
- `web/dispatch.html`

Run validation:

```powershell
python tools\validate_seed.py
python tools\validate_task_batches.py
python tools\validate_collaboration_state.py
```
