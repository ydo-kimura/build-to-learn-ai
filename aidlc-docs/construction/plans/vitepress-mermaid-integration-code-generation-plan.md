# コード生成計画 (Code Generation Plan) - VitePress Mermaid Plugin Integration

本計画は、VitePress カリキュラムに `vitepress-plugin-mermaid` および `mermaid` を導入し、生の Mermaid 記述（コードブロック）をブラウザ上で美しく動的にレンダリングするための実装手順です。

## 1. ユニットコンテキスト (Unit Context)
- **ユニット名**: `vitepress-mermaid-integration`
- **依存関係**: なし (独立した設定変更)
- **影響範囲**: `package.json`, `.vitepress/config.js`
- **対象ストーリー**: 「VitePress ドキュメント内での Mermaid ダイアグラム自動レンダリングの実現」

---

## 2. 詳細実装ステップ (Detailed Execution Steps)

### ステップ 1: package.json の更新
- [x] 既存の `package.json` の `devDependencies` に以下のパッケージを追加します。
  - `"vitepress-plugin-mermaid": "^2.0.17"`
  - `"mermaid": "^11.15.0"`
- **ファイルパス**: `/Volumes/External/Documents/job-change/package.json`

### ステップ 2: .vitepress/config.js の更新
- [x] `.vitepress/config.js` を変更します。
  - `import { withMermaid } from 'vitepress-plugin-mermaid'` をインポート。
  - 既存の `export default defineConfig({ ... })` を `export default withMermaid(defineConfig({ ... }))` に書き換え、Mermaid プラグインを有効化します。
- **ファイルパス**: `/Volumes/External/Documents/job-change/.vitepress/config.js`

### ステップ 3: パッケージのインストール (DevContainer 上での実行)
- [x] ユーザーの指示に従い、ホスト側ではなく **DevContainer 内**で `pnpm install` を実行します。
- **実行コマンド**: DevContainer 内で `pnpm install`
- **期待結果**: `node_modules` にプラグインおよび依存関係が正しく追加されること。

### ステップ 4: ローカルビルド検証 (DevContainer 上での実行)
- [x] **DevContainer 内**で `pnpm docs:build` を実行し、VitePress の静的ビルドプロセスがエラーなく完了することを確認します。
- **実行コマンド**: DevContainer 内で `pnpm docs:build`
- **期待結果**: `VitePress build complete` が成功出力されること。

---

## 3. 成功基準 (Success Criteria)
- `package.json` と `.vitepress/config.js` が正しく変更されている。
- パッケージが DevContainer 上で正常にインストールされている。
- カリキュラム内の Mermaid ダイアグラム表示箇所（例: `curriculum/unit22_llm_evolution/index.md`）で、生のコードではなく図面としてレンダリングされること（Build and Test フェーズで検証）。
