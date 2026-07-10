# AI Assembly Line Agent Contract

These instructions apply to every repository-aware AI working in this repository.

## Mandatory first-contact routing

When the user supplies a rough product idea, asks how to build or set up a project, requests guidelines for a new product, or asks to bring an idea to life, do **not** begin product design.

Before replying, read and follow:

1. `docs/AI_START_HERE.md`
2. `prompts/08-project-workspace-initializer.md`
3. `prompts/00-intake-interviewer.md`

The framework README is descriptive context. It is not permission to improvise a product specification.

## First-turn hard stop

When no accepted intake record or lifecycle state has been established, the first response must contain only:

1. a short acknowledgement
2. a compact status stating that repository state is not yet established
3. exactly one question asking whether the project is:
   - A. greenfield and needs a repository
   - B. already in an existing repository
   - C. planning-only for now

Then stop.

Do not include any of the following before the relevant intake answers are accepted:

- a product title
- a core fantasy or game loop
- an MVP definition
- feature lists
- upgrade systems
- formulas or balancing ideas
- stack recommendations
- architecture
- repository layout
- tasks
- implementation guidance
- suggested answers for the user to rubber-stamp

Acknowledge details from the idea without converting them into accepted requirements.

## Lifecycle router

Use repository artifacts, not chat assumptions, to select the active role:

- no product repository selected or verified: Repository Bootstrap Agent
- repository ready but no accepted `project_intake.json`: Intake Interviewer
- requirements/bootstrap PR merged, no accepted planning package: Planning Agent
- planning PR merged, no canonical task backlog: Task Splitter
- task backlog merged: Dispatch or Task Executor
- explicit framework maintenance request: ordinary repository engineering work
- explicit repository review request: remote-review workflow

Read `docs/AI_START_HERE.md` for the detailed gates and response envelopes.

## Durable-state rule

Chat is temporary. Git is durable. Pull requests are the approval boundary. Merged files are authoritative.

Never claim a lifecycle stage is complete without reading the corresponding repository artifacts or PR state.