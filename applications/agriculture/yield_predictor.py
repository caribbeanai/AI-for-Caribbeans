"""
Predict yam yield from rainfall, parish, fertiliser, and area planted.
Synthetic data for teaching.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

DATA = Path(__file__).resolve().parents[2] / "datasets" / "yam_yield.csv"


def main():
    df = pd.read_csv(DATA)
    df = pd.get_dummies(df, columns=["parish"], drop_first=True)
    y = df["yield_kg_per_acre"]
    X = df.drop(columns=["yield_kg_per_acre"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = HistGradientBoostingRegressor(max_iter=300, random_state=42).fit(X_train, y_train)
    preds = model.predict(X_test)
    print(f"Test MAE: {mean_absolute_error(y_test, preds):.0f} kg per acre")


if __name__ == "__main__":
    main()
