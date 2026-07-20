---
type: Reference
title: "Operations Runbook"
description: "Build commands, development workflow, CI/CD pipeline, DevContainer setup, and operational guidance for the build-to-learn-ai curriculum site."
tags: [operations, runbook, ci-cd, devcontainer, deployment]
---

## Development Workflow

### Local Development

```bash
# Install Node.js dependencies
pnpm install

# Start VitePress dev server (http://localhost:5173)
pnpm docs:dev

# Build for production
pnpm docs:build

# Preview production build
pnpm docs:preview
```

The dev server binds to `0.0.0.0:5173` (configured in `package.json` `docs:dev` script: `vitepress dev docs --host 0.0.0.0`). The VitePress source root is the `docs/` subdirectory — all curriculum content, assets, and config live there.

### DevContainer

A [DevContainer](../../.devcontainer/devcontainer.json) is provided for VS Code / GitHub Codespaces. It:

- Builds from [`Dockerfile`](../../.devcontainer/Dockerfile)
- Mounts host SSH directory (`~/.ssh` → `/home/node/.ssh`) for Git operations
- Installs GitHub CLI (`gh`) and configures zsh as default shell
- Runs `pnpm install` on container creation
- Forwards port 5173
- Installs VS Code extensions: ESLint, Prettier, Volar (Vue language support)

The DevContainer was added specifically to enable SSH-based Git operations and GitHub CLI access from within the development environment.

### Python Environment

Python dependencies for curriculum code examples are listed in [`/requirements.txt`](../../requirements.txt). Key libraries:

| Library                                                                                            | Used In                     |
| -------------------------------------------------------------------------------------------------- | --------------------------- |
| numpy, pandas, scikit-learn                                                                        | Units 1–9 (Classical ML)    |
| torch, torchvision                                                                                 | Units 10–16 (Deep Learning) |
| nltk, gensim                                                                                       | Units 17–18 (NLP)           |
| openai, tiktoken                                                                                   | Units 22–23 (LLM API)       |
| chromadb                                                                                           | Unit 24 (Vector DBs)        |
| langchain, langchain-openai, langchain-core, langchain-community                                   | Unit 25                     |
| langgraph                                                                                          | Unit 32                     |
| llama-index-core, llama-index-readers-file, llama-index-llms-openai, llama-index-embeddings-openai | Unit 26                     |
| mcp                                                                                                | Unit 30                     |
| smolagents                                                                                         | Units 31, 37, 40            |
| pydantic                                                                                           | Unit 39                     |
| streamlit                                                                                          | Unit 28                     |
| optuna                                                                                             | Unit 8                      |
| xgboost                                                                                            | Unit 5                      |

In Google Colab, install with:

```bash
!pip install -r https://raw.githubusercontent.com/ydo-kimura/build-to-learn-ai/main/requirements.txt
```

## CI/CD Pipeline

[`.github/workflows/openwiki-update.yml`](../../.github/workflows/openwiki-update.yml) is a scheduled GitHub Actions workflow that automatically updates the OpenWiki documentation:

- **Trigger**: Daily at 08:00 UTC (`cron: "0 8 * * *"`) or manual dispatch
- **Node.js**: Version 22
- **Process**: Installs OpenWiki globally via npm, runs `openwiki code --update --print`
- **Model**: Uses OpenRouter with `z-ai/glm-5.2` model
- **PR Creation**: Uses `peter-evans/create-pull-request@v7` to create a PR on branch `openwiki/update`
- **Paths**: Commits changes to `openwiki/`, `AGENTS.md`, `CLAUDE.md`, and the workflow file itself

The workflow requires these secrets:

- `OPENROUTER_API_KEY` — For LLM API access
- `LANGSMITH_API_KEY` — For LangChain tracing (optional)

### Pre-Commit Hooks

