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
2. **Lasso（ラッソ）回帰** ：一部の係数を「完全にゼロ」にし、モデルが予測に使う特徴量を絞る。ただし、係数がゼロでも、その特徴量が現実世界で不要だと証明されたわけではない。

章末の「3. 実践 (Practice)」では、通常の線形回帰、Ridge 回帰、Lasso 回帰を同じデータで比較します。

### 💡 具体的なビジネスユースケース

- **不動産の価格査定AI** ：物件の広さ、築年数、駅からの距離などの特徴量から、適正な家賃や売却価格を予測する。
- **小売店の売上予測** ：過去の売上実績、気温、休日の有無などのデータから、翌日の店舗ごとの売上高を予測し、発注量を最適化する。
- **広告費のROI分析（マーケティング・ミックス・モデリング）** ：テレビCMやWeb広告などの各媒体への投資額が、最終的な売上にどれだけ貢献しているかを算出し、予算配分を最適化する。


## 2. 実装例 (Implementation Example)

ここでは、Pythonと機械学習ライブラリ`scikit-learn`を使って、住宅価格を予測する線形回帰と Ridge 回帰を実装してみましょう。

下図は、データを学習用とテスト用に分割してから、学習・予測・評価へと進む機械学習の基本ワークフローです。

<img src="../../assets/units/unit01_linear_regression/images/diagram-train-test-split.svg" alt="図解：データ分割→学習→予測・評価のワークフロー" class="unit-diagram" />

まずは必要なライブラリを読み込み、データを準備します。ここでは Ridge 回帰の効果を観察しやすくするため、30件の物件に対して、同じ「本当の広さ」をもとに作られた10個のよく似た特徴量を用意します。このように特徴量同士が強く相関する状態を **多重共線性** と呼び、通常の線形回帰では係数が不安定になりやすくなります。

```python
# 必要なツールのインポート
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error

# 1. データの準備（毎回同じ結果になるよう乱数を固定）
rng = np.random.default_rng(42)

# 30件の物件について、本当の広さを20〜80㎡の範囲で作る
true_size = rng.uniform(20, 80, size=(30, 1))

# X: 本当の広さに小さな測定誤差を加えた、よく似た10個の特徴量
# 10列が同じ情報を多く含むため、特徴量同士が強く相関する
X = true_size + rng.normal(0, 0.5, size=(30, 10))

# y: 家賃（万円）。本当の広さ × 0.2 に、現実のばらつきを加える
y = true_size.ravel() * 0.2 + rng.normal(0, 3, size=30)
```

### 用意したデータセットを確認する

モデルへ渡す前に、作った `X` と `y` が意図したデータになっているかを確認します。`X` の1行は1件の物件、10列は同じ物件の「本当の広さ」をもとにした10個のよく似た特徴量、`y` の1要素はその物件の家賃です。

```python
print(f"Xの形: {X.shape}")
print(f"yの形: {y.shape}")

# 最初の3件について、データを横に並べて意味を確認する
for index in range(3):
    print(f"\n物件 {index + 1}")
    print(f"  本当の広さ: {true_size[index, 0]:.2f}㎡")
    print(f"  10個の特徴量: {np.round(X[index], 2)}")
    print(f"  家賃: {y[index]:.2f}万円")

# 例として、1列目と2列目がどの程度似ているかを相関係数で確認する
correlation = np.corrcoef(X[:, 0], X[:, 1])[0, 1]
print(f"\n1列目と2列目の相関係数: {correlation:.3f}")
```

実行すると、`X` は30行・10列、`y` は30件になります。例えば最初の物件の本当の広さは約 `66.44㎡` で、10個の特徴量はいずれも約 `66〜68` の近い値です。1列目と2列目の相関係数は約 `0.999` となり、2つの列がほぼ同じ情報を持つことも確認できます。

データの意味と形を確認できたら、学習用とテスト用に分割します。

```python
# 2. 全データの70%を学習用、30%をテスト用に分ける
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
```

