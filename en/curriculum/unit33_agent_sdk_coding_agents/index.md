# Unit 33: Agent SDK: Autonomous Coding & Software Engineering

This unit introduces the architecture, runtime environments, and critical safety mechanisms of managed, commercial **Coding / Software Engineering (SWE) Agent SDKs** (such as Google Antigravity and OpenAI Codex), which execute raw shell commands and perform file operations dynamically.

For the full hands-on curriculum, including comprehensive system architectures, safety policy coding (such as Deny-by-Default and interactive approval hooks), and assignments, please refer to the main Japanese version:

👉 **[Main Japanese Version (日本語完全版)](/curriculum/unit33_agent_sdk_coding_agents/)**

## Overview of Key Concepts Covered

1. **Uniqueness of Software Engineering (SWE) Agents**:
   - Capabilities and high-risk actions including file modifications, compiler/terminal executions, and integration with Linter/LSP engines.
   - Understanding why generic agents are insufficient and why specialized SDKs are required.
2. **Critical Security & Safety Architecture**:
   - **"Deny by Default" Policy Design**: Absolute boundaries preventing path traversal and execution of unauthorized shells/subprocesses.
   - **Human-in-the-Loop Hooks**: Intercepting dynamic commands with lifecycle callbacks (`on_pre_execute`) to prompt the user before modifications occur.
   - **Sandbox Isolation**: Executing agent containers dynamically in isolated Docker/WASM environments to protect development machines.
3. **Google Antigravity SDK (`google-antigravity`)**:
   - Examining actual Antigravity security policies, file manipulation mechanisms, and safe runtime orchestrations.

---

*For implementation samples and complete answer keys, visit [Japanese Version](/curriculum/unit33_agent_sdk_coding_agents/).*
