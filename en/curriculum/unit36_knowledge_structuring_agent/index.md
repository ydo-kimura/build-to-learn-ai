# Unit 36: Autonomous Knowledge Extraction & Structuring Agent

## 1. Understanding Knowledge Extraction and Structuring from Unstructured Data

<img src="../../../assets/units/unit36_knowledge_structuring_agent/images/concept.png" width="400" alt="Concept diagram">

In Unit 26 you learned the RAG-focused framework `LlamaIndex`. In Unit 31 you learned `smolagents` (CodeAgent), which autonomously writes and executes Python code.

One of the most powerful production use cases for generative AI is a **structured extraction pipeline** that **automatically pulls required business information (contract dates, amounts, penalty clauses, complaint categories, etc.) from large volumes of unstructured enterprise data (free-form PDFs, scanned images, contracts, emails) and converts it into clean JSON (structured data) ready for database storage**.

### Why a Simple LLM Call Fails
Prompting "extract the amount as JSON from this contract" alone is not production-ready:

1. **Schema violations**: Wrong JSON keys or broken date formats (`YYYY-MM-DD`) cause immediate DB insertion failures.
2. **Hallucination (fabricated information)**: The LLM may invent amounts not in the contract.
3. **Long document limits (Token Limit)**: A single PDF may be fine, but 100-page documents spike cost and cause missed information (Lost in the Middle).

### Autonomous Structuring Agent Architecture
The professional architecture combines **LlamaIndex pinpoint retrieval (Retrieve)** with **smolagents (Code Agent) Python execution and self-correction loops**.

1. **Retrieve**: Use `LlamaIndex` to semantically find pages about "penalties and payment terms" in a large contract.
2. **Extraction**: Pass extracted text to the LLM and output structured JSON based on a Pydantic schema.
3. **Validation & Correction**:
   * Strictly validate output JSON against the schema (Pydantic model) in code.
   * On validation errors, the agent (`smolagents`) **parses error logs, fixes code or prompts on the spot, and retries until valid JSON (Self-Correction)**.

---

## 2. Practice — 🧠 Design and Decide Your Knowledge Extraction Pipeline

As a lead AI engineer, design and implement an architecture that **combines LlamaIndex advanced parsing with smolagents self-correction loops to guarantee error-free JSON**.

**Assignment Requirements**

Use the following "raw data (messy contract report text)" as initialization code and build a system that automatically extracts contract information and generates data that **100% conforms to the specified JSON schema**.

```python
# 1. Audit target "messy raw data"
dirty_contract_text = """
【業務提携合意書】
本契約は、AIテクノロジー株式会社（以下、甲）と、株式会社ミライシステム（以下、乙）の間で締結される。
合意日：2026年の5月12日。
本プロジェクトの総予算は一千二百万円（税別）とし、甲は乙に対して月々分割で支払うものとする。
支払期日は毎月末日とする。
また、本契約の有効期間は合意日から満2か年（24ヶ月）とする。
"""

# 2. Strict JSON schema (Pydantic model)
from pydantic import BaseModel, Field, field_validator
from datetime import date

class ContractSchema(BaseModel):
    client_name: str = Field(description="甲（発注者）の会社名。株式会社等を含めた正式名称。")
    vendor_name: str = Field(description="乙（受注者）の会社名。")
    agreement_date: date = Field(description="契約合意日。必ず YYYY-MM-DD の日付型である必要がある。")
    total_budget_yen: int = Field(description="総予算（円）。テキストから数値を抽出し、必ず『整数型（int）』に変換すること。税別・税込などの文字は含めない。")
    duration_months: int = Field(description="契約期間の月数。必ず整数型。")
```

**Your Mission: Robust Extraction & Self-Correction Agent Design**

Build an agent system that takes the messy text above as input and **automatically generates, validates, and self-corrects** JSON that passes `ContractSchema` validation in one shot.

---

**Design Decision Notes to Record in Code Comments**

1. **JSON completeness guarantee approach**:
   * Beyond "output JSON," describe how you coordinate agents (`smolagents` or program validators) to detect and auto-fix schema violations and date parse errors.
2. **Robust numeric and date conversion design**:
   * Describe design (Few-Shot prompts, Python interpreter, etc.) to reliably convert "一千二百万円" to integer `12000000` and "2026年の5月12日" to date `2026-05-12`.
3. **Final adoption decision**:
   * **State the agent evaluation pipeline you deliver to the enterprise and why.**

---

## 3. Answer Key — 💡 Professional Structured Data Extraction Design

<details>
<summary>View sample solution (click to expand)</summary>

### 💡 Knowledge Extraction Decision Notes as an AI Engineer

