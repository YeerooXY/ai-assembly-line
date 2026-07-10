# Web Viewer

This directory contains the static multi-page read-only viewer for generated planning and execution-coordination state.

Serve the repo root locally with:

`python -m http.server 8000`

Then open:

`http://localhost:8000/web/`

If the browser blocks `file://` fetches, open any page directly and use the page-level file picker to load the required generated JSON files for that page.

## Project loading modes

The viewer supports two static data modes:

- Root seed mode: open `web/dispatch.html` with no `?project=` parameter. Pages load root `generated/*.json`.
- Project workspace mode: open `web/dispatch.html?project=snake-game`. Pages load `projects/index.json`, then `projects/snake-game/project_workspace.json`, then that workspace's project-scoped generated files.

Project workspace paths are resolved relative to the selected workspace root. For example, if `projects/snake-game/project_workspace.json` points `paths.generated.task_backlog` to `generated/task_backlog.json`, the browser fetches:

`../projects/snake-game/generated/task_backlog.json`

Use the project selector in the shared header to switch projects while staying on the current viewer page.

## Page roles

Dispatch is the primary task-pickup surface. Assignments and Task Batches remain useful, but they have narrower roles:

- `web/dispatch.html`: primary "what can I do next?" page. It renders topological task waves from the selected `task_backlog.json`, overlays execution state from the selected `collaboration_state.json`, colors tasks by availability, and generates one-task execution context for a fresh AI chat.
- `web/assignments.html`: audit/status page for task ownership, execution status, notes, proof references, and project-scoped collaboration state.
- `web/task-batches.html`: generation/validation page for guided task splitting, task batch index readiness, generated batch files, and dependency graph checks.

The remaining viewer pages are:

- `web/index.html`: overview from `project_spec.json`
- `web/repos.html`: repository split and ownership from `repo_plan.json`
- `web/backlog.html`: backlog grouped by `repo_target` from `task_backlog.json`
- `web/prompts.html`: prompt pack from `agent_prompts.json`
- `web/slots.html`: slot board from `slots_db.json`
- `web/planning-runs.html`: planning-run scaffold and output completeness from `planning_runs_index.json`
- `web/verification.html`: verification rules, proof requirements, and raw contract rendering from generated JSON artifacts plus `contracts/*.schema.json` and `contracts/api_contract.openapi.yaml`

See `docs/VIEWER_PAGE_ROLES.md` for the page-consolidation decision.

## Source files

Root seed sources:

- `generated/project_spec.json`
- `generated/repo_plan.json`
- `generated/task_backlog.json`
- `generated/task_batch_index.json`
- `generated/task_batches/*.json`
- `generated/collaboration_state.json`
- `generated/task_runs/*.json`
- `generated/agent_prompts.json`
- `generated/slots_db.json`
- `generated/planning_runs_index.json`

Project workspace sources are resolved through:

- `projects/index.json`
- `projects/<project-id>/project_workspace.json`
- `projects/<project-id>/generated/*.json`

Contract files are most reliable when serving the repo root with `python -m http.server 8000`. Generated JSON can also be loaded through the local file picker.

## Shared files

- `web/project-workspace.js`: project registry/workspace selection and path resolution
- `web/viewer-data.js`: generated JSON loading and file-picker fallback
- `web/viewer-layout.js`: shared shell, navigation, project selector, status handling, and helpers
- `web/page-*.js`: page-specific rendering only
- `web/page-dispatch-keyboard.js`: small keyboard helper for Enter/Space task-node activation on Dispatch
- `web/viewer.css`: shared styling

## Still intentionally absent

The viewer does not add:

- editing as persisted browser state
- backend APIs
- authentication
- realtime sync
- direct task claiming
- file writes
- frontend-only task, repo, prompt, slot, planning-run, execution, or contract models
