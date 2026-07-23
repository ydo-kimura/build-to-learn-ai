# Unit 21: 自然言語処理総合演習 (Capstone)

<p class="unit-hero">
  <img src="../../assets/units/unit21_nlp_capstone/images/hero.png" alt="ヒーロー画像：NLP Capstone" />
</p>

## 1. 総合自然言語処理（Transformer 構築）の理解

第3章（Unit 17〜20）において、テキストの分かち書きや TF-IDF に始まる自然言語処理の基礎から、単語の持つ意味を多次元ベクトル化する Word2Vec、系列データに文脈を適用させる RNN / LSTM、そして現在のLLMのすべての基盤となっている **Attention（注意機構）と Transformer アーキテクチャ** を学びました。

この総合演習では、それらの概念を結集し、 **「対訳テキストデータのトークン化 ➔ 簡易辞書（Vocabulary）の作成 ➔ 位置情報を含むエンコーダー・デコーダー型の極小 Transformer モデルの構築 ➔ 対訳学習ループの実行 ➔ 英語を入力して日本語へ自動翻訳する推論デコード」** という流れを実装します。まず4文の最小実装でTransformerの部品を確認し、次に5文へ拡張してLSTMとの比較・選定を行います。これは現代の生成AIの部品を体験するためのToyモデルであり、未知の文章への翻訳性能や実用的な品質を示すものではありません。

**💡 日常の例え：国際同時通訳者の脳内メカニズム**

- **トークン化と辞書（Vocabulary）** : 英語と日本語の言葉をそれぞれ「単語カード（番号）」に置き換えて、脳内の対訳辞書を整理すること。
- **エンコーダー（話を聞く側）** : 英語のスピーカーが話した文章の「どこが重要か（Self-Attention）」を分析し、全体の文脈を含んだ要約メモ（コンテキストベクトル）を作成すること。
- **デコーダー（翻訳を喋る側）** : メモを読みながら、これまで自分が喋った言葉の履歴と照らし合わせて、「次に最も確率が高い日本語の単語」を順番に1語ずつ（Autoregressive）紡ぎ出していくこと。

下図は、テキスト入力からエンコーダー・デコーダーを経て翻訳を出力する、 **翻訳モデルの流れ** です。

<img src="../../assets/units/unit21_nlp_capstone/images/diagram-concept.svg" alt="図解：推論時の翻訳モデルの流れ（学習・トークン化は省略）" class="unit-diagram" />

---

下図は、 **TF-IDF + 古典的 ML** と **Embeddings + NN** のスタック比較です。

<img src="../../assets/units/unit21_nlp_capstone/images/diagram-workflow.svg" alt="図解：技術スタックの選択肢（TF-IDF＋古典的 ML と Embeddings＋NN の比較）" class="unit-diagram" />

## 2. 実装例 (Implementation Example)

ここでは、PyTorchの `nn.Transformer` モジュールをベースとし、ごく少数のサンプル英文と日本文のデータセットを使って、Transformerを用いた「英語 ➔ 日本語」の簡易的な翻訳モデルを構築・学習・推論する動作例を実装します。

> **Colab セットアップ:** 現行の Colab には PyTorch が含まれているため、追加インストールは不要です。

```python
import math
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

# 3. 位置エンコーディングの定義
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=64):
        super().__init__()
        # 最長文と特殊トークンに余裕を持たせた固定長。推論ループの上限10もこの範囲内。
        position = torch.arange(max_len, dtype=torch.float32).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2, dtype=torch.float32)
                             * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, d_model)
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]

# 4. 簡易Transformerモデルの定義
class Seq2SeqTransformer(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model=32, nhead=2, num_layers=1):
        super().__init__()
        # 単語埋め込みレイヤー
        self.src_embedding = nn.Embedding(src_vocab_size, d_model)
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, d_model)
        self.positional_encoding = PositionalEncoding(d_model)

        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_layers,
            num_decoder_layers=num_layers,
            batch_first=True
        )

        self.fc_out = nn.Linear(d_model, tgt_vocab_size)

    def forward(self, src, tgt):
        src_emb = self.positional_encoding(self.src_embedding(src))
        tgt_emb = self.positional_encoding(self.tgt_embedding(tgt))

        # デコーダーが未来の単語を見ないようにする「マスク（Causal Mask）」を作成
        tgt_seq_len = tgt.size(1)
        tgt_mask = self.transformer.generate_square_subsequent_mask(tgt_seq_len).to(src.device)

        out = self.transformer(src_emb, tgt_emb, tgt_is_causal=True, tgt_mask=tgt_mask)
        return self.fc_out(out)

# 5. モデルのインスタンス化と学習の設定
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

# このデータセットは4文だけなので、まずは学習した文を再現できるかを確認します。
# 実務では、未使用の検証データ、BLEU/ROUGE等の評価、未知語の扱いを別途設計します。
for source, expected in corpus:
    predicted = translate(source)
    print(f"期待値: {expected} / 予測: {predicted}")
```

---

## 3. 実践 (Practice) - 🧠 自分で比較し決定するNLPアーキテクチャ設計

