# カリキュラム品質修正計画 (Curriculum Quality Fix Plan)

**作成日** : 2026-07-02
**背景** : 全41ユニット＋Appendix の4観点レビュー（初心者向けわかりやすさ・図解適切性・例示適切性・章末問題の質）で検出された重要度「高」14件・「中」約30件を修正する。

**修正方針** :
- 既存の「例え話 → 図解 → 実装 → 実践 → 答え合わせ」フォーマットを維持する
- 答え合わせは「コード＋なぜそうするかの解説」を標準形とする（Unit 17〜20 の水準に統一）
- 太字記法 ` **text** `（前後半角スペース）と図解ブリッジ文「下図は〜」の規約を遵守する
- 各フェーズ完了ごとに `pnpm docs:build` 相当の検証は最終フェーズでまとめて実施

---

## Phase 1: 実行不能の解消（環境・依存関係）

- [x] **1-1. Appendix** : Colab 一括インストール URL のプレースホルダー `[あなたのユーザー名]/[リポジトリ名]` を実リポジトリパスに置換（リポジトリの origin URL を確認して反映）
- [x] **1-2. requirements.txt** : `smolagents`（Unit 31/37/40）、`pydantic`（Unit 37）を追記。バージョンは既存記法に合わせる
- [x] **1-3. Unit 28** : `pip install langchain-community` の導入手順を実装例の冒頭に追記
- [x] **1-4. Appendix** : 後半ユニット（Unit 31 以降）実行前の追加インストール手順の節を追記

## Phase 2: 教材の信頼性に関わる技術的誤りの修正

- [x] **2-1. Unit 34** : 虚構の「Google Antigravity SDK（google-antigravity）」の記載を削除し、実在する SDK（Claude Code / OpenAI Codex CLI / GitHub Copilot 等の一般論）に置換。Mermaid 図・クラス名も修正
- [x] **2-2. Unit 34** : 「OpenAI Codex SDK (Legacy / Current Assistants)」の名称整理（Codex モデルと Assistants API の混同を解消）
- [x] **2-3. Unit 5** : XGBoost の並列化説明を「ブースティング自体は逐次のまま、木構築内部（特徴量ヒストグラム計算等）を並列化」と正確に修正
- [x] **2-4. Unit 36** : サンプルデータ生成をコメント通り「画像・テキストと相関のあるラベル」になるよう修正（シグナルを混入したデータ生成に変更）、または コメントを実態に合わせ修正して演習の結論を成立させる
- [x] **2-5. Unit 16** : BatchNorm を実装例に実際に組み込む（冒頭宣言との一致）
- [x] **2-6. Unit 16** : 転移学習の凍結方針を Unit 15 と整合させる（バックボーン凍結＋最終層学習、または全層 fine-tune を選ぶ理由を明記）
- [x] **2-7. Unit 16** : 演習データを完全ランダムから学習可能なデータ（構造を持つ合成データ or MNIST サブセット）に変更し、精度比較が成立するようにする
- [x] **2-8. Unit 33** : 推測的な製品名（AgentCore Payments 等）を検証可能な一般的記述に修正
- [x] **2-9. Unit 12** : SGD vs Adam 比較で同一初期重みのコピーを使う公平比較に修正。「確率スコア」コメントを「logits」に修正

## Phase 3: 答え合わせ（Answer Key）の欠落補完

- [x] **3-1. Unit 21** : アプローチ A（LSTM+Attention）の実装コードを Answer Key に追加し、「A を選ぶ」結論の根拠（実行結果比較）を成立させる
- [x] **3-2. Unit 26** : アプローチ A（手組み）/ B（LlamaIndex）/ C（LangChain）の比較コード骨子を Answer Key に追加
- [x] **3-3. Unit 31** : アプローチ A（ReAct / Tool Calling）の実装例を Answer Key に追加
- [x] **3-4. Unit 33** : Answer Key を完成させる（`ReceptionAgent` の分岐追加・`AgentOrchestrator` への登録・実行例まで）
- [x] **3-5. Unit 35** : アプローチ A（`EVAL_TONE_PROMPT` 単次元評価）の実装を Answer Key に追加
- [x] **3-6. Unit 37** : 自己修正ループ（バリデーション失敗時の `agent.run` 再試行）を実際に実装。未使用の `field_validator` import を解消（使うか削除）

