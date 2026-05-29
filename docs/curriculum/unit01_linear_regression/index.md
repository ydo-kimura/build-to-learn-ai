# Unit 1: 線形回帰と正則化回帰

<p class="unit-hero">
  <img src="../../assets/units/unit01_linear_regression/images/hero.png" alt="ヒーロー画像：部屋の広さから家賃を予測する線形回帰" />
</p>

## 1. 線形回帰と正則化の理解

### 線形回帰とは？ 〜「家賃の予測」で考える〜

線形回帰を日常に例えるなら、 **「過去のデータから、1つの真っ直ぐな定規を使って未来を予測する」** ようなものです。

例えば、「部屋の広さ（平方メートル）」から「家賃（万円）」を予測したいとします。
データをグラフにプロットしてみると、だいたい広くなればなるほど家賃が高くなる傾向が見えます。このデータの中央を貫くように「ピッタリ合う1本の直線を引く」のが線形回帰です。

下図は、部屋の広さと家賃の散布図に、データの中央を貫くように最適な回帰直線を当てはめたイメージです。

<img src="../../assets/units/unit01_linear_regression/images/diagram-linear-regression.svg" alt="図解：散布図と最適な回帰直線：部屋の広さと家賃" class="unit-diagram" />

| 部屋の広さ（原因：特徴量） | 家賃（結果：目的変数） |
| :------------------------- | :--------------------- |
| 20㎡                       | 6万円                  |
| 30㎡                       | 8万円                  |
| 40㎡                       | 10万円                 |

この直線を数式で表すと：
**家賃 = (係数 × 部屋の広さ) + 基本料金（切片）**
となります。アルゴリズムの仕事は、過去のデータに最もよく当てはまる「係数」と「基本料金」を見つけ出すことです。

### 正則化（Regularization）とは？ 〜「こだわりすぎ」を防ぐブレーキ〜

しかし、家賃は広さだけでなく「駅からの距離」「築年数」「近くにコンビニがあるか」など、たくさんの要因で決まります。
データが複雑になると、機械学習モデルは「過去のデータにピッタリ合わせようと頑張りすぎる」ことがあります。これを **過学習（オーバーフィッティング）** と呼びます。

例えるなら、 **「過去問を丸暗記しすぎて、本番の応用問題が全く解けない受験生」** のような状態です。

下図は、過去のデータに合わせすぎて波打ってしまった過学習の曲線と、正則化によってシンプルに保たれた直線を比較したものです。

<img src="../../assets/units/unit01_linear_regression/images/diagram-regularization.svg" alt="図解：過学習の波打つ曲線 vs 正則化されたシンプルな直線" class="unit-diagram" />

これを防ぐための「ブレーキ」が **正則化** です。正則化には主に2つの種類があります：

1. **Ridge（リッジ）回帰** ：全体的に係数を小さく抑え、「極端な思い込み」を防ぐ。
2. **Lasso（ラッソ）回帰** ：重要でない要因の係数を「完全にゼロ」にして無視する。断捨離が得意。

なお、Lasso 回帰は章末の「3. 実践 (Practice)」で実際に手を動かして試します。

### 💡 具体的なビジネスユースケース

- **不動産の価格査定AI** ：物件の広さ、築年数、駅からの距離などの特徴量から、適正な家賃や売却価格を予測する。
- **小売店の売上予測** ：過去の売上実績、気温、休日の有無などのデータから、翌日の店舗ごとの売上高を予測し、発注量を最適化する。
- **広告費のROI分析（マーケティング・ミックス・モデリング）** ：テレビCMやWeb広告などの各媒体への投資額が、最終的な売上にどれだけ貢献しているかを算出し、予算配分を最適化する。

---

## 2. 実装例 (Implementation Example)

ここでは、Pythonと機械学習ライブラリ`scikit-learn`を使って、住宅価格を予測する線形回帰と Ridge 回帰を実装してみましょう。

下図は、データを学習用とテスト用に分割してから、学習・予測・評価へと進む機械学習の基本ワークフローです。

<img src="../../assets/units/unit01_linear_regression/images/diagram-train-test-split.svg" alt="図解：データ分割→学習→予測・評価のワークフロー" class="unit-diagram" />

まずは必要なライブラリを読み込み、データを準備します。※ここで使うのはランダムに生成したダミーデータで、本文の例え話（20㎡ → 6万円）とは数値のスケールが異なる点にご注意ください。

