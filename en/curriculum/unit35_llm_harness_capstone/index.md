# Unit 35: LLM Automated Evaluation, Guardrails & Agent Capstone

<p class="unit-hero">
  <img src="../../../assets/units/unit35_llm_harness_capstone/images/hero.png" alt="Hero: LLM Harness Capstone" />
</p>

## 1. Understanding Harness Engineering (LLM Automated Evaluation)

<img src="../../../assets/units/unit35_llm_harness_capstone/images/diagram-concept.svg" alt="Diagram: Dual harness" class="unit-diagram" />



In Chapter 4, you covered LLM API usage, scratch RAG construction, LangChain basics, prompt chaining, Web UI chatbots, and autonomous AI agents.

This capstone unit brings it together with **Harness Engineering (LLM evaluation harness)**—among the most important skills in enterprise AI system development.

### What Is Harness Engineering?
Traditional software testing uses deterministic tests: if output differs by one character from expected, the test fails. That approach does not work for LLM applications whose outputs vary slightly each run.

An **automated evaluation system (evaluation harness)** automatically and quantitatively measures whether prompt tuning or RAG changes **actually improved accuracy (or caused regression/degradation)**.

**💡 Everyday analogy: automatic quality inspection for a custom coffee blend**

* **Typical RAG/Agent**: "We brewed coffee with today's beans—it works!"
* **Harness engineering**: Build an automatic lab that measures sweetness, acidity, and bitterness with sensors, visualizes "bitterness down 10% vs last week's recipe, acidity improved in balance," and fully controls flavor drift (regression).

| Evaluation Dimension | Meaning | Measurement (LLM-as-a-Judge) |
| :--- | :--- | :--- |
| **Faithfulness** | Whether the answer is grounded in retrieved reference documents (facts)—degree of hallucination exclusion. | Compare extracted documents and generated answer; have an evaluator LLM strictly score "does it contain unsupported claims?" |
| **Answer Relevance** | Whether the generated answer appropriately addresses the user's original question. | Compare question and answer; judge whether irrelevant or off-topic content is included. |

This unit implements **LLM-as-a-Judge** from scratch: static test input/output pairs (question, reference document, AI answer) scored automatically by an evaluator LLM, quantifying accuracy before and after prompt improvements.

---

<img src="../../../assets/units/unit35_llm_harness_capstone/images/diagram-workflow.svg" alt="Diagram: Defense layers" class="unit-diagram" />

## 2. Implementation Example

Here you implement an evaluation harness that feeds test cases (questions and documents) and uses an evaluator LLM API to **automatically score on a 5-point scale how faithful the generated answer is to document facts (Faithfulness)**.

Run `pip install openai` beforehand and set `OPENAI_API_KEY` in environment variables.

