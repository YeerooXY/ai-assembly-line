from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

import validate_seed


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "generated" / "task_batch_index.json"
BATCHES_DIR = ROOT / "generated" / "task_batches"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def validate_batch_index(index: Any) -> list[str]:
    validate_seed.expect_object_keys(
        index,
        "generated/task_batch_index.json",
        {"schema_version", "source_plan_path", "batching_strategy", "batches"},
    )
    validate_seed.expect_non_empty_string(index["schema_version"], "task_batch_index.schema_version")
    validate_seed.expect_non_empty_string(index["source_plan_path"], "task_batch_index.source_plan_path")
    validate_seed.expect(
        index["batching_strategy"] in {"owner_role", "repo_target", "lane", "milestone", "mixed"},
        "task_batch_index.batching_strategy must be an allowed strategy",
    )
    validate_seed.expect_type(index["batches"], list, "task_batch_index.batches")

    batch_ids: set[str] = set()
    task_ids: set[str] = set()
    messages = ["SCHEMA OK   generated/task_batch_index.json -> contracts/task_batch_index.schema.json (builtin)"]

    for batch_index, batch in enumerate(index["batches"]):
        label = f"task_batch_index.batches[{batch_index}]"
        validate_seed.expect_object_keys(
            batch,
            label,
            {
                "batch_id",
                "owner_role",
                "repo_targets",
                "lanes",
                "milestones",
                "expected_task_count",
                "expected_task_ids",
                "depends_on_batches",
                "output_path",
                "status",
            },
            {"notes"},
        )
        validate_seed.expect_non_empty_string(batch["batch_id"], f"{label}.batch_id")
        validate_seed.expect(
            batch["batch_id"] not in batch_ids,
            f"{label}.batch_id must be unique: {batch['batch_id']}",
        )
        batch_ids.add(batch["batch_id"])
        validate_seed.expect_non_empty_string(batch["owner_role"], f"{label}.owner_role")
        validate_seed.expect_string_array(batch["repo_targets"], f"{label}.repo_targets")
        validate_seed.expect_string_array(batch["lanes"], f"{label}.lanes")
        validate_seed.expect_string_array(batch["milestones"], f"{label}.milestones")
        validate_seed.expect_type(batch["expected_task_count"], int, f"{label}.expected_task_count")
        validate_seed.expect(batch["expected_task_count"] >= 0, f"{label}.expected_task_count must be >= 0")
        validate_seed.expect_string_array(batch["expected_task_ids"], f"{label}.expected_task_ids")
        validate_seed.expect(
            len(batch["expected_task_ids"]) == batch["expected_task_count"],
            f"{label}.expected_task_ids length must match expected_task_count",
        )
        for task_id in batch["expected_task_ids"]:
            validate_seed.expect(task_id not in task_ids, f"task id appears in multiple batches: {task_id}")
            task_ids.add(task_id)
        validate_seed.expect_string_array(batch["depends_on_batches"], f"{label}.depends_on_batches")
        validate_seed.expect_non_empty_string(batch["output_path"], f"{label}.output_path")
        validate_seed.expect(
            batch["output_path"] == f"generated/task_batches/{batch['batch_id']}.json",
            f"{label}.output_path must be generated/task_batches/{batch['batch_id']}.json",
        )
        validate_seed.expect(
            batch["status"] in {"planned", "generated", "validated", "accepted", "rejected"},
            f"{label}.status must be an allowed status",
        )
        if "notes" in batch:
            validate_seed.expect_non_empty_string(batch["notes"], f"{label}.notes")

    for batch_index, batch in enumerate(index["batches"]):
        for dependency in batch["depends_on_batches"]:
            validate_seed.expect(
                dependency in batch_ids,
                f"task_batch_index.batches[{batch_index}].depends_on_batches refers to unknown batch: {dependency}",
            )

    return messages


