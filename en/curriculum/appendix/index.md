# Appendix: Learning Environment and API Setup

This guide walks you through setting up your environment on Google Colaboratory, installing required libraries, securely managing your OpenAI API key, and tracking your progress using project management boards.

---

## 🚀 1. Learn Using Google Colaboratory

All units are designed to run out-of-the-box on **Google Colaboratory (Colab)**. You do not need to install local environments or worry about GPU hardware.

1. **Access Google Colab**: Navigate to [Google Colaboratory](https://colab.research.google.com/) and sign in with your Google account.
2. **Create Notebook**: Click "New Notebook" to prepare a fresh workstation.
3. **Enable GPU (Recommended for Chapter 2+)**:
   * For Deep Learning (Unit 9-14) and NLP (Unit 15-18), using a GPU will accelerate execution.
   * Go to **Runtime > Change runtime type**, select **T4 GPU** (free tier), and click Save.

---

## 📦 2. Fast Library Installation

You can install all required packages at once in a Colab code cell:

Run this command at the top of your notebook:
```bash
!pip install -r https://raw.githubusercontent.com/[Your-Username]/[Your-Repo]/main/requirements.txt
```

> **💡 Running Locally?**
> If you prefer running models locally (e.g., Jupyter Lab), navigate to the monorepo root and execute:
> ```bash
> pip install -r requirements.txt
> ```

---

## 🔑 3. Acquire & Secure OpenAI API Key (For Chapter 4 & 5)

For Chapter 4 (LLMs) and Chapter 5 (Capstones), you will integrate with OpenAI.

### ① API Key Issuance and Costs
* Sign up at [OpenAI Developer Platform](https://platform.openai.com/) and generate an API key (`sk-...`).
* **Cost Estimation**: OpenAI API is pay-as-you-go. The model used (`gpt-4o-mini`) is highly cost-efficient. Each call costs around $0.0001 to $0.001. The entire curriculum will only cost a few cents.
* **Tip**: We strongly advise setting a budget cap (e.g., max $5/month) in the OpenAI usage limits panel to prevent accidental charges.

### ② Secure Key Management (Environment Variables)
Never paste your raw API key directly in code cells (hardcoding key poses severe security risk of leakages on GitHub).

In Google Colab, securely store it via **Secrets**:
1. Click the **Key icon 🔑 (Secrets)** on the left sidebar.
2. Under **Name**, enter `OPENAI_API_KEY`.
3. Under **Value**, paste your OpenAI API key.
4. Toggle **Notebook access** ON.
5. In your code, load it dynamically using:
   ```python
   import os
   from google.colab import userdata

   os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
   ```

---

## 📊 4. Task Management via CSV (Linear / GitHub Projects)

To help maintain study momentum and visualize progress, we have bundled **`tasks-export.csv`** in the repository root.

By importing this file into your favorite PM tools, you can instantly spin up a Kanban board covering all 33 units.

### ① Importing to Linear (Recommended)
[Linear](https://linear.app/) is a modern, high-speed task manager built for software developers.

1. Download [tasks-export.csv](../../tasks-export.csv) from your repository root.
2. Sign in to Linear and go to **Settings > Import / export**.
3. Under **Import**, select **CSV**.
4. Drag and drop your `tasks-export.csv` file.
5. Map the CSV columns to Linear fields as follows:
   * `Title` ──> **Title**
   * `Description` ──> **Description** (Includes direct markdown links to curriculum files)
   * `Status` ──> **Status** (Imports as "Todo")
   * `Label` ──> **Labels** (Indicates chapters: e.g., `Chapter-1`)
   * `Priority` ──> **Priority** (`Medium` / `High` / `Critical`)
6. Execute import to instantly populate your Kanban board!

### ② Importing to GitHub Projects
You can track progress directly in your GitHub Fork repository via [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects).

1. In your GitHub repository, click **Projects** on the top navigation bar, then click **New project** (Select Board or Table template).
2. You can bulk-import the tasks using GitHub CLI or import tools like `github-project-import`.
3. Map the fields (Title, Description, Status, Label) to build a beautiful tracking dashboard.
