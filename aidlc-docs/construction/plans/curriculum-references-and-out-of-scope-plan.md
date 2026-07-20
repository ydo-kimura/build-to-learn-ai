# カリキュラム参照リンク・スコープ外トピック拡充 計画

**作成日**: 2026-07-02  
**依頼**: Unit 0 の「扱わないトピック」拡充、各チャプターへの深掘り参照リンク追加（Hugging Face Tokenizers の例に倣う）  
**方針（再発防止）**: 修正詳細の決定・実施・章ごとのレビューは Fable 5 が担当する

---

## 1. 背景と課題

### 現状

- Unit 0 末尾に「扱わないトピック」3件のみ（LoRA、streaming、BPE）。BPE のみ Hugging Face に言及するが **URL 未記載**
- カリキュラム内の外部リンクは Appendix 中心で、各 Unit には **深掘り用の参照リンクセクションが未整備**
- Unit 番号・章構成は **6箇所以上に重複定義** されており、追記時に不整合が起きやすい

### 不整合が起きる箇所（SSoT が分散）

| 箇所                                    | 内容                                             |
| :-------------------------------------- | :----------------------------------------------- |
| `.vitepress/config.js`                  | サイドバー（ja / en）、Unit 番号・タイトル・パス |
| `curriculum/unit00_roadmap/index.md`    | 全 Unit 一覧、章番号、相対リンク                 |
| `curriculum/unitNN_*/index.md` ×40      | 本文中の「Unit X」「第Y章」言及                  |
| `index.md`（ホーム）                    | 5章の feature カード                             |
| `tasks-export.csv`                      | 進捗管理用タスク（Unit タイトル）                |
| `en/curriculum/unit00_roadmap/index.md` | 英語版（現状スコープ外節なし）                   |

**リスク例**

- Unit 0 に「Unit 23 を前提」と書いたが、番号変更後に Unit 24 になっている
- `../unit23_llm_api/index.md` のパス typo でビルドは通るがリンク切れ
- 外部 URL が移転・404 になる

---

## 2. 設計方針

### 2.1 単一の正（SSoT）を導入する

**新規ファイル**: `curriculum/curriculum-registry.yaml`

各 Unit について以下を1か所で管理する:

```yaml
units:
  - id: 23
    slug: unit23_llm_api
    chapter: 4
    title_ja: "LLM API の利用とプロンプトエンジニアリング"
    title_en: "LLM API Usage & Prompting"
    prerequisites: [22]
    further_reading:
      - label: "OpenAI API リファレンス（Chat Completions）"
        url: "https://platform.openai.com/docs/api-reference/chat"
        type: official
      - label: "OpenAI — Prompt engineering ガイド"
        url: "https://platform.openai.com/docs/guides/prompt-engineering"
        type: guide
```

**スコープ外トピック**も同ファイルの `out_of_scope` セクションで管理:

```yaml
out_of_scope:
  - id: bpe-tokenizers
    title_ja: "サブワードトークナイザ（BPE など）"
    reason_ja: "本カリキュラムはトークン化の実装より、LLM を API で使うことに集中"
    prerequisite_units: [17, 20]
    links:
      - label: "Hugging Face — Tokenizers ドキュメント"
        url: "https://huggingface.co/docs/tokenizers"
        type: official
```

→ Unit 0 の該当節は **手書きではなく、この YAML から生成または照合** する（Phase 0 で検証スクリプト、Phase 1 で Unit 0 本文更新）。

### 2.2 リンク記法の統一ルール

| 種類               | ルール                                                                        | 例                                                                                   |
| :----------------- | :---------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| **カリキュラム内** | 必ず相対パス + 表示名。裸の「Unit 23」だけは Unit 0 / スコープ外節では禁止    | `[Unit 23](../unit23_llm_api/index.md)`                                              |
| **範囲指定**       | 各端を個別リンク                                                              | `[Unit 22](../unit22_llm_evolution/index.md)〜[Unit 23](../unit23_llm_api/index.md)` |
| **章番号**         | 「第4章」と書く場合、Unit 0 の章見出しと一致させる（第1章=Unit 1–9 等）       | 変更時は registry の `chapter` フィールドを先に更新                                  |
| **外部**           | 必ず `[サービス名 — ページ名](https://...)` 形式。裸 URL 禁止                 | `[Hugging Face — Tokenizers](https://huggingface.co/docs/tokenizers)`                |
| **Appendix**       | 絵文字アンカー禁止（過去の教訓）。`../appendix/index.md` + セクション名の平文 | 既存 Unit 27–29 パターンに合わせる                                                   |

