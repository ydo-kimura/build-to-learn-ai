# カリキュラム再レビュー結果 (Re-Review Findings)

**実施日** : 2026-07-02
**背景** : 高・中・低重要度の一連の修正適用後の再レビュー。章別4観点（わかりやすさ / 図解 / 例示 / 章末問題）＋技術的正確性＋Markdown 体裁を並列レビューし、カリキュラム全体の網羅性・順序性も評価した。

**結果サマリ** : 高 2件 / 中 19件 / 低 約50件。図解の実在・ブリッジ文・alt 形式・リンクは全ユニットで問題なし。前回までの修正はすべて反映済みであることを確認。

---

## 高重要度（2件）

- [x] **H-1. Unit 30** : 本文 1.1 と Mermaid 図の Host / Client 定義が公式 MCP 仕様と逆転（本文:「Client = Cursor/Claude Desktop の UI」「Host = 仲介スクリプト」）。同ユニットの SVG（Host ⊃ MCP Client → Server）は正しく、本文と図が矛盾。1.1 の 3 ロール説明・Mermaid・L154 の見出しを「Host（アプリ）⊃ Client（コネクタ）→ Server」に統一する
- [x] **H-2. Unit 17** : SVG 図中の「High TF × low IDF = important」が誤り（正しくは high IDF）。`scripts/` の該当生成コードを修正して再生成

## 中重要度（19件）

### 説明と実装の不一致

- [x] **M-1. Unit 3** : 本文で「K-NN/SVM はスケーリングが鉄則」と強調しつつ、解答は `StandardScaler` なしで理由説明もない。digits は 0〜16 の同一スケールである旨を解説に明記（または標準化して比較）
- [x] **M-2. Unit 32** : 実践は「振り分けグラフ（LangGraph）に HITL を追加」と指示するのに、解答は 2.3 の手組み Python 版で StateGraph 不使用。StateGraph + 承認ノード（checkpointer / interrupt）版に差し替えるか断り書きを追加
- [x] **M-3. Unit 38** : 比較マトリクスは「Pydantic 検証」「JSON Schema 出力を強制」と述べるが、解答コードは `json.loads` のみ。表記を「JSON Mode + 構造化出力」に改めるか解答に Pydantic 検証を追加
- [x] **M-4. Unit 21** : 実践の `"i love learning"` を「未知の英文」と呼ぶが訓練コーパス5文に含まれており、答え合わせの「過学習で誤訳する」筋書きも再現性が疑わしい。5文目をホールドアウトするか課題設定の文言を変更

### 答え合わせの解説不足

- [x] **M-5. Unit 25** : 答え合わせが解答コードのみで「### 解説」がない（temperature=0.0 の理由、防御プロンプトの重要性等を追加）
- [x] **M-6. Unit 29** : 同上（システムプロンプトに日付・ビジネスルールを厳密に書く理由、却下時にツール実行をスキップする仕組みとリスク）
- [x] **M-7. Unit 30** : 同上（バリデーションをツール内に置く理由 = LLM 入力は信頼できない境界）
- [x] **M-8. Unit 34** : 同上（書き込みとコマンド実行の両方に承認フックを通す理由、Deny by Default とフックの二段構え）

### 図解

- [x] **M-9. Unit 12** : SVG 2点で左右パネルの内容が同一（「SGD」パネルにも Adam 曲線が混在）なのにタイトルだけ異なる。生成スクリプトを修正して左右を対比内容に再生成
- [x] **M-10. Unit 21** : concept 図は「翻訳モデルフロー」だがブリッジ文と alt は「NLP プロジェクト全体の流れ」。ブリッジ文・alt を図の実内容（テキスト→エンコーダー→デコーダー→翻訳）に合わせる
- [x] **M-11. Unit 31** : workflow 図のブリッジ文「ツールルーティングの特徴」が図の実内容（コードエージェント循環）と不一致で、concept 図とほぼ同内容の図が本文を挟まず連続。ブリッジ文修正＋配置見直し

### 技術・事実の正確性

- [x] **M-12. Unit 33** : Assistants API と Agents SDK を一体の製品として説明（Handoffs は Agents SDK、Thread 永続化は Assistants API の機能。Assistants API は廃止予定）。分けて記述する
- [x] **M-13. Unit 33** : 「分散型エージェント（Llama Agents）」を Meta 帰属として記述（`llama-agents` は LlamaIndex 系 OSS）。「Llama Stack の Agents API」に修正
- [x] **M-14. Unit 34** : `is_path_safe` の `startswith(self.allowed_directory)` は前方一致すり抜けを許す脆弱パターン。`os.path.commonpath` 比較等に修正（落とし穴として教材化も可）
- [x] **M-15. Unit 17** : Practice のテストメール2件目が学習語彙と重ならず「正常」と判定されない恐れ。テストデータまたは語彙を調整

### 体裁・整合

- [x] **M-16. Unit 16** : 設計意思決定マトリクスがヘッダー4列に対しデータ行3セルで最終列が空欄。セルを補完
- [x] **M-17. Unit 35** : L155 の太字前後スペース規約違反1件
- [x] **M-18. Unit 39** : `$P^*$` の TeX 記法が math プラグイン未導入のため生テキスト表示。プレーン表記「P*」に変更
- [x] **M-19. Appendix** : (a) `llama-index` 系・`mcp` が requirements.txt に未収載なのに「一括インストール」と記載。(b) 「追加ライブラリ」として挙げる smolagents/pydantic/langgraph は requirements.txt に収載済みで自己矛盾。(c) 実在未確認ツール「github-project-import」の記載。3点を整理

