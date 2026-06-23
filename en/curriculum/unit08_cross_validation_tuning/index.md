# Unit 8: Cross-Validation and Hyperparameter Tuning

## 1. Understanding Cross-Validation and Hyperparameter Tuning

<img src="../../../assets/units/unit08_cross_validation_tuning/images/concept.png" width="400" alt="Concept diagram">

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

| Method | Analogy |
| :--- | :--- |
| **Grid search** | Try **all 100 combinations** of brightness (0–10) and contrast (0–10) on a TV. Thorough but slow. |
| **Random search** | Sample **dozens of random combinations**. Faster, often good enough. |

### 💡 Real-World Business Use Cases

- **Medical AI safety**: Prove stable accuracy across hospitals with cross-validation — not overfit to one site.
- **Trading strategy optimization**: Grid-search parameters to maximize backtest return while controlling risk.
- **ML pipeline efficiency**: Automate tuning so data scientists spend time on features, not manual knob turning.

---

## 2. Implementation Example

Using **breast cancer data** and **random forest**, we'll run **`GridSearchCV`** — grid search **with 5-fold cross-validation** — a standard production pattern.

```python
# 必要なツールのインポート
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# 1. データの準備
cancer = load_breast_cancer()
X = cancer.data
y = cancer.target

# 全データの20%は、グリッドサーチが一切見ない「最終テスト用」として隠しておきます
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

**Code walkthrough**
Hold out 20% as a **final exam** (`X_test`) that grid search never sees — used only after tuning finishes.

```python
# 2. 試したい設定値（ハイパーパラメータ）のリストを辞書型で作る
param_grid = {
    'n_estimators': [10, 50, 100],  # 木の数：3パターン
    'max_depth': [None, 5, 10]      # 木の深さ制限：3パターン
}
# -> 合計 3 × 3 = 9通りの組み合わせを試すことになります

# 3. グリッドサーチの設定
rf_model = RandomForestClassifier(random_state=42)

# cv=5 は「交差検証を5回（5分割）でやってね」という指示です
grid_search = GridSearchCV(
    estimator=rf_model, 
    param_grid=param_grid, 
    cv=5, 
    scoring='accuracy'
)

# 4. 全通りの組み合わせを試す（学習とテストの繰り返し）実行！
grid_search.fit(X_train, y_train)
```

**Code walkthrough**
List candidate settings in `param_grid`.
`GridSearchCV` runs **5-fold CV for each of 9 combos** — **45 model fits** under the hood!

```python
# 5. 最強の設定と、その時のスコアを確認する
print("最も良かった設定（ベストパラメータ）:", grid_search.best_params_)
print(f"その設定の時の交差検証スコア（平均）: {grid_search.best_score_:.3f}")

# 6. 「最強の設定になったモデル」を使って、最後に隠しておいた「本番のテストデータ」に挑戦！
best_model = grid_search.best_estimator_
final_score = best_model.score(X_test, y_test)
print(f"最終テストデータでの正解率: {final_score:.3f}")
```

**Code walkthrough**
After `.fit()`, `best_params_` holds the winning settings and `best_estimator_` is the retrained best model. Score it once on `X_test` — complete tuning pipeline.

---

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

---

## 4. Answer Key

Write your own code first, then open the answer below to check your work.

<details>
<summary>View sample solution (click to expand)</summary>

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

# 1. データの読み込みと分割
wine = load_wine()
X = wine.data
y = wine.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. モデルと試したいパラメータの準備
knn = KNeighborsClassifier()
param_grid = {
    'n_neighbors': [1, 3, 5, 7, 9]
}

# 3. グリッドサーチの設定と実行
# cv=5 で5回の交差検証を行います
grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# 4. 結果の確認
print("最も良かったKの数:", grid_search.best_params_)
print(f"その時の交差検証スコア: {grid_search.best_score_:.3f}")

# (おまけ) 最終テスト
best_knn = grid_search.best_estimator_
print(f"テストデータでの正解率: {best_knn.score(X_test, y_test):.3f}")
```

**Solution walkthrough**
You've graduated from gut-feel settings! In practice, run `GridSearchCV` on several algorithms, compare fully tuned models, and pick what ships to production.
</details>
