# Build to Learn: AI

日本語 | [English](README.md)

Build to Learn: AI は、機械学習の基礎から LLM、RAG、AI エージェント、実務向けの総合演習までを体系的に学ぶための実践カリキュラムです。教材サイトは VitePress で構築されています。

## 公開サイト

[https://ydo-kimura.github.io/build-to-learn-ai/](https://ydo-kimura.github.io/build-to-learn-ai/)

## 学習内容

- 回帰、分類、木モデル、クラスタリング、次元削減などの機械学習基礎
- ニューラルネットワーク、CNN、転移学習などのディープラーニング
- TF-IDF、Word2Vec、LSTM、Attention、Transformer などの自然言語処理
- LLM API、プロンプト設計、RAG、評価、AI エージェント
- 不正検知、契約書処理、需要予測、マルチエージェントなどの総合演習

## 必要な環境

- Node.js 24
- pnpm 11
- Python 3（教材内の図と Mermaid の検証に使用）

## セットアップ

```bash
pnpm install --frozen-lockfile
```

## ローカル開発

```bash
pnpm run docs:dev
```

## 検証とビルド

```bash
pnpm run docs:check-mermaid
pnpm run docs:check-diagrams
pnpm run docs:build
pnpm run docs:preview
```

`main` ブランチへの push で GitHub Actions が VitePress サイトをビルドし、GitHub Pages にデプロイします。
