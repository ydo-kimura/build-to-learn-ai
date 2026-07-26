# Prep 5: データ理解と前処理の基礎

この Prep では、モデルへ渡す前のデータを観察し、前処理を「なぜ、どのデータに対して行うのか」から学びます。Unit 01 では scikit-learn のデータセットと回帰モデルを使います。型や列の意味を確認しないまま前処理だけを実行すると、表示された数値が何を表すのか、モデルがどこまでを学習済みなのかを説明できません。

この Prep は、[Prep 4: pandas の基礎](../prep04_pandas/index.md)を終えていることを前提にします。NumPy 配列、pandas の `DataFrame` と `Series`、`X` と `y` の役割に不安がある場合は、先に戻ってください。

すでにデータローダーの返り値、欠損値・重複・外れ値候補の調べ方、標準化、データリーク、`ColumnTransformer`、`Pipeline` を説明できる場合は、スキップ判定だけ行って Unit 01 へ進んでかまいません。

## この Prep の到達目標

- scikit-learn のデータローダーが返す `Bunch`、NumPy 配列、pandas の表を区別できる
- `X`、`y`、行、列、特徴量、目的変数の対応を形と名前から確認できる
- 欠損値、重複、外れ値候補、数値列、カテゴリ列を観察し、確認と処置を混同しない
- 標準化と、この教材でいう範囲への正規化の目的を説明できる
- 学習用とテスト用に分割してから、学習用データだけで前処理を `fit` する理由を説明できる
- 数値列とカテゴリ列へ別々の前処理を適用し、`ColumnTransformer` と `Pipeline` にまとめられる
- 前処理をしても精度が必ず良くなるわけではないと説明できる

## スキップ判定

次のコードを実行せずに読んでください。

```python
from sklearn.datasets import load_diabetes

dataset = load_diabetes()

print(type(dataset))
print(type(dataset.data), dataset.data.shape)
print(type(dataset.target), dataset.target.shape)
print(dataset.feature_names)
```

次のすべてに答えられる場合は、この Prep をスキップできます。

1. `dataset`、`dataset.data`、`dataset.target` はそれぞれ何の型か
2. `(442, 10)` と `(442,)` は、何件のデータと何個の特徴量を表すか
3. `feature_names` は何の名前か
4. 前処理の `fit` をテストデータへしてはいけない理由は何か
5. `StandardScaler` と `MinMaxScaler` は、何をそろえるために使うか
6. 欠損値や大きな値を見つけたとき、すぐに削除してよいとは限らないのはなぜか
7. `ColumnTransformer` と `Pipeline` がそれぞれ何をまとめるか

1つでも説明できない項目があれば、最初から進めてください。答えは、実践と答え合わせを終えた後に自分の言葉で確認します。

## 学習を始める前の準備

新しい Colab Notebook を1つ作り、この Prep のコードを上から順に入力してください。コードを実行する前に、型、形、表示される列名、どの処理が学習するかをテキストセルへ予想して書きます。

標準的な Colab 環境には、この Prep で使う NumPy、pandas、scikit-learn が用意されています。ここでは追加インストールしません。

まず、データを扱うためのライブラリを読み込みます。1行ずつ読み込むことで、どの名前をどこから使うのかを確認します。

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes
```

`np` と `pd` は、Prep 3 と Prep 4 で使った NumPy と pandas の慣習的な短い名前です。`load_diabetes` は scikit-learn に用意された糖尿病データセットのローダーです。

## 1. データローダーの返り値を確認する

まず、データセットを読み込み、その返り値を観察します。

```python
dataset = load_diabetes()

