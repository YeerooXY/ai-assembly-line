# AI Assembly Line Context Pack

This file is generated from `generated/review_manifest.json` by `tools/build_context_pack.py`.
Treat the Git repository as the only source of truth and do not rely on chat history.

## `README.md`

- Category: `root-doc`
- Purpose: Repository overview, source-of-truth rules, viewer constraints, validation guidance, and remote AI review links.
- Required: `true`

```markdown
# AI Assembly Line

`ai-assembly-line` is the seed repository for a human-in-the-loop multi-agent software assembly line.

Its first job is not autonomous execution. Its first job is project decomposition:

- rough idea -> structured project specification
- structured project specification -> repo split
- repo split -> microtask backlog
- microtask backlog -> role-specific prompt pack
- planning artifacts -> verification rules

## Phase 0 Goal

Build the planning kernel and the first "spec compiler":

`rough idea -> safe, structured project specification`

This repository is intentionally limited to planning, contracts, prompts, and read-only presentation scaffolding.

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
2. Data schemas
   - `contracts/*.schema.json`
3. API contract
   - `contracts/api_contract.openapi.yaml`
4. Canonical generated planning state
   - `generated/repo_plan.json`
   - `generated/task_backlog.json`
   - `generated/agent_prompts.json`
   - `generated/slots_db.json`

## Frontend Rule

Any frontend built from this repository must render the current product spec and contract-defined generated artifacts.

It must not invent:

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

Rule: the frontend must render generated state and must not invent task, repo, prompt, slot, or contract structure.

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
- `web/verification.html`

The generated sources remain:

- `generated/project_spec.json`
- `generated/repo_plan.json`
- `generated/task_backlog.json`
- `generated/agent_prompts.json`
- `generated/slots_db.json`

The viewer displays:

- project overview
- repository split and repo ownership
- task backlog grouped by repo target
- agent prompts
- slot board
- verification rules, source-of-truth notes, proof requirements, and raw contract files

The viewer intentionally does not do the following yet:

- editing
- backend APIs
- authentication
- realtime sync
- mutable workflow state
- frontend-owned task, repo, prompt, slot, or contract models

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
- verification rules

## Repository Map

- `PROJECT_SPEC.md`: current repo-level phase-0 specification
- `PROJECT_SPEC_TEMPLATE.md`: reusable template for future planning runs
- `PRODUCT_RULES.md`: hard rules and safety boundaries
- `docs/`: public overview, workflow, roles, task format, verification rules
- `docs/EXTERNAL_REVIEW_PROMPT.md`: fresh-clone external reviewer prompt
- `contracts/`: schemas and OpenAPI contract
- `generated/`: canonical machine-readable planning artifacts for the current seed state
- `examples/coc-base-builder/`: example decomposition for a safe base layout planner
- `prompts/`: copy-paste role prompts
- `tools/validate_seed.py`: repository JSON validation utility
- `web/`: static multi-page read-only viewer over generated state

## Remote AI Review

For remote AI or web-only review environments, start with:

- `docs/AI_CONTEXT.md`
- `docs/EXTERNAL_REVIEW_PROMPT.md`
- `generated/review_manifest.json`
- `generated/context_pack.md`

These files provide broad review context for the current repository state. They are intended to reduce setup friction for web-only review environments, not to imply that one file permanently contains the entire repository.

## Validation

Run:

```powershell
python tools/validate_seed.py
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

This repository is currently a Phase 0 planning kernel and static viewer.

Start here:
- `PROJECT_SPEC.md`
- `PRODUCT_RULES.md`
- `generated/`
- `web/index.html`

Run validation:

```powershell
python tools\validate_seed.py

```

## `PROJECT_SPEC.md`

- Category: `root-doc`
- Purpose: Human-readable phase 0 product specification and current viewer scope.
- Required: `true`

```markdown
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

The frontend must render project state from spec and generated contract files.

It must not invent:

- tasks
- repos
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
- `generated/agent_prompts.json`
- `generated/slots_db.json`

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
- role prompts
- verification rules

The initial version is deliberately narrow. It focuses on decomposition quality, contract discipline, and safe scope boundaries.

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

Produce a microtask backlog with explicit owners, dependencies, and verification criteria.

## 6. Generate Prompt Pack

Produce prompts for planner, contracts, frontend, backend, core engine, and red team roles.

## 7. Verify

Validate contracts, check rule compliance, and red-team likely drift paths.

## 8. Human Review

Accept, revise, or reject the planning outputs before any implementation phase begins.

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

- `risk_tags`
- `notes`

## Rules

- Use stable identifiers.
- Keep tasks implementation-sized.
- Make acceptance criteria externally checkable.
- Reference the source spec or contract context where possible.

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
- Purpose: Canonical machine-readable product spec and frontend screen list.
- Required: `true`

```json
{
  "project_name": "AI Assembly Line",
  "product_summary": {
    "goal": "Turn rough software ideas into structured, reviewable planning artifacts before implementation begins.",
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
    "Human review is required before generated planning artifacts are treated as approved.",
    "Unsafe requests must be rejected or safely reinterpreted into planning-only outputs.",
    "The initial frontend may render generated state but must not invent task, repo, prompt, slot, or contract structure.",
    "The phase 0 seed must remain free of authentication, databases, realtime sync, and agent automation."
  ],
  "repo_split": [
    {
      "name": "seed-docs-and-rules",
      "purpose": "Store the human-readable phase 0 specification, product rules, workflow notes, and reusable planning template.",
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
      "purpose": "Define machine-readable contracts for project specs, repo plans, tasks, slots, prompts, and future read-only APIs.",
      "contains": [
        "contracts/*.schema.json",
        "contracts/api_contract.openapi.yaml"
      ],
      "depends_on": [
        "seed-docs-and-rules"
      ]
    },
    {
      "name": "seed-generated-state",
      "purpose": "Provide canonical generated artifacts for the current seed repository state.",
      "contains": [
        "generated/project_spec.json",
        "generated/repo_plan.json",
        "generated/task_backlog.json",
        "generated/agent_prompts.json",
        "generated/slots_db.json"
      ],
      "depends_on": [
        "seed-docs-and-rules",
        "seed-contracts"
      ]
    },
    {
      "name": "seed-prompts",
      "purpose": "Store role-specific prompt source material aligned to the contracts and current project spec.",
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
        "web/prompts.html",
        "web/slots.html",
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
        "ProjectSpec drives RepoPlan, Task, AgentPrompt, and AgentSlot artifacts."
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
      "name": "Contracts and Verification",
      "renders_from": [
        "generated/project_spec.json",
        "generated/task_backlog.json",
        "generated/agent_prompts.json",
        "generated/slots_db.json",
        "contracts/project_spec.schema.json",
        "contracts/repo_plan.schema.json",
        "contracts/task.schema.json",
        "contracts/slot.schema.json",
        "contracts/agent_prompt.schema.json",
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
    "Compile rough planning intent into explicit project structure.",
    "Maintain contract-first generated artifacts for the seed repository.",
    "Preserve traceability from product rules to repo plan, tasks, prompts, and slots.",
    "Reject or reinterpret unsafe scope expansion into planning-only outputs.",
    "Support deterministic validation of machine-readable seed artifacts."
  ],
  "verification_tasks": [
    "Parse every JSON file in the repository and fail clearly on invalid syntax.",
    "Validate canonical generated project state against the contracts in contracts/.",
    "Verify that the generated artifacts stay aligned with the current phase 0 scope limits.",
    "Verify that future frontend work renders generated state and does not invent hidden models.",
    "Red-team prompt drift toward automation, auth, persistence, or realtime scope."
  ],
  "starter_prompts": {
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
      "purpose": "Own the reusable planning spec template and human-readable product rules for phase 0.",
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
      "purpose": "Own JSON schemas and the future read-only API contract.",
      "contains": [
        "contracts/project_spec.schema.json",
        "contracts/repo_plan.schema.json",
        "contracts/task.schema.json",
        "contracts/slot.schema.json",
        "contracts/agent_prompt.schema.json",
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
      "purpose": "Own the canonical machine-readable planning artifacts consumed by future read-only interfaces.",
      "contains": [
        "generated/project_spec.json",
        "generated/repo_plan.json",
        "generated/task_backlog.json",
        "generated/agent_prompts.json",
        "generated/slots_db.json"
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
      "purpose": "Own copy-paste role prompts constrained by the project spec and contracts.",
      "contains": [
        "prompts/00-planning-agent.md",
        "prompts/01-contract-steward.md",
        "prompts/02-frontend-builder.md",
        "prompts/03-backend-builder.md",
        "prompts/04-core-engine-builder.md",
        "prompts/05-red-team-verifier.md"
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
        "web/prompts.html",
        "web/slots.html",
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
- Purpose: Canonical task backlog grouped by repo ownership targets.
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

## `generated/agent_prompts.json`

- Category: `generated-state`
- Purpose: Canonical machine-readable prompt pack for the current seed.
- Required: `true`

```json
{
  "project_name": "AI Assembly Line",
  "prompts": [
    {
      "prompt_id": "planning-agent-phase0",
      "role": "Planning Agent",
      "target_repo": "seed-generated-state",
      "allowed_files": [
        "PROJECT_SPEC.md",
        "PROJECT_SPEC_TEMPLATE.md",
        "PRODUCT_RULES.md",
        "docs/",
        "generated/"
      ],
      "forbidden_files": [
        "web/app/",
        "db/",
        "auth/",
        "workers/"
      ],
      "input_context_required": [
        "Current phase specification",
        "Product rules",
        "Existing contracts"
      ],
      "task_boundaries": [
        "Produce planning artifacts only.",
        "Do not add frontend implementation, auth, databases, realtime sync, or agent automation.",
        "Keep outputs traceable to the source-of-truth spec."
      ],
      "output_required": [
        "Updated generated project state",
        "Traceable repo split",
        "Bounded task backlog"
      ],
      "verification_required": [
        "Generated outputs remain within phase 0 scope.",
        "JSON artifacts parse successfully."
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
        "Define strict contracts for machine-readable planning artifacts.",
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
        "Do not invent task, repo, prompt, slot, or contract structure.",
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
        "Repo plan"
      ],
      "task_boundaries": [
        "Stay within deterministic planning compilation and validation responsibilities.",
        "Do not build autonomous execution paths."
      ],
      "output_required": [
        "Deterministic generated planning artifacts",
        "Traceability notes across contracts and prompts"
      ],
      "verification_required": [
        "Artifacts stay deterministic and schema-aligned.",
        "No forbidden runtime scope is introduced."
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
        "Prompt pack"
      ],
      "task_boundaries": [
        "Search for unsafe reinterpretation, schema drift, and hidden state invention.",
        "Keep review findings tied to current contracts and source-of-truth files."
      ],
      "output_required": [
        "Attack cases",
        "Rejection rationale",
        "Verification gaps"
      ],
      "verification_required": [
        "Attack cases cover auth, database, realtime, automation, and invented frontend state drift.",
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
      "purpose": "Repository overview, source-of-truth rules, viewer constraints, validation guidance, and remote AI review links.",
      "required": true
    },
    {
      "path": "PROJECT_SPEC.md",
      "category": "root-doc",
      "purpose": "Human-readable phase 0 product specification and current viewer scope.",
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
      "purpose": "Canonical machine-readable product spec and frontend screen list.",
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
      "purpose": "Canonical task backlog grouped by repo ownership targets.",
      "required": true
    },
    {
      "path": "generated/agent_prompts.json",
      "category": "generated-state",
      "purpose": "Canonical machine-readable prompt pack for the current seed.",
      "required": true
    },
    {
      "path": "generated/slots_db.json",
      "category": "generated-state",
      "purpose": "Canonical slot board data consumed by the static viewer.",
      "required": true
    },
    {
      "path": "generated/review_manifest.json",
      "category": "generated-state",
      "purpose": "Remote review manifest listing the key files needed to inspect the repository without a full clone.",
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
      "path": "contracts/api_contract.openapi.yaml",
      "category": "contract",
      "purpose": "Future API and spec-compiler contract draft, not an implemented backend.",
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
      "path": "web/README.md",
      "category": "viewer",
      "purpose": "Static viewer documentation and file:// versus local server usage notes.",
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
      "purpose": "Shared viewer shell, status handling, and reusable rendering helpers.",
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
      "path": "web/page-verification.js",
      "category": "viewer",
      "purpose": "Verification page rendering logic, including raw contract display.",
      "required": true
    },
    {
      "path": "web/viewer.css",
      "category": "viewer",
      "purpose": "Shared static viewer styles.",
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
    }
  ]
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
        "planning_agent",
        "contract_steward",
        "frontend_builder",
        "backend_builder",
        "core_engine_builder",
        "red_team_verifier"
      ],
      "properties": {
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
    "id": { "type": "string", "pattern": "^[a-z0-9\\-]+$" },
    "title": { "type": "string", "minLength": 1 },
    "summary": { "type": "string", "minLength": 1 },
    "owner_role": { "type": "string", "minLength": 1 },
    "repo_target": { "type": "string", "minLength": 1 },
    "depends_on": { "type": "array", "items": { "type": "string" } },
    "inputs": { "type": "array", "items": { "type": "string" } },
    "outputs": { "type": "array", "items": { "type": "string" } },
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
    "risk_tags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "notes": {
      "type": "string"
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

## `prompts/00-planning-agent.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the planning agent role.
- Required: `true`

```markdown
# Planning Agent Prompt

You are the planning agent for AI Assembly Line.

Your job is to convert a rough idea into a structured project specification.

Required outputs:

- safe product interpretation
- product summary
- scope boundaries
- repo split
- domain model
- API contract draft
- frontend screens
- backend services
- core-engine responsibilities
- verification tasks
- role-specific starter prompts

Rules:

- work from strict files and contracts, not inferred product structure
- reinterpret unsafe automation requests into safe planning tools when possible
- reject scopes involving botting, client control, account access, emulator control, or live service interference
- keep the output implementation-ready but planning-only

```

## `prompts/01-contract-steward.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the contract steward role.
- Required: `true`

```markdown
# Contract Steward Prompt

You are the contract steward for AI Assembly Line.

Your job is to keep schemas strict, coherent, and useful to downstream builders.

Rules:

- prefer explicit required fields
- disallow undocumented structure unless there is a strong reason not to
- keep schemas aligned with `PROJECT_SPEC.md`
- ensure the frontend can render generated state directly from contracts
- reject schema drift that would let builders invent hidden state

```

## `prompts/02-frontend-builder.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the Phase 0 frontend builder role.
- Required: `true`

```markdown
# Frontend Builder Prompt

You are the frontend builder for AI Assembly Line.

Build UI from source-of-truth files:

- `PROJECT_SPEC.md`
- `generated/project_spec.json`
- `generated/repo_plan.json`
- `generated/task_backlog.json`
- `generated/agent_prompts.json`
- `generated/slots_db.json`
- `contracts/*.schema.json`
- `contracts/api_contract.openapi.yaml`

Rules:

- do not invent frontend-owned task, repo, prompt, slot, or contract structures
- render missing or invalid data as visible contract failures
- the first visible version is read-only
- no backend routes, login, realtime sync, editing, or mutable coordination logic in this phase

```

## `prompts/03-backend-builder.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the backend builder role.
- Required: `true`

```markdown
# Backend Builder Prompt

You are the backend builder for AI Assembly Line.

Implement only the HTTP surface described by `contracts/api_contract.openapi.yaml` when a later implementation phase begins.

Rules:

- keep endpoints contract-first
- support read-only project state first
- no authentication
- no database
- no background orchestration
- no autonomous multi-agent execution

```

## `prompts/04-core-engine-builder.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the core engine builder role.
- Required: `true`

```markdown
# Core Engine Builder Prompt

You are the core engine builder for AI Assembly Line.

Implement deterministic planning logic and spec-compilation helpers.

Priorities:

- decomposition logic
- validation
- normalization
- verification support

Rules:

- outputs must remain traceable to the spec
- deterministic behavior is preferred over clever heuristics with hidden state
- keep implementation boundaries separate from UI and transport layers

```

## `prompts/05-red-team-verifier.md`

- Category: `prompt-source`
- Purpose: Prompt source file for the red-team verifier role.
- Required: `true`

```markdown
# Red Team Verifier Prompt

You are the red team verifier for AI Assembly Line.

Attack the planning outputs for:

- unsafe reinterpretation
- scope creep
- schema drift
- hidden frontend state invention
- unverifiable tasks
- prompt ambiguity

Rules:

- produce concrete failing cases
- tie each failure back to a rule or missing guardrail
- prioritize risks that would make the assembly line unsafe or incoherent

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

## `web/README.md`

- Category: `viewer`
- Purpose: Static viewer documentation and file:// versus local server usage notes.
- Required: `true`

```markdown
# Web Viewer

This directory contains the static multi-page read-only viewer for the generated planning state.

Serve the repo root locally with:

`python -m http.server 8000`

Then open:

`http://localhost:8000/web/`

The viewer pages are:

- `web/index.html`: overview from `generated/project_spec.json`
- `web/repos.html`: repository split and ownership from `generated/repo_plan.json`
- `web/backlog.html`: backlog grouped by `repo_target` from `generated/task_backlog.json`
- `web/prompts.html`: prompt pack from `generated/agent_prompts.json`
- `web/slots.html`: slot board from `generated/slots_db.json`
- `web/verification.html`: verification rules, proof requirements, and raw contract rendering from generated JSON artifacts plus `contracts/*.schema.json` and `contracts/api_contract.openapi.yaml`

If the browser blocks `file://` fetches, open any page directly and use the page-level file picker to load the required `generated/*.json` files for that page.
Generated JSON and contract files are handled differently on the Verification page:

- generated JSON can still be loaded through the local file picker
- contract files are fetched from repository paths and are most reliable when serving the repo root with `python -m http.server 8000`

Shared files:

- `web/viewer-data.js`: generated JSON loading and file-picker fallback
- `web/viewer-layout.js`: shared shell, navigation, status handling, and helpers
- `web/page-*.js`: page-specific rendering only
- `web/viewer.css`: shared styling

The viewer does not add:

- editing
- backend APIs
- authentication
- realtime sync
- frontend-only task, repo, prompt, slot, or contract models

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
  agentPrompts: "../generated/agent_prompts.json",
  slotsDb: "../generated/slots_db.json",
};

export const CONTRACT_FILES = {
  projectSpecSchema: "../contracts/project_spec.schema.json",
  repoPlanSchema: "../contracts/repo_plan.schema.json",
  taskSchema: "../contracts/task.schema.json",
  slotSchema: "../contracts/slot.schema.json",
  agentPromptSchema: "../contracts/agent_prompt.schema.json",
  apiContract: "../contracts/api_contract.openapi.yaml",
};

export const FILE_NAMES = {
  projectSpec: "project_spec.json",
  repoPlan: "repo_plan.json",
  taskBacklog: "task_backlog.json",
  agentPrompts: "agent_prompts.json",
  slotsDb: "slots_db.json",
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
- Purpose: Shared viewer shell, status handling, and reusable rendering helpers.
- Required: `true`

```javascript
import { formatError, isFileProtocol, loadGeneratedState, loadLocalState, sourceFilesForKeys } from "./viewer-data.js";

const NAV_ITEMS = [
  { id: "overview", label: "Overview", href: "index.html" },
  { id: "repos", label: "Repos", href: "repos.html" },
  { id: "backlog", label: "Backlog", href: "backlog.html" },
  { id: "prompts", label: "Prompts", href: "prompts.html" },
  { id: "slots", label: "Slots", href: "slots.html" },
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
          This page renders generated state only. It does not edit or invent task, repo, prompt, slot, or contract structure.
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
  { id: "slotSchema", path: "contracts/slot.schema.json", kind: "json" },
  { id: "agentPromptSchema", path: "contracts/agent_prompt.schema.json", kind: "json" },
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
- Purpose: Shared static viewer styles.
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
.chip.status-complete {
  background: var(--accent-soft);
  color: var(--accent);
}

.chip.status-planned,
.chip.status-review {
  background: #eee7c8;
  color: #6d5a12;
}

.chip.status-blocked {
  background: var(--warn-soft);
  color: var(--warn);
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
    ROOT / "generated" / "agent_prompts.json",
    ROOT / "generated" / "slots_db.json",
    ROOT / "generated" / "review_manifest.json",
    ROOT / "contracts" / "project_spec.schema.json",
    ROOT / "contracts" / "repo_plan.schema.json",
    ROOT / "contracts" / "task.schema.json",
    ROOT / "contracts" / "slot.schema.json",
    ROOT / "contracts" / "agent_prompt.schema.json",
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
        {"risk_tags", "notes"},
    )
    expect_non_empty_string(value["id"], f"{label}.id")
    expect(re.fullmatch(r"[a-z0-9\-]+", value["id"]) is not None, f"{label}.id must match ^[a-z0-9\\-]+$")
    expect_non_empty_string(value["title"], f"{label}.title")
    expect_non_empty_string(value["summary"], f"{label}.summary")
    expect_non_empty_string(value["owner_role"], f"{label}.owner_role")
    expect_non_empty_string(value["repo_target"], f"{label}.repo_target")
    expect_string_array(value["depends_on"], f"{label}.depends_on")
    expect_string_array(value["inputs"], f"{label}.inputs")
    expect_string_array(value["outputs"], f"{label}.outputs")
    expect_string_array(value["acceptance_criteria"], f"{label}.acceptance_criteria", min_items=1)
    expect_string_array(value["verification"], f"{label}.verification", min_items=1)
    if "risk_tags" in value:
        expect_string_array(value["risk_tags"], f"{label}.risk_tags")
    if "notes" in value:
        expect_non_empty_string(value["notes"], f"{label}.notes")


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


def main() -> int:
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

    OUTPUT_PATH.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    print(f"WROTE {OUTPUT_PATH.relative_to(ROOT).as_posix()}")

    for warning in warnings:
        print(warning)

    if missing_required:
        print(f"RESULT FAIL missing_required={len(missing_required)}")
        return 1

    print(f"RESULT OK included={included_count} warnings={len(warnings)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

```