## 低重要度（約50件・抜粋）

- Unit 0: 助詞脱落（L137）、太字範囲が長すぎる（L11）、表セルの表現（L27）
- Unit 2: One-vs-Rest 説明が現行 sklearn（多項ソフトマックス）と不一致、max_iter の「おまじない」説明
- Unit 4: 過学習観察コードが fit/比較まで示していない
- Unit 5: eval_metric「おまじない」説明の陳腐化、連続空行
- Unit 6: 太字規約違反1件、DBSCAN 正式名称の欠け、標準化への言及なし
- Unit 8: workflow 図の軸ラベルと本文例のパラメータ不一致
- Unit 9: 「0〜10で100通り」→ 正しくは 11×11=121、ビジネスユースケース節なし
- Unit 10: ブリッジ文「数式レベル」が過大、二乗和と MSE の混用
- Unit 12: Momentum 説明の重複（インラインコード＋コードブロック）
- Unit 13: 「3つのテクニック」vs 表4行、冒頭の範囲宣言と実装（Early Stopping 含む）の不一致、評価 print の「テストデータ」誤記
- Unit 10〜13, 29〜31: 「のセクション を」の不要スペース（共通）
- Unit 21: Positional Encoding 省略の注記なし、意思決定マトリクスの列数不一致
- Unit 23: 「100%遵守」の誇張、CoT 誤答例の数値と説明の不整合
- Unit 24: 表セルの太字とパイプの間のスペース不統一、「10個」vs 解答8個
- Unit 25: 見出しの不自然なスペース、retriever 出力の repr 直流し（format_docs 推奨）、図中 RetrievalQA（旧 API）への一言
- Unit 26: 太字規約違反、「レシーバークラス」誤記、「午後15:00」重複表記、Unit 25 と異なる FAISS 使用
- Unit 27: 太字規約違反1件
- Unit 28: ブリッジ文「スレッド表示」と図の不一致、`get_session_history` の説明の不正確さ
- Unit 29: 「インプロセス」未説明
- Unit 30: 「URL形式」→「URI形式」
- Unit 31: docstring コメントと実装（description 属性）の不一致、`LocalPythonInterpreter` 旧称、「完全に遮断」「安全です」の断定過剰、ReAct 評価の誇張
- Unit 32: `bool | None`（Python 3.10+）への注記
- Unit 33/34: 章立てが他ユニットと不一致、`__main__` 二重実行の注記なし、`broken_code` 未使用
- Unit 35: 防御レイヤ図が本文説明なしで浮いている、「スルーハルシネーション」造語、表セルのスペース不統一
- Unit 36: 「個別に」重複、concept 図2モーダルへの注記、`stratify` なし、比較未実施なのに優位性を断定
- Unit 37: ナレッジグラフが本文未登場、「100%（保証）」の断定、「情報リーク」の語の紛らわしさ
- Unit 39: 実践セルに import なし
- Unit 40: concept 図の部署名と本文の不一致への一言、「完全に防護」の過大表現
- Appendix: .txt/.csv リンクがビルド成果物にコピーされない可能性、raw URL の疎通未確認

---

## カリキュラム全体レビュー（網羅性・順序性）

### 順序性: 良好

- ML → DL → NLP/Transformer → LLM/Agent → 実務 Capstone の章構成は「LLM を使うだけでなく中身を理解できる AI エンジニア」という Unit 0 の目的に合致
- 章内の依存関係も正しい（例: Unit 24 スクラッチ RAG → 25/26 フレームワーク、Unit 27 は Unit 25 の LCEL を前提）

### トピックの漏れ（候補）

- [x] **G-1（中〜高）不均衡データ対応** : 全40ユニットで言及ゼロ。Unit 2（分類評価）と Unit 36（不正検知＝典型的な不均衡問題）に補足を推奨
- [x] **G-2（中）カテゴリ変数のエンコーディング** : One-Hot 等の言及ゼロ。第1章（Unit 4/5 あたり）に1節または注記を推奨
- [x] **G-3（中）Transformer → LLM の橋渡し** : 事前学習・次トークン予測・RLHF の説明がなく、Unit 20 と Unit 22 の間に概念の跳びがある。Unit 22 冒頭に1〜2段落追加を推奨
- [x] **G-4（低〜中）ROC-AUC** : Precision/Recall/F1 は Unit 2 でカバー済みだが AUC 未登場
- [x] **G-5（低〜中）モデルの保存・再利用** : `torch.save` / `joblib` が未カバー
- [x] **G-6（低）意図的スコープ外の明示** : LLM ファインチューニング（LoRA）、ストリーミング応答、サブワードトークナイザ（BPE）は未カバー。「扱わない理由・学習後の次の一歩」を Unit 0 か Appendix に一言添えると親切

---

**修正状況**: 2026-07-02 高2件・中19件・低約50件・全体ギャップ6件（G-1〜G-6）すべて修正済み。修正詳細は curriculum-re-review-fix-plan.md に記録（修正詳細の決定・実施・章ごとのレビューはすべて Fable 5 が担当）。
