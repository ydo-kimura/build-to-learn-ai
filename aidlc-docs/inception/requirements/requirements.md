# 転職戦略およびポートフォリオ要件定義書 (Requirements)

## 1. 意図分析 (Intent Analysis)

- **User Request** : AIエンジニアへの転職に向けた戦略とポートフォリオ構築。特定の技術（AIエージェント等）に固執せず、様々なビジネス要件に対して多様なAIパターンで実装できる能力をアピールしたい。現状は「LLMユーザー」の状態からのスタート。
- **Request Type** : 新規プロジェクト (Greenfield) / 戦略および自己学習・ポートフォリオ構築
- **Scope Estimate** : 全体戦略（基礎学習から多様なAI実装パターンの実践まで）
- **Complexity Estimate** : Moderate（中程度：学習フェーズから様々な要件に応じた実装を反復する必要がある）

## 2. 回答サマリー (Answers Summary)

- **活動の優先順位** : まずは「機械学習・LLMの基礎勉強」フェーズを最優先とし、「学習 → 実践 → アウトプット」のサイクルを回す。
- **注力技術領域** : 「AIエンジニア」としての多様な実装力。特定のアーキテクチャ（AIエージェント等）に限定せず、様々な要件に応じた複数のAI実装パターン（RAG、プロンプトチェーン、エージェント等）を経験・証明することを目指す。
- **技術スタック** : 機械学習・LLMの実装学習のベースとして「Python」に完全に集中する。「TypeScript/Next.js」や「Rust」は学習対象ではなく、学習や実践（実装）の過程において、デモの動作確認等で必要になった場合にのみ補助ツールとして利用する。
- **拡張機能 (Extensions)** :
  - セキュリティ (Security Baseline): 無効 (No)
  - テスト (Property-Based Testing): 無効 (No)

## 3. 機能要件 (Functional Requirements - Portfolio Actions)

「LLMユーザー」から「課題解決ができるAIエンジニア」へとステップアップし、その過程をポートフォリオ化するためのアプローチを以下のように定義する。

### 3.1. プロジェクトの初期ゴール (Initial Goal)

- **AIエンジニアとしての自信の獲得** : 「自分はAIエンジニアである」と自信を持って名乗れるだけの実装力と体系的な知識を身につけることを個人的な最初のゴールとする。
- **採用担当者からの客観的評価の獲得** : アウトプット（GitHubリポジトリ、技術ブログ等）を見たリクルーターや転職先の採用担当者・エンジニアから、「AIエンジニアとしての確かな実力とポテンシャルがある」と高く評価・判断してもらうことを対外的なゴールとする。

### 3.2. 統合サイクル（学習・ユースケース考案・実装・アウトプット）

各技術トピックごとに、以下のサイクルをシームレスに回していく。

1. **体系的学習 (Study)** : 機械学習の基礎、ニューラルネットワーク、Transformer、LLMの仕組みなどを体系的かつ網羅的に学習する。
2. **ユースケース考案 (Ideation)** : 学習した技術（RAG、チェーン、エージェント等）を適用できそうな具体的なビジネス要件や課題（ユースケース）を自ら考える。
3. **実践・実装 (Implementation)** : 考案したユースケースに基づき、PyTorchやLangChain等を用いて小規模なモデルやPoCを自ら実装し、「なぜそう動くのか」をコードレベルで体感・検証する。
4. **アウトプット (Output)** : 学習内容と実装経験を統合し、技術ブログ（Zenn, Qiitaなど）に継続的に記事として公開し、学習の軌跡をポートフォリオ化する。また、関連ツールへのOSSコントリビュートも適宜行う。

### 3.3. 実践過程での補助ツール利用

- 実装したAIシステムの動作確認を行う際など、学習や実践のプロセス上で必要になった場合にのみ、TypeScript/Next.jsやRust等をテスト用UI作成などの補助ツールとして適宜利用する（あくまで学習の補助として）。

## 4. 非機能要件 (Non-Functional Requirements - Strategic Criteria)

- **目的適合性** : すべての開発や執筆は、「AIエンジニアとしての実務能力の証明」に直結すること。
- **段階的アプローチ (Iterative)** : 最初から巨大なものを作らず、小さく作りながら公開・発信のサイクルを速く回すこと（Agileアプローチ）。
- **可視性 (Visibility)** : コードはGitHubで公開し、ドキュメント（READMEやアーキテクチャ図）を充実させ、リクルーターや採用側エンジニアがすぐに動かして技術力を評価できるように工夫すること。

## 5. VitePress Mermaid プラグイン追加要件 (VitePress Mermaid Plugin Integration)

### 5.1. 目的と機能要件 (Goal & Functional Requirements)