```python
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 1. Test case definitions
test_cases = [
    {
        "id": "case_A_faithful",
        "context": "Our hotel check-in is at 15:00 and check-out at 10:00. Pets are not allowed. Breakfast is served from 7:00 AM on the 1st floor dining room.",
        "question": "What time is check-in, and can I bring my pet?",
        "answer": "Check-in begins at 3:00 PM (15:00). We regret to inform you that pets are not permitted."
    },
    {
        "id": "case_B_hallucination",
        "context": "Our hotel check-in is at 15:00 and check-out at 10:00. Pets are not allowed. Breakfast is served from 7:00 AM on the 1st floor dining room.",
        "question": "What time is check-in, and can I bring my pet?",
        "answer": "Check-in is from 3 PM. Pets are not allowed. Also, complimentary high-speed Wi-Fi is available throughout the hotel."
    }
]

# 2. Evaluation prompt design for LLM-as-a-Judge
EVAL_SYSTEM_PROMPT = """You are an extremely strict AI quality assurance (QA) auditor.
Compare the provided Reference Document (Context) and AI Answer, and judge how faithfully the AI answer reflects document facts.

Follow the [Evaluation Criteria] below and output an integer score from 1 to 5 plus a detailed reason for your score.

[Evaluation Criteria]
5 - Perfectly faithful: Every fact in the answer is directly stated in the reference document. No hallucinations or unsupported inferences.
4 - Mostly faithful: Generally matches the document but with slight nuance beyond the text (facts not distorted).
3 - Partially divergent / includes inference: Aligns with the document but adds minor assumptions not explicitly stated.
2 - Major hallucination: States undocumented services or rules as definite facts.
1 - Completely wrong / contradictory: Contradicts the document or ignores it entirely.

Return ONLY the following JSON format. No extra explanation.
{
  "score": (integer from 1 to 5),
  "reason": "(Why you gave this score, citing evidence and any hallucination)"
}"""

def run_evaluation_harness(case):
    prompt_user = f"""[User Question]
{case['question']}

[Reference Document (Context)]
{case['context']}

[AI Answer]
{case['answer']}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": EVAL_SYSTEM_PROMPT},
            {"role": "user", "content": prompt_user}
        ],
        temperature=0.0, # Must be 0 to reduce variance
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# Run harness
print("=== Running Evaluation Harness ===")
for case in test_cases:
    print(f"\n[Test Case ID: {case['id']}]")
    print(f"AI Answer: \"{case['answer']}\"")
    eval_result = run_evaluation_harness(case)
    print(f"➔ Score: {eval_result['score']} / 5")
    print(f"➔ Reason: {eval_result['reason']}")
```

---

## 3. Practice — 🧠 Compare and Decide Business Evaluation Metrics and Harness Design

The hardest—and most skill-demanding—part of production LLM systems is designing the **evaluation harness (automated tests)**. Do not stop at "seems to work"; experience deciding **which evaluation metrics to define and how to apply judge models** aligned with system purpose and business value.

**Assignment Requirements**

You are a QA lead engineer auditing a luxury hotel's automated concierge AI (chatbot).

This test goes beyond factual correctness to **answer quality (business evaluation metrics)** that protects brand value.

Build a harness that automatically evaluates the two extreme test cases below.

```python
# 1. Test cases to evaluate
relevance_test_cases = [
    {
        "id": "case_C_ideal",
        "question": "Can I check in late at night?",
        "answer": "Yes, our front desk operates 24 hours a day, so you may check in safely even if you arrive late at night. We look forward to welcoming you."
    },
    {
        "id": "case_D_bad_tone",
        "question": "Can I check in late at night?",
        "answer": "Yeah we're open 24/7 so showing up late is fine. Just come whenever."
    }
]
```

**Your Mission: Compare Two Evaluation Approaches and Decide**

As the hotel's brand auditor, **implement and compare both** contrasting automated evaluation approaches below.

1. **Approach A (Hospitality tone & quality evaluation harness)**
   * **Design**: Use an LLM as judge with a **single evaluation prompt (`EVAL_TONE_PROMPT`)** scoring Tone & Quality (wording, hospitality, politeness) from 1 to 5.
   * **Characteristics**: Specialized for brand-damage prevention; quickly detects tone drift.
2. **Approach B (Two-dimensional multi-faceted quality harness)**
   * **Design**: Have the LLM output **two separate dimensions**—Answer Relevance and Brand Safety—and quantify them together.
   * **Characteristics**: Visualizes trade-offs (e.g., perfectly polite but irrelevant vs. rude but accurate).

---

**Design Decision Notes to Record in Code Comments**

1. **Evaluation prompt design (eliminating ambiguity)**:
   * Describe how you defined concrete criteria for scores 1–5 so the LLM scores consistently.
2. **Difference in results between the two approaches**:
   * Using OpenAI API and JSON Mode, run both approaches on test cases and compare scores and reasons.
3. **Quantitative evaluation and final decision**:
   * Compare audit cost (API fees), defect diversity detected, and maintainability; **state which harness you choose for production QA and why.**

---

## 4. Answer Key — 💡 Production Evaluation Design

