from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


TOOLS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_ROOT))
SPEC = importlib.util.spec_from_file_location(
    "prepare_task_context", TOOLS_ROOT / "prepare_task_context.py"
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CompletionDiscoveryTests(unittest.TestCase):
    def test_task_id_matching_is_case_insensitive_and_does_not_match_partial_ids(self) -> None:
        matches = MODULE.task_ids_from_text(
            "EH-010: Validate evidence; follow-up EH-010A is unrelated.",
            {"EH-01", "EH-010", "MT-012"},
        )

        self.assertEqual({"EH-010"}, matches)

    def test_merged_completion_evidence_unblocks_a_dependent_unclaimed_task(self) -> None:
        tasks = [
            {"id": "EH-010", "title": "Evidence review", "depends_on": []},
            {"id": "MT-012", "title": "Movement evidence", "depends_on": ["EH-010"]},
        ]
        state = {
            "actors": [],
            "task_assignments": [],
            "task_claims": [],
        }

        rows = MODULE.build_rows(
            tasks,
            state,
            {"EH-010": ["merged GitHub PR #86: EH-010: Validate evidence reviews"]},
        )
        rows_by_id = {row["id"]: row for row in rows}

        self.assertEqual("done", rows_by_id["EH-010"]["dispatch_status"])
        self.assertEqual("available", rows_by_id["MT-012"]["dispatch_status"])
        self.assertIn("merged GitHub PR #86", rows_by_id["EH-010"]["dispatch_reason"])


if __name__ == "__main__":
    unittest.main()
