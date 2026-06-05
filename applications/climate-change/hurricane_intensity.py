"""
Predict peak wind speed of a tropical cyclone from early track data.
Uses a synthetic dataset to demonstrate the pipeline.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

DATA = Path(__file__).resolve().parents[2] / "datasets" / "atlantic_storms.csv"


def main():
    df = pd.read_csv(DATA)
    features = ["init_wind_mph", "init_pressure_mb", "sst_c", "shear_kt", "lat", "lon"]
    X = df[features]
    y = df["peak_wind_mph"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    print(f"MAE: {mean_absolute_error(y_test, preds):.1f} mph")
    sample = pd.DataFrame({
        "init_wind_mph": [60], "init_pressure_mb": [990], "sst_c": [29.5],
        "shear_kt": [8], "lat": [14.5], "lon": [-58.2],
    })
    print(f"Forecast peak wind: {model.predict(sample)[0]:.0f} mph")


if __name__ == "__main__":
    main()
