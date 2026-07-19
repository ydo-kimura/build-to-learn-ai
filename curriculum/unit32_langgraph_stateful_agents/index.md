# Unit 32: LangGraph — グラフベースのステートフルエージェント

<p class="unit-hero">
  <img src="../../assets/units/unit32_langgraph_stateful_agents/images/hero.png" alt="ヒーロー画像：LangGraph によるチケット振り分けグラフ" />
</p>

Unit 31 では smolagents の **コード生成型エージェント（Code Agent）** を学びました。本ユニットでは、 **グラフベースのワークフロー制御** という別のパラダイムを学びます。LangGraph は、エージェントの処理を「ノード」と「エッジ」で明示的に設計し、 **共有ステート（State）** をノード間で受け渡しながら、条件分岐や人間の承認（Human-in-the-loop）を組み込めるフレームワークです。

---

## 1. LangGraph とステートフルワークフローの理解

> 本章では、Pythonの型ヒントである `TypedDict` と `Literal` を使ってステートの形と分岐先を表します。型ヒントに不慣れでも実装を追えるよう、コード内の役割をコメントで補足しています。

### 1.1 なぜグラフなのか？

Unit 29 の ReAct は **While ループ内の暗黙的な制御フロー** でした。Unit 31 の smolagents は **LLM が書いたコードの実行** に特化しています。一方、業務システムでは次のような要件が頻出します。

- 「分類結果に応じて、処理経路を **明示的に分岐** したい」
- 「重要案件だけ **人間の承認** を挟みたい」
- 「途中状態を **永続化** し、後から再開したい」

LangGraph は、こうした要件を **有向グラフ（Directed Graph）** として設計します。

| 概念 | 役割 | 日常の例え |
| :--- | :--- | :--- |
| **State（ステート）** | ノード間で共有するデータ（辞書 / TypedDict） | カスタマーサポートの「チケット票」 |
| **Node（ノード）** | ステートを読み取り、更新する処理単位 | 「分類する」「請求担当へ渡す」 |
| **Edge（エッジ）** | 次に実行するノードを決める遷移 | 「請求系なら Billing ノードへ」 |


下図は、LangGraph の **State / Node / Edge** というグラフの基本要素です。

<img src="../../assets/units/unit32_langgraph_stateful_agents/images/diagram-concept.svg" alt="図解：State を共有しながら分岐するグラフ構造" class="unit-diagram" />

### 1.2 smolagents（Code Agent）との比較

| 評価軸 | smolagents (Code Agent) | LangGraph (Graph Workflow) |
| :--- | :--- | :--- |
| **制御の見え方** | LLM が生成した Python コードの中に埋もれる | グラフとして **可視化・監査しやすい** |
| **条件分岐** | コード内の if 文に依存 | **エッジ関数** で明示的に定義 |
| **Human-in-the-loop** | 実装は可能だが設計が散らばりやすい | **専用ノード** として組み込みやすい |
| **向いているタスク** | 計算・データ加工の一撃解決 | 部門振り分け、承認フロー、長寿命ワークフロー |

### 1.3 代表的なユースケース

* **カスタマーサポートの自動振り分け** : 問い合わせを billing / technical / escalate にルーティング
* **Human-in-the-loop** : VIP 顧客や高額案件のみ人間承認を必須化
* **マルチステップ業務フロー** : 検索 → 要約 → 承認 → 送信 を段階的に実行

```mermaid
graph TD
    Start([チケット受付]) --> Classify[分類ノード]
    Classify -->|billing| Billing[請求対応]
    Classify -->|technical| Technical[技術対応]
    Classify -->|escalate| Escalate[エスカレーション]
    Billing --> End([完了])
    Technical --> End
    Escalate --> End
```


下図は、問い合わせを **Classify → Billing / Technical / Escalate** に振り分けるルーティングです。

<img src="../../assets/units/unit32_langgraph_stateful_agents/images/diagram-workflow.svg" alt="図解：チケット振り分け" class="unit-diagram" />

