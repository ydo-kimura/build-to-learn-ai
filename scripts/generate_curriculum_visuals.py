#!/usr/bin/env python3
"""Generate rich hero PNGs and section SVG diagrams for curriculum units 4–39."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from curriculum_svg_lib import (
    diagram_card,
    diagram_compare,
    flow_horizontal,
    hero_two_panel,
    mini_agent_evolution,
    mini_api_flow,
    mini_attention,
    mini_autograd,
    mini_animal_tree,
    mini_chat_history,
    mini_cnn,
    mini_code_agent,
    mini_coding_agent,
    mini_crossval,
    mini_dbscan,
    mini_doc_extract,
    mini_dropout,
    mini_embedding,
    mini_eval_harness,
    mini_fusion,
    mini_grid_search,
    mini_guardrails,
    mini_kmeans,
    mini_langgraph,
    mini_state_graph,
    mini_loss_curves,
    mini_lstm,
    mini_mcp,
    mini_multi_agent,
    mini_nn_layers,
    mini_optimizers,
    mini_overfit,
    mini_parallel_trees,
    mini_pca,
    mini_pipeline,
    mini_pricing,
    mini_rag,
    mini_react_loop,
    mini_rf_vote,
    mini_rnn,
    mini_sequential_boost,
    mini_tensor,
    mini_tfidf,
    mini_timeseries,
    mini_train_val,
    mini_training_loop,
    mini_transfer,
    mini_transformer,
    mini_vector_search,
)

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "units"

# slug -> (title, hero_fn, concept_fn, workflow_fn)
# Each *_fn returns SVG string
UNIT_BUILDERS: dict[str, tuple] = {}


def _register(slug: str, title: str, hero, concept, workflow):
    UNIT_BUILDERS[slug] = (title, hero, concept, workflow)


_register(
    "unit04_decision_trees_random_forests",
    "Decision Trees & Random Forests",
    lambda: hero_two_panel(
        "Decision Trees & Random Forests",
        "Decision Tree", "Yes/No splits → classify",
        mini_animal_tree(),
        "Random Forest", "Many trees vote",
        mini_rf_vote(),
    ),
    lambda: diagram_card(
        "Decision Tree: animal classification",
        mini_animal_tree(),
        "Each split asks the best Yes/No question",
    ),
    lambda: diagram_card(
        "Random Forest: majority vote",
        mini_rf_vote(),
        "Tree 1→A, Tree 2→A, Tree 3→B → Majority A",
        accent="#7c3aed",
    ),
)

_register(
    "unit05_gradient_boosting_xgboost",
    "Gradient Boosting & XGBoost",
    lambda: hero_two_panel(
        "Gradient Boosting & XGBoost",
        "Random Forest", "Parallel trees vote",
        mini_parallel_trees(),
        "Boosting", "Fix prior errors sequentially",
        mini_sequential_boost(),
        right_color="#f59e0b",
    ),
    lambda: diagram_card(
        "Sequential boosting: correct residuals",
        mini_sequential_boost(compact=True),
        "Each tree learns the previous model's error",
    ),
    lambda: diagram_compare(
        "Random Forest (parallel)",
        mini_parallel_trees(compact=True),
        "XGBoost (sequential + fast)",
        mini_sequential_boost(compact=True),
    ),
)

_register(
    "unit06_clustering_algorithms",
    "Clustering Algorithms",
    lambda: hero_two_panel(
        "Clustering Algorithms",
        "K-Means", "Find K centroids",
        mini_kmeans(),
        "DBSCAN", "Density-based clusters",
        mini_dbscan(),
        right_color="#8b5cf6",
    ),
    lambda: diagram_card("K-Means: assign → move centroids → repeat", mini_kmeans(), "Best for round blob-shaped clusters"),
    lambda: diagram_compare("K-Means", mini_kmeans(compact=True), "DBSCAN", mini_dbscan(compact=True), "DBSCAN finds arbitrary shapes + labels noise"),
)

_register(
    "unit07_dimensionality_reduction",
    "Dimensionality Reduction",
    lambda: hero_two_panel(
        "Dimensionality Reduction (PCA)",
        "High-D data", "Many correlated features",
        mini_pca(),
        "PCA projection", "Keep most variance in fewer dims",
        mini_pca(),
        right_color="#f97316",
    ),
    lambda: diagram_card("PCA: project 3D cloud onto 2D plane", mini_pca(), "Lose the least important variance"),
    lambda: diagram_card(
        "Use cases",
        flow_horizontal([("Visualize", "#3b82f6"), ("Speed up", "#8b5cf6"), ("Denoise", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit08_cross_validation_tuning",
    "Cross Validation & Tuning",
    lambda: hero_two_panel(
        "Cross Validation & Hyperparameter Tuning",
        "K-Fold CV", "Rotate test folds",
        mini_crossval(),
        "Grid Search", "Try hyperparameter combos",
        mini_grid_search(),
        right_color="#22c55e",
    ),
    lambda: diagram_card("5-Fold cross validation", mini_crossval(), "Each fold takes a turn as test set; average scores"),
    lambda: diagram_card("Hyperparameter grid search", mini_grid_search(), "Pick best combo by CV score", accent="#7c3aed"),
)

_register(
    "unit09_classical_ml_capstone",
    "Classical ML Capstone",
    lambda: hero_two_panel(
        "Classical ML Capstone",
        "Raw data", "Features + labels",
        mini_pipeline(),
        "Full pipeline", "Train → tune → evaluate",
        flow_horizontal([("Metrics", "#ec4899"), ("Model", "#22c55e"), ("Notebook", "#3b82f6")], y=50),
    ),
    lambda: diagram_card("End-to-end ML pipeline", mini_pipeline(), "Load → clean → split → model → tune"),
    lambda: diagram_card(
        "Deliverables",
        flow_horizontal([("Metrics report", "#ef4444"), ("Saved model", "#22c55e"), ("Reproducible notebook", "#3b82f6")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit10_nn_from_scratch",
    "Neural Networks from Scratch",
    lambda: hero_two_panel(
        "Neural Networks from Scratch",
        "Forward pass", "Input → hidden → output",
        mini_nn_layers(),
        "Training loop", "Forward → loss → backward → update",
        mini_training_loop(),
        right_color="#f59e0b",
    ),
    lambda: diagram_card("Network layers", mini_nn_layers(), "Input layer → hidden layer → output layer"),
    lambda: diagram_card("Training loop", mini_training_loop(), "Compute loss, backprop gradients, update weights", accent="#7c3aed"),
)

_register(
    "unit11_pytorch_basics",
    "PyTorch Basics",
    lambda: hero_two_panel(
        "PyTorch Basics",
        "Tensor", "Multi-dimensional arrays",
        mini_tensor(),
        "Autograd", "Automatic gradients",
        mini_autograd(),
        right_color="#7c3aed",
    ),
    lambda: diagram_card("Tensor shapes & matrix multiply", mini_tensor(), "(batch, features) → logits"),
    lambda: diagram_card("Training step", mini_autograd(), "loss.backward() → optimizer.step()", accent="#22c55e"),
)

_register(
    "unit12_optimizers_loss",
    "Optimizers & Loss Functions",
    lambda: hero_two_panel(
        "Optimizers & Loss Functions",
        "Loss function", "Measure prediction error",
        mini_loss_curves(),
        "Optimizer", "Update weights toward minimum",
        mini_optimizers(),
        right_color="#22c55e",
    ),
    lambda: diagram_card(
        "MSE vs Cross-Entropy",
        mini_loss_curves(),
    ),
    lambda: diagram_card(
        "SGD vs Adam",
        mini_optimizers(),
    ),
)

_register(
    "unit13_regularization",
    "Regularization in Deep Learning",
    lambda: hero_two_panel(
        "Regularization in Deep Learning",
        "Overfitting", "Memorize training noise",
        mini_overfit(),
        "Dropout / BatchNorm", "Improve generalization",
        mini_dropout(),
        left_color="#ef4444",
        right_color="#22c55e",
    ),
    lambda: diagram_compare("Overfitting", mini_overfit(compact=True), "Dropout", mini_dropout(compact=True), "Randomly zero neurons during training"),
    lambda: diagram_card(
        "BatchNorm",
        flow_horizontal([("Normalize", "#3b82f6"), ("Scale", "#8b5cf6"), ("Shift", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit14_cnn_basics",
    "CNN Basics",
    lambda: hero_two_panel(
        "Convolutional Neural Networks",
        "Convolution", "Detect local features",
        mini_cnn(),
        "Why CNN?", "Keep spatial structure",
        mini_cnn(),
        right_color="#22c55e",
    ),
    lambda: diagram_card("CNN block: Conv → ReLU → Pool → Linear", mini_cnn(), "Stack blocks to learn hierarchical features"),
    lambda: diagram_card(
        "Translation tolerance",
        flow_horizontal([("Filter slides", "#3b82f6"), ("Same pattern", "#8b5cf6"), ("Anywhere", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit15_transfer_learning",
    "Transfer Learning",
    lambda: hero_two_panel(
        "Transfer Learning",
        "Pretrained backbone", "ImageNet weights (frozen)",
        mini_transfer(),
        "Fine-tune head", "Train on your classes",
        mini_transfer(),
        right_color="#22c55e",
    ),
    lambda: diagram_card("Freeze backbone, replace last layer", mini_transfer(), "Reuse learned features with small labeled data"),
    lambda: diagram_card(
        "ResNet18 flow",
        flow_horizontal([("224×224", "#3b82f6"), ("Features", "#8b5cf6"), ("2-class", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit16_deep_learning_capstone",
    "Deep Learning Capstone",
    lambda: hero_two_panel(
        "Deep Learning Capstone",
        "Data + augment", "Custom image dataset",
        flow_horizontal([("Dataset", "#3b82f6"), ("Augment", "#8b5cf6"), ("ResNet", "#22c55e")], y=50),
        "Train + monitor", "Watch train vs val curves",
        mini_train_val(),
        right_color="#f59e0b",
    ),
    lambda: diagram_card("Image classification pipeline", flow_horizontal([("Load", "#3b82f6"), ("Augment", "#f59e0b"), ("Fine-tune", "#22c55e"), ("Plot", "#ec4899")], y=30), "End-to-end image ML project"),
    lambda: diagram_card("Evaluation: train vs validation curves", mini_train_val(), "Early stopping when val loss diverges", accent="#7c3aed"),
)

_register(
    "unit17_nlp_preprocessing_tfidf",
    "NLP Preprocessing & TF-IDF",
    lambda: hero_two_panel(
        "NLP Preprocessing & TF-IDF",
        "Raw text", "Tokenize + clean",
        mini_tfidf(),
        "TF-IDF vector", "Sparse word importance",
        mini_tfidf(),
        right_color="#8b5cf6",
    ),
    lambda: diagram_card("Text preprocessing pipeline", mini_tfidf(), "Lowercase → remove stopwords → tokenize"),
    lambda: diagram_card(
        "TF-IDF intuition",
        flow_horizontal([("High TF", "#3b82f6"), ("× high IDF", "#f59e0b"), ("= important", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit18_word_embeddings_word2vec",
    "Word Embeddings (Word2Vec)",
    lambda: hero_two_panel(
        "Word Embeddings (Word2Vec)",
        "One-hot", "Sparse huge vectors",
        mini_embedding(),
        "Dense embedding", "Similar words close together",
        mini_embedding(),
        right_color="#22c55e",
    ),
    lambda: diagram_card("Word2Vec: train on context", mini_embedding(), "king - man + woman ≈ queen"),
    lambda: diagram_card(
        "Embedding layer",
        flow_horizontal([("vocab", "#3b82f6"), ("→ vector", "#8b5cf6"), ("→ NN", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit19_rnns_lstms",
    "RNNs & LSTMs",
    lambda: hero_two_panel(
        "RNNs & LSTMs",
        "RNN", "Sequential hidden state",
        mini_rnn(),
        "LSTM", "Gated long-term memory",
        mini_lstm(),
        right_color="#7c3aed",
    ),
    lambda: diagram_card("RNN unrolling through time", mini_rnn(), "h_t depends on h_{t-1}; vanishing gradient risk"),
    lambda: diagram_card("LSTM gates: forget / input / output", mini_lstm(), "Better for long sequences", accent="#7c3aed"),
)

_register(
    "unit20_attention_transformers",
    "Attention & Transformers",
    lambda: hero_two_panel(
        "Attention & Transformers",
        "Self-Attention", "All token pairs relate",
        mini_attention(),
        "Transformer block", "Parallel sequence processing",
        mini_transformer(),
        right_color="#22c55e",
    ),
    lambda: diagram_card("Attention weights: Query × Key", mini_attention(), "Weighted sum of Values for each token"),
    lambda: diagram_card("Transformer block", mini_transformer(), "Multi-head attention → FFN → residual + norm", accent="#7c3aed"),
)

_register(
    "unit21_nlp_capstone",
    "NLP Capstone",
    lambda: hero_two_panel(
        "NLP Capstone",
        "Text data", "Preprocess + featurize",
        mini_tfidf(),
        "Model + eval", "End-to-end NLP project",
        flow_horizontal([("Clean", "#3b82f6"), ("Train", "#22c55e"), ("Metrics", "#ec4899")], y=50),
    ),
    lambda: diagram_card("Translation model flow", flow_horizontal([("Text", "#3b82f6"), ("Encoder", "#8b5cf6"), ("Decoder", "#f59e0b"), ("Translation", "#22c55e")], y=30)),
    lambda: diagram_compare("TF-IDF + ML", mini_tfidf(compact=True), "Embeddings+NN", mini_embedding(compact=True), "Choose stack based on data size and task"),
)

_register(
    "unit22_llm_evolution",
    "LLM to AI Agent Evolution",
    lambda: hero_two_panel(
        "LLM → AI Agent Evolution",
        "LLM", "Text in → text out",
        flow_horizontal([("Prompt", "#3b82f6"), ("LLM", "#8b5cf6"), ("Text", "#22c55e")], y=50),
        "AI Agent", "Tools + memory + planning",
        mini_agent_evolution(),
        right_color="#22c55e",
    ),
    lambda: diagram_card("Evolution path", mini_agent_evolution(), "Completion API → RAG → Agents with tools"),
    lambda: diagram_card(
        "Agent capabilities",
        flow_horizontal([("Plan", "#3b82f6"), ("Call APIs", "#f59e0b"), ("Iterate", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit23_llm_api",
    "LLM API & Prompting",
    lambda: hero_two_panel(
        "LLM API & Prompting",
        "Your app", "HTTP request to API",
        mini_api_flow(),
        "Prompt patterns", "Zero / few / chain-of-thought",
        flow_horizontal([("Zero-shot", "#3b82f6"), ("Few-shot", "#8b5cf6"), ("CoT", "#22c55e")], y=50),
        right_color="#f59e0b",
    ),
    lambda: diagram_card("API call flow", mini_api_flow(), "system + user messages → model → completion"),
    lambda: diagram_card("Prompt patterns", flow_horizontal([("Zero-shot", "#3b82f6"), ("Few-shot", "#8b5cf6"), ("Chain-of-thought", "#22c55e")], y=30), "Choose pattern based on task complexity", accent="#7c3aed"),
)

_register(
    "unit24_vector_dbs_rag_from_scratch",
    "Vector DBs & Scratch RAG",
    lambda: hero_two_panel(
        "Vector DBs & RAG from Scratch",
        "Documents", "Chunk + embed + store",
        mini_rag(),
        "Retrieve + generate", "Grounded LLM answer",
        mini_vector_search(),
        right_color="#ec4899",
    ),
    lambda: diagram_card("RAG pipeline", mini_rag(), "Chunk docs → embed → store → query → top-k → LLM"),
    lambda: diagram_card("Vector search", mini_vector_search(), "Cosine similarity returns relevant chunks", accent="#7c3aed"),
)

_register(
    "unit25_langchain_basics_rag",
    "LangChain Basics & RAG",
    lambda: hero_two_panel(
        "LangChain Basics & RAG",
        "LangChain", "Composable chains",
        mini_rag(),
        "RAG chain", "Retriever + LLM",
        flow_horizontal([("Loader", "#3b82f6"), ("Vector store", "#8b5cf6"), ("QA chain", "#22c55e")], y=50),
    ),
    lambda: diagram_card("LangChain RAG", flow_horizontal([("Document loader", "#3b82f6"), ("Vector store", "#8b5cf6"), ("RetrievalQA", "#22c55e")], y=30), "Plug-and-play RAG components"),
    lambda: diagram_card(
        "Abstractions",
        flow_horizontal([("Prompt templates", "#3b82f6"), ("Output parsers", "#8b5cf6"), ("Chains", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit26_llamaindex_basics_rag",
    "LlamaIndex Basics & RAG",
    lambda: hero_two_panel(
        "LlamaIndex Basics & RAG",
        "Index", "Structured document data",
        flow_horizontal([("Load", "#3b82f6"), ("Index", "#8b5cf6"), ("Store", "#22c55e")], y=50),
        "Query engine", "Natural language Q&A",
        flow_horizontal([("Query", "#f59e0b"), ("Retrieve", "#8b5cf6"), ("Answer", "#22c55e")], y=50),
        right_color="#22c55e",
    ),
    lambda: diagram_card("LlamaIndex flow", flow_horizontal([("Load docs", "#3b82f6"), ("Build index", "#8b5cf6"), ("query()", "#22c55e")], y=30), "Data-centric indexing API"),
    lambda: diagram_compare("LangChain", mini_rag(compact=True), "LlamaIndex", flow_horizontal([("Index", "#3b82f6"), ("Query engine", "#22c55e")], y=30), "LlamaIndex: simpler query API, data-first"),
)

_register(
    "unit27_prompt_chaining",
    "Prompt Chaining",
    lambda: hero_two_panel(
        "Prompt Chaining",
        "Step 1", "Extract facts",
        flow_horizontal([("Prompt A", "#3b82f6"), ("Output", "#8b5cf6")], y=55),
        "Step 2", "Reason + final answer",
        flow_horizontal([("Prompt B", "#f59e0b"), ("Result", "#22c55e")], y=55),
        right_color="#22c55e",
    ),
    lambda: diagram_card("Chain of prompts", flow_horizontal([("Prompt A", "#3b82f6"), ("→ output", "#8b5cf6"), ("→ Prompt B", "#f59e0b"), ("→ final", "#22c55e")], y=30), "Feed prior output into next prompt"),
    lambda: diagram_card(
        "Why chain?",
        flow_horizontal([("Break tasks", "#3b82f6"), ("Debug steps", "#8b5cf6"), ("Better quality", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit28_context_aware_chatbot",
    "Context-Aware Chatbot",
    lambda: hero_two_panel(
        "Context-Aware Chatbot",
        "User message", "New conversation turn",
        mini_chat_history(),
        "Chat history", "Remember prior context",
        mini_chat_history(),
        right_color="#7c3aed",
    ),
    lambda: diagram_card("Session memory", mini_chat_history(), "Store past messages; send history each API call"),
    lambda: diagram_card(
        "Chat loop",
        flow_horizontal([("User input", "#3b82f6"), ("Add to history", "#8b5cf6"), ("API call", "#f59e0b"), ("Reply", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit29_ai_agent_implementation",
    "AI Agent (ReAct)",
    lambda: hero_two_panel(
        "AI Agent (ReAct)",
        "Thought", "Plan next step",
        mini_react_loop(),
        "Action + observe", "Tool use loop",
        mini_react_loop(),
        right_color="#22c55e",
    ),
    lambda: diagram_card("ReAct loop", mini_react_loop(), "Thought → Action → Observation → repeat"),
    lambda: diagram_card(
        "Scratch agent",
        flow_horizontal([("Define tools", "#3b82f6"), ("Parse LLM", "#8b5cf6"), ("Execute", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit30_mcp_fundamentals",
    "Model Context Protocol",
    lambda: hero_two_panel(
        "Model Context Protocol (MCP)",
        "MCP Client", "Host application",
        mini_mcp(),
        "MCP Server", "Tools + resources",
        mini_mcp(),
        right_color="#7c3aed",
    ),
    lambda: diagram_card("MCP architecture", mini_mcp(), "Client discovers server → call tools via protocol"),
    lambda: diagram_card(
        "Build a server",
        flow_horizontal([("Expose functions", "#3b82f6"), ("Stdio/HTTP", "#8b5cf6"), ("Discover", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit31_smolagents_code_agent",
    "smolagents Code Agent",
    lambda: hero_two_panel(
        "smolagents Code Agent",
        "Natural language", "Task description",
        flow_horizontal([("Task", "#3b82f6"), ("LLM", "#8b5cf6")], y=55),
        "Code execution", "Python in sandbox",
        mini_code_agent(),
        right_color="#f59e0b",
    ),
    lambda: diagram_card("Code agent loop", mini_code_agent(), "LLM writes code → sandbox runs → return result"),
    lambda: diagram_card(
        "Code agent cycle",
        flow_horizontal([("Task", "#3b82f6"), ("Write code", "#8b5cf6"), ("Sandbox run", "#f59e0b"), ("Result", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit32_langgraph_stateful_agents",
    "LangGraph: Stateful Agents",
    lambda: hero_two_panel(
        "LangGraph: Stateful Agents",
        "Ticket input", "Shared state (TypedDict)",
        mini_langgraph(),
        "Graph routing", "Nodes + conditional edges",
        flow_horizontal([("Classify", "#3b82f6"), ("Route", "#8b5cf6"), ("Respond", "#22c55e")], y=50),
        right_color="#7c3aed",
    ),
    lambda: diagram_card(
        "Graph concepts",
        mini_state_graph(),
    ),
    lambda: diagram_card(
        "Support routing",
        mini_langgraph(),
        "Classify → billing / technical / escalate",
        accent="#7c3aed",
    ),
)

_register(
    "unit33_agent_sdk_general_agents",
    "Agent SDK: General Agents",
    lambda: hero_two_panel(
        "Agent SDK: General Agents",
        "Business task", "Multi-step workflow",
        flow_horizontal([("Task", "#3b82f6"), ("Agent", "#8b5cf6"), ("Tools", "#22c55e")], y=50),
        "Orchestrated", "Autonomous execution",
        flow_horizontal([("Report", "#ec4899"), ("Process", "#f59e0b"), ("Done", "#22c55e")], y=50),
    ),
    lambda: diagram_card("General agent", flow_horizontal([("Define agent", "#3b82f6"), ("Add tools", "#8b5cf6"), ("Run task", "#22c55e")], y=30), "SDK-managed autonomous agent"),
    lambda: diagram_card(
        "Use cases",
        flow_horizontal([("Report gen", "#3b82f6"), ("Data processing", "#8b5cf6"), ("Automation", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit34_agent_sdk_coding_agents",
    "Agent SDK: Coding Agents",
    lambda: hero_two_panel(
        "Agent SDK: Coding Agents",
        "Repo context", "Files + tests",
        mini_coding_agent(),
        "Edit + verify", "Propose changes, run tests",
        mini_coding_agent(),
        right_color="#22c55e",
    ),
    lambda: diagram_card("Coding agent flow", mini_coding_agent(), "Read codebase → propose edits → run tests"),
    lambda: diagram_card(
        "Best practices",
        flow_horizontal([("Small diffs", "#3b82f6"), ("Run tests", "#f59e0b"), ("Human review", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit35_llm_harness_capstone",
    "LLM Harness Capstone",
    lambda: hero_two_panel(
        "LLM Harness Capstone",
        "LLM output", "Needs quality checks",
        flow_horizontal([("Generate", "#3b82f6"), ("Output", "#8b5cf6")], y=55),
        "Eval harness", "Judge + guard + fallback",
        mini_eval_harness(),
        right_color="#ef4444",
    ),
    lambda: diagram_card("Dual harness", flow_horizontal([("Generation", "#3b82f6"), ("Evaluation", "#ef4444"), ("Feedback", "#22c55e")], y=30), "Generate and evaluate in one pipeline"),
    lambda: diagram_card(
        "Defense layers",
        flow_horizontal([("Policy", "#3b82f6"), ("LLM judge", "#8b5cf6"), ("Fallback", "#ef4444")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit36_multimodal_fraud_detection",
    "Multimodal Fraud Detection",
    lambda: hero_two_panel(
        "Multimodal Fraud Detection",
        "Text + image", "Two modalities",
        mini_fusion(),
        "Late fusion", "Combined fraud score",
        mini_fusion(),
        right_color="#ef4444",
    ),
    lambda: diagram_card("Late fusion architecture", mini_fusion(), "Text encoder + image encoder → merge scores"),
    lambda: diagram_card(
        "Fraud signals",
        flow_horizontal([("Suspicious text", "#ef4444"), ("Image mismatch", "#f59e0b"), ("High score", "#dc2626")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit37_knowledge_structuring_agent",
    "Knowledge Structuring Agent",
    lambda: hero_two_panel(
        "Knowledge Structuring Agent",
        "Unstructured docs", "Contracts, PDFs",
        mini_doc_extract(),
        "Structured JSON", "Entities + relations",
        mini_doc_extract(),
        right_color="#22c55e",
    ),
    lambda: diagram_card("Extraction agent", mini_doc_extract(), "Read document → extract schema fields → validate JSON"),
    lambda: diagram_card(
        "Output",
        flow_horizontal([("Knowledge graph", "#3b82f6"), ("Queryable", "#8b5cf6"), ("Records", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)

_register(
    "unit38_guardrails_evaluation_harness",
    "Guardrails & Evaluation",
    lambda: hero_two_panel(
        "Guardrails & Evaluation",
        "User input", "Risky content",
        mini_guardrails(),
        "Eval harness", "Test + score + track",
        mini_eval_harness(),
        left_color="#ef4444",
        right_color="#22c55e",
    ),
    lambda: diagram_card("Input/output guardrails", mini_guardrails(), "Block, rewrite, or reject unsafe content"),
    lambda: diagram_card("Evaluation harness", mini_eval_harness(), "Test cases + LLM-as-judge + regression tracking", accent="#7c3aed"),
)

_register(
    "unit39_timeseries_price_optimizer",
    "Time Series & Pricing",
    lambda: hero_two_panel(
        "Time Series & Dynamic Pricing",
        "Historical demand", "Time-indexed data",
        mini_timeseries(),
        "Forecast + price", "Optimize revenue",
        mini_pricing(),
        right_color="#22c55e",
    ),
    lambda: diagram_card("Time series ML", mini_timeseries(), "Train on past only — avoid data leakage"),
    lambda: diagram_card("Dynamic pricing", mini_pricing(), "Demand curve → pick optimal price point", accent="#7c3aed"),
)

_register(
    "unit40_multiagent_customer_support",
    "Multi-Agent Customer Support",
    lambda: hero_two_panel(
        "Multi-Agent Customer Support",
        "Triage agent", "Route incoming ticket",
        mini_multi_agent(),
        "Specialist agents", "Resolve by department",
        mini_multi_agent(),
        right_color="#22c55e",
    ),
    lambda: diagram_card("Multi-agent flow", mini_multi_agent(), "Classifier → department → expert agent responds"),
    lambda: diagram_card(
        "Coordination",
        flow_horizontal([("Shared context", "#3b82f6"), ("Handoff", "#f59e0b"), ("Resolve", "#22c55e")], y=30),
        accent="#7c3aed",
    ),
)


def svg_to_png(svg_path: Path, png_path: Path) -> None:
    result = subprocess.run(
        [
            "convert",
            "-background",
            "white",
            "-density",
            "144",
            "-font",
            "DejaVu-Sans",
            str(svg_path),
            str(png_path),
        ],
        capture_output=True,
    )
    if not png_path.exists() or png_path.stat().st_size < 8000:
        raise RuntimeError(
            f"Failed to convert {svg_path}: {result.stderr.decode(errors='replace')}"
        )


def write_assets(slug: str) -> None:
    _, _, concept_fn, workflow_fn = UNIT_BUILDERS[slug]
    img_dir = ASSETS / slug / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    # Hero PNG is generated separately via GenerateImage (see scripts/hero_prompts.py)
    (img_dir / "diagram-concept.svg").write_text(concept_fn(), encoding="utf-8")
    (img_dir / "diagram-workflow.svg").write_text(workflow_fn(), encoding="utf-8")
    print(f"  ✓ diagrams: {slug}")


def main() -> None:
    diagrams_only = len(sys.argv) > 1 and sys.argv[1] == "--diagrams-only"
    slugs = sorted(UNIT_BUILDERS.keys())

    print(f"Generating visuals for {len(slugs)} units...")
    for slug in slugs:
        if diagrams_only:
            _, _, concept_fn, workflow_fn = UNIT_BUILDERS[slug]
            img_dir = ASSETS / slug / "images"
            img_dir.mkdir(parents=True, exist_ok=True)
            (img_dir / "diagram-concept.svg").write_text(concept_fn(), encoding="utf-8")
            (img_dir / "diagram-workflow.svg").write_text(workflow_fn(), encoding="utf-8")
            print(f"  ✓ diagrams: {slug}")
        else:
            write_assets(slug)

    print("Done.")


if __name__ == "__main__":
    main()
