"""
Compute a simple bleaching risk score from sea surface temperature anomalies.
Mirrors NOAA Coral Reef Watch's idea, simplified for teaching.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[2] / "datasets" / "sst_anomaly.csv"


def risk(degree_heating_weeks: float) -> str:
    if degree_heating_weeks >= 8:
        return "Alert 2, severe bleaching and mortality likely"
    if degree_heating_weeks >= 4:
        return "Alert 1, significant bleaching likely"
    if degree_heating_weeks >= 1:
        return "Warning, possible bleaching"
    if degree_heating_weeks > 0:
        return "Watch"
    return "No stress"


def main():
    df = pd.read_csv(DATA)
    df["hot_spot"] = (df["sst_anomaly_c"] - 1.0).clip(lower=0)
    df["dhw"] = df.groupby("site")["hot_spot"].transform(
        lambda s: s.rolling(window=12, min_periods=1).sum() / 2
    )
    df["status"] = df["dhw"].apply(risk)
    print(df.tail(10).to_string(index=False))


if __name__ == "__main__":
    main()
