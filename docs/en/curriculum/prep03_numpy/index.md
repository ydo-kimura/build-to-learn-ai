# Prep 3: NumPy Foundations

This Prep teaches the NumPy foundations needed to work with multiple numeric values as arrays. In Unit 01 and later units, features and targets appear as NumPy arrays. Before building a model, you will learn to inspect an array’s dimensions, shape, rows, columns, selections, and aggregate results for yourself.

This Prep assumes that you have completed [Prep 2: Python Foundations](../prep02_python_basics/index.md). Review Prep 2 first if you are unsure about lists, indexes, slices, imports, attributes, or methods.

If you already use NumPy and can explain one- and two-dimensional shapes, the shape left by a slice, the results of `axis=0` and `axis=1`, a two-dimensional `X`, and a one-dimensional `y`, complete the skip check and continue to the next Prep.

## Learning goals

- Explain a relevant difference between a Python list and a NumPy array by comparing actual operation results
- Inspect an array with `dtype`, `ndim`, and `shape`
- Explain the differences among `(4,)`, `(4, 3)`, and `(4, 1)`
- Select a row, a column, a range, and one value with indexes and slices
- Distinguish aggregation over an entire array, each column, and each row
- Explain which values `axis=0` and `axis=1` aggregate and what remains in the result
- Decide whether a computable value is also useful in light of the data’s meaning
- Explain the shapes of a two-dimensional feature matrix `X` and a one-dimensional target vector `y`

## Skip check

Read the following code without running it.

```python
import numpy as np

values = np.array(
    [
        [10, 20, 30],
        [40, 50, 60],
    ]
)

print(values.shape)
print(values[:, 1])
print(values.mean(axis=0))
print(values.mean(axis=1))
```

You may skip this Prep if you can answer all of the following:

1. What is `values.ndim`?
2. What is `values.shape`?
3. Which rows and columns does `values[:, 1]` select?
4. What are the value and shape of `values[:, 1]`?
5. With `axis=0`, which axis is aggregated, and how many results remain?
6. With `axis=1`, which axis is aggregated, and how many results remain?
7. When one column of a two-dimensional `X` is selected as `y`, how do the dimensions of `X` and `y` differ?

If there is even one item you cannot explain, continue from the beginning. After completing the explanations and hands-on practice, return and verify your own answers.

## Before you begin

Create one new Colab notebook and enter the code in this Prep from top to bottom. Before running each block, record your predicted values and shapes in a text cell.

A standard Colab environment already provides NumPy, so you do not need to install anything for this Prep.

First, make NumPy available under the short name `np`.

```python
import numpy as np
```

`np` is a conventional name widely used in NumPy learning materials and documentation. It is not a separate library from NumPy.

## 1. Compare a Python list and a NumPy array

In Prep 2, you grouped multiple values in a list.

```python
numbers = [1, 2, 3]

print(type(numbers))
print(numbers * 2)
```

```text
<class 'list'>
[1, 2, 3, 1, 2, 3]
```

Using `* 2` on a list repeats its sequence twice. It does not double each number.

Create a NumPy array from the same values.

```python
array_numbers = np.array(numbers, dtype=np.int64)

print(type(array_numbers))
print(array_numbers * 2)
print(array_numbers.dtype)
```

```text
<class 'numpy.ndarray'>
[2 4 6]
int64
```

Using `* 2` on the NumPy array doubles every element. NumPy can apply the same numerical operation to many values at once.

`ndarray` stands for an N-dimensional array, the NumPy type used here. `dtype` is the data type of the elements stored in the array. Because this code specifies `dtype=np.int64`, the values are stored as 64-bit integers.

Neither a list nor an array is always the better choice. A list can be enough for a sequence such as a collection of names. A NumPy array becomes useful when you apply the same calculation to many numeric values or work with data organized into rows and columns.

## 2. Inspect dimensions and shapes

This Prep uses the following four learning records.

