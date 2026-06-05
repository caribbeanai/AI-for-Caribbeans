"""
A simple monthly stayover arrivals forecast for a Caribbean destination.
Uses seasonal lags. Reuses the Barbados dataset for demonstration.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_percentage_error

DATA = Path(__file__).resolve().parents[2] / "datasets" / "barbados_arrivals.csv"


def main():
    df = pd.read_csv(DATA).sort_values("date").reset_index(drop=True)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["lag_1"] = df["arrivals"].shift(1)
    df["lag_12"] = df["arrivals"].shift(12)
    df = df.dropna().reset_index(drop=True)
    split = int(len(df) * 0.8)
    train, test = df.iloc[:split], df.iloc[split:]
    features = ["month", "year", "lag_1", "lag_12"]
    model = HistGradientBoostingRegressor(max_iter=400, random_state=42).fit(train[features], train["arrivals"])
    preds = model.predict(test[features])
    print(f"MAPE: {mean_absolute_percentage_error(test['arrivals'], preds) * 100:.2f}%")


if __name__ == "__main__":
    main()
