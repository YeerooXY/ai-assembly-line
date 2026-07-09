# Project Intake Workflow

Project intake is the first user-facing step of AI Assembly Line.

Its purpose is to turn a rough idea into an interactive intake session and then into a structured intake record before the Planning Agent creates project specs, repo splits, task backlogs, role prompts, and verification rules.

The intake flow is intentionally interactive. It should ask only the questions that materially change the plan, suggest sensible defaults when possible, and stop asking once enough information exists to create a useful first planning run.

## Position in the assembly line

```text
rough idea
  -> guided intake interview
  -> intake_session.json
  -> project_intake.json
  -> planning run
  -> project_spec.json
  -> repo_plan.json
  -> task_backlog.json
  -> agent_prompts.json
  -> slots_db.json
  -> human review
```

The intake session is the interactive state while questions are still being asked.

The intake record is not an implementation plan. It is the structured input that keeps the implementation plan grounded.

## First response rule

When a user starts a project with only a rough idea, the first response must begin intake.

The Intake Interviewer must not immediately output:

- a full guideline document
- a full architecture
- a final stack decision
- a full MVP scope
- a task backlog
- agent assignments
- implementation code

Instead, it should output:

1. a short acknowledgement
2. an `intake_session` update following `contracts/intake_session.schema.json`
3. the next high-impact questions

This is true even if the user asks for guidelines or says they want to bring the idea to life. Those requests still start intake unless a complete intake record already exists.

See `docs/INTAKE_SESSION_FORMAT.md`.

## Recommended target-project layout

For real projects, the steering and generated planning artifacts should live inside the target project repository, not only in this template repository.

Recommended layout:

```text
my-project/
  src/
  tests/
  README.md
  .ai-assembly/
    steering/
      PRODUCT_RULES.md
      PROJECT_SPEC_TEMPLATE.md
      prompts/
      contracts/
    intake/
      intake_session.json
      project_intake.json
    planning_runs/
      <run-slug>/
        input-idea.md
        planning-run.md
        outputs/
        review-notes.md
    generated/
      project_spec.json
      repo_plan.json
      task_backlog.json
      agent_prompts.json
      slots_db.json
      planning_runs_index.json
```

The `ai-assembly-line` repository is the upstream template and steering kit. The target project repository should contain the snapshot that agents and humans actually use.

## Intake modes

### Quick mode

Use when the user wants a fast first draft.

Rules:

- Ask at most five high-impact questions.
- Make low-risk assumptions explicitly.
- Mark risky unknowns as open questions.
- Produce a draft intake record quickly.

### Guided mode

Use as the default.

Rules:

- Ask questions in small sections.
- Suggest reasonable stack options when the user has not chosen one.
- Confirm the MVP before planning.
- Confirm team/agent working style before task decomposition.
- Produce a structured intake record after enough information is known.

### Expert mode

Use when the user already has strong constraints.

Rules:

- Let the user paste stack choices, tool paths, repo constraints, architecture notes, and team layout.
- Ask only for missing high-risk decisions.
- Produce the intake record with minimal back-and-forth.

## Question sections

The Intake Interviewer should cover these sections, but not necessarily all in one message.

### 1. Goal

- What are you trying to build?
- Who is it for?
- What problem does it solve or what experience should it create?

### 2. MVP

- What is the smallest useful version?
- What can be postponed?
- What would make the first version successful?

### 3. Platform and stack

- Is there a preferred stack?
- Should the AI suggest a stack?
- What platforms matter first: desktop, web, mobile, server, embedded, CLI?
- Are there existing tools, local paths, SDKs, credentials, or hardware constraints?

When suggesting a stack, provide options with tradeoffs and a recommendation. Do not force a stack silently.

### 4. Existing project state

- Is this greenfield or an existing repository?
- Where is the project path?
- Are there existing source files, tests, docs, or architecture decisions?

### 5. Team and agent layout

- Will one person work alone?
- Will multiple humans work in parallel?
- Will multiple AI agents work in parallel?
- Should tasks be split by frontend/backend/core/test/docs or by feature slices?

### 6. Working style

- Does the user prefer very small tasks or larger milestones?
- Should tasks be optimized for beginner contributors, expert contributors, AI agents, or mixed teams?
- What proof is required for a task to count as done?

### 7. Safety and boundaries

- Are there external services, accounts, credentials, games, scraping, automation, or platform terms involved?
- Which actions are explicitly out of scope?
- What must never be automated?

## Ask/assume/stop rule

The intake should not ask questions forever.

Ask when the answer changes architecture, stack, MVP, safety, or parallelization.

Assume when the missing detail is low-risk and easy to revise later.

Stop and ask when the missing detail is high-risk, such as:

- real-time multiplayer versus turn-based multiplayer
- browser-first versus desktop-first
- existing repository versus greenfield
- required engine/framework
- external accounts, credentials, scraping, or automation
- team size and parallel work expectations
- hardware, SDK, or local tool constraints

## Intake session output

While questions are still open, the intake interview should produce `intake_session.json`-shaped updates conforming to `contracts/intake_session.schema.json`.

The session should include:

- current section
- completed and incomplete sections
- questions already asked
- answers received so far
- stack options when suggested
- assumptions
- open questions
- readiness to generate `project_intake.json`
- next action

## Required intake output

Only when the session is ready should the intake interview produce `project_intake.json` conforming to `contracts/project_intake.schema.json`.

The record should include:

- project goal
- MVP
- target users
- platform targets
- stack preference or stack recommendation
- existing tools and paths
- existing repository state
- team/agent mode
- working style
- constraints
- assumptions
- open questions
- safety boundaries
- acceptance signals

## Hand-off to Planning Agent

After the intake record is complete enough, the Planning Agent should use it to create:

- `project_spec.json`
- `repo_plan.json`
- `task_backlog.json`
- `agent_prompts.json`
- `slots_db.json`

The Planning Agent must preserve all high-risk unknowns as open questions or verification tasks instead of pretending they are solved.
