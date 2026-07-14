from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from workspace_paths import WorkspacePaths, discover_workspace_paths, load_json, normalize_relative_path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "1.0.0"
LOCKED_STATUSES = {"claimed", "in_progress"}
REVIEW_STATUSES = {"review"}
DONE_STATUSES = {"done"}
BLOCKED_STATUSES = {"blocked"}
ACTIVE_CLAIM_STATUSES = {"claimed", "in_progress"}


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def non_empty_string(value: Any, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def string_list(value: Any, label: str) -> list[str]:
    if value is None:
        return []
    expect(isinstance(value, list), f"{label} must be a list")
    result: list[str] = []
    for index, item in enumerate(value):
        expect(isinstance(item, str) and item.strip(), f"{label}[{index}] must be a non-empty string")
        result.append(item)
    return result


def object_list(value: Any, label: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    expect(isinstance(value, list), f"{label} must be a list")
    result: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        expect(isinstance(item, dict), f"{label}[{index}] must be an object")
        result.append(item)
    return result


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"missing {label}: {path}")


def display_path(paths: WorkspacePaths, path: Path) -> str:
    return paths.display(path)


def configured_relative_path(workspace: dict[str, Any], *keys: str, fallback: str) -> str:
    value: Any = workspace
    for key in keys:
        if not isinstance(value, dict):
            value = None
            break
        value = value.get(key)
    return normalize_relative_path(non_empty_string(value, fallback))


def read_workspace(paths: WorkspacePaths) -> dict[str, Any]:
    if paths.manifest_path is None:
        return {}

    workspace = load_json(paths.manifest_path)
    expect(isinstance(workspace, dict), f"{paths.manifest_path} must be a JSON object")
    return workspace


def read_context_documents(paths: WorkspacePaths, workspace: dict[str, Any]) -> list[dict[str, str]]:
    if not workspace:
        return []

    candidates = (
        ("handoff", "Current handoff", ("paths", "context", "handoff")),
        ("repository_notes", "Repository notes", ("paths", "context", "repo_notes")),
        ("local_setup", "Local setup", ("paths", "context", "local_setup")),
    )
    documents: list[dict[str, str]] = []
    for document_id, title, keys in candidates:
        value: Any = workspace
        for key in keys:
            if not isinstance(value, dict):
                value = None
                break
            value = value.get(key)
        if not isinstance(value, str) or not value.strip():
            continue

        path = paths.workspace_root / normalize_relative_path(value)
        if not path.is_file():
            continue
        documents.append(
            {
                "id": document_id,
                "title": title,
                "path": display_path(paths, path),
                "content": path.read_text(encoding="utf-8").strip(),
            }
        )
    return documents


def git_value(root: Path, *arguments: str) -> tuple[str | None, bool]:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None, False
    return result.stdout.strip(), True


def git_snapshot(root: Path) -> dict[str, Any]:
    commit, commit_ok = git_value(root, "rev-parse", "--verify", "HEAD")
    branch, branch_ok = git_value(root, "branch", "--show-current")
    dirty_output, dirty_ok = git_value(root, "status", "--porcelain")
    return {
        "git_commit": commit if commit_ok else None,
        "git_branch": branch if branch_ok and branch else None,
        "is_dirty": bool(dirty_output) if dirty_ok else None,
    }


def claim_status_to_assignment_status(status: Any) -> str | None:
    if not isinstance(status, str) or not status:
        return None
    if status == "submitted":
        return "review"
    if status == "released":
        return "released"
    return status


def is_done(row: dict[str, Any]) -> bool:
    return row["execution_status"] in DONE_STATUSES or row["planning_status"] == "done"


def build_rows(tasks: list[dict[str, Any]], state: dict[str, Any]) -> list[dict[str, Any]]:
    task_map: dict[str, dict[str, Any]] = {}
    for index, task in enumerate(tasks):
        task_id = task.get("id")
        expect(isinstance(task_id, str) and task_id.strip(), f"task_backlog[{index}].id must be a non-empty string")
        expect(task_id not in task_map, f"task_backlog has duplicate task id: {task_id}")
        task_map[task_id] = task

    actors = object_list(state.get("actors"), "collaboration_state.actors")
    actor_map = {
        actor["actor_id"]: actor
        for actor in actors
        if isinstance(actor.get("actor_id"), str) and actor["actor_id"]
    }

    assignments = object_list(state.get("task_assignments"), "collaboration_state.task_assignments")
    assignment_map: dict[str, dict[str, Any]] = {}
    for assignment in assignments:
        task_id = assignment.get("task_id")
        if isinstance(task_id, str) and task_id:
            expect(task_id not in assignment_map, f"collaboration_state has duplicate assignment for {task_id}")
            assignment_map[task_id] = assignment

    claims = object_list(state.get("task_claims"), "collaboration_state.task_claims")
    claim_map: dict[str, dict[str, Any]] = {}
    for claim in claims:
        task_id = claim.get("task_id")
        if isinstance(task_id, str) and task_id and claim.get("status") in ACTIVE_CLAIM_STATUSES:
            claim_map[task_id] = claim

    raw_rows: list[dict[str, Any]] = []
    for task in tasks:
        task_id = task["id"]
        assignment = assignment_map.get(task_id)
        active_claim = claim_map.get(task_id)
        assigned_actor_id = (
            assignment.get("assigned_to") if assignment else None
        ) or (active_claim.get("actor_id") if active_claim else None)
        actor = actor_map.get(assigned_actor_id) if isinstance(assigned_actor_id, str) else None
        dependencies = string_list(task.get("depends_on"), f"task_backlog[{task_id}].depends_on")
        proof = object_list(assignment.get("proof") if assignment else [], f"assignment[{task_id}].proof")
        updated_at = (
            assignment.get("updated_at") if assignment else None
        ) or (active_claim.get("claimed_at") if active_claim else None) or (
            active_claim.get("released_at") if active_claim else None
        )

        raw_rows.append(
            {
                "task": task,
                "assignment": assignment,
                "active_claim": active_claim,
                "actor": actor,
                "id": task_id,
                "title": non_empty_string(task.get("title"), task_id),
                "summary": non_empty_string(task.get("summary"), ""),
                "planning_status": non_empty_string(task.get("status"), "not set"),
                "execution_status": non_empty_string(
                    assignment.get("status") if assignment else claim_status_to_assignment_status(active_claim.get("status") if active_claim else None),
                    "unclaimed",
                ),
                "assigned_to": non_empty_string(
                    actor.get("display_name") if actor else (assignment.get("assignee_label") if assignment else assigned_actor_id),
                    "Unassigned",
                ),
                "assignee_type": non_empty_string(
                    assignment.get("assignee_type") if assignment else (actor.get("kind") if actor else None),
                    "unassigned",
                ),
                "depends_on": dependencies,
                "proof": proof,
                "notes": non_empty_string(
                    assignment.get("notes") if assignment else (active_claim.get("notes") if active_claim else None),
                    "",
                ),
                "updated_at": updated_at if isinstance(updated_at, str) and updated_at else None,
            }
        )

    rows_by_id = {row["id"]: row for row in raw_rows}
    rows: list[dict[str, Any]] = []
    for row in raw_rows:
        missing_dependencies = [dependency_id for dependency_id in row["depends_on"] if dependency_id not in task_map]
        dependency_rows = [rows_by_id[dependency_id] for dependency_id in row["depends_on"] if dependency_id in rows_by_id]
        blocked_dependencies = [
            dependency for dependency in dependency_rows if dependency["execution_status"] in BLOCKED_STATUSES
        ]
        unfinished_dependencies = [dependency for dependency in dependency_rows if not is_done(dependency)]

        dispatch_status = "available"
        dispatch_reason = "All dependencies are done and the task is free to take."
        if is_done(row):
            dispatch_status = "done"
            dispatch_reason = "Done. Review proof before using this as dependency context."
        elif row["execution_status"] in BLOCKED_STATUSES or missing_dependencies or blocked_dependencies:
            dispatch_status = "blocked"
            if missing_dependencies:
                dispatch_reason = f"Missing dependency reference(s): {', '.join(missing_dependencies)}."
            elif blocked_dependencies:
                dispatch_reason = "Blocked by dependency task(s): " + ", ".join(
                    dependency["id"] for dependency in blocked_dependencies
                ) + "."
            else:
                dispatch_reason = f"Blocked: {row['notes']}" if row["notes"] else "Task is explicitly blocked."
        elif row["execution_status"] in LOCKED_STATUSES:
            dispatch_status = "locked"
            dispatch_reason = f"Locked by {row['assigned_to']} ({row['execution_status']})."
        elif row["execution_status"] in REVIEW_STATUSES:
            dispatch_status = "waiting"
            dispatch_reason = "In review; wait for proof acceptance before taking follow-up work."
        elif unfinished_dependencies:
            dispatch_status = "waiting"
            dispatch_reason = "Waiting for dependency task(s): " + ", ".join(
                dependency["id"] for dependency in unfinished_dependencies
            ) + "."

        rows.append(
            {
                **row,
                "dependency_rows": dependency_rows,
                "missing_dependencies": missing_dependencies,
                "blocked_dependencies": blocked_dependencies,
                "unfinished_dependencies": unfinished_dependencies,
                "dispatch_status": dispatch_status,
                "dispatch_reason": dispatch_reason,
            }
        )
    classified_rows_by_id = {row["id"]: row for row in rows}
    for row in rows:
        dependency_rows = [
            classified_rows_by_id[dependency_id]
            for dependency_id in row["depends_on"]
            if dependency_id in classified_rows_by_id
        ]
        row["dependency_rows"] = dependency_rows
        row["blocked_dependencies"] = [
            dependency for dependency in dependency_rows if dependency["execution_status"] in BLOCKED_STATUSES
        ]
        row["unfinished_dependencies"] = [dependency for dependency in dependency_rows if not is_done(dependency)]
    return rows


def build_assignee(row: dict[str, Any]) -> dict[str, Any] | None:
    actor = row["actor"]
    if isinstance(actor, dict):
        return {
            "actor_id": actor.get("actor_id"),
            "display_name": row["assigned_to"],
            "kind": row["assignee_type"],
        }

    assignment = row["assignment"] or {}
    active_claim = row["active_claim"] or {}
    actor_id = assignment.get("assigned_to") or active_claim.get("actor_id")
    if isinstance(actor_id, str) and actor_id:
        return {
            "actor_id": actor_id,
            "display_name": row["assigned_to"],
            "kind": row["assignee_type"],
        }
    return None


def return_template(task_id: str) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "task_id": task_id,
        "run_id": "<unique-run-id>",
        "actor_id": "<your-actor-id>",
        "status": "review",
        "implementation_summary": "<what changed>",
        "files_changed": [],
        "verification": [],
        "proof": [],
        "blockers": [],
        "notes": "<optional notes>",
        "updated_at": "<ISO-8601 timestamp>",
    }