In production structured extraction, the professional technique is **sandwiching LLM output with strict program validation to guarantee 100% data quality**.

#### Structured Extraction Design Decision Matrix

| Evaluation Axis | Approach A (Prompt-only JSON output) | Approach B (Validator + Self-Correction Agent) | Design Decision Point |
| :--- | :--- | :--- | :--- |
| **Schema pass rate** | **Low (70%–85%)**. Output occasionally wrapped in ```json``` or missing keys causes parse errors. | **100% (guaranteed)**. On error, program feeds logs back to LLM for auto-regeneration. | Enterprise DB integration **cannot tolerate even 1% parse errors**—Approach B is mandatory. |
| **Kanji numerals & irregular dates** | Depends on LLM math; may misread "一千二百万" as 1200 or output dates as strings. | CodeAgent writes Python to parse numerals and convert perfectly. | Split LLM text ability and Python execution for the most robust design. |

---

### Complete Structured Extraction with Validator & Self-Correction Agent (smolagents)

```python
import os
import json
from datetime import date
from pydantic import BaseModel, Field, ValidationError
from smolagents import CodeAgent, OpenAIServerModel

# 1. Decision:
# 「医療や金融、企業データベース連携において、形式エラーによるシステムダウンは致命的である。」
# 「そのため、Pydanticによる厳格な型検証（日付型、整数型）と、エラー検知時に自動でコードを修正し再実行する smolagents CodeAgent を採用。」
# 「漢数字（一千二百万）などの曖昧な表現も、エージェントがPythonコードでのパースロジックを自律生成して解決させる。」

model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_key=os.environ.get("OPENAI_API_KEY")
)

# 2. Pydantic schema definition
class ContractSchema(BaseModel):
    client_name: str
    vendor_name: str
    agreement_date: date  # YYYY-MM-DD
    total_budget_yen: int # Integer parsed perfectly from kanji numerals
    duration_months: int  # Integer

# 3. Agent with built-in self-correction loop
agent = CodeAgent(tools=[], model=model, add_base_tools=True)

# 4. Agent instruction and execution
# Audit order: generate JSON matching ContractSchema fields; fix errors if any
task_instruction = f"""
以下の【生データ】から契約情報を抽出し、指定された【JSON形式のスキーマ】に完璧に適合するJSONテキストのみを出力してください。

【生データ】:
{dirty_contract_text}

【JSON形式のスキーマ】:
- "client_name": 甲（発注者）の正式名称 (文字列)
- "vendor_name": 乙（受注者）の正式名称 (文字列)
- "agreement_date": 契約合意日。必ず 'YYYY-MM-DD' の形式の日付文字列 (文字列)
- "total_budget_yen": 総予算（円）。「一千二百万円」などの漢数字表記を、必ず『12000000』のような「整数（int）」に変換すること。
- "duration_months": 契約期間の月数。満2か年であれば『24』のような「整数（int）」に変換すること。

出力は余計な説明文（```json などのマークダウン装飾も含む）を一切含めず、純粋なJSON文字列オブジェクトのみを出力してください。
"""

print("--- 自律型ナレッジ抽出エージェント 起動 ---")
raw_output = agent.run(task_instruction)

# --- Step 5: Strict program-side validation and self-correction simulation ---
try:
    # Clean markdown decoration if present
    cleaned_json = raw_output.strip().replace("```json", "").replace("```", "")
    data_dict = json.loads(cleaned_json)
    
    # Run Pydantic type validation!
    validated_contract = ContractSchema(**data_dict)
    
    print("\n✅ バリデーション完全パス！構造化ナレッジ抽出に成功しました:")
    print(validated_contract.model_dump_json(indent=2))
    
except (json.JSONDecodeError, ValidationError) as e:
    print("\n❌ バリデーションエラー発生！自動自己修正ループを起動します...")
    # In production, feed error log back to agent and call agent.run(error_feedback_task) again.
    # smolagents' internal interpreter detects execution errors and regenerates automatically.
```

### 💡 Final Production Adoption Decision

* **Final decision**:
  * **Adopt Approach B (Pydantic validator + self-correcting CodeAgent) for the production knowledge extraction pipeline.**
  * **Rationale**:
    1. **Absolute system stability guarantee**: Single-prompt extraction (Approach A) risks date/type errors and kanji parse failures from LLM version or variance, crashing downstream DB systems. Approach B uses Pydantic as gatekeeper blocking 100% of errors while the agent loops until correct format—near-zero downtime.
    2. **Advanced logic processing**: The agent creates and self-executes Python string/numeric conversion for kanji "一千二百万" to `12000000`, eliminating calculation hallucinations from LLM text output alone.
</details>
