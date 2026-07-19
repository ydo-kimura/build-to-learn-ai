# カリキュラム レビュー結果（`curriculum/`）

## Scope

- **対象**: 日本語版カリキュラム `curriculum/` 配下の全44ファイル（Unit 0 ロードマップ + Unit 1〜42 + Appendix）
- **目的**: AIエンジニア初学者向け自習コンテンツとしての品質監査
- **モード**: Review only（本ファイルに結果を記録。対象ファイルは変更しない）
- **レビュー観点**: 誤字脱字 / 不自然な表現 / 論理の飛躍・矛盾 / 読者に不足している前提 / カリキュラム構成の不備 / Hero画像のわかりづらさ・テーマ乖離 / 図と内容の不整合

## Checks performed

1. **機械横断検証**: 全 `<img>` 参照の存在確認（0件欠落）、VitePress sidebar 登録照合（全43ユニット一致）、相対リンク解決（全件 OK）、Mermaid ブロック宣言構文（8箇所正常）、全 Python コードブロックの AST 構文検証（0件エラー）、`assets/` と `public/assets/` の MD5 一致確認（全 hero 画像一致）、旧アセットディレクトリへの参照有無（0件）
2. **本文精読（aggregator 直接）**: Unit 0 / 1 / 12 / 22 / 23 / 29 / 30 / 32 / 33 / 35 / 36 / 38 / Appendix を読了
3. **実行検証**: Unit 35 の toy BPE コードを実際に実行し、mermaid 図との整合を確認
4. **Hero 画像の視覚確認**: 22枚の `hero.png` を視覚モデルで評価
5. **SVG 図のテキスト照合**: 全 `diagram-*.svg` 内の `<text>` 要素を抽出し、本文の「下図は〜」説明と照合
6. **章別本文精読（サブエージェント5件）**: CH1（Unit 1-9）、CH2（Unit 10-16）、CH3（Unit 17-21）、CH4（Unit 23-34）、CH5（Unit 37-42）を完了。結果は本ファイルに統合済み。

## Checks not performed

- **Hero 画像（残り約20枚）**: Unit 2–4, 7–9, 11, 13–16, 18, 20–21, 24–28, 31, 33–34, 37, 40–42 の一部は未視覚確認。PNG 内テキストは grep 不可のため検証外。
- **VitePress build**: 未実行（Pass 1 は静的検証のみ。Pass 2 で実施予定）

> **Hero 画像所見の信頼性について**: 視覚モデルによる評価であり、画像解像度・フォントによる誤認識の可能性を含む。修正前に実画像での目視確認を推奨する。

---

## Findings

### 集計サマリー

| Severity | 件数 |
|----------|------|
| Critical | 3 |
| High | 16 |
| Medium | 40 |
| Low | 21 |
| **合計** | **80** |

> 集計は findings 見出しを機械的に grep して数えた実数（CH4-02 を Rejected から復元、CH1-12 / CH4-19 を追加した最終値）。サブエージェント自身の件数集計には一部誤りがあった。

---

### Critical（3件）

#### [CH1-01] Critical — Unit 9 Capstone が Unit 8 で未導入の概念を前提

- **Location**: `curriculum/unit09_classical_ml_capstone/index.md:35, 279-280`
- **観点**: 読者に不足している前提、カリキュラム構成の不備
- **Evidence**: L35「前処理から Optuna による XGBoost のチューニング、5-Fold交差検証までのプロフェッショナルなパイプラインを実装します。」/ L280「内側の交差検証は『最適なハイパーパラメータ（L1ペナルティ強度 alpha）の選択』だけに使い、外側の交差検証は『選ばれたモデルの汎化性能の評価』だけに使う」
- **Failure scenario**: Unit 8 を終えた読者が「同じCVでパラメータ選択と性能評価をやるとリークする」という概念を知らないまま Capstone に進み、「なぜ二重構造なのか」「Optuna とは何か」が理解できず、Capstone の教育効果が著しく低下する。
- **Recommended action**: Unit 8 に「パラメータ選択と評価を同じデータで行うと情報リークが起きる」という警告と「ネストCV」の概念を1段落追加する。または Unit 9 Section 1 に「Unit 8 の GridSearchCV との違い」を明示する。
- **Confidence**: High（aggregator 直接検証: Unit 8 に「ネスト」「Optuna」「リーク」「情報漏洩」の grep が 0 件）
- **Validation performed**: grep による Unit 8 全文検索で該当用語ゼロを確認

#### [CH3-07] Critical — Unit 20 Self-Attention に √dₖ スケーリングが欠落

- **Location**: `curriculum/unit20_attention_transformers/index.md:88–92`（実装例）および 167–178（解答例）
- **観点**: 論理の飛躍・矛盾、図と内容の不整合
- **Evidence**: L96 `scores = torch.matmul(Q, K.transpose(0, 1))` → L102 `attention_weights = F.softmax(scores, dim=-1)`。スケーリングなし。L69–72 の手順説明にも `√dₖ` への言及なし。
- **Failure scenario**: Vaswani et al. (2017) の核心である「内積の次元が大きくなると分散が増大し softmax が飽和するため `√dₖ` で割る」という動機が伝わらない。読者が実務で `d_model=512` 等のコードを読んだとき、なぜ `scores / math.sqrt(d_k)` があるのか理解できず、実装を「魔法の定数」として暗記する羽目になる。Transformer の説明の正確性が問われる Unit 20 において、これは数式の整合性上の欠陥。
- **Recommended action**: L96 を `scores = torch.matmul(Q, K.transpose(0, 1)) / math.sqrt(K.size(-1))` に修正し、L70 の手順説明に「③ 内積が大きくなりすぎないよう `√d_k` で割る（スケーリング）」のステップを追加する。
- **Confidence**: High（aggregator 直接検証: `sqrt`/`√`/`スケーリング`/`scaling` の grep が Unit 20 で 0 件）
- **Validation performed**: grep による全文検索でスケーリング言及ゼロを確認

#### [CH5-01] Critical — Unit 38 画像モーダル: 表は CNN、コードは RandomForest

