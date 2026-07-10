# Planning Runs

This directory stores traceable repository-first planning runs created from merged project requirements.

Each run lives in:

```text
planning_runs/<run-slug>/
```

Typical contents:

- `input-idea.md`: references and summarizes the merged requirements; it must not override them
- `planning-run.md`: AI-ready Planning Agent prompt generated for the run
- `review-notes.md`: human acceptance or rejection notes
- `outputs/`: planning artifacts proposed by the run

Normal required outputs:

- `project_spec.json`
- `repo_plan.json`
- `agent_prompts.json`
- `slots_db.json`

The final `task_backlog.json` is deliberately deferred to the Task Splitter after the planning PR is merged.

What should be committed:

- accepted or reviewable run folders
- safe requirements references and summaries
- the generated planning prompt
- planning output artifacts
- human review outcome

What should not be committed:

- secrets
- tokens
- credentials
- sensitive proprietary input that should not live in Git
- a fake placeholder backlog created only to satisfy an older workflow

Planning runs remain human-reviewed planning artifacts. They do not imply implemented software or accepted task decomposition.
