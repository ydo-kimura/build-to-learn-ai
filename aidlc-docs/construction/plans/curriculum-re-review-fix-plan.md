# 再レビュー指摘の修正計画 (Re-Review Fix Plan)

**作成日** : 2026-07-02
**方針（再発防止プロセス）** :
1. 修正の詳細（箇所・変更内容・理由）は Fable 5（メインエージェント）が本計画に明記し、修正も Fable 5 が直接実施する
2. 修正完了後、章ごとに git diff を本計画と突き合わせて Fable 5 がレビューし、「レビュー済」チェックを付ける
3. 最後に機械検証（太字規約・図解検証・ビルド）を再実行する

**対象** : curriculum-re-review-findings.md の高2・中19・低約50・全体ギャップ6件すべて

---

## Phase 1: SVG 生成スクリプト（Fable 5 が直接修正）

- [x] **S-1 (H-2)** : generate_curriculum_visuals.py L320 の「× low IDF」→「× high IDF」に修正（TF-IDF の定義: 重要 = 高TF × 高IDF）
- [x] **S-2 (M-9)** : unit12 の concept/workflow 図を、左右同一内容の diagram_compare から単一パネルの diagram_card に変更（mini_loss_curves は MSE/CE 両曲線、mini_optimizers は SGD/Adam 両軌跡を1枚で対比しているため）。タイトルは「MSE vs Cross-Entropy」「SGD vs Adam」
- [x] **S-3** : 再生成 + public/ 同期

## Phase 2: ユニット別修正（Fable 5 が直接修正・レビュー）

各ユニットの修正詳細:

