# Prep 2: Python Foundations

This Prep teaches the Python foundations needed to read the code in Unit 01 and later units. You will not only look at finished code: you will predict values, type and run the code yourself, modify it, and inspect what changes.

This lesson is for learners who are new to Python. If you can already use variables, lists, dictionaries, conditions, loops, functions, and imports, and can explain the difference between an attribute and a method, complete the skip check and continue to the next Prep.

This Prep assumes that you have completed [Prep 1: Notebook and Colab Foundations](../prep01_notebook_colab/index.md). Review Prep 1 first if you are unsure about Colab operation or cell execution order.

## Learning goals

- Assign values to variables and distinguish numbers, strings, and booleans
- Group multiple values in lists and dictionaries and retrieve the values you need
- Use indentation to show the scope of `if` and `for`
- Pass arguments to a function and receive its return value
- Explain the difference between `object.attribute` and `object.method()`
- Import and use a required feature
- Inspect values with `print()` and f-strings
- Use the final line of an error to decide what to inspect first

## Skip check

Read the following code without running it.

```python
scores = [72, 85, 91]

def average(values):
    return sum(values) / len(values)

result = average(scores)

if result >= 80:
    print(f"Average: {result:.1f}, status: pass")
else:
    print(f"Average: {result:.1f}, status: try again")
```

You may skip this Prep if you can answer all of the following:

1. What `scores`, `values`, and `result` each represent
2. What values `scores[0]` and `scores[:2]` produce
3. Where values move when `average(scores)` runs
4. Which line receives the value returned by `return`
5. Whether `result >= 80` is `True` or `False`
6. The exact string displayed at the end
7. The difference between code such as `values` and `values.append(100)`

If there is even one item you cannot explain, continue from the beginning.

## Before you begin

Create one new Colab notebook and enter the code in this Prep from top to bottom. Before running each example, record your predicted output in a text cell.

For hands-on learning, we recommend turning off Colab AI assistance so that you can compare your own code with the actual result. See **Turn off AI assistance before the hands-on exercise** in Prep 1.

Every example in this Prep uses only Python built-ins or the standard library. You do not need to install NumPy or pandas.

## 1. Assign values to variables

A program works with values such as numbers and text. A variable gives a value a name so that you can use it later.

```python
learner_name = "Aoi"
score = 72
completed = False

print(learner_name)
print(score)
print(completed)
```

```text
Aoi
72
False
```

The `=` symbol assigns the value on its right to the variable on its left. It does not ask whether both sides are equal. Here, the string `"Aoi"` is given the name `learner_name`.

Assigning a new value to the same variable replaces the value used afterward.

```python
score = 72
score = 80
print(score)
```

```text
80
```

Python is case-sensitive. `score` and `Score` are different names.

### Basic value types

These are the first value types you will often use in this curriculum.

| Kind    | Python name | Example         | Typical use                    |
| ------- | ----------- | --------------- | ------------------------------ |
| Integer | `int`       | `72`            | Counts and whole-number scores |
| Decimal | `float`     | `72.5`          | Averages, ratios, measurements |
| String  | `str`       | `"Aoi"`         | Names, labels, explanations    |
| Boolean | `bool`      | `True`, `False` | Whether a condition holds      |

Use `type()` to inspect the type of a value.

```python
print(type(72))
print(type(72.5))
print(type("Aoi"))
print(type(False))
```

```text
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
```

For now, it is enough to understand that `class` identifies the kind of value. This Prep does not teach how to define classes.

## 2. Calculate and compare

Operators let you calculate with numbers.

```python
first_score = 72
second_score = 85

total = first_score + second_score
average_of_two = total / 2

print(total)
print(average_of_two)
```

```text
157
78.5
```

| Operator | Meaning        | Example  | Result |
| -------- | -------------- | -------- | ------ |
| `+`      | Addition       | `7 + 2`  | `9`    |
| `-`      | Subtraction    | `7 - 2`  | `5`    |
| `*`      | Multiplication | `7 * 2`  | `14`   |
| `/`      | Division       | `7 / 2`  | `3.5`  |
| `**`     | Exponent       | `3 ** 2` | `9`    |

A comparison produces the boolean value `True` or `False`.

```python
score = 72

print(score >= 70)
print(score == 80)
print(score != 80)
```

```text
True
False
True
```

