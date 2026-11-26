#!/usr/bin/env python3
"""Copy generated hero PNGs into all synchronized unit image folders."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST_DIRS = (
    ROOT / "docs" / "assets" / "units",
    ROOT / "docs" / "public" / "assets" / "units",
    ROOT / "docs" / "public" / "en" / "assets" / "units",
)

# Units 04–42 that ship raster hero.png assets.
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
    "unit32_langgraph_stateful_agents",
    "unit33_agent_sdk_general_agents",
    "unit34_agent_sdk_coding_agents",
    # unit35_tokenizer_bpe and unit36_lora_qlora use vector hero.svg
    "unit37_llm_harness_capstone",
    "unit38_multimodal_fraud_detection",
    "unit39_knowledge_structuring_agent",
    "unit40_guardrails_evaluation_harness",
    "unit41_timeseries_price_optimizer",
    "unit42_multiagent_customer_support",
]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Copy generated unitNN-hero.png files to docs/assets/units, "
            "docs/public/assets/units, and docs/public/en/assets/units."
        )
    )
    parser.add_argument(
        "src",
        nargs="?",
        default=os.environ.get("HERO_ASSETS_SRC"),
        help="Source directory containing unitNN-hero.png files (or set HERO_ASSETS_SRC).",
    )
    args = parser.parse_args(argv)
    if not args.src:
        parser.error(
            "Source directory is required: pass a directory path as a CLI argument "
            "or set the HERO_ASSETS_SRC environment variable."
        )
    return args


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    src_dir = Path(args.src).expanduser()
    if not src_dir.is_dir():
        print(f"Error: source directory does not exist: {src_dir}", file=sys.stderr)
        raise SystemExit(1)

    missing: list[str] = []
    copied = 0
    for slug in SLUGS:
        num = slug.split("_", 1)[0].removeprefix("unit")
        src = src_dir / f"unit{num}-hero.png"
        if not src.is_file():
            missing.append(str(src))
            continue
        for dest_root in DEST_DIRS:
            dest_dir = dest_root / slug / "images"
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest_dir / "hero.png")
        copied += 1
        print(f"  ✓ {slug}")

    if missing:
        print("\nMissing:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        raise SystemExit(1)
    print(
        f"\nCopied {copied} hero images to {len(DEST_DIRS)} destinations "
        f"({copied * len(DEST_DIRS)} files total)."
    )


if __name__ == "__main__":
    main()
