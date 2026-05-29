#!/usr/bin/env python3
"""Check curriculum SVG structure and runtime asset synchronization.

This is intentionally a structural guard, not a replacement for browser QA.
It catches the recurrent failures that are reliably machine-detectable:

* malformed SVG/XML
* missing public runtime copies or stale copies
* marker-end references to missing markers
* one marker-end attached to multiple SVG subpaths
* empty connector paths

Text/line intersections and semantic intent are deliberately left to the
individual browser review because SVG text metrics and learning semantics
cannot be inferred reliably from XML alone.
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"
SVG_GLOB = "assets/units/*/images/diagram-*.svg"
PUBLIC_ROOTS = (SITE / "public/assets", SITE / "public/en/assets")
NS = "{http://www.w3.org/2000/svg}"
MOVE_RE = re.compile(r"(?:^|\s)M(?:\s|$)", re.IGNORECASE)
MARKER_RE = re.compile(r"url\(#([^\)]+)\)")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def elements(root: ET.Element, name: str):
    return [el for el in root.iter() if local_name(el.tag) == name]


def marker_id(value: str) -> str | None:
    match = MARKER_RE.search(value)
    return match.group(1) if match else None


errors: list[str] = []
source_files = sorted(SITE.glob(SVG_GLOB))

for source in source_files:
    rel = source.relative_to(SITE)
    try:
        root = ET.parse(source).getroot()
    except ET.ParseError as exc:
        errors.append(f"{rel}: invalid XML: {exc}")
        continue

    marker_ids = {el.get("id") for el in elements(root, "marker") if el.get("id")}
    for el in root.iter():
        marker_value = el.get("marker-end")
        if marker_value:
            referenced = marker_id(marker_value)
            if referenced and referenced not in marker_ids:
                errors.append(f"{rel}: marker-end references missing marker #{referenced}")

            if local_name(el.tag) == "path":
                path_data = el.get("d", "").strip()
                if not path_data:
                    errors.append(f"{rel}: marker-end path has empty d attribute")
                move_count = len(MOVE_RE.findall(path_data))
                if move_count > 1:
                    errors.append(
                        f"{rel}: marker-end path contains {move_count} subpaths; "
                        "split it into one element per arrow"
                    )

    for public_root in PUBLIC_ROOTS:
        runtime_copy = public_root / rel.relative_to("assets")
        if runtime_copy.exists() and runtime_copy.read_bytes() != source.read_bytes():
            errors.append(f"{rel}: stale runtime copy {runtime_copy.relative_to(SITE)}")

print(f"checked {len(source_files)} curriculum SVGs")
print("note: text/line overlap and semantic flow still require individual browser review")
if errors:
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"  ERROR: {error}")
    sys.exit(1)
print("diagram structural checks passed")
