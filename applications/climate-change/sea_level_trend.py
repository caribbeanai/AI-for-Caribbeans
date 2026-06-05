"""
Sea level trend at a Caribbean tide station, simple linear plus seasonal model.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

DATA = Path(__file__).resolve().parents[2] / "datasets" / "sea_level_monthly.csv"


def main():
    df = pd.read_csv(DATA)
    df["t"] = (df["year"] - df["year"].min()) * 12 + df["month"]
    df["sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["cos"] = np.cos(2 * np.pi * df["month"] / 12)
    model = LinearRegression().fit(df[["t", "sin", "cos"]], df["level_mm"])
    rate_mm_per_year = model.coef_[0] * 12
    print(f"Estimated sea level rise: {rate_mm_per_year:.2f} mm per year")
    print(f"Over 30 years: about {rate_mm_per_year * 30:.0f} mm")


if __name__ == "__main__":
    main()
