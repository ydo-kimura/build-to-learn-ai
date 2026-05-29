# Unit 4: 決定木とランダムフォレスト

## 1. 決定木とランダムフォレストの理解

<img src="./images/concept.png" width="400" alt="コンセプト図解">

これまで数式や境界線を使ってデータを分けてきましたが、今回はもっと人間の思考回路に近い、非常に分かりやすいアルゴリズム「決定木（Decision Tree）」と、その進化系である「ランダムフォレスト（Random Forest）」について学びます。

### 決定木とは？ 〜「アキネーター（20の扉）」ゲーム〜
決定木は、**「Yes/Noで答えられる質問を繰り返して、答えを絞り込んでいく」**アルゴリズムです。

思い浮かべたキャラクターを当てるゲーム「アキネーター」を知っていますか？
「その人は実在する？」「男性？」「YouTuber？」といった質問を順番に繰り返すことで、何万という選択肢からたった1つの答えに辿り着きます。決定木がやっているのはまさにこれです。

#### 例え話：動物の分類
データを「犬」「猫」「鳥」に分類したいとします。
決定木はデータを分析し、最も綺麗に分けられる「最強の質問」を自動的に探し出して、ツリー（木）を作っていきます。

1. **質問1：**「羽が生えている？」
   - Yes → 鳥！🐦
   - No → 次の質問へ
2. **質問2：**「散歩が好き？」
   - Yes → 犬！🐶
   - No → 猫！🐱

| 決定木のメリット | 決定木のデメリット |
| :--- | :--- |
| なぜその予測になったか、人間が図を見て理解しやすい（解釈性が最強） | 過去のデータを丸暗記しすぎて、応用が利かなくなる（過学習しやすい） |
| データのスケール（単位）を揃えなくてもそのまま使える | 木が深くなりすぎると、少しデータが変わっただけで結果がガラリと変わる |

### ランダムフォレストとは？ 〜「三人寄れば文殊の知恵」〜
決定木の最大の弱点は「過学習」でした。1本の木を深く成長させすぎると、変なマニアックな質問ばかりする「偏屈な木」になってしまいます。

これを解決するのが**ランダムフォレスト**（ランダムな森）です。
「1本の木がダメなら、**特徴の違う木を100本作って、みんなで多数決をとればいいじゃないか！**」という、力技でありながら非常に強力なアプローチです。（これを**アンサンブル学習**と呼びます）

#### 例え話：美味しいレストラン探し
- **決定木（1人）**：「俺の経験上、赤い看板で、メニューが3つしかない店は絶対に美味い！」（←偏見が強すぎる）
- **ランダムフォレスト（100人会議）**：
  - Aさん「評価が星4以上の店がいい」
  - Bさん「私は行列ができている店」
  - Cさん「店内が清潔な店」
  👉 **みんなの意見（予測）の多数決をとって、一番票が多かった店を最終決定とする！**

一人一人は少し間違えるかもしれませんが、みんなで集まれば「知恵」になります。ランダムフォレストは、データの選ばれ方や質問の候補を**あえて少しランダムにずらして**たくさんの木を作り、多数決で最強の予測を行います。

### 💡 具体的なビジネスユースケース

- **コールセンターの問い合わせ自動振り分け**：顧客の入力したキーワードや選択肢に基づく「Yes/No」の決定木ルールにより、最適な担当部署へ自動ルーティングする。
- **人事採用での退職リスク予測**：従業員の残業時間、給与テーブル、評価スコアなどのデータからランダムフォレストを用いて退職リスクを予測し、マネージャーがフォローアップを行う対象者を抽出する。
- **銀行の不正検知（フロードディテクション）**：クレジットカードの利用場所、金額、時間帯などの多数の特徴をランダムフォレストで解析し、普段の行動パターンから外れた疑わしい取引を瞬時にブロックする。

---

## 2. 実装例 (Implementation Example)

「乳がんの診断データ」を使って、決定木（1本の木）とランダムフォレスト（たくさんの木の多数決）の精度を比較してみましょう。

```python
# 必要なツールのインポート
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. データの準備と分割
cancer = load_breast_cancer()
X = cancer.data
y = cancer.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

**【コードの解説】**
いつものようにデータを読み込み、学習用とテスト用に分割しています。

```python
# 2. 決定木（1本の木）の学習と予測
# max_depth で木の深さ（質問の回数）を制限できます。今回は制限なしで作ります。
tree_model = DecisionTreeClassifier(random_state=42)
tree_model.fit(X_train, y_train)

tree_pred = tree_model.predict(X_test)
print(f"決定木の正解率: {accuracy_score(y_test, tree_pred):.3f}")
```

**【コードの解説】**
`DecisionTreeClassifier` で決定木を作ります。1本の木なので学習は一瞬で終わります。

```python
# 3. ランダムフォレスト（多数決）の学習と予測
# n_estimators=100 は「木を100本作って森を作る」という指示です
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)
print(f"ランダムフォレストの正解率: {accuracy_score(y_test, rf_pred):.3f}")
```

**【コードの解説】**
`RandomForestClassifier` がランダムフォレストのクラスです。先ほどの `DecisionTree` と使い方は全く同じですが、内部で100本の木を作って多数決をとってくれています。結果を比べると、ランダムフォレストの方が正解率が高くなり、より安定した予測ができていることが分かります。

---

## 3. 実践 (Practice)

ランダムフォレストは、分類だけでなく「数値を予測する回帰」にも使えます。以下の要件に従って実装してみましょう！

**【課題の要件】**
Unit 1で使った「糖尿病の進行度予測データセット」を使い、今度はランダムフォレストを使って回帰（数値予測）を行ってみます。

1. `sklearn.datasets` から `load_diabetes` を読み込んでください。
2. データを学習用（80%）とテスト用（20%）に分割してください。
3. 今回は**数値の予測（回帰）**なので、`RandomForestClassifier` ではなく **`RandomForestRegressor`** を使ってモデルを作成し、学習させてください。（木の数は100本でOKです）
4. テストデータに対して予測を行い、MSE（平均二乗誤差）を計算して表示してください。（`mean_squared_error`を使用します）

**【ヒント】**
- `from sklearn.ensemble import RandomForestRegressor` をインポートします。
- `from sklearn.metrics import mean_squared_error` も必要です。

---

## 4. 答え合わせ (Answer Key)

自分でコードを書いてから、以下の答えを開いて確認してみましょう。

<details>
<summary>解答例を見る（クリックで展開）</summary>

```python
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# 1. データの読み込み
diabetes = load_diabetes()
X = diabetes.data
y = diabetes.target

# 2. データの分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. ランダムフォレスト（回帰）モデルの作成と学習
# 数値予測なので Regressor を使います
rf_reg_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg_model.fit(X_train, y_train)

# 4. 予測と評価
y_pred = rf_reg_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print(f"ランダムフォレスト回帰のMSE: {mse:.2f}")
```

**【解答コードの解説】**
分類（Classifier）と回帰（Regressor）でクラス名が少し違うだけで、使い方は全く同じです！
ランダムフォレストは非常に強力で、どんなデータセットに対しても「とりあえず最初に試してみるべき最強の基準（ベースライン）」として実務でもめちゃくちゃ頻繁に使われます。
</details>
