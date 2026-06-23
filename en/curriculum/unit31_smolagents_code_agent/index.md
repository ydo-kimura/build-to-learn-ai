# Unit 31: smolagents and Autonomous AI Agents

> [!IMPORTANT]
> **Preparing Your OpenAI API Key**
> An **OpenAI API key** is required to continue Chapter 4. For how to obtain a key, billing considerations, and secure environment variable setup using Google Colab secrets, see [Appendix (Learning Environment and Key Setup)](../appendix/index.md#🔑-3-openai-api-key-acquisition-and-secure-management-chapter-4) first.

## 1. Understanding AI Agents and smolagents

<img src="../../../assets/units/unit31_smolagents_code_agent/images/concept.png" width="400" alt="Concept diagram">

In Units 27–28, you learned chaining and chatbot implementation. In Units 29–30, you studied the fundamentals of AI agents (scratch ReAct) and MCP (Model Context Protocol), a common open standard.

However, when an AI system does more than "output text as instructed" and instead **autonomously decides when and how to use external tools (search, databases, calculators, external APIs, etc.) to achieve complex user goals**, we call that system an **AI Agent**.

### Limitations of the Traditional ReAct Paradigm
Representative AI agent implementations (such as ReAct) followed a **text-based (JSON) reasoning loop** like this:

1. **Thought**: "I need to use the search tool next."
2. **Action**: Output JSON such as `{"tool": "Search", "query": "today's weather"}`.
3. **Observation**: Python parses the JSON, runs the tool, and returns the result to the LLM as text.

This approach is powerful, but it has a serious practical problem: **as loop count grows, the system becomes fragile**, and when the LLM handles multi-step data processing or complex calculations in text (for example, averaging five search results), **parse errors and reasoning drift are highly likely to break the pipeline**.

### smolagents and the Code Agent Revolution
To break through this limit, Hugging Face released the ultra-lightweight, state-of-the-art framework **`smolagents`**.

Instead of traditional text-based tool calling, `smolagents` introduces a design where **the LLM writes Python code to solve the task and executes it immediately in a secure sandbox to obtain results (Code Agent)**.

| Feature | Traditional Agent (ReAct) | smolagents (CodeAgent) |
| :--- | :--- | :--- |
| **Instruction format** | Text (JSON schema, etc.) | **Generated Python code** |
| **Complex data processing** | The LLM manages a loop of one tool call at a time (fragile). | Outputs Python such as "loop over the list and compute the average" and resolves it in one shot inside a container. |
| **Success rate & reasoning efficiency** | Low to medium (prompt collapse is common). | **Very high** (execution is handled reliably by the program). |
| **Code footprint** | Tends to grow (LangChain and others have complex setup). | **Extremely lightweight** (a robust agent runs in just a few lines). |

---

## 2. Implementation Example

Here, you build a lightweight agent with `smolagents` `CodeAgent` where the LLM **writes Python code on its own and autonomously combines the provided tools**.

Run `pip install smolagents openai` beforehand and set `OPENAI_API_KEY` in your environment variables.

```python
import os
from smolagents import CodeAgent, Tool, OpenAIServerModel

# 1. LLM model setup (using OpenAI API)
# gpt-4o-mini has strong code generation ability and works well as a CodeAgent
model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_key=os.environ.get("OPENAI_API_KEY")
)

# 2. Define custom tools the agent can use
# The function docstring becomes the tool description (instruction manual) for the agent
class TemperatureConverterTool(Tool):
    name = "convert_fahrenheit_to_celsius"
    description = "華氏（Fahrenheit）の温度を、摂氏（Celsius）に変換します。"
    inputs = {
        "fahrenheit": {
            "type": "number",
            "description": "変換したい華氏の温度数値"
        }
    }
    output_type = "number"

    def forward(self, fahrenheit: float) -> float:
        return (fahrenheit - 32) * 5 / 9

# 3. Instantiate the custom tool
temp_tool = TemperatureConverterTool()

# 4. Build the CodeAgent
# Pass the LLM and the list of available tools
agent = CodeAgent(
    tools=[temp_tool], 
    model=model,
    add_base_tools=True # Automatically add basic tools such as calculator and time
)

# 5. Instruct and run the agent
# The agent finds the Celsius conversion tool, writes code to call it, and executes it on the spot
print("--- smolagents (CodeAgent) 起動 ---")
task = "現在の華氏100度は、摂氏で何度ですか？小数点以下2桁で教えてください。"
result = agent.run(task)

print(f"\n最終回答:\n{result}")
```

---

## 3. Practice — 🧠 Compare and Decide Your Agent Paradigm

In AI agent development, maximize business success (robustness) by learning to decide **whether to adopt traditional ReAct (tool calling) or the latest Code Agent approach** from quantitative performance and safety perspectives.

**Assignment Requirements**

You are tasked with building an autonomous customer agent for an e-commerce site that **automatically calculates product discount rates and final prices**.

Compare the two approaches below and build the agent.

```python
# Task given by the user:
# 「商品Aの価格は12,000円です。これに対して『15%割引』のVIPクーポンを適用し、さらに『消費税10%』を加算した、お客様が実際に支払う最終価格を求めてください。」
```

**Your Mission: Compare Two Agent Approaches and Decide for Production**

Compare and analyze the design intent of the two approaches below, then decide which to apply as the production chat agent system.

1. **Approach A (Traditional text-based tool calling / ReAct agent)**
   * **Characteristics**: The LLM loops in text—"call the discount tool next → then call the tax tool"—parsing and advancing step by step.
2. **Approach B (smolagents Python code execution agent)**
   * **Characteristics**: The LLM generates simple Python such as "apply 15% discount to the price, then multiply by 1.10" in one shot and runs it in a sandbox to get the answer.

---

**Design Decision Notes to Record in Code Comments**

1. **smolagents final price calculation agent implementation**:
   * Use `smolagents` `CodeAgent` so the LLM generates and executes code for discount and tax calculations autonomously.
2. **Agent robustness (task success rate) comparison**:
   * Explain why CodeAgent approaches near-100% success while ReAct tends to drift between "apply discount" and "compute tax".
3. **Security and execution sandbox importance**:
   * Describe the role of smolagents' secure execution environment (LocalPythonInterpreter) and production security measures (blocking malicious code).
4. **Final adoption decision**:
   * **State which agent approach you adopt for production and why.**

---

## 4. Answer Key — 💡 Professional Agent Design Guidelines

<details>
<summary>View sample solution (click to expand)</summary>

### 💡 Agent Architecture Selection as an AI Engineer

Let's organize the trade-offs between ReAct and Code Agent.

#### Design Decision Matrix (Production Criteria)

| Evaluation Axis | Approach A (Traditional ReAct) | Approach B (smolagents CodeAgent) | Design Decision Point |
| :--- | :--- | :--- | :--- |
| **Task success (Robustness)** | **Low**. The LLM manages multi-tool order and intermediate calculations as text state transitions; longer tasks break easily. | **Very high**. The LLM focuses on writing logic (programs); Python executes reliably. | **smolagents wins**. For business agents with calculation and data processing, CodeAgent success rates dominate ReAct. |
| **Security risk** | Safer. The LLM only outputs text; Python runs predefined fixed functions. | **Mitigation required**. Malicious generated code (e.g., deleting system files) could run. | `smolagents` ships a secure interpreter with strict whitelists for functions and modules. |
| **Debuggability** | Hard. You must trace prompts to find where reasoning went wrong. | **Easy**. Generated Python appears in logs, so bugs are obvious. | Code-level debugging gives developers strong confidence when tracing and optimizing agents. |

---

### Reliable Price Calculation Agent with smolagents

```python
import os
from smolagents import CodeAgent, OpenAIServerModel

# 1. Decision:
# 「割引適用と税金計算といった『ロジックの連鎖』と『正確な数値処理』が求められるタスクにおいて、」
# 「従来のReActではプロンプト崩壊が起きやすいため、コード生成一撃で解決できる smolagents の CodeAgent を採用。」
# 「生成されたコードの実行は、標準のホワイトリスト制限されたセキュアなLocalPythonInterpreterで行う。」

model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Even without custom calculation tools, CodeAgent can run basic Python arithmetic
# (four operations and loops) using standard sandbox Python features alone
agent = CodeAgent(
    tools=[], 
    model=model,
    add_base_tools=True # Add basic arithmetic capability
)

print("--- 業務価格算出エージェント ---")
task = """
商品Aの価格は12,000円です。
これに対して『15%割引』のVIPクーポンを適用し、
さらに『消費税10%』を加算した、お客様が実際に支払う最終価格を求めてください。
"""

result = agent.run(task)
print(f"\n最終価格: {result}")
```

### 💡 Final Production Adoption Decision

* **Final decision**:
  * **Adopt Approach B (smolagents CodeAgent) for the production agent system.**
  * **Rationale**:
    1. **Overwhelming reliability (zero parse errors)**: ReAct required messy glue such as regex-parsing discount text before passing to tax calculation; CodeAgent generates `final_price = 12000 * 0.85 * 1.1` in one shot, eliminating intermediate prompt errors.
    2. **Fast debugging**: Audit logs record raw Python scripts, so when calculations are wrong, you can quickly identify which prompt wording skewed logic generation.
    3. **Security safety**: `smolagents` runs on a Local interpreter that blocks system access and dangerous imports (`os`, `subprocess`, etc.), so you get Code Agent power without practical vulnerabilities.
</details>
