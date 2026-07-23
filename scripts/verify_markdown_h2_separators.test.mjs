import assert from "node:assert/strict";
import test from "node:test";

import { createMarkdownRenderer } from "vitepress";

import {
  findH2Separators,
  formatIssue,
} from "./verify_markdown_h2_separators.mjs";

const markdown = await createMarkdownRenderer("docs");

test("detects a horizontal rule immediately before H2", () => {
  const source = ["Paragraph.", "", "---", "", "## Practice"].join("\n");
  const issues = findH2Separators(source, "broken.md", markdown);

  assert.deepEqual(issues, [
    {
      file: "broken.md",
      line: 3,
      heading: "Practice",
    },
  ]);
  assert.match(formatIssue(issues[0]), /^broken\.md:3:/);
});

test("detects alternate Markdown horizontal-rule syntax before H2", () => {
  const source = ["Paragraph.", "", "***", "", "## Practice"].join("\n");
  assert.equal(findH2Separators(source, "broken.md", markdown).length, 1);
});

test("allows H2 without a preceding horizontal rule", () => {
  const source = ["Paragraph.", "", "## Practice"].join("\n");
  assert.deepEqual(findH2Separators(source, "valid.md", markdown), []);
});

test("allows a horizontal rule before H3", () => {
  const source = ["Paragraph.", "", "---", "", "### Detail"].join("\n");
  assert.deepEqual(findH2Separators(source, "valid.md", markdown), []);
});

test("allows a horizontal rule when prose appears before the next H2", () => {
  const source = [
    "Paragraph.",
    "",
    "---",
    "",
    "More prose.",
    "",
    "## Practice",
  ].join("\n");
  assert.deepEqual(findH2Separators(source, "valid.md", markdown), []);
});

test("ignores frontmatter delimiters", () => {
  const source = ["---", "title: Example", "---", "", "## Practice"].join("\n");
  assert.deepEqual(findH2Separators(source, "frontmatter.md", markdown), []);
});

test("ignores horizontal-rule text inside fenced code", () => {
  const source = [
    "```markdown",
    "---",
    "",
    "## Example",
    "```",
    "",
    "## Practice",
  ].join("\n");
  assert.deepEqual(findH2Separators(source, "code.md", markdown), []);
});