print(type(dataset))
print(dataset.keys())
```

```text
<class 'sklearn.utils._bunch.Bunch'>
dict_keys([...])
```

`dataset` は `Bunch` です。`Bunch` は名前を付けて複数の値をまとめる、辞書に似た入れ物です。`keys()` で、`data`、`target`、`feature_names` など、入っている項目名を確認できます。scikit-learn の版によって、表示される項目名の並びや追加項目は少し異なることがあります。

ここで重要なのは、`dataset` 自体は NumPy 配列でも pandas の表でもないことです。必要な値を名前で取り出します。

```python
print(type(dataset.data), dataset.data.shape)
print(type(dataset.target), dataset.target.shape)
print(dataset.feature_names)
```

```text
<class 'numpy.ndarray'> (442, 10)
<class 'numpy.ndarray'> (442,)
['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']
```

`dataset.data` は、442行10列の `numpy.ndarray` です。1行が1人、10列が測定された特徴量です。`dataset.target` は、同じ442人に対応する一次元の `numpy.ndarray` です。`feature_names` は `data` の各列の名前であり、目的変数の名前ではありません。

`Bunch` が常に配列だけを返すわけではありません。別のローダーでは、読み込み方の指定によって pandas の表を返せるものもあります。返り値を決めつけず、`type()` と `shape` を確認する習慣を付けます。

## 2. X と y を観察する

配列には列名が含まれません。観察しやすくするため、`data` を `DataFrame`、`target` を名前付きの `Series` にします。

```python
diabetes_X = pd.DataFrame(
    dataset.data,
    columns=dataset.feature_names,
)
diabetes_y = pd.Series(
    dataset.target,
    name="progression",
)

print(diabetes_X.shape)
print(diabetes_X.head())
print(diabetes_y.shape)
print(diabetes_y.head())
```

`diabetes_X` の列名は `feature_names` から付けました。`diabetes_y` の `progression` は、この教材で付けた目的変数の表示名です。目的変数の値は、1年後の糖尿病進行度を表す定量的な指標です。

ここでは、次の対応を言葉にして確認します。

- `X` は予測の手がかりとして使う特徴量です。この例では `(442, 10)` で、442人分の10特徴量です。
- `y` は予測したい目的変数です。この例では `(442,)` で、442人に1つずつ対応します。
- `X` の行数と `y` の要素数が同じで、同じ位置が同じ人を指します。
- `X` の行はサンプル、`X` の列は特徴量です。pandas の表では、行・列・列名を表示して確認できます。

`age` や `bmi` という列名を見て、表示値を年齢やBMIの元の単位だと解釈してはいけません。この糖尿病データセットの特徴量は、すでに平均を中心に尺度調整されています。したがって、このデータセットは「ローダー、型、形、列名」を観察する例には使えますが、これから初めてスケーラーを学習させる例には使いません。

## 3. 前処理が必要かをデータから考える

前処理は、機械的に決まった操作ではありません。まずデータの意味と状態を観察し、何が問題なのかを考えます。次は、学習記録を模した小さな生データです。`course_type` はカテゴリ列、`score` は予測したい得点です。

```python
raw_records = pd.DataFrame(
    {
        "study_minutes": [30, 45, 60, 90, 120, 150, 180, 240, 300, 360, 420, 999],
        "attempts": [1, 1, 2, 2, 3, np.nan, 3, 4, 4, 5, 5, 10],
        "course_type": [
            "self",
            "guided",
            "self",
            "guided",
            "self",
            "guided",
            "self",
            "guided",
            "self",
            "guided",
            "self",
            "guided",
        ],
        "score": [50, 55, 60, 67, 72, 78, 80, 86, 89, 92, 95, 99],
    }
)
raw_records = pd.concat([raw_records, raw_records.iloc[[3]]], ignore_index=True)

print(raw_records)
print(raw_records.dtypes)
```

最後の `pd.concat` は、4番目の行を意図的にもう一度追加しています。そのため、この教材用データには、同じ内容の重複行が1件あります。実際のデータで同じ行を見つけても、ただちに重複だと決めつけません。別の記録として存在してよいのか、収集時の重複なのかをデータの担当者と確認します。

次に、欠損値、完全に同じ行、数値の範囲を確認します。

```python
print(raw_records.isna().sum())
print(raw_records.duplicated().sum())
print(raw_records[["study_minutes", "attempts"]].agg(["min", "max"]))
```

```text
study_minutes    0
attempts         1
course_type      0
score            0
dtype: int64
1
     study_minutes  attempts
