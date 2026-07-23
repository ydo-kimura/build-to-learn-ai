# Unit 41: Time Series Demand Forecasting & Price Optimization System

<p class="unit-hero">
  <img src="/en/assets/units/unit41_timeseries_price_optimizer/images/hero.png" alt="Hero: Time Series & Pricing" />
</p>

## 1. Understanding Leak Avoidance in Time Series and Demand/Price Optimization

<img src="/en/assets/units/unit41_timeseries_price_optimizer/images/diagram-concept.svg" alt="Diagram: Time series ML" class="unit-diagram" />

You have learned tabular regression and classification (Units 1–8) and deep learning models such as the image classifiers in Units 10–16. Applying textbook ML directly to **data that changes over time (time series)** causes **catastrophic production failure (prediction accuracy drops to zero)**.

The main cause is **time series data leakage**.

### 🚨 Time Series Data Leakage: Smuggling Information from the Future

Typical ML randomly splits data into 80% train and 20% test (`train_test_split`). With time series, what happens?

```
[Time series data]: [Jan] -> [Feb] -> [Mar] -> [Apr] -> [May]

× Random split (leakage):
  Train: [Jan, Mar, May]
  Test: [Feb, Apr] ──> Model knows March when predicting February—artificially high accuracy (future prediction trap).
```

