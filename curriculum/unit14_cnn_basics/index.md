# Unit 14: 畳み込みニューラルネットワークの基礎

<p class="unit-hero">
  <img src="../../assets/units/unit14_cnn_basics/images/hero.png" alt="ヒーロー画像：CNN Basics" />
</p>

> [!TIP]
> **Google Colab で学習を進める方へ**
> ディープラーニング編（Unit 10〜16）では、計算を高速化するために **GPU の有効化** をおすすめします。設定手順は [Appendix (学習環境とキーの準備)](../appendix/index.md) の「Google Colaboratory での学習の進め方」のセクションを最初にご覧ください。

## 1. CNN Basics の理解

これまで学んできたニューラルネットワーク（MLP）は、画像を扱うのが大の苦手でした。なぜなら、画像を「1列の長〜いデータ」に引き延ばして処理してしまうため、画像の「縦・横の繋がり（形や輪郭）」という大切な情報が失われてしまうからです。

そこで登場するのが、画像認識の革命児 **CNN（畳み込みニューラルネットワーク / Convolutional Neural Network）** です！

**CNNは「虫眼鏡を持った名探偵」**

CNNの仕組みは、一枚の絵を「小さな虫眼鏡」で端から端までじっくりと舐め回すように観察するプロセスに似ています。

| CNNのパーツ | 名探偵の例え | 役割 |
|---|---|---|
| **畳み込み層 (Conv2d)** | 虫眼鏡で特定の特徴を探す | 「ここは縦の線があるぞ」「ここは丸い形だ」といった特徴（エッジや模様）を抽出します。 |
| **プーリング層 (MaxPool2d)** | 情報を要約・縮小する | 「このエリアに丸い形があった！」という一番強い証拠だけを残し、画像を小さく圧縮します。ズレに強くなります。 |
| **全結合層 (Linear)** | 証拠を並べて犯人を推理する | 最後に集まった「耳」「ヒゲ」「しっぽ」などの特徴リストを見て、「これは猫だ！」と最終判断を下します。 |

CNNは、 **「畳み込み（特徴を探す） → プーリング（要約する）」** のセットを何度か繰り返し、最後に **「全結合（推理する）」** という流れで構成されます。この形は、現代のAI画像認識の超基本スタイルです。


下図は、 **Conv → Pool → Linear** と積み重なる特徴抽出のブロックです。

<img src="../../assets/units/unit14_cnn_basics/images/diagram-concept.svg" alt="図解：CNN の基本ブロック（畳み込み→プーリング→全結合）" class="unit-diagram" />

### 💡 具体的なビジネスユースケース

- **製造業での不良品検知** : 工場のラインにカメラを設置し、流れてくる製品の傷や汚れなどの特徴（エッジ）を捉えて、自動で不良品を弾くシステム。
- **自動運転の物体認識** : 車載カメラの映像から、歩行者、他の車、信号機、道路標識などを瞬時に認識し、安全な運転制御に繋げる。
- **医療でのガン細胞検出** : CTスキャンやMRIの画像から、人間の目では見逃しがちな微小な腫瘍の形状（丸みや輪郭）を捉え、医師の診断をサポートする。


下図は、フィルタが画像上をスライドし **位置に依存しないパターン** を検出するイメージです。

<img src="../../assets/units/unit14_cnn_basics/images/diagram-workflow.svg" alt="図解：画像に CNN が向いている理由" class="unit-diagram" />

## 2. 実装例 (Implementation Example)

ここでは、PyTorchを使って、CNNの超基本的なネットワークモデルを構築してみましょう。手書き数字認識（MNIST）などでよく使われるシンプルな構造を作ります。なお、実際の画像データセットを読み込んで学習・評価まで行う一連の流れは [Unit 16（Capstone）](../unit16_deep_learning_capstone/index.md) で実践しますので、ここではネットワーク構造の理解に集中しましょう。

