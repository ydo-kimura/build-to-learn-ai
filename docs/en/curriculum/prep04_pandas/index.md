# Prep 4: pandas Foundations

This Prep teaches the pandas foundations for working with tabular data whose rows and columns have names. Unit 01 asks you to inspect a dataset’s column names, shape, and value ranges before building a model. First, learn to explain where each value is in a table and which rows and columns you selected.

This Prep assumes you completed [Prep 3: NumPy Foundations](../prep03_numpy/index.md). Review Prep 3 first if you are unsure about array `shape`, a two-dimensional feature matrix `X`, or a one-dimensional target vector `y`.

If you already use pandas and can inspect a table, select required rows and columns, and extract `X` and `y`, complete the skip check and continue to the next Prep.

## Learning goals

- Explain the difference between a `Series` and a `DataFrame`
- Explain what rows, columns, an index, and column names identify in a table
- Inspect data with `shape`, `columns`, `dtypes`, `head()`, `info()`, and `describe()`
- Select data by one column, multiple columns, position, label, and condition
- Locate missing values and count them for each column
- Extract pandas `X` and `y`, then convert them to NumPy arrays
- Explain what `to_numpy()` retains and what information it removes

## Skip check

Read the following code without running it.

```python
import pandas as pd

records = pd.DataFrame(
    {
        "study_hours": [2, 4, 6, 8],
        "attempts": [1, 2, 3, 4],
        "score": [60, 72, 84, 96],
    },
    index=pd.Index(["Aoi", "Ren", "Mio", "Sora"], name="learner"),
)

X = records[["study_hours", "attempts"]]
y = records["score"]
```

You may skip this Prep if you can answer all of the following:

1. What are the type and shape of `records`?
2. What is the difference between a row label, a column name, and a value?
3. Why is `X` a `DataFrame` while `y` is a `Series`?
4. What does each of `records.iloc[1:3, [0, 2]]` and `records.loc["Ren":"Mio", ["study_hours", "score"]]` use as its basis for selection?
5. What does `isna().sum()` check?
6. What information disappears from the result of `X.to_numpy()`?

If there is even one item you cannot explain, continue from the beginning. Return here after completing the Prep and answer in your own words.

## Before you begin

Create one new Colab notebook and enter this Prep’s code from top to bottom. Before running each block, write your prediction of the type, shape, rows, and columns in a text cell.

A standard Colab environment already provides pandas, so you do not need to install anything for this Prep.

First, make pandas available under the short name `pd`.

```python
import pandas as pd
```

`pd` is a conventional name widely used in pandas learning materials and documentation. It is not a separate library from pandas.

## 1. Create a named column and a named table

Prep 3 used the learning records for four people as a NumPy array. pandas lets you give the same values column names and row labels.

| Learner | Study hours | Attempts | Score |
| ------- | ----------: | -------: | ----: |
| Aoi     |           2 |        1 |    60 |
| Ren     |           4 |        2 |    72 |
| Mio     |           6 |        3 |    84 |
| Sora    |           8 |        4 |    96 |

Create the table as follows.

```python
records = pd.DataFrame(
    {
        "study_hours": [2, 4, 6, 8],
        "attempts": [1, 2, 3, 4],
        "score": [60, 72, 84, 96],
    },
    index=pd.Index(["Aoi", "Ren", "Mio", "Sora"], name="learner"),
)

print(records)
```

```text
         study_hours  attempts  score
learner
Aoi                2         1     60
Ren                4         2     72
Mio                6         3     84
Sora               8         4     96
```

The entire `records` object is a `DataFrame`: a two-dimensional table in which every row is one observation and every column is one variable.

- `Aoi`, `Ren`, `Mio`, and `Sora` are **index labels** that identify rows.
- `study_hours`, `attempts`, and `score` are **column names**.
- Values such as `2` and `60` are the recorded **data values**.

An index is a name used to find a row. In this example, the index itself is not automatically a feature for prediction.

Selecting one column usually produces a `Series`.

```python
study_hours = records["study_hours"]

print(type(study_hours))
print(study_hours)
```

```text
<class 'pandas.Series'>
learner
Aoi     2
Ren     4
Mio     6
Sora    8
Name: study_hours, dtype: int64
```

A `Series` is a one-dimensional sequence of values with an index and a name. Here the values are study hours, the index is the learner name, and `Name` is the column name.

Selecting multiple columns keeps a `DataFrame`.

```python
features = records[["study_hours", "attempts"]]

print(type(features))
print(features)
```

```text
<class 'pandas.DataFrame'>
         study_hours  attempts
learner
Aoi                2         1
Ren                4         2
Mio                6         3
Sora                8         4
```

