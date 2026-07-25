# Prep 2: Python の基礎

この Prep では、Unit 01 以降のコードを読むために必要な Python の基礎を学びます。完成したコードを眺めるだけではなく、値を予想し、自分で入力して実行し、少し変更して結果を確かめます。

Python を初めて使う人を対象にしています。すでに Python の変数、リスト、辞書、条件分岐、繰り返し、関数、インポートを使えて、属性とメソッドの違いを説明できる場合は、スキップ判定だけ行って次の Prep に進んでかまいません。

この Prep は、[Prep 1: Notebook／Colab の基礎](../prep01_notebook_colab/index.md)を終えていることを前提にします。Colab の操作やセルの実行順に不安がある場合は、先に Prep 1 を確認してください。

## この Prep の到達目標

- 値を変数に代入し、数値、文字列、真偽値を区別できる
- リストと辞書に複数の値をまとめ、必要な値を取り出せる
- `if` と `for` の処理範囲をインデントで表せる
- 関数に引数を渡し、戻り値を受け取れる
- `object.attribute` と `object.method()` の違いを説明できる
- 必要な機能をインポートして使える
- `print()` と f-string で値を確認できる
- エラーの最後の行から、最初に確認する場所を判断できる

## スキップ判定

次のコードを、実行せずに読んでください。

```python
scores = [72, 85, 91]

def average(values):
    return sum(values) / len(values)

result = average(scores)

if result >= 80:
    print(f"平均: {result:.1f}、判定: 合格")
else:
    print(f"平均: {result:.1f}、判定: もう一度")
```

次のすべてに答えられる場合は、この Prep をスキップできます。

1. `scores`、`values`、`result` がそれぞれ何を表すか
2. `scores[0]` と `scores[:2]` がどの値になるか
3. `average(scores)` を実行すると、どこからどこへ値が渡るか
4. `return` が返した値を、どの行が受け取るか
5. `result >= 80` が `True` と `False` のどちらになるか
6. 最後に表示される文字列は何か
7. `values` と `values.append(100)` のような書き方の違い

1つでも説明できない項目があれば、最初から進めてください。

## 学習を始める前の準備

新しい Colab Notebook を1つ作り、この Prep のコードを上から順に入力します。各コードを実行する前に、何が表示されるかをテキストセルへ書いてください。

実践中は、自分で考えたコードと実際の結果を比べられるよう、Colab のAIアシストをオフにすることを推奨します。設定方法は Prep 1 の「実践前にAIアシストをオフにする」を参照してください。

この Prep のコードは、Python の標準機能だけで実行できます。NumPy や pandas のインストールは不要です。

## 1. 値を変数に代入する

プログラムは、数値や文字などの値を扱います。値に名前を付けて、後から使えるようにしたものが変数です。

```python
learner_name = "Aoi"
score = 72
completed = False

print(learner_name)
print(score)
print(completed)
```

```text
Aoi
72
False
```

`=` は、右側の値を左側の変数へ代入する記号です。「左右が等しいか」を調べる記号ではありません。上のコードでは、文字列 `"Aoi"` に `learner_name` という名前を付けています。

同じ変数へ新しい値を代入すると、その後は新しい値が使われます。

```python
score = 72
score = 80
print(score)
```

```text
80
```

Python では、大文字と小文字を区別します。`score` と `Score` は別の名前です。

### 基本的な値の種類

このカリキュラムで最初によく使う値は、次の4種類です。

| 種類   | Python での名前 | 例              | 用途                   |
| ------ | --------------- | --------------- | ---------------------- |
| 整数   | `int`           | `72`            | 人数、回数、整数の得点 |
| 小数   | `float`         | `72.5`          | 平均、割合、測定値     |
| 文字列 | `str`           | `"Aoi"`         | 名前、ラベル、説明     |
| 真偽値 | `bool`          | `True`、`False` | 条件が成立するかどうか |

`type()` を使うと、値の種類を確認できます。

```python
print(type(72))
print(type(72.5))
print(type("Aoi"))
print(type(False))
```

```text
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
```

ここで表示される `class` は、値の種類を表していると理解できれば十分です。この Prep では、クラスの作り方までは扱いません。

## 2. 計算と比較をする

数値は、演算子を使って計算できます。

```python
first_score = 72
second_score = 85

total = first_score + second_score
average_of_two = total / 2

print(total)
print(average_of_two)
```