- **目的** : VitePressカリキュラムドキュメント内で Mermaid 記法を用いて記述された各種ダイアグラム（アーキテクチャ図、シーケンス図、ワークフロー等）を、ブラウザ上で動的かつ美しくレンダリングできるようにする。
- **導入パッケージ** :
  - `vitepress-plugin-mermaid` (安定版最新: `2.0.17`)
  - `mermaid` (安定版最新: `11.15.0`)
- **設定変更** :
  - `.vitepress/config.js` を更新し、`vitepress-plugin-mermaid` から `withMermaid` をインポートして既存の `defineConfig` 設定をラップする。
- **ダイアグラムの表示検証** :
  - カリキュラム内のドキュメント（例: 各種ユニットの index.md やロードマップ）に含まれる Mermaid 記法がエラーなく綺麗にレンダリングされることを確認する。

### 5.2. 非機能要件 (Non-Functional Requirements)

- **ビルドの安定性** : プラグイン導入後も、`pnpm docs:build` でエラーなくビルドが完了すること。
- **動作パフォーマンス** : サーバー起動時およびビルド時のオーバーヘッドが最小限に抑えられ、ホットリロードが正常に動作すること。
- **環境の不変性 (DevContainer)** : DevContainer 起動時にも必要なパッケージが正しくインストールされ、追加の手動セットアップなしで Mermaid が動作すること（`package.json` への追記による管理）。

## 6. OpenWiki PR自動更新要件 (2026-07-21)

### 6.1. 意図分析

- **User Request**: 既存の定期更新workflowとは分離してPR専用workflowを追加し、PR作成・更新時にOpenWikiを再生成して、その差分を同じPRへ追加する。
- **Request Type**: CI/CD Enhancement
- **Scope Estimate**: 新規PR専用workflow 1ファイルの追加。既存の定期更新workflowは維持する。
- **Complexity Estimate**: Simple。ただしsecrets、fork PR、checkout ref、書き込み権限を安全に扱う必要がある。

### 6.2. 機能要件

1. `.github/workflows/openwiki-pr-update.yml` を新設し、`pull_request` の `opened`、`synchronize`、`reopened` でOpenWiki更新処理を起動する。
2. 同一リポジトリ内のPRではPRのheadブランチをcheckoutし、OpenWiki生成差分がある場合だけコミットして同じheadブランチへpushする。
3. 既存の `.github/workflows/openwiki-update.yml` は定期・手動更新専用として維持し、従来どおり `openwiki/update` ブランチの更新PRを作成する。
4. OpenWiki生成結果に差分がなければ、空コミットや不要なpushを行わない。
5. 同じPRに対する重複実行を抑止する。

### 6.3. セキュリティ・運用要件

1. fork由来PRとDependabot PRでは、OpenWiki生成に必要なrepository secretsと書き込み可能な `GITHUB_TOKEN` が通常利用できないため、自動更新ジョブを実行しない。
2. `pull_request_target` は使用しない。PR内のコードを実行しながらbase repositoryのsecretsを渡す構成を避ける。
3. `OPENROUTER_API_KEY`、`LANGSMITH_API_KEY` など既存secretsの扱いを変更しない。
4. workflow-level permissionsは既存の `contents: write` と `pull-requests: write` を維持する。
5. リポジトリ設定でGitHub Actionsによるread/write権限が許可されていることを運用上の前提とする。
6. 既存・新規のOpenWiki workflowで使用する全GitHub Actionsを、最新安定版タグが指す完全な40文字コミットSHAへ固定する。
7. 各 `uses:` 行のSHA直後に、対応する完全なバージョン番号をコメントで記載する。
8. 2026-07-21時点の検証済みAction指定は次のとおりとする。
   - `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2`
   - `actions/setup-node@48b55a011bda9f5d6aeb4c2d9c7362e8dae4041e # v6.4.0`
   - `peter-evans/create-pull-request@5f6978faf089d4d20b00c7766989d076bb2fc7f1 # v8.1.1`
9. OpenWiki実行環境のNode.jsは `24` に固定する。

### 6.4. 受け入れ基準

- YAMLが正常に解析できる。
- PR専用workflowと定期・手動workflowの責務が分離されている。
- `schedule`／`workflow_dispatch` の既存フローが変更されない。
- 同一リポジトリPRではheadブランチ上でOpenWikiを生成し、差分だけを同じPRへ追加できる。
- fork／Dependabot PRではsecretsを参照する更新ジョブが安全にスキップされる。
- OpenWiki差分がない場合は成功終了し、コミットを作成しない。
- 両workflowのすべての `uses:` が完全なコミットSHAで固定され、右側に完全な安定版バージョンコメントがある。
- 両workflowの `actions/setup-node` がNode.js 24を設定する。