| Learner | Study hours | Attempts | Score |
| ------- | ----------: | -------: | ----: |
| Aoi     |           2 |        1 |    60 |
| Ren     |           4 |        2 |    72 |
| Mio     |           6 |        3 |    84 |
| Sora    |           8 |        4 |    96 |

Each row represents one learner. Each column represents one measured item: study hours, attempts, and score from left to right.

### A one-dimensional array

Create an array containing only the scores.

```python
scores = np.array([60, 72, 84, 96], dtype=np.int64)

print(scores)
print(scores.ndim)
print(scores.shape)
```

```text
[60 72 84 96]
1
(4,)
```

`ndim` is the number of dimensions. The values in `scores` extend in one direction, so it is one-dimensional and its `ndim` is `1`.

`shape` is a tuple that tells you how many elements exist along each dimension. `(4,)` means there are four elements in one dimension. The comma after `4` indicates that `(4,)` is a one-element tuple rather than an integer in parentheses.

### A two-dimensional array

Put the table’s numeric values into a four-row, three-column array.

```python
records = np.array(
    [
        [2, 1, 60],
        [4, 2, 72],
        [6, 3, 84],
        [8, 4, 96],
    ],
    dtype=np.int64,
)

print(records)
print(records.ndim)
print(records.shape)
```

```text
[[ 2  1 60]
 [ 4  2 72]
 [ 6  3 84]
 [ 8  4 96]]
2
(4, 3)
```

`records` extends in the two directions of rows and columns, so its `ndim` is `2`. Its shape `(4, 3)` means four rows and three columns.

- The four rows are the records for Aoi, Ren, Mio, and Sora.
- The three columns are study hours, attempts, and score.

When you inspect a shape, do not stop at reading “four and three.” Match each number to what it counts in the original data.

### Four rows and one column are still two-dimensional

Arrange the scores as four rows and one column.

```python
scores_column = np.array(
    [
        [60],
        [72],
        [84],
        [96],
    ],
    dtype=np.int64,
)

print(scores_column)
print(scores_column.ndim)
print(scores_column.shape)
```

```text
[[60]
 [72]
 [84]
 [96]]
2
(4, 1)
```

`(4, 1)` means four rows and one column. Even with only one column, the array has both a row direction and a column direction, so it is two-dimensional.

The same four scores can have shape `(4,)` as a one-dimensional array or `(4, 1)` as a two-dimensional array. The number of values alone does not determine the dimensions or shape. You must also inspect the structure in which the values are arranged.

## 3. Select rows, columns, ranges, and one value

NumPy indexes start at `0`, like Python list indexes. In a two-dimensional array, specify positions inside the brackets in `row, column` order.

### Select one row

```python
first_learner = records[0]

print(first_learner)
print(first_learner.ndim)
print(first_learner.shape)
```

```text
[ 2  1 60]
1
(3,)
```

`records[0]` selects row zero: Aoi’s study hours, attempts, and score. The original `records` array is two-dimensional, but selecting one row produces a one-dimensional array with three elements.

### Select one column

```python
study_hours = records[:, 0]

print(study_hours)
print(study_hours.ndim)
print(study_hours.shape)
```

```text
[2 4 6 8]
1
(4,)
```

A colon `:` represents the full range at that position. `records[:, 0]` means “select column zero from every row.” The result contains the study hours for all four learners.

### Select a range of rows

```python
first_two_learners = records[:2, :]

print(first_two_learners)
print(first_two_learners.ndim)
print(first_two_learners.shape)
```

```text
[[ 2  1 60]
 [ 4  2 72]]
2
(2, 3)
```

`records[:2, :]` selects everything from the start up to, but not including, row two and selects every column. The two rows for Aoi and Ren remain, so the result has shape `(2, 3)`.

### Select one value

```python
mio_score = records[2, 2]

print(mio_score)
print(np.ndim(mio_score))
print(np.shape(mio_score))
```

```text
84
0
()
```

`records[2, 2]` selects row two and column two, Mio’s score of `84`. Because the result is one value rather than a row or column, it is a NumPy scalar rather than an array.