```text
157
78.5
```

最初によく使う演算子は次のとおりです。

| 演算子 | 意味   | 例       | 結果  |
| ------ | ------ | -------- | ----- |
| `+`    | 足し算 | `7 + 2`  | `9`   |
| `-`    | 引き算 | `7 - 2`  | `5`   |
| `*`    | 掛け算 | `7 * 2`  | `14`  |
| `/`    | 割り算 | `7 / 2`  | `3.5` |
| `**`   | べき乗 | `3 ** 2` | `9`   |

比較の結果は、真偽値 `True` または `False` になります。

```python
score = 72

print(score >= 70)
print(score == 80)
print(score != 80)
```

```text
True
False
True
```

| 演算子 | 調べること           |
| ------ | -------------------- |
| `==`   | 左右の値が等しい     |
| `!=`   | 左右の値が等しくない |
| `>`    | 左が右より大きい     |
| `<`    | 左が右より小さい     |
| `>=`   | 左が右以上           |
| `<=`   | 左が右以下           |

代入の `=` と、等しいかを比較する `==` は役割が異なります。

## 3. リストで複数の値を順番にまとめる

リストは、複数の値を順番に並べてまとめるものです。角括弧 `[]` の中をカンマで区切ります。

```python
scores = [72, 85, 91]
print(scores)
```

```text
[72, 85, 91]
```

### インデックスで1つ取り出す

リスト内の位置を表す番号をインデックスといいます。Python のインデックスは `0` から始まります。

```python
scores = [72, 85, 91]

print(scores[0])
print(scores[1])
print(scores[2])
```

```text
72
85
91
```

3個の値があっても、最後のインデックスは `2` です。

### スライスで範囲を取り出す

スライスを使うと、リストの一部を新しいリストとして取り出せます。

```python
scores = [72, 85, 91]
print(scores[0:2])
print(scores[:2])
```

```text
[72, 85]
[72, 85]
```

`0:2` は、インデックス `0` から始めて、インデックス `2` の直前までという意味です。終点の値 `scores[2]` は含まれません。先頭から取り出す場合は、`0` を省略して `scores[:2]` と書けます。

### リストを変更する

`append()` を使うと、リストの末尾に値を追加できます。

```python
scores = [72, 85, 91]
scores.append(88)
print(scores)
```

```text
[72, 85, 91, 88]
```

`len()` は、リストに値がいくつあるかを返します。

```python
print(len(scores))
```

```text
4
```

## 4. 辞書で名前と値を対応させる

辞書は、キーと値を組み合わせて管理するものです。リストが位置で値を取り出すのに対し、辞書はキーを指定して値を取り出します。

```python
learner_scores = {
    "Aoi": 72,
    "Ren": 85,
    "Mio": 91,
}

print(learner_scores["Ren"])
```

```text
85
```

この辞書では、学習者名がキー、得点が値です。`learner_scores["Ren"]` は、キー `"Ren"` に対応する値を取り出しています。

値の追加や変更も、キーを指定して行います。

```python
learner_scores["Sora"] = 88
learner_scores["Aoi"] = 80

print(learner_scores["Sora"])
print(learner_scores["Aoi"])
```

```text
88
80
```

後の実践では、1人につき複数の得点を持たせるため、辞書の値にリストを使います。

```python
learner_scores = {
    "Aoi": [72, 80, 88],
    "Ren": [65, 70, 75],
    "Mio": [90, 94, 96],
}

print(learner_scores["Aoi"])
print(learner_scores["Aoi"][0])
```

```text
[72, 80, 88]
72
```

最初の角括弧で辞書のキー `"Aoi"` を指定し、次の `[0]` でその人の得点リストの先頭を取り出しています。

## 5. `if` で条件によって処理を分ける

`if` は、条件が `True` のときだけ処理を実行します。条件が成立しない場合の処理は `else` に書けます。

```python
score = 72

if score >= 80:
    print("合格")
else:
    print("もう一度")
```

```text
もう一度
```

`if` と `else` の行末にはコロン `:` が必要です。その内側で実行する行は、先頭に空白を入れて字下げします。この字下げをインデントといいます。

```text
if 条件:
    条件が True のときの処理
else:
    条件が False のときの処理
```

