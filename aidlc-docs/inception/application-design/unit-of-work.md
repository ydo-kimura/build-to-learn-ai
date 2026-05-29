# ユニット（カリキュラム）定義 (Unit of Work Definitions)

本ドキュメントは、AIエンジニアとしての実力証明を目的としたポートフォリオプロジェクトにおける「学習・実践トピック（Unit）」の定義とコード構成戦略を記述します。

## コード構成戦略 (Code Organization Strategy)

- **アプローチ**: モノレポ構成 (Monorepo)
- **構造**: トピック（Unit）ごとに独立したディレクトリを作成します。
- **共有要素**: 共通のユーティリティ（APIキー管理やログ設定など）は、必要に応じて `shared/` などの共通ディレクトリに抽出しますが、基本的には各Unitが独立して動作するように設計します。

### 想定ディレクトリ構造
```text
/Volumes/External/Documents/job-change/
├── aidlc-docs/               # AI-DLCドキュメント
├── shared/                   # 共通設定・ユーティリティ（後から必要に応じて追加）
├── unit01-ml-basics/         # Unit 1: 機械学習・PyTorch基礎
├── unit02-simple-nn/         # Unit 2: PyTorchでのシンプルなNN実装
├── unit03-nlp-fundamentals/  # Unit 3: 自然言語処理の基礎（Word2Vec, RNN等）
├── unit04-transformer-intro/ # Unit 4: Transformerアーキテクチャの基礎
├── unit05-llm-api-usage/     # Unit 5: LLM API（OpenAI等）の基本的な利用
├── unit06-rag-from-scratch/  # Unit 6: フレームワークなしで作るRAG基礎
├── unit07-langchain-rag/     # Unit 7: LangChainを用いた実用的なRAG構築
├── unit08-prompt-chaining/   # Unit 8: プロンプトチェーンによる業務自動化
├── unit09-chatbot-memory/    # Unit 9: メモリ・コンテキスト管理を備えたチャットボット
└── unit10-ai-agent-poc/      # Unit 10: ツール呼び出し・自律エージェントの基礎
```

## Unit定義一覧

### Unit 1: Linear & Regularized Regression (線形回帰と正則化)
- **概要**: 機械学習の第一歩。線形回帰、Ridge回帰、Lasso回帰の実装。
- **アウトプット**: 住宅価格予測モデルと、L1/L2正則化による重みの変化の確認。

### Unit 2: Logistic Regression & Classification Metrics (ロジスティック回帰と評価指標)
- **概要**: 2値分類の基礎。ロジスティック回帰の実装と、適合率・再現率・F1スコア・ROC曲線の理解。
- **アウトプット**: タイタニックデータ等を用いた生存予測と混同行列の可視化。

### Unit 3: K-NN & Support Vector Machines (非線形分類の基礎)
- **概要**: 距離ベースのアルゴリズム(k-NN)と、マージン最大化(SVM)、カーネルトリックの理解。
- **アウトプット**: アヤメの分類と、決定境界（Decision Boundary）の可視化。

### Unit 4: Decision Trees & Random Forests (決定木とバギング)
- **概要**: 解釈性の高い決定木と、それを集積したランダムフォレスト（バギング）の実装。
- **アウトプット**: アンサンブル学習による精度向上と「特徴量重要度」の抽出。

### Unit 5: Gradient Boosting & XGBoost (勾配ブースティング)
- **概要**: 実務コンペで最強クラスの予測精度を誇る勾配ブースティング（XGBoostやLightGBM）の学習。
- **アウトプット**: XGBoostを用いた高精度予測モデルの実装。

### Unit 6: Clustering Algorithms (クラスタリング)
- **概要**: 正解データのない教師なし学習。K-Means法と階層的クラスタリング。
- **アウトプット**: 顧客データのセグメンテーション（グループ分け）。

### Unit 7: Dimensionality Reduction - PCA (主成分分析)
- **概要**: 多次元データの次元を削減し、情報を圧縮・可視化するPCAの理解。
- **アウトプット**: 高次元データ（画像や特徴量群）の2次元プロット可視化。

### Unit 8: Cross Validation & Hyperparameter Tuning (交差検証とチューニング)
- **概要**: 汎化性能を測る交差検証（CV）と、GridSearchやOptunaを用いたハイパーパラメータの自動最適化。
- **アウトプット**: 既存モデルの精度を極限まで引き上げるOptuna最適化スクリプト。

---
## 【第2章】ディープラーニング基礎 (Deep Learning Fundamentals)

### Unit 9: Neural Networks from Scratch (ゼロから作るNN)
- **概要**: NumPyのみで順伝播と誤差逆伝播（バックプロパゲーション）を実装し、数理的基礎を体得。
- **アウトプット**: NumPy製MLPによるXOR問題や単純な分類タスクの解決。

