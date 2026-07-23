# Unit 1: Linear & Regularized Regression

<p class="unit-hero">
  <img src="/en/assets/units/unit01_linear_regression/images/hero.png" alt="Hero: predicting rent from room size with linear regression" />
</p>

## 1. Understanding Linear Regression and Regularization

### What Is Linear Regression? — Predicting Rent

In everyday terms, linear regression is like **using one straight ruler to predict the future from past data**.

Suppose you want to predict **rent (in 10,000 yen)** from **room size (square meters)**.
When you plot the data, you usually see that larger rooms tend to cost more. Linear regression draws **one line that best fits the middle of the data**.

<img src="/en/assets/units/unit01_linear_regression/images/diagram-linear-regression.svg" alt="Scatter plot with best-fit regression line: room size vs rent" class="unit-diagram" />

| Room size (feature) | Rent (target) |
| :------------------ | :------------ |
| 20㎡                | 60,000 yen    |
| 30㎡                | 80,000 yen    |
| 40㎡                | 100,000 yen   |

In formula form, this line looks like:
**Rent = (coefficient × room size) + base fee (intercept)**
The algorithm's job is to find the **coefficient** and **base fee** that best fit the historical data.

### What Is Regularization? — A Brake Against Overfitting

In reality, rent depends on many factors: distance from the station, building age, nearby convenience stores, and more.
When data gets complex, a model may try **too hard to fit the training data perfectly**. That is called **overfitting**.

Think of it like **a student who memorizes past exam questions but cannot solve new problems on test day**.

<img src="/en/assets/units/unit01_linear_regression/images/diagram-regularization.svg" alt="Overfitting wiggly curve vs regularized simpler line" class="unit-diagram" />

**Regularization** is the brake that prevents this. There are two main types:

1. **Ridge regression**: Shrinks coefficients overall to prevent extreme assumptions.
2. **Lasso regression**: Sets some coefficients to **exactly zero**, narrowing the features the model uses for prediction. A zero coefficient does not prove that the feature is irrelevant in the real world.

In the practice section, you will compare ordinary linear regression, Ridge regression, and Lasso regression on the same dataset.

### 💡 Real-World Business Use Cases

- **Real estate valuation AI**: Predict fair rent or sale price from features such as floor area, building age, and distance to the nearest station.
- **Retail sales forecasting**: Predict next-day store revenue from past sales, temperature, and holidays to optimize ordering.
- **Marketing mix modeling (ad ROI analysis)**: Estimate how much each channel (TV, web ads, etc.) contributes to revenue and optimize budget allocation.


## 2. Implementation Example

Here we use Python and the `scikit-learn` library to build linear regression and Ridge regression models that predict housing prices.

<img src="/en/assets/units/unit01_linear_regression/images/diagram-train-test-split.svg" alt="Workflow: split data, fit model, predict and evaluate with MSE" class="unit-diagram" />

First, import the libraries and prepare the data. To make Ridge's effect visible, we create 30 properties with 10 similar features derived from the same underlying "true size." Strong correlation among features is called **multicollinearity**, and it can make ordinary linear-regression coefficients unstable.

```python
# Import required libraries
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error

# 1. Prepare reproducible data
rng = np.random.default_rng(42)

# Create the true size of 30 properties between 20 and 80 square meters
true_size = rng.uniform(20, 80, size=(30, 1))

# X: 10 similar features made by adding small measurement errors to true size
# The columns contain much of the same information, so they are strongly correlated
X = true_size + rng.normal(0, 0.5, size=(30, 10))

# y: rent in units of 10,000 yen, plus real-world variation
y = true_size.ravel() * 0.2 + rng.normal(0, 3, size=30)
```

### Inspect the prepared dataset

Before passing the data to a model, verify that `X` and `y` have the intended meaning. Each row of `X` is one property, its 10 columns are similar features derived from that property's "true size," and one element of `y` is that property's rent.

```python
print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")

# Place the first three records side by side to inspect their meaning
for index in range(3):
    print(f"\nProperty {index + 1}")
    print(f"  True size: {true_size[index, 0]:.2f} square meters")
    print(f"  10 features: {np.round(X[index], 2)}")
    print(f"  Rent: {y[index]:.2f} (10,000 yen)")

# Check how similar the first and second columns are
correlation = np.corrcoef(X[:, 0], X[:, 1])[0, 1]
print(f"\nCorrelation between columns 1 and 2: {correlation:.3f}")
```