**【コードの解説】**
これは Ridge 回帰の「ブレーキ」が役立つ場面を再現するための模擬データです。物件数は30件と少ない一方で、確認したとおり似た特徴量が10個あります。さらに家賃にはノイズも含まれるため、通常の線形回帰は学習データの偶然のばらつきまで拾いやすくなります。`train_test_split` を使い、学習に使わないテストデータで予測性能を比べます。

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
mse_lr = mean_squared_error(y_test, y_pred_lr)
print(f"通常の線形回帰のMSE: {mse_lr:.2f}")
```

**【コードの解説】**
`LinearRegression()` でモデルを作成し、`.fit()` で学習します。その後、`.predict()` を使って未知のテストデータの家賃を予測し、MSE を計算・表示します。固定した条件では `通常の線形回帰のMSE: 20.34` と表示されます。まずこの値を通常の線形回帰の結果として確認し、次の Ridge 回帰との比較基準にします。

同様に、正則化（Ridge）を使ったバージョンも書いてみましょう。

```python
# 6. 正則化モデル (Ridge) の準備と学習
# alpha はブレーキの強さです。大きいほどブレーキが強くかかります
model_ridge = Ridge(alpha=100.0)
model_ridge.fit(X_train, y_train)

# テストデータで予測
y_pred_ridge = model_ridge.predict(X_test)

# 答え合わせ（精度評価）
mse_ridge = mean_squared_error(y_test, y_pred_ridge)
improvement_rate = (mse_lr - mse_ridge) / mse_lr * 100

print(f"通常の線形回帰のMSE: {mse_lr:.2f}")
print(f"Ridge回帰のMSE: {mse_ridge:.2f}")
print(f"MSEの改善率: {improvement_rate:.1f}%")
```

固定した条件で実行すると、通常の線形回帰の MSE は `20.34`、Ridge 回帰は `10.52` となり、Ridge 回帰の MSE は `48.3%` 小さくなります。この例では、互いによく似た10個の特徴量に対して係数が極端にならないよう Ridge の「ブレーキ」が働き、未知のテストデータへの予測が改善しました。

### MSE の値はどう読む？

MSE（Mean Squared Error、平均二乗誤差）は、各データについて **「予測値 − 正解値」を二乗し、その平均を取った値** です。

- MSE は必ず `0` 以上になります。`0` なら、すべての予測が正解と完全に一致しています。
- 同じ目的変数・単位・テストデータで比べる場合は、MSE が小さいモデルほど予測誤差が小さいと判断できます。ここでは `10.52 < 20.34` なので Ridge 回帰の方が良い結果です。
- 固定された上限はありません。予測が大きく外れるほど値は大きくなり、差を二乗するため外れ値の影響も強く受けます。
- 今回の目的変数は家賃の「万円」ですが、MSE の単位は二乗された「万円²」です。そのため、MSE `20.34` は「平均で20.34万円ずれた」という意味ではありません。元の万円単位で感覚をつかむには、MSE の平方根である RMSE を使うと、通常の線形回帰は約 `4.51` 万円、Ridge 回帰は約 `3.24` 万円です。
- 目的変数の単位や値の大きさ、テストデータの分け方が違う MSE 同士は、数値だけで単純比較できません。

なお、Ridge 回帰が常に通常の線形回帰より良くなるわけではありません。効果はデータの性質と `alpha` によって変わります。この例は、少ないデータに強く相関する特徴量とノイズがある、Ridge 回帰が役立ちやすい条件を意図的に再現しています。


## 3. 実践 (Practice)

さて、次はあなたの番です。ここまでの実装例を写すのではなく、別の実データについて、データの意味を確認するところからモデルの比較と結果の解釈までを自分で行います。

### 使用するデータ

scikit-learn の Diabetes dataset は、442人の糖尿病患者について、調査開始時の10個の特徴量と、1年後の糖尿病進行度を表す数値を記録したデータです。

| 特徴量 | 内容                                     |
| :----- | :--------------------------------------- |
| `age`  | 年齢                                     |
| `sex`  | 性別                                     |
| `bmi`  | BMI（体格指数）                          |
| `bp`   | 平均血圧                                 |
| `s1`   | 総血清コレステロール                     |
| `s2`   | LDL（低密度リポタンパク質）              |
| `s3`   | HDL（高密度リポタンパク質）              |
| `s4`   | 総コレステロールと HDL の比              |
| `s5`   | 血清トリグリセリド値の対数と考えられる値 |
| `s6`   | 血糖値                                   |

これらの特徴量は、すでに平均を中心に尺度調整されています。したがって、表示される `age` や `bmi` の値は、年齢やBMIの元の単位そのものではありません。目的変数は、1年後の糖尿病進行度を表す定量的な指標です。

### Step 1：データセットを観察する

モデルを作る前に、何件のデータがあり、各列と目的変数が何を表しているかを確認します。ここを飛ばすと、後で係数や MSE が出ても、その数値が何についての結果なのかを説明できません。

`load_diabetes()` は、デフォルトでは配列そのものではなく、データや説明をまとめた `Bunch` を返します。`Bunch` は辞書に似た入れ物で、項目を `diabetes.data` のように取り出せます。このデータセットでは、特徴量が `data`、目的変数が `target` に NumPy 配列として入っています。返り値を決めつけず、まず実際の型と中身を確認しましょう。

1. `load_diabetes()` でデータを読み込み、結果を `diabetes` に代入してください。
2. `diabetes` の型と、格納されている項目の一覧を表示してください。さらに、`diabetes.data` と `diabetes.target` の型を表示してください。
3. `diabetes.data` を `X`、`diabetes.target` を `y` として取り出してください。
4. `X.shape`、`diabetes.feature_names`、特徴量の先頭1件、目的変数の最小値・最大値・平均値を表示してください。
5. 各特徴量と目的変数の相関係数を計算し、絶対値が大きい順に表示してください。
6. 出力と上の特徴量表を照らし合わせ、次を確認してください。
   - どのオブジェクトが `Bunch` で、どのオブジェクトが `ndarray` か。
   - 患者数と特徴量数はいくつか。
   - 目的変数はどの程度の範囲にあるか。
   - 目的変数と強い相関が見られる特徴量はどれか。

**【ヒント】**

- `load_diabetes()` は、次のようにインポートします。

  ```python
  from sklearn.datasets import load_diabetes
  ```

- 相関係数は `np.corrcoef(X[:, 列番号], y)[0, 1]` で計算できます。
- 相関は2変数が一緒に変化する傾向を表します。相関が強くても、その特徴量が病気の進行を引き起こすと証明されたわけではありません。

### Step 2：通常の線形回帰を実装する

まず正則化を使わない線形回帰を作り、後で比較する基準にします。

1. データを学習用（80%）とテスト用（20%）に分割してください。`test_size=0.2`、`random_state=42` を指定します。
2. `LinearRegression` を学習データで学習させ、テストデータを予測してください。
3. MSE を計算して表示してください。
4. テストデータの先頭5件について、実際の進行度、予測した進行度、その差を並べて表示してください。
5. 個々の予測のずれと、全テストデータをまとめた MSE の役割の違いを説明してください。

### Step 3：Ridge 回帰と Lasso 回帰を実装する

通常の線形回帰と同じ学習データ・テストデータを使い、正則化によって結果がどう変わるかを比較します。評価データが違うと MSE を公平に比較できないため、データは分割し直しません。

1. Ridge 回帰（`alpha=0.1`）と Lasso 回帰（`alpha=0.1`）を学習させてください。
2. 同じテストデータを予測し、通常の線形回帰を含む3モデルの MSE を並べて表示してください。
3. 10個の特徴量について、通常の線形回帰、Ridge、Lasso が学習した係数を並べて表示してください。

**【ヒント】**

- 学習後の係数は各モデルの `.coef_` で確認できます。
- `zip(diabetes.feature_names, model_lr.coef_, model_ridge.coef_, model_lasso.coef_)` を使うと、特徴量名と3モデルの係数を対応づけられます。

### Step 4：結果を解釈する

出力した数値を見て、次を自分の言葉で説明してください。

1. どのモデルの MSE が最も小さかったか。
2. Ridge の係数は、通常の線形回帰と比べてどう変わったか。
3. Lasso で係数がゼロになった特徴量はどれか。
4. 係数がゼロであることから、この学習条件について何が言えるか。
5. 係数がゼロであることだけでは、医学的に何を断定できないか。


## 4. 答え合わせ (Answer Key)

自分でコードを書いてから、以下の答えを開いて確認してみましょう。

<details>
<summary>解答例を見る（クリックで展開）</summary>

### Step 1：データセットを観察する

```python
import numpy as np
from sklearn.datasets import load_diabetes

