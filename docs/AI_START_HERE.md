# AI Start Here

This file is the mandatory intent and lifecycle router for AI systems entering `ai-assembly-line`.

Do not treat the repository README as a request to brainstorm the user's product. First decide which framework role is active.

## Intent routing

### The user supplied a rough product idea

Activate the Repository Bootstrap Agent and Intake Interviewer:

- `prompts/08-project-workspace-initializer.md`
- `prompts/00-intake-interviewer.md`

Do not activate the Planning Agent, Task Splitter, or implementation roles yet.

### The user asks to review or modify the framework itself

Treat it as normal repository engineering work. Inspect the requested framework files and make a focused branch/PR.

### The user asks to review an existing repository state

Use `docs/AI_CONTEXT.md` and the curated review manifest. Do not confuse a review request with a new-project intake request.

## Startup lock for rough ideas

A rough idea is not an accepted MVP, specification, architecture, or task backlog.

When repository state is unknown, the first user-facing response must be limited to:

```text
<short acknowledgement>

Intake status: started
Product idea: <brief neutral description, without expanding it>
Repository state: not established

Which situation applies?

A. Greenfield — this project needs a new product repository
B. Existing repository — a product repository already exists
C. Planning-only — continue intake without creating a repository yet
```

Then stop.

Do not add a working title, game loop, MVP, feature list, formulas, stack recommendation, architecture, repository layout, or tasks. Do not show future questions.

The user may answer `A`, `B`, `C`, or give a custom repository-state answer.

## Why this lock exists

The first repository decision changes where durable state belongs and whether normal branch/PR workflows are possible. Product design generated before that decision is unreviewed speculation and must not be presented as accepted project state.

## Lifecycle gates

### Gate 0 — Repository state unknown

Required next action: ask the A/B/C repository-state question and stop.

### Gate 1 — Repository selected but not ready

Verify:

- repository exists and is accessible
- at least one commit exists
- default branch exists
- branch creation is possible
- pull requests are possible

Ask or act on only the next blocking repository-readiness item. Do not begin detailed intake output or product planning.

### Gate 1.5 — Product repository entrypoints installed

After `tools/bootstrap_product_repository.py` succeeds, install repository-level AI routing into the product repository before continuing intake:

```text
tools/install_product_agent_entrypoints.py
```

The local command handoff must run both installation and `--check` verification in the same resolved shell-specific block. It must create:

```text
AGENTS.md
.github/copilot-instructions.md
assembly/docs/AI_START_HERE.md
```

Expected success markers are:

```text
RESULT OK product_agent_entrypoints_installed=true
RESULT OK product_agent_entrypoints_ready=true
```

With GitHub write access, create the equivalent files directly on the bootstrap branch instead of asking the user to run the local tool.

This gate makes the questionnaire and lifecycle routing survive when a fresh AI tab later opens the product repository.

### Gate 2 — Repository ready, intake incomplete

Activate `prompts/00-intake-interviewer.md` in guided mode.

Each response must contain only:

1. a short record of the answer just accepted
2. compact intake status
3. exactly one next high-impact question or decision card

Then stop.

Do not infer the remaining MVP from the idea. Do not silently accept agent recommendations.

### Gate 3 — Intake ready

Only after blocking questions are answered:

- create schema-valid `project_intake.json`
- render matching `REQUIREMENTS.md`
- update the handoff
- open the requirements/bootstrap PR

Do not create `project_spec.json`, `repo_plan.json`, task batches, or implementation code.

### Gate 4 — Requirements PR merged

Activate `prompts/00-planning-agent.md` from merged repository files.

### Gate 5 — Planning PR merged

Activate `prompts/06-task-splitter.md` from merged planning artifacts.

### Gate 6 — Task backlog merged

Use Dispatch and one-task execution workflows.

## Transition rule

When one role hands off to another, explicitly reload the next role's prompt from the repository. A sentence such as “continue using the Intake Interviewer rules” is not enough unless the full prompt is read and its response envelope is followed.

## Regression examples

### Incorrect first response

- invents a project name
- describes the gameplay loop
- proposes upgrades and monetization
- recommends a stack
- then asks about the repository at the end

### Correct first response

- acknowledges the idea briefly
- states that repository state is not established
- asks A/B/C for greenfield, existing repository, or planning-only
- stops immediately

### Incorrect guided-intake response

- answers the current choice
- fills in the rest of the MVP automatically
- outputs complete requirements

### Correct guided-intake response

- records the user's answer
- asks exactly one next high-impact question
- stops
