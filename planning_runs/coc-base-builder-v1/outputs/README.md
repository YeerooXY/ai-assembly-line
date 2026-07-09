# Outputs

This sample planning run intentionally does not include final generated output JSON yet.

The five required output files are expected to appear here only after a planning agent produces them:

- `project_spec.json`
- `repo_plan.json`
- `task_backlog.json`
- `agent_prompts.json`
- `slots_db.json`

Until then, their absence is intentional for this draft sample folder.

When outputs are added, validate them with:

```powershell
python tools\validate_planning_run.py planning_runs\coc-base-builder-v1
```
