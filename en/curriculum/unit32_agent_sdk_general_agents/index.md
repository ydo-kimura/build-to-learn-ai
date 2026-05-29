# Unit 32: Agent SDK: General & Business Automation

This unit introduces the architecture and engineering implementations of managed, commercial **Agent SDKs** provided by major AI/Cloud vendors (e.g., OpenAI, AWS, Meta), as opposed to open-source frameworks.

For the full hands-on curriculum, including comprehensive system architectures, step-by-step programming practices (such as building episodic memory and role-handoff mechanisms), and assignments, please refer to the main Japanese version:

👉 **[Main Japanese Version (日本語完全版)](/curriculum/unit32_agent_sdk_general_agents/)**

## Overview of Key Concepts Covered

1. **Managed Agent SDK Architecture**:
   - **AWS Bedrock AgentCore SDK (`bedrock-agentcore-sdk-python`)**: Integrating with enterprise data, managed routing, and episodic memory layers.
   - **OpenAI Agents SDK**: Assistants API lifecycle, role handoffs, and snapshotting/thread persistence.
   - **Meta Llama Stack**: Open API standardization, safety filtering (Llama Guard 3), and sovereign multi-cloud deployments.
2. **Business Integration**:
   - Designing persistent, context-aware user sessions using episodic memory.
   - Conceptualizing autonomous transactions and wallet connections (e.g., Stripe, Coinbase, Mock Bedrock Payments).
3. **Architectural Evaluation (OSS vs. Vendor SDKs)**:
   - Comparing trade-offs between flexibility, security, hosting costs, and lock-in risks.

---

*For implementation samples and complete answer keys, visit [Japanese Version](/curriculum/unit32_agent_sdk_general_agents/).*
