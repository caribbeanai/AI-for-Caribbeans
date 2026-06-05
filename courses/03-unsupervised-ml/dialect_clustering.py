"""
Cluster Caribbean dialect phrases by surface form using character n-grams.
A teaching example, not a serious dialectology study.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

DATA = Path(__file__).resolve().parents[2] / "datasets" / "caribbean_dialect_phrases.csv"


def main():
    df = pd.read_csv(DATA)
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=1)
    X = vec.fit_transform(df["phrase"])
    model = KMeans(n_clusters=5, random_state=42, n_init="auto").fit(X)
    df["cluster"] = model.labels_
    for c in sorted(df["cluster"].unique()):
        print(f"\nCluster {c}:")
        for _, row in df[df["cluster"] == c].head(6).iterrows():
            print(f"  [{row['country']}] {row['phrase']}")


if __name__ == "__main__":
    main()