Python は、インデントを見て処理のまとまりを判断します。見た目を整えるだけの空白ではありません。このカリキュラムでは、インデント1段に半角スペース4個を使います。

## 6. `for` で同じ処理を繰り返す

`for` は、リストなどから値を1つずつ取り出し、同じ処理を繰り返します。

```python
scores = [72, 85, 91]

for score in scores:
    print(score)
```

```text
72
85
91
```

1回目は `score` に `72`、2回目は `85`、3回目は `91` が代入されます。リストの値をすべて取り出すと、繰り返しは終了します。

繰り返しの内側も、インデントで表します。

```python
scores = [72, 85, 91]

for score in scores:
    if score >= 80:
        print(score)
```

```text
85
91
```

`print(score)` は `if` の内側にあり、`if` は `for` の内側にあります。そのため、各得点を順番に調べ、80以上の値だけが表示されます。

## 7. 関数に処理をまとめる

関数は、名前を付けた処理のまとまりです。同じ計算を何度も使いたいときに、処理を関数へまとめます。

```python
def average(values):
    total = sum(values)
    count = len(values)
    return total / count
```

`def` で関数を定義します。`average` が関数名、丸括弧内の `values` が引数を受け取る変数です。

関数は、定義しただけでは計算を実行しません。関数名の後ろに丸括弧を付け、必要な値を渡して呼び出します。

```python
scores = [72, 85, 91]
result = average(scores)
print(result)
```

```text
82.66666666666667
```

この呼び出しでは、次の順番で値が動きます。

1. `average(scores)` が、リスト `[72, 85, 91]` を関数へ渡す
2. 関数内では、そのリストを `values` という名前で使う
3. `sum(values)` が合計、`len(values)` が個数を返す
4. `return total / count` が計算結果を関数の外へ返す
5. 返された値を `result` が受け取る

`return` を実行すると、関数の処理はそこで終わります。`print()` が画面へ表示するのに対し、`return` は呼び出し元へ値を返します。

### 引数と戻り値を変えて確かめる

同じ関数へ別のリストを渡せます。

```python
first_result = average([72, 80, 88])
second_result = average([90, 94, 96])

print(first_result)
print(second_result)
```

```text
80.0
93.33333333333333
```

関数が行う計算は同じでも、引数として渡す値が変われば、戻り値も変わります。

## 8. `print()` と f-string で結果を確認する

`print()` の丸括弧へ変数を渡すと、その値を表示できます。文字列の先頭に `f` を付けた f-string を使うと、文章の中へ変数の値を埋め込めます。

```python
learner_name = "Aoi"
result = 80.0

print(f"{learner_name}の平均は{result}です")
```

```text
Aoiの平均は80.0です
```

波括弧 `{}` の中に書いた変数が、その値へ置き換わります。

小数の表示桁数も指定できます。

```python
result = 93.33333333333333
print(f"平均: {result:.1f}")
```

```text
平均: 93.3
```

`:.1f` は、小数点以下1桁で表示する指定です。表示は丸められますが、変数 `result` に保存された元の値そのものを変更するわけではありません。

## 9. 属性とメソッドを見分ける

Python では、値と、その値に関係する情報や処理を、ドット `.` でつないで使うことがあります。

```text
object.attribute
object.method()
```

- 属性は、そのオブジェクトが持つ情報です。名前の後ろに丸括弧を付けません。
- メソッドは、そのオブジェクトに関係する処理です。呼び出すための丸括弧 `()` を付けます。

標準ライブラリの日付を使って違いを確認します。

```python
from datetime import date

lesson_date = date(2026, 7, 26)

print(lesson_date.year)
print(lesson_date.isoformat())
```

```text
2026
2026-07-26
```

`lesson_date.year` は、日付が持っている年の情報を読む属性です。`lesson_date.isoformat()` は、日付を決まった形式の文字列へ変換するメソッドです。

Unit 01 以降でも、次のようなコードが登場します。

```python
X.shape
model.fit(X, y)
```

`X.shape` はデータの行数と列数を持つ属性なので、丸括弧を付けません。`model.fit(X, y)` はモデルを学習させるメソッドなので、引数を丸括弧へ渡して呼び出します。

リストの `scores.append(88)` や辞書の `learner_scores.items()` もメソッドです。

## 10. 必要な機能をインポートする

Python のすべての機能が、最初から同じ名前空間に用意されているわけではありません。別のモジュールにある機能を使うときは、`import` で読み込みます。