```python
# 必要なツールのインポート
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error

# 1. データの準備 (今回はダミーデータを作成します)
# np.random.seed(42) で毎回同じランダムな数値が出るように固定します
np.random.seed(42)

# X: 部屋の広さ（20〜80平米のデータを100件）
X = np.random.randint(20, 80, size=(100, 1))

# y: 家賃（広さ × 0.2 + 誤差を少し加える）
y = X * 0.2 + np.random.randn(100, 1) * 2

# 2. データを「学習用」と「テスト用」に分割
# 全データのうち、80%を学習（過去問）に、20%をテスト（本番試験）に使います
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

**【コードの解説】**
ここでは、部屋の広さから家賃を予測するための「模擬データ」を作りました。モデルがズルをしないように、`train_test_split`という機能を使って、学習に使うデータと後で答え合わせをするテスト用のデータに分けています。

次に、実際にモデルに学習させて予測を行います。

```python
# 3. モデルの準備と学習
# 普通の線形回帰モデルを作成
model_lr = LinearRegression()

# 学習データ（X_train, y_train）を使って、最適な直線を引く（学習）
model_lr.fit(X_train, y_train)

# 4. テストデータで予測
y_pred_lr = model_lr.predict(X_test)

# 5. 答え合わせ（精度評価）
# MSE (平均二乗誤差): 予測と実際の値がどれくらいズレているかを計算
mse_lr = mean_squared_error(y_test, y_pred_lr)
print(f"通常の線形回帰のMSE: {mse_lr:.2f}")
```

**【コードの解説】**
`LinearRegression()` でモデルを作成し、`.fit()` を呼ぶだけで、AIが最適な直線を計算してくれます。これが機械学習の「学習フェーズ」です。その後、`.predict()` を使って未知のデータ（テストデータ）の家賃を予測し、実際の正解とどれくらいズレているか（MSE）を計算しました。

同様に、正則化（Ridge）を使ったバージョンも書いてみましょう。

```python
# 6. 正則化モデル (Ridge) の準備と学習
# alpha はブレーキの強さです。大きいほどブレーキが強くかかります
model_ridge = Ridge(alpha=1.0)
model_ridge.fit(X_train, y_train)

# テストデータで予測
y_pred_ridge = model_ridge.predict(X_test)

# 答え合わせ（精度評価）
mse_ridge = mean_squared_error(y_test, y_pred_ridge)
print(f"Ridge回帰のMSE: {mse_ridge:.2f}")
```

このシンプルなデータでは結果はほぼ同じになりますが、特徴量（列）が100個や1000個もあるような複雑なデータになると、Ridge回帰の「ブレーキ」が効果を発揮し、精度が良くなります。

---

## 3. 実践 (Practice)

さて、次はあなたの番です！以下の要件に従って、自分自身でモデルを構築してみましょう。

**【課題の要件】**
別のデータセット「糖尿病の進行度予測（Diabetes dataset）」を使います。これは、年齢やBMI、血圧などの複数の数値（特徴量）から、1年後の糖尿病の進行度（目的変数）を予測するタスクです。

1. `sklearn.datasets` から `load_diabetes` を使ってデータを読み込んでください。
2. データを学習用（80%）とテスト用（20%）に分割してください。
3. 今回は **Lasso回帰（Lasso）** モデルを作成して学習させてください。（`alpha=0.1` とします）
4. テストデータに対して予測を行い、MSE（平均二乗誤差）を表示してください。

**【ヒント】**

- `from sklearn.linear_model import Lasso` を追加でインポートする必要があります。
- データの読み込み方は `from sklearn.datasets import load_diabetes` とし、`data = load_diabetes()` の後に `X = data.data`、`y = data.target` とします。

---

## 4. 答え合わせ (Answer Key)

自分でコードを書いてから、以下の答えを開いて確認してみましょう。

<details>
<summary>解答例を見る（クリックで展開）</summary>

```python
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error

# 1. データの読み込み
diabetes = load_diabetes()
X = diabetes.data
y = diabetes.target

# 2. データの分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Lasso回帰モデルの作成と学習
# alpha=0.1 を指定して、Lasso回帰モデルを作ります
model_lasso = Lasso(alpha=0.1)
model_lasso.fit(X_train, y_train)

# 4. 予測と評価
y_pred = model_lasso.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print(f"Lasso回帰のMSE: {mse:.2f}")

# (おまけ) Lasso回帰の特徴である「使われなかった特徴量」を確認してみましょう
print(f"ゼロになった係数の数: {np.sum(model_lasso.coef_ == 0)} 個")
```

**【解答コードの解説】**
Lasso回帰の最大の特徴は、 **「結果に関係ない特徴量の係数をキッチリ 0 にしてくれる」** ことです。これによって、どのデータが本当に予測に重要なのかが人間にも分かりやすくなる（解釈性が上がる）というメリットがあります！
</details>
