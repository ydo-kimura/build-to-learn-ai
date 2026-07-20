# 結合テスト手順書 (Integration Test Instructions)

本結合テストでは、VitePress ドキュメント内（フロントエンド側）で Mermaid 記法を用いたダイアグラムが正しくビジュアルレンダリングされていることをブラウザで検証します。

## 目的

- Mermaid ブロック（` ```mermaid `）が生のテキストコードブロックとして出力されるのを防ぎ、動的な SVG 図面として表示されていることを確認します。

---

## 結合テスト手順 (Run Integration Tests)

### 1. ローカル開発サーバーの起動 (Start Dev Server)

DevContainer 上で開発サーバーを起動します（通常はコンテナ起動時に自動起動しているか、バックグラウンドで起動済みです）。
必要に応じて、以下のコマンドで手動起動することもできます。

```bash
docker exec -d -w /workspaces/job-change flamboyant_lovelace pnpm docs:dev
```

### 2. 対象画面へのアクセス (Access Target Page)

ブラウザを起動し、以下の Mermaid ダイアグラムが存在するカリキュラムページにアクセスします。

- **検証先URL** : `http://localhost:5173/curriculum/unit22_llm_evolution/`

### 3. 表示の検証 (Verify Visual Rendering)

以下の点を目視で確認します。

- **合格基準** :
  - `graph TD` などの Mermaid 構文テキスト（生のコードブロック）が消え、カラーリングおよびフォントの適用されたグラフィカルなフローチャート図面が表示されていること。
  - 図面の各ノード（四角形や丸型など）および接続矢印（アロー）が崩れずに正常に描写されていること。
  - VitePress のダークモード/ライトモードを切り替えた際にも、ダイアグラムが追従して見やすく表示されること。