def validate_task_batch(path: Path, payload: Any, expected_batch: dict[str, Any]) -> list[str]:
    label = rel(path)
    validate_seed.expect_object_keys(payload, label, {"schema_version", "batch_id", "source_plan_path", "tasks"})
    validate_seed.expect_non_empty_string(payload["schema_version"], f"{label}.schema_version")
    validate_seed.expect(
        payload["batch_id"] == expected_batch["batch_id"],
        f"{label}.batch_id must match task_batch_index: {expected_batch['batch_id']}",
    )
    validate_seed.expect_non_empty_string(payload["source_plan_path"], f"{label}.source_plan_path")
    validate_seed.expect_type(payload["tasks"], list, f"{label}.tasks")
    validate_seed.expect(
        len(payload["tasks"]) == expected_batch["expected_task_count"],
        f"{label}.tasks length must match expected_task_count",
    )

    expected_task_ids = set(expected_batch["expected_task_ids"])
    actual_task_ids = set()
    messages = [f"SCHEMA OK   {label} -> contracts/task_batch.schema.json (builtin)"]

    for task_index, task in enumerate(payload["tasks"]):
        task_label = f"{label}.tasks[{task_index}]"
        validate_seed.validate_task(task, task_label)
        validate_seed.expect(
            task["id"] in expected_task_ids,
            f"{task_label}.id is not listed in task_batch_index expected_task_ids: {task['id']}",
        )
        validate_seed.expect(task["id"] not in actual_task_ids, f"duplicate task id in {label}: {task['id']}")
        actual_task_ids.add(task["id"])
        messages.append(f"SCHEMA OK   {task_label} -> contracts/task.schema.json (builtin)")

    missing = expected_task_ids - actual_task_ids
    validate_seed.expect(not missing, f"{label} is missing expected task id(s): {sorted(missing)}")
    return messages


def topological_order(tasks: dict[str, dict[str, Any]]) -> list[str]:
    indegree = {task_id: 0 for task_id in tasks}
    outgoing: dict[str, list[str]] = defaultdict(list)

    for task_id, task in tasks.items():
        for dependency in task["depends_on"]:
            validate_seed.expect(
                dependency in tasks,
                f"task {task_id} depends_on unknown task id: {dependency}",
            )
            outgoing[dependency].append(task_id)
            indegree[task_id] += 1

        for blocked in task.get("blocks", []):
            validate_seed.expect(
                blocked in tasks,
                f"task {task_id} blocks unknown task id: {blocked}",
            )

    queue = deque(sorted(task_id for task_id, degree in indegree.items() if degree == 0))
    ordered: list[str] = []

    while queue:
        task_id = queue.popleft()
        ordered.append(task_id)
        for dependent in sorted(outgoing[task_id]):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                queue.append(dependent)

    validate_seed.expect(
        len(ordered) == len(tasks),
        "task dependency graph contains a cycle",
    )
    return ordered


def validate_batch_order(index: dict[str, Any], task_to_batch: dict[str, str], tasks: dict[str, dict[str, Any]]) -> list[str]:
    batch_order = {batch["batch_id"]: index for index, batch in enumerate(index["batches"])}

    for task_id, task in tasks.items():
        task_batch = task_to_batch[task_id]
        for dependency in task["depends_on"]:
            dependency_batch = task_to_batch[dependency]
            validate_seed.expect(
                batch_order[dependency_batch] <= batch_order[task_batch],
                f"batch order violation: task {task_id} depends on later batch task {dependency}",
            )

    return ["GRAPH OK    batch order respects task dependencies"]


def main() -> int:
    if not INDEX_PATH.is_file():
        print(f"MISSING FAIL {rel(INDEX_PATH)}")
        return 1

    try:
        index = load_json(INDEX_PATH)
    except Exception as exc:
        print(f"PARSE FAIL {rel(INDEX_PATH)}: {exc}")
        return 1

    failures = 0
    all_tasks: dict[str, dict[str, Any]] = {}
    task_to_batch: dict[str, str] = {}

    try:
        for message in validate_batch_index(index):
            print(message)

        expected_batches = {batch["batch_id"]: batch for batch in index["batches"]}
        for batch in index["batches"]:
            path = ROOT / batch["output_path"]
            if batch["status"] == "planned" and not path.exists():
                print(f"BATCH SKIP  {batch['batch_id']} status=planned output_missing_ok")
                continue

            validate_seed.expect(path.is_file(), f"missing task batch file: {batch['output_path']}")
            payload = load_json(path)
            for message in validate_task_batch(path, payload, batch):
                print(message)

            for task in payload["tasks"]:
                validate_seed.expect(task["id"] not in all_tasks, f"duplicate task id across batches: {task['id']}")
                all_tasks[task["id"]] = task
                task_to_batch[task["id"]] = batch["batch_id"]

        for path in sorted(BATCHES_DIR.glob("*.json")):
            batch_id = path.stem
            validate_seed.expect(batch_id in expected_batches, f"unexpected task batch file not in index: {rel(path)}")

        if all_tasks:
            ordered = topological_order(all_tasks)
            print(f"GRAPH OK    tasks_topologically_sorted={len(ordered)}")
            for message in validate_batch_order(index, task_to_batch, all_tasks):
                print(message)
        else:
            print("GRAPH OK    no generated task batches yet")

    except Exception as exc:
        failures += 1
        print(f"RESULT FAIL {exc}")

    if failures:
        return 1

    print(f"RESULT OK   batches={len(index['batches'])} tasks={len(all_tasks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
