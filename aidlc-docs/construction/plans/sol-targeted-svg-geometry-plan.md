# Sol Targeted SVG Geometry Remediation Plan

Scope: 24 specified source SVGs. Review and edit each source directly, then synchronize only its matching `public/assets` and `public/en/assets` runtime copies. Preserve unrelated worktree changes. Do not edit `review.md`, authoring rules, or unspecified Unit files.

Current focused tranche (2026-07-21 JST): Unit 01 train/test split arrow geometry and evaluation-circle label clearance. Remaining entries stay pending outside this tranche.

## Preparation

- [x] Resume the existing AI-DLC Code Generation / Build and Test workflow.
- [x] Read the common workflow, continuity, content-validation, question-format, and curriculum diagram authoring rules.
- [x] Confirm Security Baseline and Property-Based Testing extensions remain disabled.
- [x] Inventory the requested files and identify the existing dirty worktree as user-owned.
- [x] Read each diagram's surrounding lesson text and record its supported edge flow.
- [x] Inspect each requested source SVG individually at full readable size before editing.

## Direct source editing

- [ ] Unit 04 workflow: move vote labels above cards and center/symmetrize branches.
- [ ] Unit 05 concept: center and symmetrize branch connectors.
- [ ] Unit 09 concept: separate the 5-to-4 connector from its text.
- [ ] Unit 11 workflow: halve arrowheads and connect exact card boundaries.
- [ ] Unit 12 concept: halve arrowheads.
- [ ] Unit 14 concept: connect exact card boundaries.
- [ ] Unit 14 workflow: remove card decoration, fix overflow, and use symmetric one-bend connectors.
- [ ] Unit 16 concept: connect exact card boundaries.
- [ ] Unit 17 workflow: halve arrowheads and replace curves with symmetric one-bend connectors.
- [ ] Unit 19 concept: halve arrowheads and clear labels.
- [ ] Unit 19 workflow: halve arrowheads, resize the right card, and use symmetric one-bend boundary connectors.
- [ ] Unit 21 concept: balance card widths and use small boundary-connected arrows.
- [ ] Unit 21 workflow: reserve right-side arrow lanes and replace the duplicate upper flow with supporting explanation.
- [x] Unit 22 concept: reduce only outer arrowheads, preserve RAG internals, replace Agent curve with a lower-right-upper polyline, and join its return/arrow segments at `(1102, 260)`.
- [ ] Unit 23 workflow: separate connector labels from arrow paths.
- [x] Unit 28 workflow: replace malformed connector with a two-bend boundary-connected polyline.
- [x] Unit 30 concept: balance card widths and connector lanes; connect both card boundaries naturally.
- [x] Unit 32 workflow: align Classify and Technical centers and share the Classify junction intersection.
- [x] Unit 38 concept: center the complete box/connector group within the backdrop, preserve parallel late-fusion semantics, and reserve safe side and arrow lanes.
- [x] Unit 38 workflow: center the complete box/connector group within the backdrop and reserve safe side and merge/output arrow lanes.
- [ ] Unit 39 concept: halve arrowheads, connect boundaries, and move Retry above STRUCTURED RECORD.
- [ ] Unit 40 concept: redesign card widths/lanes, preserve readable equal font sizes, and halve arrowheads.
- [ ] Unit 40 workflow: halve arrowheads, connect boundaries, and remove curves.
- [ ] Unit 41 concept: balance fonts/connectors, halve arrowheads, and connect boundaries.
- [ ] Unit 42 concept: balance cards/connectors, halve arrowheads, and connect boundaries.
- [ ] Unit 42 workflow: balance cards/connectors, halve arrowheads, and connect boundaries.

## Synchronization and verification

### Current focused tranche

- [x] Synchronize Unit 22 concept source to `public/assets` and `public/en/assets` with byte parity.
- [x] Validate Unit 22 concept XML and exact Agent-loop path coordinates.
- [x] Run `git diff --check` after the focused change.
- [x] Skip browser inspection as explicitly requested; visual review remains with Terra.

- [x] Synchronize Unit 28 workflow, Unit 30 concept, and Unit 32 workflow sources to `public/assets` and `public/en/assets` with byte parity.
- [x] Validate all nine synchronized files as well-formed XML and verify the requested orthogonal paths, boundary endpoints, balanced widths, aligned centers, and shared junction.
- [x] Run `git diff --check` after the three-diagram focused change.
- [x] Skip browser inspection as explicitly requested.

