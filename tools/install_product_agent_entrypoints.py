from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def verify_product_repository(target: Path) -> dict[str, Any]:
    if not target.is_dir():
        raise ValueError(f"target repository directory not found: {target}")
    if run_git(target, "rev-parse", "--is-inside-work-tree") != "true":
        raise ValueError(f"target is not a Git work tree: {target}")
    run_git(target, "rev-parse", "--verify", "HEAD")

    workspace_path = target / "project_workspace.json"
    if not workspace_path.is_file():
        raise FileNotFoundError("missing project_workspace.json; run bootstrap_product_repository.py first")

    workspace = load_json(workspace_path)
    project_id = workspace.get("project_id")
    name = workspace.get("name")
    if not isinstance(project_id, str) or not project_id:
        raise ValueError("project_workspace.json is missing project_id")
    if not isinstance(name, str) or not name:
        raise ValueError("project_workspace.json is missing name")

    required_prompts = (
        "assembly/prompts/00-intake-interviewer.md",
        "assembly/prompts/00-planning-agent.md",
        "assembly/prompts/06-task-splitter.md",
        "assembly/prompts/07-task-executor.md",
    )
    for relative in required_prompts:
        if not (target / relative).is_file():
            raise FileNotFoundError(f"missing installed lifecycle prompt: {relative}")

    return workspace


def agents_content(workspace: dict[str, Any]) -> str:
    name = workspace["name"]
    return f"""# {name} AI Agent Contract

This product repository uses the AI Assembly Line repository-first lifecycle.

## Select the role from committed artifacts

Before responding, inspect:

- `project_workspace.json`
- `assembly/intake/project_intake.json`
- `assembly/requirements/REQUIREMENTS.md`
- `assembly/generated/project_spec.json`
- `assembly/generated/repo_plan.json`
- `assembly/generated/task_backlog.json`
- relevant pull-request state when available

Then route:

- no accepted `project_intake.json`: read `assembly/prompts/00-intake-interviewer.md`
- requirements accepted, no planning package: read `assembly/prompts/00-planning-agent.md`
- planning accepted, no canonical backlog: read `assembly/prompts/06-task-splitter.md`
- backlog accepted: use Dispatch or `assembly/prompts/07-task-executor.md`

## Intake hard stop

While intake is incomplete, ask exactly one high-impact question per turn and stop after it.

Do not turn a rough idea into a complete MVP, feature list, stack, architecture, repository layout, or task plan. Record only answers the user actually supplied. Do not silently choose recommendations.

A normal intake response contains only:

1. a brief acknowledgement or record of the last answer
2. compact status showing known facts and the current missing decision
3. exactly one next question or decision card

Then stop.

## Durable state

Chat is temporary. Git is durable. Pull requests are the approval boundary. Merged files are authoritative.

Do not claim a lifecycle stage is complete without reading the corresponding committed artifacts or PR state.

Before every repository write, inspect the active branch's pull-request state
and compare it with the current default branch. A merged branch is permanently
closed; continue from a fresh branch based on current default. Use local Git only
after verifying a checkout and tools. Pretty-print generated JSON, commit related
state files atomically, and report validation only when the repository validator
actually ran.
"""


def copilot_content(workspace: dict[str, Any]) -> str:
    return f"""# {workspace['name']} Copilot Instructions

Read `AGENTS.md` and `assembly/docs/AI_START_HERE.md` before responding.

Use committed artifacts to select the active AI Assembly Line role. While `assembly/intake/project_intake.json` is missing or incomplete, follow `assembly/prompts/00-intake-interviewer.md`, ask exactly one question per turn, and stop after the question.

Do not invent the complete MVP, features, stack, architecture, repository layout, or tasks from a rough idea.
"""


def start_here_content(workspace: dict[str, Any]) -> str:
    return f"""# {workspace['name']} AI Start Here

This is a bootstrapped AI Assembly Line product repository.

## Read state before answering

1. Read `project_workspace.json`.
2. Check which accepted artifacts exist.
3. Activate the role that owns the next missing artifact.
4. Read the complete role prompt before replying.

## Lifecycle routing

| Accepted state | Active role |
|---|---|
| No `assembly/intake/project_intake.json` | Intake Interviewer |
| Intake/requirements accepted, no project spec/repo plan | Planning Agent |
| Planning package accepted, no task backlog | Task Splitter |
| Task backlog accepted | Dispatch / Task Executor |

## Intake response lock

When intake is incomplete, read `assembly/prompts/00-intake-interviewer.md` and ask exactly one high-impact question per turn.

Do not output a complete MVP, game loop, feature inventory, stack, architecture, repository layout, or tasks. Stop immediately after the one question.

## Repository handoff

Requirements, planning, and task decomposition belong in separate reviewable pull requests. A fresh tab reloads context from merged files rather than relying on old chat history.
"""


def expected_files(workspace: dict[str, Any]) -> dict[Path, str]:
    return {
        Path("AGENTS.md"): agents_content(workspace),
        Path(".github/copilot-instructions.md"): copilot_content(workspace),
        Path("assembly/docs/AI_START_HERE.md"): start_here_content(workspace),
    }


def install(target: Path, workspace: dict[str, Any], *, force: bool) -> list[str]:
    created: list[str] = []
    for relative, content in expected_files(workspace).items():
        destination = target / relative
        if destination.exists() and not force:
            raise FileExistsError(f"refusing to overwrite existing file: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        created.append(relative.as_posix())
    return created


def check(target: Path, workspace: dict[str, Any]) -> list[str]:
    markers_by_path = {
        Path("AGENTS.md"): (
            "ask exactly one",
            "Then stop",
            "Chat is temporary",
            "merged branch is permanently",
        ),
        Path(".github/copilot-instructions.md"): (
            "ask exactly one question per turn",
            "stop after the question",
            "Do not invent the complete MVP",
        ),
        Path("assembly/docs/AI_START_HERE.md"): (
            "ask exactly one high-impact question per turn",
            "Stop immediately after the one question",
            "A fresh tab reloads context",
        ),
    }

    errors: list[str] = []
    checked: list[str] = []
    for relative, expected in expected_files(workspace).items():
        path = target / relative
        if not path.is_file():
            errors.append(f"missing product AI entrypoint: {relative.as_posix()}")
            continue
        actual = path.read_text(encoding="utf-8")
        for marker in markers_by_path[relative]:
            if marker not in actual:
                errors.append(f"{relative.as_posix()} missing marker: {marker}")
        if relative == Path("AGENTS.md") and workspace["name"] not in actual:
            errors.append("AGENTS.md does not match project name")
        checked.append(relative.as_posix())

    if errors:
        raise ValueError("; ".join(errors))
    return checked


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install or verify AI lifecycle entrypoints in a bootstrapped product repository."
    )
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        target = args.target.resolve()
        workspace = verify_product_repository(target)
        if args.check:
            checked = check(target, workspace)
            print(f"RESULT OK product_agent_entrypoints_ready=true files={len(checked)}")
            return 0

        created = install(target, workspace, force=args.force)
        for path in created:
            print(f"CREATED {path}")
        print(f"RESULT OK product_agent_entrypoints_installed=true files={len(created)}")
        return 0
    except Exception as exc:
        print(f"RESULT FAIL {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
