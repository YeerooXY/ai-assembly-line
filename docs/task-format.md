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

- `risk_tags`
- `notes`

## Rules

- Use stable identifiers.
- Keep tasks implementation-sized.
- Make acceptance criteria externally checkable.
- Reference the source spec or contract context where possible.
