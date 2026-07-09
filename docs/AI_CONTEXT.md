# AI Context Gateway

This repository exposes a deliberate remote-review context gateway for AI systems that cannot clone Git repositories or run local shell commands.

## Source Of Truth Rules

- Treat the Git repository as the only source of truth.
- Do not rely on chat history, assistant claims, or out-of-band summaries.
- Read repository files directly.
- Generated JSON files are the canonical planning state.
- The static viewer in `web/` is read-only and must not invent task, repo, prompt, slot, contract, or hidden workflow state.

## Remote Review Entry Order

1. Start from `generated/context_pack.md` if it is available.
2. If `generated/context_pack.md` is unavailable, start from `generated/review_manifest.json`.
3. Use the manifest to fetch the listed files directly from the repository.

## What To Understand First

- `README.md`
- `PROJECT_SPEC.md`
- `PRODUCT_RULES.md`
- `generated/project_spec.json`
- `generated/repo_plan.json`
- `generated/task_backlog.json`
- `generated/task_batch_index.json`
- `generated/task_batches/*.json`
- `generated/agent_prompts.json`
- `generated/slots_db.json`
- `generated/planning_runs_index.json`

## What The Viewer Is Allowed To Do

- Render generated planning state directly.
- Render contract files read-only on the Verification page.
- Fail visibly when required source-of-truth files are missing or invalid.

## What The Viewer Must Not Do

- Add backend behavior
- Add authentication
- Add realtime sync
- Add editing
- Add mutable workflow state
- Add frontend-owned task, repo, prompt, slot, or contract models
