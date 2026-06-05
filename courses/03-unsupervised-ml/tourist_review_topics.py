"""
Find topics in a small set of Caribbean tourism reviews.
Uses TF IDF plus k-means for portability without heavy dependencies.
For better results swap in sentence-transformers and HDBSCAN.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

DATA = Path(__file__).resolve().parents[2] / "datasets" / "tourism_reviews.csv"


def top_terms(vectoriser, model, n=6):
    terms = vectoriser.get_feature_names_out()
    for i, centre in enumerate(model.cluster_centers_):
        idx = centre.argsort()[::-1][:n]
        print(f"Cluster {i}:", ", ".join(terms[j] for j in idx))


def main():
    df = pd.read_csv(DATA)
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2)
    X = vec.fit_transform(df["review"])
    model = KMeans(n_clusters=5, random_state=42, n_init="auto").fit(X)
    df["cluster"] = model.labels_
    top_terms(vec, model)
    print("\nExample by cluster:")
    for c in sorted(df["cluster"].unique()):
        sample = df[df["cluster"] == c]["review"].iloc[0]
        print(f"  [{c}] {sample[:120]}")


if __name__ == "__main__":
    main()
