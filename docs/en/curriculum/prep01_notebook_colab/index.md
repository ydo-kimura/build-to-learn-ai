# Prep 1: Notebook and Colab Foundations

In this Prep, you will learn how to use Google Colaboratory (Colab) to enter code yourself, run it in the intended order, and inspect the result.

A notebook is different from a program that you always run from beginning to end. You can execute small pieces of code in separate cells, but the order in which you run those cells can cause the visible code and the values in the runtime to disagree. The main purpose of this Prep is to observe that difference yourself.

## Learning goals

- Create, edit, run, and delete code and text cells
- Inspect cell output and execution state
- Explain the difference between a notebook and its runtime
- Explain why cells should be run from top to bottom
- Read an error, correct the code, and rerun the cell
- Restart the runtime and run every cell from the beginning

## Skip check

Open a new Colab notebook and check whether you can do the following without instructions:

1. Create one code cell and one text cell
2. Use the same variable in two code cells and explain why execution order can change the output
3. Restart the runtime and confirm that the variable is gone
4. Read the last line of an error, correct the code, and rerun it
5. Use **Run all** to reproduce the same result from top to bottom

You may skip this Prep if you can complete every operation and explain why each result occurs. If there is even one operation you cannot complete or explain, continue through the hands-on exercise.

## Before you begin

For access to Colab and creation of a new notebook, see **Learning with Google Colaboratory** in [Environment and API Setup (Appendix)](../appendix/index.md). This Prep starts with an empty notebook that you have already created.

## 1. A notebook is a file made of cells

A notebook mainly uses two kinds of cells.

| Cell      | What it contains                  | What happens when it runs                                         |
| --------- | --------------------------------- | ----------------------------------------------------------------- |
| Code cell | Python code                       | The code runs and, when applicable, output appears below the cell |
| Text cell | Headings, explanations, and notes | Markdown is formatted as readable text                            |

In Colab, use **+ Code** and **+ Text** at the top of the page to add cells. Click a cell to edit it. Run a code cell with the run button on its left or with `Shift + Enter`.

When a cell is selected, its toolbar or more-actions menu lets you move or delete it. If you delete a cell accidentally, immediately use **Edit > Undo cell operation** to restore it.

### Code cells and output

Enter the following code in one code cell and run it.

```python
message = "First run"
print(message)
```

The following output appears below the cell.

```text
First run
```

The left side of a code cell distinguishes a cell that has not run, is running, or has finished. When your interface shows an execution number, it means “which execution occurred in the current runtime,” not “where this cell appears in the notebook.”

If you run the same cell again, its output is replaced by the new result and its execution number is updated.

### Text cells

Enter the following content in a text cell.

```markdown
## Experiment notes

Use this cell to record the purpose of the code and what the result shows.
```

When you run the text cell, `##` is rendered as a heading. While learning, use text cells to record both your prediction before execution and your interpretation of the result.

## 2. A notebook and its runtime are different

The notebook is the file that stores the code and text written in its cells. The runtime is the execution environment that runs the code and temporarily remembers variables you create.

Run the following two code cells from top to bottom.

Cell A:

```python
status = "first value"
```

Cell B:

```python
print(status)
```

The output is:

```text
first value
```

When Cell A runs, the runtime remembers a variable named `status` and its value. Cell B reads and displays the value currently remembered by the runtime.

### When visible code and the runtime value disagree

Edit Cell A as follows, but do not run it yet.

```python
status = "second value"
```

If you now run only Cell B again, the output is still:

```text
first value
```

Cell A visibly contains `"second value"`, but editing a cell does not change the runtime. Run Cell A and then Cell B, and the output changes to `second value`.

The basic way to avoid this mismatch is to run cells from top to bottom.

## 3. Restart and Run all

Restarting the runtime clears variables and other state that the runtime temporarily remembered. The cells written in the notebook remain.

1. Select **Runtime > Restart session**
2. Without running Cell A, run only `print(status)` in Cell B
3. Confirm that a `NameError` appears

After a restart, the runtime does not yet know `status`, so Cell B cannot run by itself. Run Cell A and then Cell B to display the value again.

Use **Runtime > Run all** when you want to check whether the entire notebook can be reproduced. A notebook that works only after you run a later cell early is not reproducible from top to bottom.

The runtime state can also be lost when you close the browser or Colab disconnects after a period of inactivity. A saved notebook can remain even when variables and temporary files from its runtime do not.

## 4. An error tells you where to start looking

Run the following cell as-is in a new runtime.

```python
print(course_name)
```

Because `course_name` does not exist yet, the final line contains an error like:

```text
NameError: name 'course_name' is not defined
```

When an error is long, begin with its last line. Here it says that the name `course_name` has not been defined.

Correct the same cell as follows and run it again.

```python
course_name = "AI curriculum"
print(course_name)
```

```text
AI curriculum
```

An error does not mean that you need to create a new notebook. Inspect the cause, correct the code, and rerun the cell. After correcting it, restart the runtime and use **Run all** to confirm that the notebook also works from top to bottom.

## 5. Saving and copying a notebook

A notebook created in Colab is stored in Google Drive, and edits are saved automatically. To preserve the original while making a separate experiment, select **File > Save a copy in Drive**.

