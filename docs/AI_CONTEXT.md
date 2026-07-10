# AI Context Gateway

This repository has two different AI entry modes. Choose the mode before reading deeper files.

## New product idea

When the user supplies a rough idea, asks how to build a new product, requests project guidelines, or asks to bring an idea to life, do **not** use the remote-review file list as a product-design prompt.

Start with:

1. `AGENTS.md`
2. `docs/AI_START_HERE.md`
3. `prompts/08-project-workspace-initializer.md`
4. `prompts/00-intake-interviewer.md`

When repository state is unknown, ask only whether the project is greenfield, already has a product repository, or is planning-only. Stop after that one question. Do not output an MVP, features, stack, architecture, or tasks.

## Explicit repository review

Use the remote-review workflow only when the user asks to inspect, audit, understand, or modify the existing framework repository.

### Source-of-truth rules

- Treat the Git repository as the only source of truth.
- Do not rely on chat history, assistant claims, or out-of-band summaries.
- Read repository files directly.
- Generated JSON files are canonical only for the lifecycle stage that owns them.
- The static viewer is read-only and must not invent task, repository, prompt, slot, contract, or hidden workflow state.

### Remote-review entry order

1. Read `AGENTS.md` and `docs/AI_START_HERE.md` to confirm the user's intent.
2. For review intent, load `generated/review_manifest.json`.
3. Fetch the listed files directly from the repository.
4. Prefer a real clone whenever possible so validators and generated state can be inspected together.

### What to understand first

- `README.md`
- `PROJECT_SPEC.md`
- `PRODUCT_RULES.md`
- `docs/REPOSITORY_FIRST_LIFECYCLE.md`
- `prompts/08-project-workspace-initializer.md`
- `prompts/00-intake-interviewer.md`
- `prompts/00-planning-agent.md`
- `prompts/06-task-splitter.md`

### Viewer boundaries

The viewer may:

- render committed project artifacts directly
- render contract files read-only
- fail visibly when required source-of-truth files are missing or invalid

The viewer must not:

- add backend behavior
- add authentication
- add realtime synchronization
- add editing
- add mutable workflow state
- create frontend-owned task, repository, prompt, slot, or contract models