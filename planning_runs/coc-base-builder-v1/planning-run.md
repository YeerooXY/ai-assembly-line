# Planning Run Prompt

You are producing a manual planning run for the `ai-assembly-line` workflow.

## Run Slug

`coc-base-builder-v1`

## Goal

Convert the rough software idea below into a safe, structured planning artifact set.

Generated outputs are drafts until a human accepts them.
If the idea implies unsafe automation, botting, account control, live-service interference, or other unsafe behavior, safely reinterpret it into the nearest safe planning-only scope or explicitly reject the unsafe parts.

## Rough Idea

# Input Idea

Create a safe offline strategy-game base layout planner for players who want to compare and organize defensive layouts outside the game.

The tool should help users:

- sketch layout ideas on a grid
- compare tradeoffs between layouts
- record notes about strengths and weaknesses
- review planning outputs before any later implementation work

Safety and scope requirements:

- no botting
- no game-client automation
- no account automation
- no emulator control
- no live-service interaction
- no cheating
- no scraping private game APIs

## Required Output Files

Return exactly these artifact types:

- `project_spec.json`
- `repo_plan.json`
- `task_backlog.json`
- `agent_prompts.json`
- `slots_db.json`

## Output Requirements

- `project_spec.json` must describe the product summary, boundaries, repo split, domain model, frontend screens, backend services, core engine responsibilities, verification tasks, and starter prompts.
- `repo_plan.json` must define the repo ownership split.
- `task_backlog.json` must define tasks with owners, dependencies, acceptance criteria, and verification.
- `agent_prompts.json` must define prompt boundaries tied to the repo split.
- `slots_db.json` must define role slots and verification requirements.

## Constraints

- Produce planning artifacts only.
- Do not implement software.
- Do not add hidden workflow state.
- Keep outputs human-reviewable and machine-readable.
- Keep repo targets, task dependencies, prompts, and slots internally consistent.

## Response Format

Return each file in its own fenced code block with the filename immediately above the fence, for example:

`project_spec.json`
```json
{ ... }
```

Use valid JSON for all five files.
