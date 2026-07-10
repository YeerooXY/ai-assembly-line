# Outputs

This sample planning run intentionally does not include final planning JSON yet.

The four planning output files are expected here only after a Planning Agent produces them:

- `project_spec.json`
- `repo_plan.json`
- `agent_prompts.json`
- `slots_db.json`

`task_backlog.json` is intentionally deferred to the Task Splitter after the planning PR is merged.

Until then, the missing files are intentional for this draft sample.

When outputs are added, validate them with:

```powershell
python tools\validate_planning_run.py planning_runs\coc-base-builder-v1
```
