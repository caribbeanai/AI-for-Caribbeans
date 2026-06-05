"""
Kids mango sorter.
A first AI program. We teach the computer the difference between
two mango types using two numbers: length in cm, and roundness from 0 to 1.
Run it, then change the numbers at the bottom and see what happens.

Author: Adrian Dunkley
"""

from dataclasses import dataclass


@dataclass
class Mango:
    length_cm: float
    roundness: float
    name: str


training_mangoes = [
    Mango(7.0, 0.9, "Julie"),
    Mango(7.5, 0.88, "Julie"),
    Mango(6.5, 0.92, "Julie"),
    Mango(7.2, 0.9, "Julie"),
    Mango(12.0, 0.4, "East Indian"),
    Mango(13.5, 0.35, "East Indian"),
    Mango(12.5, 0.42, "East Indian"),
    Mango(14.0, 0.38, "East Indian"),
]


def distance(a, b):
    return ((a.length_cm - b.length_cm) ** 2 + (a.roundness - b.roundness) ** 2) ** 0.5


def guess(unknown_mango):
    closest = min(training_mangoes, key=lambda m: distance(m, unknown_mango))
    return closest.name


if __name__ == "__main__":
    mystery_one = Mango(length_cm=7.1, roundness=0.91, name="?")
    mystery_two = Mango(length_cm=13.0, roundness=0.4, name="?")

    print("Mango one looks like a:", guess(mystery_one))
    print("Mango two looks like a:", guess(mystery_two))
    print()
    print("Change the numbers above and run again. Try length 10 with roundness 0.6.")