## Phase 4: 図と本文の不一致解消

- [x] **4-1. Unit 6** : パーティの例えを2テーブル（K=2）に修正して図と一致させる（または SVG を3クラスタに変更。本文修正の方が影響が小さいため本文側を推奨）
- [x] **4-2. Unit 28** : workflow 図（SVG）を CLI チャットループの図（Input → History append → API call → Reply）に差し替え。`generate_curriculum_visuals.py` を修正して再生成
- [x] **4-3. Unit 32** : `langgraph` パッケージの `StateGraph` を使った最小実装例を実装セクションに追加（手組み版は「内部の仕組み理解」用として位置づけを明記）。requirements.txt に `langgraph` を追加
- [x] **4-4. Unit 21** : concept 図を翻訳 Capstone に合った内容（Text → Encoder → Decoder → Translation）に差し替え。`generate_curriculum_visuals.py` を修正して再生成
- [x] **4-5. Unit 30** : concept 図を Host / Client / Server の3層構成に修正して本文・Mermaid と一致させる
- [x] **4-6. Unit 40** : concept 図（Triage → Billing/Tech/Sales）を説明フェーズ本文にも配置
- [x] **4-7. Unit 13** : `diagram-concept.svg` の alt を「過学習 vs Dropout」に修正
- [x] **4-8. Unit 38** : `diagram-concept.svg` の alt を「Guardrails」に修正
- [x] **4-9. Unit 9** : concept 図（Load→Clean→Split→Train→Eval）と本文パイプライン記述の用語を一致させる

## Phase 5: 横断課題（答え合わせ解説・ブリッジ文・難易度）

