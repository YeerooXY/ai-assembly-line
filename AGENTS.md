# AI Assembly Line Agent Contract

These instructions apply to every repository-aware AI working in this repository.

## Mandatory first-contact routing

When the user supplies a rough product idea, asks how to build or set up a project, requests guidelines for a new product, or asks to bring an idea to life, do **not** begin product design.

Before replying, read and follow:

1. `docs/AI_START_HERE.md`
2. `docs/CANONICAL_PROJECT_LIFECYCLE.md`
3. `docs/INTAKE_DURABILITY_AND_RESPONSE_DISCIPLINE.md`
4. `prompts/08-project-workspace-initializer.md`
5. `prompts/00-intake-interviewer.md`

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

## Guided-intake response lock

Repository instructions override personality, warmth, enthusiasm, storytelling, and stylistic defaults during guided intake.

After an unambiguous answer, the response may contain only:

1. one concise recorded-answer line
2. compact status only when useful
3. exactly one next question or A/B/C decision card

Then stop.

If the user answers only `A`, `B`, `C`, `recommended`, or another short unambiguous selection, record it and move directly to the next question. Do not explain why the choice is good, restate it in detail, invent a design principle, create planning epics, summarize the project, or preview future questions.

Use A/B/C cards strongly for high-impact decisions. Include concise pros, cons, MVP risk, later scaling/refactor risk when relevant, and one recommendation that may be a hybrid.

## Per-decision durability

Once a writable product repository branch exists, persist every accepted intake answer before asking the next question. Update:

- `assembly/intake/intake_session.json`
- `assembly/intake/LIVE_DECISIONS.md`

Then make a focused commit and verify the write succeeded.

Do not batch ten decisions merely to reduce commits. Fine-grained commits are intentional recovery points.

If writes are unavailable, explicitly mark persistence as blocked and track unsaved decisions. Never imply chat-only state is durable.

## Canonical gated lifecycle

Follow `docs/CANONICAL_PROJECT_LIFECYCLE.md` exactly:

```text
Idea
  -> guided intake with per-decision commits
  -> requirements/bootstrap PR
  -> planning and architecture PR
  -> task-splitting PR
  -> dependency audit
  -> canonical backlog
  -> development waves
```

Do not blur stages or place later-stage artifacts in an earlier PR.

- Planning starts only after the requirements PR is merged.
- Task splitting starts only after the planning PR is merged.
- Development starts only after the dependency audit passes and the canonical backlog is merged.
- Every dependency must use an exact task ID before the backlog becomes canonical.

## Resume contract

A fresh agent must recover state from repository artifacts, not remembered chat.

Read, when present:

1. `project_workspace.json`
2. `assembly/context/handoff.md`
3. `assembly/intake/LIVE_DECISIONS.md`
4. `assembly/intake/intake_session.json`
5. `assembly/intake/project_intake.json`
6. `assembly/requirements/REQUIREMENTS.md`
7. planning artifacts
8. canonical backlog and collaboration state
9. relevant PR state

If chat loss is suspected, stop new intake, inspect durable state, mark reconstructed material as unverified, and re-confirm it one decision at a time.

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

Never claim a lifecycle stage is complete without reading the corresponding repository artifacts, validation output, dependency audit, and PR state.
