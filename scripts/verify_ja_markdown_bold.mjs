#!/usr/bin/env node

import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import { createMarkdownRenderer } from "vitepress";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SCRIPT_DIR, "..");
const DOCS_ROOT = path.join(ROOT, "docs");
const CURRICULUM_ROOT = path.join(DOCS_ROOT, "curriculum");

export async function collectMarkdownFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const paths = [];

  for (const entry of entries.sort((a, b) => a.name.localeCompare(b.name))) {
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      paths.push(...(await collectMarkdownFiles(entryPath)));
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      paths.push(entryPath);
    }
  }

  return paths;
}

function excerptForToken(sourceLines, token) {
  const [startLine = 0, endLine = startLine + 1] = token.map ?? [];
  return sourceLines
    .slice(startLine, endLine)
    .join(" ")
    .trim()
    .replace(/\s+/g, " ");
}

export function findExposedBold(source, file, markdown) {
  const sourceLines = source.split(/\r?\n/);
  const issues = [];

  for (const token of markdown.parse(source, {})) {
    if (!token.children) {
      continue;
    }

    const line = (token.map?.[0] ?? 0) + 1;
    const excerpt = excerptForToken(sourceLines, token);

    for (const child of token.children) {
      if (child.type !== "text" || !child.content.includes("**")) {
        continue;
      }

      issues.push({
        file,
        line,
        excerpt,
        text: child.content,
      });
    }
  }

  return issues;
}

export function formatIssue(issue) {
  return `${issue.file}:${issue.line}: exposed ** in rendered prose: ${issue.excerpt}`;
}

export async function verifyJapaneseCurriculum({
  curriculumRoot = CURRICULUM_ROOT,
  docsRoot = DOCS_ROOT,
} = {}) {
  const markdown = await createMarkdownRenderer(docsRoot);
  const files = await collectMarkdownFiles(curriculumRoot);
  const issues = [];

  for (const file of files) {
    const source = await readFile(file, "utf8");
    const relativeFile = path.relative(ROOT, file);
    issues.push(...findExposedBold(source, relativeFile, markdown));
  }

  return { files, issues };
}

async function main() {
  const { files, issues } = await verifyJapaneseCurriculum();

  if (issues.length > 0) {
    console.error("Japanese bold verification failed:");
    for (const issue of issues) {
      console.error(`- ${formatIssue(issue)}`);
    }
    return 1;
  }

  console.log(
    `Japanese bold verification passed: ${files.length} Markdown files`
  );
  return 0;
}

const isDirectRun =
  process.argv[1] &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href;

if (isDirectRun) {
  process.exitCode = await main();
}
