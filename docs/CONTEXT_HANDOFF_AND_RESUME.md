# Context Handoff and Deterministic Resume

Context handoff is a continuous repository property, not a special ceremony performed only when a user asks to switch chats.

## UX goal

At any moment, a fresh agent must be able to answer from repository state alone:

- Where is the project in the lifecycle?
- Which role is active?
- Which repository, branch, commit, and PR contain the current work?
- Which files are authoritative?
- What was completed last?
- What is being decided or implemented now?
- What must happen next?
- Are any accepted decisions unsaved?
- Which AI Assembly Line version and instructions govern the project?

The user must not need to explain what the previous agent knew or invent a handoff prompt.

## Required portable artifacts

Every product repository maintains:

```text
assembly/context/CURRENT_HANDOFF.json
assembly/context/NEW_CHAT_RESUME.md
```

`CURRENT_HANDOFF.json` is the machine-readable resume capsule and must validate against `assembly/contracts/context_handoff.schema.json`.

`NEW_CHAT_RESUME.md` is the zero-explanation entrypoint a user can point a fresh agent to.

## Always-ready update triggers

Update and commit both artifacts whenever any of these changes:

- an intake decision is accepted, revised, or superseded;
- the current discovery section or question changes;
- persistence becomes blocked or clean again;
- a PR is opened, retargeted, merged, or closed;
- the lifecycle phase changes;
- the active role changes;
- planning ownership or milestones change;
- task splitting identifies a new active lane or dependency-ready task;
- a task completes or becomes blocked;
- the exact next action changes.

Handoff state should normally be clean before the agent asks the user another question or ends a work turn.

## Resume sequence

A fresh agent must:

1. read repository `AGENTS.md`;
2. read `project_workspace.json`;
3. read `assembly/context/CURRENT_HANDOFF.json`;
4. verify repository, branch, commit, and PR state;
5. read every path in `authoritative_artifacts`;
6. read the complete active-role prompt from installed `assembly/prompts/`;
7. follow the recorded `next_action`;
8. avoid repeating accepted questions or tasks;
9. persist new accepted state before moving on.

The installed product-repository instructions are primary. The local framework checkout is not required for ordinary resume because the curated prompts, contracts, and tools are installed under `assembly/`.

## Framework provenance

The handoff records:

- framework repository;
- installed framework ref;
- installed kit version.

This lets a fresh agent understand which rules apply and whether the product kit may need an explicit upgrade PR.

Do not silently use newer framework behavior that is absent from the installed product kit.

## Portable and local state

Committed handoff state must contain portable repository-relative information only.

Do not commit:

- personal absolute paths;
- usernames or home-directory paths;
- editor state;
- local credentials;
- machine-specific interpreter paths.

Optional machine-local discovery may live in:

```text
.assembly/local_context.json
```

That file must be gitignored. It may record local checkout paths, shell, interpreter, and editor/tool details.

## Personality and operating behavior

Handoff does not attempt to mimic the previous agent's personality. It preserves project behavior through committed rules:

- active role and full role prompt;
- response envelope;
- one-question or one-task mode;
- decision-card rules;
- persistence rules;
- Product DNA and requirements;
- architecture, ownership, and proof requirements.

Generic model personality must not override the repository contract.

## Validation requirements

The validator must fail when:

- the JSON does not match the handoff schema;
- the repository does not match `project_workspace.json`;
- the active branch does not match the checked-out branch when local validation is used;
- the recorded commit is missing or not reachable from the active branch;
- an authoritative artifact is missing;
- `next_action` is empty;
- persistence status is not `ready`;
- unsaved decisions are nonzero;
- the active role conflicts with the lifecycle phase;
- the framework repository or installed version is absent.

Expected success marker:

```text
RESULT OK context_handoff_ready=true unsaved_decisions=0
```

## Recovery behavior

When validation fails, do not continue normal product discovery, planning, task splitting, or implementation.

Report the exact stale or missing state, repair the handoff from committed artifacts and PR state, and mark any reconstructed content unverified until the user confirms it.

## Minimal user experience

A user opening a new chat should only need to provide the repository and say:

```text
Read assembly/context/NEW_CHAT_RESUME.md and follow it exactly.
```

When repository-aware tooling can discover the current project automatically, even that instruction may be replaced by a future Resume action in the UI.
