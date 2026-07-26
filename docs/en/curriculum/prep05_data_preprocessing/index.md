# Prep 5: Data Understanding and Preprocessing Basics

In this Prep, you will inspect data before passing it to a model and learn preprocessing from the question of why it is needed and which data it must use. Unit 01 uses a scikit-learn dataset and a regression model. If you run preprocessing without checking types, column meanings, and learning boundaries, you cannot explain what the displayed values mean or what the model has already learned from.

This Prep assumes you have finished [Prep 4: pandas Basics](../prep04_pandas/index.md). Return there first if you are unsure about NumPy arrays, pandas `DataFrame` and `Series` objects, or the roles of `X` and `y`.

If you can already explain dataset-loader results, missing values, duplicates, possible outliers, scaling, data leakage, `ColumnTransformer`, and `Pipeline`, you may use only the skip check and continue to Unit 01.

## Goals for this Prep

- Distinguish a scikit-learn loader's `Bunch`, NumPy arrays, and pandas tables.
- Check the relationship among `X`, `y`, rows, columns, features, and a target from shapes and names.
- Inspect missing values, duplicates, possible outliers, numeric columns, and categorical columns without confusing observation with a treatment decision.
- Explain standardization and the range scaling called normalization in this lesson.
- Explain why preprocessing must be `fit` on training data only after the split.
- Apply separate preprocessing to numeric and categorical columns, then combine it with `ColumnTransformer` and `Pipeline`.
- Explain why preprocessing does not guarantee a higher model score.

## Skip check

Read this code without running it.

```python
from sklearn.datasets import load_diabetes

dataset = load_diabetes()

print(type(dataset))
print(type(dataset.data), dataset.data.shape)
print(type(dataset.target), dataset.target.shape)
print(dataset.feature_names)
```

You may skip this Prep if you can answer all of the following.

1. What types are `dataset`, `dataset.data`, and `dataset.target`?
2. What do `(442, 10)` and `(442,)` say about the number of records and features?
3. What does `feature_names` name?
4. Why must preprocessing not be `fit` on test data?
5. What do `StandardScaler` and `MinMaxScaler` make comparable?
6. Why is finding a missing value or a large value not enough to decide that it should be deleted?
7. What does each of `ColumnTransformer` and `Pipeline` combine?

If you cannot explain even one item, start from the beginning. After you finish the practice and answer check, return here and answer in your own words.

## Before you start

Create one new Colab notebook and enter this Prep's code from top to bottom. Before executing a cell, write your prediction of the type, shape, displayed column names, and which operation learns from data in a text cell.

A standard Colab environment already includes NumPy, pandas, and scikit-learn, so this Prep does not install anything.

First import the libraries used to work with the data. Importing one item per line makes it clear where each name comes from.

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes
```

`np` and `pd` are the conventional short names for NumPy and pandas that you used in Prep 3 and Prep 4. `load_diabetes` is scikit-learn's loader for its diabetes dataset.

## 1. Inspect a dataset loader's return value

First load the dataset and inspect what it returns.

```python
dataset = load_diabetes()

print(type(dataset))
print(dataset.keys())
```

```text
<class 'sklearn.utils._bunch.Bunch'>
dict_keys([...])
```

`dataset` is a `Bunch`: a dictionary-like container that holds several named values. Its `keys()` let you inspect names such as `data`, `target`, and `feature_names`. The exact ordering and extra names can vary slightly with the scikit-learn version.

The important point is that `dataset` itself is neither a NumPy array nor a pandas table. Retrieve each value by name.

```python
print(type(dataset.data), dataset.data.shape)
print(type(dataset.target), dataset.target.shape)
print(dataset.feature_names)
```

```text
<class 'numpy.ndarray'> (442, 10)
<class 'numpy.ndarray'> (442,)
['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']
```

`dataset.data` is a `(442, 10)` `numpy.ndarray`: 442 people in rows and 10 measured features in columns. `dataset.target` is a one-dimensional `numpy.ndarray` with one value for those same 442 people. `feature_names` names the columns of `data`; it does not name the target.

A `Bunch` does not always mean that every returned value is an array. Other loaders can return pandas objects depending on their loading options. Do not assume the type: check `type()` and `shape`.

## 2. Inspect X and y

Arrays do not include column names. To make observation easier, turn `data` into a `DataFrame` and `target` into a named `Series`.

```python
diabetes_X = pd.DataFrame(
    dataset.data,
    columns=dataset.feature_names,
)
diabetes_y = pd.Series(
    dataset.target,
    name="progression",
)

