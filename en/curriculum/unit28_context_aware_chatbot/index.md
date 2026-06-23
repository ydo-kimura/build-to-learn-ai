# Unit 28: Context-Aware Chatbot

> [!IMPORTANT]
> **OpenAI API key setup**
> This unit uses the OpenAI API. See [Appendix (Learning Environment and API Setup)](../appendix/index.md#🔑-3-openai-api-key-acquisition-and-secure-management-chapter-4) for secure key configuration.


## 1. Understanding Context-Aware Chatbot

<img src="../../../assets/units/unit28_context_aware_chatbot/images/concept.png" width="400" alt="Concept diagram">

### Why memory matters
LLMs via API are basically **amnesiac**.
Teach “My name is Taro” in turn 1; ask “What is my name?” in turn 2—they say “I don’t know.” Each call is independent.

Context-aware chatbots need **memory**.

**💡 Everyday analogy: a forgetful waiter**
- **Memoryless AI**: Forgets who you are every time—“What would you like to order?” No context from “refill my water.”
- **Memory AI (Chatbot)**: Keeps conversation notes and **reads the full history before replying**.

### Memory in LangChain
LangChain can **automatically append conversation history** to prompts.

| Memory mechanism | Pros | Cons |
| :--- | :--- | :--- |
| **Remember all (Buffer Memory)** | Perfect context from the start | Long chats → huge payloads → higher API cost |
| **Recent window (Window Memory)** | Only last N turns; saves tokens | Forgets older topics |

### 💡 Concrete business use cases
- **Personalized AI mentor/coaching**: Remember goals and daily progress—“Last week you struggled with X; how did it go?”
- **Long-term customer support (CRM chat)**: Reference purchase and inquiry history—“How is the product you bought last time?”
- **Game/entertainment NPCs**: Remember player actions and dialogue; attitude and lines change on next meeting.

## 2. Implementation Example

Use LangChain’s `RunnableWithMessageHistory` for a chatbot that remembers past conversation.

> ※ Newer LangChain recommends this over legacy `ConversationBufferMemory`.

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. LLMの準備
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 2. プロンプトの準備
# MessagesPlaceholder を使うことで、「ここに過去の会話履歴を挿入する」という予約席を作れます
prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは親友のようにフランクに話すチャットボットです。"),
    MessagesPlaceholder(variable_name="chat_history"), # 会話履歴が入る場所
    ("user", "{input}")
])

# チェーンを作成
chain = prompt | llm

# 3. 記憶（メモリ）の保存場所（データベースの代わり）
# ユーザーごとの会話履歴を保存する辞書を用意します
store = {}

# セッションID（ユーザーID）を受け取り、その人の会話履歴を返す関数
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory() # 新規ユーザーなら新しいノートを作成
    return store[session_id]

# 4. チェーンに「記憶機能」を合体させる
# history_messages_key に、プロンプトで予約した変数名(chat_history)を指定します
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# =========================================
# チャットボットとの会話シミュレーション
# =========================================
# 同じセッションIDを使うことで、「同一人物との連続した会話」になります
config = {"configurable": {"session_id": "user_123"}}

print("ユーザー: 私の名前はタロウです。リンゴが好きです。")
response1 = with_message_history.invoke(
    {"input": "私の名前はタロウです。リンゴが好きです。"},
    config=config
)
print("AI:", response1.content, "\n")

print("ユーザー: 私の名前を覚えていますか？好きな食べ物は何でしたっけ？")
response2 = with_message_history.invoke(
    {"input": "私の名前を覚えていますか？好きな食べ物は何でしたっけ？"},
    config=config
)
print("AI:", response2.content)
```

**🔍 Detailed code walkthrough**
1. **Prompt trick**: `MessagesPlaceholder` reserves a slot where LangChain inserts full history before the latest user message.
2. **History store**: `store = {}` holds per-user history; production uses Redis or a database.
3. **Memory wrapper**: `RunnableWithMessageHistory` auto-reads and saves history.
4. **Session continuity**: Same `session_id` lets the AI recall Taro’s prior statements.

## 3. Practice

Create an **infinite-loop chatbot** you control from the terminal.

**【Requirements】**
- Use `while True:` and `input("あなた: ")` for user input.
- Exit on `exit` or `quit`.
- Use `with_message_history` to keep context across turns.

**💡 Hint**
- History accumulates—ask about several turns ago to verify memory.

## 4. Answer Key

<details>
<summary>View sample solution (click to expand)</summary>

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは優秀なアシスタントです。会話の文脈を把握して自然に応答してください。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

chain = prompt | llm
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chatbot = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

config = {"configurable": {"session_id": "my_interactive_session"}}

print("=======================================")
print("チャットボットが起動しました。")
print("終了するには 'exit' または 'quit' と入力してください。")
print("=======================================\n")

while True:
    # ユーザーからの入力を受け取る
    user_input = input("あなた: ")
    
    # 終了コマンドの確認
    if user_input.lower() in ["exit", "quit"]:
        print("AI: お話しできて楽しかったです。さようなら！")
        break
        
    # 入力が空でなければAIに送信
    if user_input.strip() != "":
        response = chatbot.invoke(
            {"input": user_input},
            config=config
        )
        print(f"AI: {response.content}\n")
```
</details>