- **Location**: `curriculum/unit38_multimodal_fraud_detection/index.md:25`（表）・191（コード）
- **観点**: 図と内容の不整合、論理の飛躍・矛盾
- **Evidence**: 表（L25）: `テーブル（XGBoost）、テキスト（NLPモデル）、画像（CNNモデル）を個別に訓練し` / コード（L195）: `model_img = RandomForestClassifier(max_depth=4, n_estimators=30, random_state=42)`
- **Failure scenario**: 学習者が表を読んで「後期融合＝CNNを使うもの」と理解した後、コードを見てRandomForestが使われていることに混乱する。CNNの実装方法を探すか、教材の誤りと判断して教材全体の信頼性を損なう。最悪の場合、学習者がCNN実装を試みて時間を浪費する。
- **Recommended action**: 表の記述を「画像（CNNやRandomForestなどのモデル）」に修正するか、コード内のコメントで「本教材では簡略化のためRandomForestを使用（実務ではCNN特徴量が一般的）」と明記する。
- **Confidence**: High（aggregator 直接検証: コード行 185-214 を読了し、CNN の存在しないことを確認）

---

### High（15件）

#### [CH1-02] High — Unit 5 が Unit 9 で One-Hot エンコーディングを約束するが実際には登場しない

- **Location**: `curriculum/unit05_gradient_boosting_xgboost/index.md:38` / `curriculum/unit09_classical_ml_capstone/index.md:15`
- **Evidence**: Unit 5 L38「その代表的な方法（One-Hot エンコーディング）は Unit 9 で実際に使います。」/ Unit 9 L15「今回の題材は全列が数値のため登場しませんが、実務のテーブルデータでは欠損値補完と並ぶ定番の工程です）」
- **Failure scenario**: 読者が「Unit 9 で One-Hot エンコーディングを学べる」と期待して進むと、実際には使われず、第1章を通じてカテゴリ変数の処理方法を一切学べない。
- **Recommended action**: Unit 5 L38 を「Unit 9 で概念を解説します（実装例は省略）」に修正するか、Unit 9 の実装例にカテゴリ列を追加して One-Hot エンコーディングを実際に実行する。
- **Confidence**: High

#### [CH1-03] High — Unit 3 で「鉄則」とした StandardScaler を Practice で省略

- **Location**: `curriculum/unit03_knn_svm/index.md:53, 195`
- **Evidence**: L53「学習の前にすべての特徴量を同じくらいのスケール（ものさし）に揃える 特徴量スケーリング（標準化） を行うのが鉄則です。」/ L195「なお、この解答では本文で「鉄則」とした StandardScaler による標準化をあえて省略しています。」
- **Failure scenario**: 読者が「鉄則」を学んだ直後に「わざとやらない」課題に直面し、いつ鉄則を破っていいのかの判断基準が分からない。
- **Recommended action**: Practice の要件に「（オプション）StandardScaler で標準化も試してみましょう」を追加し、解答例で「今回は省略」の理由を Practice セクションの注記として明示する。
- **Confidence**: High

#### [CH1-04] High — Unit 9 Capstone で pandas 高度操作が前提説明なしに登場

- **Location**: `curriculum/unit09_classical_ml_capstone/index.md:201-277`
- **Evidence**: `SimpleImputer`, `LassoCV`, `pd.Series`, `sort_values` などが Unit 1-8 で一切教えられていない。
- **Failure scenario**: Unit 1-8 で scikit-learn の基本的な使い方を学んだ読者が、Capstone で突然 `SimpleImputer`、`LassoCV`、`pd.Series` のフィルタリング・ソートに出会い、コードを読めない。
- **Recommended action**: Unit 9 Section 1 または実装例の冒頭に「本ユニットで新しく登場するライブラリ・機能」のリストと簡単な説明を追加する。
- **Confidence**: High

#### [CH2-01] High — Unit 10 誤差逆伝播の符号と勾配降下法の整合性

- **Location**: `curriculum/unit10_nn_from_scratch/index.md:139-143`
- **観点**: 論理の飛躍・矛盾
- **Evidence**: `d_output = error * sigmoid_derivative(output)`（`error = y - output`）/ `W2 += a1.T.dot(d_output) * learning_rate`（加算で更新）
- **Failure scenario**: 読者が Unit 12 で `loss.backward()` による自動微分（勾配降下法）に移行した際、「なぜUnit 10では加算で更新できたのか」が分からず、勾配降下法の基本原理を誤解する。数式とコードの整合が取れていないため、理解が断片的になる。
- **Recommended action**: コードコメントまたは解説に「`error = y - output` は勾配の負の符号を含んでいるため、加算更新で勾配降下と等価になる」と明記。または、勾配降下法の標準形に合わせて `d_output = (output - y) * sigmoid_derivative(output)`、`W2 -= ...` の形式に変更し、説明を統一する。
- **Confidence**: High（数学的には正しいが、教育的一貫性に欠ける）

#### [CH2-02] High — Unit 11 で BCELoss + Sigmoid の組み合わせ（数値不安定リスク）

- **Location**: `curriculum/unit11_pytorch_basics/index.md:99, 113, 220`
- **Evidence**: `criterion = nn.BCELoss()`（L99）/ `x = self.sigmoid(x)`（L83）/ Answer Key: `criterion = nn.MSELoss()`（L197）
- **Failure scenario**: 実務で BCELoss + Sigmoid を使用した際、勾配消失や NaN 発生に遭遇しやすくなる。また、読者が「分類問題では MSELoss でもよい」と誤解する。
- **Recommended action**: 実装例を `nn.BCEWithLogitsLoss()` に変更し、モデルの最終層から `self.sigmoid` を除去。Answer Key では MSELoss を「回帰用」と明確に区別する。
- **Confidence**: High

#### [CH3-01] High — Unit 17 TF-IDF 計算例が IDF の働きを一度も示していない

- **Location**: `curriculum/unit17_nlp_preprocessing_tfidf/index.md:92`
- **Evidence**: 「このように、本Aの中では『AI』の方が『データ』よりも高いスコアを獲得します。出現頻度が高い単語ほど、その本を特徴づけるキーワードとして重視されるわけです。」（両単語とも IDF = log(3/2) で同一）
- **Failure scenario**: 読者は「IDFが同じならTFだけで決まる」＝「IDFは不要なのでは？」と誤解する。TF-IDFの核心である「よく出る × 珍しい」の掛け算の意義が、教材上で一切検証されない。
- **Recommended action**: コーパスに「の」等の全3冊共通単語（`IDF = log(3/3) = 0` → TF-IDF = 0）を追加し、「どんなに頻出でもIDF=0なら無価値」という対比例を1セット追加する。
- **Confidence**: High

#### [CH3-08] High — Unit 20 Positional Encoding を Q/K/V 全てに加算（原論文と矛盾）

