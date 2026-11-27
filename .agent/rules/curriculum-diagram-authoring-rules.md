# Curriculum Diagram Authoring Rules

These rules are mandatory whenever an AI creates or edits a curriculum diagram.
They apply to SVG and raster diagrams, regardless of whether the diagram is a
concept illustration, a graph, or a workflow. SVG-specific requirements are
marked explicitly; raster images must satisfy the same visual and semantic
requirements through the rendered image.

## 1. Inspect before drawing

- Read the section text, examples, hands-on, and the sentence immediately before the diagram.
- Identify the single learning point the diagram must make visible.
- Before drawing, list the inputs, states, transformations, conditions,
  outputs, and feedback described by the section.
- Build an edge inventory: for every connector record `source`, `target`, what
  flows along it, and whether it is `sequence`, `alternative`, `parallel`,
  `data flow`, or `feedback`.
- Every edge must be supported by the section text, implementation example, or
  hands-on. Do not invent implicit processing or causal order.
- Inspect the existing diagram at readable browser size before editing it.
- Do not infer geometry from a thumbnail or contact sheet. Use individual full-size previews.
- Preserve correct content and terminology; redesign only what improves clarity.

## 2. Layout and safe zones

- Reserve separate zones for title, explanatory text, nodes, connectors, labels, and graph annotations.
- Keep explanatory text, annotations, legends, and card text outside plotted
  data, curves, axes, gridlines, and connector paths. Axis labels and tick
  labels are allowed only in a dedicated band around the plot.
- Keep a minimum SVG-space buffer of `max(8, 2 × stroke-width)` between text
  bounds and any unrelated line or arrow. Do not rely on a stroke being
  “behind” text.
- Keep node labels inside their cards with at least 16 SVG units of padding.
  Distinguish node labels, edge labels, annotations, and legends: edge labels
  belong near a connector, while legends and annotations belong in dedicated
  non-plot areas.
- Never let a callout, legend, formula, or annotation cover a data point or model line.
- Use whitespace to show hierarchy. Do not solve crowding by shrinking text until it becomes unreadable.

## 3. Arrow and connector geometry

- Every arrow is one independent connector with one `marker-end`.
- A split consists of one arrowless trunk from the parent to one shared
  junction, followed by one independent arrowed branch per child. Do not put
  `marker-end` on the trunk.
- A merge consists of independent input branches into one visible junction and
  one output connector with the arrowhead after the junction.
- The shaft must terminate at the arrowhead; never draw a line that stops short of its marker.
- Use `assets/units/unit10_nn_from_scratch/images/diagram-workflow.svg` as the visual
  baseline for arrowhead scale. The shaft must end at the marker's tip; it must never
  protrude beyond the arrowhead. Treat the arrowhead as the selected endpoint, not the
  shaft: tune `refX`, `refY`, `markerUnits`, and the path endpoint together.
- Every connector must also start at the source shape's outer boundary or an
  explicitly named port. Do not start from the middle of a card or from empty
  space.
- The rendered arrow tip must touch the target boundary, not its center,
  corner, or empty space beyond it. Set `refX`/`refY` and `markerUnits`
  deliberately; do not assume the path endpoint equals the visible tip.
- The shaft and arrowhead must be collinear and centered. Use small arrowheads
  with a clear tip, and keep arrowhead length/width no greater than the
  connector's intended visual weight.
- Do not use curved connectors for curriculum diagrams. Route connectors with
  one or two orthogonal straight segments instead, keeping symmetric layouts
  symmetric and routing away from labels and neighboring lines.
- Do not use one `<path>` containing multiple `M` subpaths with a single `marker-end`; only the final subpath receives the marker.
- For a normal flow, connect parent bottom-center to child top-center. For
  horizontal flow, connect right-center to left-center. Treat these as
  defaults; circles, diamonds, and multi-port nodes may use an explicitly
  chosen semantic port on their outer boundary.
- For a split, use one shared junction: the parent exits once, reaches one common bend, and branches from that same coordinate.
- Keep the parent-to-junction trunk and each child branch visually distinct.
  The junction-to-child distance must be at least the arrowhead length plus
  `2 × stroke-width`.
- Leave enough vertical or horizontal clearance between the shared branch line
  and each child arrowhead. An arrowhead must never touch, overlap, or
  visually merge with the branch line; if necessary, move the parent upward,
  move the child downward, or move the junction.
