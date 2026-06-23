# Unit 10: ゼロから作るニューラルネットワーク

> [!TIP]
> **Google Colab で学習を進める方へ**
> ディープラーニング編（Unit 10〜16）では、計算を高速化するために **GPU の有効化** をおすすめします。設定手順は [Appendix (学習環境とキーの準備)](../appendix/index.md#🚀-1-google-colaboratory-での学習の進め方) を最初にご覧ください。




## 1. ニューラルネットワークの理解

<img src="../../assets/units/unit10_nn_from_scratch/images/concept.png" width="400" alt="コンセプト図解">

ニューラルネットワークを理解するために、**「会社での稟議（りんぎ）の決裁プロセス」**に例えてみましょう。

社長（最終的な答え）が「このプロジェクトにGOを出すか？」を決めるために、平社員、係長、部長といった複数の階層（層）を通って情報が伝わります。

1. **入力層（平社員）**: 外部からデータ（プロジェクトの資料）を受け取ります。
2. **隠れ層（係長・部長）**: データを色々な角度から評価し、「これは重要そうだな（重み：ウェイト）」、「いや、うちの部署には関係ない（バイアス）」と判断して、情報を次の階層へ伝えます。この階層がたくさんある（深い）ものを**ディープラーニング**と呼びます。
3. **出力層（社長）**: 最終的に「承認」か「却下」か（犬か猫か、など）の決断を下します。

| ネットワークの用語 | 会社での例え | 役割 |
|---|---|---|
| **ノード（ニューロン）** | 社員一人ひとり | 情報を受け取り、判断して次に渡す |
| **重み (Weight)** | 意見の重要度 | どの情報（誰の意見）を重視するか |
| **バイアス (Bias)** | 部署の基本方針 | そもそも賛成しやすいか、反対しやすいかという偏り |
| **活性化関数 (Activation)** | はんこを押す基準 | 情報が一定の基準を超えたら次に伝えるフィルター |

このUnitでは、フレームワークに頼らず、この「情報の伝達（順伝播）」と「間違いの修正（誤差逆伝播）」をPythonの計算（NumPy）だけで表現してみましょう！

### 💡 具体的なビジネスユースケース

- **顧客の離反予測**: ユーザーの行動履歴や契約状況を入力として、解約する確率を予測し、引き留め施策の対象者を抽出する。
- **異常検知システム**: センサーから得られる複数の温度や振動データを入力し、正常時とは異なるパターンの「異常（故障の予兆）」を検知する。
- **融資の審査AI**: 顧客の年収、借入残高、勤続年数などのデータをもとに、ローンの審査基準を満たすかどうか（返済能力があるか）を自動判定する。

## 2. 実装例 (Implementation Example)

ここでは、最もシンプルな「1つの隠れ層を持つニューラルネットワーク」を、ゼロから実装してみます。XOR（排他的論理和）という少し複雑なパターンのデータを学習させてみましょう。

まずは必要なライブラリの読み込みと、データの準備です。

```python
import numpy as np

# 入力データ (4つのパターン)
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

# 正解ラベル (XORパターンの答え)
y = np.array([
    [0],
    [1],
    [1],
    [0]
])
```

上記のコードは、2つの入力（例えば「雨が降っているか」「傘を持っているか」のような2択）に対して、答え（0か1か）を持った簡単なデータセットを用意しています。

次に、ネットワークの初期設定を行います。重みとバイアスをランダムに準備します。

```python
# 乱数のシードを固定（毎回同じ結果にするため）
np.random.seed(42)

# ネットワークの形を決める
input_size = 2   # 入力層の人数（2人）
hidden_size = 3  # 隠れ層の人数（3人）
output_size = 1  # 出力層の人数（社長1人）

# 重み（W）とバイアス（b）の初期化
# 係長への重みと基本方針
W1 = np.random.randn(input_size, hidden_size) 
b1 = np.zeros((1, hidden_size))

# 社長への重みと基本方針
W2 = np.random.randn(hidden_size, output_size)
b2 = np.zeros((1, output_size))
```

ここでは、入力層（2個）→隠れ層（3個）→出力層（1個）という構造を作っています。`np.random.randn`は「最初は適当に決める」という作業をしています。学習を通じてこの適当な値を正しく直していくのがAIの学習です。

いよいよ学習のメインループです。

```python
# シグモイド関数（活性化関数：0〜1の間に数値を押し込めるフィルター）
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# シグモイド関数の微分（間違いを修正するときに使います）
def sigmoid_derivative(x):
    return x * (1 - x)

# 学習率（1回の反省でどれくらい思い切り直すか）
learning_rate = 0.5
epochs = 5000 # 学習を繰り返す回数

for epoch in range(epochs):
    # -------------------------
    # 1. 順伝播 (Forward Propagation) - 稟議を上に回す
    # -------------------------
    # 隠れ層の計算
    z1 = np.dot(X, W1) + b1       # 入力 × 重み + バイアス
    a1 = sigmoid(z1)              # フィルターを通す
    
    # 出力層の計算
    z2 = np.dot(a1, W2) + b2      # 隠れ層の出力 × 重み + バイアス
    output = sigmoid(z2)          # 社長の最終判断 (0〜1の確率)
    
    # -------------------------
    # 2. 誤差の計算 - 社長の判断と正解のズレを確認
    # -------------------------
    error = y - output
    
    # -------------------------
    # 3. 誤差逆伝播 (Backpropagation) - 間違いの原因を探って下に伝える
    # -------------------------
    # 出力層の反省点
    d_output = error * sigmoid_derivative(output)
    
    # 隠れ層の反省点
    error_hidden_layer = d_output.dot(W2.T)
    d_hidden_layer = error_hidden_layer * sigmoid_derivative(a1)
    
    # -------------------------
    # 4. 重みとバイアスの更新 - 反省を活かしてルールを修正する
    # -------------------------
    W2 += a1.T.dot(d_output) * learning_rate
    b2 += np.sum(d_output, axis=0, keepdims=True) * learning_rate
    W1 += X.T.dot(d_hidden_layer) * learning_rate
    b1 += np.sum(d_hidden_layer, axis=0, keepdims=True) * learning_rate

print("学習後のAIの予測結果:")
print(np.round(output, 3))
```

**解説:**
ループの中で、大きく分けて以下の4ステップを繰り返しています。
1. **順伝播**: 入力データから、現在の重みを使って予測値を出します（稟議が上がっていく）。
2. **誤差の計算**: 予測値と正解がどれくらいズレているか（間違えたか）を計算します。
3. **誤差逆伝播（バックプロパゲーション）**: 出口（出力層）から入り口（隠れ層）に向かって、「誰のせいで間違えたのか（誰の重みを直せばいいか）」を計算して遡ります。
4. **更新**: 計算した「直すべき量」をもとに、重み（W）とバイアス（b）を微調整します。

これを5000回（エポック）繰り返すことで、AIは徐々に正解を導き出せる賢いネットワークへと成長します。

## 3. 実践 (Practice)

さあ、あなたの番です！
先ほどのXORデータセットではなく、簡単な「OR回路（どちらかが1なら正解は1）」のデータセットを使って、ゼロからニューラルネットワークの学習ループを実装してみてください。

**要件定義:**
- 入力データ `X` と正解ラベル `y` を以下のように設定してください。
  - `X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])`
  - `y = np.array([[0], [1], [1], [1]])`
- 入力層は2、隠れ層は2、出力層は1のネットワークを構築してください。
- 活性化関数にはシグモイド関数を使用します。
- エポック数は3000回とし、学習後に予測値を出力して正解（0, 1, 1, 1 に近い値）になっているか確認してください。

**ヒント:**
ベースの実装例のコードをコピーして、データセットと隠れ層のサイズ（`hidden_size`）を変更するだけで動作するはずです！

## 4. 答え合わせ (Answer Key)

<details>
<summary>解答例を見る（クリックで展開）</summary>

```python
import numpy as np

# データの準備 (OR回路)
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
y = np.array([
    [0],
    [1],
    [1],
    [1]
])

# 活性化関数とその微分
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# ネットワークの構築
np.random.seed(42)
input_size = 2
hidden_size = 2  # 隠れ層を2人に変更
output_size = 1

W1 = np.random.randn(input_size, hidden_size)
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size)
b2 = np.zeros((1, output_size))

# 学習ループ
learning_rate = 0.5
epochs = 3000

for epoch in range(epochs):
    # 1. 順伝播
    z1 = np.dot(X, W1) + b1
    a1 = sigmoid(z1)
    z2 = np.dot(a1, W2) + b2
    output = sigmoid(z2)
    
    # 2. 誤差計算
    error = y - output
    
    # 3. 誤差逆伝播
    d_output = error * sigmoid_derivative(output)
    error_hidden_layer = d_output.dot(W2.T)
    d_hidden_layer = error_hidden_layer * sigmoid_derivative(a1)
    
    # 4. 更新
    W2 += a1.T.dot(d_output) * learning_rate
    b2 += np.sum(d_output, axis=0, keepdims=True) * learning_rate
    W1 += X.T.dot(d_hidden_layer) * learning_rate
    b1 += np.sum(d_hidden_layer, axis=0, keepdims=True) * learning_rate

print("学習後のAIの予測結果 (0, 1, 1, 1 に近ければ成功):")
print(np.round(output, 3))
```

</details>
