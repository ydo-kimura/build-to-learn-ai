# Unit 30: Model Context Protocol (MCP) Fundamentals and Building Your Own Server

> [!IMPORTANT]
> **Preparing your OpenAI API key**
> Chapter 4 requires an **OpenAI API key**. For how to obtain a key, billing notes, and secure environment-variable setup with Google Colab secrets, read [Appendix (Learning Environment and API Setup)](../appendix/index.md#🔑-3-openai-api-key-acquisition-and-secure-management-chapter-4) first.

## 1. Understanding Model Context Protocol (MCP)

When giving AI agents tools—file ops, DB search, external APIs—teams traditionally implemented custom interfaces per framework (LangChain, LlamaIndex) or vendor API, **by hand**.

That tied you to specific frameworks and forced rewriting the same tool wiring for every new agent—a serious scalability problem.

**Model Context Protocol (MCP)**, proposed by Anthropic, is an open standard that normalizes how LLMs (AI clients) connect to external data and tools—**“USB for the AI world”**—so one tool works in any MCP-compatible client.

### 1.1 MCP three-layer architecture
MCP uses three cooperating roles:

```mermaid
graph LR
    Client[Client / IDE等<br>Claude, Cursor] <--> Host[Host / エージェント本体<br>mcp-host, custom script]
    Host <--> Server[Server / 各自作リソース・ツール<br>Sqlite, Filesystem, Google]
```

#### Text alternative for system structure
1. **Client**: UI the user operates (Cursor IDE, Claude Desktop)—handles LLM dialog and tool approval.
2. **Host**: Mediator driving the agent; receives client intent and routes to the right MCP server.
3. **Server**: Process hosting real tools and data; responds to Host requests (via JSON-RPC) with Resources or Tools—not roaming autonomously.

### 1.2 MCP’s three pillars (Resources, Prompts, Tools)
MCP servers expose three standard data forms to LLMs:

* **Resources**:
  * Read-only static data agents can fetch (files, DB contents, API responses).
  * Addressed like URLs (e.g., `mysql://customer_db/profile`) for context.
* **Prompts**:
  * Reusable prompt templates on the server (e.g., `/analyze-log`).
  * Inject user args and give optimal instructions to the LLM.
* **Tools**:
  * Dynamic functions with writes/changes/irreversible actions (save file, payment, run command).
  * Designed for easy **human-in-the-loop** approval before execution.

### 1.3 JSON-RPC over Standard I/O (stdio)
MCP’s base protocol is lightweight **JSON-RPC 2.0**.
For local runs, **stdio** (stdin/stdout) avoids open network ports—strong local security.

### 💡 Concrete business use cases
* **Secure database audit**: Run SQL MCP server locally over stdio; Host requests data through audit hooks only.
* **Shared dev-tool connection**: MCP-wrap internal APIs once; Cursor IDE and Claude Desktop plug in with zero extra code for all devs.

---

## 2. Implementation Example

Use the lightweight Python **`mcp` (MCP SDK)** library to build an MCP server so agents can **search a customer profile database via the standard protocol**.

Run `pip install mcp` first.

### Sample implementation (mcp_server.py)

```python
import sys
from mcp.server.fastmcp import FastMCP

# 1. FastMCP サーバーの初期化 (名前を登録)
# FastMCP は Python のデコレータを用いて、非常に直感的にリソースやツールを追加できるSDKです。
mcp = FastMCP("customer-insights-server")

# 模擬的な顧客データベース
CUSTOMER_DATABASE = {
    "cust_001": {
        "name": "アリス",
        "tier": "VIP",
        "email": "alice@example.com",
        "status": "Active"
    },
    "cust_002": {
        "name": "ボブ",
        "tier": "Regular",
        "email": "bob@example.com",
        "status": "Suspended"
    }
}

# ==========================================
# 2. Resources (リソース) の定義
# ==========================================
# `@mcp.resource()` デコレータを使い、エージェントに「静的な参照用データ」を提供します。
# 顧客全体のIDリストを静的に返すリソースを定義します。
@mcp.resource("customer://list")
def get_customer_list() -> str:
    """登録されているすべての顧客IDのリストを返します。"""
    return ", ".join(CUSTOMER_DATABASE.keys())

# 動的なパスを持つリソースの定義 (URLパラメータの利用)
@mcp.resource("customer://{customer_id}/profile")
def get_customer_profile(customer_id: str) -> str:
    """指定された顧客IDのプロフィール詳細を返します。"""
    cust = CUSTOMER_DATABASE.get(customer_id.lower())
    if cust:
        return (
            f"--- 顧客プロフィール ({customer_id}) ---\n"
            f"名前: {cust['name']}\n"
            f"会員ランク: {cust['tier']}\n"
            f"ステータス: {cust['status']}"
        )
    return f"エラー: 顧客ID '{customer_id}' は存在しません。"

# ==========================================
# 3. Tools (ツール) の定義
# ==========================================
# `@mcp.tool()` デコレータを使い、エージェントに「実行可能なアクション」を提供します。
# 関数の型ヒントと docstring が、そのまま自動で LLM への機能説明（Tool Schema）になります。
@mcp.tool()
def update_member_tier(customer_id: str, new_tier: str) -> str:
    """
    指定された顧客IDの会員ランクを更新します。
    
    引数:
        customer_id: 対象の顧客ID (例: cust_001)
        new_tier: 新しいランク名 (例: VIP, Regular)
    """
    cust = CUSTOMER_DATABASE.get(customer_id.lower())
    if not cust:
        return f"エラー: 顧客ID '{customer_id}' は見つかりません。"
    
    old_tier = cust["tier"]
    cust["tier"] = new_tier
    return f"成功: 顧客 {customer_id} のランクを {old_tier} から {new_tier} に更新しました。"

# ==========================================
# 4. stdio 接続でのサーバー起動
# ==========================================
if __name__ == "__main__":
    # コマンドライン引数や環境によって起動方法を決定できます。
    # ここでは MCP Host から呼び出される標準 stdio プロセスとして起動します。
    print("🚀 MCP Customer Insights Server Starting...", file=sys.stderr)
    mcp.run(transport="stdio")
```

### 💡 Note: invoking from Host (client side)
Add this server path to `mcpServers` in Claude Desktop / Cursor config—it plugs in as agent capability immediately.

```json
"mcpServers": {
  "customer-insights": {
    "command": "python",
    "args": ["/absolute/path/to/mcp_server.py"]
  }
}
```

---

## 3. Practice

### 🧠 Design and implement: customer-support MCP server

Support agents handle “show recent purchases” and “calculate applicable discount” through MCP’s clean standard interface.

**【Requirements】**
Using `FastMCP`, build **`support_mcp_server.py`**—a **customer-support MCP server** meeting:

1. **Static Resources**:
   * Define resource path `support://{order_id}/items`.
   * Return purchased item list and payment amount for order ID (e.g., `order_101`).
2. **Dynamic Tools**:
   * Define `calculate_loyalty_points(amount: int, tier: str)`.
   * Input: payment amount (JPY) and tier (VIP / Regular). Compute loyalty points:
     * **VIP**: 5% of amount
     * **Regular**: 1% of amount
3. **Safety**:
   * Validate inputs (e.g., negative amount) and return error strings.
4. Complete runnable Python script starting with stdio transport.

---

## 4. Answer Key

<details>
<summary>View sample solution (click to expand)</summary>

Complete support MCP server implementation:

```python
import sys
from mcp.server.fastmcp import FastMCP

# 1. MCPサーバーのインスタンス化
mcp = FastMCP("enterprise-support-server")

# 模擬的な注文履歴データベース
ORDERS_DATABASE = {
    "order_101": {
        "items": ["スニーカー", "Tシャツ"],
        "total_jpy": 15000
    },
    "order_202": {
        "items": ["プレミアムジャケット"],
        "total_jpy": 25000
    }
}

# ==========================================
# 2. 静的リソース (Resources) の定義
# ==========================================
@mcp.resource("support://{order_id}/items")
def get_order_items(order_id: str) -> str:
    """
    指定された注文IDの注文アイテムと総額を返します。
    """
    order = ORDERS_DATABASE.get(order_id.lower())
    if order:
        items_str = ", ".join(order["items"])
        return (
            f"--- 注文履歴 ({order_id}) ---\n"
            f"購入商品: {items_str}\n"
            f"合計支払額: {order['total_jpy']} 円"
        )
    return f"エラー: 注文ID '{order_id}' の履歴は見つかりません。"

# ==========================================
# 3. 動的ツール (Tools) の定義
# ==========================================
@mcp.tool()
def calculate_loyalty_points(amount: int, tier: str) -> str:
    """
    顧客の購入金額と会員ランクから、今回の買い物で付与されるロイヤルティポイント（円換算）を算出します。
    
    引数:
        amount: 今回の購入金額 (日本円)
        tier: 顧客の会員ランク (VIP または Regular)
    """
    # 安全設計: 不正入力の防御
    if amount < 0:
        return "エラー: 購入金額は0以上の整数でなければなりません。"
    
    clean_tier = tier.strip().upper()
    if clean_tier not in ["VIP", "REGULAR"]:
        return "エラー: 会員ランクは 'VIP' または 'Regular' のいずれかを指定してください。"
    
    # ビジネスロジックの実行
    if clean_tier == "VIP":
        points = int(amount * 0.05)
        rate_str = "5% (VIP特典)"
    else:
        points = int(amount * 0.01)
        rate_str = "1% (一般会員特典)"
        
    return (
        f"--- ポイント計算結果 ---\n"
        f"購入金額: {amount} 円\n"
        f"適用レート: {rate_str}\n"
        f"付与予定ポイント: {points} pt (1pt = 1円)"
    )

# ==========================================
# 4. 起動処理
# ==========================================
if __name__ == "__main__":
    # stdio トランスポートで起動し、外部ホスト・エージェントプロセスと安全に通信
    print("🚀 Support MCP Server Starting...", file=sys.stderr)
    mcp.run(transport="stdio")
```
</details>