---

## 2. 実装例 (Implementation Example)

ここでは **OpenAI API キー不要** のローカル完結シミュレーションで、LangGraph を使ったステートフルワークフローを実装します。キーワードベースの簡易分類器で、カスタマーサポートチケットを **classify ➔ billing / technical / escalate** に振り分けます。

事前に `pip install langgraph` を実行してください。

### 2.1 LangGraph（StateGraph）による実装

`TypedDict` で State を定義 → `StateGraph(State)` でグラフを作成 → `add_node` でノードを追加 → `add_conditional_edges` で分岐を定義 → `compile()` → `invoke()`、というのが LangGraph の基本の流れです。

```python
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END


# 1. State の定義: ノード間で共有される「チケット票」
class TicketState(TypedDict):
    message: str
    category: str
    route: str
    response: str


# 2. ノードの定義: State を読み取り、更新したいキーだけを辞書で返す
def classify_node(state: TicketState) -> dict:
    """チケット本文からカテゴリを推定するノード"""
    text = state["message"].lower()
    if any(k in text for k in ("refund", "billing", "invoice", "請求", "返金")):
        category = "billing"
    elif any(k in text for k in ("error", "bug", "crash", "障害", "動かない")):
        category = "technical"
    else:
        category = "escalate"
    return {"category": category}


def billing_node(state: TicketState) -> dict:
    return {"route": "billing", "response": "請求チームが24時間以内にご連絡します。"}


def technical_node(state: TicketState) -> dict:
    return {"route": "technical", "response": "技術サポートがログを確認し、再現手順をお伺いします。"}


def escalate_node(state: TicketState) -> dict:
    return {"route": "escalate", "response": "専任担当者が優先対応します。"}


# 3. 条件分岐エッジ: State を見て「次に進むノード名」を返す関数
def route_ticket(state: TicketState) -> Literal["billing", "technical", "escalate"]:
    return state["category"]  # type: ignore[return-value]


# 4. グラフの組み立て
builder = StateGraph(TicketState)

builder.add_node("classify", classify_node)
builder.add_node("billing", billing_node)
builder.add_node("technical", technical_node)
builder.add_node("escalate", escalate_node)

builder.add_edge(START, "classify")  # 開始 → 分類ノード
builder.add_conditional_edges(       # 分類結果に応じて3方向に分岐
    "classify",
    route_ticket,
    {"billing": "billing", "technical": "technical", "escalate": "escalate"},
)
builder.add_edge("billing", END)
builder.add_edge("technical", END)
builder.add_edge("escalate", END)

# 5. コンパイルして実行可能なグラフに変換
graph = builder.compile()

if __name__ == "__main__":
    samples = [
        "先月の請求書の金額がおかしいです。返金できますか？",
        "アプリが起動直後にクラッシュします。",
        "サービス全般について相談したいです。",
    ]
    for msg in samples:
        result = graph.invoke({"message": msg})
        print(f"[{result['route']}] {result['response']}")
```

**実行結果のイメージ**

```text
[billing] 請求チームが24時間以内にご連絡します。
[technical] 技術サポートがログを確認し、再現手順をお伺いします。
[escalate] 専任担当者が優先対応します。
```

### 2.2 チェックポイントによる永続化と再開（MemorySaver）

「1.1 なぜグラフなのか？」で触れた **「途中状態を永続化し、後から再開したい」** という要件は、`compile()` 時に **checkpointer** を渡すだけで実現できます。実行時に `thread_id` を指定すると、その ID ごとに State が保存され、同じ ID を指定すれば保存されたステートを読み出して処理を再開できます。

```python
from langgraph.checkpoint.memory import MemorySaver

# チェックポインタを渡してコンパイル（本番では SQLite / Postgres 用の Saver に差し替え可能）
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# thread_id ごとに独立した State が保存される
config = {"configurable": {"thread_id": "ticket-001"}}
result = graph.invoke({"message": "請求書の返金をお願いします。"}, config)
print(result["response"])  # -> 請求チームが24時間以内にご連絡します。

# 後から同じ thread_id を指定すれば、保存済みのステートを取り出して再開できる
saved = graph.get_state(config)
print(saved.values["category"])  # -> billing
```

