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
# Simple LCEL chain example
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

# 1. Prepare simple internal documents (knowledge source)
documents = [
    "Tech Academy Inc. summer break runs from August 13 through August 16 (4 days).",
    "As a benefit, employees may receive up to 50,000 yen per year in book purchase support (Tech Book Support).",
    "Expense reports must be submitted through Money Forward by the 25th of each month."
]

# 2. Prepare embedding model and vector store
# Uses LangChain's lightweight in-memory vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = InMemoryVectorStore.from_texts(documents, embedding=embeddings)

# 3. Create retriever
# Automatically finds top-K documents related to the user's question
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

# 4. Prepare LLM model and prompt template
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

# Template receives context (retrieved documents) and question (user query)
prompt = ChatPromptTemplate.from_template(
    """Answer the user's question accurately based on the reference information below.
If the information is not found, respond with "Sorry, I could not find that information."

[Reference Information]
{context}

[Question]
{question}
"""
)

# 5. Build RAG pipeline (chain) with LCEL
# RunnablePassthrough passes the input question downstream unchanged
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# 6. Run
if __name__ == "__main__":
    # Test question 1
    query_1 = "When does Obon holiday start and end?"
    response_1 = rag_chain.invoke(query_1)
    print(f"Question: {query_1}")
    print(f"Answer: {response_1}\n")

    # Test question 2
    query_2 = "Is there a subsidy program for buying books?"
    response_2 = rag_chain.invoke(query_2)
    print(f"Question: {query_2}")
    print(f"Answer: {response_2}\n")

    # Test question 3
    query_3 = "When is the company payday?"
    response_3 = rag_chain.invoke(query_3)
    print(f"Question: {query_3}")
    print(f"Answer: {response_3}\n")
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
    "Internal PC passwords must be at least 12 characters combining uppercase, lowercase, digits, and symbols, and must be changed every 90 days.",
    "When sending customer personal information or confidential files externally, always use company-approved shared links with a password and expiration (maximum 7 days).",
    "When working outside the office after business hours, you must submit a Remote Work Request to your manager by the previous day and obtain approval."
]
```

**💡 Hint**
- Like the example, use `InMemoryVectorStore.from_texts` for the vector database.
- In the prompt template, instruct strict adherence to security policy; for unlisted rules answer “No matching entry found in the security policy”.

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
    # 1. Prepare security policy data
    security_policies = [
        "Internal PC passwords must be at least 12 characters combining uppercase, lowercase, digits, and symbols, and must be changed every 90 days.",
        "When sending customer personal information or confidential files externally, always use company-approved shared links with a password and expiration (maximum 7 days).",
        "When working outside the office after business hours, you must submit a Remote Work Request to your manager by the previous day and obtain approval."
    ]
    
    # 2. Initialize embedding model and vector store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = InMemoryVectorStore.from_texts(security_policies, embedding=embeddings)
    
    # 3. Configure retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
    
    # 4. Configure LLM (temperature=0.0 for production use to eliminate randomness)
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    
    # 5. Security consultation prompt
    prompt = ChatPromptTemplate.from_template(
        """You are a specialist assistant for internal information security questions.
Answer user inquiries accurately based on the security policy information below.
For matters not explicitly stated in the policy, do not guess; respond strictly with "No matching entry found in the security policy."

[Security Policy Information]
{context}

[Question]
{question}
"""
)
    
    # 6. Build chain with LCEL
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    
    return rag_chain

# Test run
if __name__ == "__main__":
    qa_chain = create_security_qa_chain()
    
    # Test 1: question covered by policy
    q1 = "How often must I change my password?"
    print(f"Question: {q1}")
    print(f"Answer: {qa_chain.invoke(q1)}\n")
    
    # Test 2: question covered by policy
    q2 = "What is the expiration for shared links when sending customer data externally?"
    print(f"Question: {q2}")
    print(f"Answer: {qa_chain.invoke(q2)}\n")
    
    # Test 3: question not covered by policy
    q3 = "What should I do if I lose my office access card?"
    print(f"Question: {q3}")
    print(f"Answer: {qa_chain.invoke(q3)}\n")
```
</details>
