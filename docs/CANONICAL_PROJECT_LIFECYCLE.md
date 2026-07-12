# Canonical Project Lifecycle

This is the required repository-first lifecycle for real products using AI Assembly Line.

It is based on the proven Destructro Truck flow and hardened against lost chat context.

```text
Idea
  -> repository bootstrap
  -> guided intake with per-decision commits
  -> requirements/bootstrap PR
  -> planning and architecture PR
  -> task-splitting PR
  -> dependency audit
  -> canonical backlog
  -> development waves
```

Chat may disappear at any time. Every stage must be recoverable from repository artifacts alone.

## Stage 0 — Idea and repository bootstrap

Goal: establish the durable home for the product before detailed design begins.

Required outcomes:

- product repository selected or created;
- initial commit and default branch exist;
- bootstrap/intake branch exists;
- AI Assembly Line kit and repository entrypoints are installed;
- `project_workspace.json` identifies the repository and lifecycle paths.

Do not begin architecture, task generation, or implementation during this stage.

## Stage 1 — Guided intake

Goal: turn the rough idea into accepted product constraints and an explicit MVP boundary.

The interviewer asks one high-impact question per turn. Strong A/B/C decision cards are preferred for choices that affect scope, architecture, platform, multiplayer, safety, proof, or future refactor risk.

### Durable live artifacts

Maintain:

```text
assembly/intake/intake_session.json
assembly/intake/LIVE_DECISIONS.md
```

Every accepted answer must be written and committed before the next question is asked.

`LIVE_DECISIONS.md` is a human-readable recovery log. Each entry should contain:

```text
Decision ID
Topic
Accepted choice
Material constraints or rationale supplied by the user
Status: accepted / revised / superseded
Commit reference when practical
```

Draft intake commits are recovery state, not final approval.

### Intake must cover, when relevant

- product goal and target users;
- MVP must-haves;
- explicit postponed scope and non-goals;
- target platforms;
- gameplay or product modes;
- progression and persistence;
- offline/online boundaries;
- multiplayer scope;
- external services and accounts;
- accessibility and release expectations;
- stack constraints or selection;
- team and AI-agent parallelization;
- review and proof requirements;
- safety and licensing boundaries;
- acceptance signals.

### Intake completion gate

Do not open the requirements PR while blocking questions remain.

The stage is complete only when:

- `project_intake.json` is schema-valid;
- `REQUIREMENTS.md` matches it;
- MVP and postponed scope are explicit;
- assumptions and non-blocking open questions are recorded;
- handoff identifies the exact next role;
- the requirements/bootstrap PR is reviewed and merged.

## Stage 2 — Requirements

Goal: create the authoritative statement of what the product must be, without deciding implementation tasks.

Canonical artifacts:

```text
assembly/intake/project_intake.json
assembly/requirements/REQUIREMENTS.md
assembly/context/handoff.md
```

Requirements should state observable behavior and boundaries, including offline/online behavior, saves, progression, accessibility, release expectations, proof, and non-goals where relevant.

Do not create architecture or a task backlog in the requirements PR.

## Stage 3 — Planning and architecture

Goal: decide how accepted requirements will be implemented before tasks are created.

The Planning Agent must start from merged requirements, not chat memory.

Planning should define:

- repository and module structure;
- shared schemas and contracts;
- subsystem ownership boundaries;
- agent or workstream roles;
- dependency waves;
- concurrency and file-ownership rules;
- integration strategy;
- verification and Red Team strategy;
- major milestones and release gates;
- technical risks and prototypes needed to resolve them.

Canonical planning artifacts include:

```text
assembly/generated/project_spec.json
assembly/generated/repo_plan.json
assembly/generated/agent_prompts.json
assembly/generated/slots_db.json
assembly/planning_runs/<run-id>/
```

### Planning completion gate

The stage is complete only when:

- requirements are traceable into the architecture;
- roles and ownership boundaries are explicit;
- shared contracts are identified before parallel work;
- integration and adversarial review responsibilities exist;
- dependency waves are plausible;
- planning artifacts validate;
- the planning PR is reviewed and merged.

Do not generate the canonical task backlog in the planning PR.

## Stage 4 — Task splitting

Goal: convert each accepted role and architecture lane into small, reviewable, dependency-safe tasks.

Tasks should use stable numbered IDs such as:

```text
1.1
1.2
2.1
2.2
```

Each task must define:

- owner role or slot;
- objective;
- in-scope and out-of-scope work;
- exact dependencies by task ID;
- files or contracts owned;
- acceptance criteria;
- proof required;
- integration notes;
- risks or blockers.

Major milestones should have explicit boss tasks that prove a complete subsystem or release gate, rather than merely completing one implementation fragment.

Examples include:

- complete fixed MVP content;
- complete deterministic offline state loop;
- complete player-facing flow;
- online and release proof;
- final MVP release acceptance;
- final adversarial review.

## Stage 5 — Dependency audit

Goal: prove the generated plan is executable before development starts.

Replace every vague dependency phrase with exact task IDs.

Audit must report:

- total task count;
- zero missing task references;
- zero duplicate IDs;
- zero circular dependencies;
- topological wave count;
- dependency-ready first tasks;
- any deliberate cross-role integration chains;
- boss-task reachability from their prerequisites.

If a cycle exists, revise task ownership or sequencing. Never waive a cycle because the tasks are conceptually related.

## Stage 6 — Canonical backlog

Canonical machine-readable artifacts:

```text
assembly/generated/task_batch_index.json
assembly/generated/task_batches/*.json
assembly/generated/task_backlog.json
assembly/generated/collaboration_state.json
```

Detailed human-readable task files may exist per agent or role, but the machine-readable backlog is authoritative for Dispatch.

### Task-splitting completion gate

The stage is complete only when:

- every accepted planning role is fully split;
- every dependency uses an exact valid ID;
- the dependency audit passes;
- canonical artifacts validate;
- first dependency-ready tasks are identified;
- the Task Splitter PR is reviewed and merged.

## Stage 7 — Development waves

Development begins only after the canonical backlog is merged.

Dispatch selects tasks whose dependencies are complete. Each Task Executor receives one task and the minimum required repository context.

Implementation PRs must include the proof required by their task. Integration and Red Team work proceed as first-class lanes, not as cleanup after feature work.

## Resume contract

A fresh agent or chat must not rely on remembered conversation.

Read, in order when they exist:

1. repository `AGENTS.md`;
2. `project_workspace.json`;
3. `assembly/context/handoff.md`;
4. `assembly/intake/LIVE_DECISIONS.md` while intake is active;
5. `assembly/intake/intake_session.json` while intake is active;
6. `assembly/intake/project_intake.json`;
7. `assembly/requirements/REQUIREMENTS.md`;
8. planning-run artifacts and generated planning package;
9. canonical task backlog and collaboration state;
10. relevant PR state.

Choose the active role from committed and merged state, then read the complete role prompt.

## Recovery rules

If chat context disappears:

- stop generating new decisions;
- inspect the active branch and durable intake artifacts;
- compare any surviving transcript with `LIVE_DECISIONS.md`;
- mark reconstructed material as unverified;
- ask the user to re-verify reconstructed decisions one by one;
- commit each verified correction immediately.

Never present inferred or reconstructed choices as already accepted.

## Proven reference

`YeerooXY/destructro-truck` is the reference implementation of the intended lifecycle:

- requirements were completed and merged before architecture;
- architecture established eight explicit roles and ownership boundaries;
- roles were split into numbered tasks with exact dependencies;
- the full graph was audited before development;
- canonical backlog artifacts were merged before Dispatch began.