- **Location**: `curriculum/unit20_attention_transformers/index.md:175–178`（解答例）
- **Evidence**: L176–178 `query = query + positional_encoding` / `key = key + positional_encoding` / `value = value + positional_encoding`。対して L51–52 の本文説明は「各単語の**入力ベクトル**に位置ベクトルを加算」。
- **Failure scenario**: Vaswani et al. では PE は **エンコーダー/デコーダーの入力埋め込みにのみ** 加算され、その後 W_q/W_k/W_v で線形変換される。Q/K/V それぞれに PE を加えると、V（内容情報）に位置情報が混入し、Attention の重み付き和が「内容＋位置」の混合ベクトルを返すため、本文の「V = 実際の中身・意味」という定義と矛盾する。
- **Recommended action**: 解答例を「埋め込み `x` に PE を加算してから Q/K/V に渡す」形に修正するか、現行の簡略化を行う場合は「実際は入力埋め込みにのみ加算する」旨の注記を追加する。
- **Confidence**: High

#### [CH3-09] High — Unit 20 `nn.MultiheadAttention` デモがランダム入力で意味を持たない

- **Location**: `curriculum/unit20_attention_transformers/index.md:137–139`
- **Evidence**: L137–139 `query = torch.rand(...)` / `key = torch.rand(...)` / `value = torch.rand(...)`
- **Failure scenario**: 実装例（L82–86）では "it" と "animal" に意図的に似た特徴を持たせ、L113 で「交差する部分のスコアが高くなっている」と説明している。しかし課題でいきなり `torch.rand` に切り替わると、softmax 後の重みはほぼ一様分布になり、「どの単語がどの単語に注目したか」を読者が**数値で確認できない**。
- **Recommended action**: 課題のデータ生成に意図的な類似性を埋め込むか、「この課題は形状の確認が目的であり、重みの意味は実装例で確認済み」と明示する。
- **Confidence**: High

#### [CH3-11] High — Unit 21 最終意思決定が Toy 条件を一般則のように断定

- **Location**: `curriculum/unit21_nlp_capstone/index.md:439`
- **Evidence**: L439「『本番適用モデルとして、アプローチA（RNN/LSTM + Attention）を選択する。』」（太字の断定的結論）
- **Failure scenario**: 初学者が「5文なら LSTM が勝つ」→「じゃあ自分の小規模データでも LSTM でいい」と短絡し、2026 年時点の実務標準（Transformer 系がデフォルト）と逆行する判断をしかねない。
- **Recommended action**: L439 を「**この極小データ実験では** アプローチAを選択する。ただし実務ではデータ規模が数千文を超えた時点で Transformer を第一候補とする」と条件を明確化する。
- **Confidence**: High

#### [CH4-01] High — Unit 25 の IMPORTANT ブロックが API キー設定に言及していない

- **Location**: `curriculum/unit25_langchain_basics_rag/index.md:7-13`
- **Evidence**: `> このユニットを進めるには、`langchain` および `langchain-openai` ライブラリが必要です。` / `> 手元の環境で以下のコマンドを実行してインストールしてください。`（API キー記述なし）
- **Failure scenario**: 読者が Unit 24 の RAG 実装を終えた後、Unit 25 の LangChain コードを実行しようとした際、`ChatOpenAI` が API キーを要求してエラーで失敗。学習が途中で止まる。
- **Recommended action**: Unit 25 の IMPORTANT ブロックに Unit 23/24 と同様の API キー準備案内を追加する。
- **Confidence**: High（aggregator 直接検証: Unit 25 行 7-13 を読了し、API キー言及なしを確認）

#### [CH4-02] High — Unit 29 解説の「Unit 34〜38 で学ぶガードレール」参照先が実際の内容と不整合

- **Location**: `curriculum/unit29_ai_agent_implementation/index.md:441`
- **観点**: 論理の飛躍・矛盾、カリキュラム構成の不備
- **Evidence**: 「実務では、Unit 34〜38 で学ぶように『高額の払い戻しは人間の承認を必須にする』等のガードレールをプログラム側に敷くのが鉄則です。」
- **Failure scenario**: 読者が Unit 34〜38 にガードレール設計の解説を探すが、Unit 34（コーディングエージェント）・Unit 35（BPEトークナイザー）・Unit 36（LoRA/QLoRA）にはガードレール／人間承認の記述が一切なく、実際のガードレール解説は参照範囲外の Unit 40 にある。読者は「教材の参照が間違っている」と判断し、カリキュラム全体の信頼性を損なう。Human-in-the-loop は Unit 32 で既出のため、参照先としても不適切。
- **Recommended action**: 「Unit 40 で学ぶように」に修正するか、「第5章のガードレール設計（Unit 40）」と明示する。あわせて「Unit 32 で学んだ Human-in-the-loop の考え方」との言及も有効。
- **Confidence**: High（aggregator 直接検証: Unit 35/36 の全文 grep で「ガードレール/guardrail/承認/human-in-the-loop」が0件。ガードレール単元は Unit 40）
- **Validation performed**: Unit 29 行 430–441 の read_file、Unit 35/36 への grep、Unit 40 タイトル確認。一度「文脈整合」として棄却したが、grep 検証で参照先に内容が存在しないことが確定し復元。

#### [CH4-03] High — Unit 29 解答解説でコード内の関数名と不一致

- **Location**: `curriculum/unit29_ai_agent_implementation/index.md:441`
- **Evidence**: コード（L313–346）: `check_purchase_date` / `execute_refund`。解説（L441）: `LLM が get_order_info の結果...` / `払い戻しツール（process_refund）を呼ばない`。
- **Failure scenario**: 読者がコードと解説を照らし合わせた際、関数名が一致せず「どの関数を指しているのか」混乱する。
- **Recommended action**: 解説内の関数名を `check_purchase_date` / `execute_refund` に統一する。
- **Confidence**: High（aggregator 直接検証: Unit 29 行 240-258, 292-302, 441 を読了し不一致を確認）

#### [CH5-02] High — Unit 38 「メタラーニング」と「メタラーナー」の混在

- **Location**: `curriculum/unit38_multimodal_fraud_detection/index.md:25, 172, 218, 243`
- **Evidence**: 行25: `メタラーニング/スタッキング` / 行172: `メタラーナー(LogisticRegression)で結合する` / 行243: `メタスタッキング`
- **Failure scenario**: メタラーニング（few-shot学習などの手法群）とメタラーナー（スタッキングにおける統合モデル）は異なる概念であり、混同すると技術的な誤解を招く。
- **Recommended action**: 表では「メタラーニング（統合手法）」、コードでは「メタラーナー（統合モデル）」と使い分けを明確にし、初出時に両者の違いを注記する。
- **Confidence**: High

#### [CH5-03] High — Unit 39 JSON クリーンアップ処理が機能しない

