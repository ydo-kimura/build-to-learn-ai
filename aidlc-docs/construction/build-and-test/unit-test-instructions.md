# 単体テスト手順書 (Unit Test Execution)

本統合において実行される単体検証テスト（ビルドおよび構文エラーテスト）の手順です。

## テストの目的
- `package.json` と `.vitepress/config.js` の変更が、VitePress の設定構文エラーを引き起こさないことを検証します。
- 静的アセットのバンドルが問題なく終了することを確認します。

---

## テスト実行手順 (Run Unit Tests)

### 1. ビルド検証の実行 (VitePress Compiler Test)
DevContainer 上でビルドテストを実行します。
```bash
docker exec -w /workspaces/job-change flamboyant_lovelace pnpm docs:build
```

### 2. 結果の検証 (Verify Results)
- **期待される結果**:
  - `devDependencies` に追加されたパッケージが正常に解決され、バンドル処理が完了すること。
  - レンダリング時に Vue または VitePress が警告を吐かないこと。
  - ビルド完了メッセージ（例: `build complete in X.XXs`）が出力されること。

### 3. テスト結果の判定
- `docs:build` が成功して終了コード `0` を返した場合、単体テストは合格 (Pass) とみなされます。
