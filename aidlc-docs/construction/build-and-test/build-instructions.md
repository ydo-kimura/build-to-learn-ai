# ビルド手順書 (Build Instructions)

VitePress Mermaid プラグイン統合におけるビルド手順について説明します。
本プロジェクトでは、環境の一貫性を保つため、すべてのビルドおよび依存関係の追加は必ず **DevContainer上** で実行されます。

## 前提条件 (Prerequisites)
- **ビルドツール (Build Tool)**: `pnpm` (LTS/最新安定版 `v11.4.0`)
- **Node.js**: `v22` (Active LTS)
- **実行環境**: DevContainer (`flamboyant_lovelace` 内の `/workspaces/job-change`)

---

## ビルド手順 (Build Steps)

### 1. 依存関係のインストール (Install Dependencies)
DevContainer 上で以下のコマンドを実行し、パッケージをインストールします。
```bash
# ホスト側（または DevContainer 端末内）で実行
docker exec -w /workspaces/job-change flamboyant_lovelace pnpm install
```
- **期待される結果**: `node_modules` に `vitepress-plugin-mermaid` および `mermaid` が正しく追加されること。

### 2. VitePress カリキュラムのビルド (Build VitePress)
コンパイルおよび静的 HTML ファイルの生成を行います。
```bash
docker exec -w /workspaces/job-change flamboyant_lovelace pnpm docs:build
```
- **期待される結果**: 警告やエラーなく `VitePress build complete` が出力されること。

## トラブルシューティング (Troubleshooting)

### エラー: `No package.json found in /`
- **原因**: `docker exec` 実行時に作業ディレクトリを指定していないため、コンテナのルートディレクトリで実行されてしまっています。
- **対策**: 必ず作業ディレクトリを `-w /workspaces/job-change` として明示的に指定して実行してください。