`records["study_hours"]` has one pair of brackets, so it selects one column as a `Series`. `records[["study_hours", "attempts"]]` specifies a list of column names, so it selects a two-column `DataFrame`.

## 2. Inspect a table before changing it

Before creating model inputs `X` and `y`, inspect how many rows and columns the table has and which names and value types its columns use.

```python
print(type(records))
print(records.shape)
print(records.columns)
print(records.dtypes)
print(records.head())
```

```text
<class 'pandas.DataFrame'>
(4, 3)
Index(['study_hours', 'attempts', 'score'], dtype='str')
study_hours    int64
attempts       int64
score          int64
dtype: object
         study_hours  attempts  score
learner
Aoi                2         1     60
Ren                4         2     72
Mio                6         3     84
Sora                8         4     96
```

- `type(records)` confirms that the object is a `DataFrame`.
- `(4, 3)` from `shape` means four rows and three columns.
- `columns` lists names, not data values.
- `dtypes` identifies the type of values stored in each column. `int64` is an integer column.
- `head()` displays the first rows so you can see what the table contains.

`head()` displays every row here because the table has only four. For a larger table it displays the first five rows by default.

## 3. Read `info()` and `describe()`

`info()` gives a compact structural summary.

```python
records.info()
```

```text
<class 'pandas.DataFrame'>
Index: 4 entries, Aoi to Sora
Data columns (total 3 columns):
 #   Column       Non-Null Count  Dtype
---  ------       --------------  -----
 0   study_hours  4 non-null      int64
 1   attempts     4 non-null      int64
 2   score        4 non-null      int64
dtypes: int64(3)
memory usage: ...
```

This tells you the table has four rows and three columns, each column has four non-missing values, and every column is integer-valued. The precise `memory usage` number varies with the pandas version and environment, so it is not a value to memorize.

Use `describe()` for a summary of numeric columns.

```python
print(records.describe())
```

```text
       study_hours  attempts      score
count     4.000000  4.000000   4.000000
mean      5.000000  2.500000  78.000000
min       2.000000  1.000000  60.000000
max       8.000000  4.000000  96.000000
```

The actual output also contains `std`, `25%`, `50%`, and `75%`. At this point, make sure you can read these values for every column:

- `count`: number of non-missing values
- `mean`: average
- `min`: minimum
- `max`: maximum

For example, `score` has mean `78.0`, minimum `60.0`, and maximum `96.0`. These are computed separately for each column, so the score mean is meaningful in a way that the mixed-unit whole-array mean in Prep 3 was not.

## 4. Select rows and columns deliberately

Several operations can select part of a table. The syntax and meaning depend on whether the selection is based on a name, position, label, or condition.

### Select by column name

Use a column-name string to select one column.

```python
scores = records["score"]

print(type(scores), scores.shape)
print(scores)
```

```text
<class 'pandas.Series'> (4,)
learner
Aoi     60
Ren     72
Mio     84
Sora    96
Name: score, dtype: int64
```

Use a list of column names to select multiple columns.

```python
two_columns = records[["study_hours", "score"]]

print(type(two_columns), two_columns.shape)
print(two_columns)
```

```text
<class 'pandas.DataFrame'> (4, 2)
         study_hours  score
learner
Aoi                2     60
Ren                4     72
Mio                6     84
Sora                8     96
```

Both examples select by column name, not by numeric position.

### Select by position with `iloc`

`iloc` selects rows and columns by their zero-based **position**. This selects row positions 1 and 2 (Ren and Mio) and column positions 0 and 2 (study hours and score).

```python
by_position = records.iloc[1:3, [0, 2]]

print(type(by_position), by_position.shape)
print(by_position)
```

```text
<class 'pandas.DataFrame'> (2, 2)
         study_hours  score
learner
Ren                4     72
Mio                6     84
```

Like a NumPy slice, `1:3` starts at 1 and stops before 3, so it includes positions 1 and 2.

### Select by label with `loc`

`loc` selects by actual **labels** in the index or columns.

```python
by_label = records.loc["Ren":"Mio", ["attempts", "score"]]

print(type(by_label), by_label.shape)
print(by_label)
```

```text
<class 'pandas.DataFrame'> (2, 2)
         attempts  score
learner
Ren             2     72
Mio             3     84
```

`"Ren":"Mio"` is a label range. With this `loc` label range, the ending label `"Mio"` is included. That differs from the stop position in an `iloc` slice, so always identify the basis of a selection.

### Select by a condition

You can select rows that meet a condition, such as scores of 80 or higher.