- **Location**: `curriculum/unit39_knowledge_structuring_agent/index.md:225`
- **Evidence**: `cleaned_json = str(raw_output).strip().replace("JSON_MARKDOWN", "")`
- **Failure scenario**: LLMが ```` ```json\n{...}\n``` ```` という形式で出力した場合、`"JSON_MARKDOWN"` という文字列が存在しないため除去されず、`json.loads()` が失敗する。
- **Recommended action**: 実際のマークダウン装飾を除去するコードに修正する。例：`re.sub(r'^```json\s*|\s*```$', '', cleaned_json, flags=re.MULTILINE)`
- **Confidence**: High

#### [CH5-04] High — Unit 37 タイトルに「防御」が含まれるが内容は評価ハーネスのみ

- **Location**: `curriculum/unit37_llm_harness_capstone/index.md:1, 29`
- **Evidence**: 行1: `# Unit 37: LLM自動評価・防御とエージェント総合演習 (Capstone)` / 行29: `本ユニットの「評価（Evaluation）」と、Unit 40 で学ぶ「ガードレール（Guardrails / 防御）」は役割が異なります。`
- **Failure scenario**: 学習者がタイトルを見て「このユニットで防御（ガードレール）を学ぶ」と期待するが、実際には評価ハーネスの構築のみを扱い、防御はUnit 40に譲られている。
- **Recommended action**: タイトルを「LLM自動評価ハーネス総合演習（Capstone）」に修正し、「防御」の文言を削除する。
- **Confidence**: High

#### [CH5-05] High — Unit 42 マルチエージェント構成が4箇所で異なる

- **Location**: `curriculum/unit42_multiagent_customer_support/index.md:23-31, 33-35, 102-127, 282-308`
- **Evidence**: ASCIIアート（2子エージェント）・概念図（Triage→Billing/Tech/Sales）・実装例コード（2子エージェント）・解答コード（3子エージェント）で構成が異なる。
- **Failure scenario**: 学習者が「マルチエージェントは2つなのか3つなのか」「配送・決済なのか、注文・手数料・ポイントなのか」を混乱する。
- **Recommended action**: 実装例と解答で子エージェント数を統一する（例：実装例も3子エージェントにする）。
- **Confidence**: High

---

### Medium（29件）

#### [CH1-05] Medium — Unit 2 解答解説で「ソフトマックス関数」が突然登場

- **Location**: `curriculum/unit02_logistic_regression/index.md:171`
- **Evidence**: L171「内部では ソフトマックス関数 という仕組みを使って…」（Section 1 ではシグモイド関数のみ説明）
- **Recommended action**: Section 1 に「シグモイド関数の多クラス版がソフトマックス関数」という1文を追加する。

#### [CH1-06] Medium — Unit 4-9 の hero 画像 alt が英語アルゴリズム名のみ

- **Location**: `curriculum/unit04_decision_trees_random_forests/index.md:4` 他
- **Evidence**: Unit 1-3 は日本語で内容説明、Unit 4-9 は英語アルゴリズム名のみ。
- **Recommended action**: Unit 4-9 の alt テキストを日本語の内容説明に統一する。

#### [CH1-07] Medium — Unit 5 同一段落内に「なお」が2回

- **Location**: `curriculum/unit05_gradient_boosting_xgboost/index.md:38`
- **Recommended action**: 2つ目の「なお」を「また」または「加えて」に変更する。

#### [CH1-08] Medium — Unit 9 で固定パラメータ XGBoost に対する Lasso 優位を断定

- **Location**: `curriculum/unit09_classical_ml_capstone/index.md:284`
- **Evidence**: XGBoost のパラメータは固定値（Optuna 未使用）だが「多くの場合アプローチA（Lasso）の方が…優れたRMSEを示します」と断定。
- **Recommended action**: 「本演習の固定パラメータ設定では Lasso が優位ですが、XGBoost を Optuna 等で適切にチューニングすれば逆転する可能性があります」と明記する。

#### [CH1-12] Medium — Unit 6 alt テキストに本文の色情報が反映されていない

- **Location**: `curriculum/unit06_clustering_algorithms/index.md:33, 35`
- **Evidence**: L33「オレンジと紫の2つの 重心（centroid） を中心に」/ L35 `alt="図解：K-Means の2クラスタと重心（Centroid A・B）"`（色の指定なし）
- **Failure scenario**: スクリーンリーダー利用者が alt テキストだけを読んだ場合、本文で言及されている色の情報が伝わらない。
- **Recommended action**: alt テキストに「オレンジと紫の2クラスタと重心」を含める。
- **Confidence**: Medium

#### [CH2-03] Medium — Unit 11 ダミーデータの論理的一貫性が低い

- **Location**: `curriculum/unit11_pytorch_basics/index.md:56-62`
- **Evidence**: 入力 `[2.0, 7.0]`（勉強2時間・睡眠7時間）が不合格(0)、`[5.0, 8.0]`（勉強5時間・睡眠8時間）が合格(1)という設定は常識的な因果関係と逆転。
- **Recommended action**: データを論理的に整合させるか、「これはダミーデータであり、必ずしも現実の因果関係を表していない」と注記する。

#### [CH2-04] Medium — Unit 12 Adam 学習率 lr=0.05 が異常に高い

- **Location**: `curriculum/unit12_optimizers_loss/index.md:194`
- **Evidence**: `optimizer = optim.Adam(model.parameters(), lr=0.05)`
- **Recommended action**: `lr=0.001` または `lr=0.01` に修正。教育的意図がある場合はコメントで明記する。

#### [CH2-05] Medium — Unit 13 評価フェーズで検証データを使用していない

- **Location**: `curriculum/unit13_regularization/index.md:248-255`
- **Evidence**: `final_pred = model(X_train)`（X_val が定義されていない）
- **Recommended action**: `X_val` / `y_val` を別途生成し、検証データでの Loss を表示するコードに変更する。

#### [CH2-06] Medium — Unit 13 Early Stopping でベストモデルの保存・復元がない

- **Location**: `curriculum/unit13_regularization/index.md:137-167`
- **Evidence**: `best_val_loss` 更新時に `torch.save` や `model.load_state_dict` がない。
- **Recommended action**: `torch.save(model.state_dict(), 'best_model.pth')` を追加し、早期終了後に `model.load_state_dict(...)` で復元するコードを追加する。

#### [CH2-07] Medium — Unit 14 畳み込み出力サイズ計算で padding=1 の効果が未説明