# データの読み込み
diabetes = load_diabetes()

# 返り値と、その中にあるデータの型を確認
print(f"load_diabetes()の返り値の型: {type(diabetes).__name__}")
print(f"格納されている項目: {list(diabetes.keys())}")
print(f"dataの型: {type(diabetes.data).__name__}")
print(f"targetの型: {type(diabetes.target).__name__}")

# 特徴量と目的変数を取り出す
X = diabetes.data
y = diabetes.target

# 大きさと内容の確認
print(f"データの形: {X.shape}")
print(f"特徴量名: {diabetes.feature_names}")
print("先頭患者の特徴量:")
for name, value in zip(diabetes.feature_names, X[0]):
    print(f"  {name}: {value:.4f}")

print(f"目的変数の最小値: {y.min():.0f}")
print(f"目的変数の最大値: {y.max():.0f}")
print(f"目的変数の平均値: {y.mean():.2f}")

# 各特徴量と目的変数の相関を確認
correlations = []
for column_index, name in enumerate(diabetes.feature_names):
    correlation = np.corrcoef(X[:, column_index], y)[0, 1]
    correlations.append((name, correlation))

for name, correlation in sorted(correlations, key=lambda item: abs(item[1]), reverse=True):
    print(f"{name}: {correlation:.3f}")
