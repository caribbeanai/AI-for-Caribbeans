"""
Dengue case early warning from rainfall and prior case count.
Tiny synthetic dataset, illustrates the modelling pattern.

Author: Adrian Dunkley
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


def synth(rng=None):
    rng = rng or np.random.default_rng(7)
    n = 240
    month = np.tile(np.arange(1, 13), n // 12)
    rainfall = 80 + 60 * (np.sin(2 * np.pi * (month - 5) / 12)) + rng.normal(0, 20, n)
    lag1 = np.r_[5, rng.integers(0, 30, n - 1)]
    cases = (0.4 * rainfall + 1.6 * lag1 + rng.normal(0, 6, n)).clip(min=0).astype(int)
    return pd.DataFrame({"month": month, "rainfall_mm": rainfall, "lag1_cases": lag1, "cases": cases})


def main():
    df = synth()
    X = df[["month", "rainfall_mm", "lag1_cases"]]
    y = df["cases"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = HistGradientBoostingRegressor(max_iter=300, random_state=42).fit(X_train, y_train)
    preds = model.predict(X_test)
    print(f"MAE: {mean_absolute_error(y_test, preds):.1f} cases per district month")


if __name__ == "__main__":
    main()