The output shows that `X` has 30 rows and 10 columns, while `y` has 30 values. For example, the first property's true size is about `66.44` square meters, and all 10 features are close values of roughly `66–68`. The correlation between the first and second columns is approximately `0.999`, confirming that they contain almost the same information.

After checking the data's meaning and shape, split it into training and test sets.

```python
# 2. Use 70% for training and 30% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
```

**Code walkthrough**
This mock dataset reproduces a situation where Ridge's "brake" can help. There are only 30 properties but, as the inspection showed, 10 similar features, and rent also contains noise. Ordinary linear regression can therefore fit accidental variation in the training data. We use `train_test_split` to compare both models on test data that was not used for training.

Next, train the model and make predictions.

```python
# 3. Prepare and train the model
# Create a standard linear regression model
model_lr = LinearRegression()

# Fit the best line using training data (X_train, y_train)
model_lr.fit(X_train, y_train)

# 4. Predict on the test set
y_pred_lr = model_lr.predict(X_test)

# 5. Evaluate accuracy
mse_lr = mean_squared_error(y_test, y_pred_lr)
print(f"Linear regression MSE: {mse_lr:.2f}")
```

**Code walkthrough**
Create a model with `LinearRegression()`, call `.fit()` to train it, and use `.predict()` to forecast rent for unseen test data. We then calculate and display its MSE. With the fixed conditions, the output is `Linear regression MSE: 20.34`. Confirm this result first, then use it as the baseline for the Ridge comparison.

Let's also build a regularized (Ridge) version.

```python
# 6. Prepare and train a regularized (Ridge) model
# alpha controls regularization strength — larger values apply a stronger penalty
model_ridge = Ridge(alpha=100.0)
model_ridge.fit(X_train, y_train)

# Predict on the test set
y_pred_ridge = model_ridge.predict(X_test)

# Evaluate accuracy
mse_ridge = mean_squared_error(y_test, y_pred_ridge)
improvement_rate = (mse_lr - mse_ridge) / mse_lr * 100

print(f"Linear regression MSE: {mse_lr:.2f}")
print(f"Ridge regression MSE: {mse_ridge:.2f}")
print(f"MSE reduction: {improvement_rate:.1f}%")
```

With these fixed conditions, ordinary linear regression produces an MSE of `20.34`, while Ridge produces `10.52`—a `48.3%` reduction. In this example, Ridge's "brake" prevents coefficients for the 10 similar features from becoming extreme, improving predictions on unseen test data.

### How should you read an MSE value?

MSE (mean squared error) is calculated by **squaring "prediction − actual value" for every sample and then taking the average**.

- MSE is always `0` or greater. An MSE of `0` means every prediction exactly matches its actual value.
- When the target, units, and test data are the same, the model with the smaller MSE has less prediction error. Here, `10.52 < 20.34`, so Ridge performs better.
- MSE has no fixed upper limit. Larger misses produce larger values, and squaring makes it especially sensitive to outliers.
- The target here is rent in units of 10,000 yen, but MSE uses squared units: `(10,000 yen)²`. Therefore, an MSE of `20.34` does not mean the prediction is off by 203,400 yen on average. Taking the square root gives RMSE in the original units: about `4.51` (45,100 yen) for ordinary linear regression and `3.24` (32,400 yen) for Ridge.
- You cannot directly compare MSE values calculated with different targets, units, or test splits just by looking at their numbers.

Ridge is not guaranteed to outperform ordinary linear regression on every dataset. Its effect depends on the data and the choice of `alpha`. This example intentionally recreates conditions where Ridge is useful: limited data, strongly correlated features, and noise.


## 3. Practice

Now it is your turn. Instead of copying the implementation example, work with a different real dataset and complete the process yourself—from understanding the data through comparing models and interpreting the results.

### Dataset

The scikit-learn Diabetes dataset contains 10 baseline features for 442 diabetes patients and a quantitative measure of disease progression one year later.

