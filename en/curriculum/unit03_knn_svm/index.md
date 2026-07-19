# Unit 3: K-NN and Support Vector Machines

<p class="unit-hero">
  <img src="/en/assets/units/unit03_knn_svm/images/hero.png" alt="Hero: K-NN neighbor voting and SVM margin boundary" />
</p>

## 1. Understanding K-NN and SVM

This unit covers two famous classifiers with very different philosophies: **K-NN (K-Nearest Neighbors)** and **SVM (Support Vector Machine)**. Both are intuitive and have distinctive strengths.

### What Is K-NN? — "Birds of a Feather Flock Together"
K-NN is sometimes called the **"laziest"** algorithm in machine learning because it does not learn a complex formula upfront — it simply **memorizes past data**.

How does it predict on new data?
By **majority vote among nearby neighbors**: "You're probably the same category as the people closest to you."

#### Analogy: Guessing a Transfer Student's Club
A transfer student arrives (unknown data). Will they join sports or culture club?
K-NN works like this:
1. Find the **K students** (e.g., 3) most similar in hobbies and personality (features).
2. If those three are "sports, sports, culture," predict **sports** by majority vote.

<img src="/en/assets/units/unit03_knn_svm/images/diagram-knn.svg" alt="K=3 nearest neighbors vote for new data point classification" class="unit-diagram" />

| Choice of K (how many neighbors?) | Pros | Cons |
| :--- | :--- | :--- |
| **K too small (e.g., K=1)** | Can draw complex boundaries | Easily fooled by noisy outliers |
| **K too large (e.g., K=100)** | Stable against noise | Ignores fine detail; predictions become coarse |

### What Is SVM? — The Craftsman Who Draws the Widest Road
SVM is a strict, skilled **"boundary drawer."**

When splitting data into two groups (red team vs. blue team), any line is not enough. SVM seeks a boundary **as far as possible from both sides** — the safest dividing line.

#### Analogy: Borders and Margins
Draw a border between red country and blue country.
If the border hugs a red house too closely, small shifts cause misclassification. SVM finds the closest red and blue houses (**support vectors**) and draws the border to maximize the **margin** — the buffer zone between them.

<img src="/en/assets/units/unit03_knn_svm/images/diagram-svm.svg" alt="SVM decision boundary with maximum margin and support vectors" class="unit-diagram" />

SVM also has the **kernel trick**.
When data cannot be separated by a straight line, the kernel "lifts" points into higher dimensions so a plane can slice them apart — enabling complex classification.

### 💡 Real-World Business Use Cases

- **Similar-product recommendations (K-NN)**: Find products with similar price, category, and ratings — "Customers who bought this also viewed…"
- **Visual inspection and anomaly detection (SVM)**: Learn complex boundaries between good and defective products from surface images to automate QC.
- **Clinical decision support (SVM)**: Classify disease status from lab values and vitals with high accuracy to assist physicians.

---

## 2. Implementation Example

We use the famous **Iris dataset** to classify three iris species from sepal and petal measurements. We'll implement both K-NN and SVM and compare them.

<img src="/en/assets/units/unit03_knn_svm/images/diagram-comparison.svg" alt="K-NN vs SVM: lazy memorizer vs optimal boundary finder" class="unit-diagram" />

```python
# Import required libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# 1. Prepare the data
iris = load_iris()
X = iris.data
y = iris.target

# Split into 80% training and 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

**Code walkthrough**
Standard load and split. Four flower features and three species labels.

```python
# 2. Train and predict with K-NN
# K=3: look at the 3 nearest neighbors and vote by majority
knn_model = KNeighborsClassifier(n_neighbors=3)

# Memorize past data (training)
knn_model.fit(X_train, y_train)

# Predict and compute accuracy
knn_pred = knn_model.predict(X_test)
knn_acc = accuracy_score(y_test, knn_pred)

print(f"K-NN accuracy: {knn_acc:.3f}")
```

**Code walkthrough**
`KNeighborsClassifier` with `n_neighbors=3` means "ask three nearest neighbors." For K-NN, `.fit()` mostly stores data in memory rather than computing weights.

```python
# 3. Train and predict with SVM
# kernel='rbf' enables the kernel trick for nonlinear decision boundaries
svm_model = SVC(kernel='rbf', random_state=42)

# Find the widest margin boundary (training)
svm_model.fit(X_train, y_train)

# Predict and compute accuracy
svm_pred = svm_model.predict(X_test)
svm_acc = accuracy_score(y_test, svm_pred)

print(f"SVM accuracy:  {svm_acc:.3f}")
```

**Code walkthrough**
`SVC` (Support Vector Classification) is the SVM class. `kernel='rbf'` is the popular default for nonlinear boundaries. Both algorithms perform very well on this task!

---

## 3. Practice

Build an SVM classifier following the requirements below.

**Requirements**
Use the **Digits dataset** — coarse 8×8 pixel images of handwritten digits 0–9.

1. Load data with `load_digits` from `sklearn.datasets`.
2. Split into 80% training and 20% test.
3. Create and train an `SVC` model.
4. Predict on the test set and print accuracy.

**About scaling:** Because all features here are pixel values with the same unit and range, `StandardScaler` is not essential. If you have time, compare results with and without scaling and consider how the answer would change when features use different units.

**Hints**
- Load with `digits = load_digits()`. Images are already flattened to numeric vectors — use `X = digits.data` as usual.

---

## 4. Answer Key

Write your own code first, then open the answer below to check your work.

<details>
<summary>View sample solution (click to expand)</summary>

```python
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# 1. Load the data
digits = load_digits()
X = digits.data
y = digits.target

# 2. Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Create and train an SVM model
# Use default settings this time
svm_model = SVC(random_state=42)
svm_model.fit(X_train, y_train)

# 4. Predict and evaluate
y_pred = svm_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Handwritten digit recognition (SVM) accuracy: {accuracy:.3f}")
```

**Solution walkthrough**
Even on pixel-style data like handwritten digits, SVM often reaches ~98% accuracy with minimal code — a strong, practical algorithm!
</details>