min             30       1.0
max            999      10.0
```

この表示から、次のことが分かります。

- `attempts` に欠損値が1つあります。欠損値を見つけたことと、中央値などで補完すると決めたことは別です。
- 完全に一致する行が1つあります。この教材では意図的に作った重複なので、後で1行にします。
- `study_minutes` の999は、他の値よりかなり大きい外れ値候補です。しかし、999分学習した記録が本当にあり得ないとは、この表だけでは判断できません。この教材では残します。
- `study_minutes` と `attempts` は数値列、`course_type` は文字列で表現されたカテゴリ列です。同じ処理をそのまま適用できません。

外れ値候補、欠損値、重複を見つける操作は観察です。削除、補完、丸めなどの処置は、目的・収集方法・誤入力の可能性を確認してから決めます。前処理をしたからといって、モデルの精度が必ず良くなるわけでもありません。

## 4. 尺度調整の目的

`study_minutes` は数十から数百、`attempts` は1から10程度です。単位や幅が大きく違う数値列があると、距離や係数の大きさに敏感なモデルでは、値の幅が広い列の影響が大きくなりやすくなります。尺度調整は、列の意味を同じにする操作ではなく、数値の幅を扱いやすくそろえる操作です。

この節では、30分と999分だけの小さな配列で変換結果を見ます。これは変換の形を観察する例であり、後のモデルの前処理を学習させるデータではありません。

```python
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

scale_example = np.array([[30], [999]])

standardized_example = StandardScaler().fit_transform(scale_example)
range_scaled_example = MinMaxScaler().fit_transform(scale_example)

print(standardized_example.round(3))
print(range_scaled_example.round(3))
```

```text
[[-1.]
 [ 1.]]
[[0.]
 [1.]]
```

`StandardScaler` は、`fit` したデータの各列を平均0、標準偏差1を基準にした値へ変換します。この例では、2つの値が平均から同じだけ離れているため、およそ `-1` と `1` になります。

`MinMaxScaler` は、`fit` したデータの最小値を0、最大値を1とする範囲へ変換します。この教材では、このような範囲への変換を「正規化」と呼びます。ただし「正規化」という言葉は、分野によって別の変換を指すこともあります。何をする処理かを `MinMaxScaler` のような具体的な名前で確認します。

どちらを選ぶかはモデルとデータによります。尺度調整は有用な前処理になり得ますが、実際に評価データで比較しなければ、精度への影響は分かりません。

## 5. 学習データだけで前処理を学習する

スケーラーや補完器は、`fit` すると平均、中央値、最頻値、カテゴリ一覧などをデータから覚えます。これらは学習の一部です。そのため、テストデータを見せる前に学習用とテスト用へ分けます。

この教材用データの重複は意図的に作ったものなので、まず1行にします。外れ値候補と欠損値は、この時点では残します。

```python
from sklearn.model_selection import train_test_split

clean_records = raw_records.drop_duplicates()

X = clean_records.drop(columns="score")
y = clean_records["score"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
)

print(X_train.shape, X_test.shape)
print(y_train.shape, y_test.shape)
```

```text
(9, 3) (3, 3)
(9,) (3,)
```

`fit` は、学習用データから変換に必要な情報を覚える操作です。`transform` は、覚えた情報を使って値を変換する操作です。テスト用データには `transform` だけを行います。

次のように、分割前の `X` 全体で `fit` するのは誤りです。テスト用の行の中央値や最大値などを、学習の段階で見てしまいます。これはデータリークです。

```python
# 誤り: X にはテスト用の行も含まれます。
# preprocessor.fit(X)
```

このコードは実行しません。正しい流れは、次の節のように、前処理とモデルをまとめた `Pipeline` に `X_train` と `y_train` だけを渡して `fit` することです。

## 6. ColumnTransformer と Pipeline でまとめる

数値列とカテゴリ列では、必要な処理が異なります。

- 数値列では、欠損した `attempts` を学習用データの中央値で補完し、その後に標準化します。
- カテゴリ列では、欠損があれば学習用データの最頻値で補完し、`guided` と `self` を列へ展開するOne-Hot Encodingを行います。

この二つの流れを小さな `Pipeline` にし、列ごとに振り分ける `ColumnTransformer` に渡します。さらに、前処理と回帰モデルを一番外側の `Pipeline` にまとめます。

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

numeric_features = ["study_minutes", "attempts"]
categorical_features = ["course_type"]

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numeric_features),
        ("category", categorical_pipeline, categorical_features),
    ]
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", Ridge()),
    ]
)
```

