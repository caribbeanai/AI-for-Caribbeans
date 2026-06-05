"""
Forecast shelter demand given storm category, lead time, and parish exposure.

Author: Adrian Dunkley
"""

from dataclasses import dataclass


@dataclass
class Forecast:
    storm_category: int
    parishes_in_track: int
    coastal_population: int
    lead_time_hours: int


def expected_shelter_demand(f: Forecast) -> int:
    base_rate = {1: 0.005, 2: 0.012, 3: 0.03, 4: 0.06, 5: 0.10}.get(f.storm_category, 0.005)
    lead_factor = 1.0 if f.lead_time_hours >= 48 else 0.7
    parish_factor = 1.0 + 0.05 * max(0, f.parishes_in_track - 1)
    return int(f.coastal_population * base_rate * lead_factor * parish_factor)


if __name__ == "__main__":
    examples = [
        Forecast(3, 4, 350_000, 36),
        Forecast(5, 6, 600_000, 60),
        Forecast(1, 2, 120_000, 24),
    ]
    for e in examples:
        print(f"Cat {e.storm_category}, {e.parishes_in_track} parishes -> {expected_shelter_demand(e):,} people likely seeking shelter")
