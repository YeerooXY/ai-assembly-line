# AI Assembly Line Agent Contract

These instructions apply to every repository-aware AI working in this repository.

## Mandatory first-contact routing

When the user supplies a rough product idea, asks how to build or set up a project, requests guidelines for a new product, or asks to bring an idea to life, do **not** begin product design.

Before replying, read and follow:

1. `docs/AI_START_HERE.md`
2. `docs/CANONICAL_PROJECT_LIFECYCLE.md`
3. `docs/PRODUCT_DISCOVERY_ORDER.md`
4. `docs/INTAKE_DURABILITY_AND_RESPONSE_DISCIPLINE.md`
5. `docs/CONTEXT_HANDOFF_AND_RESUME.md`
6. `prompts/08-project-workspace-initializer.md`
7. `prompts/00-intake-interviewer.md`

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

## Weighted Product Discovery

Internally this lifecycle stage remains `intake`; present it to users as **Product Discovery**.

Follow the decision order in `docs/PRODUCT_DISCOVERY_ORDER.md`:

```text
product identity
  -> target users
  -> core experience or workflow
  -> largest scope-cutting decisions
  -> MVP boundary
  -> required product systems
  -> stack and architecture constraints
```

At each turn, ask the unresolved question with the highest expected impact on scope, architecture, cost, safety, platform support, or later refactor risk.

Do not ask low-level mechanics or UX questions while unresolved high-level decisions such as target users, offline/online, single-user/multi-user, multiplayer, target platform, or product maturity could invalidate them.

Resolve connectivity and participation separately when relevant:

- connectivity: offline / online / hybrid
- participation: solo or single-user / local multi-user / asynchronous multi-user / real-time multiplayer or collaboration

Technology follows accepted product needs. Do not select a stack first unless the user has a genuine non-negotiable technical constraint.

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

## Product DNA

When Product Discovery is ready for final review, create:

```text
assembly/intake/PROJECT_DNA.md
```

Use `docs/templates/PROJECT_DNA.md` as the shape. It is a concise north-star summary derived only from accepted decisions. It does not replace `project_intake.json` or `REQUIREMENTS.md`.

## Always-ready context handoff

Every active product repository must continuously maintain:

- `assembly/context/CURRENT_HANDOFF.json`
- `assembly/context/NEW_CHAT_RESUME.md`

Update and commit them whenever the active decision, next action, lifecycle phase, role, branch, pull request, blocker, persistence status, or implementation task changes.

Before ending a work turn or asking the user the next guided question, handoff persistence should normally be `ready` with zero unsaved decisions.

A fresh agent must read `CURRENT_HANDOFF.json`, verify branch and commit state, read every authoritative artifact listed there, load the complete active-role prompt, and continue from the exact `next_action`.

Do not ask the user to reconstruct what the previous agent knew. Do not infer missing state from personality or chat memory.

Validate locally with:

```text
python assembly/tools/validate_context_handoff.py --root .
```

Expected marker:

```text
RESULT OK context_handoff_ready=true unsaved_decisions=0
```

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
2. `assembly/context/CURRENT_HANDOFF.json`
3. `assembly/context/NEW_CHAT_RESUME.md`
4. every authoritative artifact listed in the handoff
5. `assembly/context/handoff.md`
6. `assembly/intake/LIVE_DECISIONS.md`
7. `assembly/intake/intake_session.json`
8. `assembly/intake/PROJECT_DNA.md`
9. `assembly/intake/project_intake.json`
10. `assembly/requirements/REQUIREMENTS.md`
11. planning artifacts
12. canonical backlog and collaboration state
13. relevant PR state

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

Never claim a lifecycle stage is complete without reading the corresponding repository artifacts, validation output, dependency audit, handoff state, and PR state.

## Repository-tool safety

Before repository-connected work, read and follow
`docs/WEB_AGENT_GITHUB_SAFETY.md`.

In particular:

- use local Git only after a checkout and required tools are verified;
- use direct connector reads for known branches and paths;
- compare the stage branch with the current default branch before every write;
- treat a merged branch as permanently closed and continue from a fresh branch;
- pretty-print generated JSON and commit related state files atomically;
- call artifacts validated only after the documented validator actually runs.
