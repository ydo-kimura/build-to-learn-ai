# AI-DLC State Tracking

## Project Information

- **Project Type** : Greenfield (Main Curriculum completed, now iterating feature enhancement)
- **Start Date** : 2026-05-28T06:10:24Z
- **Current Stage** : CONSTRUCTION - Code Generation

## Workspace State

- **Existing Code** : Yes (VitePress curriculum site)
- **Reverse Engineering Needed** : No
- **Workspace Root** : /workspaces/build-to-learn-ai

## Code Location Rules

- **Application Code** : Workspace root (NEVER in aidlc-docs/)
- **Documentation** : aidlc-docs/ only
- **Structure patterns** : See code-generation.md Critical Rules

## Extension Configuration

| Extension              | Enabled | Decided At            |
| ---------------------- | ------- | --------------------- |
| Security Baseline      | No      | Requirements Analysis |
| Property-Based Testing | No      | Requirements Analysis |

## Execution Plan Summary

- **Total Stages** : 5 main stages for Mermaid Plugin integration
- **Stages to Execute** : Workspace Detection, Requirements Analysis, Workflow Planning, Code Generation, Build and Test.
- **Stages to Skip** : Reverse Engineering, User Stories, Application Design, Units Generation, Functional Design, NFR Requirements, NFR Design, Infrastructure Design (All skipped due to single feature plugin configuration scope).

## Stage Progress

### 🔵 INCEPTION PHASE

- [x] Workspace Detection (COMPLETED)
- [x] Requirements Analysis (COMPLETED)
- [x] Workflow Planning (COMPLETED - Presenting for approval)
- [-] Application Design (SKIPPED)
- [-] Units Generation (SKIPPED)

### 🟢 CONSTRUCTION PHASE

- [-] Functional Design (SKIPPED)
- [-] NFR Requirements (SKIPPED)
- [-] NFR Design (SKIPPED)
- [-] Infrastructure Design (SKIPPED)
- [x] Code Generation (COMPLETED)
- [x] Build and Test (COMPLETED)

### 🟡 OPERATIONS PHASE

- [ ] Operations - PLACEHOLDER

## Current Status

- **Lifecycle Phase** : CONSTRUCTION
- **Current Stage** : CONSTRUCTION - Build and Test (COMPLETED for curriculum quality fixes)
- **Next Stage** : Execute the delegated remediation plan in `aidlc-docs/construction/plans/curriculum-review-delegation-plan.md` after baseline isolation (no curriculum fixes applied in the planning turn)
- **Status** : Completed: Mermaid plugin, LangGraph unit + renumbering, curriculum consistency fixes, diagram/text integration, curriculum quality fix plan (all 7 phases done), low-severity fix plan (Phases A-E done), re-review fix plan (all findings fixed: H2/M19/L~50/G1-G6; new QA process applied — Fable 5 decides fix details, executes directly, and reviews each chapter against the plan; verified with curriculum review remediation plan, VitePress build, 82 diagrams, 280 Python blocks across Japanese and English, section shape, and local references). Added Unit 0 scope guidance, Unit 22 tokenizer foundations, Unit 23 token-count/streaming practice, Unit 35 Tokenizer/BPE fundamentals, Unit 36 LoRA/QLoRA fundamentals, shifted Capstones to Unit 37〜42, synchronized English Unit 0〜42 structure and new content, separated English curriculum images into `en/assets/units/`, localized Japanese hero-image titles, and made `public/assets/` and `public/en/assets/` the deployed language-specific asset sources. Remaining backlog: deeper prose parity review for older English units.

## Latest Execution Update

- **Date** : 2026-07-20
- **Status** : Delegated `review.md` remediation completed for valid findings across Japanese Units 1〜42 and corresponding English units. Technical fixes include TF-IDF/attention/position encoding, PyTorch loss and validation examples, Agent references and function names, JSON code-fence cleanup, and the Unit 42 three-specialist structure. Title-only Japanese PNG hero localization was removed; Unit 35/36 SVG explanatory translations were retained. Static validation passed. `openwiki/` internal references are excluded through targeted `ignoreDeadLinks` patterns, and VitePress build now passes with only a chunk-size warning.

## Latest Targeted Diagram Remediation

- [x] Unit 01 train/test split focused correction completed: Unit 10 marker geometry, exact boundary endpoints, and evaluation-circle label clearance applied; three locale/runtime files synchronized and validated.
- [x] Unit 23 concept, Unit 24 concept, Unit 25 concept/workflow, Unit 26 concept, and Unit 30 concept focused correction completed: Unit 10 marker geometry, orthogonal routing, label/card clearance, exact boundary endpoints, and existing connector colors/line styles preserved; 18 locale/runtime files synchronized and validated.
- [x] Unit 20 workflow focused geometry correction completed: requested font sizes, aligned card edges, Unit 10 marker geometry, and boundary-to-boundary residual shortcuts applied; three locale/runtime files synchronized and validated.
- [x] Unit 02 sigmoid, Unit 07 PCA concept/workflow, Unit 11 workflow, Unit 14 workflow, Unit 16 workflow, Unit 17 workflow, Unit 19 workflow, Unit 30 concept, and legacy Unit 40 evaluation-harness workflow content corrected.
- [x] Source SVGs synchronized to matching `public/assets/` and `public/en/assets/` copies.
- [x] Individual natural-size and rendered-page-width browser checks completed.
- [x] Targeted XML/structure/synchronization check, direct VitePress build, and `git diff --check` passed.
- [x] `review.md` and rule files were not edited; no commit created.

## Active Targeted Workflow — OpenWiki PR Auto-update

- **Started**: 2026-07-20T18:10:34Z
- **Current Stage**: INCEPTION - Workflow Planning (approval pending)
- **Scope**: Add safe `pull_request`-driven OpenWiki generation and commit generated changes back to same-repository PR branches.
- **Extensions**: Security Baseline disabled; Property-Based Testing disabled per existing Extension Configuration.
- [x] Workspace Detection
- [x] Requirements Analysis artifact generated
- [x] Requirements approval
- [ ] Workflow Planning approval
- [ ] Code Generation
- [ ] Build and Test
