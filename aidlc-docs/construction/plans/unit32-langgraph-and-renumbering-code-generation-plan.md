# Code Generation Plan - LangGraph Integration & Global Renumbering

本計画は、新規ユニット「Unit 32: LangGraph: グラフベースのステートフルエージェント」の追加と、それに伴う既存の Unit 32〜39 の Unit 33〜40 へのリナンバリングおよび全参照の置換を安全に実行するための詳細なコード生成計画です。

---

## 1. ユニットのコンテキストと依存関係 (Unit Context & Dependencies)

- **新規ユニット**: `Unit 32: LangGraph: グラフベースのステートフルエージェント`
- **ポジショニング**: 
  - Unit 31（smolagentsによるコード生成型エージェント）と Unit 33（商用Agent SDKによる汎用エージェント）の間に位置し、状態遷移（グラフ）ベースのワークフロー制御という新しいパラダイムを提示します。
- **前提参照**:
  - Unit 25（LangChainによるRAG構築の基礎）
  - Unit 29（スクラッチReActによる自律ループの原理）
  - Unit 30（MCPによる外部ツール統合）
  - Unit 31（smolagentsによるコード生成型自律エージェント）

---

## 2. 実行ステップ一覧 (Execution Steps)

### フェーズ1: LangGraph 新規教材の作成
- [ ] **Step 1**: `curriculum/unit32_langgraph_stateful_agents/index.md` ファイルの新規作成
  - **導入ブリッジ文**: 「Unit 31ではsmolagentsのコード生成型エージェントを学びましたが、本ユニットではグラフベースのワークフロー制御という別のパラダイムを学びます」
  - **1. 説明フェーズ**: ノード（Node）、エッジ（Edge）、ステート（State/TypedDict）の核心概念、smolagents（コード生成型）との比較テーブル、主要ユースケース（条件分岐、ヒューマン・イン・ザ・ループ）の解説。
  - **2. 実装例**: 「カスタマーサポートチケットの自動振り分け（classify ➔ billing / technical / escalate）」を模擬するシミュレーションPythonコード（OpenAI APIキー不要、ローカル完結）とMermaidによるグラフ可視化。
  - **3. 実践課題**: 上記に「重要チケットは自動応答前に人間の承認を待つヒューマン・イン・ザ・ループ」ノードを追加する課題。
  - **4. 答え合わせ**: 実践課題の完全な解答コード（`<details>` タグ囲み）。

### フェーズ2: 既存フォルダのリナンバリング
- [ ] **Step 2**: `curriculum/` 配下の既存のフォルダ名を、N ➔ N+1 にそれぞれリネーム（git mv を使用）
  - `unit32_agent_sdk_general_agents` ➔ `unit33_agent_sdk_general_agents`
  - `unit33_agent_sdk_coding_agents` ➔ `unit34_agent_sdk_coding_agents`
  - `unit34_llm_harness_capstone` ➔ `unit35_llm_harness_capstone`
  - `unit35_multimodal_fraud_detection` ➔ `unit36_multimodal_fraud_detection`
  - `unit36_knowledge_structuring_agent` ➔ `unit37_knowledge_structuring_agent`
  - `unit37_guardrails_evaluation_harness` ➔ `unit38_guardrails_evaluation_harness`
  - `unit38_timeseries_price_optimizer` ➔ `unit39_timeseries_price_optimizer`
  - `unit39_multiagent_customer_support` ➔ `unit40_multiagent_customer_support`

### フェーズ3: グローバル参照の置換と辻褄合わせ
- [ ] **Step 3**: `.vitepress/config.js` の更新
  - sidebar の `Ch4: LLM Applied` および `Ch5: Capstones` の各エントリについて、`unit32_`〜`unit39_` のパスおよびユニット番号の表記を `unit33_`〜`unit40_` にシフト。
  - `Ch4` に新規 `unit32_langgraph_stateful_agents` のエントリを追加。
- [ ] **Step 4**: 日本語トップページ `index.md` および英語トップページ `en/index.md` の更新
  - features セクションの `第4章` の詳細に `LangGraph` と `Agent SDK` を含める形に更新。
  - 具体的なユニット総数表記があれば「全40ユニット」に更新（またはDRY化）。
- [ ] **Step 5**: `tasks-export.csv` の更新
  - `unit32` 〜 `unit39` のタスク番号と参照パスを `unit33` 〜 `unit40` にシフト。
  - 新規 `unit32` (LangGraph) のタスク行を追加。
- [ ] **Step 6**: 各ユニットマークダウン内の参照および Appendix の更新
  - `appendix/index.md` の L72「一瞬で全39ユニット」をDRY化、または「全40ユニット」に更新。
  - 他のマークダウン内の相対リンク（例: `../unit32_...` などのパス）やテキスト参照（例: 「Unit 39では」など）を N+1 に一括置換。

### フェーズ4: 検証とビルド
- [ ] **Step 7**: DevContainer 上での VitePress ビルド検証
  - `env NODE_OPTIONS="--max-old-space-size=1024" pnpm docs:build` を実行し、全40ユニット構成で VitePress がエラーなく正常に静的ビルドされることを確認。
  - リンク切れや Mermaid 構文エラーがないか確認。

---

## 3. ストーリートレーサビリティ (Story Traceability)

- **実装対象**: カリキュラム全体の整合性・信頼性のさらなる強化、および最先端エージェント技術（LangGraph）の追加。
- **検証基準**: `pnpm docs:build` が警告・エラーなしで 100% 成功すること。
