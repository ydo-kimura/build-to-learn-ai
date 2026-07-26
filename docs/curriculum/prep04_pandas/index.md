# Prep 4: pandas の基礎

この Prep では、行と列に名前を付けた表形式データを扱う pandas の基礎を学びます。Unit 01 では、データセットの列名、形、値の範囲を確認してからモデルを作ります。その前に、表のどこに何の値があり、どの行・列を選んだのかを自分で説明できるようにしましょう。

この Prep は、[Prep 3: NumPy の基礎](../prep03_numpy/index.md)を終えていることを前提にします。配列の `shape`、二次元の特徴量 `X`、一次元の目的変数 `y` に不安がある場合は、先に Prep 3 を確認してください。

pandas をすでに使えて、表の状態を確認し、必要な行と列を選び、`X` と `y` を取り出せる場合は、スキップ判定だけ行って次の Prep に進んでかまいません。

## この Prep の到達目標

- `Series` と `DataFrame` の違いを説明できる
- 行、列、インデックス、列名が表のどこを指すか説明できる
- `shape`、`columns`、`dtypes`、`head()`、`info()`、`describe()` でデータを観察できる
- 1列、複数列、位置、ラベル、条件を使って必要な値を選べる
- 欠損値の場所と列ごとの個数を確認できる
- pandas の `X` と `y` を取り出し、NumPy 配列へ変換できる
- `to_numpy()` の後に残る情報と失われる情報を説明できる

## スキップ判定

次のコードを実行せずに読んでください。

```python
import pandas as pd

records = pd.DataFrame(
    {
        "study_hours": [2, 4, 6, 8],
        "attempts": [1, 2, 3, 4],
        "score": [60, 72, 84, 96],
    },
    index=pd.Index(["Aoi", "Ren", "Mio", "Sora"], name="learner"),
)

X = records[["study_hours", "attempts"]]
y = records["score"]
```

次のすべてに答えられる場合は、この Prep をスキップできます。

1. `records` の型と形は何か
2. 行ラベル、列名、値の違いは何か
3. `X` が `DataFrame`、`y` が `Series` になる理由は何か
4. `records.iloc[1:3, [0, 2]]` と `records.loc["Ren":"Mio", ["study_hours", "score"]]` は、何を基準に選ぶか
5. `isna().sum()` は何を確かめるか
6. `X.to_numpy()` の結果から、どの情報が失われるか

1つでも説明できない項目があれば、最初から進めてください。最後まで終えた後に、ここへ戻って自分の言葉で答えられるか確かめます。

## 学習を始める前の準備

新しい Colab Notebook を1つ作り、この Prep のコードを上から順に入力してください。実行前に、表示される型、形、行、列をテキストセルへ予想して書きます。

標準的な Colab 環境には pandas が用意されているため、この Prep のために追加インストールする必要はありません。

最初に、pandas を `pd` という短い名前で使えるようにします。

```python
import pandas as pd
```

`pd` は pandas の教材や公式ドキュメントで広く使われる慣習的な名前です。pandas そのものと別のライブラリではありません。

## 1. 名前付きの1列と表を作る

Prep 3 では、4人分の学習記録を NumPy の配列として扱いました。pandas では、同じ値に列名と行ラベルを付けて表にできます。

| 学習者 | 学習時間 | 挑戦回数 | 得点 |
| ------ | -------: | -------: | ---: |
| Aoi    |        2 |        1 |   60 |
| Ren    |        4 |        2 |   72 |
| Mio    |        6 |        3 |   84 |
| Sora   |        8 |        4 |   96 |

次のコードで表を作ります。

```python
records = pd.DataFrame(
    {
        "study_hours": [2, 4, 6, 8],
        "attempts": [1, 2, 3, 4],
        "score": [60, 72, 84, 96],
    },
    index=pd.Index(["Aoi", "Ren", "Mio", "Sora"], name="learner"),
)

print(records)
```

```text
         study_hours  attempts  score
learner
Aoi                2         1     60
Ren                4         2     72
Mio                6         3     84
Sora               8         4     96
```

`records` 全体は `DataFrame` です。二次元の表で、各行は1人の観察結果、各列は1つの項目を表します。

