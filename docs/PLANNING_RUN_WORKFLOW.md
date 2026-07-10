# Planning Run Workflow

A planning run converts merged project requirements into a reviewable planning package inside the product repository.

It does not start from a rough idea and it does not own the final executable task backlog in the normal guided workflow.

## Preconditions

Planning may start when:

- the product repository exists and is initialized
- the requirements/bootstrap PR is merged
- `project_workspace.json` is present
- the accepted intake and requirements files are present
- blocking high-risk questions have been resolved or explicitly preserved

## Repository-first flow

```text
merged requirements
  -> fresh planning context
  -> inspect repository and accepted intake
  -> generate planning package
  -> planning PR
  -> human review and merge
  -> task splitting in a fresh context
```

The planning agent reads merged files rather than relying on the intake conversation.

## Planning outputs

The normal planning PR should produce:

```text
assembly/generated/project_spec.json
assembly/generated/repo_plan.json
assembly/generated/agent_prompts.json
assembly/generated/slots_db.json
assembly/generated/planning_runs_index.json
assembly/planning_runs/<run-id>/...
```

The planning package should define:

- accepted product interpretation
- MVP and non-goals
- architecture and module boundaries
- repository/file ownership
- shared contracts and interfaces
- screens and user flows
- verification strategy
- implementation lanes and roles
- assumptions and open questions

## Deliberate task-backlog separation

For the default guided flow, planning does not generate the final `task_backlog.json`.

Large plans may exceed a comfortable web-AI context or response size. After the planning PR is merged, a fresh Task Splitter conversation reads the accepted planning package and creates task batches plus the canonical backlog in a separate PR.

A small project may explicitly choose a combined planning-and-task PR, but that is an optimization, not the default.

## Planning PR

The planning stage should create a branch and open a PR in the selected product repository.

The PR description should include:

- accepted requirements source
- architecture summary
- major repository/module boundaries
- unresolved questions or blockers
- verification strategy
- confirmation that task decomposition is intentionally deferred

Generated planning artifacts remain drafts until this PR is reviewed and merged.

## Review outcome

Reviewers should confirm:

- the plan matches merged requirements
- architecture and repository ownership are coherent
- shared interfaces are defined before parallel implementation
- verification is concrete
- open questions are visible
- the plan is sufficient for a separate task-splitting run
