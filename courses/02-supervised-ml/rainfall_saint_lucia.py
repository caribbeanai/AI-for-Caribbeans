"""
Predict monthly rainfall in Saint Lucia from month, year, and mean temperature.
Uses the synthetic dataset at datasets/saint_lucia_rainfall.csv.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

DATA = Path(__file__).resolve().parents[2] / "datasets" / "saint_lucia_rainfall.csv"


def main():
    df = pd.read_csv(DATA)
    df["wet_season"] = df["month"].between(6, 11).astype(int)

    features = ["month", "year", "mean_temp_c", "wet_season"]
    X = df[features]
    y = df["rainfall_mm"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Test MAE: {mae:.1f} mm")

    sample = pd.DataFrame({"month": [9], "year": [2026], "mean_temp_c": [28.4], "wet_season": [1]})
    print(f"September 2026 forecast: {model.predict(sample)[0]:.0f} mm")


if __name__ == "__main__":
    main()