`handle_unknown="ignore"` は、テスト用や将来のデータに学習時になかったカテゴリが出たとき、そのカテゴリに対応する列をすべて0として処理を続ける指定です。未知のカテゴリをどう扱うべきかは業務上の意味も確認しますが、この指定により予測時に即座にエラーになることは避けられます。

外側の `pipeline.fit(X_train, y_train)` を実行すると、内部の補完器、スケーラー、One-Hot Encoder、Ridge 回帰がすべて学習用データだけから `fit` されます。`pipeline.predict(X_test)` では、学習済みの前処理をテスト用データへ適用してから予測します。

```python
pipeline.fit(X_train, y_train)

transformed_train = pipeline.named_steps["preprocessor"].transform(X_train)
transformed_test = pipeline.named_steps["preprocessor"].transform(X_test)

print(pipeline.named_steps["preprocessor"].get_feature_names_out())
print(transformed_train.shape, transformed_test.shape)
print(np.round(transformed_train[:3], 3))
print(np.round(pipeline.predict(X_test), 1))
```

```text
['numeric__study_minutes' 'numeric__attempts'
 'category__course_type_guided' 'category__course_type_self']
(9, 4) (3, 4)
[[ 0.206  0.181  0.     1.   ]
 [-0.333 -0.226  1.     0.   ]
 [-0.656 -0.634  0.     1.   ]]
[83.9 81.  67.1]
```

変換後は、数値列2本とカテゴリから作られた列2本で、4列になりました。`get_feature_names_out()` は、変換後の列がどこから来たかを確認するために使います。変換結果は設定やライブラリの版によって、NumPy 配列または疎行列のような配列形式になることがあります。まず `shape` と特徴量名を確かめます。

最後の3つの数値はテスト用3件への予測です。ここでは、予測値の良し悪しを結論付けていません。どの評価指標を使うか、何と比較するか、前処理前後で同じテストデータを使えているかを決めて、初めて精度を評価できます。

## 7. 実践

ここからは自分で組み立てます。答え合わせを見る前に、新しいセルで各Stepのコードを書き、予想と実行結果を比べてください。既出のセルをコピーしてもかまいませんが、何を `fit` し、何を `transform` するかをコメントで説明します。

### Step 1: ローダーの中身を予想して確認する

`load_diabetes()` を読み込み、返り値、`data`、`target` の型と形、`feature_names` を表示してください。`dataset` 自体と `dataset.data` が同じ型ではない理由を1文で書いてください。

### Step 2: 生データの状態を観察する

この Prep の `raw_records` について、各列の欠損値数、完全に一致する行数、`study_minutes` と `attempts` の最小値・最大値を表示してください。999を削除するかどうかを、表だけでは決められない理由も書いてください。

### Step 3: X と y を分けてから分割する

意図的な完全重複だけを除き、`score` 以外を `X`、`score` を `y` にしてください。`test_size=0.25`、`random_state=42` で学習用とテスト用に分割し、4つの形を表示してください。欠損値をこの段階で補完しないでください。

### Step 4: 列ごとの前処理を組み立てる