- [x] **Unit 0** : L137 助詞補完「実装が終わるまで」/ L11 太字範囲を「基礎的な機械学習（ML）やディープラーニング（DL）の知識が不可欠」に短縮 / L27 表セル「極めて低い（API利用なら即時可能）」/ 末尾に「本カリキュラムで扱わないトピック（次の一歩）」節を追加（G-6: LLMファインチューニング(LoRA)・ストリーミング応答・サブワードトークナイザ(BPE)は扱わない旨と学習後の方向性）— レビュー済 [x]
- [x] **Unit 2** : One-vs-Rest 説明を「内部ではソフトマックスで全クラスの確率を同時計算」に修正 / max_iter 説明に「Unit 3 で学ぶ標準化を行うと少ない回数で収束」の1文 / G-1: 評価指標の節に不均衡データの注記（正解率の罠、`class_weight="balanced"` の1行例）/ G-4: ROC-AUC の短い言及と `roc_auc_score` の1行 — レビュー済 [x]
- [x] **Unit 3 (M-1)** : 答え合わせ解説に「digits は全特徴量 0〜16 の同一スケールのため標準化を省略。単位が異なる実データでは鉄則どおり標準化する」を追加 — レビュー済 [x]
- [x] **Unit 4** : 過学習観察コードに fit + 訓練/テスト正解率の比較 print を追加 — レビュー済 [x]
- [x] **Unit 5** : eval_metric の説明を「評価指標の明示指定（二値分類では logloss が定番）」に変更 / 連続空行の整理 / G-2 補助: カテゴリ変数は数値化が必要な旨の1文 — レビュー済 [x]
- [x] **Unit 6** : L106 太字規約修正 / DBSCAN 正式名称補完 / 「実データでは Unit 3 と同じく標準化が鉄則」の1文 — レビュー済 [x]
- [x] **Unit 8** : workflow 図ラベルと本文例の不一致は図が汎用例のため「（図は max_depth×学習率の例）」の一言をブリッジ文に追加 — レビュー済 [x]
- [x] **Unit 9** : 「100通り」→「121通り（11×11）」/ G-2: 前処理の説明に One-Hot エンコーディング（`pd.get_dummies` / `OneHotEncoder`）の段落を追加 / G-5: 答え合わせ末尾に `joblib.dump/load` の2行とモデル保存の一言 — レビュー済 [x]
- [x] **Unit 10** : ブリッジ文「数式レベル」→「構造レベル」/ 「誤差の二乗和」と MSE の関係を一言整理 — レビュー済 [x]
- [x] **Unit 12** : Momentum 説明の重複を解消（インライン言及を残しコードブロックに一本化）/ 図差し替えに伴う alt・ブリッジ文の整合確認 — レビュー済 [x]
- [x] **Unit 13** : 「3つのテクニック」→「4つのテクニック」（表と一致）/ 冒頭の範囲宣言に Early Stopping を追加 / 評価 print の「テストデータ」誤記修正 — レビュー済 [x]
- [x] **Unit 10〜16, 29〜31 共通** : 「のセクション を」→「のセクションを」（前回の私のアンカー修正で混入したスペース）— レビュー済 [x]
- [x] **Unit 16 (M-16)** : 設計意思決定マトリクスの欠損セルを補完 / G-5: `torch.save(model.state_dict(), ...)` の2行と一言 — レビュー済 [x]
- [x] **Unit 17 (M-15)** : Practice のテストメール2件目を学習語彙と重なる文面に変更（または語彙が重なるよう学習データを1件追加）— レビュー済 [x]
- [x] **Unit 21 (M-4, M-10)** : concept 図のブリッジ文・alt を「翻訳モデルの流れ（テキスト→エンコーダー→デコーダー→翻訳）」に修正 / 「未知の英文」の課題設定を「訓練済みの文の再現確認＋単語を入れ替えた未知の文での汎化観察」に再構成し、答え合わせの筋書きも整合させる / Positional Encoding 省略の注記1文 / 意思決定マトリクスの欠損セル補完 — レビュー済 [x]
- [x] **Unit 22 (G-3)** : 冒頭に「Transformer から LLM へ」の橋渡し段落（事前学習=次トークン予測、大規模化、指示チューニング/RLHF）を追加 / L143 太字後コロンのスペース — レビュー済 [x]
- [x] **Unit 23** : 「100%遵守」→「ほぼ確実に遵守」/ CoT 誤答例の数値と説明の整合 — レビュー済 [x]
- [x] **Unit 24** : 表セルのスペース統一 / 実践指示「8〜10個ほど」に変更 — レビュー済 [x]
- [x] **Unit 25 (M-5)** : 答え合わせに「### 解説」を追加（temperature=0.0、防御プロンプト、retriever→context）/ 見出しスペース修正 / 図中 RetrievalQA への一言 / format_docs の推奨注記 — レビュー済 [x]
- [x] **Unit 26** : 太字規約 / 「レシーバー」→「リトリーバー（Retriever）」/ 「午後15:00」→「15:00」/ FAISS を Unit 25 と同じ InMemoryVectorStore に統一 — レビュー済 [x]
- [x] **Unit 27** : L33 太字規約修正 — レビュー済 [x]
- [x] **Unit 28** : ブリッジ文を図の実内容（入力→履歴追加→API→応答）に修正 / `get_session_history` の説明を正確化 — レビュー済 [x]
- [x] **Unit 29 (M-6)** : 答え合わせに「### 解説」追加 / 「インプロセス」を平易に言い換え — レビュー済 [x]
- [x] **Unit 30 (H-1, M-7)** : 1.1 の Host/Client/Server 定義と Mermaid を公式仕様（Host ⊃ Client → Server）に是正 / L154 見出しの用語統一 / 「URL形式」→「URI形式」/ 答え合わせに「### 解説」追加（バリデーションをツール内に置く理由）— レビュー済 [x]
- [x] **Unit 31 (M-11)** : workflow 図のブリッジ文を「タスク受領→コード生成→サンドボックス実行→結果返却の循環」に修正し、図の連続を本文で分離 / docstring コメントを description 属性に合わせる / `LocalPythonInterpreter`→`LocalPythonExecutor` / 「完全に遮断」「安全です」を緩和 / ReAct 評価の誇張を緩和 — レビュー済 [x]
- [x] **Unit 32 (M-2)** : 答え合わせに LangGraph（StateGraph + 条件分岐 + interrupt/承認ノード）版の解答を追加し、手組み版は「構造理解用の参考」と位置づけを明記 / `bool | None` に Python 3.10+ の注記 — レビュー済 [x]
- [x] **Unit 33 (M-12, M-13)** : Assistants API と Agents SDK を分離して記述（Handoffs は Agents SDK、Thread 永続化は Assistants API、後者は Responses API への移行で廃止予定）/ 「Llama Agents」→「Llama Stack の Agents API」/ `__main__` 追記位置の注記 — レビュー済 [x]
- [x] **Unit 34 (M-8, M-14)** : `is_path_safe` を `os.path.commonpath` 比較に修正し、startswith の落とし穴を注記として教材化 / 答え合わせに「### 解説」追加 / `broken_code` を print で使用 — レビュー済 [x]
- [x] **Unit 35 (M-17)** : L155 太字規約修正 / 表セルスペース統一 / 「スルーハルシネーション」→平易な表現 / 防御レイヤ図のブリッジ文に「詳細は Unit 38」の一言 — レビュー済 [x]
- [x] **Unit 36 (G-1)** : 「個別に」重複削除 / `stratify=y_labels` 追加 / 優位性断定を「期待される」に緩和 / concept 図ブリッジ文に2モーダル簡略化の注記 / 不均衡データの注記（不正15%と評価指標の選び方、`class_weight` への言及）を追加 — レビュー済 [x]
- [x] **Unit 37** : workflow 図ブリッジ文を「DBに保存・検索可能なレコード」寄りに修正 / 「100%（保証）」→「実質100%（失敗時は人間へエスカレーション）」/ 「情報リーク」→「変換ミス」— レビュー済 [x]
- [x] **Unit 38 (M-3)** : マトリクスと最終決定の記述を実装（JSON Mode + json.loads）に合わせる / ルールベース検査の過剰ブロック注記コメント — レビュー済 [x]
- [x] **Unit 39 (M-18)** : `$P^*$` → `P*` / 実践セル冒頭に import 2行 — レビュー済 [x]
- [x] **Unit 40** : concept 図ブリッジ文に「（図は一般的な部署分けの例）」/ 「完全に防護」→「攻撃面を大幅に縮小」— レビュー済 [x]
- [x] **Appendix (M-19)** : requirements.txt に `llama-index` 系・`mcp` を追記し「一括インストール」の記述と整合 / 「追加ライブラリ」節を「requirements.txt に含まれる。個別インストール時のコマンド」に書き換え / 「github-project-import」を GitHub CLI ベースの手順に置換 / .txt/.csv リンクを GitHub blob URL に変更 — レビュー済 [x]

## Phase 3: 検証

- [x] **V-1** : fix_ja_markdown_bold.py 再実行
- [x] **V-2** : verify_curriculum_diagrams.py で全図解検証
- [x] **V-3** : pnpm docs:build 成功確認
- [x] **V-4** : 章ごとの diff レビュー完了確認（全ユニットの「レビュー済」チェック）
- [x] **V-5** : findings のチェックボックス消化、aidlc-state.md・audit.md 更新
