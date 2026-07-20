# Targeted Diagram Legibility Remediation Plan

Scope: 16 source SVGs in Units 01–03, 07–09, and 20. Edit only `assets/units/...`; synchronize matching runtime copies after source review. Do not edit `review.md` or rule files.

## Inception / preparation

- [x] Confirm workspace state, existing user changes, source/runtime paths, and page width.
- [x] Read curriculum diagram authoring and content-validation rules.
- [x] Inspect every target SVG individually at source size in the browser.
- [x] Measure the standard curriculum image width (673px at a 1440px viewport).

## Construction / source edits

- [x] Review and improve Unit 01 source diagrams.
- [x] Review and improve Unit 02 source diagrams.
- [x] Review and improve Unit 03 source diagrams.
- [x] Review and improve Unit 07 concept/workflow.
- [x] Review and improve Unit 08 concept/workflow.
- [x] Review and improve Unit 09 concept/workflow.
- [x] Review and improve Unit 20 concept/workflow.
- [x] Leave any diagram unchanged when a legibility change would damage meaning or layout; record the reason. No target required a full no-change exception; narrow labels were kept below the safe enlargement threshold.

## Synchronization and verification

- [ ] Synchronize changed sources to matching `public/assets` and `public/en/assets` copies only.
- [ ] Inspect changed diagrams individually at source size after edits.
- [ ] Inspect the actual Japanese curriculum pages at the 673px diagram width.
- [ ] Check XML well-formedness, SVG structure, and source/runtime byte parity.
- [ ] Run `pnpm run docs:check-diagrams`.
- [ ] Run `pnpm run docs:build`.
- [ ] Run `git diff --check` and confirm `review.md` and rule files are unchanged by this task.
- [ ] Report exact changed file list, per-file visual/geometry/semantic/locale status, and unresolved items.