| Operator | Question it asks                         |
| -------- | ---------------------------------------- |
| `==`     | Are the values equal?                    |
| `!=`     | Are the values different?                |
| `>`      | Is the left value greater?               |
| `<`      | Is the left value smaller?               |
| `>=`     | Is the left value greater than or equal? |
| `<=`     | Is the left value smaller than or equal? |

Assignment `=` and equality comparison `==` have different roles.

## 3. Group ordered values in a list

A list groups multiple values in order. Separate the values with commas inside square brackets `[]`.

```python
scores = [72, 85, 91]
print(scores)
```

```text
[72, 85, 91]
```

### Retrieve one value by index

An index is a number that identifies a position in a list. Python indexes start at `0`.

```python
scores = [72, 85, 91]

print(scores[0])
print(scores[1])
print(scores[2])
```

```text
72
85
91
```

Even though the list has three values, its last index is `2`.

### Retrieve a range with a slice

A slice retrieves part of a list as a new list.

```python
scores = [72, 85, 91]
print(scores[0:2])
print(scores[:2])
```

```text
[72, 85]
[72, 85]
```

`0:2` means start at index `0` and stop immediately before index `2`. The value at `scores[2]` is not included. When starting at the beginning, omit `0` and write `scores[:2]`.

### Change a list

The `append()` method adds a value to the end.

```python
scores = [72, 85, 91]
scores.append(88)
print(scores)
```

```text
[72, 85, 91, 88]
```

`len()` returns the number of values.

```python
print(len(scores))
```

```text
4
```

## 4. Associate names and values in a dictionary

A dictionary manages pairs of keys and values. A list retrieves a value by position; a dictionary retrieves a value by key.

```python
learner_scores = {
    "Aoi": 72,
    "Ren": 85,
    "Mio": 91,
}

print(learner_scores["Ren"])
```

```text
85
```

The learner names are keys and the scores are values. `learner_scores["Ren"]` retrieves the value associated with the key `"Ren"`.

Specify a key to add or replace a value.

```python
learner_scores["Sora"] = 88
learner_scores["Aoi"] = 80

print(learner_scores["Sora"])
print(learner_scores["Aoi"])
```

```text
88
80
```

The hands-on exercise stores a list of scores as each dictionary value.

```python
learner_scores = {
    "Aoi": [72, 80, 88],
    "Ren": [65, 70, 75],
    "Mio": [90, 94, 96],
}

print(learner_scores["Aoi"])
print(learner_scores["Aoi"][0])
```

```text
[72, 80, 88]
72
```

The first pair of brackets selects Aoi’s list. The following `[0]` retrieves the first score in that list.

## 5. Branch with `if`

An `if` statement runs a block only when its condition is `True`. Use `else` for the block that runs when the condition is false.

```python
score = 72

if score >= 80:
    print("pass")
else:
    print("try again")
```

```text
try again
```

The `if` and `else` lines end with a colon `:`. Indent the lines that belong to each block. Python uses this indentation to identify the block; it is not merely visual spacing. This curriculum uses four spaces for one indentation level.

## 6. Repeat with `for`

A `for` loop takes values from a list or another collection one at a time and repeats the same block.

```python
scores = [72, 85, 91]

for score in scores:
    print(score)
```

```text
72
85
91
```

On the first iteration, `score` receives `72`; then it receives `85` and `91`. The loop stops after using every value.

Blocks can be nested.

```python
scores = [72, 85, 91]

for score in scores:
    if score >= 80:
        print(score)
```

```text
85
91
```

`print(score)` is inside `if`, which is inside `for`. Each score is checked, but only values of 80 or more are displayed.

## 7. Group a calculation in a function

A function is a named block of work. Define a function when you want to reuse the same calculation.

```python
def average(values):
    total = sum(values)
    count = len(values)
    return total / count
```

`def` defines a function. `average` is its name, and `values` is a parameter that receives an argument.

Defining the function does not run the calculation. Call it by writing parentheses after its name and passing the required value.

```python
scores = [72, 85, 91]
result = average(scores)
print(result)
```

```text
82.66666666666667
```

The values move as follows:

1. `average(scores)` passes `[72, 85, 91]` to the function.
2. Inside the function, the list is named `values`.
3. `sum(values)` returns the total and `len(values)` returns the count.
4. `return total / count` returns the result to the caller.
5. `result` receives the returned value.

`print()` displays a value on screen. `return` sends a value back to the caller and ends the function at that point.

The same function accepts another list.

