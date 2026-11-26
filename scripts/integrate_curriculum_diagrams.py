#!/usr/bin/env python3
"""Move unit diagrams inline with explanatory bridge text (Japanese curriculum)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "docs/curriculum"

IMG_CONCEPT = re.compile(
    r'\n*<img src="[^"]*diagram-concept\.svg"[^>]*class="unit-diagram"\s*/>\n*',
    re.MULTILINE,
)
IMG_WORKFLOW = re.compile(
    r'\n*<img src="[^"]*diagram-workflow\.svg"[^>]*class="unit-diagram"\s*/>\n*',
    re.MULTILINE,
)

SKIP_SLUGS = {
    "unit00_roadmap",
    "unit01_linear_regression",
    "unit02_logistic_regression",
    "unit03_knn_svm",
    "unit04_decision_trees_random_forests",
    "unit06_clustering_algorithms",
    "unit10_nn_from_scratch",
}

# slug -> (concept_bridge, concept_anchor, workflow_bridge, workflow_anchor)
# anchor: unique substring of ### heading to insert AFTER that subsection body
UNIT_CONFIG: dict[str, tuple[str, str, str, str]] = {
    "unit05_gradient_boosting_xgboost": (
        "下図は、前のモデルの **残差（誤差）** を次の木が順番に補正していくブースティングの流れです。",
        "### 勾配ブースティングとは",
        "下図は、左の **並列投票（Random Forest）** と、右の **逐次補正（XGBoost）** の違いを比較したものです。",
        "### XGBoostとは",
    ),
    "unit07_dimensionality_reduction": (
        "下図は、3次元の点群を **主成分方向** に射影して2次元に圧縮する PCA のイメージです。",
        "### PCA（主成分分析）の仕組み",
        "下図は、次元削減の主な活用場面（可視化・高速化・ノイズ除去）をまとめたものです。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit08_cross_validation_tuning": (
        "下図は、5分割交差検証で **各フォールドが1回ずつテスト役** になる様子です。",
        "### 交差検証（Cross Validation）",
        "下図は、ハイパーパラメータの組み合わせを試し、 **最高スコアの設定** を選ぶグリッドサーチです。",
        "### ハイパーパラメータ・チューニング",
    ),
    "unit09_classical_ml_capstone": (
        "下図は、データ読み込みから評価までの **エンドツーエンド ML パイプライン** です。",
        "## 1. エンドツーエンド",
        "下図は、プロジェクトの成果物（メトリクス・モデル・再現可能なノートブック）を示しています。",
        "<<before>>## 2. 実装例",
    ),
    "unit11_pytorch_basics": (
        "下図は、 **Tensor** の形状と `matmul` による順伝播のイメージです。",
        "**PyTorchは「魔法のレゴブロック」**",
        "下図は、`loss.backward()` で勾配を求め、 **optimizer** で重みを更新する1ステップです。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit12_optimizers_loss": (
        "下図は、回帰向け **MSE** と分類向け **Cross-entropy** の損失曲線の違いです。",
        "| **Adam (アダム)**",
        "下図は、固定ステップの **SGD** と適応的な **Adam** の更新の違いです。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit13_regularization": (
        "下図は、左の **過学習（ノイズへの追従）** と、右の **Dropout** による正則化を比較しています。",
        "| **Dropout (ドロップアウト)**",
        "下図は、 **BatchNorm** による正規化→スケール→シフトの流れです。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit14_cnn_basics": (
        "下図は、 **Conv → Pool → Linear** と積み重なる特徴抽出のブロックです。",
        "**「畳み込み（特徴を探す）",
        "下図は、フィルタが画像上をスライドし **位置に依存しないパターン** を検出するイメージです。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit15_transfer_learning": (
        "下図は、 **凍結したバックボーン** と、自分のデータで学習する **新しい出力層** の構成です。",
        "転移学習（Transfer Learning）",
        "下図は、画像入力から特徴抽出、2クラス分類までの **ResNet フロー** です。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit16_deep_learning_capstone": (
        "下図は、データ読み込みから可視化までの **画像分類パイプライン** です。",
        "## 1. 総合ディープラーニング",
        "下図は、 **訓練精度と検証精度** の乖離を監視し、早期停止を判断するカーブです。",
        "<<before>>## 2. 実装例",
    ),
    "unit17_nlp_preprocessing_tfidf": (
        "下図は、テキストから **スパースな TF-IDF ベクトル** を作る前処理の流れです。",
        "### 📌 TF-IDFとは？",
        "下図は、 **TF（頻度）** と **IDF（希少性）** を掛け合わせて重要語を強調するイメージです。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit18_word_embeddings_word2vec": (
        "下図は、 **one-hot（疎）** から **密な埋め込み空間** への変換です。",
        "### 📌 Word2Vecとは？",
        "下図は、語彙をベクトルに変換して **ニューラルネットに入力** する埋め込み層です。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit19_rnns_lstms": (
        "下図は、時刻ごとに **隠れ状態 h_t** が前の状態に依存して伝わる RNN の展開です。",
        "### 📌 日常的な例え",
        "下図は、LSTM の **Forget / Input / Output** ゲートが情報の保持と更新を制御する様子です。",
        "### 📌 LSTMの3つのゲート機構",
    ),
    "unit20_attention_transformers": (
        "下図は、 **Query × Key** で得た重みを使い、各トークンが他トークンを参照する Attention です。",
        "### 📌 日常的な例え",
        "下図は、Transformer ブロックの **Multi-head Attention → FFN → Add+Norm** の流れです。",
        "### 📌 Transformerとは？",
    ),
    "unit21_nlp_capstone": (
        "下図は、テキスト整形から評価レポートまでの **NLP プロジェクト全体の流れ** です。",
        "## 1. 総合自然言語処理",
        "下図は、 **TF-IDF + 古典的 ML** と **Embeddings + NN** のスタック比較です。",
        "<<before>>## 2. 実装例",
    ),
    "unit22_llm_evolution": (
        "下図は、 **Completion API → RAG → Agent** へと能力が拡張していく進化の道筋です。",
        "### 技術の進化と関係性マップ",
        "下図は、エージェントが **計画・ツール呼び出し・反復** でタスクを遂行する流れです。",
        "### 💡 日常の例え話で理解する",
    ),
    "unit23_llm_api": (
        "下図は、アプリから **POST /chat/completions** へ送り、JSON で応答を受け取る API フローです。",
        "### LLM APIとは？",
        "下図は、 **Zero-shot / Few-shot / Chain-of-thought** のプロンプトパターンの比較です。",
        "### ③ Chain-of-Thought",
    ),
    "unit24_vector_dbs_rag_from_scratch": (
        "下図は、文書の **Chunk → Embed → Retrieve → LLM** という RAG パイプラインです。",
        "### RAG",
        "下図は、クエリ **Q** からコサイン類似度で **top-k** チャンクを検索する様子です。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit25_langchain_basics_rag": (
        "下図は、LangChain における **Document loader → Vector store → RetrievalQA** の RAG チェーンです。",
        "### LangChain",
        "下図は、 **Prompt templates / Output parsers / Chains** などの再利用可能な抽象化です。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit26_llamaindex_basics_rag": (
        "下図は、LlamaIndex の **Load docs → Build index → query()** というデータ中心の流れです。",
        "### LlamaIndex とは？",
        "下図は、 **LangChain** と **LlamaIndex** の RAG 設計思想の比較です。",
        "<<before>>## 2. 実装例",
    ),
    "unit27_prompt_chaining": (
        "下図は、 **Prompt A の出力を Prompt B に渡す** チェーンの流れです。",
        "### プロンプトチェーン（Prompt Chaining）",
        "下図は、タスク分割・デバッグ・品質向上といった **チェーン化の利点** です。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit28_context_aware_chatbot": (
        "下図は、過去の **User / Bot メッセージを履歴として保持** し、毎回 API に送る構成です。",
        "### メモリ（記憶）の必要性",
        "下図は、 **入力欄・スレッド表示・API 呼び出し** からなるチャット UI の流れです。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit29_ai_agent_implementation": (
        "下図は、 **Thought → Action → Observation** を繰り返す ReAct ループです。下の repeat 矢印が反復を表します。",
        "### 1.1 ReAct",
        "下図は、ツール定義から実行までの **スクラッチエージェント** の構成です。",
        "### 1.2 OpenAI Tool Calling",
    ),
    "unit30_mcp_fundamentals": (
        "下図は、 **MCP Client（ホストアプリ）** と **MCP Server（ツール群）** の接続アーキテクチャです。",
        "### 1.1 MCP の 3層アーキテクチャ",
        "下図は、関数を公開し **Stdio/HTTP** 経由でクライアントに発見されるサーバー構築の流れです。",
        "### 💡 具体的なビジネスユースケース",
    ),
    "unit31_smolagents_code_agent": (
        "下図は、LLM がコードを書き、 **サンドボックスで実行** して結果を返すコードエージェントのループです。",
        "### smolagents と「Code Agent」",
        "下図は、軽量ライブラリによる **ツールルーティング** の特徴をまとめたものです。",
        "<<before>>## 2. 実装例",
    ),
    "unit32_langgraph_stateful_agents": (
        "下図は、LangGraph の **State / Node / Edge** というグラフの基本要素です。",
        "### 1.1 なぜグラフなのか？",
        "下図は、問い合わせを **Classify → Billing / Technical / Escalate** に振り分けるルーティングです。",
        "### 1.3 代表的なユースケース",
    ),
    "unit33_agent_sdk_general_agents": (
        "下図は、 **Define agent → Add tools → Run task** という汎用エージェントの流れです。",
        "### 1.1 マネージド Agent SDK",
        "下図は、レポート生成・データ処理・自動化など **SDK エージェントのユースケース** です。",
        "<<before>>## 2. 実装例",
    ),
    "unit34_agent_sdk_coding_agents": (
        "下図は、 **Read repo → Edit code → Run tests** のコーディングエージェントの反復です。",
        "### 1.1 自律コーディング",
        "下図は、小さな差分とテスト実行を繰り返す **安全な開発プラクティス** です。",
        "<<before>>## 2. 実装例",
    ),
    "unit35_tokenizer_bpe": (
        "下図は、文字単位から頻出ペアを結合し、再利用できるVocabularyを作る中心概念です。",
        "### BPEの基本的な考え方",
        "下図は、学習済みVocabularyを使うTokenizer実行時の流れです。",
        "<<before>>## 2. 実装例",
    ),
    "unit36_lora_qlora": (
        "下図は、凍結したベース重み`W`に、学習可能な低ランク更新`B × A`を加えるLoRAの構造です。",
        "## 1. ファインチューニングとLoRAの理解",
        "下図は、ベースモデルを凍結し、必要に応じて量子化してからLoRAアダプターを取り付け、学習・評価する流れです。",
        "<<before>>## 2. 実装例",
    ),
    "unit37_llm_harness_capstone": (
        "下図は、 **Generation → Evaluation → Feedback** の二重ハーネス構成です。",
        "### ハーネスエンジニアリングとは？",
        "下図は、本番運用時にこの評価器を組み込む発展形で、ポリシー検査・LLM ジャッジ・フォールバックを重ねる **多層防御** の構成です（ランタイム防御の詳細は Unit 40 で扱います）。",
        "<<before>>## 2. 実装例",
    ),
    "unit38_multimodal_fraud_detection": (
        "下図は、 **Text / Image エンコーダ** のスコアを統合する Late fusion アーキテクチャです。",
        "### モーダル融合（Fusion）",
        "下図は、テキストと画像の **矛盾シグナル** から不正スコアを上げる流れです。",
        "<<before>>## 2. 実装例",
    ),
    "unit39_knowledge_structuring_agent": (
        "下図は、 **PDF → Agent 抽出 → JSON スキーマ** のナレッジ構造化パイプラインです。",
        "### 自律型構造化エージェント",
        "下図は、構造化データを **ナレッジグラフ・クエリ可能なレコード** として活用する流れです。",
        "<<before>>## 2. 実装例",
    ),
    "unit40_guardrails_evaluation_harness": (
        "下図は、 **Input → Guardrail → Safe out** の入出力ガードレールです。",
        "### 🛡️ Guardrails の位置づけ",
        "下図は、 **Test cases → LLM judge → Scores** の評価ハーネスと回帰追跡です。",
        "### 🧠 LLM-as-a-Judge",
    ),
    "unit41_timeseries_price_optimizer": (
        "下図は、過去データのみで学習し **未来を予測する時系列 ML**（リーク回避）のイメージです。",
        "### 🚨 時系列データリーク",
        "下図は、需要曲線上の **最適価格点（optimal）** で収益を最大化するダイナミックプライシングです。",
        "### 📈 需要予測から価格最適化",
    ),
    "unit42_multiagent_customer_support": (
        "下図は、 **Triage** から Billing / Tech / Sales へ振り分けるマルチエージェントの流れです。",
        "### 🤝 マルチエージェント",
        "下図は、エージェント間で **共有コンテキストを引き継ぎ** 解決する協調の流れです。",
        "### 💡 具体的なビジネスユースケース",
    ),
}

FALLBACK_SECTION2 = re.compile(r"(\n## 2\.)")


def _extract_img(pattern: re.Pattern[str], text: str) -> tuple[str, str]:
    m = pattern.search(text)
    if not m:
        return text, ""
    tag = m.group().strip()
    before = text[: m.start()].rstrip()
    after = text[m.end() :].lstrip()
    if before and after:
        return before + "\n\n" + after, tag
    if before:
        return before + "\n", tag
    if after:
        return after, tag
    return "", tag


def _insert_after_anchor(
    text: str, anchor: str, bridge: str, img_tag: str
) -> tuple[str, bool]:
    if not img_tag or not anchor:
        return text, False
    if anchor.startswith("<<before>>"):
        anchor = anchor[len("<<before>>") :]
        idx = text.find(anchor)
        if idx < 0:
            return text, False
        before = text[:idx].rstrip()
        prefix = f"{before}\n\n" if before else ""
        return f"{prefix}{bridge}\n\n{img_tag}\n\n{text[idx:]}", True

    idx = text.find(anchor)
    if idx < 0:
        return text, False
    # end of subsection: next ### or ## or --- at line start
    rest = text[idx:]
    m = re.search(r"\n(?=### |## |---\n)", rest[1:])
    end = idx + 1 + m.start() if m else len(text)
    before = text[:end].rstrip()
    after = text[end:]
    block = f"\n\n{bridge}\n\n{img_tag}\n"
    return before + block + after, True


def _already_integrated(text: str, img_tag: str) -> bool:
    if not img_tag:
        return True
    pos = text.find(img_tag)
    if pos < 0:
        return False
    before = text[max(0, pos - 200) : pos]
    return "下図" in before or "図は" in before


def _find_img(pattern: re.Pattern[str], text: str) -> str:
    m = pattern.search(text)
    return m.group().strip() if m else ""


def _integrate_img(
    text: str, pattern: re.Pattern[str], anchor: str, bridge: str
) -> str:
    stripped, img_tag = _extract_img(pattern, text)
    if not img_tag:
        return text
    updated, inserted = _insert_after_anchor(stripped, anchor, bridge, img_tag)
    return updated if inserted else text


def _integrate_fallback(text: str, pattern: re.Pattern[str]) -> str:
    stripped, img_tag = _extract_img(pattern, text)
    if not img_tag:
        return text
    sec2 = FALLBACK_SECTION2.search(stripped)
    if not sec2:
        return text
    before = stripped[: sec2.start()].rstrip()
    prefix = f"{before}\n\n" if before else ""
    return f"{prefix}{img_tag}\n{sec2.group(1)}{stripped[sec2.end():]}"


def process_file(path: Path, dry_run: bool) -> bool:
    slug = path.parent.name
    if slug in SKIP_SLUGS:
        return False

    original = path.read_text(encoding="utf-8")
    concept_tag = _find_img(IMG_CONCEPT, original)
    workflow_tag = _find_img(IMG_WORKFLOW, original)
    if not concept_tag and not workflow_tag:
        return False

    need_concept = bool(concept_tag) and not _already_integrated(original, concept_tag)
    need_workflow = bool(workflow_tag) and not _already_integrated(original, workflow_tag)
    if not need_concept and not need_workflow:
        return False

    text = original
    cfg = UNIT_CONFIG.get(slug)
    if cfg:
        c_bridge, c_anchor, w_bridge, w_anchor = cfg
        if need_concept:
            text = _integrate_img(text, IMG_CONCEPT, c_anchor, c_bridge)
        if need_workflow:
            text = _integrate_img(text, IMG_WORKFLOW, w_anchor, w_bridge)
    else:
        # fallback: place un-integrated imgs at end of section 1 before ## 2.
        if need_concept:
            text = _integrate_fallback(text, IMG_CONCEPT)
        if need_workflow:
            text = _integrate_fallback(text, IMG_WORKFLOW)

    if text == original:
        return False
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    if text == original:
        return False
    if not dry_run:
        path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    dry = "--dry-run" in sys.argv
    changed = 0
    for path in sorted(CURRICULUM.glob("unit*/index.md")):
        if process_file(path, dry):
            changed += 1
            print(("would fix: " if dry else "fixed: ") + str(path.relative_to(ROOT)))
    print(f"{'Would change' if dry else 'Changed'} {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
