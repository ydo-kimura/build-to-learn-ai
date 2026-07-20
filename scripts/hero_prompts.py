"""Hero image prompts for units 4–39 (Unit 1–3 style educational infographics)."""

HERO_STYLE = (
    "Wide educational hero banner, 3:2 aspect ratio. "
    "CONCRETE and LITERAL infographic — NOT abstract art. "
    "Clean white background, textbook diagram aesthetic, "
    "large readable English labels, crisp sans-serif fonts, "
    "blue (#3b82f6) and accent colors, plenty of whitespace."
)

HERO_PROMPTS: dict[str, str] = {
    "unit04_decision_trees_random_forests": (
        f'{HERO_STYLE} Title at top: "Decision Trees & Random Forests". '
        "LEFT panel (blue border): a clear decision tree flowchart — root box "
        '"Feathers?" branches to "Bird" (yes) and "Walks?" (no), then Dog/Cat. '
        "RIGHT panel (purple border): three small tree icons each outputting A, A, B "
        'with a box below saying "Majority Vote → A". '
        "Caption under left: Yes/No splits. Caption under right: Many trees vote."
    ),
    "unit05_gradient_boosting_xgboost": (
        f'{HERO_STYLE} Title: "Gradient Boosting & XGBoost". '
        "LEFT: four parallel decision trees labeled Tree 1–4 with arrow to "
        '"Parallel Vote" (Random Forest style). '
        "RIGHT: three sequential boxes showing error correction: "
        '"+5m error" → "-4m fix" → "-1m fix" → "Final prediction" (Boosting). '
        "Labels: Parallel vs Sequential."
    ),
    "unit06_clustering_algorithms": (
        f'{HERO_STYLE} Title: "Clustering Algorithms". '
        "LEFT panel: K-Means scatter plot with 2 color clusters (orange, purple) "
        "and centroid markers labeled Centroid A, Centroid B. "
        "RIGHT panel: DBSCAN with two dense blob clusters circled and gray noise points. "
        "Labels: K-Means vs DBSCAN."
    ),
    "unit07_dimensionality_reduction": (
        f'{HERO_STYLE} Title: "PCA: Dimensionality Reduction". '
        "LEFT: 3D scatter cloud of blue points in a cube labeled High-D (100 features). "
        "CENTER: large arrow labeled Project. "
        "RIGHT: same points flattened on 2D plane labeled 2D (keep 95% variance). "
        "Show PCA concept visually."
    ),
    "unit08_cross_validation_tuning": (
        f'{HERO_STYLE} Title: "Cross Validation & Hyperparameter Tuning". '
        "LEFT: 5-fold CV diagram — 5 rows of colored train/test fold bars, "
        'labeled "Rotate test fold". '
        "RIGHT: 3×3 grid heatmap of scores (0.65–0.91) with best cell highlighted green "
        'labeled "Best: max_depth=5, lr=0.1".'
    ),
    "unit09_classical_ml_capstone": (
        f'{HERO_STYLE} Title: "Classical ML Capstone". '
        "Three sections left to right: "
        "(1) Raw data table icon with rows/columns labeled Features + Labels. "
        "(2) Large pipeline flowchart: Load → Clean → Split → Train → Tune → Predict "
        "with colored boxes and arrows. "
        "(3) Results panel: accuracy gauge 92%, saved model .pkl icon, notebook icon. "
        "Shows complete end-to-end ML project overview."
    ),
    "unit10_nn_from_scratch": (
        f'{HERO_STYLE} Title: "Neural Networks from Scratch". '
        "LEFT: neural network diagram — input nodes x1,x2,x3 connected to hidden h1,h2 "
        "connected to output y, with weight lines. "
        "RIGHT: training loop cycle: Forward → Loss → Backward → Update with arrows in a loop. "
        "Educational ML diagram style."
    ),
    "unit11_pytorch_basics": (
        f'{HERO_STYLE} Title: "PyTorch Basics". '
        "LEFT: 3D tensor block labeled shape (batch, features) with numbers inside. "
        "RIGHT: autograd flow: loss.backward() → gradients → optimizer.step() "
        "with code-style labels in boxes."
    ),
    "unit12_optimizers_loss": (
        f'{HERO_STYLE} Title: "Loss Functions & Optimizers". '
        "LEFT: two loss curves — red MSE curve and blue cross-entropy curve on axes. "
        "RIGHT: optimization path — dashed SGD zigzag vs smooth Adam curve descending to minimum. "
        "Labels: MSE / Cross-entropy, SGD / Adam."
    ),
    "unit13_regularization": (
        f'{HERO_STYLE} Title: "Regularization in Deep Learning". '
        "LEFT: overfitting graph — wavy red curve through blue data points, "
        'labeled "Memorizes noise". '
        "RIGHT: dropout network — some neurons crossed out randomly, "
        'labeled "Dropout 50%" and "Generalizes better".'
    ),
    "unit14_cnn_basics": (
        f'{HERO_STYLE} Title: "CNN Basics". '
        "LEFT: small image grid (pixel squares) with convolution filter sliding over it, "
        "showing feature map output. "
        "RIGHT: CNN architecture: Image → Conv2d → ReLU → MaxPool → Linear → Class label. "
        "Show spatial feature detection."
    ),
    "unit15_transfer_learning": (
        f'{HERO_STYLE} Title: "Transfer Learning". '
        "LEFT: large frozen ResNet backbone block (gray, padlock icon) labeled ImageNet pretrained. "
        "RIGHT: small green trainable head labeled Your 2 classes with arrow from backbone. "
        "Show freeze + fine-tune concept."
    ),
    "unit16_deep_learning_capstone": (
        f'{HERO_STYLE} Title: "Deep Learning Capstone". '
        "LEFT: image augmentation examples — original cat photo + rotated/flipped versions. "
        "RIGHT: train vs validation accuracy curves over epochs, "
        "with early stopping marker where val diverges."
    ),
    "unit17_nlp_preprocessing_tfidf": (
        f'{HERO_STYLE} Title: "NLP Preprocessing & TF-IDF". '
        "LEFT: raw sentence 'The cat sat on the mat' with tokens highlighted. "
        "RIGHT: sparse TF-IDF matrix grid with high values for cat/sat highlighted. "
        "Show text → numeric features."
    ),
    "unit18_word_embeddings_word2vec": (
        f'{HERO_STYLE} Title: "Word2Vec Embeddings". '
        "LEFT: one-hot vector (long sparse bar) labeled king. "
        "RIGHT: 2D embedding space with king, queen, man, woman positioned so "
        'king - man + woman ≈ queen shown with arrows. '
        "Dense vs sparse comparison."
    ),
    "unit19_rnns_lstms": (
        f'{HERO_STYLE} Title: "RNNs & LSTMs". '
        "LEFT: unrolled RNN — cells h0, h1, h2, h3 connected sequentially with x inputs. "
        "RIGHT: LSTM cell diagram with Forget, Input, Output gates labeled. "
        "Sequential memory concept."
    ),
    "unit20_attention_transformers": (
        f'{HERO_STYLE} Title: "Attention & Transformers". '
        "LEFT: attention heatmap matrix (4×4) with brighter diagonal, "
        'labeled "Query × Key weights". '
        "RIGHT: Transformer block: Multi-Head Attention → Add&Norm → FFN → Add&Norm."
    ),
    "unit21_nlp_capstone": (
        f'{HERO_STYLE} Title: "NLP Capstone". '
        "Full NLP project overview: text documents → preprocessing → "
        "TF-IDF or Embeddings → classifier → precision/recall metrics report. "
        "End-to-end pipeline with icons for each stage."
    ),
    "unit22_llm_evolution": (
        f'{HERO_STYLE} Title: "LLM → AI Agent Evolution". '
        "Three stages left to right with arrows: "
        "(1) LLM text completion chat bubble, "
        "(2) RAG with document retrieval, "
        "(3) AI Agent with tools (search, calculator, code). "
        "Evolution timeline style."
    ),
    "unit23_llm_api": (
        f'{HERO_STYLE} Title: "LLM API & Prompting". '
        "LEFT: HTTP request JSON with system/user messages going to OpenAI API cloud. "
        "RIGHT: three prompt pattern cards: Zero-shot, Few-shot (with examples), "
        "Chain-of-Thought."
    ),
    "unit24_vector_dbs_rag_from_scratch": (
        f'{HERO_STYLE} Title: "Vector DBs & RAG from Scratch". '
        "Pipeline: Documents → Chunk → Embed (vector) → Store in Vector DB → "
        "Query → Top-k retrieve → LLM generates grounded answer. "
        "Show cosine similarity search with nearest vectors highlighted."
    ),
    "unit25_langchain_basics_rag": (
        f'{HERO_STYLE} Title: "LangChain RAG". '
        "LangChain chain diagram: Document Loader → Text Splitter → Embeddings → "
        "Vector Store → Retriever → LLM Chain → Answer. "
        "Composable blocks with LangChain-style labels."
    ),
    "unit26_llamaindex_basics_rag": (
        f'{HERO_STYLE} Title: "LlamaIndex RAG". '
        "LEFT: documents feeding into Index builder. "
        "RIGHT: Query Engine — natural language question → retrieved chunks → answer. "
        "Data-centric indexing concept."
    ),
    "unit27_prompt_chaining": (
        f'{HERO_STYLE} Title: "Prompt Chaining". '
        "Two-step chain: Prompt A (Extract facts) → output box → "
        "Prompt B (Reason & answer) → final result. "
        "Show data flowing between prompt steps with arrows."
    ),
    "unit28_context_aware_chatbot": (
        f'{HERO_STYLE} Title: "Context-Aware Chatbot". '
        "Chat UI mockup: message history (user/bot bubbles) stored in session memory, "
        "new message sent with full history to API. "
        "Show conversation context being preserved."
    ),
    "unit29_ai_agent_implementation": (
        f'{HERO_STYLE} Title: "ReAct AI Agent". '
        "ReAct loop diagram: Thought → Action (tool call) → Observation → "
        "repeat until Done. "
        "Show example: Thought: search web, Action: search(), Observation: results."
    ),
    "unit30_mcp_fundamentals": (
        f'{HERO_STYLE} Title: "Model Context Protocol (MCP)". '
        "Architecture: MCP Client (host app like IDE) ↔ MCP Server (tools + resources). "
        "Show tool discovery and function calls via protocol."
    ),
    "unit31_smolagents_code_agent": (
        f'{HERO_STYLE} Title: "smolagents Code Agent". '
        "Loop: User task → LLM writes Python code → Sandbox executes → "
        "Result returned. "
        "Show code block and execution output."
    ),
    "unit32_langgraph_stateful_agents": (
        f'{HERO_STYLE} Title: "LangGraph: Stateful Agents". '
        "LEFT panel (blue border): support ticket routing graph — "
        'root node "Classify Ticket" with three branches to '
        '"Billing", "Technical", "Escalate" boxes connected by arrows. '
        'Shared state box labeled "State (TypedDict)" at bottom. '
        "RIGHT panel (purple border): Human-in-the-loop gate — "
        '"VIP ticket" pauses at "Human Approval" node before routing. '
        "Show nodes, conditional edges, and state passing between steps. "
        "Caption: Graph workflow vs linear ReAct loop."
    ),
    "unit33_agent_sdk_general_agents": (
        f'{HERO_STYLE} Title: "Agent SDK: General Agents". '
        "Business task card → SDK Agent orchestrator → multiple tools "
        "(report, data, email) → completed deliverable. "
        "Enterprise agent workflow."
    ),
    "unit34_agent_sdk_coding_agents": (
        f'{HERO_STYLE} Title: "Agent SDK: Coding Agents". '
        "Repo files + tests → coding agent reads → proposes code edit diff → "
        "runs tests → pass/fail. "
        "Software development agent loop."
    ),
    "unit35_llm_harness_capstone": (
        f'{HERO_STYLE} Title: "LLM Harness Capstone". '
        "Dual pipeline: Generation (LLM output) → Evaluation Harness "
        "(policy check + LLM judge score) → pass/reject/fallback. "
        "Quality and safety layers."
    ),
    "unit36_multimodal_fraud_detection": (
        f'{HERO_STYLE} Title: "Multimodal Fraud Detection". '
        "Text description + product image → separate encoders → late fusion → "
        "fraud score 0.87 (HIGH RISK). "
        "Show suspicious text/image mismatch."
    ),
    "unit37_knowledge_structuring_agent": (
        f'{HERO_STYLE} Title: "Knowledge Structuring Agent". '
        "PDF contract document → AI extraction agent → structured JSON "
        "with entities and relations. "
        "Unstructured to structured transformation."
    ),
    "unit38_guardrails_evaluation_harness": (
        f'{HERO_STYLE} Title: "Guardrails & Evaluation". '
        "LEFT: input guardrail blocking harmful content. "
        "RIGHT: evaluation harness with test cases, LLM judge scores, "
        "regression dashboard."
    ),
    "unit39_timeseries_price_optimizer": (
        f'{HERO_STYLE} Title: "Time Series & Dynamic Pricing". '
        "LEFT: historical demand line chart over months. "
        "RIGHT: price vs revenue curve with optimal price point marked. "
        "Forecast + pricing optimization."
    ),
    "unit40_multiagent_customer_support": (
        f'{HERO_STYLE} Title: "Multi-Agent Customer Support". '
        "Incoming ticket → Triage agent routes to specialist agents "
        "(Billing, Tech, Sales) → resolved response. "
        "Multi-agent coordination diagram."
    ),
}