print(diabetes_X.shape)
print(diabetes_X.head())
print(diabetes_y.shape)
print(diabetes_y.head())
```

`diabetes_X` gets its column names from `feature_names`. `progression` is the display name that this lesson gives the target series. Its values are a quantitative measure of diabetes progression one year later.

State the following relationship in words.

- `X` contains features used as clues for a prediction. Here it has shape `(442, 10)`: 10 features for 442 people.
- `y` is the target to predict. Here it has shape `(442,)`: one value for each person.
- The number of rows in `X` equals the number of items in `y`; the same position refers to the same person.
- A row of `X` is a sample and a column of `X` is a feature. A pandas table lets you inspect its rows, columns, and column names.

Do not interpret the displayed `age` or `bmi` values as raw years or raw BMI units just because of their column names. The features in this diabetes dataset are already centered and scale-adjusted. This dataset is therefore useful for observing a loader, types, shapes, and names, but not for freshly fitting a scaler in this lesson.

## 3. Decide whether preprocessing is needed from the data

Preprocessing is not a mechanical list of operations. First observe the meaning and condition of the data, then decide what needs attention. The following small raw dataset represents study records. `course_type` is categorical and `score` is the target to predict.

```python
raw_records = pd.DataFrame(
    {
        "study_minutes": [30, 45, 60, 90, 120, 150, 180, 240, 300, 360, 420, 999],
        "attempts": [1, 1, 2, 2, 3, np.nan, 3, 4, 4, 5, 5, 10],
        "course_type": [
            "self",
            "guided",
            "self",
            "guided",
            "self",
            "guided",
            "self",
            "guided",
            "self",
            "guided",
            "self",
            "guided",
        ],
        "score": [50, 55, 60, 67, 72, 78, 80, 86, 89, 92, 95, 99],
    }
)
raw_records = pd.concat([raw_records, raw_records.iloc[[3]]], ignore_index=True)

print(raw_records)
print(raw_records.dtypes)
```

The final `pd.concat` deliberately adds a second copy of the fourth row. This exercise dataset therefore has one duplicate row. A matching row in real data is not automatically a duplicate to delete: confirm whether it is a valid separate record or a collection error with the people responsible for the data.

Now inspect missing values, fully matching rows, and numeric ranges.

```python
print(raw_records.isna().sum())
print(raw_records.duplicated().sum())
print(raw_records[["study_minutes", "attempts"]].agg(["min", "max"]))
```

```text
study_minutes    0
attempts         1
course_type      0
score            0
dtype: int64
1
     study_minutes  attempts
min             30       1.0
max            999      10.0
```

The output tells us the following.

- `attempts` has one missing value. Finding it is different from deciding to fill it with a median or another value.
- One row is fully duplicated. In this lesson it was created on purpose, so we will later reduce it to one row.
- The value 999 in `study_minutes` is a possible outlier because it is much larger than the others. This table alone cannot tell us whether 999 minutes is impossible, so this lesson keeps it.
- `study_minutes` and `attempts` are numeric columns; `course_type` is a categorical column represented by strings. They cannot receive exactly the same preprocessing.

Finding possible outliers, missing values, and duplicates is observation. Deleting, filling, or rounding them is a treatment decision made after checking the purpose, collection method, and possible input errors. Preprocessing also does not automatically make a model more accurate.

## 4. Why adjust scales?

`study_minutes` ranges from tens to hundreds while `attempts` ranges roughly from 1 to 10. When numeric columns have very different units and ranges, models sensitive to distances or coefficient sizes can be overly influenced by the wide-range column. Scale adjustment does not make the columns mean the same thing; it puts their numeric ranges into a more comparable form.

This section uses a two-value array of 30 and 999 minutes to inspect the shape of each conversion. It is only a transformation example, not the data used to fit the later model preprocessing.

```python
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

scale_example = np.array([[30], [999]])

standardized_example = StandardScaler().fit_transform(scale_example)
range_scaled_example = MinMaxScaler().fit_transform(scale_example)