### 2.3 参考: LangGraph が内部で何をしているかを理解するための手組み版

以下は、上記の LangGraph 実装とまったく同じ処理を、フレームワークなしの素の Python で書いた **手組み版** です。`add_conditional_edges` が「分岐関数の戻り値で次の関数を選ぶ辞書引き」に、`invoke` が「関数を順に呼び出すオーケストレータ関数」に対応していることが分かります。LangGraph のありがたみ（宣言的なグラフ定義、可視化、チェックポイント）を実感するために、内部動作のイメージとして目を通してみてください。

```python
from typing import Literal, TypedDict


class TicketState(TypedDict):
    message: str
    category: str
    route: str
    response: str


def classify_node(state: TicketState) -> TicketState:
    """チケット本文からカテゴリを推定するノード"""
    text = state["message"].lower()
    if any(k in text for k in ("refund", "billing", "invoice", "請求", "返金")):
        state["category"] = "billing"
    elif any(k in text for k in ("error", "bug", "crash", "障害", "動かない")):
        state["category"] = "technical"
    else:
        state["category"] = "escalate"
    return state


def route_ticket(state: TicketState) -> Literal["billing", "technical", "escalate"]:
    """条件分岐エッジ: 次に実行するノード名を返す"""
    return state["category"]  # type: ignore[return-value]


def billing_node(state: TicketState) -> TicketState:
    state["route"] = "billing"
    state["response"] = "請求チームが24時間以内にご連絡します。"
    return state


def technical_node(state: TicketState) -> TicketState:
    state["route"] = "technical"
    state["response"] = "技術サポートがログを確認し、再現手順をお伺いします。"
    return state


def escalate_node(state: TicketState) -> TicketState:
    state["route"] = "escalate"
    state["response"] = "専任担当者が優先対応します。"
    return state


# --- グラフ実行（LangGraph 相当の手組みオーケストレータ） ---
NODE_MAP = {
    "billing": billing_node,
    "technical": technical_node,
    "escalate": escalate_node,
}


def run_support_graph(message: str) -> TicketState:
    state: TicketState = {
        "message": message,
        "category": "",
        "route": "",
        "response": "",
    }
    state = classify_node(state)
    next_node = route_ticket(state)
    state = NODE_MAP[next_node](state)
    return state


if __name__ == "__main__":
    samples = [
        "先月の請求書の金額がおかしいです。返金できますか？",
        "アプリが起動直後にクラッシュします。",
        "サービス全般について相談したいです。",
    ]
    for msg in samples:
        result = run_support_graph(msg)
        print(f"[{result['route']}] {result['response']}")
```

> [!TIP]
> 本番開発では 2.1 のように `langgraph` パッケージの `StateGraph` を使い、ノードとエッジを宣言的に登録するのが標準です。2.3 の手組み版は **LangGraph が内部で何をしているかを理解するための学習用** の位置づけです。

---

## 3. 実践 (Practice)

**【課題】** 上記の振り分けグラフに、次の **Human-in-the-loop** を追加してください。

1. チケット本文に `VIP` または `緊急` が含まれる場合、自動応答の前に **人間承認ノード** で処理を一時停止する
2. 承認が得られた場合のみ、元のルーティング（billing / technical / escalate）へ進む
3. 承認が拒否された場合は、「担当者が後日ご連絡します」と応答して終了する

**設計メモとしてコメントで書くこと**

- なぜ「暗黙の if 文」ではなく **グラフ上の専用ノード** として承認を切り出すと保守しやすいか
- smolagents の Code Agent ではなく LangGraph を選ぶ理由（本課題の文脈で）

---

## 4. 答え合わせ (Answer Key)

<details>
<summary>解答例を見る（クリックで展開）</summary>

