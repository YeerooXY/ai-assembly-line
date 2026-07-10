from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_MARKERS = {
    "AGENTS.md": [
        "Mandatory first-contact routing",
        "First-turn hard stop",
        "A. greenfield",
        "Then stop",
    ],
    "README.md": [
        "AI agent entrypoint — mandatory",
        "docs/AI_START_HERE.md",
        "Then stop",
        "Do not invent a title, MVP, game loop",
    ],
    "docs/AI_START_HERE.md": [
        "Startup lock for rough ideas",
        "Repository state: not established",
        "A. Greenfield",
        "Then stop",
    ],
    ".github/copilot-instructions.md": [
        "Read `AGENTS.md`",
        "do not brainstorm the product",
        "stop after that question",
    ],
    "prompts/08-project-workspace-initializer.md": [
        "Mandatory first-turn lock",
        "prompts/00-intake-interviewer.md",
        "Then stop",
        "Do not inspect the framework and then “map”",
    ],
    "prompts/00-intake-interviewer.md": [
        "Critical start-request rule",
        "First-turn hard stop",
        "ask exactly one user-facing question per turn",
    ],
}


def main() -> int:
    errors: list[str] = []

    for relative, markers in REQUIRED_MARKERS.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing required AI entrypoint: {relative}")
            continue
        content = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in content:
                errors.append(f"{relative} missing marker: {marker}")

    manifest_path = ROOT / "generated" / "review_manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid review manifest: {exc}")
    else:
        listed = {
            item.get("path")
            for item in manifest.get("review_files", [])
            if isinstance(item, dict)
        }
        for required in ("AGENTS.md", "docs/AI_START_HERE.md"):
            if required not in listed:
                errors.append(f"review manifest missing AI entrypoint: {required}")

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"RESULT FAIL agent_entrypoints errors={len(errors)}")
        return 1

    print(
        "RESULT OK agent_entrypoints "
        f"files={len(REQUIRED_MARKERS)} first_turn_lock=true"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
