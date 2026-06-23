# Unit 0: Overall Roadmap and Guidelines

Welcome! This repository is a comprehensive curriculum designed to take you from the fundamentals of machine learning through to building the latest LLMs and AI agents.

This curriculum is structured as a collection of micro-PoCs (proof-of-concept projects), each designed to be completed in a few hours. By coding a little every day, you will steadily build genuine skills and confidence as an AI engineer.

---

## 💡 Why Learn Machine Learning and Deep Learning in the LLM Era?

LLMs (large language models) and autonomous agents—exemplified by ChatGPT—are at the center of AI today. However, to call yourself a top-tier **AI engineer or system architect** in practice, you need more than LLMs alone: foundational knowledge of machine learning (ML) and deep learning (DL) is essential.

The main reason is that **ML, DL, and LLMs each have different technical characteristics (data types, inference speed, cost, explainability), and the problems they fit best are fundamentally different in real-world systems.**

---

### 📊 ML, DL, and LLM: Technical Comparison Matrix

When embedding AI into production systems, architects weigh the following trade-offs when choosing a technology.

| Evaluation Axis | Machine Learning (ML) | Deep Learning (DL) | Large Language Model (LLM) |
| :--- | :--- | :--- | :--- |
| **Best-fit data** | **Structured data** (numeric values, categories, sales history in customer databases, etc.) | **Unstructured data** (images, audio, waveforms, video, etc.) | **Natural language (text)**, program code, complex dialogue |
| **Inference speed** | **Extremely fast** (milliseconds to tens of milliseconds) | **Fast** (tens to hundreds of milliseconds; GPU required) | **Slow** (seconds to tens of seconds; API latency) |
| **Compute cost (infra)** | **Very low** (runs on CPU; pennies to dollars scale) | **Moderate** (edge devices or affordable GPUs) | **Very high** (pay-per-use API or multi-million-dollar dedicated GPUs) |
| **Explainability** | **Strongest** (decision process can be traced mathematically) | **Low** (multi-layer nets become black boxes) | **Very low** (hallucinations; logical grounding not guaranteed) |
| **Adoption difficulty** | **Moderate** (careful preprocessing and feature engineering by humans) | **High** (powerful automatic feature learning, but needs large datasets and expertise) | **Very low with APIs** (pretrained models run immediately with prompts) |

---

### 🎯 Right Tool for the Right Job (Fit Map)

As a system architect in practice, here is how to choose the right technology for each problem domain.

#### 1. Where Machine Learning (ML) Fits (Chapter 1)
* **Representative use cases**: Customer churn prediction, sales and inventory demand forecasting, real-estate price estimation, time-series dynamic pricing.
* **Why choose ML**: For numeric and categorical data in enterprise databases, ML (e.g., XGBoost) remains the **most accurate, fastest, and most explainable (business-justifiable) option** for tabular prediction.
* **⚠️ Anti-pattern—solving with an LLM**:
  Passing a customer's purchase history as text to an LLM and asking "Will this person churn next month?" is among the worst choices. Inference takes seconds, API token costs balloon, numeric stability is poor, and accuracy is far below ML.

#### 2. Where Deep Learning (DL) Fits (Chapters 2–3, first half)
* **Representative use cases**: Defect detection on factory production lines (image recognition), cancer detection in medical imaging, voice-command recognition, anomaly detection in machine vibration waveforms.
* **Why choose DL**: For unstructured data such as images and waveforms, humans cannot hand-engineer features as formulas. DL (e.g., CNNs) automatically extracts features like edges and shapes from data and excels at image and audio tasks.
* **⚠️ Anti-pattern—solving with an LLM**:
  Sending images from a conveyor belt to a multimodal LLM API and asking "Is there a defect?" introduces seconds of latency per call, so it cannot keep up with lines running dozens of items per second. API costs would destroy the business model. The right answer is a lightweight custom DL model (CNN) running on the edge in milliseconds.

#### 3. Where LLMs and Agents Fit (Chapters 4–5)
* **Representative use cases**: Extracting specific clauses from contracts and structuring them as JSON, automating customer-support dialogue, generating source code from specifications, autonomous tool execution and workflow automation.
* **Why choose LLMs**: For abstract, high-level tasks that resist rule-based automation—understanding natural-language context, generating code, and multi-step business reasoning—LLMs and autonomous agents are the best fit.

---

### 💡 Conclusion: Why We Start with Machine Learning (ML)

Modern AI systems are not built from LLMs alone. In practice, **hybrid designs are the norm**: lightweight ML or DL models process data quickly in the background, and LLMs consume those results to interact with humans.

1. **Right tool for the right job**: Learn each technology's strengths and limits so you can avoid wasted infrastructure cost and response-time degradation (degradation) as an architect.
2. **Understanding model internals**: The heart of LLMs (Attention and Transformers) stands on the history of deep learning and NLP. Chapters 1–3 give you the foundation to reason about how modern LLMs and agents behave and to tune them seriously in production.

---

## 🗺️ Curriculum Structure

The curriculum is organized into five chapters: foundational and advanced units, plus real-world application capstones.

### Chapter 1: Machine Learning Fundamentals
Learn algorithms that predate deep learning and still dominate tabular data. Often called "classical," they are not outdated—they are among the most widely used and powerful techniques in real business settings.
- **Unit 1**: [Linear & Regularized Regression](../unit01_linear_regression/index.md)
- **Unit 2**: [Logistic Regression & Classification Metrics](../unit02_logistic_regression/index.md)
- **Unit 3**: [K-NN & Support Vector Machines](../unit03_knn_svm/index.md)
- **Unit 4**: [Decision Trees & Random Forests](../unit04_decision_trees_random_forests/index.md)
- **Unit 5**: [Gradient Boosting & XGBoost](../unit05_gradient_boosting_xgboost/index.md)
- **Unit 6**: [Clustering Algorithms](../unit06_clustering_algorithms/index.md)
- **Unit 7**: [Dimensionality Reduction & PCA](../unit07_dimensionality_reduction/index.md)
- **Unit 8**: [Cross Validation & Hyperparameter Tuning](../unit08_cross_validation_tuning/index.md)
- **Unit 9**: [Machine Learning Capstone](../unit09_classical_ml_capstone/index.md)

