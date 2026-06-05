"""
Type 2 diabetes risk screening, simplified.
This is a teaching example. Do not use to make medical decisions.

Author: Adrian Dunkley
"""

from dataclasses import dataclass


@dataclass
class Profile:
    age: int
    bmi: float
    waist_cm: float
    family_history: bool
    activity_minutes_per_week: int
    sweet_drinks_per_day: int


def score(p: Profile) -> int:
    s = 0
    if p.age >= 45: s += 2
    if p.age >= 60: s += 1
    if p.bmi >= 25: s += 2
    if p.bmi >= 30: s += 2
    if p.waist_cm >= 94: s += 1
    if p.waist_cm >= 102: s += 1
    if p.family_history: s += 3
    if p.activity_minutes_per_week < 150: s += 2
    if p.sweet_drinks_per_day >= 1: s += 1
    if p.sweet_drinks_per_day >= 3: s += 2
    return s


def band(score_value: int) -> str:
    if score_value <= 3: return "Low risk"
    if score_value <= 7: return "Moderate risk, consider lifestyle changes"
    if score_value <= 11: return "High risk, see a doctor for a fasting blood test"
    return "Very high risk, please see a doctor soon"


if __name__ == "__main__":
    profile = Profile(age=52, bmi=29.4, waist_cm=98, family_history=True,
                      activity_minutes_per_week=60, sweet_drinks_per_day=2)
    s = score(profile)
    print(f"Risk score: {s}")
    print(band(s))
    print("This is an educational tool. Speak with a doctor for any health decision.")
