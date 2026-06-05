"""
Tiny rule based spending categoriser, with hooks to plug in an LLM for harder cases.

Author: Adrian Dunkley
"""

from dataclasses import dataclass


RULES = {
    "food": ["supermarket", "hi-lo", "massy", "loshusan", "pricesmart", "shoppers fair", "kfc", "juici", "popeyes"],
    "transport": ["jpsco", "uber", "jus drive", "taxi", "gas", "petrojam", "rubis", "esso", "shell"],
    "utilities": ["jps", "nwc", "flow", "digicel", "lime", "lucelec", "wasa"],
    "housing": ["rent", "mortgage", "ncb mortgage"],
    "entertainment": ["netflix", "spotify", "cinema", "palace amusement"],
    "health": ["pharmacy", "fontana", "andrew's", "drug store", "doctor"],
    "school": ["school fees", "books", "stationery", "uniform"],
}


@dataclass
class Txn:
    description: str
    amount: float
    currency: str


def categorise(t: Txn) -> str:
    text = t.description.lower()
    for cat, keywords in RULES.items():
        if any(k in text for k in keywords):
            return cat
    return "other"


def summary(transactions):
    totals = {}
    for t in transactions:
        cat = categorise(t)
        totals[cat] = totals.get(cat, 0) + t.amount
    return totals


if __name__ == "__main__":
    txns = [
        Txn("HI-LO Sovereign", 9500, "JMD"),
        Txn("JPS December", 7800, "JMD"),
        Txn("Flow internet", 4500, "JMD"),
        Txn("Uber Half Way Tree", 1200, "JMD"),
        Txn("Fontana Pharmacy", 3200, "JMD"),
        Txn("Netflix", 1800, "JMD"),
        Txn("Rent New Kingston", 95000, "JMD"),
    ]
    for cat, total in sorted(summary(txns).items(), key=lambda kv: -kv[1]):
        print(f"{cat:14} JMD {total:>10,.0f}")
