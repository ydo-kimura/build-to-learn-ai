# Unit 8: Cross-Validation and Hyperparameter Tuning

<p class="unit-hero">
  <img src="/en/assets/units/unit08_cross_validation_tuning/images/hero.png" alt="Hero: cross-validation and hyperparameter tuning" />
</p>

## 1. Understanding Cross-Validation and Hyperparameter Tuning

<img src="/en/assets/units/unit08_cross_validation_tuning/images/diagram-concept.svg" alt="Diagram: 5-Fold cross validation" class="unit-diagram" />

So far we've split data with `train_test_split` and set knobs like `n_neighbors=3`. Practitioners don't trust **one lucky split** or **gut-feel settings**. This unit covers **more reliable evaluation** and **finding settings that maximize performance**.

### What Is Cross-Validation? — Take Multiple Practice Exams

`train_test_split` cuts data once into train (80%) and test (20%).
Problem: **easy test questions might inflate your score by luck**.

**K-fold cross-validation** fixes that — like **taking five mock exams with rotating question sets and averaging the scores**.

1. Split data into, say, 5 blocks (K=5).
2. Use block 1 as test, blocks 2–5 as train — score it.
3. Use block 2 as test, others as train — score again.
4. Repeat for all 5 blocks. **Average the five scores** as the model's true skill estimate.

### What Is Hyperparameter Tuning? — Find the Ultimate Settings

Models have human-chosen **hyperparameters**:

- **K-NN**: How many neighbors? (`n_neighbors`)
- **Random forest**: How many trees? (`n_estimators`) How deep? (`max_depth`)

Don't guess — use **grid search** to **try combinations and pick the best score**.

| Method            | Analogy                                                                                           |
| :---------------- | :------------------------------------------------------------------------------------------------ |
| **Grid search**   | Try **all 100 combinations** of brightness (0–10) and contrast (0–10) on a TV. Thorough but slow. |
| **Random search** | Sample **dozens of random combinations**. Faster, often good enough.                              |

### 💡 Real-World Business Use Cases

- **Medical AI safety**: Prove stable accuracy across hospitals with cross-validation — not overfit to one site.
- **Trading strategy optimization**: Grid-search parameters to maximize backtest return while controlling risk.
- **ML pipeline efficiency**: Automate tuning so data scientists spend time on features, not manual knob turning.

---

<img src="/en/assets/units/unit08_cross_validation_tuning/images/diagram-workflow.svg" alt="Diagram: Hyperparameter grid" class="unit-diagram" />

## 2. Implementation Example

Using **breast cancer data** and **random forest**, we'll run **`GridSearchCV`** — grid search **with 5-fold cross-validation** — a standard production pattern.

```python
# Import required libraries
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# 1. Prepare the data
cancer = load_breast_cancer()
X = cancer.data
y = cancer.target

# Hold out 20% as a final test set that grid search never sees
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

**Code walkthrough**
Hold out 20% as a **final exam** (`X_test`) that grid search never sees — used only after tuning finishes.

```python
# 2. Define hyperparameter candidates as a dictionary
param_grid = {
    'n_estimators': [10, 50, 100],  # number of trees: 3 options
    'max_depth': [None, 5, 10]      # tree depth limit: 3 options
}
# -> 3 x 3 = 9 combinations to try

# 3. Configure grid search
rf_model = RandomForestClassifier(random_state=42)

# cv=5 means run 5-fold cross-validation
grid_search = GridSearchCV(
    estimator=rf_model,
    param_grid=param_grid,
    cv=5,
    scoring='accuracy'
)

# 4. Try all combinations (repeated train and validate)
grid_search.fit(X_train, y_train)
```

**Code walkthrough**
List candidate settings in `param_grid`.
`GridSearchCV` runs **5-fold CV for each of 9 combos** — **45 model fits** under the hood!

```python
# 5. Inspect the best settings and cross-validation score
print("Best parameters:", grid_search.best_params_)
print(f"Mean cross-validation score: {grid_search.best_score_:.3f}")

# 6. Evaluate the best model on the held-out final test set
best_model = grid_search.best_estimator_
final_score = best_model.score(X_test, y_test)
print(f"Final test accuracy: {final_score:.3f}")
```

**Code walkthrough**
After `.fit()`, `best_params_` holds the winning settings and `best_estimator_` is the retrained best model. Score it once on `X_test` — complete tuning pipeline.


## 3. Practice

Try grid search yourself.

**Requirements**
Use the **Wine dataset** and **K-NN** to find the best number of neighbors.

1. Load with `load_wine` and split with `train_test_split`.
2. Prepare `KNeighborsClassifier()`.
3. Set `param_grid` with `'n_neighbors': [1, 3, 5, 7, 9]`.
4. Run `GridSearchCV` with `cv=5` and print `best_params_`.

**Hints**

- Import `from sklearn.neighbors import KNeighborsClassifier`.
- `param_grid` looks like `{'n_neighbors': [1, 3, 5, 7, 9]}`.


## 4. Answer Key

Write your own code first, then open the answer below to check your work.

<details>
<summary>View sample solution (click to expand)</summary>

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

# 1. Load and split the data
wine = load_wine()
X = wine.data
y = wine.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Prepare model and parameter grid
knn = KNeighborsClassifier()
param_grid = {
    'n_neighbors': [1, 3, 5, 7, 9]
}

# 3. Configure and run grid search
# cv=5 runs 5-fold cross-validation
grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# 4. Inspect results
print("Best number of neighbors (K):", grid_search.best_params_)
print(f"Mean cross-validation score: {grid_search.best_score_:.3f}")

# Bonus: final test evaluation
best_knn = grid_search.best_estimator_
print(f"Test accuracy: {best_knn.score(X_test, y_test):.3f}")
```

**Solution walkthrough**
You've graduated from gut-feel settings! In practice, run `GridSearchCV` on several algorithms, compare fully tuned models, and pick what ships to production.
</details>