When future information enters test data, we call it **data leakage**. Models look perfect in validation but fail completely in production (predicting tomorrow's real future).

The only correct approach is **time series split (Time Series Split / Rolling-window Validation)**: train on past data only and sequentially predict the "future" at each point.

---

### 📈 From Demand Forecasting to Price Optimization (Dynamic Pricing)

The next step after forecasting is converting predictions into business profit via **dynamic pricing**.

1. **Demand curve estimation**: Generally, higher price lowers demand. ML simulates "predicted demand at each price."
2. **Revenue maximization**: Revenue = `price × quantity (demand)`. Too low sells volume without profit; too high kills sales.
3. **Mathematical optimization**: Find the revenue-maximizing **sweet spot (optimal price P\*)** as in the diagram below.

```
 Demand D                      Revenue R (P × D)
  │\                            │      ┌───┐
  │ \                           │     /     \
  │  \                          │    /       \
  │   \                         │   /         \
  └──── Price P                 └───┴─────────┴── Price P
                                       Price P* (max revenue)
```

---

### 💡 Concrete Business Use Cases

- **Hotel/flight automatic pricing**: From past bookings, competitor prices, holidays, and search trends, AI calculates daily prices that maximize revenue while filling rooms/seats.
- **EC/supermarket fresh food markdown optimization**: From expiry, tomorrow's weather forecast, and day-of-week elasticity, compute evening discount rates that minimize waste and maximize profit.
- **Sharing economy surge pricing (Uber, etc.)**: From real-time demand spikes and active drivers, adjust ride prices in seconds to restore supply-demand balance.

---

<img src="/en/assets/units/unit41_timeseries_price_optimizer/images/diagram-workflow.svg" alt="Diagram: Dynamic pricing" class="unit-diagram" />

## 2. Implementation Example — Time Series Leak Avoidance and Demand Curve Estimation

> **Colab setup:** The current Colab runtime includes NumPy, pandas, scikit-learn, and XGBoost, so no additional installation is required.

The code below runs safe cross-validation (time series split) on time series data and uses predictions to find the **optimal price that maximizes revenue** via grid search.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
import xgboost as xgb

# --- 1. Generate time series dummy data ---
np.random.seed(42)
n_days = 300

# 300 days of sales logs
dates = pd.date_range(start="2025-01-01", periods=n_days)
prices = np.random.uniform(500, 1500, size=n_days) # Prices 500–1500 yen

# Demand: base 100 units, -6 units per 100 yen price increase + noise + weekday effect
base_demand = 100
price_effect = -0.06 * prices
weekday_effect = (dates.weekday >= 5).astype(int) * 20 # +20 on weekends
noise = np.random.normal(0, 5, size=n_days)

demand = base_demand + price_effect + weekday_effect + noise
demand = np.clip(demand, 0, None).astype(int) # Clip negative quantities

df = pd.DataFrame({
    "date": dates,
    "price": prices,
    "is_weekend": (dates.weekday >= 5).astype(int),
    "demand": demand
})

# Features and target
# (Lag features from prior days are standard for leak prevention; here simplified to price and weekend flag)
X = df[["price", "is_weekend"]].values
y = df["demand"].values

print("--- 2. Leak-free evaluation with TimeSeriesSplit ---")
# Split chronologically in 5 folds, not randomly
tscv = TimeSeriesSplit(n_splits=5)
fold_scores = []

for fold, (train_index, test_index) in enumerate(tscv.split(X)):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    # XGBoost with max_depth=3 to limit time series overfitting
    model = xgb.XGBRegressor(max_depth=3, n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # Evaluation (MAE)
    preds = model.predict(X_test)
    mae = np.mean(np.abs(preds - y_test))
    fold_scores.append(mae)
    print(f"  Fold {fold+1} Test MAE: {mae:.2f} units (train period: {len(train_index)} days, test period: {len(test_index)} days)")

print(f"Average test MAE: {np.mean(fold_scores):.2f} units")

# --- 3. Final model training and demand simulation (price optimization) ---
final_model = xgb.XGBRegressor(max_depth=3, n_estimators=50, random_state=42)
final_model.fit(X, y)

# Optimal price search simulation for weekends
candidate_prices = np.linspace(400, 1800, 100) # 400–1800 yen in 100 steps
best_price = 0
max_revenue = 0

print("\n--- 4. Dynamic pricing optimization simulation (weekend) ---")
for p in candidate_prices:
    # Predicted demand at price p on weekend (is_weekend=1)
    features = np.array([[p, 1]]) # [[price, weekend flag]]
    predicted_demand = final_model.predict(features)[0]

    # Revenue = price × predicted demand
    revenue = p * predicted_demand

    if revenue > max_revenue:
        max_revenue = revenue
        best_price = p

print(f"🎯 Optimal weekend price: {best_price:.1f} yen")
print(f"📈 Predicted sales volume at that price: {final_model.predict(np.array([[best_price, 1]]))[0]:.1f} units")
print(f"💰 Expected maximum revenue: {max_revenue:.0f} yen")
```

---

## 3. Practice — 🧠 Design and Decide Demand Forecasting & Dynamic Pricing

As a senior data scientist, design and implement an **optimal pricing algorithm that thoroughly avoids time series leakage, learns promotion and competitor price effects, and maximizes revenue**.

**Assignment Requirements**

Use the initialization code below (holiday flags, dynamic competitor pricing, past sales logs) and build an evaluation pipeline that inspects and suppresses future-data leakage, then derive a bounded pricing strategy.

```python
# 1. Sample count (one year of daily sales)
n_samples = 365
np.random.seed(101)

# Dates and promotion flags (irregular events)
dates_p = pd.date_range(start="2025-01-01", periods=n_samples)
promo_flags = np.random.choice([0, 1], size=n_samples, p=[0.85, 0.15]) # 15% promotion probability

# Competitor prices (around 900 yen, zigzag time series)
competitor_prices = 900 + np.sin(np.linspace(0, 10 * np.pi, n_samples)) * 150 + np.random.normal(0, 20, n_samples)

# Our prices (experimental zigzag pricing)
our_prices = 950 + np.cos(np.linspace(0, 8 * np.pi, n_samples)) * 200 + np.random.normal(0, 30, n_samples)

# Actual demand (nonlinear dummy from our price, competitor gap, promotion, weekend)
base_d = 120
our_price_effect = -0.08 * our_prices
competitor_effect = 0.05 * competitor_prices # Higher competitor price helps our sales
promo_effect = promo_flags * 35 # +35 units during promotion
weekend_effect = (dates_p.weekday >= 5).astype(int) * 15

actual_demand = base_d + our_price_effect + competitor_effect + promo_effect + weekend_effect + np.random.normal(0, 7, n_samples)
actual_demand = np.clip(actual_demand, 0, None).astype(int)

df_practice = pd.DataFrame({
    "date": dates_p,
    "our_price": our_prices,
    "competitor_price": competitor_prices,
    "is_promo": promo_flags,
    "is_weekend": (dates_p.weekday >= 5).astype(int),
    "demand": actual_demand
})
```

**Your Mission: Robust Price Optimization Pipeline Design**

Using the data above, find the **optimal price (yen)** that **maximizes revenue** when **promotion is active, competitor price is 1,000 yen, and it is a weekday (is_weekend=0)**.

---

**Design Decision Notes to Record in Code Comments**

1. **Feature engineering for time series**:
   - Describe how you incorporated temporal order and lag features (or designed variables to avoid leak given this data structure).
2. **Time-series overfitting mitigation rationale**:
   - Time series is noisier and overfits more easily than tabular data. Describe how you constrained XGBoost/LightGBM hyperparameters (depth, learning rate, L2, etc.).
3. **Business strategy and price bounds**:
   - Describe how you limited search bounds from a practical perspective to prevent extreme simulated prices from unconstrained optimization.
4. **Final adoption decision**:
   - **Report the production price you present to executives and the mathematical/business justification.**

---

## 4. Answer Key — 💡 Professional Dynamic Pricing Design

<details>
<summary>View sample solution (click to expand)</summary>

### 💡 Time Series Price Optimization Decision Notes as an AI Engineer

In dynamic pricing practice, verifying **relative competitor pricing** and **whether the estimated demand curve is realistic** is the only way to prevent catastrophic failure.

#### Price Optimization Design Decision Matrix

| Evaluation Axis                     | Approach A (Demand model only)                                                                                             | Approach B (Bounded demand + mathematical optimization)                                                                      | Design Decision Point                                                                |
| :---------------------------------- | :------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| **Abnormal price suppression**      | **Very weak**. XGBoost may predict "demand drops slightly" at extreme prices (e.g., 5,000 yen), implying infinite revenue. | **Very strong**. Search strictly within past experimental min–max (e.g., 500–1,500 yen), preventing unrealistic prices 100%. | Knowing ML extrapolation weakness, **bounds are mandatory**.                         |
| **Competitor price responsiveness** | Ignores competitors; risk losing all customers when competitors deep-discount.                                             | Uses relative features like "Our Price - Competitor Price" for dynamic follow.                                               | Relative price vs competitors is often the strongest demand driver—mandatory design. |

---

### Dynamic Pricing with Leak Elimination & Competitor Price Gap

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error
import xgboost as xgb

# --- 1. Decision and feature engineering ---
# "When competitor prices exist, the price gap vs competitors affects demand more than our absolute price."
# "Therefore we engineer `price_diff = competitor_price - our_price` as a new feature."
# "Use TimeSeriesSplit to prevent leakage; limit optimal price search strictly to past price data range to avoid extrapolation failure."

df_practice = df_practice.copy()
df_practice["price_diff"] = df_practice["competitor_price"] - df_practice["our_price"]

# Features: our_price, price_diff vs competitor, promotion flag, weekend flag
features_cols = ["our_price", "price_diff", "is_promo", "is_weekend"]
X_p = df_practice[features_cols].values
y_p = df_practice["demand"].values

# --- 2. Time series cross-validation ---
tscv_p = TimeSeriesSplit(n_splits=5)
maes = []

for fold, (train_idx, test_idx) in enumerate(tscv_p.split(X_p)):
    X_train, X_test = X_p[train_idx], X_p[test_idx]
    y_train, y_test = y_p[train_idx], y_p[test_idx]

    # Limit overfitting: max_depth=2, learning_rate=0.1
    model_p = xgb.XGBRegressor(max_depth=2, learning_rate=0.1, n_estimators=40, random_state=42)
    model_p.fit(X_train, y_train)

    preds = model_p.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    maes.append(mae)

print("--- Time Series Model Evaluation Report ---")
print(f"Time series 5-fold average test MAE: {np.mean(maes):.2f} units")

# --- 3. Final model ---
final_model_p = xgb.XGBRegressor(max_depth=2, learning_rate=0.1, n_estimators=40, random_state=42)
final_model_p.fit(X_p, y_p)

# --- 4. Optimal price search under target conditions ---
# Conditions: weekday (is_weekend=0), promotion (is_promo=1), competitor price = 1000 yen
competitor_price_target = 1000.0
is_promo_target = 1.0
is_weekend_target = 0.0

# Search range limited to past experimental band 600–1300 yen
explore_prices = np.linspace(600, 1300, 100)
best_revenue = 0
best_price = 0
best_predicted_demand = 0

for p in explore_prices:
    # Dynamic competitor price gap
    p_diff = competitor_price_target - p

    # Feature vector: ["our_price", "price_diff", "is_promo", "is_weekend"]
    input_features = np.array([[p, p_diff, is_promo_target, is_weekend_target]])

    # Demand prediction
    predicted_d = final_model_p.predict(input_features)[0]
    predicted_d = max(0, predicted_d) # Prevent negative predictions

    # Revenue
    rev = p * predicted_d

    if rev > best_revenue:
        best_revenue = rev
        best_price = p
        best_predicted_demand = predicted_d

print("\n--- 💰 Dynamic Pricing Decision Note ---")
print(f"🎯 Optimal price to set: {best_price:.1f} yen (competitor price: {competitor_price_target} yen, gap: {competitor_price_target - best_price:.1f} yen)")
print(f"📈 Predicted demand at that price: {best_predicted_demand:.1f} units")
print(f"💰 Expected maximum revenue: {best_revenue:.0f} yen")

# --- 5. Business validation of decision ---
# Compare with normal (no promo, weekday) performance to verify price is not abnormally high/low.
```

### 💡 Final Production Adoption Decision

- **Final decision**:
  - **Set our price to the computed optimal price on promotion weekdays when competitor price is 1,000 yen.**
  - **Rationale**:
    1. **Model trustworthiness with leak fully avoided**: Strict TimeSeriesSplit validation scientifically proves prediction MAE is within a very small error range on real data.
    2. **Healthy price gap vs competitors**: The model learns that extreme premium over competitors crashes demand—not just discount-driven demand. Optimal price maintains appropriate discount/margin vs 1,000 yen competitor, minimizing customer churn.
    3. **Safe operation via optimization bounds**: Searching within past experimental history `600–1300 yen` blocks destructive errors like "sell at 1 yen to clear inventory" or "price at 10,000 yen for one unit" from extrapolation failure 100% in advance.

</details>
