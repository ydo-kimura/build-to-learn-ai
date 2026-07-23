#!/usr/bin/env node

import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import { createMarkdownRenderer } from "vitepress";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SCRIPT_DIR, "..");
const DOCS_ROOT = path.join(ROOT, "docs");

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

function headingText(tokens, headingIndex) {
  const inline = tokens[headingIndex + 1];
  return inline?.type === "inline" ? inline.content : "";
}

function maskFrontmatter(source) {
  const lines = source.split(/\r?\n/);
  const firstContentLine = lines.findIndex((line) => line.trim() !== "");

  if (firstContentLine === -1 || lines[firstContentLine].trim() !== "---") {
    return source;
  }

  const closingLine = lines.findIndex(
    (line, index) => index > firstContentLine && line.trim() === "---"
  );
  if (closingLine === -1) {
    return source;
  }

  for (let index = firstContentLine; index <= closingLine; index += 1) {
    lines[index] = "";
  }
  return lines.join("\n");
}

export function findH2Separators(source, file, markdown) {
  const tokens = markdown.parse(maskFrontmatter(source), {});
  const issues = [];

  for (let index = 0; index < tokens.length - 1; index += 1) {
    const token = tokens[index];
    const next = tokens[index + 1];

    if (
      token.type !== "hr" ||
      next.type !== "heading_open" ||
      next.tag !== "h2"
    ) {
      continue;
    }

    issues.push({
      file,
      line: (token.map?.[0] ?? 0) + 1,
      heading: headingText(tokens, index + 1),
    });
  }

  return issues;
}

export function formatIssue(issue) {
  return `${issue.file}:${issue.line}: remove the horizontal rule before H2 "${issue.heading}"`;
}

export async function verifyMarkdown({
  docsRoot = DOCS_ROOT,
  root = ROOT,
} = {}) {
  const markdown = await createMarkdownRenderer(docsRoot);
  const files = await collectMarkdownFiles(docsRoot);
  const issues = [];

  for (const file of files) {
    const source = await readFile(file, "utf8");
    const relativeFile = path.relative(root, file);
    issues.push(...findH2Separators(source, relativeFile, markdown));
  }

  return { files, issues };
}

async function main() {
  const { files, issues } = await verifyMarkdown();

  if (issues.length > 0) {
    console.error("H2 separator verification failed:");
    for (const issue of issues) {
      console.error(`- ${formatIssue(issue)}`);
    }
    return 1;
  }

  console.log(
    `H2 separator verification passed: ${files.length} Markdown files`
  );
  return 0;
}

const isDirectRun =
  process.argv[1] &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href;

if (isDirectRun) {
  process.exitCode = await main();
}
