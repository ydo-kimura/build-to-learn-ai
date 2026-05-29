# Unit 20: Attention and Transformers

<p class="unit-hero">
  <img src="/en/assets/units/unit20_attention_transformers/images/hero.png" alt="Hero: Attention & Transformers" />
</p>

## 1. Understanding Attention and Transformers

<img src="/en/assets/units/unit20_attention_transformers/images/diagram-concept.svg" alt="Diagram: Attention weights" class="unit-diagram" />

RNNs and LSTMs pass memory like a relay baton—long texts still forget early content.
**Attention** and the **Transformer** architecture built on it solved this and became the core of modern AI (ChatGPT and similar models). Self-Attention has quadratic computation with respect to sequence length, so long contexts require careful handling of compute, context length, positional information, and generation speed.

### 📌 Everyday analogy: "focus" in a meeting

You are taking minutes for a 10-person meeting.

**How an RNN listens:**
Try to memorize every word in order. Long meetings cause "what did someone say at the start…?" overload.

**How Attention listens:**
Focus on **keywords**.
"When 'revenue' appears, it strongly relates to 'target' the CEO said earlier!"—**directly compute relationships between distant words**.

**Self-Attention** in Transformers lets every word in a sentence simultaneously see how much it relates to every other word.

| Word | The | animal | didn't | cross | the | street | because | it  | was | too | tired |
| :--- | :-- | :----- | :----- | :---- | :-- | :----- | :------ | :-- | :-- | :-- | :---- |

What does "it" refer to? Humans know "tired" applies to "animal," not "street."
Self-Attention gives **strong attention** to "animal" and "tired" when processing "it."

### 📌 What is a Transformer?

Instead of processing word by word like RNNs, read **all words at once** and compute relationships with Attention—enabling parallel, fast training and models as large as ChatGPT.

### 📌 Positional Encoding—keeping order information

RNNs processed one word at a time, naturally knowing **word order**.
Transformers read everything in parallel—fast, but **position information is lost**.

In the meeting analogy, you know every keyword but not **who spoke first vs who replied later**. "The cat chased the dog" vs "The dog chased the cat" differ completely without order.

**Positional Encoding** fixes this by adding a **special vector for "which position am I in?"** to each word's input—parallel speed with order preserved.

### 💡 Concrete Business Use Cases

- **High-quality machine translation**: Attention captures long-range dependencies for natural, context-aware translation (Google Translate, DeepL, etc.).
- **Complex enterprise Q&A chatbots**: LLM foundations that attend to the right passages in long internal policy documents.
- **Contract review automation**: Find payment or confidentiality clauses in long legal text and flag risky wording with context.

<img src="/en/assets/units/unit20_attention_transformers/images/diagram-workflow.svg" alt="Diagram: Transformer block" class="unit-diagram" />

## 2. Implementation Example

Here you will experience the core Self-Attention computation in PyTorch—scoring which words attend to which.

### Code walkthrough

Self-Attention builds three vectors per word:

1. **Query (Q)**: What am I looking for? (e.g., "I am it—what do I refer to?")
2. **Key (K)**: What am I? (e.g., "I am animal" / "I am street")
3. **Value (V)**: My actual content/meaning

Steps:

- Take the dot product of `Q` and `K`, then divide by `√d_k` (the square root of the key dimension) to get **attention scores**. This reduces softmax saturation when the dimension is large.
- Softmax scores to probabilities summing to 1.
- Weight `V` by those probabilities for the output.

