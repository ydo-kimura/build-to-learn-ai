#!/usr/bin/env python3
"""Insert half-width spaces around **bold** when adjacent to CJK / JP punctuation.

VitePress (this project) does not parse **bold** unless:
  - there is a half-width space BEFORE opening **
  - there is a half-width space AFTER closing **
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Character before opening ** that requires a preceding space
NEEDS_SPACE_BEFORE = re.compile(
    r"[\u3040-\u30ff\u4e00-\u9fff\u3000-\u303f\uff00-\uffef"
    r"a-zA-Z0-9"
    r"]"
)

# Character after closing ** that requires a following space
NEEDS_SPACE_AFTER = re.compile(
    r"[\u3040-\u30ff\u4e00-\u9fff\u3000-\u303f\uff00-\uffef"
    r"a-zA-Z0-9"
    r",.;:()、。）」』【（：；！？"
    r"]"
)

# Do not add space before ** when preceded by these (markdown syntax)
SKIP_BEFORE = set(" \t\n\r|([{>#!-*+" + "'" + '"')


def fix_bold_segment(line: str) -> str:
    out: list[str] = []
    i = 0
    n = len(line)
    while i < n:
        if line[i : i + 2] != "**":
            out.append(line[i])
            i += 1
            continue

        j = line.find("**", i + 2)
        if j == -1:
            out.append(line[i])
            i += 1
            continue

        inner = line[i + 2 : j]
        # skip empty or likely mistaken patterns
        if not inner.strip():
            out.append(line[i : j + 2])
            i = j + 2
            continue

        if out and out[-1] not in SKIP_BEFORE and NEEDS_SPACE_BEFORE.match(out[-1]):
            if out[-1] != " ":
                out.append(" ")

        out.append("**")
        out.append(inner)
        out.append("**")
        i = j + 2

        if i < n and line[i] != " " and NEEDS_SPACE_AFTER.match(line[i]):
            out.append(" ")

    return "".join(out)


def fix_line(line: str) -> str:
  # preserve leading whitespace
    m = re.match(r"^(\s*)", line)
    prefix = m.group(1) if m else ""
    return prefix + fix_bold_segment(line[len(prefix) :])


def fix_markdown(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out_lines: list[str] = []
    in_fence = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        # skip inline-code-only lines is hard; process prose parts only
        if "`" in line:
            # split by backticks, fix even segments only
            parts = line.split("`")
            for idx, part in enumerate(parts):
                if idx % 2 == 0:
                    parts[idx] = fix_line(part) if part else part
            out_lines.append("`".join(parts))
        else:
            out_lines.append(fix_line(line) if line.endswith("\n") else fix_line(line + "\n").rstrip("\n"))
    return "".join(out_lines)


def collect_targets() -> list[Path]:
    paths: list[Path] = []
    for base in [ROOT / "curriculum", ROOT / "aidlc-docs"]:
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            if "/en/" in p.as_posix() or p.parts[-2:-1] == ("en",):
                continue
            paths.append(p)
    return sorted(paths)


def main() -> int:
    dry = "--dry-run" in sys.argv
    changed_files = 0
    for path in collect_targets():
        original = path.read_text(encoding="utf-8")
        fixed = fix_markdown(original)
        if fixed != original:
            changed_files += 1
            if dry:
                print(f"would fix: {path.relative_to(ROOT)}")
            else:
                path.write_text(fixed, encoding="utf-8")
                print(f"fixed: {path.relative_to(ROOT)}")
    print(f"{'Would change' if dry else 'Changed'} {changed_files} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