The notebook stores cell code, text, and saved output. Saving is not the same as saving the variables remembered by the runtime. When you open the notebook on another day, run its cells from top to bottom to recreate its state.

## 6. Turn off AI assistance before the hands-on exercise

For the following hands-on exercise, turn off Colab’s AI code completion and generation. The goal is to create the cells yourself, predict the output, read the error, and correct it instead of copying a suggested answer.

1. Open **Tools > Settings** in Colab
2. Select **AI Assistance**
3. Disable AI coding features, or revoke consent and hide the AI features shown in that panel
4. Close Settings and confirm that AI suggestions no longer appear while you type

If AI features are not visible in your account, no action is needed. Interfaces and account availability can differ; see the [official Google Colab FAQ](https://research.google.com/colaboratory/intl/en-GB/faq.html) if the setting differs.

AI assistance is not prohibited throughout the curriculum. After completing this hands-on exercise, you may enable it again from the same settings panel when appropriate.

## 7. Hands-on practice

Prepare an empty notebook and complete the following steps from top to bottom. Do not open the expected results yet. Before each execution, write your prediction in a text cell.

### Step 1: Create code and text cells

1. Add a text cell. Enter the heading “Notebook execution experiment” and describe the purpose of the experiment, then run the cell.
2. Add a code cell below it and run the following code.

```python
note = "The first cell ran"
print(note)
```

3. Record the displayed output and the interface indication that tells you the code cell has finished.
4. Add one more empty code cell, delete it, and restore it with **Edit > Undo cell operation**.

### Step 2: Observe how execution order affects a value

Create Cell A and Cell B.

Cell A:

```python
color = "blue"
```

Cell B:

```python
print(color)
```

1. Run Cell A and then Cell B. Record the output.
2. Edit Cell A to `color = "red"`, but do not run it yet.
3. Predict what will appear if you run only Cell B now.
4. Run Cell B and compare the result with your prediction.
5. Run Cell A and then Cell B. Observe how the output changes.

### Step 3: Restart the runtime

1. Select **Runtime > Restart session**.
2. Predict what will happen if you run only Cell B immediately after the restart.
3. Run Cell B and record the final line of the error.
4. Run Cell A and then Cell B, and confirm that the error is resolved.

### Step 4: Correct an error and rerun the cell

Enter the following code in a new code cell and run it.

```python
print(topic)
```

1. Record the type of error displayed.
2. Use the last line to explain what is missing.
3. Correct the same cell so that it assigns `"Notebook"` to `topic` before displaying it.
4. Rerun the corrected cell and confirm that it displays `Notebook`.

### Step 5: Reproduce the notebook from the top

1. Restart the runtime again.
2. Select **Run all**.
3. Confirm that execution reaches the end and reproduces the same results.
4. If execution stops with an error, find which required variable was not created before the failing cell and correct the cell order or code.

### Step 6: Confirm saving and copying

1. Rename the notebook.
2. Confirm that it is saved in Google Drive.
3. Select **File > Save a copy in Drive**.
4. Confirm that the original and copy are separate files.

### Hints

- Editing a cell does not change the value in the runtime.
- A `NameError` appears when the runtime does not yet know a name you used.
- If **Run all** stops, inspect the order above the cell where it stopped.
- The saved notebook and the currently connected runtime are different things.

## 8. Answer key

Open this section only after attempting every step and recording your predicted and actual outputs.

<details>
<summary>Show answers and checkpoints</summary>

### Step 1

The code cell displays:

```text
The first cell ran
```

The text cell is formatted as a heading and paragraph. The code cell shows a finished state or execution number.

### Step 2

Running Cell A and then Cell B initially displays `blue`.

After you edit Cell A to `"red"` without running it, Cell B still displays `blue`. The runtime still remembers the value `"blue"` from the last execution of Cell A.

After you run the edited Cell A and then Cell B, the output is `red`. Changing the visible code and executing that code to change runtime state are separate actions.

### Step 3

Running only Cell B immediately after a restart produces an error like:

```text
NameError: name 'color' is not defined
```

The restart removed the variable `color` from the runtime. Running Cell A before Cell B recreates it and displays `red`.

### Step 4

The initial `print(topic)` raises a `NameError` because `topic` has not been created. One correction is:

```python
topic = "Notebook"
print(topic)
```

```text
Notebook
```

### Step 5

If **Run all** reaches the end after a restart, the notebook creates every required variable from top to bottom.

If the uncorrected `print(topic)` remains, execution stops there. As in the corrected Step 4 cell, `topic` must be created before it is used.

### Step 6

The notebook name and content are stored in Google Drive. The file created by **Save a copy in Drive** can be edited independently of the original.

However, the current runtime—not the saved file—remembers variables such as `color` and `topic`. When you open the copy or return on another day, run the cells from the top to recreate the state.

</details>

## Completion check

You have completed Prep 1 when you can confirm all of the following:

- You created, ran, and deleted code and text cells yourself
- You recorded predicted and actual outputs
- You explained why editing a cell alone does not change the runtime value
- You explained the `NameError` after a restart
- You corrected an error and reran the same cell
- You reproduced the result with **Run all** after a restart
- You explained the difference between saved notebook content and runtime state

If you turned off AI assistance for the hands-on exercise, you may enable it again from **Tools > Settings > AI Assistance** when appropriate.