- `Aoi`、`Ren`、`Mio`、`Sora` は行を識別する**インデックスのラベル**です
- `study_hours`、`attempts`、`score` は**列名**です
- `2` や `60` は表に記録された**値**です

インデックスは行を見つけるための名前です。この例では、インデックス自身を予測の手がかりとして使うわけではありません。

表から1列だけ選ぶと、多くの場合は `Series` になります。

```python
study_hours = records["study_hours"]

print(type(study_hours))
print(study_hours)
```

```text
<class 'pandas.Series'>
learner
Aoi     2
Ren     4
Mio     6
Sora    8
Name: study_hours, dtype: int64
```

`Series` は、インデックスと名前を持つ一次元の値の並びです。この場合、値は学習時間、インデックスは学習者名、`Name` は列名です。

一方、複数列を選ぶと `DataFrame` のままです。

```python
features = records[["study_hours", "attempts"]]

print(type(features))
print(features)
```

```text
<class 'pandas.DataFrame'>
         study_hours  attempts
learner
Aoi                2         1
Ren                4         2
Mio                6         3
Sora               8         4
```

`records["study_hours"]` の角括弧は1組なので、1列の `Series` です。`records[["study_hours", "attempts"]]` は「列名を並べたリスト」を指定しているため、2列の `DataFrame` になります。

## 2. 表を変える前に観察する

モデル用の `X` や `y` を作る前に、まず表に何行・何列あり、どんな名前・型の列があるかを確認します。

```python
print(type(records))
print(records.shape)
print(records.columns)
print(records.dtypes)
print(records.head())
```

```text
<class 'pandas.DataFrame'>
(4, 3)
Index(['study_hours', 'attempts', 'score'], dtype='str')
study_hours    int64
attempts       int64
score          int64
dtype: object
         study_hours  attempts  score
learner
Aoi                2         1     60
Ren                4         2     72
Mio                6         3     84
Sora               8         4     96
```

- `type(records)` は、表が `DataFrame` であることを確認します
- `shape` の `(4, 3)` は、4行3列を意味します
- `columns` は列名の一覧です。ここでは値ではなく名前が表示されています
- `dtypes` は各列にどんな型の値が入っているかを示します。`int64` は整数の列です
- `head()` は先頭の数行を表示します。行数が多い表でも、まず中身を見渡すために使います

`head()` がすべての行を表示したのは、この表が4行しかないためです。大きい表でも、既定では先頭5行だけを表示します。

## 3. `info()` と `describe()` を読む

`info()` は、表の構造を短くまとめます。

```python
records.info()
```

```text
<class 'pandas.DataFrame'>
Index: 4 entries, Aoi to Sora
Data columns (total 3 columns):
 #   Column       Non-Null Count  Dtype
---  ------       --------------  -----
 0   study_hours  4 non-null      int64
 1   attempts     4 non-null      int64
 2   score        4 non-null      int64
dtypes: int64(3)
memory usage: ...
```

ここでは、4行3列であること、全列に4個ずつ欠損していない値があること、3列とも整数型であることを読み取れます。最後の `memory usage` の数値は pandas の版や環境で変わるため、暗記する値ではありません。

数値列の要約を見たいときは `describe()` を使います。

```python
print(records.describe())
```

```text
       study_hours  attempts      score
count     4.000000  4.000000   4.000000
mean      5.000000  2.500000  78.000000
min       2.000000  1.000000  60.000000
max       8.000000  4.000000  96.000000
```

実際には `std`、`25%`、`50%`、`75%` の行も表示されます。今は、各列について次を確認できれば十分です。

- `count`: 欠損していない値の個数
- `mean`: 平均
- `min`: 最小値
- `max`: 最大値

たとえば `score` の平均は `78.0`、最小値は `60.0`、最大値は `96.0` です。ここでは列ごとに別々に集計されるため、Prep 3 の「単位が違う列をまとめた平均」と違い、得点の平均として意味を読み取れます。

## 4. 行と列を意図して選ぶ

同じ「一部を選ぶ」操作でも、何を基準に選ぶかで書き方と意味が変わります。

### 列名で選ぶ

1列は列名の文字列で選びます。

