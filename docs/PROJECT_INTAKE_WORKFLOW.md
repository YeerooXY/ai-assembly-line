# Project Intake Workflow

Project intake is the first guided conversation after a repository has been selected or prepared.

Its purpose is to turn a rough idea into an accepted requirements package without jumping directly into architecture or executable tasks.

## Position in the repository-first lifecycle

```text
rough idea
  -> create or select repository
  -> verify repository readiness
  -> guided intake interview
  -> project_intake.json + REQUIREMENTS.md
  -> requirements/bootstrap PR
  -> human review and merge
  -> planning run
```

The product repository is the durable handoff between stages. Chat history is not the source of truth.

See `docs/REPOSITORY_FIRST_LIFECYCLE.md` for the complete lifecycle and phase gates.

## Repository gate

Before requirements are persisted, determine whether the project is:

- greenfield and needs a repository
- greenfield with a newly created repository
- an existing repository
- planning-only with no repository yet

For a normal greenfield product, the preferred route is:

1. propose repository owner, name, visibility, and default branch
2. create the repository when connected tooling supports it, otherwise guide the user through the short manual creation step
3. verify that the repository exists, is accessible, and has an initialized default branch
4. continue intake against that repository

Do not create a real product under `ai-assembly-line/projects/<id>/` merely because the product repository is not ready. Central registry mode is optional, not the default escape hatch.

## Guided intake behavior

Guided mode remains the default.

- Ask exactly one high-impact user-facing question per turn unless the user requests a batch.
- Ask when an answer changes MVP, architecture, platform, safety, stack, repository setup, or parallelization.
- Assume only low-risk details that are easy to revise.
- Use A/B/C decision cards for difficult choices, with pros, cons, MVP risk, later refactor risk, and one recommendation.
- Do not silently accept the recommendation.
- Keep future unknowns in internal/open-question state rather than displaying a long checklist.
- Do not dump raw `intake_session` JSON unless requested, needed for review, or ready to persist.

## First response hard stop

For a rough idea without a complete intake record, respond with only:

1. a short acknowledgement
2. a compact intake status
3. one next high-impact question

Then stop.

Do not include a final stack, full architecture, repository layout, task backlog, agent assignments, implementation code, or suggested answers on the first turn.

## Questions that matter

Intake should cover only the decisions necessary to produce a useful requirements PR:

- product goal and target users
- smallest useful MVP
- target platforms
- preferred or recommended stack direction
- greenfield versus existing repository
- repository owner/name/visibility for greenfield work
- existing code, docs, tests, constraints, SDKs, or hardware
- human and AI collaboration model
- task size and proof expectations
- external services, credentials, automation, and safety boundaries
- acceptance signals for the MVP

## Intake state and final output

While questions remain, maintain an internal `intake_session` conforming to `contracts/intake_session.schema.json`.

When ready, produce `project_intake.json` conforming to `contracts/project_intake.schema.json` plus a concise human-readable `REQUIREMENTS.md`.

The requirements package should preserve:

- accepted decisions
- explicit assumptions
- unresolved non-blocking questions
- rejected or deferred scope
- repository identity and readiness
- MVP acceptance signals

## Requirements/bootstrap PR

For a repository-first project, intake ends by preparing a PR in the product repository.

Typical files:

```text
project_workspace.json
assembly/intake/project_intake.json
assembly/requirements/REQUIREMENTS.md
assembly/context/handoff.md
assembly/context/repository-notes.md
assembly/generated/collaboration_state.json
```

The PR description should summarize accepted decisions, open questions, and what becomes available after merge.

This PR must not include the final architecture or task backlog.

## Hand-off to Planning

Planning becomes available only after the requirements PR is merged.

The Planning Agent should read the merged repository files, especially:

```text
project_workspace.json
assembly/intake/project_intake.json
assembly/requirements/REQUIREMENTS.md
repository source/docs/tests
```

It should not depend on the original intake chat.
