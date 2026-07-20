# カリキュラム整合性修正計画 (Curriculum Consistency Fix Plan)

本計画は、構成の再編（LangChain/LlamaIndex RAG の追加や Agent SDK ユニットの増設）に伴い、第4章および第5章全体の各カリキュラム Markdown ファイル内に残ってしまっている古いユニット番号の参照、相対リンクの崩れ、および設定ファイル `.vitepress/config.js` のサイドバー定義のズレを一括して修正し、全体の整合性（辻褄）を合わせるための手順です。

## 1. ユニットコンテキスト (Unit Context)

- **ユニット名** : `curriculum-consistency-alignment`
- **対象ストーリー** :
  - LlamaIndex ユニット（Unit 26）における LangChain (Unit 25) への言及漏れの修正（ユーザー様からの的確なご指摘に完全対応）。
  - 設定ファイル `config.js` のサイドバー定義（全39ユニットへの拡張と、抜け落ちていた `unit23_llm_api` の追加、全番号・パスのズレの同期）。
  - カリキュラム全体のユニット記述における古い参照（全33ユニット表記、および古いユニット番号）のアップデート。

---

## 2. 詳細実装ステップ (Detailed Execution Steps)

### ステップ 1: .vitepress/config.js のサイドバー再構築

- [x] 日本語ロケール（`locales.root`）の第4章および第5章のサイドバー項目を修正し、抜けていた `Unit 23` を追加した全39ユニットの正しい構成（Unit 22〜Unit 39）に同期します。
- [x] 英語ロケール（`locales.en`）の第4章および第5章のサイドバー項目も同様に正しい構成に同期します。
- **ファイルパス** : `/Volumes/External/Documents/job-change/.vitepress/config.js`

### ステップ 2: curriculum/unit26_llamaindex_basics_rag/index.md の修正 (ご指摘箇所・3者比較拡張)

- [x] 冒頭 (L7) において、手組みRAGへの言及（Unit 24）と、LangChain RAG（Unit 25）への言及の繋がりを整理します。
- [x] 練習問題「## 3. 実践」内のシナリオを拡張し、アプローチA（手組み）、アプローチB（LlamaIndex）に加え、 **「アプローチC（LangChain RAG / Unit 25）」** を評価対象に加えた3者比較意思決定問題へアップグレードします。
- [x] 解答例「## 4. 答え合わせ」内の「設計意思決定マトリクス」テーブルに「アプローチC（LangChain）」の列を追加し、開発スピード・拡張性・内部ロジックの透明性のトレードオフを完璧に整理します。
- [x] 最終意思決定の解説コメントにも、手組み・LangChain・LlamaIndexの3者の使い分けのプロフェッショナルな視点を追記し、教材全体の辻褄を合わせます。
- **ファイルパス** : `/Volumes/External/Documents/job-change/curriculum/unit26_llamaindex_basics_rag/index.md`

### ステップ 3: curriculum/appendix/index.md の修正 (ユニット総数表記の更新)

- [x] 冒頭 (L70) および Linear インポート説明 (L87) 内の古い総数表記「全33ユニット」を、現在の構成である「全39ユニット」に更新します。
- **ファイルパス** : `/Volumes/External/Documents/job-change/curriculum/appendix/index.md`

### ステップ 4: curriculum/unit23_llm_api/index.md のタイポ修正

- [x] 冒頭 (L5) における Appendix への相対リンクアンカーのタイポ（`of 取得`）を、正しい日本語（`の取得`）に修正します。
- **ファイルパス** : `/Volumes/External/Documents/job-change/curriculum/unit23_llm_api/index.md`

### ステップ 5: curriculum/unit25_langchain_basics_rag/index.md の前提参照修正

- [x] 冒頭 (L15) における手組みRAGの前提参照が `Unit 23` となっているのを、正しい `Unit 24` に修正します。
- **ファイルパス** : `/Volumes/External/Documents/job-change/curriculum/unit25_langchain_basics_rag/index.md`

### ステップ 6: curriculum/unit31_smolagents_code_agent/index.md の前提参照修正

- [x] 冒頭 (L7) において、前提となる Chaining およびチャットボットを `Unit 25, 26` と指しているのを、正しい `Unit 27` (Chaining) と `Unit 28` (Chatbot) に修正します。
- **ファイルパス** : `/Volumes/External/Documents/job-change/curriculum/unit31_smolagents_code_agent/index.md`

### ステップ 7: curriculum/unit34_llm_harness_capstone/index.md の章末参照修正

- [x] 冒頭 (L7) における第4章の範囲記述 `Unit 19〜24` を、正しい `Unit 22〜33` に修正します。
- [x] 本ユニットを最終ユニット `Unit 25` と指している箇所 (L9) を、正しい第5章の最初のユニットである `Unit 34` に修正します。
- **ファイルパス** : `/Volumes/External/Documents/job-change/curriculum/unit34_llm_harness_capstone/index.md`

### ステップ 8: curriculum/unit36_knowledge_structuring_agent/index.md の前提参照修正

- [x] 冒頭 (L7) における LlamaIndex の参照 `Unit 24`（正しくは `Unit 26`）、および smolagents の参照 `Unit 27`（正しくは `Unit 31`）をそれぞれ修正します。
- **ファイルパス** : `/Volumes/External/Documents/job-change/curriculum/unit36_knowledge_structuring_agent/index.md`

### ステップ 9: curriculum/unit39_multiagent_customer_support/index.md の前提参照修正

- [x] 冒頭 (L7) における smolagents の参照 `Unit 27`（正しくは `Unit 31`）を修正します。
- **ファイルパス** : `/Volumes/External/Documents/job-change/curriculum/unit39_multiagent_customer_support/index.md`

### ステップ 10: ローカルビルドおよび表示検証 (DevContainer 上での実行)

- [x] **DevContainer 内** で `pnpm docs:build` を実行し、全39ユニット構成の静的ビルドプロセスがエラーなく完了することを確認します。
- [x] カリキュラム上のロードマップや各ユニットのサイドバー項目が正しい順序・正しいテキストで表示され、デッドリンクがないことを確認します。

---

## 3. 成功基準 (Success Criteria)

- 設定ファイル `.vitepress/config.js` において、`Unit 22` から `Unit 39` までのすべてのカリキュラムファイルへのルーティングおよびサイドバー表示が崩れず同期されていること。
- ユーザー様がご指摘された `Unit 26` (LlamaIndex) の内容が、手組みRAG (Unit 24) および LangChain RAG (Unit 25) を正しく前提知識・対比対象として踏まえた丁寧な3者比較（実践問題・マトリクス・適用判断）に修正されていること。
- 第4章および第5章全体の Markdown ファイルに含まれるユニット番号の参照関係に矛盾がないこと。
- `pnpm docs:build` がエラーなく正常終了すること。
