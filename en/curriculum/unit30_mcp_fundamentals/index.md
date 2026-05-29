# Unit 30: Model Context Protocol (MCP) Fundamentals & Server Implementation (Model Context Protocol の基本原理とサーバー自作)

This unit introduces the conceptual background, protocol specification, and practical implementations of the **Model Context Protocol (MCP)**, an open standard designed by Anthropic to unify how AI applications securely connect to data sources and tools.

For the full hands-on curriculum, including comprehensive system architectures, step-by-step programming practices (such as building custom database search engines and loyalty point calculators), and assignments, please refer to the main Japanese version:

👉 **[Main Japanese Version (日本語完全版)](/curriculum/unit30_mcp_fundamentals/)**

## Overview of Key Concepts Covered

1. **MCP 3-Tier Architecture**:
   - Understanding the roles of **Client**, **Host**, and **Server**.
   - Committing to secure process execution over stdio (standard input/output) using lightweight JSON-RPC 2.0 communication.
2. **The 3 Pillars of MCP**:
   - **Resources**: Providing read-only, dynamic/static datasets referenced via standard URLs.
   - **Prompts**: Providing reusable template schemas with dynamic user variables to steer LLM context.
   - **Tools**: Providing executable, dynamic actions (with safety validation and human-in-the-loop approval hooks).
3. **Hands-on Server Implementation (FastMCP)**:
   - Constructing custom Python-based MCP servers using the `FastMCP` framework.
   - White-boxing data retrieval tools, validation boundaries, and exposing them natively to IDEs (e.g., Cursor) and desktop clients.

---

*For implementation samples and complete answer keys, visit [Japanese Version](/curriculum/unit30_mcp_fundamentals/).*
