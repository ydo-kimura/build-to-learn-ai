---
type: Reference
title: "Architecture Overview"
description: "VitePress site architecture, locale configuration, theme customization, Mermaid integration, and build pipeline for the build-to-learn-ai curriculum site."
tags: [architecture, vitepress, build, theme]
---

# Architecture Overview

The site is a static-generated VitePress application with bilingual locale support, Mermaid diagram rendering, and a custom theme. The curriculum content lives entirely in Markdown files — there is no backend or database.

## VitePress Configuration

The central config file is [`docs/.vitepress/config.js`](../../docs/.vitepress/config.js). It wraps the VitePress config with `withMermaid()` from `vitepress-plugin-mermaid` to enable inline Mermaid diagram rendering.

### Locale Configuration

The site defines two locales, each with its own complete sidebar and navigation:

| Locale         | Path   | Language | Label   |
| -------------- | ------ | -------- | ------- |
| Root (default) | `/`    | `ja-JP`  | 日本語  |
| English        | `/en/` | `en-US`  | English |

Each locale's sidebar is organized into 6 groups: Introduction + 5 Chapters. Unit titles and navigation labels are fully translated. The VitePress locale switcher lets users toggle between `/` and `/en/` while preserving the current page path.

### Build Exclusions

The config excludes AIDLC docs, node_modules, `.agent/`, and `README.md` from the build via `srcExclude`:

```javascript
srcExclude: [
  "**/aidlc-docs/**",
  "**/node_modules/**",
  "**/.agent/**",
  "README.md",
];
```

### Dead Link Handling

The config includes `ignoreDeadLinks` patterns that exclude OpenWiki internal references to repository-internal files (aidlc-docs, .aidlc-rule-details, .devcontainer, .agent, scripts, .github) from VitePress dead-link checking. This allows OpenWiki documentation to link to source files that are not part of the published site without breaking the build.

```javascript
ignoreDeadLinks: [
  /^\.\/\.\.\/\.\.\/aidlc-docs\/(aidlc-state|audit)$/,
  /^\.\/\.\.\/\.\.\/\.aidlc-rule-details\/index$/,
  /^\.\/\.\.\/\.\.\/\.devcontainer\/Dockerfile$/,
  /^\.\/\.\.\/\.\.\/\.agent\/rules\/git-commit-rules$/,
  /^\.\/\.\.\/\.\.\/\.github\/PULL_REQUEST_TEMPLATE$/,
  /^\.\/\.\.\/\.agent\/rules\/(senior-engineer-conduct|git-commit-rules|indexing-codebase|language-strategies)$/,
  /^\.\/\.\.\/\.\.\/scripts\/index$/,
];
```

### Mermaid Plugin

The `vitepress-plugin-mermaid` integration was added in a dedicated AIDLC construction phase. Vite's `optimizeDeps` includes `mermaid` and `dayjs` for pre-bundling. Mermaid diagrams in curriculum markdown use standard fenced code blocks with the `mermaid` language tag and are rendered client-side.

## Theme Customization

The custom theme extends VitePress's DefaultTheme with one CSS file: [`docs/.vitepress/theme/custom.css`](../../docs/.vitepress/theme/custom.css).

### Layout Adjustments

- **Wider layout**: `--vp-layout-max-width` is set to `min(1920px, calc(100vw - 32px))` — significantly wider than the VitePress default.
- **Sidebar**: Width increased to 340px (from default ~272px) to accommodate long Japanese unit titles. Left-aligned with 24px inset.
- **Content area**: `VPContent.has-sidebar` padding adjusted to align with the wider sidebar.
- **NavBar**: Title area width synchronized with sidebar width.

### Custom CSS Classes

The curriculum markdown uses two custom classes defined in `custom.css`:

| Class           | Usage                                                                                    |
| --------------- | ---------------------------------------------------------------------------------------- |
| `.unit-hero`    | Hero banner images at the top of each unit — styled with rounded corners and shadow      |
| `.unit-diagram` | SVG concept/workflow diagrams within sections — centered with rounded corners and shadow |

## Build Pipeline

```
Markdown (docs/curriculum/*.md, docs/en/curriculum/*.md)
    ↓
VitePress build (pnpm docs:build)
    ↓
Static HTML/CSS/JS in docs/.vitepress/dist/
```

### Build Scripts

Defined in [`package.json`](../../package.json):

| Script         | Command                                                | Purpose                                          |
| -------------- | ------------------------------------------------------ | ------------------------------------------------ |
| `docs:dev`     | `vitepress dev docs --host 0.0.0.0`                    | Dev server with hot reload                       |
| `docs:build`   | `pnpm run docs:check-diagrams && vitepress build docs` | Production build (runs all diagram checks first) |
| `docs:preview` | `vitepress preview docs`                               | Preview built site                               |

### Dependencies

The site depends on VitePress 1.6+, Vue 3.4+, Mermaid 11+, and the VitePress Mermaid plugin. Node.js 22 is used in CI.

### Asset Serving

Static assets are served from `docs/public/`. The repository maintains two parallel asset trees:

- `docs/assets/units/<slug>/images/` — canonical source (where generation scripts write)
- `docs/public/assets/units/<slug>/images/` — deployed copy (served by VitePress)

The [visual asset pipeline](../workflows/visual-pipeline.md) writes to `docs/assets/` and the `docs/public/assets/` copy serves as the runtime source. Both trees must stay in sync; the pipeline documents the complementary reference and structural checks.

## DevContainer

A [DevContainer](../../.devcontainer/devcontainer.json) configuration is provided for VS Code / Codespaces. It:

- Builds from a custom Dockerfile
- Mounts the host SSH directory for Git access
- Installs GitHub CLI and zsh
- Runs `pnpm install` on container creation
- Forwards port 5173 (VitePress dev server)
- Installs ESLint, Prettier, and Volar extensions

The DevContainer was added to enable SSH-based Git operations and GitHub CLI access from within the development environment, as documented in the [operations runbook](../operations/runbook.md).