- **Location**: `curriculum/unit14_cnn_basics/index.md:116-122`
- **Evidence**: `self.conv1 = nn.Conv2d(..., padding=1)` だが、解説では「プーリングで縦横が半分になる」ことのみ強調。
- **Recommended action**: 「`padding=1` かつ `kernel_size=3` の場合、畳み込み後のサイズは入力と同じになる」と明記する。

#### [CH2-08] Medium — Unit 16 Capstone で初出概念が一括導入

- **Location**: `curriculum/unit16_deep_learning_capstone/index.md:38-499`
- **Evidence**: `torchvision.transforms`、`matplotlib`、`torch.save/load_state_dict` が Unit 10-15 で前提説明なしに使用。
- **Recommended action**: Unit 14 で `transforms` を導入、Unit 13 または 16 で学習曲線プロットを解説、モデル保存にミニ解説を添える。

#### [CH2-09] Medium — Unit 11 テンソル概念の説明が薄い

- **Location**: `curriculum/unit11_pytorch_basics/index.md:24-27`
- **Evidence**: テンソルの次元概念、shape確認方法、バッチ次元の意味が未説明。
- **Recommended action**: スカラー→ベクトル→行列→テンソルの図解と `tensor.shape` / `tensor.ndim` の確認コードを追加する。

#### [CH2-10] Medium — Unit 14 `x.view(-1, ...)` は非連続テンソルで RuntimeError の可能性

- **Location**: `curriculum/unit14_cnn_basics/index.md:208`
- **Evidence**: `x = x.view(-1, 16 * 8 * 8)`
- **Recommended action**: `x = torch.flatten(x, 1)` または `nn.Flatten()` に変更する。

#### [CH3-02] Medium — Unit 17 Janome の surface 出力を「語幹抽出」と結びつける記述が不整合

- **Location**: `curriculum/unit17_nlp_preprocessing_tfidf/index.md:28`
- **Evidence**: L18「『走る』『走った』『走れ』は同じ『走る』という行動を指しています（ステミング・レンマ化による語幹抽出）。」→ L36 `print(tokens)  # ['私', 'は', '今日', '図書館', 'に', '行き', 'まし', 'た']`
- **Recommended action**: `token.base_form` を使う1行例を追加し、surface と base_form の違いを明示する。

#### [CH3-03] Medium — Unit 18 本文と図でアナロジー計算式の言語・記号が不一致

- **Location**: `curriculum/unit18_word_embeddings_word2vec/index.md:28` / `diagram-concept.svg`
- **Evidence**: 本文 L28「`王様 - 男 + 女 = 女王`」／ SVG「`king - man + woman ≈ queen`」
- **Recommended action**: 本文を `王様 − 男 + 女 ≈ 女王` に統一し、「この計算は厳密な一致ではなく近似である」旨を1文追加する。

#### [CH3-04] Medium — Unit 18 極小コーパスで `most_similar` の期待値と注記が自己矛盾

- **Location**: `curriculum/unit18_word_embeddings_word2vec/index.md:102`
- **Evidence**: L118「（例：queen, manなど）が高い類似度スコアで出力されます。」→ L121「出力は実行するたびに変わりえます。」
- **Recommended action**: L118 の「（例：queen, manなど）」を削除し、「出力される単語は実行ごとに変わる」に一本化する。

#### [CH3-05] Medium — Unit 19 LSTM を「3つのゲート」のみで説明（セル状態更新式欠落）

- **Location**: `curriculum/unit19_rnns_lstms/index.md:46–50`
- **Evidence**: L41「内部に **3つのゲート（門）** を持っている」／ L46–48 の表（忘却・入力・出力ゲートのみ）
- **Recommended action**: 「厳密には、3つのゲートに加えて『新しい記憶の候補（candidate cell state）』を作る処理があり、この4要素でセル状態を更新します」というコラムを追加する。

#### [CH3-06] Medium — Unit 19 "apple" 課題の解説が LSTM の強みを誇張

- **Location**: `curriculum/unit19_rnns_lstms/index.md:252`
- **Evidence**: 「LSTMは『今までどの文字が来たか』という文脈（記憶）を持っているため…」（位置オフセットで説明可能な現象を LSTM の記憶力の証拠として扱っている）
- **Recommended action**: 解説を「この例では系列の順番を追跡する必要があり、隠れ状態がその役割を担う」とトーンを下げる。

#### [CH3-10] Medium — Unit 20 「コンテキスト長」等の制約を唐突に羅列

- **Location**: `curriculum/unit20_attention_transformers/index.md:10`
- **Evidence**: 「Transformerにも計算量、コンテキスト長、位置情報、推論速度などの制約があります。」（本章および Unit 21 で一切深掘りされない）
- **Recommended action**: 各制約を脚注1行ずつで軽く解説するか、「計算量は系列長の二乗に比例するため、長文では工夫が必要」の1文を追加する。

#### [CH3-12] Medium — Unit 21 概要が「4文だけで学習」とのみ言及（5文拡張を隠している）

- **Location**: `curriculum/unit21_nlp_capstone/index.md:11, 174`
- **Evidence**: L11「4文だけで学習するため…」／ L188「以下の拡張された『5文の対訳データセット』を用い…」
- **Recommended action**: L11 を「まず4文の最小実装で Transformer の部品を確認し、次に5文に拡張して LSTM との比較・選定を行います」と2段構成を明示する。

#### [CH3-13] Medium — Unit 21 `max_len=64` がマジックナンバー化

- **Location**: `curriculum/unit21_nlp_capstone/index.md:92, 168–178`
- **Evidence**: L84 `def __init__(self, d_model, max_len=64):` ／ L157 `for _ in range(10):`
- **Recommended action**: L84 にコメントで「コーパスの最長文（4語）＋特殊トークン＋余裕を見て 64 に設定。推論ループの上限 10 もこれ以下」と1行追加する。

#### [CH3-14] Medium — 全5ファイルで NLP 用語の表記ゆれ

- **Location**: Unit 17-21 全体
- **Evidence**: 「トークン化」「分かち書き」「形態素解析」「分散表現」「Embedding」「埋め込み」が混在。
- **Recommended action**: Unit 17 冒頭に「本章の用語集」ボックスを設け、対応表を掲載する。

#### [CH3-15] Medium — Unit 19 で PyTorch がインストール手順なしに突然登場

- **Location**: `curriculum/unit19_rnns_lstms/index.md:98` / `curriculum/unit21_nlp_capstone/index.md:34`
- **Evidence**: Unit19 L98 `import torch`（インストール手順なし）／ Unit21 L34「事前に `pip install torch` を実行してください。」（初めての手順言及が Unit 21）
- **Recommended action**: Unit 19 の実装例冒頭に「本章から PyTorch を使用します。未インストールの場合は `pip install torch` を実行してください」と1行追加する。