```python
scores = records["score"]

print(type(scores), scores.shape)
print(scores)
```

```text
<class 'pandas.Series'> (4,)
learner
Aoi     60
Ren     72
Mio     84
Sora    96
Name: score, dtype: int64
```

複数列は、列名をリストにして選びます。

```python
two_columns = records[["study_hours", "score"]]

print(type(two_columns), two_columns.shape)
print(two_columns)
```

```text
<class 'pandas.DataFrame'> (4, 2)
         study_hours  score
learner
Aoi                2     60
Ren                4     72
Mio                6     84
Sora                8     96
```

ここで使ったのは列名です。`0` や `1` のような位置ではありません。

### `iloc` で位置から選ぶ

`iloc` は、0から始まる**位置**で行と列を選びます。次は、位置1・2の行（Ren、Mio）と、位置0・2の列（学習時間、得点）を選びます。

```python
by_position = records.iloc[1:3, [0, 2]]

print(type(by_position), by_position.shape)
print(by_position)
```

```text
<class 'pandas.DataFrame'> (2, 2)
         study_hours  score
learner
Ren                4     72
Mio                6     84
```

`1:3` は1から始めて3の手前までなので、位置1と2です。NumPy のスライスと同じく、終点の3は含みません。

### `loc` でラベルから選ぶ

`loc` は、インデックスや列の**ラベル**で選びます。

```python
by_label = records.loc["Ren":"Mio", ["attempts", "score"]]

print(type(by_label), by_label.shape)
print(by_label)
```

```text
<class 'pandas.DataFrame'> (2, 2)
         attempts  score
learner
Ren             2     72
Mio             3     84
```

`"Ren":"Mio"` はラベルの範囲です。この `loc` のラベル範囲では、終点の `"Mio"` も含まれます。`iloc` の位置スライスとは終点の扱いが違うため、何を基準にしているかを必ず確認してください。

### 条件で選ぶ

「得点が80点以上」のように、値の条件で行を選ぶこともできます。

```python
high_scores = records.loc[records["score"] >= 80, ["study_hours", "score"]]

print(type(high_scores), high_scores.shape)
print(high_scores)
```

```text
<class 'pandas.DataFrame'> (2, 2)
         study_hours  score
learner
Mio                6     84
Sora               8     96
```

`records["score"] >= 80` は、各行について条件を満たすかを `True` / `False` で表します。`loc` は `True` の行だけを残します。これは因果関係を示す操作ではなく、指定した条件に合う記録を取り出す操作です。

## 5. 欠損値を見つけて数える

実データには、記録されていない値が含まれることがあります。まずは、欠損値がどこにあり、列ごとに何個あるかを観察します。

元の `records` を変えないよう、コピーに1つだけ欠損値を入れます。

```python
records_with_missing = records.copy()
records_with_missing.loc["Mio", "attempts"] = None

print(records_with_missing)
```

```text
         study_hours  attempts  score
learner
Aoi                2       1.0     60
Ren                4       2.0     72
Mio                6       NaN     84
Sora                8       4.0     96
```

`NaN` は数値データでよく表示される欠損値の表現です。ここで値を平均などで埋めたり、行を削除したりはしません。

場所を確認するには `isna()` を使います。

```python
print(records_with_missing.isna())
```

```text
         study_hours  attempts  score
learner
Aoi            False     False  False
Ren            False     False  False
Mio            False      True  False
Sora           False     False  False
```

`True` は「その位置が欠損値」を表します。列ごとの個数は、`sum()` を続けて計算します。

```python
print(records_with_missing.isna().sum())
```

```text
study_hours    0
attempts       1
score          0
dtype: int64
```

`attempts` だけに1個の欠損値があります。欠損値の扱い方を決めるのは、値の意味、欠損した理由、分析の目的に依存します。補完や削除などの前処理は Prep 5 で扱います。この Prep では、見つけて数えられれば十分です。

## 6. pandas の `X` と `y` を NumPy 配列へ変換する

ここでも、学習時間と挑戦回数から得点を予測することを考えます。

```python
X = records[["study_hours", "attempts"]]
y = records["score"]

print(type(X), X.shape)
print(X.columns)
print(X.index)

print(type(y), y.shape)
print(y.name)
print(y.index)
```

