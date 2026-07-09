# AI Assembly Line

`ai-assembly-line` is the seed repository for a human-in-the-loop multi-agent software assembly line.

Its first job is not autonomous execution. Its first job is project decomposition:

- rough idea -> guided project intake
- guided project intake -> structured project specification
- structured project specification -> repo split
- repo split -> microtask backlog
- microtask backlog -> role-specific prompt pack
- planning artifacts -> verification rules

## Phase 0 Goal

Build the planning kernel and the first "spec compiler":

`rough idea -> safe, structured project specification`

This repository is intentionally limited to intake, planning, contracts, prompts, and read-only presentation scaffolding.

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
   - `generated/agent_prompts.json`
   - `generated/slots_db.json`
5. Derived planning-run index
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

Rule: the frontend must render generated state and must not invent intake, task, repo, prompt, slot, or contract structure.

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
- `web/prompts.html`
- `web/slots.html`
- `web/planning-runs.html`
- `web/verification.html`

The generated sources remain:

- `generated/project_spec.json`
- `generated/repo_plan.json`
- `generated/task_backlog.json`
- `generated/agent_prompts.json`
- `generated/slots_db.json`
- `generated/planning_runs_index.json`

The viewer displays:

- project overview
- repository split and repo ownership
- task backlog grouped by repo target
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
- frontend-owned intake, task, repo, prompt, slot, planning-run, or contract models

## Initial Public Surface

The first public-facing web output should be read-only and contract-driven.

It should display:

- project name
- product goal
- repo split
- agent roles
- task backlog
- contract files
- prompt pack
- planning-run index
- verification rules

## Repository Map

- `PROJECT_SPEC.md`: current repo-level phase-0 specification
- `PROJECT_SPEC_TEMPLATE.md`: reusable template for future planning runs
- `PRODUCT_RULES.md`: hard rules and safety boundaries
- `docs/`: public overview, workflow, intake workflow, roles, task format, verification rules
- `docs/PROJECT_INTAKE_WORKFLOW.md`: interactive intake workflow for turning rough ideas into structured intake records
- `docs/EXTERNAL_REVIEW_PROMPT.md`: fresh-clone external reviewer prompt
- `docs/PLANNING_RUN_WORKFLOW.md`: manual planning-run workflow
- `docs/TASK_CREATION_GUIDE.md`: generic schema-aligned guide for creating implementation-ready task records
- `contracts/`: schemas and OpenAPI contract
- `contracts/project_intake.schema.json`: schema for guided project intake records
- `contracts/collaboration_state.schema.json`: draft schema for future human and web-AI coordination state
- `generated/`: canonical machine-readable planning artifacts for the current seed state
- `generated/planning_runs_index.json`: derived index of manual planning-run folders and output completeness
- `examples/coc-base-builder/`: example decomposition for a safe base layout planner
- `planning_runs/`: manual planning-run folders and review artifacts
- `prompts/`: copy-paste role prompts and task-splitting prompts, including the intake interviewer
- `tools/validate_seed.py`: repository JSON validation utility
- `tools/init_planning_run.py`: manual planning-run folder initializer
- `tools/validate_planning_run.py`: planning-run output validator
- `tools/build_planning_runs_index.py`: derives `generated/planning_runs_index.json` from `planning_runs/`
- `tools/sync_and_check.ps1`: local helper for pulling GitHub-side changes and running validation checks
- `web/`: static multi-page read-only viewer over generated state

## Remote AI Review

For remote AI or web-only review environments, start with:

- `docs/AI_CONTEXT.md`
- `docs/EXTERNAL_REVIEW_PROMPT.md`
- `generated/review_manifest.json`
- `generated/context_pack.md`

These files provide broad review context for the current repository state. They are intended to reduce setup friction for web-only review environments, not to imply that one file permanently contains the entire repository.

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
```

Planning run outputs can be validated separately with:

```powershell
python tools/validate_planning_run.py planning_runs\<run-slug>
```

The validator:

- fails clearly when required generated and contract files are missing
- parses every JSON file in the repository
- reports each valid JSON file
- reports parse failures clearly
- schema-validates the canonical generated artifacts when `jsonschema` is available
- runs dependency-light consistency checks across generated planning artifacts
- optionally parses `contracts/api_contract.openapi.yaml` when `PyYAML` is available

For fresh-clone external review instructions, see `docs/EXTERNAL_REVIEW_PROMPT.md`.
The static viewer reads contract files directly for the Verification page, but this is still read-only documentation and not an implemented backend or live API.

## Current Use

This repository is currently a Phase 0 intake and planning kernel with a static viewer.

Start here:
- `docs/PROJECT_INTAKE_WORKFLOW.md`
- `prompts/00-intake-interviewer.md`
- `PROJECT_SPEC.md`
- `PRODUCT_RULES.md`
- `generated/`
- `web/index.html`

Run validation:

```powershell
python tools\validate_seed.py
```
