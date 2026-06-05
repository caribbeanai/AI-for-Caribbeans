"""
Aspect plus sentiment tagging for tourism reviews using simple keyword rules.
For production swap rules for a fine tuned classifier or an LLM with structured output.

Author: Adrian Dunkley
"""

from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[2] / "datasets" / "tourism_reviews.csv"

ASPECTS = {
    "food": ["food", "breakfast", "dinner", "menu", "chef", "buffet", "bar"],
    "service": ["staff", "service", "front desk", "receptionist", "concierge"],
    "rooms": ["room", "bed", "shower", "bathroom", "ac", "balcony"],
    "location": ["beach", "location", "pool", "view", "town"],
    "value": ["price", "value", "money", "expensive", "cheap", "deal"],
}

POSITIVE = {"great", "excellent", "amazing", "wonderful", "good", "lovely", "perfect", "friendly", "clean"}
NEGATIVE = {"bad", "poor", "terrible", "rude", "dirty", "slow", "broken", "noisy", "overpriced"}


def label(review):
    text = review.lower()
    pos = sum(1 for w in POSITIVE if w in text)
    neg = sum(1 for w in NEGATIVE if w in text)
    sentiment = "positive" if pos > neg else "negative" if neg > pos else "neutral"
    aspects = [a for a, kws in ASPECTS.items() if any(k in text for k in kws)] or ["overall"]
    return sentiment, aspects


def main():
    df = pd.read_csv(DATA)
    rows = []
    for _, row in df.iterrows():
        sentiment, aspects = label(row["review"])
        for a in aspects:
            rows.append({"aspect": a, "sentiment": sentiment})
    summary = pd.DataFrame(rows).value_counts().unstack(fill_value=0)
    print(summary)


if __name__ == "__main__":
    main()
