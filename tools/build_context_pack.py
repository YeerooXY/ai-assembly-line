from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "generated" / "review_manifest.json"
OUTPUT_PATH = ROOT / "generated" / "context_pack.md"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def file_language(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "json"
    if suffix == ".js":
        return "javascript"
    if suffix == ".html":
        return "html"
    if suffix == ".css":
        return "css"
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    if suffix == ".md":
        return "markdown"
    if suffix == ".py":
        return "python"
    return ""


def fenced_block(path: Path, content: str) -> str:
    language = file_language(path)
    fence = f"```{language}" if language else "```"
    return f"{fence}\n{content}\n```"


def main() -> int:
    manifest = load_json(MANIFEST_PATH)
    entries = manifest["review_files"]

    warnings: list[str] = []
    missing_required: list[str] = []
    included_count = 0
    sections: list[str] = [
        "# AI Assembly Line Context Pack",
        "",
        "This file is generated from `generated/review_manifest.json` by `tools/build_context_pack.py`.",
        "Treat the Git repository as the only source of truth and do not rely on chat history.",
        "",
    ]

    for entry in entries:
        rel_path = entry["path"]
        category = entry["category"]
        purpose = entry["purpose"]
        required = bool(entry["required"])
        path = ROOT / rel_path

        if path == OUTPUT_PATH:
            sections.extend(
                [
                    f"## `{rel_path}`",
                    "",
                    f"- Category: `{category}`",
                    f"- Purpose: {purpose}",
                    f"- Required: `{str(required).lower()}`",
                    "",
                    "_Skipped self-embedding to avoid recursive context-pack inclusion._",
                    "",
                ]
            )
            included_count += 1
            print(f"SKIP SELF {rel_path}")
            continue

        if not path.exists():
            message = f"{'ERROR' if required else 'WARN '} missing {'required' if required else 'optional'} file: {rel_path}"
            if required:
                missing_required.append(rel_path)
            else:
                warnings.append(message)
            print(message)
            continue

        content = path.read_text(encoding="utf-8")
        sections.extend(
            [
                f"## `{rel_path}`",
                "",
                f"- Category: `{category}`",
                f"- Purpose: {purpose}",
                f"- Required: `{str(required).lower()}`",
                "",
                fenced_block(path, content),
                "",
            ]
        )
        included_count += 1
        print(f"INCLUDED {rel_path}")

    OUTPUT_PATH.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    print(f"WROTE {OUTPUT_PATH.relative_to(ROOT).as_posix()}")

    for warning in warnings:
        print(warning)

    if missing_required:
        print(f"RESULT FAIL missing_required={len(missing_required)}")
        return 1

    print(f"RESULT OK included={included_count} warnings={len(warnings)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
