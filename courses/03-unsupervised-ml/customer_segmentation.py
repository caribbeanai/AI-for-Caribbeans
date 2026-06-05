"""
Customer segmentation for a Trinidad supermarket chain.
Cluster on monthly spend, visit count, fresh produce share, and average ticket.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DATA = Path(__file__).resolve().parents[2] / "datasets" / "supermarket_customers.csv"


def main():
    df = pd.read_csv(DATA)
    features = ["monthly_spend_ttd", "visits_per_month", "fresh_share", "avg_ticket_ttd"]
    X = StandardScaler().fit_transform(df[features])
    model = KMeans(n_clusters=4, random_state=42, n_init="auto").fit(X)
    df["segment"] = model.labels_
    print(df.groupby("segment")[features].mean().round(2))
    print("\nCounts per segment:")
    print(df["segment"].value_counts().sort_index())


if __name__ == "__main__":
    main()
