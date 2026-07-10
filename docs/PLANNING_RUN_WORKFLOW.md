# Planning Run Workflow

A planning run converts merged project requirements into a reviewable planning package inside the product repository.

It does not start from a rough idea and it does not own the final executable task backlog in the normal guided workflow.

## Preconditions

Planning may start when:

- the product repository exists and is initialized
- the requirements/bootstrap PR is merged
- `project_workspace.json` is present
- accepted intake and requirements files are present
- blocking high-risk questions have been resolved or explicitly preserved

## Repository-first flow

```text
merged requirements
  -> fresh Planning Agent context
  -> inspect repository and accepted intake
  -> create planning artifacts on a branch
  -> validate planning run
  -> planning PR
  -> human review and merge
  -> fresh Task Splitter context
```

The Planning Agent reads merged files rather than relying on the intake conversation.

See:

- `prompts/00-planning-agent.md`
- `docs/AGENT_PR_WORKFLOW.md`
- `docs/REPOSITORY_FIRST_LIFECYCLE.md`

## Planning outputs

The normal planning run produces:

```text
project_spec.json
repo_plan.json
agent_prompts.json
slots_db.json
```

These files are first saved under the planning-run `outputs/` directory for review/validation and then written to the configured workspace paths in the planning PR.

The repository may also update:

```text
planning_runs_index.json
planning_runs/<run-id>/...
```

The planning package defines:

- accepted product interpretation
- MVP and non-goals
- architecture and module boundaries
- repository/file ownership
- shared contracts and interfaces
- screens and user flows
- verification strategy
- implementation lanes and roles
- assumptions and open questions
- enough guidance for a fresh Task Splitter

## Deliberate task-backlog separation

The normal planning run does not require or generate:

```text
task_batch_index.json
task_batches/*.json
task_backlog.json
```

Large plans may exceed a comfortable web-AI context or response size. After the planning PR is merged, a fresh Task Splitter reads the accepted planning package and creates task batches plus the canonical backlog in a separate PR.

A small project may explicitly choose a combined planning-and-task PR, but that is an optimization, not the default.

## Manual planning-run helper

Create a run scaffold:

```powershell
python tools\init_planning_run.py <run-id>
```

Reference the merged requirements in:

```text
planning_runs/<run-id>/input-idea.md
```

Refresh the AI-ready prompt by running the initializer again, then use the Planning Agent.

Validate outputs with:

```powershell
python tools\validate_planning_run.py planning_runs\<run-id>
```

The validator confirms the four planning artifacts and explicitly does not require `task_backlog.json`.

## Planning PR

When repository write access exists, the Planning Agent should create or reuse one branch:

```text
ai/planning-<run-id>
```

The PR description should include:

- accepted requirements source
- planning-run identifier
- architecture summary
- major repository/module boundaries
- unresolved questions or blockers
- verification strategy
- validation performed
- confirmation that task decomposition is intentionally deferred

Generated planning artifacts remain drafts until the PR is reviewed and merged.

## Review outcome

Reviewers should confirm:

- the plan matches merged requirements
- architecture and repository ownership are coherent
- shared interfaces are defined before parallel implementation
- role prompts and planned slots align with the repo plan
- verification is concrete
- open questions are visible
- the plan is sufficient for a separate task-splitting run
