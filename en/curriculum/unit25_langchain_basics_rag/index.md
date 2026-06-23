# Unit 25: LangChain Basics and RAG

> [!IMPORTANT]
> **Prerequisites and library installation**
> This unit requires `langchain` and `langchain-openai`.
> Install on your environment:
> ```bash
> pip install langchain langchain-openai
> ```

---

## 1. Understanding LangChain Basics and RAG

In Unit 24 you **hand-built RAG from scratch**—calling APIs directly, splitting documents, vectorizing, computing cosine similarity—deeply understanding retrieval + generation.

In production, hand-building everything is heavy. Switching models (OpenAI to Anthropic/Claude), organizing prompts, and chaining reasoning steps quickly turns code into spaghetti.

**LangChain** is the de facto LLM application framework—common components and powerful wiring.

### What is LangChain?

LangChain provides reusable parts and mechanisms to build LLM apps efficiently.

#### 💡 Everyday analogy: system kitchen and standard parts
Hand-building is cutting wood and tightening screws for custom shelves and sinks. LangChain is **combining pre-standardized system-kitchen parts (stove, cabinets, dishwasher)**. Swap OpenAI for Claude like swapping gas for induction—same interface.

### LangChain’s four major components

| Component | Role | Example class |
| :--- | :--- | :--- |
| **Models** | Gateway to LLMs; common interface across vendors. | `ChatOpenAI` |
| **Prompts** | Template prompts and variable injection. | `ChatPromptTemplate` |
| **OutputParsers** | Parse LLM text (JSON, CSV, etc.) into program-friendly forms. | `StrOutputParser` |
| **Chains (LCEL)** | Wire parts into one pipeline. | `prompt | model | parser` |

### LCEL (LangChain Expression Language)

LangChain uses **LCEL** with Python’s pipe operator **`|`** to define left-to-right data flow.

```python
# シンプルなLCELチェーンの例
chain = prompt | model | output_parser
```

Data flows through `prompt` (variables filled), `model` (LLM), `output_parser` (text extracted)—what took 10+ lines hand-built becomes one elegant line.

### 💡 Concrete business use cases

- **Cross-document internal search**: Unify PDFs and wiki with LangChain Retriever for QA aligned with latest policies.
- **Multi-vendor chat**: Seamlessly switch OpenAI and Anthropic by data sensitivity and cost.
- **Data analysis pipeline**: Flow CSV/SQL results through prompt templates; LCEL chains produce analysis and chart JSON automatically.

---

## 2. Implementation Example

Build a **simple in-memory vector store RAG** with LangChain LCEL.
Notice how much simpler cosine similarity and wiring become versus scratch.

> ※ Requires `OPENAI_API_KEY` in environment variables.

```python
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore

# 1. 簡易的な社内ドキュメント（知識ソース）の用意
documents = [
    "株式会社テックアカデミーの夏季休暇は、8月13日から8月16日までの4日間です。",
    "福利厚生として、年間最大5万円の書籍購入補助（テックブックサポート）が利用可能です。",
    "経費精算は、毎月25日までにシステム「マネーフォワード」経由で申請する必要があります。"
]

# 2. Embedding（ベクトル化モデル）とベクターストアの準備
# LangChainが提供する軽量なインメモリベクターストアを使用します
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = InMemoryVectorStore.from_texts(documents, embedding=embeddings)

# 3. Retriever（検索機）の作成
# これにより、ユーザーの質問に関連する文書を自動でトップK件探してくる「窓口」ができます
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

# 4. LLMモデルとプロンプトテンプレートの準備
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

# context（検索された文書）と question（ユーザーの質問）を受け取るテンプレート
prompt = ChatPromptTemplate.from_template(
    """以下の参考情報を元に、ユーザーの質問に正確に答えてください。
情報が見つからない場合は「申し訳ありませんが、その情報は見つかりませんでした」と答えてください。

【参考情報】
{context}

【質問】
{question}
"""
)

# 5. LCELによる RAG パイプライン（チェーン）の構築
# RunnablePassthrough は、入力された質問をそのまま下流のプロンプトに流すための仕組みです
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# 6. 実行
if __name__ == "__main__":
    # テスト質問 1
    query_1 = "お盆休みはいつからいつまでですか？"
    response_1 = rag_chain.invoke(query_1)
    print(f"質問: {query_1}")
    print(f"回答: {response_1}\n")

    # テスト質問 2
    query_2 = "本を買うための補助制度はありますか？"
    response_2 = rag_chain.invoke(query_2)
    print(f"質問: {query_2}")
    print(f"回答: {response_2}\n")

    # テスト質問 3
    query_3 = "会社の給料日はいつですか？"
    response_3 = rag_chain.invoke(query_3)
    print(f"質問: {query_3}")
    print(f"回答: {response_3}\n")
```