```

`load_diabetes()` の返り値は `Bunch`、その中の `data` と `target` は `ndarray` と表示されます。データは442行・10列で、目的変数は `25` から `346`、平均は約 `152.13` です。このデータでは `bmi`、`s5`、`bp` などが目的変数と比較的強い相関を示します。ただし、これはデータ全体を1特徴量ずつ見た相関であり、因果関係やモデル内での重要度をそのまま表すものではありません。

### Step 2：通常の線形回帰を実装する

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# 学習用とテスト用に分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 通常の線形回帰を学習・予測
model_lr = LinearRegression()
model_lr.fit(X_train, y_train)
pred_lr = model_lr.predict(X_test)

mse_lr = mean_squared_error(y_test, pred_lr)
print(f"通常の線形回帰のMSE: {mse_lr:.2f}")

# 先頭5件の実測値と予測値を確認
print("実際の値 / 予測値 / 予測と実際の差")
for actual, predicted in zip(y_test[:5], pred_lr[:5]):
    print(f"{actual:6.1f} / {predicted:6.1f} / {predicted - actual:7.1f}")
```

通常の線形回帰の MSE は約 `2900.19` です。先頭5件だけでも、予測が実際の値より約79小さい例や約110大きい例があることを確認できます。個々の差は各患者の予測を確認する値で、MSE はテストデータ全体の差を二乗して平均した評価値です。

### Step 3：Ridge 回帰と Lasso 回帰を実装する

```python
from sklearn.linear_model import Ridge, Lasso

# 同じ学習データで正則化モデルを学習
model_ridge = Ridge(alpha=0.1)
model_lasso = Lasso(alpha=0.1)
model_ridge.fit(X_train, y_train)
model_lasso.fit(X_train, y_train)

# 同じテストデータを予測
pred_ridge = model_ridge.predict(X_test)
pred_lasso = model_lasso.predict(X_test)

mse_ridge = mean_squared_error(y_test, pred_ridge)
mse_lasso = mean_squared_error(y_test, pred_lasso)

print(f"通常の線形回帰のMSE: {mse_lr:.2f}")
print(f"Ridge回帰のMSE: {mse_ridge:.2f}")
print(f"Lasso回帰のMSE: {mse_lasso:.2f}")

# 特徴量名と3モデルの係数を対応づける
print("特徴量 / 通常の線形回帰 / Ridge / Lasso")
for name, coef_lr, coef_ridge, coef_lasso in zip(
    diabetes.feature_names,
    model_lr.coef_,
    model_ridge.coef_,
    model_lasso.coef_,
):
    print(f"{name:>3} / {coef_lr:8.2f} / {coef_ridge:8.2f} / {coef_lasso:8.2f}")
```

**【結果の確認方法】**

コードの書き方や変数名が解答例と異なっていても、指定した条件で次の結果になれば正しく実装できています。

- 通常の線形回帰の MSE は約 `2900.19`、Ridge 回帰は約 `2856.49`、Lasso 回帰は約 `2798.19` になる。
- この条件では Lasso 回帰の MSE が3モデルの中で最も小さい。
- Lasso 回帰では `age`、`s2`、`s4` の係数がゼロになる。

ライブラリのバージョンによって末尾の数値がわずかに異なることがあります。結果が大きく異なる場合は、3モデルで同じ学習データとテストデータを使っているか、分割条件と `alpha` が指定どおりかを確認してください。

### Step 4：結果を解釈する

この実行では、正則化を使った Ridge と Lasso の MSE が通常の線形回帰より小さくなりました。ただし、正則化モデルが常に勝つわけではなく、結果はデータと `alpha` によって変わります。

Ridge は通常の線形回帰で大きくなった係数を全体として抑えますが、係数を完全なゼロにはしません。Lasso はこの条件で `age`、`s2`、`s4` の係数をゼロにしました。これは「この分割と `alpha=0.1` で学習したモデルが、その3特徴量を予測に使わなかった」という意味です。

一方で、特徴量同士には相関があり、`alpha` を変えると係数も変わります。そのため、係数がゼロになったという結果だけで、その特徴量が医学的に不要、糖尿病進行度と無関係、または患者の診断に使えないと断定することはできません。
</details>
