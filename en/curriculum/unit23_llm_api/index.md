# Unit 23: LLM API Usage and Prompt Engineering

> [!IMPORTANT]
> **Preparing your OpenAI API key**
> Chapter 4 requires an **OpenAI API key**. For how to obtain a key, billing notes, and secure environment-variable setup with Google Colab secrets, read [Appendix (Learning Environment and API Setup)](../appendix/index.md#🔑-3-openai-api-key-acquisition-and-secure-management-chapter-4) first.

---

## 1. Understanding LLM API Usage & Prompting

<img src="../../../assets/units/unit23_llm_api/images/concept.png" width="400" alt="Concept diagram" style="display:none;">

### What is an LLM API?
You probably open a browser and type when using ChatGPT. But to embed AI in your own apps and systems, a human cannot type every time.

That is where **API (Application Programming Interface)** comes in.
An API is like **“a gateway between programs.”**

**💡 Everyday analogy: restaurant ordering system**
- **Browser ChatGPT**: You talk directly to the waiter (AI) to order food (answers).
- **API ChatGPT**: Your phone ordering app (your Python program) sends digital orders directly to the kitchen (AI server).

| Comparison | Browser (Web UI) | API |
| :--- | :--- | :--- |
| **User** | Human | Program (Python, etc.) |
| **Purpose** | Personal Q&A and tasks | Automation, embedding in custom apps |
| **Customization** | Limited | Fine control (temperature/randomness, etc.) |
| **Billing** | Often monthly subscription | Often pay-as-you-go |

### What is prompting?
The “instruction sheet” you send to the AI through the API.
AI is smart but poor at “reading the room,” so you must specify **role**, **format**, and **priorities** concretely.

### 💡 Concrete business use cases
- **Customer support automation**: Link company FAQ database to the API for 24/7 first-line automated responses.
- **Sales material generation**: Pass customer info and meeting notes to generate personalized proposal drafts and email copy instantly.
- **Internal document summarization and translation**: Automatically summarize and translate overseas reports and long meeting minutes to speed internal sharing.

---

## 2. Three Core Prompt Engineering Techniques

To control LLM output and get stable, intended answers in production, you need **prompt engineering**. Here are the three foundational techniques for all AI development.

### ① Zero-shot Prompting
* **Concept**: Give the LLM only task instructions (system message, etc.) and input—**no example answers (shots)**—the simplest approach.
* **Analogy**: A test where you get the real question with no practice—“Summarize this passage.”
* **Prompt example**:
  ```
  ユーザー入力: "次のスマートフォンのレビューを、ポジティブかネガティブで分類してください：画面が大きくて見やすいが、少し重たい。"
  ```
* **Pros**: Shortest prompts; minimum token cost.
* **Cons**: Hard to enforce complex formats or custom classification rules; answers vary more.

### ② Few-shot Prompting
* **Concept**: Include several **input–desired output pairs** in the prompt so the model learns the pattern in context before the real task.
* **Analogy**: Show example Q&A sets before the exam—“Now solve this problem.”
* **Prompt example**:
  ```
  指示: "入力された文章の感情を、[ポジティブ] または [ネガティブ] のいずれか1つのタグで答えてください。"
  入力例1: "配送がとても早くて助かりました！" -> 出力例1: "[ポジティブ]"
  入力例2: "ボタンの反応が悪く、たまにフリーズします。" -> 出力例2: "[ネガティブ]"
  
  本番入力: "デザインは可愛いけれど、充電の持ちがイマイチです。"
  ```
* **Why few-shot?**: Text-only instructions like “always output `[ポジティブ]` in brackets” sometimes fail (“The sentiment is positive.”). **Examples strongly mimic format and tone**, improving format compliance.

### ③ Chain-of-Thought (CoT) Prompting
* **Concept**: Instead of jumping to the answer, prompt the LLM to **output reasoning steps in order**. Often triggered by “Think step by step” (Zero-shot CoT).
* **Analogy**: “Show all intermediate steps,” not “answer only”—like math where showing work reduces errors.
* **Prompt example**:
  ```
  指示: "次の数学の問題を、段階的に順を追って考えながら解いてください。"
  問題: "リンゴが5個あります。2個食べました。その後、3個入りのパックを3つ買いました。今リンゴは何個ですか？"
  ```
  * *Without CoT*: “10 apples” (mental shortcut, misses ×3).
  * *With CoT*:
    > 1. 最初にリンゴが 5 個ありました。
    > 2. 2 個食べたので、残りは 5 - 2 = 3 個になります。
    > 3. 次に、3個入りのパックを 3 つ買ったので、新しく増えたリンゴは 3 × 3 = 9 個です。
    > 4. よって、最終的な合計は 3 + 9 = 12 個になります。答：12個。
* **Why accuracy improves**: LLMs predict the next token probabilistically. Forcing one-shot answers lets one early mistake collapse the chain. CoT lets the model **use its own prior reasoning text as context** for the next step—dramatically improving complex math and logic.

---

### 📊 Prompt technique selection matrix

Choose techniques by task difficulty in production systems.

| Technique | Suitable tasks | Dev cost | Token cost (billing) | Output stability |
| :--- | :--- | :--- | :--- | :--- |
| **Zero-shot** | Simple translation, rough summarization, general Q&A | Very low | Very cheap | Low–medium |
| **Few-shot** | Strict JSON output, domain-specific sentiment tags, length control | Low (just prepare examples) | Medium | Very high |
| **Chain-of-Thought** | Math, complex legal/business logic, multi-condition reasoning | Low–medium | High (reasoning length) | Very high |

---

## 3. Implementation Example

Use OpenAI’s API—the most widely used worldwide—to ask the AI a question from Python.

> ※ Run `pip install openai` first and obtain an OpenAI API key.

```python
import os
from openai import OpenAI

# 1. APIクライアントの準備
# APIキーは環境変数から読み込むのが安全です
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 2. プロンプト（指示書）の作成
# system: AIの「役割」や「前提条件」を指定します
# user: あなたからの「具体的な質問やお願い」を指定します
messages = [
    {"role": "system", "content": "あなたは初心者向けに優しく教えるプログラミング講師です。"},
    {"role": "user", "content": "APIとは何ですか？小学生にもわかるように説明してください。"}
]

# 3. AI（LLM）に注文（リクエスト）を送る
response = client.chat.completions.create(
    model="gpt-4o-mini", # 使用するAIのモデル名
    messages=messages,   # 先ほど作成したプロンプト
    temperature=0.7      # 回答の「創造性」（0に近いほど正確、1に近いほど自由な発想）
)

# 4. 返ってきた回答を取り出して表示する
# responseの中には様々なデータが含まれているので、文章の部分だけを抽出します
print("AIの回答:")
print(response.choices[0].message.content)
```

**🔍 Detailed code walkthrough**
1. **API client setup**: `OpenAI` class sets your API key—like an ID proving you can pay for orders.
2. **Prompt creation**: Put conversation history in the `messages` list as dicts. `system` sets persona (“friendly teacher”); `user` asks the question.
3. **Send request**: `client.chat.completions.create` performs the call. `model` picks capability/speed; `temperature` adjusts randomness/creativity.
4. **Extract answer**: The API returns a large object with metadata. Follow `response.choices[0].message.content` for the text only.

---

## 4. Practice

Now that you know the API, build a function for **sentiment analysis**.

**【Requirements】**
- Function name: `analyze_sentiment(text)`
- Argument `text`: review string (product review, etc.).
- Return value: have the AI classify as “ポジティブ”, “ネガティブ”, or “ニュートラル” and return **only that word** as a string (e.g., `"ポジティブ"`).

**💡 Hint**
- In `system`, strongly instruct: “You are a sentiment analysis system. Output exactly one of 『ポジティブ』, 『ネガティブ』, or 『ニュートラル』. No extra explanation.”

---

## 5. Answer Key

<details>
<summary>View sample solution (click to expand)</summary>

```python
import os
from openai import OpenAI

def analyze_sentiment(text):
    # クライアントの初期化
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # 役割と指示を細かく設定したプロンプト
    messages = [
        {
            "role": "system", 
            "content": "あなたは優秀な感情分析アシスタントです。ユーザーの入力に対して、「ポジティブ」「ネガティブ」「ニュートラル」のいずれか1つの単語のみで答えてください。説明や句読点も含めないでください。"
        },
        {
            "role": "user", 
            "content": text
        }
    ]
    
    # APIへリクエスト
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.0 # 感情分析のように正確性が求められるタスクは0にするのがコツです
    )
    
    # 結果のテキストだけを返す
    return response.choices[0].message.content

# テスト実行
if __name__ == "__main__":
    test_review_1 = "この商品は最高です！人生が変わりました。"
    print(f"「{test_review_1}」 -> {analyze_sentiment(test_review_1)}")
    
    test_review_2 = "すぐに壊れてしまいました。最悪です。"
    print(f"「{test_review_2}」 -> {analyze_sentiment(test_review_2)}")
```
</details>
