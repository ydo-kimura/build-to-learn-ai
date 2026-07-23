# Unit 21: NLP Capstone (Comprehensive Exercise)

<p class="unit-hero">
  <img src="/en/assets/units/unit21_nlp_capstone/images/hero.png" alt="Hero: NLP Capstone" />
</p>

## 1. Understanding Comprehensive NLP (Building a Transformer)

<img src="/en/assets/units/unit21_nlp_capstone/images/diagram-concept.svg" alt="Diagram: NLP project flow" class="unit-diagram" />

In Chapter 3 (Units 17–20), you learned NLP fundamentals starting with tokenization and TF-IDF, then Word2Vec for multi-dimensional word vectors, RNN/LSTM for applying context to sequential data, and finally **Attention and the Transformer architecture**—the foundation of all modern LLMs.

In this capstone, you bring those concepts together and implement a translation engine from scratch: **tokenize parallel text data ➔ build a simple vocabulary ➔ construct a tiny encoder–decoder Transformer ➔ run a parallel-corpus training loop ➔ perform inference decoding that translates English input into Japanese automatically**. First inspect the Transformer components on a four-sentence minimal implementation, then extend to five sentences to compare and select it against an LSTM. This is a toy model and does not demonstrate useful translation quality on unseen text.

**💡 Everyday analogy: the simultaneous interpreter’s inner mechanism**

- **Tokenization and vocabulary**: Replace English and Japanese words with “word cards (IDs)” and organize an in-brain parallel dictionary.
- **Encoder (the listener)**: Analyze “what matters (Self-Attention)” in the English speaker’s sentence and produce a summary note (context vector) that captures the full context.
- **Decoder (the translator who speaks)**: Read the note and, comparing it with what it has already said, generate the next most probable Japanese word one at a time (autoregressive).

---

<img src="/en/assets/units/unit21_nlp_capstone/images/diagram-workflow.svg" alt="Diagram: Stack options" class="unit-diagram" />

## 2. Implementation Example

Here we use PyTorch’s `nn.Transformer` module with a very small sample English–Japanese dataset to build, train, and run inference on a simple English ➔ Japanese translation model with a complete code example.

> **Colab setup:** The current Colab runtime includes PyTorch, so no additional installation is required.

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Fix random seed
torch.manual_seed(42)

# 1. Tiny English-English parallel corpus and simple tokenizer (whitespace split)
corpus = [
    ("hello world", "greetings earth"),
    ("i love ai", "I adore AI"),
    ("this is deep learning", "that is neural learning"),
    ("make a future", "build a future")
]

# Build word vocabulary
# Special tokens: <pad> (padding), <sos> (start), <eos> (end)
src_vocab = {"<pad>": 0}
tgt_vocab = {"<pad>": 0, "<sos>": 1, "<eos>": 2}

for src_sentence, tgt_sentence in corpus:
    for word in src_sentence.split():
        if word not in src_vocab:
            src_vocab[word] = len(src_vocab)

    for word in tgt_sentence.split():
        if word not in tgt_vocab:
            tgt_vocab[word] = len(tgt_vocab)

# Reverse vocabulary (lookup word from ID)
inv_tgt_vocab = {v: k for k, v in tgt_vocab.items()}

# 2. Convert text to ID vectors
def sentence_to_ids(sentence, vocab, add_sos=False, add_eos=False):
    ids = []
    if add_sos:
        ids.append(vocab["<sos>"])
    for word in sentence.split():
        if word in vocab:
            ids.append(vocab[word])
    if add_eos:
        ids.append(vocab["<eos>"])
    return ids

# 3. Define a simple Transformer model
class Seq2SeqTransformer(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model=32, nhead=2, num_layers=1):
        super().__init__()
        # Word embedding layers
        self.src_embedding = nn.Embedding(src_vocab_size, d_model)
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, d_model)

        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_layers,
            num_decoder_layers=num_layers,
            batch_first=True
        )

        self.fc_out = nn.Linear(d_model, tgt_vocab_size)

    def forward(self, src, tgt):
        src_emb = self.src_embedding(src)
        tgt_emb = self.tgt_embedding(tgt)

        # Create causal mask so the decoder cannot see future tokens
        tgt_seq_len = tgt.size(1)
        tgt_mask = self.transformer.generate_square_subsequent_mask(tgt_seq_len).to(src.device)

        out = self.transformer(src_emb, tgt_emb, tgt_is_causal=True, tgt_mask=tgt_mask)
        return self.fc_out(out)

