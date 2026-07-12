# Intake Durability and Response Discipline

This policy applies to every guided AI Assembly Line intake, regardless of the model's personality, preferred writing style, or conversational habits.

## Purpose

Long guided sessions can lose chat context. Verbose reflections after every answer also consume context and cause the interviewer to drift into planning. Accepted decisions must therefore be persisted immediately and responses must remain mechanically concise.

## Personality-resistant response contract

Repository instructions override personality, warmth, enthusiasm, storytelling, and stylistic defaults during guided intake.

After the user answers a question, the response may contain only:

1. one concise recorded-answer line;
2. one compact status line when it materially helps;
3. exactly one next question or A/B/C decision card.

Then stop.

Do not add:

- praise or validation of the user's choice;
- an explanation of why the choice is excellent, coherent, exciting, or consistent;
- examples expanding the accepted feature unless clarification is required;
- newly invented design principles, epics, tasks, roadmaps, or observations;
- summaries of the entire project after each answer;
- previews of future questions;
- meta-commentary about the intake process.

### Minimal-answer rule

When the user replies only `A`, `B`, `C`, `recommended`, or another unambiguous short selection:

- record the selected option;
- persist it;
- immediately ask the next question.

Do not paraphrase or elaborate the option beyond one short line.

When the user includes reasoning or extra constraints:

- preserve the material constraints in durable state;
- acknowledge them in at most two short lines;
- do not restate their reasoning at length.

## Strong A/B/C mode

Use A/B/C decision cards for high-impact choices whenever two or three meaningful alternatives exist.

Each card should contain only:

- the decision title;
- A/B/C options;
- concise pros;
- concise cons;
- MVP risk;
- later scaling/refactor risk when relevant;
- one recommendation, which may be a hybrid.

Avoid decorative prose between sections. The user may answer with a letter, `recommended`, a hybrid, or a custom choice.

Do not silently convert a hybrid/custom answer into one of the listed options.

## Per-decision persistence

Once a product repository and writable bootstrap/intake branch exist, every accepted answer must be persisted before asking the next question.

Default draft path:

```text
assembly/intake/intake_session.json
```

A human-readable live log may also be maintained at:

```text
assembly/intake/LIVE_INTAKE.md
```

The agent should:

1. update the current intake state with only accepted facts;
2. commit the update on the active bootstrap/intake branch;
3. use a focused commit message such as `Record intake decision 12: multiplayer scope`;
4. verify the write succeeded;
5. ask the next question.

Do not wait for ten questions, the end of a chapter, or the final requirements package. Fine-grained commits are intentional recovery points.

If repository writes are temporarily unavailable:

- say `Persistence status: blocked` in the compact status;
- retain a clearly marked unsaved decision count;
- persist all unsaved decisions as soon as writes become available;
- never imply that chat-only state is durable.

## Source-of-truth boundary

Draft intake commits are recovery state, not accepted requirements. The requirements/bootstrap pull request remains the human approval boundary, and merged `project_intake.json` plus `REQUIREMENTS.md` remain authoritative.

## Proven-good reference

The `YeerooXY/destructro-truck` intake is a reference for the desired flow: disciplined one-question turns, aggressively protected MVP scope, concise decisions, and a complete final intake without conversational drift.
