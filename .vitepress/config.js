import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(
  defineConfig({
  base: "/",
  srcExclude: [
    '**/aidlc-docs/**',
    '**/node_modules/**',
    '**/.agent/**',
    'README.md'
  ],
  vite: {
    optimizeDeps: {
      include: ['mermaid', 'dayjs']
    }
  },
  locales: {
    root: {
      label: '日本語',
      lang: 'ja-JP',
      link: '/',
      title: "Build to Learn: AI",
      description: "機械学習の基礎からLLM・AIエージェントまでを体系的に学ぶ即戦力カリキュラム",
      themeConfig: {
        selectText: '言語',
        label: '日本語',
        nav: [
          { text: 'ホーム', link: '/' },
          { text: 'カリキュラム', link: '/curriculum/unit00_roadmap/' },
          { text: '学習環境とAPI準備 (Appendix)', link: '/curriculum/appendix/' }
        ],
        sidebar: [
          {
            text: 'イントロダクション',
            items: [
              { text: '全体のロードマップ', link: '/curriculum/unit00_roadmap/' },
              { text: '学習環境とAPI準備 (Appendix)', link: '/curriculum/appendix/' }
            ]
          },
          {
            text: '第1章: 機械学習の基礎と主要アルゴリズム',
            items: [
              { text: 'Unit 1: 線形回帰と正則化回帰', link: '/curriculum/unit01_linear_regression/' },
              { text: 'Unit 2: ロジスティック回帰と分類評価指標', link: '/curriculum/unit02_logistic_regression/' },
              { text: 'Unit 3: K-NN とサポートベクターマシン', link: '/curriculum/unit03_knn_svm/' },
              { text: 'Unit 4: 決定木とランダムフォレスト', link: '/curriculum/unit04_decision_trees_random_forests/' },
              { text: 'Unit 5: 勾配ブースティングと XGBoost', link: '/curriculum/unit05_gradient_boosting_xgboost/' },
              { text: 'Unit 6: クラスタリングアルゴリズム', link: '/curriculum/unit06_clustering_algorithms/' },
              { text: 'Unit 7: 次元削減と主成分分析', link: '/curriculum/unit07_dimensionality_reduction/' },
              { text: 'Unit 8: 交差検証とハイパーパラメータ調整', link: '/curriculum/unit08_cross_validation_tuning/' },
              { text: 'Unit 9: 機械学習総合演習 (Capstone)', link: '/curriculum/unit09_classical_ml_capstone/' }
            ]
          },
          {
            text: '第2章: ディープラーニング基礎',
            items: [
              { text: 'Unit 10: ゼロから作るニューラルネットワーク', link: '/curriculum/unit10_nn_from_scratch/' },
              { text: 'Unit 11: PyTorch の基礎とシンプルな多層パーセプトロン', link: '/curriculum/unit11_pytorch_basics/' },
              { text: 'Unit 12: 最適化手法と損失関数', link: '/curriculum/unit12_optimizers_loss/' },
              { text: 'Unit 13: ディープラーニングにおける過学習防止策', link: '/curriculum/unit13_regularization/' },
              { text: 'Unit 14: 畳み込みニューラルネットワークの基礎', link: '/curriculum/unit14_cnn_basics/' },
              { text: 'Unit 15: ResNet を用いた転移学習', link: '/curriculum/unit15_transfer_learning/' },
              { text: 'Unit 16: ディープラーニング総合演習 (Capstone)', link: '/curriculum/unit16_deep_learning_capstone/' }
            ]
          },
          {
            text: '第3章: 自然言語処理とモダンアーキテクチャ',
            items: [
              { text: 'Unit 17: 自然言語前処理と TF-IDF', link: '/curriculum/unit17_nlp_preprocessing_tfidf/' },
              { text: 'Unit 18: 単語の分散表現 (Word2Vec)', link: '/curriculum/unit18_word_embeddings_word2vec/' },
              { text: 'Unit 19: リカレントニューラルネットワークと LSTM', link: '/curriculum/unit19_rnns_lstms/' },
              { text: 'Unit 20: 注意機構と Transformer', link: '/curriculum/unit20_attention_transformers/' },
              { text: 'Unit 21: 自然言語処理総合演習 (Capstone)', link: '/curriculum/unit21_nlp_capstone/' }
            ]
          },
          {
            text: '第4章: LLM応用とAIエージェント',
            items: [
              { text: 'Unit 22: LLMからAIエージェントへの進化', link: '/curriculum/unit22_llm_evolution/' },
              { text: 'Unit 23: LLM API の利用とプロンプトエンジニアリング', link: '/curriculum/unit23_llm_api/' },
              { text: 'Unit 24: ベクトルデータベースとスクラッチ RAG', link: '/curriculum/unit24_vector_dbs_rag_from_scratch/' },
              { text: 'Unit 25: LangChainの基礎とRAG', link: '/curriculum/unit25_langchain_basics_rag/' },
              { text: 'Unit 26: LlamaIndex の基礎と検索拡張生成', link: '/curriculum/unit26_llamaindex_basics_rag/' },
              { text: 'Unit 27: プロンプトの連鎖による段階的推論', link: '/curriculum/unit27_prompt_chaining/' },
              { text: 'Unit 28: 文脈を記憶するチャットボット', link: '/curriculum/unit28_context_aware_chatbot/' },
              { text: 'Unit 29: AIエージェントの基本原理とスクラッチReAct実装', link: '/curriculum/unit29_ai_agent_implementation/' },
              { text: 'Unit 30: Model Context Protocol (MCP) の基本原理とサーバー自作', link: '/curriculum/unit30_mcp_fundamentals/' },
              { text: 'Unit 31: smolagents と自律型 AI エージェント', link: '/curriculum/unit31_smolagents_code_agent/' },
              { text: 'Unit 32: Agent SDK: 汎用・業務自動化', link: '/curriculum/unit32_agent_sdk_general_agents/' },
              { text: 'Unit 33: Agent SDK: コーディング・自律開発', link: '/curriculum/unit33_agent_sdk_coding_agents/' }
            ]
          },
          {
            text: '第5章: 実務適用と総合応用実践 (Capstones)',
            items: [
              { text: 'Unit 34: LLM自動評価・防御とエージェント総合演習 (Capstone)', link: '/curriculum/unit34_llm_harness_capstone/' },
              { text: 'Unit 35: マルチモーダル不正検知システム', link: '/curriculum/unit35_multimodal_fraud_detection/' },
              { text: 'Unit 36: 自律型ナレッジ抽出・構造化エージェント', link: '/curriculum/unit36_knowledge_structuring_agent/' },
              { text: 'Unit 37: エンタープライズAI自動評価・防御ハーネス', link: '/curriculum/unit37_guardrails_evaluation_harness/' },
              { text: 'Unit 38: 時系列需要予測・価格最適化システム', link: '/curriculum/unit38_timeseries_price_optimizer/' },
              { text: 'Unit 39: 自律型カスタマーサポート・マルチエージェント', link: '/curriculum/unit39_multiagent_customer_support/' }
            ]
          }
        ]
      }
    },
    en: {
      label: 'English',
      lang: 'en-US',
      link: '/en/',
      title: "Build to Learn: AI",
      description: "A systematic curriculum from machine learning fundamentals to LLMs and AI Agents.",
      themeConfig: {
        selectText: 'Languages',
        label: 'English',
        nav: [
          { text: 'Home', link: '/en/' },
          { text: 'Curriculum', link: '/en/curriculum/unit00_roadmap/' },
          { text: 'Appendix', link: '/en/curriculum/appendix/' }
        ],
        sidebar: [
          {
            text: 'Introduction',
            items: [
              { text: 'Overall Roadmap', link: '/en/curriculum/unit00_roadmap/' },
              { text: 'Environment Setup (Appendix)', link: '/en/curriculum/appendix/' }
            ]
          },
          {
            text: 'Chapter 1: Machine Learning Fundamentals',
            items: [
              { text: 'Unit 1: Linear & Regularized Regression', link: '/en/curriculum/unit01_linear_regression/' },
              { text: 'Unit 2: Logistic Regression & Metrics', link: '/en/curriculum/unit02_logistic_regression/' },
              { text: 'Unit 3: K-NN & Support Vector Machines', link: '/en/curriculum/unit03_knn_svm/' },
              { text: 'Unit 4: Decision Trees & Random Forests', link: '/en/curriculum/unit04_decision_trees_random_forests/' },
              { text: 'Unit 5: Gradient Boosting & XGBoost', link: '/en/curriculum/unit05_gradient_boosting_xgboost/' },
              { text: 'Unit 6: Clustering Algorithms', link: '/en/curriculum/unit06_clustering_algorithms/' },
              { text: 'Unit 7: Dimensionality Reduction', link: '/en/curriculum/unit07_dimensionality_reduction/' },
              { text: 'Unit 8: Cross Validation & Tuning', link: '/en/curriculum/unit08_cross_validation_tuning/' },
              { text: 'Unit 9: Machine Learning Capstone', link: '/en/curriculum/unit09_classical_ml_capstone/' }
            ]
          },
          {
            text: 'Chapter 2: Deep Learning Fundamentals',
            items: [
              { text: 'Unit 10: NN from Scratch', link: '/en/curriculum/unit10_nn_from_scratch/' },
              { text: 'Unit 11: PyTorch Basics & Simple MLP', link: '/en/curriculum/unit11_pytorch_basics/' },
              { text: 'Unit 12: Optimizers & Loss Functions', link: '/en/curriculum/unit12_optimizers_loss/' },
              { text: 'Unit 13: Regularization in DL', link: '/en/curriculum/unit13_regularization/' },
              { text: 'Unit 14: CNN Basics', link: '/en/curriculum/unit14_cnn_basics/' },
              { text: 'Unit 15: Transfer Learning with ResNet', link: '/en/curriculum/unit15_transfer_learning/' },
              { text: 'Unit 16: Deep Learning Capstone', link: '/en/curriculum/unit16_deep_learning_capstone/' }
            ]
          },
          {
            text: 'Chapter 3: NLP & Modern Architectures',
            items: [
              { text: 'Unit 17: NLP Preprocessing & TF-IDF', link: '/en/curriculum/unit17_nlp_preprocessing_tfidf/' },
              { text: 'Unit 18: Word Embeddings (Word2Vec)', link: '/en/curriculum/unit18_word_embeddings_word2vec/' },
              { text: 'Unit 19: RNNs & LSTMs', link: '/en/curriculum/unit19_rnns_lstms/' },
              { text: 'Unit 20: Attention & Transformers', link: '/en/curriculum/unit20_attention_transformers/' },
              { text: 'Unit 21: NLP Capstone', link: '/en/curriculum/unit21_nlp_capstone/' }
            ]
          },
          {
            text: 'Chapter 4: LLM Applied & AI Agents',
            items: [
              { text: 'Unit 22: Evolution from LLM to AI Agent', link: '/en/curriculum/unit22_llm_evolution/' },
              { text: 'Unit 23: LLM API Usage & Prompting', link: '/en/curriculum/unit23_llm_api/' },
              { text: 'Unit 24: Vector DBs & RAG From Scratch', link: '/en/curriculum/unit24_vector_dbs_rag_from_scratch/' },
              { text: 'Unit 25: LangChain Basics & RAG', link: '/en/curriculum/unit25_langchain_basics_rag/' },
              { text: 'Unit 26: LlamaIndex Basics & RAG', link: '/en/curriculum/unit26_llamaindex_basics_rag/' },
              { text: 'Unit 27: Prompt Chaining', link: '/en/curriculum/unit27_prompt_chaining/' },
              { text: 'Unit 28: Context-Aware Chatbot', link: '/en/curriculum/unit28_context_aware_chatbot/' },
              { text: 'Unit 29: AI Agent Fundamentals & Scratch ReAct Implementation', link: '/en/curriculum/unit29_ai_agent_implementation/' },
              { text: 'Unit 30: Model Context Protocol (MCP) Fundamentals & Server Implementation', link: '/en/curriculum/unit30_mcp_fundamentals/' },
              { text: 'Unit 31: smolagents & AI Agent', link: '/en/curriculum/unit31_smolagents_code_agent/' },
              { text: 'Unit 32: Agent SDK: General & Business Automation', link: '/en/curriculum/unit32_agent_sdk_general_agents/' },
              { text: 'Unit 33: Agent SDK: Autonomous Coding & Software Engineering', link: '/en/curriculum/unit33_agent_sdk_coding_agents/' }
            ]
          },
          {
            text: 'Chapter 5: Real-World AI Application Capstones',
            items: [
              { text: 'Unit 34: LLM Harness & Agent Capstone', link: '/en/curriculum/unit34_llm_harness_capstone/' },
              { text: 'Unit 35: Multimodal Fraud Detection', link: '/en/curriculum/unit35_multimodal_fraud_detection/' },
              { text: 'Unit 36: Autonomous Knowledge Structuring', link: '/en/curriculum/unit36_knowledge_structuring_agent/' },
              { text: 'Unit 37: Guardrails & LLM-as-a-Judge', link: '/en/curriculum/unit37_guardrails_evaluation_harness/' },
              { text: 'Unit 38: TimeSeries & Dynamic Pricing', link: '/en/curriculum/unit38_timeseries_price_optimizer/' },
              { text: 'Unit 39: Multi-Agent Customer Support', link: '/en/curriculum/unit39_multiagent_customer_support/' }
            ]
          }
        ]
      }
    }
  },
  themeConfig: {
    socialLinks: [
      { icon: 'github', link: 'https://github.com/' }
    ]
  }
}))