### 2.3 各 Unit の「さらに学ぶ」セクション

**見出し（統一）**: `### 📚 さらに学ぶ（参考リンク）`  
**配置**: 「1. 〜の理解」セクションの末尾、`---` の直前（実装例の前）  
**件数**: 2〜4 リンク（多すぎると初学者が迷う）  
**内訳の目安**:

- 1件: 公式ドキュメント（必須）
- 1件: チュートリアル / ガイド
- 0〜1件: 論文・概念解説（Unit 20 Transformer など理論系）
- 0〜1件: 本カリキュラムの関連 Unit への内部リンク（前提・発展）

**VitePress 表示**: 通常の Markdown リンクで問題なし（Appendix と同様）。

---

## 3. Unit 0「扱わないトピック」の拡充案

現行 3 件に加え、**カリキュラムで触れず実務では頻出**のトピックを追加する。いずれも「本編に含めない理由」と「前提 Unit（リンク付き）」「深掘り URL」をセットで記載する。

| ID                 | トピック                                 | 扱わない理由（要約）                               | 前提 Unit（リンク） | 深掘りリンク（案）                                                                                                                     |
| :----------------- | :--------------------------------------- | :------------------------------------------------- | :------------------ | :------------------------------------------------------------------------------------------------------------------------------------- |
| `lora`             | LLM ファインチューニング（LoRA / QLoRA） | API 利用に集中。重み更新は環境・GPU コストが大きい | 15, 22, 23          | [HF — PEFT](https://huggingface.co/docs/peft), [HF — TRL](https://huggingface.co/docs/trl)                                             |
| `streaming`        | ストリーミング応答                       | UI 実装の詳細はフレームワーク依存                  | 23, 28              | [OpenAI — Streaming](https://platform.openai.com/docs/api-reference/streaming)                                                         |
| `bpe`              | サブワードトークナイザ（BPE）            | トークン化実装はスコープ外                         | 17, 20              | [HF — Tokenizers](https://huggingface.co/docs/tokenizers)                                                                              |
| `mlops`            | MLOps・本番デプロイ・モデル監視          | 学習パイプライン構築が主目的                       | 9, 16               | [Google ML — MLOps 概要](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) |
| `distributed`      | 分散学習・マルチ GPU                     | 単一マシン PoC に集中                              | 11, 16              | [PyTorch — Distributed](https://pytorch.org/tutorials/beginner/dist_overview.html)                                                     |
| `object-detection` | 物体検出・セグメンテーション             | CNN 基礎まで。検出は別領域                         | 14, 15              | [torchvision — Detection](https://pytorch.org/vision/stable/models.html#object-detection)                                              |
| `speech`           | 音声認識・音声合成                       | 非音声データが主                                   | 14                  | [OpenAI — Audio API](https://platform.openai.com/docs/guides/audio)                                                                    |
| `gnn`              | グラフニューラルネットワーク             | 表・画像・テキストが主                             | 10, 11              | [PyG — チュートリアル](https://pytorch-geometric.readthedocs.io/)                                                                      |
| `rl-full`          | 強化学習（ゲーム・制御）全般             | Unit 22 で RLHF のみ言及                           | 22                  | [Spinning Up in RL](https://spinningup.openai.com/)                                                                                    |
| `vector-ops`       | ベクトル DB の本番運用・スケール         | RAG 概念と API 利用まで                            | 24, 25              | [Chroma docs](https://docs.trychroma.com/), [LangChain — Vector stores](https://python.langchain.com/docs/concepts/vectorstores/)      |

**Unit 0 本文の構成案（拡充後）**

1. 導入1文（現行維持）
2. **テーブル形式**（一覧性）: トピック | 理由 | 前提 | 深掘り
3. またはカテゴリ別リスト（LLM 系 / ML 運用系 / DL 応用系）— ユーザー好みで Phase 1 開始前に1つに決定

**注意**: 上記は「スコープ外の案内」であり、新 Unit を増やす計画ではない。将来 Unit を追加する場合は registry → config.js → unit00 → 全 cross-ref の順で更新する（§5 チェックリスト）。

---

## 4. 各 Unit の深掘りリンク割当（全40 Unit）

registry の `further_reading` に登録し、各 `index.md` に反映する。以下は **Fable 5 が確定した割当案**（実装時に URL の生存確認を行う）。

### 第1章（Unit 1–9）— ML

| Unit | 参照リンク（案）                                       |
| :--- | :----------------------------------------------------- |
| 1    | scikit-learn LinearRegression, Ridge 公式              |
| 2    | scikit-learn metrics, imbalanced-learn（不均衡データ） |
| 3    | scikit-learn preprocessing, SVM 公式                   |
| 4    | scikit-learn tree / ensemble                           |
| 5    | XGBoost 公式ドキュメント                               |
| 6    | scikit-learn cluster                                   |
| 7    | scikit-learn decomposition (PCA)                       |
| 8    | scikit-learn GridSearchCV, Optuna ドキュメント         |
| 9    | scikit-learn Pipeline, joblib 永続化                   |

### 第2章（Unit 10–16）— DL

| Unit | 参照リンク（案）                               |
| :--- | :--------------------------------------------- |
| 10   | 3Blue1Brown NN シリーズ（概念）, backprop 解説 |
| 11   | PyTorch 公式チュートリアル                     |
| 12   | PyTorch optim, loss functions                  |
| 13   | PyTorch dropout / regularization               |
| 14   | PyTorch torchvision CNN                        |
| 15   | torchvision transfer learning, ImageNet        |
| 16   | torch.save 公式, 転移学習ベストプラクティス    |

### 第3章（Unit 17–21）— NLP

| Unit | 参照リンク（案）                                        |
| :--- | :------------------------------------------------------ |
| 17   | scikit-learn TfidfVectorizer, NLTK（任意）              |
| 18   | gensim Word2Vec, Mikolov 論文（概念）                   |
| 19   | PyTorch RNN チュートリアル, LSTM 解説                   |
| 20   | Attention Is All You Need（論文）, HF Transformers 概念 |
| 21   | seq2seq / NMT 概説, 関連 Unit 20 リンク                 |

### 第4章（Unit 22–34）— LLM & Agent

| Unit | 参照リンク（案）                                            |
| :--- | :---------------------------------------------------------- |
| 22   | OpenAI models 概要, HF ブログ（LLM スケーリング）           |
| 23   | OpenAI prompt engineering, streaming ガイド                 |
| 24   | OpenAI embeddings, cosine similarity 解説                   |
| 25   | LangChain 公式 docs, LCEL                                   |
| 26   | LlamaIndex 公式 docs                                        |
| 27   | LangChain LCEL チェーン                                     |
| 28   | LangChain memory / RunnableWithMessageHistory               |
| 29   | OpenAI function calling 公式                                |
| 30   | MCP 公式仕様（modelcontextprotocol.io）                     |
| 31   | Hugging Face smolagents 公式                                |
| 32   | LangGraph 公式 docs                                         |
| 33   | OpenAI Agents SDK, Assistants→Responses 移行ドキュメント    |
| 34   | サンドボックス・DevContainer セキュリティベストプラクティス |

### 第5章（Unit 35–40）— Capstone

| Unit | 参照リンク（案）                                               |
| :--- | :------------------------------------------------------------- |
| 35   | LLM-as-a-Judge 調査論文・ブログ, RAGAS（任意）                 |
| 36   | imbalanced-learn, 不正検知 ML 概説                             |
| 37   | Pydantic 公式, structured output ガイド                        |
| 38   | Guardrails AI / NeMo Guardrails（概念比較）, JSON mode         |
| 39   | 時系列 CV（sklearn TimeSeriesSplit）, 価格最適化の因果推論入門 |
| 40   | smolagents multi-agent, マルチエージェント設計パターン         |

---

## 5. 実装フェーズ

### Phase 0: 基盤（SSoT + 検証）— 先行必須

- [ ] **P0-1**: `curriculum/curriculum-registry.yaml` 作成（40 Unit + out_of_scope 10件）
- [ ] **P0-2**: `scripts/verify_curriculum_registry.py` 作成
  - registry の slug と実ディレクトリの一致
  - `unit00_roadmap` 内の `../unitNN_*` リンクが全て存在
  - config.js サイドバーの link パスと registry の slug 一致
  - Unit 0 の「Unit N」言及が registry の id と一致（正規表現抽出）
- [ ] **P0-3**: CI または `pnpm docs:build` 前の verify ステップに組み込み（任意）

### Phase 1: Unit 0 スコープ外トピック拡充

- [ ] **P1-1**: 現行3件に公式 URL を追加（BPE → HF Tokenizers 等）
- [ ] **P1-2**: §3 の追加7件を Unit 0 に反映（リンク・前提 Unit はすべて registry 経由で記述）
- [ ] **P1-3**: Unit 0 冒頭に「Unit 番号はロードマップとサイドバーが正。本文中の Unit 参照は学習の目安」と1文（任意）
- [ ] **P1-4**: Fable 5 レビュー — Unit 0 の全リンク・Unit 番号を registry と突合

### Phase 2: 全 Unit に「さらに学ぶ」セクション追加

- [ ] **P2-1**: 第1章 Unit 1–9（9ファイル）
- [ ] **P2-2**: 第2章 Unit 10–16（7ファイル）
- [ ] **P2-3**: 第3章 Unit 17–21（5ファイル）
- [ ] **P2-4**: 第4章 Unit 22–34（13ファイル）
- [ ] **P2-5**: 第5章 Unit 35–40（6ファイル）
- [ ] **P2-6**: 章ごとに Fable 5 レビュー（registry の further_reading と index.md の一致）

### Phase 3: 周辺ファイルの整合（必要最小限）

- [ ] **P3-1**: Appendix に「スコープ外トピック一覧は Unit 0 を参照」と1行（重複管理を避ける）
- [ ] **P3-2**: 英語版 `en/curriculum/unit00_roadmap` への同内容反映 — **別タスクとして backlog**（日本語優先の場合は Phase 3 をスキップ可）

### Phase 4: 検証

- [ ] **V-1**: `verify_curriculum_registry.py` 全パス
- [ ] **V-2**: `verify_curriculum_diagrams.py`（既存）
- [ ] **V-3**: `fix_ja_markdown_bold.py`（既存）
- [ ] **V-4**: `pnpm docs:build`
- [ ] **V-5**: 外部リンクのサンプル HEAD チェック（主要10 URL。404 は手動代替 URL に差し替え）

---

## 6. 将来 Unit を追加する場合のチェックリスト

新 Unit（例: Unit 41）やスコープ外トピックの **本編昇格** 時は、**必ずこの順序** で更新する:

1. `curriculum-registry.yaml` にエントリ追加 / `out_of_scope` から削除
2. `curriculum/unitNN_slug/index.md` 作成
3. `.vitepress/config.js`（ja + en サイドバー）
4. `curriculum/unit00_roadmap/index.md` 章一覧
5. 依存 Unit の本文（「Unit X 参照」）を grep で洗い出し更新
6. `tasks-export.csv`（進捗管理を使う場合）
7. `index.md` ホーム（章の説明が変わる場合のみ）
8. `verify_curriculum_registry.py` 実行

**スコープ外 → 本編に昇格したトピック**は、Unit 0 の該当行を削除し、新 Unit へのリンクに差し替える（二重記載禁止）。

---

## 7. 見積もりとスコープ

| Phase   | 作業量 | 備考                          |
| :------ | :----- | :---------------------------- |
| Phase 0 | 小     | 一度作れば以降の安全網        |
| Phase 1 | 小     | Unit 0 のみ + registry        |
| Phase 2 | 中     | 40ファイル × 均一フォーマット |
| Phase 3 | 小     | Appendix 1行 + en は backlog  |
| Phase 4 | 小     | 自動検証                      |

**今回のスコープ外**: 英語版カリキュラム全文の同期は含めない（別 PR 推奨）。

---

## 8. 承認時の確認事項（ユーザーへの質問）

実装に入る前に、以下を確認したい:

1. **スコープ外トピック**: §3 の10件でよいか？ 追加・削除の希望はあるか？
2. **Unit 0 の表示形式**: テーブル一覧 vs カテゴリ別リスト、どちらがよいか？
3. **英語版**: Phase 3-2 を同時に行うか、日本語完了後に backlog とするか？
4. **リンクの言語**: 公式ドキュメントは英語 URL が多い。見出しは日本語説明 + 英語ページでよいか？

---

**次のステップ**: 上記 §8 の確認後、「修正して」または項目ごとの指示をいただければ、Phase 0 から Fable 5 が実装を開始する。
