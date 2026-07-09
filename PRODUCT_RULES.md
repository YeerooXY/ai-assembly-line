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
