#!/usr/bin/env python3
"""Verify curriculum diagram integrity across Japanese and English pages.

Checks for every <img class="unit-diagram"> in curriculum/*/index.md:
  1. the referenced SVG file exists (both in assets/ and public/assets/)
  2. the alt text follows the「図解：<日本語説明>」convention (contains Japanese)
  3. a bridge sentence (non-empty text line) directly precedes the image tag

Checks for every <img class="unit-diagram"> in en/curriculum/*/index.md:
  4. the referenced file resolves to an existing asset under docs/public/
  5. the alt text is non-empty

Checks across all unit* directories:
  6. Japanese and English pages have identical unit-diagram counts per unit
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"
PUBLIC = SITE / "public"
JP_RE = re.compile(r"[ぁ-んァ-ヶ一-龠]")
IMG_TAG_RE = re.compile(r"<img\b[^>]*>")
ATTR_RE = re.compile(r'\b([a-zA-Z_:][\w:.-]*)\s*=\s*"([^"]*)"')


def iter_unit_diagrams(line: str):
    """Yield (src, alt) for each <img ... class="unit-diagram"> on a line."""
    for match in IMG_TAG_RE.finditer(line):
        attrs = dict(ATTR_RE.findall(match.group(0)))
        classes = attrs.get("class", "").split()
        if "unit-diagram" in classes:
            yield attrs.get("src", ""), attrs.get("alt", "")


errors: list[str] = []
ja_count = 0
en_count = 0
ja_unit_counts: dict[str, int] = {}
en_unit_counts: dict[str, int] = {}

for md in sorted(SITE.glob("curriculum/*/index.md")):
    lines = md.read_text(encoding="utf-8").splitlines()
    rel = md.relative_to(SITE)
    unit_name = md.parent.name
    unit_diagrams = 0
    for i, line in enumerate(lines):
        for src, alt in iter_unit_diagrams(line):
            ja_count += 1
            unit_diagrams += 1
            # 1. file existence (src is relative to the md file's directory or root-relative)
            if not src:
                errors.append(f"{rel}:{i+1}: missing src attribute")
            else:
                if src.startswith("/"):
                    target = (SITE / src.lstrip("/")).resolve()
                else:
                    target = (md.parent / src).resolve()
                if not target.exists():
                    errors.append(f"{rel}:{i+1}: missing SVG {src}")
                pub = (
                    PUBLIC / target.relative_to(SITE)
                    if target.is_relative_to(SITE)
                    else None
                )
                if pub is not None and not pub.exists():
                    errors.append(f"{rel}:{i+1}: missing public copy {pub.relative_to(SITE)}")
            # 2. alt convention
            if not alt.startswith("図解："):
                errors.append(f"{rel}:{i+1}: alt not starting with 図解： -> {alt!r}")
            elif not JP_RE.search(alt[3:]):
                errors.append(f"{rel}:{i+1}: alt has no Japanese description -> {alt!r}")
            # 3. bridge sentence: nearest non-empty line above must be prose (not a heading/image/fence)
            j = i - 1
            while j >= 0 and not lines[j].strip():
                j -= 1
            prev = lines[j].strip() if j >= 0 else ""
            if not prev or prev.startswith("#") or prev.startswith("<img") or prev.startswith("```"):
                errors.append(f"{rel}:{i+1}: no bridge sentence before image (prev: {prev[:40]!r})")
    if unit_name.startswith("unit"):
        ja_unit_counts[unit_name] = unit_diagrams

for md in sorted(SITE.glob("en/curriculum/*/index.md")):
    lines = md.read_text(encoding="utf-8").splitlines()
    rel = md.relative_to(SITE)
    unit_name = md.parent.name
    unit_diagrams = 0
    for i, line in enumerate(lines):
        for src, alt in iter_unit_diagrams(line):
            en_count += 1
            unit_diagrams += 1
            # 4. EN public asset resolution (handles leading /en/assets/... paths)
            if not src:
                errors.append(f"{rel}:{i+1}: missing src attribute")
            else:
                if src.startswith("/"):
                    pub_target = (PUBLIC / src.lstrip("/")).resolve()
                else:
                    resolved = (md.parent / src).resolve()
                    pub_target = (
                        (PUBLIC / resolved.relative_to(SITE)).resolve()
                        if resolved.is_relative_to(SITE)
                        else None
                    )
                if (
                    pub_target is None
                    or not pub_target.is_relative_to(PUBLIC)
                    or not pub_target.exists()
                ):
                    errors.append(f"{rel}:{i+1}: missing EN public asset {src}")
            # 5. non-empty alt text
            if not alt.strip():
                errors.append(f"{rel}:{i+1}: empty alt attribute for {src}")
    if unit_name.startswith("unit"):
        en_unit_counts[unit_name] = unit_diagrams

# 6. per-unit JA vs EN diagram count parity across all unit* directories
all_units = sorted(set(ja_unit_counts) | set(en_unit_counts))
for unit_name in all_units:
    ja_n = ja_unit_counts.get(unit_name)
    en_n = en_unit_counts.get(unit_name)
    if ja_n is None:
        errors.append(f"en/curriculum/{unit_name}/index.md: missing matching JA unit index")
    elif en_n is None:
        errors.append(f"curriculum/{unit_name}/index.md: missing matching EN unit index")
    elif ja_n != en_n:
        errors.append(
            f"{unit_name}: JA/EN unit-diagram count mismatch (JA={ja_n}, EN={en_n})"
        )

print(
    f"checked {ja_count} JA and {en_count} EN unit-diagram images "
    f"across {len(all_units)} units"
)
if errors:
    print(f"{len(errors)} problem(s):")
    for e in errors:
        print("  " + e)
    sys.exit(1)
print("all OK")
