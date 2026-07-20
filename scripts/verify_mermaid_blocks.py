"""Run lightweight safety checks for Mermaid blocks embedded in curriculum Markdown."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_ROOTS = (ROOT / "docs/curriculum", ROOT / "docs/en")
FENCE_PATTERN = re.compile(r"```mermaid\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)
NODE_ID_PATTERN = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*[\[({]")
UNQUOTED_QUOTED_LABEL_PATTERN = re.compile(
    r"\b[A-Za-z_][A-Za-z0-9_]*\[(?!\")[^\]\n]*\"[^\]\n]*\]"
)


def iter_markdown_files() -> list[Path]:
    return sorted(
        path
        for root in MARKDOWN_ROOTS
        if root.exists()
        for path in root.rglob("*.md")
    )


def validate_block(path: Path, block: str, block_number: int) -> list[str]:
    errors: list[str] = []
    if not block.strip():
        errors.append(f"{path}: Mermaid block {block_number} is empty")
        return errors

    for node_id in NODE_ID_PATTERN.findall(block):
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", node_id):
            errors.append(
                f"{path}: Mermaid block {block_number} has invalid node ID {node_id!r}"
            )

    if UNQUOTED_QUOTED_LABEL_PATTERN.search(block):
        errors.append(
            f"{path}: Mermaid block {block_number} has a quoted label inside an "
            "unquoted node label; quote the complete label"
        )
    return errors


def main() -> int:
    errors: list[str] = []
    block_count = 0

    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        blocks = FENCE_PATTERN.findall(text)
        block_count += len(blocks)
        for block_number, block in enumerate(blocks, start=1):
            errors.extend(validate_block(path, block, block_number))

    if errors:
        print("Mermaid block verification failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1

    print(f"Mermaid block verification passed: {block_count} blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