#### [CH4-05] Medium — Unit 28 `ChatMessageHistory` のインポート元が旧式

- **Location**: `curriculum/unit28_context_aware_chatbot/index.md:59-60`
- **Evidence**: `from langchain_community.chat_message_histories import ChatMessageHistory`
- **Recommended action**: 最新の LangChain ドキュメントで推奨されるインポートパスを確認し、必要に応じて変更する。

#### [CH4-06] Medium — Unit 33/34 で「Agent SDK」が実ライブラリかシミュレーションか曖昧

- **Location**: `curriculum/unit33_agent_sdk_general_agents/index.md:10` / `unit34_agent_sdk_coding_agents/index.md:7-11`
- **Evidence**: 行 10 で「概念を確認するシミュレーションです」と明記しつつ、OpenAI Agents SDK を実名で紹介後、実装例は完全自作シミュレーション。
- **Recommended action**: 冒頭で「本章では実際の SDK は使用せず、SDK の概念を理解するためのシミュレーションコードを記述します」と明確に断る。

#### [CH4-07] Medium — Unit 29 ReAct エージェントの戻り値が成功/タイムアウトで同型

- **Location**: `curriculum/unit29_ai_agent_implementation/index.md:397, 419`
- **Evidence**: 正常完了時 `return response_message.content` / タイムアウト時 `return "処理がタイムアウトしました。"`（両方 str 型）
- **Recommended action**: 戻り値を `Tuple[bool, str]` または `Optional[str]` に変更する。

#### [CH4-08] Medium — Unit 23 「温度感（ランダム性）」が不自然

- **Location**: `curriculum/unit23_llm_api/index.md:29`
- **Evidence**: `温度感（ランダム性）など細かく設定可能`
- **Recommended action**: 「temperature（出力のランダム性を調整するパラメータ）」または「温度パラメータ（ランダム性）」に変更する。

#### [CH4-09] Medium — RAG 3連続（24→25→26）が冗長

- **Location**: `curriculum/unit24_vector_dbs_rag_from_scratch/index.md` / `unit25_langchain_basics_rag/index.md` / `unit26_llamaindex_basics_rag/index.md`
- **Evidence**: 3ユニット連続で同一の社内規定FAQ RAG を構築。
- **Recommended action**: Unit 25 を「LangChain による RAG」、Unit 26 を「LlamaIndex による RAG と3手法比較」として差別化を強化する。

#### [CH4-10] Medium — Unit 33/34 で OpenAI API キーが必要と案内（実際は使用しない）

- **Location**: `curriculum/unit33_agent_sdk_general_agents/index.md:7-9` / `unit34_agent_sdk_coding_agents/index.md:7-11`
- **Evidence**: IMPORTANT コールアウトで「OpenAI の API キーが必要です」と案内しているが、実装例は OpenAI API を使用しないシミュレーションコード。
- **Recommended action**: 「本章では OpenAI API キーは使用しません。概念的なシミュレーションコードを実行します」と明記する。

#### [CH4-11] Medium — Unit 30 MCP の時系列情報がない

- **Location**: `curriculum/unit30_mcp_fundamentals/index.md:13`
- **Evidence**: 「Anthropic が提唱した」のみで、発表時期（2024年11月）や Linux Foundation への寄贈（2025年）といった情報がない。
- **Recommended action**: 「2024年11月に Anthropic が提唱し、2025年には Linux Foundation 傘下の Agents 標準化プロジェクトへ寄贈された」といった時系列情報を1行追加する。

#### [CH4-12] Medium — Unit 31 の冒頭で認知ジャンプが大きい

- **Location**: `curriculum/unit31_smolagents_code_agent/index.md:13`
- **Evidence**: 「Unit 27〜28において、Chainingやチャットボットの実装、さらにUnit 29〜30において、AIエージェントの基本原理…」と急にエージェントの話に移行。
- **Recommended action**: 「Unit 27–28 では LLM の基本的な使い方（チェーン、メモリ）を学び、Unit 29–30 ではエージェントの自律性とツール連携を学びました。ここからはエージェントの実装パラダイムを比較します」と橋渡しの説明を追加する。

#### [CH4-13] Medium — Unit 32 で `TypedDict` / `Literal` 等の型ヒント知識が前提

- **Location**: `curriculum/unit32_langgraph_stateful_agents/index.md:83-87`
- **Evidence**: `class TicketState(TypedDict):` / `def route_ticket(state: TicketState) -> Literal["billing", "technical", "escalate"]:` / `# type: ignore[return-value]`
- **Recommended action**: 冒頭で「本章では Python の型ヒント（`TypedDict`, `Literal`）を使用します。第X章で学習済みを前提とします」と明記する。

#### [CH4-14] Medium — Unit 25-28 が LangChain に偏重

- **Location**: Unit 25-28
- **Evidence**: Unit 25–28 はすべて LangChain を使用。Unit 26 のみ LlamaIndex を扱うが、Unit 27–28 は LangChain に戻る。
- **Recommended action**: Unit 27 または Unit 28 の実装例を LlamaIndex 版に変更するか、Unit 26 で LlamaIndex の ChatMemory 機能を追加で扱う。

#### [CH5-06] Medium — Unit 38 概念図でテーブルモーダルが欠落

- **Location**: `curriculum/unit38_multimodal_fraud_detection/index.md:28-30`
- **Evidence**: 行28: `本文の3モーダルのうち、図では代表的な2モーダルに簡略化しています`（テーブルモーダルが図から完全に欠落）
- **Recommended action**: 概念図にテーブルモーダルを追加して3モーダル構成にするか、注記を「テーブルモーダルは図では省略（実装コードに含まれる）」とより明確に修正する。

#### [CH5-07] Medium — Unit 41 「探索上限付近」という表現が誤解を招く

- **Location**: `curriculum/unit41_timeseries_price_optimizer/index.md:327`
- **Evidence**: 理論最適価格1,281円は探索範囲600〜1,300円の上限近くに位置するが、「探索上限付近」という表現で境界への張り付きを強調。
- **Recommended action**: 「理論最適値1,281円は探索範囲600〜1,300円の上限近くに位置するため、木モデルの外挿限界により予測が平坦化しやすい。このため探索境界を学習データ範囲内に厳密に設定することが重要」と説明する。

#### [CH5-08] Medium — Unit 41 「ディープラーニングモデルを学んできました」が曖昧

