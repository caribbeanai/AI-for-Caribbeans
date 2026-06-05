"""
Scenario: spot anomalous fishing landings per port and day.
Uses datasets/fishing_landings.csv with IsolationForest.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.ensemble import IsolationForest

DATA = Path(__file__).resolve().parents[2] / "datasets" / "fishing_landings.csv"


def main():
    df = pd.read_csv(DATA)
    agg = df.groupby(["date", "port"]).agg(
        total_kg=("weight_kg", "sum"),
        species_count=("species", "nunique"),
        avg_price=("price_per_kg_usd", "mean"),
    ).reset_index()
    X = agg[["total_kg", "species_count", "avg_price"]]
    flags = IsolationForest(contamination=0.02, random_state=42).fit_predict(X)
    agg["anomaly"] = (flags == -1)
    suspicious = agg[agg["anomaly"]].sort_values("total_kg", ascending=False).head(10)
    print(suspicious.to_string(index=False))


if __name__ == "__main__":
    main()
