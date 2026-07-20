---
type: Reference
title: "Visual Asset Pipeline"
description: "Python scripts for SVG diagram generation, hero image deployment, diagram integration into curriculum markdown, and verification of visual asset integrity."
tags: [scripts, svg, assets, pipeline, diagrams]
---

The repository has a multi-stage visual asset pipeline that generates SVG diagrams, deploys hero images, integrates diagrams into curriculum Markdown at semantic locations, and verifies asset integrity. All scripts live in [`/scripts/`](../../scripts/).

## Pipeline Overview

```bash
hero_prompts.py (prompt definitions)
       ↓ [external AI image generation]
deploy_hero_images.py → docs/assets/units/<slug>/images/hero.png

generate_curriculum_visuals.py + curriculum_svg_lib.py
       ↓ [Python SVG string building]
       → docs/assets/units/<slug>/images/diagram-concept.svg
       → docs/assets/units/<slug>/images/diagram-workflow.svg
       ↓ [ImageMagick convert]
       → docs/assets/units/<slug>/images/concept.png

integrate_curriculum_diagrams.py → docs/curriculum/<slug>/index.md
       (inserts <img> tags with bridge sentences at semantic locations)

fix_ja_markdown_bold.py → docs/curriculum/<slug>/index.md
       (fixes **bold** spacing around CJK characters)

verify_curriculum_diagrams.py → checks integrity of final Markdown
       (file existence, alt text, bridge sentences)

verify_mermaid_blocks.py → validates Mermaid syntax in docs/curriculum/ and docs/en/
       (node IDs, quoted labels, empty blocks)

verify_curriculum_diagram_geometry.py → validates SVG structure
       (XML validity, stale existing runtime copies, marker references, split paths)

[copy step] → docs/public/assets/units/<slug>/images/ (mirror of docs/assets/)
```

## Scripts

### `generate_curriculum_visuals.py`

The main SVG generation script. It maintains a `UNIT_BUILDERS` registry mapping each unit slug to a tuple of `(title, hero_fn, concept_fn, workflow_fn)`. Each function returns an SVG string. The script:

- Imports ~50 diagram-building functions from `curriculum_svg_lib.py`
- Creates `docs/assets/units/<slug>/images/` directories
- Writes `diagram-concept.svg` and `diagram-workflow.svg` per unit
- Optionally rasterizes SVGs to PNG via ImageMagick (`convert` at 144 DPI)
- Supports `--diagrams-only` flag to skip PNG conversion

Hero PNGs are explicitly **not** generated here — they are created externally and deployed separately.

### `curriculum_svg_lib.py`

A zero-dependency, pure-Python SVG generation library (~38KB). Builds SVG XML strings programmatically with no external dependencies.

**Primitive builders** (private, `_`-prefixed):

- `_t()` — `<text>` element with auto-escaping
- `_rect()` — `<rect>` with rounded corners
- `_circle()` — `<circle>` element
- `_line()` — `<line>` with optional dash pattern
- `_arrow()` — Line + triangular arrowhead
- `_label_box()` — Composite rect + centered text

**Utility functions:**

- `esc(text)` — XML-escapes `&`, `<`, `>`, `"`
- `_title_size(text, max_size)` — Auto-shrinks title font size based on text length
- `_box_w_for_label(text)` — Calculates box width from label length

**Composite layout builders** (public API):

- `svg_doc(view_w, view_h, body, aria)` — Wraps content in `<svg>` with viewBox and accessibility attributes
- `hero_two_panel(title, left_*, right_*)` — 1200×320 hero banner with two side-by-side panels and arrow
- `diagram_card(title, body, subtitle, accent)` — 700×380 card with accent-colored title bar
- `diagram_compare(title_l, body_l, title_r, body_r, caption)` — Side-by-side comparison layout
- `flow_horizontal(steps, y, max_width)` — Horizontal arrow-connected flow with auto-scaling
- `mini_tree(root, left, right, ll, lr)` — Binary tree diagram
- ~40 `mini_*()` functions — Unit-specific concept diagrams (e.g., `mini_cnn()`, `mini_transformer()`, `mini_rag()`, `mini_mcp()`)

Each `mini_*` function accepts an optional `compact=True` parameter for use inside `diagram_compare` layouts.

### `deploy_hero_images.py`

Copies externally-generated hero PNGs from a Cursor workspace directory into the project's `docs/assets/units/<slug>/images/hero.png`. It:

- Expects source files named `unit04-hero.png`, `unit05-hero.png`, etc.
- Validates that all expected files are present
- Exits with error code 1 if any are missing
- Uses `shutil.copy2()` for file metadata preservation

### `hero_prompts.py`

A data module containing `HERO_PROMPTS` — a dict mapping each unit slug to a detailed English text prompt for an AI image generator. A shared `HERO_STYLE` constant defines the common aesthetic: "Wide educational hero banner, 3:2 aspect ratio, clean white background, textbook diagram aesthetic, blue (#3b82f6) and accent colors."

### `integrate_curriculum_diagrams.py`

Performs **semantic placement** of diagram images within `docs/curriculum/` Markdown. It:

1. **Extracts** existing `<img>` tags for `diagram-concept.svg` and `diagram-workflow.svg` from the file
2. **Re-inserts** them after specific heading anchors defined in a `UNIT_CONFIG` dict, with a Japanese "bridge sentence" (`下図は…` / "The diagram below shows…") directly before each image
3. **Idempotency**: Checks if the image is already preceded by a bridge sentence within 200 chars and skips if so
4. **Fallback**: If no config exists for a slug, images are placed before `## 2.` section divider