```text
<class 'pandas.DataFrame'> (4, 2)
Index(['study_hours', 'attempts'], dtype='str')
Index(['Aoi', 'Ren', 'Mio', 'Sora'], dtype='str', name='learner')
<class 'pandas.Series'> (4,)
score
Index(['Aoi', 'Ren', 'Mio', 'Sora'], dtype='str', name='learner')
```

`X` は2列を選んだ `DataFrame`、`y` は1列を選んだ `Series` です。両方とも同じ4人のインデックスを持つので、Aoi の特徴量と Aoi の得点を対応させられます。

scikit-learn に渡すときは、pandas の表をそのまま使える場合もあります。NumPy 配列として確認したいときは `to_numpy()` を使います。

```python
X_array = X.to_numpy()
y_array = y.to_numpy()

print(type(X_array), X_array.shape)
print(X_array)
print(type(y_array), y_array.shape)
print(y_array)
```

```text
<class 'numpy.ndarray'> (4, 2)
[[2 1]
 [4 2]
 [6 3]
 [8 4]]
<class 'numpy.ndarray'> (4,)
[60 72 84 96]
```

値の並びと形は残ります。一方で、`X_array` には `study_hours` や `attempts` という列名も、Aoi などの行ラベルもありません。`y_array` にも `score` という名前や行ラベルはありません。

`to_numpy()` は値を配列に変換する操作です。どの列を特徴量にするか、どの列を目的変数にするかを自動で決める操作ではありません。`X` と `y` を選ぶ判断は、変換する前に自分で行います。

## 7. 実践

ここからは、完成した実装例を写すのではなく、自分でコードを組み立てます。各 Step で、次の順序を守ってください。

1. 実行前に、型、形、選ばれる行や列を予想する
2. 自分でコードを書いて実行する
3. 予想と出力を比べる
4. 出力が何を表すかを文章で説明する

### Step 1: 表を作って観察する

1. Aoi、Ren、Mio、Sora をインデックスにして、学習時間、挑戦回数、得点の `DataFrame` を作ってください。
2. `type`、`shape`、`columns`、`dtypes`、`head()` を表示してください。
3. 4行3列という形と、各列の名前・型を説明してください。

### Step 2: `info()` と `describe()` を読む

1. 作った表に `info()` を実行してください。
2. 各列の non-null の個数と型を確認してください。
3. `describe()` を表示し、得点の個数、平均、最小、最大を説明してください。
4. `memory usage` の数値を答えに使わない理由を書いてください。

### Step 3: 列、位置、ラベル、条件で選ぶ

1. 得点だけを1列の `Series` として選んでください。
2. 学習時間と挑戦回数を2列の `DataFrame` として選んでください。
3. `iloc` で Ren と Mio の学習時間・得点を選んでください。
4. `loc` で Ren から Mio までの挑戦回数・得点を選んでください。
5. 得点80点以上の人の学習時間・得点を条件で選んでください。
6. それぞれが名前、位置、ラベル、条件のどれを基準にしているか説明してください。

### Step 4: 欠損値を観察する

1. 元の表を `copy()` してください。
2. コピーした表の Mio の挑戦回数を `None` にしてください。
3. `isna()` で欠損値の場所を表示してください。
4. `isna().sum()` で列ごとの個数を表示してください。
5. 値を埋めたり行を削除したりせず、どの列に何個あるかを説明してください。

### Step 5: pandas の `X` と `y` を取り出す

1. 学習時間と挑戦回数を `X` として取り出してください。
2. 得点を `y` として取り出してください。
3. `X` と `y` の型、形、列名または名前、インデックスを表示してください。
4. `X` が `DataFrame`、`y` が `Series` になる理由を説明してください。

### Step 6: NumPy 配列に変換する

1. `X.to_numpy()` と `y.to_numpy()` を実行してください。
2. 変換後の型、形、値を表示してください。
3. 変換前にあった列名、`y` の名前、行ラベルのうち、何が配列に残らないか説明してください。
4. `to_numpy()` が特徴量と目的変数を自動で選ぶ操作ではない理由を説明してください。

## 8. 答え合わせ