A scalar is zero-dimensional, and `np.shape()` returns the empty tuple `()`. The shape has not “broken”; the result is a single value with no row or column extent.

## 4. Aggregate an array

NumPy methods can aggregate the numbers stored in an array.

```python
print(records.min())
print(records.max())
print(records.mean())
```

```text
1
96
28.5
```

- The minimum is the smallest attempt count, `1`.
- The maximum is the largest score, `96`.
- The mean is `28.5`, calculated from all 12 numeric values.

NumPy performed the calculation correctly. However, `28.5` mixes study hours, attempts, and scores, which have different units. Calling it an “average learning record of 28.5” would not explain what is equal to 28.5.

Being able to calculate a value does not guarantee that the value is useful in light of the data’s meaning. When aggregating, inspect which values were combined and what units or roles they have.

## 5. Aggregate with `axis`

For a two-dimensional array, `axis` chooses the axis to aggregate. Memorizing only “`axis=0` is columns, `axis=1` is rows” can become confusing when an array’s shape changes.

Check these two questions together:

1. Along which axis were values aggregated?
2. What kind of result remained after that axis was aggregated?

### `axis=0`: aggregate through the rows

```python
column_means = records.mean(axis=0)

print(column_means)
print(column_means.shape)
```

```text
[ 5.   2.5 78. ]
(3,)
```

The input `records` has shape `(4, 3)`. With `axis=0`, NumPy moves down through the four rows to aggregate the values. The row axis is aggregated, leaving one result for each of the three columns.

- Value zero, `5.0`: mean study hours, `(2 + 4 + 6 + 8) / 4`
- Value one, `2.5`: mean attempts, `(1 + 2 + 3 + 4) / 4`
- Value two, `78.0`: mean score, `(60 + 72 + 84 + 96) / 4`

The input shape is `(4, 3)`, and the output shape is `(3,)`. Aggregating the four learner rows leaves three item-level values. Each column combines values with the same meaning and unit, so each result can be explained.

### `axis=1`: aggregate through the columns

```python
row_means = records.mean(axis=1)

print(row_means)
print(row_means.shape)
```

```text
[21. 26. 31. 36.]
(4,)
```

With `axis=1`, NumPy moves across the three columns within each row. The column axis is aggregated, leaving one result for each of the four rows.

- Value zero, `21.0`: Aoi’s `(2 + 1 + 60) / 3`
- Value one, `26.0`: Ren’s `(4 + 2 + 72) / 3`
- Value two, `31.0`: Mio’s `(6 + 3 + 84) / 3`
- Value three, `36.0`: Sora’s `(8 + 4 + 96) / 3`

The input shape is `(4, 3)`, and the output shape is `(4,)`. Aggregating three columns leaves one result for each of four learners.

These four means mix study hours, attempts, and scores. They demonstrate how the NumPy axis behaves, but they are not meaningful learner-evaluation metrics. Do not treat the presence of output as success by itself. Make sure you can explain what values were combined.

## 6. Feature matrix `X` and target vector `y`

In machine learning, the columns used as clues for prediction are called features. The value you want to predict is called the target.

For this example, suppose you want to predict score from study hours and attempts.

- Feature matrix `X`: study hours and attempts
- Target vector `y`: score

```python
X = records[:, :2]
y = records[:, 2]

print(X)
print(X.ndim)
print(X.shape)

print(y)
print(y.ndim)
print(y.shape)
```

```text
[[2 1]
 [4 2]
 [6 3]
 [8 4]]
2
(4, 2)
[60 72 84 96]
1
(4,)
```

`X` is a two-dimensional array with two features for four learners, so it has four rows and two columns. `y` has one score for each learner, so it is a one-dimensional array with four elements.

In scikit-learn, features are commonly passed as two-dimensional data in which rows are samples and columns are features. The target is commonly passed as one-dimensional data with one value corresponding to each sample.