| Feature | Meaning                                 |
| :------ | :-------------------------------------- |
| `age`   | Age                                     |
| `sex`   | Sex                                     |
| `bmi`   | Body mass index                         |
| `bp`    | Average blood pressure                  |
| `s1`    | Total serum cholesterol                 |
| `s2`    | LDL (low-density lipoproteins)          |
| `s3`    | HDL (high-density lipoproteins)         |
| `s4`    | Total cholesterol divided by HDL        |
| `s5`    | Possibly the log of serum triglycerides |
| `s6`    | Blood sugar                             |

The feature values have already been mean-centered and scaled. Therefore, the displayed `age` and `bmi` values are not in their original units. The target is a quantitative measure of diabetes progression one year after baseline.

### Step 1: Observe the dataset

Before building a model, identify how many records exist and what the features and target represent. If you skip this step, later coefficients and MSE values have no interpretable context.

By default, `load_diabetes()` does not return an array directly. It returns a `Bunch` that groups the data and its description. A `Bunch` is similar to a dictionary and lets you retrieve an item with attribute access such as `diabetes.data`. In this dataset, `data` contains the features and `target` contains the target values as NumPy arrays. Inspect the actual types and contents before assuming what a loader returns.

1. Load the dataset with `load_diabetes()` and assign the result to `diabetes`.
2. Print the type of `diabetes` and the names of the items it contains. Also print the types of `diabetes.data` and `diabetes.target`.
3. Assign `diabetes.data` to `X` and `diabetes.target` to `y`.
4. Print `X.shape`, `diabetes.feature_names`, the first feature row, and the target's minimum, maximum, and mean.
5. Calculate the correlation between each feature and the target, then display the results in descending order of absolute correlation.
6. Use the output and feature table above to identify:
   - Which object is a `Bunch` and which objects are `ndarray` instances.
   - The number of patients and features.
   - The range of the target.
   - The features with relatively strong correlations with the target.

**Hints**

- Import `load_diabetes()` as follows:

  ```python
  from sklearn.datasets import load_diabetes
  ```

- Calculate a correlation with `np.corrcoef(X[:, column_index], y)[0, 1]`.
- Correlation describes how two variables tend to change together. A strong correlation does not prove that a feature causes disease progression.

### Step 2: Implement ordinary linear regression

Start with an unregularized linear-regression model to create a baseline for comparison.

1. Split the data into 80% training and 20% test with `test_size=0.2` and `random_state=42`.
2. Train `LinearRegression` on the training data and predict the test data.
3. Calculate and display MSE.
4. For the first five test samples, display the actual progression value, predicted value, and their difference.
5. Explain the difference between inspecting individual prediction errors and using MSE to summarize the full test set.

### Step 3: Implement Ridge and Lasso

Use the same training and test data to see how regularization changes the result. Do not split the data again, because MSE values from different test sets are not a fair model comparison.

1. Train Ridge with `alpha=0.1` and Lasso with `alpha=0.1`.
2. Predict the same test data and display the MSE values for all three models.
3. For each of the 10 feature names, display the coefficient learned by ordinary linear regression, Ridge, and Lasso.

**Hints**

- Learned coefficients are available through each model's `.coef_`.
- Use `zip(diabetes.feature_names, model_lr.coef_, model_ridge.coef_, model_lasso.coef_)` to align feature names with the three sets of coefficients.

### Step 4: Interpret the results

Use the output to explain the following in your own words:

1. Which model has the smallest MSE?
2. How do the Ridge coefficients differ from the ordinary linear-regression coefficients?
3. Which Lasso coefficients are zero?
4. What does a zero coefficient tell you about this training setup?
5. What medical conclusion cannot be made from a zero coefficient alone?


## 4. Answer Key

Write your own code first, then open the answer below to check your work.

<details>
<summary>View sample solution (click to expand)</summary>

### Step 1: Observe the dataset

```python
import numpy as np
from sklearn.datasets import load_diabetes

# Load the data
diabetes = load_diabetes()

# Inspect the return value and the types of the data it contains
print(f"Type returned by load_diabetes(): {type(diabetes).__name__}")
print(f"Stored items: {list(diabetes.keys())}")
print(f"Type of data: {type(diabetes.data).__name__}")
print(f"Type of target: {type(diabetes.target).__name__}")

# Extract the features and target
X = diabetes.data
y = diabetes.target

# Inspect size and contents
print(f"Data shape: {X.shape}")
print(f"Feature names: {diabetes.feature_names}")
print("First patient's features:")
for name, value in zip(diabetes.feature_names, X[0]):
    print(f"  {name}: {value:.4f}")

print(f"Target minimum: {y.min():.0f}")
print(f"Target maximum: {y.max():.0f}")
print(f"Target mean: {y.mean():.2f}")

# Inspect each feature's correlation with the target
correlations = []
for column_index, name in enumerate(diabetes.feature_names):
    correlation = np.corrcoef(X[:, column_index], y)[0, 1]
    correlations.append((name, correlation))

for name, correlation in sorted(correlations, key=lambda item: abs(item[1]), reverse=True):
    print(f"{name}: {correlation:.3f}")
```