### Unit 10: PyTorch Basics & Simple MLP (PyTorch入門)
- **概要**: PyTorchのテンソル操作、Autograd（自動微分）、Dataset/DataLoaderの基本構造。
- **アウトプット**: PyTorchを用いた標準的な学習ループと推論パイプライン。

### Unit 11: Optimizers & Loss Functions (最適化手法と損失関数)
- **概要**: SGD、Momentum、Adamなど最適化手法の違いと、回帰/分類における適切な損失関数の選択。
- **アウトプット**: 異なるOptimizerでの学習曲線の比較（TensorBoard可視化）。

### Unit 12: Regularization in DL (DLの過学習対策)
- **概要**: Dropout、Batch Normalization、Early Stoppingなど、深いネットワークを安定させる技術。
- **アウトプット**: 過学習を起こすモデルに対する正則化手法の適用と改善の確認。

### Unit 13: CNN Basics (CNNの基礎)
- **概要**: 画像認識の要である畳み込み層（Conv2D）とプーリング層の理解。
- **アウトプット**: 手書き数字（MNIST）やCIFAR-10を用いたシンプルなCNN分類器。

### Unit 14: Transfer Learning with ResNet (転移学習)
- **概要**: 事前学習済みモデル（ResNet等）の重みを利用し、少ないデータで高精度なモデルを作る手法。
- **アウトプット**: 犬猫分類などのカスタムデータセットに対する高精度な転移学習モデル。

---
## 【第3章】自然言語処理とモダンアーキテクチャ (NLP & Modern Architectures)

### Unit 15: NLP Preprocessing & TF-IDF (NLPの前処理)
- **概要**: 形態素解析、ストップワード除去、トークン化と、古典的なTF-IDFによるベクトル化。
- **アウトプット**: テキストデータの前処理パイプライン構築。

### Unit 16: Word Embeddings (単語の分散表現)
- **概要**: Word2VecやGloVeなど、単語を密ベクトル空間に配置する技術の理解。
- **アウトプット**: 単語間の類似度計算やベクトル演算（王 - 男 + 女 = 女王）のPoC。

### Unit 17: RNNs & LSTMs (系列データとRNN)
- **概要**: 時系列やテキストの順序を考慮するRNNと、長期記憶を保持するLSTMの実装。
- **アウトプット**: LSTMを用いたテキスト分類（感情分析）モデル。

### Unit 18: Attention & Transformers (Transformerアーキテクチャ)
- **概要**: 現代LLMの心臓部であるSelf-Attention機構の概念理解とミニ実装。
- **アウトプット**: Attention機構のシンプルなスクラッチ実装と重みの可視化。

---
## 【第4章】LLM応用とAIエージェント (LLM Applied & AI Agents)

### Unit 19: LLM API Usage & Prompting (LLM APIとプロンプト)
- **概要**: OpenAI APIなどの利用法と、Few-shot、Chain-of-Thoughtなどのプロンプトエンジニアリング。
- **アウトプット**: 構造化データ（JSON等）を安定して出力させるAPIラッパー。

### Unit 20: Vector DBs & RAG From Scratch (手組みRAG)
- **概要**: ChromaDB等のベクトルDBの使い方と、フレームワークなしでのRAG（検索拡張生成）の実装。
- **アウトプット**: 手作りのシンプルな文書検索・回答スクリプト。

### Unit 21: LangChain Basics & RAG (LangChainを用いたRAG)
- **概要**: LangChainのエコシステム（Loader, Splitter, VectorStore, Retriever）を活用した堅牢なRAG。
- **アウトプット**: PDF等から情報を抽出して回答する実用的なRAGシステム。

### Unit 22: Prompt Chaining (プロンプトチェーン)
- **概要**: 出力結果を次のプロンプトの入力に渡すパイプラインを構築し、段階的な推論を自動化。
- **アウトプット**: 分類→抽出→要約のようなマルチステップの推論スクリプト。

### Unit 23: Context-Aware Chatbot (コンテキスト対応チャットボット)
- **概要**: 対話履歴（メモリ）の保持とコンテキストウィンドウ管理を備えたUI付きチャットボット。
- **アウトプット**: Streamlit等を用いた対話型チャットボットアプリケーション。

### Unit 24: AI Agent Implementation (AIエージェントの実装)
- **概要**: ツール呼び出し（Function Calling）とReActパターンによる自律的なタスク解決エージェント。
- **アウトプット**: ユーザーの意図を解釈して複数の関数を組み合わせ実行する自律エージェント。
