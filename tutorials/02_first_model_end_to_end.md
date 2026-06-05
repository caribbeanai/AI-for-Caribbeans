# Tutorial 2, Build your first model end to end

Predict Saint Lucia rainfall. We will go through the steps a real data scientist takes.

## Step 1, look at the data

```python
import pandas as pd
df = pd.read_csv("datasets/saint_lucia_rainfall.csv")
print(df.head())
print(df.describe())
```

You should see month, year, mean temperature, and rainfall in millimetres.

## Step 2, plot it

```python
import matplotlib.pyplot as plt
df.groupby("month")["rainfall_mm"].mean().plot(kind="bar")
plt.title("Average monthly rainfall, Saint Lucia")
plt.xlabel("Month")
plt.ylabel("mm")
plt.show()
```

You will see a wet season pattern. June to November is wet.

## Step 3, engineer a feature

```python
df["wet_season"] = df["month"].between(6, 11).astype(int)
```

## Step 4, split

```python
from sklearn.model_selection import train_test_split
X = df[["month", "year", "mean_temp_c", "wet_season"]]
y = df["rainfall_mm"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

## Step 5, train

```python
from sklearn.ensemble import HistGradientBoostingRegressor
model = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, random_state=42)
model.fit(X_train, y_train)
```

## Step 6, evaluate

```python
from sklearn.metrics import mean_absolute_error
preds = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, preds):.1f} mm")
```

## Step 7, predict next September

```python
sample = pd.DataFrame({"month": [9], "year": [2026], "mean_temp_c": [28.4], "wet_season": [1]})
print(model.predict(sample)[0])
```

## What you learned

- Load, look, plot, split, train, evaluate, predict.
- The same shape applies to nearly every supervised ML problem.

The full script is at `courses/02-supervised-ml/rainfall_saint_lucia.py`.