<details>
<summary>View sample solution (click to expand)</summary>

### 💡 Guidelines for Evaluation Metric Design

Review the most important rules when designing LLM-as-a-Judge evaluation prompts.

#### Evaluation Harness Approach Comparison Matrix

| Evaluation Axis | Approach A (Tone-focused) | Approach B (2D evaluation) | Design Decision Point |
| :--- | :--- | :--- | :--- |
| **Detection power** | Pinpoints tone issues (casual speech, etc.). | Detects tone issues plus whether the answer ignores the question. | **Approach B is professional-grade**. Brand polish means nothing if the guest's question (late check-in) is ignored. |
| **Scoring variance** | Single prompt may over-score polite but irrelevant answers. | Separating Relevance and Tone stabilizes judge logic. | Explicit banned phrases (e.g., 〜っす) and dimension separation keep variance under ~1%. |
| **API cost** | One request—lower cost. | Slightly higher tokens for two dimensions or complex output. | In development and CI/CD automation, accuracy and debuggability beat cost. |

---

### Complete Comparative Evaluation Harness Code

```python
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 1. Decision:
# "For a luxury hotel concierge, politeness is assumed, but Answer Relevance and Tone are separate axes."
# "Therefore we build Approach B (2D evaluation harness) outputting both as separate keys."

EVAL_2D_PROMPT = """You are the general manager of a luxury hotel and chief auditor of brand image and service quality.
Analyze the provided User Question and AI Answer, and score strictly on the following two dimensions.

1. [Answer Relevance]
   * 5: Answers the user's question completely and precisely with no excess or omission.
   * 3: Functional answer but includes unnecessary content or missing information.
   * 1: Does not answer the question or provides irrelevant information.

2. [Brand Safety & Tone]
   * 5: Perfect formal hospitality language and warm welcome (e.g., "We look forward to welcoming you").
   * 3: Not rude but includes overly casual phrasing such as "That's fine" or "Sure thing."
   * 1: Contains slang, overly casual speech, or rude expressions anywhere in the answer.

Return ONLY the following JSON format. No extra explanation.
{
  "relevance_score": (integer from 1 to 5),
  "relevance_reason": "(Specific reason for relevance score)",
  "tone_score": (integer from 1 to 5),
  "tone_reason": "(Specific reason for tone score)"
}"""

def run_2d_evaluation_harness(case):
    prompt_user = f"""[User Question]
{case['question']}

[AI Answer]
{case['answer']}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": EVAL_2D_PROMPT},
            {"role": "user", "content": prompt_user}
        ],
        temperature=0.0, # Must be 0 to prevent judge variance
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# 2. Run harness and quantify
print("=== Running 2D Multi-Faceted Evaluation Harness ===")
for case in relevance_test_cases:
    print(f"\n[Test Case ID: {case['id']}]")
    print(f"Answer: \"{case['answer']}\"")
    
    result = run_2d_evaluation_harness(case)
    print(f"➔ Answer Relevance: {result['relevance_score']} / 5")
    print(f"  Reason: {result['relevance_reason']}")
    print(f"➔ Brand Tone: {result['tone_score']} / 5")
    print(f"  Reason: {result['tone_reason']}")
```

### 💡 Final Production Adoption Decision

Running this 2D harness produces clear differentiation:

* **Final production decision**:
  * **Select Approach B (2D multi-faceted evaluation harness) for CI/CD automated quality audit.**
  * **Rationale**:
    1. Tone-only evaluation (Approach A) can high-score polite answers that fail to address the question (silent hallucination).
    2. Approach B allows a gatekeeper rule: only release when both `relevance_score` and `tone_score` are 5, protecting hotel reputation technologically.
    3. Separate reasons for relevance and tone make prompt debugging obvious and dramatically improve developer productivity.

To control LLM behavior correctly, **elevate evaluation harness architecture to match business requirements—not just the model (concierge AI)**. That is harness engineering, the most important skill for scaling AI in production.
</details>