まずは準備です。今回は「1チャンネル（白黒画像）」で「28×28ピクセル」のダミー画像データを想定します。

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# ダミーの画像データ (バッチサイズ:10, チャンネル数:1(白黒), 縦:28, 横:28)
# PyTorchの画像データは必ず [バッチ数, チャンネル数, 縦, 横] の順番になります！
dummy_images = torch.randn(10, 1, 28, 28)
```

次に、虫眼鏡（CNN）の設計図を書きます。

```python
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # 1. 最初の虫眼鏡（畳み込み層）
        # 入力1チャンネル(白黒) -> 出力16種類の虫眼鏡を使う -> 3x3のサイズの虫眼鏡
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        
        # 2. 次の虫眼鏡
        # 入力16種類 -> 出力32種類のさらに複雑な特徴を探す虫眼鏡
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        
        # 3. プーリング層（要約ツール）
        # 2x2の範囲の中で一番強い特徴だけを残す（画像サイズが縦横半分になります）
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # 4. 全結合層（推理パート）
        # 画像が2回半分(28->14->7)になるので、最終的な特徴の数は 32(種類) * 7(縦) * 7(横) = 1568個
        self.fc1 = nn.Linear(32 * 7 * 7, 128) # 1568個の証拠から128個のまとめを作る
        self.fc2 = nn.Linear(128, 10)         # 最後に「0〜9の数字」の10クラスに分類する

    def forward(self, x):
        # --- 特徴抽出パート (虫眼鏡 & 要約) ---
        # 1回目の虫眼鏡 -> 活性化(ReLU) -> 要約(半分に) [28x28 -> 14x14]
        x = self.pool(F.relu(self.conv1(x)))
        
        # 2回目の虫眼鏡 -> 活性化(ReLU) -> 要約(半分に) [14x14 -> 7x7]
        x = self.pool(F.relu(self.conv2(x)))
        
        # --- 推理パート (全結合) ---
        # 画像(縦横の箱)の状態から、1列の長いリストに引き延ばす！ (Flatten)
        x = x.view(-1, 32 * 7 * 7)
        
        # リストをもとに最終推理
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = SimpleCNN()
```

最後に、作成したモデルにダミー画像を通してみて、きちんと推論ができるか（エラーが出ないか）確認してみましょう。

```python
# ダミー画像をモデルに推論させる
output = model(dummy_images)

# 出力の形を確認
print("出力のサイズ:", output.shape)
# 出力結果: torch.Size([10, 10])
# (10枚の画像それぞれに対して、0〜9の10種類の確率スコアが出力されている)
```

**解説:**
CNNの実装で初心者が一番つまづくのが **「全結合層（Linear）に渡すときの数の計算」** です。
- 最初の画像は `28x28`。
- `MaxPool2d(2)` を1回通ると、縦横が半分になるので `14x14`。
- もう1回通ると `7x7`。
- 最後にチャンネル数が `32` に増えているので、全部の証拠の数は `32(種類) × 7(縦) × 7(横) = 1568個` になります。
これを `x.view(-1, 1568)` で1列にガラガラと崩して並べ替えてから全結合層に渡すのが、CNNのお決まりのテクニックです。

構造の確認ができたら、実際に学習ループを回してみましょう。Unit 11〜12 で学んだ「お決まりの5ステップ」は、CNNでも全く同じです。

```python
import torch.optim as optim

# ダミーの正解ラベル（10枚の画像それぞれに 0〜9 のどれかを割り当て）
torch.manual_seed(42)
dummy_labels = torch.randint(0, 10, (10,))

# 分類問題なので CrossEntropyLoss、Optimizer は Adam
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 学習ループ（数エポックだけ回して Loss が下がることを確認）
model.train()
for epoch in range(5):
    optimizer.zero_grad()
    outputs = model(dummy_images)          # ① 予測（順伝播）
    loss = criterion(outputs, dummy_labels) # ② 誤差の計算
    loss.backward()                         # ③ 誤差逆伝播
    optimizer.step()                        # ④ 重みの更新
    print(f"Epoch {epoch+1} | Loss: {loss.item():.4f}")
