from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

SOURCE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9\-]*$")
KIT_VERSION = "0.1.1"

CONTRACT_FILES = (
    "repository_bootstrap.schema.json",
    "project_workspace.schema.json",
    "project_lifecycle.schema.json",
    "intake_session.schema.json",
    "project_intake.schema.json",
    "project_spec.schema.json",
    "repo_plan.schema.json",
    "task.schema.json",
    "task_batch_index.schema.json",
    "task_batch.schema.json",
    "task_run.schema.json",
    "task_execution_context.schema.json",
    "collaboration_state.schema.json",
    "slot.schema.json",
    "agent_prompt.schema.json",
    "api_contract.openapi.yaml",
)

PROMPT_FILES = (
    "00-intake-interviewer.md",
    "00-planning-agent.md",
    "06-task-splitter.md",
    "07-task-executor.md",
    "08-project-workspace-initializer.md",
)

TOOL_FILES = (
    "workspace_paths.py",
    "init_planning_run.py",
    "validate_planning_run.py",
    "build_planning_runs_index.py",
    "validate_seed.py",
    "validate_task_batches.py",
    "build_task_backlog_from_batches.py",
    "validate_collaboration_state.py",
    "prepare_task_context.py",
)

IGNORED_NAMES = {"__pycache__", ".DS_Store"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_text(path: Path, content: str, *, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def validate_project_id(project_id: str) -> None:
    if PROJECT_ID_RE.fullmatch(project_id) is None:
        raise ValueError("project_id must match ^[a-z0-9][a-z0-9\\-]*$")


def run_git(target: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(target), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise ValueError(detail)
    return result.stdout.strip()


def verify_git_repository(target: Path, expected_branch: str) -> dict[str, Any]:
    if not target.is_dir():
        raise ValueError(f"target repository directory not found: {target}")

    inside = run_git(target, "rev-parse", "--is-inside-work-tree")
    if inside != "true":
        raise ValueError(f"target is not a Git work tree: {target}")

    head = run_git(target, "rev-parse", "--verify", "HEAD")
    current_branch = run_git(target, "branch", "--show-current")
    if not current_branch:
        raise ValueError("target repository is in detached HEAD state")

    try:
        run_git(target, "rev-parse", "--verify", expected_branch)
    except ValueError as exc:
        raise ValueError(f"expected default branch {expected_branch!r} does not exist locally: {exc}") from exc

    return {
        "initialized": True,
        "head": head,
        "current_branch": current_branch,
    }


def iter_reusable_files() -> Iterable[tuple[Path, Path]]:
    for source in sorted((SOURCE_ROOT / "web").rglob("*")):
        if source.is_file() and source.name not in IGNORED_NAMES and source.suffix not in IGNORED_SUFFIXES:
            yield source, Path("assembly/web") / source.relative_to(SOURCE_ROOT / "web")

    for name in CONTRACT_FILES:
        source = SOURCE_ROOT / "contracts" / name
        if not source.is_file():
            raise FileNotFoundError(f"missing reusable contract: {source}")
        yield source, Path("assembly/contracts") / name

    for name in PROMPT_FILES:
        source = SOURCE_ROOT / "prompts" / name
        if not source.is_file():
            raise FileNotFoundError(f"missing reusable prompt: {source}")
        yield source, Path("assembly/prompts") / name

    for name in TOOL_FILES:
        source = SOURCE_ROOT / "tools" / name
        if not source.is_file():
            raise FileNotFoundError(f"missing reusable tool: {source}")
        yield source, Path("assembly/tools") / name


def copy_reusable_kit(target: Path, *, force: bool) -> list[str]:
    installed: list[str] = []
    for source, relative_target in iter_reusable_files():
        destination = target / relative_target
        if destination.exists() and not force:
            raise FileExistsError(f"refusing to overwrite installed kit file: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        installed.append(relative_target.as_posix())
    return installed


def workspace_payload(args: argparse.Namespace) -> dict[str, Any]:
    repository_url = args.repository_url or f"https://github.com/{args.repository_full_name}"
    return {
        "schema_version": "0.2.0",
        "project_id": args.project_id,
        "name": args.name,
        "status": "draft",
        "default_view": "overview",
        "repository": {
            "provider": args.provider,
            "full_name": args.repository_full_name,
            "default_branch": args.default_branch,
            "initialized": True,
            "visibility": args.visibility,
            "web_url": repository_url,
            "implementation_root": ".",
        },
        "workflow": {
            "mode": "repository_first",
            "state_source": "merged_artifacts_and_pull_requests",
            "change_boundary": "pull_request",
            "requirements_pr": "separate",
            "planning_pr": "separate",
            "task_split_pr": "separate",
        },
        "paths": {
            "generated": {
                "project_spec": "assembly/generated/project_spec.json",
                "repo_plan": "assembly/generated/repo_plan.json",
                "task_backlog": "assembly/generated/task_backlog.json",
                "task_batch_index": "assembly/generated/task_batch_index.json",
                "task_batches_dir": "assembly/generated/task_batches",
                "collaboration_state": "assembly/generated/collaboration_state.json",
                "agent_prompts": "assembly/generated/agent_prompts.json",
                "slots_db": "assembly/generated/slots_db.json",
                "task_runs_dir": "assembly/generated/task_runs",
                "planning_runs_index": "assembly/generated/planning_runs_index.json",
            },
            "intake": {
                "dir": "assembly/intake",
                "intake_session": "assembly/intake/intake_session.json",
                "project_intake": "assembly/intake/project_intake.json",
            },
            "requirements": {
                "dir": "assembly/requirements",
                "requirements_doc": "assembly/requirements/REQUIREMENTS.md",
            },
            "planning_runs": "assembly/planning_runs",
            "context": {
                "dir": "assembly/context",
                "handoff": "assembly/context/handoff.md",
                "repo_notes": "assembly/context/repository-notes.md",
                "local_setup": "assembly/context/local-setup.md",
            },
            "prompts": "assembly/prompts",
            "contracts": "assembly/contracts",
            "viewer": "assembly/web",
            "tools": "assembly/tools",
        },
        "implementation_repos": [
            {
                "repo_id": args.project_id,
                "path": ".",
                "kind": "monorepo_path",
                "remote_url": repository_url,
                "branch": args.default_branch,
            }
        ],
        "ai_guidance": {
            "onboarding_mode": "guided_pr",
            "human_next_step": (
                "Complete guided intake and open the requirements/bootstrap pull request. "
                "Do not generate architecture or implementation tasks yet."
            ),
            "notes": [
                "Chat context is temporary; merged repository files are authoritative.",
                "Planning and task decomposition belong in later pull requests.",
            ],
        },
    }


def requirements_template(name: str) -> str:
    return f"""# {name} Requirements

Status: draft until guided intake is complete and this pull request is reviewed.

## Goal

Replace this section with the accepted project goal from guided intake.

## Target users

- Add accepted target users.

## MVP

### Must have

- Add accepted MVP requirements.

### Explicitly postponed

- Add postponed scope.

## Platforms and stack constraints

- Add accepted platform and stack decisions.

## Working style and proof

- Add task-size, review, and proof expectations.

## Safety boundaries and non-goals

- Add accepted boundaries.

## Assumptions

- Add low-risk assumptions.

## Open questions

- Keep only non-blocking questions here. Resume intake for blocking questions.

## Acceptance signals

- Add observable signals that the requirements package is ready for planning.
"""


def handoff_template(name: str) -> str:
    return f"""# {name} Handoff

## Current lifecycle phase

Repository ready; requirements/bootstrap is in progress.

## Source of truth

- `project_workspace.json`
- `assembly/intake/project_intake.json` after guided intake
- `assembly/requirements/REQUIREMENTS.md`

## Next action

Complete guided intake, review the requirements PR, merge it, then start a fresh Planning Agent context from the merged repository files.
"""


def repo_notes_template(args: argparse.Namespace) -> str:
    return f"""# Repository Notes

- Repository: `{args.repository_full_name}`
- Default branch: `{args.default_branch}`
- Project ID: `{args.project_id}`
- Workflow: repository-first
- Persistent changes: pull requests
"""


def local_setup_template() -> str:
    return """# Local Setup

Serve the repository root:

```powershell
python -m http.server 8000
```

Open the copied read-only viewer:

```text
http://localhost:8000/assembly/web/
```

Pages that depend on planning or task artifacts will remain incomplete until the corresponding PRs are merged.
"""


def kit_manifest(args: argparse.Namespace, installed_files: list[str]) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "kit_version": KIT_VERSION,
        "source_repository": "YeerooXY/ai-assembly-line",
        "source_ref": args.source_ref,
        "project_id": args.project_id,
        "managed_paths": [
            "assembly/web",
            "assembly/contracts",
            "assembly/prompts",
            "assembly/tools",
        ],
        "installed_files": sorted(installed_files),
        "project_owned_paths": [
            "project_workspace.json",
            "assembly/intake",
            "assembly/requirements",
            "assembly/planning_runs",
            "assembly/generated",
            "assembly/context",
        ],
        "upgrade_rule": (
            "Refresh managed paths from the framework in a dedicated pull request. "
            "Never overwrite project-owned planning or execution state automatically."
        ),
    }


def scaffold_product_repository(args: argparse.Namespace) -> list[str]:
    target = args.target.resolve()
    verify_git_repository(target, args.default_branch)

    existing_workspace = target / "project_workspace.json"
    if existing_workspace.exists() and not args.force:
        raise FileExistsError(
            "project_workspace.json already exists; use --check to inspect or --force for an explicit reinstall"
        )

    installed = copy_reusable_kit(target, force=args.force)
    created: list[str] = list(installed)

    for relative in (
        "assembly/intake",
        "assembly/requirements",
        "assembly/planning_runs",
        "assembly/generated/task_batches",
        "assembly/generated/task_runs",
        "assembly/context",
    ):
        (target / relative).mkdir(parents=True, exist_ok=True)

    generated_files = {
        "project_workspace.json": json.dumps(workspace_payload(args), indent=2, ensure_ascii=False) + "\n",
        "assembly/kit_manifest.json": json.dumps(
            kit_manifest(args, installed), indent=2, ensure_ascii=False
        ) + "\n",
        "assembly/requirements/REQUIREMENTS.md": requirements_template(args.name),
        "assembly/context/handoff.md": handoff_template(args.name),
        "assembly/context/repository-notes.md": repo_notes_template(args),
        "assembly/context/local-setup.md": local_setup_template(),
        "assembly/generated/task_runs/README.md": (
            "# Task Runs\n\nTask executor proof reports belong here after task decomposition.\n"
        ),
        "assembly/generated/task_batches/.gitkeep": "",
        "assembly/intake/.gitkeep": "",
        "assembly/planning_runs/.gitkeep": "",
    }

    for relative, content in generated_files.items():
        write_text(target / relative, content, force=args.force)
        created.append(relative)

    return sorted(set(created))


def check_product_repository(args: argparse.Namespace) -> list[str]:
    target = args.target.resolve()
    verify_git_repository(target, args.default_branch)

    workspace_path = target / "project_workspace.json"
    manifest_path = target / "assembly" / "kit_manifest.json"
    if not workspace_path.is_file():
        raise FileNotFoundError("missing project_workspace.json")
    if not manifest_path.is_file():
        raise FileNotFoundError("missing assembly/kit_manifest.json")

    workspace = load_json(workspace_path)
    manifest = load_json(manifest_path)

    errors: list[str] = []
    if workspace.get("project_id") != args.project_id:
        errors.append("project_workspace.json project_id does not match --project-id")
    if workspace.get("repository", {}).get("full_name") != args.repository_full_name:
        errors.append("project_workspace.json repository.full_name does not match")
    if workspace.get("workflow", {}).get("mode") != "repository_first":
        errors.append("project_workspace.json workflow.mode must be repository_first")

    for relative in manifest.get("installed_files", []):
        if not (target / relative).is_file():
            errors.append(f"missing installed kit file: {relative}")

    if errors:
        raise ValueError("; ".join(errors))

    return manifest.get("installed_files", [])


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install the reusable AI Assembly Line kit into an initialized product repository. "
            "This tool does not commit, push, or open a pull request."
        )
    )
    parser.add_argument("--target", type=Path, required=True, help="Path to the initialized product repository clone.")
    parser.add_argument("--project-id", required=True, help="Stable lowercase project slug.")
    parser.add_argument("--name", required=True, help="Human-readable project name.")
    parser.add_argument("--repository-full-name", required=True, help="Provider repository identity, e.g. owner/repo.")
    parser.add_argument("--repository-url", default="", help="Repository web URL. Defaults to GitHub URL.")
    parser.add_argument("--provider", choices=["github", "gitlab", "local_git", "other"], default="github")
    parser.add_argument("--default-branch", default="main")
    parser.add_argument("--visibility", choices=["public", "private", "internal", "unknown"], default="unknown")
    parser.add_argument("--source-ref", default="main", help="Framework ref recorded in assembly/kit_manifest.json.")
    parser.add_argument("--force", action="store_true", help="Explicitly overwrite managed/bootstrap files.")
    parser.add_argument("--check", action="store_true", help="Verify an existing installation without writing.")
    args = parser.parse_args(argv)
    validate_project_id(args.project_id)
    return args


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        if args.check:
            installed = check_product_repository(args)
            print(f"RESULT OK product_repository_ready=true installed_files={len(installed)}")
            return 0

        created = scaffold_product_repository(args)
        for path in created:
            print(f"CREATED {path}")
        print("NEXT complete guided intake on this branch, replace draft requirements, add project_intake.json, validate, then open the requirements/bootstrap PR")
        print(f"RESULT OK product_repository_bootstrapped=true files={len(created)}")
        return 0
    except Exception as exc:
        print(f"RESULT FAIL {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