すべての Step を実行し、出力の意味を書いてから開いてください。変数名や表示順は少し違ってもかまいません。同じ値、型、形を得て説明できれば正解です。

<details>
<summary>答え合わせを開く</summary>

### Step 1

```python
records = pd.DataFrame(
    {
        "study_hours": [2, 4, 6, 8],
        "attempts": [1, 2, 3, 4],
        "score": [60, 72, 84, 96],
    },
    index=pd.Index(["Aoi", "Ren", "Mio", "Sora"], name="learner"),
)

print(type(records))
print(records.shape)
print(records.columns)
print(records.dtypes)
print(records.head())
```

`records` は `DataFrame`、形は `(4, 3)` です。4人分の記録が行、`study_hours`、`attempts`、`score` が列です。3列は整数の値を持ちます。

### Step 2

```python
records.info()
print(records.describe())
```

`info()` では、3列すべての non-null の個数が4、型が `int64` と分かります。`describe()` では、得点の個数は4、平均は `78.0`、最小は `60.0`、最大は `96.0` です。`memory usage` は環境で変わるため、比較する対象ではありません。

### Step 3

```python
scores = records["score"]
features = records[["study_hours", "attempts"]]
by_position = records.iloc[1:3, [0, 2]]
by_label = records.loc["Ren":"Mio", ["attempts", "score"]]
high_scores = records.loc[records["score"] >= 80, ["study_hours", "score"]]

print(type(scores), scores.shape)
print(type(features), features.shape)
print(by_position)
print(by_label)
print(high_scores)
```

`scores` は `(4,)` の `Series`、`features` は `(4, 2)` の `DataFrame` です。`iloc` は0から始まる位置、`loc` は `Ren` や `Mio` のラベル、最後の `loc` は得点80以上という条件を基準に選んでいます。

### Step 4

```python
records_with_missing = records.copy()
records_with_missing.loc["Mio", "attempts"] = None

print(records_with_missing.isna())
print(records_with_missing.isna().sum())
```

`Mio` の `attempts` だけが `True` です。列ごとの個数は `study_hours` が0、`attempts` が1、`score` が0です。ここでは欠損を見つけて数えただけで、補完や削除はしていません。

### Step 5

```python
X = records[["study_hours", "attempts"]]
y = records["score"]

print(type(X), X.shape, list(X.columns), list(X.index))
print(type(y), y.shape, y.name, list(y.index))
```

`X` は2列を選んだ `(4, 2)` の `DataFrame`、`y` は1列を選んだ `(4,)` の `Series` です。どちらも Aoi、Ren、Mio、Sora の同じ順序のインデックスを持っています。

### Step 6

```python
X_array = X.to_numpy()
y_array = y.to_numpy()

print(type(X_array), X_array.shape)
print(X_array)
print(type(y_array), y_array.shape)
print(y_array)
```

`X_array` は `(4, 2)`、`y_array` は `(4,)` の `numpy.ndarray` です。値と順序は残りますが、列名、`y` の名前、Aoi などのインデックスは配列に残りません。どの列を `X` と `y` にするかは、変換前に自分で選んでいます。

</details>

## 完了チェック

次をすべて満たせたら、Prep 4 は完了です。

- `Series` が名前とインデックスを持つ1列の値、`DataFrame` が名前付きの表であると説明できた
- `shape`、`columns`、`dtypes`、`head()`、`info()`、`describe()` の役割を使い分けられた
- 1列と複数列の選択で、結果の型と形がどう変わるか説明できた
- `iloc` の位置、`loc` のラベル、条件選択の違いを説明できた
- 欠損値の場所と列ごとの個数を確認できた
- 欠損値を見つけることと、欠損値を修復することが別の作業だと説明できた
- pandas の `X` と `y` を取り出し、同じインデックスが対応関係を示すと説明できた
- `to_numpy()` の後に、値と順序は残るがラベルは失われると説明できた
- Notebook を再起動して上から実行し、同じ結果を再現できた

説明できない項目があれば、その節へ戻って、選ぶ列や条件を1つ変えて再実行してください。次の Prep 5 では、欠損値の補完・削除、尺度調整、カテゴリ変数の変換などの前処理を、なぜ必要かから扱います。
