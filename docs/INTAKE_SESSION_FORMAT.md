# Intake Session Format

`project_intake.json` is the final structured intake record.

`intake_session.json` is the internal interactive state used while the Intake Interviewer is still asking questions.

A frontend can render `intake_session.json` directly. In normal chat, the assistant should show compact human-readable intake status instead of dumping raw JSON.

## Why this exists

A rough project idea should not immediately turn into a full guideline document, project spec, backlog, or implementation plan.

The intended chat flow is:

```text
rough idea
  -> compact intake status
  -> one focused question or decision card
  -> project_intake.json
  -> planning artifacts
```

This prevents the AI from jumping the gun and generating a fake-complete plan before high-risk decisions are answered.

## Source of truth

The internal session schema is:

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
- temporary or starter project guidelines
- technical steering rules
- target repository layout
- repo/package split
- definition of done
- suggested answers or default answers for the user to accept
- a full project specification
- a full task backlog
- agent work assignments
- implementation code
- architecture as if all decisions are final

Instead, it must output:

1. a short acknowledgement
2. a compact human-readable intake status summary
3. the next high-impact question, preferably as a decision card when the choice affects MVP difficulty or later scaling/refactor pain

Then it must stop. If `readiness.can_generate_intake` is `false`, the response must not continue with guidelines, recommendations, architecture, repo layout, task rules, suggested answers, or a checklist of future questions.

Do not print raw `intake_session` JSON by default. Keep it internally and show JSON only when the user asks for it, the session becomes ready for `project_intake.json`, state review is needed, or saving/exporting/persisting is requested.

## Guidelines wording trap

A user may ask for `guidelines`, `steering help`, `starter rules`, or help `setting up` a project while providing only a rough idea.

That wording still means: start intake.

It does not permit the Intake Interviewer to produce starter steering rules, temporary guidelines, stack recommendations, repo split, definition of done, suggested answers, or a checklist of future intake questions.

The correct response is to say that guidelines can be produced after the high-risk intake questions are answered, then provide only the compact intake status and the single next question in guided mode.

## Minimal first response shape

For a rough idea like `I want to build a tiny shared grocery list app for two people`, the first response should look like this:

```text
Yes — this starts intake, because guidelines should come after the high-risk project choices are known.

Intake status: started
Project: shared-grocery-list
Known: tiny shared grocery list app for two people
Still needed: MVP boundary

Decision: What is the smallest useful MVP for the two of you?

A) One-device local list
What it means: One list on one device, no sharing between devices.
Pros: fastest to build and easiest to test.
Cons: not truly shared.
MVP risk: low.
Scaling/refactor risk: high — adding real sharing later may require rethinking storage and state.
Best when: You only want to validate the list UI first.

B) Manual share/export list
What it means: One person can copy/export the list and send it to the other.
Pros: simple, with some sharing behavior.
Cons: clunky and not live.
MVP risk: low-medium.
Scaling/refactor risk: medium.
Best when: Sharing matters, but live collaboration is not required yet.

C) Real shared list with sync
What it means: Both people can edit the same list from separate devices.
Pros: matches the actual product idea.
Cons: needs backend/sync/conflict decisions.
MVP risk: medium-high.
Scaling/refactor risk: low-medium — avoids fake-sharing rework later.
Best when: The core value is truly shared usage.

Agent recommendation: C — if “shared” is the point of the product; A only if you want the fastest throwaway prototype.

Question: Choose A, B, C, recommended, or custom.
```

This is not a required exact output. It is the intended shape: compact state plus one useful decision.

In guided mode, `next_action.questions` should contain only the single next question. Other unanswered decisions belong in `open_questions`, not in the visible next-question list.

## Compact guided updates

Normal guided turns should not print the full JSON.

Use a compact update like:

```text
Recorded: MVP sharing mode = real shared list with sync.
Status: MVP boundary is clear; platform/stack is still open.

Decision: Which platform should the MVP target first?
...
```

Show the full `intake_session` only when:

- the user asks to see the JSON or full session state,
- the session becomes ready for `project_intake.json`,
- a save/export/persist step is requested, or
- the state has become ambiguous and needs explicit review.

The compact update still represents an updated `intake_session`; it just does not dump the entire object into the chat.

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

If `can_generate_intake` is `false`, the next output should ask the next single question in guided mode or suggest stack options only when `next_action.type` is `suggest_stack`.
