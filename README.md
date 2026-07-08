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
- `contracts/`: schemas and OpenAPI contract
- `generated/`: canonical machine-readable planning artifacts for the current seed state
- `examples/coc-base-builder/`: example decomposition for a safe base layout planner
- `prompts/`: copy-paste role prompts
- `tools/validate_seed.py`: repository JSON validation utility
- `web/static-docs-or-dashboard-placeholder/`: placeholder for the first read-only UI

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
