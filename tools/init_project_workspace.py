from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
REGISTRY = PROJECTS_DIR / "index.json"
PROJECT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9\-]*$")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any, *, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path.relative_to(ROOT).as_posix()} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str, *, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def validate_project_id(project_id: str) -> None:
    if PROJECT_ID_RE.fullmatch(project_id) is None:
        raise ValueError("project_id must match ^[a-z0-9][a-z0-9\\-]*$")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "new-project"


def workspace_json(project_id: str, name: str, status: str, repo_kind: str | None) -> dict[str, Any]:
    repos = []
    if repo_kind:
        repos.append({"repo_id": project_id, "path": f"repos/{project_id}", "kind": repo_kind})

    return {
        "schema_version": "0.1.0",
        "project_id": project_id,
        "name": name,
        "status": status,
        "default_view": "dispatch",
        "paths": {
            "generated": {
                "project_spec": "generated/project_spec.json",
                "repo_plan": "generated/repo_plan.json",
                "task_backlog": "generated/task_backlog.json",
                "task_batch_index": "generated/task_batch_index.json",
                "task_batches_dir": "generated/task_batches",
                "collaboration_state": "generated/collaboration_state.json",
                "agent_prompts": "generated/agent_prompts.json",
                "slots_db": "generated/slots_db.json",
                "task_runs_dir": "generated/task_runs",
                "planning_runs_index": "generated/planning_runs_index.json",
            },
            "intake": {
                "dir": "intake",
                "intake_session": "intake/intake_session.json",
                "project_intake": "intake/project_intake.json",
            },
            "planning_runs": "planning_runs",
            "context": {
                "dir": "context",
                "handoff": "context/handoff.md",
                "repo_notes": "context/repo-notes.md",
                "local_setup": "context/local-setup.md",
            },
            "prompts": "prompts",
            "repos": "repos",
        },
        "implementation_repos": repos,
        "ai_guidance": {
            "onboarding_mode": "local_initializer",
            "human_next_step": "Run guided intake, then create a planning run for this workspace.",
            "notes": [
                "Generated planning state belongs under this project's generated/ directory.",
                "Do not place project files in the root generated/ directory.",
            ],
        },
    }


def collaboration_state(project_id: str) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "workspace_id": project_id,
        "generated_from": "generated/task_backlog.json",
        "actors": [
            {
                "actor_id": "human-owner",
                "display_name": "Human Owner",
                "kind": "human",
                "status": "active",
                "notes": "Human owner/operator for manual task assignment and review.",
            },
            {
                "actor_id": "web-ai-task-executor",
                "display_name": "Web AI Task Executor",
                "kind": "web_ai",
                "status": "active",
                "notes": "Copy-paste AI executor working from one task JSON at a time.",
            },
            {
                "actor_id": "local-ai-codex",
                "display_name": "Local AI / Codex",
                "kind": "local_ai",
                "status": "active",
                "notes": "Local repo-aware implementation agent.",
            },
        ],
        "task_assignments": [],
        "task_claims": [],
        "artifact_submissions": [],
        "reviews": [],
        "audit_events": [],
    }


def task_batch_index() -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "source_plan_path": "planning_runs/<run-slug>/outputs/generated-plan.md",
        "batching_strategy": "mixed",
        "batches": [],
    }


def load_registry() -> dict[str, Any]:
    if REGISTRY.exists():
        return load_json(REGISTRY)
    return {"schema_version": "0.1.0", "default_project_id": None, "projects": []}


def update_registry(project_id: str, name: str, status: str, *, force: bool) -> None:
    registry = load_registry()
    projects = registry.setdefault("projects", [])
    entry = {
        "project_id": project_id,
        "name": name,
        "workspace_path": f"projects/{project_id}/project_workspace.json",
        "status": status,
        "default_view": "dispatch",
        "tags": ["guided"],
    }

    existing = next((item for item in projects if item.get("project_id") == project_id), None)
    if existing:
        if not force:
            raise FileExistsError(f"projects/index.json already contains {project_id}")
        existing.clear()
        existing.update(entry)
    else:
        projects.append(entry)

    if registry.get("default_project_id") is None:
        registry["default_project_id"] = project_id

    write_json(REGISTRY, registry, overwrite=True)


def create_workspace(args: argparse.Namespace) -> None:
    project_id = args.project_id or slugify(args.name)
    validate_project_id(project_id)

    root = PROJECTS_DIR / project_id
    if root.exists() and not args.force:
        raise FileExistsError(f"{root.relative_to(ROOT).as_posix()} already exists")

    for path in [
        "intake",
        "planning_runs",
        "generated/task_batches",
        "generated/task_runs",
        "context",
        "prompts",
        "repos",
    ]:
        (root / path).mkdir(parents=True, exist_ok=True)

    write_json(root / "project_workspace.json", workspace_json(project_id, args.name, args.status, args.implementation_repo_kind), overwrite=args.force)
    write_json(root / "generated" / "collaboration_state.json", collaboration_state(project_id), overwrite=args.force)
    write_json(root / "generated" / "task_batch_index.json", task_batch_index(), overwrite=args.force)
    write_json(root / "generated" / "task_backlog.json", [], overwrite=args.force)

    write_text(root / "README.md", f"# {args.name}\n\nCreated by `tools/init_project_workspace.py`. Start with guided intake, planning, task splitting, then Dispatch.\n", overwrite=args.force)
    write_text(root / "context" / "handoff.md", f"# {args.name} Handoff\n\nHuman-readable project context for task execution.\n", overwrite=args.force)
    write_text(root / "context" / "repo-notes.md", "# Repository Notes\n\nAdd implementation repo notes here.\n", overwrite=args.force)
    write_text(root / "context" / "local-setup.md", "# Local Setup\n\nAdd local setup notes here.\n", overwrite=args.force)
    write_text(root / "generated" / "task_runs" / "README.md", "# Task Runs\n\nSave per-task executor reports here as `<task_id>.json`.\n", overwrite=args.force)
    write_text(root / "generated" / "task_batches" / ".gitkeep", "", overwrite=args.force)
    write_text(root / "prompts" / ".gitkeep", "", overwrite=args.force)
    write_text(root / "repos" / ".gitkeep", "", overwrite=args.force)

    update_registry(project_id, args.name, args.status, force=args.force)
    print(f"CREATED projects/{project_id}/project_workspace.json")
    print("UPDATED projects/index.json")
    print("NEXT run: python tools\\validate_project_workspaces.py")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a guided AI Assembly Line project workspace.")
    parser.add_argument("project_id", nargs="?", help="Project id/slug, e.g. snake-game. Defaults to a slug from --name.")
    parser.add_argument("--name", required=True, help="Human-readable project name.")
    parser.add_argument("--status", choices=["draft", "active", "paused", "archived"], default="draft")
    parser.add_argument("--implementation-repo-kind", choices=["local", "submodule", "external", "monorepo_path"], default=None)
    parser.add_argument("--force", action="store_true", help="Overwrite/update existing workspace files and registry entry.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        create_workspace(parse_args(argv))
    except Exception as exc:
        print(f"RESULT FAIL {exc}")
        return 1
    print("RESULT OK project_workspace_created=true")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