Units 00, 01, 02, 03, 04, 06, and 10 are skipped (they have custom/legacy diagram setups).

### `verify_curriculum_diagrams.py`

An integrity-checking script that validates three invariants for every `<img class="unit-diagram">` across all `docs/curriculum/*/index.md` files:

| Check           | Rule                                                                                 |
| --------------- | ------------------------------------------------------------------------------------ |
| File existence  | SVG must exist in both `docs/assets/` and `docs/public/assets/`                      |
| Alt convention  | `alt` must start with `図解：` and contain Japanese characters                       |
| Bridge sentence | A prose line (not heading, image, or code fence) must directly precede the image tag |

Exits with code 1 if any violations are found.

### `verify_mermaid_blocks.py`

Validates Mermaid fenced code blocks in `docs/curriculum/` and `docs/en/` Markdown files. Checks for:

| Check               | Rule                                                                              |
| ------------------- | --------------------------------------------------------------------------------- |
| Empty blocks        | Mermaid blocks must not be empty                                                  |
| Node ID validity    | Node IDs must match `[A-Za-z_][A-Za-z0-9_]*`                                      |
| Quoted label safety | A quoted string inside an unquoted node label is flagged (quote the entire label) |

This script was added to prevent malformed Mermaid syntax from breaking the VitePress build. It is wired into the build pipeline via `pnpm run docs:check-mermaid`.

### `verify_curriculum_diagram_geometry.py`

Validates SVG structural integrity for `docs/assets/units/*/images/diagram-*.svg` files. It catches machine-detectable failures:

- Malformed SVG/XML
- Stale existing runtime copies in `docs/public/assets/` and `docs/public/en/assets/`
- `marker-end` references to missing `<marker>` definitions
- One `marker-end` attached to multiple SVG subpaths (split trunk with arrowhead)
- Empty arrowed connector paths (a `marker-end` path with no `d` attribute)

This is intentionally a structural guard, not a replacement for browser QA — text/line intersections and semantic intent are left to human review. It reports stale copies only when the corresponding runtime file already exists; the page-reference verifier remains responsible for detecting missing Japanese runtime assets.

### Required review for diagram changes

The [curriculum diagram authoring rules](../../.agent/rules/curriculum-diagram-authoring-rules.md) govern changes made through this pipeline. Before editing, inspect the surrounding lesson and existing diagram at readable size, identify the single learning point, and inventory only the source-supported edges. Preserve correct terminology and behavior rather than redesigning for appearance alone.

For each changed diagram, review both the full-size SVG and the rendered curriculum page; verify connector boundaries, arrowheads, labels, and semantic flow. Synchronize every page-referenced runtime copy, then run the automated checks described in the [operations runbook](../operations/runbook.md). The rules also require review by a model different from the authoring model; high-risk or batch work requires two independent reviewers and recorded resolution of disagreements. A successful build or file-existence check alone is not sufficient evidence of visual or semantic correctness.

### `fix_ja_markdown_bold.py`

Fixes a VitePress parsing issue where `**bold**` adjacent to CJK characters is not rendered as bold. The script:

- Inserts half-width spaces around `**bold**` markers when adjacent to CJK characters or Japanese punctuation
- Skips code blocks (` ``` ` fences) and inline code
- Targets `docs/curriculum/` and `aidlc-docs/` directories (excluding `/en/` subdirectories)
- Supports `--dry-run` flag

## Asset Directory Structure

### `docs/assets/` (Canonical Source)

```bash
docs/assets/units/
├── unit01_linear_regression/images/
│   ├── hero.png
│   ├── diagram-concept.svg
│   ├── diagram-workflow.svg
│   ├── concept.png
│   └── (unit-specific SVGs: diagram-linear-regression.svg, etc.)
├── unit02_logistic_regression/images/
│   └── ...
└── ... (through unit42)
```

### `docs/public/assets/` (Deployed Mirror)

An identical copy of `docs/assets/units/` that VitePress serves as static files. The `verify_curriculum_diagrams.py` script checks that referenced SVGs exist in **both** locations.

### Per-Unit Files

| File                   | Source                                       | Type                       |
| ---------------------- | -------------------------------------------- | -------------------------- |
| `hero.png`             | AI image generator → `deploy_hero_images.py` | Raster (~900KB–1MB)        |
| `hero.svg`             | `generate_curriculum_visuals.py`             | Vector (units 35, 36 only) |
| `diagram-concept.svg`  | `generate_curriculum_visuals.py`             | Vector (~2–3KB)            |
| `diagram-workflow.svg` | `generate_curriculum_visuals.py`             | Vector (~2–3KB)            |
| `concept.png`          | ImageMagick rasterization of SVG             | Raster (~150KB)            |

## Key Design Decisions

- **Separation of concerns**: Hero PNGs (raster, AI-generated) are deployed via `deploy_hero_images.py`, while concept/workflow SVGs (vector, programmatically generated) are created via `generate_curriculum_visuals.py`. Both end up in the same `images/` directory.
- **Zero-dependency SVG**: The `curriculum_svg_lib.py` library builds SVG XML with string concatenation — no Jinja2, no lxml, no svgwrite. This ensures the pipeline runs in any Python environment.
- **Semantic placement**: Diagrams are not placed at arbitrary locations — `integrate_curriculum_diagrams.py` uses heading anchors and bridge sentences to ensure each image is contextually introduced.
- **Dual asset trees**: The `docs/assets/` → `docs/public/assets/` mirror ensures generated assets are both version-controlled and served by VitePress.
