"""
A tiny RAG demo over Caribbean country facts.
Embeddings are simulated with TF IDF so the script runs without API calls.
Swap in real embeddings for production.

Author: Adrian Dunkley
"""

from pathlib import Path
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA = Path(__file__).resolve().parents[2] / "datasets" / "caribbean_country_facts.json"


def load_chunks():
    raw = json.loads(DATA.read_text())
    chunks = []
    for country, facts in raw.items():
        for fact in facts:
            chunks.append({"country": country, "text": f"{country}: {fact}"})
    return chunks


def retrieve(query, chunks, vec, matrix, k=3):
    q = vec.transform([query])
    sims = cosine_similarity(q, matrix).ravel()
    top = sims.argsort()[::-1][:k]
    return [chunks[i] for i in top]


def main():
    chunks = load_chunks()
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    matrix = vec.fit_transform([c["text"] for c in chunks])

    for q in [
        "Which island is called the Spice Isle?",
        "Where is the Sisserou Parrot from?",
        "What language is spoken in Aruba?",
        "Which Caribbean country has the largest area?",
    ]:
        print(f"\nQ: {q}")
        for c in retrieve(q, chunks, vec, matrix):
            print(f"  - {c['text']}")


if __name__ == "__main__":
    main()
