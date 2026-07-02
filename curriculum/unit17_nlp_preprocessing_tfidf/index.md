# Unit 17: 自然言語前処理と TF-IDF

<p class="unit-hero">
  <img src="../../assets/units/unit17_nlp_preprocessing_tfidf/images/hero.png" alt="ヒーロー画像：NLP Preprocessing & TF-IDF" />
</p>


## 1. NLPの前処理とTF-IDFの理解

人間の言葉をコンピュータに理解させるための第一歩は、 **「テキストデータを整理整頓して、数字のリスト（ベクトル）に変換すること」** です。

### 📌 日常的な例え：図書館での本の分類
あなたが図書館の司書だとします。新しく届いた本をどう分類するかを考える時、本の中にある「単語」に注目しますよね。
- 「リンゴ」「みかん」「バナナ」が多く出てくる本なら「果物」
- 「関数」「変数」「コンパイル」なら「プログラミング」

しかし、すべての本に「これ」「それ」「です」「ます」という言葉（ストップワード）が出てきます。これらの言葉は、本の特徴を掴む役には立ちません。
また、「走る」「走った」「走れ」は同じ「走る」という行動を指しています（ステミング・レンマ化による語幹抽出）。

NLPの **前処理** は、司書が本の特徴を掴むために行う「余計な言葉の除外」と「言葉の統一」の作業なのです。

### 📝 コラム：日本語NLPの前処理

英語のテキストは単語がスペースで区切られているため、コンピュータが「どこからどこまでが一つの単語か」を簡単に判別できます。しかし、日本語は「私は今日図書館に行きました」のように、単語の間にスペースがありません。

そのため、日本語のNLPでは最初のステップとして **形態素解析（分かち書き）** が必要になります。形態素解析とは、文を最小の意味単位（形態素）に分割する処理のことです。

例：「私は今日図書館に行きました」→「私 / は / 今日 / 図書館 / に / 行き / まし / た」

代表的なライブラリとして **MeCab** （高速・辞書が豊富）と **Janome** （Pure Python で環境構築が簡単）があります。Janomeを使えば、たった数行で分かち書きができます：

```python
from janome.tokenizer import Tokenizer
t = Tokenizer()
tokens = [token.surface for token in t.tokenize("私は今日図書館に行きました")]
print(tokens)  # ['私', 'は', '今日', '図書館', 'に', '行き', 'まし', 'た']
```

以下に、英語と日本語の前処理フローの違いをまとめます：

| ステップ | 英語 | 日本語 |
| :--- | :--- | :--- |
| **単語の分割** | スペースで分割するだけ | 形態素解析（MeCab / Janome）が必要 |
| **大文字・小文字の統一** | 必要（Apple → apple） | 不要（そもそも大文字・小文字の区別がない） |
| **ストップワード除去** | the, is, at など | は、が、の、です、ます など |
| **語幹の抽出** | ステミング / レンマ化 | 形態素解析で原形を取得 |

> 💡 図書館の例えでいうと、英語の本はすでに単語ごとにスペースで区切られた状態で届きますが、日本語の本は「すべての文字がぎっしり詰まった巻物」で届くようなもの。司書（コンピュータ）がまず巻物を単語ごとに切り分ける作業が、形態素解析です。

### 📌 TF-IDFとは？
前処理が終わった後、各単語の「重要度」を点数化する手法が **TF-IDF** (Term Frequency-Inverse Document Frequency) です。

| 要素 | 意味 | 図書館の例え | 計算のイメージ |
| :--- | :--- | :--- | :--- |
| **TF (単語の出現頻度)** | その文書内で、ある単語が何回出てきたか | この本には「AI」という単語がたくさん出てくる！ | 頻度が高いほど点数が高い |
| **IDF (逆文書頻度)** | 全文書の中で、その単語がどれくらい珍しいか | 「AI」は他の本にはあまり出てこない、珍しいキーワードだ！ | 珍しい単語ほど点数が高い |

**TF-IDFの点数 = TF（よく出る） × IDF（珍しい）**

つまり、「その本にはよく出てくるけれど、図書館全体で見るとあまり使われていない言葉」が、その本を最もよく表すキーワードとして高い点数を得る仕組みです。


下図は、テキストから **スパースな TF-IDF ベクトル** を作る前処理の流れです。

