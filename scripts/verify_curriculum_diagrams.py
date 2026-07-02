#!/usr/bin/env python3
"""Verify curriculum diagram integrity.

Checks for every <img class="unit-diagram"> in curriculum/*/index.md:
  1. the referenced SVG file exists (both in assets/ and public/assets/)
  2. the alt text follows the「図解：<日本語説明>」convention (contains Japanese)
  3. a bridge sentence (non-empty text line) directly precedes the image tag
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JP_RE = re.compile(r"[ぁ-んァ-ヶ一-龠]")
IMG_RE = re.compile(r'<img\s+src="([^"]+)"\s+alt="([^"]*)"[^>]*class="unit-diagram"[^>]*/?>')

errors = []
count = 0

for md in sorted(ROOT.glob("curriculum/*/index.md")):
    lines = md.read_text(encoding="utf-8").splitlines()
    rel = md.relative_to(ROOT)
    for i, line in enumerate(lines):
        for m in IMG_RE.finditer(line):
            count += 1
            src, alt = m.group(1), m.group(2)
            # 1. file existence (src is relative to the md file's directory)
            target = (md.parent / src).resolve()
            if not target.exists():
                errors.append(f"{rel}:{i+1}: missing SVG {src}")
            pub = ROOT / "public" / target.relative_to(ROOT) if target.is_relative_to(ROOT) else None
            if pub is not None and not pub.exists():
                errors.append(f"{rel}:{i+1}: missing public copy {pub.relative_to(ROOT)}")
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

print(f"checked {count} unit-diagram images")
if errors:
    print(f"{len(errors)} problem(s):")
    for e in errors:
        print("  " + e)
    sys.exit(1)
print("all OK")