```python
first_result = average([72, 80, 88])
second_result = average([90, 94, 96])

print(first_result)
print(second_result)
```

```text
80.0
93.33333333333333
```

The calculation stays the same, while changing the argument changes the return value.

## 8. Inspect results with `print()` and f-strings

Passing a variable to `print()` displays its value. An f-string, marked by `f` before the opening quote, embeds values in text.

```python
learner_name = "Aoi"
result = 80.0

print(f"{learner_name}'s average is {result}")
```

```text
Aoi's average is 80.0
```

A variable inside braces `{}` is replaced by its value. You can also specify the displayed decimal places.

```python
result = 93.33333333333333
print(f"Average: {result:.1f}")
```

```text
Average: 93.3
```

`:.1f` displays one digit after the decimal point. It rounds the displayed text but does not replace the original value stored in `result`.

## 9. Distinguish attributes and methods

Python often uses a dot `.` to connect a value with related information or behavior.

```text
object.attribute
object.method()
```

- An attribute is information held by an object. It has no call parentheses.
- A method is an operation related to an object. Call it with parentheses `()`.

Use a date from the standard library to observe the difference.

```python
from datetime import date

lesson_date = date(2026, 7, 26)

print(lesson_date.year)
print(lesson_date.isoformat())
```

```text
2026
2026-07-26
```

`lesson_date.year` is an attribute containing the year. `lesson_date.isoformat()` is a method that converts the date to a string in a defined format.

Unit 01 and later units contain code such as:

```python
X.shape
model.fit(X, y)
```

`X.shape` is an attribute containing the number of rows and columns, so it has no parentheses. `model.fit(X, y)` is a method that trains a model, so it is called with arguments in parentheses.

The list expression `scores.append(88)` and dictionary expression `learner_scores.items()` are also method calls.

## 10. Import a required feature

Not every Python feature is available under a name in your program from the beginning. Use `import` to load a feature from another module.

```python
import math

print(math.sqrt(81))
```

```text
9.0
```

`import math` loads the `math` module. Refer to its functions with the module name, as in `math.sqrt()`.

You can also import one name from a module.

```python
from datetime import date

today = date(2026, 7, 26)
print(today)
```

```text
2026-07-26
```

`from datetime import date` loads only `date` from the `datetime` module. You can then call it directly as `date(...)`.

Unit 01 contains an import like:

```python
from sklearn.datasets import load_diabetes
```

This loads the function `load_diabetes` from `sklearn.datasets`. Afterward, `load_diabetes()` calls that function.

## 11. Read the final line of an error

An error tells you where to begin checking your code. When the output looks long, start with its final line.

### `NameError`: the name has not been created

```python
print(final_score)
```

```text
NameError: name 'final_score' is not defined
```

The name `final_score` has not been created by an assignment or definition. Check its spelling and capitalization and whether you ran the required cell first.

### `KeyError`: the dictionary does not contain the key

```python
learner_scores = {"Aoi": 72, "Ren": 85}
print(learner_scores["Mio"])
```

The final line is:

```text
KeyError: 'Mio'
```

The dictionary does not contain the key `"Mio"`. Use `learner_scores.keys()` to inspect the available keys.

You do not need to delete a cell after an error. Identify the cause, correct the same cell, and run it again. Finally, restart the runtime and run every cell from the top to confirm that the notebook is reproducible.

## 12. Hands-on practice

Combine values, lists, dictionaries, conditions, loops, functions, and f-strings to summarize learning records for three people.

Open the answer key only after trying every step. For each step, first predict the output, then run the code, and finally record why any difference occurred.

### Step 1: Inspect the data

Enter and run this dictionary.

```python
learner_scores = {
    "Aoi": [72, 80, 88],
    "Ren": [65, 70, 75],
    "Mio": [90, 94, 96],
}
```

Write code yourself to display:

1. Aoi’s score list
2. Ren’s first score
3. Mio’s first two scores
4. The number of learners in `learner_scores`

Predict each result before displaying it.

### Step 2: Write a function that returns an average

Define a function named `average` that receives a list of numbers and returns the total divided by the count.

Pass Aoi’s score list to the function, assign the return value to `aoi_average`, and display it. Calculate the expected average by hand first.

### Step 3: Display all three averages

The `items()` method retrieves every key and value from a dictionary.

```python
for name, scores in learner_scores.items():
    print(name, scores)
```

Use this shape to call `average(scores)` for each learner and display:

