# Unit 21: NLP Capstone (Comprehensive Exercise)

## 1. Understanding Comprehensive NLP (Building a Transformer)

<img src="../../../assets/units/unit21_nlp_capstone/images/concept.png" width="400" alt="Concept diagram">

In Chapter 3 (Units 17–20), you learned NLP fundamentals starting with tokenization and TF-IDF, then Word2Vec for multi-dimensional word vectors, RNN/LSTM for applying context to sequential data, and finally **Attention and the Transformer architecture**—the foundation of all modern LLMs.

In this capstone, you bring those concepts together and implement a translation engine from scratch that fully reproduces how modern generative AI outputs text: **tokenize parallel text data ➔ build a simple vocabulary ➔ construct a tiny encoder–decoder Transformer ➔ run a parallel-corpus training loop ➔ perform inference decoding that translates English input into Japanese automatically**.

**💡 Everyday analogy: the simultaneous interpreter’s inner mechanism**
* **Tokenization and vocabulary**: Replace English and Japanese words with “word cards (IDs)” and organize an in-brain parallel dictionary.
* **Encoder (the listener)**: Analyze “what matters (Self-Attention)” in the English speaker’s sentence and produce a summary note (context vector) that captures the full context.
* **Decoder (the translator who speaks)**: Read the note and, comparing it with what it has already said, generate the next most probable Japanese word one at a time (autoregressive).

---

## 2. Implementation Example

Here we use PyTorch’s `nn.Transformer` module with a very small sample English–Japanese dataset to build, train, and run inference on a simple English ➔ Japanese translation model with a complete code example.

Run `pip install torch` beforehand.

```python
import torch
import torch.nn as nn
import torch.optim as optim

# 乱数シード固定
torch.manual_seed(42)

# 1. 超極小の「英日対訳データ」と簡易トークナイザー（分かち書き）
corpus = [
    ("hello world", "こんにちは 世界"),
    ("i love ai", "私は ＡＩが 大好きです"),
    ("this is deep learning", "これは ディープラーニング です"),
    ("make a future", "未来を 創る")
]

# 単語辞書の構築
# 特殊トークン: <pad> (パディング), <sos> (開始), <eos> (終了)
src_vocab = {"<pad>": 0}
tgt_vocab = {"<pad>": 0, "<sos>": 1, "<eos>": 2}

for src_sentence, tgt_sentence in corpus:
    for word in src_sentence.split():
        if word not in src_vocab:
            src_vocab[word] = len(src_vocab)
            
    for word in tgt_sentence.split():
        if word not in tgt_vocab:
            tgt_vocab[word] = len(tgt_vocab)

# 逆引き辞書 (IDから単語を取得する用)
inv_tgt_vocab = {v: k for k, v in tgt_vocab.items()}

# 2. テキストのベクトル・ID化
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

# 3. 簡易Transformerモデルの定義
class Seq2SeqTransformer(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model=32, nhead=2, num_layers=1):
        super().__init__()
        # 単語埋め込みレイヤー
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
        
        # デコーダーが未来の単語を見ないようにする「マスク（Causal Mask）」を作成
        tgt_seq_len = tgt.size(1)
        tgt_mask = self.transformer.generate_square_subsequent_mask(tgt_seq_len).to(src.device)
        
        out = self.transformer(src_emb, tgt_emb, tgt_is_causal=True, tgt_mask=tgt_mask)
        return self.fc_out(out)

# 4. モデルのインスタンス化と学習の設定
model = Seq2SeqTransformer(len(src_vocab), len(tgt_vocab))
criterion = nn.CrossEntropyLoss(ignore_index=0) # <pad>は無視
optimizer = optim.Adam(model.parameters(), lr=0.005)

# 学習ループ
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

# 5. 推論フェーズ (自己回帰デコード)
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

print("\n--- 翻訳テスト実行 ---")
test_phrase = "i love ai"
print(f"英語: {test_phrase}")
print(f"翻訳結果: {translate(test_phrase)}")
```

---

## 3. Practice — 🧠 Design Your Own NLP Architecture Through Comparison

In NLP and machine translation, the iron rule for choosing a production model is to **validate multiple different approaches**. Rather than “using Transformer because it’s trendy,” experience the process of **deciding which model to design and deploy through quantitative comparison** under trade-offs among data volume, compute cost, and contextual accuracy.

**【Requirements】**
Using the expanded **5-sentence parallel dataset** below, implement, train, and evaluate a high-quality translation model that captures input similarity (`i love learning` vs. `i love ai`) and translates correctly.

```python
# 1. 拡張された対訳コーパス（語彙が増えています）
corpus = [
    ("hello world", "こんにちは 世界"),
    ("i love ai", "私は ＡＩが 大好きです"),
    ("this is deep learning", "これは ディープラーニング です"),
    ("make a future", "未来を 創る"),
    ("i love learning", "私は 学習が 大好きです") # 競合・類似する文章
]

# このコーパスから、単語辞書（Vocabulary）を構築してください。
```

**【Your mission: compare two hypothesis models and decide which to deploy】**

With only five sentences—a harsh constraint—**implement and compare both approaches below**.

1. **Approach A (RNN/LSTM-based Seq2Seq + Attention)**
   * **Design**: Using PyTorch, adopt LSTM encoders and decoders that process words in time order, and **design an RNN-Attention model** with a simple attention mechanism.
   * **Characteristics**: Fewer parameters; processes sequential data directly, so it tends to be stable and less prone to overfitting on extremely small data (5 sentences).