数値列 `study_minutes` と `attempts` には、中央値補完の後に標準化を行ってください。カテゴリ列 `course_type` には、最頻値補完の後に One-Hot Encoding を行ってください。二つを `ColumnTransformer` にまとめ、さらに `Ridge` を含む外側の `Pipeline` を作ってください。

### Step 5: 学習、変換、予測の境界を確認する

外側の `Pipeline` を `X_train` と `y_train` だけで学習させてください。変換後の特徴量名、学習用・テスト用の変換後の形、テスト用予測を表示してください。なぜ `X_test` に対して `fit` をしていないのかを1文で書いてください。

## 8. 答え合わせ

<details>
<summary>実践を終えてから開く</summary>

### Step 1 の答え

```python
dataset = load_diabetes()

print(type(dataset))
print(type(dataset.data), dataset.data.shape)
print(type(dataset.target), dataset.target.shape)
print(dataset.feature_names)
```

`dataset` は名前付きの入れ物である `Bunch`、`dataset.data` と `dataset.target` は値を持つ NumPy 配列です。入れ物と、その中に入れた配列は役割が異なるため、型も異なります。

### Step 2 の答え

```python
print(raw_records.isna().sum())
print(raw_records.duplicated().sum())
print(raw_records[["study_minutes", "attempts"]].agg(["min", "max"]))
```

`attempts` には欠損値が1つ、完全一致の行は1つあります。999は外れ値候補ですが、特別な集中学習の正しい記録か、入力ミスかを表だけから断定できません。

### Step 3 の答え

```python
clean_records = raw_records.drop_duplicates()

X = clean_records.drop(columns="score")
y = clean_records["score"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
)

print(X_train.shape, X_test.shape)
print(y_train.shape, y_test.shape)
```

形は順に `(9, 3)`、`(3, 3)`、`(9,)`、`(3,)` です。補完器が学習用データだけから中央値を覚えられるよう、補完は分割後に行います。

### Step 4 の答え

```python
numeric_features = ["study_minutes", "attempts"]
categorical_features = ["course_type"]

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numeric_features),
        ("category", categorical_pipeline, categorical_features),
    ]
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", Ridge()),
    ]
)
```

数値列とカテゴリ列では処理が異なるため、小さなパイプラインを分け、`ColumnTransformer` で列へ振り分けます。

### Step 5 の答え

```python
pipeline.fit(X_train, y_train)

transformed_train = pipeline.named_steps["preprocessor"].transform(X_train)
transformed_test = pipeline.named_steps["preprocessor"].transform(X_test)

print(pipeline.named_steps["preprocessor"].get_feature_names_out())
print(transformed_train.shape, transformed_test.shape)
print(np.round(pipeline.predict(X_test), 1))
```

変換後の形は学習用が `(9, 4)`、テスト用が `(3, 4)` です。`X_test` を `fit` すると、テストデータの情報を前処理の学習に使ってしまい、未知のデータに対する評価ではなくなります。

</details>

## 完了チェック

次をすべて満たせたら、Prep 5 は完了です。

- `Bunch`、NumPy 配列、pandas の表がそれぞれ何を保持するか説明できた
- `X` の行と `y` の位置が同じサンプルを指すことを、形と表示から確認できた
- 欠損値、重複、外れ値候補を見つけることと、処置を決めることを区別できた
- 標準化と範囲への正規化が、列の数値の幅をそろえる処理だと説明できた
- データを分割してから、学習用データだけで前処理を `fit` する理由を説明できた
- 数値列とカテゴリ列に異なる前処理を行い、変換後の特徴量名と形を確認できた
- `Pipeline` が前処理とモデルを一貫した順序で扱う理由を説明できた
- 前処理の有無による精度の違いは、同じ評価条件で比較して初めて判断できると説明できた

説明できない項目があれば、該当する節へ戻り、表示された型、形、特徴量名が何を表すかを自分の言葉で書き直してください。次は [Unit 1: 線形回帰と正則化回帰](../unit01_linear_regression/index.md) で、ここで確認した `X`、`y`、分割、評価の考え方を使って線形回帰を実装します。