# 4. Instantiate model and configure training
model = Seq2SeqTransformer(len(src_vocab), len(tgt_vocab))
criterion = nn.CrossEntropyLoss(ignore_index=0) # ignore <pad>
optimizer = optim.Adam(model.parameters(), lr=0.005)

# Training loop
model.train()
for epoch in range(100):
    epoch_loss = 0
    for src_text, tgt_text in corpus:
        src_ids = torch.tensor([sentence_to_ids(src_text, src_vocab)], dtype=torch.long)
        tgt_in_ids = torch.tensor([sentence_to_ids(tgt_text, tgt_vocab, add_sos=True)], dtype=torch.long)
        tgt_out_ids = torch.tensor([sentence_to_ids(tgt_text, tgt_vocab, add_eos=True)], dtype=torch.long)

        optimizer.zero_grad()
        outputs = model(src_ids, tgt_in_ids)
        loss = criterion(outputs.view(-1, len(tgt_vocab)), tgt_out_ids.view(-1))
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()

    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}/100 | Total Loss: {epoch_loss:.4f}")

# 5. Inference phase (autoregressive decoding)
model.eval()
def translate(src_sentence):
    src_ids = torch.tensor([sentence_to_ids(src_sentence, src_vocab)], dtype=torch.long)
    tgt_ids = [tgt_vocab["<sos>"]]

    for _ in range(10):
        tgt_tensor = torch.tensor([tgt_ids], dtype=torch.long)
        with torch.no_grad():
            outputs = model(src_ids, tgt_tensor)

        next_word_id = outputs[0, -1].argmax().item()
        if next_word_id == tgt_vocab["<eos>"]:
            break
        tgt_ids.append(next_word_id)

    return " ".join([inv_tgt_vocab[idx] for idx in tgt_ids[1:]])

print("\n--- Translation test ---")
test_phrase = "i love ai"
print(f"Source: {test_phrase}")
print(f"Translation: {translate(test_phrase)}")
```


## 3. Practice — 🧠 Design Your Own NLP Architecture Through Comparison

In NLP and machine translation, the iron rule for choosing a production model is to **validate multiple different approaches**. Rather than “using Transformer because it’s trendy,” experience the process of **deciding which model to design and deploy through quantitative comparison** under trade-offs among data volume, compute cost, and contextual accuracy.

**【Requirements】**
Using the expanded **5-sentence parallel dataset** below, implement, train, and evaluate a high-quality translation model that captures input similarity (`i love learning` vs. `i love ai`) and translates correctly.

```python
# 1. Expanded parallel corpus (vocabulary has grown)
corpus = [
    ("hello world", "greetings earth"),
    ("i love ai", "I adore AI"),
    ("this is deep learning", "that is neural learning"),
    ("make a future", "build a future"),
    ("i love learning", "I adore studying") # competing / similar sentence
]