Also confirm that the row counts match.

```python
print(X.shape[0])
print(y.shape[0])
print(X.shape[0] == y.shape[0])
```

```text
4
4
True
```

Row zero of `X` and value zero of `y` both refer to Aoi. The same positional relationship applies to every learner. If the row counts differed, there would be no complete one-to-one correspondence between feature rows and target values.

This Prep stops at understanding shapes and correspondence. Unit 01 will train a model. Prep 4 will introduce labeled tabular data with column names and row labels.

## 7. Hands-on practice

From this point, build the code yourself instead of copying a finished implementation. Use the following table and instructions to complete the six steps in order.

| Learner | Study hours | Attempts | Score |
| ------- | ----------: | -------: | ----: |
| Aoi     |           2 |        1 |    60 |
| Ren     |           4 |        2 |    72 |
| Mio     |           6 |        3 |    84 |
| Sora    |           8 |        4 |    96 |

Use the following sequence in every step:

1. Predict the values, dimensions, and shapes before writing code.
2. Write and run the code yourself.
3. Compare your prediction with the output.
4. Explain in words what each output value represents.

### Step 1: Compare list and array operations

1. Assign `[2, 4, 6, 8]` to a list named `study_hours_list`.
2. Display the result of using `* 2` on the list.
3. Create a NumPy array named `study_hours_array` from the same values.
4. Display the result of using `* 2` on the NumPy array.
5. Explain why the two results differ.

### Step 2: Inspect dimensions and shapes

1. Create a one-dimensional `scores` array containing only the scores.
2. Create a two-dimensional `records` array containing every numeric value in the table.
3. Create a two-dimensional `scores_column` array containing the scores in four rows and one column.
4. Display `ndim` and `shape` for all three arrays.
5. Explain what `(4,)`, `(4, 3)`, and `(4, 1)` represent.

### Step 3: Select the required positions

Select the following from `records`. Display each value and its shape.

1. Ren’s complete row
2. The attempt counts for all learners
3. Study hours and attempts for the first three learners
4. Sora’s single score

Explain why only the final result is zero-dimensional.

### Step 4: Aggregate the entire array

Calculate the minimum, maximum, and mean over all of `records`.

Then explain:

1. Which table entries are the minimum and maximum
2. How many values were combined in the overall mean
3. Whether the overall mean can be interpreted as study hours, attempts, or score

### Step 5: Calculate means along each axis

1. Display the mean and shape for `axis=0`.
2. Explain what each of the three output values represents.
3. Display the mean and shape for `axis=1`.
4. Explain what each of the four output values represents.
5. State which result is easier to interpret using the original data’s meaning, and explain why.

Do not write only a shortcut such as “`axis=0` is the column mean.” Explain which axis was aggregated and what remained.

### Step 6: Create `X` and `y`

1. Select study hours and attempts as a two-dimensional `X`.
2. Select scores as a one-dimensional `y`.
3. Display the `type`, `ndim`, and `shape` of both.
4. Display the comparison that checks whether `X` and `y` have the same number of rows.
5. Explain how each row of `X` corresponds to each value of `y`.

## 8. Answer key

Open this section only after you have run every step and written what its output means. Your code may differ slightly. It is correct if it produces the same values and shapes and you can explain why.

<details>
<summary>Open the answer key</summary>

### Step 1

```python
study_hours_list = [2, 4, 6, 8]
print(study_hours_list * 2)

study_hours_array = np.array(study_hours_list, dtype=np.int64)
print(study_hours_array * 2)
```

```text
[2, 4, 6, 8, 2, 4, 6, 8]
[ 4  8 12 16]
```

The list operation repeats the sequence twice. The NumPy operation multiplies every element by two.

### Step 2

```python
scores = np.array([60, 72, 84, 96], dtype=np.int64)

records = np.array(
    [
        [2, 1, 60],
        [4, 2, 72],
        [6, 3, 84],
        [8, 4, 96],
    ],
    dtype=np.int64,
)

scores_column = np.array(
    [
        [60],
        [72],
        [84],
        [96],
    ],
    dtype=np.int64,
)

print(scores.ndim, scores.shape)
print(records.ndim, records.shape)
print(scores_column.ndim, scores_column.shape)
```

