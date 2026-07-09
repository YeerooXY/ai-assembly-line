# Web Viewer

This directory contains the static multi-page read-only viewer for the generated planning state.

Serve the repo root locally with:

`python -m http.server 8000`

Then open:

`http://localhost:8000/web/`

The viewer pages are:

- `web/index.html`: overview from `generated/project_spec.json`
- `web/repos.html`: repository split and ownership from `generated/repo_plan.json`
- `web/backlog.html`: backlog grouped by `repo_target` from `generated/task_backlog.json`
- `web/prompts.html`: prompt pack from `generated/agent_prompts.json`
- `web/slots.html`: slot board from `generated/slots_db.json`
- `web/verification.html`: verification rules, proof requirements, and raw contract rendering from generated JSON artifacts plus `contracts/*.schema.json` and `contracts/api_contract.openapi.yaml`

If the browser blocks `file://` fetches, open any page directly and use the page-level file picker to load the required `generated/*.json` files for that page.
The Verification page can still use that fallback for generated JSON, but contract rendering is fetched from the repository paths and is most reliable when serving the repo root with `python -m http.server 8000`.

Shared files:

- `web/viewer-data.js`: generated JSON loading and file-picker fallback
- `web/viewer-layout.js`: shared shell, navigation, status handling, and helpers
- `web/page-*.js`: page-specific rendering only
- `web/viewer.css`: shared styling

The viewer does not add:

- editing
- backend APIs
- authentication
- realtime sync
- frontend-only task, repo, prompt, slot, or contract models