```text
Aoi: 80.0
Ren: 70.0
Mio: 93.3
```

Use `:.1f` in an f-string to display one decimal place.

### Step 4: Add a status with a condition

Assign `"pass"` to `status` when the average is 80 or more, and `"try again"` otherwise. Display the name, average, and status as:

```text
Aoi: 80.0 - pass
Ren: 70.0 - try again
Mio: 93.3 - pass
```

Place `if` and `else` inside `for`. Place `print()` where it runs once for each learner.

### Step 5: Add one learner and rerun

Add this learner to the dictionary:

```python
learner_scores["Sora"] = [78, 82, 85]
```

Before rerunning Step 4, predict Sora’s average and status. Then explain why the same loop handles four learners without changing its body.

### Step 6: Read and correct an error

Run this code as written:

```python
print(learner_scores["Rin"])
```

1. Record the final line of the error.
2. Explain the error type and cause.
3. Inspect the keys that actually exist.
4. Replace `"Rin"` with an existing key and rerun the same cell.

### Hints

- Retrieve a dictionary value with `dictionary[key]`.
- The first list value is `[0]`; the first two values are `[:2]`.
- Use `len()` for the count and `sum()` for the total.
- Use `return` to send a calculated value out of a function.
- Do not omit the parentheses in `items()`.
- Lines containing `if`, `else`, and `for` end with a colon.

## 13. Answer key

<details>
<summary>Show answers and checkpoints</summary>

### Step 1

```python
print(learner_scores["Aoi"])
print(learner_scores["Ren"][0])
print(learner_scores["Mio"][:2])
print(len(learner_scores))
```

```text
[72, 80, 88]
65
[90, 94]
3
```

The dictionary key selects one learner’s list. An index or slice can then retrieve values from that list. `len(learner_scores)` returns the number of dictionary keys.

### Step 2

```python
def average(values):
    return sum(values) / len(values)

aoi_average = average(learner_scores["Aoi"])
print(aoi_average)
```

```text
80.0
```

The list from `learner_scores["Aoi"]` becomes `values`. `aoi_average` receives the value `80.0` returned by the function.

### Step 3

```python
for name, scores in learner_scores.items():
    result = average(scores)
    print(f"{name}: {result:.1f}")
```

```text
Aoi: 80.0
Ren: 70.0
Mio: 93.3
```

`items()` retrieves each dictionary key and value as a pair. `name` receives the key, and `scores` receives its score list.

### Step 4

```python
for name, scores in learner_scores.items():
    result = average(scores)

    if result >= 80:
        status = "pass"
    else:
        status = "try again"

    print(f"{name}: {result:.1f} - {status}")
```

```text
Aoi: 80.0 - pass
Ren: 70.0 - try again
Mio: 93.3 - pass
```

Aoi’s average is exactly `80.0`. The condition uses `>=`, not `>`, so the status is pass.

### Step 5

```python
learner_scores["Sora"] = [78, 82, 85]

for name, scores in learner_scores.items():
    result = average(scores)

    if result >= 80:
        status = "pass"
    else:
        status = "try again"

    print(f"{name}: {result:.1f} - {status}")
```

```text
Aoi: 80.0 - pass
Ren: 70.0 - try again
Mio: 93.3 - pass
Sora: 81.7 - pass
```

The loop processes every item currently in the dictionary. Adding Sora changes the data, so the function and loop body do not need to change.

### Step 6

The final line is:

```text
KeyError: 'Rin'
```

The key `"Rin"` does not exist.

```python
print(learner_scores.keys())
```

After inspecting the keys, one correction is:

```python
print(learner_scores["Sora"])
```

```text
[78, 82, 85]
```

</details>

## Completion check

You have completed Prep 2 when you can confirm all of the following:

- You can explain assigned values and the results of `type()`.
- You can explain the different roles of `=` and `==`.
- You retrieved list values with an index and a slice.
- You retrieved a dictionary value with a key.
- You used indentation to show the scope of `if` and `for`.
- You passed an argument to a function and assigned its return value.
- You can explain why an attribute has no call parentheses and a method does.
- You can read `import` and `from ... import ...`.
- You displayed a name and formatted decimal with an f-string.
- You used the final line of `NameError` and `KeyError` to explain the cause.
- You restarted the runtime and reproduced the hands-on result from the top.

If you cannot explain an item, return to that section, change one value, and run it again. If you can explain how the result changes, you understand the behavior rather than only recognizing the finished code.
