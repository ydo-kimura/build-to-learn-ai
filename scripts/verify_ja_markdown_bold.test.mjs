import assert from "node:assert/strict";
import test from "node:test";

import { createMarkdownRenderer } from "vitepress";

import { findExposedBold, formatIssue } from "./verify_ja_markdown_bold.mjs";

const markdown = await createMarkdownRenderer("docs");

test("accepts correctly delimited Japanese bold text", () => {
  const source = "メニューから **「ランタイム」** を選択します。";
  assert.deepEqual(findExposedBold(source, "valid.md", markdown), []);
});

test("detects bold delimiters exposed next to Japanese prose", () => {
  const source = [
    "# Fixture",
    "",
    "1. **「ランタイム」→「ランタイムを接続解除して削除」**で戻します。",
  ].join("\n");

  const issues = findExposedBold(source, "broken.md", markdown);

  assert.equal(issues.length, 1);
  assert.equal(issues[0].file, "broken.md");
  assert.equal(issues[0].line, 3);
  assert.match(issues[0].text, /^\*\*/);
  assert.match(formatIssue(issues[0]), /^broken\.md:3:/);
});

test("allows literal bold markers in inline code", () => {
  const source = "Markdown のボールド記号は `**` です。";
  assert.deepEqual(findExposedBold(source, "inline-code.md", markdown), []);
});

test("allows literal bold markers in fenced code", () => {
  const source = ["```text", "**literal**", "```"].join("\n");
  assert.deepEqual(findExposedBold(source, "fenced-code.md", markdown), []);
});
