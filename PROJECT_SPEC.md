# AI Assembly Line Project Spec

## 1. Product Summary

- Project name: AI Assembly Line
- Core goal: turn rough software ideas into structured, reviewable planning artifacts before implementation begins
- Primary output: a spec compiler that converts idea notes into project specs, repo plans, task backlogs, role prompts, and verification guidance
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
- Human review is required before planning artifacts are treated as approved.
- Example projects involving games must be reinterpreted into safe planning tools when necessary.
- The system must refuse scopes that imply client automation, account access, botting, evasion, or interference with third-party live services.

## 3. Phase 0 Deliverables

- repo-level planning documents
- JSON schemas for core generated artifacts
- a seed OpenAPI contract for a future read-only/project-state API
- role-specific prompt pack
- one worked example: `coc-base-builder`

## 4. Source-of-Truth Layers

### Product Spec

- `PROJECT_SPEC.md`
- current machine-readable product spec: `generated/project_spec.json`

### Schemas

- `project_spec.schema.json`
- `slot.schema.json`
- `task.schema.json`
- `repo_plan.schema.json`

### API Contract

- `api_contract.openapi.yaml`

## 5. First Web Surface

The initial web surface should be read-only and generated from the source-of-truth files.

Current static viewer pages:

- Overview
- Repo Split
- Backlog
- Prompts
- Slots
- Verification

## 6. Frontend Constraint

The frontend must render the current `PROJECT_SPEC.md` and contract-defined generated files.

It must not invent its own:

- task model
- repo model
- prompt model
- slot model
- contract model
- verification model

## 7. Core Functional Feature

The first functional feature is the spec compiler:

`rough idea -> safe structured project specification`

The output should include:

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

## 8. Verification Strategy

- validate generated JSON against schemas
- verify examples against product rules
- verify prompt packs against scope boundaries
- verify frontend plans are contract-driven
- red-team unsafe interpretations and scope drift
