# Task Generation Workflow

Task generation is a separate repository-first lifecycle stage that begins only after the planning PR is reviewed and merged.

The Planning Agent defines the accepted product, architecture, repository ownership, interfaces, roles, and verification strategy. The Task Splitter converts that merged package into executable task batches and the canonical backlog.

## Workflow position

```text
initialized repository
  -> requirements/bootstrap PR merged
  -> planning PR merged
  -> fresh Task Splitter context
  -> task batch index + batch files on one branch
  -> validation + canonical task backlog
  -> task-decomposition PR
  -> human review and merge
  -> Dispatch
```

The Task Splitter must read merged repository files rather than relying on the planning conversation.

## Preconditions

Task generation may start when:

- `project_workspace.json` exists
- accepted intake and requirements files exist
- `project_spec.json` exists
- `repo_plan.json` exists
- the planning PR is merged
- repository targets, lanes, interfaces, and verification expectations are sufficiently defined

If these gates are missing, return to the appropriate earlier lifecycle stage. Do not compensate by inventing architecture inside task records.

## Source inputs

Resolve paths through `project_workspace.json`.

Read:

- accepted intake and requirements
- `project_spec.json`
- `repo_plan.json`
- `agent_prompts.json`
- `slots_db.json`
- planning-run trace and review notes
- current repository tree
- task, batch, collaboration-state, and slot contracts
- task creation and card-format guidance

Repository files are authoritative.

## Outputs

The task-decomposition branch and PR should produce or update:

- configured `task_batch_index.json`
- every indexed file under the configured task-batches directory
- configured canonical `task_backlog.json`
- configured `collaboration_state.json`
- configured `slots_db.json` when task readiness changes

The Task Splitter must not modify accepted requirements or redesign `project_spec.json` / `repo_plan.json`.

## Repository branch workflow

Use one unmerged branch for the whole split:

```text
ai/task-split-<planning-run-id>
```

For a large plan:

1. create and commit the batch index
2. generate exactly one next batch per guided continuation
3. commit each batch to the same branch
4. update batch statuses
5. recover from fresh chats by inspecting the branch
6. validate after all batches exist
7. build the canonical backlog
8. update collaboration state and slot readiness
9. open one task-decomposition PR

The branch is the durable in-progress state. Conversation memory is optional.

Before every continuation, inspect the branch's PR state and compare it with the
current default branch. A merged task-split branch is closed permanently. If a
partial task-decomposition PR was merged, create a fresh continuation branch
from current default and deliberately recover only unmerged work before
generating another batch. Do not append commits to the merged branch.

## Workspace-relative paths

`project_workspace.json` determines repository-root-relative locations.

For every index entry:

```text
output_path = <paths.generated.task_batches_dir>/<batch_id>.json
```

Valid examples include:

```text
generated/task_batches/frontend.json
assembly/generated/task_batches/frontend.json
projects/example/generated/task_batches/frontend.json
```

The validator checks the configured directory rather than assuming root `generated/`.

## Generation phases

### 1. Freeze accepted planning state

Record:

- accepted planning source paths
- MVP boundary
- repo/module ownership
- interface-first ordering
- implementation lanes
- verification expectations
- unresolved blockers

If a high-risk product decision is absent from the accepted plan, do not decide it silently.

### 2. Create the batch index

Group work by owner role, repo target, lane, milestone, or a mixed strategy.

The index should:

- keep batches small enough for one focused web-AI response
- allocate stable task IDs
- declare cross-batch dependencies
- point to exact repository-root-relative batch paths
- order batches topologically

### 3. Generate shared contracts first

Contract/interface tasks should precede implementation tasks that consume them.

Examples:

- game rules contract
- API or event contract
- data model
- file ownership boundary
- test scenario matrix

### 4. Generate parallel lanes

Use lanes that reduce file overlap, such as:

- `shared-contract`
- `client-ui`
- `backend-game-state`
- `core-domain`
- `tests-verification`
- `docs-devex`

Prefer a small contract-first layer followed by parallel feature or subsystem work.

### 5. Make dependencies explicit

Every task must reference prerequisite task IDs.

Dependencies may cross batches, but a task may depend only on a task in the same or an earlier batch.

### 6. Add observable completion proof

Every task needs:

- acceptance criteria
- verification steps
- required proof when appropriate
- explicit non-goals where scope could drift

A task without observable verification is not ready.

### 7. Build the canonical backlog

After every batch validates:

```powershell
python tools\validate_task_batches.py
python tools\build_task_backlog_from_batches.py
python tools\validate_task_batches.py
```

In a standalone workspace, the copied tools auto-detect a nearby `project_workspace.json`. An explicit workspace-manifest path may also be supplied.

### 8. Update coordination state

After backlog creation:

- point collaboration state at the canonical backlog
- preserve valid actors and history
- flag stale references
- do not auto-claim tasks
- do not mark tasks complete without proof
- update slot readiness only when justified by task coverage and dependencies

### 9. Open the PR

The task-decomposition PR should summarize:

- accepted planning source
- batching strategy
- batch and task counts
- dependency/cycle validation
- backlog and collaboration-state paths
- slot changes
- blockers and post-MVP separation
- validation results

The backlog becomes accepted only after merge.

## Parallel-safe task rules

For each task, confirm:

1. one owner can complete it in one focused session
2. dependencies are explicit
3. allowed files or repository boundaries are clear
4. acceptance criteria are observable
5. verification is concrete
6. unresolved product decisions are not silently decided
7. the task does not overlap another task unnecessarily

Split or rewrite tasks that fail these checks.

## Blocking tasks

Use a blocking task only when the accepted plan intentionally preserves a decision that must be resolved before downstream work.

If many blocking tasks are required, the planning package is not ready and should be revised instead.

## Done state

Task decomposition is ready for review when:

- every index batch has its expected file
- every expected task ID exists exactly once
- dependencies reference existing tasks
- the graph is acyclic
- batch order is topological
- contract/interface work precedes consumers
- MVP and post-MVP work are distinguishable
- every task has acceptance criteria and verification
- the canonical backlog was generated from validated batches
- collaboration state references the canonical backlog
- one complete PR contains the proposed task state