```

今回はランダムなダミーデータなので精度に意味はありませんが、Loss が徐々に下がっていけば「CNNでも学習ループがきちんと動いている」ことが確認できます。

## 3. 実践 (Practice)

CNNの構造に慣れるため、少しだけ形の違うネットワークを作ってみましょう！

**要件定義:**
- 今度はカラー画像を想定します。ダミーのカラー画像 `color_images` を `(バッチサイズ:5, チャンネル数:3, 縦:32, 横:32)` のサイズで作成してください。
- 以下の構造を持つ `ColorCNN` クラスを作成してください。
  - **畳み込み層1** : 入力チャンネル3 → 出力チャンネル8, カーネルサイズ3, パディング1
  - **プーリング層** : サイズ2のMaxPool
  - **畳み込み層2** : 入力チャンネル8 → 出力チャンネル16, カーネルサイズ3, パディング1
  - （ここでもう一度上記のプーリング層を通します）
  - **全結合層1** : （計算を頑張ってみましょう！32サイズが2回半分になるので…？）→ 出力64
  - **全結合層2** : 入力64 → 出力5（今回は5種類の動物に分類するとします）
- forward関数の中で `relu` を通しながらデータを流し、最後にダミー画像を入れて出力サイズが `[5, 5]` になるか確認してください。

**ヒント:**
32×32の画像が2回半分（16×16 → 8×8）になります。最後のチャンネル数は16なので、全結合層に渡すサイズは `16 * 8 * 8` になります。

## 4. 答え合わせ (Answer Key)

<details>
<summary>解答例を見る（クリックで展開）</summary>

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# 1. カラー画像のダミーデータ作成
# (バッチ数:5, チャンネル:3(RGB), 縦:32, 横:32)
color_images = torch.randn(5, 3, 32, 32)

# 2. モデルの定義
class ColorCNN(nn.Module):
    def __init__(self):
        super(ColorCNN, self).__init__()
        # 最初の虫眼鏡 (カラー画像なので入力チャンネルは3)
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=8, kernel_size=3, padding=1)
        # 次の虫眼鏡
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, padding=1)
        
        # プーリング層
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # 全結合層
        # 画像サイズ: 32 -> (pool) -> 16 -> (pool) -> 8
        # チャンネル数: 16
        # 引き延ばした後のサイズ: 16 * 8 * 8 = 1024
        self.fc1 = nn.Linear(16 * 8 * 8, 64)
        self.fc2 = nn.Linear(64, 5) # 5クラス分類

    def forward(self, x):
        # 畳み込み 1回目
        x = self.pool(F.relu(self.conv1(x)))
        # 畳み込み 2回目
        x = self.pool(F.relu(self.conv2(x)))
        
        # 1列に引き延ばす (Flatten)
        x = x.view(-1, 16 * 8 * 8)
        
        # 推理パート
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = ColorCNN()

# 3. テスト実行
output = model(color_images)
print("出力のサイズ:", output.shape)
# 期待される出力: torch.Size([5, 5]) 
# (5枚の画像それぞれに5クラスのスコアが出力されている)
```

### 解説

この課題の最大のポイントは、 **全結合層に渡す Flatten サイズの計算** です。計算の手順を追いかけてみましょう。まず入力画像は `32×32` です。畳み込み層は `padding=1` かつ `kernel_size=3` なので画像サイズは変わりません（ここが縮まないのがポイントです）。サイズを変えるのは `MaxPool2d(2)` で、1回通すごとに縦横が半分になります。つまり `32×32 → (1回目のプール) → 16×16 → (2回目のプール) → 8×8` と縮んでいきます。一方、チャンネル数（虫眼鏡の種類）は `3 → 8 → 16` と増えていくので、最終的な特徴マップは「16チャネル × 8×8」となり、Flatten 後のサイズは `16 × 8 × 8 = 1024` 個になります。この「プーリングで縦横が何回半分になるか」と「最後のチャンネル数」を掛け算する、というのが Flatten サイズ計算の公式です。ここを間違えると `nn.Linear` の入力サイズが合わずエラーになるので、CNNを設計するときは必ず紙の上でサイズの変化を追いかける習慣をつけましょう。

</details>