自然言語処理や機械翻訳システムにおいても、ビジネス上の最終適用モデルを選ぶためには「複数の異なるアプローチ」を検証することが絶対の鉄則です。「最新のTransformerが流行っているから使う」のではなく、データ量や計算コスト、および文脈理解の正確性というトレードオフのもとで、 **「どのモデルをどう設計し適用するか」を定量的な比較から決定するプロセス** を体験しましょう。

**【課題の要件】**
以下の拡張された「5文の対訳データセット」を用い、入力文の類似性（`i love learning` と `i love ai`）を捉えつつ、正しく翻訳できる高品質な翻訳モデルを実装・学習・評価してください。

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

**【あなたのミッション：2つの仮説モデルの比較と適用意思決定】**

データ数が極小（わずか5文）という過酷な状況において、以下の2つのアプローチを **両方自分で実装して比較検証** してください。

1. **アプローチA（RNN / LSTMベースのSeq2Seq ＋ Attentionモデル）**
   - **設計** : PyTorchを用いて、単語を時系列順に処理するLSTMをエンコーダーおよびデコーダーに採用し、簡易的なAttentionメカニズムを組み込んだ **RNN-Attentionモデルを設計** してください。
   - **特徴** : パラメータ数が比較的少なく、時系列データをそのまま処理します。極めて小さなデータ（5文）では学習しやすい場合がありますが、汎化は別途検証が必要です。
2. **アプローチB（Transformerモデル）**
   - **設計** : PyTorchの `nn.Transformer` モジュールをベースとし、Causal Mask（未来視不可マスク）を正しく適用した **エンコーダー・デコーダー型Transformerモデルを構築** してください。
   - **特徴** : 表現力と並列計算能力が高い一方、データ数が5文という極小環境では過学習しやすい可能性があります。ハイパーパラメータ（`d_model`, `nhead`, `num_layers` など）と検証条件を小さく設計します。

---

**【コード内にコメントで記述すべき「設計判断ノート」】**

1. **辞書（Vocabulary）とトークン化の共通設計** :
   - 特殊トークン（`<pad>`, `<sos>`, `<eos>`）をどう定義し、どのように文章をID配列に変換するかを記述してください。
2. **モデルサイズ・ハイパーパラメータの個別設計理由** :
   - アプローチA（LSTM）の隠れ層次元数、アプローチB（Transformer）の `d_model`, `nhead`, レイヤー数をどのように「極小データ向け」に設計したかの根拠を記述してください。
3. **学習と自己回帰デコードの実装** :
   - 最適なエポック数と学習率を決定して学習を実行してください。
   - 訓練データに含まれる英文 `"i love learning"` （類似文 `"i love ai"` と競合しやすい文）を入力した際に、1語ずつ次の単語を予測して出力する「自己回帰デコード（Autoregressive Decoding）」を両モデルで実装し、両者を正しく区別して翻訳できるかを確認してください。
4. **定量評価と最終意思決定** :
   - テスト文が期待される日本語（`私は 学習が 大好きです`）に正しく翻訳されたかを確認し、 **あなたが最終的に本番適用として選んだモデルと、その論理的な理由** を記述してください。

---

## 4. 答え合わせ (Answer Key) - 💡 プロのNLPアーキテクチャ設計と意思決定

<details>
<summary>解答例を見る（クリックで展開）</summary>

### 💡 AIエンジニアとしてのNLP設計決定の基準

自然言語処理モデルを実務で設計・適用する際の代表的なトレードオフを確認しましょう。

#### 設計意思決定マトリクス（今回の極小データケース）

| 評価軸             | アプローチA（RNN/LSTM + Attention）                                                            | アプローチB（Transformer）                                                             | 今回の設計判断のポイント                                                                                        |
| :----------------- | :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| **小データ適応力** | 比較的単純な構造で学習できる場合があるが、過学習しないとは限らない。                           | パラメータ数や設定によって過学習しやすい。                                             | 今回の5文データだけで一般的な優劣を断定せず、学習曲線と評価用データを確認する。                                 |
| **長文の理解**     | 長距離依存を扱いにくくなる場合がある。                                                         | Self-Attentionにより長距離依存を扱いやすいが、長さ・計算量・学習データの影響を受ける。 | 長文の実データで評価し、Transformerを含む候補を比較する。                                                       |
| **学習の並列性**   | 1単語ずつ順番に処理するため、GPUでの並列計算ができず、巨大データの学習には膨大な時間がかかる。 | 訓練時に全単語を一括処理できるため並列計算が可能で、超高速。                           | 5文では速度差はありませんが、LLMの心臓部としての仕組み（Causal Maskなど）を正しく理解し実装することが重要です。 |

---