```python
import math

print(math.sqrt(81))
```

```text
9.0
```

`import math` は、`math` モジュールを読み込みます。使うときは `math.sqrt()` のように、モジュール名を付けます。

特定の名前だけを読み込む書き方もあります。

```python
from datetime import date

today = date(2026, 7, 26)
print(today)
```

```text
2026-07-26
```

`from datetime import date` は、`datetime` モジュールから `date` だけを読み込みます。その後は `date(...)` と直接書けます。

Unit 01 では、次のようなインポートが登場します。

```python
from sklearn.datasets import load_diabetes
```

これは、`sklearn.datasets` から `load_diabetes` という関数を読み込むコードです。インポートの後に `load_diabetes()` と書くことで、その関数を呼び出せます。

## 11. エラーの最後の行を読む

エラーは、コードのどこを最初に確認すればよいかを知らせる出力です。長く見える場合も、まず最後の行を読みます。

### `NameError`: その名前がまだ作られていない

```python
print(final_score)
```

```text
NameError: name 'final_score' is not defined
```

`final_score` という名前を、代入や関数定義でまだ作っていないことを表します。スペルや大文字と小文字、必要なセルを先に実行したかを確認します。

### `KeyError`: 辞書にそのキーがない

```python
learner_scores = {"Aoi": 72, "Ren": 85}
print(learner_scores["Mio"])
```

最後の行には、次のように表示されます。

```text
KeyError: 'Mio'
```

辞書 `learner_scores` にキー `"Mio"` がないことを表します。利用できるキーは `learner_scores.keys()` で確認できます。

エラーが出たセルを消してやり直す必要はありません。原因を確認して同じセルを修正し、もう一度実行します。最後にランタイムを再起動し、上からすべてのセルを実行して再現できることも確認してください。

## 12. 実践

ここまで説明した値、リスト、辞書、条件分岐、繰り返し、関数、f-string を組み合わせ、3人分の学習記録を集計します。

答え合わせは、すべての Step を自分で試してから開いてください。各 Step では、最初に出力を予想し、次にコードを実行し、最後に予想と結果が違った理由をテキストセルへ書きます。

### Step 1: データを観察する

次の辞書をコードセルへ入力して実行してください。

```python
learner_scores = {
    "Aoi": [72, 80, 88],
    "Ren": [65, 70, 75],
    "Mio": [90, 94, 96],
}
```

次の値を表示するコードを自分で書いてください。

1. Aoi の得点リスト
2. Ren の最初の得点
3. Mio の先頭から2個の得点
4. `learner_scores` に登録されている学習者数

表示する前に、それぞれの結果を予想してください。

### Step 2: 平均を返す関数を作る

数値のリストを受け取り、合計を個数で割った値を返す `average` 関数を定義してください。

その関数へ Aoi の得点リストを渡し、戻り値を `aoi_average` に代入して表示します。表示前に、平均がいくつになるか手計算してください。

### Step 3: 3人分の平均を表示する

辞書のすべてのキーと値を取り出すには、`items()` メソッドを使えます。

```python
for name, scores in learner_scores.items():
    print(name, scores)
```

この形を参考にして、3人それぞれについて `average(scores)` を呼び出し、次の形式で表示してください。

```text
Aoi: 80.0
Ren: 70.0
Mio: 93.3
```

平均は f-string の `:.1f` を使い、小数点以下1桁で表示します。

### Step 4: 条件で判定を加える

平均が80以上なら `"合格"`、80未満なら `"もう一度"` を変数 `status` に代入してください。その後、名前、平均、判定を次の形式で表示します。

```text
Aoi: 80.0 - 合格
Ren: 70.0 - もう一度
Mio: 93.3 - 合格
```

`if` と `else` は `for` の内側に置きます。表示する `print()` も、3人それぞれについて実行される位置に置いてください。

### Step 5: 1人追加して再実行する

辞書へ次の学習者を追加してください。

```python
learner_scores["Sora"] = [78, 82, 85]
```

Step 4 の繰り返しをもう一度実行する前に、Sora の平均と判定を予想してください。実行後、既存のコードを変更せずに4人分を処理できた理由を説明してください。

### Step 6: エラーを読んで修正する

次のコードをそのまま実行してください。

```python
print(learner_scores["Rin"])
```

