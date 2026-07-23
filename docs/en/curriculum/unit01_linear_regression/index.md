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
2. **Lasso regression**: Sets unimportant feature coefficients to **exactly zero**, effectively ignoring them. It is good at decluttering.

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

# 2. Use 70% for training and 30% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
```

**Code walkthrough**
This mock dataset reproduces a situation where Ridge's "brake" can help. There are only 30 properties but 10 similar features, and rent also contains noise. Ordinary linear regression can therefore fit accidental variation in the training data. We use `train_test_split` to compare both models on test data that was not used for training.

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
```

**Code walkthrough**
Create a model with `LinearRegression()`, call `.fit()` to train it, and use `.predict()` to forecast rent for unseen test data. We then calculate its MSE.

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

Now it's your turn! Build a model following the requirements below.

**Requirements**
Use the **Diabetes dataset** — predict one-year diabetes progression from numeric features such as age, BMI, and blood pressure.

1. Load data with `load_diabetes` from `sklearn.datasets`.
2. Split the data into 80% training and 20% test.
3. Create and train a **Lasso** model with `alpha=0.1`.
4. Predict on the test set and print MSE (mean squared error).

**Hints**

- Add `from sklearn.linear_model import Lasso`.
- Load with `from sklearn.datasets import load_diabetes`, then set `X = data.data` and `y = data.target` after `data = load_diabetes()`.


## 4. Answer Key

Write your own code first, then open the answer below to check your work.

<details>
<summary>View sample solution (click to expand)</summary>

```python
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error

# 1. Load the data
diabetes = load_diabetes()
X = diabetes.data
y = diabetes.target

# 2. Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Create and train a Lasso regression model
# alpha=0.1 sets the L1 regularization strength
model_lasso = Lasso(alpha=0.1)
model_lasso.fit(X_train, y_train)

# 4. Predict and evaluate
y_pred = model_lasso.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print(f"Lasso regression MSE: {mse:.2f}")

# Bonus: check how many feature coefficients Lasso set to exactly zero
print(f"Number of zero coefficients: {np.sum(model_lasso.coef_ == 0)}")
```

**Solution walkthrough**
The standout feature of Lasso is that it **sets coefficients of irrelevant features to exactly zero**. That makes it easier for humans to see which inputs truly matter — a big win for interpretability!
</details>
