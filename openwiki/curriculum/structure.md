---
type: Reference
title: "Curriculum Structure"
description: "The 43-unit bilingual curriculum structure, 4-section unit template, chapter organization, cross-referencing patterns, and content conventions for the build-to-learn-ai repository."
tags: [curriculum, content, bilingual, pedagogy]
---

The curriculum is the core product of this repository: a 43-unit (Unit 0–42) learning path from classical ML to LLM-based AI agents, delivered as Markdown files in two language editions.

## Directory Layout

```
/docs/curriculum/                          # Japanese (root locale)
├── unit00_roadmap/index.md
├── unit01_linear_regression/index.md
├── ...
└── unit42_multiagent_customer_support/index.md

/docs/en/curriculum/                       # English (en locale)
├── unit00_roadmap/index.md
├── unit01_linear_regression/index.md
├── ...
└── unit42_multiagent_customer_support/index.md
```

Each unit is a single `index.md` file inside a `unitNN_<snake_case_name>/` directory. There are no sub-files — all content, code, and diagrams live in this one Markdown file.

## Chapter Organization

| Chapter                          | Units            | Capstone Unit |
| -------------------------------- | ---------------- | ------------- |
| Introduction                     | Unit 0 (Roadmap) | —             |
| Ch.1: ML Fundamentals            | Units 1–9        | Unit 9        |
| Ch.2: Deep Learning Fundamentals | Units 10–16      | Unit 16       |
| Ch.3: NLP & Modern Architectures | Units 17–21      | Unit 21       |
| Ch.4: LLM Applied & AI Agents    | Units 22–36      | —             |
| Ch.5: Real-World Capstones       | Units 37–42      | All 6 units   |

The sidebar in [`docs/.vitepress/config.js`](../../docs/.vitepress/config.js) mirrors this structure for both locales. Chapter 4 is the largest (15 units) because it covers the full LLM application stack: API usage, RAG (scratch, LangChain, LlamaIndex), prompt chaining, chatbots, ReAct agents, MCP, smolagents, LangGraph, Agent SDK, tokenizers, and LoRA fine-tuning.

## Unit Template

Every content unit (1–42) follows a rigid **4-section structure**:

| Section | JA Heading                              | EN Heading                     | Purpose                                                                                          |
| ------- | --------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------ |
| 1       | `## 1. [トピック名]の理解`              | `## 1. Understanding [Topic]`  | Conceptual explanation with everyday analogies, math intuition, diagrams, and business use cases |
| 2       | `## 2. 実装例 (Implementation Example)` | `## 2. Implementation Example` | Working code with step-by-step commentary                                                        |
| 3       | `## 3. 実践 (Practice)`                 | `## 3. Practice`               | Hands-on exercise with requirements, hints, and a different dataset                              |
| 4       | `## 4. 答え合わせ (Answer Key)`         | `## 4. Answer Key`             | Solution code in a collapsible `<details>` block with explanation                                |

### Recurring Elements

**Within Section 1:**

- Everyday analogies (e.g., "company approval process" for NNs, "meeting attention" for Transformers, "chef and kitchen" for LLM/Agent)
- `### 💡 具体的なビジネスユースケース` — 3 concrete enterprise scenarios
- Concept and workflow diagrams (SVG images)

**Within Section 2:**

- Multiple small code blocks (3–6 per section), each followed by `**【コードの解説】**` / `**Code walkthrough**` commentary
- `np.random.seed(42)` / `random_state=42` for reproducibility
- OpenAI API examples use `gpt-4o-mini` with `temperature=0.0` (evaluation) or `0.7` (creative)

**Within Section 3:**

- `**【課題の要件】**` / `**【Requirements】**` — numbered deliverables
- `**【ヒント】**` / `**Hint**` — scaffolding clues
- Capstone units (37+) require "design decision notes" as annotated code comments

**Within Section 4:**

