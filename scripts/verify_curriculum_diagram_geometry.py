#!/usr/bin/env python3
"""Check curriculum SVG structure and runtime asset synchronization.

This is intentionally a structural guard, not a replacement for browser QA.
It catches the recurrent failures that are reliably machine-detectable:

* orphaned unit asset directories under docs/assets/units, docs/public/assets/units,
  and docs/public/en/assets/units without a matching docs/curriculum/ directory
* malformed SVG/XML across diagram-*.svg and hero.svg files
* root-level background <rect> elements exceeding the SVG viewBox dimensions
* missing public runtime copies or stale copies
* marker-end references to missing markers
* one marker-end attached to multiple SVG subpaths
* curved Bezier commands (C/S/Q/T) on marker-end connector paths
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
SVG_GLOBS = (
    "assets/units/*/images/diagram-*.svg",
    "assets/units/*/images/hero.svg",
)
PUBLIC_ROOTS = (SITE / "public/assets", SITE / "public/en/assets")
UNIT_ASSET_ROOTS = (
    SITE / "assets/units",
    SITE / "public/assets/units",
    SITE / "public/en/assets/units",
)
MOVE_RE = re.compile(r"(?:^|\s)M(?:\s|$)", re.IGNORECASE)
CURVE_CMD_RE = re.compile(r"[CSQT]", re.IGNORECASE)
MARKER_RE = re.compile(r"url\(#([^\)]+)\)")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def elements(root: ET.Element, name: str):
    return [el for el in root.iter() if local_name(el.tag) == name]


def marker_id(value: str) -> str | None:
    match = MARKER_RE.search(value)
    return match.group(1) if match else None


def parse_viewbox(value: str | None) -> tuple[float, float, float, float] | None:
    if not value:
        return None
    parts = [p for p in re.split(r"[\s,]+", value.strip()) if p]
    if len(parts) != 4:
        return None
    try:
        return tuple(float(p) for p in parts)  # type: ignore[return-value]
    except ValueError:
        return None


def parse_length(value: str | None, reference: float | None = None) -> float | None:
    if value is None:
        return None
    raw = value.strip()
    if not raw:
        return None
    if raw.endswith("%"):
        if reference is None:
            return None
        try:
            return reference * float(raw[:-1]) / 100.0
        except ValueError:
            return None
    if raw.endswith("px"):
        raw = raw[:-2].strip()
    try:
        return float(raw)
    except ValueError:
        return None


errors: list[str] = []

curriculum_dir = SITE / "curriculum"
valid_units = {
    entry.name for entry in curriculum_dir.iterdir() if entry.is_dir()
} if curriculum_dir.is_dir() else set()

for unit_root in UNIT_ASSET_ROOTS:
    if not unit_root.is_dir():
        continue
    for entry in sorted(unit_root.iterdir()):
        if entry.is_dir() and entry.name not in valid_units:
            errors.append(
                f"{entry.relative_to(SITE)}: orphaned unit directory "
                f"(missing docs/curriculum/{entry.name})"
            )

source_files = sorted({p for pattern in SVG_GLOBS for p in SITE.glob(pattern)})

for source in source_files:
    rel = source.relative_to(SITE)
    try:
        root = ET.parse(source).getroot()
    except ET.ParseError as exc:
        errors.append(f"{rel}: invalid XML: {exc}")
        continue

    viewbox_attr = root.get("viewBox")
    viewbox = parse_viewbox(viewbox_attr)
    if viewbox_attr is not None and viewbox is None:
        errors.append(f"{rel}: invalid viewBox {viewbox_attr!r}")
    elif viewbox is not None:
        _, _, vb_width, vb_height = viewbox
        for child in root:
            if local_name(child.tag) != "rect":
                continue
            x_val = parse_length(child.get("x"), vb_width) if child.get("x") is not None else 0.0
            y_val = parse_length(child.get("y"), vb_height) if child.get("y") is not None else 0.0
            if x_val == 0.0 and y_val == 0.0:
                rect_w = parse_length(child.get("width"), vb_width)
                rect_h = parse_length(child.get("height"), vb_height)
                if rect_w is not None and rect_w > vb_width:
                    errors.append(
                        f"{rel}: root background <rect> width ({rect_w:g}) "
                        f"exceeds viewBox width ({vb_width:g})"
                    )
                if rect_h is not None and rect_h > vb_height:
                    errors.append(
                        f"{rel}: root background <rect> height ({rect_h:g}) "
                        f"exceeds viewBox height ({vb_height:g})"
                    )

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
                if CURVE_CMD_RE.search(path_data):
                    errors.append(
                        f"{rel}: marker-end path uses curved Bezier command; "
                        "use orthogonal/straight path segments"
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