**🔍 Detailed code walkthrough**
1. **InMemoryVectorStore**: Your scratch “vector database.” Embeds documents with `OpenAIEmbeddings` and stores in memory.
2. **Retriever**: `as_retriever` returns an object that searches top-K relevant docs—cosine similarity and sorting hidden inside.
3. **LCEL data flow**:
   - `{"context": retriever, "question": RunnablePassthrough()}`
     Question splits: one path to `retriever` for `context`, one passthrough as `question`.
   - `| prompt`
     Fills `{context}` and `{question}` in the template.
   - `| model`
     Sends completed prompt to GPT-4o-mini.
   - `| StrOutputParser()`
     Extracts answer text from the response object.

---

## 3. Practice

Build an internal **security policy consultation assistant** with LangChain RAG.

**【Requirements】**
- Store the “security policy data” below in a vector store.
- Build an LCEL chain that retrieves relevant policies and answers user questions.
- Function name: `create_security_qa_chain()`
  - Return the constructed `rag_chain` object.

**【Security policy data】**
```python
security_policies = [
    "社内PCのパスワードは、英大文字・小文字・数字・記号を組み合わせた12文字以上とし、90日ごとに変更しなければならない。",
    "顧客の個人情報や機密ファイルを外部に送信する際は、必ず会社の指定する共有リンクにパスワードと有効期限（最大7日間）を設定すること。",
    "業務時間外に社外で仕事をする場合は、必ず前日までに「リモートワーク申請」を上長に提出し、承認を得る必要がある。"
]
```

**💡 Hint**
- Like the example, use `InMemoryVectorStore.from_texts` for the vector database.
- In the prompt template, instruct strict adherence to security policy; for unlisted rules answer “セキュリティ規約に該当する記載がありません”.

---

## 4. Answer Key

<details>
<summary>View sample solution (click to expand)</summary>

```python
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore

def create_security_qa_chain():
    # 1. セキュリティ規約データの用意
    security_policies = [
        "社内PCのパスワードは、英大文字・小文字・数字・記号を組み合わせた12文字以上とし、90日ごとに変更しなければならない。",
        "顧客の個人情報や機密ファイルを外部に送信する際は、必ず会社の指定する共有リンクにパスワードと有効期限（最大7日間）を設定すること。",
        "業務時間外に社外で仕事をする場合は、必ず前日までに「リモートワーク申請」を上長に提出し、承認を得る必要がある。"
    ]
    
    # 2. Embeddingモデルとベクターストアの初期化
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = InMemoryVectorStore.from_texts(security_policies, embedding=embeddings)
    
    # 3. Retriever（検索機）の設定
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
    
    # 4. LLMモデルの設定（実務用途なのでランダム性を排除するため temperature=0.0）
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    
    # 5. セキュリティ相談専用のプロンプト
    prompt = ChatPromptTemplate.from_template(
        """あなたは社内の情報セキュリティに関する質問に答える専門アシスタントです。
以下のセキュリティ規約情報を元に、ユーザーの相談に正確に答えてください。
規約に明示的に記載されていない事柄については、勝手に推測して答えず、「セキュリティ規約に該当する記載がありません」と厳格に答えてください。

【セキュリティ規約情報】
{context}

【質問】
{question}
"""
)
    
    # 6. LCELによるチェーンの構築
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    
    return rag_chain

# テスト実行
if __name__ == "__main__":
    qa_chain = create_security_qa_chain()
    
    # テスト 1: 規約に記載のある質問
    q1 = "パスワードは何日ごとに変更すればいいですか？"
    print(f"質問: {q1}")
    print(f"回答: {qa_chain.invoke(q1)}\n")
    
    # テスト 2: 規約に記載のある質問
    q2 = "社外に顧客データを送る場合の共有リンクの期限は？"
    print(f"質問: {q2}")
    print(f"回答: {qa_chain.invoke(q2)}\n")
    
    # テスト 3: 規約に記載のない質問
    q3 = "オフィスの入退館カードを紛失した場合はどうすればいいですか？"
    print(f"質問: {q3}")
    print(f"回答: {qa_chain.invoke(q3)}\n")
```
</details>
