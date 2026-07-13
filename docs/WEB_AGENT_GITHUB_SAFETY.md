# Web-Agent GitHub Safety

Repository-connected agents do not all have a local checkout, Git, GitHub CLI,
or a shell. Detect the available capabilities before choosing a workflow. A
missing local tool is not evidence that the remote repository, branch, or file
is missing.

## Choose the operating mode first

Use local Git only after all of the following have been verified:

- the repository has an explicit local checkout;
- the current directory is inside that checkout;
- `git status` succeeds;
- the expected remote and branch are known;
- any required CLI authentication succeeds.

Otherwise, use the GitHub connector directly for repository reads, comparisons,
branch operations, commits, and pull requests. Do not repeatedly try local
`git` or `gh` commands in a container that has no checkout or CLI.

## Prefer direct reads for known state

- For a known branch name, read a known file at that ref, compare the branch to
  the default branch, or inspect its pull request directly. An empty branch
  search result is not proof that the branch does not exist.
- Fetch a known repository path directly. Reserve code search for genuinely
  unknown locations.
- Before fetching an uncertain path, inspect a repository tree, a known parent
  directory, imports, links, or the workspace manifest. Stop guessing after a
  failed fetch and establish the path first.

Connector search is discovery assistance, not an authoritative existence test.

## Recheck branch and pull-request state before every write

At startup, before each guided continuation, and before finalization:

1. read the current default-branch head;
2. inspect the stage branch's pull-request state;
3. compare the default branch with the stage branch;
4. stop if the stage PR is merged or the branch is behind the default branch.

A merged branch is closed permanently. Never append work to it, even if the
remote still permits commits. Create a fresh continuation branch from the
current default branch.

If commits were accidentally added after merge, do not continue writing and do
not silently merge the diverged branch. Record the exact ahead/behind state,
create a new branch from current default, and deliberately cherry-pick or
reapply only the unmerged commits. Review the recovered diff before continuing.

## Make related repository updates atomic

When several generated files form one state transition, commit them together.
With a GitHub connector that exposes low-level Git objects, prefer:

```text
create blobs
  -> create one tree
  -> create one commit
  -> update the branch ref once
```

Avoid one connector commit per file for an index, batch, and handoff update that
must agree with each other. Fine-grained intake decision commits remain
intentional recovery points and are not covered by this batching rule.

## Keep generated files reviewable

- Pretty-print JSON with consistent indentation.
- End text and JSON files with a newline.
- Inspect the resulting diff or file content after writing.
- Do not place an entire generated JSON document on one line; connector output
  and line-range review become unreliable when that line is truncated.

## Report validation precisely

Run the repository's actual validator in an environment that has the repository
and required runtime. Manual schema inspection is not executable validation.

Use precise status language:

- `schema-valid` only when schema validation actually ran and passed;
- `repository validator passed` only when the documented validator command ran
  successfully;
- `structurally checked against the schema` for manual inspection;
- `validation pending` when execution is unavailable or the full graph is not
  yet present.

Do not mark an index entry `validated` solely from manual review. Preserve and
report validator failures, including failures caused by intentionally missing
future batches, instead of relabeling them as success.

## Safe continuation checklist

Before writing the next generated batch:

- [ ] repository and default branch are explicit;
- [ ] operating mode (local checkout or connector-only) is verified;
- [ ] lifecycle prerequisite PRs are merged;
- [ ] the active stage PR is still open or has not yet been created;
- [ ] the active branch is not behind the default branch;
- [ ] known files were read directly from the intended ref;
- [ ] uncertain paths were established before fetching;
- [ ] the write will be one atomic, pretty-printed state transition;
- [ ] validation claims match commands that actually ran.