# Build a word vocabulary (Vocabulary) from this corpus.
```

**【Your mission: compare two hypothesis models and decide which to deploy】**

With only five sentences—a harsh constraint—**implement and compare both approaches below**.

1. **Approach A (RNN/LSTM-based Seq2Seq + Attention)**
   - **Design**: Using PyTorch, adopt LSTM encoders and decoders that process words in time order, and **design an RNN-Attention model** with a simple attention mechanism.
   - **Characteristics**: Fewer parameters and direct sequential processing can make it easier to train on tiny data, but generalization still requires held-out evaluation.
2. **Approach B (Transformer model)**
   - **Design**: Build an **encoder–decoder Transformer** based on PyTorch’s `nn.Transformer`, applying the Causal Mask (no peeking at future tokens) correctly.
   - **Characteristics**: High expressive power and parallel training, but only 5 sentences can make overfitting likely. Keep hyperparameters (`d_model`, `nhead`, `num_layers`, etc.) small and evaluate on held-out examples.

---

**【Design decision notes to record in code comments】**

1. **Shared vocabulary and tokenization design**:
   - Describe how you define special tokens (`<pad>`, `<sos>`, `<eos>`) and convert sentences to ID arrays.
2. **Model size and hyperparameter rationale per approach**:
   - Explain how you sized Approach A (LSTM) hidden dimensions and Approach B (Transformer) `d_model`, `nhead`, and layer count for “tiny data.”
3. **Training and autoregressive decoding**:
   - Choose optimal epochs and learning rate and run training.
   - Implement **autoregressive decoding** (predicting the next word one at a time) on both models for the unseen English sentence `"i love learning"`.
4. **Quantitative evaluation and final decision**:
   - Verify whether the test sentence translates to the expected output (`I adore studying`), and **document which model you chose for production and why**.


## 4. Answer Key — 💡 Professional NLP Architecture Design and Decision-Making

<details>
<summary>View sample solution (click to expand)</summary>

### 💡 Criteria for NLP design decisions as an AI engineer

Review representative trade-offs when designing and deploying NLP models in practice.

#### Design decision matrix (this tiny-data case)

| Evaluation axis             | Approach A (RNN/LSTM + Attention)                                                   | Approach B (Transformer)                                                                                              | Design decision point                                                                                                                        |
| :-------------------------- | :---------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| **Small-data fit**          | A relatively simple structure can be easier to train, but it can still overfit.     | Parameter count and settings can make overfitting more likely. Compare learning curves and held-out data.             |
| **Long-text understanding** | Long-range dependencies can become difficult to retain.                             | Self-Attention can handle long-range dependencies more directly, but length, compute, and training data still matter. |
| **Training parallelism**    | Processes one word at a time; no GPU parallelism; huge datasets take enormous time. | Batch-processes all tokens during training; highly parallel and fast.                                                 | Speed difference is negligible at 5 sentences, but correctly understanding and implementing LLM core mechanisms (Causal Mask, etc.) matters. |

---

### Comparison pipeline implementation example

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Fix random seed
torch.manual_seed(42)

# 1. Shared parallel corpus and vocabulary construction
corpus = [
    ("hello world", "greetings earth"),
    ("i love ai", "I adore AI"),
    ("this is deep learning", "that is neural learning"),
    ("make a future", "build a future"),
    ("i love learning", "I adore studying")
]

src_vocab = {"<pad>": 0}
tgt_vocab = {"<pad>": 0, "<sos>": 1, "<eos>": 2}

for src_sentence, tgt_sentence in corpus:
    for word in src_sentence.split():
        if word not in src_vocab:
            src_vocab[word] = len(src_vocab)
    for word in tgt_sentence.split():
        if word not in tgt_vocab:
            tgt_vocab[word] = len(tgt_vocab)

inv_tgt_vocab = {v: k for k, v in tgt_vocab.items()}

def sentence_to_ids(sentence, vocab, add_sos=False, add_eos=False):
    ids = []
    if add_sos:
        ids.append(vocab["<sos>"])
    for word in sentence.split():
        if word in vocab:
            ids.append(vocab[word])
    if add_eos:
        ids.append(vocab["<eos>"])
    return ids

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------------------------------------------
# Approach B: Transformer translation model (designed to be ultra-compact)
# -----------------------------------------------------------------
# Implement Transformer as the foundation of LLMs, for contrast with Approach A (LSTM).
class Seq2SeqTransformer(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model=32, nhead=2, num_layers=1):
        super().__init__()
        self.src_embedding = nn.Embedding(src_vocab_size, d_model)
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, d_model)
        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_layers,
            num_decoder_layers=num_layers,
            batch_first=True
        )
        self.fc_out = nn.Linear(d_model, tgt_vocab_size)

    def forward(self, src, tgt):
        src_emb = self.src_embedding(src)
        tgt_emb = self.tgt_embedding(tgt)

        # Generate causal mask (prevents seeing future tokens)
        tgt_seq_len = tgt.size(1)
        tgt_mask = self.transformer.generate_square_subsequent_mask(tgt_seq_len).to(src.device)

        out = self.transformer(src_emb, tgt_emb, tgt_is_causal=True, tgt_mask=tgt_mask)
        return self.fc_out(out)

# -----------------------------------------------------------------
# Model training loop (Transformer)
# -----------------------------------------------------------------
# With tiny data, use d_model=32, nhead=2, layers=1 to reduce overfitting while keeping multi-head attention
model = Seq2SeqTransformer(len(src_vocab), len(tgt_vocab), d_model=32, nhead=2, num_layers=1).to(device)
criterion = nn.CrossEntropyLoss(ignore_index=0)
optimizer = optim.Adam(model.parameters(), lr=0.005)

model.train()
for epoch in range(120):
    epoch_loss = 0
    for src_text, tgt_text in corpus:
        src_ids = torch.tensor([sentence_to_ids(src_text, src_vocab)], dtype=torch.long).to(device)
        tgt_in_ids = torch.tensor([sentence_to_ids(tgt_text, tgt_vocab, add_sos=True)], dtype=torch.long).to(device)
        tgt_out_ids = torch.tensor([sentence_to_ids(tgt_text, tgt_vocab, add_eos=True)], dtype=torch.long).to(device)

        optimizer.zero_grad()
        outputs = model(src_ids, tgt_in_ids)
        loss = criterion(outputs.view(-1, len(tgt_vocab)), tgt_out_ids.view(-1))
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()

# -----------------------------------------------------------------
# Translation inference via autoregressive decoding (Transformer)
# -----------------------------------------------------------------
model.eval()
def translate(src_sentence):
    src_ids = torch.tensor([sentence_to_ids(src_sentence, src_vocab)], dtype=torch.long).to(device)
    tgt_ids = [tgt_vocab["<sos>"]]

    for _ in range(10):
        tgt_tensor = torch.tensor([tgt_ids], dtype=torch.long).to(device)
        with torch.no_grad():
            outputs = model(src_ids, tgt_tensor)

        next_word_id = outputs[0, -1].argmax().item()
        if next_word_id == tgt_vocab["<eos>"]:
            break
        tgt_ids.append(next_word_id)

    return " ".join([inv_tgt_vocab[idx] for idx in tgt_ids[1:]])

print("--- Evaluation results based on design decision ---")
test_phrase = "i love learning"
print(f"Input (English): {test_phrase}")
print(f"Translation output: {translate(test_phrase)}")
```

