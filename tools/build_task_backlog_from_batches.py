from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import validate_task_batches
import validate_seed


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "generated" / "task_batch_index.json"
OUTPUT_PATH = ROOT / "generated" / "task_backlog.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def build_backlog(index: dict[str, Any]) -> list[dict[str, Any]]:
    validate_task_batches.validate_batch_index(index)
    validate_seed.expect(
        len(index["batches"]) > 0,
        "task_batch_index.batches is empty; refusing to overwrite generated/task_backlog.json",
    )

    all_tasks: dict[str, dict[str, Any]] = {}
    task_to_batch: dict[str, str] = {}

    for batch in index["batches"]:
        batch_path = ROOT / batch["output_path"]
        validate_seed.expect(
            batch_path.is_file(),
            f"missing task batch file: {batch['output_path']}",
        )

        payload = load_json(batch_path)
        validate_task_batches.validate_task_batch(batch_path, payload, batch)

        for task in payload["tasks"]:
            task_id = task["id"]
            validate_seed.expect(task_id not in all_tasks, f"duplicate task id across batches: {task_id}")
            all_tasks[task_id] = task
            task_to_batch[task_id] = batch["batch_id"]

    ordered_task_ids = validate_task_batches.topological_order(all_tasks)
    validate_task_batches.validate_batch_order(index, task_to_batch, all_tasks)
    return [all_tasks[task_id] for task_id in ordered_task_ids]


def main() -> int:
    if not INDEX_PATH.is_file():
        print(f"MISSING FAIL {rel(INDEX_PATH)}")
        return 1

    try:
        index = load_json(INDEX_PATH)
        backlog = build_backlog(index)
        write_json(OUTPUT_PATH, backlog)
    except Exception as exc:
        print(f"RESULT FAIL {exc}")
        return 1

    print(f"RESULT OK   wrote {rel(OUTPUT_PATH)} tasks={len(backlog)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
