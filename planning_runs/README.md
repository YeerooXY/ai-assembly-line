# Planning Runs

This directory stores manual planning runs created from rough software ideas.

Each planning run should live in its own folder:

```text
planning_runs/<run-slug>/
```

Typical contents:

- `input-idea.md`: the rough idea captured for the run
- `planning-run.md`: the AI-ready prompt generated from that idea
- `review-notes.md`: human acceptance or rejection notes
- `outputs/`: saved planning artifacts returned by the AI tool

What should be committed:

- run folders that are accepted, shared for review, or useful as traceable examples
- the original input idea when it is safe to store in the repository
- the generated planning prompt
- the saved output artifacts
- the human review outcome

What should not be committed:

- secrets
- tokens
- credentials
- unsafe or sensitive proprietary input that should not live in Git

Planning runs remain human-reviewed planning artifacts. They do not imply implemented software or autonomous execution.