### 比較検証パイプラインの実装例

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
# アプローチA: LSTMベースの Seq2Seq + 簡易Attention 翻訳モデル
# -----------------------------------------------------------------
# 極小データ（5文）向けに、埋め込み・隠れ層とも32次元の小さな構成に設計
class Seq2SeqLSTM(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, emb_dim=32, hidden_dim=32):
        super().__init__()
        self.src_embedding = nn.Embedding(src_vocab_size, emb_dim)
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, emb_dim)
        # エンコーダー: 英語の単語列を順番に読み、文脈を隠れ状態に蓄積する
        self.encoder = nn.LSTM(emb_dim, hidden_dim, batch_first=True)
        # デコーダー: エンコーダーの最終状態を受け取り、日本語を1語ずつ生成する
        self.decoder = nn.LSTM(emb_dim, hidden_dim, batch_first=True)
        # Attentionで得た文脈ベクトルとデコーダー出力を結合して次の単語を予測
        self.fc_out = nn.Linear(hidden_dim * 2, tgt_vocab_size)

    def forward(self, src, tgt):
        enc_out, (h, c) = self.encoder(self.src_embedding(src))
        dec_out, _ = self.decoder(self.tgt_embedding(tgt), (h, c))
        # 簡易Attention: デコーダー各時刻の出力とエンコーダー全時刻の出力の
        # 内積をスコアとし、softmaxで重み付けして文脈ベクトルを作る
        scores = torch.bmm(dec_out, enc_out.transpose(1, 2))
        attn_weights = torch.softmax(scores, dim=-1)
        context = torch.bmm(attn_weights, enc_out)
        return self.fc_out(torch.cat([dec_out, context], dim=-1))

# アプローチAの訓練ループ
model_a = Seq2SeqLSTM(len(src_vocab), len(tgt_vocab)).to(device)
criterion_a = nn.CrossEntropyLoss(ignore_index=0)
optimizer_a = optim.Adam(model_a.parameters(), lr=0.005)

model_a.train()
for epoch in range(120):
    for src_text, tgt_text in corpus:
        src_ids = torch.tensor([sentence_to_ids(src_text, src_vocab)], dtype=torch.long).to(device)
        tgt_in_ids = torch.tensor([sentence_to_ids(tgt_text, tgt_vocab, add_sos=True)], dtype=torch.long).to(device)
        tgt_out_ids = torch.tensor([sentence_to_ids(tgt_text, tgt_vocab, add_eos=True)], dtype=torch.long).to(device)

        optimizer_a.zero_grad()
        outputs = model_a(src_ids, tgt_in_ids)
        loss = criterion_a(outputs.view(-1, len(tgt_vocab)), tgt_out_ids.view(-1))
        loss.backward()
        optimizer_a.step()

# アプローチAの自己回帰デコード
model_a.eval()
def translate_a(src_sentence):
    src_ids = torch.tensor([sentence_to_ids(src_sentence, src_vocab)], dtype=torch.long).to(device)
    tgt_ids = [tgt_vocab["<sos>"]]
    for _ in range(10):
        tgt_tensor = torch.tensor([tgt_ids], dtype=torch.long).to(device)
        with torch.no_grad():
            outputs = model_a(src_ids, tgt_tensor)
        next_word_id = outputs[0, -1].argmax().item()
        if next_word_id == tgt_vocab["<eos>"]:
            break
        tgt_ids.append(next_word_id)
    return " ".join([inv_tgt_vocab[idx] for idx in tgt_ids[1:]])

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
print(f"アプローチA (LSTM+Attention) の翻訳出力: {translate_a(test_phrase)}")
print(f"アプローチB (Transformer) の翻訳出力: {translate(test_phrase)}")
```

### 💡 プロフェッショナルとしての最終適用モデル決定

極小データセット（5文）での実験において、驚くべき結果が得られます。

- **意思決定の裏付け（アプローチA vs アプローチB）** :
  - データ数が5文しかない場合、アプローチA（`Seq2SeqLSTM`）は構造が比較的単純なため学習しやすい場合があります。ただし、この小さな訓練集合だけで過学習や汎化を判断できないため、別の文で確認します。
  - アプローチB（`Seq2SeqTransformer`）は、設定を小さくしてもマルチヘッドAttentionや内部の全結合層を含みます。5文だけでは過学習や出力の不安定さが起きる可能性があるため、同じ条件で学習曲線と評価データを比較します。ここで得られる差は、このToy条件での観測です。
- **最終適用判断（Decision）** :
  - **「この極小データ実験では、アプローチA（RNN/LSTM + Attention）を候補として選択する。」**
  - **意思決定の根拠** :
    1. 5文という超コンパクトなデータを素早く試すフェーズでは、RNNが少ない計算コストで扱いやすい場合があります。ただし、実運用の選択は検証データ、レイテンシ、保守性を含めて判断します。
    2. もし将来的にコーパス（対訳データ）が数万文規模にスケールアップすることが確実な場合は、並列計算と長距離文脈に強い **アプローチB（Transformer）** にシステムアーキテクチャを移行する、という二段構えのロードマップを引くのが最も現実的で優れたアーキテクトの判断です。

「Transformerだから常に使う」のではなく、 **「現時点のデータ規模と運用コストにおいて候補を比較し、必要に応じてRNN/LSTMからTransformerへ拡張する」** という意思決定を、検証結果とともに説明できることが重要です。
</details>
