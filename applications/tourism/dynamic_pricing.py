"""
A first cut dynamic pricing model. Maps demand signal to a recommended rate
within a min and max floor.

Author: Adrian Dunkley
"""

from dataclasses import dataclass


@dataclass
class PricingInputs:
    base_rate_usd: float
    occupancy_30d_pct: float
    pace_vs_last_year_pct: float
    days_to_arrival: int
    is_high_season: bool


def recommend_rate(p: PricingInputs) -> float:
    rate = p.base_rate_usd
    rate *= 1 + (p.occupancy_30d_pct - 60) * 0.005
    rate *= 1 + p.pace_vs_last_year_pct * 0.003
    if p.is_high_season:
        rate *= 1.10
    if p.days_to_arrival <= 7:
        rate *= 0.95
    elif p.days_to_arrival >= 60:
        rate *= 1.05
    floor = p.base_rate_usd * 0.75
    ceiling = p.base_rate_usd * 1.6
    return max(floor, min(ceiling, round(rate, 2)))


if __name__ == "__main__":
    cases = [
        PricingInputs(220, 85, 12, 30, True),
        PricingInputs(220, 45, -5, 5, False),
        PricingInputs(220, 70, 0, 90, True),
    ]
    for c in cases:
        print(f"{c} -> recommended USD {recommend_rate(c)}")
