# Task Generation Workflow

Task generation starts only after intake is complete enough for planning.

The Planning Agent turns an accepted `project_intake.json` into planning artifacts, including a parallel-safe `task_backlog.json`.

## Workflow position

```text
rough idea
  -> intake_session.json
  -> project_intake.json
  -> planning run
  -> project_spec.json
  -> repo_plan.json
  -> task_backlog.json
  -> agent_prompts.json
  -> slots_db.json
```

Do not generate implementation tasks before the intake record is ready. Open high-risk decisions must remain open questions or blocking tasks instead of being silently assumed.

## Inputs

Task generation should read:

- accepted `project_intake.json`, when available
- `PROJECT_SPEC.md` / `PROJECT_SPEC_TEMPLATE.md`
- `PRODUCT_RULES.md`
- `docs/PLANNING_RUN_WORKFLOW.md`
- `docs/TASK_CREATION_GUIDE.md`
- `docs/TASK_CARD_FORMAT.md`
- existing contracts under `contracts/`
- generated repo plan, if already drafted
- any existing planning-run notes

## Outputs

A complete planning run should produce or update:

- `project_spec.json`
- `repo_plan.json`
- `task_backlog.json`
- `agent_prompts.json`
- `slots_db.json`

The task backlog must be traceable to the project spec and repo plan.

For large plans, generate task output in batches rather than one large `task_backlog.json` response. The preferred web AI flow is guided: paste `prompts/06-task-splitter.md` with `MODE: guided`, save the first response as `generated/task_batch_index.json`, then reply `continue` until each `generated/task_batches/<batch_id>.json` file has been emitted.

## Generation phases

### 1. Freeze the accepted intake

Before generating tasks, summarize the accepted decisions:

- goal
- MVP boundary
- platform target
- stack / engine direction
- project state: greenfield or existing repo
- team/agent working style
- safety boundaries
- proof required for done
- open questions

If any high-risk answer is still missing, do not pretend it is solved. Either ask intake to continue or create an explicit blocking task.

### 2. Define shared contracts first

For parallel work, generate contract/spec tasks before implementation tasks.

Examples:

- game rules spec
- API contract
- WebSocket event contract
- data model sketch
- file ownership map
- test scenario matrix

This prevents client and backend workers from inventing incompatible assumptions.

### 3. Split work into lanes

Use lanes that let people or agents work in parallel with minimal file overlap.

Common lanes:

- `shared-contract`
- `client-ui`
- `backend-game-state`
- `core-domain`
- `tests-verification`
- `docs-devex`

For a two-worker project, a good default is:

```text
Worker A: client/UI tasks
Worker B: backend/core-state tasks
Shared first: contracts, interfaces, test scenarios
```

Do not split only by technology if the MVP needs vertical slices. Prefer a small number of contract-first tasks, followed by parallel implementation slices.

### 4. Make dependencies explicit

Every task should list its prerequisites by task ID.

Good dependency graph:

```text
T-001 Define realtime event contract
T-002 Implement backend room creation     depends on T-001
T-003 Implement client room join screen   depends on T-001
T-004 Verify join-room flow               depends on T-002, T-003
```

Bad dependency graph:

```text
T-001 Build backend
T-002 Build frontend
T-003 Test everything
```

### 5. Add acceptance criteria and verification

Every task needs observable acceptance criteria and proof of done.

Examples:

- command output
- passing tests
- manual flow checklist
- screenshot or recorded demo
- contract reference
- schema validation
- no forbidden files touched

A task without verification is not ready for assignment.

### 6. Preserve scope boundaries

The backlog must separate:

- MVP tasks
- post-MVP tasks
- blocked tasks
- research/spike tasks
- explicit non-goals

Do not let future scaling concerns explode the first backlog. Add future-proofing only when it prevents obvious near-term rework.

## Parallel-safe task rules

For each task, ask:

1. Can one owner complete this without waiting for another unfinished implementation task?
2. Are dependencies explicit?
3. Are file/repo boundaries clear?
4. Can the reviewer verify completion?
5. Does it avoid silently deciding unresolved intake questions?

If the answer is no, split or rewrite the task.

## MVP-first rule

The first backlog should make the smallest playable or useful version real.

For games and realtime apps, prefer this order:

1. shared rules/events contract
2. minimal backend state loop
3. minimal client UI loop
4. one end-to-end playable flow
5. verification and regression tests
6. polish and future features

Avoid starting with account systems, matchmaking, skins, analytics, scaling infrastructure, or deployment complexity unless the intake record explicitly requires them for MVP.

## Blocking tasks

If planning cannot proceed without a decision, create a blocking task instead of guessing.

Example:

```text
T-BLOCK-001 Decide deployment target
Reason: Hosting choice changes backend runtime, environment config, and verification steps.
Required answer: local-only, LAN, cloud staging, or production hosting.
```

Blocking tasks should be few. If there are many, intake is not ready.

## Done state

A generated task backlog is ready when:

- every task has a stable ID
- every task has a lane/owner target
- dependencies reference valid task IDs
- MVP tasks are separated from post-MVP tasks
- shared contract tasks come before parallel implementation work
- every task has acceptance criteria
- every task has verification steps
- open questions are explicit
- no task requires forbidden scope

For batched generation, the backlog is ready only after every accepted batch validates individually, task IDs/dependencies form an acyclic graph, and batch order is topological.