### 💡 Final production model decision as a professional

Experiments on this tiny dataset (5 sentences) yield surprising results.

- **Decision rationale (Approach A vs. Approach B)**:
  - With only 5 sentences, Approach A (RNN/LSTM + Attention) converges very stably due to its simpler structure, avoids overfitting, and tends to output `"I adore studying"` perfectly. Approach B (Transformer) has many attention-head and fully connected parameters; with 5 sentences, attention for `"i love learning"` and `"i love ai"` can collide (mix and overfit), causing decode-time hallucination—e.g., wrongly outputting `"I adore AI"`.
- **Final deployment decision**:
  - **“For this tiny-data experiment, select Approach A (RNN/LSTM + Attention) as the candidate.”**
  - **Rationale**:
    1. For ultra-compact domain rule data (e.g., manual parallel text) that must be memorized and applied immediately, RNN delivers far lower compute cost and prevents overfitting while preserving translation quality on tiny data.
    2. If parallel corpus scale to tens of thousands of sentences is certain later, a two-stage roadmap—migrating architecture to **Approach B (Transformer)** for parallelism and long-range context—is the most realistic, architect-level judgment.

Rather than “Transformer is strongest, so always use it,” **choosing classical RNN/LSTM for current data scale and operating cost, then scaling to Transformer as volume grows** is the highest-value judgment expected of enterprise AI engineers.
</details>
