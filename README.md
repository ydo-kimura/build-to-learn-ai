# Build to Learn: AI

[日本語](README.ja.md) | English

Build to Learn: AI is a hands-on curriculum that progresses from machine learning fundamentals to LLMs, RAG, AI agents, and real-world capstone projects. The learning site is built with VitePress.

## Published site

[https://ydo-kimura.github.io/build-to-learn-ai/](https://ydo-kimura.github.io/build-to-learn-ai/)

## Curriculum

- Machine learning foundations, including regression, classification, tree models, clustering, and dimensionality reduction
- Deep learning with neural networks, CNNs, and transfer learning
- NLP from TF-IDF, Word2Vec, and LSTMs to Attention and Transformers
- LLM APIs, prompt design, RAG, evaluation, and AI agents
- Capstone projects covering fraud detection, contract processing, demand forecasting, and multi-agent systems

## Prerequisites

- Node.js 24
- pnpm 11
- Python 3 for diagram and Mermaid validation

## Setup

```bash
pnpm install --frozen-lockfile
```

## Local development

```bash
pnpm run docs:dev
```

## Validation and build

```bash
pnpm run docs:check-mermaid
pnpm run docs:check-diagrams
pnpm run docs:build
pnpm run docs:preview
```

Every push to `main` triggers GitHub Actions to build the VitePress site and deploy it to GitHub Pages.