- [ ] Synchronize each reviewed source to matching Japanese and English runtime copies.
- [ ] Reinspect every changed source at original-size URL.
- [ ] Reinspect every changed diagram on its actual Japanese curriculum page.
- [ ] Validate XML well-formedness, independent connector structure, boundary endpoints, and source/runtime byte parity.
- [ ] Obtain two independent reviewer-model checks and resolve disagreements.
- [ ] Run `pnpm run docs:check-diagrams`.
- [ ] Run `pnpm run docs:build`.
- [ ] Run `git diff --check` and verify protected files were not changed by this task.
- [ ] Report exact files, per-file visual/geometry/semantic/locale status, and unresolved items.

### Unit 20 workflow focused correction

- [x] Retain `INPUT X` at x=640, width=105; align self-attention Add left edge at x=640.
- [x] Align `Q×K → weights` and self-attention Add right edges at x=900.
- [x] Apply the requested one-point font reductions and position-label clearance.
- [x] Route the self-attention shortcut through the left lane from input left-center to Add left-center.
- [x] Widen the feed-forward Add; narrow and right-align both Linear cards.
- [x] Split from `INPUT X'` bottom-center and terminate the shortcut at Add left-center `(1000, 633)`.
- [x] Apply Unit 10 marker geometry, synchronize both runtime copies, and pass XML, coordinate, byte-parity, and diff checks.

### Units 23–26 and 30 focused correction

- [x] Reinspect Unit 23 concept, Unit 24 concept, Unit 25 concept/workflow, Unit 26 concept, and Unit 30 concept against the Unit 10 arrow baseline.
- [x] Correct arrow scale, orthogonal routes, connector-label clearance, card padding, and exact boundary endpoints while preserving existing connector colors and line styles.
- [x] Synchronize the six source SVGs to their matching `public/assets` and `public/en/assets` runtime copies.
- [x] Validate all 18 files as well-formed XML and verify source/runtime byte parity.
- [x] Run `git diff --check` and confirm no unspecified SVG was edited in this focused correction.

### Unit 38 focused correction

- [x] Reinspect Unit 38 concept/workflow source, surrounding lesson text, existing target-file diff, and Unit 10 marker baseline.
- [x] Record the supported edge inventory: concept has two independent modality pipelines merging into late fusion; workflow has two independent fraud signals merging into fusion, then review.
- [x] Resize and reposition only the Unit 38 diagram box groups to center them within each backdrop with safe side margins, text padding, and connector lanes.
- [x] Preserve existing connector line style, color, meaning, independent merge structure, and Unit 10 marker geometry.
- [x] Synchronize both sources to matching `public/assets` and `public/en/assets` runtime copies.
- [x] Validate all six files as well-formed XML and verify source/runtime byte parity.
- [x] Inspect both changed sources at original size and on the Japanese curriculum page at its standard rendered width; verify the English page loads both `/en/assets` copies.
- [ ] Obtain the required independent reviewer-model check; no multi-agent reviewer tool is available in this session, so this remains explicitly unresolved.
- [x] Run the repository diagram checks through `pnpm run docs:build`; 86 diagram references, 98 SVG structural checks, 14 Mermaid blocks, and the VitePress build passed.
- [x] Run `git diff --check` and report the exact changed files.

### Unit 01 train/test split focused correction

- [x] Reinspect the Unit 01 source, runtime references, existing target-file diff, and Unit 10 marker baseline.
- [x] Record the supported edge flow: all data enters the split; training data enters fitting; fitting precedes prediction; held-out test data supports prediction/evaluation; predictions enter evaluation.
- [x] Apply Unit 10 marker geometry while preserving connector colors, widths, line styles, and meaning.
- [x] Terminate every connector tip at the exact target boundary, including `.fit()` to `.predict()`.
- [x] Resize/reposition the evaluation circle and its `MSE` / `prediction vs truth` labels so no text intersects the circle stroke.
- [x] Synchronize the source to matching `public/assets` and `public/en/assets` runtime copies.
- [x] Validate all three files as well-formed XML and verify source/runtime byte parity, requested geometry, and `git diff --check`.
- [x] Inspect the changed SVG at original size and at a 673px page-equivalent width with the local renderer after Browser policy blocked the local `file:` URL.