A [Husky](https://typicode.github.io/husky/) pre-commit hook (`.husky/pre-commit`) runs:

1. **lint-staged** (`pnpm exec lint-staged`) — Runs Prettier on staged files per `.lintstagedrc` (all files: `prettier --ignore-path .prettierignore --ignore-unknown --write`).
2. **Diagram checks** (`pnpm run docs:check-diagrams`) — Runs the full verification suite: `verify_curriculum_diagrams.py` + `verify_curriculum_diagram_geometry.py` + `verify_mermaid_blocks.py` (see Build Verification below).

Prettier is configured via `.prettierrc` (2-space indent, 80-char print width, double quotes, ES5 trailing commas). `.prettierignore` excludes `pnpm-lock.yaml`.

### No Test Pipeline

The repository does not currently have a dedicated test CI workflow. Build verification is performed manually via `pnpm docs:build` (which chains `docs:check-diagrams` before `vitepress build docs`) during the AIDLC Build and Test stage. The pre-commit hook also runs `docs:check-diagrams`, which executes `verify_curriculum_diagrams.py`, `verify_curriculum_diagram_geometry.py`, and `verify_mermaid_blocks.py` in sequence.

## Build Verification

When modifying curriculum content, verify the build:

```bash
# Full VitePress build (runs all diagram checks first, then builds)
pnpm docs:build

# Run all diagram verification only (diagrams + geometry + mermaid)
pnpm run docs:check-diagrams

# Run individual verification scripts
python3 scripts/verify_curriculum_diagrams.py          # SVG existence, alt text, bridge sentences
python3 scripts/verify_curriculum_diagram_geometry.py   # SVG structural integrity, runtime sync
python3 scripts/verify_mermaid_blocks.py                # Mermaid syntax validation
```

The `docs:build` script chains `docs:check-diagrams` (which itself runs `verify_curriculum_diagrams.py` → `verify_curriculum_diagram_geometry.py` → `verify_mermaid_blocks.py`) before `vitepress build docs`, so all diagram and Mermaid checks run automatically as part of every build. The pre-commit hook also runs `docs:check-diagrams` to catch issues before they reach CI.

The AIDLC build-and-test stage validates:

- VitePress build succeeds without errors
- All 82 SVG diagrams render correctly
- 280+ Python code blocks across JA and EN are syntactically valid
- Section structure is consistent across units

## Git Conventions

### Conventional Commits

All commits must follow [Conventional Commits](https://www.conventionalcommits.org/) format, enforced by [`.agent/rules/git-commit-rules.md`](../../.agent/rules/git-commit-rules.md):

```
<type>[optional scope]: <description>

[optional body]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `build`, `ci`, `revert`

**Rules**:

- Description: 50 chars max, no trailing period
- Language: English for `/commit` workflow, Japanese for `/commit-ja` workflow
- No emoji, slang, or vague messages ("update", "fix", "change" are prohibited)
- Body: 72-char line wrap for English

### Branch Strategy

The repository uses feature branches with PR-based merges. Recent merge history shows branches named like `fix/curriculum-quality-review`, `feat/add-unit32-langgraph`, `feat/devcontainer-ssh-gh-cli`, `cursor/curriculum-unit-visuals`, etc.

### PR Template

PRs use a [bilingual template](../../.github/PULL_REQUEST_TEMPLATE.md) (Japanese with English parentheticals) that includes:

- Description and linked issue
- Type of change (bug fix, new feature, breaking change, documentation update)
- Testing checklist
- Self-review checklist

## Agent Configuration

### AGENTS.md

The [`AGENTS.md`](../../AGENTS.md) file at the repository root is the entry point for the AIDLC workflow. It mandates:

- Loading rule details from `.aidlc-rule-details/`
- Displaying a welcome message at workflow start
- Following the adaptive workflow for any software development request
- Content validation (Mermaid syntax, ASCII art, escaping)
- Question format guidelines (A–E multiple choice)
- Following `.agent/rules/curriculum-diagram-authoring-rules.md` when creating or editing curriculum diagrams

### .agent/ Directory

The `.agent/` directory contains always-on rules and workflows for AI assistants:

- **Rules** (`/.agent/rules/`): `senior-engineer-conduct.md` (safety over obedience, no silent failures, CoT enforcement), `git-commit-rules.md`, `indexing-codebase.md` (index before act, grep don't guess, verify after change), `language-strategies.md` (Japanese for user-facing output, English for code)
- **Workflows** (`/.agent/workflows/`): `ask`, `commit`, `commit-ja`, `discard`, `explain`, `grasp`, `plan`, `review`
- **Skills** (`/.agent/skills/`): `indexing-awareness` (directory structure indexing), `knowledge-cutoff-awareness`

### CLAUDE.md and GEMINI.md

[`CLAUDE.md`](../../CLAUDE.md) contains the OpenWiki section marker (auto-managed by the OpenWiki update workflow). [`GEMINI.md`](../../GEMINI.md) directs to `AGENTS.md` and `.agent/` rules.
