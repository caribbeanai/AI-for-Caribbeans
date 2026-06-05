"""
Scenario: predict whether a Caribbean hotel booking will be cancelled.
Uses the synthetic dataset at datasets/hotel_bookings_caribbean.csv.

Run:
  python courses/02-supervised-ml/hotel_cancellation.py

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

DATA = Path(__file__).resolve().parents[2] / "datasets" / "hotel_bookings_caribbean.csv"


def main():
    df = pd.read_csv(DATA)
    df = pd.get_dummies(df, columns=["destination", "channel"], drop_first=True)
    y = df["is_cancelled"]
    X = df.drop(columns=["is_cancelled"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = HistGradientBoostingClassifier(max_iter=400, random_state=42).fit(X_train, y_train)
    probs = model.predict_proba(X_test)[:, 1]
    print(f"ROC AUC: {roc_auc_score(y_test, probs):.3f}")
    print(classification_report(y_test, model.predict(X_test)))


if __name__ == "__main__":
    main()
