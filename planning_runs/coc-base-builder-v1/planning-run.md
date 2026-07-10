# Planning Run Prompt

You are producing a repository-first planning run for the `ai-assembly-line` workflow.

## Run Slug

`coc-base-builder-v1`

## Preconditions

- The product repository is initialized.
- Accepted requirements are the source of truth.
- Task decomposition is deliberately deferred to a later Task Splitter run.

## Accepted Requirements Reference

Create a safe offline strategy-game base layout planner for players who want to compare and organize defensive layouts outside the game.

The tool should help users:

- sketch layout ideas on a grid
- compare tradeoffs between layouts
- record notes about strengths and weaknesses
- review planning outputs before later implementation work

Safety and scope requirements:

- no botting
- no game-client automation
- no account automation
- no emulator control
- no live-service interaction
- no cheating
- no scraping private game APIs

## Required Output Files

- `project_spec.json`
- `repo_plan.json`
- `agent_prompts.json`
- `slots_db.json`

## Deliberate Separation

Do not produce `task_batch_index.json`, task batch files, or `task_backlog.json`.

After the planning package is reviewed and merged, a fresh Task Splitter context should create the implementation tasks in a separate PR.

## Output Requirements

- `project_spec.json` defines the accepted product, boundaries, domain model, screens, responsibilities, interfaces, and verification.
- `repo_plan.json` defines repository/module ownership.
- `agent_prompts.json` defines role-level prompt boundaries tied to the repo plan.
- `slots_db.json` defines planned role/lane slots and verification expectations.

## Constraints

- Produce planning artifacts only.
- Do not implement software.
- Do not add hidden workflow state.
- Keep project names, repo targets, prompts, and slots internally consistent.
- Preserve unresolved questions rather than inventing answers.

## Response Format

Return each file in its own fenced JSON block with the filename immediately above it.

Use valid JSON for all four files.
