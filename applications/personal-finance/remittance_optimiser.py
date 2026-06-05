"""
Pick the lowest cost channel for a USD to local currency remittance.
Toy rates, do not use for actual transfers without verifying.

Author: Adrian Dunkley
"""

from dataclasses import dataclass


@dataclass
class Channel:
    name: str
    fixed_fee_usd: float
    percent_fee: float
    rate_vs_mid: float


CHANNELS = [
    Channel("Bank wire", 25.0, 0.0, 0.965),
    Channel("Western Union cash pickup", 8.0, 0.012, 0.972),
    Channel("MoneyGram online", 5.0, 0.010, 0.973),
    Channel("Wise", 0.0, 0.008, 0.995),
    Channel("Remitly economy", 2.99, 0.004, 0.988),
]


def cost(amount_usd: float, mid_rate: float, channel: Channel) -> dict:
    received_local = amount_usd * mid_rate * channel.rate_vs_mid - channel.fixed_fee_usd * mid_rate
    effective_fee_usd = amount_usd - received_local / mid_rate
    return {
        "channel": channel.name,
        "received_local": round(received_local, 2),
        "effective_fee_usd": round(effective_fee_usd, 2),
    }


def main():
    amount_usd = 500
    jmd_mid = 156.0
    print(f"Sending USD {amount_usd} at mid rate {jmd_mid} JMD/USD\n")
    results = sorted(
        (cost(amount_usd, jmd_mid, c) for c in CHANNELS),
        key=lambda r: -r["received_local"],
    )
    for r in results:
        print(f"{r['channel']:30} receives JMD {r['received_local']:>10,.2f}  (fee USD {r['effective_fee_usd']:.2f})")


if __name__ == "__main__":
    main()
