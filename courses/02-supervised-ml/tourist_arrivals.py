"""
Forecast monthly stayover tourist arrivals to Barbados.
Uses datasets/barbados_arrivals.csv. Toy model for teaching.

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
    df["high_season"] = df["month"].isin([12, 1, 2, 3]).astype(int)
    df["lag_1"] = df["arrivals"].shift(1)
    df["lag_12"] = df["arrivals"].shift(12)
    df = df.dropna().reset_index(drop=True)

    split = int(len(df) * 0.8)
    train, test = df.iloc[:split], df.iloc[split:]
    features = ["month", "year", "high_season", "lag_1", "lag_12"]

    model = HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05, random_state=42)
    model.fit(train[features], train["arrivals"])
    preds = model.predict(test[features])
    mape = mean_absolute_percentage_error(test["arrivals"], preds)
    print(f"MAPE on test: {mape * 100:.1f}%")
    print(test[["date", "arrivals"]].assign(pred=preds.round().astype(int)).tail(6).to_string(index=False))


if __name__ == "__main__":
    main()
