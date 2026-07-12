from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise ValueError(detail)
    return result.stdout.strip()


def validate(root: Path) -> list[str]:
    workspace_path = root / "project_workspace.json"
    handoff_path = root / "assembly/context/CURRENT_HANDOFF.json"
    resume_path = root / "assembly/context/NEW_CHAT_RESUME.md"

    if not workspace_path.is_file():
        raise FileNotFoundError("missing project_workspace.json")
    if not handoff_path.is_file():
        raise FileNotFoundError("missing assembly/context/CURRENT_HANDOFF.json")
    if not resume_path.is_file():
        raise FileNotFoundError("missing assembly/context/NEW_CHAT_RESUME.md")

    workspace = load_json(workspace_path)
    handoff = load_json(handoff_path)
    errors: list[str] = []

    required = (
        "schema_version",
        "project_id",
        "repository",
        "lifecycle_phase",
        "active_role",
        "active_branch",
        "last_verified_commit",
        "authoritative_artifacts",
        "next_action",
        "persistence",
        "framework",
    )
    for key in required:
        if key not in handoff:
            errors.append(f"handoff missing required field: {key}")

    repository = workspace.get("repository", {}).get("full_name")
    if repository and handoff.get("repository") != repository:
        errors.append("handoff repository does not match project_workspace.json")

    project_id = workspace.get("project_id")
    if project_id and handoff.get("project_id") != project_id:
        errors.append("handoff project_id does not match project_workspace.json")

    current_branch = run_git(root, "branch", "--show-current")
    if handoff.get("active_branch") != current_branch:
        errors.append(
            f"handoff active_branch {handoff.get('active_branch')!r} does not match checked-out branch {current_branch!r}"
        )

    commit = handoff.get("last_verified_commit")
    if isinstance(commit, str) and commit:
        try:
            run_git(root, "cat-file", "-e", f"{commit}^{{commit}}")
            run_git(root, "merge-base", "--is-ancestor", commit, current_branch)
        except ValueError:
            errors.append("last_verified_commit is missing or not reachable from active branch")

    artifacts = handoff.get("authoritative_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("authoritative_artifacts must be a non-empty list")
    else:
        for relative in artifacts:
            if not isinstance(relative, str) or not relative:
                errors.append("authoritative_artifacts contains an invalid path")
            elif not (root / relative).is_file():
                errors.append(f"missing authoritative artifact: {relative}")

    if not isinstance(handoff.get("next_action"), str) or not handoff["next_action"].strip():
        errors.append("next_action must be non-empty")

    persistence = handoff.get("persistence")
    if not isinstance(persistence, dict):
        errors.append("persistence must be an object")
        unsaved = -1
    else:
        if persistence.get("status") != "ready":
            errors.append("persistence status is not ready")
        unsaved = persistence.get("unsaved_decisions")
        if not isinstance(unsaved, int) or unsaved != 0:
            errors.append("unsaved_decisions must be 0")

    framework = handoff.get("framework")
    if not isinstance(framework, dict):
        errors.append("framework must be an object")
    else:
        for key in ("repository", "installed_ref", "kit_version"):
            if not isinstance(framework.get(key), str) or not framework[key].strip():
                errors.append(f"framework.{key} must be non-empty")

    role_by_phase = {
        "bootstrap": "repository_bootstrap_agent",
        "product_discovery": "intake_interviewer",
        "planning": "planning_agent",
        "task_splitting": "task_splitter",
    }
    expected_role = role_by_phase.get(handoff.get("lifecycle_phase"))
    if expected_role and handoff.get("active_role") != expected_role:
        errors.append(
            f"active_role {handoff.get('active_role')!r} conflicts with lifecycle phase; expected {expected_role!r}"
        )

    resume = resume_path.read_text(encoding="utf-8")
    for marker in ("CURRENT_HANDOFF.json", "authoritative_artifacts", "next_action"):
        if marker not in resume:
            errors.append(f"NEW_CHAT_RESUME.md missing marker: {marker}")

    if errors:
        raise ValueError("; ".join(errors))

    return [
        "project_workspace.json",
        "assembly/context/CURRENT_HANDOFF.json",
        "assembly/context/NEW_CHAT_RESUME.md",
        *artifacts,
    ]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an AI Assembly Line context handoff.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        checked = validate(args.root.resolve())
        print(
            "RESULT OK context_handoff_ready=true "
            f"unsaved_decisions=0 files={len(set(checked))}"
        )
        return 0
    except Exception as exc:
        print(f"RESULT FAIL {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