課題の指示どおり、2.1 で組み立てた `StateGraph` に **人間承認ノード** を追加するのが本命の解答です。承認待ちでグラフを一時停止するために、2.2 で学んだ **checkpointer** と、LangGraph の **`interrupt()`** （ノード内で実行を中断し、外部からの入力を待つ仕組み）を使います。

```python
from typing import Literal, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt


# 注: `bool | None` の書き方は Python 3.10 以降の記法です。
#     3.9 以前では `from typing import Optional` として `Optional[bool]` と書きます。
class TicketState(TypedDict):
    message: str
    category: str
    route: str
    needs_human: bool
    approved: bool | None
    response: str


def classify_node(state: TicketState) -> dict:
    text = state["message"].lower()
    if any(k in text for k in ("refund", "billing", "invoice", "請求", "返金")):
        category = "billing"
    elif any(k in text for k in ("error", "bug", "crash", "障害", "動かない")):
        category = "technical"
    else:
        category = "escalate"
    # 重要チケットは自動応答前に人間承認へ
    needs_human = any(k in state["message"] for k in ("VIP", "緊急"))
    return {"category": category, "needs_human": needs_human}


def human_approval_node(state: TicketState) -> dict:
    # interrupt() でグラフはここで一時停止し、State は checkpointer に保存される。
    # 承認者の入力（True/False）が Command(resume=...) で渡されると再開する。
    approved = interrupt({"question": f"承認しますか？: {state['message']}"})
    if approved:
        return {"approved": True}
    return {"approved": False, "response": "担当者が後日ご連絡します。"}


def billing_node(state: TicketState) -> dict:
    return {"route": "billing", "response": "請求チームが24時間以内にご連絡します。"}


def technical_node(state: TicketState) -> dict:
    return {"route": "technical", "response": "技術サポートがログを確認し、再現手順をお伺いします。"}


def escalate_node(state: TicketState) -> dict:
    return {"route": "escalate", "response": "専任担当者が優先対応します。"}


# 【設計メモ】承認を「暗黙の if 文」ではなくグラフ上の専用ノードにする理由:
#   承認ロジックを各応答ノードに散らすと、監査ログの記録・承認UIへの接続・
#   タイムアウト処理などをノードごとに重複実装することになる。専用ノードなら
#   グラフ図上で「どこで人間が介在するか」が一目で分かり、差し替えも1箇所で済む。
def after_classify(state: TicketState) -> Literal["human_approval", "billing", "technical", "escalate"]:
    if state["needs_human"]:
        return "human_approval"
    return state["category"]  # type: ignore[return-value]


def after_human(state: TicketState) -> Literal["billing", "technical", "escalate", "__end__"]:
    if not state["approved"]:
        return END  # 拒否されたら応答を出さずに終了
    return state["category"]  # type: ignore[return-value]


builder = StateGraph(TicketState)
builder.add_node("classify", classify_node)
builder.add_node("human_approval", human_approval_node)
builder.add_node("billing", billing_node)
builder.add_node("technical", technical_node)
builder.add_node("escalate", escalate_node)

builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", after_classify)
builder.add_conditional_edges("human_approval", after_human)
builder.add_edge("billing", END)
builder.add_edge("technical", END)
builder.add_edge("escalate", END)

# interrupt() を使うには checkpointer が必須（停止中の State を保存するため）
graph = builder.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "ticket-vip-001"}}

    # 1回目の invoke: VIP チケットなので human_approval ノードで一時停止する
    result = graph.invoke(
        {"message": "VIP顧客です。請求書の返金を緊急でお願いします。"}, config
    )
    print("グラフは承認待ちで停止中...")

    # 承認者の判断を Command(resume=...) で渡すと、停止地点から再開する
    result = graph.invoke(Command(resume=True), config)   # True=承認 / False=拒否
    print(result["response"])  # -> 請求チームが24時間以内にご連絡します。
```