print(standardized_example.round(3))
print(range_scaled_example.round(3))
```

```text
[[-1.]
 [ 1.]]
[[0.]
 [1.]]
```

`StandardScaler` converts each column using the mean 0 and standard deviation 1 of the data it was `fit` on. In this example, the two values sit equally far from the mean, so they become approximately `-1` and `1`.

`MinMaxScaler` maps the minimum and maximum of the data it was `fit` on to 0 and 1. This Prep calls this range conversion “normalization.” The word “normalization” can mean other transformations in other contexts, so check the concrete operation, such as `MinMaxScaler`.

Which method to choose depends on the model and the data. Scale adjustment can be useful, but only a comparison on appropriate evaluation data can tell you its effect on a model score.

## 5. Fit preprocessing on training data only

Scalers and imputers learn values from data during `fit`: a mean, median, most frequent value, or list of categories. That learning is part of training. Split into training and test data before letting them learn.

Because the duplicate in this exercise was deliberately created, first keep one copy. Keep the possible outlier and the missing value at this point.

```python
from sklearn.model_selection import train_test_split

clean_records = raw_records.drop_duplicates()

X = clean_records.drop(columns="score")
y = clean_records["score"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
)

print(X_train.shape, X_test.shape)
print(y_train.shape, y_test.shape)
```

```text
(9, 3) (3, 3)
(9,) (3,)
```

`fit` learns the values needed for a conversion from training data. `transform` applies those learned values. Test data receives `transform` only.

The following is wrong because `X` still includes the test rows. It lets preprocessing learn a test-row median, maximum, or other information. That is data leakage.

```python
# Incorrect: X includes test rows.
# preprocessor.fit(X)
```

Do not run that code. The correct flow in the next section gives only `X_train` and `y_train` to the outer `Pipeline` when it calls `fit`.

## 6. Combine work with ColumnTransformer and Pipeline

Numeric and categorical columns need different work.

- For numeric columns, fill a missing `attempts` value with the training-data median, then standardize.
- For a categorical column, fill a missing value with the training-data most frequent value, then expand `guided` and `self` with one-hot encoding.

Put each flow in a small `Pipeline`, send each flow to the right columns with `ColumnTransformer`, then place preprocessing and a regression model in one outer `Pipeline`.

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

numeric_features = ["study_minutes", "attempts"]
categorical_features = ["course_type"]

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numeric_features),
        ("category", categorical_pipeline, categorical_features),
    ]
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", Ridge()),
    ]
)
```

`handle_unknown="ignore"` means that when a test or future record has a category not present during training, the matching one-hot columns are all 0 and the process continues. You still need to consider the business meaning of an unknown category, but this option avoids an immediate prediction error.

When you run `pipeline.fit(X_train, y_train)`, its imputer, scaler, one-hot encoder, and Ridge regression all `fit` only on training data. `pipeline.predict(X_test)` applies the already learned preprocessing to test data, then predicts.

```python
pipeline.fit(X_train, y_train)

transformed_train = pipeline.named_steps["preprocessor"].transform(X_train)
transformed_test = pipeline.named_steps["preprocessor"].transform(X_test)

print(pipeline.named_steps["preprocessor"].get_feature_names_out())
print(transformed_train.shape, transformed_test.shape)
print(np.round(transformed_train[:3], 3))
print(np.round(pipeline.predict(X_test), 1))
```

```text
['numeric__study_minutes' 'numeric__attempts'
 'category__course_type_guided' 'category__course_type_self']
(9, 4) (3, 4)
[[ 0.206  0.181  0.     1.   ]
 [-0.333 -0.226  1.     0.   ]
 [-0.656 -0.634  0.     1.   ]]
[83.9 81.  67.1]
```

After transformation, the two numeric columns and two columns created from the category make four columns. Use `get_feature_names_out()` to check where transformed columns came from. Depending on configuration and library version, a transformed result can be a NumPy array or an array-like sparse matrix. Inspect its shape and feature names first.

The final three values are predictions for the three test records. This lesson does not conclude whether those predictions are good. You can evaluate a score only after choosing a metric and comparison and confirming that preprocessing variants used the same test data.

## 7. Practice

Now build it yourself. Before opening the answers, write each step in a new cell and compare your prediction with the result. You may copy an earlier cell, but add a comment that explains what is `fit` and what is only `transform`.

### Step 1: Predict and inspect the loader contents

