# Unit 29: AI Agent Fundamentals & Scratch ReAct Implementation (AIエージェントの基本原理とスクラッチReAct実装)

This unit introduces the conceptual background, execution loops, and raw implementations of **自律 AI エージェント (Autonomous AI Agents)**. You will build a complete **ReAct (Reasoning and Acting)** autonomous loop from scratch using only Python and OpenAI's Tool Calling API, without relying on any framework.

For the full hands-on curriculum, including comprehensive system architectures, step-by-step programming practices (such as implementing custom database tools and refund authorization workflows), and assignments, please refer to the main Japanese version:

👉 **[Main Japanese Version (日本語完全版)](/curriculum/unit29_ai_agent_implementation/)**

## Overview of Key Concepts Covered

1. **ReAct Paradigm**:
   - The cycle of **Thought（思考）**, **Action（行動）**, and **Observation（観察）** inside an autonomous execution loop.
   - Why frame-based JSON parsing is prone to failure and how to design robust logic.
2. **OpenAI Tool Calling (Function Calling)**:
   - Defining function schemas and mapping them dynamically to executable functions in host environments.
   - Crafting robust prompt contexts to anchor the agent's behavior.
3. **Loop Control & Boundary Safety**:
   - Managing execution states using custom Python `while` loops.
   - Setting limits on iteration thresholds (`max_iterations`) and implementing defensive logic to prevent infinite execution costs.

---

*For implementation samples and complete answer keys, visit [Japanese Version](/curriculum/unit29_ai_agent_implementation/).*
