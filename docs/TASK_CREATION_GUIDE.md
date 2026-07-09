# Task Creation Guide

This guide defines how to create implementation-ready tasks for any project planned through AI Assembly Line.

Use the accepted intake, project spec, repo plan, and task schema as the source of truth. Project-specific examples may use concrete repo names and prefixes, but the canonical task format must stay reusable.

## Core Rule

Every task must answer:

```text
What repo or area owns this?
What role owns this?
What exactly changes?
What does it depend on?
What downstream work does it unblock?
How do we prove it works?
What edge cases and non-goals must not drift?
```

If a task cannot answer those questions, it is not ready.

## Task Size

A task should usually fit in one focused work session.

Use:

- `S`: small, usually 30-90 minutes
- `M`: medium, usually 2-4 hours
- `L`: too large for direct execution; split before assignment

Milestones are not tasks. Phrases like `build the backend`, `create the client`, or `implement multiplayer` should be decomposed into smaller work packets.

## Task Hierarchy

Use this hierarchy:

```text
Milestone
  -> feature group or lane
    -> task
      -> verification evidence
```

Prefer shared contract/interface tasks before implementation tasks when multiple people or AI agents will work in parallel.

## Task IDs

Use stable IDs. Two good styles are:

- Project-agnostic lowercase IDs, such as `define-room-event-contract`
- Project-specific prefix IDs, such as `CONTRACT-001` or `UI-003`

Dependencies and blocked-work references must use task IDs, not task titles.

## Canonical Fields

Tasks in `task_backlog.json` must conform to `contracts/task.schema.json`.

Required fields:

```yaml
id:
title:
summary:
owner_role:
repo_target:
depends_on:
inputs:
outputs:
acceptance_criteria:
verification:
```

Recommended optional fields:

```yaml
status:
priority:
milestone:
lane:
allowed_areas:
blocks:
objective:
context:
implementation_notes:
proof_required:
edge_cases:
non_goals:
estimated_size:
risk_tags:
handoff_notes:
notes:
```

Do not use `repo` in canonical task JSON. Use `repo_target`, because it should match a repo or ownership target from `repo_plan.json`.

## Field Guidance

`status` should be one of:

```text
draft
ready
in_progress
blocked
review
done
rejected
```

`priority` should be one of:

```text
P0: blocks many other tasks
P1: needed for MVP
P2: useful but not blocking
P3: later or nice-to-have
```

`blocks` should list task IDs or stable work IDs that depend on this task.

`objective` should state the purpose in one short paragraph.

`context` should capture decisions or constraints the task must preserve.

`implementation_notes` may guide execution, but should not become a full implementation script.

`proof_required` should list evidence expected from the executor, such as test output, build output, logs, screenshots, fixtures, or manual test notes.

`edge_cases` should list behavior that must be tested or explicitly documented.

`non_goals` should list scope the task must not expand into.

`estimated_size` should be `S`, `M`, or `L`. A task marked `L` should normally be split before execution.

## Standard Template

```yaml
id:
title:
summary:
owner_role:
repo_target:
status: draft
priority:
milestone:
lane:
allowed_areas: []
depends_on: []
blocks: []

objective: >
  Describe the task in one short paragraph.

context: >
  Include the project decisions this task must respect.

inputs:
  - 

outputs:
  - 

implementation_notes:
  - 

acceptance_criteria:
  - Code builds or the non-code artifact is complete.
  - Required files, contracts, or docs exist.
  - Relevant tests or checks pass where practical.

verification:
  - Reviewer can validate the outputs against the acceptance criteria.

proof_required:
  - Build, test, validation, log, screenshot, fixture, or manual test evidence.
  - Short change summary.

edge_cases:
  - 

non_goals:
  - 

estimated_size:
```

## Dependency Rules

Create shared contracts before consumers.

Do not create implementation tasks that require undefined APIs, event contracts, schemas, package boundaries, or file ownership rules.

A task should normally belong to one `repo_target`. If it touches multiple repos, mark it as integration or QA work and make the cross-repo proof explicit.

## Large Plan Batch Workflow

For large generated plans, do not ask a web AI to return the whole backlog in one response.

Use a two-step batch workflow:

1. Generate a compact `task_batch_index` grouped by `owner_role`, `repo_target`, or `lane`.
2. Generate one selected batch at a time as a `contracts/task_batch.schema.json` object.

This keeps outputs copy-pastable and reduces the chance of truncation.

Each task batch must conform to `contracts/task_batch.schema.json`.

Each task inside the batch must still conform to `contracts/task.schema.json`.

The future frontend should support:

- copy prompt for batch index
- paste returned batch index
- choose one batch
- copy prompt for that selected batch
- paste returned task JSON
- validate task graph dependencies and topological batch order
- merge accepted batches into `generated/task_backlog.json`

## Review Checklist

Before marking a task `ready`, check:

- The repo or ownership target is clear.
- The owner role is clear.
- The objective is narrow.
- Dependencies and blocked work are listed.
- Acceptance criteria are pass/fail.
- Proof requirements are specific.
- Edge cases and non-goals are explicit.
- Another person or AI agent can verify the task without guessing intent.