### Chapter 2: Deep Learning Fundamentals
Learn neural networks and PyTorch basics for unstructured data such as images.
- **Unit 10**: [Neural Networks from Scratch](../unit10_nn_from_scratch/index.md)
- **Unit 11**: [PyTorch Basics & Simple MLP](../unit11_pytorch_basics/index.md)
- **Unit 12**: [Optimizers & Loss Functions](../unit12_optimizers_loss/index.md)
- **Unit 13**: [Regularization in Deep Learning](../unit13_regularization/index.md)
- **Unit 14**: [CNN Basics](../unit14_cnn_basics/index.md)
- **Unit 15**: [Transfer Learning with ResNet](../unit15_transfer_learning/index.md)
- **Unit 16**: [Deep Learning Capstone](../unit16_deep_learning_capstone/index.md)

### Chapter 3: NLP & Modern Architectures
From text-processing fundamentals through to Transformers, the core of modern LLMs.
- **Unit 17**: [NLP Preprocessing & TF-IDF](../unit17_nlp_preprocessing_tfidf/index.md)
- **Unit 18**: [Word Embeddings (Word2Vec)](../unit18_word_embeddings_word2vec/index.md)
- **Unit 19**: [RNNs & LSTMs](../unit19_rnns_lstms/index.md)
- **Unit 20**: [Attention & Transformers](../unit20_attention_transformers/index.md)
- **Unit 21**: [NLP Capstone](../unit21_nlp_capstone/index.md)

### Chapter 4: LLM Applied & AI Agents
Use LLMs as components to build advanced reasoning pipelines and autonomous agents. The final part of this chapter also covers enterprise-grade commercial Agent SDKs.
- **Unit 22**: [Evolution from LLM to AI Agent](../unit22_llm_evolution/index.md)
- **Unit 23**: [LLM API Usage & Prompt Engineering](../unit23_llm_api/index.md)
- **Unit 24**: [Vector Databases & RAG From Scratch](../unit24_vector_dbs_rag_from_scratch/index.md)
- **Unit 25**: [LangChain Basics & RAG](../unit25_langchain_basics_rag/index.md)
- **Unit 26**: [LlamaIndex Basics & RAG](../unit26_llamaindex_basics_rag/index.md)
- **Unit 27**: [Prompt Chaining & Stepwise Reasoning](../unit27_prompt_chaining/index.md)
- **Unit 28**: [Context-Aware Chatbot](../unit28_context_aware_chatbot/index.md)
- **Unit 29**: [AI Agent Fundamentals & Scratch ReAct Implementation](../unit29_ai_agent_implementation/index.md)
- **Unit 30**: [Model Context Protocol (MCP) Fundamentals & Server Implementation](../unit30_mcp_fundamentals/index.md)
- **Unit 31**: [smolagents & Autonomous AI Agents](../unit31_smolagents_code_agent/index.md)
- **Unit 32**: [Agent SDK: General & Business Automation](../unit32_agent_sdk_general_agents/index.md)
- **Unit 33**: [Agent SDK: Autonomous Coding & Software Engineering](../unit33_agent_sdk_coding_agents/index.md)

### Chapter 5: Real-World AI Application Capstones
Apply everything you have learned—ML, DL, NLP, and LLMs—to high-difficulty problems common in real business settings. You will design architectures, implement, and evaluate from scratch. Every unit in this chapter is a comprehensive capstone.
- **Unit 34**: [LLM Evaluation, Guardrails & Agent Capstone](../unit34_llm_harness_capstone/index.md)
- **Unit 35**: [Multimodal Fraud Detection](../unit35_multimodal_fraud_detection/index.md)
- **Unit 36**: [Autonomous Knowledge Extraction & Structuring Agent](../unit36_knowledge_structuring_agent/index.md)
- **Unit 37**: [Enterprise AI Evaluation & Guardrails Harness](../unit37_guardrails_evaluation_harness/index.md)
- **Unit 38**: [Time-Series Demand Forecasting & Dynamic Pricing](../unit38_timeseries_price_optimizer/index.md)
- **Unit 39**: [Autonomous Multi-Agent Customer Support](../unit39_multiagent_customer_support/index.md)

---

## 📝 How to Learn

Each unit's `index.md` follows four steps. Open your environment (Jupyter Notebook, etc.), copy the code, run it, and learn by doing.

### 1. [Topic Name] (Conceptual Understanding)
First, understand the algorithm or technology: background, mathematical foundations, and trade-offs. Explanations use diagrams and concrete examples for beginners.

### 2. Implementation Example
A complete baseline implementation on the main dataset, with detailed commentary. Copy the code, run it, and experiment by changing parameters.

### 3. Practice (Assignment)
Using what you learned in step 2, implement a pipeline on a **different dataset** on your own. Thinking through and building this yourself is where real skill forms.

### 4. Answer Key
Solutions and explanations for the practice assignment. They are hidden inside `<details>` tags—try not to open them until you finish your own implementation. Compare your code with the reference and look for improvements.

---

Start by reviewing the [Appendix (Environment & API Setup)](../appendix/index.md) to prepare your workspace, then begin your journey from [Unit 1](../unit01_linear_regression/index.md)!
