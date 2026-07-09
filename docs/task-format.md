# Task Format

Each generated task should be small, testable, and traceable.

## Required Fields

- `id`
- `title`
- `summary`
- `owner_role`
- `repo_target`
- `depends_on`
- `inputs`
- `outputs`
- `acceptance_criteria`
- `verification`

## Optional Fields

- `status`
- `priority`
- `milestone`
- `lane`
- `allowed_areas`
- `blocks`
- `objective`
- `context`
- `implementation_notes`
- `proof_required`
- `edge_cases`
- `non_goals`
- `estimated_size`
- `risk_tags`
- `notes`
- `handoff_notes`

## Rules

- Use stable identifiers.
- Keep tasks implementation-sized.
- Make acceptance criteria externally checkable.
- Reference the source spec or contract context where possible.
- Use `status`, `priority`, `milestone`, `lane`, `allowed_areas`, `blocks`, `proof_required`, `edge_cases`, `non_goals`, and `handoff_notes` when they make parallel work safer.
