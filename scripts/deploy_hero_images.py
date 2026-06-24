#!/usr/bin/env python3
"""Copy generated hero PNGs from Cursor assets to unit image folders."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path("/home/node/.cursor/projects/workspaces-build-to-learn-ai/assets")
DEST = ROOT / "assets" / "units"

SLUGS = [
    "unit04_decision_trees_random_forests",
    "unit05_gradient_boosting_xgboost",
    "unit06_clustering_algorithms",
    "unit07_dimensionality_reduction",
    "unit08_cross_validation_tuning",
    "unit09_classical_ml_capstone",
    "unit10_nn_from_scratch",
    "unit11_pytorch_basics",
    "unit12_optimizers_loss",
    "unit13_regularization",
    "unit14_cnn_basics",
    "unit15_transfer_learning",
    "unit16_deep_learning_capstone",
    "unit17_nlp_preprocessing_tfidf",
    "unit18_word_embeddings_word2vec",
    "unit19_rnns_lstms",
    "unit20_attention_transformers",
    "unit21_nlp_capstone",
    "unit22_llm_evolution",
    "unit23_llm_api",
    "unit24_vector_dbs_rag_from_scratch",
    "unit25_langchain_basics_rag",
    "unit26_llamaindex_basics_rag",
    "unit27_prompt_chaining",
    "unit28_context_aware_chatbot",
    "unit29_ai_agent_implementation",
    "unit30_mcp_fundamentals",
    "unit31_smolagents_code_agent",
    "unit32_agent_sdk_general_agents",
    "unit33_agent_sdk_coding_agents",
    "unit34_llm_harness_capstone",
    "unit35_multimodal_fraud_detection",
    "unit36_knowledge_structuring_agent",
    "unit37_guardrails_evaluation_harness",
    "unit38_timeseries_price_optimizer",
    "unit39_multiagent_customer_support",
]


def main() -> None:
    missing: list[str] = []
    for slug in SLUGS:
        num = slug.split("_")[0].replace("unit", "")
        src = SRC / f"unit{num}-hero.png"
        dest_dir = DEST / slug / "images"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / "hero.png"
        if not src.exists():
            missing.append(str(src))
            continue
        shutil.copy2(src, dest)
        print(f"  ✓ {slug}")

    if missing:
        print("\nMissing:")
        for m in missing:
            print(f"  - {m}")
        raise SystemExit(1)
    print(f"\nCopied {len(SLUGS)} hero images.")


if __name__ == "__main__":
    main()
