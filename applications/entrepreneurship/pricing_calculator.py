"""
Compute a defensible service price for a Caribbean freelancer.
Inputs: target annual income, billable hours, overhead, expected utilisation.

Author: Adrian Dunkley
"""

from dataclasses import dataclass


@dataclass
class PricingInputs:
    target_annual_income_usd: float
    overhead_annual_usd: float
    weeks_worked: int = 46
    hours_per_week: int = 30
    utilisation_pct: float = 0.6


def hourly_rate(p: PricingInputs) -> float:
    billable_hours = p.weeks_worked * p.hours_per_week * p.utilisation_pct
    revenue_needed = p.target_annual_income_usd + p.overhead_annual_usd
    return round(revenue_needed / billable_hours, 2)


def project_price(rate_per_hour: float, hours_estimate: float, buffer_pct: float = 0.25) -> float:
    return round(rate_per_hour * hours_estimate * (1 + buffer_pct), 2)


if __name__ == "__main__":
    inputs = PricingInputs(target_annual_income_usd=36_000, overhead_annual_usd=6_000)
    r = hourly_rate(inputs)
    print(f"Recommended hourly rate: USD {r}")
    print(f"Quote for a 20 hour build: USD {project_price(r, 20)}")
    print(f"Quote for a 60 hour build: USD {project_price(r, 60)}")