```python
high_scores = records.loc[records["score"] >= 80, ["study_hours", "score"]]

print(type(high_scores), high_scores.shape)
print(high_scores)
```

```text
<class 'pandas.DataFrame'> (2, 2)
         study_hours  score
learner
Mio                6     84
Sora                8     96
```

`records["score"] >= 80` produces `True` or `False` for every row. `loc` keeps only the `True` rows. This operation retrieves records matching a stated condition; it does not establish a causal relationship.

## 5. Find and count missing values

Real data can contain values that were not recorded. First observe where missing values are and how many occur in each column.

Make a copy so the original `records` remains unchanged, then add one missing value.

```python
records_with_missing = records.copy()
records_with_missing.loc["Mio", "attempts"] = None

print(records_with_missing)
```

```text
         study_hours  attempts  score
learner
Aoi                2       1.0     60
Ren                4       2.0     72
Mio                6       NaN     84
Sora                8       4.0     96
```

`NaN` is a common displayed representation of a missing numeric value. Do not fill the value or delete the row here.

Use `isna()` to locate the missing value.

```python
print(records_with_missing.isna())
```

```text
         study_hours  attempts  score
learner
Aoi            False     False  False
Ren            False     False  False
Mio            False      True  False
Sora           False     False  False
```

`True` means that position is missing. Add `sum()` to count missing values by column.

```python
print(records_with_missing.isna().sum())
```

```text
study_hours    0
attempts       1
score          0
dtype: int64
```

Only `attempts` has one missing value. How to handle a missing value depends on its meaning, why it is missing, and the analysis goal. Prep 5 covers decisions such as filling or removing values. This Prep stops at finding and counting them.

## 6. Convert pandas `X` and `y` to NumPy arrays

Again, suppose you want to predict score from study hours and attempts.

```python
X = records[["study_hours", "attempts"]]
y = records["score"]

print(type(X), X.shape)
print(X.columns)
print(X.index)

print(type(y), y.shape)
print(y.name)
print(y.index)
```

```text
<class 'pandas.DataFrame'> (4, 2)
Index(['study_hours', 'attempts'], dtype='str')
Index(['Aoi', 'Ren', 'Mio', 'Sora'], dtype='str', name='learner')
<class 'pandas.Series'> (4,)
score
Index(['Aoi', 'Ren', 'Mio', 'Sora'], dtype='str', name='learner')
```

`X` is a `DataFrame` with two selected columns, and `y` is a `Series` with one selected column. Both use the same learner index, so Aoi’s features correspond to Aoi’s score.

scikit-learn can often receive a pandas table directly. To inspect the values as a NumPy array, use `to_numpy()`.

```python
X_array = X.to_numpy()
y_array = y.to_numpy()

print(type(X_array), X_array.shape)
print(X_array)
print(type(y_array), y_array.shape)
print(y_array)
```

```text
<class 'numpy.ndarray'> (4, 2)
[[2 1]
 [4 2]
 [6 3]
 [8 4]]
<class 'numpy.ndarray'> (4,)
[60 72 84 96]
```

The values and their order remain. However, `X_array` has neither the column names `study_hours` and `attempts` nor row labels such as Aoi. `y_array` also loses its name `score` and its row labels.

`to_numpy()` converts chosen values to an array. It does not decide which columns are features or which column is the target. You choose `X` and `y` before converting them.

## 7. Hands-on practice

From this point, build the code yourself instead of copying a finished implementation. In every step:

1. Predict the type, shape, and selected rows or columns before execution.
2. Write and run the code yourself.
3. Compare the output with your prediction.
4. Explain what the output represents in words.

### Step 1: Create and inspect the table

1. Create a `DataFrame` for study hours, attempts, and scores with Aoi, Ren, Mio, and Sora as its index.
2. Display its `type`, `shape`, `columns`, `dtypes`, and `head()`.
3. Explain its four-row, three-column shape and the name and type of each column.

### Step 2: Read `info()` and `describe()`

1. Run `info()` on the table.
2. Identify the non-null count and type of every column.
3. Display `describe()` and explain the score count, mean, minimum, and maximum.
4. Explain why you should not use the `memory usage` number as an answer.

### Step 3: Select by column, position, label, and condition

1. Select scores as a one-column `Series`.
2. Select study hours and attempts as a two-column `DataFrame`.
3. Use `iloc` to select study hours and scores for Ren and Mio.
4. Use `loc` to select attempts and scores from Ren through Mio.
5. Select study hours and scores for people whose score is 80 or higher.
6. Explain whether each operation uses a name, position, label, or condition.

### Step 4: Observe a missing value

