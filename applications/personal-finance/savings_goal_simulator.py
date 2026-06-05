"""
Savings goal simulator. How long to a goal at a given monthly amount and interest.

Author: Adrian Dunkley
"""


def months_to_goal(goal: float, monthly: float, annual_rate: float = 0.04) -> int:
    if monthly <= 0:
        return -1
    r = annual_rate / 12
    balance = 0.0
    months = 0
    while balance < goal and months < 600:
        balance = balance * (1 + r) + monthly
        months += 1
    return months


if __name__ == "__main__":
    scenarios = [
        ("Down payment, 2BR apartment, New Kingston", 4_000_000, 35_000, 0.05),
        ("Emergency fund, six months expenses", 600_000, 25_000, 0.04),
        ("Children school fees, prep school in Bridgetown", 30_000, 1_500, 0.03),
        ("Family trip to Curaçao", 250_000, 20_000, 0.03),
    ]
    for label, goal, monthly, rate in scenarios:
        m = months_to_goal(goal, monthly, rate)
        years = m / 12
        print(f"{label}\n  Goal: {goal:,.0f}  Monthly: {monthly:,.0f}  Rate: {rate*100:.1f}%  Time: {m} months (~{years:.1f} years)\n")