The output identifies the value returned by `load_diabetes()` as a `Bunch` and its `data` and `target` items as `ndarray` instances. The data has 442 rows and 10 columns. The target ranges from `25` to `346` and has a mean of approximately `152.13`. In this dataset, `bmi`, `s5`, and `bp` have relatively strong correlations with the target. These are one-feature-at-a-time correlations across the full dataset; they do not directly establish causation or importance within a multifeature model.

### Step 2: Implement ordinary linear regression

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Split into training and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and predict with ordinary linear regression
model_lr = LinearRegression()
model_lr.fit(X_train, y_train)
pred_lr = model_lr.predict(X_test)

mse_lr = mean_squared_error(y_test, pred_lr)
print(f"Linear regression MSE: {mse_lr:.2f}")

# Inspect the first five actual and predicted values
print("Actual / Predicted / Prediction minus actual")
for actual, predicted in zip(y_test[:5], pred_lr[:5]):
    print(f"{actual:6.1f} / {predicted:6.1f} / {predicted - actual:7.1f}")
```

The ordinary linear-regression MSE is approximately `2900.19`. Even among the first five samples, one prediction is about 79 below its actual value and another is about 110 above. The individual differences describe specific patient predictions, while MSE summarizes squared errors across the entire test set.

### Step 3: Implement Ridge and Lasso

```python
from sklearn.linear_model import Ridge, Lasso

# Train regularized models on the same training data
model_ridge = Ridge(alpha=0.1)
model_lasso = Lasso(alpha=0.1)
model_ridge.fit(X_train, y_train)
model_lasso.fit(X_train, y_train)

# Predict the same test data
pred_ridge = model_ridge.predict(X_test)
pred_lasso = model_lasso.predict(X_test)

mse_ridge = mean_squared_error(y_test, pred_ridge)
mse_lasso = mean_squared_error(y_test, pred_lasso)

print(f"Linear regression MSE: {mse_lr:.2f}")
print(f"Ridge regression MSE: {mse_ridge:.2f}")
print(f"Lasso regression MSE: {mse_lasso:.2f}")

# Align feature names with coefficients from all three models
print("Feature / Linear regression / Ridge / Lasso")
for name, coef_lr, coef_ridge, coef_lasso in zip(
    diabetes.feature_names,
    model_lr.coef_,
    model_ridge.coef_,
    model_lasso.coef_,
):
    print(f"{name:>3} / {coef_lr:8.2f} / {coef_ridge:8.2f} / {coef_lasso:8.2f}")
```

**How to check your result**

Your implementation is correct even if its structure and variable names differ from the sample solution, as long as the specified conditions produce the following results:

- The MSE values are approximately `2900.19` for ordinary linear regression, `2856.49` for Ridge, and `2798.19` for Lasso.
- Under these conditions, Lasso has the smallest MSE of the three models.
- Lasso sets the coefficients for `age`, `s2`, and `s4` to zero.

The last few digits may vary slightly between library versions. If your result is substantially different, check that all three models used the same training and test data and that the split conditions and `alpha` values match the requirements.

### Step 4: Interpret the results

In this run, the regularized Ridge and Lasso models have lower test MSE than ordinary linear regression. Regularized models do not always perform better; the result depends on the data and the choice of `alpha`.

Ridge generally reduces coefficients that become large under ordinary linear regression, but it does not set them exactly to zero. Under these conditions, Lasso sets the `age`, `s2`, and `s4` coefficients to zero. This means that the model trained with this split and `alpha=0.1` did not use those three features for prediction.

The features are correlated with one another, and changing `alpha` changes the coefficients. A zero coefficient therefore does not prove that a feature is medically unnecessary, unrelated to diabetes progression, or unsuitable for clinical diagnosis.
</details>
