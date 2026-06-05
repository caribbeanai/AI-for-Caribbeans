"""
Detect unusual spikes in Coronation Market produce prices.
Uses simple z-score on a rolling window.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[2] / "datasets" / "market_prices_weekly.csv"


def main():
    df = pd.read_csv(DATA)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["item", "date"]).reset_index(drop=True)
    df["rolling_mean"] = df.groupby("item")["price_jmd_per_lb"].transform(lambda s: s.rolling(8, min_periods=4).mean())
    df["rolling_std"] = df.groupby("item")["price_jmd_per_lb"].transform(lambda s: s.rolling(8, min_periods=4).std())
    df["z"] = (df["price_jmd_per_lb"] - df["rolling_mean"]) / df["rolling_std"]
    alerts = df[df["z"].abs() > 2].dropna()
    print(f"{len(alerts)} unusual price events detected")
    print(alerts.tail(10).to_string(index=False))


if __name__ == "__main__":
    main()