def executor_payload(task_id: str, instructions_path: str, schema_path: str, task_runs_prefix: str, target: str) -> dict[str, Any]:
    environment_guidance: list[str] = []
    if target == "web_ai":
        environment_guidance = [
            "For GitHub and pull-request work, use the built-in GitHub connector authenticated for this repository.",
            "Do not block on the absence of a separate local checkout or the gh CLI when the connector already provides repository access.",
        ]

    return {
        "target": target,
        "instructions_path": instructions_path,
        "task_run_schema_path": schema_path,
        "expected_task_run_path": f"{task_runs_prefix}{task_id}.json",
        "hard_rules": [
            "Work only on the selected task.",
            "Do not broaden scope.",
            "Respect dependencies, allowed files, outputs, non-goals, and verification.",
            "Do not mark done without accepted proof.",
            "If required context is missing, return blocked with a clear blocker.",
            "Return one task_run JSON object only.",
        ],
        "environment_guidance": environment_guidance,
        "return_status_guidance": {
            "review": "Use status review when implementation appears complete but still needs human review.",
            "blocked": "Use status blocked if required context or dependencies are missing.",
        },
        "return_template": return_template(task_id),
    }


def dependency_payload(dependency: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_id": dependency["id"],
        "title": dependency["title"],
        "dispatch_status": dependency["dispatch_status"],
        "execution_status": dependency["execution_status"],
        "reason": dependency["dispatch_reason"],
        "proof": dependency["proof"],
    }