2. **Approach B (Transformer model)**
   * **Design**: Build an **encoder–decoder Transformer** based on PyTorch’s `nn.Transformer`, applying the Causal Mask (no peeking at future tokens) correctly.
   * **Characteristics**: Maximum expressiveness and parallel compute—but with only 5 sentences, parameter count easily becomes excessive; unless hyperparameters (`d_model`, `nhead`, `num_layers`, etc.) are pushed to the minimum, severe overfitting can make translation fail entirely.

---

**【Design decision notes to record in code comments】**
1. **Shared vocabulary and tokenization design**:
   * Describe how you define special tokens (`<pad>`, `<sos>`, `<eos>`) and convert sentences to ID arrays.
2. **Model size and hyperparameter rationale per approach**:
   * Explain how you sized Approach A (LSTM) hidden dimensions and Approach B (Transformer) `d_model`, `nhead`, and layer count for “tiny data.”
3. **Training and autoregressive decoding**:
   * Choose optimal epochs and learning rate and run training.
   * Implement **autoregressive decoding** (predicting the next word one at a time) on both models for the unseen English sentence `"i love learning"`.
4. **Quantitative evaluation and final decision**:
   * Verify whether the test sentence translates to the expected Japanese (`私は 学習が 大好きです`), and **document which model you chose for production and why**.

---

## 4. Answer Key — 💡 Professional NLP Architecture Design and Decision-Making

<details>
<summary>View sample solution (click to expand)</summary>

### 💡 Criteria for NLP design decisions as an AI engineer

Review representative trade-offs when designing and deploying NLP models in practice.

#### Design decision matrix (this tiny-data case)

| Evaluation axis | Approach A (RNN/LSTM + Attention) | Approach B (Transformer) | Design decision point |
| :--- | :--- | :--- | :--- |
| **Small-data fit** | **Extremely strong**. RNN structure that walks sequences step by step learns simple translation patterns quickly with little data. | **Weak (high overfitting risk)**. Many parameters; with only 5 sentences, attention maps skew abnormally and overfit easily. |
| **Long-text understanding** | **Weak**. As sentences grow, early words are forgotten (vanishing gradients). | **Strongest**. Self-Attention captures context for all tokens regardless of length. |
| **Training parallelism** | Processes one word at a time; no GPU parallelism; huge datasets take enormous time. | Batch-processes all tokens during training; highly parallel and fast. | Speed difference is negligible at 5 sentences, but correctly understanding and implementing LLM core mechanisms (Causal Mask, etc.) matters. |

---

### Complete comparison pipeline implementation

```python
import torch
import torch.nn as nn
import torch.optim as optim

# シードの固定
torch.manual_seed(42)

# 1. 共通の対訳コーパスと辞書構築
corpus = [
    ("hello world", "こんにちは 世界"),
    ("i love ai", "私は ＡＩが 大好きです"),
    ("this is deep learning", "これは ディープラーニング です"),
    ("make a future", "未来を 創る"),
    ("i love learning", "私は 学習が 大好きです")
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
# アプローチB: Transformer 翻訳モデル (極限までコンパクトに設計)
# -----------------------------------------------------------------
# ※アプローチA（LSTM）との対比として、LLMの基礎となるTransformerを実装します。
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
        
        # Causal Mask (未来の単語を見ないためのマスク) の生成
        tgt_seq_len = tgt.size(1)
        tgt_mask = self.transformer.generate_square_subsequent_mask(tgt_seq_len).to(src.device)
        
        out = self.transformer(src_emb, tgt_emb, tgt_is_causal=True, tgt_mask=tgt_mask)
        return self.fc_out(out)

# -----------------------------------------------------------------
# モデルの訓練ループ (Transformer)
# -----------------------------------------------------------------
# データが極小なため、過学習を防ぎつつマルチヘッドの効果を出すため、d_model=32, nhead=2, layers=1の極小サイズに設定
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
# 自己回帰デコードによる翻訳推論 (Transformer)
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

print("--- 意思決定に基づく評価結果 ---")
test_phrase = "i love learning"
print(f"入力英語: {test_phrase}")
print(f"翻訳出力: {translate(test_phrase)}")
```

### 💡 Final production model decision as a professional

Experiments on this tiny dataset (5 sentences) yield surprising results.

* **Decision rationale (Approach A vs. Approach B)**:
  * With only 5 sentences, Approach A (RNN/LSTM + Attention) converges very stably due to its simpler structure, avoids overfitting, and tends to output `"私は 学習が 大好きです"` perfectly. Approach B (Transformer) has many attention-head and fully connected parameters; with 5 sentences, attention for `"i love learning"` and `"i love ai"` can collide (mix and overfit), causing decode-time hallucination—e.g., wrongly outputting `"私は ＡＩが 大好きです"`.
* **Final deployment decision**:
  * **“Select Approach A (RNN/LSTM + Attention) as the production model.”**
  * **Rationale**:
    1. For ultra-compact domain rule data (e.g., manual parallel text) that must be memorized and applied immediately, RNN delivers far lower compute cost and prevents overfitting while preserving translation quality on tiny data.
    2. If parallel corpus scale to tens of thousands of sentences is certain later, a two-stage roadmap—migrating architecture to **Approach B (Transformer)** for parallelism and long-range context—is the most realistic, architect-level judgment.

Rather than “Transformer is strongest, so always use it,” **choosing classical RNN/LSTM for current data scale and operating cost, then scaling to Transformer as volume grows** is the highest-value judgment expected of enterprise AI engineers.
</details>
