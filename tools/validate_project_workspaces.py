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
GENERATED_FILE_KEYS = {
    "project_spec",
    "repo_plan",
    "task_backlog",
    "task_batch_index",
    "collaboration_state",
    "agent_prompts",
    "slots_db",
}
WORKFLOW_MODES = {"repository_first", "central_registry", "planning_only"}
STATE_SOURCES = {"merged_artifacts_and_pull_requests", "local_files", "manual"}
CHANGE_BOUNDARIES = {"pull_request", "direct_commit", "manual"}
REPO_PROVIDERS = {"github", "gitlab", "local_git", "other"}


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


def validate_repository(repository: Any, label: str) -> None:
    item = require_keys(
        repository,
        label,
        {"provider", "full_name", "default_branch", "initialized"},
        {"visibility", "web_url", "implementation_root"},
    )
    require(item["provider"] in REPO_PROVIDERS, f"{label}.provider is invalid")
    require(isinstance(item["full_name"], str) and item["full_name"], f"{label}.full_name must be non-empty")
    require(isinstance(item["default_branch"], str) and item["default_branch"], f"{label}.default_branch must be non-empty")
    require(isinstance(item["initialized"], bool), f"{label}.initialized must be boolean")
    if "implementation_root" in item:
        require_rel_path(item["implementation_root"], f"{label}.implementation_root")


def validate_workflow(workflow: Any, label: str) -> None:
    item = require_keys(
        workflow,
        label,
        {"mode", "state_source", "change_boundary"},
        {"requirements_pr", "planning_pr", "task_split_pr"},
    )
    require(item["mode"] in WORKFLOW_MODES, f"{label}.mode is invalid")
    require(item["state_source"] in STATE_SOURCES, f"{label}.state_source is invalid")
    require(item["change_boundary"] in CHANGE_BOUNDARIES, f"{label}.change_boundary is invalid")
    for key in ("requirements_pr", "planning_pr", "task_split_pr"):
        if key in item:
            require(item[key] in {"separate", "combined", "optional"}, f"{label}.{key} is invalid")


def infer_artifact_phase(project_root: Path, generated: dict[str, str], intake: dict[str, str]) -> str:
    has_intake = (project_root / intake["project_intake"]).is_file()
    has_plan = all((project_root / generated[key]).is_file() for key in ("project_spec", "repo_plan"))
    has_tasks = all((project_root / generated[key]).is_file() for key in ("task_batch_index", "task_backlog", "collaboration_state"))
    if has_tasks:
        return "execution_ready"
    if has_plan:
        return "task_splitting"
    if has_intake:
        return "planning"
    return "requirements"


def validate_workspace(project_root: Path, payload: Any, registry_entry: dict[str, Any]) -> tuple[list[str], str]:
    label = registry_entry["workspace_path"]
    workspace = require_keys(
        payload,
        label,
        {"schema_version", "project_id", "name", "status", "default_view", "paths"},
        {"description", "repository", "workflow", "implementation_repos", "ai_guidance"},
    )
    require(workspace["project_id"] == registry_entry["project_id"], f"{label}.project_id must match registry")
    require(workspace["status"] == registry_entry["status"], f"{label}.status must match registry")
    require(workspace["default_view"] in VIEWS, f"{label}.default_view must be one of {sorted(VIEWS)}")

    if "repository" in workspace:
        validate_repository(workspace["repository"], f"{label}.repository")
    if "workflow" in workspace:
        validate_workflow(workspace["workflow"], f"{label}.workflow")

    paths = require_keys(
        workspace["paths"],
        f"{label}.paths",
        {"generated", "intake", "planning_runs", "context", "prompts"},
        {"requirements", "contracts", "viewer", "tools", "repos"},
    )
    generated = require_keys(paths["generated"], f"{label}.paths.generated", GENERATED_KEYS, {"planning_runs_index"})
    for key, value in generated.items():
        require_rel_path(value, f"{label}.paths.generated.{key}")

    intake = require_keys(paths["intake"], f"{label}.paths.intake", {"dir", "project_intake"}, {"intake_session"})
    context = require_keys(paths["context"], f"{label}.paths.context", {"dir", "handoff"}, {"repo_notes", "local_setup"})
    path_values: dict[str, str] = {**intake, **context, "planning_runs": paths["planning_runs"], "prompts": paths["prompts"]}

    if "requirements" in paths:
        requirements = require_keys(paths["requirements"], f"{label}.paths.requirements", {"dir", "requirements_doc"})
        path_values.update(requirements)

    for optional_key in ("contracts", "viewer", "tools", "repos"):
        if optional_key in paths:
            path_values[optional_key] = paths[optional_key]

    for key, value in path_values.items():
        require_rel_path(value, f"{label}.paths.{key}")

    required_dirs = {
        project_root / intake["dir"],
        project_root / paths["planning_runs"],
        project_root / Path(generated["task_batches_dir"]).parent,
        project_root / generated["task_batches_dir"],
        project_root / generated["task_runs_dir"],
        project_root / context["dir"],
        project_root / paths["prompts"],
    }
    for optional_key in ("requirements", "contracts", "viewer", "tools", "repos"):
        if optional_key == "requirements" and optional_key in paths:
            required_dirs.add(project_root / paths[optional_key]["dir"])
        elif optional_key in paths:
            required_dirs.add(project_root / paths[optional_key])

    for directory in required_dirs:
        require(directory.is_dir(), f"missing workspace directory: {rel(directory)}")

    warnings: list[str] = []
    for key in GENERATED_FILE_KEYS:
        path = project_root / generated[key]
        if not path.exists():
            warnings.append(f"WORKSPACE WARN artifact not created yet: {rel(path)}")

    if (project_root / generated["task_backlog"]).is_file():
        for prerequisite in ("project_spec", "repo_plan"):
            require((project_root / generated[prerequisite]).is_file(), f"task backlog exists before prerequisite: {rel(project_root / generated[prerequisite])}")
    if (project_root / generated["collaboration_state"]).is_file():
        require((project_root / generated["task_backlog"]).is_file(), "collaboration state exists before task backlog")

    for index, repo in enumerate(workspace.get("implementation_repos", [])):
        repo_label = f"{label}.implementation_repos[{index}]"
        item = require_keys(repo, repo_label, {"repo_id", "path", "kind"}, {"remote_url", "branch"})
        require_project_id(item["repo_id"], f"{repo_label}.repo_id")
        require_rel_path(item["path"], f"{repo_label}.path")
        require(item["kind"] in {"local", "submodule", "external", "monorepo_path"}, f"{repo_label}.kind is invalid")

    return warnings, infer_artifact_phase(project_root, generated, intake)


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
            workspace_warnings, phase = validate_workspace(workspace_path.parent, load_json(workspace_path), entry)
            warnings.extend(workspace_warnings)
        except Exception as exc:
            return fail(f"workspace_invalid {entry['workspace_path']}: {exc}")
        active += 1 if entry["status"] == "active" else 0
        print(f"WORKSPACE OK {entry['project_id']} ({entry['status']}, phase={phase}) -> {entry['workspace_path']}")

    for warning in warnings:
        print(warning)
    print(f"RESULT OK project_workspaces={len(projects)} active={active} warnings={len(warnings)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