**【設計メモ】smolagents の Code Agent ではなく LangGraph を選ぶ理由（本課題の文脈で）** : 本課題は「計算を一発で解く」タスクではなく、 **部門振り分け＋承認ゲートという制御フローの管理** が主役です。「どこで止まり、誰が再開させるか」を宣言的なグラフとして可視化・永続化できる LangGraph が適しています。

---

**【参考】手組み版での実装（LangGraph が内部で行っていることの理解用）**

2.3 の手組み版に同じ HITL を追加すると以下のようになります。グラフライブラリなしでも同じ制御は書けますが、「承認待ちでの一時停止・再開」や状態の永続化を自力で管理する必要があることが分かります。

```python
from typing import Literal, TypedDict


class TicketState(TypedDict):
    message: str
    category: str
    route: str
    needs_human: bool
    approved: bool | None
    response: str


def classify_node(state: TicketState) -> TicketState:
    text = state["message"].lower()
    if any(k in text for k in ("refund", "billing", "invoice", "請求", "返金")):
        state["category"] = "billing"
    elif any(k in text for k in ("error", "bug", "crash", "障害", "動かない")):
        state["category"] = "technical"
    else:
        state["category"] = "escalate"
    return state


def detect_human_gate(state: TicketState) -> TicketState:
    # 重要チケットは自動応答前に人間承認へ
    text = state["message"]
    state["needs_human"] = any(k in text for k in ("VIP", "緊急"))
    return state


def human_approval_node(state: TicketState) -> TicketState:
    # 実務では UI / Slack 承認に接続。ここではシミュレーション
    print(f"[HUMAN REVIEW] {state['message']}")
    answer = input("Approve? (y/n): ").strip().lower()
    state["approved"] = answer in ("y", "yes")
    if not state["approved"]:
        state["response"] = "担当者が後日ご連絡します。"
    return state


def billing_node(state: TicketState) -> TicketState:
    state["route"] = "billing"
    state["response"] = "請求チームが24時間以内にご連絡します。"
    return state


def technical_node(state: TicketState) -> TicketState:
    state["route"] = "technical"
    state["response"] = "技術サポートがログを確認し、再現手順をお伺いします。"
    return state


def escalate_node(state: TicketState) -> TicketState:
    state["route"] = "escalate"
    state["response"] = "専任担当者が優先対応します。"
    return state


NODE_MAP = {
    "billing": billing_node,
    "technical": technical_node,
    "escalate": escalate_node,
}


def after_classify(state: TicketState) -> Literal["human", "route"]:
    return "human" if state["needs_human"] else "route"


def after_human(state: TicketState) -> Literal["route", "done"]:
    return "route" if state.get("approved") else "done"


def run_support_graph_with_hitl(message: str) -> TicketState:
    state: TicketState = {
        "message": message,
        "category": "",
        "route": "",
        "needs_human": False,
        "approved": None,
        "response": "",
    }
    state = classify_node(state)
    state = detect_human_gate(state)

    if after_classify(state) == "human":
        state = human_approval_node(state)
        if after_human(state) == "done":
            return state

    next_node = state["category"]
    return NODE_MAP[next_node](state)


if __name__ == "__main__":
    result = run_support_graph_with_hitl("VIP顧客です。請求書の返金を緊急でお願いします。")
    print(result["response"])
```

### 💡 プロとしての設計判断

* **Human-in-the-loop は専用ノードに分離する** : 承認ロジックを各応答ノードに散らすと、監査ログや UI 連携が困難になる。グラフ上で `human_approval` を1箇所に置くと、本番の Slack 承認や管理画面へ差し替えやすい。
* **LangGraph 版と手組み版の比較** : 手組み版では `input()` でプログラム全体をブロックして承認を待つしかないが、LangGraph 版は `interrupt()` + checkpointer により **プロセスを終了しても承認待ち状態が保存され、後から再開できる** 。この「止めて、保存して、再開する」能力こそが、実務で LangGraph を選ぶ最大の理由である。

</details>
