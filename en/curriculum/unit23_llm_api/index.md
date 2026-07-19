# Unit 23: LLM API Usage and Prompt Engineering

<p class="unit-hero">
  <img src="/en/assets/units/unit23_llm_api/images/hero.png" alt="Hero: LLM API & Prompting" />
</p>

> [!IMPORTANT]
> **Preparing your OpenAI API key**
> Chapter 4 requires an **OpenAI API key**. For how to obtain a key, billing notes, and secure environment-variable setup with Google Colab secrets, read [Appendix (Learning Environment and API Setup)](../appendix/index.md#🔑-3-openai-api-key-acquisition-and-secure-management-chapter-4) first.

---

## 1. Understanding LLM API Usage & Prompting

<img src="/en/assets/units/unit23_llm_api/images/diagram-concept.svg" alt="Diagram: API call flow" class="unit-diagram" />



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

<img src="/en/assets/units/unit23_llm_api/images/diagram-workflow.svg" alt="Diagram: Prompt patterns" class="unit-diagram" />

## 2. Three Core Prompt Engineering Techniques

To control LLM output and get stable, intended answers in production, you need **prompt engineering**. Here are the three foundational techniques for all AI development.

### ① Zero-shot Prompting
* **Concept**: Give the LLM only task instructions (system message, etc.) and input—**no example answers (shots)**—the simplest approach.
* **Analogy**: A test where you get the real question with no practice—“Summarize this passage.”
* **Prompt example**:
  ```
  User input: "Classify the following smartphone review as positive or negative: The screen is large and easy to read, but it feels a bit heavy."
  ```
* **Pros**: Shortest prompts; minimum token cost.
* **Cons**: Hard to enforce complex formats or custom classification rules; answers vary more.

### ② Few-shot Prompting
* **Concept**: Include several **input–desired output pairs** in the prompt so the model learns the pattern in context before the real task.
* **Analogy**: Show example Q&A sets before the exam—“Now solve this problem.”
* **Prompt example**:
  ```
  Instruction: "Classify the sentiment of the input text with exactly one tag: [Positive] or [Negative]."
  Example input 1: "Delivery was very fast and helpful!" -> Example output 1: "[Positive]"
  Example input 2: "The buttons respond poorly and it freezes sometimes." -> Example output 2: "[Negative]"
  
  Production input: "The design is cute, but battery life is disappointing."
  ```
* **Why few-shot?**: Text-only instructions like “always output `[Positive]` in brackets” sometimes fail (“The sentiment is positive.”). **Examples strongly mimic format and tone**, improving format compliance.

### ③ Chain-of-Thought (CoT) Prompting
* **Concept**: Instead of jumping to the answer, prompt the LLM to **output reasoning steps in order**. Often triggered by “Think step by step” (Zero-shot CoT).
* **Analogy**: “Show all intermediate steps,” not “answer only”—like math where showing work reduces errors.
* **Prompt example**:
  ```
  Instruction: "Solve the following math problem step by step, showing your reasoning at each stage."
  Problem: "You have 5 apples. You ate 2. Then you bought 3 packs of 3 apples each. How many apples do you have now?"
  ```
  * *Without CoT*: “10 apples” (mental shortcut, misses ×3).
  * *With CoT*:
    > 1. Initially there were 5 apples.
    > 2. After eating 2, the remainder is 5 - 2 = 3 apples.
    > 3. Next, buying 3 packs of 3 adds 3 x 3 = 9 apples.
    > 4. Therefore the final total is 3 + 9 = 12 apples. Answer: 12 apples.
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

# 1. Prepare API client
# Loading the API key from environment variables is the safe approach
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 2. Create the prompt (instruction sheet)
# system: specify the AI's "role" and "context"
# user: specify your "concrete question or request"
messages = [
    {"role": "system", "content": "You are a programming instructor who teaches beginners kindly."},
    {"role": "user", "content": "What is an API? Explain it so an elementary school student can understand."}
]

# 3. Send a request to the AI (LLM)
response = client.chat.completions.create(
    model="gpt-4o-mini", # model name to use
    messages=messages,   # prompt created above
    temperature=0.7      # response "creativity" (closer to 0 = more precise, closer to 1 = more creative)
)

# 4. Extract and display the answer text
# The response object contains various metadata; extract only the message text
print("AI answer:")
print(response.choices[0].message.content)
```

### Extension: inspect input token count

Measuring tokens before sending a request helps estimate context usage and approximate cost. This calls a model tokenizer; it does not implement the tokenizer internals.

```python
import tiktoken

text = "LLMs split text into tokens before processing it."

try:
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
except KeyError:
    encoding = tiktoken.get_encoding("cl100k_base")

token_ids = encoding.encode(text)
print("Characters:", len(text))
print("Tokens:", len(token_ids))
print("First token IDs:", token_ids[:10])
```

Compare English, Japanese, and code inputs. Character count and token count are not always proportional. For exact billing and model support, check the current model documentation.

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
- Return value: have the AI classify as “Positive”, “Negative”, or “Neutral” and return **only that word** as a string (e.g., `"Positive"`).

**💡 Hint**
- In `system`, strongly instruct: “You are a sentiment analysis system. Output exactly one of Positive, Negative, or Neutral. No extra explanation.”

### Extension: streaming responses

After completing the sentiment-analysis exercise, change the API call to streaming mode.

**Requirements**
- Set `stream=True` and print each received chunk as it arrives.
- Join all chunks into a final result.
- Compare time-to-first-output and implementation differences with a normal response.
- Do not treat an interrupted response as a completed business result.

Streaming can make output appear sooner, but it does not guarantee correctness or safety.

---

## 5. Answer Key

<details>
<summary>View sample solution (click to expand)</summary>

```python
import os
from openai import OpenAI

def analyze_sentiment(text):
    # Initialize client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Prompt with detailed role and instructions
    messages = [
        {
            "role": "system", 
            "content": "You are an excellent sentiment analysis assistant. For each user input, respond with exactly one word: Positive, Negative, or Neutral. Do not include explanations or punctuation."
        },
        {
            "role": "user", 
            "content": text
        }
    ]
    
    # Send request to API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.0 # use 0 for accuracy-critical tasks like sentiment analysis
    )
    
    # Return only the result text
    return response.choices[0].message.content

# Test run
if __name__ == "__main__":
    test_review_1 = "This product is amazing! It changed my life."
    print(f'"{test_review_1}" -> {analyze_sentiment(test_review_1)}')
    
    test_review_2 = "It broke immediately. Terrible."
    print(f'"{test_review_2}" -> {analyze_sentiment(test_review_2)}')
```
</details>

### Extension answer: streaming response

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explain AI in one sentence."}],
    stream=True,
)

chunks = []
try:
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
        chunks.append(content)
    final_text = "".join(chunks)
    print("\n\nFinal result:", final_text)
except Exception as exc:
    print(f"\nStreaming did not complete: {exc}")
```

If an exception occurs, do not save `final_text` as a confirmed business response.