def context_payload(row: dict[str, Any], instructions_path: str, schema_path: str, task_runs_prefix: str, target: str) -> dict[str, Any]:
    return {
        "task_id": row["id"],
        "title": row["title"],
        "summary": row["summary"],
        "task": row["task"],
        "dispatch": {
            "status": row["dispatch_status"],
            "reason": row["dispatch_reason"],
            "planning_status": row["planning_status"],
            "execution_status": row["execution_status"],
            "assignment": row["assignment"] or {"task_id": row["id"], "status": "unclaimed"},
            "active_claim": row["active_claim"],
            "assignee": build_assignee(row),
            "updated_at": row["updated_at"],
            "dependencies": [dependency_payload(dependency) for dependency in row["dependency_rows"]],
            "missing_dependency_ids": row["missing_dependencies"],
            "blocked_dependency_ids": [dependency["id"] for dependency in row["blocked_dependencies"]],
            "unfinished_dependency_ids": [dependency["id"] for dependency in row["unfinished_dependencies"]],
        },
        "executor": executor_payload(row["id"], instructions_path, schema_path, task_runs_prefix, target),
    }


def normalized_timestamp(raw: str | None) -> str:
    if raw is None:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("--generated-at must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError("--generated-at must include a timezone")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def build_collection(paths: WorkspacePaths, args: argparse.Namespace) -> dict[str, Any]:
    require_file(paths.task_backlog, "task backlog")
    require_file(paths.collaboration_state, "collaboration state")
    workspace = read_workspace(paths)
    tasks = load_json(paths.task_backlog)
    state = load_json(paths.collaboration_state)
    expect(isinstance(tasks, list), f"{paths.task_backlog} must be a JSON array")
    expect(isinstance(state, dict), f"{paths.collaboration_state} must be a JSON object")
    task_rows = build_rows(object_list(tasks, "task_backlog"), state)
    rows_by_id = {row["id"]: row for row in task_rows}

    prompts_dir = configured_relative_path(workspace, "paths", "prompts", fallback="prompts")
    contracts_dir = configured_relative_path(workspace, "paths", "contracts", fallback="contracts")
    task_runs_dir = configured_relative_path(
        workspace,
        "paths",
        "generated",
        "task_runs_dir",
        fallback="generated/task_runs",
    )
    prompt_path = paths.workspace_root / prompts_dir / "07-task-executor.md"
    task_run_schema_path = paths.workspace_root / contracts_dir / "task_run.schema.json"
    require_file(prompt_path, "task executor prompt")
    require_file(task_run_schema_path, "task run schema")

    if args.task_id:
        expect(args.task_id in rows_by_id, f"task not found in backlog: {args.task_id}")
        selected_rows = [rows_by_id[args.task_id]]
        selection_mode = "task_id"
        requested_task_id: str | None = args.task_id
    elif args.all_tasks:
        selected_rows = task_rows
        selection_mode = "all"
        requested_task_id = None
    else:
        selected_rows = [row for row in task_rows if row["dispatch_status"] == "available"]
        selection_mode = "ready"
        requested_task_id = None

    task_runs_prefix = f"{task_runs_dir.rstrip('/')}/"
    project_id = non_empty_string(workspace.get("project_id"), non_empty_string(state.get("workspace_id"), "root"))
    project_name = non_empty_string(workspace.get("name"), "Root Generated State")
    context_documents = read_context_documents(paths, workspace)
    source_artifacts = [
        {
            "id": "task_backlog",
            "path": display_path(paths, paths.task_backlog),
            "format": "json",
            "description": "Canonical task definitions.",
        },
        {
            "id": "collaboration_state",
            "path": display_path(paths, paths.collaboration_state),
            "format": "json",
            "description": "Current assignment, claim, review, and proof state.",
        },
        {
            "id": "task_executor_prompt",
            "path": display_path(paths, prompt_path),
            "format": "markdown",
            "description": "Task-executor operating rules.",
        },
        {
            "id": "task_run_schema",
            "path": display_path(paths, task_run_schema_path),
            "format": "json",
            "description": "Required task-run return contract.",
        },
    ]
    source_artifacts.extend(
        {
            "id": document["id"],
            "path": document["path"],
            "format": "markdown",
            "description": document["title"],
        }
        for document in context_documents
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "kind": "task_execution_context_collection",
        "generated_at": normalized_timestamp(args.generated_at),
        "selection": {
            "mode": selection_mode,
            "requested_task_id": requested_task_id,
            "source_task_count": len(task_rows),
            "included_context_count": len(selected_rows),
        },
        "workspace": {
            "mode": "project" if paths.manifest_path is not None else "root",
            "project_id": project_id,
            "project_name": project_name,
            "workspace_root": ".",
            "task_run_path_prefix": task_runs_prefix,
        },
        "snapshot": git_snapshot(paths.workspace_root),
        "source_artifacts": source_artifacts,
        "workspace_context": context_documents,
        "contexts": [
            context_payload(
                row,
                display_path(paths, prompt_path),
                display_path(paths, task_run_schema_path),
                task_runs_prefix,
                "web_ai" if args.web_agent else "unspecified",
            )
            for row in selected_rows
        ],
    }


def validate_collection_builtin(payload: Any) -> None:
    expect(isinstance(payload, dict), "task context payload must be an object")
    required = {
        "schema_version",
        "kind",
        "generated_at",
        "selection",
        "workspace",
        "snapshot",
        "source_artifacts",
        "workspace_context",
        "contexts",
    }
    expect(set(payload) == required, "task context payload has unexpected or missing top-level fields")
    expect(payload["schema_version"] == SCHEMA_VERSION, "task context schema version is invalid")
    expect(payload["kind"] == "task_execution_context_collection", "task context kind is invalid")
    expect(isinstance(payload["contexts"], list), "task context contexts must be a list")
    expect(
        payload["selection"].get("included_context_count") == len(payload["contexts"]),
        "task context included_context_count does not match contexts",
    )
    for index, context in enumerate(payload["contexts"]):
        expect(isinstance(context, dict), f"contexts[{index}] must be an object")
        expect(context.get("task_id") == context.get("task", {}).get("id"), f"contexts[{index}] task id does not match task")
        dispatch = context.get("dispatch")
        expect(isinstance(dispatch, dict), f"contexts[{index}].dispatch must be an object")
        expect(dispatch.get("status") in {"available", "waiting", "locked", "blocked", "done"}, f"contexts[{index}] has invalid dispatch status")
        executor = context.get("executor")
        expect(isinstance(executor, dict), f"contexts[{index}].executor must be an object")
        expect(executor.get("expected_task_run_path", "").endswith(f"{context['task_id']}.json"), f"contexts[{index}] task-run path is invalid")


def validate_collection(payload: dict[str, Any]) -> None:
    validate_collection_builtin(payload)
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return

    schema_path = ROOT / "contracts" / "task_execution_context.schema.json"
    require_file(schema_path, "task execution context schema")
    jsonschema.validate(instance=payload, schema=load_json(schema_path))


def proof_summary(proof_items: list[dict[str, Any]]) -> str:
    if not proof_items:
        return "no proof recorded"
    parts: list[str] = []
    for item in proof_items:
        bits = [item.get("kind"), item.get("status"), item.get("path"), item.get("summary")]
        parts.append(" / ".join(str(bit) for bit in bits if isinstance(bit, str) and bit))
    return "; ".join(part or "proof" for part in parts)


def format_context_documents(documents: list[dict[str, str]]) -> str:
    if not documents:
        return ""
    parts = ["## Workspace Context", ""]
    for document in documents:
        parts.extend(
            [
                f"### {document['title']}",
                f"Source: `{document['path']}`",
                "",
                document["content"] or "(empty)",
                "",
            ]
        )
    return "\n".join(parts).strip()


def format_context_markdown(collection: dict[str, Any], context: dict[str, Any]) -> str:
    workspace = collection["workspace"]
    dispatch = context["dispatch"]
    executor = context["executor"]
    dependencies = dispatch["dependencies"]
    dependency_summary = (
        "\n".join(
            "\n".join(
                [
                    f"- {dependency['task_id']}: {dependency['dispatch_status']}",
                    f"  title: {dependency['title']}",
                    f"  execution_status: {dependency['execution_status']}",
                    f"  reason: {dependency['reason']}",
                    f"  proof: {proof_summary(dependency['proof'])}",
                ]
            )
            for dependency in dependencies
        )
        if dependencies
        else "- No dependencies."
    )
    missing_summary = (
        f"\nMissing dependency reference(s): {', '.join(dispatch['missing_dependency_ids'])}"
        if dispatch["missing_dependency_ids"]
        else ""
    )
    proof_summaries = (
        "\n".join(
            f"- {dependency['task_id']}: {proof_summary(dependency['proof'])}" for dependency in dependencies
        )
        if dependencies
        else "- No dependency proof required."
    )
    environment_guidance = ""
    if executor["environment_guidance"]:
        environment_guidance = "\n\n## Environment Guidance\n\n" + "\n".join(
            f"- {guidance}" for guidance in executor["environment_guidance"]
        )
    documents = format_context_documents(collection["workspace_context"])
    documents_section = f"\n\n{documents}" if documents else ""
    snapshot = collection["snapshot"]
    snapshot_line = "Git snapshot: unavailable."
    if snapshot["git_commit"]:
        branch = snapshot["git_branch"] or "detached HEAD"
        dirty = "dirty" if snapshot["is_dirty"] else "clean"
        snapshot_line = f"Git snapshot: {snapshot['git_commit']} on {branch} ({dirty})."

    return f"""--- CONTEXT {context['task_id']} START ---

# AI Assembly Line - One Task Execution Context

You are executing exactly one task from the AI Assembly Line backlog.

Project: {workspace['project_name']}
Project ID: {workspace['project_id']}
Workspace: {workspace['workspace_root']}
{snapshot_line}

Use the task executor rules from:
{executor['instructions_path']}

Hard rules:
{chr(10).join(f'- {rule}' for rule in executor['hard_rules'])}

Expected output path:
{executor['expected_task_run_path']}

Dispatch status: {dispatch['status']}
Reason: {dispatch['reason']}
Assigned to: {(dispatch['assignee'] or {}).get('display_name', 'Unassigned')} ({(dispatch['assignee'] or {}).get('kind', 'unassigned')})
Updated at: {dispatch['updated_at'] or 'not recorded'}{documents_section}{environment_guidance}

## Selected Task JSON

```json
{json.dumps(context['task'], indent=2, ensure_ascii=False)}
```

## Current Assignment Metadata

```json
{json.dumps(dispatch['assignment'], indent=2, ensure_ascii=False)}
```

## Active Claim Metadata

```json
{json.dumps(dispatch['active_claim'] or {'task_id': context['task_id'], 'status': 'none'}, indent=2, ensure_ascii=False)}
```

## Dependency Summary

{dependency_summary}{missing_summary}

## Dependency Proof Summaries

{proof_summaries}

## Required Return Shape

Return exactly one JSON object compatible with `{executor['task_run_schema_path']}`:

```json
{json.dumps(executor['return_template'], indent=2, ensure_ascii=False)}
```

{executor['return_status_guidance']['review']}
{executor['return_status_guidance']['blocked']}
Do not mark done without accepted proof.

--- CONTEXT {context['task_id']} END ---
"""


def format_markdown(collection: dict[str, Any]) -> str:
    contexts = collection["contexts"]
    if not contexts:
        selection = collection["selection"]
        return (
            "# AI Assembly Line - Task Contexts\n\n"
            f"No tasks matched the {selection['mode']} selection.\n"
        )
    return "\n".join(format_context_markdown(collection, context).rstrip() for context in contexts) + "\n"


def write_output(path: Path, content: str) -> None:
    target = path.expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(content)
            temporary_path = Path(handle.name)
        os.replace(temporary_path, target)
        temporary_path = None
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build read-only, one-task execution context from an AI Assembly Line backlog. "
            "Markdown is for agents; JSON is a stable source for a future UI."
        )
    )
    selector = parser.add_mutually_exclusive_group()
    selector.add_argument("--task-id", help="Build context for one task, including its current dispatch state.")
    selector.add_argument("--ready", action="store_true", help="Build context for every currently available task (the default).")
    selector.add_argument("--all", dest="all_tasks", action="store_true", help="Build context for every backlog task.")
    parser.add_argument(
        "--workspace",
        help="Optional path to project_workspace.json. Defaults to workspace discovery from the installed tool.",
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, help="Optional output file. The file is atomically replaced.")
    parser.add_argument(
        "--generated-at",
        help="Optional ISO-8601 timestamp for a reproducible JSON snapshot; defaults to the current UTC time.",
    )
    parser.add_argument(
        "--web-agent",
        action="store_true",
        help="Add GitHub-connector guidance for a browser/web AI executor.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        paths = discover_workspace_paths(ROOT, args.workspace)
        collection = build_collection(paths, args)
        validate_collection(collection)
        content = (
            json.dumps(collection, indent=2, ensure_ascii=False) + "\n"
            if args.format == "json"
            else format_markdown(collection)
        )
        if args.output:
            write_output(args.output, content)
            print(
                "RESULT OK "
                f"task_contexts={collection['selection']['included_context_count']} "
                f"format={args.format} output={args.output}",
                file=sys.stderr,
            )
        else:
            sys.stdout.write(content)
        return 0
    except Exception as exc:
        print(f"RESULT FAIL {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
