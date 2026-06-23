# Unit 10: Neural Networks from Scratch

> [!TIP]
> **Using Google Colab**
> For the deep learning units (Units 10–16), we recommend **enabling a GPU** for faster training. See [Appendix (Learning environment and API keys)](../appendix/index.md#🚀-1-learning-with-google-colaboratory) for setup steps.




## 1. Understanding Neural Networks

<img src="../../../assets/units/unit10_nn_from_scratch/images/concept.png" width="400" alt="Concept diagram">

To understand neural networks, picture **a company's approval workflow**.

The CEO (final answer) decides "Go or no-go on this project?" Information flows through layers — staff, team leads, directors.

1. **Input layer (staff)**: Receives external data (project documents).
2. **Hidden layers (team leads, directors)**: Evaluate from many angles — "This looks important (weight)," "Not relevant to our team (bias)" — and pass signals upward. Many hidden layers = **deep learning**.
3. **Output layer (CEO)**: Final decision — approve or reject (dog or cat, etc.).

| Network term | Company analogy | Role |
|---|---|---|
| **Node (neuron)** | One employee | Receives input, decides, passes forward |
| **Weight** | Importance of an opinion | Which input to trust |
| **Bias** | Team's default stance | Lean toward yes or no |
| **Activation function** | Stamp threshold | Pass signal only if it clears a bar |

In this unit we'll implement **forward propagation** and **backpropagation** using only **NumPy** — no deep learning framework!

### 💡 Real-World Business Use Cases

- **Churn prediction**: Predict cancellation probability from usage and contract data to target retention offers.
- **Anomaly detection**: Flag unusual sensor patterns (temperature, vibration) that may indicate failure.
- **Loan underwriting**: Auto-assess repayment ability from income, debt, and tenure.

## 2. Implementation Example

We build the simplest network — **one hidden layer** — from scratch and train it on **XOR**, a slightly nonlinear pattern.

First, load libraries and prepare data.

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

This sets up four input patterns (e.g., "Is it raining?" and "Do you have an umbrella?") with binary labels.

Next, initialize the network — random weights and biases.

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

Structure: input (2) → hidden (3) → output (1). `np.random.randn` starts with random values; training adjusts them.

Now the main training loop.

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

**Walkthrough**
Each epoch repeats four steps:
1. **Forward propagation**: Compute predictions from inputs and current weights (memo goes up the chain).
2. **Error calculation**: Measure gap between prediction and label.
3. **Backpropagation**: Trace blame from output back to hidden layers — who caused the mistake?
4. **Update**: Nudge weights (W) and biases (b) by the computed corrections.

Repeat for 5000 epochs and the network learns XOR.

## 3. Practice

Your turn!
Use a simple **OR gate** dataset (if either input is 1, output is 1) and implement the training loop from scratch.

**Requirements**
- Set input `X` and labels `y`:
  - `X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])`
  - `y = np.array([[0], [1], [1], [1]])`
- Build a network: 2 inputs, **2 hidden** units, 1 output.
- Use sigmoid activation.
- Train for **3000 epochs** and print predictions — they should be close to 0, 1, 1, 1.

**Hint**
Copy the example code and change the dataset and `hidden_size` — that's enough!

## 4. Answer Key

<details>
<summary>View sample solution (click to expand)</summary>

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
