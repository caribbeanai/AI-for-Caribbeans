"""
Your first AI script.

We will predict hurricane category from wind speed using a simple rule-based
model, then a tiny learned model. This puts the contrast between rule based
AI and machine learning in your hands.

Author: Adrian Dunkley
"""

from sklearn.tree import DecisionTreeClassifier


def rule_based_category(wind_mph: float) -> int:
    """Saffir-Simpson scale, simplified."""
    if wind_mph < 74:
        return 0
    if wind_mph < 96:
        return 1
    if wind_mph < 111:
        return 2
    if wind_mph < 130:
        return 3
    if wind_mph < 157:
        return 4
    return 5


storms = [
    {"name": "Gilbert 1988 Jamaica", "wind": 175, "cat": 5},
    {"name": "Ivan 2004 Grenada", "wind": 165, "cat": 5},
    {"name": "Tomas 2010 Saint Lucia", "wind": 100, "cat": 2},
    {"name": "Maria 2017 Dominica", "wind": 175, "cat": 5},
    {"name": "Irma 2017 Barbuda", "wind": 180, "cat": 5},
    {"name": "Dorian 2019 Bahamas", "wind": 185, "cat": 5},
    {"name": "Beryl 2024 Carriacou", "wind": 165, "cat": 5},
]

print("Rule based predictions:")
for s in storms:
    print(f"  {s['name']:<35} predicted cat {rule_based_category(s['wind'])}, actual {s['cat']}")

X = [[s["wind"]] for s in storms]
y = [s["cat"] for s in storms]
model = DecisionTreeClassifier(random_state=42).fit(X, y)

print("\nLearned model predictions:")
for s in storms:
    print(f"  {s['name']:<35} predicted cat {model.predict([[s['wind']]])[0]}, actual {s['cat']}")

print("\nTry: model.predict([[90]]) for a storm of 90 mph wind.")
print("Predicted:", model.predict([[90]])[0])