- [x] **5-1. Unit 10** : 答え合わせに解説を追加（OR が XOR より学習しやすい理由等）。`sigmoid_derivative` の引数がシグモイド出力である旨の注記を追加
- [x] **5-2. Unit 11** : 答え合わせに ReLU 追加・MSELoss 変更の意図と期待挙動の解説を追加
- [x] **5-3. Unit 12** : 答え合わせに CrossEntropyLoss の logits 入力・Softmax 不要の解説を追加
- [x] **5-4. Unit 13** : Early Stopping の最小実装例（val loss 監視＋patience）を実装例に追加
- [x] **5-5. Unit 14** : 実装例に最小学習ループを追加。答え合わせに Flatten サイズ計算（16×8×8）の解説を追加
- [x] **5-6. Unit 16** : Early Stopping ロジックを実装例に追加。train/val を同一データからの分割に修正
- [x] **5-7. Unit 22** : 答え合わせに解説セクションを追加
- [x] **5-8. Unit 23** : 答え合わせに解説（temperature=0.0 の理由等）を追加。セクション番号の欠番（##3）を修正
- [x] **5-9. Unit 24** : 答え合わせに解説（top-3 検索の意図・複数文書参照の利点）を追加
- [x] **5-10. Unit 27** : 答え合わせに `RunnablePassthrough.assign` を選ぶ理由とデータフローの解説を追加
- [x] **5-11. Unit 28** : 答え合わせに解説を追加。Buffer/Window Memory 表と `RunnableWithMessageHistory` 実装の対応を1段落補足
- [x] **5-12. Unit 1〜3** : 全図解（計8点）に「下図は〜」のブリッジ文を追加
- [x] **5-13. Unit 3** : 特徴量スケーリングの重要性（K-NN/SVM は距離ベース）の説明とコード（StandardScaler）を追加
- [x] **5-14. Unit 6** : DBSCAN の最小実装例（`sklearn.cluster.DBSCAN`）を実装例に追加
- [x] **5-15. Unit 19** : RNN の最小コード例（`nn.RNN`）を追加。文字のスカラー入力について「通常は Embedding 層を使う」旨の注記を追加
- [x] **5-16. Unit 26** : 誤記「内部ロジック of 透明性」→「内部ロジックの透明性」を修正
- [x] **5-17. Unit 26/31** : 実践課題に「まず写経で動かす → 次に設計判断」の段階的ステップを追記し、難易度の乖離を緩和
- [x] **5-18. Unit 29** : ReAct（テキスト形式）と OpenAI Tool Calling ループの関係を1文補足
- [x] **5-19. Unit 30** : クライアント側からの接続・呼び出しデモ（最小例）を補足に追加。Resources の URL スキーム例を統一
- [x] **5-20. Unit 31** : workflow 図をコード生成→サンドボックス実行ループの内容に修正。「成功率100%」等の断定表現を緩和
- [x] **5-21. Unit 32** : チェックポイント／永続化（`MemorySaver`）の最小例を追加
- [x] **5-22. Unit 33** : Handoff 後に委譲先エージェントが同一ターンで応答する実装に修正
- [x] **5-23. Unit 35** : 「第4章（Unit 22〜33）」の章範囲表記を確認・修正。「防御」の役割分担（Unit 38 との違い）を1段落補足
- [x] **5-24. Unit 36** : メタラーナー学習に検証セット分割を使うスタッキング標準手法に修正
- [x] **5-25. Unit 38** : 入力ガードレールにルールベース（regex）併用の言及と最小例を追加
- [x] **5-26. Unit 39** : 答え合わせに最適価格の具体的な計算結果例を追記。価格の内生性についての注記を追加
- [x] **5-27. Unit 18** : EC レコメンド例を「Item2Vec として知られる応用」と正確に位置づけ
- [x] **5-28. Unit 17** : IDF の対数底（scikit-learn は自然対数）の注記を追加。見出しの不自然なスペースを修正
- [x] **5-29. Unit 5** : sklearn の `GradientBoostingClassifier` への言及を1段落追加（汎用 GBM と XGBoost の関係）
- [x] **5-30. Unit 21** : 「完全に再現」等の過大表現を「小規模データで仕組みを体験」に修正

## Phase 6: 実行計画・状態管理の記録整合

- [x] **6-1** : `curriculum-consistency-fix-plan.md` の完了済みチェックボックス16個を消化（実態確認済み）
- [x] **6-2** : `unit32-langgraph-and-renumbering-code-generation-plan.md` の完了済みチェックボックス7個を消化
- [x] **6-3** : `aidlc-state.md` の Current Status・Workspace Root を現状に更新

## Phase 7: 検証

- [x] **7-1** : `fix_ja_markdown_bold.py` を再実行（新規追加文の太字スペース規約遵守）
- [x] **7-2** : SVG 変更分を `generate_curriculum_visuals.py --diagrams-only` で再生成し `public/assets/units/` に同期
- [x] **7-3** : VitePress ビルド（`pnpm docs:build`）でエラー・デッドリンクなしを確認
- [x] **7-4** : 修正済み全ユニットの図解ブリッジ文・alt・実在チェックをスクリプトで一括検証
- [x] **7-5** : `aidlc-state.md`・`audit.md` に完了記録

---

**推定影響範囲** : `curriculum/` 33ファイル、`scripts/generate_curriculum_visuals.py`、`scripts/curriculum_svg_lib.py`、`requirements.txt`、`assets/units/`（SVG 4点再生成）、`aidlc-docs/` 3ファイル

**リスク** : 低〜中。Markdown とスクリプトの変更のみで、git で全てロールバック可能。Answer Key へのコード追加は実行検証を伴わない教材コードのため、コードレビューによる論理確認を行う。

**対象外（今回のスコープ外）** :
- 英語版カリキュラム（`en/curriculum/`）への同内容の反映
- 重要度「低」の指摘（別途対応可）
