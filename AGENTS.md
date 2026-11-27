# AGENTS.md — Agent Instructions Index

This file is the single entry point for all AI coding agents working in this repository.
Read and follow the detailed rules, skills, and workflows under `.agent/` according to your task.

## Rules (`.agent/rules/`)

- **[aidlc-workflow.md](.agent/rules/aidlc-workflow.md)** — Adaptive AWS AI-DLC software development workflow (read at the start of software development requests; overrides built-in workflows)
- **[language-strategies.md](.agent/rules/language-strategies.md)** — Language rules (Japanese for user-facing output/artifacts, English for code)
- **[senior-engineer-conduct.md](.agent/rules/senior-engineer-conduct.md)** — Engineering conduct and quality standards
- **[devcontainer-execution-rules.md](.agent/rules/devcontainer-execution-rules.md)** — Running build, test, `git`/`gh`, and CLI commands inside the DevContainer
- **[git-main-sync-rules.md](.agent/rules/git-main-sync-rules.md)** — Main branch sync, worktree usage, and Conventional Branch naming
- **[git-commit-rules.md](.agent/rules/git-commit-rules.md)** — Commit message conventions
- **[curriculum-diagram-authoring-rules.md](.agent/rules/curriculum-diagram-authoring-rules.md)** — Curriculum diagram authoring and verification rules
- **[indexing-codebase.md](.agent/rules/indexing-codebase.md)** — Codebase indexing guidelines
- **[graft.md](.agent/rules/graft.md)** — Graft repo context graph usage (read before codebase exploration; `graft map`, `graft ask`, `graft grep`, `graft skeleton`, `graft callers`, `graft build`)
- **[openwiki.md](.agent/rules/openwiki.md)** — OpenWiki documentation navigation and update policy

## Skills (`.agent/skills/`)

- **[indexing-awareness](.agent/skills/indexing-awareness/SKILL.md)** — Structural index and dependency tracing for RAG-like context retrieval
- **[knowledge-cutoff-awareness](.agent/skills/knowledge-cutoff-awareness/SKILL.md)** — Anchoring to current system date/time to prevent knowledge-cutoff errors

## Workflows (`.agent/workflows/`)

- **[ask.md](.agent/workflows/ask.md)** — Answering questions
- **[plan.md](.agent/workflows/plan.md)** — Planning changes
- **[grasp.md](.agent/workflows/grasp.md)** — Grasping codebase context
- **[explain.md](.agent/workflows/explain.md)** — Explaining code or concepts
- **[review.md](.agent/workflows/review.md)** — Reviewing changes
- **[commit.md](.agent/workflows/commit.md)** — Generating commit messages from staged changes (English, read-only)
- **[commit-ja.md](.agent/workflows/commit-ja.md)** — Generating commit messages from staged changes (Japanese, read-only)
- **[discard.md](.agent/workflows/discard.md)** — Summarizing the current session for a fresh handoff (read-only)
