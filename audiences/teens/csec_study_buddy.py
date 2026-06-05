"""
CSEC study buddy. A tiny offline quiz that drills you on Caribbean History,
Social Studies, and Mathematics. Extend it with your own subjects.

Author: Adrian Dunkley
"""

import random

questions = [
    ("Who led the Morant Bay Rebellion in 1865?", "paul bogle"),
    ("In which year did Jamaica gain independence?", "1962"),
    ("Name the two main islands that form Trinidad and Tobago.", "trinidad and tobago"),
    ("What is the capital of Saint Vincent and the Grenadines?", "kingstown"),
    ("Solve: 12% of 250.", "30"),
    ("Which Caribbean island is known as Spice Isle?", "grenada"),
    ("Who was the first prime minister of Barbados?", "errol barrow"),
    ("What currency does the Eastern Caribbean share?", "eastern caribbean dollar"),
]

random.shuffle(questions)
score = 0
for q, a in questions:
    user = input(f"Q: {q}\n> ").strip().lower()
    if user == a:
        print("Correct.\n")
        score += 1
    else:
        print(f"Answer was: {a}\n")
print(f"Final score: {score} / {len(questions)}")