Load `load_diabetes()` and display the types and shapes of the return value, `data`, and `target`, plus `feature_names`. Write one sentence explaining why `dataset` and `dataset.data` do not have the same type.

### Step 2: Inspect the condition of raw data

For this Prep's `raw_records`, display each column's missing-value count, the number of fully matching rows, and the minimum and maximum of `study_minutes` and `attempts`. Also write why the table alone cannot decide whether to delete 999.

### Step 3: Separate X and y, then split

Remove only the deliberately created exact duplicate, make `X` from every column except `score`, and make `y` from `score`. Split with `test_size=0.25` and `random_state=42`, then display all four shapes. Do not fill the missing value yet.

### Step 4: Build column-specific preprocessing

For numeric `study_minutes` and `attempts`, use median imputation followed by standardization. For categorical `course_type`, use most-frequent imputation followed by one-hot encoding. Combine them with `ColumnTransformer`, then create an outer `Pipeline` containing it and `Ridge`.

### Step 5: Check the boundary between fitting, transforming, and predicting

Fit the outer `Pipeline` with only `X_train` and `y_train`. Display transformed feature names, transformed training and test shapes, and test predictions. Write one sentence explaining why you did not `fit` on `X_test`.

## 8. Answer check

<details>
<summary>Open only after completing the practice</summary>

### Step 1 answer

```python
dataset = load_diabetes()

print(type(dataset))
print(type(dataset.data), dataset.data.shape)
print(type(dataset.target), dataset.target.shape)
print(dataset.feature_names)
```

`dataset` is the named `Bunch` container; `dataset.data` and `dataset.target` are NumPy arrays that hold values. The container and the arrays inside it have different roles, so they have different types.

### Step 2 answer

```python
print(raw_records.isna().sum())
print(raw_records.duplicated().sum())
print(raw_records[["study_minutes", "attempts"]].agg(["min", "max"]))
```

`attempts` has one missing value and there is one fully matching row. The value 999 is a possible outlier, but the table cannot prove whether it is a valid intensive-study record or an input error.

### Step 3 answer

```python
clean_records = raw_records.drop_duplicates()

X = clean_records.drop(columns="score")
y = clean_records["score"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
)

print(X_train.shape, X_test.shape)
print(y_train.shape, y_test.shape)
```

The shapes are `(9, 3)`, `(3, 3)`, `(9,)`, and `(3,)`. Impute after splitting so the imputer can learn its median only from training data.

### Step 4 answer

```python
numeric_features = ["study_minutes", "attempts"]
categorical_features = ["course_type"]

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numeric_features),
        ("category", categorical_pipeline, categorical_features),
    ]
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", Ridge()),
    ]
)
```

The two column types need different operations, so use small pipelines and route them by column with `ColumnTransformer`.

### Step 5 answer

```python
pipeline.fit(X_train, y_train)

transformed_train = pipeline.named_steps["preprocessor"].transform(X_train)
transformed_test = pipeline.named_steps["preprocessor"].transform(X_test)

print(pipeline.named_steps["preprocessor"].get_feature_names_out())
print(transformed_train.shape, transformed_test.shape)
print(np.round(pipeline.predict(X_test), 1))
```

The transformed shapes are `(9, 4)` for training and `(3, 4)` for test data. Fitting on `X_test` would let preprocessing learn from test information, so the result would no longer be an evaluation on unseen data.

</details>

## Completion check

You have completed Prep 5 when you can confirm all of the following:

- You can explain what a `Bunch`, a NumPy array, and a pandas table each hold.
- You checked from shapes and displayed values that an `X` row and a `y` position refer to the same sample.
- You can distinguish finding missing values, duplicates, and possible outliers from deciding how to treat them.
- You can explain that standardization and range normalization adjust the numeric range of columns.
- You can explain why you split first and `fit` preprocessing on training data only.
- You applied different preprocessing to numeric and categorical columns and inspected the transformed feature names and shape.
- You can explain why `Pipeline` keeps preprocessing and model work in one consistent order.
- You can explain that score differences with and without preprocessing must be compared under the same evaluation conditions.

If you cannot explain an item, return to the related section and restate what the displayed type, shape, or feature name means. In Unit 01, you will use this understanding of `X`, `y`, splitting, and evaluation to implement linear regression.