<img src="../../assets/units/unit17_nlp_preprocessing_tfidf/images/diagram-concept.svg" alt="図解：テキスト前処理の流れ" class="unit-diagram" />

### 📐 TF-IDFの基本数式

もう少しだけ踏み込んで、実際の計算式を見てみましょう。

- **TF（Term Frequency）** = 単語tの文書d内の出現回数 ÷ 文書dの総単語数
- **IDF（Inverse Document Frequency）** = log（総文書数 ÷ 単語tを含む文書数）

図書館の例で具体的に計算してみます。3冊の本があるとしましょう：

| 本 | 内容（前処理後の単語） |
| :--- | :--- |
| 本A | AI, 学習, AI, データ（4単語） |
| 本B | スポーツ, 試合, データ（3単語） |
| 本C | AI, プログラム, 関数（3単語） |

「 **AI** 」という単語の本Aでのスコアを計算すると：
- TF(AI, 本A) = 2 ÷ 4 = **0.50** （本Aの中で半分がAI）
- IDF(AI) = log(3 ÷ 2) ≈ **0.18** （3冊中2冊に出現→やや珍しい）
- **TF-IDF = 0.50 × 0.18 ≈ 0.09**

「 **データ** 」という単語の本Aでのスコアも計算すると：
- TF(データ, 本A) = 1 ÷ 4 = **0.25**
- IDF(データ) = log(3 ÷ 2) ≈ **0.18** （3冊中2冊に出現）
- **TF-IDF = 0.25 × 0.18 ≈ 0.05**

> 💡 このように、本Aの中では「AI」の方が「データ」よりも高いスコアを獲得します。出現頻度が高い単語ほど、その本を特徴づけるキーワードとして重視されるわけです。

> ⚠️ **補足：scikit-learn の実装との違い** : 上の手計算では話を簡単にするため常用対数（log10）を使いましたが、scikit-learn の `TfidfVectorizer` の実装では **自然対数（ln）** が使われます。さらに、ゼロ除算を防ぐための `smooth_idf`（分子・分母に1を加える平滑化）や、ベクトルの長さを揃える正規化などの調整が入るため、 **手計算の結果とライブラリの出力値は少し異なります** 。「計算の考え方は同じだが、実装上の工夫で数値がずれる」と理解しておけば大丈夫です。

### 💡 具体的なビジネスユースケース
- **カスタマーサポートの自動振り分け** : 顧客からの問い合わせメールの内容（テキスト）から特徴的なキーワードを抽出し、担当部署（営業、技術サポート、返品対応など）へ自動的にルーティングするシステム。
- **ニュースアプリの記事推薦** : ユーザーが過去に読んだ記事のTF-IDF特徴量と、新着記事の特徴量を比較し、興味を持ちそうなニュースを自動でレコメンドする機能。
- **社内文書の検索システム** : 大量の社内マニュアルや契約書の中から、社員が入力した検索キーワードに対して、最も関連性の高いドキュメントをスコアリングして上位表示するシステム。


下図は、 **TF（頻度）** と **IDF（希少性）** を掛け合わせて重要語を強調するイメージです。

<img src="../../assets/units/unit17_nlp_preprocessing_tfidf/images/diagram-workflow.svg" alt="図解：TF-IDF の考え方（頻度×希少性）" class="unit-diagram" />

## 2. 実装例 (Implementation Example)

ここでは、Pythonと`scikit-learn`を使って、簡単なニュース記事（テキストデータ）からTF-IDFを計算し、機械学習モデルで分類するまでの流れを実装します。

### コードの解説
これから書くコードは以下の順番で処理を行います。
1. **テキストの準備** : 分類したいテキストデータを用意します。
2. **前処理・特徴量抽出 (TF-IDF)** : `TfidfVectorizer` を使って、テキストを数値（特徴量）に変換します。この時、英語のストップワード（the, is, atなど）を自動で除外します。
3. **モデルの学習** : 変換された数値データを使って、記事がどのカテゴリに属するかを学習します。
4. **予測** : 新しいテキストがどのカテゴリになるかを予測します。

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# 1. データの準備（簡単なニュースのタイトル）
texts = [
    "Apple releases new iPhone with advanced camera",    # テクノロジー
    "Google announces new AI language model",            # テクノロジー
    "Real Madrid wins the Champions League final",       # スポーツ
    "NBA finals: Lakers defeat the Warriors",            # スポーツ
]
# ラベル（0: テクノロジー, 1: スポーツ）
labels = [0, 0, 1, 1]

