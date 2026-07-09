# Intake Decision Cards

Guided intake asks one question per assistant turn.

A question may still be rich enough to help the user make a good decision. For difficult architecture, MVP, stack, scaling, sync, persistence, or team-split choices, present the one question as a decision card.

## Purpose

Decision cards prevent two bad outcomes:

1. The assistant asks a vague question and leaves the user to guess the consequences.
2. The assistant silently chooses a stack, MVP, or architecture and calls it a recommendation.

A decision card keeps the user in control while making the tradeoffs visible.

## Required shape

Use this shape when a choice is hard or has long-term consequences:

```text
Decision: <one decision the user must make>

A) <option name>
What it means: <plain-language explanation>
Pros: <short list or sentence>
Cons: <short list or sentence>
MVP risk: <low | medium | high> — <why>
Scaling/refactor risk: <low | medium | high> — <why>
Best when: <when this option fits>

B) <option name>
...

C) <option name>
...

Agent recommendation: <A/B/C> — <reason>

Question: Choose A, B, C, recommended, or custom.
```

This still counts as one guided intake question.

## Rules

- Provide at most three main options unless the user asks for more.
- Include an `Agent recommendation`, but never silently apply it.
- The user may answer `A`, `B`, `C`, `recommended`, or a custom answer.
- If the user answers `recommended`, record the recommended option as the selected answer and keep the rationale.
- If the user gives a custom answer, record it and update open questions if the custom answer introduces risk.
- Keep future decisions in `open_questions`; do not turn the card into a checklist of multiple questions.
- Do not use decision cards for trivial low-risk choices.
- For the first high-impact MVP-boundary question of a rough idea, prefer a decision card when sensible options can be inferred from the idea.

## When to use decision cards

Use decision cards for choices that materially affect:

- MVP scope
- platform target
- stack or engine
- backend architecture
- realtime versus asynchronous behavior
- sync/storage model
- persistence/auth/accounts
- deployment model
- team/agent split
- proof required for done
- choices that may create later scaling or refactor pain

## Example: MVP boundary

```text
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

## Example: stack direction

```text
Recorded: team mode = 2 people working in parallel.
Status: Ready for stack choice.

Decision: Which stack direction do you want for the MVP?

A) Flutter client + backend service
What it means: Build the UI in Flutter and a separate backend for rooms, game state, and realtime events.
Pros: Best fit for desktop-first now and mobile later; one client codebase can travel far.
Cons: Backend still needs separate WebSocket/game-state work; Flutter desktop packaging has some setup cost.
MVP risk: medium — more initial setup than a pure web prototype.
Scaling/refactor risk: low-medium — mobile later is much less painful.
Best when: Mobile later is real, not just a vague maybe.

B) React + Tauri desktop client + backend
What it means: Build a web-style UI wrapped as a lightweight desktop app, with a separate backend.
Pros: Fast desktop MVP; clean client/backend split; familiar web tooling.
Cons: Mobile later probably needs a separate client or rewrite.
MVP risk: low-medium — good speed if the team knows web tooling.
Scaling/refactor risk: medium — mobile later can become a second project.
Best when: Desktop MVP speed matters more than mobile reuse.

C) React web app + Electron wrapper + backend
What it means: Build a browser-style app and package it with Electron for desktop.
Pros: Fastest if the team knows web tooling; huge ecosystem.
Cons: Heavier desktop app; mobile later is not clean; easier to accumulate frontend/backend coupling.
MVP risk: low — quickest path to something playable.
Scaling/refactor risk: high — can become painful if mobile and polish matter later.
Best when: The goal is to prove gameplay fast.

Agent recommendation: A — because the stated goal is desktop first, but mobile later matters.

Question: Choose A, B, C, recommended, or custom.
```