- **Location**: `curriculum/unit41_timeseries_price_optimizer/index.md:9`
- **Evidence**: 「これまで、テーブルデータの回帰や分類（Unit 1〜8）、およびディープラーニングモデルを学んできました。」（具体的なユニット番号なし）
- **Recommended action**: 「ディープラーニングモデル（Unit 10〜16の画像分類など）」と具体的に明記する。

#### [CH5-09] Medium — Unit 37 「完全に保証するわけではありません」が「部分的には保証する」と誤読される余地

- **Location**: `curriculum/unit37_llm_harness_capstone/index.md:20`
- **Evidence**: 「測定だけで品質を完全に保証するわけではありません。」
- **Recommended action**: 「評価ハーネスは品質改善の指標を提供しますが、品質を保証するものではありません。本番運用では人手レビューと継続的監視が必須です」と修正する。

#### [CH5-10] Medium — Unit 42 「セキュリティ境界の分離が困難」が誤解を招く

- **Location**: `curriculum/unit42_multiagent_customer_support/index.md:14`
- **Evidence**: 行14 で問題提起し、行39 で「エージェントの分割だけでセキュリティ境界が成立するわけではない」と補足（25行離れている）。
- **Recommended action**: 行14 の直後に「（ただし、分割だけでは不十分で、認証・認可等の実装が必須。詳細は後述）」と注記を追加する。

#### [CH5-11] Medium — Unit 40 「CoT を課し」で精度向上を断言

- **Location**: `curriculum/unit40_guardrails_evaluation_harness/index.md:242`
- **Evidence**: 「LLMジャッジに Chain of Thought（思考のプロセス）を課し、文脈から判断させることで誤判定を最小限に抑える。」
- **Recommended action**: 「Chain of Thoughtなどの推論促進手法を適用し、検証用ケースで効果を測定することで誤判定を抑制する」と、効果の検証プロセスを明記する。

#### [CH5-12] Medium — Unit 39 「失敗」という表現が強すぎる

- **Location**: `curriculum/unit39_knowledge_structuring_agent/index.md:13-17`
- **Evidence**: 「なぜ単なる LLM 呼び出しでは失敗するのか？」
- **Recommended action**: 「なぜ単なる LLM 呼び出しでは本番運用に不十分なのか？」と見出しを修正する。

---

### Low（22件）

#### [CH1-09] Low — Unit 2/5 で Wine データセットの test_size が異なる

- **Location**: `curriculum/unit02_logistic_regression/index.md:129` / `unit05_gradient_boosting_xgboost/index.md:112`
- **Evidence**: Unit 2 は test_size=0.3、Unit 5 は test_size=0.2。
- **Recommended action**: 両ユニットで test_size を統一するか、Unit 5 に「Unit 2 と分割比率が異なるため直接比較はできません」と注記する。

#### [CH1-10] Low — Unit 4 本文の日本語質問と図の英語ラベルが乖離

- **Location**: `curriculum/unit04_decision_trees_random_forests/index.md:21-30`
- **Evidence**: 本文「羽が生えている？」「散歩が好き？」/ 図 alt「Feathers? / Walks?」
- **Recommended action**: 図のラベルを日本語に統一するか、L28 で「図では英語表記になっています」と明記する。

#### [CH2-11] Low — Unit 12 「5隠れ層」が「5つの隠れ層」と誤読される

- **Location**: `curriculum/unit12_optimizers_loss/index.md:179`
- **Evidence**: `# 3入力 -> 5隠れ層 -> 3出力`
- **Recommended action**: `# 3入力 -> 隠れ層(5ユニット) -> 3出力` に修正する。

#### [CH2-12] Low — Unit 15 転移学習の注意点が1文に過密

- **Location**: `curriculum/unit15_transfer_learning/index.md:23`
- **Evidence**: 1文に5つの概念が詰め込まれ、「利用できる場合がありますが」という hedging が不信感を与える。
- **Recommended action**: 2文に分割する。

#### [CH2-13] Low — Unit 15 タイトルは ResNet だが練習問題は MobileNet V2

- **Location**: `curriculum/unit15_transfer_learning/index.md:1, 136-182`
- **Evidence**: タイトル「ResNet を用いた転移学習」/ 練習問題 `models.mobilenet_v2`
- **Recommended action**: 練習問題も ResNet を使用するか、タイトルを「学習済みモデルを用いた転移学習」に一般化する。

#### [CH2-14] Low — Unit 16 `torch.load()` に `weights_only=True` がない

- **Location**: `curriculum/unit16_deep_learning_capstone/index.md:496`
- **Evidence**: `model_b.load_state_dict(torch.load("resnet18_defect.pth"))`
- **Recommended action**: `torch.load(..., weights_only=True)` に修正する。

#### [CH2-15] Low — 全ユニットで旧式 `super(ClassName, self).__init__()` を使用

- **Location**: Unit 11-14
- **Evidence**: `super(ClassName, self).__init__()`（Python 2 互換の旧式）
- **Recommended action**: `super().__init__()` に統一する。

#### [CH2-16] Low — Unit 10 バイアスの説明が「関係ない」となっており本来の意味と矛盾

- **Location**: `curriculum/unit10_nn_from_scratch/index.md:22`
- **Evidence**: `「いや、うちの部署には関係ない（バイアス）」`
- **Recommended action**: `「そもそもうちの部署は前向きだ（バイアス）」` のように修正する。

#### [CH2-17] Low — 全7ファイルの hero 画像 alt が英語ベース

- **Location**: Unit 10-16
- **Evidence**: `alt="ヒーロー画像：Neural Networks from Scratch"` 等
- **Recommended action**: 日本語統一する（例: `alt="ヒーロー画像：ゼロから作るニューラルネットワーク"`）。

#### [CH3-16] Low — Unit 19 TF-IDF / Word2Vec を「記憶をリセットして読む」と擬人化

- **Location**: `curriculum/unit19_rnns_lstms/index.md:17-19`
- **Evidence**: 「普通のAI（これまでのモデル）の読み方：毎ページ、記憶をリセットして読みます。」
- **Recommended action**: 「これまでのモデル（TF-IDF・Word2Vec）には、そもそも『前の単語を覚えておく』という時間方向の仕組みがありませんでした。」と書き換える。

#### [CH3-17] Low — Unit 20 Self-Attention 例示テーブルにデータ行がない

- **Location**: `curriculum/unit20_attention_transformers/index.md:24-26`
- **Evidence**: 単語リストのヘッダー行のみで、アテンション重みのデータ行がない。
- **Recommended action**: 「it」の行に仮想的な重み値を入れたデータ行を1行追加するか、テーブルを削除して箇条書きに変更する。