# 2. TF-IDFを用いたベクトル化とモデル構築のパイプライン
# stop_words="english" で「the」「with」などの不要な単語を除外します
model = make_pipeline(
    TfidfVectorizer(stop_words="english"),
    MultinomialNB() # テキスト分類によく使われるナイーブベイズ分類器
)

# 3. モデルの学習
model.fit(texts, labels)
print("モデルの学習が完了しました！")

# 4. 新しいテキストで予測
new_texts = [
    "New smartphone features AI capabilities",
    "Who will win the basketball match tonight?"
]

# 予測を実行
predictions = model.predict(new_texts)

# 結果の表示
category_names = ["テクノロジー", "スポーツ"]
for text, pred in zip(new_texts, predictions):
    print(f"テキスト: '{text}' -> 予測カテゴリ: {category_names[pred]}")
```

### コード実行後の理解ポイント
上記のコードで `TfidfVectorizer` は裏側で以下を行っています：
- すべての文字を小文字に統一。
- "the", "with" などの重要でないストップワードを除去。
- 残った単語（Apple, iPhone, wins, matchなど）のTF-IDFスコアを計算。
初心者の方は、まずは「テキストがそのままでは計算できないため、TfidfVectorizerという魔法の箱を通すことで数値に変換されている」と理解してください。

## 3. 実践 (Practice)

今度はあなた自身で実装してみましょう。スパムメール（迷惑メール）を判定するシステムを作ります。

**【課題の要件】**
1. 以下のデータセットを使用してください。
2. `TfidfVectorizer` と `MultinomialNB` （または `LogisticRegression`） を使って分類モデルを構築してください。
3. `test_emails` の各メールが「スパム」か「正常」かを予測して出力してください。

**【データセット】**
```python
# 学習用データ
train_emails = [
    "Win a free iPhone right now! Click here",         # 1: スパム
    "Hey, are we still on for lunch tomorrow?",        # 0: 正常
    "Limited time offer! Buy one get one free",        # 1: スパム
    "Please find attached the meeting minutes",        # 0: 正常
    "Congratulations! You won a million dollars",      # 1: スパム
]
train_labels = [1, 0, 1, 0, 1]

# テスト用データ
test_emails = [
    "Click here to claim your free vacation",
    "Please send the meeting report by tomorrow"
]
```

**【ヒント】**
- `TfidfVectorizer(stop_words="english")` を使って無駄な単語を取り除きましょう。
- パイプライン（`make_pipeline`）を使うとスッキリ書けますが、別々に記述しても正解です。

## 4. 答え合わせ (Answer Key)

<details>
<summary>解答例を見る（クリックで展開）</summary>

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

# 学習用データ
train_emails = [
    "Win a free iPhone right now! Click here",
    "Hey, are we still on for lunch tomorrow?",
    "Limited time offer! Buy one get one free",
    "Please find attached the meeting minutes",
    "Congratulations! You won a million dollars",
]
train_labels = [1, 0, 1, 0, 1]

# テスト用データ
test_emails = [
    "Click here to claim your free vacation",
    "Please send the meeting report by tomorrow"
]

# モデルの作成（今回はロジスティック回帰を使用）
model = make_pipeline(
    TfidfVectorizer(stop_words="english"),
    LogisticRegression()
)

# 学習
model.fit(train_emails, train_labels)

# 予測
predictions = model.predict(test_emails)

# 結果の表示
label_map = {0: "正常 (Ham)", 1: "スパム (Spam)"}
for email, pred in zip(test_emails, predictions):
    print(f"メール: '{email}'\n-> 判定結果: {label_map[pred]}\n")
```

**解答の解説：**
「free」や「claim」、「won」といった単語がスパム（1）によく出現するため、TF-IDFによってそれらの単語に高いスコアがつけられます。その結果、新しいメールに「free」が含まれていると、モデルは「これはスパムである確率が高い」と正しく判断できます。一方、2通目には正常メール側の学習データに登場した「meeting」「tomorrow」が含まれているため、「正常」と判定されます。このように、極小データでは **テスト文に学習済みの単語が含まれているか** が判定を大きく左右する点も覚えておきましょう。

</details>
