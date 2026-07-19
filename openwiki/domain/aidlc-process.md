---
type: Reference
title: "AIDLC Process"
description: "The AI Development Lifecycle governance framework used to plan, build, and iteratively refine the curriculum. Covers phases, state tracking, audit trail, rule details, and construction plans."
tags: [aidlc, governance, process, audit, lifecycle]
---

# AIDLC Process

The **AIDLC (AI Development Lifecycle)** is an adaptive, AI-driven software development lifecycle framework that governs all changes to this repository. It was used to plan, build, and iteratively refine the curriculum through structured phases, audit trails, and quality remediation cycles.

## Lifecycle Phases

The AIDLC has three phases, each containing conditional stages:

### INCEPTION Phase — Planning & Architecture

| Stage | Always/Conditional | Purpose |
|---|---|---|
| Workspace Detection | Always | Scan for existing code, determine Greenfield vs. Brownfield, create `aidlc-state.md` |
| Reverse Engineering | Conditional (brownfield) | Analyze existing codebase |
| Requirements Analysis | Always (adaptive depth) | Capture intent, functional/non-functional requirements via Q&A |
| User Stories | Conditional | Break requirements into user stories |
| Workflow Planning | Always | Produce execution plan: stages to execute vs. skip |
| Application Design | Conditional | Architect application structure |
| Units Generation | Conditional | Decompose work into units of work with dependency ordering |

### CONSTRUCTION Phase — Implementation & Testing

| Stage | Always/Conditional | Purpose |
|---|---|---|
| Functional Design | Conditional (per-unit) | Domain entities, business rules, business logic |
| NFR Requirements | Conditional | Non-functional requirement analysis |
| NFR Design | Conditional | Performance, security, observability design |
| Infrastructure Design | Conditional | Cloud/deployment infrastructure |
| Code Generation | Always (per-unit) | Two-part: planning → generation (with approval gate) |
| Build and Test | Always | Build, unit tests, integration tests, verify success criteria |

### OPERATIONS Phase — Placeholder

Currently a placeholder for future deployment, monitoring, and maintenance workflows.

## State Tracking

[`aidlc-docs/aidlc-state.md`](../../aidlc-docs/aidlc-state.md) is the **single source of truth** for project lifecycle state. It contains:

- **Project Information**: Type (Greenfield), start date, current stage
- **Workspace State**: Existing code flag, workspace root path
- **Code Location Rules**: Application code → workspace root; Documentation → `aidlc-docs/` only
- **Extension Configuration**: Table of optional extensions (Security Baseline, Property-Based Testing) with enabled/disabled status
- **Execution Plan Summary**: Total stages, stages to execute, stages to skip
- **Stage Progress**: Checkbox tracker per phase (`[x]` completed, `[-]` skipped, `[ ]` pending)
- **Current Status**: Lifecycle phase, current stage, next stage, detailed narrative of completed work and remaining backlog

### Current State

As of the last update, the project is in the CONSTRUCTION phase with Build and Test completed. Major completed work includes:
- Mermaid plugin integration
- LangGraph unit addition and unit renumbering (Units 35–42 shifted)
- Curriculum consistency fixes across all 41+ units
- Diagram/text integration
- Multi-phase curriculum quality remediation (7 phases, re-review fixes, low-severity fixes)
- English/Japanese parity synchronization (Units 0–42)
- Language-specific asset separation (`en/assets/units/`)
- Tokenizer/BPE and LoRA/QLoRA units added (Units 35, 36)

**Remaining backlog**: Deeper prose parity review for older English units.

## Audit Trail

[`aidlc-docs/audit.md`](../../aidlc-docs/audit.md) is an append-only chronological log of every significant interaction between the user and the AI during the AIDLC process. Each entry follows a structured format:

```
## [Stage Name] [(Revision N)] [(Approval)]
**Timestamp** : ISO 8601
**User Input** : "..."
**AI Response** : "..."
**Context** : Stage execution / revision request / approval
---
```

The audit trail captures the initial user request (a career-change strategy toward AI engineering), 9 requirements revision cycles, planning approvals, and every code generation execution. This creates a complete, traceable history of every decision, revision, and approval.

## Rule Details

The [`.aidlc-rule-details/`](../../.aidlc-rule-details/) directory contains detailed procedural instructions for each AIDLC stage. These are the "implementation guide" files that the AI assistant reads and follows when executing a particular stage.