#### [CH3-18] Low — Unit 21 図のノード数（4段階）が本文（5段階）より簡略化

- **Location**: `curriculum/unit21_nlp_capstone/index.md:21` / `diagram-concept.svg`
- **Evidence**: SVG「Text → Encoder → Decoder → Translation」（4ノード）／ 本文 L11「トークン化 ➔ 辞書作成 ➔ モデル構築 ➔ 学習ループ ➔ 推論デコード」（5段階）
- **Recommended action**: alt テキストを「図解：推論時の翻訳モデルの流れ（学習・トークン化は省略）」に変更する。

#### [CH4-15] Low — Unit 27 「プロンプトチェーン」「プロンプトチェイニング」「Chaining」の表記ゆれ

- **Location**: `curriculum/unit27_prompt_chaining/index.md:1, 16, 30`
- **Recommended action**: 「プロンプトチェーン（Prompt Chaining）」に統一する。

#### [CH4-16] Low — Unit 29-34 で「💡 日常の例え」が激減

- **Location**: Unit 29-34
- **Evidence**: Unit 23–28 は「💡 日常の例え」が複数存在、Unit 29–34 は Mermaid 図と技術説明が中心。
- **Recommended action**: Unit 29–34 にも簡単な日常例を1つ追加する。

#### [CH4-17] Low — Unit 34 「Linter/LSP」が初出で説明不足

- **Location**: `curriculum/unit34_agent_sdk_coding_agents/index.md:22`
- **Recommended action**: Appendix または脚注で LSP の簡単な説明を追加する。

#### [CH4-18] Low — Unit 33 「Handoffs」が初出で用語がブレている

- **Location**: `curriculum/unit33_agent_sdk_general_agents/index.md:33` / Unit 29, 32
- **Evidence**: Unit 33「Handoffs」/ Unit 29「ツール選択」/ Unit 32「委譲」
- **Recommended action**: Unit 29 または Unit 33 で「Handoffs（ツール委譲、ハンドオフ）」として用語を統一する。

#### [CH4-19] Low — Unit 23 に tiktoken のインストール指示がない

- **Location**: `curriculum/unit23_llm_api/index.md:117 付近（pip install 記述部）および 148-167（tiktoken 使用コード）`
- **Evidence**: Unit 23 行 148–167 に `import tiktoken` + `tiktoken.encoding_for_model("gpt-4o-mini")` の実コードが存在するが、インストール案内は `pip install openai` のみで `pip install tiktoken` の明示指示がない。Unit 35 の実践はこのコードを参照している。
- **Failure scenario**: tiktoken 未導入の読者が Unit 23 のトークン数測定コード（およびそれを参照する Unit 35 の実践）で `ModuleNotFoundError` に遭遇する。
- **Recommended action**: Unit 23 のインストール案内に `pip install tiktoken` を追記する。
- **Confidence**: High

#### [CH5-13] Low — Unit 37 `temperature=0.0` のコメント「候補値」が不自然

- **Location**: `curriculum/unit37_llm_harness_capstone/index.md:107, 227, 288`
- **Evidence**: `temperature=0.0, # 評価の揺らぎを抑える候補値。ブレや誤判定をゼロにはできない`
- **Recommended action**: `temperature=0.0, # 再現性を最大化（ただし完全な決定論的動作は保証されない）` と修正する。

#### [CH5-14] Low — Unit 38 「約15%」の乱数変動説明がない

- **Location**: `curriculum/unit38_multimodal_fraud_detection/index.md:41`
- **Evidence**: 行41「本ユニットのデータは不正が約15%ですが」/ コード `y_labels = (np.random.rand(n_samples) < 0.15).astype(int)`
- **Recommended action**: 「約15%（乱数シードにより若干変動）」と注記を追加する。

#### [CH5-15] Low — Unit 42 「Devin等のクローン」が商用製品名で陳腐化リスク

- **Location**: `curriculum/unit42_multiagent_customer_support/index.md:47`
- **Evidence**: `AIによる自律型ソフトウェア開発（Devin等のクローン）`
- **Recommended action**: 「AIによる自律型ソフトウェア開発（自律コーディングエージェント）」と一般化するか、「（例：Devin、2026年時点）」と時点を明記する。

#### [CH5-16] Low — Unit 40 「無認可の具体的な銘柄推奨」が冗長

- **Location**: `curriculum/unit40_guardrails_evaluation_harness/index.md:51`
- **Evidence**: `無認可の具体的な銘柄推奨を行わないよう`
- **Recommended action**: 「未許可の投資助言（具体的な銘柄推奨）を行わないよう」または「具体的な銘柄推奨（無認可の投資助言）を行わないよう」と整理する。

---

## Rejected findings（偽陽性・取り下げ）

### [CH1-11] Low — 取り下げ（サブエージェント自身が取り下げ）

- **Location**: 全ユニットの Markdown 表
- **Claim**: 先頭セルが空
- **棄却理由**: 再確認の結果、先頭セルは空ではなく正常なヘッダー行であることを確認。サブエージェント自身が取り下げ。

### [CH4-04] High — 棄却（aggregator 直接検証で偽陽性と確認）

- **Location**: `curriculum/unit26_llamaindex_basics_rag/index.md:38`
- **Claim**: HTML img タグの構文が不正（`class="unit-diagram" /` とクローズタグ `/>` が分離）
- **棄却理由**: aggregator が `search_files` で Unit 26 の全 `<img>` タグを直接確認した結果、行 4, 31, 38 すべて正常な `<img ... class="unit-diagram" />` であった。偽陽性。

---

## Verification plan（Pass 2 以降で実施）

1. **Hero 画像の実画像目視確認**: M1/M2 のタイポ・論理矛盾を実画像で確認（vision 誤認識の除外）
2. **Unit 35 コードの追加実行**: merges 引数を変えた再実行で図の修正方針を確定
3. **`npm run docs:build`**: 修正後の VitePress ビルドで参照・画像の整合を確認
4. **`python3 scripts/verify_curriculum_diagrams.py`**: 図の検証スクリプトで一貫性確認
5. **Critical/High findings の直接検証**: Pass 2 で修正前に、CH1-01, CH3-07, CH5-01 および主要 High findings を aggregator が直接コード/テキストで再確認

---

**Pass 1（証拠収集）は完了しました。**

このレビュー結果を確認し、採用する finding についてクロスモデル検証と修正の適用を希望する場合は、次のように返信してください:

> **「検証して修正」**

（Pass 2 では、採用した finding を現在のファイルに対して再確認し、Reference モデルの助言で severity・因果・修正案を検証したうえで、承認された最小限の修正を適用します。）
