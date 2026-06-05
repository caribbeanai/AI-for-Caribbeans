"""
Classify mango variety from physical measurements.
Variety: Julie, East Indian, Bombay, Number Eleven.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

DATA = Path(__file__).resolve().parents[2] / "datasets" / "caribbean_mangoes.csv"


def main():
    df = pd.read_csv(DATA)
    X = df[["length_cm", "width_cm", "weight_g", "sweetness_brix"]]
    y = df["variety"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    model = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)
    preds = model.predict(X_test)
    print(classification_report(y_test, preds))

    sample = pd.DataFrame({
        "length_cm": [7.2], "width_cm": [6.0], "weight_g": [220], "sweetness_brix": [17],
    })
    print("Sample prediction:", model.predict(sample)[0])


if __name__ == "__main__":
    main()
