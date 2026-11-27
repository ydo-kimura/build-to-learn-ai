---
trigger: always_on
globs: ["**/*"]
---

# Main Synchronization Rules

**Activation:** This rule is **ALWAYS ON** for Git work after a merge and before new work begins.

## Purpose

Prevent new branches and pull requests from being based on stale history. The required outcome is that new work starts from the latest remote default branch without losing or hiding existing local changes.

## Trigger Conditions

Run this procedure when the user states or requests any of the following:

- The current pull request was merged.
- Work on a new issue, task, or unrelated change should begin.
- A new work branch should be created.

Do not run it when the user explicitly asks to continue the current unmerged branch or names a different base branch.

## Required Procedure

1. Resolve the repository and intended worktree.
2. When relevant, verify the reported pull request is merged using a read-only check.
3. Inspect the current branch and changes:

   ```bash
   git status --short --branch
   ```

4. Inspect worktrees before switching branches:

   ```bash
   git worktree list
   ```

5. If the intended worktree is clean and no other worktree already holds `main`, switch to `main`:

   ```bash
   git switch main
   ```

6. Update `main` using fast-forward only:

   ```bash
   git pull --ff-only origin main
   ```

7. Verify local `main` and `origin/main` resolve to the same commit before starting new work.
8. Create the new work branch from this updated `main` following the Branch Naming rules below.

The invariant is: **a new work branch must start from the latest `origin/main` unless the user explicitly selects another base.**

## Branch Naming (Conventional Branch)

This naming rule **always applies** to every new work branch and worktree, even when branching from a base other than `main`.

- **REQUIRED**: Follow **Conventional Branch** naming: `<type>/<short-kebab-description>` where `<short-kebab-description>` uses lowercase letters, digits, and hyphens only.
  - Allowed types (aligned with `git-commit-rules.md`, plus `hotfix` / `release`): `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `build`, `perf`, `style`, `revert`, `hotfix`, `release` (e.g., `docs/curriculum-review-fixes`, `fix/unit07-svg-arrows`).
- **PROHIBITED**: Never use AI or agent/tool prefixes for branch names (e.g., `codex/`, `claude/`, `cursor/`, `gemini/`, `ai/`, `agent/`).

## Dirty Worktree Safety

If tracked modifications or untracked files are present:

- Do not switch branches.
- Do not automatically stash, commit, discard, move, or overwrite the changes.
- Do not use `git reset --hard`, `git checkout --`, `git clean`, or an equivalent destructive command.
- Report the current branch and affected paths to the user.
- Continue only after the existing work is safely resolved or the user gives explicit direction.

## Divergence and Failure Handling

If `git pull --ff-only origin main` cannot fast-forward:

- Stop the synchronization procedure.
- Do not create a merge commit or start a rebase automatically.
- Report the local and remote branch relationship.
- Ask for direction before altering history.

If `main` is already checked out in another worktree:

- Do not attempt to check it out again.
- Identify the existing `main` worktree.
- Update that worktree only when it is clean and within the current task's scope.
- Otherwise report the worktree conflict and preserve its state.

## Branch Retention

- Do not automatically delete merged local branches.
- Do not automatically delete merged remote branches.
- Branch cleanup is a separate action and requires an explicit user request.

## Completion Check

Before creating the next work branch, confirm:

- The selected base is `main`, unless the user specified otherwise.
- The base worktree is clean.
- Local `main` equals `origin/main`.
- The new branch is created after synchronization, not before it.
- The new branch name follows Conventional Branch (`<type>/<short-kebab-description>`) and does not use any AI/agent prefix.

