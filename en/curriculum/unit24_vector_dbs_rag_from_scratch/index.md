# Unit 24: Vector Databases and RAG From Scratch

<p class="unit-hero">
  <img src="../../assets/units/unit24_vector_dbs_rag_from_scratch/images/hero.png" alt="Hero: Vector DBs & Scratch RAG" />
</p>

> [!IMPORTANT]
> **OpenAI API key setup**
> This unit uses the OpenAI API. See [Appendix (Learning Environment and API Setup)](../appendix/index.md#🔑-3-openai-api-key-acquisition-and-secure-management-chapter-4) for secure key configuration.


## 1. Understanding Vector DBs & RAG From Scratch

<img src="../../assets/units/unit24_vector_dbs_rag_from_scratch/images/diagram-concept.svg" alt="Diagram: RAG pipeline" class="unit-diagram" />



### What is a Vector DB?
To help AI understand language, words must become **numeric sequences (vectors)**—called **embeddings**.
A Vector DB stores these sequences and specializes in finding “semantically similar” items instantly.

**💡 Everyday analogy: bookstore shelving**
- **Traditional DB (keyword search)**: Books in alphabetical order. Search “apple” finds only books containing “apple,” not “Apple.”
- **Vector DB (semantic search)**: Books shelved by meaning. Search “apple” and books about “fruit” or “Apple” nearby are found even without exact text match.

### What is RAG (Retrieval-Augmented Generation)?
LLMs like ChatGPT only know training data— they cannot answer about latest news or your company’s confidential rules.
**“Search materials first (Retrieval), then have the AI answer using them (Generation)”** is RAG.

**💡 Everyday analogy: open-book exam**
- **Plain LLM**: Student relying on memory alone (forgets or guesses wrong).
- **RAG**: Student opens the textbook (Vector DB) to relevant pages and writes answers from them (accurate, up-to-date).

| Process | Student analogy | RAG system |
| :--- | :--- | :--- |
| **1. Question input** | Read exam question | User asks “How do I take paid leave per company policy?” |
| **2. Retrieval** | Find relevant pages in textbook index | Vectorize question; search Vector DB for similar passages |
| **3. Augmentation** | Open pages on desk | Paste retrieved text into prompt |
| **4. Generation** | Write answer in own words while reading | Instruct LLM “answer from reference text”; get response |

### 💡 Concrete business use cases
- **Internal policy/manual search**: Vectorize huge document sets; employees ask “How do I …?” and get accurate answers from relevant rules—a help desk.
- **E-commerce semantic search**: User searches “cool clothes for the beach in summer”; recommend items by meaning (vector) even without keywords in product names.
- **Past troubleshooting search**: Engineer enters error/symptom; Vector DB finds similar incidents and fixes for faster incident response.

<img src="../../assets/units/unit24_vector_dbs_rag_from_scratch/images/diagram-workflow.svg" alt="Diagram: Vector search" class="unit-diagram" />

## 2. Implementation Example

Build RAG from zero using basic Python and simple vector libraries—no heavy RAG framework.

> ※ Install `pip install scikit-learn openai` first. (We use scikit-learn cosine similarity for clarity.)

```python
import os
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# =========================================
# [Setup] Build a stand-in for a Vector DB
# =========================================

# 1. Document list serving as knowledge (e.g., internal manuals)
documents = [
    "AI training requires large amounts of data.",
    "Our company grants 10 days of paid leave six months after joining.",
    "Submit expense reports through System X by the end of each month.",
    "Python is an excellent programming language for AI development."
]

# 2. Function to convert text into a vector (numeric array)
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small" # OpenAI embedding model
    )
    return response.data[0].embedding

# 3. Vectorize and store all documents (simple Vector DB complete)
print("Vectorizing documents...")
doc_embeddings = [get_embedding(doc) for doc in documents]

# =========================================
# [Execution] Run the RAG pipeline
# =========================================

# 4. User question
question = "When do I receive paid leave?"
print(f"Question: {question}")

# 5. Vectorize the question as well
question_embedding = get_embedding(question)

# 6. [Retrieval] Compute similarity between question vector and each document vector
# cosine_similarity: closer to 1 means more semantically similar
similarities = cosine_similarity([question_embedding], doc_embeddings)[0]

# Get index of the most similar (closest in meaning) document
best_index = np.argmax(similarities)
best_document = documents[best_index]
print(f"Retrieved reference: {best_document}")

# 7. [Augmentation & Generation] Embed retrieved material in prompt and generate answer
prompt = f"""
Answer the user's [Question] using only the [Reference Material] below.

[Reference Material]
{best_document}

[Question]
{question}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.0
)

print("\nFinal AI answer:")
print(response.choices[0].message.content)
```

**🔍 Detailed code walkthrough**
1. **Setup (build database)**: Prepare the knowledge list to teach the AI.
2. **Vectorization (Embedding)**: Convert text to numeric arrays so the computer can measure “semantic nearness.”
3. **Retrieval**: Vectorize the user question; use **cosine similarity** to find the closest document—even without keyword match.
4. **Prompt creation (Augmentation)**: Build “answer from this material” instructions and insert retrieved text.
5. **Answer generation (Generation)**: Send the prompt to the LLM for an answer grounded in retrieved content.

## 3. Practice

Extend the example to retrieve **top 3 related documents** and embed all of them in the prompt.

**【Requirements】**
- Expand the document database to about 10 entries (AI topics, company rules, etc.).
- Instead of `np.argmax()` for one document, retrieve the **top 3** by similarity.
- Concatenate all three in the prompt’s [Reference Material] section and have the AI answer.

**💡 Hint**
- `np.argsort()` returns sorted indices; reverse for descending similarity order.

## 4. Answer Key

<details>
<summary>View sample solution (click to expand)</summary>

```python
import os
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_embedding(text):
    response = client.embeddings.create(
        input=text, model="text-embedding-3-small"
    )
    return response.data[0].embedding

# 1. Document list (expanded dataset)
documents = [
    "AI training requires large amounts of data.",
    "Our company grants 10 days of paid leave six months after joining.",
    "Submit expense reports through System X by the end of each month.",
    "Python is an excellent programming language for AI development.",
    "To request paid leave, notify your manager at least one week in advance.",
    "System X login passwords must be changed every 3 months.",
    "Three days of summer special leave are granted as additional time off.",
    "Machine learning includes supervised learning and unsupervised learning."
]

print("Vectorizing documents...")
doc_embeddings = [get_embedding(doc) for doc in documents]

question = "What are the rules and allocation for taking paid leave?"
question_embedding = get_embedding(question)

# 2. Compute similarity
similarities = cosine_similarity([question_embedding], doc_embeddings)[0]

# 3. Get indices of the top 3 highest similarities
# argsort returns ascending order; [::-1] reverses to descending, [:3] takes top 3
top_3_indices = np.argsort(similarities)[::-1][:3]

# 4. Extract and combine the top 3 documents
retrieved_docs = []
for idx in top_3_indices:
    retrieved_docs.append(documents[idx])

# Join documents with newlines
context_text = "\n- ".join(retrieved_docs)
print(f"[Retrieved materials]\n- {context_text}\n")

# 5. Embed in prompt and generate
prompt = f"""
Answer the user's [Question] using only the [Reference Material] below.

[Reference Material]
- {context_text}

[Question]
{question}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.0
)

print("[AI answer]")
print(response.choices[0].message.content)
```
</details>
