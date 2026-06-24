# Unit 17: NLP Preprocessing and TF-IDF

<p class="unit-hero">
  <img src="../../../assets/units/unit17_nlp_preprocessing_tfidf/images/hero.png" alt="Hero: NLP Preprocessing & TF-IDF" />
</p>



## 1. Understanding NLP Preprocessing and TF-IDF

<img src="../../../assets/units/unit17_nlp_preprocessing_tfidf/images/diagram-concept.svg" alt="Diagram: Text preprocessing" class="unit-diagram" />



The first step in getting computers to understand human language is **"cleaning up text and converting it into a list of numbers (vectors)."**

### 📌 Everyday analogy: classifying books in a library
Imagine you are a librarian deciding how to classify new books. You look at the **words** inside:
- Many occurrences of "apple," "orange," "banana" → "Fruit"
- "function," "variable," "compile" → "Programming"

But every book also contains "this," "that," "is," "are" (**stop words**) that do not characterize the book.
Also, "run," "ran," "running" refer to the same action (**stemming/lemmatization** extracts the root).

**NLP preprocessing** is the librarian's work of **removing noise and normalizing words** to capture what makes each text distinctive.

### 📝 Column: Japanese NLP preprocessing

English text is space-separated, so computers easily know word boundaries. Japanese does not: 「私は今日図書館に行きました」 has no spaces between words.

So the first step in Japanese NLP is **morphological analysis (tokenization / word segmentation)**—splitting text into minimal meaningful units (morphemes).

Example: 「私は今日図書館に行きました」 → 「私 / は / 今日 / 図書館 / に / 行き / まし / た」

Popular libraries include **MeCab** (fast, rich dictionaries) and **Janome** (pure Python, easy setup). With Janome, segmentation takes just a few lines:

```python
from janome.tokenizer import Tokenizer
t = Tokenizer()
japanese_text = "\u79c1\u306f\u4eca\u65e5\u56fe\u66f8\u9928\u306b\u884c\u304d\u307e\u3057\u305f"
tokens = [token.surface for token in t.tokenize(japanese_text)]
print(tokens)  # Morpheme list from morphological analysis
```

Differences between English and Japanese preprocessing flows:

| Step | English | Japanese |
| :--- | :--- | :--- |
| **Word splitting** | Split on spaces | Morphological analysis (MeCab / Janome) |
| **Case normalization** | Needed (Apple → apple) | Not needed (no case distinction) |
| **Stop word removal** | the, is, at, etc. | は, が, の, です, ます, etc. |
| **Stem extraction** | Stemming / lemmatization | Base forms from morphological analysis |

> 💡 In the library analogy, English books arrive already space-separated; Japanese arrives like a scroll with every character packed together—the librarian must cut it into words first (morphological analysis).

### 📌 What is TF-IDF?
After preprocessing, **TF-IDF** (Term Frequency–Inverse Document Frequency) scores how important each word is.

| Component | Meaning | Library analogy | Computation intuition |
| :--- | :--- | :--- | :--- |
| **TF (term frequency)** | How often a word appears in one document | "The word AI appears a lot in this book!" | Higher frequency → higher score |
| **IDF (inverse document frequency)** | How rare the word is across all documents | "AI rarely appears in other books—a distinctive keyword!" | Rarer words → higher score |

**TF-IDF score = TF (frequent locally) × IDF (rare globally)**

Words that appear often in one book but rarely in the whole library become the keywords that best represent that book.

### 📐 Basic TF-IDF formulas

A bit more formally:

- **TF (Term Frequency)** = count of term t in document d ÷ total word count in document d
- **IDF (Inverse Document Frequency)** = log(total documents ÷ documents containing term t)

Example with three books:

| Book | Content (after preprocessing) |
| :--- | :--- |
| Book A | AI, learning, AI, data (4 words) |
| Book B | sports, game, data (3 words) |
| Book C | AI, program, function (3 words) |

Score for "**AI**" in Book A:
- TF(AI, Book A) = 2 ÷ 4 = **0.50**
- IDF(AI) = log(3 ÷ 2) ≈ **0.18**
- **TF-IDF = 0.50 × 0.18 ≈ 0.09**

Score for "**data**" in Book A:
- TF(data, Book A) = 1 ÷ 4 = **0.25**
- IDF(data) = log(3 ÷ 2) ≈ **0.18**
- **TF-IDF = 0.25 × 0.18 ≈ 0.05**

> 💡 In Book A, "AI" scores higher than "data" because local frequency matters—frequent words characterize the document.