- For a merge, branches must enter a visible shared junction or the target node at consistent boundaries.
- Never use a connector whose endpoint is merely near a node. Verify the endpoint against the node rectangle.
- Except at an intentional junction, connectors must not cross or touch other
  connectors, arrowheads, or labels. Change the route or layout when they do.
- Use dashed connectors only when their meaning is explicit (for example
  feedback, residual, optional, projection, reference, or inferred relation).
  Explain that meaning with a label or legend; never use dashed lines as
  decoration.

## 4. Decision trees and branching diagrams

- All child branches from one decision node must leave from the same parent exit/junction.
- Keep the parent node far enough from the split junction that the parent-to-junction shaft and both branch segments are visually distinct.
- A branch may not touch another trunk, branch, arrowhead, or label except at
  the explicitly intended junction.
- Place YES/NO (or equivalent) labels immediately after the split, on the same relative side of each branch.
- Keep branch labels clear of the branch line and never place them over a junction.
- Point each arrow to the top-center of the child node or leaf. Do not point to a leaf corner or empty space.
- Keep sibling cards separated enough that their arrows and labels cannot overlap.
- Center the primary box group and its connecting arrows inside the backdrop.
  Exclude fixed titles/headers and fixed bottom captions from the centering
  calculation; keep those fixed elements clear of the centered box group. The
  box group must remain visually centered even when a caption is anchored at the
  bottom, and no element may overlap the title or caption.

## 5. Graphs and annotations

- Treat the plot rectangle, axes, grid, curves, points, legend, and annotations as separate layout objects.
- Place annotations in an unused margin or in a dedicated callout area.
- If an annotation must point into a plot, use a short guide line that does not cross data or labels.
- After moving an annotation, recheck both ends of every curve and every nearby data point.

## 6. Semantic flow requirements

- A diagram must represent the concept accurately, not merely look connected.
- For every edge in the inventory, be able to explain whether it carries data,
  control, an evaluation result, retrieved context, or feedback. Do not turn
  parallel inputs into a serial chain, or choices into mandatory steps, unless
  the source content explicitly says so.
- Transformer residuals must be local, forward connections from each
  sublayer input to its corresponding Add node. Match the diagram to the
  section's Pre-LN/Post-LN treatment; do not loop from a later block back to
  the original input.
- RAG diagrams must distinguish indexing from query-time retrieval and show the query plus retrieved context entering generation.
- Prompt-pattern diagrams must not imply that mutually selectable strategies are always executed in a fixed serial chain.
- Late-fusion diagrams must show independent modality processing before scores are fused.
- Guardrail diagrams must show both input and output checks when the title claims input/output guardrails.
- Evaluation-harness diagrams must show the evaluated application/candidate output before the judge scores it.
- Time-series diagrams must not imply that forecasting happens directly from a
  split without feature creation and model training, unless the diagram
  explicitly identifies a naïve or statistical baseline.
- Knowledge graphs/stores must appear before the query/answer step when they are the searchable knowledge source.

## 7. Locale and asset synchronization

- Determine the actual runtime path from the page source for each locale before copying files.
- In this repository, `assets/units/...` is the Japanese editing source,
  `public/assets/...` is its runtime copy, and English pages currently load
  `public/en/assets/...`. There is no implicit `en/assets` editing source.
- Keep each editing source and every page-referenced runtime copy byte-identical.
- If a locale has its own translated diagram, declare that locale's editing
  source explicitly; never call different files “synchronized”.
- If a diagram is intentionally not present in one locale, verify that no page references it.

## 8. Required review before completion

For every changed diagram:

1. Render the SVG directly at full readable size in the browser.
2. Render the actual curriculum page at its standard content width; both views
   are required because a direct asset can be readable while the page-scale
   image is not.
3. Check every arrow start, bend, arrowhead, and target boundary.
4. Check every label against nearby lines, curves, points, and card edges.
5. Compare the rendered graph with the edge inventory and section learning objective.
6. Check all locale copies and run `pnpm run docs:check-diagrams` and
   `pnpm run docs:build`.
7. For batch work, report the exact file list and count, per-file visual /
   geometry / semantic / locale status, fixes, unresolved items, and any
   independent review disagreement. If one file is unconfirmed, do not report
   the batch as fully checked.
8. A second model, different from the model that created or edited the figure,
   must independently review the changed diagrams. For a high-risk or batch
   change, use two independent reviewer models and record disagreements and
   their resolution. The authoring model may not self-approve its own visual
   or semantic result.

Never report “all diagrams checked” based only on a contact sheet, thumbnail,
file existence check, or build success.
