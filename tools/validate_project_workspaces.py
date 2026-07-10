from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "projects" / "index.json"
PROJECT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9\-]*$")
STATUSES = {"draft", "active", "paused", "archived"}
VIEWS = {"overview", "planning-runs", "task-batches", "dispatch", "assignments", "verification"}
GENERATED_KEYS = {
    "project_spec",
    "repo_plan",
    "task_backlog",
    "task_batch_index",
    "task_batches_dir",
    "collaboration_state",
    "agent_prompts",
    "slots_db",
    "task_runs_dir",
}
ACTIVE_GENERATED_FILES = {
    "project_spec",
    "repo_plan",
    "task_backlog",
    "task_batch_index",
    "collaboration_state",
    "agent_prompts",
    "slots_db",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> int:
    print(f"RESULT FAIL {message}")
    return 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_project_id(value: Any, label: str) -> str:
    require(isinstance(value, str) and PROJECT_ID_RE.fullmatch(value), f"{label} must match ^[a-z0-9][a-z0-9\\-]*$")
    return value


def require_rel_path(value: Any, label: str) -> str:
    require(isinstance(value, str) and value.strip(), f"{label} must be a non-empty relative path")
    path = value.replace("\\", "/")
    parts = Path(path).parts
    require(not path.startswith("/"), f"{label} must not be absolute")
    require(not re.match(r"^[A-Za-z]:", path), f"{label} must not be drive-qualified")
    require(".." not in parts, f"{label} must not contain '..'")
    return path


def require_keys(obj: Any, label: str, required: set[str], optional: set[str] | None = None) -> dict[str, Any]:
    optional = optional or set()
    require(isinstance(obj, dict), f"{label} must be an object")
    keys = set(obj)
    missing = required - keys
    unexpected = keys - required - optional
    require(not missing, f"{label} missing required keys: {sorted(missing)}")
    require(not unexpected, f"{label} has unexpected keys: {sorted(unexpected)}")
    return obj


def validate_registry(payload: Any) -> list[dict[str, Any]]:
    registry = require_keys(payload, "projects/index.json", {"schema_version", "projects"}, {"default_project_id"})
    require(isinstance(registry["schema_version"], str) and registry["schema_version"], "registry schema_version must be non-empty")
    require(isinstance(registry["projects"], list), "registry projects must be an array")

    seen: set[str] = set()
    for index, project in enumerate(registry["projects"]):
        label = f"projects/index.json.projects[{index}]"
        entry = require_keys(project, label, {"project_id", "name", "workspace_path", "status", "default_view"}, {"description", "tags"})
        project_id = require_project_id(entry["project_id"], f"{label}.project_id")
        require(project_id not in seen, f"duplicate project_id {project_id}")
        seen.add(project_id)
        require(isinstance(entry["name"], str) and entry["name"], f"{label}.name must be non-empty")
        require(entry["status"] in STATUSES, f"{label}.status must be one of {sorted(STATUSES)}")
        require(entry["default_view"] in VIEWS, f"{label}.default_view must be one of {sorted(VIEWS)}")
        workspace_path = require_rel_path(entry["workspace_path"], f"{label}.workspace_path")
        require(workspace_path == f"projects/{project_id}/project_workspace.json", f"{label}.workspace_path must be projects/{project_id}/project_workspace.json")

    default_project_id = registry.get("default_project_id")
    if default_project_id is not None:
        require_project_id(default_project_id, "projects/index.json.default_project_id")
        require(default_project_id in seen, "default_project_id must refer to a listed project")

    return registry["projects"]


def validate_workspace(project_root: Path, payload: Any, registry_entry: dict[str, Any]) -> list[str]:
    label = registry_entry["workspace_path"]
    workspace = require_keys(payload, label, {"schema_version", "project_id", "name", "status", "default_view", "paths"}, {"description", "implementation_repos", "ai_guidance"})
    require(workspace["project_id"] == registry_entry["project_id"], f"{label}.project_id must match registry")
    require(workspace["status"] == registry_entry["status"], f"{label}.status must match registry")
    require(workspace["default_view"] in VIEWS, f"{label}.default_view must be one of {sorted(VIEWS)}")

    paths = require_keys(workspace["paths"], f"{label}.paths", {"generated", "intake", "planning_runs", "context", "prompts", "repos"})
    generated = require_keys(paths["generated"], f"{label}.paths.generated", GENERATED_KEYS, {"planning_runs_index"})
    for key, value in generated.items():
        require_rel_path(value, f"{label}.paths.generated.{key}")

    intake = require_keys(paths["intake"], f"{label}.paths.intake", {"dir", "project_intake"}, {"intake_session"})
    context = require_keys(paths["context"], f"{label}.paths.context", {"dir", "handoff"}, {"repo_notes", "local_setup"})
    for key, value in {**intake, **context, "planning_runs": paths["planning_runs"], "prompts": paths["prompts"], "repos": paths["repos"]}.items():
        require_rel_path(value, f"{label}.paths.{key}")

    warnings: list[str] = []
    required_dirs = [
        project_root / "intake",
        project_root / "planning_runs",
        project_root / "generated",
        project_root / generated["task_batches_dir"],
        project_root / generated["task_runs_dir"],
        project_root / "context",
        project_root / "prompts",
        project_root / "repos",
    ]
    for directory in required_dirs:
        require(directory.is_dir(), f"missing workspace directory: {rel(directory)}")

    for key in ACTIVE_GENERATED_FILES:
        path = project_root / generated[key]
        if workspace["status"] == "active":
            require(path.is_file(), f"active workspace missing generated file: {rel(path)}")
        elif not path.exists():
            warnings.append(f"WORKSPACE WARN draft workspace missing generated file: {rel(path)}")

    for index, repo in enumerate(workspace.get("implementation_repos", [])):
        repo_label = f"{label}.implementation_repos[{index}]"
        item = require_keys(repo, repo_label, {"repo_id", "path", "kind"}, {"remote_url", "branch"})
        require_project_id(item["repo_id"], f"{repo_label}.repo_id")
        require_rel_path(item["path"], f"{repo_label}.path")
        require(item["kind"] in {"local", "submodule", "external", "monorepo_path"}, f"{repo_label}.kind is invalid")

    return warnings


def main() -> int:
    if not REGISTRY.exists():
        return fail("missing projects/index.json")

    try:
        projects = validate_registry(load_json(REGISTRY))
    except Exception as exc:
        return fail(f"registry_invalid: {exc}")

    warnings: list[str] = []
    active = 0
    for entry in projects:
        workspace_path = ROOT / entry["workspace_path"]
        if not workspace_path.is_file():
            return fail(f"missing workspace manifest: {entry['workspace_path']}")
        try:
            warnings.extend(validate_workspace(workspace_path.parent, load_json(workspace_path), entry))
        except Exception as exc:
            return fail(f"workspace_invalid {entry['workspace_path']}: {exc}")
        active += 1 if entry["status"] == "active" else 0
        print(f"WORKSPACE OK {entry['project_id']} ({entry['status']}) -> {entry['workspace_path']}")

    for warning in warnings:
        print(warning)
    print(f"RESULT OK project_workspaces={len(projects)} active={active} warnings={len(warnings)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