```python
import torch
import torch.nn.functional as F

# 1. Prepare data (3 words, each with a 4-dimensional vector)
# Example: [animal, street, it]
x = torch.tensor([
    [1.0, 0.0, 1.0, 0.0],  # Word 1 (animal) features
    [0.0, 1.0, 0.0, 1.0],  # Word 2 (street) features
    [1.0, 0.0, 0.5, 0.0],  # Word 3 (it) features; similar to animal
])

# 2. Prepare Q, K, V
# In a real model, linear projections would be applied here; use x directly for simplicity
Q = x
K = x
V = x

# 3. Compute attention scores (Q @ K^T)
# Measures similarity between each pair of words
scores = torch.matmul(Q, K.transpose(0, 1)) / torch.sqrt(torch.tensor(K.size(-1), dtype=K.dtype))
print("--- Attention Scores ---")
print(scores)

# 4. Softmax to probabilities (0-1 weights summing to 1)
attention_weights = F.softmax(scores, dim=-1)
print("\n--- Attention Weights ---")
print(attention_weights)

# 5. Final output: weighted sum of V by attention weights
output = torch.matmul(attention_weights, V)
print("\n--- Self-Attention output ---")
print(output)
```

### Key takeaways after running the code

- In `scores`, word 3 (it) vs word 1 (animal) has a high score (similar features).
- `attention_weights` show "it" pulling more information from "animal" when building meaning—that is Attention.

## 3. Practice

Use PyTorch's built-in `nn.MultiheadAttention` layer to run Attention.

**【Requirements】**

1. Use the random input embeddings below. This exercise checks tensor shapes and the API; the random weights do not necessarily encode a meaningful word relationship.
2. Implement sinusoidal or learned positional encoding.
3. Create Attention with `nn.MultiheadAttention` (`embed_dim=8`, `num_heads=2`).
4. Add positional information to the input embeddings, pass them as `query`, `key`, and `value`, and print `attn_output`.

**【Dataset】**

```python
import torch
import torch.nn as nn

# sequence_length=5, batch_size=1, embed_dim=8
# All values generated randomly
sequence_length = 5
batch_size = 1
embed_dim = 8

embedded = torch.rand(sequence_length, batch_size, embed_dim)
```

**【Hints】**

- Create layer: `attention_layer = nn.MultiheadAttention(embed_dim=8, num_heads=2)`
- Add positional information to the input embeddings before Attention. In this simplified example, do not add the same positional encoding separately to `query`, `key`, and `value`.
- Forward: `attn_output, attn_weights = attention_layer(embedded, embedded, embedded)`
- Built-in layers handle Q, K, V math in one line!

## 4. Answer Key

<details>
<summary>View sample solution (click to expand)</summary>

```python
import torch
import torch.nn as nn

# 1. Prepare data
sequence_length = 5
batch_size = 1
embed_dim = 8

# Create input embeddings before passing them to Attention
embedded = torch.rand(sequence_length, batch_size, embed_dim)

# 2. Add sinusoidal positional encoding to the input embeddings
position = torch.arange(sequence_length, dtype=torch.float32).unsqueeze(1)
div_term = torch.exp(torch.arange(0, embed_dim, 2, dtype=torch.float32) * (-torch.log(torch.tensor(10000.0)) / embed_dim))
positional_encoding = torch.zeros(sequence_length, 1, embed_dim)
positional_encoding[:, 0, 0::2] = torch.sin(position * div_term)
positional_encoding[:, 0, 1::2] = torch.cos(position * div_term)
embedded = embedded + positional_encoding

# 3. Define MultiheadAttention layer
# embed_dim: vector dimension per token
# num_heads: number of parallel attention heads
attention_layer = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=2)

# 4. Run attention
print("Running attention...")
attn_output, attn_weights = attention_layer(embedded, embedded, embedded)

# 4. Inspect results
print("\n--- Attention output (attn_output) ---")
print(attn_output.shape) # Same shape as the input embeddings: (5, 1, 8)
print(attn_output)

print("\n--- Attention weights (attn_weights) ---")
print(attn_weights.shape) # Which token attends to which: (1, 5, 5)
```

**Solution explanation:**
In real AI development you rarely write the math from scratch—you stack blocks like `nn.MultiheadAttention` and `nn.TransformerEncoderLayer`.
Stack many Attention layers, train on huge data, and you get the large language models (LLMs) you know well.

</details>
