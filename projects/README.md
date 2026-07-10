# Project Workspaces

The recommended workflow for a real product is repository-first.

## Recommended: product repository owns the project

```text
product-repository/
  project_workspace.json
  README.md
  src/
  tests/

  assembly/
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

The product repository owns its accepted requirements, planning artifacts, task decomposition, execution state, implementation, and proof.

The normal lifecycle is:

```text
create/select repository
  -> requirements PR
  -> planning PR
  -> task-split PR
  -> Dispatch
  -> implementation PRs
```

Merged repository files are the handoff between web-AI tabs and agents. Users should not be asked to copy JSON into arbitrary folders.

See `docs/REPOSITORY_FIRST_LIFECYCLE.md`.

## What `ai-assembly-line` owns

This repository remains the reusable factory:

- prompts and workflow contracts
- schemas
- viewer source
- validation tools
- project-kit templates
- future export/sync tooling

It should not gain a new real-project folder every time somebody starts a product.

## Optional: central registry mode

`projects/` and `projects/index.json` remain supported for:

- framework development and tests
- seed/demo workspaces
- monorepos
- local multi-project dashboards
- deliberately centralized planning-only work

A central workspace may still look like:

```text
projects/<project-id>/
  project_workspace.json
  intake/
  requirements/
  planning_runs/
  generated/
  context/
  prompts/
  repos/
```

Use `tools/init_project_workspace.py` only when central registry mode is actually desired.

## Core rule

```text
humans describe intent
AI creates reviewable repository changes
validators verify artifacts
pull requests approve durable state
the static UI reads merged state
Dispatch launches one task at a time
```
