# Unit 27: Stepwise Reasoning Through Prompt Chaining

<p class="unit-hero">
  <img src="/en/assets/units/unit27_prompt_chaining/images/hero.png" alt="Hero: Prompt Chaining" />
</p>

> [!IMPORTANT]
> **OpenAI API key setup**
> This unit uses the OpenAI API. See [Appendix (Learning Environment and API Setup)](../appendix/index.md#🔑-3-openai-api-key-acquisition-and-secure-management-chapter-4) for secure key configuration.

## 1. Understanding Prompt Chaining

<img src="/en/assets/units/unit27_prompt_chaining/images/diagram-concept.svg" alt="Diagram: Chain of prompts" class="unit-diagram" />

### What is prompt chaining?

When asking the AI to do complex work, one big question often confuses it and fails.
**Split processing into small steps and pass each step’s output to the next**—that is prompt chaining.

**💡 Everyday analogy: factory assembly line**
Instead of one craftsperson doing everything:

1. **Worker A (AI-1)** peels apples.
2. **Worker B (AI-2)** receives peeled apples and dices them.
3. **Worker C (AI-3)** receives diced apples and cooks jam.
   Each person’s output becomes the next person’s input—a relay.

### Building on Unit 25: chaining with LCEL

Unit 25 taught single chains as `prompt | model | parser`.

The essence of prompt chaining is **linking multiple independent chains with `|` for a data relay**.

Example: chain 1 (topic → catchphrase) and chain 2 (catchphrase → tweet):

| Step                       | Data flow image                                    | LCEL expression                    |
| :------------------------- | :------------------------------------------------- | :--------------------------------- |
| **Topic input**            | User enters topic                                  | `{"topic": "sample topic"}`        |
| **First chain (Chain 1)**  | Topic → catchphrase                                | `chain1 = prompt1                  | llm     | parser` |
| **Relay**                  | Map Chain 1 output to key `ad_copy` for next input | `{"ad_copy": chain1}`              |
| **Second chain (Chain 2)** | Catchphrase → final tweet                          | `final_chain = {"ad_copy": chain1} | prompt2 | llm     | parser` |

LangChain’s `|` is not just part wiring—it **treats whole chains as input sources** and streams them into the next chain.

### 💡 Concrete business use cases

- **Marketing content pipeline**: Target + appeal point → ① catchphrase → ② blog outline → ③ section drafts → ④ SNS promo copy.
- **Hierarchical long-report summarization**: ① chapter summaries → ② full summary → ③ three-bullet executive summary.
- **Customer feedback deep analysis**: ① sentiment → ② categorize negatives → ③ improvement plans per category.

<img src="/en/assets/units/unit27_prompt_chaining/images/diagram-workflow.svg" alt="Diagram: Why chain" class="unit-diagram" />

## 2. Implementation Example

Build a two-step LCEL chain:

- **Step 1**: Generate a catchphrase from a given topic.
- **Step 2**: Write a promotional tweet using that catchphrase.

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Prepare LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
# Utility to extract clean string output
output_parser = StrOutputParser()

# =========================================
# Chain 1: Generate a catchphrase
# =========================================
prompt1 = ChatPromptTemplate.from_template(
    "Write one compelling catchphrase for the topic '{topic}'."
)
# Use | (pipe) to connect prompt -> LLM -> string extraction
chain1 = prompt1 | llm | output_parser

# =========================================
# Chain 2: Create a tweet
# =========================================
prompt2 = ChatPromptTemplate.from_template(
    "Using the catchphrase below, write a promotional tweet for social media. Include hashtags.\n\nCatchphrase: {catchphrase}"
)
chain2 = prompt2 | llm | output_parser

# =========================================
# Combine into a prompt chain
# =========================================
# {"catchphrase": chain1} passes chain1 output automatically as "catchphrase" to chain2
overall_chain = {"catchphrase": chain1} | chain2

# Run
topic = "flying sneakers"
print(f"Topic: {topic}\n")

print("Running chain...")
result = overall_chain.invoke({"topic": topic})

print("\n[Final result: promotional tweet]")
print(result)
```

**🔍 Detailed code walkthrough**

1. **Parts**: LLM and `StrOutputParser` for clean text output.
2. **Chain 1**: `prompt1` takes `{topic}` and generates catchphrase via `|`.
3. **Chain 2**: `prompt2` takes `{catchphrase}` and generates tweet.
4. **Combine**: `{"catchphrase": chain1} | chain2` runs chain1 first and passes result as `catchphrase` to chain2.

## 3. Practice

Build a **three-step** prompt chain.

**【Topic: automated blog article pipeline】**

1. **Step 1**: From theme `{topic}`, generate a **blog title**.
2. **Step 2**: From title `{title}`, generate an **outline (table of contents)**.
3. **Step 3**: Using `{title}` and `{outline}`, write the **introduction (lead paragraph)**.

**💡 Hint**

- `RunnablePassthrough` can forward variables, but you can also wire with dictionaries.
- Final step may look like `{"title": chain1, "outline": chain2_that_uses_title}`—try LangChain’s powerful chaining syntax.

## 4. Answer Key

<details>
<summary>View sample solution (click to expand)</summary>

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
parser = StrOutputParser()

# 1. Title generation chain
prompt_title = ChatPromptTemplate.from_template("Write one compelling blog title for the theme '{topic}'.")
chain_title = prompt_title | llm | parser

# 2. Outline generation chain
prompt_outline = ChatPromptTemplate.from_template("Create a 3-chapter outline (table of contents) for a blog post titled '{title}'.")
chain_outline = prompt_outline | llm | parser

# 3. Introduction generation chain
prompt_intro = ChatPromptTemplate.from_template("""
Write an engaging introduction (lead paragraph) of about 200 words for a blog post with the title and outline below.

Title: {title}
Outline:\n{outline}
""")
chain_intro = prompt_intro | llm | parser

# =========================================
# Advanced chain composition (using RunnablePassthrough)
# =========================================
# RunnablePassthrough.assign keeps existing input (title here) while adding a new variable (outline).

overall_chain = (
    # Receive {"topic": "..."} and add title variable
    {"title": chain_title}
    # Keep {"title": "..."} and add outline variable
    | RunnablePassthrough.assign(outline=chain_outline)
    # Pass {"title": "...", "outline": "..."} to chain_intro
    | chain_intro
)

# Run
result = overall_chain.invoke({"topic": "Growing houseplants for beginners"})

print("[Generated introduction]")
print(result)
```

</details>
