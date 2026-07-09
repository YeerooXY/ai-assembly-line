# Intake Session Format

`project_intake.json` is the final structured intake record.

`intake_session.json` is the interactive state used while the Intake Interviewer is still asking questions.

The frontend should render `intake_session.json` while intake is in progress, then render or save `project_intake.json` once the session is ready.

## Why this exists

A rough project idea should not immediately turn into a full guideline document, project spec, backlog, or implementation plan.

The first response should be an intake session update:

```text
rough idea
  -> intake_session update
  -> focused questions
  -> project_intake.json
  -> planning artifacts
```

This prevents the AI from jumping the gun and generating a fake-complete plan before high-risk decisions are answered.

## Source of truth

The schema is:

```text
contracts/intake_session.schema.json
```

The session eventually produces:

```text
contracts/project_intake.schema.json
```

## Required behavior for a new project request

When a user provides only a rough idea, the Intake Interviewer must not output:

- a full guideline document
- a full project specification
- a full task backlog
- agent work assignments
- implementation code
- architecture as if all decisions are final

Instead, it must output:

1. a short acknowledgement
2. an `intake_session` state block
3. the next high-impact questions

## Session states

Allowed `status` values:

- `not_started`
- `in_progress`
- `ready_for_intake_record`
- `intake_record_drafted`
- `blocked`

Allowed `next_action.type` values:

- `ask_questions`
- `suggest_stack`
- `draft_project_intake`
- `handoff_to_planning`
- `blocked`

## Minimal first response shape

For a rough idea like `I want to build a multiplayer Tron game`, the first response should look like this:

```json
{
  "schema_version": "0.1.0",
  "project_slug": "multiplayer-tron",
  "mode": "guided",
  "status": "in_progress",
  "current_section": "goal-and-mvp",
  "sections": [
    {
      "id": "goal-and-mvp",
      "label": "Goal and MVP",
      "status": "in_progress",
      "questions": [
        {
          "id": "goal-001",
          "question": "What kind of multiplayer should the first playable version support: local same-keyboard, LAN, private online rooms, or public matchmaking?",
          "answer": "",
          "risk_level": "high",
          "affects": ["mvp", "networking", "stack"]
        }
      ]
    }
  ],
  "stack_options": [],
  "assumptions": [
    "The project is a standalone original game, not automation of an existing game or service."
  ],
  "open_questions": [
    {
      "question": "What kind of multiplayer should the MVP support?",
      "risk_if_unanswered": "The architecture and stack cannot be chosen safely."
    }
  ],
  "readiness": {
    "can_generate_intake": false,
    "missing_high_risk_answers": [
      "MVP multiplayer mode",
      "target platform",
      "stack preference or permission to recommend one",
      "greenfield versus existing repo",
      "parallel humans/AI agents"
    ]
  },
  "next_action": {
    "type": "ask_questions",
    "questions": [
      "What kind of multiplayer should the first playable version support: local same-keyboard, LAN, private online rooms, or public matchmaking?",
      "Which platform matters first: browser, desktop, mobile, or something else?",
      "Do you already prefer a stack, or should I recommend one?",
      "Is this a greenfield project or an existing repository?",
      "How many humans or AI agents should work in parallel?"
    ]
  }
}
```

This is not a required exact output. It is the intended shape: visible session state plus focused questions.

## Frontend rendering guidance

A frontend intake page should render:

- current status
- current section
- completed sections
- unanswered high-risk questions
- suggested stack options
- assumptions
- readiness to generate `project_intake.json`
- next action

The frontend must not invent intake fields outside `contracts/intake_session.schema.json`.

## Transition to project_intake.json

Only when `readiness.can_generate_intake` is `true` should the Intake Interviewer draft `project_intake.json`.

If `can_generate_intake` is `false`, the next output should ask questions or suggest stack options instead of creating planning artifacts.
