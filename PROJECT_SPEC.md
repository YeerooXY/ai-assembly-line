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