1. Use `copy()` to duplicate the original table.
2. Set Mio’s attempts in the copy to `None`.
3. Display the missing-value locations with `isna()`.
4. Display the count in each column with `isna().sum()`.
5. Without filling or deleting anything, state which column has how many missing values.

### Step 5: Extract pandas `X` and `y`

1. Select study hours and attempts as `X`.
2. Select score as `y`.
3. Display their types, shapes, column names or name, and indexes.
4. Explain why `X` is a `DataFrame` and `y` is a `Series`.

### Step 6: Convert to NumPy arrays

1. Run `X.to_numpy()` and `y.to_numpy()`.
2. Display their types, shapes, and values.
3. Explain which column names, `y` name, and row labels do not remain in the arrays.
4. Explain why `to_numpy()` does not automatically choose features and a target.

## 8. Answer key

Open this section only after running every step and writing what the output means. Your variable names and display order may differ. Your work is correct if you obtain and explain the same values, types, and shapes.

<details>
<summary>Open the answer key</summary>

### Step 1

```python
records = pd.DataFrame(
    {
        "study_hours": [2, 4, 6, 8],
        "attempts": [1, 2, 3, 4],
        "score": [60, 72, 84, 96],
    },
    index=pd.Index(["Aoi", "Ren", "Mio", "Sora"], name="learner"),
)

print(type(records))
print(records.shape)
print(records.columns)
print(records.dtypes)
print(records.head())
```

`records` is a `DataFrame` with shape `(4, 3)`. The rows are four learner records; `study_hours`, `attempts`, and `score` are columns. All three columns contain integer values.

### Step 2

```python
records.info()
print(records.describe())
```

`info()` shows four non-null values and `int64` type for all three columns. In `describe()`, score has count `4`, mean `78.0`, minimum `60.0`, and maximum `96.0`. `memory usage` varies by environment, so it is not a comparison target.

### Step 3

```python
scores = records["score"]
features = records[["study_hours", "attempts"]]
by_position = records.iloc[1:3, [0, 2]]
by_label = records.loc["Ren":"Mio", ["attempts", "score"]]
high_scores = records.loc[records["score"] >= 80, ["study_hours", "score"]]

print(type(scores), scores.shape)
print(type(features), features.shape)
print(by_position)
print(by_label)
print(high_scores)
```

`scores` is a `(4,)` `Series`; `features` is a `(4, 2)` `DataFrame`. `iloc` uses zero-based positions, `loc` uses labels `Ren` and `Mio`, and the final `loc` uses the score-at-least-80 condition.

### Step 4

```python
records_with_missing = records.copy()
records_with_missing.loc["Mio", "attempts"] = None

print(records_with_missing.isna())
print(records_with_missing.isna().sum())
```

Only Mio’s `attempts` position is `True`. The per-column counts are `0` for `study_hours`, `1` for `attempts`, and `0` for `score`. This observes the missing value only; it does not fill or delete it.

### Step 5

```python
X = records[["study_hours", "attempts"]]
y = records["score"]

print(type(X), X.shape, list(X.columns), list(X.index))
print(type(y), y.shape, y.name, list(y.index))
```

`X` is a `(4, 2)` `DataFrame` made from two columns; `y` is a `(4,)` `Series` made from one column. Both have the same Aoi, Ren, Mio, Sora index order.

### Step 6

```python
X_array = X.to_numpy()
y_array = y.to_numpy()

print(type(X_array), X_array.shape)
print(X_array)
print(type(y_array), y_array.shape)
print(y_array)
```

`X_array` is a `(4, 2)` `numpy.ndarray` and `y_array` is a `(4,)` `numpy.ndarray`. Values and order remain, but column names, the name of `y`, and indexes such as Aoi do not. You selected the `X` and `y` columns before conversion.

</details>

## Completion check

You have completed Prep 4 when you can confirm all of the following:

- You can explain that a `Series` is one named, indexed column of values and a `DataFrame` is a named table.
- You used `shape`, `columns`, `dtypes`, `head()`, `info()`, and `describe()` for their distinct purposes.
- You can explain how one-column and multiple-column selection change the result type and shape.
- You can distinguish `iloc` positions, `loc` labels, and conditional selection.
- You located missing values and counted them for each column.
- You can explain that finding missing values and repairing them are different tasks.
- You extracted pandas `X` and `y` and explained how their common index shows correspondence.
- You can explain that `to_numpy()` keeps values and order but removes labels.
- You restarted the notebook, ran it from the top, and reproduced the same results.

If you cannot explain an item, return to that section, change one selected column or condition, and run it again. Prep 5 will cover why and how to preprocess data, including choices about filling or deleting missing values, scale adjustment, and categorical values.
