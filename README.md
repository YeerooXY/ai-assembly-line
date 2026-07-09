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

## Validation

Run:

```powershell
python tools/validate_seed.py
```

The validator:

- parses every JSON file in the repository
- reports each valid JSON file
- reports parse failures clearly
- schema-validates the canonical generated artifacts when `jsonschema` is available

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
