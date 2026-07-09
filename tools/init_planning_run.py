from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANNING_RUNS_DIR = ROOT / "planning_runs"
REQUIRED_OUTPUTS = [
    "project_spec.json",
    "repo_plan.json",
    "task_backlog.json",
    "agent_prompts.json",
    "slots_db.json",
]


def usage() -> int:
    print("Usage: python tools/init_planning_run.py <run-slug>")
    return 1


def validate_slug(run_slug: str) -> None:
    if re.fullmatch(r"[a-z0-9][a-z0-9\\-]*", run_slug) is None:
        raise ValueError("run-slug must match ^[a-z0-9][a-z0-9\\-]*$")


def default_input_idea() -> str:
    return (
        "# Input Idea\n\n"
        "Replace this text with the rough software idea for the planning run.\n"
        "Describe the product, target users, constraints, and any known safety concerns.\n"
    ).strip()


def planning_prompt(run_slug: str, input_idea: str) -> str:
    output_list = "\n".join(f"- `{name}`" for name in REQUIRED_OUTPUTS)
    return f"""# Planning Run Prompt

You are producing a manual planning run for the `ai-assembly-line` workflow.

## Run Slug

`{run_slug}`

## Goal

Convert the rough software idea below into a safe, structured planning artifact set.

Generated outputs are drafts until a human accepts them.
If the idea implies unsafe automation, botting, account control, live-service interference, or other unsafe behavior, safely reinterpret it into the nearest safe planning-only scope or explicitly reject the unsafe parts.

## Rough Idea

{input_idea}

## Required Output Files

Return exactly these artifact types:

{output_list}

## Output Requirements

- `project_spec.json` must describe the product summary, boundaries, repo split, domain model, frontend screens, backend services, core engine responsibilities, verification tasks, and starter prompts.
- `repo_plan.json` must define the repo ownership split.
- `task_backlog.json` must define tasks with owners, dependencies, acceptance criteria, and verification.
- `agent_prompts.json` must define prompt boundaries tied to the repo split.
- `slots_db.json` must define role slots and verification requirements.

## Constraints

- Produce planning artifacts only.
- Do not implement software.
- Do not add hidden workflow state.
- Keep outputs human-reviewable and machine-readable.
- Keep repo targets, task dependencies, prompts, and slots internally consistent.

## Response Format

Return each file in its own fenced code block with the filename immediately above the fence, for example:

`project_spec.json`
```json
{{ ... }}
```

Use valid JSON for all five files.
"""


def review_template() -> str:
    return """# Review

## Outcome

- [ ] Accepted
- [ ] Needs revision
- [ ] Rejected

## Review Notes

- Safety interpretation:
- Structural validity:
- Repo/task/prompt/slot coherence:
- Reviewer decision rationale:
"""


def outputs_readme() -> str:
    expected = "\n".join(f"- `{name}`" for name in REQUIRED_OUTPUTS)
    return f"""# Outputs

Save the AI-returned planning artifacts for this run in this folder.

Expected files:

{expected}

Validate them with:

```powershell
python tools\\validate_planning_run.py <path-to-this-folder>
```
"""


def write_if_missing(path: Path, content: str) -> str:
    if path.exists():
        return "exists"
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return "created"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return usage()

    run_slug = argv[1]
    try:
        validate_slug(run_slug)
    except ValueError as exc:
        print(f"ERROR {exc}")
        return 1

    run_dir = PLANNING_RUNS_DIR / run_slug
    outputs_dir = run_dir / "outputs"
    run_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    input_idea_path = run_dir / "input-idea.md"
    input_status = write_if_missing(input_idea_path, default_input_idea())
    input_idea = input_idea_path.read_text(encoding="utf-8").strip()

    planning_prompt_path = run_dir / "planning-run.md"
    planning_prompt_path.write_text(planning_prompt(run_slug, input_idea).rstrip() + "\n", encoding="utf-8")

    review_status = write_if_missing(run_dir / "review-notes.md", review_template())
    outputs_status = write_if_missing(outputs_dir / "README.md", outputs_readme())

    print(f"RUN DIR   {run_dir.relative_to(ROOT).as_posix()}")
    print(f"INPUT     {input_status} {input_idea_path.relative_to(ROOT).as_posix()}")
    print(f"PROMPT    updated {planning_prompt_path.relative_to(ROOT).as_posix()}")
    print(f"REVIEW    {review_status} {run_dir.joinpath('review-notes.md').relative_to(ROOT).as_posix()}")
    print(f"OUTPUTS   {outputs_status} {outputs_dir.joinpath('README.md').relative_to(ROOT).as_posix()}")
    print("NEXT      edit input-idea.md, rerun this script, paste planning-run.md into a web AI, save outputs/, validate, and review")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