```text
1 (4,)
2 (4, 3)
2 (4, 1)
```

`scores` is a one-dimensional array with four elements. `records` is a four-row, three-column two-dimensional array. `scores_column` is a four-row, one-column two-dimensional array.

### Step 3

```python
ren_record = records[1]
attempts = records[:, 1]
first_three_features = records[:3, :2]
sora_score = records[3, 2]

print(ren_record, ren_record.shape)
print(attempts, attempts.shape)
print(first_three_features, first_three_features.shape)
print(sora_score, np.ndim(sora_score), np.shape(sora_score))
```

```text
[ 4  2 72] (3,)
[1 2 3 4] (4,)
[[2 1]
 [4 2]
 [6 3]] (3, 2)
96 0 ()
```

The first three results are arrays containing multiple values. `sora_score` selects one position as a scalar, so it is zero-dimensional and has shape `()`.

### Step 4

```python
print(records.min())
print(records.max())
print(records.mean())
```

```text
1
96
28.5
```

The minimum `1` is Aoi’s attempt count. The maximum `96` is Sora’s score. The mean `28.5` combines all 12 values in the four-row, three-column array. Because those columns use different units, the result cannot be interpreted as study hours, attempts, or score.

### Step 5

```python
column_means = records.mean(axis=0)
row_means = records.mean(axis=1)

print(column_means)
print(column_means.shape)
print(row_means)
print(row_means.shape)
```

```text
[ 5.   2.5 78. ]
(3,)
[21. 26. 31. 36.]
(4,)
```

`axis=0` aggregates the four rows and leaves one result for each of three columns: mean study hours `5.0`, mean attempts `2.5`, and mean score `78.0`.

`axis=1` aggregates the three columns and leaves one result for each of four rows. These are the within-row means for Aoi, Ren, Mio, and Sora. They are mathematically correct but difficult to interpret as learning metrics because each combines values with different units.

### Step 6

```python
X = records[:, :2]
y = records[:, 2]

print(type(X))
print(X)
print(X.ndim, X.shape)

print(type(y))
print(y)
print(y.ndim, y.shape)

print(X.shape[0] == y.shape[0])
```

```text
<class 'numpy.ndarray'>
[[2 1]
 [4 2]
 [6 3]
 [8 4]]
2 (4, 2)
<class 'numpy.ndarray'>
[60 72 84 96]
1 (4,)
True
```

`X` is a two-dimensional array with two features for four learners. `y` is a one-dimensional array with one score for each learner. The same position in both arrays refers to the same learner.

</details>

## Completion check

You have completed Prep 3 when you can confirm all of the following:

- You can explain why the same `* 2` operation behaves differently for a list and an `ndarray`.
- You can explain the roles of `dtype`, `ndim`, and `shape`.
- You can connect `(4,)`, `(4, 3)`, and `(4, 1)` to dimensions, rows, and columns.
- You selected a row, a column, a range, and one value from a two-dimensional array.
- You can explain whether a selection produces a scalar, a one-dimensional array, or a two-dimensional array.
- You can distinguish whole-array aggregation from aggregation along an axis.
- You can explain both the aggregated axis and the result that remains for `axis=0` and `axis=1`.
- You can explain why a displayed calculation is not necessarily useful given the original data’s meaning.
- You created a two-dimensional `X` and a one-dimensional `y` and explained the correspondence between their rows and values.
- You restarted the runtime, ran the notebook from the top, and reproduced the same values and shapes.

If you cannot explain an item, return to that section, select a different row or column, and run it again. When you can predict both the result’s value and its shape and meaning, you can inspect NumPy arrays for yourself.

Prep 4 will introduce pandas tables with column names and row labels and will compare them with NumPy arrays.
