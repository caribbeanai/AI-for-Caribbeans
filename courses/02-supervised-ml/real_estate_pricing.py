"""
Scenario: price a Caribbean residential listing in its local currency.
Uses datasets/real_estate_listings.csv.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split

DATA = Path(__file__).resolve().parents[2] / "datasets" / "real_estate_listings.csv"


def main():
    df = pd.read_csv(DATA)
    print("Currencies in data:", df["currency"].unique())

    # Train one model per currency to avoid mixing scales.
    for currency, group in df.groupby("currency"):
        group = pd.get_dummies(group, columns=["city", "neighbourhood"], drop_first=True)
        y = group["price_local"]
        X = group.drop(columns=["price_local", "currency"])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = HistGradientBoostingRegressor(max_iter=400, random_state=42).fit(X_train, y_train)
        mape = mean_absolute_percentage_error(y_test, model.predict(X_test))
        print(f"  {currency}: MAPE {mape * 100:.1f}%")


if __name__ == "__main__":
    main()
