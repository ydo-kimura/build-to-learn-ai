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
| :--- | :--- |
| 20㎡ | 60,000 yen |
| 30㎡ | 80,000 yen |
| 40㎡ | 100,000 yen |

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

---

## 2. Implementation Example

Here we use Python and the `scikit-learn` library to build linear regression and Ridge regression models that predict housing prices.

<img src="/en/assets/units/unit01_linear_regression/images/diagram-train-test-split.svg" alt="Workflow: split data, fit model, predict and evaluate with MSE" class="unit-diagram" />

First, import the libraries and prepare the data.

```python
# Import required libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error

# 1. Prepare data (we create dummy data this time)
# np.random.seed(42) fixes the random numbers so results are reproducible
np.random.seed(42)

# X: room size (100 samples between 20 and 80 square meters)
X = np.random.randint(20, 80, size=(100, 1))

# y: rent (size * 0.2 plus a small random error term)
y = X * 0.2 + np.random.randn(100, 1) * 2

# 2. Split data into training and test sets
# Use 80% for training (practice) and 20% for testing (final exam)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

**Code walkthrough**
We created mock data to predict rent from room size. To prevent cheating, we used `train_test_split` to separate training data from test data used for scoring later.

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
# MSE (mean squared error): how far predictions are from actual values
mse_lr = mean_squared_error(y_test, y_pred_lr)
print(f"Linear regression MSE: {mse_lr:.2f}")
```

**Code walkthrough**
Create a model with `LinearRegression()`, then call `.fit()` and the algorithm finds the best line. That is the training phase. After that, `.predict()` forecasts rent on unseen test data, and we measure error with MSE.

Let's also build a regularized (Ridge) version.

```python
# 6. Prepare and train a regularized (Ridge) model
# alpha controls regularization strength — larger values apply a stronger penalty
model_ridge = Ridge(alpha=1.0)
model_ridge.fit(X_train, y_train)

# Predict on the test set
y_pred_ridge = model_ridge.predict(X_test)

# Evaluate accuracy
mse_ridge = mean_squared_error(y_test, y_pred_ridge)
print(f"Ridge regression MSE: {mse_ridge:.2f}")
```

On this simple dataset the results are nearly identical, but with hundreds or thousands of features, Ridge's "brake" often improves accuracy.

---

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

---

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