- `<details><summary>` collapsible solution
- `### 解説` / `### Explanation` — post-solution analysis
- Capstones add comparison matrices (Approach A vs B tables)

### Unit 0 Exception

Unit 0 (roadmap) has a unique structure: ML/DL/LLM comparison matrix → curriculum structure (chapter listing with links) → how-to-learn guide → advanced topics not covered. It serves as the entry point for new learners.

## Bilingual Organization

### Translation Patterns

- **Headings**: Fully translated (e.g., `## 1. 線形回帰と正則化の理解` → `## 1. Understanding Linear Regression and Regularization`)
- **Code comments**: Japanese in JA version, English in EN version
- **Image paths**: JA uses relative paths (`../../assets/...`); EN uses absolute paths (`/en/assets/...`)
- **Content**: EN version is slightly more concise (e.g., Unit 0 JA ~17KB vs EN ~13KB)
- **Assets**: Separate `docs/assets/` and `docs/en/assets/` directories with per-unit image folders containing the same filenames

### Language Switcher

The VitePress locale config provides a language switcher in the nav bar that toggles between `/` and `/en/` while preserving the current page path. This is configured in [`docs/.vitepress/config.js`](../../docs/.vitepress/config.js) under the `locales` key.

## Cross-Referencing Patterns

Cross-references between units are pervasive and deliberate:

1. **Roadmap master links** (Unit 0) — Complete curriculum map with relative `../unitNN_name/index.md` links to every unit
2. **"Previously learned" references** — Nearly every unit opens by referencing what was learned in prior units (e.g., "In Unit 1, we learned linear regression...")
3. **Forward references** — Units preview what's coming next (e.g., Unit 22 previews Units 23–34)
4. **Appendix references** — Units requiring API keys or GPU link to the appendix for setup instructions
5. **Inter-unit comparisons** — Some units explicitly compare implementations (e.g., Unit 26 creates a 3-way comparison of RAG approaches across Units 24, 25, and 26)

## Content Conventions

### Pedagogical

- **Analogy first**: Every concept section opens with a relatable everyday analogy
- **Progressive complexity**: Scratch implementation first (NumPy) → framework next (PyTorch) → production tool last (API/SDK)
- **Anti-pattern warnings**: `⚠️ LLMで解こうとするアンチパターン` — cautions against using LLMs where classical ML/DL is better
- **Business use cases**: Always 3 concrete enterprise scenarios per unit

### Formatting

- Horizontal rules (`---`) separate major sections
- Emoji prefixes in sub-headings: `💡` (use cases), `📌` (key concepts), `🚨` (problems), `🤝` (solutions), `🧠` (design exercises)
- Tables for comparisons (ML/DL/LLM matrix, approach comparisons)
- VitePress alert blocks: `> [!TIP]`, `> [!IMPORTANT]`, `> [!NOTE]`

### Code

- All code blocks use ` ```python ` (occasionally ` ```bash ` for pip commands)
- Numbered step annotations in code comments: `# 1. データの準備`, `# 2. データの分割`
- Answer key code always wrapped in `<details><summary>` collapsible HTML

## Asset Naming

Each unit's `images/` directory follows a consistent naming convention, managed by the [visual asset pipeline](../workflows/visual-pipeline.md):

| File                       | Type       | Description                                                                                           |
| -------------------------- | ---------- | ----------------------------------------------------------------------------------------------------- |
| `hero.png` (or `hero.svg`) | Raster/SVG | Banner image at top of unit                                                                           |
| `diagram-concept.svg`      | Vector SVG | Conceptual architecture diagram                                                                       |
| `diagram-workflow.svg`     | Vector SVG | Process/workflow diagram                                                                              |
| `concept.png`              | Raster     | Rasterized version of concept SVG (for fallback)                                                      |
| Unit-specific SVGs         | Vector SVG | Some units have topic-specific diagrams (e.g., `diagram-sigmoid.svg`, `diagram-confusion-matrix.svg`) |
