# AI Assembly Line Context Pack

This file is generated from `generated/review_manifest.json` by `tools/build_context_pack.py`.
Treat the Git repository as the only source of truth and do not rely on chat history.

## `README.md`

- Category: `root-doc`
- Purpose: Repository overview, source-of-truth rules, intake workflow, Dispatch workflow, viewer constraints, validation guidance, and remote AI review links.
- Required: `true`

```markdown
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

```

## `PROJECT_SPEC.md`

- Category: `root-doc`
- Purpose: Human-readable phase 0 product specification covering guided intake, planning, execution-coordination artifacts, and current viewer scope.
- Required: `true`

```markdown
# AI Assembly Line Project Spec

## 1. Product Summary

- Project name: AI Assembly Line
- Core goal: turn rough software ideas into structured, reviewable intake and planning artifacts before implementation begins
- Primary output: an intake-guided spec compiler that converts idea notes into project intake records, project specs, repo plans, task backlogs, role prompts, and verification guidance
- Intended users: founders, product leads, technical planners, engineering teams supervising AI-assisted software work
- Non-goals for this phase:
  - multi-agent execution
  - authentication
  - databases
  - realtime collaboration
  - autonomous orchestration
  - a live operational dashboard

## 2. Safety and Product Boundaries

- The product is a planning system, not an automation runtime.
- Human review is required before intake or planning artifacts are treated as approved.
- Example projects involving games must be reinterpreted into safe planning tools when necessary.
- The system must refuse scopes that imply client automation, account access, botting, evasion, or interference with third-party live services.
- The intake process must preserve high-risk unknowns instead of pretending they are solved.

## 3. Phase 0 Deliverables

- repo-level planning documents
- an interactive project intake workflow and intake prompt
- JSON schemas for intake and core generated artifacts
- a seed OpenAPI contract for future read-only project-state endpoints plus a future spec-compiler draft route; no backend is implemented in Phase 0
- role-specific prompt pack
- guided task-batch generation workflow for large plans
- one worked example: `coc-base-builder`
- a static read-only viewer for generated planning state, task batches, and planning-run readiness

## 4. Source-of-Truth Layers

### Product Spec

- `PROJECT_SPEC.md`
- current machine-readable product spec: `generated/project_spec.json`

### Intake Workflow

- `docs/PROJECT_INTAKE_WORKFLOW.md`
- `prompts/00-intake-interviewer.md`
- `contracts/project_intake.schema.json`

### Schemas

- `project_intake.schema.json`
- `project_spec.schema.json`
- `agent_prompt.schema.json`
- `slot.schema.json`
- `task.schema.json`
- `task_batch_index.schema.json`
- `task_batch.schema.json`
- `collaboration_state.schema.json`
- `repo_plan.schema.json`

### API Contract

- `api_contract.openapi.yaml`

## 5. First Web Surface

The initial web surface should be read-only and generated from the source-of-truth files.

Current static viewer pages:

- Overview
- Repo Split
- Backlog
- Task Batches
- Prompts
- Slots
- Planning Runs
- Verification

## 6. Frontend Constraint

The frontend must render the current `PROJECT_SPEC.md` and contract-defined generated files.

It must not invent its own:

- intake model
- task model
- repo model
- prompt model
- slot model
- contract model
- verification model

## 7. Core Functional Feature

The first functional feature is the intake-guided spec compiler:

`rough idea -> guided intake -> safe structured project specification`

The intake output should include:

1. project goal
2. MVP boundary
3. target users
4. target platforms
5. stack preference or stack recommendation
6. existing tools, paths, and project state
7. team/agent working style
8. safety boundaries
9. assumptions and open questions
10. acceptance signals

The planning output should include:

1. product summary
2. safety and scope boundaries
3. repo split
4. domain model
5. API contract draft
6. frontend screens
7. backend services
8. core-engine responsibilities
9. verification tasks
10. copy-paste prompts for AI roles
11. guided task-batch files for large plans

Backend services are planning/spec sections only in Phase 0 and do not imply current backend implementation.

## 8. Verification Strategy

- validate generated JSON against schemas
- verify intake records against `contracts/project_intake.schema.json` when present
- verify examples against product rules
- verify prompt packs against scope boundaries
- verify task batches with schema, dependency, blocking, cycle, and topological-order checks
- verify frontend plans are contract-driven
- red-team unsafe interpretations, unbounded intake assumptions, and scope drift

```

## `PROJECT_SPEC_TEMPLATE.md`

- Category: `root-doc`
- Purpose: Reusable planning template that shows the intended product-spec structure.
- Required: `false`

```markdown
# Project Specification Template

Use this template for future project-planning runs. Fill every section explicitly and keep generated artifacts aligned to `contracts/`.

## Product Summary

- Project name:
- Problem being solved:
- Target users:
- Core user value:
- Phase target:

## Safety / Legal / Platform Boundaries

- Allowed behaviors:
- Disallowed behaviors:
- Platform interaction limits:
- Data handling limits:
- Review or compliance notes:

## User Personas

- Persona name:
  - role:
  - goals:
  - pain points:
  - approval authority:

## Core User Flows

- Flow name:
  - trigger:
  - steps:
  - outputs:
  - failure modes:

## Non-Goals

- Explicitly excluded scope:

## Repository Split

- Repo or package name:
  - purpose:
  - owns:
  - depends_on:
  - excludes:

## Domain Model

- Entity name:
  - fields:
  - relationships:
  - validation notes:

## API Surface

- Endpoint or interface:
  - method_or_type:
  - path_or_name:
  - input_shape:
  - output_shape:
  - boundary notes:

## Frontend Screens

- Screen name:
  - primary user:
  - renders_from:
  - allowed interactions:
  - states:

## Core Engine Responsibilities

- Deterministic logic:
- Validation rules:
- Transformation rules:
- Scoring or evaluation rules:
- Export or compilation rules:

## Backend Responsibilities

- Read-only or write responsibilities:
- Validation responsibilities:
- Integration boundaries:
- Explicit exclusions:

## Verification Strategy

- JSON and schema validation:
- Contract validation:
- Fixture coverage:
- Negative testing:
- Human review gates:

## Red Team Attack Plan

- Misuse case:
  - attacker goal:
  - exploit path:
  - expected rejection or guardrail:
  - verification artifact:

## Microtask Backlog

- Task id:
  - title:
  - owner role:
  - depends_on:
  - outputs:
  - acceptance criteria:

## Agent Prompt Pack

- Prompt id:
  - role:
  - target repo:
  - allowed files:
  - forbidden files:
  - required context:
  - required outputs:
  - verification required:

## Definition of Done

- The project spec is internally consistent.
- Machine-readable outputs validate against `contracts/`.
- The planned frontend consumes generated state instead of inventing structure.
- Unsafe or out-of-scope interpretations are rejected or safely reinterpreted.
- Human reviewers can trace repos, tasks, prompts, and verification work back to this spec.

```

## `PRODUCT_RULES.md`

- Category: `root-doc`
- Purpose: Hard product rules, scope boundaries, and frontend source-of-truth constraints.
- Required: `true`

```markdown
# Product Rules

## Planning-First Rule

Build decomposition and specification quality before building automation.

## Spec Compiler Rule

The first useful feature is `rough idea -> structured project specification`.

## Human Approval Rule

Generated planning artifacts are drafts until a human accepts them.

## Frontend Source-of-Truth Rule

The frontend must render project state from spec and generated state files and contract files.

It must not invent:

- tasks
- repos
- prompts
- slots
- contracts
- verification structures

## Schema Rule

Machine-readable planning artifacts must validate against the schemas in `contracts/`.

## API Contract Rule

Any HTTP layer must be described in `contracts/api_contract.openapi.yaml` before implementation.

## Scope Lock Rule

Do not add the following in this repository's initial phase:

- authentication
- databases
- realtime sync
- websocket coordination
- background workers
- autonomous multi-agent execution
- task claiming logic
- live dashboards with mutable state

## Safety Reinterpretation Rule

Unsafe or automation-oriented idea phrasing must be converted into the nearest safe planning interpretation or rejected.

Example:

- reject: botting, client control, account automation
- accept: offline planner, simulator-style evaluator, spec-only decomposition

## Traceability Rule

Tasks, prompts, and repo plans must trace back to the current project spec.

```

## `.gitignore`

- Category: `repo-config`
- Purpose: Local noise and generated cache ignore rules, including local tasks_created.json scratch output.
- Required: `false`

```
# Python cache files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
venv/

# Local environment/config files
.env
.env.*

# Local scratch/generated experiments
# Canonical task state lives under generated/task_backlog.json,
# generated/collaboration_state.json, and generated/task_runs/.
tasks_created.json

# OS/editor noise
.DS_Store
Thumbs.db
.vscode/
.idea/

```

## `docs/AI_CONTEXT.md`

- Category: `review-doc`
- Purpose: Remote AI review entry guidance for environments that cannot clone or run shell commands.
- Required: `true`

```markdown
# AI Context Gateway

This repository exposes a deliberate remote-review context gateway for AI systems that cannot clone Git repositories or run local shell commands.

## Source Of Truth Rules

- Treat the Git repository as the only source of truth.
- Do not rely on chat history, assistant claims, or out-of-band summaries.
- Read repository files directly.
- Generated JSON files are the canonical planning state.
- The static viewer in `web/` is read-only and must not invent task, repo, prompt, slot, contract, or hidden workflow state.

## Remote Review Entry Order

1. Start from `generated/context_pack.md` if it is available.
2. If `generated/context_pack.md` is unavailable, start from `generated/review_manifest.json`.
3. Use the manifest to fetch the listed files directly from the repository.

## What To Understand First

- `README.md`
- `PROJECT_SPEC.md`
- `PRODUCT_RULES.md`
- `generated/project_spec.json`
- `generated/repo_plan.json`
- `generated/task_backlog.json`
- `generated/task_batch_index.json`
- `generated/task_batches/*.json`
- `generated/agent_prompts.json`
- `generated/slots_db.json`
- `generated/planning_runs_index.json`

## What The Viewer Is Allowed To Do

- Render generated planning state directly.
- Render contract files read-only on the Verification page.
- Fail visibly when required source-of-truth files are missing or invalid.

## What The Viewer Must Not Do

- Add backend behavior
- Add authentication
- Add realtime sync
- Add editing
- Add mutable workflow state
- Add frontend-owned task, repo, prompt, slot, or contract models

```

## `docs/EXTERNAL_REVIEW_PROMPT.md`

- Category: `review-doc`
- Purpose: External reviewer instructions, including clone and no-clone fallback flows.
- Required: `true`

```markdown
# External Review Prompt

Use this prompt when reviewing `ai-assembly-line` from a fresh clone.

If clone access fails, use the no-clone fallback in this same document.

## Review Rules

- Treat the Git repository contents as the only source of truth.
- Do not rely on chat history, prior assistant claims, or out-of-band context.
- Review the repository as it exists on disk after cloning.

## Fresh-Clone Review Steps

1. Clone the repository and enter the repo root.
2. Read the top-level guidance first:
   - `README.md`
   - `PROJECT_SPEC.md`
   - `PRODUCT_RULES.md`
3. Inspect the contract and generated-state layers:
   - `contracts/`
   - `generated/`
4. Inspect the static viewer:
   - `web/`
   - `web/README.md`
   - `web/index.html`
   - `web/repos.html`
   - `web/backlog.html`
   - `web/prompts.html`
   - `web/slots.html`
   - `web/verification.html`
   - every `.js` file under `web/`
5. Inspect relevant docs under `docs/`.

## No-Clone Fallback

If the review environment cannot clone the repository or run shell commands:

1. Fetch and read `generated/context_pack.md`.
2. If `generated/context_pack.md` is missing, fetch `generated/review_manifest.json`.
3. Use the manifest to inspect the listed files manually.
4. Keep treating the Git repository files as the only source of truth.
5. Do not rely on chat history or unstated repository context.

## Validation Commands

Run these checks from the repository root:

```powershell
python tools\validate_seed.py
```

```powershell
Get-ChildItem web -Filter *.js | ForEach-Object { node --check $_.FullName }
```

If you want to review the static viewer in a browser, serve the repository root and open the viewer from `http://localhost:8000/web/`:

```powershell
python -m http.server 8000
```

## Review Focus

Confirm whether the repository currently behaves as a Phase 0 planning kernel and static read-only viewer.

Check for:

- source-of-truth drift between `README.md`, `PROJECT_SPEC.md`, `PRODUCT_RULES.md`, `contracts/`, `generated/`, and `web/`
- stale references to placeholder web surfaces that no longer exist
- viewer pages that claim behavior not backed by generated JSON
- frontend-owned models or invented workflow state
- schema drift or undocumented generated structure
- any accidental addition of backend behavior, authentication, databases, realtime sync, editing, or mutable dashboards

## Expected Reviewer Posture

- Be strict about traceability.
- Prefer concrete file references over high-level impressions.
- Treat missing validation, stale docs, and mismatched generated artifacts as review findings.

```

## `docs/public-overview.md`

- Category: `review-doc`
- Purpose: Short public-facing overview of the planning-kernel repository scope.
- Required: `true`

```markdown
# Public Overview

AI Assembly Line is a planning kernel for software teams using AI agents under human supervision.

It creates a strict path from rough idea to implementation-ready planning artifacts:

- project specification
- repository split
- task backlog
- task batches for large plans
- role prompts
- verification rules

The initial version is deliberately narrow. It focuses on decomposition quality, contract discipline, safe scope boundaries, and read-only inspection of generated planning state.

```

## `docs/workflow.md`

- Category: `review-doc`
- Purpose: Workflow description for decomposition, tasks, prompts, and verification.
- Required: `true`

```markdown
# Workflow

## 1. Input Idea

Capture a rough product idea in plain language.

## 2. Safe Interpretation

Rewrite or constrain the idea into an allowed product boundary when needed.

## 3. Compile Spec

Produce a structured project specification from the idea.

## 4. Split Repositories

Generate a repo plan describing packages or repositories and their boundaries.

## 5. Generate Tasks

Produce a microtask backlog with explicit owners, dependencies, and verification criteria. For large plans, use guided task-batch generation so each response produces one copy-pastable file.

## 6. Generate Prompt Pack

Produce prompts for planner, contracts, frontend, backend, core engine, and red team roles.

## 7. Verify

Validate contracts, check rule compliance, and red-team likely drift paths.

## 8. Human Review

Accept, revise, or reject the planning outputs before any implementation phase begins.

```

## `docs/PROJECT_INTAKE_WORKFLOW.md`

- Category: `review-doc`
- Purpose: Interactive intake workflow for turning a rough idea into an intake_session.json state and then a structured project_intake.json record before planning.
- Required: `true`

```markdown
# Project Intake Workflow

Project intake is the first user-facing step of AI Assembly Line.

Its purpose is to turn a rough idea into an interactive intake session and then into a structured intake record before the Planning Agent creates project specs, repo splits, task backlogs, role prompts, and verification rules.

The intake flow is intentionally interactive. It should ask only the questions that materially change the plan, suggest sensible defaults when possible, and stop asking once enough information exists to create a useful first planning run.

## Position in the assembly line

```text
rough idea
  -> guided intake interview
  -> intake_session.json
  -> project_intake.json
  -> planning run
  -> project_spec.json
  -> repo_plan.json
  -> task_backlog.json
  -> agent_prompts.json
  -> slots_db.json
  -> human review
```

The intake session is the internal interactive state while questions are still being asked.

The intake record is not an implementation plan. It is the structured input that keeps the implementation plan grounded.

## First response rule

When a user starts a project with only a rough idea, the first response must begin intake.

The Intake Interviewer must not immediately output:

- a full guideline document
- temporary or starter project guidelines
- technical steering rules
- target repository layout
- repo/package split
- definition of done
- suggested answers or default answers for the user to accept
- a full architecture
- a final stack decision
- a full MVP scope
- a task backlog
- agent assignments
- implementation code

Instead, it should output:

1. a short acknowledgement
2. a compact human-readable intake status summary
3. the next high-impact question, preferably as a decision card when the choice affects MVP difficulty or later scaling/refactor risk

This is true even if the user asks for guidelines or says they want to bring the idea to life. Those requests still start intake unless a complete intake record already exists.

If `readiness.can_generate_intake` is `false`, the first response must stop after the single next question in guided mode. It must not continue with project guidelines, technical steering, repository layout, default answers, stack choices, definition-of-done rules, or a checklist of future questions.

Do not print raw `intake_session` JSON by default. Keep it internally and show JSON only when the user asks for it, the session becomes ready for `project_intake.json`, state review is needed, or saving/exporting/persisting is requested.

See `docs/INTAKE_SESSION_FORMAT.md` and `docs/INTAKE_DECISION_CARDS.md`.

## Guidelines wording trap

A user may say something like:

```text
Here is the ai-assembly-line repo that helps with planning. I want to build a multiplayer Tron game. Can you help me set guidelines for the project based on the repo's steering help?
```

That is still a request to start intake, not a request to produce guidelines.

The correct first response is:

1. short acknowledgement
2. compact intake status
3. one high-impact question or decision card
4. stop

The incorrect response is anything that continues with starter steering rules, a recommended stack, repo/package split, project layout, definition of done, suggested answers, planning-run guidelines, raw JSON dump by default, or a batch checklist of future questions.

## Recommended target-project layout

For real projects, the steering and generated planning artifacts should live inside the target project repository, not only in this template repository.

Recommended layout:

```text
my-project/
  src/
  tests/
  README.md
  .ai-assembly/
    steering/
      PRODUCT_RULES.md
      PROJECT_SPEC_TEMPLATE.md
      prompts/
      contracts/
    intake/
      intake_session.json
      project_intake.json
    planning_runs/
      <run-slug>/
        input-idea.md
        planning-run.md
        outputs/
        review-notes.md
    generated/
      project_spec.json
      repo_plan.json
      task_backlog.json
      agent_prompts.json
      slots_db.json
      planning_runs_index.json
```

The `ai-assembly-line` repository is the upstream template and steering kit. The target project repository should contain the snapshot that agents and humans actually use.

Do not output this layout in the first response to a rough idea when `readiness.can_generate_intake` is `false`. This layout is guidance for later workspace initialization, not a substitute for intake.

## Intake modes

### Quick mode

Use when the user wants a fast first draft.

Rules:

- Ask at most five questions.
- Make low-risk assumptions explicit.
- Mark risky unknowns as open questions.
- Produce a draft intake record quickly.

### Guided mode

Use as the default.

Rules:

- Ask exactly one high-impact question per assistant turn unless the user explicitly asks for a batch.
- The one question should be the next unanswered decision that most changes architecture, stack, MVP, safety, or parallelization.
- Do not include a checklist of future questions in the same turn.
- Use compact human-readable updates instead of repeating raw JSON unless the user asks to see the state.
- For hard choices, present the one question as an A/B/C decision card with pros, cons, MVP risk, later scaling/refactor risk, and one explicit agent recommendation.
- The first MVP-boundary question for a rough idea should normally be a decision card when sensible options can be inferred.
- The user may answer `A`, `B`, `C`, `recommended`, or a custom answer.
- Do not silently apply the recommendation; record it only if the user chooses it.
- After the user answers, update `intake_session` internally and ask the next one-question step.
- Only produce `project_intake.json` after the session is ready.
- Suggest reasonable stack options only after platform, multiplayer/sync mode, and project state are known.
- Confirm the MVP before planning.
- Confirm team/agent working style before task decomposition.

### Expert mode

Use when the user already has strong constraints.

Rules:

- Let the user paste stack choices, tool paths, repo constraints, architecture notes, and team layout.
- Ask only for missing high-risk decisions.
- Produce the intake record with minimal back-and-forth.

## Decision-card guided questions

Guided mode still asks one question per turn. A decision card is a richer way to ask that one question when the choice is difficult.

Use a decision card when the answer may create MVP difficulty or later scaling/refactor pain, especially for:

- MVP scope
- platform target
- stack or engine
- realtime versus asynchronous behavior
- backend architecture
- accounts/auth/persistence
- deployment model
- team/agent split
- proof required for done

A decision card should include:

- the single decision being made
- two or three options labeled A/B/C
- what each option means
- pros
- cons
- MVP risk
- later scaling/refactor risk
- when each option is best
- one `Agent recommendation`, with rationale
- a final question: `Choose A, B, C, recommended, or custom.`

This still counts as one guided question. Future decisions stay in `open_questions`, not in the visible decision card.

If the user answers `recommended`, record the recommended option as the selected answer and preserve the rationale. If the user answers with a custom option, record it and keep any new uncertainty as an open question.

## Question sections

The Intake Interviewer should cover these sections, but not necessarily all in one message.

### 1. Goal

- What are you trying to build?
- Who is it for?
- What problem does it solve or what experience should it create?

### 2. MVP

- What is the smallest useful version?
- What can be postponed?
- What would make the first version successful?

### 3. Platform and stack

- Is there a preferred stack?
- Should the AI suggest a stack?
- What platforms matter first: desktop, web, mobile, server, embedded, CLI?
- Are there existing tools, local paths, SDKs, credentials, or hardware constraints?

When suggesting a stack, provide options with tradeoffs and a recommendation. Do not force a stack silently.

Do not suggest concrete stack options on the first response to a rough idea when high-risk answers such as platform, multiplayer/sync mode, existing project state, and team/agent layout are still unknown.

When enough context exists, prefer a decision card for stack/platform choices so the user can compare MVP speed against later scaling/refactor pain.

### 4. Existing project state

- Is this greenfield or an existing repository?
- Where is the project path?
- Are there existing source files, tests, docs, or architecture decisions?

### 5. Team and agent layout

- Will one person work alone?
- Will multiple humans work in parallel?
- Will multiple AI agents work in parallel?
- Should tasks be split by frontend/backend/core/test/docs or by feature slices?

### 6. Working style

- Does the user prefer very small tasks or larger milestones?
- Should tasks be optimized for beginner contributors, expert contributors, AI agents, or mixed teams?
- What proof is required for a task to count as done?

### 7. Safety and boundaries

- Are there external services, accounts, credentials, games, scraping, automation, or platform terms involved?
- Which actions are explicitly out of scope?
- What must never be automated?

## Ask/assume/stop rule

The intake should not ask questions forever.

Ask when the answer changes architecture, stack, MVP, safety, or parallelization.

Assume when the missing detail is low-risk and easy to revise later.

Stop and ask when the missing detail is high-risk, such as:

- real-time multiplayer versus turn-based multiplayer
- local-only versus real shared sync
- browser-first versus desktop-first
- existing repository versus greenfield
- required engine/framework
- external accounts, credentials, scraping, or automation
- team size and parallel work expectations
- hardware, SDK, or local tool constraints

## Intake session output

While questions are still open, maintain an internal `intake_session` state conforming to `contracts/intake_session.schema.json`.

The session should include:

- current section
- completed and incomplete sections
- questions already asked
- answers received so far
- stack options when suggested
- assumptions
- open questions
- readiness to generate `project_intake.json`
- next action

If `readiness.can_generate_intake` is `false`, the output is not allowed to continue into guidelines or planning artifacts.

In guided mode, `next_action.questions` should contain only the single next question. Other unanswered decisions belong in `open_questions`, not in the visible next-question list.

Decision-card options are human-facing guidance. Record only the user's selected answer as the intake answer; do not treat unchosen options as project decisions.

## Required intake output

Only when the session is ready should the intake interview produce `project_intake.json` conforming to `contracts/project_intake.schema.json`.

The record should include:

- project goal
- MVP
- target users
- platform targets
- stack preference or stack recommendation
- existing tools and paths
- existing repository state
- team/agent mode
- working style
- constraints
- assumptions
- open questions
- safety boundaries
- acceptance signals

## Hand-off to Planning Agent

After the intake record is complete enough, the Planning Agent should use it to create:

- `project_spec.json`
- `repo_plan.json`
- `task_backlog.json`
- `agent_prompts.json`
- `slots_db.json`

The Planning Agent must preserve all high-risk unknowns as open questions or verification tasks instead of pretending they are solved.

```

## `docs/INTAKE_SESSION_FORMAT.md`

- Category: `review-doc`
- Purpose: Interactive intake-session response format and first-turn hard-stop rules for rough project requests.
- Required: `true`

```markdown
# Intake Session Format

`project_intake.json` is the final structured intake record.

`intake_session.json` is the internal interactive state used while the Intake Interviewer is still asking questions.

A frontend can render `intake_session.json` directly. In normal chat, the assistant should show compact human-readable intake status instead of dumping raw JSON.

## Why this exists

A rough project idea should not immediately turn into a full guideline document, project spec, backlog, or implementation plan.

The intended chat flow is:

```text
rough idea
  -> compact intake status
  -> one focused question or decision card
  -> project_intake.json
  -> planning artifacts
```

This prevents the AI from jumping the gun and generating a fake-complete plan before high-risk decisions are answered.

## Source of truth

The internal session schema is:

```text
contracts/intake_session.schema.json
```

The session eventually produces:

```text
contracts/project_intake.schema.json
```

## Required behavior for a new project request

When a user provides only a rough idea, the Intake Interviewer must not output:

- a full guideline document
- temporary or starter project guidelines
- technical steering rules
- target repository layout
- repo/package split
- definition of done
- suggested answers or default answers for the user to accept
- a full project specification
- a full task backlog
- agent work assignments
- implementation code
- architecture as if all decisions are final

Instead, it must output:

1. a short acknowledgement
2. a compact human-readable intake status summary
3. the next high-impact question, preferably as a decision card when the choice affects MVP difficulty or later scaling/refactor pain

Then it must stop. If `readiness.can_generate_intake` is `false`, the response must not continue with guidelines, recommendations, architecture, repo layout, task rules, suggested answers, or a checklist of future questions.

Do not print raw `intake_session` JSON by default. Keep it internally and show JSON only when the user asks for it, the session becomes ready for `project_intake.json`, state review is needed, or saving/exporting/persisting is requested.

## Guidelines wording trap

A user may ask for `guidelines`, `steering help`, `starter rules`, or help `setting up` a project while providing only a rough idea.

That wording still means: start intake.

It does not permit the Intake Interviewer to produce starter steering rules, temporary guidelines, stack recommendations, repo split, definition of done, suggested answers, or a checklist of future intake questions.

The correct response is to say that guidelines can be produced after the high-risk intake questions are answered, then provide only the compact intake status and the single next question in guided mode.

## Minimal first response shape

For a rough idea like `I want to build a tiny shared grocery list app for two people`, the first response should look like this:

```text
Yes — this starts intake, because guidelines should come after the high-risk project choices are known.

Intake status: started
Project: shared-grocery-list
Known: tiny shared grocery list app for two people
Still needed: MVP boundary

Decision: What is the smallest useful MVP for the two of you?

A) One-device local list
What it means: One list on one device, no sharing between devices.
Pros: fastest to build and easiest to test.
Cons: not truly shared.
MVP risk: low.
Scaling/refactor risk: high — adding real sharing later may require rethinking storage and state.
Best when: You only want to validate the list UI first.

B) Manual share/export list
What it means: One person can copy/export the list and send it to the other.
Pros: simple, with some sharing behavior.
Cons: clunky and not live.
MVP risk: low-medium.
Scaling/refactor risk: medium.
Best when: Sharing matters, but live collaboration is not required yet.

C) Real shared list with sync
What it means: Both people can edit the same list from separate devices.
Pros: matches the actual product idea.
Cons: needs backend/sync/conflict decisions.
MVP risk: medium-high.
Scaling/refactor risk: low-medium — avoids fake-sharing rework later.
Best when: The core value is truly shared usage.

Agent recommendation: C — if “shared” is the point of the product; A only if you want the fastest throwaway prototype.

Question: Choose A, B, C, recommended, or custom.
```

This is not a required exact output. It is the intended shape: compact state plus one useful decision.

In guided mode, `next_action.questions` should contain only the single next question. Other unanswered decisions belong in `open_questions`, not in the visible next-question list.

## Compact guided updates

Normal guided turns should not print the full JSON.

Use a compact update like:

```text
Recorded: MVP sharing mode = real shared list with sync.
Status: MVP boundary is clear; platform/stack is still open.

Decision: Which platform should the MVP target first?
...
```

Show the full `intake_session` only when:

- the user asks to see the JSON or full session state,
- the session becomes ready for `project_intake.json`,
- a save/export/persist step is requested, or
- the state has become ambiguous and needs explicit review.

The compact update still represents an updated `intake_session`; it just does not dump the entire object into the chat.

## Frontend rendering guidance

A frontend intake page should render:

- current status
- current section
- completed sections
- unanswered high-risk questions
- suggested stack options
- assumptions
- readiness to generate `project_intake.json`
- next action

The frontend must not invent intake fields outside `contracts/intake_session.schema.json`.

## Transition to project_intake.json

Only when `readiness.can_generate_intake` is `true` should the Intake Interviewer draft `project_intake.json`.

If `can_generate_intake` is `false`, the next output should ask the next single question in guided mode or suggest stack options only when `next_action.type` is `suggest_stack`.

```

## `docs/INTAKE_DECISION_CARDS.md`

- Category: `review-doc`
- Purpose: Decision-card guidance for one-question guided intake choices with A/B/C options, tradeoffs, MVP risk, scaling risk, and explicit recommendations.
- Required: `true`

```markdown
# Intake Decision Cards

Guided intake asks one question per assistant turn.

A question may still be rich enough to help the user make a good decision. For difficult architecture, MVP, stack, scaling, sync, persistence, or team-split choices, present the one question as a decision card.

## Purpose

Decision cards prevent two bad outcomes:

1. The assistant asks a vague question and leaves the user to guess the consequences.
2. The assistant silently chooses a stack, MVP, or architecture and calls it a recommendation.

A decision card keeps the user in control while making the tradeoffs visible.

## Required shape

Use this shape when a choice is hard or has long-term consequences:

```text
Decision: <one decision the user must make>

A) <option name>
What it means: <plain-language explanation>
Pros: <short list or sentence>
Cons: <short list or sentence>
MVP risk: <low | medium | high> — <why>
Scaling/refactor risk: <low | medium | high> — <why>
Best when: <when this option fits>

B) <option name>
...

C) <option name>
...

Agent recommendation: <A/B/C> — <reason>

Question: Choose A, B, C, recommended, or custom.
```

This still counts as one guided intake question.

## Rules

- Provide at most three main options unless the user asks for more.
- Include an `Agent recommendation`, but never silently apply it.
- The user may answer `A`, `B`, `C`, `recommended`, or a custom answer.
- If the user answers `recommended`, record the recommended option as the selected answer and keep the rationale.
- If the user gives a custom answer, record it and update open questions if the custom answer introduces risk.
- Keep future decisions in `open_questions`; do not turn the card into a checklist of multiple questions.
- Do not use decision cards for trivial low-risk choices.
- For the first high-impact MVP-boundary question of a rough idea, prefer a decision card when sensible options can be inferred from the idea.

## When to use decision cards

Use decision cards for choices that materially affect:

- MVP scope
- platform target
- stack or engine
- backend architecture
- realtime versus asynchronous behavior
- sync/storage model
- persistence/auth/accounts
- deployment model
- team/agent split
- proof required for done
- choices that may create later scaling or refactor pain

## Example: MVP boundary

```text
Intake status: started
Project: shared-grocery-list
Known: tiny shared grocery list app for two people
Still needed: MVP boundary

Decision: What is the smallest useful MVP for the two of you?

A) One-device local list
What it means: One list on one device, no sharing between devices.
Pros: fastest to build and easiest to test.
Cons: not truly shared.
MVP risk: low.
Scaling/refactor risk: high — adding real sharing later may require rethinking storage and state.
Best when: You only want to validate the list UI first.

B) Manual share/export list
What it means: One person can copy/export the list and send it to the other.
Pros: simple, with some sharing behavior.
Cons: clunky and not live.
MVP risk: low-medium.
Scaling/refactor risk: medium.
Best when: Sharing matters, but live collaboration is not required yet.

C) Real shared list with sync
What it means: Both people can edit the same list from separate devices.
Pros: matches the actual product idea.
Cons: needs backend/sync/conflict decisions.
MVP risk: medium-high.
Scaling/refactor risk: low-medium — avoids fake-sharing rework later.
Best when: The core value is truly shared usage.

Agent recommendation: C — if “shared” is the point of the product; A only if you want the fastest throwaway prototype.

Question: Choose A, B, C, recommended, or custom.
```

## Example: stack direction

```text
Recorded: team mode = 2 people working in parallel.
Status: Ready for stack choice.

Decision: Which stack direction do you want for the MVP?

A) Flutter client + backend service
What it means: Build the UI in Flutter and a separate backend for rooms, game state, and realtime events.
Pros: Best fit for desktop-first now and mobile later; one client codebase can travel far.
Cons: Backend still needs separate WebSocket/game-state work; Flutter desktop packaging has some setup cost.
MVP risk: medium — more initial setup than a pure web prototype.
Scaling/refactor risk: low-medium — mobile later is much less painful.
Best when: Mobile later is real, not just a vague maybe.

B) React + Tauri desktop client + backend
What it means: Build a web-style UI wrapped as a lightweight desktop app, with a separate backend.
Pros: Fast desktop MVP; clean client/backend split; familiar web tooling.
Cons: Mobile later probably needs a separate client or rewrite.
MVP risk: low-medium — good speed if the team knows web tooling.
Scaling/refactor risk: medium — mobile later can become a second project.
Best when: Desktop MVP speed matters more than mobile reuse.

C) React web app + Electron wrapper + backend
What it means: Build a browser-style app and package it with Electron for desktop.
Pros: Fastest if the team knows web tooling; huge ecosystem.
Cons: Heavier desktop app; mobile later is not clean; easier to accumulate frontend/backend coupling.
MVP risk: low — quickest path to something playable.
Scaling/refactor risk: high — can become painful if mobile and polish matter later.
Best when: The goal is to prove gameplay fast.

Agent recommendation: A — because the stated goal is desktop first, but mobile later matters.

Question: Choose A, B, C, recommended, or custom.
```

```

## `docs/PLANNING_RUN_WORKFLOW.md`

- Category: `review-doc`
- Purpose: Manual planning-run workflow for turning a rough idea or intake record into saved planning artifacts and human-reviewed outputs.
- Required: `true`

```markdown
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

```

## `docs/TASK_GENERATION_WORKFLOW.md`

- Category: `review-doc`
- Purpose: Workflow for turning an accepted intake record into parallel-safe task_backlog.json tasks with dependencies and verification.
- Required: `true`

```markdown
# Task Generation Workflow

Task generation starts only after intake is complete enough for planning.

The Planning Agent turns an accepted `project_intake.json` into planning artifacts, including a parallel-safe `task_backlog.json`.

## Workflow position

```text
rough idea
  -> intake_session.json
  -> project_intake.json
  -> planning run
  -> project_spec.json
  -> repo_plan.json
  -> task_backlog.json
  -> agent_prompts.json
  -> slots_db.json
```

Do not generate implementation tasks before the intake record is ready. Open high-risk decisions must remain open questions or blocking tasks instead of being silently assumed.

## Inputs

Task generation should read:

- accepted `project_intake.json`, when available
- `PROJECT_SPEC.md` / `PROJECT_SPEC_TEMPLATE.md`
- `PRODUCT_RULES.md`
- `docs/PLANNING_RUN_WORKFLOW.md`
- `docs/TASK_CREATION_GUIDE.md`
- `docs/TASK_CARD_FORMAT.md`
- existing contracts under `contracts/`
- generated repo plan, if already drafted
- any existing planning-run notes

## Outputs

A complete planning run should produce or update:

- `project_spec.json`
- `repo_plan.json`
- `task_backlog.json`
- `agent_prompts.json`
- `slots_db.json`

The task backlog must be traceable to the project spec and repo plan.

For large plans, generate task output in batches rather than one large `task_backlog.json` response. The preferred web AI flow is guided: paste `prompts/06-task-splitter.md` with `MODE: guided`, save the first response as `generated/task_batch_index.json`, then reply `continue` until each `generated/task_batches/<batch_id>.json` file has been emitted.

## Generation phases

### 1. Freeze the accepted intake

Before generating tasks, summarize the accepted decisions:

- goal
- MVP boundary
- platform target
- stack / engine direction
- project state: greenfield or existing repo
- team/agent working style
- safety boundaries
- proof required for done
- open questions

If any high-risk answer is still missing, do not pretend it is solved. Either ask intake to continue or create an explicit blocking task.

### 2. Define shared contracts first

For parallel work, generate contract/spec tasks before implementation tasks.

Examples:

- game rules spec
- API contract
- WebSocket event contract
- data model sketch
- file ownership map
- test scenario matrix

This prevents client and backend workers from inventing incompatible assumptions.

### 3. Split work into lanes

Use lanes that let people or agents work in parallel with minimal file overlap.

Common lanes:

- `shared-contract`
- `client-ui`
- `backend-game-state`
- `core-domain`
- `tests-verification`
- `docs-devex`

For a two-worker project, a good default is:

```text
Worker A: client/UI tasks
Worker B: backend/core-state tasks
Shared first: contracts, interfaces, test scenarios
```

Do not split only by technology if the MVP needs vertical slices. Prefer a small number of contract-first tasks, followed by parallel implementation slices.

### 4. Make dependencies explicit

Every task should list its prerequisites by task ID.

Good dependency graph:

```text
T-001 Define realtime event contract
T-002 Implement backend room creation     depends on T-001
T-003 Implement client room join screen   depends on T-001
T-004 Verify join-room flow               depends on T-002, T-003
```

Bad dependency graph:

```text
T-001 Build backend
T-002 Build frontend
T-003 Test everything
```

### 5. Add acceptance criteria and verification

Every task needs observable acceptance criteria and proof of done.

Examples:

- command output
- passing tests
- manual flow checklist
- screenshot or recorded demo
- contract reference
- schema validation
- no forbidden files touched

A task without verification is not ready for assignment.

### 6. Preserve scope boundaries

The backlog must separate:

- MVP tasks
- post-MVP tasks
- blocked tasks
- research/spike tasks
- explicit non-goals

Do not let future scaling concerns explode the first backlog. Add future-proofing only when it prevents obvious near-term rework.

## Parallel-safe task rules

For each task, ask:

1. Can one owner complete this without waiting for another unfinished implementation task?
2. Are dependencies explicit?
3. Are file/repo boundaries clear?
4. Can the reviewer verify completion?
5. Does it avoid silently deciding unresolved intake questions?

If the answer is no, split or rewrite the task.

## MVP-first rule

The first backlog should make the smallest playable or useful version real.

For games and realtime apps, prefer this order:

1. shared rules/events contract
2. minimal backend state loop
3. minimal client UI loop
4. one end-to-end playable flow
5. verification and regression tests
6. polish and future features

Avoid starting with account systems, matchmaking, skins, analytics, scaling infrastructure, or deployment complexity unless the intake record explicitly requires them for MVP.

## Blocking tasks

If planning cannot proceed without a decision, create a blocking task instead of guessing.

Example:

```text
T-BLOCK-001 Decide deployment target
Reason: Hosting choice changes backend runtime, environment config, and verification steps.
Required answer: local-only, LAN, cloud staging, or production hosting.
```

Blocking tasks should be few. If there are many, intake is not ready.

## Done state

A generated task backlog is ready when:

- every task has a stable ID
- every task has a lane/owner target
- dependencies reference valid task IDs
- MVP tasks are separated from post-MVP tasks
- shared contract tasks come before parallel implementation work
- every task has acceptance criteria
- every task has verification steps
- open questions are explicit
- no task requires forbidden scope

For batched generation, the backlog is ready only after every accepted batch validates individually, task IDs/dependencies form an acyclic graph, and batch order is topological.

```

## `docs/EXECUTION_WORKFLOW.md`

- Category: `review-doc`
- Purpose: File-based execution loop for task assignments, executor prompts, task_run reports, and proof review without backend persistence.
- Required: `true`

```markdown
# Execution Workflow

This repo still uses a static, file-based workflow. Execution state is recorded as generated JSON, not as frontend-owned mutable state.

## Source files

- `generated/task_backlog.json` is the canonical task list.
- `generated/collaboration_state.json` overlays ownership, execution status, notes, and proof references.
- `contracts/collaboration_state.schema.json` defines actors and task assignment state.
- `contracts/task_run.schema.json` defines one executor completion report.
- `generated/task_runs/<task_id>.json` may hold detailed proof for one task execution run.

## Basic loop

1. Pick one task from `generated/task_backlog.json`.
2. Add or update one `task_assignments` entry in `generated/collaboration_state.json`.
3. Give the task JSON to `prompts/07-task-executor.md`.
4. Save the returned report as `generated/task_runs/<task_id>.json` or another stable run file.
5. Add a short proof reference to the task assignment in `generated/collaboration_state.json`.
6. Review the proof before treating the task as done.

## Status meanings

- `unclaimed`: no active owner; normally derived when no assignment record exists.
- `claimed`: an actor has taken responsibility but has not started visible work.
- `in_progress`: active implementation or verification is underway.
- `review`: implementation/proof exists and needs review.
- `done`: accepted proof exists.
- `blocked`: work cannot safely continue without a decision, dependency, or missing context.
- `released`: previously claimed work was released back to the pool.

## Validation

Run:

```powershell
python tools\validate_collaboration_state.py
```

For generated task batches, build the canonical backlog after every batch validates:

```powershell
python tools\validate_task_batches.py
python tools\build_task_backlog_from_batches.py
```

## Frontend

Open `web/assignments.html` from the static viewer. It renders task ownership and proof from files only. It does not claim, edit, lock, or write state.

```

## `docs/VIEWER_PAGE_ROLES.md`

- Category: `review-doc`
- Purpose: Dispatch/Assignments/Task Batches page-role split, making Dispatch the primary what-can-I-do-next surface.
- Required: `true`

```markdown
# Viewer Page Roles

The static viewer has overlapping pages on purpose, but each page has a different job.

## Primary workflow page

### Dispatch

`web/dispatch.html` is the primary "what can I do next?" page.

Use it to:

- see tasks grouped by topological dependency wave
- find green/available tasks whose dependencies are done
- avoid locked, blocked, waiting, and done tasks
- open one task's detail panel
- copy the full one-task execution context into a fresh AI chat
- copy raw task JSON when needed

Dispatch does not claim, lock, edit, or write task state. It only renders source-of-truth files and produces copyable context.

## Audit/status page

### Assignments

`web/assignments.html` is the audit and status page for file-based collaboration state.

Use it to:

- inspect actors
- inspect assignment records
- inspect proof references
- preview/copy/download replacement `generated/collaboration_state.json` through the static helper

Assignments remains file-based. It does not write directly to the repo.

## Generation/validation page

### Task Batches

`web/task-batches.html` is the generation and validation page for batch-created task files.

Use it to:

- inspect `generated/task_batch_index.json`
- inspect generated batch file readiness
- validate dependency graph shape before merging task batches into the canonical backlog

Once batches are accepted and merged into `generated/task_backlog.json`, Dispatch becomes the primary page for picking the next task.

```

## `docs/TASK_CREATION_GUIDE.md`

- Category: `review-doc`
- Purpose: Generic schema-aligned guide for creating implementation-ready tasks with ownership, status, priority, proof, edge cases, and non-goals.
- Required: `true`

```markdown
# Task Creation Guide

This guide defines how to create implementation-ready tasks for any project planned through AI Assembly Line.

Use the accepted intake, project spec, repo plan, and task schema as the source of truth. Project-specific examples may use concrete repo names and prefixes, but the canonical task format must stay reusable.

## Core Rule

Every task must answer:

```text
What repo or area owns this?
What role owns this?
What exactly changes?
What does it depend on?
What downstream work does it unblock?
How do we prove it works?
What edge cases and non-goals must not drift?
```

If a task cannot answer those questions, it is not ready.

## Task Size

A task should usually fit in one focused work session.

Use:

- `S`: small, usually 30-90 minutes
- `M`: medium, usually 2-4 hours
- `L`: too large for direct execution; split before assignment

Milestones are not tasks. Phrases like `build the backend`, `create the client`, or `implement multiplayer` should be decomposed into smaller work packets.

## Task Hierarchy

Use this hierarchy:

```text
Milestone
  -> feature group or lane
    -> task
      -> verification evidence
```

Prefer shared contract/interface tasks before implementation tasks when multiple people or AI agents will work in parallel.

## Task IDs

Use stable IDs. Two good styles are:

- Project-agnostic lowercase IDs, such as `define-room-event-contract`
- Project-specific prefix IDs, such as `CONTRACT-001` or `UI-003`

Dependencies and blocked-work references must use task IDs, not task titles.

## Canonical Fields

Tasks in `task_backlog.json` must conform to `contracts/task.schema.json`.

Required fields:

```yaml
id:
title:
summary:
owner_role:
repo_target:
depends_on:
inputs:
outputs:
acceptance_criteria:
verification:
```

Recommended optional fields:

```yaml
status:
priority:
milestone:
lane:
allowed_areas:
blocks:
objective:
context:
implementation_notes:
proof_required:
edge_cases:
non_goals:
estimated_size:
risk_tags:
handoff_notes:
notes:
```

Do not use `repo` in canonical task JSON. Use `repo_target`, because it should match a repo or ownership target from `repo_plan.json`.

## Field Guidance

`status` should be one of:

```text
draft
ready
in_progress
blocked
review
done
rejected
```

`priority` should be one of:

```text
P0: blocks many other tasks
P1: needed for MVP
P2: useful but not blocking
P3: later or nice-to-have
```

`blocks` should list task IDs or stable work IDs that depend on this task.

`objective` should state the purpose in one short paragraph.

`context` should capture decisions or constraints the task must preserve.

`implementation_notes` may guide execution, but should not become a full implementation script.

`proof_required` should list evidence expected from the executor, such as test output, build output, logs, screenshots, fixtures, or manual test notes.

`edge_cases` should list behavior that must be tested or explicitly documented.

`non_goals` should list scope the task must not expand into.

`estimated_size` should be `S`, `M`, or `L`. A task marked `L` should normally be split before execution.

## Standard Template

```yaml
id:
title:
summary:
owner_role:
repo_target:
status: draft
priority:
milestone:
lane:
allowed_areas: []
depends_on: []
blocks: []

objective: >
  Describe the task in one short paragraph.

context: >
  Include the project decisions this task must respect.

inputs:
  - 

outputs:
  - 

implementation_notes:
  - 

acceptance_criteria:
  - Code builds or the non-code artifact is complete.
  - Required files, contracts, or docs exist.
  - Relevant tests or checks pass where practical.

verification:
  - Reviewer can validate the outputs against the acceptance criteria.

proof_required:
  - Build, test, validation, log, screenshot, fixture, or manual test evidence.
  - Short change summary.

edge_cases:
  - 

non_goals:
  - 

estimated_size:
```

## Dependency Rules

Create shared contracts before consumers.

Do not create implementation tasks that require undefined APIs, event contracts, schemas, package boundaries, or file ownership rules.

A task should normally belong to one `repo_target`. If it touches multiple repos, mark it as integration or QA work and make the cross-repo proof explicit.

## Large Plan Batch Workflow

For large generated plans, do not ask a web AI to return the whole backlog in one response.

Use a guided batch workflow for normal web AI usage:

1. Paste `prompts/06-task-splitter.md` with `MODE: guided` and the accepted generated plan.
2. Save the first returned JSON block as `generated/task_batch_index.json`.
3. Reply `continue`, `next`, or equivalent.
4. Save each returned JSON block as `generated/task_batches/<batch_id>.json`.
5. Repeat until the task splitter says no batches remain.

This keeps outputs copy-pastable and reduces the chance of truncation.

The explicit `MODE: batch-index` and `MODE: task-batch` controls still exist for debugging or recovering a lost chat context, but the guided flow should be the default user-facing flow.

Each task batch must conform to `contracts/task_batch.schema.json`.

Each task inside the batch must still conform to `contracts/task.schema.json`.

The future frontend should support:

- copy prompt for batch index
- paste returned batch index
- continue through one generated batch per response
- paste each returned task batch JSON
- validate task graph dependencies and topological batch order
- merge accepted batches into `generated/task_backlog.json`

## Review Checklist

Before marking a task `ready`, check:

- The repo or ownership target is clear.
- The owner role is clear.
- The objective is narrow.
- Dependencies and blocked work are listed.
- Acceptance criteria are pass/fail.
- Proof requirements are specific.
- Edge cases and non-goals are explicit.
- Another person or AI agent can verify the task without guessing intent.

```

## `docs/TASK_CARD_FORMAT.md`

- Category: `review-doc`
- Purpose: Task-card format guidance for small, owned, bounded, dependency-aware, verifiable, parallel-safe tasks.
- Required: `true`

```markdown
# Task Card Format

A task card is the smallest useful planning unit in `task_backlog.json`.

It should be small enough for one person or agent to complete without owning the whole project, but large enough to produce a meaningful, reviewable change.

## Purpose

Task cards prevent vague planning output such as:

```text
Build the backend.
Build the frontend.
Add multiplayer.
```

Instead, every task should make ownership, boundaries, dependencies, and proof of completion explicit.

## Required task qualities

A good task is:

- **small** — one clear change, not an epic
- **owned** — assigned to one lane or role
- **bounded** — lists allowed repo area or files when possible
- **dependency-aware** — states what must exist first
- **verifiable** — includes concrete proof of done
- **parallel-safe** — avoids unnecessary file overlap with other tasks
- **traceable** — maps back to the accepted intake/project spec

## Recommended fields

Use fields that match the current task contract when generating machine-readable output. The planning text should still cover these concepts even if the schema names differ.

```json
{
  "id": "define-shared-event-contract",
  "title": "Define shared event contract",
  "summary": "Define the minimal producer/consumer events required for the first end-to-end MVP flow.",
  "owner_role": "Contract Agent",
  "status": "ready",
  "priority": "P0",
  "milestone": "Shared Contract Foundations",
  "lane": "shared-contract",
  "repo_target": "shared-contracts",
  "depends_on": [],
  "blocks": [
    "implement-producer-flow",
    "implement-consumer-flow"
  ],
  "allowed_areas": [
    "docs/",
    "shared/contracts/"
  ],
  "objective": "Define the initial event contract so downstream workers can implement compatible behavior.",
  "context": "The task must preserve the accepted architecture and avoid inventing implementation details outside the contract.",
  "inputs": [
    "accepted project_intake.json",
    "repo_plan.json"
  ],
  "outputs": [
    "docs/events.md"
  ],
  "implementation_notes": [
    "Keep the contract implementation-agnostic.",
    "List sender, receiver, payload, and expected behavior for each event."
  ],
  "acceptance_criteria": [
    "MVP lifecycle events are listed.",
    "Primary command and result events are listed.",
    "Each event includes sender, payload, and expected receiver behavior."
  ],
  "verification": [
    "Contract document exists and is referenced by downstream implementation tasks.",
    "No implementation task invents events outside the contract without updating it."
  ],
  "proof_required": [
    "Path to the contract document.",
    "Short summary of event coverage."
  ],
  "edge_cases": [
    "Unknown event type",
    "Missing payload",
    "Version mismatch"
  ],
  "non_goals": [
    "Do not implement producer behavior.",
    "Do not implement consumer behavior."
  ],
  "estimated_size": "S",
  "handoff_notes": "Downstream implementation tasks should start from this contract."
}
```

## Field guidance

### `id`

Use stable task IDs. Dependencies should reference IDs, not titles.

### `title`

Use an action-oriented title:

```text
Good: Define room lifecycle WebSocket events
Bad: WebSocket stuff
```

### `lane`

Use lanes that allow parallel work. Common lanes:

- `shared-contract`
- `client-ui`
- `backend-game-state`
- `tests-verification`
- `docs-devex`

### `repo_target` / `allowed_areas`

Make file ownership clear enough to avoid two people editing the same files unnecessarily.

### `depends_on`

Dependencies should be minimal. Too many dependencies serialize the whole project; too few create merge chaos.

### `acceptance_criteria`

Acceptance criteria must be observable. Avoid vague criteria like `works well`.

### `verification`

Verification should tell a reviewer how to prove the task is done:

- run a command
- inspect a file
- execute a manual flow
- check a contract reference
- run tests
- verify no forbidden files changed

## Task sizing

Prefer tasks that fit in one focused implementation session.

Split a task when:

- it touches unrelated repo areas
- it needs multiple people to coordinate
- it mixes contract design and implementation
- it mixes UI and backend behavior before a contract exists
- it cannot be verified with a clear proof step

Do not split a task when the pieces cannot be tested or reviewed independently.

## Parallel-work rule

For two or more workers, create shared contract tasks first, then split client/backend/core/test work around those contracts.

Example split:

```text
T-001 shared-contract: Define game event contract
T-002 backend-game-state: Implement room creation using T-001
T-003 client-ui: Implement room join UI using T-001
T-004 tests-verification: Add integration scenario for room join
```

This allows backend and client work to proceed in parallel without inventing incompatible APIs.

```

## `docs/roles.md`

- Category: `review-doc`
- Purpose: Role descriptions for the planning kernel and static viewer work.
- Required: `true`

```markdown
# Roles

## Planning Agent

Turns rough ideas into structured product specs and decomposition artifacts.

## Contract Steward

Maintains schemas, contract compatibility, and fixture validity.

## Frontend Builder

Builds read-only static frontend views for Phase 0 that render generated planning state and contracts without inventing structure.

## Backend Builder

Implements API surfaces described by the OpenAPI contract when a later phase allows it.

## Core Engine Builder

Implements deterministic planning-kernel logic and validators for the current seed repository.

Domain-specific scoring or simulation-style evaluation belongs to future or example-specific work, such as `examples/coc-base-builder/`, not the current Phase 0 planning kernel.

## Red Team Verifier

Tries to trigger scope drift, safety failures, undocumented state, and weak verification logic.

## Human Reviewer

Approves scopes, boundaries, and planning outputs.

```

## `docs/task-format.md`

- Category: `review-doc`
- Purpose: Task record expectations referenced by generated planning artifacts.
- Required: `true`

```markdown
# Task Format

Each generated task should be small, testable, and traceable.

## Required Fields

- `id`
- `title`
- `summary`
- `owner_role`
- `repo_target`
- `depends_on`
- `inputs`
- `outputs`
- `acceptance_criteria`
- `verification`

## Optional Fields

- `status`
- `priority`
- `milestone`
- `lane`
- `allowed_areas`
- `blocks`
- `objective`
- `context`
- `implementation_notes`
- `proof_required`
- `edge_cases`
- `non_goals`
- `estimated_size`
- `risk_tags`
- `notes`
- `handoff_notes`

## Rules

- Use stable identifiers.
- Keep tasks implementation-sized.
- Make acceptance criteria externally checkable.
- Reference the source spec or contract context where possible.
- Use `status`, `priority`, `milestone`, `lane`, `allowed_areas`, `blocks`, `proof_required`, `edge_cases`, `non_goals`, and `handoff_notes` when they make parallel work safer.

```

## `docs/verification-rules.md`

- Category: `review-doc`
- Purpose: Verification and frontend source-of-truth rules referenced by the generated planning state.
- Required: `true`

```markdown
# Verification Rules

## Structural Rules

- JSON outputs must validate against the schemas in `contracts/`.
- API route definitions must align with `contracts/api_contract.openapi.yaml`.
- Example artifacts must remain within the allowed scope in `PRODUCT_RULES.md`.

## Consistency Rules

- Repo plans must cover the responsibilities named in the project spec.
- Tasks must map to a repo target and owner role.
- Prompt packs must use the same scope boundaries as the spec.

## Frontend Rules

- The frontend must render source-of-truth artifacts directly.
- Missing fields should fail visibly, not be replaced with invented structure.

## Safety Rules

- Reject scopes that imply bots, account automation, emulator control, client memory access, or live service interference.
- Reject features that turn planning artifacts into hidden operational state.

## Red Team Targets

- scope inflation
- unsafe reinterpretation
- contract drift
- hidden frontend state invention
- unverifiable prompts

```

## `generated/context_pack.md`

- Category: `entry-point`
- Purpose: Single-file remote review context pack for web-only AI environments. Included as an entry point but skipped for self-embedding during context-pack generation.
- Required: `false`

_Skipped self-embedding to avoid recursive context-pack inclusion._

## `generated/project_spec.json`

- Category: `generated-state`
- Purpose: Canonical machine-readable product spec and frontend screen list, including Dispatch, Assignments, CollaborationState, and TaskRun concepts.
- Required: `true`

```json
{
  "project_name": "AI Assembly Line",
  "product_summary": {
    "goal": "Turn rough software ideas into structured, reviewable intake and planning artifacts before implementation begins.",
    "users": [
      "founders",
      "product leads",
      "technical planners",
      "engineering teams supervising AI-assisted work"
    ],
    "non_goals": [
      "interactive or mutable frontend implementation beyond the read-only static viewer",
      "authentication",
      "database persistence",
      "realtime sync",
      "background agent automation",
      "autonomous task claiming"
    ]
  },
  "safety_boundaries": [
    "The repository is planning-first and not an autonomous execution runtime.",
    "Human review is required before generated intake or planning artifacts are treated as approved.",
    "Unsafe requests must be rejected or safely reinterpreted into planning-only outputs.",
    "The initial frontend may render generated state but must not invent intake, task, repo, prompt, slot, planning-run, execution, or contract structure.",
    "The phase 0 seed must remain free of authentication, databases, realtime sync, and agent automation."
  ],
  "repo_split": [
    {
      "name": "seed-docs-and-rules",
      "purpose": "Store the human-readable phase 0 specification, product rules, intake workflow notes, workflow notes, execution workflow notes, and reusable planning template.",
      "contains": [
        "PROJECT_SPEC.md",
        "PROJECT_SPEC_TEMPLATE.md",
        "PRODUCT_RULES.md",
        "docs/"
      ],
      "depends_on": []
    },
    {
      "name": "seed-contracts",
      "purpose": "Define machine-readable contracts for intake records, project specs, repo plans, tasks, task runs, slots, prompts, file-based collaboration state, and future read-only APIs.",
      "contains": [
        "contracts/project_intake.schema.json",
        "contracts/*.schema.json",
        "contracts/api_contract.openapi.yaml"
      ],
      "depends_on": [
        "seed-docs-and-rules"
      ]
    },
    {
      "name": "seed-generated-state",
      "purpose": "Provide canonical generated artifacts, file-based execution coordination state, and derived planning-run indexes for the current seed repository state.",
      "contains": [
        "generated/project_spec.json",
        "generated/repo_plan.json",
        "generated/task_backlog.json",
        "generated/task_batch_index.json",
        "generated/collaboration_state.json",
        "generated/task_runs/",
        "generated/agent_prompts.json",
        "generated/slots_db.json",
        "generated/planning_runs_index.json"
      ],
      "depends_on": [
        "seed-docs-and-rules",
        "seed-contracts"
      ]
    },
    {
      "name": "seed-prompts",
      "purpose": "Store role-specific prompt source material aligned to the contracts, intake workflow, current project spec, task splitting, and task execution.",
      "contains": [
        "prompts/*.md"
      ],
      "depends_on": [
        "seed-docs-and-rules",
        "seed-contracts"
      ]
    },
    {
      "name": "seed-static-viewer",
      "purpose": "Own the static multi-page read-only viewer that consumes generated state directly without inventing new models.",
      "contains": [
        "web/index.html",
        "web/repos.html",
        "web/backlog.html",
        "web/dispatch.html",
        "web/assignments.html",
        "web/task-batches.html",
        "web/prompts.html",
        "web/slots.html",
        "web/planning-runs.html",
        "web/verification.html",
        "web/viewer-data.js",
        "web/viewer-layout.js",
        "web/page-*.js",
        "web/viewer.css",
        "web/README.md"
      ],
      "depends_on": [
        "seed-generated-state",
        "seed-contracts"
      ]
    }
  ],
  "domain_model": [
    {
      "name": "ProjectIntake",
      "fields": [
        "schema_version",
        "project_slug",
        "intake_mode",
        "project_goal",
        "target_users",
        "mvp",
        "target_platforms",
        "stack",
        "existing_project",
        "tools",
        "team_mode",
        "working_style",
        "constraints",
        "safety_boundaries",
        "assumptions",
        "open_questions",
        "acceptance_signals"
      ],
      "relations": [
        "ProjectIntake captures the guided interview result that feeds the Planning Agent before generated planning artifacts are produced."
      ]
    },
    {
      "name": "ProjectSpec",
      "fields": [
        "project_name",
        "product_summary",
        "safety_boundaries",
        "repo_split",
        "domain_model",
        "frontend_screens",
        "backend_services",
        "core_engine_responsibilities",
        "verification_tasks",
        "starter_prompts"
      ],
      "relations": [
        "ProjectSpec is produced after intake and drives RepoPlan, Task, CollaborationState, TaskRun, AgentPrompt, AgentSlot, and read-only planning-run index artifacts."
      ]
    },
    {
      "name": "RepoPlan",
      "fields": [
        "project_name",
        "repos"
      ],
      "relations": [
        "RepoPlan decomposes the project into contract-defined ownership units."
      ]
    },
    {
      "name": "Task",
      "fields": [
        "id",
        "title",
        "summary",
        "owner_role",
        "repo_target",
        "depends_on",
        "inputs",
        "outputs",
        "acceptance_criteria",
        "verification"
      ],
      "relations": [
        "Tasks trace back to RepoPlan units and verification goals."
      ]
    },
    {
      "name": "CollaborationState",
      "fields": [
        "schema_version",
        "workspace_id",
        "actors",
        "task_assignments",
        "task_claims",
        "artifact_submissions",
        "reviews",
        "audit_events"
      ],
      "relations": [
        "CollaborationState overlays assignment, status, notes, and proof references onto the canonical task backlog without becoming frontend-owned mutable state."
      ]
    },
    {
      "name": "TaskRun",
      "fields": [
        "schema_version",
        "task_id",
        "run_id",
        "actor_id",
        "status",
        "implementation_summary",
        "files_changed",
        "verification",
        "proof",
        "blockers",
        "updated_at"
      ],
      "relations": [
        "TaskRun records one executor completion or blocker report that can be referenced from CollaborationState proof."
      ]
    },
    {
      "name": "AgentPrompt",
      "fields": [
        "prompt_id",
        "role",
        "target_repo",
        "allowed_files",
        "forbidden_files",
        "input_context_required",
        "task_boundaries",
        "output_required",
        "verification_required"
      ],
      "relations": [
        "AgentPrompt constrains role behavior to project-approved inputs and outputs."
      ]
    },
    {
      "name": "AgentSlot",
      "fields": [
        "slot_id",
        "role",
        "status",
        "inputs",
        "outputs",
        "allowed_actions",
        "verification_requirements"
      ],
      "relations": [
        "AgentSlot is the operational slot view of role-scoped work against source-of-truth artifacts."
      ]
    },
    {
      "name": "PlanningRunIndex",
      "fields": [
        "schema_version",
        "generated_by",
        "planning_runs_path",
        "required_outputs",
        "runs"
      ],
      "relations": [
        "PlanningRunIndex is a derived read-only index of planning run folders, scaffold files, output presence, missing outputs, and run status."
      ]
    }
  ],
  "frontend_screens": [
    {
      "name": "Overview",
      "renders_from": [
        "PROJECT_SPEC.md",
        "generated/project_spec.json"
      ],
      "notes": "Read-only landing page summary of product goal, scope, and rules."
    },
    {
      "name": "Repo Split",
      "renders_from": [
        "generated/repo_plan.json"
      ],
      "notes": "Static repo ownership page that displays contract-defined ownership boundaries only."
    },
    {
      "name": "Task Backlog",
      "renders_from": [
        "generated/task_backlog.json"
      ],
      "notes": "Static backlog page that renders task cards directly from the generated backlog grouped by repo target."
    },
    {
      "name": "Dispatch",
      "renders_from": [
        "generated/task_backlog.json",
        "generated/collaboration_state.json",
        "generated/task_runs/"
      ],
      "notes": "Primary static what-can-I-do-next page. Groups tasks by topological dependency wave, colors available/locked/waiting/blocked/done state, and copies one-task execution context for a fresh AI chat."
    },
    {
      "name": "Task Assignments",
      "renders_from": [
        "generated/task_backlog.json",
        "generated/collaboration_state.json",
        "generated/task_runs/"
      ],
      "notes": "Static audit and status page for actors, assignment records, notes, and proof references. It may generate copy/download JSON but does not write state."
    },
    {
      "name": "Task Batches",
      "renders_from": [
        "generated/task_batch_index.json",
        "generated/task_batches/"
      ],
      "notes": "Static generation and validation page that renders batch index status, generated batch file readiness, task nodes, and dependency graph checks before batch output is merged into the canonical backlog."
    },
    {
      "name": "Prompt Pack",
      "renders_from": [
        "generated/agent_prompts.json"
      ],
      "notes": "Static prompts page that shows generated role prompts and contract-defined constraints."
    },
    {
      "name": "Slot Board",
      "renders_from": [
        "generated/slots_db.json"
      ],
      "notes": "Static slots page that renders the generated slot board without mutable workflow state."
    },
    {
      "name": "Planning Runs",
      "renders_from": [
        "generated/planning_runs_index.json"
      ],
      "notes": "Static planning-runs page that renders the derived planning-run index without editing or inventing planning-run state."
    },
    {
      "name": "Contracts and Verification",
      "renders_from": [
        "generated/project_spec.json",
        "generated/task_backlog.json",
        "generated/task_batch_index.json",
        "generated/collaboration_state.json",
        "generated/agent_prompts.json",
        "generated/slots_db.json",
        "contracts/project_intake.schema.json",
        "contracts/project_spec.schema.json",
        "contracts/repo_plan.schema.json",
        "contracts/task.schema.json",
        "contracts/task_batch_index.schema.json",
        "contracts/task_batch.schema.json",
        "contracts/task_run.schema.json",
        "contracts/slot.schema.json",
        "contracts/agent_prompt.schema.json",
        "contracts/collaboration_state.schema.json",
        "contracts/api_contract.openapi.yaml"
      ],
      "notes": "Static verification page that exposes generated verification requirements and renders raw contract files read-only without mutable workflow state."
    }
  ],
  "backend_services": [
    {
      "name": "read-only project state api draft",
      "responsibility": "Describe a future read-only API surface and future spec compiler draft contract without adding auth or persistence in phase 0.",
      "inputs": [
        "generated/*.json",
        "contracts/api_contract.openapi.yaml"
      ],
      "outputs": [
        "contract-defined read-only responses"
      ]
    },
    {
      "name": "seed validation utility",
      "responsibility": "Parse repository JSON artifacts and validate canonical generated state against contracts.",
      "inputs": [
        "contracts/*.schema.json",
        "generated/*.json",
        "examples/**/*.json"
      ],
      "outputs": [
        "validation report"
      ]
    }
  ],
  "core_engine_responsibilities": [
    "Capture guided intake outputs as structured source-of-truth inputs for planning.",
    "Compile rough planning intent into explicit project structure.",
    "Maintain contract-first generated artifacts for the seed repository.",
    "Derive planning-run indexes from file-based manual planning runs.",
    "Preserve traceability from product rules to intake, repo plan, tasks, prompts, slots, and planning-run readiness.",
    "Render Dispatch as a static source-of-truth view that helps humans pick available tasks without adding backend claiming, auth, realtime, or mutable frontend state.",
    "Reject or reinterpret unsafe scope expansion into planning-only outputs.",
    "Support deterministic validation of machine-readable seed artifacts."
  ],
  "verification_tasks": [
    "Parse every JSON file in the repository and fail clearly on invalid syntax.",
    "Validate canonical generated project state against the contracts in contracts/.",
    "Verify that project intake records conform to contracts/project_intake.schema.json when present.",
    "Verify that the generated artifacts stay aligned with the current phase 0 scope limits.",
    "Verify that future frontend work renders generated state and does not invent hidden models.",
    "Verify that the Dispatch page derives available, locked, waiting, blocked, and done states from task backlog plus collaboration state only.",
    "Verify that the planning-runs page renders only generated/planning_runs_index.json and does not mutate planning-run folders.",
    "Red-team prompt drift toward automation, auth, persistence, or realtime scope."
  ],
  "starter_prompts": {
    "intake_interviewer": "Guide the user from rough idea to structured project_intake.json by asking high-impact questions, suggesting stacks, and making safe assumptions.",
    "planning_agent": "Turn rough software ideas into a safe project spec, repo split, backlog, and prompt pack before implementation begins.",
    "contract_steward": "Maintain strict schemas and reject undocumented structure across project specs, repo plans, tasks, prompts, and slots.",
    "frontend_builder": "Build only read-only views that render generated state and contract-defined structure without inventing frontend-only models.",
    "backend_builder": "Define and later implement read-only contract-driven APIs only; do not add auth, databases, realtime sync, or mutable orchestration.",
    "core_engine_builder": "Keep planning compilation deterministic, traceable, and bounded to phase 0 artifact generation and validation.",
    "red_team_verifier": "Probe for unsafe reinterpretation, schema drift, invented frontend state, and any attempt to add forbidden phase 0 scope."
  }
}

```

## `generated/repo_plan.json`

- Category: `generated-state`
- Purpose: Canonical repo ownership split for the phase 0 seed.
- Required: `true`

```json
{
  "project_name": "AI Assembly Line",
  "repos": [
    {
      "name": "seed-docs-and-rules",
      "purpose": "Own the reusable planning spec template, human-readable product rules, project intake workflow, and phase 0 docs.",
      "contains": [
        "PROJECT_SPEC.md",
        "PROJECT_SPEC_TEMPLATE.md",
        "PRODUCT_RULES.md",
        "docs/"
      ],
      "depends_on": [],
      "excludes": [
        "runtime automation",
        "frontend implementation",
        "database state"
      ]
    },
    {
      "name": "seed-contracts",
      "purpose": "Own JSON schemas for intake and planning artifacts plus the future read-only API contract.",
      "contains": [
        "contracts/project_intake.schema.json",
        "contracts/project_spec.schema.json",
        "contracts/repo_plan.schema.json",
        "contracts/task.schema.json",
        "contracts/task_batch_index.schema.json",
        "contracts/task_batch.schema.json",
        "contracts/slot.schema.json",
        "contracts/agent_prompt.schema.json",
        "contracts/collaboration_state.schema.json",
        "contracts/api_contract.openapi.yaml"
      ],
      "depends_on": [
        "seed-docs-and-rules"
      ],
      "excludes": [
        "business logic",
        "invented consumer models"
      ]
    },
    {
      "name": "seed-generated-state",
      "purpose": "Own the canonical machine-readable planning artifacts and derived planning-run index consumed by read-only interfaces.",
      "contains": [
        "generated/project_spec.json",
        "generated/repo_plan.json",
        "generated/task_backlog.json",
        "generated/task_batch_index.json",
        "generated/task_batches/",
        "generated/agent_prompts.json",
        "generated/slots_db.json",
        "generated/planning_runs_index.json"
      ],
      "depends_on": [
        "seed-docs-and-rules",
        "seed-contracts"
      ],
      "excludes": [
        "schema drift",
        "undeclared JSON structures"
      ]
    },
    {
      "name": "seed-prompts",
      "purpose": "Own copy-paste role prompts constrained by the project spec, intake workflow, and contracts.",
      "contains": [
        "prompts/00-intake-interviewer.md",
        "prompts/00-planning-agent.md",
        "prompts/01-contract-steward.md",
        "prompts/02-frontend-builder.md",
        "prompts/03-backend-builder.md",
        "prompts/04-core-engine-builder.md",
        "prompts/05-red-team-verifier.md",
        "prompts/06-task-splitter.md"
      ],
      "depends_on": [
        "seed-docs-and-rules",
        "seed-contracts",
        "seed-generated-state"
      ],
      "excludes": [
        "self-authorized scope expansion",
        "unverified automation behavior"
      ]
    },
    {
      "name": "seed-static-viewer",
      "purpose": "Own the static multi-page read-only viewer that renders generated planning state directly from source-of-truth JSON files.",
      "contains": [
        "web/index.html",
        "web/repos.html",
        "web/backlog.html",
        "web/task-batches.html",
        "web/prompts.html",
        "web/slots.html",
        "web/planning-runs.html",
        "web/verification.html",
        "web/viewer-data.js",
        "web/viewer-layout.js",
        "web/page-*.js",
        "web/viewer.css",
        "web/README.md"
      ],
      "depends_on": [
        "seed-generated-state",
        "seed-contracts"
      ],
      "excludes": [
        "invented task or prompt structure",
        "authentication",
        "realtime sync",
        "mutable workflow state"
      ]
    }
  ]
}

```

## `generated/task_backlog.json`

- Category: `generated-state`
- Purpose: Canonical task backlog grouped by repo ownership targets and consumed by Dispatch.
- Required: `true`

```json
[
  {
    "id": "phase0-project-spec-template",
    "title": "Add reusable project spec template",
    "summary": "Create a reusable planning template for future project-planning runs with the required phase 0 sections.",
    "owner_role": "Planning Agent",
    "repo_target": "seed-docs-and-rules",
    "depends_on": [],
    "inputs": [
      "PROJECT_SPEC.md",
      "PRODUCT_RULES.md"
    ],
    "outputs": [
      "PROJECT_SPEC_TEMPLATE.md"
    ],
    "acceptance_criteria": [
      "The template contains every required section from the phase 0 hardening brief.",
      "The template reinforces contract-first planning and source-of-truth discipline."
    ],
    "verification": [
      "Manual review confirms the required headings are present."
    ],
    "risk_tags": [
      "template-drift"
    ]
  },
  {
    "id": "phase0-agent-prompt-contract",
    "title": "Add agent prompt schema",
    "summary": "Define a schema for generated role prompts so future prompt packs stay machine-readable and bounded.",
    "owner_role": "Contract Steward",
    "repo_target": "seed-contracts",
    "depends_on": [
      "phase0-project-spec-template"
    ],
    "inputs": [
      "PROJECT_SPEC.md",
      "prompts/"
    ],
    "outputs": [
      "contracts/agent_prompt.schema.json"
    ],
    "acceptance_criteria": [
      "The schema requires prompt id, role, repo target, file boundaries, context requirements, outputs, and verification requirements.",
      "Undocumented fields are rejected."
    ],
    "verification": [
      "generated/agent_prompts.json validates against the schema."
    ],
    "risk_tags": [
      "schema-drift"
    ]
  },
  {
    "id": "phase0-canonical-generated-state",
    "title": "Add canonical generated seed artifacts",
    "summary": "Create the generated project spec, repo plan, task backlog, prompt pack, and slot database for the current phase 0 seed.",
    "owner_role": "Planning Agent",
    "repo_target": "seed-generated-state",
    "depends_on": [
      "phase0-agent-prompt-contract"
    ],
    "inputs": [
      "PROJECT_SPEC.md",
      "PRODUCT_RULES.md",
      "contracts/"
    ],
    "outputs": [
      "generated/project_spec.json",
      "generated/repo_plan.json",
      "generated/task_backlog.json",
      "generated/agent_prompts.json",
      "generated/slots_db.json"
    ],
    "acceptance_criteria": [
      "Every generated file is valid JSON.",
      "The generated files match the current phase 0 scope and avoid forbidden runtime features.",
      "Task and slot records conform to the existing contracts."
    ],
    "verification": [
      "The seed validator parses all JSON files.",
      "Canonical generated artifacts validate against the contracts."
    ],
    "risk_tags": [
      "consistency",
      "scope-lock"
    ]
  },
  {
    "id": "phase0-seed-validator",
    "title": "Add repository JSON validation utility",
    "summary": "Create a lightweight validation script that parses every JSON file and schema-validates the canonical generated outputs.",
    "owner_role": "Backend Builder",
    "repo_target": "seed-contracts",
    "depends_on": [
      "phase0-canonical-generated-state"
    ],
    "inputs": [
      "contracts/*.schema.json",
      "generated/*.json",
      "examples/**/*.json"
    ],
    "outputs": [
      "tools/validate_seed.py"
    ],
    "acceptance_criteria": [
      "The validator reports every valid JSON file.",
      "Failures include the file path and parse or schema error detail.",
      "The script stays on the Python standard library except for optional jsonschema support."
    ],
    "verification": [
      "python tools/validate_seed.py exits successfully on the hardened seed."
    ],
    "risk_tags": [
      "tooling"
    ]
  },
  {
    "id": "phase0-readme-hardening",
    "title": "Document validation and frontend consumption rules",
    "summary": "Update the README so future contributors know how to validate the seed and what the frontend is allowed to consume.",
    "owner_role": "Frontend Builder",
    "repo_target": "seed-docs-and-rules",
    "depends_on": [
      "phase0-seed-validator"
    ],
    "inputs": [
      "README.md",
      "generated/*.json",
      "contracts/"
    ],
    "outputs": [
      "README.md"
    ],
    "acceptance_criteria": [
      "The README explains validation, source-of-truth files, and frontend rendering constraints.",
      "The README explicitly states that the frontend must not invent task, repo, prompt, slot, or contract structure."
    ],
    "verification": [
      "README.md contains the required hardening guidance."
    ],
    "risk_tags": [
      "documentation"
    ]
  }
]

```

## `generated/task_batch_index.json`

- Category: `generated-state`
- Purpose: Canonical index for copy-paste task generation batches, including batch order and expected task IDs.
- Required: `true`

```json
{
  "schema_version": "0.1.0",
  "source_plan_path": "generated_plan.md",
  "batching_strategy": "owner_role",
  "batches": []
}

```

## `generated/collaboration_state.json`

- Category: `generated-state`
- Purpose: File-based execution overlay for actors, task assignments, execution status, notes, and proof references.
- Required: `true`

```json
{
  "schema_version": "0.1.0",
  "workspace_id": "ai-assembly-line-seed",
  "generated_from": "generated/task_backlog.json",
  "actors": [
    {
      "actor_id": "human-nemo",
      "display_name": "Nemo",
      "kind": "human",
      "status": "active",
      "notes": "Human owner/operator for manual task assignment and review."
    },
    {
      "actor_id": "web-ai-task-executor",
      "display_name": "Web AI Task Executor",
      "kind": "web_ai",
      "status": "active",
      "notes": "Copy-paste AI executor working from one task JSON at a time."
    },
    {
      "actor_id": "local-ai-codex",
      "display_name": "Local AI / Codex",
      "kind": "local_ai",
      "status": "active",
      "notes": "Local repo-aware implementation agent."
    }
  ],
  "task_assignments": [],
  "task_claims": [],
  "artifact_submissions": [],
  "reviews": [],
  "audit_events": []
}

```

## `generated/task_runs/README.md`

- Category: `generated-state`
- Purpose: Directory note for per-task execution proof reports saved as generated/task_runs/<task_id>.json.
- Required: `true`

```markdown
Task run JSON files can be saved in this directory.

```

## `generated/agent_prompts.json`

- Category: `generated-state`
- Purpose: Canonical machine-readable prompt pack for the current seed, including the intake interviewer.
- Required: `true`

```json
{
  "project_name": "AI Assembly Line",
  "prompts": [
    {
      "prompt_id": "intake-interviewer-phase0",
      "role": "Intake Interviewer",
      "target_repo": "seed-docs-and-rules",
      "allowed_files": [
        "README.md",
        "PROJECT_SPEC_TEMPLATE.md",
        "PRODUCT_RULES.md",
        "docs/PROJECT_INTAKE_WORKFLOW.md",
        "docs/INTAKE_SESSION_FORMAT.md",
        "docs/INTAKE_DECISION_CARDS.md",
        "contracts/intake_session.schema.json",
        "contracts/project_intake.schema.json",
        "prompts/00-intake-interviewer.md"
      ],
      "forbidden_files": [
        "web/app/",
        "db/",
        "auth/",
        "workers/",
        "agents/runtime/"
      ],
      "input_context_required": [
        "User rough idea",
        "Project intake workflow",
        "Intake session format",
        "Intake decision card guidance",
        "Intake session schema",
        "Project intake schema",
        "Product rules",
        "Known tools, paths, stack preferences, or repo constraints"
      ],
      "task_boundaries": [
        "Treat rough ideas plus requests for help, guidelines, steering, architecture, or setup as requests to start intake.",
        "On the first response without a complete intake record, output only a short acknowledgement, compact human-readable intake status, and one high-impact guided-mode question, then stop.",
        "Do not print raw intake_session JSON by default; maintain schema-aligned state internally and show JSON only when requested, ready for project_intake, state review is needed, or saving/exporting/persisting.",
        "In guided mode, next_action.questions may contain only the single next question unless the user explicitly asks for a batch.",
        "For hard guided-mode choices, ask the single question as an A/B/C decision card with pros, cons, MVP risk, scaling/refactor risk, and one explicit agent recommendation.",
        "For the first high-impact MVP-boundary question of a rough idea, prefer a decision card when sensible options can be inferred.",
        "Allow the user to answer A, B, C, recommended, or custom; do not silently apply the recommendation.",
        "Use compact human-readable updates instead of repeating full JSON unless the user asks to see the full state.",
        "Keep future unanswered decisions in open_questions, not as a visible checklist in next_action.questions.",
        "Do not append starter guidelines, technical steering, repo/package split, definition of done, stack recommendation, suggested answers, task backlog, or agent assignments while readiness.can_generate_intake is false.",
        "Ask only questions that materially change the plan.",
        "Suggest stack options with tradeoffs only after intake has started and platform/MVP constraints make the suggestion safe.",
        "Produce a project_intake.json draft only after the intake session is ready.",
        "Do not produce implementation tasks until the intake record is complete enough."
      ],
      "output_required": [
        "Compact human-readable intake status on the first guided intake turn",
        "Compact intake update after subsequent guided-mode answers",
        "Decision card for hard guided-mode choices when useful, including first MVP-boundary choice when applicable",
        "Explicit assumptions",
        "High-risk open questions",
        "Single next high-impact question in guided mode",
        "Structured project_intake.json only when readiness.can_generate_intake is true",
        "Planning Agent hand-off summary only after project_intake.json is drafted"
      ],
      "verification_required": [
        "Internal intake session matches contracts/intake_session.schema.json.",
        "Guided-mode next_action.questions contains exactly one visible question unless the user explicitly asks for a batch.",
        "First rough-idea response does not dump raw intake_session JSON by default.",
        "Hard guided-mode choices include clear options with tradeoffs and an explicit recommendation when a decision card would help.",
        "Recommendation is not treated as accepted unless the user chooses it or answers recommended.",
        "Subsequent guided-mode turns do not repeat the full intake_session JSON unless requested, ready for project_intake, state review, or saving/exporting.",
        "No project_intake.json or planning artifacts are produced while readiness.can_generate_intake is false.",
        "First response to a rough idea does not include starter guidelines, technical steering, repo/package split, definition of done, stack recommendation, suggested answers, backlog, agent assignments, or a checklist of future questions.",
        "Final intake record matches contracts/project_intake.schema.json.",
        "Unsafe or ambiguous scope is rejected, bounded, or preserved as open questions."
      ]
    },
    {
      "prompt_id": "planning-agent-phase0",
      "role": "Planning Agent",
      "target_repo": "seed-generated-state",
      "allowed_files": [
        "PROJECT_SPEC.md",
        "PROJECT_SPEC_TEMPLATE.md",
        "PRODUCT_RULES.md",
        "docs/PLANNING_RUN_WORKFLOW.md",
        "docs/TASK_GENERATION_WORKFLOW.md",
        "docs/TASK_CARD_FORMAT.md",
        "generated/",
        "contracts/",
        "prompts/00-planning-agent.md"
      ],
      "forbidden_files": [
        "web/app/",
        "db/",
        "auth/",
        "workers/",
        "agents/runtime/"
      ],
      "input_context_required": [
        "Accepted project_intake.json when available",
        "Current phase specification",
        "Product rules",
        "Task generation workflow",
        "Task card format",
        "Existing contracts",
        "Repo plan or repo ownership assumptions"
      ],
      "task_boundaries": [
        "Produce planning artifacts only; do not implement the product.",
        "Do not generate implementation tasks from a rough idea alone; preserve missing high-risk intake answers as open questions or blocking tasks.",
        "Generate project_spec.json, repo_plan.json, task_backlog.json, agent_prompts.json, and slots_db.json only from accepted intake and source-of-truth files.",
        "Create shared contract/interface tasks before parallel client/backend/core implementation tasks.",
        "Keep MVP tasks distinct from post-MVP tasks, blocked tasks, and research/spike tasks.",
        "Do not add frontend implementation, auth, databases, realtime sync, or agent automation unless the accepted intake and repo plan require them.",
        "Keep outputs traceable to the source-of-truth spec and intake record."
      ],
      "output_required": [
        "Updated generated project state",
        "Accepted-intake summary",
        "Traceable repo split",
        "Parallel-safe task backlog",
        "Task dependencies by stable task ID",
        "Acceptance criteria and verification steps for every task",
        "Role/agent prompts derived from the backlog"
      ],
      "verification_required": [
        "Generated outputs remain within phase 0 scope.",
        "JSON artifacts parse successfully.",
        "Every task has an owner lane, repo target or allowed area, dependencies, acceptance criteria, and verification steps.",
        "Dependencies reference valid task IDs.",
        "Shared contract/interface tasks precede implementation tasks for parallel work.",
        "No task silently resolves an open high-risk intake question."
      ]
    },
    {
      "prompt_id": "contract-steward-phase0",
      "role": "Contract Steward",
      "target_repo": "seed-contracts",
      "allowed_files": [
        "contracts/",
        "generated/",
        "README.md"
      ],
      "forbidden_files": [
        "web/app/",
        "database/",
        "infra/"
      ],
      "input_context_required": [
        "Current project spec",
        "Generated artifacts",
        "Existing prompt files"
      ],
      "task_boundaries": [
        "Define strict contracts for machine-readable intake and planning artifacts.",
        "Reject undocumented fields unless explicitly approved in source-of-truth files."
      ],
      "output_required": [
        "Updated schemas",
        "Contract-consistent generated data"
      ],
      "verification_required": [
        "Canonical generated files validate against contracts.",
        "Schema additions preserve phase 0 scope boundaries."
      ]
    },
    {
      "prompt_id": "frontend-builder-phase0",
      "role": "Frontend Builder",
      "target_repo": "seed-static-viewer",
      "allowed_files": [
        "web/index.html",
        "web/repos.html",
        "web/backlog.html",
        "web/prompts.html",
        "web/slots.html",
        "web/planning-runs.html",
        "web/verification.html",
        "web/viewer-data.js",
        "web/viewer-layout.js",
        "web/page-*.js",
        "web/viewer.css",
        "web/README.md",
        "README.md",
        "generated/",
        "contracts/"
      ],
      "forbidden_files": [
        "web/app/",
        "generated/custom-ui-state.json",
        "database/",
        "auth/",
        "backend/",
        "realtime/"
      ],
      "input_context_required": [
        "Generated project spec",
        "Generated repo plan",
        "Generated task backlog",
        "Prompt schema"
      ],
      "task_boundaries": [
        "Render generated state directly.",
        "Do not invent task, repo, prompt, slot, intake, or contract structure.",
        "Do not change generated JSON structure or contracts unless explicitly assigned.",
        "Do not add backend routes, authentication, databases, realtime sync, or mutable workflow state."
      ],
      "output_required": [
        "Read-only rendering plan",
        "Consumer mapping from generated files to screens"
      ],
      "verification_required": [
        "Every rendered field traces to a source-of-truth file.",
        "Missing or invalid generated state fails visibly."
      ]
    },
    {
      "prompt_id": "backend-builder-phase0",
      "role": "Backend Builder",
      "target_repo": "seed-contracts",
      "allowed_files": [
        "contracts/",
        "tools/",
        "generated/"
      ],
      "forbidden_files": [
        "db/",
        "auth/",
        "workers/",
        "realtime/"
      ],
      "input_context_required": [
        "OpenAPI contract",
        "Generated state artifacts",
        "Validation rules"
      ],
      "task_boundaries": [
        "Support contract-first validation and future read-only interfaces only.",
        "Do not add persistence, authentication, or orchestration systems."
      ],
      "output_required": [
        "Validation tooling",
        "Read-only API planning inputs"
      ],
      "verification_required": [
        "Validation tooling reports parse and schema failures clearly.",
        "Outputs remain compatible with the declared contracts."
      ]
    },
    {
      "prompt_id": "core-engine-builder-phase0",
      "role": "Core Engine Builder",
      "target_repo": "seed-generated-state",
      "allowed_files": [
        "PROJECT_SPEC.md",
        "PRODUCT_RULES.md",
        "generated/",
        "contracts/"
      ],
      "forbidden_files": [
        "agents/runtime/",
        "workers/",
        "task-claimer/",
        "realtime/"
      ],
      "input_context_required": [
        "Current project specification",
        "Product rules",
        "Repo plan",
        "Project intake workflow"
      ],
      "task_boundaries": [
        "Stay within deterministic intake, planning compilation, and validation responsibilities.",
        "Do not build autonomous execution paths."
      ],
      "output_required": [
        "Deterministic generated planning artifacts",
        "Traceability notes across intake, contracts, and prompts"
      ],
      "verification_required": [
        "Artifacts stay deterministic and schema-aligned.",
        "No forbidden runtime scope is introduced."
      ]
    },
    {
      "prompt_id": "task-splitter-phase0",
      "role": "Task Splitter",
      "target_repo": "seed-prompts",
      "allowed_files": [
        "prompts/06-task-splitter.md",
        "docs/TASK_CREATION_GUIDE.md",
        "docs/TASK_GENERATION_WORKFLOW.md",
        "docs/TASK_CARD_FORMAT.md",
        "docs/task-format.md",
        "contracts/task.schema.json",
        "contracts/task_batch_index.schema.json",
        "contracts/task_batch.schema.json",
        "generated_plan.md",
        "generated/task_batch_index.json",
        "generated/task_batches/*.json",
        "generated/task_backlog.json"
      ],
      "forbidden_files": [
        "auth/",
        "db/",
        "workers/",
        "agents/runtime/"
      ],
      "input_context_required": [
        "Accepted generated plan",
        "Task creation guide",
        "Task generation workflow",
        "Task card format",
        "Task schema",
        "Repository split or ownership targets from the plan"
      ],
      "task_boundaries": [
        "Convert an accepted generated plan into schema-valid task batches.",
        "For large plans, use guided mode by producing a compact task_batch_index first and then one next task batch per continuation.",
        "Do not implement project code.",
        "Do not invent architecture, repositories, features, or scope beyond the accepted plan.",
        "Preserve high-risk open questions as blocking tasks or explicit context instead of silently deciding them.",
        "Create shared contract, protocol, schema, API, data model, or interface tasks before implementation tasks that consume them.",
        "Keep tasks small, verifiable, parallel-safe, and traceable to the accepted plan."
      ],
      "output_required": [
        "One copy-pastable fenced json code block per response",
        "Compact task_batch_index on the first guided response",
        "Valid task batch object for one next guided batch per continuation",
        "Task records conforming to contracts/task.schema.json in each batch",
        "Dependencies by stable task ID",
        "Repo targets from the accepted plan",
        "Acceptance criteria and verification for every task",
        "Proof requirements, edge cases, non-goals, and estimated size when useful"
      ],
      "verification_required": [
        "Guided output contains exactly one json code block plus only short Save to and Next instructions outside it.",
        "Batch index output contains no full task objects.",
        "Task batch output parses as a JSON object with a tasks array.",
        "Every task in each batch conforms to contracts/task.schema.json.",
        "Every dependency refers to a generated task ID.",
        "Every task has concrete acceptance criteria and verification.",
        "No task expands beyond the accepted MVP or contradicts explicit non-goals."
      ]
    },
    {
      "prompt_id": "red-team-verifier-phase0",
      "role": "Red Team Verifier",
      "target_repo": "seed-docs-and-rules",
      "allowed_files": [
        "PROJECT_SPEC.md",
        "PRODUCT_RULES.md",
        "docs/",
        "generated/",
        "contracts/"
      ],
      "forbidden_files": [
        "production-secrets/",
        "auth/",
        "db/"
      ],
      "input_context_required": [
        "Project rules",
        "Generated artifacts",
        "Prompt pack",
        "Intake workflow",
        "Task generation workflow"
      ],
      "task_boundaries": [
        "Search for unsafe reinterpretation, schema drift, hidden state invention, intake ambiguity, and task-generation overreach.",
        "Keep review findings tied to current contracts and source-of-truth files."
      ],
      "output_required": [
        "Attack cases",
        "Rejection rationale",
        "Verification gaps"
      ],
      "verification_required": [
        "Attack cases cover auth, database, realtime, automation, intake overreach, invented frontend state drift, and vague task backlogs.",
        "Each finding maps to a rule or contract boundary."
      ]
    }
  ]
}

```

## `generated/slots_db.json`

- Category: `generated-state`
- Purpose: Canonical slot board data consumed by the static viewer.
- Required: `true`

```json
[
  {
    "slot_id": "planning-agent-slot",
    "role": "Planning Agent",
    "status": "ready",
    "inputs": [
      "PROJECT_SPEC.md",
      "PROJECT_SPEC_TEMPLATE.md",
      "PRODUCT_RULES.md",
      "contracts/"
    ],
    "outputs": [
      "generated/project_spec.json",
      "generated/repo_plan.json",
      "generated/task_backlog.json"
    ],
    "allowed_actions": [
      "compile spec state",
      "update generated artifacts",
      "preserve scope boundaries"
    ],
    "verification_requirements": [
      "Artifacts trace back to the product spec.",
      "No forbidden phase 0 scope is introduced."
    ],
    "notes": "Planning slot for contract-first decomposition only."
  },
  {
    "slot_id": "contract-steward-slot",
    "role": "Contract Steward",
    "status": "ready",
    "inputs": [
      "contracts/",
      "generated/",
      "prompts/"
    ],
    "outputs": [
      "contracts/agent_prompt.schema.json",
      "schema-aligned generated artifacts"
    ],
    "allowed_actions": [
      "edit schemas",
      "tighten validation rules",
      "reject undocumented structure"
    ],
    "verification_requirements": [
      "Canonical generated files validate against contracts.",
      "Schema changes remain traceable to the current spec."
    ]
  },
  {
    "slot_id": "frontend-builder-slot",
    "role": "Frontend Builder",
    "status": "planned",
    "inputs": [
      "generated/project_spec.json",
      "generated/repo_plan.json",
      "generated/task_backlog.json",
      "generated/agent_prompts.json",
      "generated/slots_db.json"
    ],
    "outputs": [
      "read-only frontend rendering plan"
    ],
    "allowed_actions": [
      "render generated state",
      "map screens to source files",
      "surface contract failures"
    ],
    "verification_requirements": [
      "The frontend does not invent task, repo, prompt, slot, or contract structure.",
      "Every displayed field maps to a source-of-truth artifact."
    ]
  },
  {
    "slot_id": "backend-builder-slot",
    "role": "Backend Builder",
    "status": "planned",
    "inputs": [
      "contracts/api_contract.openapi.yaml",
      "contracts/*.schema.json",
      "generated/*.json"
    ],
    "outputs": [
      "validation tooling",
      "future read-only API plan"
    ],
    "allowed_actions": [
      "parse generated state",
      "validate contract alignment",
      "prepare read-only interfaces"
    ],
    "verification_requirements": [
      "No auth or database dependencies are added.",
      "Tooling reports failures clearly."
    ]
  },
  {
    "slot_id": "core-engine-builder-slot",
    "role": "Core Engine Builder",
    "status": "planned",
    "inputs": [
      "PROJECT_SPEC.md",
      "PRODUCT_RULES.md",
      "generated/project_spec.json"
    ],
    "outputs": [
      "deterministic planning compiler behaviors"
    ],
    "allowed_actions": [
      "enforce deterministic planning transforms",
      "preserve traceability",
      "support validation"
    ],
    "verification_requirements": [
      "Core logic remains planning-only.",
      "Generated outputs stay deterministic."
    ]
  },
  {
    "slot_id": "red-team-verifier-slot",
    "role": "Red Team Verifier",
    "status": "planned",
    "inputs": [
      "PROJECT_SPEC.md",
      "PRODUCT_RULES.md",
      "generated/",
      "contracts/"
    ],
    "outputs": [
      "red-team attack cases",
      "rejection notes"
    ],
    "allowed_actions": [
      "probe boundary drift",
      "test unsafe reinterpretation",
      "review frontend source-of-truth discipline"
    ],
    "verification_requirements": [
      "Attack cases cover automation, auth, persistence, realtime sync, and hidden frontend state.",
      "Findings reference the triggering rule or contract."
    ]
  }
]

```

## `generated/planning_runs_index.json`

- Category: `generated-state`
- Purpose: Derived index of manual planning-run folders, scaffold presence, output completeness, and run status.
- Required: `true`

```json
{
  "schema_version": "0.1.0",
  "generated_by": "tools/build_planning_runs_index.py",
  "planning_runs_path": "planning_runs",
  "required_outputs": [
    "project_spec.json",
    "repo_plan.json",
    "task_backlog.json",
    "agent_prompts.json",
    "slots_db.json"
  ],
  "runs": [
    {
      "slug": "coc-base-builder-v1",
      "path": "planning_runs/coc-base-builder-v1",
      "status": "draft_missing_outputs",
      "has_input_idea": true,
      "has_planning_prompt": true,
      "has_review_notes": true,
      "has_outputs_dir": true,
      "outputs": {
        "project_spec.json": false,
        "repo_plan.json": false,
        "task_backlog.json": false,
        "agent_prompts.json": false,
        "slots_db.json": false
      },
      "missing_outputs": [
        "project_spec.json",
        "repo_plan.json",
        "task_backlog.json",
        "agent_prompts.json",
        "slots_db.json"
      ],
      "missing_scaffold": []
    }
  ]
}

```

## `generated/review_manifest.json`

- Category: `generated-state`
- Purpose: Remote review manifest listing the key files needed to inspect the repository without a full clone.
- Required: `true`

```json
{
  "project_name": "AI Assembly Line",
  "review_files": [
    {
      "path": "README.md",
      "category": "root-doc",
      "purpose": "Repository overview, source-of-truth rules, intake workflow, Dispatch workflow, viewer constraints, validation guidance, and remote AI review links.",
      "required": true
    },
    {
      "path": "PROJECT_SPEC.md",
      "category": "root-doc",
      "purpose": "Human-readable phase 0 product specification covering guided intake, planning, execution-coordination artifacts, and current viewer scope.",
      "required": true
    },
    {
      "path": "PROJECT_SPEC_TEMPLATE.md",
      "category": "root-doc",
      "purpose": "Reusable planning template that shows the intended product-spec structure.",
      "required": false
    },
    {
      "path": "PRODUCT_RULES.md",
      "category": "root-doc",
      "purpose": "Hard product rules, scope boundaries, and frontend source-of-truth constraints.",
      "required": true
    },
    {
      "path": ".gitignore",
      "category": "repo-config",
      "purpose": "Local noise and generated cache ignore rules, including local tasks_created.json scratch output.",
      "required": false
    },
    {
      "path": "docs/AI_CONTEXT.md",
      "category": "review-doc",
      "purpose": "Remote AI review entry guidance for environments that cannot clone or run shell commands.",
      "required": true
    },
    {
      "path": "docs/EXTERNAL_REVIEW_PROMPT.md",
      "category": "review-doc",
      "purpose": "External reviewer instructions, including clone and no-clone fallback flows.",
      "required": true
    },
    {
      "path": "docs/public-overview.md",
      "category": "review-doc",
      "purpose": "Short public-facing overview of the planning-kernel repository scope.",
      "required": true
    },
    {
      "path": "docs/workflow.md",
      "category": "review-doc",
      "purpose": "Workflow description for decomposition, tasks, prompts, and verification.",
      "required": true
    },
    {
      "path": "docs/PROJECT_INTAKE_WORKFLOW.md",
      "category": "review-doc",
      "purpose": "Interactive intake workflow for turning a rough idea into an intake_session.json state and then a structured project_intake.json record before planning.",
      "required": true
    },
    {
      "path": "docs/INTAKE_SESSION_FORMAT.md",
      "category": "review-doc",
      "purpose": "Interactive intake-session response format and first-turn hard-stop rules for rough project requests.",
      "required": true
    },
    {
      "path": "docs/INTAKE_DECISION_CARDS.md",
      "category": "review-doc",
      "purpose": "Decision-card guidance for one-question guided intake choices with A/B/C options, tradeoffs, MVP risk, scaling risk, and explicit recommendations.",
      "required": true
    },
    {
      "path": "docs/PLANNING_RUN_WORKFLOW.md",
      "category": "review-doc",
      "purpose": "Manual planning-run workflow for turning a rough idea or intake record into saved planning artifacts and human-reviewed outputs.",
      "required": true
    },
    {
      "path": "docs/TASK_GENERATION_WORKFLOW.md",
      "category": "review-doc",
      "purpose": "Workflow for turning an accepted intake record into parallel-safe task_backlog.json tasks with dependencies and verification.",
      "required": true
    },
    {
      "path": "docs/EXECUTION_WORKFLOW.md",
      "category": "review-doc",
      "purpose": "File-based execution loop for task assignments, executor prompts, task_run reports, and proof review without backend persistence.",
      "required": true
    },
    {
      "path": "docs/VIEWER_PAGE_ROLES.md",
      "category": "review-doc",
      "purpose": "Dispatch/Assignments/Task Batches page-role split, making Dispatch the primary what-can-I-do-next surface.",
      "required": true
    },
    {
      "path": "docs/TASK_CREATION_GUIDE.md",
      "category": "review-doc",
      "purpose": "Generic schema-aligned guide for creating implementation-ready tasks with ownership, status, priority, proof, edge cases, and non-goals.",
      "required": true
    },
    {
      "path": "docs/TASK_CARD_FORMAT.md",
      "category": "review-doc",
      "purpose": "Task-card format guidance for small, owned, bounded, dependency-aware, verifiable, parallel-safe tasks.",
      "required": true
    },
    {
      "path": "docs/roles.md",
      "category": "review-doc",
      "purpose": "Role descriptions for the planning kernel and static viewer work.",
      "required": true
    },
    {
      "path": "docs/task-format.md",
      "category": "review-doc",
      "purpose": "Task record expectations referenced by generated planning artifacts.",
      "required": true
    },
    {
      "path": "docs/verification-rules.md",
      "category": "review-doc",
      "purpose": "Verification and frontend source-of-truth rules referenced by the generated planning state.",
      "required": true
    },
    {
      "path": "generated/context_pack.md",
      "category": "entry-point",
      "purpose": "Single-file remote review context pack for web-only AI environments. Included as an entry point but skipped for self-embedding during context-pack generation.",
      "required": false
    },
    {
      "path": "generated/project_spec.json",
      "category": "generated-state",
      "purpose": "Canonical machine-readable product spec and frontend screen list, including Dispatch, Assignments, CollaborationState, and TaskRun concepts.",
      "required": true
    },
    {
      "path": "generated/repo_plan.json",
      "category": "generated-state",
      "purpose": "Canonical repo ownership split for the phase 0 seed.",
      "required": true
    },
    {
      "path": "generated/task_backlog.json",
      "category": "generated-state",
      "purpose": "Canonical task backlog grouped by repo ownership targets and consumed by Dispatch.",
      "required": true
    },
    {
      "path": "generated/task_batch_index.json",
      "category": "generated-state",
      "purpose": "Canonical index for copy-paste task generation batches, including batch order and expected task IDs.",
      "required": true
    },
    {
      "path": "generated/collaboration_state.json",
      "category": "generated-state",
      "purpose": "File-based execution overlay for actors, task assignments, execution status, notes, and proof references.",
      "required": true
    },
    {
      "path": "generated/task_runs/README.md",
      "category": "generated-state",
      "purpose": "Directory note for per-task execution proof reports saved as generated/task_runs/<task_id>.json.",
      "required": true
    },
    {
      "path": "generated/agent_prompts.json",
      "category": "generated-state",
      "purpose": "Canonical machine-readable prompt pack for the current seed, including the intake interviewer.",
      "required": true
    },
    {
      "path": "generated/slots_db.json",
      "category": "generated-state",
      "purpose": "Canonical slot board data consumed by the static viewer.",
      "required": true
    },
    {
      "path": "generated/planning_runs_index.json",
      "category": "generated-state",
      "purpose": "Derived index of manual planning-run folders, scaffold presence, output completeness, and run status.",
      "required": true
    },
    {
      "path": "generated/review_manifest.json",
      "category": "generated-state",
      "purpose": "Remote review manifest listing the key files needed to inspect the repository without a full clone.",
      "required": true
    },
    {
      "path": "contracts/intake_session.schema.json",
      "category": "contract",
      "purpose": "Schema for interactive intake_session.json state produced before project_intake.json exists.",
      "required": true
    },
    {
      "path": "contracts/project_intake.schema.json",
      "category": "contract",
      "purpose": "Schema for guided project intake records produced before planning runs.",
      "required": true
    },
    {
      "path": "contracts/project_spec.schema.json",
      "category": "contract",
      "purpose": "Schema for the generated machine-readable project spec.",
      "required": true
    },
    {
      "path": "contracts/repo_plan.schema.json",
      "category": "contract",
      "purpose": "Schema for the generated repository plan.",
      "required": true
    },
    {
      "path": "contracts/task.schema.json",
      "category": "contract",
      "purpose": "Schema for each generated task backlog entry.",
      "required": true
    },
    {
      "path": "contracts/task_batch_index.schema.json",
      "category": "contract",
      "purpose": "Schema for the task batch index used by large copy-paste task-generation workflows.",
      "required": true
    },
    {
      "path": "contracts/task_batch.schema.json",
      "category": "contract",
      "purpose": "Schema for one generated task batch file under generated/task_batches/.",
      "required": true
    },
    {
      "path": "contracts/task_run.schema.json",
      "category": "contract",
      "purpose": "Schema for one per-task executor completion/proof report saved under generated/task_runs/.",
      "required": true
    },
    {
      "path": "contracts/slot.schema.json",
      "category": "contract",
      "purpose": "Schema for each generated slot board entry.",
      "required": true
    },
    {
      "path": "contracts/agent_prompt.schema.json",
      "category": "contract",
      "purpose": "Schema for the generated agent prompt pack.",
      "required": true
    },
    {
      "path": "contracts/collaboration_state.schema.json",
      "category": "contract",
      "purpose": "Schema for file-based coordination state: actors, task assignments, claims, artifact submissions, reviews, proof references, and audit events.",
      "required": true
    },
    {
      "path": "contracts/api_contract.openapi.yaml",
      "category": "contract",
      "purpose": "Future API and spec-compiler contract draft, not an implemented backend.",
      "required": true
    },
    {
      "path": "prompts/00-intake-interviewer.md",
      "category": "prompt-source",
      "purpose": "Prompt source file for the guided intake interviewer role.",
      "required": true
    },
    {
      "path": "prompts/00-planning-agent.md",
      "category": "prompt-source",
      "purpose": "Prompt source file for the planning agent role.",
      "required": true
    },
    {
      "path": "prompts/01-contract-steward.md",
      "category": "prompt-source",
      "purpose": "Prompt source file for the contract steward role.",
      "required": true
    },
    {
      "path": "prompts/02-frontend-builder.md",
      "category": "prompt-source",
      "purpose": "Prompt source file for the Phase 0 frontend builder role.",
      "required": true
    },
    {
      "path": "prompts/03-backend-builder.md",
      "category": "prompt-source",
      "purpose": "Prompt source file for the backend builder role.",
      "required": true
    },
    {
      "path": "prompts/04-core-engine-builder.md",
      "category": "prompt-source",
      "purpose": "Prompt source file for the core engine builder role.",
      "required": true
    },
    {
      "path": "prompts/05-red-team-verifier.md",
      "category": "prompt-source",
      "purpose": "Prompt source file for the red-team verifier role.",
      "required": true
    },
    {
      "path": "prompts/06-task-splitter.md",
      "category": "prompt-source",
      "purpose": "Copy-paste prompt template for converting an accepted generated plan into schema-valid task batches.",
      "required": true
    },
    {
      "path": "prompts/07-task-executor.md",
      "category": "prompt-source",
      "purpose": "Copy-paste prompt template for executing exactly one task and returning a task_run JSON proof report.",
      "required": true
    },
    {
      "path": "examples/coc-base-builder/input-idea.md",
      "category": "example",
      "purpose": "Example input idea used to demonstrate safe decomposition in a domain-specific sample.",
      "required": false
    },
    {
      "path": "examples/coc-base-builder/generated-project-spec.md",
      "category": "example",
      "purpose": "Human-readable example project spec output for the coc-base-builder sample.",
      "required": false
    },
    {
      "path": "examples/coc-base-builder/generated-repo-plan.json",
      "category": "example",
      "purpose": "Machine-readable example repo-plan output for the coc-base-builder sample.",
      "required": false
    },
    {
      "path": "examples/coc-base-builder/generated-task-backlog.json",
      "category": "example",
      "purpose": "Machine-readable example task backlog output for the coc-base-builder sample.",
      "required": false
    },
    {
      "path": "examples/coc-base-builder/generated-agent-prompts.md",
      "category": "example",
      "purpose": "Human-readable example prompt pack output for the coc-base-builder sample.",
      "required": false
    },
    {
      "path": "planning_runs/README.md",
      "category": "workflow",
      "purpose": "Explains planning-run folders and what run artifacts should be committed.",
      "required": true
    },
    {
      "path": "planning_runs/coc-base-builder-v1/input-idea.md",
      "category": "workflow-example",
      "purpose": "Safe sample planning-run input idea for an offline strategy-game base layout planner.",
      "required": true
    },
    {
      "path": "planning_runs/coc-base-builder-v1/planning-run.md",
      "category": "workflow-example",
      "purpose": "Sample generated planning-run prompt for the safe coc-base-builder-v1 run.",
      "required": true
    },
    {
      "path": "planning_runs/coc-base-builder-v1/outputs/README.md",
      "category": "workflow-example",
      "purpose": "Explains that the five required JSON outputs are intentionally absent until a planning agent produces them.",
      "required": true
    },
    {
      "path": "planning_runs/coc-base-builder-v1/review-notes.md",
      "category": "workflow-example",
      "purpose": "Sample review-notes scaffold for the coc-base-builder-v1 planning run.",
      "required": true
    },
    {
      "path": "web/README.md",
      "category": "viewer",
      "purpose": "Static viewer documentation, page-role split, Dispatch workflow notes, and file:// versus local server usage notes.",
      "required": true
    },
    {
      "path": "web/index.html",
      "category": "viewer",
      "purpose": "Overview page entry point for the static viewer.",
      "required": true
    },
    {
      "path": "web/repos.html",
      "category": "viewer",
      "purpose": "Repository split page entry point.",
      "required": true
    },
    {
      "path": "web/backlog.html",
      "category": "viewer",
      "purpose": "Backlog page entry point.",
      "required": true
    },
    {
      "path": "web/dispatch.html",
      "category": "viewer",
      "purpose": "Dispatch page entry point for topological what-can-I-do-next task pickup and execution-context copying.",
      "required": true
    },
    {
      "path": "web/assignments.html",
      "category": "viewer",
      "purpose": "Assignments page entry point for read-only execution ownership, status, notes, and proof review.",
      "required": true
    },
    {
      "path": "web/task-batches.html",
      "category": "viewer",
      "purpose": "Task batches page entry point for batch index status, batch file readiness, task nodes, and dependency graph checks.",
      "required": true
    },
    {
      "path": "web/prompts.html",
      "category": "viewer",
      "purpose": "Prompts page entry point.",
      "required": true
    },
    {
      "path": "web/slots.html",
      "category": "viewer",
      "purpose": "Slots page entry point.",
      "required": true
    },
    {
      "path": "web/planning-runs.html",
      "category": "viewer",
      "purpose": "Planning-runs page entry point that renders the derived planning-run index read-only.",
      "required": true
    },
    {
      "path": "web/verification.html",
      "category": "viewer",
      "purpose": "Verification page entry point that also renders raw contract files read-only.",
      "required": true
    },
    {
      "path": "web/viewer-data.js",
      "category": "viewer",
      "purpose": "Shared generated-data and contract-loading helpers for the static viewer.",
      "required": true
    },
    {
      "path": "web/viewer-layout.js",
      "category": "viewer",
      "purpose": "Shared viewer shell, status handling, navigation, and reusable rendering helpers.",
      "required": true
    },
    {
      "path": "web/page-overview.js",
      "category": "viewer",
      "purpose": "Overview page rendering logic.",
      "required": true
    },
    {
      "path": "web/page-repos.js",
      "category": "viewer",
      "purpose": "Repository split page rendering logic.",
      "required": true
    },
    {
      "path": "web/page-backlog.js",
      "category": "viewer",
      "purpose": "Backlog page rendering logic.",
      "required": true
    },
    {
      "path": "web/page-dispatch.js",
      "category": "viewer",
      "purpose": "Dispatch page rendering logic for topological task waves, availability state, task detail, and execution-context copying.",
      "required": true
    },
    {
      "path": "web/page-dispatch-keyboard.js",
      "category": "viewer",
      "purpose": "Keyboard helper that maps Enter/Space on focused dispatch nodes to click activation.",
      "required": true
    },
    {
      "path": "web/page-assignments.js",
      "category": "viewer",
      "purpose": "Assignments page rendering logic for task ownership, execution status, notes, and proof references.",
      "required": true
    },
    {
      "path": "web/page-assignment-tools.js",
      "category": "viewer",
      "purpose": "Static copy/download helper for generated collaboration state and executor prompts without writing files.",
      "required": true
    },
    {
      "path": "web/page-task-batches.js",
      "category": "viewer",
      "purpose": "Task batches page rendering logic for batch index status, batch file readiness, task nodes, and dependency graph checks.",
      "required": true
    },
    {
      "path": "web/page-prompts.js",
      "category": "viewer",
      "purpose": "Prompts page rendering logic.",
      "required": true
    },
    {
      "path": "web/page-slots.js",
      "category": "viewer",
      "purpose": "Slots page rendering logic.",
      "required": true
    },
    {
      "path": "web/page-planning-runs.js",
      "category": "viewer",
      "purpose": "Planning-runs page rendering logic for scaffold presence, output completeness, and run status.",
      "required": true
    },
    {
      "path": "web/page-verification.js",
      "category": "viewer",
      "purpose": "Verification page rendering logic, including raw contract display.",
      "required": true
    },
    {
      "path": "web/viewer.css",
      "category": "viewer",
      "purpose": "Shared static viewer styles, including dispatch state and focus/active styling.",
      "required": true
    },
    {
      "path": "tools/validate_seed.py",
      "category": "tool",
      "purpose": "Dependency-light validation script for generated JSON, contracts, and traceability consistency.",
      "required": true
    },
    {
      "path": "tools/build_context_pack.py",
      "category": "tool",
      "purpose": "Builds the remote-review context pack from this manifest.",
      "required": true
    },
    {
      "path": "tools/init_planning_run.py",
      "category": "tool",
      "purpose": "Initializes a manual planning-run folder and refreshes the AI-ready planning prompt.",
      "required": true
    },
    {
      "path": "tools/validate_planning_run.py",
      "category": "tool",
      "purpose": "Validates saved planning-run output artifacts against existing contracts and cross-artifact consistency checks.",
      "required": true
    },
    {
      "path": "tools/build_planning_runs_index.py",
      "category": "tool",
      "purpose": "Builds the derived planning-runs index consumed by later read-only review surfaces.",
      "required": true
    },
    {
      "path": "tools/validate_task_batches.py",
      "category": "tool",
      "purpose": "Validates task batch files, task dependency graph references, and topological batch order.",
      "required": true
    },
    {
      "path": "tools/build_task_backlog_from_batches.py",
      "category": "tool",
      "purpose": "Merges validated generated task batches into canonical generated/task_backlog.json while refusing empty-batch overwrites.",
      "required": true
    },
    {
      "path": "tools/validate_collaboration_state.py",
      "category": "tool",
      "purpose": "Validates file-based collaboration state, task assignments, and task run proof reports against the canonical backlog and actor list.",
      "required": true
    },
    {
      "path": "tools/sync_and_check.ps1",
      "category": "tool",
      "purpose": "Local helper that pulls GitHub-side changes, rebuilds generated indexes/context, validates artifacts, and reports status.",
      "required": false
    }
  ]
}

```

## `contracts/intake_session.schema.json`

- Category: `contract`
- Purpose: Schema for interactive intake_session.json state produced before project_intake.json exists.
- Required: `true`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/ai-assembly-line/intake_session.schema.json",
  "title": "IntakeSession",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "project_slug",
    "mode",
    "status",
    "current_section",
    "sections",
    "stack_options",
    "assumptions",
    "open_questions",
    "readiness",
    "next_action"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "minLength": 1
    },
    "project_slug": {
      "type": "string",
      "pattern": "^[a-z0-9][a-z0-9-]*$"
    },
    "mode": {
      "type": "string",
      "enum": ["quick", "guided", "expert"]
    },
    "status": {
      "type": "string",
      "enum": ["not_started", "in_progress", "ready_for_intake_record", "intake_record_drafted", "blocked"]
    },
    "current_section": {
      "type": "string",
      "minLength": 1
    },
    "sections": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "label", "status", "questions"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^[a-z0-9][a-z0-9-]*$"
          },
          "label": {
            "type": "string",
            "minLength": 1
          },
          "status": {
            "type": "string",
            "enum": ["not_started", "in_progress", "complete", "blocked", "skipped"]
          },
          "questions": {
            "type": "array",
            "items": {
              "type": "object",
              "additionalProperties": false,
              "required": ["id", "question", "answer", "risk_level", "affects"],
              "properties": {
                "id": {
                  "type": "string",
                  "pattern": "^[a-z0-9][a-z0-9-]*$"
                },
                "question": {
                  "type": "string",
                  "minLength": 1
                },
                "answer": {
                  "type": "string"
                },
                "risk_level": {
                  "type": "string",
                  "enum": ["low", "medium", "high"]
                },
                "affects": {
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1
                  }
                }
              }
            }
          }
        }
      }
    },
    "stack_options": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["name", "best_for", "risks", "recommendation_level"],
        "properties": {
          "name": {
            "type": "string",
            "minLength": 1
          },
          "best_for": {
            "type": "string",
            "minLength": 1
          },
          "risks": {
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1
            }
          },
          "recommendation_level": {
            "type": "string",
            "enum": ["recommended", "acceptable", "not_recommended", "unknown"]
          }
        }
      }
    },
    "assumptions": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      }
    },
    "open_questions": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["question", "risk_if_unanswered"],
        "properties": {
          "question": {
            "type": "string",
            "minLength": 1
          },
          "risk_if_unanswered": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    },
    "readiness": {
      "type": "object",
      "additionalProperties": false,
      "required": ["can_generate_intake", "missing_high_risk_answers"],
      "properties": {
        "can_generate_intake": {
          "type": "boolean"
        },
        "missing_high_risk_answers": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    },
    "next_action": {
      "type": "object",
      "additionalProperties": false,
      "required": ["type", "questions"],
      "properties": {
        "type": {
          "type": "string",
          "enum": ["ask_questions", "suggest_stack", "draft_project_intake", "handoff_to_planning", "blocked"]
        },
        "questions": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    }
  }
}

```

## `contracts/project_intake.schema.json`

- Category: `contract`
- Purpose: Schema for guided project intake records produced before planning runs.
- Required: `true`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/ai-assembly-line/project_intake.schema.json",
  "title": "ProjectIntake",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "project_slug",
    "intake_mode",
    "project_goal",
    "target_users",
    "mvp",
    "target_platforms",
    "stack",
    "existing_project",
    "team_mode",
    "working_style",
    "constraints",
    "safety_boundaries",
    "assumptions",
    "open_questions",
    "acceptance_signals"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "minLength": 1
    },
    "project_slug": {
      "type": "string",
      "pattern": "^[a-z0-9][a-z0-9-]*$"
    },
    "intake_mode": {
      "type": "string",
      "enum": ["quick", "guided", "expert"]
    },
    "project_goal": {
      "type": "string",
      "minLength": 1
    },
    "target_users": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      }
    },
    "mvp": {
      "type": "object",
      "additionalProperties": false,
      "required": ["summary", "must_have", "postponed"],
      "properties": {
        "summary": {
          "type": "string",
          "minLength": 1
        },
        "must_have": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          }
        },
        "postponed": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    },
    "target_platforms": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      }
    },
    "stack": {
      "type": "object",
      "additionalProperties": false,
      "required": ["preference", "recommendation", "options", "decision_status"],
      "properties": {
        "preference": {
          "type": "string"
        },
        "recommendation": {
          "type": "string"
        },
        "decision_status": {
          "type": "string",
          "enum": ["user_selected", "ai_recommended", "undecided"]
        },
        "options": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["name", "best_for", "risks"],
            "properties": {
              "name": {
                "type": "string",
                "minLength": 1
              },
              "best_for": {
                "type": "string",
                "minLength": 1
              },
              "risks": {
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1
                }
              }
            }
          }
        }
      }
    },
    "existing_project": {
      "type": "object",
      "additionalProperties": false,
      "required": ["state", "path", "notes"],
      "properties": {
        "state": {
          "type": "string",
          "enum": ["greenfield", "existing_repo", "unknown"]
        },
        "path": {
          "type": "string"
        },
        "notes": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    },
    "tools": {
      "type": "array",
      "default": [],
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["name", "path", "configuration", "notes"],
        "properties": {
          "name": {
            "type": "string",
            "minLength": 1
          },
          "path": {
            "type": "string"
          },
          "configuration": {
            "type": "string"
          },
          "notes": {
            "type": "string"
          }
        }
      }
    },
    "team_mode": {
      "type": "object",
      "additionalProperties": false,
      "required": ["humans", "ai_agents", "parallelization_goal"],
      "properties": {
        "humans": {
          "type": "integer",
          "minimum": 0
        },
        "ai_agents": {
          "type": "integer",
          "minimum": 0
        },
        "parallelization_goal": {
          "type": "string"
        }
      }
    },
    "working_style": {
      "type": "object",
      "additionalProperties": false,
      "required": ["task_size", "review_style", "proof_required"],
      "properties": {
        "task_size": {
          "type": "string",
          "enum": ["small", "medium", "large", "mixed"]
        },
        "review_style": {
          "type": "string"
        },
        "proof_required": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    },
    "constraints": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      }
    },
    "safety_boundaries": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      }
    },
    "assumptions": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      }
    },
    "open_questions": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["question", "risk_if_unanswered"],
        "properties": {
          "question": {
            "type": "string",
            "minLength": 1
          },
          "risk_if_unanswered": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    },
    "acceptance_signals": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      }
    }
  }
}

```

## `contracts/project_spec.schema.json`

- Category: `contract`
- Purpose: Schema for the generated machine-readable project spec.
- Required: `true`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://ai-assembly-line.local/contracts/project_spec.schema.json",
  "title": "ProjectSpec",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "project_name",
    "product_summary",
    "safety_boundaries",
    "repo_split",
    "domain_model",
    "frontend_screens",
    "backend_services",
    "core_engine_responsibilities",
    "verification_tasks",
    "starter_prompts"
  ],
  "properties": {
    "project_name": {
      "type": "string",
      "minLength": 1
    },
    "product_summary": {
      "type": "object",
      "additionalProperties": false,
      "required": ["goal", "users", "non_goals"],
      "properties": {
        "goal": { "type": "string" },
        "users": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "non_goals": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "safety_boundaries": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "repo_split": {
      "type": "array",
      "items": { "$ref": "#/$defs/repoUnit" },
      "minItems": 1
    },
    "domain_model": {
      "type": "array",
      "items": { "$ref": "#/$defs/domainEntity" },
      "minItems": 1
    },
    "frontend_screens": {
      "type": "array",
      "items": { "$ref": "#/$defs/screen" },
      "minItems": 1
    },
    "backend_services": {
      "type": "array",
      "items": { "$ref": "#/$defs/service" },
      "minItems": 1
    },
    "core_engine_responsibilities": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "verification_tasks": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "starter_prompts": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "intake_interviewer",
        "planning_agent",
        "contract_steward",
        "frontend_builder",
        "backend_builder",
        "core_engine_builder",
        "red_team_verifier"
      ],
      "properties": {
        "intake_interviewer": { "type": "string" },
        "planning_agent": { "type": "string" },
        "contract_steward": { "type": "string" },
        "frontend_builder": { "type": "string" },
        "backend_builder": { "type": "string" },
        "core_engine_builder": { "type": "string" },
        "red_team_verifier": { "type": "string" }
      }
    }
  },
  "$defs": {
    "repoUnit": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "purpose", "contains", "depends_on"],
      "properties": {
        "name": { "type": "string" },
        "purpose": { "type": "string" },
        "contains": { "type": "array", "items": { "type": "string" } },
        "depends_on": { "type": "array", "items": { "type": "string" } }
      }
    },
    "domainEntity": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "fields"],
      "properties": {
        "name": { "type": "string" },
        "fields": { "type": "array", "items": { "type": "string" } },
        "relations": { "type": "array", "items": { "type": "string" } }
      }
    },
    "screen": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "renders_from"],
      "properties": {
        "name": { "type": "string" },
        "renders_from": { "type": "array", "items": { "type": "string" } },
        "notes": { "type": "string" }
      }
    },
    "service": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "responsibility"],
      "properties": {
        "name": { "type": "string" },
        "responsibility": { "type": "string" },
        "inputs": { "type": "array", "items": { "type": "string" } },
        "outputs": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}

```

## `contracts/repo_plan.schema.json`

- Category: `contract`
- Purpose: Schema for the generated repository plan.
- Required: `true`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://ai-assembly-line.local/contracts/repo_plan.schema.json",
  "title": "RepoPlan",
  "type": "object",
  "additionalProperties": false,
  "required": ["project_name", "repos"],
  "properties": {
    "project_name": {
      "type": "string",
      "minLength": 1
    },
    "repos": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["name", "purpose", "contains", "depends_on", "excludes"],
        "properties": {
          "name": { "type": "string" },
          "purpose": { "type": "string" },
          "contains": { "type": "array", "items": { "type": "string" } },
          "depends_on": { "type": "array", "items": { "type": "string" } },
          "excludes": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  }
}

```

## `contracts/task.schema.json`

- Category: `contract`
- Purpose: Schema for each generated task backlog entry.
- Required: `true`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://ai-assembly-line.local/contracts/task.schema.json",
  "title": "Task",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "id",
    "title",
    "summary",
    "owner_role",
    "repo_target",
    "depends_on",
    "inputs",
    "outputs",
    "acceptance_criteria",
    "verification"
  ],
  "properties": {
    "id": { "type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9\\-]*$" },
    "title": { "type": "string", "minLength": 1 },
    "summary": { "type": "string", "minLength": 1 },
    "objective": { "type": "string", "minLength": 1 },
    "context": { "type": "string", "minLength": 1 },
    "owner_role": { "type": "string", "minLength": 1 },
    "lane": { "type": "string", "minLength": 1 },
    "repo_target": { "type": "string", "minLength": 1 },
    "status": {
      "type": "string",
      "enum": ["draft", "ready", "in_progress", "blocked", "review", "done", "rejected"]
    },
    "priority": {
      "type": "string",
      "enum": ["P0", "P1", "P2", "P3"]
    },
    "milestone": { "type": "string", "minLength": 1 },
    "allowed_areas": { "type": "array", "items": { "type": "string", "minLength": 1 } },
    "depends_on": { "type": "array", "items": { "type": "string" } },
    "blocks": { "type": "array", "items": { "type": "string" } },
    "inputs": { "type": "array", "items": { "type": "string" } },
    "outputs": { "type": "array", "items": { "type": "string" } },
    "implementation_notes": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "acceptance_criteria": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "verification": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "proof_required": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "edge_cases": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "non_goals": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "estimated_size": {
      "type": "string",
      "enum": ["S", "M", "L"]
    },
    "risk_tags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "notes": {
      "type": "string"
    },
    "handoff_notes": {
      "type": "string"
    }
  }
}

```

## `contracts/task_batch_index.schema.json`

- Category: `contract`
- Purpose: Schema for the task batch index used by large copy-paste task-generation workflows.
- Required: `true`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://ai-assembly-line.local/contracts/task_batch_index.schema.json",
  "title": "TaskBatchIndex",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "source_plan_path",
    "batching_strategy",
    "batches"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "minLength": 1
    },
    "source_plan_path": {
      "type": "string",
      "minLength": 1
    },
    "batching_strategy": {
      "type": "string",
      "enum": ["owner_role", "repo_target", "lane", "milestone", "mixed"]
    },
    "batches": {
      "type": "array",
      "items": { "$ref": "#/$defs/batch" }
    }
  },
  "$defs": {
    "batch": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "batch_id",
        "owner_role",
        "repo_targets",
        "lanes",
        "milestones",
        "expected_task_count",
        "expected_task_ids",
        "depends_on_batches",
        "output_path",
        "status"
      ],
      "properties": {
        "batch_id": {
          "type": "string",
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "owner_role": {
          "type": "string",
          "minLength": 1
        },
        "repo_targets": {
          "type": "array",
          "items": { "type": "string", "minLength": 1 }
        },
        "lanes": {
          "type": "array",
          "items": { "type": "string", "minLength": 1 }
        },
        "milestones": {
          "type": "array",
          "items": { "type": "string", "minLength": 1 }
        },
        "expected_task_count": {
          "type": "integer",
          "minimum": 0
        },
        "expected_task_ids": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^[A-Za-z0-9][A-Za-z0-9\\-]*$"
          }
        },
        "depends_on_batches": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^[a-z0-9][a-z0-9\\-]*$"
          }
        },
        "output_path": {
          "type": "string",
          "pattern": "^generated/task_batches/[a-z0-9][a-z0-9\\-]*\\.json$"
        },
        "status": {
          "type": "string",
          "enum": ["planned", "generated", "validated", "accepted", "rejected"]
        },
        "notes": {
          "type": "string"
        }
      }
    }
  }
}

```

## `contracts/task_batch.schema.json`

- Category: `contract`
- Purpose: Schema for one generated task batch file under generated/task_batches/.
- Required: `true`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://ai-assembly-line.local/contracts/task_batch.schema.json",
  "title": "TaskBatch",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "batch_id",
    "source_plan_path",
    "tasks"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "minLength": 1
    },
    "batch_id": {
      "type": "string",
      "pattern": "^[a-z0-9][a-z0-9\\-]*$"
    },
    "source_plan_path": {
      "type": "string",
      "minLength": 1
    },
    "tasks": {
      "type": "array",
      "items": {
        "$ref": "./task.schema.json"
      }
    }
  }
}

```

## `contracts/task_run.schema.json`

- Category: `contract`
- Purpose: Schema for one per-task executor completion/proof report saved under generated/task_runs/.
- Required: `true`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://ai-assembly-line.local/contracts/task_run.schema.json",
  "title": "TaskRun",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "task_id",
    "run_id",
    "actor_id",
    "status",
    "implementation_summary",
    "files_changed",
    "verification",
    "proof",
    "blockers",
    "updated_at"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "minLength": 1
    },
    "task_id": {
      "type": "string",
      "pattern": "^[A-Za-z0-9][A-Za-z0-9\\-]*$"
    },
    "run_id": {
      "type": "string",
      "pattern": "^[A-Za-z0-9][A-Za-z0-9\\-]*$"
    },
    "actor_id": {
      "type": "string",
      "pattern": "^[a-z0-9][a-z0-9\\-]*$"
    },
    "status": {
      "type": "string",
      "enum": ["review", "done", "blocked", "failed"]
    },
    "implementation_summary": {
      "type": "string",
      "minLength": 1
    },
    "files_changed": {
      "type": "array",
      "items": { "$ref": "#/$defs/file_change" }
    },
    "verification": {
      "type": "array",
      "items": { "$ref": "#/$defs/verification_result" }
    },
    "proof": {
      "type": "array",
      "items": { "$ref": "#/$defs/proof_entry" }
    },
    "blockers": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "notes": {
      "type": "string"
    },
    "submitted_at": {
      "type": "string",
      "format": "date-time"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "$defs": {
    "file_change": {
      "type": "object",
      "additionalProperties": false,
      "required": ["path", "change"],
      "properties": {
        "path": {
          "type": "string",
          "minLength": 1
        },
        "change": {
          "type": "string",
          "minLength": 1
        }
      }
    },
    "verification_result": {
      "type": "object",
      "additionalProperties": false,
      "required": ["command", "result"],
      "properties": {
        "command": {
          "type": "string",
          "minLength": 1
        },
        "result": {
          "type": "string",
          "enum": ["passed", "failed", "not_run", "manual"]
        },
        "output": {
          "type": "string"
        }
      }
    },
    "proof_entry": {
      "type": "object",
      "additionalProperties": false,
      "required": ["kind", "summary"],
      "properties": {
        "kind": {
          "type": "string",
          "enum": ["command_output", "test_output", "screenshot", "log", "file", "manual_note"]
        },
        "path": {
          "type": "string",
          "minLength": 1
        },
        "summary": {
          "type": "string",
          "minLength": 1
        },
        "status": {
          "type": "string",
          "enum": ["passed", "failed", "accepted", "needs_review"]
        },
        "recorded_at": {
          "type": "string",
          "format": "date-time"
        }
      }
    }
  }
}

```

## `contracts/slot.schema.json`

- Category: `contract`
- Purpose: Schema for each generated slot board entry.
- Required: `true`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://ai-assembly-line.local/contracts/slot.schema.json",
  "title": "AgentSlot",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "slot_id",
    "role",
    "status",
    "inputs",
    "outputs",
    "allowed_actions",
    "verification_requirements"
  ],
  "properties": {
    "slot_id": {
      "type": "string",
      "pattern": "^[a-z0-9\\-]+$"
    },
    "role": {
      "type": "string",
      "minLength": 1
    },
    "status": {
      "type": "string",
      "enum": ["planned", "ready", "active", "blocked", "review", "complete"]
    },
    "inputs": {
      "type": "array",
      "items": { "type": "string" }
    },
    "outputs": {
      "type": "array",
      "items": { "type": "string" }
    },
    "allowed_actions": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "verification_requirements": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "notes": {
      "type": "string"
    }
  }
}

```

## `contracts/agent_prompt.schema.json`

- Category: `contract`
- Purpose: Schema for the generated agent prompt pack.
- Required: `true`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://ai-assembly-line.local/contracts/agent_prompt.schema.json",
  "title": "AgentPromptSet",
  "type": "object",
  "additionalProperties": false,
  "required": ["project_name", "prompts"],
  "properties": {
    "project_name": {
      "type": "string",
      "minLength": 1
    },
    "prompts": {
      "type": "array",
      "minItems": 1,
      "items": {
        "$ref": "#/$defs/agentPrompt"
      }
    }
  },
  "$defs": {
    "agentPrompt": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "prompt_id",
        "role",
        "target_repo",
        "allowed_files",
        "forbidden_files",
        "input_context_required",
        "task_boundaries",
        "output_required",
        "verification_required"
      ],
      "properties": {
        "prompt_id": {
          "type": "string",
          "pattern": "^[a-z0-9\\-]+$"
        },
        "role": {
          "type": "string",
          "minLength": 1
        },
        "target_repo": {
          "type": "string",
          "minLength": 1
        },
        "allowed_files": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          }
        },
        "forbidden_files": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          }
        },
        "input_context_required": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          },
          "minItems": 1
        },
        "task_boundaries": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          },
          "minItems": 1
        },
        "output_required": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          },
          "minItems": 1
        },
        "verification_required": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          },
          "minItems": 1
        }
      }
    }
  }
}

```

## `contracts/collaboration_state.schema.json`

- Category: `contract`
- Purpose: Schema for file-based coordination state: actors, task assignments, claims, artifact submissions, reviews, proof references, and audit events.
- Required: `true`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://ai-assembly-line.local/contracts/collaboration_state.schema.json",
  "title": "CollaborationState",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "workspace_id",
    "actors",
    "task_assignments",
    "task_claims",
    "artifact_submissions",
    "reviews",
    "audit_events"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "minLength": 1
    },
    "workspace_id": {
      "type": "string",
      "pattern": "^[a-z0-9][a-z0-9\\-]*$"
    },
    "generated_from": {
      "type": "string",
      "minLength": 1
    },
    "actors": {
      "type": "array",
      "items": { "$ref": "#/$defs/actor" }
    },
    "task_assignments": {
      "type": "array",
      "items": { "$ref": "#/$defs/task_assignment" }
    },
    "task_claims": {
      "type": "array",
      "items": { "$ref": "#/$defs/task_claim" }
    },
    "artifact_submissions": {
      "type": "array",
      "items": { "$ref": "#/$defs/artifact_submission" }
    },
    "reviews": {
      "type": "array",
      "items": { "$ref": "#/$defs/review" }
    },
    "audit_events": {
      "type": "array",
      "items": { "$ref": "#/$defs/audit_event" }
    }
  },
  "$defs": {
    "actor": {
      "type": "object",
      "additionalProperties": false,
      "required": ["actor_id", "display_name", "kind", "status"],
      "properties": {
        "actor_id": {
          "type": "string",
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "display_name": {
          "type": "string",
          "minLength": 1
        },
        "kind": {
          "type": "string",
          "enum": ["human", "web_ai", "local_ai", "service"]
        },
        "status": {
          "type": "string",
          "enum": ["active", "inactive", "blocked"]
        },
        "notes": {
          "type": "string"
        }
      }
    },
    "task_assignment": {
      "type": "object",
      "additionalProperties": false,
      "required": ["task_id", "status", "updated_at"],
      "properties": {
        "task_id": {
          "type": "string",
          "pattern": "^[A-Za-z0-9][A-Za-z0-9\\-]*$"
        },
        "assigned_to": {
          "type": ["string", "null"],
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "assignee_type": {
          "type": "string",
          "enum": ["human", "web_ai", "local_ai", "service", "unassigned"]
        },
        "assignee_label": {
          "type": "string"
        },
        "status": {
          "type": "string",
          "enum": ["unclaimed", "claimed", "in_progress", "review", "done", "blocked", "released"]
        },
        "claimed_at": {
          "type": "string",
          "format": "date-time"
        },
        "proof": {
          "type": "array",
          "items": { "$ref": "#/$defs/proof_ref" }
        },
        "notes": {
          "type": "string"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time"
        }
      }
    },
    "proof_ref": {
      "type": "object",
      "additionalProperties": false,
      "required": ["kind", "summary"],
      "properties": {
        "kind": {
          "type": "string",
          "enum": ["command_output", "test_output", "screenshot", "log", "file", "manual_note", "task_run"]
        },
        "path": {
          "type": "string",
          "minLength": 1
        },
        "summary": {
          "type": "string",
          "minLength": 1
        },
        "status": {
          "type": "string",
          "enum": ["pending", "passed", "failed", "accepted", "needs_review"]
        },
        "recorded_at": {
          "type": "string",
          "format": "date-time"
        }
      }
    },
    "task_claim": {
      "type": "object",
      "additionalProperties": false,
      "required": ["claim_id", "task_id", "actor_id", "status", "claimed_at"],
      "properties": {
        "claim_id": {
          "type": "string",
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "task_id": {
          "type": "string",
          "pattern": "^[A-Za-z0-9][A-Za-z0-9\\-]*$"
        },
        "actor_id": {
          "type": "string",
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "status": {
          "type": "string",
          "enum": ["claimed", "in_progress", "blocked", "submitted", "released"]
        },
        "claimed_at": {
          "type": "string",
          "format": "date-time"
        },
        "released_at": {
          "type": "string",
          "format": "date-time"
        },
        "notes": {
          "type": "string"
        }
      }
    },
    "artifact_submission": {
      "type": "object",
      "additionalProperties": false,
      "required": ["submission_id", "task_id", "actor_id", "artifact_paths", "status", "submitted_at"],
      "properties": {
        "submission_id": {
          "type": "string",
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "task_id": {
          "type": "string",
          "pattern": "^[A-Za-z0-9][A-Za-z0-9\\-]*$"
        },
        "actor_id": {
          "type": "string",
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "artifact_paths": {
          "type": "array",
          "minItems": 1,
          "items": { "type": "string", "minLength": 1 }
        },
        "summary": {
          "type": "string"
        },
        "proof": {
          "type": "array",
          "items": { "$ref": "#/$defs/proof_ref" }
        },
        "status": {
          "type": "string",
          "enum": ["submitted", "needs_revision", "accepted", "rejected"]
        },
        "submitted_at": {
          "type": "string",
          "format": "date-time"
        }
      }
    },
    "review": {
      "type": "object",
      "additionalProperties": false,
      "required": ["review_id", "submission_id", "reviewer_actor_id", "status", "findings"],
      "properties": {
        "review_id": {
          "type": "string",
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "submission_id": {
          "type": "string",
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "reviewer_actor_id": {
          "type": "string",
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "status": {
          "type": "string",
          "enum": ["pending", "approved", "changes_requested", "rejected"]
        },
        "findings": {
          "type": "array",
          "items": { "type": "string", "minLength": 1 }
        },
        "reviewed_at": {
          "type": "string",
          "format": "date-time"
        }
      }
    },
    "audit_event": {
      "type": "object",
      "additionalProperties": false,
      "required": ["event_id", "actor_id", "event_type", "target_id", "created_at"],
      "properties": {
        "event_id": {
          "type": "string",
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "actor_id": {
          "type": "string",
          "pattern": "^[a-z0-9][a-z0-9\\-]*$"
        },
        "event_type": {
          "type": "string",
          "enum": ["claim_created", "claim_released", "assignment_updated", "artifact_submitted", "review_added", "status_changed"]
        },
        "target_id": {
          "type": "string",
          "minLength": 1
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "details": {
          "type": "string"
        }
      }
    }
  }
}

```

## `contracts/api_contract.openapi.yaml`

- Category: `contract`
- Purpose: Future API and spec-compiler contract draft, not an implemented backend.
- Required: `true`

```yaml
openapi: 3.1.0
info:
  title: AI Assembly Line API Contract
  version: 0.1.0
  description: >
    Seed API contract draft for future read-only project-state access and future spec compilation.
    This file documents planned interfaces only and does not imply an implemented backend in the current Phase 0 repository.
servers:
  - url: http://localhost:3000
paths:
  /project-spec:
    get:
      summary: Get the current machine-readable project spec
      operationId: getProjectSpec
      responses:
        "200":
          description: Project spec document
          content:
            application/json:
              schema:
                $ref: "./project_spec.schema.json"
  /repo-plan:
    get:
      summary: Get the current repo split
      operationId: getRepoPlan
      responses:
        "200":
          description: Repo plan document
          content:
            application/json:
              schema:
                $ref: "./repo_plan.schema.json"
  /tasks:
    get:
      summary: Get the current task backlog
      operationId: getTaskBacklog
      responses:
        "200":
          description: Array of task documents
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "./task.schema.json"
  /slots:
    get:
      summary: Get planned or active agent slots
      operationId: getSlots
      responses:
        "200":
          description: Array of slot documents
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "./slot.schema.json"
  /collaboration-state:
    get:
      summary: Get the current collaboration state draft
      description: >
        Future workflow surface for coordinating humans and web-based AI agents.
        This is a contract draft only; it does not imply an implemented backend in the current Phase 0 repository.
      operationId: getCollaborationState
      responses:
        "200":
          description: Collaboration state document
          content:
            application/json:
              schema:
                $ref: "./collaboration_state.schema.json"
  /compile-spec:
    post:
      summary: Compile a rough idea into a structured project spec draft
      description: >
        Future spec compiler draft route only. This path is not implemented by the current Phase 0 repository
        and remains a contract-first planning artifact.
      operationId: compileSpec
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              additionalProperties: false
              required:
                - raw_idea
              properties:
                raw_idea:
                  type: string
      responses:
        "200":
          description: Structured project spec draft
          content:
            application/json:
              schema:
                $ref: "./project_spec.schema.json"

```

## `prompts/00-intake-interviewer.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the guided intake interviewer role.
- Required: `true`

```markdown
# Intake Interviewer Prompt

You are the Intake Interviewer for AI Assembly Line.

Your job is to guide a user from a rough project idea to an interactive `intake_session` state and then to a structured `project_intake.json` record before the Planning Agent creates the implementation plan.

You are not implementing the product. You are not producing the full task backlog yet. You are asking the minimum useful set of questions, making safe assumptions where appropriate, and preparing a clean hand-off to the Planning Agent.

## Critical start-request rule

When a user provides only a rough idea and asks for help, guidelines, planning, architecture, or how to bring the project to life, treat that as a request to start intake.

A request for `guidelines`, `project guidelines`, `steering help`, `starter rules`, `recommendations`, or `how should we set this up` is still a start-intake request when the user has only provided a rough idea. Do not treat those words as permission to write guidelines before intake is ready.

Do not output any of the following on the first turn unless a complete intake record already exists:

- full project guidelines
- temporary or starter project guidelines
- technical steering rules
- target repository layout
- repo/package split
- definition of done
- suggested answers or default answers for the user to accept
- full architecture
- final stack decision
- full MVP scope
- full task backlog
- agent assignments
- implementation code

Instead, output:

1. a short acknowledgement
2. a compact human-readable intake status summary
3. the next high-impact question, preferably as a decision card when the choice affects MVP difficulty or later scaling/refactor risk

Then stop. If `readiness.can_generate_intake` is `false`, do not add any extra guidance after the question.

Keep the internal `intake_session` state aligned with `contracts/intake_session.schema.json`, but do not dump the raw JSON unless the user asks for it, the state is ready for `project_intake.json`, or a save/export/persist step is requested.

This rule exists so the AI does not jump the gun and pretend high-risk project decisions are already known.

## First-turn hard stop

For a rough idea with no complete intake record, the entire response must fit this envelope:

1. Short acknowledgement.
2. Compact intake status summary.
3. One next high-impact user-facing question.

After the question, stop the response.

Do not print a raw `intake_session` JSON object on the first turn by default. Use a human-readable status card such as:

```text
Intake status: started
Project: shared-grocery-list
Known: tiny shared grocery list app for two people
Still needed: MVP boundary
```

Do not append sections with headings like:

- `Starter steering rules`
- `Starter guidelines`
- `Temporary project rules`
- `Technical steering`
- `Recommended stack`
- `Repo/package split`
- `Definition of done`
- `Suggested answers`
- `My suggested answers`
- `Next planning run`
- `Project guidelines`

Even if the user explicitly asks for guidelines, say that guidelines come after the missing high-risk intake answers.

## Inputs to read first

When available, read:

- `docs/PROJECT_INTAKE_WORKFLOW.md`
- `docs/INTAKE_SESSION_FORMAT.md`
- `docs/INTAKE_DECISION_CARDS.md`
- `contracts/intake_session.schema.json`
- `contracts/project_intake.schema.json`
- `PROJECT_SPEC_TEMPLATE.md`
- `PRODUCT_RULES.md`
- the user's rough idea
- any local tool paths, stack preferences, existing repo notes, or configuration details supplied by the user

## Core behavior

Use the ask/assume/stop rule:

- Ask when an answer changes architecture, stack, MVP, safety, or parallelization.
- Assume when the missing detail is low-risk and easy to revise later.
- Stop and ask when a missing answer is high-risk.

Do not ask questions forever. The goal is to get enough information to create a useful first planning run.

## One-question guided intake rule

In guided mode, ask exactly one user-facing question per turn.

The `next_action.questions` array may contain only the single next question unless:

- the user explicitly asks for multiple questions,
- the mode is `quick`,
- the mode is `expert` and the user has requested a batch review.

Do not show future queued questions as a visible list. Keep future unknowns in `open_questions`, not in `next_action.questions`.

The first user-facing response to a rough idea should ask the first high-impact question immediately after the compact intake status summary and then stop.

## Human-readable guided update rule

In guided mode, do not print the full `intake_session` JSON by default.

Show the full `intake_session` object only when:

- the user explicitly asks to see the JSON/session state,
- the session becomes ready to draft `project_intake.json`,
- the state has become ambiguous and needs explicit review, or
- saving/exporting/persisting the state is the requested output.

For normal guided turns, use a compact intake update instead of raw JSON. The compact update should include only:

- the answer just recorded, if any,
- the current section/status if useful,
- any newly unlocked next action,
- the single next user-facing question.

Keep the full updated state internally consistent with `contracts/intake_session.schema.json`, but do not display the entire object unless one of the cases above applies.

## Decision-card guided questions

In guided mode, the assistant still asks exactly one user-facing question per turn.

For hard choices, present that one question as a decision card with A/B/C options. Use decision cards when the answer affects MVP difficulty, later scaling pain, architecture, stack, platform target, backend model, team split, or verification strategy.

The first high-impact MVP-boundary question for a rough idea should normally be a decision card, not a bare sentence, when obvious options can be inferred safely.

A decision card should include:

- the single decision being made,
- two or three options labeled A/B/C,
- what each option means,
- pros,
- cons,
- MVP risk,
- later scaling or refactor risk,
- when that option is best,
- one `Agent recommendation`, with rationale.

The user may answer `A`, `B`, `C`, `recommended`, or a custom answer.

If the user answers `recommended`, record the recommended option as the selected answer and preserve the recommendation rationale. Do not silently choose the recommendation without user confirmation.

Decision cards still count as one guided question. Do not turn them into a checklist of multiple future questions. Keep future decisions in `open_questions`.

## Intake modes

If the user does not specify a mode, default to guided mode.

### Quick mode

Ask at most five questions. Make assumptions explicit. Produce a draft intake record quickly.

### Guided mode

Ask exactly one high-impact question per turn. Use compact human-readable updates instead of raw JSON unless the user asks for the state. For hard choices, use A/B/C decision cards with pros, cons, MVP risk, scaling/refactor risk, and one explicit agent recommendation. Suggest options only when the current `next_action.type` is `suggest_stack` or when enough high-risk platform and multiplayer answers are known. Confirm the MVP and stack direction before producing the intake record.

### Expert mode

Accept pasted constraints, paths, stack choices, architecture notes, and team layout. Ask only for missing high-risk decisions.

## High-risk questions

Stop and ask instead of assuming when unclear:

- Is this greenfield or an existing repository?
- What platform matters first?
- Is multiplayer real-time, turn-based, local, or online?
- Is there a required framework, engine, SDK, or hardware target?
- Are external accounts, credentials, scraping, platform APIs, games, bots, or automation involved?
- How many humans or AI agents should work in parallel?
- What proof is required for a task to count as done?

## Stack suggestion behavior

If the user has not chosen a stack, you may ask whether they want a recommendation.

Do not include concrete stack recommendations on the first response to a rough project idea when high-risk answers are still missing. In that case, leave `stack_options` empty and ask a question such as `Do you already prefer a stack, or should I recommend one after platform and multiplayer scope are clear?`

Only suggest two or three stack options with tradeoffs when:

- the user explicitly asks to compare stacks after intake has started,
- the session `next_action.type` is `suggest_stack`, or
- enough platform and MVP constraints are known that the suggestion will not silently decide architecture.

For each option, include:

- best fit
- risks
- why it may or may not fit the user's working style
- MVP risk
- later scaling or refactor risk

Then give a recommendation, but do not silently force it. The user may choose the recommendation by saying `recommended`.

Example shape:

```text
Decision: Which stack direction should the MVP use?

A) Godot 4
Best for: fast 2D game iteration and desktop-first prototypes.
Pros: strong game tooling; quick visual iteration.
Cons: browser deployment and backend integration may need extra care.
MVP risk: low-medium.
Scaling/refactor risk: medium if web/mobile later become important.

B) TypeScript + Phaser + Colyseus
Best for: browser-first multiplayer.
Pros: easy sharing and strong web multiplayer path.
Cons: more web/backend setup before game feel is visible.
MVP risk: medium.
Scaling/refactor risk: low-medium for web-first projects.

Agent recommendation: B if browser-first multiplayer matters most; A if desktop-first game-feel iteration matters most.

Question: Choose A, B, recommended, or custom.
```

## Intake session state

While intake is in progress, maintain an internal `intake_session` object matching `contracts/intake_session.schema.json`.

The internal session should include:

- current section
- questions already asked
- answers received so far
- stack options, if suggested
- assumptions
- open questions
- readiness to generate `project_intake.json`
- next action

If `readiness.can_generate_intake` is `false`, do not produce planning artifacts yet.

In guided mode, `next_action.questions` must contain only the single next question unless the user explicitly asks for a batch.

Decision-card options are human-facing explanation. Record the selected answer in `intake_session`; do not treat unchosen options as project decisions.

## Required final intake output

When enough information exists, produce a `project_intake.json` draft matching `contracts/project_intake.schema.json`.

The record must include:

- `schema_version`
- `project_slug`
- `intake_mode`
- `project_goal`
- `target_users`
- `mvp`
- `target_platforms`
- `stack`
- `existing_project`
- `tools`
- `team_mode`
- `working_style`
- `constraints`
- `safety_boundaries`
- `assumptions`
- `open_questions`
- `acceptance_signals`

## Hand-off summary

After the JSON draft, provide a short hand-off summary for the Planning Agent:

- accepted goal
- MVP boundary
- selected or recommended stack
- target repository/workspace state
- team/agent parallelization intent
- high-risk open questions
- verification emphasis

## Safety boundaries

Reject or remove requests involving:

- botting
- unauthorized client control
- account automation
- credential collection beyond explicit safe local configuration notes
- emulator control for cheating or platform abuse
- live service interference
- scraping private APIs
- bypassing rate limits, access controls, or terms-of-service boundaries

When unsafe scope appears, state what was rejected and keep only the safe planning alternative.

```

## `prompts/00-planning-agent.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the planning agent role.
- Required: `true`

```markdown
# Planning Agent Prompt

You are the Planning Agent for AI Assembly Line.

Your job is to convert an accepted project intake into a safe, structured, implementation-ready planning package. You are not implementing the product. You are producing the planning artifacts that other roles can inspect, validate, and use.

Do not produce implementation tasks from a rough idea alone. If `project_intake.json` is missing or high-risk intake decisions are still unresolved, preserve those gaps as open questions or blocking tasks instead of inventing answers.

## Inputs to read first

Start from repository source-of-truth files when available:

- `project_intake.json`, when available
- `PROJECT_SPEC.md`
- `PROJECT_SPEC_TEMPLATE.md`
- `PRODUCT_RULES.md`
- `docs/PLANNING_RUN_WORKFLOW.md`
- `docs/TASK_GENERATION_WORKFLOW.md`
- `docs/TASK_CARD_FORMAT.md`
- `contracts/*.schema.json`
- `contracts/api_contract.openapi.yaml`
- existing examples under `examples/`
- the current planning-run `input-idea.md`

Do not rely on chat history or unstated assumptions when a repository file gives a stricter rule.

## Required planning outputs

Produce a coherent planning package covering:

- safe product interpretation
- rejected unsafe interpretations
- accepted intake summary
- product summary
- MVP boundary
- scope boundaries and non-goals
- target users and core use cases
- repo split
- domain model
- API contract draft or contract notes
- frontend screens
- backend/service responsibilities, if future-scoped
- core-engine responsibilities
- verification strategy
- parallel-safe task backlog
- role-specific starter prompts
- assumptions and open questions

For a manual planning run, the expected machine-readable outputs are:

- `project_spec.json`
- `repo_plan.json`
- `task_backlog.json`
- `agent_prompts.json`
- `slots_db.json`

Treat generated outputs as drafts until a human accepts them.

## Planning sequence

Follow this order:

1. Freeze the accepted intake decisions.
2. Create or update the project spec.
3. Create or update the repo plan.
4. Define shared contracts/interfaces before implementation tasks.
5. Generate the parallel-safe task backlog.
6. Generate role/agent prompts from the backlog and repo plan.
7. Generate slots only from assignable tasks.

Do not let task generation silently override the intake record.

## Task generation rules

When generating `task_backlog.json`, follow `docs/TASK_GENERATION_WORKFLOW.md` and `docs/TASK_CARD_FORMAT.md`.

Every task should have:

- a stable ID
- an action-oriented title
- one owner lane or role target
- a repository target or allowed area
- explicit dependencies by task ID
- a concise summary
- acceptance criteria
- verification steps
- handoff notes when another lane depends on it

Prefer small, verifiable tasks over vague umbrella tasks.

Bad tasks:

```text
Build backend.
Build frontend.
Add multiplayer.
Test app.
```

Good tasks:

```text
T-001 Define realtime room event contract.
T-002 Implement backend room creation using T-001.
T-003 Implement client room join screen using T-001.
T-004 Verify join-room end-to-end flow using T-002 and T-003.
```

## Parallel-safe backlog rules

For two or more workers, create shared contract tasks before client/backend/core implementation tasks.

Default lanes:

- `shared-contract`
- `client-ui`
- `backend-game-state`
- `core-domain`
- `tests-verification`
- `docs-devex`

A good backlog should allow parallel work without requiring two owners to edit the same files unnecessarily.

Make dependencies explicit enough for a validator or human reviewer to catch missing task IDs.

## Blocking tasks

If a high-risk decision is still missing, create a blocking task instead of guessing.

A blocking task must include:

- the missing decision
- why it blocks planning
- the exact answer needed
- which downstream tasks are blocked

If there are many blocking tasks, intake is probably not ready and should resume before planning.

## Safety reinterpretation

If the rough idea contains unsafe or policy-sensitive automation phrasing, reinterpret it into a safe planning tool when possible.

Reject or remove scopes involving:

- botting
- game-client automation
- account access or account control
- emulator control
- live service interference
- credential collection
- scraping private APIs
- bypassing rate limits, access controls, or terms-of-service boundaries

When rejecting a scope, explicitly say what was rejected and what safe alternative remains.

## Planning quality rules

- Work from strict files and contracts, not inferred product structure.
- Keep the plan implementation-ready but planning-only.
- Separate current-phase work from future-phase work.
- Keep MVP tasks distinct from post-MVP tasks.
- Prefer small, verifiable tasks over vague umbrella tasks.
- Give every task a clear repository target and verification proof.
- Create shared contract/interface tasks before parallel implementation tasks.
- Do not invent schemas that conflict with existing contracts.
- Do not imply that a backend, database, auth system, realtime sync, or autonomous agent runtime already exists unless the accepted intake and repo plan require it.
- Make dependencies explicit enough for a validator to catch missing task IDs.
- Preserve open questions instead of pretending they are solved.

## Output style

Be concrete and structured. Avoid motivational filler. Every major claim should become either a scope rule, artifact field, task, assumption, or verification requirement.

```

## `prompts/01-contract-steward.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the contract steward role.
- Required: `true`

```markdown
# Contract Steward Prompt

You are the Contract Steward for AI Assembly Line.

Your job is to keep the repository's schemas, generated JSON artifacts, OpenAPI draft, and documentation traceable to each other. You protect the source-of-truth boundary so downstream builders cannot invent hidden state or incompatible structures.

## Inputs to read first

Start from:

- `PROJECT_SPEC.md`
- `PRODUCT_RULES.md`
- `contracts/*.schema.json`
- `contracts/api_contract.openapi.yaml`
- `generated/*.json`
- `tools/validate_seed.py`
- `tools/validate_planning_run.py`
- `docs/verification-rules.md`

## Responsibilities

Check that:

- schema fields match the human-readable product spec
- required fields are explicit and useful
- `additionalProperties: false` remains intentional where strictness matters
- generated JSON can be validated without special hidden knowledge
- OpenAPI remains a draft contract, not an implied implemented backend
- frontend-visible structures come from generated state or contracts
- planning-run outputs can reuse the same contracts where practical

## Drift checks

Look for mismatches such as:

- docs list one artifact but generated state uses another
- a prompt references a repo target missing from `repo_plan.json`
- task dependencies point to non-existent task IDs
- frontend screen `renders_from` paths do not exist
- OpenAPI suggests implemented behavior that docs mark as future-only
- a viewer or builder prompt implies editing, login, database, realtime sync, or autonomous execution in Phase 0

## Rules

- Prefer explicit required fields.
- Disallow undocumented structure unless there is a strong reason not to.
- Keep schemas aligned with `PROJECT_SPEC.md` and `PRODUCT_RULES.md`.
- Ensure the frontend can render generated state directly from contracts.
- Reject schema drift that would let builders invent hidden state.
- Treat new generated indexes as derived artifacts unless the product spec says otherwise.
- Keep validators dependency-light unless an optional dependency is clearly marked as optional.

## Output style

Return precise findings with file paths, affected fields, impact, and minimal safe fixes. Do not redesign the system unless the current contract cannot express the required planning state.

```

## `prompts/02-frontend-builder.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the Phase 0 frontend builder role.
- Required: `true`

```markdown
# Frontend Builder Prompt

You are the Frontend Builder for AI Assembly Line.

Your job is to build static, read-only views over repository source-of-truth files. You do not create product state. You display existing generated state, contracts, prompts, planning-run indexes, and validation information in a way that makes drift visible.

## Inputs to read first

Build UI from source-of-truth files:

- `PROJECT_SPEC.md`
- `PRODUCT_RULES.md`
- `generated/project_spec.json`
- `generated/repo_plan.json`
- `generated/task_backlog.json`
- `generated/agent_prompts.json`
- `generated/slots_db.json`
- `generated/planning_runs_index.json`
- `contracts/*.schema.json`
- `contracts/api_contract.openapi.yaml`
- `docs/*.md`
- `prompts/*.md`

## Phase 0 scope

The current frontend is a static read-only viewer.

Allowed:

- render generated JSON artifacts
- render raw contract files
- render derived planning-run index data
- show visible fetch, parse, or validation failures
- provide local file-picker fallback for generated JSON where already supported
- keep layout simple and inspectable

Not allowed in this phase:

- editing
- login/authentication
- backend routes
- database calls
- realtime sync
- live slot leasing
- frontend-owned task, repo, prompt, slot, contract, or planning-run models
- hidden coordination logic

## Rendering rules

- Do not invent task, repo, prompt, slot, contract, planning-run, or verification structures.
- Prefer boring, readable pages over clever UI abstractions.
- Escape user-visible values before rendering.
- Treat missing required data as a visible contract/source failure.
- Keep page-specific renderers thin and driven by shared data-loading helpers.
- If adding a new page, update navigation, docs, and generated frontend screen lists together.

## Verification expectations

For every UI change, provide:

- files changed
- source artifacts rendered
- manual viewing path, usually `python -m http.server 8000`
- JS syntax check command/output
- any limitations around `file://` versus local server behavior

## Output style

Return small, reviewable changes. Explain exactly which source-of-truth files the UI consumes and which structures it refuses to invent.

```

## `prompts/03-backend-builder.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the backend builder role.
- Required: `true`

```markdown
# Backend Builder Prompt

You are the Backend Builder for AI Assembly Line.

Your role is intentionally future-scoped in Phase 0. The current repository contains contracts and planning artifacts only. You must not imply that an implemented backend exists until a later phase explicitly creates one.

## Inputs to read first

Start from:

- `PROJECT_SPEC.md`
- `PRODUCT_RULES.md`
- `contracts/api_contract.openapi.yaml`
- `contracts/*.schema.json`
- `generated/*.json`
- `docs/verification-rules.md`

## Current Phase 0 responsibility

In Phase 0, backend work means contract review and implementation planning only.

Allowed:

- review OpenAPI route shapes
- identify missing request/response fields
- propose future service boundaries
- define read-only project-state access patterns
- document future spec-compiler endpoint behavior as a draft contract
- produce tasks that remain clearly future-scoped

Not allowed in Phase 0:

- implementing HTTP routes
- adding auth
- adding a database
- adding background workers
- adding realtime sync
- adding mutable workflow state
- adding autonomous multi-agent execution

## Later implementation rules

When a later implementation phase begins:

- implement only the HTTP surface described by `contracts/api_contract.openapi.yaml`
- keep endpoints contract-first
- support read-only project state before mutation
- make every route testable with deterministic fixtures
- keep API models aligned with JSON schemas
- avoid introducing storage or auth until the product spec explicitly requires them

## Drift risks to catch

Watch for:

- docs saying "future" while code implements runtime behavior
- route contracts implying hidden database state
- endpoints accepting structures not covered by schemas
- prompts asking for autonomous orchestration before the repo has a safe runtime model
- frontend code calling backend routes in Phase 0

## Output style

Return implementation plans, contract gaps, and future-phase tasks. Do not produce backend code unless the current phase explicitly authorizes backend implementation.

```

## `prompts/04-core-engine-builder.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the core engine builder role.
- Required: `true`

```markdown
# Core Engine Builder Prompt

You are the Core Engine Builder for AI Assembly Line.

Your job is to design and implement deterministic planning-kernel logic that can turn structured inputs into validated planning artifacts. You are responsible for pure logic, normalization, consistency checks, and reproducible transformations. You are not responsible for UI, transport, auth, database persistence, or realtime coordination.

## Inputs to read first

Start from:

- `PROJECT_SPEC.md`
- `PROJECT_SPEC_TEMPLATE.md`
- `PRODUCT_RULES.md`
- `contracts/*.schema.json`
- `generated/*.json`
- `tools/validate_seed.py`
- `tools/validate_planning_run.py`
- `tools/build_planning_runs_index.py`
- `docs/PLANNING_RUN_WORKFLOW.md`

## Responsibilities

Prioritize:

- deterministic decomposition helpers
- spec-compilation helpers
- artifact normalization
- stable ID generation rules
- dependency validation
- source-path validation
- planning-run indexing
- verification support
- clear error reporting

## Boundary rules

- Keep implementation boundaries separate from UI and transport layers.
- Prefer deterministic behavior over clever heuristics with hidden state.
- Make generated outputs traceable to the spec and input idea.
- Do not call AI APIs from core logic in Phase 0.
- Do not add mutable agent runtime state.
- Do not add background orchestration.
- Do not require heavy dependencies for basic validation.

## Quality expectations

A core-engine change should usually include:

- a small command-line tool or pure function
- clear input/output files
- predictable exit codes
- explicit missing-file and parse-error messages
- cross-artifact consistency checks where useful
- documentation of generated artifacts

## Drift risks to catch

Watch for:

- validators silently ignoring missing required files
- scripts producing nondeterministic output order
- generated artifacts that cannot be rebuilt locally
- IDs or repo targets that differ across artifacts
- derived indexes that are not documented as derived
- future-phase runtime behavior sneaking into planning tools

## Output style

Return small deterministic tools and exact commands. Include what the tool reads, what it writes, and what failure modes it reports.

```

## `prompts/05-red-team-verifier.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the red-team verifier role.
- Required: `true`

```markdown
# Red Team Verifier Prompt

You are the Red Team Verifier for AI Assembly Line.

Your job is to attack planning outputs, contracts, prompts, docs, tools, and viewer behavior before they become trusted workflow state. You are not trying to be polite. You are trying to find source-of-truth drift, unsafe reinterpretations, unverifiable tasks, and scope creep.

## Inputs to inspect

Start from:

- `README.md`
- `PROJECT_SPEC.md`
- `PRODUCT_RULES.md`
- `docs/*.md`
- `contracts/*.schema.json`
- `contracts/api_contract.openapi.yaml`
- `generated/*.json`
- `prompts/*.md`
- `examples/`
- `planning_runs/`
- `tools/*.py`
- `web/`

## Attack areas

Look for:

- unsafe reinterpretation
- missing rejected-scope notes
- scope creep into backend/auth/database/realtime/editing/autonomous execution
- schema drift
- OpenAPI drift
- hidden frontend state invention
- unverifiable tasks
- prompt ambiguity
- missing dependency IDs
- generated files that cannot be rebuilt
- validators with unclear failure modes
- stale context-pack or manifest coverage
- planning-run outputs that do not match repo contracts

## Safety checks

For any domain involving games, accounts, automation, scraping, credentials, or external services, verify that the repo rejects:

- botting
- client control
- account automation
- emulator control
- live-service interference
- private API scraping
- credential handling outside explicit safe scope
- bypassing access controls or platform restrictions

## Evidence rules

For each finding, include:

- file path
- specific rule or contract involved
- why it matters
- minimal reproduction or concrete failing case
- minimal safe fix
- severity: blocker, high, medium, low, or nit

## Pass criteria

A change is acceptable when:

- generated state remains source-of-truth driven
- validators fail clearly on missing or inconsistent files
- prompts cannot reasonably be read as authorizing unsafe runtime behavior
- viewer code remains read-only and contract-driven
- future-phase ideas are labeled as future, not current implementation
- context-pack/manifest coverage is good enough for web-only review

## Output style

Return a verdict first, then findings. Keep fixes minimal. Do not redesign the repo unless a finding cannot be resolved with a small source-of-truth correction.

```

## `prompts/06-task-splitter.md`

- Category: `prompt-source`
- Purpose: Copy-paste prompt template for converting an accepted generated plan into schema-valid task batches.
- Required: `true`

```markdown
# Task Splitter Prompt

You are the Task Splitter for an AI Assembly Line planning run.

Your job is to convert an accepted generated plan into schema-valid task batch files that can be pasted back into the AI Assembly Line frontend and validated.

You are not implementing the project. You are decomposing the plan into small, verifiable, parallel-safe task records.

## Why Batches Matter

Do not generate the entire `task_backlog.json` in one response for large plans.

Large one-shot JSON outputs are hard to copy, easy to truncate, and likely to fail in web AI chats.

Instead, use this guided batch workflow:

1. Create a compact `task_batch_index` grouped by agent role, repo target, or lane.
2. On each follow-up message, generate exactly one next task batch file.
3. Continue until every batch listed in the index has been emitted.

Each response must be small enough to copy from a single code block.

## Source-of-Truth Rules

Follow these repository guides:

- `docs/TASK_CREATION_GUIDE.md`
- `docs/TASK_GENERATION_WORKFLOW.md`
- `docs/TASK_CARD_FORMAT.md`
- `docs/task-format.md`
- `contracts/task_batch_index.schema.json`
- `contracts/task_batch.schema.json`
- `contracts/task.schema.json`

Use the pasted generated plan as the accepted project source of truth.

Do not invent architecture, repositories, features, or scope that are not in the plan.

If the plan contains high-risk open questions, preserve them as blocking tasks or explicit task context instead of silently deciding them.

## Requested Mode

Use guided mode for normal web AI usage:

```text
MODE: guided
```

Guided mode is conversational:

- On the first response, return the batch index for `generated/task_batch_index.json`.
- After the user replies `continue`, `next`, `sounds good`, or equivalent, return the next not-yet-emitted batch file.
- Keep track of emitted batches from the conversation history.
- Emit batches in the exact order listed in the batch index.
- Stop after the final batch and say that no batches remain.

Explicit modes are still available for debugging or recovering from a lost chat context:

```text
MODE: batch-index
TARGET_BATCH_ID:
```

or:

```text
MODE: task-batch
TARGET_BATCH_ID: <one batch_id from the task_batch_index>
```

If `MODE` is missing, use `guided`.

If `MODE` is `task-batch` but `TARGET_BATCH_ID` is missing, return a batch index instead.

## Output UX Rule

For `MODE: guided`, return one small file per response.

Use this response shape:

````text
Save to: generated/task_batch_index.json
Next: reply continue to generate the first task batch.

```json
{ ...valid JSON for that one file... }
```
````

For batch responses, use:

````text
Save to: generated/task_batches/<batch_id>.json
Next: reply continue to generate the next task batch.

```json
{ ...valid JSON for that one batch file... }
```
````

After the final batch, use:

````text
Save to: generated/task_batches/<batch_id>.json
Next: no batches remain. Run python tools/validate_task_batches.py.

```json
{ ...valid JSON for the final batch file... }
```
````

For explicit `MODE: batch-index` or `MODE: task-batch`, return exactly one fenced `json` code block and no prose outside it.

The code block is intentional: web AI interfaces usually provide a copy button for code blocks. The future frontend should strip the fence automatically when pasting.

## Batch Index Output

When `MODE: guided` on the first response or `MODE: batch-index`, return a compact JSON object with this shape:

```json
{
  "schema_version": "0.1.0",
  "source": "accepted generated plan",
  "batching_strategy": "owner_role",
  "batches": [
    {
      "batch_id": "planning-coordinator",
      "owner_role": "Planning Coordinator Agent",
      "repo_targets": ["planning-repo"],
      "lanes": ["planning-source-of-truth"],
      "milestones": ["Milestone 0"],
      "expected_task_count": 6,
      "expected_task_ids": ["PLANNING-001"],
      "depends_on_batches": [],
      "output_path": "generated/task_batches/planning-coordinator.json",
      "status": "planned",
      "notes": "Short explanation of what this batch owns."
    }
  ]
}
```

Batching rules:

- Prefer one batch per `owner_role` when roles are clear.
- Split an oversized role into multiple batches by `repo_target`, `lane`, or milestone.
- Keep each batch small enough for one follow-up response.
- Include expected task IDs so later batches can reference dependencies consistently.
- Use stable lowercase `batch_id` values.
- Do not include full task objects in the batch index.

## Guided Continuation Output

When `MODE: guided` and the user asks to continue:

- Select the next batch in the `batches` array that has not already been emitted in this conversation.
- Return only that batch file.
- Do not ask the user to provide `TARGET_BATCH_ID`.
- Do not regenerate the batch index unless the user explicitly asks to restart.
- If the user asks for a specific batch by ID, generate that batch only and then resume the remaining order on the next continuation.
- If conversation context is missing the batch index, ask the user to paste `generated/task_batch_index.json` or restart guided mode with the generated plan.
- If every batch has already been emitted, do not output JSON. Say: `No batches remain. Run python tools/validate_task_batches.py.`

## Task Batch Output

When `MODE: task-batch` or guided continuation, return only the task batch object for the selected batch.

The top-level JSON value must be one task batch object matching `contracts/task_batch.schema.json`.

The batch object must contain `schema_version`, `batch_id`, `source_plan_path`, and `tasks`.

Each task inside `tasks` must include the required fields from `contracts/task.schema.json`:

```json
{
  "schema_version": "0.1.0",
  "batch_id": "planning-coordinator",
  "source_plan_path": "generated_plan.md",
  "tasks": [
    {
      "id": "TASK-001",
      "title": "Short action-oriented title",
      "summary": "One-sentence task summary.",
      "owner_role": "Role responsible for the task",
      "repo_target": "repo-or-ownership-target-from-the-plan",
      "depends_on": [],
      "inputs": [],
      "outputs": [],
      "acceptance_criteria": [],
      "verification": []
    }
  ]
}
```

Use these optional fields when useful:

- `status`
- `priority`
- `milestone`
- `lane`
- `allowed_areas`
- `blocks`
- `objective`
- `context`
- `implementation_notes`
- `proof_required`
- `edge_cases`
- `non_goals`
- `estimated_size`
- `risk_tags`
- `handoff_notes`
- `notes`

## Decomposition Rules

- Keep tasks small enough for one focused execution session.
- Use `estimated_size: "S"` or `estimated_size: "M"` for executable tasks.
- Mark tasks as `estimated_size: "L"` only when they should be split before execution.
- Prefer `status: "draft"` unless the task is fully specified and dependency-ready.
- Use `priority: "P0"` for work that blocks many other tasks.
- Use `priority: "P1"` for MVP-critical work.
- Use `priority: "P2"` for useful non-blocking work.
- Use `priority: "P3"` for post-MVP or nice-to-have work.
- Use `repo_target` values that match the repository split or ownership targets in the plan.
- Use `lane` values that help parallel work, such as `shared-contract`, `frontend-ui`, `backend-service`, `core-domain`, `deploy-ops`, `tests-verification`, or project-specific equivalents from the plan.
- Create shared contract, protocol, schema, API, data model, or interface tasks before implementation tasks that consume them.
- Use `depends_on` to reference task IDs that must be completed first.
- Use `blocks` to list downstream task IDs that this task unlocks when obvious.
- Include concrete `acceptance_criteria` for every task.
- Include concrete `verification` steps for every task.
- Include `proof_required` when the executor should return build output, test output, screenshots, logs, fixtures, manual test notes, or deployment command output.
- Include `edge_cases` for behavior that should not drift silently.
- Include `non_goals` to prevent scope creep.
- Do not create broad tasks like `build the backend`, `create the frontend`, or `implement multiplayer`.

## Cross-Batch Dependency Rules

- A task may depend on task IDs from another batch.
- Preserve dependency IDs from the batch index when possible.
- If a dependency task belongs to another batch, keep it in `depends_on`; do not duplicate the task.
- If a target batch cannot be generated safely without another batch, return the smallest valid set of blocking/open-question tasks for that batch.

## Suggested Ordering

Order batches roughly like this when the plan supports it:

1. Planning/source-of-truth setup
2. Shared contracts, protocols, schemas, API boundaries, data models
3. Core domain logic
4. Backend/service skeletons
5. Frontend/client skeletons
6. First end-to-end integration path
7. MVP feature slices
8. Deployment/devex
9. QA, verification, regression coverage
10. Post-MVP tasks, if the plan explicitly asks for them

## Final Instruction

Read the generated plan below.

If `MODE: guided`, return the next required file for the guided conversation.

If `MODE: batch-index`, return only the task batch index.

If `MODE: task-batch`, return only the task batch object for `TARGET_BATCH_ID`.

## Generated Plan

Paste the accepted generated plan below this line:

```

## `prompts/07-task-executor.md`

- Category: `prompt-source`
- Purpose: Copy-paste prompt template for executing exactly one task and returning a task_run JSON proof report.
- Required: `true`

```markdown
# Task Executor Prompt

You are a Task Executor for the AI Assembly Line workflow.

Your job is to complete exactly one assigned task from a schema-valid task JSON object, then return a small completion report that can be saved as `generated/task_runs/<task_id>.json` and referenced from `generated/collaboration_state.json`.

You are not replanning the project. You are executing one task within its stated boundaries.

## Inputs

The user will provide:

1. One task object from `generated/task_backlog.json` or `generated/task_batches/<batch_id>.json`.
2. Optional current repository/file context.
3. Optional assignment metadata from `generated/collaboration_state.json`.

## Hard Rules

- Work only on the provided task.
- Respect `allowed_areas`, `outputs`, `non_goals`, and `depends_on`.
- Do not silently implement dependencies that are not part of the task.
- Do not claim success without proof.
- If required context is missing, return `status: "blocked"` with a concrete blocker.
- If implementation is complete but not reviewed, return `status: "review"` unless the user explicitly asks you to mark it done and verification passed.
- If verification failed, return `status: "failed"` or `status: "blocked"`, not `done`.
- Keep the output small enough to copy from one code block.

## Execution Steps

1. Read the task JSON.
2. Confirm the task boundary in your own working context.
3. Make the smallest implementation that satisfies the acceptance criteria.
4. Run or describe the verification requested by the task.
5. Return a task run report matching `contracts/task_run.schema.json`.

## Output Format

Return exactly one fenced `json` code block and no prose outside it.

The top-level JSON value must be one task run object:

```json
{
  "schema_version": "0.1.0",
  "task_id": "TASK-001",
  "run_id": "TASK-001-run-001",
  "actor_id": "web-ai-task-executor",
  "status": "review",
  "implementation_summary": "Short summary of what was implemented.",
  "files_changed": [
    {
      "path": "path/to/file.ext",
      "change": "Short description of the change."
    }
  ],
  "verification": [
    {
      "command": "command that was run, or manual verification name",
      "result": "passed",
      "output": "Important output, shortened if needed."
    }
  ],
  "proof": [
    {
      "kind": "command_output",
      "summary": "Evidence that the task satisfies the acceptance criteria.",
      "status": "passed"
    }
  ],
  "blockers": [],
  "notes": "Optional notes for the reviewer.",
  "updated_at": "2026-07-10T00:00:00Z"
}
```

## Status Guidance

Use:

- `review` when the implementation appears complete and proof is provided, but human review is still expected.
- `done` only when the task explicitly allows executor-side completion and verification passed.
- `blocked` when missing context, failing dependencies, forbidden file boundaries, or unresolved decisions prevent safe execution.
- `failed` when implementation or verification was attempted and failed.

## Proof Guidance

Prefer concrete proof:

- test command output
- schema validation output
- linter or syntax-check output
- manual checklist result
- screenshot path or artifact path
- changed file summary

If the task asks for screenshots or browser verification and you cannot provide them, state that in `blockers` or `verification` with `result: "not_run"`.

## Final Instruction

Read the task below and return only the task run JSON report.

## Task JSON

Paste exactly one task object below this line:

```

## `examples/coc-base-builder/input-idea.md`

- Category: `example`
- Purpose: Example input idea used to demonstrate safe decomposition in a domain-specific sample.
- Required: `false`

```markdown
# Input Idea

I want to build a fully automatic base-builder app for Clash of Clans.

Safe interpretation for this repository:

- do not build a bot
- do not control a game client
- do not connect to accounts or emulators
- reinterpret the idea as an offline base layout planner and evaluator

```

## `examples/coc-base-builder/generated-project-spec.md`

- Category: `example`
- Purpose: Human-readable example project spec output for the coc-base-builder sample.
- Required: `false`

```markdown
# CoC Base Builder Generated Project Spec

## 1. Safe Product Interpretation

Requested idea: "fully automatic base-builder app for Clash of Clans"

Accepted interpretation: an offline Clash of Clans base layout planner, editor, scorer, and simulator-style evaluator.

Rejected interpretations:

- botting or gameplay automation
- game client control
- account access
- emulator orchestration
- live service interaction

## 2. Product Summary

- Product name: CoC Base Builder
- Goal: help users design and compare base layouts outside the game
- Users: players, clan planners, guide authors
- Primary outcomes:
  - edit layouts on a grid
  - score layouts with transparent heuristics
  - save and load planner files
  - run offline simulation-style evaluation

## 3. Scope Boundaries

- Allowed:
  - offline planning
  - local save/load
  - heuristic scoring
  - route and coverage simulation
- Not allowed:
  - bot behavior
  - client hooks
  - memory reading
  - account login
  - emulator control
  - live service calls

## 4. Repo Split

- `coc-base-frontend`
  - render spec-derived state, layout editor, reports
- `coc-base-backend`
  - local-only file and evaluation API
- `coc-base-engine`
  - placement rules, scoring, path evaluation
- `coc-base-contracts`
  - schemas and fixtures

## 5. Domain Model

- `BaseLayout`
  - fields: `layoutId`, `townHallLevel`, `width`, `height`, `placements`, `metadata`
- `BuildingPlacement`
  - fields: `placementId`, `buildingType`, `x`, `y`, `rotation`
- `RuleSet`
  - fields: `ruleSetId`, `weights`, `penalties`, `version`
- `ScoreReport`
  - fields: `reportId`, `totalScore`, `subscores`, `warnings`
- `SimulationReport`
  - fields: `simulationId`, `coverageSummary`, `pathingSummary`, `notes`

## 6. API Contract Draft

- `POST /compile-layout`
  - validate and normalize a layout file
- `POST /score-layout`
  - return a score report for a layout
- `POST /simulate-layout`
  - return a simulation-style evaluation report
- `POST /save-layout`
  - save a local planner document
- `POST /load-layout`
  - load a local planner document

## 7. Frontend Screens

- Overview
- Layout Editor
- Score Report
- Simulation Review
- Saved Layouts
- Contracts and Verification

Rule: the frontend must render current project state from generated files and contracts. It must not invent its own task, repo, or contract structure.

## 8. Backend Services

- layout validation service
- score service
- simulation service
- local file save/load service
- fixture serving service

## 9. Core Engine Responsibilities

- bounds checking
- placement collision validation
- score computation
- simulation-style path and coverage analysis
- deterministic serialization
- warnings for invalid or weak layouts

## 10. Verification Tasks

- validate generated JSON against schemas
- test invalid placement fixtures
- test repeatable score outputs
- test simulation report structure
- verify frontend renders contract-defined artifacts only
- red-team automation or bot reinterpretation attempts

## 11. Copy-Paste Starter Prompts

### Planning Agent

Convert rough base-builder ideas into safe offline planner specs. Reject botting, automation, client control, account access, emulator usage, and live service integration.

### Contract Steward

Define strict schemas for layouts, reports, repo plans, and tasks. Keep the frontend contract-driven and reject undocumented state.

### Frontend Builder

Build views that render the current project spec and generated artifacts directly. Do not invent structure or UI-only task models.

### Backend Builder

Implement local-only HTTP routes matching the contract draft. No auth, database, cloud sync, or live service access.

### Core Engine Builder

Implement deterministic layout validation, scoring, and simulation-style evaluation for an offline planner only.

### Red Team Verifier

Probe for bot-like reinterpretation, client hooks, account workflows, schema drift, and frontend state invention.

```

## `examples/coc-base-builder/generated-repo-plan.json`

- Category: `example`
- Purpose: Machine-readable example repo-plan output for the coc-base-builder sample.
- Required: `false`

```json
{
  "project_name": "CoC Base Builder",
  "repos": [
    {
      "name": "coc-base-frontend",
      "purpose": "Render contract-defined project state, layout editing, reports, and verification views.",
      "contains": [
        "overview page",
        "layout editor",
        "score report views",
        "simulation review views",
        "contracts browser"
      ],
      "depends_on": [
        "coc-base-contracts",
        "coc-base-engine"
      ],
      "excludes": [
        "invented state structures",
        "client automation",
        "account integration"
      ]
    },
    {
      "name": "coc-base-backend",
      "purpose": "Provide local-only API routes for validation, scoring, simulation, and file operations.",
      "contains": [
        "request validation",
        "route handlers",
        "file orchestration",
        "fixture endpoints"
      ],
      "depends_on": [
        "coc-base-contracts",
        "coc-base-engine"
      ],
      "excludes": [
        "auth",
        "database persistence",
        "cloud sync"
      ]
    },
    {
      "name": "coc-base-engine",
      "purpose": "Implement deterministic planner logic.",
      "contains": [
        "placement validation",
        "collision checks",
        "score heuristics",
        "path evaluation",
        "report generation"
      ],
      "depends_on": [
        "coc-base-contracts"
      ],
      "excludes": [
        "UI rendering",
        "real game integration"
      ]
    },
    {
      "name": "coc-base-contracts",
      "purpose": "Store schemas and fixtures shared across the planner.",
      "contains": [
        "layout schema",
        "report schemas",
        "planner state schema",
        "fixtures"
      ],
      "depends_on": [],
      "excludes": [
        "business logic",
        "undocumented UI data models"
      ]
    }
  ]
}

```

## `examples/coc-base-builder/generated-task-backlog.json`

- Category: `example`
- Purpose: Machine-readable example task backlog output for the coc-base-builder sample.
- Required: `false`

```json
[
  {
    "id": "contracts-layout-and-report-schemas",
    "title": "Define layout and report contracts",
    "summary": "Create strict schemas for base layouts, score reports, simulation reports, and planner state.",
    "owner_role": "Contract Steward",
    "repo_target": "coc-base-contracts",
    "depends_on": [],
    "inputs": [
      "generated-project-spec.md",
      "PRODUCT_RULES.md"
    ],
    "outputs": [
      "layout schema",
      "score report schema",
      "simulation report schema",
      "planner state schema"
    ],
    "acceptance_criteria": [
      "Schemas reject undocumented fields where not explicitly allowed.",
      "Schemas cover frontend-rendered artifacts.",
      "Fixtures include both valid and invalid examples."
    ],
    "verification": [
      "Schema tests pass for valid fixtures and fail for invalid fixtures."
    ],
    "risk_tags": [
      "schema-drift"
    ]
  },
  {
    "id": "engine-placement-validation",
    "title": "Implement deterministic placement validation",
    "summary": "Add bounds checks and collision rules for building placement on the planner grid.",
    "owner_role": "Core Engine Builder",
    "repo_target": "coc-base-engine",
    "depends_on": [
      "contracts-layout-and-report-schemas"
    ],
    "inputs": [
      "layout schema",
      "building definitions"
    ],
    "outputs": [
      "placement validator",
      "invalid placement fixtures"
    ],
    "acceptance_criteria": [
      "Out-of-bounds placements are rejected.",
      "Overlapping buildings are rejected.",
      "The same input yields the same validation output."
    ],
    "verification": [
      "Unit tests cover valid and invalid layouts."
    ],
    "risk_tags": [
      "determinism"
    ]
  },
  {
    "id": "engine-score-and-simulate",
    "title": "Implement score and simulation-style evaluation",
    "summary": "Produce reproducible score reports and offline simulation-style reports for saved layouts.",
    "owner_role": "Core Engine Builder",
    "repo_target": "coc-base-engine",
    "depends_on": [
      "contracts-layout-and-report-schemas",
      "engine-placement-validation"
    ],
    "inputs": [
      "rule set definitions",
      "validated layouts"
    ],
    "outputs": [
      "score module",
      "simulation module",
      "report fixtures"
    ],
    "acceptance_criteria": [
      "Reports conform to the declared contracts.",
      "Outputs are repeatable for the same layout and rule set.",
      "No live client hooks or service integrations are present."
    ],
    "verification": [
      "Fixture-based tests confirm structure and repeatability."
    ],
    "risk_tags": [
      "safety",
      "scope-drift"
    ]
  },
  {
    "id": "backend-local-api-draft",
    "title": "Implement local-only planner API draft",
    "summary": "Expose validate, score, simulate, save, and load routes matching the declared contract style.",
    "owner_role": "Backend Builder",
    "repo_target": "coc-base-backend",
    "depends_on": [
      "contracts-layout-and-report-schemas",
      "engine-score-and-simulate"
    ],
    "inputs": [
      "OpenAPI draft",
      "engine modules"
    ],
    "outputs": [
      "route handlers",
      "request and response fixtures"
    ],
    "acceptance_criteria": [
      "Input validation happens before engine execution.",
      "Responses match contract-defined shapes.",
      "No auth or database dependencies are introduced."
    ],
    "verification": [
      "Integration tests cover success and rejection cases."
    ],
    "risk_tags": [
      "boundary-control"
    ]
  },
  {
    "id": "frontend-read-only-board",
    "title": "Build read-only project board",
    "summary": "Render project name, goal, repo split, roles, backlog, contracts, prompt pack, and verification rules from source artifacts.",
    "owner_role": "Frontend Builder",
    "repo_target": "coc-base-frontend",
    "depends_on": [
      "contracts-layout-and-report-schemas"
    ],
    "inputs": [
      "PROJECT_SPEC.md",
      "generated-repo-plan.json",
      "generated-task-backlog.json",
      "prompt files",
      "verification rules"
    ],
    "outputs": [
      "read-only board UI"
    ],
    "acceptance_criteria": [
      "The UI reads source artifacts directly.",
      "No hidden UI state model replaces the contract structures.",
      "Contract mismatches fail visibly."
    ],
    "verification": [
      "UI tests render fixture artifacts and assert visible output."
    ],
    "risk_tags": [
      "frontend-state-invention"
    ]
  },
  {
    "id": "red-team-unsafe-reinterpretation",
    "title": "Create unsafe reinterpretation test set",
    "summary": "Add cases that try to turn the planner into a bot or expand it into live integration.",
    "owner_role": "Red Team Verifier",
    "repo_target": "coc-base-contracts",
    "depends_on": [
      "contracts-layout-and-report-schemas"
    ],
    "inputs": [
      "PRODUCT_RULES.md",
      "generated-project-spec.md"
    ],
    "outputs": [
      "rejection fixtures",
      "guardrail notes"
    ],
    "acceptance_criteria": [
      "Cases cover botting, account login, emulator control, client hooks, and hidden frontend state invention.",
      "Each case maps to a clear rejection reason."
    ],
    "verification": [
      "Human review confirms the rejection set covers likely drift paths."
    ],
    "risk_tags": [
      "safety",
      "scope-drift"
    ]
  }
]

```

## `examples/coc-base-builder/generated-agent-prompts.md`

- Category: `example`
- Purpose: Human-readable example prompt pack output for the coc-base-builder sample.
- Required: `false`

```markdown
# CoC Base Builder Agent Prompts

## Planning Agent

Convert rough product ideas into safe offline planner specs. If the user asks for automation, reinterpret it into a planning-only product or reject the unsafe portions. Output repo split, domain model, API draft, screens, services, verification tasks, and role prompts.

## Contract Steward

Maintain strict schemas for project specs, tasks, repo plans, layouts, reports, and slots. Ensure downstream consumers can render source artifacts directly without inventing undocumented structure.

## Frontend Builder

Build a contract-driven UI that renders the current spec, repo plan, backlog, prompts, and verification rules. Do not invent task, repo, or contract structure. Fail visibly on missing or invalid data.

## Backend Builder

Implement a local-only backend matching the contract draft. Support validation, scoring, simulation, save, and load operations. Do not add auth, databases, cloud services, or live game integration.

## Core Engine Builder

Implement deterministic layout validation, scoring, and simulation-style evaluation for an offline base planner. No game automation, client hooks, memory access, account workflows, or emulator control.

## Red Team Verifier

Probe for unsafe reinterpretation, hidden operational state, schema drift, frontend structure invention, client integration, and unverifiable prompt behavior. Produce concrete failing cases.

```

## `planning_runs/README.md`

- Category: `workflow`
- Purpose: Explains planning-run folders and what run artifacts should be committed.
- Required: `true`

```markdown
# Planning Runs

This directory stores manual planning runs created from rough software ideas.

Each planning run should live in its own folder:

```text
planning_runs/<run-slug>/
```

Typical contents:

- `input-idea.md`: the rough idea captured for the run
- `planning-run.md`: the AI-ready prompt generated from that idea
- `review-notes.md`: human acceptance or rejection notes
- `outputs/`: saved planning artifacts returned by the AI tool

What should be committed:

- run folders that are accepted, shared for review, or useful as traceable examples
- the original input idea when it is safe to store in the repository
- the generated planning prompt
- the saved output artifacts
- the human review outcome

What should not be committed:

- secrets
- tokens
- credentials
- unsafe or sensitive proprietary input that should not live in Git

Planning runs remain human-reviewed planning artifacts. They do not imply implemented software or autonomous execution.

```

## `planning_runs/coc-base-builder-v1/input-idea.md`

- Category: `workflow-example`
- Purpose: Safe sample planning-run input idea for an offline strategy-game base layout planner.
- Required: `true`

```markdown
# Input Idea

Create a safe offline strategy-game base layout planner for players who want to compare and organize defensive layouts outside the game.

The tool should help users:

- sketch layout ideas on a grid
- compare tradeoffs between layouts
- record notes about strengths and weaknesses
- review planning outputs before any later implementation work

Safety and scope requirements:

- no botting
- no game-client automation
- no account automation
- no emulator control
- no live-service interaction
- no cheating
- no scraping private game APIs

```

## `planning_runs/coc-base-builder-v1/planning-run.md`

- Category: `workflow-example`
- Purpose: Sample generated planning-run prompt for the safe coc-base-builder-v1 run.
- Required: `true`

```markdown
# Planning Run Prompt

You are producing a manual planning run for the `ai-assembly-line` workflow.

## Run Slug

`coc-base-builder-v1`

## Goal

Convert the rough software idea below into a safe, structured planning artifact set.

Generated outputs are drafts until a human accepts them.
If the idea implies unsafe automation, botting, account control, live-service interference, or other unsafe behavior, safely reinterpret it into the nearest safe planning-only scope or explicitly reject the unsafe parts.

## Rough Idea

# Input Idea

Create a safe offline strategy-game base layout planner for players who want to compare and organize defensive layouts outside the game.

The tool should help users:

- sketch layout ideas on a grid
- compare tradeoffs between layouts
- record notes about strengths and weaknesses
- review planning outputs before any later implementation work

Safety and scope requirements:

- no botting
- no game-client automation
- no account automation
- no emulator control
- no live-service interaction
- no cheating
- no scraping private game APIs

## Required Output Files

Return exactly these artifact types:

- `project_spec.json`
- `repo_plan.json`
- `task_backlog.json`
- `agent_prompts.json`
- `slots_db.json`

## Output Requirements

- `project_spec.json` must describe the product summary, boundaries, repo split, domain model, frontend screens, backend services, core engine responsibilities, verification tasks, and starter prompts.
- `repo_plan.json` must define the repo ownership split.
- `task_backlog.json` must define tasks with owners, dependencies, acceptance criteria, and verification.
- `agent_prompts.json` must define prompt boundaries tied to the repo split.
- `slots_db.json` must define role slots and verification requirements.

## Constraints

- Produce planning artifacts only.
- Do not implement software.
- Do not add hidden workflow state.
- Keep outputs human-reviewable and machine-readable.
- Keep repo targets, task dependencies, prompts, and slots internally consistent.

## Response Format

Return each file in its own fenced code block with the filename immediately above the fence, for example:

`project_spec.json`
```json
{ ... }
```

Use valid JSON for all five files.

```

## `planning_runs/coc-base-builder-v1/outputs/README.md`

- Category: `workflow-example`
- Purpose: Explains that the five required JSON outputs are intentionally absent until a planning agent produces them.
- Required: `true`

```markdown
# Outputs

This sample planning run intentionally does not include final generated output JSON yet.

The five required output files are expected to appear here only after a planning agent produces them:

- `project_spec.json`
- `repo_plan.json`
- `task_backlog.json`
- `agent_prompts.json`
- `slots_db.json`

Until then, their absence is intentional for this draft sample folder.

When outputs are added, validate them with:

```powershell
python tools\validate_planning_run.py planning_runs\coc-base-builder-v1
```

```

## `planning_runs/coc-base-builder-v1/review-notes.md`

- Category: `workflow-example`
- Purpose: Sample review-notes scaffold for the coc-base-builder-v1 planning run.
- Required: `true`

```markdown
# Review

## Outcome

- [ ] Accepted
- [ ] Needs revision
- [ ] Rejected

## Review Notes

- Safety interpretation:
- Structural validity:
- Repo/task/prompt/slot coherence:
- Reviewer decision rationale:

```

## `web/README.md`

- Category: `viewer`
- Purpose: Static viewer documentation, page-role split, Dispatch workflow notes, and file:// versus local server usage notes.
- Required: `true`

```markdown
# Web Viewer

This directory contains the static multi-page read-only viewer for the generated planning and execution-coordination state.

Serve the repo root locally with:

`python -m http.server 8000`

Then open:

`http://localhost:8000/web/`

If the browser blocks `file://` fetches, open any page directly and use the page-level file picker to load the required generated JSON files for that page.

## Page roles

Dispatch is the primary task-pickup surface. Assignments and Task Batches remain useful, but they have narrower roles:

- `web/dispatch.html`: primary "what can I do next?" page. It renders topological task waves from `generated/task_backlog.json`, overlays execution state from `generated/collaboration_state.json`, colors tasks by availability, and generates one-task execution context for a fresh AI chat.
- `web/assignments.html`: audit/status page for task ownership, execution status, notes, proof references, and copy/download helpers for `generated/collaboration_state.json`.
- `web/task-batches.html`: generation/validation page for guided task splitting, task batch index readiness, generated batch files, and dependency graph checks.

The remaining viewer pages are:

- `web/index.html`: overview from `generated/project_spec.json`
- `web/repos.html`: repository split and ownership from `generated/repo_plan.json`
- `web/backlog.html`: backlog grouped by `repo_target` from `generated/task_backlog.json`
- `web/prompts.html`: prompt pack from `generated/agent_prompts.json`
- `web/slots.html`: slot board from `generated/slots_db.json`
- `web/planning-runs.html`: planning-run scaffold and output completeness from `generated/planning_runs_index.json`
- `web/verification.html`: verification rules, proof requirements, and raw contract rendering from generated JSON artifacts plus `contracts/*.schema.json` and `contracts/api_contract.openapi.yaml`

See `docs/VIEWER_PAGE_ROLES.md` for the page-consolidation decision.

## Source files

Common generated sources:

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

Contract files are most reliable when serving the repo root with `python -m http.server 8000`. Generated JSON can also be loaded through the local file picker.

## Shared files

- `web/viewer-data.js`: generated JSON loading and file-picker fallback
- `web/viewer-layout.js`: shared shell, navigation, status handling, and helpers
- `web/page-*.js`: page-specific rendering only
- `web/page-dispatch-keyboard.js`: small keyboard helper for Enter/Space task-node activation on Dispatch
- `web/viewer.css`: shared styling

## Still intentionally absent

The viewer does not add:

- editing as persisted browser state
- backend APIs
- authentication
- realtime sync
- direct task claiming
- file writes
- frontend-only task, repo, prompt, slot, planning-run, execution, or contract models

```

## `web/index.html`

- Category: `viewer`
- Purpose: Overview page entry point for the static viewer.
- Required: `true`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Assembly Line Viewer - Overview</title>
  <link rel="stylesheet" href="viewer.css">
</head>
<body data-page="overview">
  <div id="app"></div>
  <script type="module" src="page-overview.js"></script>
</body>
</html>

```

## `web/repos.html`

- Category: `viewer`
- Purpose: Repository split page entry point.
- Required: `true`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Assembly Line Viewer - Repositories</title>
  <link rel="stylesheet" href="viewer.css">
</head>
<body data-page="repos">
  <div id="app"></div>
  <script type="module" src="page-repos.js"></script>
</body>
</html>

```

## `web/backlog.html`

- Category: `viewer`
- Purpose: Backlog page entry point.
- Required: `true`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Assembly Line Viewer - Backlog</title>
  <link rel="stylesheet" href="viewer.css">
</head>
<body data-page="backlog">
  <div id="app"></div>
  <script type="module" src="page-backlog.js"></script>
</body>
</html>

```

## `web/dispatch.html`

- Category: `viewer`
- Purpose: Dispatch page entry point for topological what-can-I-do-next task pickup and execution-context copying.
- Required: `true`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Assembly Line Viewer - Dispatch</title>
  <link rel="stylesheet" href="viewer.css">
  <link rel="stylesheet" href="dispatch.css">
</head>
<body data-page="dispatch">
  <div id="app"></div>
  <script type="module" src="page-dispatch.js"></script>
  <script type="module" src="page-dispatch-keyboard.js"></script>
</body>
</html>

```

## `web/assignments.html`

- Category: `viewer`
- Purpose: Assignments page entry point for read-only execution ownership, status, notes, and proof review.
- Required: `true`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Assembly Line Viewer - Assignments</title>
  <link rel="stylesheet" href="viewer.css">
</head>
<body data-page="assignments">
  <div id="app"></div>
  <script type="module" src="page-assignments.js"></script>
  <script type="module" src="page-assignment-tools.js"></script>
</body>
</html>

```

## `web/task-batches.html`

- Category: `viewer`
- Purpose: Task batches page entry point for batch index status, batch file readiness, task nodes, and dependency graph checks.
- Required: `true`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Assembly Line Viewer - Task Batches</title>
  <link rel="stylesheet" href="viewer.css">
</head>
<body data-page="task-batches">
  <div id="app"></div>
  <script type="module" src="page-task-batches.js"></script>
</body>
</html>

```

## `web/prompts.html`

- Category: `viewer`
- Purpose: Prompts page entry point.
- Required: `true`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Assembly Line Viewer - Prompts</title>
  <link rel="stylesheet" href="viewer.css">
</head>
<body data-page="prompts">
  <div id="app"></div>
  <script type="module" src="page-prompts.js"></script>
</body>
</html>

```

## `web/slots.html`

- Category: `viewer`
- Purpose: Slots page entry point.
- Required: `true`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Assembly Line Viewer - Slots</title>
  <link rel="stylesheet" href="viewer.css">
</head>
<body data-page="slots">
  <div id="app"></div>
  <script type="module" src="page-slots.js"></script>
</body>
</html>

```

## `web/planning-runs.html`

- Category: `viewer`
- Purpose: Planning-runs page entry point that renders the derived planning-run index read-only.
- Required: `true`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Assembly Line Viewer - Planning Runs</title>
  <link rel="stylesheet" href="viewer.css">
</head>
<body data-page="planning-runs">
  <div id="app"></div>
  <script type="module" src="page-planning-runs.js"></script>
</body>
</html>

```

## `web/verification.html`

- Category: `viewer`
- Purpose: Verification page entry point that also renders raw contract files read-only.
- Required: `true`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Assembly Line Viewer - Verification</title>
  <link rel="stylesheet" href="viewer.css">
</head>
<body data-page="verification">
  <div id="app"></div>
  <script type="module" src="page-verification.js"></script>
</body>
</html>

```

## `web/viewer-data.js`

- Category: `viewer`
- Purpose: Shared generated-data and contract-loading helpers for the static viewer.
- Required: `true`

```javascript
export const DATA_FILES = {
  projectSpec: "../generated/project_spec.json",
  repoPlan: "../generated/repo_plan.json",
  taskBacklog: "../generated/task_backlog.json",
  taskBatchIndex: "../generated/task_batch_index.json",
  collaborationState: "../generated/collaboration_state.json",
  agentPrompts: "../generated/agent_prompts.json",
  slotsDb: "../generated/slots_db.json",
  planningRunsIndex: "../generated/planning_runs_index.json",
};

export const CONTRACT_FILES = {
  projectSpecSchema: "../contracts/project_spec.schema.json",
  repoPlanSchema: "../contracts/repo_plan.schema.json",
  taskSchema: "../contracts/task.schema.json",
  taskBatchIndexSchema: "../contracts/task_batch_index.schema.json",
  taskBatchSchema: "../contracts/task_batch.schema.json",
  taskRunSchema: "../contracts/task_run.schema.json",
  slotSchema: "../contracts/slot.schema.json",
  agentPromptSchema: "../contracts/agent_prompt.schema.json",
  collaborationStateSchema: "../contracts/collaboration_state.schema.json",
  apiContract: "../contracts/api_contract.openapi.yaml",
};

export const FILE_NAMES = {
  projectSpec: "project_spec.json",
  repoPlan: "repo_plan.json",
  taskBacklog: "task_backlog.json",
  taskBatchIndex: "task_batch_index.json",
  collaborationState: "collaboration_state.json",
  agentPrompts: "agent_prompts.json",
  slotsDb: "slots_db.json",
  planningRunsIndex: "planning_runs_index.json",
};

export async function loadGeneratedState(requiredKeys) {
  const entries = await Promise.all(
    requiredKeys.map(async (key) => {
      const path = DATA_FILES[key];
      const response = await fetch(path, { cache: "no-store" });

      if (!response.ok) {
        throw new Error(`Failed to fetch ${path}: ${response.status} ${response.statusText}`);
      }

      try {
        return [key, await response.json()];
      } catch (error) {
        throw new Error(`Failed to parse ${path}: ${formatError(error)}`);
      }
    }),
  );

  return Object.fromEntries(entries);
}

export async function loadLocalState(requiredKeys, files) {
  const fileMap = new Map(Array.from(files ?? []).map((file) => [file.name, file]));

  for (const key of requiredKeys) {
    const fileName = FILE_NAMES[key];
    if (!fileMap.has(fileName)) {
      throw new Error(`Missing required file: ${fileName}`);
    }
  }

  const entries = await Promise.all(
    requiredKeys.map(async (key) => {
      const fileName = FILE_NAMES[key];
      const raw = await fileMap.get(fileName).text();

      try {
        return [key, JSON.parse(raw)];
      } catch (error) {
        throw new Error(`Failed to parse ${fileName}: ${formatError(error)}`);
      }
    }),
  );

  return Object.fromEntries(entries);
}

export async function loadTextFile(path) {
  const response = await fetch(path, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`Failed to fetch ${path}: ${response.status} ${response.statusText}`);
  }

  return response.text();
}

export function sourceFilesForKeys(requiredKeys) {
  return requiredKeys.map((key) => `generated/${FILE_NAMES[key]}`);
}

export function isFileProtocol() {
  return window.location.protocol === "file:";
}

export function formatError(error) {
  return error instanceof Error ? error.message : String(error);
}

```

## `web/viewer-layout.js`

- Category: `viewer`
- Purpose: Shared viewer shell, status handling, navigation, and reusable rendering helpers.
- Required: `true`

```javascript
import { formatError, isFileProtocol, loadGeneratedState, loadLocalState, sourceFilesForKeys } from "./viewer-data.js";

const NAV_ITEMS = [
  { id: "overview", label: "Overview", href: "index.html" },
  { id: "repos", label: "Repos", href: "repos.html" },
  { id: "backlog", label: "Backlog", href: "backlog.html" },
  { id: "assignments", label: "Assignments", href: "assignments.html" },
  { id: "dispatch", label: "Dispatch", href: "dispatch.html" },
  { id: "task-batches", label: "Task Batches", href: "task-batches.html" },
  { id: "prompts", label: "Prompts", href: "prompts.html" },
  { id: "slots", label: "Slots", href: "slots.html" },
  { id: "planning-runs", label: "Planning Runs", href: "planning-runs.html" },
  { id: "verification", label: "Verification", href: "verification.html" },
];

export function initializeViewerPage(config) {
  const {
    pageId,
    eyebrow,
    title,
    description,
    requiredKeys,
    extraSourceFiles = [],
    helperNote = "",
    renderContent,
  } = config;

  const app = document.getElementById("app");
  if (!app) {
    throw new Error('Missing required root element: #app');
  }

  const sourceFiles = [...sourceFilesForKeys(requiredKeys), ...extraSourceFiles];
  app.innerHTML = `
    <header class="hero shell-width">
      <div class="hero-copy">
        <p class="eyebrow">${escapeHtml(eyebrow)}</p>
        <h1>${escapeHtml(title)}</h1>
        <p class="lede">${escapeHtml(description)}</p>
        <nav class="site-nav" aria-label="Viewer pages">
          ${NAV_ITEMS.map((item) => renderNavLink(item, pageId)).join("")}
        </nav>
      </div>
      <div class="hero-actions">
        <button id="reloadButton" type="button">Reload Generated State</button>
        <label class="file-button" for="filePicker">Load Local JSON Files</label>
        <input id="filePicker" type="file" accept=".json" multiple>
      </div>
    </header>

    <main class="layout shell-width">
      <section class="panel status-panel">
        <h2>Status</h2>
        <p id="statusMessage" class="status loading">Loading generated state...</p>
        <p class="source-note">
          This page renders generated state only. It does not edit or invent task, repo, prompt, slot, planning-run, or contract structure.
        </p>
        <p class="source-note">
          Source of truth for this page:
          ${sourceFiles.map((path) => `<code>${escapeHtml(path)}</code>`).join(", ")}.
        </p>
        <p class="helper">
          Serve the repo root with <code>python -m http.server 8000</code> and open <code>http://localhost:8000/web/</code>.
          If the page is opened with <code>file://</code> and fetch is blocked, load the required JSON files with the button above.
        </p>
        ${helperNote ? `<p class="helper">${helperNote}</p>` : ""}
        <p class="helper">
          Required local files for this page: ${sourceFiles.map((path) => `<code>${escapeHtml(path)}</code>`).join(", ")}.
        </p>
      </section>

      <section class="panel">
        <div id="pageContent"></div>
      </section>
    </main>
  `;

  const statusMessage = document.getElementById("statusMessage");
  const pageContent = document.getElementById("pageContent");
  const reloadButton = document.getElementById("reloadButton");
  const filePicker = document.getElementById("filePicker");

  reloadButton.addEventListener("click", () => {
    void fetchAndRender();
  });

  filePicker.addEventListener("change", async (event) => {
    try {
      setStatus(statusMessage, "Loading local JSON files...", "loading");
      clearContent(pageContent);
      const data = await loadLocalState(requiredKeys, event.target.files);
      renderContent(pageContent, data);
      setStatus(statusMessage, "Loaded generated state from local files.", "success");
    } catch (error) {
      renderFailure(pageContent, statusMessage, error, requiredKeys);
    } finally {
      filePicker.value = "";
    }
  });

  void fetchAndRender();

  async function fetchAndRender() {
    try {
      setStatus(statusMessage, "Loading generated state...", "loading");
      clearContent(pageContent);
      const data = await loadGeneratedState(requiredKeys);
      renderContent(pageContent, data);
      setStatus(statusMessage, `Loaded generated state from ${sourceFiles.join(", ")}.`, "success");
    } catch (error) {
      renderFailure(pageContent, statusMessage, error, requiredKeys);
    }
  }
}

function renderFailure(pageContent, statusMessage, error, requiredKeys) {
  const fileList = sourceFilesForKeys(requiredKeys)
    .map((path) => `<code>${escapeHtml(path)}</code>`)
    .join(", ");

  const hint = isFileProtocol()
    ? 'Fetch is likely blocked under <code>file://</code>. Use <code>python -m http.server 8000</code> from the repo root or load the required files manually.'
    : 'Check that the generated JSON files exist and contain valid JSON.';

  setStatus(statusMessage, formatError(error), "error");
  pageContent.innerHTML = `
    <div class="card error-card">
      <h3>Unable to render this page</h3>
      <p>${escapeHtml(formatError(error))}</p>
      <p class="helper">This page requires ${fileList}.</p>
      <p class="helper">${hint}</p>
    </div>
  `;
}

function renderNavLink(item, pageId) {
  const className = item.id === pageId ? "nav-link active" : "nav-link";
  return `<a class="${className}" href="${item.href}">${escapeHtml(item.label)}</a>`;
}

export function renderList(items, emptyLabel = "None") {
  if (!items || items.length === 0) {
    return `<p class="muted">${escapeHtml(emptyLabel)}</p>`;
  }

  return `<ul class="list">${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

export function renderChipRow(items, emptyLabel = "None") {
  if (!items || items.length === 0) {
    return `<p class="muted">${escapeHtml(emptyLabel)}</p>`;
  }

  return `<div class="chip-row">${items.map((item) => `<span class="chip">${escapeHtml(item)}</span>`).join("")}</div>`;
}

export function renderKeyValueRows(rows) {
  return `
    <dl class="meta">
      ${rows
        .map(
          (row) => `
            <div>
              <dt>${escapeHtml(row.label)}</dt>
              <dd>${row.value}</dd>
            </div>
          `,
        )
        .join("")}
    </dl>
  `;
}

export function renderCardGrid(cardsMarkup, className = "") {
  const suffix = className ? ` ${className}` : "";
  return `<div class="card-grid${suffix}">${cardsMarkup}</div>`;
}

export function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function clearContent(pageContent) {
  pageContent.innerHTML = "";
}

function setStatus(statusMessage, message, kind) {
  statusMessage.textContent = message;
  statusMessage.className = `status ${kind}`;
}

```

## `web/page-overview.js`

- Category: `viewer`
- Purpose: Overview page rendering logic.
- Required: `true`

```javascript
import { escapeHtml, initializeViewerPage, renderCardGrid, renderChipRow, renderList } from "./viewer-layout.js";

initializeViewerPage({
  pageId: "overview",
  eyebrow: "Read-Only Planning State Viewer",
  title: "AI Assembly Line",
  description: "Overview of the generated project specification and phase 0 scope boundaries.",
  requiredKeys: ["projectSpec"],
  renderContent(container, data) {
    const projectSpec = data.projectSpec;

    container.innerHTML = `
      <div class="stack">
        <div class="card">
          <h2>${escapeHtml(projectSpec.project_name)}</h2>
          <p>${escapeHtml(projectSpec.product_summary.goal)}</p>
        </div>

        ${renderCardGrid(
          `
            <article class="card">
              <h3>Users</h3>
              ${renderChipRow(projectSpec.product_summary.users)}
            </article>
            <article class="card">
              <h3>Non-Goals</h3>
              ${renderList(projectSpec.product_summary.non_goals)}
            </article>
          `,
          "two-up",
        )}

        ${renderCardGrid(
          `
            <article class="card">
              <h3>Safety Boundaries</h3>
              ${renderList(projectSpec.safety_boundaries)}
            </article>
            <article class="card">
              <h3>Verification Tasks</h3>
              ${renderList(projectSpec.verification_tasks)}
            </article>
          `,
          "two-up",
        )}

        <article class="card">
          <h3>Core Engine Responsibilities</h3>
          ${renderList(projectSpec.core_engine_responsibilities)}
        </article>

        ${renderCardGrid(
          projectSpec.frontend_screens
            .map(
              (screen) => `
                <article class="card">
                  <h3>${escapeHtml(screen.name)}</h3>
                  <p class="muted">${escapeHtml(screen.notes)}</p>
                  <h4>Renders From</h4>
                  ${renderList(screen.renders_from)}
                </article>
              `,
            )
            .join(""),
          "three-up",
        )}

        ${renderCardGrid(
          projectSpec.domain_model
            .map(
              (entry) => `
                <article class="card">
                  <h3>${escapeHtml(entry.name)}</h3>
                  <h4>Fields</h4>
                  ${renderList(entry.fields)}
                  <h4>Relations</h4>
                  ${renderList(entry.relations)}
                </article>
              `,
            )
            .join(""),
          "three-up",
        )}
      </div>
    `;
  },
});

```

## `web/page-repos.js`

- Category: `viewer`
- Purpose: Repository split page rendering logic.
- Required: `true`

```javascript
import { escapeHtml, initializeViewerPage, renderCardGrid, renderChipRow, renderKeyValueRows, renderList } from "./viewer-layout.js";

initializeViewerPage({
  pageId: "repos",
  eyebrow: "Repository Split",
  title: "Repo Ownership",
  description: "Read-only view of the generated repository plan and contract-defined ownership boundaries.",
  requiredKeys: ["repoPlan"],
  renderContent(container, data) {
    const repoPlan = data.repoPlan;

    container.innerHTML = `
      <div class="stack">
        <div class="card">
          <h2>${escapeHtml(repoPlan.project_name)}</h2>
          <p class="muted">Each card renders directly from <code>generated/repo_plan.json</code>.</p>
        </div>

        ${renderCardGrid(
          repoPlan.repos
            .map(
              (repo) => `
                <article class="card">
                  <div class="stack">
                    <div>
                      <h3>${escapeHtml(repo.name)}</h3>
                      <p>${escapeHtml(repo.purpose)}</p>
                    </div>
                    ${renderKeyValueRows([
                      { label: "Contains", value: renderList(repo.contains) },
                      { label: "Depends On", value: repo.depends_on.length ? renderChipRow(repo.depends_on) : '<p class="muted">None</p>' },
                      { label: "Excludes", value: renderList(repo.excludes) },
                    ])}
                  </div>
                </article>
              `,
            )
            .join(""),
          "two-up",
        )}
      </div>
    `;
  },
});

```

## `web/page-backlog.js`

- Category: `viewer`
- Purpose: Backlog page rendering logic.
- Required: `true`

```javascript
import { escapeHtml, initializeViewerPage, renderChipRow, renderList } from "./viewer-layout.js";

initializeViewerPage({
  pageId: "backlog",
  eyebrow: "Task Backlog",
  title: "Backlog By Repo Target",
  description: "Generated tasks grouped by the existing repo_target values in the canonical backlog.",
  requiredKeys: ["repoPlan", "taskBacklog"],
  renderContent(container, data) {
    const repoOrder = data.repoPlan.repos.map((repo) => repo.name);
    const repoMeta = new Map(data.repoPlan.repos.map((repo) => [repo.name, repo]));
    const groups = new Map(repoOrder.map((name) => [name, []]));

    for (const task of data.taskBacklog) {
      if (!groups.has(task.repo_target)) {
        groups.set(task.repo_target, []);
      }
      groups.get(task.repo_target).push(task);
    }

    container.innerHTML = `
      <div class="stack">
        ${Array.from(groups.entries())
          .map(([repoName, tasks]) => renderTaskGroup(repoName, tasks, repoMeta.get(repoName)))
          .join("")}
      </div>
    `;
  },
});

function renderTaskGroup(repoName, tasks, repoMeta) {
  return `
    <section class="card">
      <div class="section-heading">
        <div>
          <h2>${escapeHtml(repoName)}</h2>
          <p class="muted">${repoMeta ? escapeHtml(repoMeta.purpose) : "Repo target appears in the generated backlog but not in the generated repo plan."}</p>
        </div>
        <span class="chip">${tasks.length} task${tasks.length === 1 ? "" : "s"}</span>
      </div>

      ${
        tasks.length
          ? `<div class="stack">${tasks.map((task) => renderTaskCard(task)).join("")}</div>`
          : '<p class="muted">No tasks currently generated for this repo target.</p>'
      }
    </section>
  `;
}

function renderTaskCard(task) {
  return `
    <article class="card inset-card">
      <div class="chip-row">
        <span class="chip">${escapeHtml(task.id)}</span>
        <span class="chip">${escapeHtml(task.owner_role)}</span>
      </div>
      <h3>${escapeHtml(task.title)}</h3>
      <p>${escapeHtml(task.summary)}</p>
      <div class="card-grid two-up">
        <div>
          <h4>Depends On</h4>
          ${renderList(task.depends_on)}
        </div>
        <div>
          <h4>Inputs</h4>
          ${renderList(task.inputs)}
        </div>
        <div>
          <h4>Outputs</h4>
          ${renderList(task.outputs)}
        </div>
        <div>
          <h4>Risk Tags</h4>
          ${task.risk_tags && task.risk_tags.length ? renderChipRow(task.risk_tags) : '<p class="muted">None</p>'}
        </div>
      </div>
      <div class="card-grid two-up">
        <div>
          <h4>Acceptance Criteria</h4>
          ${renderList(task.acceptance_criteria)}
        </div>
        <div>
          <h4>Verification</h4>
          ${renderList(task.verification)}
        </div>
      </div>
    </article>
  `;
}

```

## `web/page-dispatch.js`

- Category: `viewer`
- Purpose: Dispatch page rendering logic for topological task waves, availability state, task detail, and execution-context copying.
- Required: `true`

```javascript
import { escapeHtml, initializeViewerPage, renderList } from "./viewer-layout.js";

const LOCKED_STATUSES = new Set(["claimed", "in_progress"]);
const REVIEW_STATUSES = new Set(["review"]);
const DONE_STATUSES = new Set(["done"]);
const BLOCKED_STATUSES = new Set(["blocked"]);
const ACTIVE_CLAIM_STATUSES = new Set(["claimed", "in_progress"]);
const FILTERS = ["all", "available", "waiting", "locked", "blocked", "done"];

initializeViewerPage({
  pageId: "dispatch",
  eyebrow: "Execution Cockpit",
  title: "Dispatch",
  description: "Pick the next available task, copy one complete execution context, and start a focused AI task chat.",
  requiredKeys: ["taskBacklog", "collaborationState"],
  extraSourceFiles: ["prompts/07-task-executor.md", "contracts/task_run.schema.json"],
  helperNote: "Dispatch is the primary task-pickup screen. It is still static/read-only: it does not claim, lock, edit, or write files.",
  renderContent(container, data) {
    const tasks = Array.isArray(data.taskBacklog) ? data.taskBacklog : [];
    const state = data.collaborationState && typeof data.collaborationState === "object" ? data.collaborationState : {};
    const model = buildDispatchModel(tasks, state);

    container.innerHTML = renderDispatchShell(model);
    bindDispatchControls(container, model);
  },
});

function buildDispatchModel(tasks, state) {
  const actors = Array.isArray(state.actors) ? state.actors : [];
  const actorMap = new Map(actors.map((actor) => [actor.actor_id, actor]));
  const assignmentMap = buildAssignmentMap(state.task_assignments);
  const claimMap = buildActiveClaimMap(state.task_claims);
  const taskMap = new Map(tasks.map((task) => [task.id, task]));
  const layers = computeTopologicalLayers(tasks);

  const rawRows = tasks.map((task) => {
    const assignment = assignmentMap.get(task.id);
    const activeClaim = claimMap.get(task.id);
    const actorId = assignment?.assigned_to ?? activeClaim?.actor_id ?? "";
    const actor = actorId ? actorMap.get(actorId) : null;

    return {
      task,
      assignment,
      activeClaim,
      actor,
      id: task.id ?? "unknown-task",
      title: task.title ?? task.summary ?? task.id ?? "Untitled task",
      summary: task.summary ?? "",
      ownerRole: task.owner_role ?? "unknown role",
      repoTarget: task.repo_target ?? "unknown repo",
      lane: task.lane ?? "unassigned lane",
      planningStatus: task.status ?? "not set",
      executionStatus: assignment?.status ?? claimStatusToAssignmentStatus(activeClaim?.status) ?? "unclaimed",
      assignedTo: actor?.display_name ?? assignment?.assignee_label ?? assignment?.assigned_to ?? activeClaim?.actor_id ?? "Unassigned",
      assigneeType: assignment?.assignee_type ?? actor?.kind ?? (activeClaim ? "unknown" : "unassigned"),
      dependsOn: Array.isArray(task.depends_on) ? task.depends_on : [],
      outputs: Array.isArray(task.outputs) ? task.outputs : [],
      verification: Array.isArray(task.verification) ? task.verification : [],
      acceptanceCriteria: Array.isArray(task.acceptance_criteria) ? task.acceptance_criteria : [],
      proof: Array.isArray(assignment?.proof) ? assignment.proof : [],
      notes: assignment?.notes ?? activeClaim?.notes ?? "",
      updatedAt: assignment?.updated_at ?? activeClaim?.claimed_at ?? activeClaim?.released_at ?? "",
    };
  });

  const rowsById = new Map(rawRows.map((row) => [row.id, row]));
  const rows = rawRows.map((row) => classifyRow(row, rowsById, taskMap));
  const classifiedRowsById = new Map(rows.map((row) => [row.id, row]));
  const summary = summarizeRows(rows);
  const defaultTaskId = rows.find((row) => row.dispatchStatus === "available")?.id ?? rows[0]?.id ?? "";

  return {
    actors,
    state,
    tasks,
    layers,
    rows,
    rowsById: classifiedRowsById,
    summary,
    defaultTaskId,
  };
}

function buildAssignmentMap(assignments) {
  const map = new Map();
  if (!Array.isArray(assignments)) {
    return map;
  }

  for (const assignment of assignments) {
    if (assignment?.task_id) {
      map.set(assignment.task_id, assignment);
    }
  }

  return map;
}

function buildActiveClaimMap(claims) {
  const map = new Map();
  if (!Array.isArray(claims)) {
    return map;
  }

  for (const claim of claims) {
    if (claim?.task_id && ACTIVE_CLAIM_STATUSES.has(claim.status)) {
      map.set(claim.task_id, claim);
    }
  }

  return map;
}

function claimStatusToAssignmentStatus(status) {
  if (!status) {
    return null;
  }

  if (status === "submitted") {
    return "review";
  }

  if (status === "released") {
    return "released";
  }

  return status;
}

function classifyRow(row, rowsById, taskMap) {
  const missingDependencies = row.dependsOn.filter((dependencyId) => !taskMap.has(dependencyId));
  const dependencyRows = row.dependsOn.map((dependencyId) => rowsById.get(dependencyId)).filter(Boolean);
  const blockedDependencies = dependencyRows.filter((dependency) => BLOCKED_STATUSES.has(dependency.executionStatus));
  const unfinishedDependencies = dependencyRows.filter((dependency) => !isDone(dependency));

  let dispatchStatus = "available";
  let visualStatus = "available";
  let dispatchReason = "All dependencies are done and the task is free to take.";
  let unavailableDetails = [];

  if (isDone(row)) {
    dispatchStatus = "done";
    visualStatus = "done";
    dispatchReason = "Done. Review proof before using this as dependency context.";
  } else if (BLOCKED_STATUSES.has(row.executionStatus) || missingDependencies.length || blockedDependencies.length) {
    dispatchStatus = "blocked";
    visualStatus = "blocked";
    if (missingDependencies.length) {
      dispatchReason = `Missing dependency reference(s): ${missingDependencies.join(", ")}.`;
    } else if (blockedDependencies.length) {
      dispatchReason = `Blocked by dependency task(s): ${blockedDependencies.map((dependency) => dependency.id).join(", ")}.`;
    } else {
      dispatchReason = row.notes ? `Blocked: ${row.notes}` : "Task is explicitly blocked.";
    }
    unavailableDetails = buildBlockedDetails(row, missingDependencies, blockedDependencies);
  } else if (LOCKED_STATUSES.has(row.executionStatus)) {
    dispatchStatus = "locked";
    visualStatus = "locked";
    dispatchReason = `Locked by ${row.assignedTo} (${row.executionStatus}).`;
    unavailableDetails = [
      `actor: ${row.assignedTo}`,
      `status: ${row.executionStatus}`,
      row.updatedAt ? `updated: ${row.updatedAt}` : "updated: not recorded",
    ];
  } else if (REVIEW_STATUSES.has(row.executionStatus)) {
    dispatchStatus = "waiting";
    visualStatus = "waiting";
    dispatchReason = "In review; wait for proof acceptance before taking follow-up work.";
    unavailableDetails = [
      `review actor/status: ${row.assignedTo} / ${row.executionStatus}`,
      row.updatedAt ? `updated: ${row.updatedAt}` : "updated: not recorded",
    ];
  } else if (unfinishedDependencies.length) {
    dispatchStatus = "waiting";
    visualStatus = "waiting";
    dispatchReason = `Waiting for dependency task(s): ${unfinishedDependencies.map((dependency) => dependency.id).join(", ")}.`;
    unavailableDetails = unfinishedDependencies.map(
      (dependency) => `${dependency.id} - ${dependency.title} - ${dependency.executionStatus}`,
    );
  }

  return {
    ...row,
    dependencyRows,
    missingDependencies,
    blockedDependencies,
    unfinishedDependencies,
    dispatchStatus,
    visualStatus,
    dispatchReason,
    unavailableDetails,
  };
}

function buildBlockedDetails(row, missingDependencies, blockedDependencies) {
  const details = [];

  if (missingDependencies.length) {
    details.push(`missing dependencies: ${missingDependencies.join(", ")}`);
  }

  for (const dependency of blockedDependencies) {
    details.push(`${dependency.id} - ${dependency.title} - ${dependency.dispatchReason}`);
  }

  if (BLOCKED_STATUSES.has(row.executionStatus)) {
    details.push(row.notes ? `blocked note: ${row.notes}` : "assignment status is blocked");
  }

  return details;
}

function isDone(row) {
  return DONE_STATUSES.has(row.executionStatus) || row.planningStatus === "done";
}

function computeTopologicalLayers(tasks) {
  const taskMap = new Map(tasks.map((task) => [task.id, task]));
  const indegree = new Map(tasks.map((task) => [task.id, 0]));
  const dependents = new Map(tasks.map((task) => [task.id, []]));

  for (const task of tasks) {
    const dependencies = Array.isArray(task.depends_on) ? task.depends_on : [];
    for (const dependencyId of dependencies) {
      if (!taskMap.has(dependencyId)) {
        continue;
      }

      indegree.set(task.id, (indegree.get(task.id) ?? 0) + 1);
      dependents.get(dependencyId).push(task.id);
    }
  }

  const remaining = new Set(tasks.map((task) => task.id));
  let ready = tasks.filter((task) => (indegree.get(task.id) ?? 0) === 0).map((task) => task.id);
  const layers = [];

  while (ready.length) {
    const layerIds = ready.filter((taskId) => remaining.has(taskId));
    if (!layerIds.length) {
      break;
    }

    layers.push({ label: `Wave ${layers.length + 1}`, taskIds: layerIds, cyclic: false });
    const next = [];

    for (const taskId of layerIds) {
      remaining.delete(taskId);
      for (const dependentId of dependents.get(taskId) ?? []) {
        indegree.set(dependentId, (indegree.get(dependentId) ?? 0) - 1);
        if ((indegree.get(dependentId) ?? 0) === 0) {
          next.push(dependentId);
        }
      }
    }

    ready = next;
  }

  if (remaining.size) {
    layers.push({ label: "Unsorted / cyclic", taskIds: Array.from(remaining), cyclic: true });
  }

  return layers;
}

function summarizeRows(rows) {
  return rows.reduce(
    (summary, row) => {
      summary.total += 1;
      summary[row.dispatchStatus] = (summary[row.dispatchStatus] ?? 0) + 1;
      return summary;
    },
    {
      total: 0,
      available: 0,
      waiting: 0,
      locked: 0,
      blocked: 0,
      done: 0,
    },
  );
}

function renderDispatchShell(model) {
  return `
    <div class="dispatch-cockpit">
      <section class="dispatch-intro">
        <div>
          <p class="eyebrow">Static execution cockpit</p>
          <h2>Pick one task and launch a fresh AI chat</h2>
          <p class="muted">Green cards are ready now. Click a task, copy the full execution context, and save the returned report as <code>generated/task_runs/&lt;task_id&gt;.json</code>.</p>
        </div>
        <span class="chip status-available">${escapeHtml(String(model.summary.available))} ready now</span>
      </section>

      <section class="dispatch-summary" aria-label="Dispatch state summary">
        ${renderSummaryButton("available", "Available", model.summary.available)}
        ${renderSummaryButton("waiting", "Waiting", model.summary.waiting)}
        ${renderSummaryButton("locked", "Locked", model.summary.locked)}
        ${renderSummaryButton("blocked", "Blocked", model.summary.blocked)}
        ${renderSummaryButton("done", "Done", model.summary.done)}
        ${renderSummaryButton("all", "Total", model.summary.total)}
      </section>

      <section class="dispatch-workspace">
        <div class="dispatch-board card">
          <div class="section-heading dispatch-board-heading">
            <div>
              <h3>Task waves</h3>
              <p class="muted">Topological order: earlier waves unblock later waves.</p>
            </div>
            <div class="chip-row dispatch-filter-row" id="dispatchFilters">
              ${FILTERS.map((filter) => renderFilterButton(filter)).join("")}
            </div>
          </div>
          <div id="dispatchGraph" class="dependency-graph dispatch-graph"></div>
        </div>

        <aside id="dispatchDetail" class="dispatch-detail card"></aside>
      </section>
    </div>
  `;
}

function renderSummaryButton(filter, label, value) {
  return `
    <button type="button" class="dispatch-summary-button status-${escapeHtml(filter)}" data-filter="${escapeHtml(filter)}">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(String(value))}</strong>
    </button>
  `;
}

function renderFilterButton(filter) {
  return `<button type="button" class="dispatch-filter-button" data-filter="${escapeHtml(filter)}">${escapeHtml(filter)}</button>`;
}

function bindDispatchControls(container, model) {
  let selectedTaskId = model.defaultTaskId;
  let activeFilter = "available";
  const graph = container.querySelector("#dispatchGraph");
  const detail = container.querySelector("#dispatchDetail");

  container.addEventListener("click", async (event) => {
    const copyButton = event.target.closest("[data-copy-kind]");
    if (copyButton) {
      const selectedRow = model.rowsById.get(selectedTaskId);
      if (!selectedRow) {
        return;
      }

      const text = copyButton.dataset.copyKind === "task" ? JSON.stringify(selectedRow.task, null, 2) : buildExecutionContext(selectedRow, model);
      await copyText(text, copyButton);
      return;
    }

    const filterButton = event.target.closest("[data-filter]");
    if (filterButton) {
      activeFilter = filterButton.dataset.filter;
      render();
      return;
    }

    const node = event.target.closest("[data-task-id]");
    if (node) {
      selectedTaskId = node.dataset.taskId;
      render();
    }
  });

  function render() {
    graph.innerHTML = renderGraph(model, activeFilter, selectedTaskId);
    detail.innerHTML = renderTaskDetail(model.rowsById.get(selectedTaskId), model);
    for (const button of container.querySelectorAll("[data-filter]")) {
      button.classList.toggle("active", button.dataset.filter === activeFilter);
      button.setAttribute("aria-pressed", String(button.dataset.filter === activeFilter));
    }
  }

  render();
}

function renderGraph(model, activeFilter, selectedTaskId) {
  if (!model.rows.length) {
    return '<p class="muted">No tasks exist in generated/task_backlog.json yet.</p>';
  }

  const columns = model.layers.map((layer) => {
    const rows = layer.taskIds
      .map((taskId) => model.rowsById.get(taskId))
      .filter(Boolean)
      .filter((row) => activeFilter === "all" || row.dispatchStatus === activeFilter);

    return `
      <section class="graph-column dispatch-wave ${layer.cyclic ? "error-card" : ""}">
        <div class="graph-column-heading">
          <h4>${escapeHtml(layer.label)}</h4>
          <span class="chip">${escapeHtml(String(rows.length))}</span>
        </div>
        <div class="graph-node-stack">
          ${rows.length ? rows.map((row) => renderGraphNode(row, selectedTaskId)).join("") : '<p class="muted dispatch-empty-wave">No tasks for this filter.</p>'}
        </div>
      </section>
    `;
  });

  return `<div class="graph-columns dispatch-columns">${columns.join("")}</div>`;
}

function renderGraphNode(row, selectedTaskId) {
  const selectedClass = row.id === selectedTaskId ? " selected" : "";
  const selectedLabel = row.id === selectedTaskId ? '<span class="chip status-active">selected</span>' : "";
  return `
    <article class="graph-node dispatch-task-card status-${escapeHtml(row.visualStatus)}${selectedClass}" data-task-id="${escapeHtml(row.id)}" tabindex="0" aria-label="${escapeHtml(`${row.id}: ${row.dispatchStatus}`)}">
      <div class="graph-node-title">
        <strong>${escapeHtml(row.id)}</strong>
        <span class="chip status-${escapeHtml(row.visualStatus)}">${escapeHtml(row.dispatchStatus)}</span>
      </div>
      <p class="dispatch-task-title">${escapeHtml(row.title)}</p>
      <div class="graph-node-meta">
        <span>${escapeHtml(row.ownerRole)} / ${escapeHtml(row.repoTarget)}</span>
        <span>${escapeHtml(row.dispatchReason)}</span>
        ${selectedLabel}
      </div>
    </article>
  `;
}

function renderTaskDetail(row, model) {
  if (!row) {
    return '<p class="muted">Select a task to see dispatch context.</p>';
  }

  return `
    <div class="dispatch-detail-actions">
      <button type="button" class="dispatch-primary-action" data-copy-kind="context">Copy Full Execution Context</button>
      <button type="button" class="dispatch-secondary-action" data-copy-kind="task">Copy Task JSON</button>
    </div>

    <div class="dispatch-detail-heading">
      <div>
        <p class="eyebrow">Selected task</p>
        <h3>${escapeHtml(row.id)}</h3>
        <p class="muted">${escapeHtml(row.title)}</p>
      </div>
      <span class="chip status-${escapeHtml(row.visualStatus)}">${escapeHtml(row.dispatchStatus)}</span>
    </div>

    <section class="dispatch-state-explain status-${escapeHtml(row.visualStatus)}">
      <h4>${escapeHtml(stateExplanationTitle(row))}</h4>
      <p>${escapeHtml(row.dispatchReason)}</p>
      ${renderUnavailableDetails(row)}
    </section>

    <div class="dispatch-facts">
      ${renderFact("Owner", row.ownerRole)}
      ${renderFact("Repo", row.repoTarget)}
      ${renderFact("Execution", row.executionStatus)}
      ${renderFact("Assignee", row.assignedTo)}
      ${renderFact("Task run path", `generated/task_runs/${row.id}.json`, true)}
    </div>

    <h4>Dependencies</h4>
    ${renderDependencyStatus(row)}

    <h4>Acceptance Criteria</h4>
    ${renderList(row.acceptanceCriteria, "No acceptance criteria listed")}

    <h4>Expected Outputs</h4>
    ${renderList(row.outputs, "No outputs listed")}

    <h4>Verification</h4>
    ${renderList(row.verification, "No verification listed")}

    <details class="dispatch-json-preview">
      <summary>Task JSON preview</summary>
      <pre class="code-block">${escapeHtml(JSON.stringify(row.task, null, 2))}</pre>
    </details>
  `;
}

function renderFact(label, value, code = false) {
  return `
    <div class="dispatch-fact">
      <dt>${escapeHtml(label)}</dt>
      <dd>${code ? `<code>${escapeHtml(value)}</code>` : escapeHtml(value)}</dd>
    </div>
  `;
}

function stateExplanationTitle(row) {
  if (row.dispatchStatus === "available") {
    return "Ready to launch";
  }

  if (row.dispatchStatus === "waiting") {
    return REVIEW_STATUSES.has(row.executionStatus) ? "Waiting for review" : "Waiting on dependencies";
  }

  if (row.dispatchStatus === "locked") {
    return "Locked by active work";
  }

  if (row.dispatchStatus === "blocked") {
    return "Blocked";
  }

  return "Completed";
}

function renderUnavailableDetails(row) {
  if (row.dispatchStatus === "available") {
    return '<p class="helper">This is the happy path: copy the context and start one fresh AI task chat.</p>';
  }

  if (row.dispatchStatus === "done") {
    return row.proof.length
      ? `<div class="helper">Proof recorded: ${escapeHtml(summarizeProof(row.proof))}</div>`
      : '<p class="helper">No proof reference is recorded on this assignment yet.</p>';
  }

  if (!row.unavailableDetails.length) {
    return "";
  }

  return `
    <ul class="list">
      ${row.unavailableDetails.map((detail) => `<li>${escapeHtml(detail)}</li>`).join("")}
    </ul>
  `;
}

function renderDependencyStatus(row) {
  const dependencyRows = row.dependsOn.map((dependencyId) => row.dependencyRows.find((dependency) => dependency.id === dependencyId));
  const knownRows = dependencyRows.filter(Boolean);
  const missingRows = row.missingDependencies;

  if (!knownRows.length && !missingRows.length) {
    return '<p class="muted">No dependencies. This task can stand alone once unclaimed.</p>';
  }

  return `
    <div class="dispatch-dependency-list">
      ${knownRows.map((dependency) => renderDependencyCard(dependency)).join("")}
      ${missingRows.map((dependencyId) => `
        <article class="dispatch-dependency-card status-blocked">
          <strong>${escapeHtml(dependencyId)}</strong>
          <span class="chip status-blocked">missing</span>
          <p class="muted">This dependency ID is referenced but not present in the backlog.</p>
        </article>
      `).join("")}
    </div>
  `;
}

function renderDependencyCard(row) {
  return `
    <article class="dispatch-dependency-card status-${escapeHtml(row.visualStatus)}">
      <div class="graph-node-title">
        <strong>${escapeHtml(row.id)}</strong>
        <span class="chip status-${escapeHtml(row.visualStatus)}">${escapeHtml(row.dispatchStatus)}</span>
      </div>
      <p>${escapeHtml(row.title)}</p>
      <p class="muted">${escapeHtml(row.dispatchReason)}</p>
      ${row.proof.length ? renderProofSummary(row.proof) : '<p class="muted">No proof reference recorded.</p>'}
    </article>
  `;
}

function renderProofSummary(proofItems) {
  return `
    <ul class="list">
      ${proofItems.map((item) => `<li>${escapeHtml(proofLabel(item))}</li>`).join("")}
    </ul>
  `;
}

function proofLabel(item) {
  const bits = [item.kind, item.status, item.path, item.summary].filter(Boolean);
  return bits.length ? bits.join(" / ") : "proof";
}

function buildExecutionContext(row, model) {
  const dependencyRows = row.dependsOn.map((dependencyId) => model.rowsById.get(dependencyId)).filter(Boolean);
  const missingDependencySummary = row.missingDependencies.length
    ? `\nMissing dependency reference(s): ${row.missingDependencies.join(", ")}`
    : "";
  const dependencySummary = dependencyRows.length
    ? dependencyRows.map((dependency) => formatDependencyContext(dependency)).join("\n")
    : "- No dependencies.";

  return `# AI Assembly Line - One Task Execution Context

You are executing exactly one task from the AI Assembly Line backlog.

Use the task executor rules from:
prompts/07-task-executor.md

Hard rules:
- Work only on the selected task.
- Do not broaden scope.
- Respect dependencies, allowed files, outputs, non-goals, and verification.
- Do not mark done without accepted proof.
- If required context is missing, return blocked with a clear blocker.
- Return one task_run JSON object only.

Expected output path:
generated/task_runs/${row.id}.json

Dispatch status: ${row.dispatchStatus}
Reason: ${row.dispatchReason}
Assigned to: ${row.assignedTo} (${row.assigneeType})
Updated at: ${row.updatedAt || "not recorded"}

## Selected Task JSON

${JSON.stringify(row.task, null, 2)}

## Current Assignment Metadata

${JSON.stringify(row.assignment ?? { task_id: row.id, status: "unclaimed" }, null, 2)}

## Active Claim Metadata

${JSON.stringify(row.activeClaim ?? { task_id: row.id, status: "none" }, null, 2)}

## Dependency Summary

${dependencySummary}${missingDependencySummary}

## Dependency Proof Summaries

${dependencyRows.length ? dependencyRows.map((dependency) => `- ${dependency.id}: ${summarizeProof(dependency.proof)}`).join("\n") : "- No dependency proof required."}

## Required Return Shape

Return exactly one JSON object compatible with contracts/task_run.schema.json:

{
  "schema_version": "0.1.0",
  "task_id": "${row.id}",
  "run_id": "<unique-run-id>",
  "actor_id": "<your-actor-id>",
  "status": "review",
  "implementation_summary": ["<what changed>"],
  "files_changed": [],
  "verification": [],
  "proof": [],
  "blockers": [],
  "notes": [],
  "updated_at": "<ISO-8601 timestamp>"
}

Use status "review" when implementation appears complete but still needs human review.
Use status "blocked" if required context or dependencies are missing.
Do not mark "done" without accepted proof.
`;
}

function formatDependencyContext(dependency) {
  return [
    `- ${dependency.id}: ${dependency.dispatchStatus}`,
    `  title: ${dependency.title}`,
    `  execution_status: ${dependency.executionStatus}`,
    `  reason: ${dependency.dispatchReason}`,
    `  proof: ${summarizeProof(dependency.proof)}`,
  ].join("\n");
}

function summarizeProof(proofItems) {
  if (!proofItems.length) {
    return "no proof recorded";
  }

  return proofItems.map((item) => proofLabel(item)).join("; ");
}

async function copyText(text, button) {
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
    } else {
      fallbackCopy(text);
    }
    flashButton(button, "Copied");
  } catch (error) {
    fallbackCopy(text);
    flashButton(button, "Copied");
  }
}

function fallbackCopy(text) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "absolute";
  textarea.style.left = "-9999px";
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
}

function flashButton(button, label) {
  const original = button.textContent;
  button.textContent = label;
  window.setTimeout(() => {
    button.textContent = original;
  }, 1200);
}

```

## `web/page-dispatch-keyboard.js`

- Category: `viewer`
- Purpose: Keyboard helper that maps Enter/Space on focused dispatch nodes to click activation.
- Required: `true`

```javascript
document.addEventListener("keydown", (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) {
    return;
  }

  const node = target.closest(".graph-node[data-task-id]");
  if (!node) {
    return;
  }

  if (event.key !== "Enter" && event.key !== " ") {
    return;
  }

  event.preventDefault();
  node.click();
});

```

## `web/page-assignments.js`

- Category: `viewer`
- Purpose: Assignments page rendering logic for task ownership, execution status, notes, and proof references.
- Required: `true`

```javascript
import { escapeHtml, initializeViewerPage, renderCardGrid, renderChipRow, renderKeyValueRows, renderList } from "./viewer-layout.js";

initializeViewerPage({
  pageId: "assignments",
  eyebrow: "Execution Coordination",
  title: "Task Assignments",
  description: "Read-only ownership, execution status, and proof view over the canonical task backlog and file-based collaboration state.",
  requiredKeys: ["taskBacklog", "collaborationState"],
  extraSourceFiles: ["contracts/collaboration_state.schema.json", "contracts/task_run.schema.json", "generated/task_runs/*.json"],
  helperNote: "Unclaimed tasks are derived from generated/task_backlog.json when no matching task_assignments entry exists.",
  renderContent(container, data) {
    const tasks = Array.isArray(data.taskBacklog) ? data.taskBacklog : [];
    const state = data.collaborationState && typeof data.collaborationState === "object" ? data.collaborationState : {};
    const actors = Array.isArray(state.actors) ? state.actors : [];
    const assignmentMap = buildAssignmentMap(state.task_assignments);
    const rows = tasks.map((task) => buildTaskView(task, assignmentMap.get(task.id), actors));
    const summary = summarizeRows(rows);

    container.innerHTML = `
      <div class="stack">
        <section class="card">
          <div class="section-heading">
            <div>
              <h2>Collaboration State</h2>
              <p class="muted">This page overlays execution ownership on top of the generated task backlog. It does not claim, edit, or lock tasks.</p>
            </div>
            <span class="chip ${summary.blocked ? "status-blocked" : "status-complete"}">${summary.blocked ? "blocked tasks" : "ready to assign"}</span>
          </div>
          ${renderKeyValueRows([
            { label: "Schema Version", value: `<code>${escapeHtml(state.schema_version ?? "unknown")}</code>` },
            { label: "Workspace", value: `<code>${escapeHtml(state.workspace_id ?? "unknown")}</code>` },
            { label: "Actors", value: escapeHtml(String(actors.length)) },
            { label: "Tasks", value: escapeHtml(String(tasks.length)) },
            { label: "Unclaimed", value: escapeHtml(String(summary.unclaimed)) },
            { label: "In Progress", value: escapeHtml(String(summary.in_progress)) },
            { label: "Review", value: escapeHtml(String(summary.review)) },
            { label: "Done", value: escapeHtml(String(summary.done)) },
            { label: "Blocked", value: escapeHtml(String(summary.blocked)) },
          ])}
        </section>

        <section class="card">
          <h3>Actors</h3>
          ${actors.length ? renderActorCards(actors) : '<p class="muted">No collaboration actors are defined yet.</p>'}
        </section>

        <section class="card">
          <h3>Task Ownership</h3>
          ${rows.length ? renderTaskCards(rows) : '<p class="muted">No tasks exist in generated/task_backlog.json yet.</p>'}
        </section>
      </div>
    `;
  },
});

function buildAssignmentMap(assignments) {
  const map = new Map();
  if (!Array.isArray(assignments)) {
    return map;
  }

  for (const assignment of assignments) {
    if (assignment && assignment.task_id) {
      map.set(assignment.task_id, assignment);
    }
  }
  return map;
}

function buildTaskView(task, assignment, actors) {
  const actor = assignment?.assigned_to ? actors.find((candidate) => candidate.actor_id === assignment.assigned_to) : null;
  return {
    id: task.id ?? "unknown-task",
    title: task.title ?? task.summary ?? task.id ?? "Untitled task",
    ownerRole: task.owner_role ?? "unknown role",
    repoTarget: task.repo_target ?? "unknown repo",
    lane: task.lane ?? "unassigned lane",
    planningStatus: task.status ?? "not set",
    executionStatus: assignment?.status ?? "unclaimed",
    assignedTo: actor?.display_name ?? assignment?.assignee_label ?? assignment?.assigned_to ?? "Unassigned",
    assigneeType: assignment?.assignee_type ?? actor?.kind ?? "unassigned",
    claimedAt: assignment?.claimed_at ?? "",
    updatedAt: assignment?.updated_at ?? "",
    proof: Array.isArray(assignment?.proof) ? assignment.proof : [],
    notes: assignment?.notes ?? "",
    dependsOn: Array.isArray(task.depends_on) ? task.depends_on : [],
    outputs: Array.isArray(task.outputs) ? task.outputs : [],
    verification: Array.isArray(task.verification) ? task.verification : [],
  };
}

function summarizeRows(rows) {
  return rows.reduce(
    (summary, row) => {
      summary.total += 1;
      const key = row.executionStatus;
      summary[key] = (summary[key] ?? 0) + 1;
      return summary;
    },
    {
      total: 0,
      unclaimed: 0,
      claimed: 0,
      in_progress: 0,
      review: 0,
      done: 0,
      blocked: 0,
      released: 0,
    },
  );
}

function renderActorCards(actors) {
  return renderCardGrid(
    actors.map((actor) => `
      <article class="card inset-card">
        <div class="section-heading">
          <div>
            <h4>${escapeHtml(actor.display_name ?? actor.actor_id ?? "Unknown actor")}</h4>
            <p class="muted"><code>${escapeHtml(actor.actor_id ?? "missing-actor-id")}</code></p>
          </div>
          <span class="chip ${statusClass(actor.status)}">${escapeHtml(actor.status ?? "unknown")}</span>
        </div>
        ${renderKeyValueRows([
          { label: "Kind", value: `<code>${escapeHtml(actor.kind ?? "unknown")}</code>` },
          { label: "Notes", value: escapeHtml(actor.notes ?? "") },
        ])}
      </article>
    `).join(""),
    "three-up",
  );
}

function renderTaskCards(rows) {
  return renderCardGrid(rows.map((row) => renderTaskCard(row)).join(""), "two-up");
}

function renderTaskCard(row) {
  return `
    <article class="card">
      <div class="section-heading">
        <div>
          <h4>${escapeHtml(row.id)}</h4>
          <p class="muted">${escapeHtml(row.title)}</p>
        </div>
        <span class="chip ${statusClass(row.executionStatus)}">${escapeHtml(row.executionStatus)}</span>
      </div>
      ${renderKeyValueRows([
        { label: "Assigned To", value: escapeHtml(row.assignedTo) },
        { label: "Assignee Type", value: `<code>${escapeHtml(row.assigneeType)}</code>` },
        { label: "Planning Status", value: `<code>${escapeHtml(row.planningStatus)}</code>` },
        { label: "Owner Role", value: escapeHtml(row.ownerRole) },
        { label: "Repo Target", value: escapeHtml(row.repoTarget) },
        { label: "Lane", value: escapeHtml(row.lane) },
        { label: "Claimed At", value: row.claimedAt ? `<code>${escapeHtml(row.claimedAt)}</code>` : '<span class="muted">not claimed</span>' },
        { label: "Updated At", value: row.updatedAt ? `<code>${escapeHtml(row.updatedAt)}</code>` : '<span class="muted">not updated</span>' },
      ])}
      <h4>Proof</h4>
      ${renderProof(row.proof)}
      <h4>Depends On</h4>
      ${renderChipRow(row.dependsOn, "No dependencies")}
      <h4>Expected Outputs</h4>
      ${renderList(row.outputs, "No outputs listed")}
      <h4>Verification</h4>
      ${renderList(row.verification, "No verification listed")}
      ${row.notes ? `<p class="helper">${escapeHtml(row.notes)}</p>` : ""}
    </article>
  `;
}

function renderProof(proof) {
  if (!proof.length) {
    return '<p class="muted">No proof submitted yet.</p>';
  }

  return `
    <div class="stack">
      ${proof.map((item) => `
        <div class="card inset-card">
          <div class="section-heading">
            <strong>${escapeHtml(item.kind ?? "proof")}</strong>
            <span class="chip ${statusClass(item.status ?? "needs_review")}">${escapeHtml(item.status ?? "needs_review")}</span>
          </div>
          <p>${escapeHtml(item.summary ?? "No proof summary provided.")}</p>
          ${item.path ? `<p class="muted"><code>${escapeHtml(item.path)}</code></p>` : ""}
        </div>
      `).join("")}
    </div>
  `;
}

function statusClass(status) {
  const safeStatus = String(status ?? "unknown").replace(/[^a-z0-9_-]/gi, "").toLowerCase();
  return `status-${safeStatus || "unknown"}`;
}

```

## `web/page-assignment-tools.js`

- Category: `viewer`
- Purpose: Static copy/download helper for generated collaboration state and executor prompts without writing files.
- Required: `true`

```javascript
import { escapeHtml } from "./viewer-layout.js";

const STATUSES = ["unclaimed", "claimed", "in_progress", "review", "done", "blocked", "released"];
let mounted = false;

installStyles();
new MutationObserver(() => void mount()).observe(document.body, { childList: true, subtree: true });
void mount();

async function mount() {
  if (mounted) return;
  const stack = document.querySelector("#pageContent .stack");
  if (!stack) return;
  mounted = true;

  const panel = document.createElement("section");
  panel.className = "card assignment-tools-panel";
  panel.innerHTML = `<h3>Copy/Paste Execution Tools</h3><p class="helper">Loading generated files...</p>`;
  stack.insertBefore(panel, stack.children[1] ?? null);

  try {
    const [tasks, state] = await Promise.all([
      fetchJson("../generated/task_backlog.json"),
      fetchJson("../generated/collaboration_state.json"),
    ]);
    render(panel, Array.isArray(tasks) ? tasks : [], state && typeof state === "object" ? state : {});
  } catch (error) {
    panel.innerHTML = `
      <h3>Copy/Paste Execution Tools</h3>
      <p class="helper">Could not auto-load generated files: ${escapeHtml(error instanceof Error ? error.message : String(error))}</p>
      <p class="muted">Serve the repo root with <code>python -m http.server 8000</code>, then open <code>http://localhost:8000/web/assignments.html</code>.</p>
    `;
  }
}

async function fetchJson(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) throw new Error(`${path}: ${response.status} ${response.statusText}`);
  return response.json();
}

function render(panel, tasks, state) {
  const actors = Array.isArray(state.actors) ? state.actors : [];
  panel.innerHTML = `
    <div class="section-heading">
      <div>
        <h3>Copy/Paste Execution Tools</h3>
        <p class="muted">Generate executor prompts and replacement <code>generated/collaboration_state.json</code> previews. Nothing is written automatically.</p>
      </div>
      <span class="chip status-planned">static helper</span>
    </div>
    <div class="builder-grid">
      <label>Task
        <select id="toolTask">${tasks.map((task) => `<option value="${escapeHtml(task.id)}">${escapeHtml(task.id)} - ${escapeHtml(task.title ?? task.summary ?? "Untitled")}</option>`).join("")}</select>
      </label>
      <label>Actor
        <select id="toolActor"><option value="">Unassigned</option>${actors.map((actor) => `<option value="${escapeHtml(actor.actor_id)}">${escapeHtml(actor.display_name ?? actor.actor_id)} (${escapeHtml(actor.kind ?? "unknown")})</option>`).join("")}</select>
      </label>
      <label>Status
        <select id="toolStatus">${STATUSES.map((status) => `<option value="${escapeHtml(status)}">${escapeHtml(status)}</option>`).join("")}</select>
      </label>
      <label class="wide-field">Notes
        <textarea id="toolNotes" rows="3" placeholder="Short assignment note"></textarea>
      </label>
      <label class="wide-field">Proof path
        <input id="toolProofPath" type="text" placeholder="generated/task_runs/<task_id>.json">
      </label>
      <label class="wide-field">Proof summary
        <textarea id="toolProofSummary" rows="3" placeholder="Optional proof summary"></textarea>
      </label>
    </div>
    <div class="button-row">
      <button id="copyPrompt" type="button">Copy Executor Prompt</button>
      <button id="previewState" type="button">Preview State JSON</button>
      <button id="copyState" type="button">Copy State JSON</button>
      <button id="downloadState" type="button">Download State JSON</button>
    </div>
    <p id="toolMessage" class="helper">Select a task to start.</p>
    <pre id="toolPreview" class="code-block">No generated preview yet.</pre>
  `;
  wire(panel, tasks, state, actors);
}

function wire(panel, tasks, state, actors) {
  const q = (id) => panel.querySelector(id);
  const taskSelect = q("#toolTask");
  const actorSelect = q("#toolActor");
  const statusSelect = q("#toolStatus");
  const notesInput = q("#toolNotes");
  const proofPathInput = q("#toolProofPath");
  const proofSummaryInput = q("#toolProofSummary");
  const message = q("#toolMessage");
  const preview = q("#toolPreview");
  const tasksById = new Map(tasks.map((task) => [task.id, task]));
  const actorsById = new Map(actors.map((actor) => [actor.actor_id, actor]));
  const assignments = new Map((Array.isArray(state.task_assignments) ? state.task_assignments : []).map((item) => [item.task_id, item]));

  const task = () => tasksById.get(taskSelect.value) ?? tasks[0] ?? null;

  function fill() {
    const selected = task();
    if (!selected) return;
    const existing = assignments.get(selected.id);
    actorSelect.value = actorsById.has(existing?.assigned_to) ? existing.assigned_to : "";
    statusSelect.value = existing?.status ?? "claimed";
    notesInput.value = existing?.notes ?? "";
    proofPathInput.value = `generated/task_runs/${selected.id}.json`;
    proofSummaryInput.value = "";
    preview.textContent = "No generated preview yet.";
    message.textContent = `Selected ${selected.id}.`;
  }

  function assignmentFor(selected) {
    const now = new Date().toISOString();
    const actor = actorSelect.value ? actorsById.get(actorSelect.value) : null;
    const previous = assignments.get(selected.id) ?? {};
    const status = statusSelect.value;
    const unassigned = !actor || status === "unclaimed" || status === "released";
    const assignment = {
      task_id: selected.id,
      assigned_to: unassigned ? null : actor.actor_id,
      assignee_type: unassigned ? "unassigned" : actor.kind,
      assignee_label: unassigned ? "Unassigned" : actor.display_name ?? actor.actor_id,
      status,
      updated_at: now,
    };
    if (!unassigned) assignment.claimed_at = previous.claimed_at ?? now;
    const notes = notesInput.value.trim() || previous.notes;
    if (notes) assignment.notes = notes;
    const proof = Array.isArray(previous.proof) ? clone(previous.proof) : [];
    const proofPath = proofPathInput.value.trim();
    const proofSummary = proofSummaryInput.value.trim();
    if (proofPath || proofSummary) {
      proof.push({
        kind: "task_run",
        ...(proofPath ? { path: proofPath } : {}),
        summary: proofSummary || `Proof recorded for ${selected.id}.`,
        status: "needs_review",
        recorded_at: now,
      });
    }
    if (proof.length) assignment.proof = proof;
    return assignment;
  }

  function stateText() {
    const selected = task();
    const payload = clone(state);
    payload.schema_version = payload.schema_version ?? "0.1.0";
    payload.workspace_id = payload.workspace_id ?? "default-workspace";
    payload.actors = Array.isArray(payload.actors) ? payload.actors : [];
    payload.task_assignments = Array.isArray(payload.task_assignments) ? payload.task_assignments : [];
    payload.task_claims = Array.isArray(payload.task_claims) ? payload.task_claims : [];
    payload.artifact_submissions = Array.isArray(payload.artifact_submissions) ? payload.artifact_submissions : [];
    payload.reviews = Array.isArray(payload.reviews) ? payload.reviews : [];
    payload.audit_events = Array.isArray(payload.audit_events) ? payload.audit_events : [];
    if (selected) {
      const nextAssignment = assignmentFor(selected);
      const index = payload.task_assignments.findIndex((item) => item.task_id === selected.id);
      if (index >= 0) payload.task_assignments[index] = nextAssignment;
      else payload.task_assignments.push(nextAssignment);
      payload.task_assignments.sort((left, right) => left.task_id.localeCompare(right.task_id));
    }
    const text = `${JSON.stringify(payload, null, 2)}\n`;
    preview.textContent = text;
    return text;
  }

  taskSelect.addEventListener("change", fill);
  fill();

  q("#copyPrompt")?.addEventListener("click", async () => {
    const selected = task();
    if (!selected) return;
    await copyText(executorPrompt(selected, assignmentFor(selected)));
    message.textContent = `Copied executor prompt for ${selected.id}.`;
  });
  q("#previewState")?.addEventListener("click", () => {
    stateText();
    message.textContent = "Generated collaboration_state.json preview.";
  });
  q("#copyState")?.addEventListener("click", async () => {
    await copyText(stateText());
    message.textContent = "Copied collaboration_state.json preview.";
  });
  q("#downloadState")?.addEventListener("click", () => {
    downloadText("collaboration_state.json", stateText());
    message.textContent = "Downloaded collaboration_state.json preview.";
  });
}

function executorPrompt(task, assignment) {
  return `Use prompts/07-task-executor.md for this exact task. Work only inside the task boundaries and return exactly one fenced json code block matching contracts/task_run.schema.json.

Save returned report to: generated/task_runs/${task.id}.json
After review, add a proof reference for that run to generated/collaboration_state.json.

Assignment metadata:
${JSON.stringify(assignment ?? {}, null, 2)}

Task JSON:
${JSON.stringify(task, null, 2)}
`;
}

async function copyText(text) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "absolute";
  textarea.style.left = "-9999px";
  document.body.append(textarea);
  textarea.select();
  document.execCommand("copy");
  textarea.remove();
}

function downloadText(filename, text) {
  const blob = new Blob([text], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function installStyles() {
  const style = document.createElement("style");
  style.textContent = `
    .builder-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin: 14px 0; }
    .builder-grid label { display: grid; gap: 6px; color: var(--muted); line-height: 1.45; }
    .builder-grid input, .builder-grid select, .builder-grid textarea { width: 100%; border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; font: inherit; color: var(--ink); background: #fffcf5; }
    .wide-field { grid-column: span 3; }
    .button-row { display: flex; flex-wrap: wrap; gap: 10px; margin: 12px 0; }
    @media (max-width: 820px) { .builder-grid { grid-template-columns: 1fr; } .wide-field { grid-column: span 1; } }
  `;
  document.head.append(style);
}

function clone(value) {
  return JSON.parse(JSON.stringify(value ?? {}));
}

```

## `web/page-task-batches.js`

- Category: `viewer`
- Purpose: Task batches page rendering logic for batch index status, batch file readiness, task nodes, and dependency graph checks.
- Required: `true`

```javascript
import { escapeHtml, initializeViewerPage, renderCardGrid, renderChipRow, renderKeyValueRows, renderList } from "./viewer-layout.js";

initializeViewerPage({
  pageId: "task-batches",
  eyebrow: "Task Batch Workflow",
  title: "Task Batches",
  description: "Read-only view of task batch index files, generated batch files, and dependency graph readiness.",
  requiredKeys: ["taskBatchIndex"],
  helperNote: "Batch files are fetched from each batch output_path. Serve the repo root locally for automatic batch loading.",
  renderContent(container, data) {
    const index = data.taskBatchIndex;
    const batches = Array.isArray(index.batches) ? index.batches : [];
    const batchSummaryId = "batchLoadSummary";
    const batchContentId = "batchContent";

    container.innerHTML = `
      <div class="stack">
        <div class="card">
          <div class="section-heading">
            <div>
              <h2>Task Batch Index</h2>
              <p class="muted">Use this page after generating <code>generated/task_batch_index.json</code> with the Task Splitter prompt.</p>
            </div>
            <span id="${batchSummaryId}" class="chip">Loading batch files...</span>
          </div>
          ${renderKeyValueRows([
            { label: "Schema Version", value: `<code>${escapeHtml(index.schema_version ?? "unknown")}</code>` },
            { label: "Source Plan", value: `<code>${escapeHtml(index.source_plan_path ?? "unknown")}</code>` },
            { label: "Batching Strategy", value: `<code>${escapeHtml(index.batching_strategy ?? "unknown")}</code>` },
            { label: "Batches", value: escapeHtml(String(batches.length)) },
            { label: "Expected Tasks", value: escapeHtml(String(sumExpectedTasks(batches))) },
          ])}
        </div>

        <article class="card">
          <h3>Copy/Paste Flow</h3>
          ${renderList([
            "Paste prompts/06-task-splitter.md into a web AI with MODE: guided and the accepted generated plan.",
            "Save the first returned JSON block as generated/task_batch_index.json.",
            "Reply continue, next, or sounds good to generate one batch file at a time.",
            "Save each returned JSON block as generated/task_batches/<batch_id>.json.",
            "Run python tools/validate_task_batches.py to validate files and graph order.",
          ])}
        </article>

        <div id="${batchContentId}" class="stack"></div>
      </div>
    `;

    void renderBatchFiles(
      container.querySelector(`#${batchContentId}`),
      container.querySelector(`#${batchSummaryId}`),
      batches,
    );
  },
});

async function renderBatchFiles(target, summaryChip, batches) {
  if (!target || !summaryChip) {
    return;
  }

  const results = await Promise.all(batches.map((batch) => loadBatch(batch)));
  const loaded = results.filter((result) => result.status === "loaded");
  const missing = results.filter((result) => result.status !== "loaded");
  const graph = analyzeGraph(batches, loaded);

  summaryChip.textContent = `${loaded.length}/${batches.length} batch files loaded`;
  summaryChip.className = missing.length ? "chip status-planned" : "chip status-complete";

  target.innerHTML = `
    ${renderGraphCard(graph)}
    ${batches.length === 0 ? '<p class="muted">No task batches are listed yet.</p>' : renderBatchCards(results)}
  `;
}

async function loadBatch(batch) {
  const path = batch.output_path;
  if (!path) {
    return { batch, status: "error", error: "Missing output_path", payload: null };
  }

  try {
    const response = await fetch(`../${path}`, { cache: "no-store" });
    if (!response.ok) {
      return { batch, status: "missing", error: `${response.status} ${response.statusText}`, payload: null };
    }
    return { batch, status: "loaded", error: "", payload: await response.json() };
  } catch (error) {
    return { batch, status: "error", error: error instanceof Error ? error.message : String(error), payload: null };
  }
}

function analyzeGraph(batches, loadedResults) {
  const batchOrder = new Map(batches.map((batch, index) => [batch.batch_id, index]));
  const tasks = new Map();
  const taskToBatch = new Map();
  const errors = [];

  for (const result of loadedResults) {
    const batchId = result.batch.batch_id;
    const payload = result.payload;
    if (!payload || payload.batch_id !== batchId || !Array.isArray(payload.tasks)) {
      errors.push(`${batchId}: batch file shape does not match expected task batch object.`);
      continue;
    }

    for (const task of payload.tasks) {
      if (!task.id) {
        errors.push(`${batchId}: task is missing id.`);
        continue;
      }
      if (tasks.has(task.id)) {
        errors.push(`Duplicate task id: ${task.id}.`);
        continue;
      }
      tasks.set(task.id, task);
      taskToBatch.set(task.id, batchId);
    }
  }

  for (const [taskId, task] of tasks.entries()) {
    for (const dependency of task.depends_on ?? []) {
      if (!tasks.has(dependency)) {
        errors.push(`${taskId} depends on unknown task ${dependency}.`);
        continue;
      }
      const dependencyBatch = taskToBatch.get(dependency);
      const taskBatch = taskToBatch.get(taskId);
      if (batchOrder.get(dependencyBatch) > batchOrder.get(taskBatch)) {
        errors.push(`${taskId} depends on ${dependency}, which is in a later batch.`);
      }
    }

    for (const blocked of task.blocks ?? []) {
      if (!tasks.has(blocked)) {
        errors.push(`${taskId} blocks unknown task ${blocked}.`);
      }
    }
  }

  const cycleError = findCycle(tasks);
  if (cycleError) {
    errors.push(cycleError);
  }

  return {
    loadedBatchCount: loadedResults.length,
    taskCount: tasks.size,
    nodes: buildGraphNodes(tasks, taskToBatch, batchOrder),
    edges: buildGraphEdges(tasks),
    errors,
  };
}

function buildGraphNodes(tasks, taskToBatch, batchOrder) {
  return Array.from(tasks.values())
    .map((task) => ({
      id: task.id,
      title: task.title ?? task.summary ?? task.id,
      status: task.status ?? "draft",
      ownerRole: task.owner_role ?? "unknown",
      repoTarget: task.repo_target ?? "unknown",
      lane: task.lane ?? "unassigned",
      batchId: taskToBatch.get(task.id) ?? "unknown-batch",
      dependsOn: Array.isArray(task.depends_on) ? task.depends_on : [],
      blocks: Array.isArray(task.blocks) ? task.blocks : [],
    }))
    .sort((left, right) => {
      const batchDelta = (batchOrder.get(left.batchId) ?? 9999) - (batchOrder.get(right.batchId) ?? 9999);
      return batchDelta || left.id.localeCompare(right.id);
    });
}

function buildGraphEdges(tasks) {
  const edges = [];

  for (const [taskId, task] of tasks.entries()) {
    for (const dependency of task.depends_on ?? []) {
      if (tasks.has(dependency)) {
        edges.push({ from: dependency, to: taskId, kind: "depends_on" });
      }
    }

    for (const blocked of task.blocks ?? []) {
      if (tasks.has(blocked)) {
        edges.push({ from: taskId, to: blocked, kind: "blocks" });
      }
    }
  }

  return edges.sort((left, right) => `${left.from}:${left.to}:${left.kind}`.localeCompare(`${right.from}:${right.to}:${right.kind}`));
}

function findCycle(tasks) {
  const indegree = new Map(Array.from(tasks.keys()).map((taskId) => [taskId, 0]));
  const outgoing = new Map(Array.from(tasks.keys()).map((taskId) => [taskId, []]));

  for (const [taskId, task] of tasks.entries()) {
    for (const dependency of task.depends_on ?? []) {
      if (!tasks.has(dependency)) {
        continue;
      }
      outgoing.get(dependency).push(taskId);
      indegree.set(taskId, indegree.get(taskId) + 1);
    }
  }

  const queue = Array.from(indegree.entries())
    .filter(([, degree]) => degree === 0)
    .map(([taskId]) => taskId)
    .sort();
  let visited = 0;

  while (queue.length) {
    const taskId = queue.shift();
    visited += 1;
    for (const dependent of outgoing.get(taskId)) {
      indegree.set(dependent, indegree.get(dependent) - 1);
      if (indegree.get(dependent) === 0) {
        queue.push(dependent);
        queue.sort();
      }
    }
  }

  return visited === tasks.size ? "" : "Task dependency graph contains a cycle.";
}

function renderGraphCard(graph) {
  const ok = graph.errors.length === 0;
  return `
    <article class="card">
      <div class="section-heading">
        <div>
          <h2>Graph Readiness</h2>
          <p class="muted">Checks loaded batch files for dependency references, blocks references, cycles, and topological batch order.</p>
        </div>
        <span class="chip ${ok ? "status-complete" : "status-blocked"}">${ok ? "graph ok" : "graph issues"}</span>
      </div>
      ${renderKeyValueRows([
        { label: "Loaded Batches", value: escapeHtml(String(graph.loadedBatchCount)) },
        { label: "Loaded Tasks", value: escapeHtml(String(graph.taskCount)) },
        { label: "Graph Edges", value: escapeHtml(String(graph.edges.length)) },
        { label: "Issues", value: escapeHtml(String(graph.errors.length)) },
      ])}
      ${renderDependencyGraph(graph)}
      <h3>Issues</h3>
      ${renderList(graph.errors, "No graph issues in loaded batches")}
    </article>
  `;
}

function renderDependencyGraph(graph) {
  if (!graph.nodes.length) {
    return `
      <h3>Dependency Graph</h3>
      <p class="muted">No loaded task nodes yet. Generate at least one batch file to populate the graph.</p>
    `;
  }

  const groups = groupNodesByBatch(graph.nodes);
  return `
    <h3>Dependency Graph</h3>
    <p class="muted">Each card is a task node. Batch columns preserve the generated topological order; dependency and blocking edges are listed below.</p>
    <div class="dependency-graph" aria-label="Task dependency graph">
      <div class="graph-columns">
        ${groups.map((group) => renderGraphColumn(group)).join("")}
      </div>
    </div>
    <h4>Edges</h4>
    ${renderGraphEdges(graph.edges)}
  `;
}

function groupNodesByBatch(nodes) {
  const groups = [];
  const byBatch = new Map();

  for (const node of nodes) {
    if (!byBatch.has(node.batchId)) {
      const group = { batchId: node.batchId, nodes: [] };
      byBatch.set(node.batchId, group);
      groups.push(group);
    }
    byBatch.get(node.batchId).nodes.push(node);
  }

  return groups;
}

function renderGraphColumn(group) {
  return `
    <section class="graph-column">
      <div class="graph-column-heading">
        <h4>${escapeHtml(group.batchId)}</h4>
        <span class="chip">${group.nodes.length} node${group.nodes.length === 1 ? "" : "s"}</span>
      </div>
      <div class="graph-node-stack">
        ${group.nodes.map((node) => renderGraphNode(node)).join("")}
      </div>
    </section>
  `;
}

function renderGraphNode(node) {
  return `
    <article class="graph-node ${taskStatusClass(node.status)}">
      <div class="graph-node-title">
        <strong>${escapeHtml(node.id)}</strong>
        <span class="chip ${taskStatusClass(node.status)}">${escapeHtml(node.status)}</span>
      </div>
      <p>${escapeHtml(node.title)}</p>
      <div class="graph-node-meta">
        <span>${escapeHtml(node.ownerRole)}</span>
        <span>${escapeHtml(node.repoTarget)}</span>
        <span>${escapeHtml(node.lane)}</span>
      </div>
      <div class="graph-node-links">
        <span>Depends on</span>
        ${renderInlineIds(node.dependsOn, "none")}
        <span>Blocks</span>
        ${renderInlineIds(node.blocks, "none")}
      </div>
    </article>
  `;
}

function renderGraphEdges(edges) {
  if (!edges.length) {
    return '<p class="muted">No dependency or blocking edges in loaded tasks.</p>';
  }

  return `
    <div class="graph-edge-list">
      ${edges.map((edge) => `
        <div class="graph-edge">
          <code>${escapeHtml(edge.from)}</code>
          <span>${edge.kind === "blocks" ? "blocks" : "feeds"}</span>
          <code>${escapeHtml(edge.to)}</code>
          <span class="chip">${escapeHtml(edge.kind)}</span>
        </div>
      `).join("")}
    </div>
  `;
}

function renderInlineIds(ids, emptyText) {
  if (!ids.length) {
    return `<span class="muted">${escapeHtml(emptyText)}</span>`;
  }

  return `<span class="inline-id-list">${ids.map((id) => `<code>${escapeHtml(id)}</code>`).join("")}</span>`;
}

function taskStatusClass(status) {
  const safeStatus = String(status ?? "draft").replace(/[^a-z0-9_-]/gi, "").toLowerCase();
  return `status-${safeStatus || "draft"}`;
}

function renderBatchCards(results) {
  return renderCardGrid(
    results.map((result) => renderBatchCard(result)).join(""),
    "two-up",
  );
}

function renderBatchCard(result) {
  const batch = result.batch;
  const payload = result.payload;
  const tasks = payload && Array.isArray(payload.tasks) ? payload.tasks : [];
  const statusClass = result.status === "loaded" ? "status-complete" : "status-planned";

  return `
    <article class="card">
      <div class="section-heading">
        <div>
          <h3>${escapeHtml(batch.batch_id ?? "unknown-batch")}</h3>
          <p class="muted"><code>${escapeHtml(batch.output_path ?? "missing-output-path")}</code></p>
        </div>
        <span class="chip ${statusClass}">${escapeHtml(result.status)}</span>
      </div>

      ${renderKeyValueRows([
        { label: "Owner Role", value: escapeHtml(batch.owner_role ?? "unknown") },
        { label: "Expected Tasks", value: escapeHtml(String(batch.expected_task_count ?? 0)) },
        { label: "Loaded Tasks", value: escapeHtml(String(tasks.length)) },
        { label: "Status", value: `<code>${escapeHtml(batch.status ?? "unknown")}</code>` },
      ])}

      <h4>Repo Targets</h4>
      ${renderChipRow(batch.repo_targets ?? [], "No repo targets")}
      <h4>Lanes</h4>
      ${renderChipRow(batch.lanes ?? [], "No lanes")}
      <h4>Milestones</h4>
      ${renderList(batch.milestones ?? [], "No milestones")}
      <h4>Depends On Batches</h4>
      ${renderList(batch.depends_on_batches ?? [], "No batch dependencies")}
      <h4>Expected Task IDs</h4>
      ${renderChipRow(batch.expected_task_ids ?? [], "No expected task IDs")}
      ${result.error ? `<p class="helper">Batch file detail: ${escapeHtml(result.error)}</p>` : ""}
    </article>
  `;
}

function sumExpectedTasks(batches) {
  return batches.reduce((total, batch) => total + Number(batch.expected_task_count ?? 0), 0);
}

```

## `web/page-prompts.js`

- Category: `viewer`
- Purpose: Prompts page rendering logic.
- Required: `true`

```javascript
import { escapeHtml, initializeViewerPage, renderCardGrid, renderChipRow, renderList } from "./viewer-layout.js";

initializeViewerPage({
  pageId: "prompts",
  eyebrow: "Agent Prompts",
  title: "Prompt Pack",
  description: "Generated role prompts rendered directly from the canonical prompt set.",
  requiredKeys: ["agentPrompts"],
  renderContent(container, data) {
    const promptSet = data.agentPrompts;

    container.innerHTML = `
      <div class="stack">
        <div class="card">
          <h2>${escapeHtml(promptSet.project_name)}</h2>
          <p class="muted">Every prompt card below renders from <code>generated/agent_prompts.json</code>.</p>
        </div>

        ${renderCardGrid(
          promptSet.prompts
            .map(
              (prompt) => `
                <article class="card">
                  <div class="chip-row">
                    <span class="chip">${escapeHtml(prompt.prompt_id)}</span>
                    <span class="chip">${escapeHtml(prompt.target_repo)}</span>
                  </div>
                  <h3>${escapeHtml(prompt.role)}</h3>
                  <div class="card-grid two-up">
                    <div>
                      <h4>Allowed Files</h4>
                      ${renderList(prompt.allowed_files)}
                    </div>
                    <div>
                      <h4>Forbidden Files</h4>
                      ${renderList(prompt.forbidden_files)}
                    </div>
                    <div>
                      <h4>Input Context Required</h4>
                      ${renderList(prompt.input_context_required)}
                    </div>
                    <div>
                      <h4>Task Boundaries</h4>
                      ${renderList(prompt.task_boundaries)}
                    </div>
                    <div>
                      <h4>Output Required</h4>
                      ${renderList(prompt.output_required)}
                    </div>
                    <div>
                      <h4>Verification Required</h4>
                      ${renderList(prompt.verification_required)}
                    </div>
                  </div>
                </article>
              `,
            )
            .join(""),
          "two-up",
        )}
      </div>
    `;
  },
});

```

## `web/page-slots.js`

- Category: `viewer`
- Purpose: Slots page rendering logic.
- Required: `true`

```javascript
import { escapeHtml, initializeViewerPage, renderCardGrid, renderChipRow, renderList } from "./viewer-layout.js";

initializeViewerPage({
  pageId: "slots",
  eyebrow: "Agent Slot Board",
  title: "Slots",
  description: "Generated slot records grouped by current status from the canonical slot database.",
  requiredKeys: ["slotsDb"],
  renderContent(container, data) {
    const slots = data.slotsDb;
    const statusOrder = ["active", "ready", "planned", "review", "blocked", "complete"];
    const groups = new Map(statusOrder.map((status) => [status, []]));

    for (const slot of slots) {
      if (!groups.has(slot.status)) {
        groups.set(slot.status, []);
      }
      groups.get(slot.status).push(slot);
    }

    container.innerHTML = `
      <div class="stack">
        ${Array.from(groups.entries())
          .filter(([, groupSlots]) => groupSlots.length > 0)
          .map(([status, groupSlots]) => renderSlotGroup(status, groupSlots))
          .join("")}
      </div>
    `;
  },
});

function renderSlotGroup(status, slots) {
  return `
    <section class="card">
      <div class="section-heading">
        <h2>${escapeHtml(status)}</h2>
        <span class="chip status-${escapeHtml(status)}">${slots.length} slot${slots.length === 1 ? "" : "s"}</span>
      </div>
      ${renderCardGrid(slots.map((slot) => renderSlotCard(slot)).join(""), "three-up")}
    </section>
  `;
}

function renderSlotCard(slot) {
  return `
    <article class="card inset-card">
      <div class="chip-row">
        <span class="chip">${escapeHtml(slot.role)}</span>
        <span class="chip status-${escapeHtml(slot.status)}">${escapeHtml(slot.status)}</span>
      </div>
      <h3>${escapeHtml(slot.slot_id)}</h3>
      ${slot.notes ? `<p class="muted">${escapeHtml(slot.notes)}</p>` : ""}
      <h4>Inputs</h4>
      ${renderList(slot.inputs)}
      <h4>Outputs</h4>
      ${renderList(slot.outputs)}
      <h4>Allowed Actions</h4>
      ${renderList(slot.allowed_actions)}
      <h4>Verification Requirements</h4>
      ${renderList(slot.verification_requirements)}
    </article>
  `;
}

```

## `web/page-planning-runs.js`

- Category: `viewer`
- Purpose: Planning-runs page rendering logic for scaffold presence, output completeness, and run status.
- Required: `true`

```javascript
import { escapeHtml, initializeViewerPage, renderCardGrid, renderKeyValueRows, renderList } from "./viewer-layout.js";

const REQUIRED_OUTPUTS = [
  "project_spec.json",
  "repo_plan.json",
  "task_backlog.json",
  "agent_prompts.json",
  "slots_db.json",
];

initializeViewerPage({
  pageId: "planning-runs",
  eyebrow: "Manual Planning Run Index",
  title: "Planning Runs",
  description: "Read-only view of planning run folders, scaffold completeness, and generated output readiness.",
  requiredKeys: ["planningRunsIndex"],
  helperNote: "This page renders the derived planning-run index only. Rebuild it with python tools/build_planning_runs_index.py after creating or updating planning runs.",
  renderContent(container, data) {
    const index = data.planningRunsIndex;
    const runs = Array.isArray(index.runs) ? index.runs : [];
    const totalRuns = runs.length;
    const completeRuns = runs.filter((run) => run.status === "outputs_present").length;
    const incompleteRuns = totalRuns - completeRuns;

    container.innerHTML = `
      <div class="stack">
        <div class="card">
          <h2>Planning Run Index</h2>
          ${renderKeyValueRows([
            { label: "Schema Version", value: `<code>${escapeHtml(index.schema_version ?? "unknown")}</code>` },
            { label: "Generated By", value: `<code>${escapeHtml(index.generated_by ?? "unknown")}</code>` },
            { label: "Planning Runs Path", value: `<code>${escapeHtml(index.planning_runs_path ?? "planning_runs")}</code>` },
            { label: "Runs", value: escapeHtml(String(totalRuns)) },
            { label: "Complete Runs", value: escapeHtml(String(completeRuns)) },
            { label: "Incomplete Runs", value: escapeHtml(String(incompleteRuns)) },
          ])}
        </div>

        <article class="card">
          <h3>Required Outputs</h3>
          ${renderList(index.required_outputs ?? REQUIRED_OUTPUTS)}
        </article>

        ${runs.length === 0 ? `<p class="muted">No planning runs found in the index.</p>` : renderRuns(runs)}
      </div>
    `;
  },
});

function renderRuns(runs) {
  return renderCardGrid(
    runs.map((run) => renderRunCard(run)).join(""),
    "two-up",
  );
}

function renderRunCard(run) {
  const outputs = run.outputs ?? {};
  const missingOutputs = Array.isArray(run.missing_outputs) ? run.missing_outputs : [];
  const missingScaffold = Array.isArray(run.missing_scaffold) ? run.missing_scaffold : [];

  return `
    <article class="card">
      <div class="section-heading">
        <div>
          <h3>${escapeHtml(run.slug ?? "unnamed-run")}</h3>
          <p class="muted"><code>${escapeHtml(run.path ?? "planning_runs/unknown")}</code></p>
        </div>
        <span class="chip ${statusClass(run.status)}">${escapeHtml(run.status ?? "unknown")}</span>
      </div>

      ${renderKeyValueRows([
        { label: "Input Idea", value: renderBoolean(run.has_input_idea) },
        { label: "Planning Prompt", value: renderBoolean(run.has_planning_prompt) },
        { label: "Review Notes", value: renderBoolean(run.has_review_notes) },
        { label: "Outputs Directory", value: renderBoolean(run.has_outputs_dir) },
      ])}

      <h4>Output Files</h4>
      <div class="chip-row">
        ${REQUIRED_OUTPUTS.map((name) => renderOutputChip(name, outputs[name])).join("")}
      </div>

      <h4>Missing Outputs</h4>
      ${renderList(missingOutputs, "No missing output files")}

      <h4>Missing Scaffold</h4>
      ${renderList(missingScaffold, "No missing scaffold files")}
    </article>
  `;
}

function renderOutputChip(name, present) {
  const label = present ? `${name}: present` : `${name}: missing`;
  const className = present ? "chip status-complete" : "chip status-blocked";
  return `<span class="${className}">${escapeHtml(label)}</span>`;
}

function renderBoolean(value) {
  const label = value ? "present" : "missing";
  const className = value ? "chip status-complete" : "chip status-blocked";
  return `<span class="${className}">${label}</span>`;
}

function statusClass(status) {
  if (status === "outputs_present") {
    return "status-complete";
  }

  if (status === "draft_partial_outputs" || status === "draft_missing_outputs") {
    return "status-planned";
  }

  if (status === "invalid_missing_scaffold") {
    return "status-blocked";
  }

  return "";
}

```

## `web/page-verification.js`

- Category: `viewer`
- Purpose: Verification page rendering logic, including raw contract display.
- Required: `true`

```javascript
import { CONTRACT_FILES, formatError, isFileProtocol, loadTextFile } from "./viewer-data.js";
import { escapeHtml, initializeViewerPage, renderCardGrid, renderChipRow, renderList } from "./viewer-layout.js";

const CONTRACT_ENTRIES = [
  { id: "projectSpecSchema", path: "contracts/project_spec.schema.json", kind: "json" },
  { id: "repoPlanSchema", path: "contracts/repo_plan.schema.json", kind: "json" },
  { id: "taskSchema", path: "contracts/task.schema.json", kind: "json" },
  { id: "taskBatchIndexSchema", path: "contracts/task_batch_index.schema.json", kind: "json" },
  { id: "taskBatchSchema", path: "contracts/task_batch.schema.json", kind: "json" },
  { id: "slotSchema", path: "contracts/slot.schema.json", kind: "json" },
  { id: "agentPromptSchema", path: "contracts/agent_prompt.schema.json", kind: "json" },
  { id: "collaborationStateSchema", path: "contracts/collaboration_state.schema.json", kind: "json" },
  { id: "apiContract", path: "contracts/api_contract.openapi.yaml", kind: "text" },
];

initializeViewerPage({
  pageId: "verification",
  eyebrow: "Verification",
  title: "Verification Rules And Proof Requirements",
  description: "Read-only verification view assembled from the generated project spec, backlog, prompts, and slots.",
  requiredKeys: ["projectSpec", "taskBacklog", "agentPrompts", "slotsDb"],
  extraSourceFiles: CONTRACT_ENTRIES.map((entry) => entry.path),
  helperNote:
    "Generated JSON files can still be loaded with the local file picker. Contract files are fetched from repository paths separately and are most reliable when the repo root is served with python -m http.server 8000.",
  renderContent(container, data) {
    const taskGroups = groupTaskVerification(data.taskBacklog);
    const promptCards = data.agentPrompts.prompts.map(
      (prompt) => `
        <article class="card">
          <div class="chip-row">
            <span class="chip">${escapeHtml(prompt.role)}</span>
            <span class="chip">${escapeHtml(prompt.target_repo)}</span>
          </div>
          <h3>${escapeHtml(prompt.prompt_id)}</h3>
          <h4>Verification Required</h4>
          ${renderList(prompt.verification_required)}
          <h4>Task Boundaries</h4>
          ${renderList(prompt.task_boundaries)}
        </article>
      `,
    );

    const slotCards = data.slotsDb.map(
      (slot) => `
        <article class="card">
          <div class="chip-row">
            <span class="chip">${escapeHtml(slot.role)}</span>
            <span class="chip status-${escapeHtml(slot.status)}">${escapeHtml(slot.status)}</span>
          </div>
          <h3>${escapeHtml(slot.slot_id)}</h3>
          <h4>Verification Requirements</h4>
          ${renderList(slot.verification_requirements)}
        </article>
      `,
    );

    container.innerHTML = `
      <div class="stack">
        ${renderCardGrid(
          `
            <article class="card">
              <h2>Source Of Truth Notes</h2>
              <p class="muted">This page renders verification expectations from generated JSON plus raw contract files and keeps the frontend read-only.</p>
              <h3>Generated Artifacts</h3>
              ${renderList([
                "generated/project_spec.json defines top-level verification tasks and scope boundaries.",
                "generated/task_backlog.json defines task acceptance criteria and proof checks.",
                "generated/agent_prompts.json defines role-level verification requirements.",
                "generated/slots_db.json defines slot verification requirements.",
              ])}
              <h3>Contracts</h3>
              ${renderList(CONTRACT_ENTRIES.map((entry) => `${entry.path} is rendered read-only as raw contract content.`))}
            </article>
            <article class="card">
              <h2>Project Verification Rules</h2>
              <h3>Verification Tasks</h3>
              ${renderList(data.projectSpec.verification_tasks)}
              <h3>Safety Boundaries</h3>
              ${renderList(data.projectSpec.safety_boundaries)}
            </article>
          `,
          "two-up",
        )}

        <section class="card">
          <div class="section-heading">
            <h2>Backlog Proof Requirements</h2>
            <span class="chip">${data.taskBacklog.length} task${data.taskBacklog.length === 1 ? "" : "s"}</span>
          </div>
          <div class="stack">
            ${taskGroups
              .map(
                ([repoTarget, tasks]) => `
                  <article class="card inset-card">
                    <div class="section-heading">
                      <div>
                        <h3>${escapeHtml(repoTarget)}</h3>
                        <p class="muted">Acceptance criteria and verification steps grouped by existing <code>repo_target</code>.</p>
                      </div>
                      <span class="chip">${tasks.length} task${tasks.length === 1 ? "" : "s"}</span>
                    </div>
                    <div class="stack">
                      ${tasks
                        .map(
                          (task) => `
                            <div class="card inset-card">
                              <div class="chip-row">
                                <span class="chip">${escapeHtml(task.id)}</span>
                                <span class="chip">${escapeHtml(task.owner_role)}</span>
                              </div>
                              <h4>${escapeHtml(task.title)}</h4>
                              <div class="card-grid two-up">
                                <div>
                                  <h5>Acceptance Criteria</h5>
                                  ${renderList(task.acceptance_criteria)}
                                </div>
                                <div>
                                  <h5>Verification</h5>
                                  ${renderList(task.verification)}
                                </div>
                              </div>
                            </div>
                          `,
                        )
                        .join("")}
                    </div>
                  </article>
                `,
              )
              .join("")}
          </div>
        </section>

        <section class="card">
          <h2>Prompt Verification Requirements</h2>
          ${renderCardGrid(promptCards.join(""), "two-up")}
        </section>

        <section class="card">
          <h2>Slot Verification Requirements</h2>
          ${renderCardGrid(slotCards.join(""), "three-up")}
        </section>

        <section class="card">
          <div class="section-heading">
            <div>
              <h2>Contracts</h2>
              <p class="muted">Each contract is shown read-only with its source path and raw content.</p>
            </div>
            <span id="contractLoadSummary" class="chip">Loading contracts...</span>
          </div>
          <div id="contractsContent" class="stack"></div>
        </section>
      </div>
    `;

    void renderContracts(container.querySelector("#contractsContent"), container.querySelector("#contractLoadSummary"));
  },
});

function groupTaskVerification(tasks) {
  const groups = new Map();

  for (const task of tasks) {
    if (!groups.has(task.repo_target)) {
      groups.set(task.repo_target, []);
    }
    groups.get(task.repo_target).push(task);
  }

  return Array.from(groups.entries());
}

async function renderContracts(target, summaryChip) {
  if (!target || !summaryChip) {
    return;
  }

  const results = await Promise.all(CONTRACT_ENTRIES.map((entry) => loadContractEntry(entry)));
  const failures = results.filter((result) => result.status === "error").length;

  summaryChip.textContent = failures
    ? `${failures} contract load failure${failures === 1 ? "" : "s"}`
    : `${results.length} contracts loaded`;
  summaryChip.className = failures ? "chip status-blocked" : "chip status-ready";

  target.innerHTML = results.map((result) => renderContractCard(result)).join("");
}

async function loadContractEntry(entry) {
  try {
    const raw = await loadTextFile(CONTRACT_FILES[entry.id]);

    if (entry.kind === "json") {
      try {
        JSON.parse(raw);
        return { ...entry, status: "success", parseStatus: "JSON parse OK", raw };
      } catch (error) {
        return { ...entry, status: "error", parseStatus: `JSON parse failed: ${formatError(error)}`, raw };
      }
    }

    return { ...entry, status: "success", parseStatus: "Raw text rendered", raw };
  } catch (error) {
    const detail = isFileProtocol()
      ? `${formatError(error)} Serve the repo root with python -m http.server 8000 to load contract files.`
      : formatError(error);

    return { ...entry, status: "error", parseStatus: detail, raw: "" };
  }
}

function renderContractCard(result) {
  const statusClass = result.status === "success" ? "status success" : "status error";
  const body = result.raw
    ? `<pre class="code-block">${escapeHtml(result.raw)}</pre>`
    : '<p class="muted">No contract content available.</p>';

  return `
    <article class="card inset-card">
      <div class="section-heading">
        <div>
          <h3>${escapeHtml(result.path)}</h3>
          <p class="${statusClass}">${escapeHtml(result.parseStatus)}</p>
        </div>
        <span class="chip">${escapeHtml(result.kind === "json" ? "JSON schema" : "YAML draft")}</span>
      </div>
      ${body}
    </article>
  `;
}

```

## `web/viewer.css`

- Category: `viewer`
- Purpose: Shared static viewer styles, including dispatch state and focus/active styling.
- Required: `true`

```css
:root {
  --bg: #f3efe6;
  --paper: #fffdf8;
  --ink: #1f2421;
  --muted: #5f665d;
  --line: #d2c8b7;
  --accent: #1f5c4a;
  --accent-soft: #d9ebe4;
  --warn: #9d3d1f;
  --warn-soft: #f8e4dd;
  --shadow: 0 16px 40px rgba(47, 40, 26, 0.08);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  color: var(--ink);
  background:
    radial-gradient(circle at top left, rgba(31, 92, 74, 0.12), transparent 28%),
    linear-gradient(180deg, #efe7d7 0%, var(--bg) 38%, #f6f2ea 100%);
}

code {
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 0.92em;
}

.shell-width {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
}

.hero {
  padding: 32px 0 20px;
  display: flex;
  gap: 24px;
  align-items: flex-start;
  justify-content: space-between;
}

.hero-copy {
  display: grid;
  gap: 16px;
}

.eyebrow {
  margin: 0 0 8px;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--accent);
  font-size: 0.8rem;
  font-weight: 700;
}

h1 {
  margin: 0 0 10px;
  font-size: clamp(2.2rem, 4vw, 4rem);
  line-height: 0.95;
}

.lede {
  margin: 0;
  max-width: 760px;
  color: var(--muted);
  font-size: 1.02rem;
  line-height: 1.6;
}

.site-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.nav-link {
  color: var(--accent);
  text-decoration: none;
  padding: 9px 14px;
  border-radius: 999px;
  border: 1px solid rgba(31, 92, 74, 0.2);
  background: rgba(255, 253, 248, 0.72);
}

.nav-link.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: flex-end;
}

button,
.file-button {
  border: 1px solid var(--accent);
  background: var(--accent);
  color: #fff;
  border-radius: 999px;
  padding: 12px 16px;
  font: inherit;
  cursor: pointer;
  box-shadow: var(--shadow);
}

button:hover,
.file-button:hover {
  filter: brightness(1.04);
}

button.active {
  background: var(--paper);
  color: var(--accent);
  box-shadow: inset 0 0 0 2px rgba(31, 92, 74, 0.28), var(--shadow);
}

button:focus-visible,
.file-button:focus-visible,
.nav-link:focus-visible,
.graph-node:focus-visible {
  outline: 3px solid rgba(31, 92, 74, 0.42);
  outline-offset: 3px;
}

.file-button {
  display: inline-flex;
  align-items: center;
}

#filePicker {
  position: absolute;
  width: 1px;
  height: 1px;
  opacity: 0;
  pointer-events: none;
}

.layout {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 18px;
  padding-bottom: 32px;
}

.panel {
  grid-column: span 12;
  background: rgba(255, 253, 248, 0.92);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 20px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(8px);
}

.status-panel {
  background: linear-gradient(180deg, rgba(217, 235, 228, 0.84), rgba(255, 253, 248, 0.96));
}

h2,
h3,
h4 {
  margin-top: 0;
}

.status {
  margin: 0 0 12px;
  padding: 12px 14px;
  border-radius: 14px;
  background: var(--accent-soft);
  color: var(--accent);
}

.status.error {
  background: var(--warn-soft);
  color: var(--warn);
}

.status.success {
  background: var(--accent-soft);
  color: var(--accent);
}

.status.loading {
  background: #ebe6d7;
  color: #6e5d2d;
}

.helper,
.source-note,
.muted {
  color: var(--muted);
  line-height: 1.55;
}

.two-column {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.card-grid {
  display: grid;
  gap: 16px;
}

.card-grid.two-up {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.card-grid.three-up {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.stack {
  display: grid;
  gap: 14px;
}

.card {
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 16px;
  background: var(--paper);
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  border-radius: 999px;
  background: #ece6da;
  color: #584d3c;
  font-size: 0.88rem;
}

.chip.status-ready,
.chip.status-active,
.chip.status-complete,
.chip.status-available {
  background: var(--accent-soft);
  color: var(--accent);
}

.chip.status-planned,
.chip.status-review,
.chip.status-waiting {
  background: #eee7c8;
  color: #6d5a12;
}

.chip.status-blocked,
.chip.status-locked {
  background: var(--warn-soft);
  color: var(--warn);
}

.chip.status-done {
  background: #e5ebe7;
  color: #2f5f4d;
}

.error-card {
  border-color: rgba(157, 61, 31, 0.35);
  background: rgba(248, 228, 221, 0.7);
}

.code-block {
  margin: 0;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: #f6f1e6;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.45;
}

.list {
  margin: 0;
  padding-left: 18px;
  line-height: 1.55;
}

.meta {
  margin: 0;
  display: grid;
  gap: 10px;
}

.meta dt {
  font-weight: 700;
}

.meta dd {
  margin: 2px 0 0;
  color: var(--muted);
}

.section-heading {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

.section-heading h2,
.section-heading h3 {
  margin-bottom: 6px;
}

.inset-card {
  background: #fffcf5;
}

.dependency-graph {
  margin: 14px 0;
  overflow-x: auto;
  padding-bottom: 4px;
}

.graph-columns {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: minmax(260px, 1fr);
  gap: 14px;
  min-width: min-content;
}

.graph-column {
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 12px;
  background: linear-gradient(180deg, rgba(217, 235, 228, 0.62), rgba(255, 253, 248, 0.9));
}

.graph-column-heading,
.graph-node-title,
.graph-edge {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
}

.graph-column-heading h4 {
  margin: 0;
}

.graph-node-stack {
  display: grid;
  gap: 10px;
}

.graph-node {
  border: 1px solid rgba(31, 92, 74, 0.18);
  border-left: 5px solid var(--accent);
  border-radius: 14px;
  padding: 12px;
  background: var(--paper);
  cursor: pointer;
}

.graph-node:hover {
  box-shadow: var(--shadow);
}

.graph-node.status-available {
  border-left-color: #2f755f;
  background: linear-gradient(180deg, rgba(217, 235, 228, 0.72), var(--paper));
}

.graph-node.status-waiting {
  border-left-color: #b28b13;
}

.graph-node.status-locked,
.graph-node.status-blocked,
.graph-node.status-rejected {
  border-left-color: var(--warn);
}

.graph-node.status-done,
.graph-node.status-complete {
  border-left-color: #2f755f;
  opacity: 0.82;
}

.graph-node p {
  margin: 8px 0;
  line-height: 1.45;
}

.graph-node-meta,
.graph-node-links {
  display: grid;
  gap: 6px;
  color: var(--muted);
  font-size: 0.9rem;
}

.graph-node-links {
  grid-template-columns: max-content 1fr;
  margin-top: 10px;
}

.inline-id-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.graph-edge-list {
  display: grid;
  gap: 8px;
  max-height: 360px;
  overflow: auto;
  padding: 4px 0;
}

.graph-edge {
  justify-content: flex-start;
  flex-wrap: wrap;
  padding: 10px 12px;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: #fffcf5;
}

@media (max-width: 820px) {
  .hero {
    flex-direction: column;
  }

  .hero-actions {
    justify-content: flex-start;
  }

  .two-column {
    grid-template-columns: 1fr;
  }

  .card-grid.two-up,
  .card-grid.three-up {
    grid-template-columns: 1fr;
  }

  .section-heading {
    flex-direction: column;
  }
}

```

## `tools/validate_seed.py`

- Category: `tool`
- Purpose: Dependency-light validation script for generated JSON, contracts, and traceability consistency.
- Required: `true`

```python
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ROOT / "generated" / "project_spec.json",
    ROOT / "generated" / "repo_plan.json",
    ROOT / "generated" / "task_backlog.json",
    ROOT / "generated" / "task_batch_index.json",
    ROOT / "generated" / "agent_prompts.json",
    ROOT / "generated" / "slots_db.json",
    ROOT / "generated" / "review_manifest.json",
    ROOT / "contracts" / "project_spec.schema.json",
    ROOT / "contracts" / "repo_plan.schema.json",
    ROOT / "contracts" / "task.schema.json",
    ROOT / "contracts" / "task_batch_index.schema.json",
    ROOT / "contracts" / "task_batch.schema.json",
    ROOT / "contracts" / "slot.schema.json",
    ROOT / "contracts" / "agent_prompt.schema.json",
    ROOT / "contracts" / "collaboration_state.schema.json",
    ROOT / "contracts" / "api_contract.openapi.yaml",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def discover_json_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.json") if path.is_file())


def format_rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_optional_jsonschema():
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return None
    return jsonschema


def load_optional_yaml():
    try:
        import yaml  # type: ignore
    except ImportError:
        return None
    return yaml


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def expect_type(value: Any, expected_type: type | tuple[type, ...], label: str) -> None:
    expect(isinstance(value, expected_type), f"{label} must be {expected_type}, got {type(value)}")


def expect_non_empty_string(value: Any, label: str) -> None:
    expect_type(value, str, label)
    expect(bool(value.strip()), f"{label} must be a non-empty string")


def expect_string_array(value: Any, label: str, min_items: int = 0) -> None:
    expect_type(value, list, label)
    expect(len(value) >= min_items, f"{label} must contain at least {min_items} item(s)")
    for index, item in enumerate(value):
        expect_non_empty_string(item, f"{label}[{index}]")


def expect_object_keys(value: Any, label: str, required: set[str], optional: set[str] | None = None) -> None:
    optional = optional or set()
    expect_type(value, dict, label)
    keys = set(value.keys())
    missing = required - keys
    unexpected = keys - required - optional
    expect(not missing, f"{label} is missing required key(s): {sorted(missing)}")
    expect(not unexpected, f"{label} has unexpected key(s): {sorted(unexpected)}")


def validate_repo_unit(value: Any, label: str) -> None:
    expect_object_keys(value, label, {"name", "purpose", "contains", "depends_on"})
    expect_non_empty_string(value["name"], f"{label}.name")
    expect_non_empty_string(value["purpose"], f"{label}.purpose")
    expect_string_array(value["contains"], f"{label}.contains")
    expect_string_array(value["depends_on"], f"{label}.depends_on")


def validate_project_spec(value: Any, label: str) -> None:
    expect_object_keys(
        value,
        label,
        {
            "project_name",
            "product_summary",
            "safety_boundaries",
            "repo_split",
            "domain_model",
            "frontend_screens",
            "backend_services",
            "core_engine_responsibilities",
            "verification_tasks",
            "starter_prompts",
        },
    )
    expect_non_empty_string(value["project_name"], f"{label}.project_name")

    summary = value["product_summary"]
    expect_object_keys(summary, f"{label}.product_summary", {"goal", "users", "non_goals"})
    expect_non_empty_string(summary["goal"], f"{label}.product_summary.goal")
    expect_string_array(summary["users"], f"{label}.product_summary.users", min_items=1)
    expect_string_array(summary["non_goals"], f"{label}.product_summary.non_goals")

    expect_string_array(value["safety_boundaries"], f"{label}.safety_boundaries", min_items=1)

    repo_split = value["repo_split"]
    expect_type(repo_split, list, f"{label}.repo_split")
    expect(len(repo_split) >= 1, f"{label}.repo_split must contain at least 1 item")
    for index, item in enumerate(repo_split):
        validate_repo_unit(item, f"{label}.repo_split[{index}]")

    domain_model = value["domain_model"]
    expect_type(domain_model, list, f"{label}.domain_model")
    expect(len(domain_model) >= 1, f"{label}.domain_model must contain at least 1 item")
    for index, item in enumerate(domain_model):
        entry_label = f"{label}.domain_model[{index}]"
        expect_object_keys(item, entry_label, {"name", "fields"}, {"relations"})
        expect_non_empty_string(item["name"], f"{entry_label}.name")
        expect_string_array(item["fields"], f"{entry_label}.fields")
        if "relations" in item:
            expect_string_array(item["relations"], f"{entry_label}.relations")

    screens = value["frontend_screens"]
    expect_type(screens, list, f"{label}.frontend_screens")
    expect(len(screens) >= 1, f"{label}.frontend_screens must contain at least 1 item")
    for index, item in enumerate(screens):
        entry_label = f"{label}.frontend_screens[{index}]"
        expect_object_keys(item, entry_label, {"name", "renders_from"}, {"notes"})
        expect_non_empty_string(item["name"], f"{entry_label}.name")
        expect_string_array(item["renders_from"], f"{entry_label}.renders_from")
        if "notes" in item:
            expect_non_empty_string(item["notes"], f"{entry_label}.notes")

    services = value["backend_services"]
    expect_type(services, list, f"{label}.backend_services")
    expect(len(services) >= 1, f"{label}.backend_services must contain at least 1 item")
    for index, item in enumerate(services):
        entry_label = f"{label}.backend_services[{index}]"
        expect_object_keys(item, entry_label, {"name", "responsibility"}, {"inputs", "outputs"})
        expect_non_empty_string(item["name"], f"{entry_label}.name")
        expect_non_empty_string(item["responsibility"], f"{entry_label}.responsibility")
        if "inputs" in item:
            expect_string_array(item["inputs"], f"{entry_label}.inputs")
        if "outputs" in item:
            expect_string_array(item["outputs"], f"{entry_label}.outputs")

    expect_string_array(
        value["core_engine_responsibilities"],
        f"{label}.core_engine_responsibilities",
        min_items=1,
    )
    expect_string_array(value["verification_tasks"], f"{label}.verification_tasks", min_items=1)

    prompts = value["starter_prompts"]
    required_prompts = {
        "intake_interviewer",
        "planning_agent",
        "contract_steward",
        "frontend_builder",
        "backend_builder",
        "core_engine_builder",
        "red_team_verifier",
    }
    expect_object_keys(prompts, f"{label}.starter_prompts", required_prompts)
    for key in required_prompts:
        expect_non_empty_string(prompts[key], f"{label}.starter_prompts.{key}")


def validate_repo_plan(value: Any, label: str) -> None:
    expect_object_keys(value, label, {"project_name", "repos"})
    expect_non_empty_string(value["project_name"], f"{label}.project_name")
    repos = value["repos"]
    expect_type(repos, list, f"{label}.repos")
    expect(len(repos) >= 1, f"{label}.repos must contain at least 1 item")
    for index, item in enumerate(repos):
        entry_label = f"{label}.repos[{index}]"
        expect_object_keys(
            item,
            entry_label,
            {"name", "purpose", "contains", "depends_on", "excludes"},
        )
        expect_non_empty_string(item["name"], f"{entry_label}.name")
        expect_non_empty_string(item["purpose"], f"{entry_label}.purpose")
        expect_string_array(item["contains"], f"{entry_label}.contains")
        expect_string_array(item["depends_on"], f"{entry_label}.depends_on")
        expect_string_array(item["excludes"], f"{entry_label}.excludes")


def validate_task(value: Any, label: str) -> None:
    expect_object_keys(
        value,
        label,
        {
            "id",
            "title",
            "summary",
            "owner_role",
            "repo_target",
            "depends_on",
            "inputs",
            "outputs",
            "acceptance_criteria",
            "verification",
        },
        {
            "risk_tags",
            "notes",
            "lane",
            "allowed_areas",
            "handoff_notes",
            "status",
            "priority",
            "milestone",
            "blocks",
            "objective",
            "context",
            "implementation_notes",
            "proof_required",
            "edge_cases",
            "non_goals",
            "estimated_size",
        },
    )
    expect_non_empty_string(value["id"], f"{label}.id")
    expect(
        re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9\-]*", value["id"]) is not None,
        f"{label}.id must match ^[A-Za-z0-9][A-Za-z0-9\\-]*$",
    )
    expect_non_empty_string(value["title"], f"{label}.title")
    expect_non_empty_string(value["summary"], f"{label}.summary")
    if "objective" in value:
        expect_non_empty_string(value["objective"], f"{label}.objective")
    if "context" in value:
        expect_non_empty_string(value["context"], f"{label}.context")
    expect_non_empty_string(value["owner_role"], f"{label}.owner_role")
    if "lane" in value:
        expect_non_empty_string(value["lane"], f"{label}.lane")
    expect_non_empty_string(value["repo_target"], f"{label}.repo_target")
    if "status" in value:
        expect(
            value["status"] in {"draft", "ready", "in_progress", "blocked", "review", "done", "rejected"},
            f"{label}.status must be one of the allowed task states",
        )
    if "priority" in value:
        expect(value["priority"] in {"P0", "P1", "P2", "P3"}, f"{label}.priority must be P0, P1, P2, or P3")
    if "milestone" in value:
        expect_non_empty_string(value["milestone"], f"{label}.milestone")
    if "allowed_areas" in value:
        expect_string_array(value["allowed_areas"], f"{label}.allowed_areas")
    expect_string_array(value["depends_on"], f"{label}.depends_on")
    if "blocks" in value:
        expect_string_array(value["blocks"], f"{label}.blocks")
    expect_string_array(value["inputs"], f"{label}.inputs")
    expect_string_array(value["outputs"], f"{label}.outputs")
    if "implementation_notes" in value:
        expect_string_array(value["implementation_notes"], f"{label}.implementation_notes")
    expect_string_array(value["acceptance_criteria"], f"{label}.acceptance_criteria", min_items=1)
    expect_string_array(value["verification"], f"{label}.verification", min_items=1)
    if "proof_required" in value:
        expect_string_array(value["proof_required"], f"{label}.proof_required")
    if "edge_cases" in value:
        expect_string_array(value["edge_cases"], f"{label}.edge_cases")
    if "non_goals" in value:
        expect_string_array(value["non_goals"], f"{label}.non_goals")
    if "estimated_size" in value:
        expect(value["estimated_size"] in {"S", "M", "L"}, f"{label}.estimated_size must be S, M, or L")
    if "risk_tags" in value:
        expect_string_array(value["risk_tags"], f"{label}.risk_tags")
    if "notes" in value:
        expect_non_empty_string(value["notes"], f"{label}.notes")
    if "handoff_notes" in value:
        expect_non_empty_string(value["handoff_notes"], f"{label}.handoff_notes")


def validate_task_batch_index(value: Any, label: str) -> None:
    expect_object_keys(value, label, {"schema_version", "source_plan_path", "batching_strategy", "batches"})
    expect_non_empty_string(value["schema_version"], f"{label}.schema_version")
    expect_non_empty_string(value["source_plan_path"], f"{label}.source_plan_path")
    expect(
        value["batching_strategy"] in {"owner_role", "repo_target", "lane", "milestone", "mixed"},
        f"{label}.batching_strategy must be an allowed strategy",
    )
    expect_type(value["batches"], list, f"{label}.batches")

    batch_ids: set[str] = set()
    task_ids: set[str] = set()
    for index, batch in enumerate(value["batches"]):
        batch_label = f"{label}.batches[{index}]"
        expect_object_keys(
            batch,
            batch_label,
            {
                "batch_id",
                "owner_role",
                "repo_targets",
                "lanes",
                "milestones",
                "expected_task_count",
                "expected_task_ids",
                "depends_on_batches",
                "output_path",
                "status",
            },
            {"notes"},
        )
        expect_non_empty_string(batch["batch_id"], f"{batch_label}.batch_id")
        expect(
            re.fullmatch(r"[a-z0-9][a-z0-9\-]*", batch["batch_id"]) is not None,
            f"{batch_label}.batch_id must match ^[a-z0-9][a-z0-9\\-]*$",
        )
        expect(batch["batch_id"] not in batch_ids, f"{batch_label}.batch_id must be unique")
        batch_ids.add(batch["batch_id"])
        expect_non_empty_string(batch["owner_role"], f"{batch_label}.owner_role")
        expect_string_array(batch["repo_targets"], f"{batch_label}.repo_targets")
        expect_string_array(batch["lanes"], f"{batch_label}.lanes")
        expect_string_array(batch["milestones"], f"{batch_label}.milestones")
        expect_type(batch["expected_task_count"], int, f"{batch_label}.expected_task_count")
        expect(batch["expected_task_count"] >= 0, f"{batch_label}.expected_task_count must be >= 0")
        expect_string_array(batch["expected_task_ids"], f"{batch_label}.expected_task_ids")
        expect(
            len(batch["expected_task_ids"]) == batch["expected_task_count"],
            f"{batch_label}.expected_task_ids length must match expected_task_count",
        )
        for task_id in batch["expected_task_ids"]:
            expect(task_id not in task_ids, f"{batch_label}.expected_task_ids contains duplicate task id: {task_id}")
            task_ids.add(task_id)
        expect_string_array(batch["depends_on_batches"], f"{batch_label}.depends_on_batches")
        expect_non_empty_string(batch["output_path"], f"{batch_label}.output_path")
        expect(
            batch["output_path"] == f"generated/task_batches/{batch['batch_id']}.json",
            f"{batch_label}.output_path must match batch_id",
        )
        expect(
            batch["status"] in {"planned", "generated", "validated", "accepted", "rejected"},
            f"{batch_label}.status must be an allowed status",
        )
        if "notes" in batch:
            expect_non_empty_string(batch["notes"], f"{batch_label}.notes")

    for index, batch in enumerate(value["batches"]):
        for dependency in batch["depends_on_batches"]:
            expect(
                dependency in batch_ids,
                f"{label}.batches[{index}].depends_on_batches refers to unknown batch: {dependency}",
            )


def validate_slot(value: Any, label: str) -> None:
    expect_object_keys(
        value,
        label,
        {
            "slot_id",
            "role",
            "status",
            "inputs",
            "outputs",
            "allowed_actions",
            "verification_requirements",
        },
        {"notes"},
    )
    expect_non_empty_string(value["slot_id"], f"{label}.slot_id")
    expect(re.fullmatch(r"[a-z0-9\-]+", value["slot_id"]) is not None, f"{label}.slot_id must match ^[a-z0-9\\-]+$")
    expect_non_empty_string(value["role"], f"{label}.role")
    expect(
        value["status"] in {"planned", "ready", "active", "blocked", "review", "complete"},
        f"{label}.status must be one of the allowed slot states",
    )
    expect_string_array(value["inputs"], f"{label}.inputs")
    expect_string_array(value["outputs"], f"{label}.outputs")
    expect_string_array(value["allowed_actions"], f"{label}.allowed_actions", min_items=1)
    expect_string_array(
        value["verification_requirements"],
        f"{label}.verification_requirements",
        min_items=1,
    )
    if "notes" in value:
        expect_non_empty_string(value["notes"], f"{label}.notes")


def validate_agent_prompt_set(value: Any, label: str) -> None:
    expect_object_keys(value, label, {"project_name", "prompts"})
    expect_non_empty_string(value["project_name"], f"{label}.project_name")
    prompts = value["prompts"]
    expect_type(prompts, list, f"{label}.prompts")
    expect(len(prompts) >= 1, f"{label}.prompts must contain at least 1 item")
    for index, item in enumerate(prompts):
        entry_label = f"{label}.prompts[{index}]"
        expect_object_keys(
            item,
            entry_label,
            {
                "prompt_id",
                "role",
                "target_repo",
                "allowed_files",
                "forbidden_files",
                "input_context_required",
                "task_boundaries",
                "output_required",
                "verification_required",
            },
        )
        expect_non_empty_string(item["prompt_id"], f"{entry_label}.prompt_id")
        expect(
            re.fullmatch(r"[a-z0-9\-]+", item["prompt_id"]) is not None,
            f"{entry_label}.prompt_id must match ^[a-z0-9\\-]+$",
        )
        expect_non_empty_string(item["role"], f"{entry_label}.role")
        expect_non_empty_string(item["target_repo"], f"{entry_label}.target_repo")
        expect_string_array(item["allowed_files"], f"{entry_label}.allowed_files")
        expect_string_array(item["forbidden_files"], f"{entry_label}.forbidden_files")
        expect_string_array(
            item["input_context_required"],
            f"{entry_label}.input_context_required",
            min_items=1,
        )
        expect_string_array(item["task_boundaries"], f"{entry_label}.task_boundaries", min_items=1)
        expect_string_array(item["output_required"], f"{entry_label}.output_required", min_items=1)
        expect_string_array(
            item["verification_required"],
            f"{entry_label}.verification_required",
            min_items=1,
        )


def validate_without_jsonschema(path: Path, payload: Any) -> list[str]:
    rel = format_rel(path)
    messages: list[str] = []

    if rel == "generated/project_spec.json":
        validate_project_spec(payload, rel)
        return [f"SCHEMA OK   {rel} -> contracts/project_spec.schema.json (builtin)"]
    if rel == "generated/repo_plan.json":
        validate_repo_plan(payload, rel)
        return [f"SCHEMA OK   {rel} -> contracts/repo_plan.schema.json (builtin)"]
    if rel == "generated/agent_prompts.json":
        validate_agent_prompt_set(payload, rel)
        return [f"SCHEMA OK   {rel} -> contracts/agent_prompt.schema.json (builtin)"]
    if rel == "generated/task_batch_index.json":
        validate_task_batch_index(payload, rel)
        return [f"SCHEMA OK   {rel} -> contracts/task_batch_index.schema.json (builtin)"]
    if rel == "examples/coc-base-builder/generated-repo-plan.json":
        validate_repo_plan(payload, rel)
        return [f"SCHEMA OK   {rel} -> contracts/repo_plan.schema.json (builtin)"]
    if rel in {"generated/task_backlog.json", "examples/coc-base-builder/generated-task-backlog.json"}:
        expect_type(payload, list, rel)
        for index, item in enumerate(payload):
            validate_task(item, f"{rel}[{index}]")
            messages.append(f"SCHEMA OK   {rel}[{index}] -> contracts/task.schema.json (builtin)")
        return messages
    if rel == "generated/slots_db.json":
        expect_type(payload, list, rel)
        for index, item in enumerate(payload):
            validate_slot(item, f"{rel}[{index}]")
            messages.append(f"SCHEMA OK   {rel}[{index}] -> contracts/slot.schema.json (builtin)")
        return messages

    return []


def validate_with_schema(
    path: Path,
    payload: Any,
    schemas: dict[str, Any],
    jsonschema_module: Any,
) -> list[str]:
    rel = format_rel(path)

    direct_map = {
        "generated/project_spec.json": "contracts/project_spec.schema.json",
        "generated/repo_plan.json": "contracts/repo_plan.schema.json",
        "generated/agent_prompts.json": "contracts/agent_prompt.schema.json",
        "examples/coc-base-builder/generated-repo-plan.json": "contracts/repo_plan.schema.json",
    }
    element_map = {
        "generated/task_backlog.json": "contracts/task.schema.json",
        "generated/task_batch_index.json": "contracts/task_batch_index.schema.json",
        "generated/slots_db.json": "contracts/slot.schema.json",
        "examples/coc-base-builder/generated-task-backlog.json": "contracts/task.schema.json",
    }

    if rel in direct_map:
        schema = schemas[direct_map[rel]]
        jsonschema_module.validate(instance=payload, schema=schema)
        return [f"SCHEMA OK   {rel} -> {direct_map[rel]}"]

    if rel in element_map:
        if not isinstance(payload, list):
            raise jsonschema_module.ValidationError("Expected a JSON array.")
        schema = schemas[element_map[rel]]
        messages = []
        for index, item in enumerate(payload):
            jsonschema_module.validate(instance=item, schema=schema)
            messages.append(
                f"SCHEMA OK   {rel}[{index}] -> {element_map[rel]}"
            )
        return messages

    if rel.startswith("generated/task_batches/") and rel.endswith(".json"):
        schema = schemas["contracts/task_batch.schema.json"]
        jsonschema_module.validate(instance=payload, schema=schema)
        return [f"SCHEMA OK   {rel} -> contracts/task_batch.schema.json"]

    return []


def collect_string_values(value: Any) -> list[str]:
    values: list[str] = []

    if isinstance(value, str):
        values.append(value)
    elif isinstance(value, list):
        for item in value:
            values.extend(collect_string_values(item))
    elif isinstance(value, dict):
        for item in value.values():
            values.extend(collect_string_values(item))

    return values


def path_exists_or_pattern(path_value: str) -> bool:
    path = ROOT / path_value
    if path.exists():
        return True
    if any(char in path_value for char in "*?[]"):
        return any(candidate.is_file() for candidate in ROOT.glob(path_value))
    if path_value.endswith("/"):
        return path.is_dir()
    return False


def validate_required_files() -> int:
    missing_count = 0
    for path in REQUIRED_FILES:
        if not path.exists():
            print(f"MISSING FAIL {format_rel(path)}")
            missing_count += 1
    return missing_count


def validate_yaml_contract() -> int:
    yaml_module = load_optional_yaml()
    rel = "contracts/api_contract.openapi.yaml"
    path = ROOT / rel

    if yaml_module is None:
        print(f"YAML SKIP {rel} (PyYAML not installed)")
        return 0

    try:
        with path.open("r", encoding="utf-8") as handle:
            yaml_module.safe_load(handle)
    except OSError as exc:
        print(f"YAML FAIL {rel}: {exc}")
        return 1
    except Exception as exc:
        print(f"YAML FAIL {rel}: {exc}")
        return 1

    print(f"YAML OK   {rel}")
    return 0


def run_consistency_checks(parsed_payloads: dict[Path, Any]) -> list[str]:
    messages: list[str] = []
    warnings: list[str] = []

    project_spec = parsed_payloads[ROOT / "generated" / "project_spec.json"]
    repo_plan = parsed_payloads[ROOT / "generated" / "repo_plan.json"]
    task_backlog = parsed_payloads[ROOT / "generated" / "task_backlog.json"]
    agent_prompts = parsed_payloads[ROOT / "generated" / "agent_prompts.json"]
    slots_db = parsed_payloads[ROOT / "generated" / "slots_db.json"]

    repo_names = {repo["name"] for repo in repo_plan["repos"]}
    task_ids = {task["id"] for task in task_backlog}

    for index, task in enumerate(task_backlog):
        expect(
            task["repo_target"] in repo_names,
            f"generated/task_backlog.json[{index}].repo_target must exist in generated/repo_plan.json",
        )
        for dependency in task["depends_on"]:
            expect(
                dependency in task_ids,
                f"generated/task_backlog.json[{index}].depends_on entry must refer to an existing task id: {dependency}",
            )

    for index, prompt in enumerate(agent_prompts["prompts"]):
        expect(
            prompt["target_repo"] in repo_names,
            f"generated/agent_prompts.json[{index}].target_repo must exist in generated/repo_plan.json",
        )

    for index, screen in enumerate(project_spec["frontend_screens"]):
        for render_path in screen["renders_from"]:
            expect(
                path_exists_or_pattern(render_path),
                f"generated/project_spec.json.frontend_screens[{index}].renders_from path must exist: {render_path}",
            )

    for repo_index, repo in enumerate(repo_plan["repos"]):
        for contains_path in repo["contains"]:
            expect(
                path_exists_or_pattern(contains_path),
                f"generated/repo_plan.json.repos[{repo_index}].contains path must exist or match a documented pattern: {contains_path}",
            )

    forbidden_strings = {
        "seed-web-placeholder",
        "web/static-docs-or-dashboard-placeholder",
    }
    generated_files = [
        ROOT / "generated" / "project_spec.json",
        ROOT / "generated" / "repo_plan.json",
        ROOT / "generated" / "task_backlog.json",
        ROOT / "generated" / "agent_prompts.json",
        ROOT / "generated" / "slots_db.json",
    ]
    for path in generated_files:
        rel = format_rel(path)
        string_values = collect_string_values(parsed_payloads[path])
        for forbidden in forbidden_strings:
            expect(
                forbidden not in string_values,
                f"{rel} must not reference stale value: {forbidden}",
            )

    screens = project_spec["frontend_screens"]
    screen_names = {screen["name"] for screen in screens}
    expected_screen_names = {
        "Overview",
        "Repo Split",
        "Task Backlog",
        "Prompt Pack",
        "Slot Board",
        "Contracts and Verification",
    }
    expect(
        expected_screen_names.issubset(screen_names),
        "generated/project_spec.json.frontend_screens must include the actual viewer pages, including Slot Board",
    )

    slot_screen = next(screen for screen in screens if screen["name"] == "Slot Board")
    expect(
        "generated/slots_db.json" in slot_screen["renders_from"],
        "generated/project_spec.json Slot Board screen must render from generated/slots_db.json",
    )

    messages.append("CONSISTENCY OK generated task repo_target values map to generated/repo_plan.json")
    messages.append("CONSISTENCY OK generated task depends_on values refer to existing task ids")
    messages.append("CONSISTENCY OK generated prompt target_repo values map to generated/repo_plan.json")
    messages.append("CONSISTENCY OK generated frontend_screens renders_from paths exist")
    messages.append("CONSISTENCY OK generated repo_plan contains paths exist or match documented patterns")
    messages.append("CONSISTENCY OK generated artifacts contain no stale web placeholder references")
    messages.append("CONSISTENCY OK generated frontend_screens includes the actual viewer pages, including Slot Board")

    prompt_roles = {prompt["role"] for prompt in agent_prompts["prompts"]}
    for slot in slots_db:
        if slot["role"] not in prompt_roles:
            warnings.append(f"CONSISTENCY WARN slot role has no matching generated prompt role: {slot['role']}")

    return messages + warnings


def main() -> int:
    missing_required = validate_required_files()
    if missing_required:
        print(f"RESULT FAIL missing_required={missing_required}")
        return 1

    json_files = discover_json_files(ROOT)
    if not json_files:
        print("No JSON files found.")
        return 1

    jsonschema_module = load_optional_jsonschema()
    schemas: dict[str, Any] = {}

    parse_failures = 0
    schema_failures = 0
    yaml_failures = 0
    parsed_payloads: dict[Path, Any] = {}

    for path in json_files:
        rel = format_rel(path)
        try:
            payload = load_json(path)
        except json.JSONDecodeError as exc:
            parse_failures += 1
            print(
                f"PARSE FAIL {rel}: {exc.msg} "
                f"(line {exc.lineno}, column {exc.colno})"
            )
            continue
        except OSError as exc:
            parse_failures += 1
            print(f"PARSE FAIL {rel}: {exc}")
            continue

        parsed_payloads[path] = payload
        print(f"JSON OK     {rel}")

        if rel.startswith("contracts/"):
            schemas[rel] = payload

    if jsonschema_module is None:
        for path, payload in parsed_payloads.items():
            rel = format_rel(path)
            try:
                messages = validate_without_jsonschema(path, payload)
                for message in messages:
                    print(message)
            except ValueError as exc:
                schema_failures += 1
                print(f"SCHEMA FAIL {rel}: {exc}")
    else:
        for path, payload in parsed_payloads.items():
            rel = format_rel(path)
            try:
                messages = validate_with_schema(
                    path=path,
                    payload=payload,
                    schemas=schemas,
                    jsonschema_module=jsonschema_module,
                )
                for message in messages:
                    print(message)
            except jsonschema_module.ValidationError as exc:
                schema_failures += 1
                detail = exc.message
                location = " -> ".join(str(part) for part in exc.absolute_path)
                if location:
                    print(f"SCHEMA FAIL {rel}: {detail} at {location}")
                else:
                    print(f"SCHEMA FAIL {rel}: {detail}")

    if parse_failures or schema_failures:
        print(
            f"RESULT FAIL parse_failures={parse_failures} "
            f"schema_failures={schema_failures}"
        )
        return 1

    yaml_failures += validate_yaml_contract()
    if yaml_failures:
        print(
            f"RESULT FAIL parse_failures={parse_failures} "
            f"schema_failures={schema_failures} "
            f"yaml_failures={yaml_failures}"
        )
        return 1

    consistency_failures = 0
    try:
        for message in run_consistency_checks(parsed_payloads):
            print(message)
    except ValueError as exc:
        consistency_failures += 1
        print(f"CONSISTENCY FAIL {exc}")

    if consistency_failures:
        print(
            f"RESULT FAIL parse_failures={parse_failures} "
            f"schema_failures={schema_failures} "
            f"consistency_failures={consistency_failures}"
        )
        return 1

    print(
        f"RESULT OK   parsed={len(parsed_payloads)} "
        f"schema_validated={'jsonschema' if jsonschema_module else 'builtin'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## `tools/build_context_pack.py`

- Category: `tool`
- Purpose: Builds the remote-review context pack from this manifest.
- Required: `true`

```python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "generated" / "review_manifest.json"
OUTPUT_PATH = ROOT / "generated" / "context_pack.md"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def file_language(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "json"
    if suffix == ".js":
        return "javascript"
    if suffix == ".html":
        return "html"
    if suffix == ".css":
        return "css"
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    if suffix == ".md":
        return "markdown"
    if suffix == ".py":
        return "python"
    return ""


def fenced_block(path: Path, content: str) -> str:
    language = file_language(path)
    fence = f"```{language}" if language else "```"
    return f"{fence}\n{content}\n```"


def build_context_pack() -> tuple[str, int, list[str], list[str]]:
    manifest = load_json(MANIFEST_PATH)
    entries = manifest["review_files"]

    warnings: list[str] = []
    missing_required: list[str] = []
    included_count = 0
    sections: list[str] = [
        "# AI Assembly Line Context Pack",
        "",
        "This file is generated from `generated/review_manifest.json` by `tools/build_context_pack.py`.",
        "Treat the Git repository as the only source of truth and do not rely on chat history.",
        "",
    ]

    for entry in entries:
        rel_path = entry["path"]
        category = entry["category"]
        purpose = entry["purpose"]
        required = bool(entry["required"])
        path = ROOT / rel_path

        if path == OUTPUT_PATH:
            sections.extend(
                [
                    f"## `{rel_path}`",
                    "",
                    f"- Category: `{category}`",
                    f"- Purpose: {purpose}",
                    f"- Required: `{str(required).lower()}`",
                    "",
                    "_Skipped self-embedding to avoid recursive context-pack inclusion._",
                    "",
                ]
            )
            included_count += 1
            print(f"SKIP SELF {rel_path}")
            continue

        if not path.exists():
            message = f"{'ERROR' if required else 'WARN '} missing {'required' if required else 'optional'} file: {rel_path}"
            if required:
                missing_required.append(rel_path)
            else:
                warnings.append(message)
            print(message)
            continue

        content = path.read_text(encoding="utf-8")
        sections.extend(
            [
                f"## `{rel_path}`",
                "",
                f"- Category: `{category}`",
                f"- Purpose: {purpose}",
                f"- Required: `{str(required).lower()}`",
                "",
                fenced_block(path, content),
                "",
            ]
        )
        included_count += 1
        print(f"INCLUDED {rel_path}")

    text = "\n".join(sections).rstrip() + "\n"
    return text, included_count, warnings, missing_required


def report_warnings(warnings: list[str]) -> None:
    for warning in warnings:
        print(warning)


def fail_on_missing_required(missing_required: list[str]) -> int | None:
    if not missing_required:
        return None

    print(f"RESULT FAIL missing_required={len(missing_required)}")
    return 1


def write_context_pack(text: str, included_count: int, warnings: list[str], missing_required: list[str]) -> int:
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"WROTE {OUTPUT_PATH.relative_to(ROOT).as_posix()}")

    report_warnings(warnings)

    missing_result = fail_on_missing_required(missing_required)
    if missing_result is not None:
        return missing_result

    print(f"RESULT OK included={included_count} warnings={len(warnings)}")
    return 0


def check_context_pack(text: str, included_count: int, warnings: list[str], missing_required: list[str]) -> int:
    report_warnings(warnings)

    missing_result = fail_on_missing_required(missing_required)
    if missing_result is not None:
        return missing_result

    if not OUTPUT_PATH.exists():
        print("RESULT FAIL context_pack_missing=1")
        print("generated/context_pack.md does not exist.")
        print("Run: python tools\\build_context_pack.py")
        return 1

    current_text = OUTPUT_PATH.read_text(encoding="utf-8")
    if current_text != text:
        print("RESULT FAIL context_pack_stale=1")
        print("generated/context_pack.md is stale relative to generated/review_manifest.json and its referenced files.")
        print("Run: python tools\\build_context_pack.py")
        print("Then commit the regenerated generated/context_pack.md.")
        return 1

    print(f"RESULT OK context_pack_fresh=true included={included_count} warnings={len(warnings)}")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or check the remote-review context pack.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Rebuild the expected context pack in memory and fail if generated/context_pack.md is stale.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    text, included_count, warnings, missing_required = build_context_pack()

    if args.check:
        return check_context_pack(text, included_count, warnings, missing_required)

    return write_context_pack(text, included_count, warnings, missing_required)


if __name__ == "__main__":
    sys.exit(main())

```

## `tools/init_planning_run.py`

- Category: `tool`
- Purpose: Initializes a manual planning-run folder and refreshes the AI-ready planning prompt.
- Required: `true`

```python
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANNING_RUNS_DIR = ROOT / "planning_runs"
REQUIRED_OUTPUTS = [
    "project_spec.json",
    "repo_plan.json",
    "task_backlog.json",
    "agent_prompts.json",
    "slots_db.json",
]


def usage() -> int:
    print("Usage: python tools/init_planning_run.py <run-slug>")
    return 1


def validate_slug(run_slug: str) -> None:
    if re.fullmatch(r"[a-z0-9][a-z0-9\\-]*", run_slug) is None:
        raise ValueError("run-slug must match ^[a-z0-9][a-z0-9\\-]*$")


def default_input_idea() -> str:
    return (
        "# Input Idea\n\n"
        "Replace this text with the rough software idea for the planning run.\n"
        "Describe the product, target users, constraints, and any known safety concerns.\n"
    ).strip()


def planning_prompt(run_slug: str, input_idea: str) -> str:
    output_list = "\n".join(f"- `{name}`" for name in REQUIRED_OUTPUTS)
    return f"""# Planning Run Prompt

You are producing a manual planning run for the `ai-assembly-line` workflow.

## Run Slug

`{run_slug}`

## Goal

Convert the rough software idea below into a safe, structured planning artifact set.

Generated outputs are drafts until a human accepts them.
If the idea implies unsafe automation, botting, account control, live-service interference, or other unsafe behavior, safely reinterpret it into the nearest safe planning-only scope or explicitly reject the unsafe parts.

## Rough Idea

{input_idea}

## Required Output Files

Return exactly these artifact types:

{output_list}

## Output Requirements

- `project_spec.json` must describe the product summary, boundaries, repo split, domain model, frontend screens, backend services, core engine responsibilities, verification tasks, and starter prompts.
- `repo_plan.json` must define the repo ownership split.
- `task_backlog.json` must define tasks with owners, dependencies, acceptance criteria, and verification.
- `agent_prompts.json` must define prompt boundaries tied to the repo split.
- `slots_db.json` must define role slots and verification requirements.

## Constraints

- Produce planning artifacts only.
- Do not implement software.
- Do not add hidden workflow state.
- Keep outputs human-reviewable and machine-readable.
- Keep repo targets, task dependencies, prompts, and slots internally consistent.

## Response Format

Return each file in its own fenced code block with the filename immediately above the fence, for example:

`project_spec.json`
```json
{{ ... }}
```

Use valid JSON for all five files.
"""


def review_template() -> str:
    return """# Review

## Outcome

- [ ] Accepted
- [ ] Needs revision
- [ ] Rejected

## Review Notes

- Safety interpretation:
- Structural validity:
- Repo/task/prompt/slot coherence:
- Reviewer decision rationale:
"""


def outputs_readme() -> str:
    expected = "\n".join(f"- `{name}`" for name in REQUIRED_OUTPUTS)
    return f"""# Outputs

Save the AI-returned planning artifacts for this run in this folder.

Expected files:

{expected}

Validate them with:

```powershell
python tools\\validate_planning_run.py <path-to-this-folder>
```
"""


def write_if_missing(path: Path, content: str) -> str:
    if path.exists():
        return "exists"
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return "created"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return usage()

    run_slug = argv[1]
    try:
        validate_slug(run_slug)
    except ValueError as exc:
        print(f"ERROR {exc}")
        return 1

    run_dir = PLANNING_RUNS_DIR / run_slug
    outputs_dir = run_dir / "outputs"
    run_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    input_idea_path = run_dir / "input-idea.md"
    input_status = write_if_missing(input_idea_path, default_input_idea())
    input_idea = input_idea_path.read_text(encoding="utf-8").strip()

    planning_prompt_path = run_dir / "planning-run.md"
    planning_prompt_path.write_text(planning_prompt(run_slug, input_idea).rstrip() + "\n", encoding="utf-8")

    review_status = write_if_missing(run_dir / "review-notes.md", review_template())
    outputs_status = write_if_missing(outputs_dir / "README.md", outputs_readme())

    print(f"RUN DIR   {run_dir.relative_to(ROOT).as_posix()}")
    print(f"INPUT     {input_status} {input_idea_path.relative_to(ROOT).as_posix()}")
    print(f"PROMPT    updated {planning_prompt_path.relative_to(ROOT).as_posix()}")
    print(f"REVIEW    {review_status} {run_dir.joinpath('review-notes.md').relative_to(ROOT).as_posix()}")
    print(f"OUTPUTS   {outputs_status} {outputs_dir.joinpath('README.md').relative_to(ROOT).as_posix()}")
    print("NEXT      edit input-idea.md, rerun this script, paste planning-run.md into a web AI, save outputs/, validate, and review")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

```

## `tools/validate_planning_run.py`

- Category: `tool`
- Purpose: Validates saved planning-run output artifacts against existing contracts and cross-artifact consistency checks.
- Required: `true`

```python
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import validate_seed


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_OUTPUTS = {
    "project_spec.json": "contracts/project_spec.schema.json",
    "repo_plan.json": "contracts/repo_plan.schema.json",
    "task_backlog.json": "contracts/task.schema.json",
    "agent_prompts.json": "contracts/agent_prompt.schema.json",
    "slots_db.json": "contracts/slot.schema.json",
}


def usage() -> int:
    print("Usage: python tools/validate_planning_run.py <run-dir-or-outputs-dir>")
    return 1


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def resolve_outputs_dir(path_arg: str) -> Path:
    candidate = Path(path_arg).resolve()
    if not candidate.exists() or not candidate.is_dir():
        raise ValueError(f"run or outputs directory not found: {path_arg}")
    if candidate.name == "outputs":
        return candidate
    outputs_dir = candidate / "outputs"
    if outputs_dir.exists() and outputs_dir.is_dir():
        return outputs_dir
    return candidate


def validate_required_outputs(outputs_dir: Path) -> int:
    missing_count = 0
    for file_name in REQUIRED_OUTPUTS:
        path = outputs_dir / file_name
        if not path.exists():
            print(f"MISSING FAIL {path.relative_to(ROOT).as_posix()}")
            missing_count += 1
    return missing_count


def validate_builtin_payloads(outputs_dir: Path, payloads: dict[str, Any]) -> list[str]:
    messages: list[str] = []

    validate_seed.validate_project_spec(payloads["project_spec.json"], f"{outputs_dir.name}/project_spec.json")
    messages.append("SCHEMA OK   project_spec.json -> contracts/project_spec.schema.json (builtin)")

    validate_seed.validate_repo_plan(payloads["repo_plan.json"], f"{outputs_dir.name}/repo_plan.json")
    messages.append("SCHEMA OK   repo_plan.json -> contracts/repo_plan.schema.json (builtin)")

    validate_seed.validate_agent_prompt_set(payloads["agent_prompts.json"], f"{outputs_dir.name}/agent_prompts.json")
    messages.append("SCHEMA OK   agent_prompts.json -> contracts/agent_prompt.schema.json (builtin)")

    task_backlog = payloads["task_backlog.json"]
    validate_seed.expect_type(task_backlog, list, f"{outputs_dir.name}/task_backlog.json")
    for index, task in enumerate(task_backlog):
        validate_seed.validate_task(task, f"{outputs_dir.name}/task_backlog.json[{index}]")
        messages.append(f"SCHEMA OK   task_backlog.json[{index}] -> contracts/task.schema.json (builtin)")

    slots_db = payloads["slots_db.json"]
    validate_seed.expect_type(slots_db, list, f"{outputs_dir.name}/slots_db.json")
    for index, slot in enumerate(slots_db):
        validate_seed.validate_slot(slot, f"{outputs_dir.name}/slots_db.json[{index}]")
        messages.append(f"SCHEMA OK   slots_db.json[{index}] -> contracts/slot.schema.json (builtin)")

    return messages


def validate_jsonschema_payloads(outputs_dir: Path, payloads: dict[str, Any]) -> list[str]:
    jsonschema_module = validate_seed.load_optional_jsonschema()
    if jsonschema_module is None:
        return validate_builtin_payloads(outputs_dir, payloads)

    messages: list[str] = []
    schemas = {
        schema_path: load_json(ROOT / schema_path)
        for schema_path in REQUIRED_OUTPUTS.values()
    }

    jsonschema_module.validate(payloads["project_spec.json"], schemas["contracts/project_spec.schema.json"])
    messages.append("SCHEMA OK   project_spec.json -> contracts/project_spec.schema.json")

    jsonschema_module.validate(payloads["repo_plan.json"], schemas["contracts/repo_plan.schema.json"])
    messages.append("SCHEMA OK   repo_plan.json -> contracts/repo_plan.schema.json")

    jsonschema_module.validate(payloads["agent_prompts.json"], schemas["contracts/agent_prompt.schema.json"])
    messages.append("SCHEMA OK   agent_prompts.json -> contracts/agent_prompt.schema.json")

    task_backlog = payloads["task_backlog.json"]
    validate_seed.expect_type(task_backlog, list, f"{outputs_dir.name}/task_backlog.json")
    for index, task in enumerate(task_backlog):
        jsonschema_module.validate(task, schemas["contracts/task.schema.json"])
        messages.append(f"SCHEMA OK   task_backlog.json[{index}] -> contracts/task.schema.json")

    slots_db = payloads["slots_db.json"]
    validate_seed.expect_type(slots_db, list, f"{outputs_dir.name}/slots_db.json")
    for index, slot in enumerate(slots_db):
        jsonschema_module.validate(slot, schemas["contracts/slot.schema.json"])
        messages.append(f"SCHEMA OK   slots_db.json[{index}] -> contracts/slot.schema.json")

    return messages


def run_consistency_checks(payloads: dict[str, Any]) -> list[str]:
    project_spec = payloads["project_spec.json"]
    repo_plan = payloads["repo_plan.json"]
    task_backlog = payloads["task_backlog.json"]
    agent_prompts = payloads["agent_prompts.json"]
    slots_db = payloads["slots_db.json"]

    repo_names = {repo["name"] for repo in repo_plan["repos"]}
    task_ids = {task["id"] for task in task_backlog}

    validate_seed.expect(
        project_spec["project_name"] == repo_plan["project_name"] == agent_prompts["project_name"],
        "project_name must match across project_spec.json, repo_plan.json, and agent_prompts.json",
    )

    for index, task in enumerate(task_backlog):
        validate_seed.expect(
            task["repo_target"] in repo_names,
            f"task_backlog.json[{index}].repo_target must exist in repo_plan.json",
        )
        for dependency in task["depends_on"]:
            validate_seed.expect(
                dependency in task_ids,
                f"task_backlog.json[{index}].depends_on must refer to an existing task id: {dependency}",
            )

    for index, prompt in enumerate(agent_prompts["prompts"]):
        validate_seed.expect(
            prompt["target_repo"] in repo_names,
            f"agent_prompts.json[{index}].target_repo must exist in repo_plan.json",
        )

    prompt_roles = {prompt["role"] for prompt in agent_prompts["prompts"]}
    warnings = []
    for slot in slots_db:
        if slot["role"] not in prompt_roles:
            warnings.append(f"CONSISTENCY WARN slot role has no matching prompt role: {slot['role']}")

    return [
        "CONSISTENCY OK project_name aligns across primary artifacts",
        "CONSISTENCY OK task repo_target values map to repo_plan.json",
        "CONSISTENCY OK task depends_on values refer to existing task ids",
        "CONSISTENCY OK prompt target_repo values map to repo_plan.json",
        *warnings,
    ]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return usage()

    try:
        outputs_dir = resolve_outputs_dir(argv[1])
    except ValueError as exc:
        print(f"ERROR {exc}")
        return 1

    missing_required = validate_required_outputs(outputs_dir)
    if missing_required:
        print(f"RESULT FAIL missing_required={missing_required}")
        return 1

    payloads: dict[str, Any] = {}
    parse_failures = 0

    for file_name in REQUIRED_OUTPUTS:
        path = outputs_dir / file_name
        rel = path.relative_to(ROOT).as_posix()
        try:
            payloads[file_name] = load_json(path)
            print(f"JSON OK     {rel}")
        except json.JSONDecodeError as exc:
            parse_failures += 1
            print(f"PARSE FAIL {rel}: {exc.msg} (line {exc.lineno}, column {exc.colno})")
        except OSError as exc:
            parse_failures += 1
            print(f"PARSE FAIL {rel}: {exc}")

    if parse_failures:
        print(f"RESULT FAIL parse_failures={parse_failures}")
        return 1

    schema_failures = 0
    try:
        for message in validate_jsonschema_payloads(outputs_dir, payloads):
            print(message)
    except Exception as exc:
        schema_failures += 1
        print(f"SCHEMA FAIL {outputs_dir.relative_to(ROOT).as_posix()}: {exc}")

    if schema_failures:
        print(f"RESULT FAIL schema_failures={schema_failures}")
        return 1

    consistency_failures = 0
    try:
        for message in run_consistency_checks(payloads):
            print(message)
    except ValueError as exc:
        consistency_failures += 1
        print(f"CONSISTENCY FAIL {exc}")

    if consistency_failures:
        print(f"RESULT FAIL consistency_failures={consistency_failures}")
        return 1

    print("RESULT OK   planning_run_outputs_valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

```

## `tools/build_planning_runs_index.py`

- Category: `tool`
- Purpose: Builds the derived planning-runs index consumed by later read-only review surfaces.
- Required: `true`

```python
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLANNING_RUNS_DIR = ROOT / "planning_runs"
OUTPUT_PATH = ROOT / "generated" / "planning_runs_index.json"

REQUIRED_OUTPUTS = [
    "project_spec.json",
    "repo_plan.json",
    "task_backlog.json",
    "agent_prompts.json",
    "slots_db.json",
]

SCAFFOLD_FILES = {
    "input_idea": "input-idea.md",
    "planning_prompt": "planning-run.md",
    "review_notes": "review-notes.md",
}


def posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_run_entry(run_dir: Path) -> dict[str, Any]:
    outputs_dir = run_dir / "outputs"
    outputs = {name: (outputs_dir / name).is_file() for name in REQUIRED_OUTPUTS}

    scaffold_presence = {
        key: (run_dir / filename).is_file()
        for key, filename in SCAFFOLD_FILES.items()
    }
    scaffold_presence["outputs_dir"] = outputs_dir.is_dir()

    missing_scaffold = [
        filename
        for key, filename in SCAFFOLD_FILES.items()
        if not scaffold_presence[key]
    ]
    if not scaffold_presence["outputs_dir"]:
        missing_scaffold.append("outputs/")

    missing_outputs = [name for name, present in outputs.items() if not present]
    present_outputs = [name for name, present in outputs.items() if present]

    if missing_scaffold:
        status = "invalid_missing_scaffold"
    elif not present_outputs:
        status = "draft_missing_outputs"
    elif missing_outputs:
        status = "draft_partial_outputs"
    else:
        status = "outputs_present"

    return {
        "slug": run_dir.name,
        "path": posix(run_dir),
        "status": status,
        "has_input_idea": scaffold_presence["input_idea"],
        "has_planning_prompt": scaffold_presence["planning_prompt"],
        "has_review_notes": scaffold_presence["review_notes"],
        "has_outputs_dir": scaffold_presence["outputs_dir"],
        "outputs": outputs,
        "missing_outputs": missing_outputs,
        "missing_scaffold": missing_scaffold,
    }


def discover_runs() -> list[dict[str, Any]]:
    if not PLANNING_RUNS_DIR.exists():
        return []

    runs: list[dict[str, Any]] = []
    for child in sorted(PLANNING_RUNS_DIR.iterdir(), key=lambda path: path.name):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name == "__pycache__":
            continue
        runs.append(build_run_entry(child))
    return runs


def main() -> int:
    runs = discover_runs()
    index = {
        "schema_version": "0.1.0",
        "generated_by": "tools/build_planning_runs_index.py",
        "planning_runs_path": "planning_runs",
        "required_outputs": REQUIRED_OUTPUTS,
        "runs": runs,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"WROTE {posix(OUTPUT_PATH)}")
    print(f"RESULT OK runs={len(runs)}")
    for run in runs:
        print(f"RUN {run['slug']} status={run['status']} missing_outputs={len(run['missing_outputs'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## `tools/validate_task_batches.py`

- Category: `tool`
- Purpose: Validates task batch files, task dependency graph references, and topological batch order.
- Required: `true`

```python
from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

import validate_seed


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "generated" / "task_batch_index.json"
BATCHES_DIR = ROOT / "generated" / "task_batches"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def validate_batch_index(index: Any) -> list[str]:
    validate_seed.expect_object_keys(
        index,
        "generated/task_batch_index.json",
        {"schema_version", "source_plan_path", "batching_strategy", "batches"},
    )
    validate_seed.expect_non_empty_string(index["schema_version"], "task_batch_index.schema_version")
    validate_seed.expect_non_empty_string(index["source_plan_path"], "task_batch_index.source_plan_path")
    validate_seed.expect(
        index["batching_strategy"] in {"owner_role", "repo_target", "lane", "milestone", "mixed"},
        "task_batch_index.batching_strategy must be an allowed strategy",
    )
    validate_seed.expect_type(index["batches"], list, "task_batch_index.batches")

    batch_ids: set[str] = set()
    task_ids: set[str] = set()
    messages = ["SCHEMA OK   generated/task_batch_index.json -> contracts/task_batch_index.schema.json (builtin)"]

    for batch_index, batch in enumerate(index["batches"]):
        label = f"task_batch_index.batches[{batch_index}]"
        validate_seed.expect_object_keys(
            batch,
            label,
            {
                "batch_id",
                "owner_role",
                "repo_targets",
                "lanes",
                "milestones",
                "expected_task_count",
                "expected_task_ids",
                "depends_on_batches",
                "output_path",
                "status",
            },
            {"notes"},
        )
        validate_seed.expect_non_empty_string(batch["batch_id"], f"{label}.batch_id")
        validate_seed.expect(
            batch["batch_id"] not in batch_ids,
            f"{label}.batch_id must be unique: {batch['batch_id']}",
        )
        batch_ids.add(batch["batch_id"])
        validate_seed.expect_non_empty_string(batch["owner_role"], f"{label}.owner_role")
        validate_seed.expect_string_array(batch["repo_targets"], f"{label}.repo_targets")
        validate_seed.expect_string_array(batch["lanes"], f"{label}.lanes")
        validate_seed.expect_string_array(batch["milestones"], f"{label}.milestones")
        validate_seed.expect_type(batch["expected_task_count"], int, f"{label}.expected_task_count")
        validate_seed.expect(batch["expected_task_count"] >= 0, f"{label}.expected_task_count must be >= 0")
        validate_seed.expect_string_array(batch["expected_task_ids"], f"{label}.expected_task_ids")
        validate_seed.expect(
            len(batch["expected_task_ids"]) == batch["expected_task_count"],
            f"{label}.expected_task_ids length must match expected_task_count",
        )
        for task_id in batch["expected_task_ids"]:
            validate_seed.expect(task_id not in task_ids, f"task id appears in multiple batches: {task_id}")
            task_ids.add(task_id)
        validate_seed.expect_string_array(batch["depends_on_batches"], f"{label}.depends_on_batches")
        validate_seed.expect_non_empty_string(batch["output_path"], f"{label}.output_path")
        validate_seed.expect(
            batch["output_path"] == f"generated/task_batches/{batch['batch_id']}.json",
            f"{label}.output_path must be generated/task_batches/{batch['batch_id']}.json",
        )
        validate_seed.expect(
            batch["status"] in {"planned", "generated", "validated", "accepted", "rejected"},
            f"{label}.status must be an allowed status",
        )
        if "notes" in batch:
            validate_seed.expect_non_empty_string(batch["notes"], f"{label}.notes")

    for batch_index, batch in enumerate(index["batches"]):
        for dependency in batch["depends_on_batches"]:
            validate_seed.expect(
                dependency in batch_ids,
                f"task_batch_index.batches[{batch_index}].depends_on_batches refers to unknown batch: {dependency}",
            )

    return messages


def validate_task_batch(path: Path, payload: Any, expected_batch: dict[str, Any]) -> list[str]:
    label = rel(path)
    validate_seed.expect_object_keys(payload, label, {"schema_version", "batch_id", "source_plan_path", "tasks"})
    validate_seed.expect_non_empty_string(payload["schema_version"], f"{label}.schema_version")
    validate_seed.expect(
        payload["batch_id"] == expected_batch["batch_id"],
        f"{label}.batch_id must match task_batch_index: {expected_batch['batch_id']}",
    )
    validate_seed.expect_non_empty_string(payload["source_plan_path"], f"{label}.source_plan_path")
    validate_seed.expect_type(payload["tasks"], list, f"{label}.tasks")
    validate_seed.expect(
        len(payload["tasks"]) == expected_batch["expected_task_count"],
        f"{label}.tasks length must match expected_task_count",
    )

    expected_task_ids = set(expected_batch["expected_task_ids"])
    actual_task_ids = set()
    messages = [f"SCHEMA OK   {label} -> contracts/task_batch.schema.json (builtin)"]

    for task_index, task in enumerate(payload["tasks"]):
        task_label = f"{label}.tasks[{task_index}]"
        validate_seed.validate_task(task, task_label)
        validate_seed.expect(
            task["id"] in expected_task_ids,
            f"{task_label}.id is not listed in task_batch_index expected_task_ids: {task['id']}",
        )
        validate_seed.expect(task["id"] not in actual_task_ids, f"duplicate task id in {label}: {task['id']}")
        actual_task_ids.add(task["id"])
        messages.append(f"SCHEMA OK   {task_label} -> contracts/task.schema.json (builtin)")

    missing = expected_task_ids - actual_task_ids
    validate_seed.expect(not missing, f"{label} is missing expected task id(s): {sorted(missing)}")
    return messages


def topological_order(tasks: dict[str, dict[str, Any]]) -> list[str]:
    indegree = {task_id: 0 for task_id in tasks}
    outgoing: dict[str, list[str]] = defaultdict(list)

    for task_id, task in tasks.items():
        for dependency in task["depends_on"]:
            validate_seed.expect(
                dependency in tasks,
                f"task {task_id} depends_on unknown task id: {dependency}",
            )
            outgoing[dependency].append(task_id)
            indegree[task_id] += 1

        for blocked in task.get("blocks", []):
            validate_seed.expect(
                blocked in tasks,
                f"task {task_id} blocks unknown task id: {blocked}",
            )

    queue = deque(sorted(task_id for task_id, degree in indegree.items() if degree == 0))
    ordered: list[str] = []

    while queue:
        task_id = queue.popleft()
        ordered.append(task_id)
        for dependent in sorted(outgoing[task_id]):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                queue.append(dependent)

    validate_seed.expect(
        len(ordered) == len(tasks),
        "task dependency graph contains a cycle",
    )
    return ordered


def validate_batch_order(index: dict[str, Any], task_to_batch: dict[str, str], tasks: dict[str, dict[str, Any]]) -> list[str]:
    batch_order = {batch["batch_id"]: index for index, batch in enumerate(index["batches"])}

    for task_id, task in tasks.items():
        task_batch = task_to_batch[task_id]
        for dependency in task["depends_on"]:
            dependency_batch = task_to_batch[dependency]
            validate_seed.expect(
                batch_order[dependency_batch] <= batch_order[task_batch],
                f"batch order violation: task {task_id} depends on later batch task {dependency}",
            )

    return ["GRAPH OK    batch order respects task dependencies"]


def main() -> int:
    if not INDEX_PATH.is_file():
        print(f"MISSING FAIL {rel(INDEX_PATH)}")
        return 1

    try:
        index = load_json(INDEX_PATH)
    except Exception as exc:
        print(f"PARSE FAIL {rel(INDEX_PATH)}: {exc}")
        return 1

    failures = 0
    all_tasks: dict[str, dict[str, Any]] = {}
    task_to_batch: dict[str, str] = {}

    try:
        for message in validate_batch_index(index):
            print(message)

        expected_batches = {batch["batch_id"]: batch for batch in index["batches"]}
        for batch in index["batches"]:
            path = ROOT / batch["output_path"]
            if batch["status"] == "planned" and not path.exists():
                print(f"BATCH SKIP  {batch['batch_id']} status=planned output_missing_ok")
                continue

            validate_seed.expect(path.is_file(), f"missing task batch file: {batch['output_path']}")
            payload = load_json(path)
            for message in validate_task_batch(path, payload, batch):
                print(message)

            for task in payload["tasks"]:
                validate_seed.expect(task["id"] not in all_tasks, f"duplicate task id across batches: {task['id']}")
                all_tasks[task["id"]] = task
                task_to_batch[task["id"]] = batch["batch_id"]

        for path in sorted(BATCHES_DIR.glob("*.json")):
            batch_id = path.stem
            validate_seed.expect(batch_id in expected_batches, f"unexpected task batch file not in index: {rel(path)}")

        if all_tasks:
            ordered = topological_order(all_tasks)
            print(f"GRAPH OK    tasks_topologically_sorted={len(ordered)}")
            for message in validate_batch_order(index, task_to_batch, all_tasks):
                print(message)
        else:
            print("GRAPH OK    no generated task batches yet")

    except Exception as exc:
        failures += 1
        print(f"RESULT FAIL {exc}")

    if failures:
        return 1

    print(f"RESULT OK   batches={len(index['batches'])} tasks={len(all_tasks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## `tools/build_task_backlog_from_batches.py`

- Category: `tool`
- Purpose: Merges validated generated task batches into canonical generated/task_backlog.json while refusing empty-batch overwrites.
- Required: `true`

```python
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import validate_task_batches
import validate_seed


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "generated" / "task_batch_index.json"
OUTPUT_PATH = ROOT / "generated" / "task_backlog.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def build_backlog(index: dict[str, Any]) -> list[dict[str, Any]]:
    validate_task_batches.validate_batch_index(index)
    validate_seed.expect(
        len(index["batches"]) > 0,
        "task_batch_index.batches is empty; refusing to overwrite generated/task_backlog.json",
    )

    all_tasks: dict[str, dict[str, Any]] = {}
    task_to_batch: dict[str, str] = {}

    for batch in index["batches"]:
        batch_path = ROOT / batch["output_path"]
        validate_seed.expect(
            batch_path.is_file(),
            f"missing task batch file: {batch['output_path']}",
        )

        payload = load_json(batch_path)
        validate_task_batches.validate_task_batch(batch_path, payload, batch)

        for task in payload["tasks"]:
            task_id = task["id"]
            validate_seed.expect(task_id not in all_tasks, f"duplicate task id across batches: {task_id}")
            all_tasks[task_id] = task
            task_to_batch[task_id] = batch["batch_id"]

    ordered_task_ids = validate_task_batches.topological_order(all_tasks)
    validate_task_batches.validate_batch_order(index, task_to_batch, all_tasks)
    return [all_tasks[task_id] for task_id in ordered_task_ids]


def main() -> int:
    if not INDEX_PATH.is_file():
        print(f"MISSING FAIL {rel(INDEX_PATH)}")
        return 1

    try:
        index = load_json(INDEX_PATH)
        backlog = build_backlog(index)
        write_json(OUTPUT_PATH, backlog)
    except Exception as exc:
        print(f"RESULT FAIL {exc}")
        return 1

    print(f"RESULT OK   wrote {rel(OUTPUT_PATH)} tasks={len(backlog)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## `tools/validate_collaboration_state.py`

- Category: `tool`
- Purpose: Validates file-based collaboration state, task assignments, and task run proof reports against the canonical backlog and actor list.
- Required: `true`

```python
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASK_BACKLOG_PATH = ROOT / "generated" / "task_backlog.json"
COLLABORATION_STATE_PATH = ROOT / "generated" / "collaboration_state.json"
TASK_RUNS_DIR = ROOT / "generated" / "task_runs"

VALID_ASSIGNMENT_STATUSES = {"unclaimed", "claimed", "in_progress", "review", "done", "blocked", "released"}
VALID_ACTOR_KINDS = {"human", "web_ai", "local_ai", "service"}
VALID_RUN_STATUSES = {"review", "done", "blocked", "failed"}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def expect_string(value: Any, label: str, allow_empty: bool = False) -> None:
    expect(isinstance(value, str), f"{label} must be a string")
    if not allow_empty:
        expect(bool(value.strip()), f"{label} must be a non-empty string")


def expect_list(value: Any, label: str) -> None:
    expect(isinstance(value, list), f"{label} must be a list")


def validate_actor(actor: Any, label: str) -> str:
    expect(isinstance(actor, dict), f"{label} must be an object")
    expect_string(actor.get("actor_id"), f"{label}.actor_id")
    expect_string(actor.get("display_name"), f"{label}.display_name")
    expect(actor.get("kind") in VALID_ACTOR_KINDS, f"{label}.kind must be a valid actor kind")
    expect(actor.get("status") in {"active", "inactive", "blocked"}, f"{label}.status must be a valid actor status")
    return actor["actor_id"]


def validate_assignment(assignment: Any, label: str, task_ids: set[str], actor_ids: set[str]) -> str:
    expect(isinstance(assignment, dict), f"{label} must be an object")
    expect_string(assignment.get("task_id"), f"{label}.task_id")
    task_id = assignment["task_id"]
    expect(task_id in task_ids, f"{label}.task_id must refer to generated/task_backlog.json: {task_id}")
    expect(assignment.get("status") in VALID_ASSIGNMENT_STATUSES, f"{label}.status must be a valid assignment status")
    expect_string(assignment.get("updated_at"), f"{label}.updated_at")

    assigned_to = assignment.get("assigned_to")
    if assigned_to is not None:
        expect_string(assigned_to, f"{label}.assigned_to")
        expect(assigned_to in actor_ids, f"{label}.assigned_to must refer to actors[].actor_id: {assigned_to}")
    elif assignment.get("status") not in {"unclaimed", "released"}:
        raise ValueError(f"{label}.assigned_to is required unless status is unclaimed or released")

    proof = assignment.get("proof", [])
    expect_list(proof, f"{label}.proof")
    for proof_index, proof_ref in enumerate(proof):
        proof_label = f"{label}.proof[{proof_index}]"
        expect(isinstance(proof_ref, dict), f"{proof_label} must be an object")
        expect_string(proof_ref.get("kind"), f"{proof_label}.kind")
        expect_string(proof_ref.get("summary"), f"{proof_label}.summary")
        path_value = proof_ref.get("path")
        if path_value:
            expect_string(path_value, f"{proof_label}.path")

    return task_id


def validate_task_run(path: Path, payload: Any, task_ids: set[str], actor_ids: set[str]) -> list[str]:
    label = rel(path)
    expect(isinstance(payload, dict), f"{label} must be an object")
    expect_string(payload.get("task_id"), f"{label}.task_id")
    expect(payload["task_id"] in task_ids, f"{label}.task_id must refer to generated/task_backlog.json")
    expect_string(payload.get("run_id"), f"{label}.run_id")
    expect_string(payload.get("actor_id"), f"{label}.actor_id")
    expect(payload["actor_id"] in actor_ids, f"{label}.actor_id must refer to collaboration actors")
    expect(payload.get("status") in VALID_RUN_STATUSES, f"{label}.status must be a valid task run status")
    expect_string(payload.get("implementation_summary"), f"{label}.implementation_summary")
    expect_list(payload.get("files_changed"), f"{label}.files_changed")
    expect_list(payload.get("verification"), f"{label}.verification")
    expect_list(payload.get("proof"), f"{label}.proof")
    expect_list(payload.get("blockers"), f"{label}.blockers")
    expect_string(payload.get("updated_at"), f"{label}.updated_at")
    return [f"TASK RUN OK {label}"]


def main() -> int:
    try:
        task_backlog = load_json(TASK_BACKLOG_PATH)
        state = load_json(COLLABORATION_STATE_PATH)

        expect_list(task_backlog, rel(TASK_BACKLOG_PATH))
        expect(isinstance(state, dict), f"{rel(COLLABORATION_STATE_PATH)} must be an object")

        task_ids = {task["id"] for task in task_backlog if isinstance(task, dict) and "id" in task}
        expect(len(task_ids) == len(task_backlog), "generated/task_backlog.json must contain unique task ids")

        expect_list(state.get("actors"), "collaboration_state.actors")
        actor_ids = set()
        for index, actor in enumerate(state["actors"]):
            actor_id = validate_actor(actor, f"collaboration_state.actors[{index}]")
            expect(actor_id not in actor_ids, f"duplicate actor_id: {actor_id}")
            actor_ids.add(actor_id)

        expect_list(state.get("task_assignments"), "collaboration_state.task_assignments")
        assigned_task_ids = set()
        for index, assignment in enumerate(state["task_assignments"]):
            task_id = validate_assignment(assignment, f"collaboration_state.task_assignments[{index}]", task_ids, actor_ids)
            expect(task_id not in assigned_task_ids, f"duplicate task assignment for task_id: {task_id}")
            assigned_task_ids.add(task_id)

        messages = [
            f"COLLAB OK actors={len(actor_ids)} assignments={len(assigned_task_ids)} unclaimed={len(task_ids - assigned_task_ids)}"
        ]

        if TASK_RUNS_DIR.is_dir():
            for path in sorted(TASK_RUNS_DIR.glob("*.json")):
                messages.extend(validate_task_run(path, load_json(path), task_ids, actor_ids))

        for message in messages:
            print(message)
    except Exception as exc:
        print(f"RESULT FAIL {exc}")
        return 1

    print("RESULT OK   collaboration state is internally consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## `tools/sync_and_check.ps1`

- Category: `tool`
- Purpose: Local helper that pulls GitHub-side changes, rebuilds generated indexes/context, validates artifacts, and reports status.
- Required: `false`

```
param(
    [string]$PlanningRun = "",
    [switch]$SkipPlanningRun,
    [switch]$StrictPlanningRun,
    [switch]$NoPull
)

$ErrorActionPreference = "Stop"

function Invoke-NativeChecked {
    param(
        [string]$Label,
        [scriptblock]$Command,
        [switch]$AllowFailure
    )

    Write-Host "`n== $Label =="
    $global:LASTEXITCODE = 0
    & $Command
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        if ($AllowFailure) {
            Write-Host "WARN: $Label returned exit code $exitCode. Continuing because this step is allowed to fail."
        } else {
            throw "$Label failed with exit code $exitCode"
        }
    }
}

function Get-GitHead {
    $global:LASTEXITCODE = 0
    $head = (git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "git rev-parse HEAD failed with exit code $LASTEXITCODE"
    }
    return $head
}

Write-Host "== AI Assembly Line: sync and check =="

Invoke-NativeChecked "Current branch" { git branch --show-current }
Invoke-NativeChecked "Current HEAD before pull" { git log --oneline -1 }

$Before = Get-GitHead

if (-not $NoPull) {
    Invoke-NativeChecked "Pull latest" { git pull --ff-only }
} else {
    Write-Host "`n== Pull latest =="
    Write-Host "Skipped because -NoPull was supplied."
}

$After = Get-GitHead

Invoke-NativeChecked "Current HEAD after pull" { git log --oneline -1 }

if ($Before -ne $After) {
    Invoke-NativeChecked "Changed commits" { git log --oneline "$Before..$After" }
    Invoke-NativeChecked "Changed files" { git diff --name-status "$Before..$After" }
} else {
    Write-Host "`n== No new commits pulled =="
}

Invoke-NativeChecked "Build planning runs index" { python tools\build_planning_runs_index.py }
Invoke-NativeChecked "Validate seed" { python tools\validate_seed.py }
Invoke-NativeChecked "Validate task batches" { python tools\validate_task_batches.py }
Invoke-NativeChecked "Validate collaboration state" { python tools\validate_collaboration_state.py }
Invoke-NativeChecked "Check context pack freshness" { python tools\build_context_pack.py --check }

Invoke-NativeChecked "JavaScript syntax checks" {
    Get-ChildItem web -Filter *.js | Sort-Object Name | ForEach-Object {
        Write-Host (">>> node --check " + $_.Name)
        node --check $_.FullName
        if ($LASTEXITCODE -ne 0) {
            throw "node --check failed for $($_.FullName) with exit code $LASTEXITCODE"
        }
    }
}

if (-not $SkipPlanningRun -and $PlanningRun) {
    $allowPlanningFailure = -not $StrictPlanningRun
    Invoke-NativeChecked "Validate planning run: $PlanningRun" { python tools\validate_planning_run.py $PlanningRun } -AllowFailure:$allowPlanningFailure

    if ($allowPlanningFailure) {
        Write-Host "Planning run validation is allowed to fail by default because draft runs may intentionally omit generated outputs. Use -StrictPlanningRun to make this a hard failure."
    }
} else {
    Write-Host "`n== Validate planning run =="
    if ($SkipPlanningRun) {
        Write-Host "Skipped because -SkipPlanningRun was supplied."
    } else {
        Write-Host "Skipped because no -PlanningRun path was supplied."
        Write-Host "To validate one run, pass -PlanningRun planning_runs\<run-slug>."
    }
}

Invoke-NativeChecked "Git status" { git status --short }

Write-Host "`n== Done =="

```