1. エラーの最後の行を記録する
2. エラーの種類と原因を説明する
3. 辞書に実際に存在するキーを確認する
4. `"Rin"` を存在するキーへ修正し、同じセルを再実行する

### ヒント

- 辞書から値を読む形は `辞書[キー]` です。
- リストの先頭は `[0]`、先頭から2個は `[:2]` です。
- 値の個数は `len()`、合計は `sum()` で求められます。
- 関数の計算結果を外へ返すには `return` を使います。
- `items()` の丸括弧を忘れないでください。
- `if`、`else`、`for` の行末にはコロンが必要です。

## 13. 答え合わせ

<details>
<summary>答えと確認ポイントを表示する</summary>

### Step 1

```python
print(learner_scores["Aoi"])
print(learner_scores["Ren"][0])
print(learner_scores["Mio"][:2])
print(len(learner_scores))
```

```text
[72, 80, 88]
65
[90, 94]
3
```

辞書のキーで1人分のリストを取り出し、必要に応じてそのリストへインデックスやスライスを続けます。`len(learner_scores)` は、辞書にあるキーの個数を返します。

### Step 2

```python
def average(values):
    return sum(values) / len(values)

aoi_average = average(learner_scores["Aoi"])
print(aoi_average)
```

```text
80.0
```

`learner_scores["Aoi"]` のリストが引数 `values` へ渡り、`return` が返した `80.0` を `aoi_average` が受け取ります。

### Step 3

```python
for name, scores in learner_scores.items():
    result = average(scores)
    print(f"{name}: {result:.1f}")
```

```text
Aoi: 80.0
Ren: 70.0
Mio: 93.3
```

`items()` は、辞書のキーと値を組にして順番に取り出します。ここでは、キーを `name`、値である得点リストを `scores` が受け取ります。

### Step 4

```python
for name, scores in learner_scores.items():
    result = average(scores)

    if result >= 80:
        status = "合格"
    else:
        status = "もう一度"

    print(f"{name}: {result:.1f} - {status}")
```

```text
Aoi: 80.0 - 合格
Ren: 70.0 - もう一度
Mio: 93.3 - 合格
```

平均がちょうど `80.0` の Aoi は、条件が `>` ではなく `>=` なので合格になります。

### Step 5

```python
learner_scores["Sora"] = [78, 82, 85]

for name, scores in learner_scores.items():
    result = average(scores)

    if result >= 80:
        status = "合格"
    else:
        status = "もう一度"

    print(f"{name}: {result:.1f} - {status}")
```

```text
Aoi: 80.0 - 合格
Ren: 70.0 - もう一度
Mio: 93.3 - 合格
Sora: 81.7 - 合格
```

繰り返しは辞書に現在入っているすべての項目を処理します。そのため、辞書へ Sora を追加すれば、平均を計算する関数や繰り返しの中身を変更する必要はありません。

### Step 6

最後の行は次のようになります。

```text
KeyError: 'Rin'
```

辞書にキー `"Rin"` が存在しないためです。

```python
print(learner_scores.keys())
```

利用できるキーを確認し、たとえば次のように修正できます。

```python
print(learner_scores["Sora"])
```

```text
[78, 82, 85]
```

</details>

## 完了チェック

次をすべて満たせたら、Prep 2 は完了です。

- 変数へ代入した値と `type()` の結果を説明できた
- `=` と `==` の役割の違いを説明できた
- リストからインデックスとスライスで値を取り出せた
- 辞書からキーを使って値を取り出せた
- `if` と `for` の処理範囲をインデントで表せた
- 関数へ引数を渡し、`return` の戻り値を変数で受け取れた
- 属性には丸括弧がなく、メソッドには丸括弧がある理由を説明できた
- `import` と `from ... import ...` のコードを読めた
- f-string で名前と小数を表示できた
- `NameError` と `KeyError` の最後の行から原因を説明できた
- 実践をランタイム再起動後に上から実行し、同じ結果を再現できた

説明できない項目がある場合は、その節へ戻り、値を1つ変えて再実行してください。値を変えたときに結果がどう変わるか説明できれば、コードを読んだだけでなく、動きを理解できています。

次は、[Prep 3: NumPy の基礎](../prep03_numpy/index.md)で、複数の数値を配列として扱い、次元、形、行と列、集計結果を確認します。