### 💡 Concrete Business Use Cases
- **Automated customer support routing**: Extract distinctive keywords from inquiry emails and route to the right team (sales, technical support, returns).
- **News article recommendations**: Compare TF-IDF features of articles the user read with new articles to recommend relevant news.
- **Enterprise document search**: Score internal manuals and contracts against search keywords and rank the most relevant documents.

<img src="../../../assets/units/unit17_nlp_preprocessing_tfidf/images/diagram-workflow.svg" alt="Diagram: TF-IDF" class="unit-diagram" />

## 2. Implementation Example

Here you will use Python and `scikit-learn` to compute TF-IDF on simple news headlines and train a classifier.

### Code walkthrough
The code below follows this order:
1. **Prepare text**: Classification targets.
2. **Preprocess and extract features (TF-IDF)**: `TfidfVectorizer` converts text to numbers and removes English stop words (the, is, at, etc.).
3. **Train model**: Learn category labels from numeric features.
4. **Predict**: Classify new text.

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# 1. Prepare data (simple news headlines)
texts = [
    "Apple releases new iPhone with advanced camera",    # Technology
    "Google announces new AI language model",            # Technology
    "Real Madrid wins the Champions League final",       # Sports
    "NBA finals: Lakers defeat the Warriors",            # Sports
]
# Labels (0: Technology, 1: Sports)
labels = [0, 0, 1, 1]

# 2. Pipeline: TF-IDF vectorization + classifier
# stop_words="english" removes words like "the" and "with"
model = make_pipeline(
    TfidfVectorizer(stop_words="english"),
    MultinomialNB() # Naive Bayes classifier common for text
)

# 3. Train the model
model.fit(texts, labels)
print("Model training complete!")

# 4. Predict on new text
new_texts = [
    "New smartphone features AI capabilities",
    "Who will win the basketball match tonight?"
]

# Run predictions
predictions = model.predict(new_texts)

# Display results
category_names = ["Technology", "Sports"]
for text, pred in zip(new_texts, predictions):
    print(f"Text: '{text}' -> Predicted category: {category_names[pred]}")
```

### Key takeaways after running the code
`TfidfVectorizer` behind the scenes:
- Lowercases all text.
- Removes unimportant stop words like "the" and "with."
- Computes TF-IDF scores for remaining words (Apple, iPhone, wins, match, etc.).
Beginners can start with: **text cannot be computed directly—pass it through the TfidfVectorizer "magic box" to get numbers.**

## 3. Practice

Build your own spam email classifier.

**【Requirements】**
1. Use the dataset below.
2. Build a classifier with `TfidfVectorizer` and `MultinomialNB` (or `LogisticRegression`).
3. Predict whether each email in `test_emails` is spam or legitimate.

**【Dataset】**
```python
# Training data
train_emails = [
    "Win a free iPhone right now! Click here",         # 1: Spam
    "Hey, are we still on for lunch tomorrow?",        # 0: Ham
    "Limited time offer! Buy one get one free",        # 1: Spam
    "Please find attached the meeting minutes",        # 0: Ham
    "Congratulations! You won a million dollars",      # 1: Spam
]
train_labels = [1, 0, 1, 0, 1]

# Test data
test_emails = [
    "Click here to claim your free vacation",
    "Don't forget to submit your report by Friday"
]
```

**【Hints】**
- Use `TfidfVectorizer(stop_words="english")` to drop noise words.
- `make_pipeline` keeps code tidy, but separate steps are fine too.

## 4. Answer Key

<details>
<summary>View sample solution (click to expand)</summary>

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

# Training data
train_emails = [
    "Win a free iPhone right now! Click here",
    "Hey, are we still on for lunch tomorrow?",
    "Limited time offer! Buy one get one free",
    "Please find attached the meeting minutes",
    "Congratulations! You won a million dollars",
]
train_labels = [1, 0, 1, 0, 1]

# Test data
test_emails = [
    "Click here to claim your free vacation",
    "Don't forget to submit your report by Friday"
]

# Build model (Logistic Regression this time)
model = make_pipeline(
    TfidfVectorizer(stop_words="english"),
    LogisticRegression()
)

# Train
model.fit(train_emails, train_labels)

# Predict
predictions = model.predict(test_emails)

# Display results
label_map = {0: "Ham", 1: "Spam"}
for email, pred in zip(test_emails, predictions):
    print(f"Email: '{email}'\n-> Classification: {label_map[pred]}\n")
```

**Solution explanation:**
Words like "free," "claim," and "won" appear often in spam (label 1), so TF-IDF assigns them high scores. New emails containing "free" are then correctly classified as likely spam.

</details>
