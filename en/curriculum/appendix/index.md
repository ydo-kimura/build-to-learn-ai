# Appendix: Learning Environment and API Setup

This guide covers learning with Google Colaboratory (Colab), installing required libraries, and preparing and securely managing the OpenAI API key needed from Chapter 4 onward.

---

## 🚀 1. Learning with Google Colaboratory

All implementation examples and assignments assume **Google Colaboratory**, where you can run Python for free in the browser. You can start immediately without local environment setup or worrying about hardware specs (GPU, etc.).

1. **Access Colab**
   Go to [Google Colaboratory](https://colab.research.google.com/) and sign in with your Google account.
2. **Create a new notebook**
   Click **New Notebook** to create a fresh workspace.
3. **Enable GPU (recommended from Chapter 2 onward)**
   * For deep learning (Units 10–16) and NLP (Units 17–21), we recommend enabling a GPU to speed up computation.
   * From the top menu, select **Runtime > Change runtime type**, choose **T4 GPU** (free tier) under hardware accelerator, and save.

---

## 📦 2. Bulk Library Installation

Install all libraries required for each unit in one Colab cell:

Run this at the top of your notebook before you start learning:

```bash
!pip install -r https://raw.githubusercontent.com/[Your-Username]/[Your-Repo]/main/requirements.txt
```

> **💡 Running locally**
> If you use a local environment (e.g., Jupyter Lab), use [requirements.txt](../../requirements.txt) at the project root and run:
> ```bash
> pip install -r requirements.txt
> ```

---

## 🔑 3. OpenAI API Key: Acquisition and Secure Management (Chapter 4)

Chapter 4, **LLM Applied & AI Agents**, uses the OpenAI API.

### ① API key and costs
* Sign up at the [OpenAI Developer Platform](https://platform.openai.com/) and issue an API key (a string starting with `sk-...`).
* **Costs**: The API is pay-as-you-go and requires a credit card. This curriculum uses `gpt-4o-mini`, which is designed to be very inexpensive—roughly $0.0001–$0.001 per run, so the full curriculum typically costs only a few cents to a few dollars.
* **Important**: When creating your API key, we strongly recommend setting a monthly usage limit to prevent unexpected charges (e.g., max $5 or $10 per month).

### ② Secure key management in Colab (environment variables)
Never paste your API key directly into code (**hardcoding**). If you upload that to GitHub, it can be abused immediately.

In Colab, pass the key securely as follows:

1. Click the **key icon 🔑 (Secrets)** in the left sidebar.
2. Under **Name**, enter `OPENAI_API_KEY`.
3. Under **Value**, paste your OpenAI API key (`sk-...`).
4. Turn **Notebook access** ON.
5. In your code, load it as an environment variable:
   ```python
   import os
   from google.colab import userdata

   # Load the key from Colab Secrets into the environment
   os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
   ```

---

## 📊 4. Task Management with CSV (Linear / GitHub Projects)

This curriculum is designed so that advancing **one unit per day** steadily builds your skills as an AI engineer. To support consistency and motivation, we bundle a progress-tracking CSV file, **`tasks-export.csv`**, in the repository root.

Import this CSV into your preferred task manager to instantly build a Kanban board or TODO list for all units (plus environment setup) and track progress visually.

### ① Importing to Linear (recommended)
[Linear](https://linear.app/) is a fast, modern task manager well suited to software engineers.

1. Download [tasks-export.csv](../../tasks-export.csv) from the repository root (or use it directly if you cloned the repo).
2. Sign in to Linear and open **Settings > Import / export**.
3. Under **Import**, select **CSV**.
4. Drag and drop `tasks-export.csv`.
5. Map CSV columns to Linear fields as follows:
   * `Title` ──> **Title**
   * `Description` ──> **Description** (includes direct links to curriculum markdown files)
   * `Status` ──> **Status** (imports as "Todo")
   * `Label` ──> **Labels** (chapter tags such as `Chapter-1`)
   * `Priority` ──> **Priority** (`Medium` / `High` / `Critical`)
6. Linear will generate task cards for all units. Move them through **Todo → In Progress → Done** as you progress.

### ② Importing to GitHub Projects
You can manage tasks the same way with [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects) linked to your repository.

1. Fork this repository or create a private copy under your GitHub account.
2. Click **Projects** in the repository tab bar, then **New project** (choose Table or Board template).
3. Bulk-import via GitHub CLI as Issues, or use a third-party CSV import tool (e.g., `github-project-import`) or browser extension. Map fields (Title, Description, Status, Label) to build your Kanban board.
4. After import, each task card links directly to the curriculum markdown on VitePress, making daily study management smooth.