```
.aidlc-rule-details/
├── common/              # Cross-cutting rules (process overview, content validation, error handling, session continuity)
├── inception/           # One file per inception stage (workspace-detection.md, requirements-analysis.md, etc.)
├── construction/        # One file per construction stage (code-generation.md, build-and-test.md, etc.)
├── extensions/          # Optional extensions (security, testing)
└── operations/          # Placeholder
```

Each rule file contains: Purpose, Prerequisites, Numbered steps with checkboxes, Output artifacts (exact file paths), Approval gates, and Critical rules.

### Common Rules

Always loaded at workflow start:
- `process-overview.md` — Master workflow diagram and adaptive rules
- `session-continuity.md` — How to resume interrupted sessions
- `content-validation.md` — Content quality validation standards (Mermaid syntax, ASCII art, escaping)
- `question-format-guide.md` — How to format Q&A (A–E multiple choice options)

### Extension System

Extensions are opt-in modules loaded via `*.opt-in.md` files. When a user opts in, the corresponding full rule file is loaded. Extensions can be conditionally enabled/disabled via the `aidlc-state.md` extension configuration table.

## AIDLC Directory Structure

```
aidlc-docs/
├── aidlc-state.md                          # Central state tracking
├── audit.md                                # Append-only audit trail
├── inception/
│   ├── requirements/
│   │   ├── requirements.md                 # Full requirements definition
│   │   └── requirement-verification-questions.md
│   ├── plans/
│   │   ├── execution-plan.md               # Workflow plan with Mermaid diagram
│   │   └── unit-of-work-plan.md            # Work decomposition plan
│   └── application-design/
│       ├── unit-of-work.md                 # Unit (curriculum topic) definitions
│       ├── unit-of-work-dependency.md      # Inter-unit learning dependencies
│       └── unit-of-work-story-map.md       # Requirement-to-unit mapping
└── construction/
    ├── plans/
    │   ├── vitepress-mermaid-integration-code-generation-plan.md
    │   ├── unit32-langgraph-and-renumbering-code-generation-plan.md
    │   ├── curriculum-quality-fix-plan.md          # 7-phase quality remediation
    │   ├── curriculum-consistency-fix-plan.md
    │   ├── curriculum-low-severity-fix-plan.md
    │   ├── curriculum-re-review-findings.md
    │   ├── curriculum-re-review-fix-plan.md
    │   ├── curriculum-review-fix-plan.md
    │   └── curriculum-references-and-out-of-scope-plan.md
    ├── unit1/
    │   └── functional-design/
    │       ├── business-logic-model.md
    │       ├── business-rules.md
    │       └── domain-entities.md
    └── build-and-test/
        ├── build-and-test-summary.md
        ├── build-instructions.md
        ├── integration-test-instructions.md
        └── unit-test-instructions.md
```

## Relationship to the Curriculum

The AIDLC process is the **governance engine** and the curriculum repository is the **product** it governs:

| AIDLC Concept | Curriculum Manifestation |
|---|---|
| Requirements | "Confidence as an AI Engineer" + recruiter-evaluable portfolio |
| Units of Work | Curriculum units (Unit 1–42) |
| Unit Dependencies | Learning order matrix (classical ML → DL → NLP → LLM apps → agents) |
| Code Generation Plans | VitePress plugin integration, unit renumbering, content generation |
| Build & Test | `pnpm docs:build` verification, diagram rendering checks, 82 diagrams + 280 Python blocks validated |
| Iterative Fix Plans | Multi-phase curriculum quality remediation (technical errors, answer keys, diagram consistency) |

The `AGENTS.md` file at the repository root is the entry point for the AIDLC workflow. It mandates loading rule details from `.aidlc-rule-details/`, displaying a welcome message, and following the adaptive workflow for any software development request.

## Construction Plans

Construction plans are detailed code-generation plans created during the CONSTRUCTION phase. Each plan documents the exact steps, file changes, and verification criteria for a specific feature or fix:

- **Mermaid integration** — Added `vitepress-plugin-mermaid`, wrapped config, verified build
- **LangGraph unit + renumbering** — Added Unit 32, shifted Units 33–40 to 33–42, renamed asset directories
- **Curriculum quality fix** — 7-phase remediation: executable errors, technical inaccuracies, missing answer keys, diagram-text inconsistencies, cross-cutting issues, difficulty calibration, verification
- **Curriculum consistency fix** — Cross-unit consistency improvements
- **Low-severity fix** — Phases A–E for remaining quality issues
- **Re-review fix** — All findings fixed (H2/M19/L~50/G1–G6)

Each plan follows a two-part process: Part 1 (Planning — create plan, wait for approval) and Part 2 (Generation — execute the approved plan).
