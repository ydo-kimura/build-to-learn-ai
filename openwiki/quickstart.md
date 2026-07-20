---
type: Reference
title: "Build to Learn: AI — OpenWiki Quickstart"
description: "Entry point for the build-to-learn-ai repository wiki. Covers what the project is, how to run it, key directories, and links to all documentation sections."
tags: [quickstart, entrypoint, navigation]
---

## What Is This Repository?

**Build to Learn: AI** is a bilingual (Japanese / English) AI engineering curriculum built with [VitePress](https://vitepress.dev). It covers 43 units (Unit 0–42) organized into 5 chapters, progressing from classical machine learning through deep learning, NLP, and LLM-based AI agents to real-world capstone projects. The curriculum is designed for hands-on learning via Google Colab, with every unit containing concept explanations, implementation examples, practice exercises, and answer keys.

The repository also contains an **AIDLC (AI Development Lifecycle)** governance framework that was used to plan, build, and iteratively refine the curriculum through structured phases, audit trails, and quality remediation cycles.

## Quick Start

```bash
# Install dependencies
pnpm install

# Start dev server (http://localhost:5173)
pnpm docs:dev

# Build for production
pnpm docs:build

# Preview production build
pnpm docs:preview
```

Python dependencies for curriculum code examples are listed in `/requirements.txt` and can be installed in Colab via:

```bash
!pip install -r https://raw.githubusercontent.com/ydo-kimura/build-to-learn-ai/main/requirements.txt
```

## Key Directories

| Path                    | Purpose                                                                                   |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| `/docs/curriculum/`     | Japanese curriculum content (root locale) — 43 unit directories                           |
| `/docs/en/`             | English curriculum content (mirror structure)                                             |
| `/docs/assets/units/`   | Canonical source for unit images (hero, SVG diagrams, concept PNGs)                       |
| `/docs/public/assets/`  | Deployed copy of assets served by VitePress                                               |
| `/docs/.vitepress/`     | VitePress config, theme, and custom CSS                                                   |
| `/scripts/`             | Python scripts for SVG generation, hero deployment, diagram integration, and verification |
| `/aidlc-docs/`          | AIDLC process documentation (state, audit, plans, designs)                                |
| `/.aidlc-rule-details/` | Rule detail files for the AIDLC workflow                                                  |
| `/.agent/`              | AI agent rules, workflows, and skills for repository maintenance                          |
| `/.github/workflows/`   | CI/CD (OpenWiki auto-update workflow)                                                     |

## Documentation Sections

- [Architecture Overview](./architecture/overview.md) — VitePress site architecture, locale configuration, theme customization, and build pipeline.
- [Curriculum Structure](./curriculum/structure.md) — Unit template, chapter organization, bilingual setup, and content conventions.
- [Visual Asset Pipeline](./workflows/visual-pipeline.md) — SVG generation, hero image deployment, diagram integration, and verification scripts.
- [AIDLC Process](./domain/aidlc-process.md) — AI Development Lifecycle governance, state tracking, audit trail, and construction plans.
- [Operations Runbook](./operations/runbook.md) — Build commands, dev workflow, CI/CD, and DevContainer setup.

## Curriculum at a Glance

| Chapter      | Units       | Theme                                                                                                             |
| ------------ | ----------- | ----------------------------------------------------------------------------------------------------------------- |
| Introduction | Unit 0      | Roadmap, learning philosophy, ML/DL/LLM comparison                                                                |
| Chapter 1    | Units 1–9   | Classical ML (regression, classification, trees, boosting, clustering, PCA, cross-validation)                     |
| Chapter 2    | Units 10–16 | Deep Learning (NN from scratch, PyTorch, CNN, transfer learning)                                                  |
| Chapter 3    | Units 17–21 | NLP & Modern Architectures (TF-IDF, Word2Vec, RNN/LSTM, Transformer)                                              |
| Chapter 4    | Units 22–36 | LLM Applied & AI Agents (API, RAG, LangChain, LlamaIndex, MCP, smolagents, LangGraph, Agent SDK, Tokenizer, LoRA) |
| Chapter 5    | Units 37–42 | Real-World Capstones (fraud detection, knowledge structuring, guardrails, pricing, multi-agent support)           |

## Agent Rules

The repository includes AI agent configuration under `/.agent/` with always-on rules for [senior engineer conduct](../.agent/rules/senior-engineer-conduct.md), [git commit conventions](../.agent/rules/git-commit-rules.md), [project structure indexing](../.agent/rules/indexing-codebase.md), [language strategies](../.agent/rules/language-strategies.md), and [curriculum diagram authoring rules](../.agent/rules/curriculum-diagram-authoring-rules.md). These rules govern how AI assistants work within this repository.

## Backlog

- **`.agent/` workflows and skills** — Eight workflow files (`ask`, `commit`, `discard`, `explain`, `grasp`, `plan`, `review`) and two skills (`indexing-awareness`, `knowledge-cutoff-awareness`) are not yet documented in detail. Source: `/.agent/workflows/` and `/.agent/skills/`.
- **`agent-sdk.md`** — A 120KB reference document about Agent SDK categories and architecture. Not yet integrated into the wiki. Source: `/agent-sdk.md`.
- **GitHub templates** — Issue and PR templates exist under `/.github/` but are not documented. Source: `/.github/ISSUE_TEMPLATE/`, `/.github/PULL_REQUEST_TEMPLATE.md`.
