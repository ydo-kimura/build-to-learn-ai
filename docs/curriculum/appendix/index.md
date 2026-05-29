# 学習環境とAPI準備 (Appendix)

本カリキュラムをスムーズに進めるための、Google Colaboratory（以下 Colab）を利用した学習手順、ライブラリのインストール方法、および第4章で必要となる OpenAI APIキーの準備と安全な管理方法についての解説です。

---

## 🚀 1. Google Colaboratory での学習の進め方

本カリキュラムの実装例や課題は、すべてブラウザだけで無料で Python が動かせる **Google Colaboratory** を前提としています。ローカルPCの環境構築やスペック（GPUなど）を気にすることなく、すぐに学習を始められます。

1. **Colab にアクセスする**
   [Google Colaboratory](https://colab.research.google.com/) にアクセスし、Googleアカウントでログインします。
2. **新規ノートブックを作成する**
   「ノートブックを新規作成」をクリックして、新しい学習用ページを用意します。
3. **GPU を有効にする（第2章以降で推奨）**
   - ディープラーニング（Unit 10〜16）や自然言語処理（Unit 17〜21）では、計算を高速化するためにGPUを使用することをおすすめします。
   - 画面上部のメニューから **「ランタイム」 > 「ランタイムのタイプを変更」** を選択し、ハードウェアアクセラレータで **「T4 GPU」** （無料枠）を選択して保存します。

---

## 📦 2. ライブラリの一括インストール方法

各Unitの実装で必要なライブラリは、Colab のセルで以下のコマンドを実行することで、一瞬でインストールできます。

学習を始める前に、ノートブックの最初のセルで以下を実行してください：

```bash
!pip install -r https://raw.githubusercontent.com/ydo-kimura/build-to-learn-ai/main/requirements.txt
```

> **💡 ローカル環境で実行する場合**
> ローカル環境（Jupyter Labなど）で実行する場合は、プロジェクトのルートにある [requirements.txt](https://github.com/ydo-kimura/build-to-learn-ai/blob/main/requirements.txt) を使用して、ターミナルで以下を実行します。
>
> ```bash
> pip install -r requirements.txt
> ```

### 後半ユニット（Unit 26 以降）で使う主なライブラリ

以下のライブラリは、いずれも上記の `requirements.txt` の一括インストールに含まれています。特定のユニットだけを個別環境（Colab の新しいノートブックなど）で進める場合は、以下のコマンドで該当分のみをインストールすることもできます。

```bash
!pip install llama-index-core llama-index-readers-file llama-index-llms-openai llama-index-embeddings-openai mcp smolagents pydantic langgraph tiktoken
```

| ライブラリ                             | 使用ユニット    | 用途                                       |
| :------------------------------------- | :-------------- | :----------------------------------------- |
| `llama-index-core` ほか llama-index 系 | Unit 26         | LlamaIndex による RAG 構築                 |
| `mcp`                                  | Unit 30         | MCP サーバーの実装（FastMCP）              |
| `smolagents`                           | Unit 31, 37, 40 | Code Agent・マルチエージェント構築         |
| `pydantic`                             | Unit 39         | 構造化データのスキーマ定義とバリデーション |
| `tiktoken`                             | Unit 22〜23     | Tokenizerの確認とToken数の測定             |
| `langgraph`                            | Unit 32         | グラフベースのステートフルエージェント     |

---

## 🔑 3. OpenAI APIキーの取得と安全な管理（第4章）

第4章「LLM応用とAIエージェント」では、OpenAIのAPIを利用します。

### ① APIキーの取得と費用について

- OpenAIの [Developer Platform](https://platform.openai.com/) にサインアップし、APIキー（`sk-...` で始まる文字列）を発行します。
- **費用について** : APIは従量課金制です。クレジットカードの登録が必要となりますが、本カリキュラムで用いる `gpt-4o-mini` は極めて低コストに設計されています。1回の実行あたり約0.01円〜0.1円程度であり、カリキュラム全体を通しても **数十円〜数百円程度** で十分に学習可能です。
- **注意** : APIキー作成時に、意図しない高額請求を防ぐために「月額利用制限（Usage limits）」を設定しておくことを強くおすすめします（例: 月最大 $5 または $10 に設定）。

### ② Colab での安全なキー管理（環境変数）

APIキーをプログラム内に直接貼り付ける（ハードコードする）ことは、セキュリティ上 **絶対に避けてください** （GitHubにアップロードした瞬間に不正利用される危険があります）。

Colab では、以下の手順で安全にAPIキーをプログラムに渡すことができます。

1. **左側メニューの「鍵マーク🔑（シークレット）」をクリック** します。
2. **名前（Name）** に `OPENAI_API_KEY` と入力します。
3. **値（Value）** に、取得した OpenAI の APIキー（`sk-...`）を貼り付けます。
4. 右側の **「ノートブックからのアクセス（Notebook access）」をオン** にします。
5. プログラム内では、以下のように環境変数として安全に呼び出します。
   ```python
   import os
   from google.colab import userdata

   # Colabのシークレットからキーを取得し、環境変数にセットする
   os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
   ```

---

## 📊 4. 進捗管理用 CSV を使ったタスク管理 (Linear / GitHub Projects)

本カリキュラムは「毎日1ユニットずつ進める」ことで確実にAIエンジニアの実力を身につけるように設計されています。この学習の継続とモチベーション維持のために、`docs/` ディレクトリに進捗管理用のCSVファイル **`tasks-export.csv`** を同梱しています。

このCSVファイルをお好みのタスク管理ツールにインポートするだけで、一瞬で全ユニット（＋環境構築）の美しいカンバンボードやTODOリストを構築して、進捗を視覚的に管理できます。

### ① Linear へのインポート手順（推奨）

[Linear](https://linear.app/) は、現代のAIエンジニアにとって最も動作が高速でモダンなタスク管理ツールです。

1. リポジトリ内の [tasks-export.csv](https://github.com/ydo-kimura/build-to-learn-ai/blob/main/docs/tasks-export.csv) をローカルマシンにダウンロードします（`git clone` している場合はそのまま利用可能）。
2. Linear にサインインし、左上メニューの **「Settings（設定）」 > 「Import / export（インポート / エクスポート）」** にアクセスします。
3. **「Import」** セクションから、 **「CSV」** を選択します。
4. ダウンロードした `tasks-export.csv` をドラッグ＆ドロップします。
5. CSVのカラムとLinearのフィールドを以下のように対応（マッピング）させてインポートを実行します：
   - `Title` ──> **Title** (タスク名)
   - `Description` ──> **Description** (タスク詳細・カリキュラムのmdファイルへの直リンク付き)
   - `Status` ──> **Status** (「Todo」の状態でインポートされます)
   - `Label` ──> **Labels** (どの章に属しているかを示すタグ: `Chapter-1` など)
   - `Priority` ──> **Priority** (重要度: `Medium` / `High` / `Critical`)
6. これにより、Linear上に全ユニットのタスクカードが自動生成され、自分の進捗に合わせて「Todo ──> In Progress ──> Done」と動かして管理できるようになります。

### ② GitHub Projects へのインポート手順

GitHubの各リポジトリに紐づく [GitHub Projects](https://docs.github.com/ja/issues/planning-and-tracking-with-projects) でも同様にタスクを管理できます。

1. あなたの GitHub アカウントで本リポジトリを Fork またはプライベートリポジトリとして作成します。
2. リポジトリ上部タブの **「Projects」** をクリックし、 **「New project」** をクリックします（「Table」または「Board」テンプレートを選択）。
3. GitHub Projects には CSV を直接インポートする公式機能がないため、GitHub CLI（`gh`）でCSVの各行を Issue として一括登録し（例: シェルスクリプトで `gh issue create --title ... --label ...` をループ実行）、作成された Issue を Projects に追加してカンバンを作成するのが確実です。
4. インポート完了後、各タスクカードから「VitePress上の教材マークダウンファイル」に直接クリックでアクセスでき、日々の学習管理が極めてスムーズになります。
