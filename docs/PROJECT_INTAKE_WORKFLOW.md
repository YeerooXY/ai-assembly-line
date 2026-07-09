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

The intake session is the internal interactive state while questions are still being asked.

The intake record is not an implementation plan. It is the structured input that keeps the implementation plan grounded.

## First response rule

When a user starts a project with only a rough idea, the first response must begin intake.

The Intake Interviewer must not immediately output:

- a full guideline document
- temporary or starter project guidelines
- technical steering rules
- target repository layout
- repo/package split
- definition of done
- suggested answers or default answers for the user to accept
- a full architecture
- a final stack decision
- a full MVP scope
- a task backlog
- agent assignments
- implementation code

Instead, it should output:

1. a short acknowledgement
2. a compact human-readable intake status summary
3. the next high-impact question, preferably as a decision card when the choice affects MVP difficulty or later scaling/refactor risk

This is true even if the user asks for guidelines or says they want to bring the idea to life. Those requests still start intake unless a complete intake record already exists.

If `readiness.can_generate_intake` is `false`, the first response must stop after the single next question in guided mode. It must not continue with project guidelines, technical steering, repository layout, default answers, stack choices, definition-of-done rules, or a checklist of future questions.

Do not print raw `intake_session` JSON by default. Keep it internally and show JSON only when the user asks for it, the session becomes ready for `project_intake.json`, state review is needed, or saving/exporting/persisting is requested.

See `docs/INTAKE_SESSION_FORMAT.md` and `docs/INTAKE_DECISION_CARDS.md`.

## Guidelines wording trap

A user may say something like:

```text
Here is the ai-assembly-line repo that helps with planning. I want to build a multiplayer Tron game. Can you help me set guidelines for the project based on the repo's steering help?
```

That is still a request to start intake, not a request to produce guidelines.

The correct first response is:

1. short acknowledgement
2. compact intake status
3. one high-impact question or decision card
4. stop

The incorrect response is anything that continues with starter steering rules, a recommended stack, repo/package split, project layout, definition of done, suggested answers, planning-run guidelines, raw JSON dump by default, or a batch checklist of future questions.

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

Do not output this layout in the first response to a rough idea when `readiness.can_generate_intake` is `false`. This layout is guidance for later workspace initialization, not a substitute for intake.

## Intake modes

### Quick mode

Use when the user wants a fast first draft.

Rules:

- Ask at most five questions.
- Make low-risk assumptions explicit.
- Mark risky unknowns as open questions.
- Produce a draft intake record quickly.

### Guided mode

Use as the default.

Rules:

- Ask exactly one high-impact question per assistant turn unless the user explicitly asks for a batch.
- The one question should be the next unanswered decision that most changes architecture, stack, MVP, safety, or parallelization.
- Do not include a checklist of future questions in the same turn.
- Use compact human-readable updates instead of repeating raw JSON unless the user asks to see the state.
- For hard choices, present the one question as an A/B/C decision card with pros, cons, MVP risk, later scaling/refactor risk, and one explicit agent recommendation.
- The first MVP-boundary question for a rough idea should normally be a decision card when sensible options can be inferred.
- The user may answer `A`, `B`, `C`, `recommended`, or a custom answer.
- Do not silently apply the recommendation; record it only if the user chooses it.
- After the user answers, update `intake_session` internally and ask the next one-question step.
- Only produce `project_intake.json` after the session is ready.
- Suggest reasonable stack options only after platform, multiplayer/sync mode, and project state are known.
- Confirm the MVP before planning.
- Confirm team/agent working style before task decomposition.

### Expert mode

Use when the user already has strong constraints.

Rules:

- Let the user paste stack choices, tool paths, repo constraints, architecture notes, and team layout.
- Ask only for missing high-risk decisions.
- Produce the intake record with minimal back-and-forth.

## Decision-card guided questions

Guided mode still asks one question per turn. A decision card is a richer way to ask that one question when the choice is difficult.

Use a decision card when the answer may create MVP difficulty or later scaling/refactor pain, especially for:

- MVP scope
- platform target
- stack or engine
- realtime versus asynchronous behavior
- backend architecture
- accounts/auth/persistence
- deployment model
- team/agent split
- proof required for done

A decision card should include:

- the single decision being made
- two or three options labeled A/B/C
- what each option means
- pros
- cons
- MVP risk
- later scaling/refactor risk
- when each option is best
- one `Agent recommendation`, with rationale
- a final question: `Choose A, B, C, recommended, or custom.`

This still counts as one guided question. Future decisions stay in `open_questions`, not in the visible decision card.

If the user answers `recommended`, record the recommended option as the selected answer and preserve the rationale. If the user answers with a custom option, record it and keep any new uncertainty as an open question.

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

Do not suggest concrete stack options on the first response to a rough idea when high-risk answers such as platform, multiplayer/sync mode, existing project state, and team/agent layout are still unknown.

When enough context exists, prefer a decision card for stack/platform choices so the user can compare MVP speed against later scaling/refactor pain.

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
- local-only versus real shared sync
- browser-first versus desktop-first
- existing repository versus greenfield
- required engine/framework
- external accounts, credentials, scraping, or automation
- team size and parallel work expectations
- hardware, SDK, or local tool constraints

## Intake session output

While questions are still open, maintain an internal `intake_session` state conforming to `contracts/intake_session.schema.json`.

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

If `readiness.can_generate_intake` is `false`, the output is not allowed to continue into guidelines or planning artifacts.

In guided mode, `next_action.questions` should contain only the single next question. Other unanswered decisions belong in `open_questions`, not in the visible next-question list.

Decision-card options are human-facing guidance. Record only the user's selected answer as the intake answer; do not treat unchosen options as project decisions.

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
