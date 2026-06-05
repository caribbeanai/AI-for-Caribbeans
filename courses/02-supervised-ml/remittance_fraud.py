"""
Detect suspicious remittance transactions.
Toy synthetic dataset, never use this on real customer data without permission.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

DATA = Path(__file__).resolve().parents[2] / "datasets" / "remittance_transactions.csv"


def main():
    df = pd.read_csv(DATA)
    feature_cols = ["amount_usd", "sender_country_risk", "receiver_account_age_days",
                    "hour_of_day", "channel_atm", "channel_branch", "channel_online"]
    X = df[feature_cols]
    y = df["is_suspicious"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = GradientBoostingClassifier(random_state=42).fit(X_train, y_train)
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    print(classification_report(y_test, preds))
    print(f"ROC AUC: {roc_auc_score(y_test, probs):.3f}")


if __name__ == "__main__":
    main()
