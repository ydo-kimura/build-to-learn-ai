---
trigger: always_on
globs: ["**/*"]
---

# DevContainer Execution Rules

**Activation:** This rule is **ALWAYS ON** when this repository has an active DevContainer.

## Authoritative execution environment

The DevContainer is the authoritative environment for repository commands. Do not use host-machine results as a substitute for the container's dependencies, credentials, Git configuration, or runtime behavior.

## Required procedure

1. Discover the active DevContainer and its repository workspace before executing repository commands. Do not hard-code a container name; it can change when the container is rebuilt.
2. Run repository shell commands inside that container at the mounted repository workspace. This includes:
   - `git status`, staging, commits, pushes, and branch inspection;
   - `gh auth status`, GitHub CLI requests, and pull-request operations;
   - package-manager commands, builds, tests, and runtime-dependent validation.
3. Treat `gh auth status` inside the DevContainer as the authoritative authentication result. A host-machine `gh` failure does not block GitHub work when the DevContainer is authenticated.
4. If Git reports dubious ownership in the DevContainer, add only the mounted workspace as a Git safe directory inside that same container, then retry the Git command.
5. If no suitable DevContainer is running, report the blocker and ask the user to start or select one. Do not silently fall back to host execution.

## Process ownership and runtime safety

1. Never stop, restart, send signals to, or otherwise modify a process that was not started by the current task.
2. Treat an already-running development server, watcher, preview server, or other runtime as user-owned unless the current task has explicit evidence that it started that exact process.
3. For rendered-page validation, use an existing user-owned server without changing its lifecycle. If it cannot serve the required revision, report that condition and ask before starting a separate server or changing any process.
4. A non-interactive command such as `pnpm run docs:build` may be run in the DevContainer when validation is in scope, but it must not be combined with process discovery followed by a kill or restart action.

## Allowed host-side work

Host-side file editing through the shared workspace and Docker container discovery are allowed. Host-side results must not determine GitHub authentication, Git readiness, build success, or pull-request readiness while the DevContainer is available.

## Current workspace convention

The active repository workspace is mounted at `/workspaces/build-to-learn-ai`. Use the actual discovered container name with that workspace path; do not reuse a stale container name from a previous task.
